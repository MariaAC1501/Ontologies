#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# ///

"""Create blinded title/abstract screening sheets from a final Scopus union.

This script copies immutable candidate metadata into one CSV per reviewer. It
never makes eligibility decisions, assigns final corpus IDs, or overwrites an
existing batch directory.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REVIEWER_ID_RE = re.compile(r"[A-Za-z0-9_-]+\Z")
REVIEWER_HEADERS = [
    "screening_candidate_id",
    "scopus_paper_id",
    "doi",
    "title",
    "abstract",
    "year",
    "source_strata",
    "source_url",
    "screening_batch_id",
    "source_union_sha256",
    "protocol_version",
    "screening_stage",
    "reviewer_id",
    "decision",
    "primary_exclusion_reason",
    "exclusion_detail",
    "confidence",
    "full_text_url",
    "full_text_retrieval_date",
    "full_text_status",
    "bibliographic_match",
    "decision_date",
    "notes",
]


class InputError(ValueError):
    """Raised when a source union cannot initialize a screening batch."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(131_072):
            digest.update(chunk)
    return digest.hexdigest()


def read_union(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"Cannot read source union: {path}") from error
    if not isinstance(document, dict):
        raise InputError("Source union must be a JSON object")
    schema = document.get("schema_version")
    if not isinstance(schema, str) or not schema.startswith("opmad-pdm-pre-screening-union/"):
        raise InputError(f"Unsupported source-union schema: {schema!r}")
    if document.get("status") != "pre_screening_only":
        raise InputError("Source union is not marked pre_screening_only")
    records = document.get("records")
    if not isinstance(records, list) or not records:
        raise InputError("Source union has no candidate records")

    seen_ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise InputError(f"Candidate {index} is not an object")
        candidate_id = str(record.get("pre_screening_deduplication_key") or "").strip()
        paper_id = str(record.get("paperId") or "").strip()
        if not candidate_id or not paper_id:
            raise InputError(f"Candidate {index} lacks a screening or Scopus Paper ID")
        if candidate_id in seen_ids:
            raise InputError(f"Duplicate screening candidate ID: {candidate_id}")
        seen_ids.add(candidate_id)
        if not isinstance(record.get("source_strata"), list):
            raise InputError(f"Candidate {candidate_id} lacks source strata")

    expected_count = (document.get("counts") or {}).get("pre_screening_unique_candidates")
    if isinstance(expected_count, int) and expected_count != len(records):
        raise InputError("Source-union candidate count does not match its accounting")
    return document, records


def reviewer_row(
    record: dict[str, Any],
    *,
    batch_id: str,
    source_hash: str,
    protocol_version: str,
    reviewer_id: str,
) -> dict[str, str]:
    strata = record.get("source_strata") or []
    return {
        "screening_candidate_id": str(record["pre_screening_deduplication_key"]),
        "scopus_paper_id": str(record["paperId"]),
        "doi": str(record.get("doi") or ""),
        "title": str(record.get("title") or ""),
        "abstract": str(record.get("abstract") or ""),
        "year": str(record.get("year") or ""),
        "source_strata": ";".join(str(value) for value in strata),
        "source_url": str(record.get("url") or ""),
        "screening_batch_id": batch_id,
        "source_union_sha256": source_hash,
        "protocol_version": protocol_version,
        "screening_stage": "title_abstract",
        "reviewer_id": reviewer_id,
        "decision": "",
        "primary_exclusion_reason": "",
        "exclusion_detail": "",
        "confidence": "",
        "full_text_url": "",
        "full_text_retrieval_date": "",
        "full_text_status": "not_assessed",
        "bibliographic_match": "not_assessed",
        "decision_date": "",
        "notes": "",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEWER_HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--union-path", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--protocol-version", required=True)
    parser.add_argument(
        "--reviewer-id",
        action="append",
        default=None,
        help="Reviewer identifier; supply twice to override the R1/R2 default.",
    )
    parser.add_argument(
        "--created-at-utc",
        default=None,
        help="Optional ISO-8601 batch timestamp; defaults to the current UTC time.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.batch_id.strip() or not args.protocol_version.strip():
        raise InputError("batch ID and protocol version must be nonempty")
    reviewer_ids = args.reviewer_id or ["R1", "R2"]
    if len(reviewer_ids) != 2 or len(set(reviewer_ids)) != 2:
        raise InputError("Specify exactly two distinct reviewer IDs")
    if any(not REVIEWER_ID_RE.fullmatch(value) for value in reviewer_ids):
        raise InputError("Reviewer IDs may contain only letters, numbers, underscores, and hyphens")
    if args.output_dir.exists():
        raise InputError(f"Refusing to overwrite existing output directory: {args.output_dir}")

    document, records = read_union(args.union_path)
    source_hash = sha256_file(args.union_path)
    created_at = args.created_at_utc or utc_now()
    rows_by_reviewer = {
        reviewer_id: [
            reviewer_row(
                record,
                batch_id=args.batch_id,
                source_hash=source_hash,
                protocol_version=args.protocol_version,
                reviewer_id=reviewer_id,
            )
            for record in records
        ]
        for reviewer_id in reviewer_ids
    }

    args.output_dir.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{args.output_dir.name}.", dir=args.output_dir.parent))
    try:
        output_files = []
        for reviewer_id, rows in rows_by_reviewer.items():
            file_name = f"title_abstract_{reviewer_id}.csv"
            write_csv(temporary_dir / file_name, rows)
            output_files.append(file_name)
        manifest = {
            "schema_version": "opmad-pdm-human-screening-batch/v1",
            "screening_batch_id": args.batch_id,
            "protocol_version": args.protocol_version,
            "created_at_utc": created_at,
            "source_union_path": str(args.union_path),
            "source_union_sha256": source_hash,
            "source_union_schema_version": document["schema_version"],
            "candidate_id_field": "pre_screening_deduplication_key",
            "candidate_count": len(records),
            "reviewers": [{"reviewer_id": reviewer_id} for reviewer_id in reviewer_ids],
            "reviewer_files": output_files,
            "notes": "",
        }
        (temporary_dir / "batch_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary_dir.rename(args.output_dir)
    except Exception:
        shutil.rmtree(temporary_dir, ignore_errors=True)
        raise

    print(f"Created {args.output_dir} with {len(records)} candidates for {', '.join(reviewer_ids)}.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InputError as error:
        raise SystemExit(f"error: {error}")
