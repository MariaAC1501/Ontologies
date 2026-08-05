#!/usr/bin/env python3
"""Compara MMR con baselines simples sobre el pool-15 sin default de sincronización."""
from __future__ import annotations

import csv
import random
import sys
from collections import defaultdict
from pathlib import Path
from statistics import fmean, pstdev

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pipeline.diversity_rerank import (
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_casebase,
    load_taxonomy_tree,
    normalize_text,
    parse_float,
    read_csv_rows,
    solution_similarity,
)

RUN = ROOT / ".build" / "diversity_comparison_1821_v12_no_default_sync"
CASEBASE = RUN / "cbr_data" / "CleanedDATA V12-05-2021.csv"
DIVERSITY = ROOT / "external" / "Diversity-Improvement-in-CBR"
OUT = RUN / "statistical_analysis_outputs" / "alternative_baselines.csv"
N = 1821
TOP_K = 5
RANDOM_REPEATS = 100
RANDOM_SEED = 20260727

casebase = load_casebase(CASEBASE)
taxonomy = build_taxonomy_index(load_taxonomy_tree(DIVERSITY))
sim_cache: dict[tuple[str, str], float] = {}


def pair_sim(a: dict[str, str], b: dict[str, str]) -> float:
    ra, rb = a.get("Reference", ""), b.get("Reference", "")
    key = tuple(sorted((ra, rb)))
    if key not in sim_cache:
        sim_cache[key] = solution_similarity(a, b, casebase, taxonomy, DEFAULT_WEIGHTS)
    return sim_cache[key]


def metrics(selected: list[dict[str, str]]) -> tuple[float, int, bool, float]:
    similarities = [parse_float(r.get("Sim")) for r in selected]
    models = [normalize_text(r.get("Models")) for r in selected if normalize_text(r.get("Models"))]
    ild = fmean(1.0 - pair_sim(a, b) for i, a in enumerate(selected) for b in selected[i + 1 :])
    unique = len(set(models))
    return fmean(similarities), unique, unique < len(models), ild


def relevance_top5(pool: list[dict[str, str]]) -> list[dict[str, str]]:
    return pool[:TOP_K]


def exact_signature_dedup(pool: list[dict[str, str]]) -> list[dict[str, str]]:
    selected = [pool[0]]
    seen = {normalize_text(pool[0].get("Models"))}
    deferred: list[dict[str, str]] = []
    for row in pool[1:]:
        signature = normalize_text(row.get("Models"))
        if signature and signature not in seen and len(selected) < TOP_K:
            selected.append(row)
            seen.add(signature)
        else:
            deferred.append(row)
    if len(selected) < TOP_K:
        selected.extend(deferred[: TOP_K - len(selected)])
    return selected


def load_mmr(index: int) -> list[dict[str, str]]:
    return read_csv_rows(RUN / "with_diversity" / f"pool_results_{index}.diverse.csv")[1]


aggregates: dict[str, list[tuple[float, int, bool, float]]] = defaultdict(list)
pools: list[list[dict[str, str]]] = []
for i in range(1, N + 1):
    pool = read_csv_rows(RUN / "cbr_data" / f"pool_results_{i}.csv")[1]
    pools.append(pool)
    aggregates["CBR top-5"].append(metrics(relevance_top5(pool)))
    aggregates["Deduplicación exacta"].append(metrics(exact_signature_dedup(pool)))
    aggregates["MMR lambda=0.70"].append(metrics(load_mmr(i)))

# La unidad del resumen aleatorio es una repetición completa sobre las 1.821 consultas.
rng = random.Random(RANDOM_SEED)
random_run_means: list[tuple[float, float, float, float]] = []
for _ in range(RANDOM_REPEATS):
    per_query = []
    for pool in pools:
        selected = [pool[0], *rng.sample(pool[1:], TOP_K - 1)]
        per_query.append(metrics(selected))
    random_run_means.append(
        (
            fmean(x[0] for x in per_query),
            fmean(x[1] for x in per_query),
            fmean(float(x[2]) for x in per_query),
            fmean(x[3] for x in per_query),
        )
    )

rows: list[dict[str, object]] = []
for method, values in aggregates.items():
    rows.append(
        {
            "method": method,
            "n_queries": N,
            "random_repeats": 0,
            "mean_similarity_top5": fmean(v[0] for v in values),
            "mean_unique_model_signatures": fmean(v[1] for v in values),
            "queries_with_duplicate_signatures": sum(v[2] for v in values),
            "mean_intra_list_dissimilarity": fmean(v[3] for v in values),
            "replicate_sd_mean_similarity": 0.0,
            "replicate_sd_intra_list_dissimilarity": 0.0,
        }
    )
rows.append(
    {
        "method": "Aleatorio top-1 fijo",
        "n_queries": N,
        "random_repeats": RANDOM_REPEATS,
        "mean_similarity_top5": fmean(v[0] for v in random_run_means),
        "mean_unique_model_signatures": fmean(v[1] for v in random_run_means),
        "queries_with_duplicate_signatures": fmean(v[2] for v in random_run_means) * N,
        "mean_intra_list_dissimilarity": fmean(v[3] for v in random_run_means),
        "replicate_sd_mean_similarity": pstdev(v[0] for v in random_run_means),
        "replicate_sd_intra_list_dissimilarity": pstdev(v[3] for v in random_run_means),
    }
)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
print(OUT)
for row in rows:
    print(row)
