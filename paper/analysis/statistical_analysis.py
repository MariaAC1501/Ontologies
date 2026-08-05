#!/usr/bin/env python3
"""Statistical analysis for the V12 no-default-synchronization experiment.

Primary data scope: .build/diversity_comparison_1821_v12_no_default_sync
(V12/263 cases, query-year 2026, Unknown synchronization discarded as default
evidence). The script reuses the statistical protocol implemented in
paper/analysis/statistical_protocol.py: paired 20,000-resample bootstrap with
seed 20260727, Wilcoxon/rank-biserial, sign tests, task strata,
pseudoreplication diagnostics, and lambda sensitivity over the in-run pools.

The V12 final weighted-default run is read only for the descriptive ablation.
Outputs are copied to paper/supplement/statistics.
"""
from __future__ import annotations

import importlib.util
import json
import math
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "paper" / "analysis" / "statistical_analysis.py").exists() and (candidate / "pipeline" / "diversity_rerank.py").exists():
            return candidate
    raise RuntimeError(f"Could not find repository root from {start}")


ROOT = find_repo_root(Path(__file__).resolve())
PROTO_PATH = ROOT / "paper" / "analysis" / "statistical_protocol.py"
spec = importlib.util.spec_from_file_location("paper_statistical_analysis_protocol", PROTO_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not import protocol from {PROTO_PATH}")
proto = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = proto
spec.loader.exec_module(proto)

RUN_DIR = ROOT / ".build" / "diversity_comparison_1821_v12_no_default_sync"
DEFAULT_SYNC_RUN_DIR = ROOT / ".build" / "diversity_comparison_1821_v12_final"
OUT_DIR = RUN_DIR / "statistical_analysis_outputs"
CBR_DATA_DIR = RUN_DIR / "cbr_data"
CASEBASE_CSV = CBR_DATA_DIR / "CleanedDATA V12-05-2021.csv"
DIVERSITY_DIR = ROOT / "external" / "Diversity-Improvement-in-CBR"
TOP_K = proto.TOP_K
LAMBDA_MAIN = proto.LAMBDA_MAIN
SENSITIVITY_LAMBDAS = proto.SENSITIVITY_LAMBDAS
EPS = proto.EPS


def json_safe(value: Any) -> Any:
    """Replace non-finite numeric values so manifests are strict JSON."""
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(float(value)):
        return None
    if isinstance(value, np.integer):
        return int(value)
    return value


def first_ref(pattern: str) -> str:
    refs = [part.strip() for part in str(pattern).split(",") if part.strip()]
    return refs[0] if refs else ""


def refset_from_pattern(pattern: str) -> frozenset[str]:
    return frozenset(part.strip() for part in str(pattern).split(",") if part.strip())


def exact_metrics_for_run(
    run_dir: Path,
    *,
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
    load_pool: bool = False,
) -> tuple[pd.DataFrame, dict[int, list[dict[str, str]]]]:
    """Recompute the same top-k metrics from the stored CBR/reranked CSVs."""
    per_query = pd.read_csv(run_dir / "per_query.csv", sep=";", keep_default_na=False)
    cbr_dir = run_dir / "cbr_data"
    diverse_dir = run_dir / "with_diversity"
    rows: list[dict[str, Any]] = []
    pool_cache: dict[int, list[dict[str, str]]] = {}
    for _, info in per_query.iterrows():
        q = int(info["query_index"])
        _, baseline_rows = proto.read_csv_rows(cbr_dir / f"baseline_results_{q}.csv")
        _, diverse_rows = proto.read_csv_rows(diverse_dir / f"pool_results_{q}.diverse.csv")
        if load_pool:
            _, pool_cache[q] = proto.read_csv_rows(cbr_dir / f"pool_results_{q}.csv")
        bm = proto.result_metrics_from_rows(baseline_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
        dm = proto.result_metrics_from_rows(diverse_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
        rows.append(
            {
                "query_index": q,
                "facts_file": info["facts_file"],
                "task": info["task"],
                "baseline_refs": bm["refs"],
                "diverse_refs": dm["refs"],
                "changed_order": bm["refs"] != dm["refs"],
                "changed_reference_set": refset_from_pattern(bm["refs"]) != refset_from_pattern(dm["refs"]),
                "top1_preserved": first_ref(bm["refs"]) == first_ref(dm["refs"]),
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
    return pd.DataFrame(rows).sort_values("query_index"), pool_cache


def build_sensitivity(
    per_query: pd.DataFrame,
    pool_cache: dict[int, list[dict[str, str]]],
    *,
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sens_rows: list[dict[str, Any]] = []
    for lam in SENSITIVITY_LAMBDAS:
        for _, info in per_query.iterrows():
            q = int(info["query_index"])
            pool_rows = pool_cache[q]
            baseline_rows = pool_rows[:TOP_K]
            ranked = proto.rerank_mmr(
                pool_rows,
                top_k=TOP_K,
                lambda_relevance=lam,
                casebase_by_ref=casebase_by_ref,
                taxonomy_index=taxonomy_index,
                weights=proto.DEFAULT_WEIGHTS,
                keep_top1=True,
                pool_size=len(pool_rows),
            )
            diverse_rows = [row for row, _scores in ranked]
            bm = proto.result_metrics_from_rows(baseline_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
            dm = proto.result_metrics_from_rows(diverse_rows, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
            sens_rows.append(
                {
                    "lambda_relevance": lam,
                    "query_index": q,
                    "task": info["task"],
                    "baseline_refs": bm["refs"],
                    "reranked_refs": dm["refs"],
                    "changed_order": bm["refs"] != dm["refs"],
                    "changed_reference_set": refset_from_pattern(bm["refs"]) != refset_from_pattern(dm["refs"]),
                    "top1_preserved": first_ref(bm["refs"]) == first_ref(dm["refs"]),
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

    sens_metric_rows: list[dict[str, Any]] = []
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        for spec in proto.METRICS:
            baseline = sub[spec.baseline_col].to_numpy(dtype=float)
            diverse = sub[spec.diverse_col].to_numpy(dtype=float)
            diff = diverse - baseline
            pos, neg, ties, sign_p = proto.sign_test(diff)
            nonzero_n, w_stat, w_p, rb = proto.wilcoxon_test(diff)
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
                    "wilcoxon_p_text": proto.fmt_p(w_p),
                    "rank_biserial": rb,
                    "unique_models_sign_test_p": sign_p if spec.metric_id == "unique_models_top5" else None,
                    "unique_models_sign_test_p_text": proto.fmt_p(sign_p) if spec.metric_id == "unique_models_top5" else "",
                }
            )
    sens_metric_df = pd.DataFrame(sens_metric_rows)

    overview_rows: list[dict[str, Any]] = []
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        pattern_info = proto.ordered_pattern_counts(sub["reranked_refs"])
        refset_info = proto.ordered_pattern_counts(sub["reranked_refs"].map(proto.unordered_refset))
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
    sens_task_df = pd.DataFrame(sens_task_rows).sort_values(["lambda_relevance", "task"])
    return sens_df, sens_metric_df, overview_df, sens_task_df


def build_default_sync_ablation(primary_df: pd.DataFrame, default_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    merged = primary_df.merge(
        default_df,
        on="query_index",
        suffixes=("_primary_no_default", "_default_sync"),
        how="inner",
        validate="one_to_one",
    ).sort_values("query_index")
    merged["facts_file_equal"] = merged["facts_file_primary_no_default"] == merged["facts_file_default_sync"]
    merged["task_equal"] = merged["task_primary_no_default"] == merged["task_default_sync"]
    for prefix in ["baseline", "diverse"]:
        p_refs = merged[f"{prefix}_refs_primary_no_default"]
        d_refs = merged[f"{prefix}_refs_default_sync"]
        merged[f"{prefix}_ranking_equal"] = p_refs == d_refs
        merged[f"{prefix}_top1_equal"] = p_refs.map(first_ref) == d_refs.map(first_ref)
        merged[f"{prefix}_refset_equal"] = [refset_from_pattern(a) == refset_from_pattern(b) for a, b in zip(p_refs, d_refs)]
        for col in ["top_similarity", "mean_similarity", "unique_models", "intra_list_dissimilarity"]:
            merged[f"{prefix}_{col}_diff_primary_minus_default"] = (
                merged[f"{prefix}_{col}_primary_no_default"].astype(float) - merged[f"{prefix}_{col}_default_sync"].astype(float)
            )
    primary = primary_df.set_index("query_index").loc[merged["query_index"]]
    default = default_df.set_index("query_index").loc[merged["query_index"]]

    def aggregate(prefix: str, label: str, description: str) -> dict[str, Any]:
        n = int(len(merged))
        primary_dup = int(primary[f"{prefix}_has_duplicate_models"].astype(int).sum())
        default_dup = int(default[f"{prefix}_has_duplicate_models"].astype(int).sum())
        row: dict[str, Any] = {
            "comparison_scope": label,
            "description": description,
            "n_queries": n,
            "facts_file_equal_n": int(merged["facts_file_equal"].sum()),
            "task_equal_n": int(merged["task_equal"].sum()),
            "rankings_equal_n": int(merged[f"{prefix}_ranking_equal"].sum()),
            "rankings_equal_percent": int(merged[f"{prefix}_ranking_equal"].sum()) / n * 100.0,
            "top1_equal_n": int(merged[f"{prefix}_top1_equal"].sum()),
            "top1_equal_percent": int(merged[f"{prefix}_top1_equal"].sum()) / n * 100.0,
            "refsets_equal_n": int(merged[f"{prefix}_refset_equal"].sum()),
            "refsets_equal_percent": int(merged[f"{prefix}_refset_equal"].sum()) / n * 100.0,
            "primary_no_default_mean_top_similarity": float(primary[f"{prefix}_top_similarity"].mean()),
            "default_sync_mean_top_similarity": float(default[f"{prefix}_top_similarity"].mean()),
            "diff_primary_minus_default_mean_top_similarity": float(primary[f"{prefix}_top_similarity"].mean() - default[f"{prefix}_top_similarity"].mean()),
            "primary_no_default_mean_similarity_top5": float(primary[f"{prefix}_mean_similarity"].mean()),
            "default_sync_mean_similarity_top5": float(default[f"{prefix}_mean_similarity"].mean()),
            "diff_primary_minus_default_mean_similarity_top5": float(primary[f"{prefix}_mean_similarity"].mean() - default[f"{prefix}_mean_similarity"].mean()),
            "primary_no_default_mean_unique_models_top5": float(primary[f"{prefix}_unique_models"].mean()),
            "default_sync_mean_unique_models_top5": float(default[f"{prefix}_unique_models"].mean()),
            "diff_primary_minus_default_mean_unique_models_top5": float(primary[f"{prefix}_unique_models"].mean() - default[f"{prefix}_unique_models"].mean()),
            "primary_no_default_duplicate_model_lists": primary_dup,
            "default_sync_duplicate_model_lists": default_dup,
            "diff_primary_minus_default_duplicate_model_lists": primary_dup - default_dup,
            "primary_no_default_mean_intra_list_dissimilarity": float(primary[f"{prefix}_intra_list_dissimilarity"].mean()),
            "default_sync_mean_intra_list_dissimilarity": float(default[f"{prefix}_intra_list_dissimilarity"].mean()),
            "diff_primary_minus_default_mean_intra_list_dissimilarity": float(
                primary[f"{prefix}_intra_list_dissimilarity"].mean() - default[f"{prefix}_intra_list_dissimilarity"].mean()
            ),
        }
        if prefix == "diverse":
            row.update(
                {
                    "primary_no_default_changed_order_vs_own_baseline_n": int(primary["changed_order"].sum()),
                    "default_sync_changed_order_vs_own_baseline_n": int(default["changed_order"].sum()),
                    "diff_primary_minus_default_changed_order_vs_own_baseline_n": int(primary["changed_order"].sum() - default["changed_order"].sum()),
                    "primary_no_default_changed_refset_vs_own_baseline_n": int(primary["changed_reference_set"].sum()),
                    "default_sync_changed_refset_vs_own_baseline_n": int(default["changed_reference_set"].sum()),
                    "diff_primary_minus_default_changed_refset_vs_own_baseline_n": int(primary["changed_reference_set"].sum() - default["changed_reference_set"].sum()),
                    "primary_no_default_top1_preserved_vs_own_baseline_n": int(primary["top1_preserved"].sum()),
                    "default_sync_top1_preserved_vs_own_baseline_n": int(default["top1_preserved"].sum()),
                    "diff_primary_minus_default_top1_preserved_vs_own_baseline_n": int(primary["top1_preserved"].sum() - default["top1_preserved"].sum()),
                }
            )
        return row

    summary = pd.DataFrame(
        [
            aggregate("baseline", "baseline_headless_cbr_top5", "Top-5 HeadlessCBR sin diversidad: no-default-sync frente a V12 final con default ponderado"),
            aggregate("diverse", "mmr_lambda_0.70_keep_top1", "Ranking principal MMR λ=0.70, top-1 fijo: no-default-sync frente a V12 final con default ponderado"),
        ]
    )
    return merged, summary


def pseudoreplication_outputs(queries: pd.DataFrame, exact_df: pd.DataFrame, sens_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
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
        sig_frame[col] = sig_frame[col].map(proto.normalize_text)
    sig_frame["normalized_signature"] = sig_frame[signature_cols].agg(" | ".join, axis=1)
    diag_rows = [
        {"unit": "firma de consulta normalizada", "definition": "task+case-study-type+case-study+online/offline+input-for-model+input-type normalizados", **proto.ordered_pattern_counts(sig_frame["normalized_signature"])},
        {"unit": "ranking baseline ordenado", "definition": "secuencia ordenada de referencias top-5 sin diversidad", **proto.ordered_pattern_counts(exact_df["baseline_refs"])},
        {"unit": "conjunto baseline no ordenado", "definition": "conjunto de referencias top-5 sin diversidad", **proto.ordered_pattern_counts(exact_df["baseline_refs"].map(proto.unordered_refset))},
        {"unit": "ranking MMR lambda=0.70 ordenado", "definition": "secuencia ordenada de referencias top-5 con MMR, top-1 fijo", **proto.ordered_pattern_counts(exact_df["diverse_refs"])},
        {"unit": "conjunto MMR lambda=0.70 no ordenado", "definition": "conjunto de referencias top-5 con MMR, top-1 fijo", **proto.ordered_pattern_counts(exact_df["diverse_refs"].map(proto.unordered_refset))},
    ]
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        diag_rows.append({"unit": f"ranking sensibilidad lambda={lam:.1f} ordenado", "definition": "secuencia ordenada de referencias top-5 con MMR, top-1 fijo", **proto.ordered_pattern_counts(sub["reranked_refs"])})
    diag_df = pd.DataFrame(diag_rows)
    diag_df["unique_percent"] = diag_df["unique_patterns"] / diag_df["n_observations"] * 100.0

    sig_counts_df = sig_frame.groupby(["normalized_signature", *signature_cols], as_index=False).size().rename(columns={"size": "count"})
    sig_counts_df = sig_counts_df.sort_values("count", ascending=False).head(30)

    ranking_top_rows: list[dict[str, Any]] = []
    for method, series in [("baseline", exact_df["baseline_refs"]), ("mmr_lambda_0.70_existing", exact_df["diverse_refs"] )]:
        for pattern, count in Counter(series).most_common(20):
            ranking_top_rows.append({"method": method, "pattern_ordered_refs": pattern, "count": count})
    for lam in SENSITIVITY_LAMBDAS:
        sub = sens_df[sens_df["lambda_relevance"] == lam]
        for pattern, count in Counter(sub["reranked_refs"]).most_common(10):
            ranking_top_rows.append({"method": f"sensitivity_lambda_{lam:.1f}", "pattern_ordered_refs": pattern, "count": count})
    return diag_df, sig_counts_df, pd.DataFrame(ranking_top_rows)


def publication_text(
    paired_df: pd.DataFrame,
    overview_df: pd.DataFrame,
    diag_df: pd.DataFrame,
    default_sync_ablation_df: pd.DataFrame,
    task_counts: pd.DataFrame,
    exact_df: pd.DataFrame,
) -> str:
    pub_main = paired_df.copy()
    pub_main["Sin diversidad"] = pub_main["baseline_mean"].map(lambda x: proto.fmt_num(x, 4))
    pub_main["Con MMR λ=0.70"] = pub_main["diverse_mean"].map(lambda x: proto.fmt_num(x, 4))
    pub_main["Δ medio (IC95%)"] = pub_main.apply(lambda r: f"{proto.fmt_num(r['mean_change'], 4)} [{proto.fmt_num(r['ci95_mean_change_low'], 4)}, {proto.fmt_num(r['ci95_mean_change_high'], 4)}]", axis=1)
    pub_main["Δ relativo (IC95%)"] = pub_main.apply(lambda r: f"{proto.fmt_pct(r['relative_change_percent'])} [{proto.fmt_pct(r['ci95_relative_change_percent_low'])}, {proto.fmt_pct(r['ci95_relative_change_percent_high'])}]", axis=1)
    pub_main["Mejora/empeora/empate"] = pub_main.apply(lambda r: f"{int(r['improved_n'])}/{int(r['worsened_n'])}/{int(r['tied_n'])}", axis=1)
    pub_main["Wilcoxon p; r_rb"] = pub_main.apply(lambda r: "no procede (todo empates)" if pd.isna(r["wilcoxon_p"]) else f"{r['wilcoxon_p_text']}; {proto.fmt_num(r['rank_biserial'], 3)}", axis=1)
    pub_main["Sign test modelos únicos"] = pub_main["unique_models_sign_test_p_text"]

    sens_pub = overview_df.copy()
    sens_pub["λ"] = sens_pub["lambda_relevance"].map(lambda x: f"{x:.1f}")
    sens_pub["Sim. media top-5"] = sens_pub["mean_similarity_top5"].map(lambda x: proto.fmt_num(x, 4))
    sens_pub["Modelos únicos"] = sens_pub["mean_unique_models_top5"].map(lambda x: proto.fmt_num(x, 3))
    sens_pub["Listas con repetidos"] = sens_pub["queries_with_duplicate_models"].map(str)
    sens_pub["ILD"] = sens_pub["mean_intra_list_dissimilarity"].map(lambda x: proto.fmt_num(x, 4))
    sens_pub["Cambio conjunto"] = sens_pub["changed_reference_set_n"].map(lambda x: f"{int(x)}/{len(exact_df)}")
    sens_pub["Top-1 preservado"] = sens_pub["top1_preserved_n"].map(lambda x: f"{int(x)}/{len(exact_df)}")
    sens_pub["Patrones ordenados únicos"] = sens_pub["unique_ordered_ranking_patterns"].map(str)

    diag_pub = diag_df.copy()
    diag_pub["Únicos"] = diag_pub["unique_patterns"].map(str)
    diag_pub["% únicos"] = diag_pub["unique_percent"].map(lambda x: proto.fmt_pct(x))
    diag_pub["Máx. clúster"] = diag_pub["max_cluster_size"].map(str)
    diag_pub["Mediana clúster"] = diag_pub["median_cluster_size"].map(lambda x: proto.fmt_num(x, 1))

    abl = default_sync_ablation_df.copy()
    abl["Ámbito"] = abl["comparison_scope"].map({"baseline_headless_cbr_top5": "Baseline CBR", "mmr_lambda_0.70_keep_top1": "MMR λ=0.70"})
    abl["Rankings iguales"] = abl.apply(lambda r: f"{int(r['rankings_equal_n'])}/{int(r['n_queries'])}", axis=1)
    abl["Top-1 iguales"] = abl.apply(lambda r: f"{int(r['top1_equal_n'])}/{int(r['n_queries'])}", axis=1)
    abl["Conjuntos iguales"] = abl.apply(lambda r: f"{int(r['refsets_equal_n'])}/{int(r['n_queries'])}", axis=1)
    abl["Δ sim. top-5"] = abl["diff_primary_minus_default_mean_similarity_top5"].map(lambda x: proto.fmt_num(x, 4))
    abl["Δ modelos únicos"] = abl["diff_primary_minus_default_mean_unique_models_top5"].map(lambda x: proto.fmt_num(x, 4))
    abl["Δ ILD"] = abl["diff_primary_minus_default_mean_intra_list_dissimilarity"].map(lambda x: proto.fmt_num(x, 4))

    task_line = "; ".join(f"{r.task}: {int(r.n)}" for r in task_counts.itertuples(index=False))
    lines = [
        "# Análisis estadístico principal sin evidencia por defecto de sincronización",
        "",
        "Ámbito principal: `.build/diversity_comparison_1821_v12_no_default_sync` (V12/263 casos, 1.821 consultas, query-year 2026). En este análisis `Unknown synchronization` se descarta como evidencia por defecto; por tanto, este experimento sin default debe ser el resultado principal del manuscrito. El directorio `.build/diversity_comparison_1821_v12_final` se usa sólo como ablación descriptiva del default ponderado.",
        "",
        "Todas las cantidades son métricas algorítmicas de recuperación/reranking, no medidas de desempeño predictivo ni validación clínica/industrial. La ILD se calcula con la misma función de similitud entre soluciones que entra en MMR y debe leerse como métrica alineada con el objetivo optimizado.",
        "",
        f"Estratos por tarea: {task_line}.",
        "",
        "## Resultados pareados globales",
        "",
        proto.build_markdown_table(pub_main, ["metric_es", "Sin diversidad", "Con MMR λ=0.70", "Δ medio (IC95%)", "Δ relativo (IC95%)", "Mejora/empeora/empate", "Wilcoxon p; r_rb", "Sign test modelos únicos"], ["Métrica", "Sin diversidad", "Con MMR λ=0.70", "Δ medio (IC95%)", "Δ relativo (IC95%)", "Mejora/empeora/empate", "Wilcoxon p; r_rb", "Sign test"]),
        "",
        "## Sensibilidad exacta por λ (pool-15 del experimento sin default, top-k=5, top-1 fijo)",
        "",
        proto.build_markdown_table(sens_pub, ["λ", "Sim. media top-5", "Modelos únicos", "Listas con repetidos", "ILD", "Cambio conjunto", "Top-1 preservado", "Patrones ordenados únicos"], ["λ", "Sim. media top-5", "Modelos únicos", "Listas con repetidos", "ILD", "Cambio conjunto", "Top-1 preservado", "Patrones únicos"]),
        "",
        "## Ablación descriptiva frente al default ponderado",
        "",
        proto.build_markdown_table(abl, ["Ámbito", "Rankings iguales", "Top-1 iguales", "Conjuntos iguales", "Δ sim. top-5", "Δ modelos únicos", "Δ ILD"], ["Ámbito", "Rankings iguales", "Top-1 iguales", "Conjuntos iguales", "Δ sim. top-5", "Δ modelos únicos", "Δ ILD"]),
        "",
        "Las diferencias son no-default-sync menos default ponderado. La ablación muestra que el default ponderado cambia muchos rankings; debe presentarse como control, no como resultado principal, porque `Unknown synchronization` representa ausencia de información y no evidencia semántica positiva.",
        "",
        "## Diagnóstico de pseudorreplicación",
        "",
        proto.build_markdown_table(diag_pub.head(5), ["unit", "Únicos", "% únicos", "Máx. clúster", "Mediana clúster"], ["Unidad", "Únicos", "% únicos", "Máx. clúster", "Mediana clúster"]),
        "",
        "## Texto publicable sugerido",
        "",
        "En el experimento principal sin default de sincronización (V12/263 casos, 1.821 consultas, query-year 2026), el postprocesamiento MMR con λ=0,70 y top-1 fijo preservó por construcción el primer resultado y mantuvo inalterada su similitud algorítmica. La similitud media del top-5 descendió de forma pequeña, mientras que la diversidad algorítmica aumentó de forma clara: los modelos únicos por lista se aproximaron al máximo de 5,0 y la ILD media aumentó marcadamente. Este resultado debe interpretarse como redistribución algorítmica de recomendaciones, no como evidencia de mayor exactitud predictiva.",
        "",
        "La sensibilidad sobre λ mostró el compromiso esperado entre relevancia y diversidad. Valores menores de λ incrementaron más la diversidad, con menor similitud media; valores mayores preservaron más relevancia CBR, pero redujeron la ganancia de diversidad. En todos los escenarios se preservó el top-1 por diseño.",
        "",
        "Debe advertirse pseudorreplicación potencial: las 1.821 consultas no equivalen a 1.821 configuraciones independientes, porque muchas consultas comparten firmas normalizadas y patrones de ranking. Por ello, las pruebas pareadas describen estabilidad algorítmica sobre consultas generadas, no inferencia sobre una población independiente de problemas de mantenimiento predictivo.",
        "",
        "El experimento sin default debe ser el análisis principal del artículo: tratar `Unknown synchronization` como evidencia por defecto puede reforzar similitudes espurias derivadas de valores desconocidos; descartarlo produce una evaluación semánticamente más conservadora y metodológicamente preferible.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(proto.BOOTSTRAP_SEED)
    run_summary = json.loads((RUN_DIR / "summary.json").read_text(encoding="utf-8"))
    default_summary = json.loads((DEFAULT_SYNC_RUN_DIR / "summary.json").read_text(encoding="utf-8"))
    if run_summary.get("method", {}).get("drop_default_synchronization") is not True:
        raise RuntimeError("Primary run is not no-default-sync")
    if int(run_summary.get("method", {}).get("query_year")) != 2026:
        raise RuntimeError("Primary run does not use query-year 2026")
    if default_summary.get("method", {}).get("drop_default_synchronization") is not False:
        raise RuntimeError("Ablation run is not the weighted-default V12 final run")

    casebase_by_ref = proto.load_casebase(CASEBASE_CSV)
    if len(casebase_by_ref) != 263:
        raise RuntimeError(f"Expected V12 case base with 263 cases, loaded {len(casebase_by_ref)}")
    taxonomy_index = proto.build_taxonomy_index(proto.load_taxonomy_tree(DIVERSITY_DIR))
    per_query = pd.read_csv(RUN_DIR / "per_query.csv", sep=";", keep_default_na=False)
    queries = pd.read_csv(RUN_DIR / "queries.csv", sep=";", keep_default_na=False)
    if len(per_query) != 1821:
        raise RuntimeError(f"Expected 1821 queries, got {len(per_query)}")

    exact_df, pool_cache = exact_metrics_for_run(RUN_DIR, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index, load_pool=True)
    exact_df.to_csv(OUT_DIR / "per_query_metrics_exact.csv", index=False)

    default_exact_df, _ = exact_metrics_for_run(DEFAULT_SYNC_RUN_DIR, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
    default_exact_df.to_csv(OUT_DIR / "default_sync_per_query_metrics_exact.csv", index=False)
    ablation_per_query_df, default_sync_ablation_df = build_default_sync_ablation(exact_df, default_exact_df)
    ablation_per_query_df.to_csv(OUT_DIR / "default_sync_ablation_per_query.csv", index=False)
    default_sync_ablation_df.to_csv(OUT_DIR / "default_sync_ablation.csv", index=False)

    paired_df = pd.DataFrame(proto.paired_summary_rows(exact_df, proto.METRICS, rng))
    paired_df.to_csv(OUT_DIR / "paired_metric_summary.csv", index=False)

    task_counts = exact_df.groupby("task", as_index=False).size().rename(columns={"size": "n"}).sort_values(["n", "task"], ascending=[False, True])
    task_counts.to_csv(OUT_DIR / "task_counts.csv", index=False)

    strat_rows: list[dict[str, Any]] = []
    for task in sorted(exact_df["task"].unique()):
        strat_rows.extend(proto.paired_summary_rows(exact_df[exact_df["task"] == task], proto.METRICS, rng, task=task))
    strat_df = pd.DataFrame(strat_rows)
    strat_df.to_csv(OUT_DIR / "task_stratified_metric_summary.csv", index=False)

    sens_df, sens_metric_df, overview_df, sens_task_df = build_sensitivity(per_query, pool_cache, casebase_by_ref=casebase_by_ref, taxonomy_index=taxonomy_index)
    sens_df.to_csv(OUT_DIR / "sensitivity_per_query_metrics.csv", index=False)
    sens_metric_df.to_csv(OUT_DIR / "sensitivity_lambda_metric_changes.csv", index=False)
    overview_df.to_csv(OUT_DIR / "sensitivity_lambda_overview.csv", index=False)
    sens_task_df.to_csv(OUT_DIR / "sensitivity_by_task.csv", index=False)

    diag_df, sig_counts_df, ranking_top_df = pseudoreplication_outputs(queries, exact_df, sens_df)
    diag_df.to_csv(OUT_DIR / "pseudoreplication_diagnostics.csv", index=False)
    sig_counts_df.to_csv(OUT_DIR / "top_duplicate_normalized_signatures.csv", index=False)
    ranking_top_df.to_csv(OUT_DIR / "top_duplicate_ranking_patterns.csv", index=False)

    sens_07 = sens_df[sens_df["lambda_relevance"] == LAMBDA_MAIN].set_index("query_index")
    existing = exact_df.set_index("query_index")
    lambda_07_matches = int((sens_07.loc[existing.index, "reranked_refs"].to_numpy() == existing["diverse_refs"].to_numpy()).sum())

    manifest = {
        "analysis_scope": str(RUN_DIR.relative_to(ROOT)),
        "primary_experiment": "V12/263, query-year 2026, Unknown synchronization discarded as default evidence; this no-default-sync experiment should be principal",
        "descriptive_ablation_scope": str(DEFAULT_SYNC_RUN_DIR.relative_to(ROOT)),
        "source_protocol": str(PROTO_PATH.relative_to(ROOT)),
        "casebase_csv": str(CASEBASE_CSV.relative_to(ROOT)),
        "casebase_rows_loaded": len(casebase_by_ref),
        "summary_casebase_rows_loaded": run_summary.get("method", {}).get("casebase_rows_loaded"),
        "taxonomy_terms_loaded": len(taxonomy_index),
        "top_k": TOP_K,
        "main_lambda_relevance": LAMBDA_MAIN,
        "sensitivity_lambdas": SENSITIVITY_LAMBDAS,
        "keep_top1": True,
        "bootstrap_resamples": proto.BOOTSTRAP_RESAMPLES,
        "bootstrap_seed": proto.BOOTSTRAP_SEED,
        "solution_weights": proto.DEFAULT_WEIGHTS,
        "primary_query_year": run_summary.get("method", {}).get("query_year"),
        "primary_drop_default_synchronization": run_summary.get("method", {}).get("drop_default_synchronization"),
        "default_ablation_drop_default_synchronization": default_summary.get("method", {}).get("drop_default_synchronization"),
        "queries": int(len(exact_df)),
        "task_counts": task_counts.to_dict(orient="records"),
        "lambda_0_70_sensitivity_matches_existing_diverse_rankings": lambda_07_matches,
        "default_sync_ablation": default_sync_ablation_df.to_dict(orient="records"),
        "outputs_dir": str(OUT_DIR.relative_to(ROOT)),
    }
    safe_manifest = json_safe(manifest)
    (OUT_DIR / "analysis_manifest.json").write_text(json.dumps(safe_manifest, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    (OUT_DIR / "publication_text_es.md").write_text(publication_text(paired_df, overview_df, diag_df, default_sync_ablation_df, task_counts, exact_df), encoding="utf-8")
    supplement_dir = ROOT / "paper" / "supplement" / "statistics"
    supplement_dir.mkdir(parents=True, exist_ok=True)
    for source in OUT_DIR.iterdir():
        if source.is_file() and source.suffix.lower() in {".csv", ".json", ".md"}:
            shutil.copy2(source, supplement_dir / source.name)
    print(json.dumps(safe_manifest, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
