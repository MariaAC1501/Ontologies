#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# ///

"""Build a validated pre-screening union from complete Scopus query runs.

S1a may include repeated complete API passes when unstable pagination emits
repeated Scopus Paper IDs. Their unique-ID union is accepted only when it
exactly equals the stable source-reported total. This script is deliberately
limited to database-record deduplication: it does not apply eligibility
criteria, assign final corpus IDs, or make study-inclusion decisions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "opmad-pdm-pre-screening-union/v2"
SUMMARY_SCHEMA_VERSION = "opmad-pdm-pre-screening-accounting/v2"
WHITESPACE_RE = re.compile(r"\s+")
TITLE_RE = re.compile(r"[^a-z0-9]+")


class InputError(ValueError):
    """Raised when an input cannot support a complete pre-screening union."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(131_072):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def normalize_doi(value: Any) -> str:
    text = str(value or "").strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text.rstrip(".,;)")


def normalize_title(value: Any) -> str:
    return TITLE_RE.sub(" ", str(value or "").casefold()).strip()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise InputError(f"Cannot read JSON input: {path}") from error
    if not isinstance(value, dict):
        raise InputError(f"Input is not a JSON object: {path}")
    return value


def validate_commit_marker(result_path: Path) -> dict[str, Any]:
    marker_path = result_path.with_name(
        f".{result_path.name}.ACADEMIC_SEARCH_COMMIT.json"
    )
    marker = read_json(marker_path)
    if marker.get("schema") != "academic_search_output_commit_marker_v1":
        raise InputError(f"Unsupported or missing commit-marker schema: {marker_path}")
    json_receipt = marker.get("normalized_json")
    csv_receipt = marker.get("normalized_csv")
    if not isinstance(json_receipt, dict) or not isinstance(csv_receipt, dict):
        raise InputError(f"Incomplete commit marker: {marker_path}")
    if (
        json_receipt.get("sha256") != sha256_file(result_path)
        or json_receipt.get("bytes") != result_path.stat().st_size
    ):
        raise InputError(f"JSON does not match its commit marker: {result_path}")
    csv_name = csv_receipt.get("file_name")
    if not isinstance(csv_name, str) or Path(csv_name).name != csv_name:
        raise InputError(f"Unsafe or missing CSV name in commit marker: {marker_path}")
    csv_path = result_path.with_name(csv_name)
    if (
        not csv_path.is_file()
        or csv_receipt.get("sha256") != sha256_file(csv_path)
        or csv_receipt.get("bytes") != csv_path.stat().st_size
    ):
        raise InputError(f"CSV does not match its commit marker: {csv_path}")
    return {
        "commit_marker_file": marker_path.name,
        "commit_marker_sha256": sha256_file(marker_path),
        "commit_marker_bytes": marker_path.stat().st_size,
        "csv_file": csv_path.name,
        "csv_sha256": sha256_file(csv_path),
        "csv_bytes": csv_path.stat().st_size,
    }


def validate_complete_run(
    *, label: str, result_path: Path, query_path: Path
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    data = read_json(result_path)
    metadata = data.get("output_metadata")
    rows = data.get("results")
    if not isinstance(metadata, dict) or not isinstance(rows, list):
        raise InputError(f"{label} lacks output metadata or a result list")
    if metadata.get("source") != "Scopus":
        raise InputError(f"{label} is not a Scopus result")
    if metadata.get("status") != "success" or metadata.get("retrieval_complete") is not True:
        raise InputError(f"{label} is not a complete successful retrieval")
    total = data.get("total")
    retrieved = data.get("results_retrieved")
    if not isinstance(total, int) or total < 0 or total != retrieved or total != len(rows):
        raise InputError(f"{label} has inconsistent total and retained-record counts")
    try:
        archived_query = query_path.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError(f"Cannot read archived query for {label}: {query_path}") from error
    executed_query = data.get("executed_query")
    if not isinstance(executed_query, str) or normalize_whitespace(executed_query) != normalize_whitespace(archived_query):
        raise InputError(f"{label} executed query does not match its archived query file")
    marker_receipt = validate_commit_marker(result_path)
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise InputError(f"{label} row {index} is not an object")
        if not str(row.get("paperId") or "").strip():
            raise InputError(f"{label} row {index} has no Scopus Paper ID")
    receipt = {
        "label": label,
        "result_file": result_path.name,
        "result_sha256": sha256_file(result_path),
        "result_bytes": result_path.stat().st_size,
        **marker_receipt,
        "query_file": query_path.name,
        "query_sha256": sha256_file(query_path),
        "query_bytes": query_path.stat().st_size,
        "source_reported_total": total,
        "records_retrieved": retrieved,
        "pages_retrieved": data.get("pages_retrieved"),
        "executed_at_utc": metadata.get("extracted_at"),
        "retrieval_complete": True,
        "stopped_reason": metadata.get("stopped_reason"),
        "prisma_run_id": (metadata.get("prisma_search_run") or {}).get("run_id")
        if isinstance(metadata.get("prisma_search_run"), dict)
        else None,
    }
    return data, rows, receipt


def reconcile_s1a_passes(
    passes: list[tuple[list[dict[str, Any]], dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Reconcile repeated complete S1a pages without inflating source counts."""
    if not passes:
        raise InputError("At least one complete S1a pass is required")
    source_totals = {receipt["source_reported_total"] for _, receipt in passes}
    if len(source_totals) != 1:
        raise InputError("S1a source-reported totals changed across recovery passes")
    source_total = source_totals.pop()
    canonical_by_paper_id: dict[str, dict[str, Any]] = {}
    reconciled_rows: list[dict[str, Any]] = []
    pass_receipts: list[dict[str, Any]] = []
    for rows, receipt in passes:
        paper_ids = [str(row["paperId"]).strip() for row in rows]
        pass_receipt = dict(receipt)
        pass_receipt["unique_scopus_paper_ids"] = len(set(paper_ids))
        pass_receipt["repeated_page_rows"] = len(paper_ids) - len(set(paper_ids))
        pass_receipts.append(pass_receipt)
        for row in rows:
            paper_id = str(row["paperId"]).strip()
            existing = canonical_by_paper_id.get(paper_id)
            if existing is None:
                canonical_by_paper_id[paper_id] = row
                reconciled_rows.append(row)
                continue
            if normalize_doi(existing.get("doi")) != normalize_doi(row.get("doi")):
                raise InputError(
                    f"S1a recovery passes disagree on the DOI for Scopus Paper ID {paper_id}"
                )
    if len(reconciled_rows) != source_total:
        raise InputError(
            "S1a recovery-pass unique Scopus Paper IDs do not equal the stable source total"
        )
    return reconciled_rows, {
        "label": "S1a",
        "source_reported_total": source_total,
        "records_retrieved": len(reconciled_rows),
        "pages_retrieved": sum(
            receipt.get("pages_retrieved", 0)
            for _, receipt in passes
            if isinstance(receipt.get("pages_retrieved"), int)
        ),
        "retrieval_complete": True,
        "stopped_reason": "reconciled_complete_passes",
        "reconciliation_mode": "unique_scopus_paper_id_union_of_complete_passes",
        "reconciliation_pass_count": len(passes),
        "reconciliation_passes": pass_receipts,
    }


def source_membership(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_strata": [record["_stratum"]],
        "source_ranks": {record["_stratum"]: [record.get("rank")]},
        "source_paper_ids": {record["_stratum"]: [record["paperId"]]},
    }


def merge_membership(canonical: dict[str, Any], duplicate: dict[str, Any]) -> None:
    stratum = duplicate["_stratum"]
    if stratum not in canonical["source_strata"]:
        canonical["source_strata"].append(stratum)
    ranks = canonical["source_ranks"].setdefault(stratum, [])
    if duplicate.get("rank") not in ranks:
        ranks.append(duplicate.get("rank"))
    paper_ids = canonical["source_paper_ids"].setdefault(stratum, [])
    if duplicate["paperId"] not in paper_ids:
        paper_ids.append(duplicate["paperId"])


def record_copy(record: dict[str, Any], deduplication_key: str) -> dict[str, Any]:
    output = {
        key: deepcopy(value)
        for key, value in record.items()
        if key != "_stratum"
    }
    output.update(source_membership(record))
    output["pre_screening_deduplication_key"] = deduplication_key
    return output


def write_new_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    encoded = (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def build_union(
    runs: list[tuple[str, list[dict[str, Any]]]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    """Deduplicate in documented order: EID, DOI, then title/year fallback."""
    canonical_by_paper_id: dict[str, dict[str, Any]] = {}
    canonical_by_doi: dict[str, dict[str, Any]] = {}
    canonical_by_title_year: dict[tuple[str, int], dict[str, Any]] = {}
    union: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()

    for stratum, rows in runs:
        for raw_record in rows:
            record = dict(raw_record)
            record["_stratum"] = stratum
            paper_id = str(record["paperId"]).strip()
            doi = normalize_doi(record.get("doi"))
            title = normalize_title(record.get("title"))
            year = record.get("year")
            title_year = (title, year) if title and isinstance(year, int) else None

            existing = canonical_by_paper_id.get(paper_id)
            rule = "Scopus Paper ID"
            if existing is None and doi:
                existing = canonical_by_doi.get(doi)
                rule = "normalized DOI"
            # Title/year is used only when an identifier is unavailable, or
            # when the same title/year has no competing identifier. This avoids
            # silently merging distinct studies that happen to share a title.
            if existing is None and not doi and not paper_id and title_year:
                existing = canonical_by_title_year.get(title_year)
                rule = "normalized title plus publication year"

            if existing is None:
                dedup_key = f"eid:{paper_id}"
                output = record_copy(record, dedup_key)
                union.append(output)
                canonical_by_paper_id[paper_id] = output
                if doi:
                    canonical_by_doi[doi] = output
                if title_year:
                    canonical_by_title_year[title_year] = output
                continue

            merge_membership(existing, record)
            counts[rule] += 1
            events.append(
                {
                    "rule": rule,
                    "canonical_paper_id": existing["paperId"],
                    "duplicate_paper_id": paper_id,
                    "duplicate_stratum": stratum,
                    "canonical_strata": list(existing["source_strata"]),
                    "doi": doi or None,
                    "normalized_title": title or None,
                    "publication_year": year if isinstance(year, int) else None,
                }
            )

    # A title/year collision with two distinct nonempty DOI/EID values is not
    # merged. It is documented for later review instead.
    title_collisions: Counter[tuple[str, int]] = Counter()
    title_ids: dict[tuple[str, int], set[str]] = {}
    for record in union:
        title = normalize_title(record.get("title"))
        year = record.get("year")
        if title and isinstance(year, int):
            key = (title, year)
            title_collisions[key] += 1
            title_ids.setdefault(key, set()).add(str(record.get("paperId") or ""))
    unresolved_title_collisions = sum(
        1 for key, count in title_collisions.items() if count > 1 and len(title_ids[key]) > 1
    )
    counts["unresolved_title_collisions"] = unresolved_title_collisions
    return union, events, dict(counts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s1a-json", required=True, type=Path)
    parser.add_argument(
        "--s1a-repeat-json",
        action="append",
        type=Path,
        default=[],
        help="Additional complete S1a pass to reconcile by Scopus Paper ID",
    )
    parser.add_argument("--s1a-query", required=True, type=Path)
    parser.add_argument("--s1b-json", required=True, type=Path)
    parser.add_argument("--s1b-query", required=True, type=Path)
    parser.add_argument("--union-output-path", required=True, type=Path)
    parser.add_argument("--summary-output-path", required=True, type=Path)
    args = parser.parse_args()

    if args.union_output_path.resolve() == args.summary_output_path.resolve():
        parser.error("union and summary outputs must differ")

    s1a_passes: list[tuple[list[dict[str, Any]], dict[str, Any]]] = []
    for index, path in enumerate([args.s1a_json, *args.s1a_repeat_json], start=1):
        _, rows, receipt = validate_complete_run(
            label=f"S1a-pass-{index}", result_path=path, query_path=args.s1a_query
        )
        s1a_passes.append((rows, receipt))
    s1a_rows, s1a_receipt = reconcile_s1a_passes(s1a_passes)
    _, s1b_rows, s1b_receipt = validate_complete_run(
        label="S1b", result_path=args.s1b_json, query_path=args.s1b_query
    )
    union, events, event_counts = build_union([("S1a", s1a_rows), ("S1b", s1b_rows)])

    raw_rows = len(s1a_rows) + len(s1b_rows)
    within_s1a_paper_id_duplicates = sum(
        event["rule"] == "Scopus Paper ID"
        and event["duplicate_stratum"] == "S1a"
        and event["canonical_paper_id"] == event["duplicate_paper_id"]
        for event in events
    )
    within_s1b_paper_id_duplicates = sum(
        event["rule"] == "Scopus Paper ID"
        and event["duplicate_stratum"] == "S1b"
        and event["canonical_paper_id"] == event["duplicate_paper_id"]
        and event["canonical_strata"] == ["S1b"]
        for event in events
    )
    cross_stratum_paper_id_duplicates = sum(
        event["rule"] == "Scopus Paper ID"
        and event["duplicate_stratum"] == "S1b"
        and event["canonical_paper_id"] == event["duplicate_paper_id"]
        and "S1a" in event["canonical_strata"]
        for event in events
    )
    doi_duplicates = sum(
        event["rule"] == "normalized DOI"
        and event["canonical_paper_id"] != event["duplicate_paper_id"]
        for event in events
    )
    title_merges = event_counts.get("normalized title plus publication year", 0)
    counted_duplicates = (
        within_s1a_paper_id_duplicates
        + within_s1b_paper_id_duplicates
        + cross_stratum_paper_id_duplicates
        + doi_duplicates
        + title_merges
    )
    counts = {
        "raw_rows_s1a": len(s1a_rows),
        "raw_rows_s1b": len(s1b_rows),
        "raw_rows_total": raw_rows,
        "within_s1a_scopus_paper_id_duplicates": within_s1a_paper_id_duplicates,
        "within_s1b_scopus_paper_id_duplicates": within_s1b_paper_id_duplicates,
        "cross_stratum_scopus_paper_id_duplicates": cross_stratum_paper_id_duplicates,
        "doi_duplicates_with_distinct_scopus_paper_ids": doi_duplicates,
        "normalized_title_year_merges": title_merges,
        "total_duplicate_rows_removed": len(events),
        "unresolved_normalized_title_year_collisions": event_counts.get("unresolved_title_collisions", 0),
        "pre_screening_unique_candidates": len(union),
    }
    if raw_rows - len(events) != len(union) or counted_duplicates != len(events):
        raise InputError("Deduplication accounting does not reconcile")

    common = {
        "status": "pre_screening_only",
        "scope_note": "Database-record deduplication only; title/abstract and full-text eligibility screening have not started.",
        "deduplication_policy": [
            "Merge exact Scopus Paper IDs.",
            "Then merge exact normalized DOIs when Paper IDs differ.",
            "Use normalized title plus publication year only when both identifier types are unavailable; retain and report identifier-bearing title collisions for review.",
        ],
        "source_runs": [s1a_receipt, s1b_receipt],
        "counts": counts,
        "deduplication_events": events,
        "generated_at_utc": utc_now(),
    }
    summary = {"schema_version": SUMMARY_SCHEMA_VERSION, **common}
    union_document = {
        "schema_version": SCHEMA_VERSION,
        **common,
        "records": union,
    }
    write_new_json(args.summary_output_path, summary)
    try:
        write_new_json(args.union_output_path, union_document)
    except Exception:
        # The summary is an independently valid no-overwrite record of the
        # failed attempt; do not delete it or replace an existing destination.
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
