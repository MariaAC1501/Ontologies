#!/usr/bin/env python3
"""Prepare human annotation packets from frozen evidence JSONL.

This helper supports text-level validation: annotators read the evidence text used
by the extraction arms and fill a separate gold JSONL. It does not ask annotators
to verify PDF-to-text conversion fidelity.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

DEFAULT_FIELDS = (
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
    "study_title",
    "publication_identifier",
)
LIST_FIELDS = {"input_types", "model_types", "models"}
ID_FIELDS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def parse_fields(raw: Optional[Sequence[str]]) -> List[str]:
    if raw is None:
        return list(DEFAULT_FIELDS)
    fields: List[str] = []
    for token in raw:
        for part in token.split(","):
            field = part.strip()
            if field and field not in fields:
                fields.append(field)
    if not fields:
        raise UserError("--fields was provided but no fields were listed")
    return fields


def read_jsonl(path: Path) -> List[Tuple[int, Dict[str, Any]]]:
    if not path.exists():
        raise UserError(f"evidence JSONL not found: {path}")
    if not path.is_file():
        raise UserError(f"evidence JSONL path is not a file: {path}")
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
    except OSError as exc:
        raise UserError(f"could not read {path}: {exc}") from exc
    if not records:
        raise UserError(f"evidence JSONL contains no records: {path}")
    return records


def get_record_id(obj: Dict[str, Any], line_number: int) -> str:
    for key in ID_FIELDS:
        value = obj.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    metadata = obj.get("metadata")
    if isinstance(metadata, dict):
        for key in ID_FIELDS:
            value = metadata.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()
    return f"line-{line_number}"


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip()).strip("-._")
    return cleaned or "record"


def empty_gold(fields: Sequence[str]) -> Dict[str, Any]:
    return {field: ([] if field in LIST_FIELDS else None) for field in fields}


def metadata_value(metadata: Any, *path: str) -> str:
    current: Any = metadata
    for key in path:
        if not isinstance(current, dict):
            return ""
        current = current.get(key)
    if current is None:
        return ""
    if isinstance(current, (dict, list)):
        return json.dumps(current, ensure_ascii=False, sort_keys=True)
    return str(current)


def markdown_for_record(obj: Dict[str, Any], record_id: str, fields: Sequence[str]) -> str:
    metadata = obj.get("metadata", {})
    evidence_text = str(obj.get("evidence_text", ""))
    title = metadata_value(metadata, "bibliographic", "Title") or metadata_value(metadata, "sample_manifest_fields", "source_title")
    doi = metadata_value(metadata, "bibliographic", "DOI")
    scope = str(obj.get("scope", ""))
    template = {
        "record_id": record_id,
        "gold": empty_gold(fields),
        "gold_evidence": {field: "" for field in fields},
        "annotator_notes": "",
    }
    return (
        f"# Annotation evidence: {record_id}\n\n"
        "This is a text-level annotation packet. Do not verify PDF-to-text conversion; "
        "annotate only what is supported by the frozen evidence text below.\n\n"
        "## Metadata\n\n"
        f"- Title: {title}\n"
        f"- DOI: {doi}\n"
        f"- Scope: {scope}\n"
        f"- Corpus ID: {metadata_value(metadata, 'corpus_id')}\n"
        f"- PDF path (for reference only, not conversion validation): {metadata_value(metadata, 'pdf', 'file')}\n\n"
        "## Fields to annotate\n\n"
        + "\n".join(f"- `{field}`" for field in fields)
        + "\n\n## JSON object to fill in the gold file\n\n"
        "```json\n"
        + json.dumps(template, ensure_ascii=False, indent=2)
        + "\n```\n\n"
        "## Frozen evidence text\n\n"
        "```text\n"
        + evidence_text.rstrip()
        + "\n```\n"
    )


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True, help="Input evidence JSONL, usually evidence/fulltext/evidence.jsonl")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output annotation packet directory")
    parser.add_argument("--fields", nargs="*", help="Optional comma/space-separated fields to annotate")
    return parser


def run(args: argparse.Namespace) -> int:
    fields = parse_fields(args.fields)
    records = read_jsonl(args.evidence)
    docs_dir = args.output_dir / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)

    gold_rows: List[Dict[str, Any]] = []
    index_rows: List[Dict[str, str]] = []
    for line_number, obj in records:
        record_id = get_record_id(obj, line_number)
        metadata = obj.get("metadata", {})
        doc_path = docs_dir / f"{safe_name(record_id)}.md"
        doc_path.write_text(markdown_for_record(obj, record_id, fields), encoding="utf-8", newline="\n")
        row = {
            "record_id": record_id,
            "source_title": metadata_value(metadata, "bibliographic", "Title"),
            "evidence_file": str(doc_path),
            "gold": empty_gold(fields),
            "gold_evidence": {field: "" for field in fields},
            "annotator_notes": "",
        }
        gold_rows.append(row)
        index_rows.append({
            "record_id": record_id,
            "source_title": row["source_title"],
            "evidence_file": str(doc_path),
        })

    gold_template = args.output_dir / "gold_textlevel_template.jsonl"
    write_jsonl(gold_template, gold_rows)
    index_path = args.output_dir / "annotation_index.csv"
    with index_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["record_id", "source_title", "evidence_file"])
        writer.writeheader()
        writer.writerows(index_rows)

    readme = args.output_dir / "README.md"
    readme.write_text(
        "# Text-level human annotation packet\n\n"
        "Annotate against the frozen evidence files in `documents/`. Do not verify PDF-to-text conversion.\n\n"
        "Workflow:\n\n"
        "1. Copy `gold_textlevel_template.jsonl` to `gold_annotator_A.jsonl` and `gold_annotator_B.jsonl`.\n"
        "2. Each annotator reads `documents/<record_id>.md` and fills only the `gold`, `gold_evidence`, and `annotator_notes` fields.\n"
        "3. Adjudicate disagreements into `gold_adjudicated.jsonl`.\n"
        "4. Run `paper/experiments/evaluate_extraction.py` against predictions.\n",
        encoding="utf-8",
        newline="\n",
    )

    print("Annotation packet prepared")
    print(f"  records: {len(records)}")
    print(f"  fields: {', '.join(fields)}")
    print(f"  wrote: {index_path}")
    print(f"  wrote: {gold_template}")
    print(f"  documents: {docs_dir}")
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
