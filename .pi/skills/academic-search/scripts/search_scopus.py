#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///

"""
Search Scopus API for academic papers.

Supports pagination for retrieving large result sets.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name("academic-search.env"))

# Import helper utilities from current directory
_output_utils_path = os.path.join(os.path.dirname(__file__), "_output_utils.py")
import importlib.util
spec = importlib.util.spec_from_file_location("_output_utils", _output_utils_path)
_output_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_output_utils)
print_save_message = _output_utils.print_save_message
print_results_with_capped_fields = _output_utils.print_results_with_capped_fields


def get_scopus_api_key() -> str:
    """
    Retrieve Scopus API key from environment variable.

    Returns:
        Scopus API key string

    Raises:
        ValueError: If SCOPUS_API_KEY not found
    """
    api_key = os.environ.get("SCOPUS_API_KEY")
    if not api_key:
        raise ValueError(
            "SCOPUS_API_KEY not found. Set it in .env file or environment variable."
        )
    return api_key


def search_scopus(
    query: str,
    limit: int = 20,
    year_start: int = None,
    year_end: int = None,
    max_pages: int = 3,
) -> Dict[str, Any]:
    """
    Search Scopus API with pagination support.

    Args:
        query: Search query (Scopus syntax)
        limit: Maximum number of results to retrieve total
        year_start: Optional start year filter
        year_end: Optional end year filter
        max_pages: Maximum number of pages to fetch (each page = 25 results)

    Returns:
        Dictionary with query, total, pages_retrieved, and results list
    """
    import requests

    base_url = "https://api.elsevier.com/content/search/scopus"
    api_key = get_scopus_api_key()

    all_results = []
    total = 0
    pages_retrieved = 0
    remaining = limit
    offset = 0

    while remaining > 0 and pages_retrieved < max_pages:
        page_size = min(remaining, 25)  # Scopus default per page

        params = {
            "query": query,
            "apiKey": api_key,
            "count": str(page_size),
            "start": str(offset),
            "httpAccept": "application/json",
        }

        # Add year filter to query
        year_filters = []
        if year_start is not None:
            year_filters.append(f"PUBYEAR AFT {year_start - 1}")
        if year_end is not None:
            year_filters.append(f"PUBYEAR BEF {year_end + 1}")

        if year_filters:
            params["query"] += " AND " + " AND ".join(year_filters)

        try:
            response = requests.get(base_url, params=params, timeout=30)

            if response.status_code == 401:
                print("Error: Invalid Scopus API key", file=sys.stderr)
                break
            elif response.status_code == 429:
                print("Error: Scopus API rate limit exceeded", file=sys.stderr)
                break

            response.raise_for_status()
            data = response.json()

            if "search-results" not in data:
                break

            total = int(data["search-results"].get("opensearch:totalResults", 0))
            entries = data["search-results"].get("entry", [])

            if not entries:
                break

            # Scopus returns a single entry dict when there's an error, check for error message
            if isinstance(entries, dict) and "error" in entries:
                print(f"Scopus error: {entries['error']}", file=sys.stderr)
                break

            for entry in entries:
                result = {
                    "paperId": entry.get("dc:identifier", "").split(":")[-1] if entry.get("dc:identifier") else "",
                    "doi": entry.get("prism:doi", ""),
                    "title": entry.get("dc:title", ""),
                    "authors": [],
                    "year": int(entry.get("prism:coverDate", "2000").split("-")[0]) if entry.get("prism:coverDate") else None,
                    "abstract": entry.get("dc:description", ""),
                    "citationCount": int(entry.get("citedby-count", 0)) if entry.get("citedby-count") else 0,
                    "openAccess_pdf": {},
                }

                # Parse authors
                if "author" in entry:
                    authors = entry["author"]
                    if isinstance(authors, list):
                        for author in authors:
                            if isinstance(author, dict):
                                result["authors"].append({"name": author.get("given-name", "") + " " + author.get("surname", "")})

                all_results.append(result)

            pages_retrieved += 1
            remaining -= len(entries)
            offset += len(entries)

            # Stop if we've retrieved all available results
            if len(all_results) >= min(limit, total):
                break

            # Small delay between pages to be polite
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"Error fetching page {pages_retrieved + 1}: {e}", file=sys.stderr)
            break

    return {
        "query": query,
        "total": total,
        "pages_retrieved": pages_retrieved,
        "results": all_results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Scopus for academic papers")
    parser.add_argument("--query", required=True, help="Search query (Scopus syntax recommended)")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results (default: 20)")
    parser.add_argument("--year-start", type=int, help="Filter by publication year (start)")
    parser.add_argument("--year-end", type=int, help="Filter by publication year (end)")
    parser.add_argument("--max-pages", type=int, default=3, help="Maximum pages to fetch (default: 3)")
    parser.add_argument("--output-path", required=True, help="Path to save results (JSON)")
    args = parser.parse_args()

    try:
        result = search_scopus(
            query=args.query,
            limit=args.limit,
            year_start=args.year_start,
            year_end=args.year_end,
            max_pages=args.max_pages,
        )

        # Add extracted_at timestamp
        result["output_metadata"] = {
            "extracted_at": datetime.now().isoformat(),
        }

        # Save to output path
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # Print save message to stderr
        print_save_message(args.output_path)

        # Print JSON to stdout with capped fields (pure JSON for piping)
        print_results_with_capped_fields(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
