#!/usr/bin/env python3
"""Create a no-API experiment matrix for structured extraction conditions.

The matrix is a planning artifact only: it enumerates condition/scope/model arms,
records the sample size from ``sample_manifest.csv``, and writes planned commands
and output paths.  It does not call LLMs or external services.
"""

from __future__ import annotations

import argparse
import csv
import re
import shlex
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


DEFAULT_SAMPLE_MANIFEST = Path("paper/experiments/gold_sample/sample_manifest.csv")
DEFAULT_OUTPUT_DIR = Path("paper/experiments/matrix")
CONDITIONS = ("opmad_fixed", "generic_json", "llm_schema", "llm_ontology")
SCOPES = ("abstract", "sections", "fulltext")
RECORD_ID_COLUMNS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")
MATRIX_HEADERS = (
    "arm_id",
    "condition",
    "scope",
    "model",
    "sample_manifest",
    "record_count",
    "requires_llm_api",
    "uses_existing_facts",
    "planned_command",
    "predictions_output",
    "facts_output",
    "metrics_output",
    "status",
    "notes",
)


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def parse_models(raw: Sequence[str]) -> List[str]:
    models: List[str] = []
    for token in raw:
        for part in token.split(","):
            model = part.strip()
            if model and model not in models:
                models.append(model)
    if not models:
        raise UserError("--models must include at least one model name")
    return models


def read_sample_manifest(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        raise UserError(f"sample manifest not found: {path}")
    if not path.is_file():
        raise UserError(f"sample manifest is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise UserError(f"sample manifest has no header row: {path}")
            fieldnames = [name for name in reader.fieldnames if name is not None]
            rows: List[Dict[str, str]] = []
            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise UserError(
                        f"sample manifest row {row_number} has more values than header columns"
                    )
                rows.append({field: (row.get(field) or "") for field in fieldnames})
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode sample manifest as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read sample manifest {path}: {exc}") from exc

    if not rows:
        raise UserError(f"sample manifest contains no data rows: {path}")
    return fieldnames, rows


def choose_record_id(row: Dict[str, str], fallback_index: int) -> str:
    for column in RECORD_ID_COLUMNS:
        value = row.get(column, "").strip()
        if value:
            return value
    return f"sample-row-{fallback_index + 1}"


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-._")
    return cleaned or "unnamed"


def display_path(path: Path) -> str:
    return path.as_posix()


def quote_path(path: Path) -> str:
    return shlex.quote(display_path(path))


def quote_text(value: str) -> str:
    return shlex.quote(value)


def build_planned_command(
    condition: str,
    scope: str,
    model: str,
    sample_manifest: Path,
    predictions_output: Path,
    facts_output: Path,
) -> str:
    if condition == "opmad_fixed":
        return " ".join(
            [
                "python",
                "paper/experiments/predictions_from_facts.py",
                "--manifest",
                quote_path(sample_manifest),
                "--output",
                quote_path(predictions_output),
                "--ontology",
                "pipeline/seed_ontology/opmad_seed.ttl",
            ]
        )

    command = [
        "# PLAN ONLY:",
        "run-llm-extraction-adapter",
        "--condition",
        quote_text(condition),
        "--scope",
        quote_text(scope),
        "--model",
        quote_text(model),
        "--manifest",
        quote_path(sample_manifest),
        "--output",
        quote_path(predictions_output),
        "--facts-output-dir",
        quote_path(facts_output),
    ]
    if condition == "llm_schema":
        command.extend(["--schema", "pipeline/extraction_schema.py"])
    elif condition == "llm_ontology":
        command.extend(["--schema", "pipeline/extraction_schema.py"])
        command.extend(["--ontology", "pipeline/seed_ontology/opmad_seed.ttl"])
    return " ".join(command)


def build_matrix_rows(
    sample_manifest: Path, output_dir: Path, record_count: int, models: Sequence[str]
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for condition in CONDITIONS:
        for scope in SCOPES:
            for model in models:
                safe_model = safe_name(model)
                arm_id = f"{condition}__{scope}__{safe_model}"
                base = output_dir / "runs" / condition / scope / safe_model
                predictions_output = base / "predictions.jsonl"
                facts_output = base / "facts"
                metrics_output = base / "eval"
                requires_llm = condition != "opmad_fixed"
                uses_existing_facts = condition == "opmad_fixed"
                notes = (
                    "Deterministic baseline from manifest facts_file; model/scope are "
                    "retained for paired bookkeeping and no model is called."
                    if condition == "opmad_fixed"
                    else "LLM arm is declarative only; implement/approve an adapter before execution."
                )
                rows.append(
                    {
                        "arm_id": arm_id,
                        "condition": condition,
                        "scope": scope,
                        "model": model,
                        "sample_manifest": display_path(sample_manifest),
                        "record_count": str(record_count),
                        "requires_llm_api": "true" if requires_llm else "false",
                        "uses_existing_facts": "true" if uses_existing_facts else "false",
                        "planned_command": build_planned_command(
                            condition=condition,
                            scope=scope,
                            model=model,
                            sample_manifest=sample_manifest,
                            predictions_output=predictions_output,
                            facts_output=facts_output,
                        ),
                        "predictions_output": display_path(predictions_output),
                        "facts_output": display_path(facts_output),
                        "metrics_output": display_path(metrics_output),
                        "status": "planned-not-run",
                        "notes": notes,
                    }
                )
    return rows


def write_matrix(path: Path, rows: Sequence[Dict[str, str]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(MATRIX_HEADERS))
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        raise UserError(f"could not write matrix CSV {path}: {exc}") from exc


def condition_notes() -> List[str]:
    return [
        "- `opmad_fixed`: deterministic conversion of existing `facts_file` TTL outputs via `predictions_from_facts.py`.",
        "- `generic_json`: planned generic JSON extraction prompt without OPMAD-specific constraints.",
        "- `llm_schema`: planned LLM extraction constrained by the 19-field structured schema.",
        "- `llm_ontology`: planned LLM extraction with schema plus OPMAD ontology context.",
    ]


def scope_notes() -> List[str]:
    return [
        "- `abstract`: title/abstract-only evidence package when available.",
        "- `sections`: selected methods/results/maintenance-relevant sections.",
        "- `fulltext`: whole available paper text/PDF-derived text.",
    ]


def write_protocol(
    path: Path,
    sample_manifest: Path,
    fieldnames: Sequence[str],
    rows: Sequence[Dict[str, str]],
    models: Sequence[str],
    matrix_rows: Sequence[Dict[str, str]],
) -> None:
    record_ids = [choose_record_id(row, index) for index, row in enumerate(rows)]
    preview_ids = record_ids[:20]
    matrix_csv = path.parent / "matrix.csv"
    fixed_commands = [
        row["planned_command"]
        for row in matrix_rows
        if row["condition"] == "opmad_fixed" and row["scope"] == "fulltext"
    ]
    fixed_command = fixed_commands[0] if fixed_commands else (
        "python paper/experiments/predictions_from_facts.py "
        f"--manifest {quote_path(sample_manifest)} "
        f"--output {quote_path(path.parent / 'runs/opmad_fixed/fulltext/predictions.jsonl')} "
        "--ontology pipeline/seed_ontology/opmad_seed.ttl"
    )
    lines: List[str] = []
    lines.extend(
        [
            "# Experiment matrix protocol",
            "",
            "This protocol was generated without calling LLMs, web services, or paid APIs.",
            "The CSV matrix is a planning artifact; rows marked `planned-not-run` are not evidence of execution.",
            "",
            "## Inputs",
            "",
            f"- Sample manifest: `{display_path(sample_manifest)}`",
            f"- Records in sample: {len(rows)}",
            f"- Manifest columns: {', '.join(fieldnames)}",
            f"- Models: {', '.join(models)}",
            f"- Conditions: {', '.join(CONDITIONS)}",
            f"- Scopes: {', '.join(SCOPES)}",
            "",
            "## Conditions",
            "",
        ]
    )
    lines.extend(condition_notes())
    lines.extend(["", "## Scopes", ""])
    lines.extend(scope_notes())
    lines.extend(
        [
            "",
            "## Generated artifacts",
            "",
            f"- Matrix CSV: `{display_path(matrix_csv)}` ({len(matrix_rows)} planned arms)",
            "- Planned predictions outputs: `runs/<condition>/<scope>/<model>/predictions.jsonl`",
            "- Planned evaluation outputs: `runs/<condition>/<scope>/<model>/eval/`",
            "",
            "## Deterministic fixed-facts baseline",
            "",
            "The only generated command that can run without an LLM adapter is the fixed-facts baseline:",
            "",
            "```bash",
            fixed_command,
            "```",
            "",
            "If the matrix was built with concrete model names, the `opmad_fixed` rows keep those model labels only for paired bookkeeping; they still do not call a model.",
            "",
            "## Planned LLM arms",
            "",
            "Rows for `generic_json`, `llm_schema`, and `llm_ontology` contain `# PLAN ONLY:` commands. Replace `run-llm-extraction-adapter` with an approved runner before execution, set budgets, and log the provider/model/version separately.",
            "",
            "## Evaluation template",
            "",
            "```bash",
            "python paper/experiments/evaluate_extraction.py \\",
            "  --gold paper/experiments/gold_sample/gold_annotated.jsonl \\",
            "  --predictions <predictions_output_from_matrix> \\",
            "  --output-dir <metrics_output_from_matrix> \\",
            "  --fields reference,publication_year,task,case_study,case_study_type,input_for_model,number_of_input_variables,input_types,data_preprocessing,model_approach,model_types,models,module_synchronization,number_of_failure_modes,performance_indicator,performance,complementary_notes,study_title,publication_identifier",
            "```",
            "",
            "## Sample record-id preview",
            "",
        ]
    )
    if preview_ids:
        for record_id in preview_ids:
            lines.append(f"- `{record_id}`")
        if len(record_ids) > len(preview_ids):
            lines.append(f"- ... ({len(record_ids) - len(preview_ids)} additional records)")
    else:
        lines.append("- (none)")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as exc:
        raise UserError(f"could not write protocol README {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample-manifest",
        type=Path,
        required=True,
        help="Input sample_manifest.csv produced by prepare_gold_sample.py.",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        required=True,
        help="Model names to enumerate. Accepts space- or comma-separated values.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory for matrix.csv and README_protocol.md (default: {DEFAULT_OUTPUT_DIR}).",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    models = parse_models(args.models)
    fieldnames, sample_rows = read_sample_manifest(args.sample_manifest)
    matrix_rows = build_matrix_rows(
        sample_manifest=args.sample_manifest,
        output_dir=args.output_dir,
        record_count=len(sample_rows),
        models=models,
    )

    matrix_path = args.output_dir / "matrix.csv"
    protocol_path = args.output_dir / "README_protocol.md"
    write_matrix(matrix_path, matrix_rows)
    write_protocol(
        path=protocol_path,
        sample_manifest=args.sample_manifest,
        fieldnames=fieldnames,
        rows=sample_rows,
        models=models,
        matrix_rows=matrix_rows,
    )

    print("Experiment matrix prepared")
    print(f"  sample records: {len(sample_rows)}")
    print(f"  models: {', '.join(models)}")
    print(f"  planned arms: {len(matrix_rows)}")
    print(f"  wrote: {matrix_path}")
    print(f"  wrote: {protocol_path}")
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
