#!/usr/bin/env python3
"""Ablaciones de atributos y recencia sobre las consultas headless myCBR."""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from statistics import fmean

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pipeline.diversity_rerank as diversity_module  # noqa: E402
from pipeline.diversity_rerank import (  # noqa: E402
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_casebase,
    load_taxonomy_tree,
    normalize_text,
    parse_float,
    rerank_mmr,
    solution_similarity,
)

SOURCE_RUN = ROOT / ".build" / "diversity_comparison_1821_v12_no_default_sync"
BUILD = ROOT / ".build" / "cbr_ablation_revision"
OUT = ROOT / "paper" / "supplement" / "audit"
CASEBASE_PATH = SOURCE_RUN / "cbr_data" / "CleanedDATA V12-05-2021.csv"
DIVERSITY_DIR = ROOT / "external" / "Diversity-Improvement-in-CBR"
N = 1821
_original_solution_similarity = solution_similarity
_similarity_cache: dict[tuple[str, str], float] = {}


def cached_solution_similarity(a, b, casebase_by_ref, taxonomy_index, weights):
    left, right = sorted((str(a.get("Reference", "")).strip(), str(b.get("Reference", "")).strip()))
    key = (left, right)
    if key not in _similarity_cache:
        _similarity_cache[key] = _original_solution_similarity(a, b, casebase_by_ref, taxonomy_index, weights)
    return _similarity_cache[key]


diversity_module.solution_similarity = cached_solution_similarity
solution_similarity = cached_solution_similarity


def read_rows(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "utf-8", "latin-1", "windows-1252"):
        try:
            with path.open(encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle, delimiter=";"))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode {path}")


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def clear(row: dict[str, str], value_field: str, weight_field: str) -> None:
    row[value_field] = ""
    row[weight_field] = ""


def condition_rows(base: list[dict[str, str]], condition: str) -> list[dict[str, str]]:
    rows = [dict(row) for row in base]
    for row in rows:
        if condition == "task_year_only":
            for field, weight in [("Case study type", "w2"), ("Case study", "w3"), ("Online/Offline", "w4"), ("Input for the model", "w5"), ("Input type", "w6")]:
                clear(row, field, weight)
        elif condition == "task_asset_year":
            for field, weight in [("Case study type", "w2"), ("Online/Offline", "w4"), ("Input for the model", "w5"), ("Input type", "w6")]:
                clear(row, field, weight)
        elif condition == "task_input_year":
            for field, weight in [("Case study type", "w2"), ("Case study", "w3"), ("Online/Offline", "w4"), ("Input for the model", "w5")]:
                clear(row, field, weight)
        elif condition == "asset_input_year_no_task":
            clear(row, "Task", "w1")
        elif condition.startswith("main_year_"):
            row["Query Year"] = condition.rsplit("_", 1)[-1]
        elif condition != "main":
            raise ValueError(condition)
        row["Number of cases to retrieve"] = "15"
    return rows


def run_batch(input_path: Path, prefix: str) -> None:
    classpath = (ROOT / ".build" / "cbr" / "jar-classpath.txt").read_text(encoding="utf-8").strip()
    command = [
        "java", "-Djava.awt.headless=true", "-cp", classpath, "HeadlessCBR",
        "--data-dir", str(SOURCE_RUN / "cbr_data"), "query-batch", str(input_path), prefix,
    ]
    subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    base_queries = read_rows(SOURCE_RUN / "query_batch_input_pool.csv")
    conditions = [
        "main", "task_year_only", "task_asset_year", "task_input_year", "asset_input_year_no_task",
        "main_year_2021", "main_year_2025", "main_year_2027",
    ]
    data_dir = SOURCE_RUN / "cbr_data"
    outputs: dict[str, tuple[Path, str]] = {"main": (data_dir, "pool_results_")}
    for condition in conditions[1:]:
        condition_dir = BUILD / condition
        condition_dir.mkdir(exist_ok=True)
        input_path = condition_dir / "queries.csv"
        write_rows(input_path, condition_rows(base_queries, condition))
        prefix = f"ablation_{condition}_pool_results_"
        existing = list(data_dir.glob(f"{prefix}*.csv"))
        expected_complete = bool(existing) if condition == "asset_input_year_no_task" else len(existing) == N
        if not expected_complete:
            run_batch(input_path, prefix)
        outputs[condition] = (data_dir, prefix)

    casebase = load_casebase(CASEBASE_PATH)
    taxonomy = build_taxonomy_index(load_taxonomy_tree(DIVERSITY_DIR))
    main_top1: dict[int, str] = {}
    summary_rows: list[dict[str, object]] = []
    per_rows: list[dict[str, object]] = []
    for condition in conditions:
        baseline_values = []
        mmr_values = []
        baseline_patterns = Counter()
        mmr_patterns = Counter()
        top1_changed = 0
        for index in range(1, N + 1):
            output_dir, prefix = outputs[condition]
            result_path = output_dir / f"{prefix}{index}.csv"
            if not result_path.exists():
                continue
            rows = read_rows(result_path)[:15]
            if len(rows) < 5:
                continue
            baseline = rows[:5]
            mmr = [row for row, _score in rerank_mmr(rows, top_k=5, lambda_relevance=0.7, casebase_by_ref=casebase, taxonomy_index=taxonomy, weights=DEFAULT_WEIGHTS, keep_top1=True, pool_size=15)]

            def metrics(selected: list[dict[str, str]]) -> tuple[float, int, bool, float, str]:
                similarities = [parse_float(row.get("Sim")) for row in selected]
                signatures = []
                for row in selected:
                    ref = str(row.get("Reference", "")).strip()
                    value = normalize_text(casebase.get(ref, {}).get("Models") or row.get("Models"))
                    if value:
                        signatures.append(value)
                distances = [
                    1.0 - solution_similarity(a, b, casebase, taxonomy, DEFAULT_WEIGHTS)
                    for i, a in enumerate(selected) for b in selected[i + 1 :]
                ]
                refs = ",".join(str(row.get("Reference", "")).strip() for row in selected)
                return fmean(similarities), len(set(signatures)), len(signatures) != len(set(signatures)), fmean(distances), refs

            bm = metrics(baseline)
            dm = metrics(mmr)
            top1 = bm[4].split(",")[0]
            if condition == "main":
                main_top1[index] = top1
            elif top1 != main_top1[index]:
                top1_changed += 1
            baseline_values.append(bm)
            mmr_values.append(dm)
            baseline_patterns[bm[4]] += 1
            mmr_patterns[dm[4]] += 1
            per_rows.append({
                "condition": condition, "query_index": index, "baseline_refs": bm[4], "mmr_refs": dm[4],
                "baseline_mean_similarity": bm[0], "mmr_mean_similarity": dm[0],
                "baseline_ild": bm[3], "mmr_ild": dm[3], "baseline_unique_signatures": bm[1], "mmr_unique_signatures": dm[1],
            })
        summary_rows.append({
            "condition": condition,
            "n_queries": N,
            "successful_queries": len(baseline_values),
            "baseline_mean_similarity": fmean(value[0] for value in baseline_values),
            "mmr_mean_similarity": fmean(value[0] for value in mmr_values),
            "baseline_mean_ild": fmean(value[3] for value in baseline_values),
            "mmr_mean_ild": fmean(value[3] for value in mmr_values),
            "baseline_unique_signatures": fmean(value[1] for value in baseline_values),
            "mmr_unique_signatures": fmean(value[1] for value in mmr_values),
            "baseline_duplicate_lists": sum(value[2] for value in baseline_values),
            "mmr_duplicate_lists": sum(value[2] for value in mmr_values),
            "baseline_unique_ranking_patterns": len(baseline_patterns),
            "mmr_unique_ranking_patterns": len(mmr_patterns),
            "baseline_max_pattern_cluster": max(baseline_patterns.values()),
            "mmr_max_pattern_cluster": max(mmr_patterns.values()),
            "top1_changed_vs_main": top1_changed,
        })
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUT / "cbr_attribute_year_ablations.csv", index=False)
    pd.DataFrame(per_rows).to_csv(BUILD / "per_query_ablations.csv", index=False)
    lines = [
        "# Ablaciones de atributos y recencia myCBR", "",
        "| Condición | Éxito | Sim. CBR | Sim. MMR | ILD CBR | ILD MMR | Patrones CBR | Top-1 distinto |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary.itertuples(index=False):
        lines.append(f"| {row.condition} | {int(row.successful_queries)}/{int(row.n_queries)} | {row.baseline_mean_similarity:.4f} | {row.mmr_mean_similarity:.4f} | {row.baseline_mean_ild:.4f} | {row.mmr_mean_ild:.4f} | {int(row.baseline_unique_ranking_patterns)} | {int(row.top1_changed_vs_main)} |")
    lines.extend(["", "Estas ablaciones describen sensibilidad del motor heredado; no estiman relevancia humana."])
    (OUT / "CBR_ABLATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "cbr_ablation_manifest.json").write_text(json.dumps({"conditions": conditions, "queries": N, "pool": 15, "top_k": 5, "lambda": 0.7}, indent=2), encoding="utf-8")
    print((OUT / "CBR_ABLATION_REPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
