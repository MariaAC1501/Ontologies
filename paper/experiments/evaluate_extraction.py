#!/usr/bin/env python3
"""Evaluate structured extraction predictions against expert gold JSONL.

The evaluator compares per-record, per-field sets of normalized values. Values may
be scalars or lists. Normalization uses only the Python standard library:
casefolding, Unicode normalization, punctuation-to-space, and whitespace collapse.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


DEFAULT_OUTPUT_DIR = Path("paper/experiments/eval")
ID_FIELDS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")
GOLD_CONTAINERS = ("gold", "annotation", "annotations", "fields")
PREDICTION_CONTAINERS = (
    "prediction",
    "predictions",
    "predicted",
    "extraction",
    "extracted",
    "fields",
)
RESERVED_TOP_LEVEL_KEYS = {
    *ID_FIELDS,
    *GOLD_CONTAINERS,
    *PREDICTION_CONTAINERS,
    "annotator_notes",
    "corpus_id",
    "facts_file",
    "manifest",
    "metadata",
    "meta",
    "notes",
    "pdf_file",
    "source_title",
    "strata",
    "title",
}


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def parse_field_list(raw: Optional[Sequence[str]]) -> Optional[List[str]]:
    if raw is None:
        return None
    fields: List[str] = []
    for comma_part in " ".join(raw).split(","):
        for part in comma_part.split():
            field = part.strip()
            if field and field not in fields:
                fields.append(field)
    return fields


def load_jsonl(path: Path) -> List[Tuple[int, Dict[str, Any]]]:
    if not path.exists():
        raise UserError(f"JSONL file not found: {path}")
    if not path.is_file():
        raise UserError(f"JSONL path is not a file: {path}")

    records: List[Tuple[int, Dict[str, Any]]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    raise UserError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
                if not isinstance(obj, dict):
                    raise UserError(f"{path}:{line_number}: expected a JSON object")
                records.append((line_number, obj))
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode JSONL as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read JSONL {path}: {exc}") from exc

    if not records:
        raise UserError(f"JSONL file has no records: {path}")
    return records


def get_record_id(obj: Dict[str, Any], line_number: int) -> str:
    for key in ID_FIELDS:
        value = obj.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()

    manifest = obj.get("manifest")
    if isinstance(manifest, dict):
        for key in ID_FIELDS:
            value = manifest.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()

    # Last-resort fallback supports paired JSONL files with identical ordering.
    return f"line:{line_number}"


def extract_payload(obj: Dict[str, Any], kind: str) -> Dict[str, Any]:
    containers = GOLD_CONTAINERS if kind == "gold" else PREDICTION_CONTAINERS
    for key in containers:
        value = obj.get(key)
        if isinstance(value, dict):
            return value
        if value is not None and not isinstance(value, dict):
            raise UserError(f"{kind} container {key!r} must be an object when present")

    # Convenience fallback for JSONL records where fields live at top level.
    payload = {
        key: value
        for key, value in obj.items()
        if key not in RESERVED_TOP_LEVEL_KEYS and not key.startswith("_")
    }
    return payload


def index_records(
    records: Sequence[Tuple[int, Dict[str, Any]]], kind: str
) -> Tuple[List[str], Dict[str, Dict[str, Any]]]:
    order: List[str] = []
    index: Dict[str, Dict[str, Any]] = {}
    for line_number, obj in records:
        record_id = get_record_id(obj, line_number)
        if record_id in index:
            raise UserError(f"duplicate {kind} record_id {record_id!r}")
        order.append(record_id)
        index[record_id] = extract_payload(obj, kind)
    return order, index


def normalize_text(value: Any) -> str:
    text = str(value)
    text = unicodedata.normalize("NFKC", text).casefold()
    chars: List[str] = []
    for char in text:
        if unicodedata.category(char).startswith("P"):
            chars.append(" ")
        else:
            chars.append(char)
    return " ".join("".join(chars).split())


def iter_scalar_values(value: Any) -> Iterable[Any]:
    if value is None:
        return
    if isinstance(value, list):
        for item in value:
            yield from iter_scalar_values(item)
        return
    if isinstance(value, tuple):
        for item in value:
            yield from iter_scalar_values(item)
        return
    if isinstance(value, dict):
        yield json.dumps(value, ensure_ascii=False, sort_keys=True)
        return
    yield value


def value_set(value: Any) -> Set[str]:
    normalized: Set[str] = set()
    for item in iter_scalar_values(value):
        text = normalize_text(item)
        if text:
            normalized.add(text)
    return normalized


def safe_divide(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def prf(tp: int, fp: int, fn: int) -> Dict[str, float]:
    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    hallucination_rate = safe_divide(fp, tp + fp)
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "hallucination_rate": hallucination_rate,
    }


def fmt_float(value: float) -> str:
    return f"{value:.6f}"


def evaluate(
    gold_order: Sequence[str],
    gold_index: Dict[str, Dict[str, Any]],
    prediction_index: Dict[str, Dict[str, Any]],
    fields: Sequence[str],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    field_stats: Dict[str, Dict[str, int]] = {
        field: {
            "tp": 0,
            "fp": 0,
            "fn": 0,
            "exact_count": 0,
            "gold_items": 0,
            "predicted_items": 0,
        }
        for field in fields
    }

    record_exact_count = 0
    matched_prediction_records = 0

    for record_id in gold_order:
        gold_payload = gold_index[record_id]
        prediction_payload = prediction_index.get(record_id, {})
        if record_id in prediction_index:
            matched_prediction_records += 1

        record_exact = True
        for field in fields:
            gold_values = value_set(gold_payload.get(field))
            predicted_values = value_set(prediction_payload.get(field))

            tp = len(gold_values & predicted_values)
            fp = len(predicted_values - gold_values)
            fn = len(gold_values - predicted_values)

            stats = field_stats[field]
            stats["tp"] += tp
            stats["fp"] += fp
            stats["fn"] += fn
            stats["gold_items"] += len(gold_values)
            stats["predicted_items"] += len(predicted_values)
            if gold_values == predicted_values:
                stats["exact_count"] += 1
            else:
                record_exact = False

        if record_exact:
            record_exact_count += 1

    field_rows: List[Dict[str, Any]] = []
    totals = {"tp": 0, "fp": 0, "fn": 0, "gold_items": 0, "predicted_items": 0}
    record_count = len(gold_order)
    for field in fields:
        stats = field_stats[field]
        metrics = prf(stats["tp"], stats["fp"], stats["fn"])
        exact_match = safe_divide(stats["exact_count"], record_count)
        field_rows.append(
            {
                "field": field,
                "records": record_count,
                "tp": stats["tp"],
                "fp": stats["fp"],
                "fn": stats["fn"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
                "exact_match": exact_match,
                "hallucination_rate": metrics["hallucination_rate"],
                "gold_items": stats["gold_items"],
                "predicted_items": stats["predicted_items"],
            }
        )
        for key in totals:
            totals[key] += stats[key]

    summary_metrics = prf(totals["tp"], totals["fp"], totals["fn"])
    extra_prediction_records = sorted(set(prediction_index) - set(gold_order))
    missing_prediction_records = sorted(set(gold_order) - set(prediction_index))
    summary: Dict[str, Any] = {
        "record_count": record_count,
        "prediction_record_count": len(prediction_index),
        "matched_prediction_records": matched_prediction_records,
        "missing_prediction_records": len(missing_prediction_records),
        "extra_prediction_records": len(extra_prediction_records),
        "fields": list(fields),
        "tp": totals["tp"],
        "fp": totals["fp"],
        "fn": totals["fn"],
        "precision": summary_metrics["precision"],
        "recall": summary_metrics["recall"],
        "f1": summary_metrics["f1"],
        "exact_match": safe_divide(record_exact_count, record_count),
        "record_exact_match_count": record_exact_count,
        "hallucination_rate": summary_metrics["hallucination_rate"],
        "gold_items": totals["gold_items"],
        "predicted_items": totals["predicted_items"],
        "normalization": "Unicode NFKC, casefold, punctuation replaced by spaces, whitespace collapsed",
    }
    if missing_prediction_records:
        summary["missing_prediction_record_ids"] = missing_prediction_records[:50]
    if extra_prediction_records:
        summary["extra_prediction_record_ids"] = extra_prediction_records[:50]

    return summary, field_rows


def choose_fields(
    requested: Optional[List[str]],
    gold_index: Dict[str, Dict[str, Any]],
    prediction_index: Dict[str, Dict[str, Any]],
) -> List[str]:
    if requested is not None:
        if not requested:
            raise UserError("--fields was provided but no fields were listed")
        return requested

    discovered: Set[str] = set()
    for payload in list(gold_index.values()) + list(prediction_index.values()):
        discovered.update(str(key) for key in payload.keys())
    fields = sorted(discovered)
    if not fields:
        raise UserError(
            "no fields found. Add annotations under a 'gold' object and predictions "
            "under a 'prediction' object, or pass --fields."
        )
    return fields


def write_outputs(
    output_dir: Path, summary: Dict[str, Any], field_rows: Sequence[Dict[str, Any]]
) -> Tuple[Path, Path]:
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise UserError(f"could not create output directory {output_dir}: {exc}") from exc

    metrics_path = output_dir / "metrics.json"
    field_metrics_path = output_dir / "field_metrics.csv"

    try:
        with metrics_path.open("w", encoding="utf-8") as handle:
            json.dump(summary, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        with field_metrics_path.open("w", encoding="utf-8", newline="") as handle:
            fieldnames = [
                "field",
                "records",
                "tp",
                "fp",
                "fn",
                "precision",
                "recall",
                "f1",
                "exact_match",
                "hallucination_rate",
                "gold_items",
                "predicted_items",
            ]
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in field_rows:
                formatted = dict(row)
                for key in ("precision", "recall", "f1", "exact_match", "hallucination_rate"):
                    formatted[key] = fmt_float(float(formatted[key]))
                writer.writerow(formatted)
    except OSError as exc:
        raise UserError(f"could not write evaluation outputs in {output_dir}: {exc}") from exc

    return metrics_path, field_metrics_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate prediction JSONL against expert gold JSONL."
    )
    parser.add_argument("--gold", type=Path, required=True, help="Expert gold JSONL")
    parser.add_argument(
        "--predictions", type=Path, required=True, help="Prediction JSONL to evaluate"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--fields",
        nargs="*",
        default=None,
        help="Optional comma/space-separated fields to evaluate. Defaults to all discovered fields.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    gold_records = load_jsonl(args.gold)
    prediction_records = load_jsonl(args.predictions)

    gold_order, gold_index = index_records(gold_records, "gold")
    _, prediction_index = index_records(prediction_records, "prediction")
    fields = choose_fields(parse_field_list(args.fields), gold_index, prediction_index)

    summary, field_rows = evaluate(gold_order, gold_index, prediction_index, fields)
    summary["gold_path"] = str(args.gold)
    summary["predictions_path"] = str(args.predictions)

    metrics_path, field_metrics_path = write_outputs(args.output_dir, summary, field_rows)

    print("Extraction evaluation complete")
    print(f"  records: {summary['record_count']}")
    print(f"  fields: {', '.join(fields)}")
    print(f"  precision: {summary['precision']:.6f}")
    print(f"  recall: {summary['recall']:.6f}")
    print(f"  f1: {summary['f1']:.6f}")
    print(f"  exact_match: {summary['exact_match']:.6f}")
    print(f"  hallucination_rate: {summary['hallucination_rate']:.6f}")
    print(f"  wrote: {metrics_path}")
    print(f"  wrote: {field_metrics_path}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except UserError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
