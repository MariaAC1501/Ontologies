#!/usr/bin/env python3
"""Build 19-field prediction JSONL records from manifest-listed TTL facts.

The script is intentionally deterministic and does not call external APIs.  It
reads a sample or extraction manifest, loads each row's ``facts_file`` Turtle file
with ``pipeline.facts_to_csv``, converts the first extracted case for that file,
and writes one JSON object per manifest row.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.facts_to_csv import graph_to_cases, load_graph_from_ttl, parse_ontology_labels


DEFAULT_ONTOLOGY = Path("pipeline/seed_ontology/opmad_seed.ttl")
DEFAULT_OUTPUT = Path("paper/experiments/predictions.jsonl")
FACTS_COLUMN = "facts_file"
RECORD_ID_COLUMNS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")
CANONICAL_FIELDS = (
    "reference",
    "publication_year",
    "task",
    "case_study",
    "case_study_type",
    "input_for_model",
    "number_of_input_variables",
    "input_types",
    "data_preprocessing",
    "model_approach",
    "model_types",
    "models",
    "module_synchronization",
    "number_of_failure_modes",
    "performance_indicator",
    "performance",
    "complementary_notes",
    "study_title",
    "publication_identifier",
)
LIST_FIELDS = {"input_types", "model_types", "models"}


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def read_manifest(path: Path) -> Tuple[List[str], List[Tuple[int, Dict[str, str]]]]:
    if not path.exists():
        raise UserError(f"manifest not found: {path}")
    if not path.is_file():
        raise UserError(f"manifest is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise UserError(f"manifest has no header row: {path}")
            fieldnames = [name for name in reader.fieldnames if name is not None]
            if FACTS_COLUMN not in fieldnames:
                raise UserError(f"manifest must contain a {FACTS_COLUMN!r} column: {path}")

            rows: List[Tuple[int, Dict[str, str]]] = []
            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise UserError(
                        f"manifest row {row_number} has more values than header columns"
                    )
                rows.append((row_number, {field: (row.get(field) or "") for field in fieldnames}))
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode manifest as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read manifest {path}: {exc}") from exc

    if not rows:
        raise UserError(f"manifest contains no data rows: {path}")
    return fieldnames, rows


def candidate_paths(value: str, manifest_path: Path) -> Iterable[Path]:
    """Yield plausible filesystem paths for a manifest-relative value."""
    normalized = value.strip().replace("\\", os.sep)
    if not normalized:
        return

    candidate = Path(normalized).expanduser()
    if candidate.is_absolute():
        yield candidate
        return

    bases: List[Path] = [Path.cwd(), manifest_path.parent]
    bases.extend(manifest_path.parent.parents)

    seen = set()
    for base in bases:
        full = (base / candidate).resolve()
        if full not in seen:
            seen.add(full)
            yield full


def resolve_existing_path(value: str, manifest_path: Path) -> Optional[Path]:
    for path in candidate_paths(value, manifest_path):
        if path.exists() and path.is_file():
            return path
    return None


def choose_record_id(
    row: Dict[str, str], row_number: int, fallback_index: int, requested_column: Optional[str]
) -> str:
    if requested_column:
        value = row.get(requested_column, "").strip()
        if value:
            return value
        return f"manifest-row-{row_number}"

    for column in RECORD_ID_COLUMNS:
        value = row.get(column, "").strip()
        if value:
            return value
    return f"manifest-row-{row_number or fallback_index + 1}"


def empty_prediction() -> Dict[str, Any]:
    return {
        field: ([] if field in LIST_FIELDS else None)
        for field in CANONICAL_FIELDS
    }


def case_to_prediction(case: Any) -> Dict[str, Any]:
    prediction: Dict[str, Any] = {}
    for field in CANONICAL_FIELDS:
        value = getattr(case, field)
        if field in LIST_FIELDS:
            value = list(value)
        prediction[field] = value
    return prediction


def build_record(
    row: Dict[str, str],
    row_number: int,
    fallback_index: int,
    manifest_path: Path,
    ontology_labels: Dict[str, str],
    record_id_column: Optional[str],
) -> Tuple[Dict[str, Any], List[str]]:
    record_id = choose_record_id(row, row_number, fallback_index, record_id_column)
    facts_value = row.get(FACTS_COLUMN, "").strip()
    errors: List[str] = []
    resolved_facts_file = ""
    prediction = empty_prediction()
    case_count = 0

    try:
        if not facts_value:
            raise UserError(f"missing {FACTS_COLUMN!r} value")
        facts_path = resolve_existing_path(facts_value, manifest_path)
        if facts_path is None:
            raise UserError(f"facts TTL not found or not a file: {facts_value}")
        resolved_facts_file = str(facts_path)

        graph = load_graph_from_ttl(facts_path)
        cases = graph_to_cases(graph, ontology_labels)
        case_count = len(cases)
        if not cases:
            raise UserError(f"no cases extracted from facts TTL: {facts_path}")
        prediction = case_to_prediction(cases[0])
    except Exception as exc:  # per-record isolation is the purpose of this CLI
        errors.append(str(exc))

    record: Dict[str, Any] = {
        "record_id": record_id,
        "prediction": prediction,
        "metadata": {
            "manifest_row_number": row_number,
            "facts_file": facts_value,
            "resolved_facts_file": resolved_facts_file,
            "case_index": 0 if case_count else None,
            "case_count": case_count,
            "errors": errors,
        },
    }
    return record, errors


def write_jsonl(path: Path, records: Sequence[Dict[str, Any]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise UserError(f"could not write predictions JSONL {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
        help="Input sample_manifest.csv or extraction_manifest.csv containing facts_file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output predictions JSONL path (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        default=DEFAULT_ONTOLOGY,
        help=f"Ontology TTL for label lookup (default: {DEFAULT_ONTOLOGY}).",
    )
    parser.add_argument(
        "--record-id-column",
        help=(
            "Optional manifest column to use as record_id. Defaults to the first "
            "available of record_id, corpus_id, paper_id, doc_id, id."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Abort on the first per-record conversion error instead of recording it.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    manifest_path = args.manifest
    fieldnames, rows = read_manifest(manifest_path)

    if args.record_id_column and args.record_id_column not in fieldnames:
        raise UserError(
            f"--record-id-column {args.record_id_column!r} not found in manifest"
        )

    try:
        ontology_labels = parse_ontology_labels(args.ontology)
    except Exception as exc:
        raise UserError(f"could not parse ontology labels from {args.ontology}: {exc}") from exc

    records: List[Dict[str, Any]] = []
    error_count = 0
    for index, (row_number, row) in enumerate(rows):
        record, errors = build_record(
            row=row,
            row_number=row_number,
            fallback_index=index,
            manifest_path=manifest_path,
            ontology_labels=ontology_labels,
            record_id_column=args.record_id_column,
        )
        if errors:
            error_count += 1
            if args.strict:
                raise UserError(
                    f"{record['record_id']} (manifest row {row_number}): {'; '.join(errors)}"
                )
        records.append(record)

    write_jsonl(args.output, records)

    print("Predictions from facts prepared")
    print(f"  manifest rows: {len(rows)}")
    print(f"  successful records: {len(rows) - error_count}")
    print(f"  records with errors: {error_count}")
    print(f"  canonical fields: {len(CANONICAL_FIELDS)}")
    print(f"  wrote: {args.output}")
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
