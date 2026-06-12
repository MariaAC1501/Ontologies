#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///

"""Merge and deduplicate saved academic search result JSON files into a single corpus file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ARXIV_ID_RE = re.compile(r"(?:arxiv:)?(\d{4}\.\d{4,5}|[a-z\-]+/\d{7})(?:v\d+)?", re.IGNORECASE)
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def normalize_text(value: str) -> str:
    return NON_ALNUM_RE.sub(" ", (value or "").lower()).strip()


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.removeprefix("https://doi.org/")
    value = value.removeprefix("http://doi.org/")
    value = value.removeprefix("doi:")
    return value.strip()


def extract_arxiv_id(*values: Any) -> str:
    for value in values:
        text = str(value or "")
        match = ARXIV_ID_RE.search(text)
        if match:
            return match.group(1).lower()
    return ""


def infer_source(path: Path) -> str:
    stem = path.stem.lower()
    if "semantic" in stem:
        return "semantic_scholar"
    if "scopus" in stem:
        return "scopus"
    if "arxiv" in stem:
        return "arxiv"
    if "google" in stem and "scholar" in stem:
        return "google_scholar"
    return "unknown"


def iter_input_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser()
        if path.is_dir():
            files.extend(sorted(p for p in path.glob("*.json") if p.is_file()))
        elif path.is_file():
            files.append(path)
        else:
            print(f"Warning: input not found, skipping: {path}", file=sys.stderr)
    return files


def choose_better(existing: Any, candidate: Any) -> Any:
    if existing in (None, "", [], {}):
        return candidate
    if candidate in (None, "", [], {}):
        return existing
    if isinstance(existing, str) and isinstance(candidate, str):
        return candidate if len(candidate) > len(existing) else existing
    if isinstance(existing, list) and isinstance(candidate, list):
        return candidate if len(candidate) > len(existing) else existing
    if isinstance(existing, dict) and isinstance(candidate, dict):
        return candidate if len(candidate) > len(existing) else existing
    return candidate if candidate else existing


def make_dedup_key(record: dict[str, Any]) -> str:
    doi = normalize_doi(record.get("doi", ""))
    if doi:
        return f"doi:{doi}"

    arxiv_id = extract_arxiv_id(record.get("paperId"), record.get("doi"), record.get("openAccess_pdf", {}).get("url"))
    if arxiv_id:
        return f"arxiv:{arxiv_id}"

    title = normalize_text(record.get("title", ""))
    year = record.get("year") or ""
    if title:
        return f"title:{title}|year:{year}"

    paper_id = str(record.get("paperId", "")).strip()
    if paper_id:
        return f"paperid:{paper_id.lower()}"

    return f"fallback:{hash(json.dumps(record, sort_keys=True, ensure_ascii=False))}"


def load_search_file(path: Path) -> dict[str, Any]:
    with path.open() as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected top-level JSON object in {path}")
    return data


def merge_records(files: list[Path]) -> dict[str, Any]:
    merged: dict[str, dict[str, Any]] = {}
    inputs: list[dict[str, Any]] = []
    total_raw_results = 0

    for path in files:
        data = load_search_file(path)
        source = infer_source(path)
        results = data.get("results", []) or []
        if not isinstance(results, list):
            raise ValueError(f"Expected 'results' list in {path}")

        input_summary = {
            "path": str(path),
            "source": source,
            "query": data.get("query", ""),
            "total": data.get("total", 0),
            "results_retrieved": data.get("results_retrieved", len(results)),
            "results_in_file": len(results),
        }
        inputs.append(input_summary)

        for rank, raw in enumerate(results, start=1):
            if not isinstance(raw, dict):
                continue
            total_raw_results += 1
            record = {
                "paperId": raw.get("paperId", ""),
                "doi": normalize_doi(raw.get("doi", "")),
                "title": raw.get("title", ""),
                "authors": raw.get("authors", []) or [],
                "year": raw.get("year"),
                "abstract": raw.get("abstract", ""),
                "citationCount": raw.get("citationCount", 0) or 0,
                "openAccess_pdf": raw.get("openAccess_pdf", {}) or {},
            }
            dedup_key = make_dedup_key(record)
            provenance = {
                "source": source,
                "input_file": str(path),
                "query": data.get("query", ""),
                "rank": rank,
                "paperId": record.get("paperId", ""),
            }

            if dedup_key not in merged:
                merged[dedup_key] = {
                    **record,
                    "dedup_key": dedup_key,
                    "duplicate_count": 1,
                    "sources": [source],
                    "provenance": [provenance],
                }
                continue

            existing = merged[dedup_key]
            for field in ["paperId", "doi", "title", "authors", "year", "abstract", "openAccess_pdf"]:
                existing[field] = choose_better(existing.get(field), record.get(field))
            existing["citationCount"] = max(existing.get("citationCount", 0) or 0, record.get("citationCount", 0) or 0)
            existing["duplicate_count"] += 1
            if source not in existing["sources"]:
                existing["sources"].append(source)
            existing["provenance"].append(provenance)

    merged_results = sorted(
        merged.values(),
        key=lambda item: (
            -(item.get("citationCount", 0) or 0),
            -(item.get("year", 0) or 0),
            normalize_text(item.get("title", "")),
        ),
    )

    for index, item in enumerate(merged_results, start=1):
        item["corpus_id"] = f"paper-{index:04d}"

    return {
        "generated_at": datetime.now().isoformat(),
        "inputs": inputs,
        "dedup_summary": {
            "input_files": len(files),
            "raw_results": total_raw_results,
            "unique_results": len(merged_results),
            "duplicates_removed": total_raw_results - len(merged_results),
        },
        "results": merged_results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge and deduplicate academic search result JSON files")
    parser.add_argument("--input", nargs="+", required=True, help="Input JSON files and/or directories")
    parser.add_argument("--output-path", required=True, help="Path to save merged corpus JSON")
    args = parser.parse_args()

    files = iter_input_files(args.input)
    if not files:
        print("Error: no input JSON files found", file=sys.stderr)
        sys.exit(1)

    merged = merge_records(files)

    output_path = Path(args.output_path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "status": "success",
        "output_path": str(output_path),
        "input_files": len(files),
        "raw_results": merged["dedup_summary"]["raw_results"],
        "unique_results": merged["dedup_summary"]["unique_results"],
        "duplicates_removed": merged["dedup_summary"]["duplicates_removed"],
    }, indent=2, ensure_ascii=False))
