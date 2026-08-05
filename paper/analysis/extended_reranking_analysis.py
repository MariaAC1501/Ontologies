#!/usr/bin/env python3
"""Sensibilidad extendida y comparadores de diversificación sobre pool-30.

La ILD se evalúa siempre con los pesos principales para que las condiciones sean
comparables. Se añaden conteos exactos de firmas, tipos y enfoques como métricas
que no reutilizan la combinación continua optimizada por MMR.
"""
from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from statistics import fmean
from typing import Callable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.diversity_rerank import (  # noqa: E402
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_casebase,
    load_taxonomy_tree,
    normalize_text,
    parse_float,
    solution_similarity,
)

RUN = ROOT / ".build" / "diversity_comparison_1821_v12_pool30_revision"
CASEBASE_PATH = RUN / "cbr_data" / "CleanedDATA V12-05-2021.csv"
DIVERSITY_DIR = ROOT / "external" / "Diversity-Improvement-in-CBR"
OUT = ROOT / "paper" / "supplement" / "audit"
N = 1821
MAIN_WEIGHTS = tuple(DEFAULT_WEIGHTS)
WEIGHT_SCENARIOS = {
    "main_20_25_40_15": MAIN_WEIGHTS,
    "uniform_25_25_25_25": (0.25, 0.25, 0.25, 0.25),
    "model_heavy_10_15_65_10": (0.10, 0.15, 0.65, 0.10),
    "no_preprocessing_24_29_47_00": (0.24, 0.29, 0.47, 0.00),
}
LAMBDAS = [0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
POOL_SIZES = [10, 15, 20, 30]
TOP_KS = [3, 5, 10]


def read_rows(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "utf-8", "latin-1", "windows-1252"):
        try:
            with path.open(encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle, delimiter=";"))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode {path}")


casebase = load_casebase(CASEBASE_PATH)
taxonomy = build_taxonomy_index(load_taxonomy_tree(DIVERSITY_DIR))
sim_cache: dict[tuple[str, str, tuple[float, float, float, float]], float] = {}


def enriched(row: dict[str, str]) -> dict[str, str]:
    ref = str(row.get("Reference", "")).strip()
    merged = dict(casebase.get(ref, {}))
    merged.update({key: value for key, value in row.items() if str(value).strip()})
    return merged


def pair_sim(a: dict[str, str], b: dict[str, str], weights: tuple[float, float, float, float] = MAIN_WEIGHTS) -> float:
    ra, rb = str(a.get("Reference", "")).strip(), str(b.get("Reference", "")).strip()
    left, right = sorted((ra, rb))
    key = (left, right, tuple(weights))
    if key not in sim_cache:
        sim_cache[key] = solution_similarity(a, b, casebase, taxonomy, weights)
    return sim_cache[key]


def mmr(pool: list[dict[str, str]], *, k: int, lam: float, weights: tuple[float, float, float, float], keep_top1: bool) -> list[dict[str, str]]:
    candidates = pool[:]
    selected: list[dict[str, str]] = []
    if keep_top1 and candidates:
        selected.append(candidates.pop(0))
    while candidates and len(selected) < k:
        best_index = 0
        best_score = -math.inf
        for index, candidate in enumerate(candidates):
            relevance = parse_float(candidate.get("Sim"))
            redundancy = max((pair_sim(candidate, prior, weights) for prior in selected), default=0.0)
            score = lam * relevance - (1.0 - lam) * redundancy
            if score > best_score + 1e-15:
                best_score = score
                best_index = index
        selected.append(candidates.pop(best_index))
    return selected


def maxsum(pool: list[dict[str, str]], *, k: int, lam: float = 0.7) -> list[dict[str, str]]:
    candidates = pool[:]
    selected = [candidates.pop(0)]
    while candidates and len(selected) < k:
        best_index = 0
        best_score = -math.inf
        for index, candidate in enumerate(candidates):
            relevance = parse_float(candidate.get("Sim"))
            mean_distance = fmean(1.0 - pair_sim(candidate, prior) for prior in selected)
            score = lam * relevance + (1.0 - lam) * mean_distance
            if score > best_score + 1e-15:
                best_score = score
                best_index = index
        selected.append(candidates.pop(best_index))
    return selected


def exact_dedup(pool: list[dict[str, str]], *, k: int) -> list[dict[str, str]]:
    selected = [pool[0]]
    seen = {normalize_text(enriched(pool[0]).get("Models"))}
    deferred: list[dict[str, str]] = []
    for row in pool[1:]:
        signature = normalize_text(enriched(row).get("Models"))
        if signature and signature not in seen and len(selected) < k:
            selected.append(row)
            seen.add(signature)
        else:
            deferred.append(row)
    selected.extend(deferred[: max(0, k - len(selected))])
    return selected[:k]


def feature_tokens(row: dict[str, str]) -> frozenset[str]:
    data = enriched(row)
    tokens: set[str] = set()
    for field in ["Model Approach", "Model Type", "Models", "Data Pre-processing"]:
        value = normalize_text(data.get(field))
        if not value:
            continue
        tokens.add(f"{field}={value}")
        for token in re.findall(r"[a-z0-9]+", value):
            if len(token) > 1:
                tokens.add(f"{field}:{token}")
    return frozenset(tokens)


def token_cosine(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / math.sqrt(len(a) * len(b))


def dpp_lexical(pool: list[dict[str, str]], *, k: int, quality_scale: float = 3.0) -> list[dict[str, str]]:
    """Greedy MAP-DPP with a PSD cosine kernel over prefixed solution tokens."""
    n = len(pool)
    features = [feature_tokens(row) for row in pool]
    relevance = np.array([parse_float(row.get("Sim")) for row in pool], dtype=float)
    quality = np.exp(quality_scale * (relevance - relevance.max()))
    kernel = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            value = token_cosine(features[i], features[j])
            if i == j:
                value = 1.0
            kernel[i, j] = kernel[j, i] = value
    lmat = quality[:, None] * kernel * quality[None, :]
    lmat += np.eye(n) * 1e-9
    selected = [0]
    remaining = list(range(1, n))
    while remaining and len(selected) < k:
        best = remaining[0]
        best_logdet = -math.inf
        for candidate in remaining:
            subset = selected + [candidate]
            sign, logdet = np.linalg.slogdet(lmat[np.ix_(subset, subset)])
            score = float(logdet) if sign > 0 else -math.inf
            if score > best_logdet + 1e-12:
                best_logdet = score
                best = candidate
        selected.append(best)
        remaining.remove(best)
    return [pool[index] for index in selected]


def metrics(selected: list[dict[str, str]]) -> dict[str, float | int | bool]:
    sims = [parse_float(row.get("Sim")) for row in selected]
    enriched_rows = [enriched(row) for row in selected]
    model_signatures = [normalize_text(row.get("Models")) for row in enriched_rows if normalize_text(row.get("Models"))]
    model_types = [normalize_text(row.get("Model Type")) for row in enriched_rows if normalize_text(row.get("Model Type"))]
    approaches = [normalize_text(row.get("Model Approach")) for row in enriched_rows if normalize_text(row.get("Model Approach"))]
    pair_distances = [1.0 - pair_sim(a, b) for i, a in enumerate(selected) for b in selected[i + 1 :]]
    return {
        "mean_similarity": fmean(sims),
        "top1_similarity": sims[0],
        "ild_main_weights": fmean(pair_distances) if pair_distances else 0.0,
        "unique_model_signatures": len(set(model_signatures)),
        "unique_model_types": len(set(model_types)),
        "unique_model_approaches": len(set(approaches)),
        "has_duplicate_model_signature": len(model_signatures) != len(set(model_signatures)),
    }


def aggregate(method: str, settings: dict[str, object], values: list[dict[str, float | int | bool]]) -> dict[str, object]:
    row: dict[str, object] = {"method": method, **settings, "n_queries": len(values)}
    for key in ["mean_similarity", "top1_similarity", "ild_main_weights", "unique_model_signatures", "unique_model_types", "unique_model_approaches"]:
        row[key] = fmean(float(value[key]) for value in values)
    row["queries_with_duplicate_model_signature"] = sum(bool(value["has_duplicate_model_signature"]) for value in values)
    return row


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pools = [read_rows(RUN / "cbr_data" / f"pool_results_{index}.csv") for index in range(1, N + 1)]
    if any(len(pool) < 30 for pool in pools):
        raise RuntimeError("Expected pool-30 for every query")

    sensitivity_rows: list[dict[str, object]] = []
    for pool_size in POOL_SIZES:
        for top_k in TOP_KS:
            if top_k > pool_size:
                continue
            baseline = [metrics(pool[:top_k]) for pool in pools]
            sensitivity_rows.append(aggregate("CBR", {"pool_size": pool_size, "top_k": top_k, "lambda": 1.0, "keep_top1": True, "weights": "n/a"}, baseline))
            for lam in LAMBDAS:
                values = [metrics(mmr(pool[:pool_size], k=top_k, lam=lam, weights=MAIN_WEIGHTS, keep_top1=True)) for pool in pools]
                sensitivity_rows.append(aggregate("MMR", {"pool_size": pool_size, "top_k": top_k, "lambda": lam, "keep_top1": True, "weights": "main"}, values))

    for name, weights in WEIGHT_SCENARIOS.items():
        values = [metrics(mmr(pool[:15], k=5, lam=0.7, weights=weights, keep_top1=True)) for pool in pools]
        sensitivity_rows.append(aggregate("MMR_weight_sensitivity", {"pool_size": 15, "top_k": 5, "lambda": 0.7, "keep_top1": True, "weights": name}, values))
    values = [metrics(mmr(pool[:15], k=5, lam=0.7, weights=MAIN_WEIGHTS, keep_top1=False)) for pool in pools]
    sensitivity_rows.append(aggregate("MMR_no_top1_constraint", {"pool_size": 15, "top_k": 5, "lambda": 0.7, "keep_top1": False, "weights": "main"}, values))
    sensitivity = pd.DataFrame(sensitivity_rows)
    sensitivity.to_csv(OUT / "extended_mmr_sensitivity.csv", index=False)

    comparator_specs: list[tuple[str, Callable[[list[dict[str, str]]], list[dict[str, str]]]]] = [
        ("CBR top-5", lambda pool: pool[:5]),
        ("Exact signature dedup", lambda pool: exact_dedup(pool[:15], k=5)),
        ("MMR lambda=0.70", lambda pool: mmr(pool[:15], k=5, lam=0.7, weights=MAIN_WEIGHTS, keep_top1=True)),
        ("Greedy max-sum lambda=0.70", lambda pool: maxsum(pool[:15], k=5, lam=0.7)),
        ("Lexical MAP-DPP", lambda pool: dpp_lexical(pool[:15], k=5)),
    ]
    comparator_rows = []
    for name, selector in comparator_specs:
        values = [metrics(selector(pool)) for pool in pools]
        comparator_rows.append(aggregate(name, {"pool_size": 15, "top_k": 5, "lambda": "", "keep_top1": True, "weights": "main evaluation"}, values))
    comparators = pd.DataFrame(comparator_rows)
    comparators.to_csv(OUT / "strong_reranking_comparators.csv", index=False)

    main_pool = sensitivity[
        (sensitivity["method"] == "MMR")
        & (sensitivity["top_k"] == 5)
        & (sensitivity["lambda"] == 0.7)
        & (sensitivity["pool_size"].isin(POOL_SIZES))
    ].sort_values("pool_size")
    report_lines = [
        "# Sensibilidad extendida del reranking",
        "",
        "La ILD de todas las condiciones se recalculó con los pesos principales 0,20/0,25/0,40/0,15 para conservar comparabilidad.",
        "",
        "## Tamaño del pool (top-5, lambda=0,70, top-1 fijo)",
        "",
        "| Pool | Similitud media | ILD | Firmas únicas | Listas repetidas |",
        "|---:|---:|---:|---:|---:|",
    ]
    for row in main_pool.itertuples(index=False):
        report_lines.append(f"| {int(row.pool_size)} | {row.mean_similarity:.4f} | {row.ild_main_weights:.4f} | {row.unique_model_signatures:.3f} | {int(row.queries_with_duplicate_model_signature)} |")
    report_lines.extend([
        "",
        "## Comparadores fuertes",
        "",
        "| Método | Similitud | ILD principal | Firmas | Tipos | Enfoques | Listas repetidas |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in comparators.itertuples(index=False):
        report_lines.append(f"| {row.method} | {row.mean_similarity:.4f} | {row.ild_main_weights:.4f} | {row.unique_model_signatures:.3f} | {row.unique_model_types:.3f} | {row.unique_model_approaches:.3f} | {int(row.queries_with_duplicate_model_signature)} |")
    report_lines.extend([
        "",
        "xQuAD no se ejecutó porque el corpus no define intenciones/subtópicos por consulta. Una comparación CNN requiere modificar/reconstruir la memoria CBR y no es un reranker sobre el mismo pool; queda separada conceptualmente.",
    ])
    (OUT / "EXTENDED_RERANKING_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    metadata = {
        "run": str(RUN.relative_to(ROOT)),
        "queries": N,
        "pool_sizes": POOL_SIZES,
        "top_ks": TOP_KS,
        "lambdas": LAMBDAS,
        "main_weights": MAIN_WEIGHTS,
        "weight_scenarios": WEIGHT_SCENARIOS,
        "ild_evaluation_weights": MAIN_WEIGHTS,
    }
    (OUT / "extended_reranking_manifest.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print((OUT / "EXTENDED_RERANKING_REPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
