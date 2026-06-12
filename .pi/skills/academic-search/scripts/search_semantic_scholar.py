#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

"""
Search Semantic Scholar API for academic papers.

Supports pagination to retrieve more than the default 100 result limits.
"""

import argparse
import importlib.util
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name("academic-search.env"))

# Import helper utilities from current directory
_output_utils_path = os.path.join(os.path.dirname(__file__), "_output_utils.py")
spec = importlib.util.spec_from_file_location("_output_utils", _output_utils_path)
_output_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_output_utils)
print_save_message = _output_utils.print_save_message
print_results_with_capped_fields = _output_utils.print_results_with_capped_fields

REQUESTED_FIELDS = [
    "paperId",
    "externalIds",
    "title",
    "authors",
    "year",
    "abstract",
    "citationCount",
    "openAccessPdf",
    "url",
]
NON_ID_METADATA_FIELDS = [
    "doi",
    "externalIds",
    "title",
    "authors",
    "year",
    "abstract",
    "citationCount",
    "openAccessPdf",
    "openAccess_pdf",
    "url",
]


def has_meaningful_value(value: Any) -> bool:
    """Return True when a Semantic Scholar field contains useful data."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def build_semantic_scholar_query(
    query: str,
    year_start: int | None = None,
    year_end: int | None = None,
) -> str:
    """
    Build a Semantic Scholar query string.

    The returned string is not URL-encoded because ``requests`` handles that.
    """
    query_parts: list[str] = []

    if year_start is not None or year_end is not None:
        start = "" if year_start is None else str(year_start)
        end = "" if year_end is None else str(year_end)
        query_parts.append(f"year:{start}-{end}")

    cleaned_query = query.strip()
    if cleaned_query:
        query_parts.append(cleaned_query)

    return " ".join(query_parts)


def detect_degraded_results(results: list[dict[str, Any]]) -> str | None:
    """
    Detect the known Semantic Scholar failure mode where only ``paperId`` is returned.
    """
    if not results:
        return None

    degraded_count = 0
    for paper in results:
        if not any(has_meaningful_value(paper.get(field)) for field in NON_ID_METADATA_FIELDS):
            degraded_count += 1

    if degraded_count == len(results):
        sample_keys = sorted({key for paper in results[:3] for key in paper.keys()})
        return (
            "Semantic Scholar returned results with paperId only; all requested metadata fields "
            f"were empty or missing. Sample keys in response: {sample_keys}. "
            "This usually indicates the fields parameter was not accepted or the API returned a degraded response."
        )

    return None


def search_semantic_scholar(
    query: str,
    limit: int = 20,
    year_start: int | None = None,
    year_end: int | None = None,
    max_pages: int = 3,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Search Semantic Scholar API with pagination support.

    Args:
        query: Search query
        limit: Maximum number of results to retrieve total
        year_start: Optional start year filter
        year_end: Optional end year filter
        max_pages: Maximum number of pages to fetch (each page = up to 100 results)
        offset: Starting offset for pagination

    Returns:
        Dictionary with query, total, pages_retrieved, and results list
    """
    import requests

    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    all_results: list[dict[str, Any]] = []
    total = 0
    pages_retrieved = 0

    current_offset = offset
    remaining = limit
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    consecutive_rate_limits = 0

    while remaining > 0 and pages_retrieved < max_pages:
        page_size = min(remaining, 100)  # Semantic Scholar max per page is 100

        params = {
            "query": build_semantic_scholar_query(query, year_start, year_end),
            "fields": ",".join(REQUESTED_FIELDS),
            "limit": page_size,
            "offset": current_offset,
        }

        headers = {}
        if api_key:
            headers["x-api-key"] = api_key

        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=30)

            # Handle rate limit with exponential backoff
            if response.status_code == 429:
                consecutive_rate_limits += 1
                retry_after_header = response.headers.get("Retry-After")
                retry_delay = int(retry_after_header) if retry_after_header and retry_after_header.isdigit() else min(2 ** consecutive_rate_limits, 60)
                if consecutive_rate_limits >= 3:
                    raise RuntimeError(
                        "Semantic Scholar API returned HTTP 429 repeatedly. "
                        "Set a valid SEMANTIC_SCHOLAR_API_KEY or retry later."
                    )
                print(f"Rate limited. Waiting {retry_delay}s before retry...", file=sys.stderr)
                time.sleep(retry_delay)
                continue

            consecutive_rate_limits = 0
            response.raise_for_status()
            data = response.json()

            # Warn about missing API key if results seem degraded or rate limited
            if not api_key and pages_retrieved == 0:
                print("Warning: SEMANTIC_SCHOLAR_API_KEY not set. Results may be limited or rate-limited.", file=sys.stderr)

            if "data" not in data or not data["data"]:
                break

            raw_results = data["data"]
            degradation_error = detect_degraded_results(raw_results)
            if degradation_error:
                raise RuntimeError(degradation_error)

            total = data.get("total", 0)

            # Format results to match our schema
            for paper in raw_results:
                result = {
                    "paperId": paper.get("paperId", ""),
                    "doi": (paper.get("externalIds") or {}).get("DOI", ""),
                    "title": paper.get("title", ""),
                    "authors": [
                        {"name": author.get("name", "")}
                        for author in paper.get("authors", [])
                        if isinstance(author, dict)
                    ],
                    "year": paper.get("year"),
                    "abstract": paper.get("abstract", ""),
                    "citationCount": paper.get("citationCount", 0),
                    "openAccess_pdf": {},
                }

                if "openAccessPdf" in paper and paper["openAccessPdf"]:
                    result["openAccess_pdf"] = {"url": paper["openAccessPdf"].get("url", "")}

                all_results.append(result)

            pages_retrieved += 1
            remaining -= len(raw_results)
            current_offset += len(raw_results)

            # Stop if we've retrieved all available results
            if len(all_results) >= min(limit, total):
                break

            # Small delay between pages to be polite
            time.sleep(0.1)

        except RuntimeError:
            raise
        except requests.RequestException as e:
            print(f"Error fetching page {pages_retrieved + 1}: {e}", file=sys.stderr)
            if getattr(e, "response", None) is not None:
                body = e.response.text[:200].replace("\n", " ")
                print(f"HTTP {e.response.status_code}: {body}", file=sys.stderr)
            break

    return {
        "query": query,
        "total": total,
        "pages_retrieved": pages_retrieved,
        "results": all_results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Semantic Scholar for academic papers")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results (default: 20)")
    parser.add_argument("--year-start", type=int, help="Filter by publication year (start)")
    parser.add_argument("--year-end", type=int, help="Filter by publication year (end)")
    parser.add_argument("--max-pages", type=int, default=3, help="Maximum pages to fetch (default: 3)")
    parser.add_argument("--output-path", required=True, help="Path to save results (JSON)")
    args = parser.parse_args()

    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")

    try:
        result = search_semantic_scholar(
            query=args.query,
            limit=args.limit,
            year_start=args.year_start,
            year_end=args.year_end,
            max_pages=args.max_pages,
        )
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    degraded_results_error = detect_degraded_results(result["results"])

    # Add extracted_at timestamp
    result["output_metadata"] = {
        "extracted_at": datetime.now().isoformat(),
    }
    if degraded_results_error:
        result["output_metadata"]["warning"] = degraded_results_error

    # Save to output path
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Validate results look reasonable
    if result["total"] == 0 or len(result["results"]) == 0:
        print("Warning: No results found. This may indicate:", file=sys.stderr)
        print("  1. Invalid or pending SEMANTIC_SCHOLAR_API_KEY", file=sys.stderr)
        print("  2. Query returned no matches", file=sys.stderr)
        print("  3. API service issue", file=sys.stderr)
        if not api_key:
            print("\nAn API key is strongly recommended for full results.", file=sys.stderr)
    elif degraded_results_error:
        print(f"Error: {degraded_results_error}", file=sys.stderr)
        print("Saved output for inspection, but treating this run as a failure.", file=sys.stderr)
        print_save_message(args.output_path)
        sys.exit(1)

    # Print save message to stderr
    print_save_message(args.output_path)

    # Print JSON to stdout with capped fields (pure JSON for piping)
    print_results_with_capped_fields(result)
