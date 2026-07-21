#!/usr/bin/env python3
"""Rerank CBR retrieval CSVs with diversity-aware MMR.

This module integrates the vendored ``external/Diversity-Improvement-in-CBR``
submodule as a post-processing stage for the current headless CBR flow.

The upstream Diversity project is GUI/research oriented and imports datasets at
module import time. To keep this repository's CLI deterministic and lightweight,
this script reuses its core idea (pairwise solution dissimilarity) and, when
available, reads its model taxonomy from ``Methods2.py`` without importing the
module. The reranker operates on CSV files produced by ``HeadlessCBR``.
"""

from __future__ import annotations

import argparse
import ast
import csv
import glob
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASEBASE_CSV = REPO_ROOT / (
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/"
    "CleanedDATA V21-07-2021.csv"
)
DEFAULT_DIVERSITY_SUBMODULE = REPO_ROOT / "external/Diversity-Improvement-in-CBR"
DEFAULT_WEIGHTS = (0.20, 0.25, 0.40, 0.15)  # approach, model type, models, preprocessing


@dataclass(frozen=True)
class RerankScores:
    cbr_rank: int
    cbr_score: float
    diversity_penalty: float
    diversity_score: float
    rerank_score: float


def normalize_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.strip().lower()
    text = text.replace("\ufeff", "")
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_token(value: object) -> str:
    text = normalize_text(value)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_float(value: object, default: float = 0.0) -> float:
    text = "" if value is None else str(value).strip()
    if not text:
        return default
    text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return default


def split_multi(value: object) -> list[str]:
    text = "" if value is None else str(value)
    # CBR fields use comma-separated multi-values. Keep model names with spaces.
    parts = re.split(r"\s*,\s*", text)
    return [part.strip() for part in parts if part.strip()]


def levenshtein_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i]
        for j, cb in enumerate(b, start=1):
            insert = current[j - 1] + 1
            delete = previous[j] + 1
            replace = previous[j - 1] + (0 if ca == cb else 1)
            current.append(min(insert, delete, replace))
        previous = current
    return previous[-1]


def levenshtein_similarity(a: object, b: object) -> float:
    left = normalize_text(a)
    right = normalize_text(b)
    if not left and not right:
        return 0.0
    if left == right:
        return 1.0
    max_len = max(len(left), len(right))
    if max_len == 0:
        return 0.0
    return max(0.0, 1.0 - levenshtein_distance(left, right) / max_len)


def token_jaccard(a: object, b: object) -> float:
    left = {token for token in normalize_token(a).split() if token}
    right = {token for token in normalize_token(b).split() if token}
    if not left and not right:
        return 0.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def field_similarity(a: object, b: object) -> float:
    if normalize_text(a) == normalize_text(b) and normalize_text(a):
        return 1.0
    return max(token_jaccard(a, b), levenshtein_similarity(a, b))


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    encodings = ("utf-8-sig", "utf-8", "latin-1", "windows-1252")
    last_error: Exception | None = None
    for encoding in encodings:
        try:
            with path.open("r", encoding=encoding, errors="strict", newline="") as handle:
                reader = csv.DictReader(handle, delimiter=";")
                rows = list(reader)
                return list(reader.fieldnames or []), rows
        except UnicodeDecodeError as exc:
            last_error = exc
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        rows = list(reader)
        if rows or reader.fieldnames:
            return list(reader.fieldnames or []), rows
    if last_error:
        raise last_error
    return [], []


def write_csv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_casebase(path: Path) -> dict[str, dict[str, str]]:
    _, rows = read_csv_rows(path)
    by_reference: dict[str, dict[str, str]] = {}
    for row in rows:
        ref = (row.get("Reference") or "").strip()
        if ref:
            by_reference[ref] = row
    return by_reference


def load_taxonomy_tree(diversity_submodule: Path) -> list[list[str]]:
    """Read ``Similarity.TaxonomyTree`` from Diversity's Methods2.py.

    Importing ``Methods2`` has heavy side effects and optional dependencies, so
    this uses AST literal extraction instead.
    """

    methods2 = diversity_submodule / "Methods2.py"
    if not methods2.exists():
        return []
    try:
        tree = ast.parse(methods2.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Attribute) and target.attr == "TaxonomyTree":
                try:
                    value = ast.literal_eval(node.value)
                except Exception:
                    continue
                if isinstance(value, list):
                    cleaned: list[list[str]] = []
                    for group in value:
                        if isinstance(group, list):
                            cleaned.append([str(item) for item in group])
                    return cleaned
    return []


def build_taxonomy_index(taxonomy_tree: list[list[str]]) -> dict[str, int]:
    index: dict[str, int] = {}
    for group_index, group in enumerate(taxonomy_tree):
        for item in group:
            token = normalize_token(item)
            if token:
                index[token] = group_index
    return index


def taxonomy_similarity(model_a: object, model_b: object, taxonomy_index: dict[str, int]) -> float | None:
    tokens_a = [normalize_token(part) for part in split_multi(model_a)]
    tokens_b = [normalize_token(part) for part in split_multi(model_b)]
    families_a = [taxonomy_index[token] for token in tokens_a if token in taxonomy_index]
    families_b = [taxonomy_index[token] for token in tokens_b if token in taxonomy_index]
    if not families_a or not families_b:
        return None

    best = 0.0
    for family_a in families_a:
        for family_b in families_b:
            distance = abs(family_a - family_b)
            if distance == 0:
                score = 1.0
            elif distance >= 6:
                score = 0.1
            elif 2 < distance < 5:
                score = 0.5
            elif distance < 2:
                score = 0.8
            else:
                score = 0.6
            best = max(best, score)
    return best


def model_similarity(model_a: object, model_b: object, taxonomy_index: dict[str, int]) -> float:
    if normalize_text(model_a) == normalize_text(model_b) and normalize_text(model_a):
        return 1.0
    tax = taxonomy_similarity(model_a, model_b, taxonomy_index)
    lexical = max(token_jaccard(model_a, model_b), levenshtein_similarity(model_a, model_b))
    if tax is None:
        return lexical
    return max(tax, lexical)


def row_value(row: dict[str, str], fallback: dict[str, str], *names: str) -> str:
    for name in names:
        value = (row.get(name) or "").strip()
        if value:
            return value
    for name in names:
        value = (fallback.get(name) or "").strip()
        if value:
            return value
    return ""


def solution_signature(row: dict[str, str], casebase_by_ref: dict[str, dict[str, str]]) -> dict[str, str]:
    ref = (row.get("Reference") or "").strip()
    fallback = casebase_by_ref.get(ref, {})
    return {
        "model_approach": row_value(row, fallback, "Model Approach"),
        "model_type": row_value(row, fallback, "Model Type"),
        "models": row_value(row, fallback, "Models"),
        "data_preprocessing": row_value(row, fallback, "Data Pre-processing"),
    }


def normalize_weights(weights: Iterable[float]) -> tuple[float, float, float, float]:
    values = tuple(float(value) for value in weights)
    if len(values) != 4:
        raise ValueError("solution weights must contain exactly 4 values")
    total = sum(values)
    if total <= 0:
        return DEFAULT_WEIGHTS
    return tuple(value / total for value in values)  # type: ignore[return-value]


def solution_similarity(
    row_a: dict[str, str],
    row_b: dict[str, str],
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
    weights: tuple[float, float, float, float],
) -> float:
    sig_a = solution_signature(row_a, casebase_by_ref)
    sig_b = solution_signature(row_b, casebase_by_ref)
    sims = (
        field_similarity(sig_a["model_approach"], sig_b["model_approach"]),
        field_similarity(sig_a["model_type"], sig_b["model_type"]),
        model_similarity(sig_a["models"], sig_b["models"], taxonomy_index),
        1.0 if normalize_text(sig_a["data_preprocessing"]) == normalize_text(sig_b["data_preprocessing"]) and normalize_text(sig_a["data_preprocessing"]) else 0.0,
    )
    return max(0.0, min(1.0, sum(sim * weight for sim, weight in zip(sims, weights))))


def rerank_mmr(
    rows: list[dict[str, str]],
    *,
    top_k: int,
    lambda_relevance: float,
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
    weights: tuple[float, float, float, float],
    keep_top1: bool,
    pool_size: int | None,
) -> list[tuple[dict[str, str], RerankScores]]:
    if top_k <= 0:
        return []
    lambda_relevance = max(0.0, min(1.0, lambda_relevance))
    pool = rows[:pool_size] if pool_size and pool_size > 0 else list(rows)
    if not pool:
        return []

    remaining = list(enumerate(pool, start=1))
    selected: list[tuple[int, dict[str, str], RerankScores]] = []

    if keep_top1 and remaining:
        rank, first = remaining.pop(0)
        rel = parse_float(first.get("Sim"), default=0.0)
        selected.append((rank, first, RerankScores(rank, rel, 0.0, 1.0, rel)))

    while remaining and len(selected) < top_k:
        best_index = 0
        best_scores: RerankScores | None = None
        best_key: tuple[float, float, int] | None = None

        for idx, (rank, row) in enumerate(remaining):
            rel = parse_float(row.get("Sim"), default=0.0)
            if selected:
                penalty = max(
                    solution_similarity(row, already, casebase_by_ref, taxonomy_index, weights)
                    for _, already, _ in selected
                )
            else:
                penalty = 0.0
            diversity_score = 1.0 - penalty
            score = (lambda_relevance * rel) - ((1.0 - lambda_relevance) * penalty)
            key = (score, rel, -rank)
            if best_key is None or key > best_key:
                best_key = key
                best_index = idx
                best_scores = RerankScores(rank, rel, penalty, diversity_score, score)

        rank, row = remaining.pop(best_index)
        assert best_scores is not None
        selected.append((rank, row, best_scores))

    return [(row, scores) for _, row, scores in selected]


def output_fieldnames(input_fieldnames: list[str]) -> list[str]:
    extras = [
        "cbr_rank",
        "cbr_score",
        "diversity_penalty",
        "diversity_score",
        "rerank_score",
        "rerank_method",
    ]
    return input_fieldnames + [field for field in extras if field not in input_fieldnames]


def output_path_for(input_path: Path, output_dir: Path, suffix: str) -> Path:
    return output_dir / f"{input_path.stem}{suffix}"


def process_file(
    input_path: Path,
    *,
    output_dir: Path,
    suffix: str,
    top_k: int,
    lambda_relevance: float,
    casebase_by_ref: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
    weights: tuple[float, float, float, float],
    keep_top1: bool,
    pool_size: int | None,
) -> dict[str, object]:
    fieldnames, rows = read_csv_rows(input_path)
    ranked = rerank_mmr(
        rows,
        top_k=top_k,
        lambda_relevance=lambda_relevance,
        casebase_by_ref=casebase_by_ref,
        taxonomy_index=taxonomy_index,
        weights=weights,
        keep_top1=keep_top1,
        pool_size=pool_size,
    )
    out_rows: list[dict[str, object]] = []
    for row, scores in ranked:
        out = dict(row)
        out.update(
            {
                "cbr_rank": scores.cbr_rank,
                "cbr_score": f"{scores.cbr_score:.6f}",
                "diversity_penalty": f"{scores.diversity_penalty:.6f}",
                "diversity_score": f"{scores.diversity_score:.6f}",
                "rerank_score": f"{scores.rerank_score:.6f}",
                "rerank_method": f"mmr(lambda={lambda_relevance:.3f})",
            }
        )
        out_rows.append(out)

    out_path = output_path_for(input_path, output_dir, suffix)
    write_csv_rows(out_path, output_fieldnames(fieldnames), out_rows)

    original_top_refs = [(row.get("Reference") or "").strip() for row in rows[:top_k]]
    reranked_refs = [(row.get("Reference") or "").strip() for row, _ in ranked]
    changed = original_top_refs != reranked_refs
    unique_models = len({normalize_text(row.get("Models")) for row, _ in ranked if normalize_text(row.get("Models"))})
    return {
        "input": str(input_path),
        "output": str(out_path),
        "input_rows": len(rows),
        "output_rows": len(out_rows),
        "changed_top_k_order": changed,
        "original_top_refs": original_top_refs,
        "reranked_refs": reranked_refs,
        "unique_models": unique_models,
    }


def expand_result_paths(patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        expanded = sorted(glob.glob(pattern))
        if expanded:
            paths.extend(Path(item) for item in expanded)
        else:
            path = Path(pattern)
            if path.exists():
                paths.append(path)
    return sorted({path.resolve() for path in paths})


def parse_weights(text: str) -> tuple[float, float, float, float]:
    values = [float(part.strip()) for part in text.split(",") if part.strip()]
    return normalize_weights(values)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diversity-aware reranking for HeadlessCBR CSV outputs.")
    parser.add_argument("--results", nargs="+", required=True, help="Result CSV path(s) or glob(s) from HeadlessCBR.")
    parser.add_argument("--casebase-csv", default=str(DEFAULT_CASEBASE_CSV), help="Reference CBR casebase CSV used to enrich result rows.")
    parser.add_argument("--diversity-submodule", default=str(DEFAULT_DIVERSITY_SUBMODULE), help="Path to external/Diversity-Improvement-in-CBR.")
    parser.add_argument("--output-dir", required=True, help="Directory where reranked CSV files will be written.")
    parser.add_argument("--suffix", default=".diverse.csv", help="Suffix appended to each input result stem.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of reranked rows to write per result CSV.")
    parser.add_argument("--pool-size", type=int, default=0, help="Maximum number of CBR candidates to consider; 0 means all rows.")
    parser.add_argument("--lambda-relevance", type=float, default=0.75, help="MMR relevance weight in [0,1]. Higher preserves CBR order more strongly.")
    parser.add_argument("--solution-weights", default=",".join(str(value) for value in DEFAULT_WEIGHTS), help="Comma-separated weights: model_approach,model_type,models,data_preprocessing.")
    parser.add_argument("--no-keep-top1", action="store_true", help="Allow MMR to move the original top-1 candidate.")
    parser.add_argument("--summary", help="Optional JSON summary output path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result_paths = expand_result_paths(args.results)
    if not result_paths:
        raise SystemExit("No result CSV files matched --results")

    casebase_by_ref = load_casebase(Path(args.casebase_csv))
    taxonomy_tree = load_taxonomy_tree(Path(args.diversity_submodule))
    taxonomy_index = build_taxonomy_index(taxonomy_tree)
    weights = parse_weights(args.solution_weights)
    output_dir = Path(args.output_dir)

    summaries = [
        process_file(
            path,
            output_dir=output_dir,
            suffix=args.suffix,
            top_k=args.top_k,
            lambda_relevance=args.lambda_relevance,
            casebase_by_ref=casebase_by_ref,
            taxonomy_index=taxonomy_index,
            weights=weights,
            keep_top1=not args.no_keep_top1,
            pool_size=args.pool_size if args.pool_size > 0 else None,
        )
        for path in result_paths
    ]

    report = {
        "method": "diversity-aware MMR post-processing",
        "diversity_submodule": str(Path(args.diversity_submodule).resolve()),
        "taxonomy_terms_loaded": len(taxonomy_index),
        "casebase_rows_loaded": len(casebase_by_ref),
        "inputs": len(result_paths),
        "top_k": args.top_k,
        "pool_size": args.pool_size if args.pool_size > 0 else "all",
        "lambda_relevance": args.lambda_relevance,
        "solution_weights": weights,
        "files_changed_top_k_order": sum(1 for item in summaries if item["changed_top_k_order"]),
        "files": summaries,
    }

    if args.summary:
        summary_path = Path(args.summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    else:
        print(json.dumps(report, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
