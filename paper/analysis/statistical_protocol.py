#!/usr/bin/env python3
"""Statistical analysis for the corrected V12 diversity comparison.

This script intentionally reads only .build/diversity_comparison_1821_v12_corrected
and the in-run V12 case base copied beside PredictMaint_myCBR.prj. It does not
read unique_full/V21 outputs and does not modify manuscript/source files.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from scipy.stats import binomtest, rankdata, wilcoxon

# statistical_analysis_outputs -> run dir -> .build -> repo root
ROOT = Path(__file__).resolve().parents[2]
RUN_DIR = ROOT / ".build" / "diversity_comparison_1821_v12_corrected"
OUT_DIR = RUN_DIR / "statistical_analysis_outputs"
CBR_DATA_DIR = RUN_DIR / "cbr_data"
DIVERSE_DIR = RUN_DIR / "with_diversity"
CASEBASE_CSV = CBR_DATA_DIR / "CleanedDATA V12-05-2021.csv"
DIVERSITY_DIR = ROOT / "external" / "Diversity-Improvement-in-CBR"
BOOTSTRAP_SEED = 20260727
BOOTSTRAP_RESAMPLES = 20_000
TOP_K = 5
LAMBDA_MAIN = 0.70
SENSITIVITY_LAMBDAS = [0.5, 0.6, 0.7, 0.8, 0.9]
EPS = 1e-12

sys.path.insert(0, str(ROOT))
import pipeline.diversity_rerank as diversity_rerank_module  # noqa: E402
from pipeline.diversity_rerank import (  # noqa: E402
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_casebase,
    load_taxonomy_tree,
    normalize_text,
    parse_float,
    read_csv_rows,
    rerank_mmr,
)

_original_solution_similarity = diversity_rerank_module.solution_similarity
_solution_similarity_cache: dict[tuple[str, str], float] = {}


def cached_solution_similarity(
    row_a: dict[str, str],
    row_b: dict[str, str],
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
    weights: tuple[float, float, float, float],
) -> float:
    """Cache the pipeline similarity by V12 reference pair for speed.

    The corrected experiment uses a fixed V12 case base and fixed solution weights;
    rows with the same references have the same solution fields for the MMR/ILD
    function, so this preserves the exact pipeline calculation while avoiding
    repeated Levenshtein/taxonomy work.
    """
    ref_a = (row_a.get("Reference") or "").strip()
    ref_b = (row_b.get("Reference") or "").strip()
    key = (ref_a, ref_b) if ref_a <= ref_b else (ref_b, ref_a)
    if key not in _solution_similarity_cache:
        _solution_similarity_cache[key] = _original_solution_similarity(row_a, row_b, casebase_by_ref, taxonomy_index, weights)
    return _solution_similarity_cache[key]


# rerank_mmr resolves solution_similarity in the pipeline module global namespace.
diversity_rerank_module.solution_similarity = cached_solution_similarity
solution_similarity = cached_solution_similarity


@dataclass(frozen=True)
class MetricSpec:
    metric_id: str
    metric_es: str
    baseline_col: str
    diverse_col: str
    family_es: str
    higher_is_better: bool = True


METRICS = [
    MetricSpec(
        "top_similarity",
        "similitud algorítmica del primer resultado",
        "baseline_top_similarity",
        "diverse_top_similarity",
        "relevancia algorítmica",
    ),
    MetricSpec(
        "mean_similarity_top5",
        "similitud algorítmica media del top-5",
        "baseline_mean_similarity",
        "diverse_mean_similarity",
        "relevancia algorítmica",
    ),
    MetricSpec(
        "unique_models_top5",
        "modelos únicos en el top-5",
        "baseline_unique_models",
        "diverse_unique_models",
        "diversidad algorítmica",
    ),
    MetricSpec(
        "intra_list_dissimilarity",
        "disimilitud intra-lista (ILD) algorítmica",
        "baseline_intra_list_dissimilarity",
        "diverse_intra_list_dissimilarity",
        "diversidad algorítmica",
    ),
]


def fmt_p(value: Any) -> str:
    if value is None:
        return ""
    try:
        p = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(p):
        return ""
    if p == 0.0:
        return "<1e-300"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def fmt_num(value: Any, digits: int = 4) -> str:
    if value is None:
        return ""
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(x):
        return ""
    return f"{x:.{digits}f}"


def fmt_pct(value: Any, digits: int = 2) -> str:
    if value is None:
        return ""
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(x):
        return ""
    return f"{x:.{digits}f}%"


def refs_signature(rows: list[dict[str, str]]) -> str:
    return ",".join((row.get("Reference") or "").strip() for row in rows)


def result_metrics_from_rows(
    rows: list[dict[str, str]],
    *,
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
) -> dict[str, Any]:
    rows = rows[:TOP_K]
    references = [(row.get("Reference") or "").strip() for row in rows]
    similarities = [parse_float(row.get("Sim"), default=0.0) for row in rows]
    models = [normalize_text(row.get("Models")) for row in rows if normalize_text(row.get("Models"))]
    pairwise_dissimilarities: list[float] = []
    for left_index, left in enumerate(rows):
        for right in rows[left_index + 1 :]:
            sim = solution_similarity(left, right, casebase_by_ref, taxonomy_index, DEFAULT_WEIGHTS)
            pairwise_dissimilarities.append(1.0 - sim)
    return {
        "refs": ",".join(references),
        "top_similarity": similarities[0] if similarities else 0.0,
        "mean_similarity": float(np.mean(similarities)) if similarities else 0.0,
        "unique_models": len(set(models)),
        "has_duplicate_models": int(len(models) != len(set(models))),
        "intra_list_dissimilarity": float(np.mean(pairwise_dissimilarities)) if pairwise_dissimilarities else 0.0,
    }


def rank_biserial_from_diff(diff: np.ndarray) -> float | None:
    nonzero = diff[np.abs(diff) > EPS]
    if len(nonzero) == 0:
        return None
    ranks = rankdata(np.abs(nonzero), method="average")
    w_plus = float(ranks[nonzero > 0].sum())
    w_minus = float(ranks[nonzero < 0].sum())
    denom = w_plus + w_minus
    if denom <= 0:
        return None
    return (w_plus - w_minus) / denom


def wilcoxon_test(diff: np.ndarray) -> tuple[int, float | None, float | None, float | None]:
    nonzero_n = int(np.sum(np.abs(diff) > EPS))
    if nonzero_n == 0:
        return 0, None, None, None
    try:
        res = wilcoxon(diff, zero_method="wilcox", correction=False, alternative="two-sided", method="auto")
        statistic = float(res.statistic)
        p_value = float(res.pvalue)
    except Exception:
        statistic = None
        p_value = None
    return nonzero_n, statistic, p_value, rank_biserial_from_diff(diff)


def sign_test(diff: np.ndarray) -> tuple[int, int, int, float | None]:
    pos = int(np.sum(diff > EPS))
    neg = int(np.sum(diff < -EPS))
    ties = int(len(diff) - pos - neg)
    n = pos + neg
    if n == 0:
        return pos, neg, ties, None
    return pos, neg, ties, float(binomtest(pos, n=n, p=0.5, alternative="two-sided").pvalue)


def bootstrap_ci(
    baseline: np.ndarray,
    diverse: np.ndarray,
    rng: np.random.Generator,
    *,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
    chunk_size: int = 1000,
) -> dict[str, float]:
    baseline = baseline.astype(float)
    diverse = diverse.astype(float)
    n = len(baseline)
    if n == 0:
        return {
            "ci95_mean_change_low": math.nan,
            "ci95_mean_change_high": math.nan,
            "ci95_relative_change_percent_low": math.nan,
            "ci95_relative_change_percent_high": math.nan,
        }
    diffs: list[np.ndarray] = []
    rels: list[np.ndarray] = []
    diff_vec = diverse - baseline
    done = 0
    while done < n_resamples:
        m = min(chunk_size, n_resamples - done)
        idx = rng.integers(0, n, size=(m, n), endpoint=False)
        boot_base = baseline[idx].mean(axis=1)
        boot_diff = diff_vec[idx].mean(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            boot_rel = np.where(np.abs(boot_base) > EPS, (boot_diff / boot_base) * 100.0, np.nan)
        diffs.append(boot_diff)
        rels.append(boot_rel)
        done += m
    diff_all = np.concatenate(diffs)
    rel_all = np.concatenate(rels)
    return {
        "ci95_mean_change_low": float(np.nanquantile(diff_all, 0.025)),
        "ci95_mean_change_high": float(np.nanquantile(diff_all, 0.975)),
        "ci95_relative_change_percent_low": float(np.nanquantile(rel_all, 0.025)),
        "ci95_relative_change_percent_high": float(np.nanquantile(rel_all, 0.975)),
    }


def paired_summary_rows(df: pd.DataFrame, specs: Iterable[MetricSpec], rng: np.random.Generator, *, task: str | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in specs:
        baseline = df[spec.baseline_col].to_numpy(dtype=float)
        diverse = df[spec.diverse_col].to_numpy(dtype=float)
        diff = diverse - baseline
        pos, neg, ties, sign_p = sign_test(diff)
        nonzero_n, w_stat, w_p, rb = wilcoxon_test(diff)
        boot = bootstrap_ci(baseline, diverse, rng)
        base_mean = float(np.mean(baseline)) if len(baseline) else math.nan
        div_mean = float(np.mean(diverse)) if len(diverse) else math.nan
        mean_change = div_mean - base_mean
        relative_change = (mean_change / base_mean * 100.0) if abs(base_mean) > EPS else math.nan
        row = {
            "task": task if task is not None else "ALL",
            "metric_id": spec.metric_id,
            "metric_es": spec.metric_es,
            "family_es": spec.family_es,
            "higher_is_better": spec.higher_is_better,
            "n": int(len(df)),
            "baseline_mean": base_mean,
            "baseline_sd": float(np.std(baseline, ddof=1)) if len(baseline) > 1 else 0.0,
            "baseline_median": float(np.median(baseline)) if len(baseline) else math.nan,
            "baseline_q1": float(np.quantile(baseline, 0.25)) if len(baseline) else math.nan,
            "baseline_q3": float(np.quantile(baseline, 0.75)) if len(baseline) else math.nan,
            "diverse_mean": div_mean,
            "diverse_sd": float(np.std(diverse, ddof=1)) if len(diverse) > 1 else 0.0,
            "diverse_median": float(np.median(diverse)) if len(diverse) else math.nan,
            "diverse_q1": float(np.quantile(diverse, 0.25)) if len(diverse) else math.nan,
            "diverse_q3": float(np.quantile(diverse, 0.75)) if len(diverse) else math.nan,
            "mean_change": mean_change,
            "median_change": float(np.median(diff)) if len(diff) else math.nan,
            "relative_change_percent": relative_change,
            "improved_n": pos if spec.higher_is_better else neg,
            "worsened_n": neg if spec.higher_is_better else pos,
            "tied_n": ties,
            "wilcoxon_n_nonzero": nonzero_n,
            "wilcoxon_statistic": w_stat,
            "wilcoxon_p": w_p,
            "wilcoxon_p_text": fmt_p(w_p),
            "rank_biserial": rb,
            "unique_models_sign_test_p": sign_p if spec.metric_id == "unique_models_top5" else None,
            "unique_models_sign_test_p_text": fmt_p(sign_p) if spec.metric_id == "unique_models_top5" else "",
        }
        row.update(boot)
        rows.append(row)
    return rows


def ordered_pattern_counts(values: Iterable[str]) -> dict[str, Any]:
    counts = Counter(values)
    multiplicities = np.array(list(counts.values()), dtype=float)
    return {
        "n_observations": int(sum(counts.values())),
        "unique_patterns": int(len(counts)),
        "singleton_patterns": int(sum(1 for c in counts.values() if c == 1)),
        "max_cluster_size": int(max(counts.values()) if counts else 0),
        "median_cluster_size": float(np.median(multiplicities)) if len(multiplicities) else 0.0,
        "mean_cluster_size": float(np.mean(multiplicities)) if len(multiplicities) else 0.0,
    }


def unordered_refset(pattern: str) -> str:
    refs = [part.strip() for part in str(pattern).split(",") if part.strip()]
    return ",".join(sorted(refs, key=lambda x: int(x) if x.isdigit() else x))


def build_markdown_table(df: pd.DataFrame, columns: list[str], headers: list[str], max_rows: int | None = None) -> str:
    view = df.loc[:, columns].copy()
    if max_rows is not None:
        view = view.head(max_rows)
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for _, row in view.iterrows():
        vals = [str(row[col]) for col in columns]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(BOOTSTRAP_SEED)

    casebase_by_ref = load_casebase(CASEBASE_CSV)
    taxonomy_index = build_taxonomy_index(load_taxonomy_tree(DIVERSITY_DIR))
    per_query = pd.read_csv(RUN_DIR / "per_query.csv", sep=";", keep_default_na=False)
    queries = pd.read_csv(RUN_DIR / "queries.csv", sep=";", keep_default_na=False)

    # Main exact per-query metrics from existing baseline and lambda=.70 diverse CSVs.
    exact_rows: list[dict[str, Any]] = []
    pool_cache: dict[int, list[dict[str, str]]] = {}
    for _, info in per_query.iterrows():
        q = int(info["query_index"])
        _, baseline_rows = read_csv_rows(CBR_DATA_DIR / f"baseline_results_{q}.csv")
        _, diverse_rows = read_csv_rows(DIVERSE_DIR / f"pool_results_{q}.diverse.csv")
        _, pool_rows = read_csv_rows(CBR_DATA_DIR / f"pool_results_{q}.csv")
        pool_cache[q] = pool_rows
        bm = result_metrics_from_rows(baseline_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
        dm = result_metrics_from_rows(diverse_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
        exact_rows.append(
            {
                "query_index": q,
                "facts_file": info["facts_file"],
                "task": info["task"],
                "baseline_refs": bm["refs"],
                "diverse_refs": dm["refs"],
                "changed_order": bm["refs"] != dm["refs"],
                "changed_reference_set": set(bm["refs"].split(",")) != set(dm["refs"].split(",")),
                "top1_preserved": (bm["refs"].split(",")[0] if bm["refs"] else "") == (dm["refs"].split(",")[0] if dm["refs"] else ""),
                "baseline_top_similarity": bm["top_similarity"],
                "diverse_top_similarity": dm["top_similarity"],
                "baseline_mean_similarity": bm["mean_similarity"],
                "diverse_mean_similarity": dm["mean_similarity"],
                "baseline_unique_models": bm["unique_models"],
                "diverse_unique_models": dm["unique_models"],
                "baseline_has_duplicate_models": bm["has_duplicate_models"],
                "diverse_has_duplicate_models": dm["has_duplicate_models"],
                "baseline_intra_list_dissimilarity": bm["intra_list_dissimilarity"],
                "diverse_intra_list_dissimilarity": dm["intra_list_dissimilarity"],
            }
        )
    exact_df = pd.DataFrame(exact_rows).sort_values("query_index")
    exact_df.to_csv(OUT_DIR / "per_query_metrics_exact.csv", index=False)

    paired_rows = paired_summary_rows(exact_df, METRICS, rng)
    paired_df = pd.DataFrame(paired_rows)
    paired_df.to_csv(OUT_DIR / "paired_metric_summary.csv", index=False)

    task_counts = exact_df.groupby("task", as_index=False).size().rename(columns={"size": "n"}).sort_values(["n", "task"], ascending=[False, True])
    task_counts.to_csv(OUT_DIR / "task_counts.csv", index=False)

    strat_rows: list[dict[str, Any]] = []
    for task in sorted(exact_df["task"].unique()):
        sub = exact_df[exact_df["task"] == task]
        strat_rows.extend(paired_summary_rows(sub, METRICS, rng, task=task))
    strat_df = pd.DataFrame(strat_rows)
    strat_df.to_csv(OUT_DIR / "task_stratified_metric_summary.csv", index=False)

    # Exact lambda sensitivity using pipeline.diversity_rerank.rerank_mmr on existing pool_results.
    sens_rows: list[dict[str, Any]] = []
    for lam in SENSITIVITY_LAMBDAS:
        for _, info in per_query.iterrows():
            q = int(info["query_index"])
            pool_rows = pool_cache[q]
            baseline_rows = pool_rows[:TOP_K]
            ranked = rerank_mmr(
                pool_rows,
                top_k=TOP_K,
                lambda_relevance=lam,
                casebase_by_ref=casebase_by_ref,
                taxonomy_index=taxonomy_index,
                weights=DEFAULT_WEIGHTS,
                keep_top1=True,
                pool_size=len(pool_rows),
            )
            diverse_rows = [row for row, _scores in ranked]
            bm = result_metrics_from_rows(baseline_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
            dm = result_metrics_from_rows(diverse_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
            sens_rows.append(
                {
                    "lambda_relevance": lam,
                    "query_index": q,
                    "task": info["task"],
                    "baseline_refs": bm["refs"],
                    "reranked_refs": dm["refs"],
                    "changed_order": bm["refs"] != dm["refs"],
                    "changed_reference_set": set(bm["refs"].split(",")) != set(dm["refs"].split(",")),
                    "top1_preserved": (bm["refs"].split(",")[0] if bm["refs"] else "") == (dm["refs"].split(",")[0] if dm["refs"] else ""),
                    "baseline_top_similarity": bm["top_similarity"],
                    "diverse_top_similarity": dm["top_similarity"],
                    "baseline_mean_similarity": bm["mean_similarity"],
                    "diverse_mean_similarity": dm["mean_similarity"],
                    "baseline_unique_models": bm["unique_models"],
                    "diverse_unique_models": dm["unique_models"],
                    "baseline_has_duplicate_models": bm["has_duplicate_models"],
                    "diverse_has_duplicate_models": dm["has_duplicate_models"],
                    "baseline_intra_list_dissimilarity": bm["intra_list_dissimilarity"],
                    "diverse_intra_list_dissimilarity": dm["intra_list_dissimilarity"],
                }
            )
    sens_df = pd.DataFrame(sens_rows)
    sens_df.to_csv(OUT_DIR / "sensitivity_per_query_metrics.csv", index=False)

    sens_metric_rows: list[dict[str, Any]] = []
    # No bootstrap in sensitivity: these are exact summaries over the deterministic rerank.
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        for spec in METRICS:
            baseline = sub[spec.baseline_col].to_numpy(dtype=float)
            diverse = sub[spec.diverse_col].to_numpy(dtype=float)
            diff = diverse - baseline
            pos, neg, ties, sign_p = sign_test(diff)
            nonzero_n, w_stat, w_p, rb = wilcoxon_test(diff)
            base_mean = float(np.mean(baseline))
            div_mean = float(np.mean(diverse))
            mean_change = div_mean - base_mean
            sens_metric_rows.append(
                {
                    "lambda_relevance": lam,
                    "metric_id": spec.metric_id,
                    "metric_es": spec.metric_es,
                    "family_es": spec.family_es,
                    "n": int(len(sub)),
                    "baseline_mean": base_mean,
                    "reranked_mean": div_mean,
                    "mean_change": mean_change,
                    "relative_change_percent": (mean_change / base_mean * 100.0) if abs(base_mean) > EPS else math.nan,
                    "improved_n": pos if spec.higher_is_better else neg,
                    "worsened_n": neg if spec.higher_is_better else pos,
                    "tied_n": ties,
                    "wilcoxon_n_nonzero": nonzero_n,
                    "wilcoxon_statistic": w_stat,
                    "wilcoxon_p": w_p,
                    "wilcoxon_p_text": fmt_p(w_p),
                    "rank_biserial": rb,
                    "unique_models_sign_test_p": sign_p if spec.metric_id == "unique_models_top5" else None,
                    "unique_models_sign_test_p_text": fmt_p(sign_p) if spec.metric_id == "unique_models_top5" else "",
                }
            )
    sens_metric_df = pd.DataFrame(sens_metric_rows)
    sens_metric_df.to_csv(OUT_DIR / "sensitivity_lambda_metric_changes.csv", index=False)

    overview_rows: list[dict[str, Any]] = []
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        pattern_info = ordered_pattern_counts(sub["reranked_refs"])
        refset_info = ordered_pattern_counts(sub["reranked_refs"].map(unordered_refset))
        overview_rows.append(
            {
                "lambda_relevance": lam,
                "top_k": TOP_K,
                "keep_top1": True,
                "n_queries": int(len(sub)),
                "mean_top_similarity": float(sub["diverse_top_similarity"].mean()),
                "mean_similarity_top5": float(sub["diverse_mean_similarity"].mean()),
                "mean_unique_models_top5": float(sub["diverse_unique_models"].mean()),
                "queries_with_duplicate_models": int(sub["diverse_has_duplicate_models"].sum()),
                "mean_intra_list_dissimilarity": float(sub["diverse_intra_list_dissimilarity"].mean()),
                "changed_order_n": int(sub["changed_order"].sum()),
                "changed_reference_set_n": int(sub["changed_reference_set"].sum()),
                "top1_preserved_n": int(sub["top1_preserved"].sum()),
                "unique_ordered_ranking_patterns": pattern_info["unique_patterns"],
                "max_ordered_pattern_cluster": pattern_info["max_cluster_size"],
                "unique_unordered_refsets": refset_info["unique_patterns"],
                "max_unordered_refset_cluster": refset_info["max_cluster_size"],
            }
        )
    overview_df = pd.DataFrame(overview_rows)
    overview_df.to_csv(OUT_DIR / "sensitivity_lambda_overview.csv", index=False)

    sens_task_rows: list[dict[str, Any]] = []
    for (lam, task), sub in sens_df.groupby(["lambda_relevance", "task"]):
        sens_task_rows.append(
            {
                "lambda_relevance": lam,
                "task": task,
                "n": int(len(sub)),
                "mean_similarity_top5": float(sub["diverse_mean_similarity"].mean()),
                "mean_similarity_change": float((sub["diverse_mean_similarity"] - sub["baseline_mean_similarity"]).mean()),
                "mean_unique_models_top5": float(sub["diverse_unique_models"].mean()),
                "mean_unique_models_change": float((sub["diverse_unique_models"] - sub["baseline_unique_models"]).mean()),
                "queries_with_duplicate_models": int(sub["diverse_has_duplicate_models"].sum()),
                "mean_intra_list_dissimilarity": float(sub["diverse_intra_list_dissimilarity"].mean()),
                "mean_ild_change": float((sub["diverse_intra_list_dissimilarity"] - sub["baseline_intra_list_dissimilarity"]).mean()),
                "changed_reference_set_n": int(sub["changed_reference_set"].sum()),
                "changed_order_n": int(sub["changed_order"].sum()),
            }
        )
    pd.DataFrame(sens_task_rows).sort_values(["lambda_relevance", "task"]).to_csv(OUT_DIR / "sensitivity_by_task.csv", index=False)

    # Pseudoreplication diagnostics: normalized query signatures and ranking patterns.
    signature_cols = [
        "normalized_task",
        "normalized_case_study_type",
        "normalized_case_study",
        "normalized_online_offline",
        "normalized_input_for_model",
        "normalized_input_type",
    ]
    sig_frame = queries[["query_index", *signature_cols]].copy()
    for col in signature_cols:
        sig_frame[col] = sig_frame[col].map(normalize_text)
    sig_frame["normalized_signature"] = sig_frame[signature_cols].agg(" | ".join, axis=1)
    signature_counts = sig_frame["normalized_signature"].value_counts()
    sig_diag = ordered_pattern_counts(sig_frame["normalized_signature"])

    diag_rows = []
    diag_rows.append({"unit": "firma de consulta normalizada", "definition": "task+case-study-type+case-study+online/offline+input-for-model+input-type normalizados", **sig_diag})
    diag_rows.append({"unit": "ranking baseline ordenado", "definition": "secuencia ordenada de referencias top-5 sin diversidad", **ordered_pattern_counts(exact_df["baseline_refs"])})
    diag_rows.append({"unit": "conjunto baseline no ordenado", "definition": "conjunto de referencias top-5 sin diversidad", **ordered_pattern_counts(exact_df["baseline_refs"].map(unordered_refset))})
    diag_rows.append({"unit": "ranking MMR lambda=0.70 ordenado", "definition": "secuencia ordenada de referencias top-5 con MMR, top-1 fijo", **ordered_pattern_counts(exact_df["diverse_refs"])})
    diag_rows.append({"unit": "conjunto MMR lambda=0.70 no ordenado", "definition": "conjunto de referencias top-5 con MMR, top-1 fijo", **ordered_pattern_counts(exact_df["diverse_refs"].map(unordered_refset))})
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        diag_rows.append({"unit": f"ranking sensibilidad lambda={lam:.1f} ordenado", "definition": "secuencia ordenada de referencias top-5 con MMR, top-1 fijo", **ordered_pattern_counts(sub["reranked_refs"])})
    diag_df = pd.DataFrame(diag_rows)
    diag_df["unique_percent"] = diag_df["unique_patterns"] / diag_df["n_observations"] * 100.0
    diag_df.to_csv(OUT_DIR / "pseudoreplication_diagnostics.csv", index=False)

    # Top repeated normalized signatures with their normalized fields.
    sig_counts_df = sig_frame.groupby(["normalized_signature", *signature_cols], as_index=False).size().rename(columns={"size": "count"})
    sig_counts_df.sort_values("count", ascending=False).head(30).to_csv(OUT_DIR / "top_duplicate_normalized_signatures.csv", index=False)

    ranking_top_rows: list[dict[str, Any]] = []
    for method, series in [
        ("baseline", exact_df["baseline_refs"]),
        ("mmr_lambda_0.70_existing", exact_df["diverse_refs"]),
    ]:
        for pattern, count in Counter(series).most_common(20):
            ranking_top_rows.append({"method": method, "pattern_ordered_refs": pattern, "count": count})
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        for pattern, count in Counter(sub["reranked_refs"]).most_common(10):
            ranking_top_rows.append({"method": f"sensitivity_lambda_{lam:.1f}", "pattern_ordered_refs": pattern, "count": count})
    pd.DataFrame(ranking_top_rows).to_csv(OUT_DIR / "top_duplicate_ranking_patterns.csv", index=False)

    # Validate that sensitivity lambda=.70 reproduces the existing reranked files.
    sens_07 = sens_df[sens_df["lambda_relevance"] == LAMBDA_MAIN].set_index("query_index")
    existing = exact_df.set_index("query_index")
    lambda_07_matches = int((sens_07.loc[existing.index, "reranked_refs"].to_numpy() == existing["diverse_refs"].to_numpy()).sum())

    manifest = {
        "analysis_scope": str(RUN_DIR.relative_to(ROOT)),
        "ignored_scope": "unique_full/V21 and any directory outside diversity_comparison_1821_v12_corrected",
        "casebase_csv": str(CASEBASE_CSV.relative_to(ROOT)),
        "casebase_rows_loaded": len(casebase_by_ref),
        "taxonomy_terms_loaded": len(taxonomy_index),
        "top_k": TOP_K,
        "main_lambda_relevance": LAMBDA_MAIN,
        "sensitivity_lambdas": SENSITIVITY_LAMBDAS,
        "keep_top1": True,
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": BOOTSTRAP_SEED,
        "solution_weights": DEFAULT_WEIGHTS,
        "queries": int(len(exact_df)),
        "task_counts": task_counts.to_dict(orient="records"),
        "lambda_0_70_sensitivity_matches_existing_diverse_rankings": lambda_07_matches,
    }
    (OUT_DIR / "analysis_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Publication-oriented markdown with compact tables.
    pub_main = paired_df.copy()
    pub_main["Sin diversidad"] = pub_main["baseline_mean"].map(lambda x: fmt_num(x, 4))
    pub_main["Con MMR λ=0.70"] = pub_main["diverse_mean"].map(lambda x: fmt_num(x, 4))
    pub_main["Δ medio (IC95%)"] = pub_main.apply(
        lambda r: f"{fmt_num(r['mean_change'], 4)} [{fmt_num(r['ci95_mean_change_low'], 4)}, {fmt_num(r['ci95_mean_change_high'], 4)}]",
        axis=1,
    )
    pub_main["Δ relativo (IC95%)"] = pub_main.apply(
        lambda r: f"{fmt_pct(r['relative_change_percent'])} [{fmt_pct(r['ci95_relative_change_percent_low'])}, {fmt_pct(r['ci95_relative_change_percent_high'])}]",
        axis=1,
    )
    pub_main["Mejora/empeora/empate"] = pub_main.apply(lambda r: f"{int(r['improved_n'])}/{int(r['worsened_n'])}/{int(r['tied_n'])}", axis=1)
    pub_main["Wilcoxon p; r_rb"] = pub_main.apply(
        lambda r: "no procede (todo empates)" if pd.isna(r["wilcoxon_p"]) else f"{r['wilcoxon_p_text']}; {fmt_num(r['rank_biserial'], 3)}",
        axis=1,
    )
    pub_main["Sign test modelos únicos"] = pub_main["unique_models_sign_test_p_text"]

    sens_pub = overview_df.copy()
    sens_pub["λ"] = sens_pub["lambda_relevance"].map(lambda x: f"{x:.1f}")
    sens_pub["Sim. media top-5"] = sens_pub["mean_similarity_top5"].map(lambda x: fmt_num(x, 4))
    sens_pub["Modelos únicos"] = sens_pub["mean_unique_models_top5"].map(lambda x: fmt_num(x, 3))
    sens_pub["Listas con repetidos"] = sens_pub["queries_with_duplicate_models"].map(str)
    sens_pub["ILD"] = sens_pub["mean_intra_list_dissimilarity"].map(lambda x: fmt_num(x, 4))
    sens_pub["Cambio conjunto"] = sens_pub["changed_reference_set_n"].map(lambda x: f"{int(x)}/{len(exact_df)}")
    sens_pub["Top-1 preservado"] = sens_pub["top1_preserved_n"].map(lambda x: f"{int(x)}/{len(exact_df)}")
    sens_pub["Patrones ordenados únicos"] = sens_pub["unique_ordered_ranking_patterns"].map(str)

    diag_pub = diag_df.copy()
    diag_pub["Únicos"] = diag_pub["unique_patterns"].map(str)
    diag_pub["% únicos"] = diag_pub["unique_percent"].map(lambda x: fmt_pct(x))
    diag_pub["Máx. clúster"] = diag_pub["max_cluster_size"].map(str)
    diag_pub["Mediana clúster"] = diag_pub["median_cluster_size"].map(lambda x: fmt_num(x, 1))

    md_lines = [
        "# Análisis estadístico corregido: diversidad CBR V12",
        "",
        "Ámbito: se usó exclusivamente `.build/diversity_comparison_1821_v12_corrected`, con la case base `CleanedDATA V12-05-2021.csv` de 263 casos coincidente con `PredictMaint_myCBR.prj`. No se usaron métricas de `unique_full/V21`.",
        "",
        "Todas las cantidades son métricas algorítmicas de recuperación/reranking, no medidas de desempeño predictivo ni validación clínica/industrial. La ILD se calcula con la misma función de similitud entre soluciones que entra en el término de diversidad de MMR; por tanto, es una métrica alineada con el objetivo optimizado y no una comprobación independiente.",
        "",
        "## Resultados pareados globales",
        "",
        build_markdown_table(
            pub_main,
            ["metric_es", "Sin diversidad", "Con MMR λ=0.70", "Δ medio (IC95%)", "Δ relativo (IC95%)", "Mejora/empeora/empate", "Wilcoxon p; r_rb", "Sign test modelos únicos"],
            ["Métrica", "Sin diversidad", "Con MMR λ=0.70", "Δ medio (IC95%)", "Δ relativo (IC95%)", "Mejora/empeora/empate", "Wilcoxon p; r_rb", "Sign test"],
        ),
        "",
        "## Sensibilidad exacta por λ (pool-15 existente, top-k=5, top-1 fijo)",
        "",
        build_markdown_table(
            sens_pub,
            ["λ", "Sim. media top-5", "Modelos únicos", "Listas con repetidos", "ILD", "Cambio conjunto", "Top-1 preservado", "Patrones ordenados únicos"],
            ["λ", "Sim. media top-5", "Modelos únicos", "Listas con repetidos", "ILD", "Cambio conjunto", "Top-1 preservado", "Patrones únicos"],
        ),
        "",
        "## Diagnóstico de pseudorreplicación",
        "",
        build_markdown_table(
            diag_pub.head(5),
            ["unit", "Únicos", "% únicos", "Máx. clúster", "Mediana clúster"],
            ["Unidad", "Únicos", "% únicos", "Máx. clúster", "Mediana clúster"],
        ),
        "",
        "## Texto publicable sugerido",
        "",
        "En el experimento corregido V12 (1.821 consultas derivadas de artefactos OntoCast y case base myCBR de 263 casos), el postprocesamiento MMR con λ=0,70 y top-1 fijo mantuvo inalterada la similitud algorítmica del primer resultado. La similitud media algorítmica del top-5 descendió ligeramente, mientras que las métricas algorítmicas de diversidad aumentaron: los modelos únicos por lista alcanzaron el máximo de 5,0 y la ILD media aumentó de forma marcada. Este resultado debe interpretarse como una redistribución algorítmica de recomendaciones, no como evidencia de mayor exactitud predictiva.",
        "",
        "La sensibilidad exacta sobre los `pool_results` existentes mostró el compromiso esperado: λ más bajos favorecieron más diversidad (mayor ILD y menos modelos repetidos) con menor similitud media; λ más altos preservaron más relevancia CBR pero redujeron la ganancia de diversidad. En todos los escenarios se preservó el primer resultado por construcción.",
        "",
        "Debe advertirse pseudorreplicación potencial: las 1.821 consultas no equivalen a 1.821 configuraciones independientes, porque muchas consultas comparten firmas normalizadas y patrones de ranking. Por ello, las pruebas pareadas describen estabilidad algorítmica sobre consultas generadas, no inferencia sobre una población independiente de problemas de mantenimiento predictivo.",
    ]
    (OUT_DIR / "publication_text_es.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
