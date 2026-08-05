#!/usr/bin/env python3
"""Convert 19-field prediction JSONL records into HeadlessCBR batch queries.

The CLI prepares reproducible downstream CBR inputs for RQ5.  It reads one JSON
object per line with ``record_id`` and a ``prediction`` object using the canonical
19-field extraction schema, normalizes the query-bearing fields against the
legacy CBR case-base vocabulary, and writes:

* ``query_batch_input.csv``: semicolon-separated input for HeadlessCBR/GUI3
  ``query-batch``.
* ``query_metadata.csv``: per-input metadata aligned by row order.

It deliberately does not run Java, HeadlessCBR, or MMR reranking.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_CASEBASE_CSV = Path(
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data"
) / "CleanedDATA V12-05-2021.csv"
DEFAULT_QUERY_YEAR = 2026
DEFAULT_NUMBER_OF_CASES = 15
QUERY_BATCH_FILENAME = "query_batch_input.csv"
QUERY_METADATA_FILENAME = "query_metadata.csv"
METADATA_HEADERS = ("record_id", "normalization_notes", "active_field_count", "error")
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
EMPTY_NORMALIZED_QUERY = {
    "task": "",
    "case_study_type": "",
    "case_study": "",
    "online_offline": "",
    "input_for_model": "",
    "input_type": "",
}


class UserError(Exception):
    """Raised for user-facing CLI errors."""


@dataclass
class PredictionRecord:
    line_number: int
    record_id: str
    prediction: Dict[str, Any]
    errors: List[str]


CbrHelpers = Tuple[
    Sequence[str],
    Callable[[Dict[str, str], int, int], Dict[str, str]],
    Callable[..., Tuple[Dict[str, str], List[str]]],
    Callable[[Path], Dict[str, set[str]]],
]


def import_cbr_helpers() -> CbrHelpers:
    """Load the canonical CBR query helpers with a clear error on failure."""
    try:
        from scripts.compare_diversity_all_papers import (  # type: ignore
            QUERY_HEADERS,
            normalize_query,
            query_csv_row,
            read_reference_vocabulary,
        )
    except Exception as exc:  # pragma: no cover - exercised only in broken envs
        raise UserError(
            "could not import CBR query helpers from "
            "scripts.compare_diversity_all_papers. Run this script from the "
            "repository checkout and ensure the project dependencies are "
            f"available. Original error ({type(exc).__name__}): {exc}"
        ) from exc

    return QUERY_HEADERS, query_csv_row, normalize_query, read_reference_vocabulary


def resolve_repo_path(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded.resolve()
    return (ROOT / expanded).resolve()


def value_to_text(value: Any) -> str:
    """Render JSON scalar/list values deterministically for legacy CSV fields."""
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        parts = [value_to_text(item) for item in value]
        return ", ".join(part for part in parts if part)
    if isinstance(value, set):
        parts = sorted(value_to_text(item) for item in value)
        return ", ".join(part for part in parts if part)
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isfinite(value) and value.is_integer():
            return str(int(value))
        return str(value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return " ".join(str(value).split()).strip()


def number_to_text(value: Any) -> str:
    text = value_to_text(value)
    if not text:
        return ""
    try:
        number = float(text)
    except ValueError:
        return text
    if math.isfinite(number) and number.is_integer():
        return str(int(number))
    return text


def prediction_to_case_row(prediction: Dict[str, Any]) -> Dict[str, str]:
    """Map canonical prediction fields to the row shape expected by normalize_query."""
    return {
        "Task": value_to_text(prediction.get("task")),
        "Case study type": value_to_text(prediction.get("case_study_type")),
        "Case study": value_to_text(prediction.get("case_study")),
        "Online/Off-line": value_to_text(prediction.get("module_synchronization")),
        "Input for the model": value_to_text(prediction.get("input_for_model")),
        "Input type": value_to_text(prediction.get("input_types")),
        "Number of input variables": number_to_text(
            prediction.get("number_of_input_variables")
        ),
    }


def load_prediction_records(path: Path) -> List[PredictionRecord]:
    if not path.exists():
        raise UserError(f"predictions JSONL not found: {path}")
    if not path.is_file():
        raise UserError(f"predictions JSONL path is not a file: {path}")

    records: List[PredictionRecord] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue

                record_id = f"line:{line_number}"
                prediction: Dict[str, Any] = {}
                errors: List[str] = []
                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError as exc:
                    errors.append(
                        f"invalid JSON at line {line_number}, column {exc.colno}: {exc.msg}"
                    )
                else:
                    if not isinstance(obj, dict):
                        errors.append("top-level JSON value is not an object")
                    else:
                        raw_record_id = obj.get("record_id")
                        if raw_record_id is None or not str(raw_record_id).strip():
                            errors.append("missing record_id")
                        else:
                            record_id = str(raw_record_id).strip()

                        raw_prediction = obj.get("prediction")
                        if not isinstance(raw_prediction, dict):
                            errors.append("missing or invalid prediction object")
                        else:
                            prediction = raw_prediction
                            missing = [
                                field
                                for field in CANONICAL_FIELDS
                                if field not in raw_prediction
                            ]
                            if missing:
                                errors.append(
                                    "missing canonical prediction fields: "
                                    + ", ".join(missing)
                                )

                records.append(
                    PredictionRecord(
                        line_number=line_number,
                        record_id=record_id,
                        prediction=prediction,
                        errors=errors,
                    )
                )
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode predictions JSONL as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read predictions JSONL {path}: {exc}") from exc

    if not records:
        raise UserError(f"predictions JSONL has no records: {path}")
    return records


def semicolon_cell(value: Any) -> str:
    return value_to_text(value).replace(";", ",").replace("\r", " ").replace("\n", " ")


def write_semicolon_rows(
    path: Path, headers: Sequence[str], rows: Sequence[Dict[str, Any]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(";".join(semicolon_cell(header) for header in headers) + "\n")
        for row in rows:
            handle.write(
                ";".join(semicolon_cell(row.get(header, "")) for header in headers) + "\n"
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        required=True,
        help="Input predictions JSONL with record_id and a 19-field prediction object.",
    )
    parser.add_argument(
        "--casebase-csv",
        type=Path,
        default=DEFAULT_CASEBASE_CSV,
        help=f"CBR case-base CSV used for vocabulary normalization (default: {DEFAULT_CASEBASE_CSV}).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help=(
            "Output directory for query_batch_input.csv and query_metadata.csv. "
            "Existing files with those names are overwritten."
        ),
    )
    parser.add_argument(
        "--query-year",
        type=int,
        default=DEFAULT_QUERY_YEAR,
        help=f"Query year passed to myCBR recency similarity (default: {DEFAULT_QUERY_YEAR}).",
    )
    parser.add_argument(
        "--number-of-cases",
        type=int,
        default=DEFAULT_NUMBER_OF_CASES,
        help=f"Number of CBR cases to retrieve per query (default: {DEFAULT_NUMBER_OF_CASES}).",
    )
    parser.add_argument(
        "--drop-default-synchronization",
        action="store_true",
        help="Treat the bridge default 'Unknown synchronization' as missing.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    if args.number_of_cases <= 0:
        raise UserError("--number-of-cases must be positive")

    query_headers, query_csv_row, normalize_query, read_reference_vocabulary = import_cbr_helpers()

    predictions_path = args.predictions.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    casebase_path = resolve_repo_path(args.casebase_csv)
    if not casebase_path.is_file():
        raise UserError(f"case-base CSV not found: {casebase_path}")

    records = load_prediction_records(predictions_path)
    try:
        vocabulary = read_reference_vocabulary(casebase_path)
    except Exception as exc:
        raise UserError(
            f"could not read reference vocabulary from {casebase_path}: "
            f"{type(exc).__name__}: {exc}"
        ) from exc

    query_rows: List[Dict[str, str]] = []
    metadata_rows: List[Dict[str, Any]] = []
    records_with_errors = 0
    total_active_fields = 0

    for record in records:
        record_errors = list(record.errors)
        normalization_notes = ""
        active_field_count = 0
        normalized_query = dict(EMPTY_NORMALIZED_QUERY)

        if record.prediction:
            case_row = prediction_to_case_row(record.prediction)
        else:
            case_row = prediction_to_case_row({})

        try:
            normalized_query, notes = normalize_query(
                case_row,
                vocabulary,
                drop_default_synchronization=args.drop_default_synchronization,
            )
            normalization_notes = " | ".join(notes)
            active_field_count = sum(1 for value in normalized_query.values() if value)
        except Exception as exc:
            record_errors.append(
                f"normalization failed: {type(exc).__name__}: {exc}"
            )
            normalized_query = dict(EMPTY_NORMALIZED_QUERY)
            normalization_notes = ""
            active_field_count = 0

        try:
            query_row = query_csv_row(
                normalized_query,
                args.number_of_cases,
                args.query_year,
            )
        except Exception as exc:
            record_errors.append(f"query row build failed: {type(exc).__name__}: {exc}")
            query_row = query_csv_row(
                dict(EMPTY_NORMALIZED_QUERY),
                args.number_of_cases,
                args.query_year,
            )
            active_field_count = 0

        if record_errors:
            records_with_errors += 1
        total_active_fields += active_field_count
        query_rows.append(query_row)
        metadata_rows.append(
            {
                "record_id": record.record_id,
                "normalization_notes": normalization_notes,
                "active_field_count": str(active_field_count),
                "error": " | ".join(record_errors),
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    query_batch_path = output_dir / QUERY_BATCH_FILENAME
    metadata_path = output_dir / QUERY_METADATA_FILENAME
    write_semicolon_rows(query_batch_path, query_headers, query_rows)
    write_semicolon_rows(metadata_path, METADATA_HEADERS, metadata_rows)

    print("CBR query inputs prepared")
    print(f"  input records: {len(records)}")
    print(f"  records with errors: {records_with_errors}")
    print(f"  total active query fields: {total_active_fields}")
    print(f"  wrote: {query_batch_path}")
    print(f"  wrote: {metadata_path}")
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
