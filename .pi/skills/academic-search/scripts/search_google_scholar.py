#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "scholarly",
# ]
# ///

"""
Search Google Scholar for academic papers.

Uses the scholarly library to retrieve results from Google Scholar.
Note: Google Scholar does not have an official API, so this uses web scraping
and may be subject to rate limiting or blocking.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

# Import helper utilities from current directory
_output_utils_path = os.path.join(os.path.dirname(__file__), "_output_utils.py")
import importlib.util
spec = importlib.util.spec_from_file_location("_output_utils", _output_utils_path)
_output_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_output_utils)
print_save_message = _output_utils.print_save_message
print_results_with_capped_fields = _output_utils.print_results_with_capped_fields


GOOGLE_SCHOLAR_PAGE_SIZE = 10
DOI_URL_PATTERN = re.compile(r"doi\.org/([^\s&]+)")



def parse_scholar_result(paper: Dict[str, Any]) -> Dict[str, Any]:
    # Extract year from bib if available
    year = None
    if "pub_year" in paper.get("bib", {}):
        try:
            year = int(paper["bib"]["pub_year"])
        except (ValueError, TypeError):
            pass

    # Extract authors
    authors = []
    if "author" in paper.get("bib", {}):
        author_value = paper["bib"]["author"]
        if isinstance(author_value, str):
            authors = [{"name": name.strip()} for name in author_value.split(" and ")]
        elif isinstance(author_value, list):
            authors = [{"name": name} for name in author_value]

    doi = ""
    pub_url = paper.get("pub_url", "")
    doi_match = DOI_URL_PATTERN.search(pub_url)
    if doi_match:
        doi = doi_match.group(1)

    return {
        "paperId": pub_url,
        "doi": doi,
        "title": paper.get("bib", {}).get("title", ""),
        "authors": authors,
        "year": year,
        "abstract": paper.get("bib", {}).get("abstract", ""),
        "citationCount": paper.get("num_citations", 0),
        "openAccess_pdf": {"url": paper["eprint_url"]} if paper.get("eprint_url") else {},
    }



def search_google_scholar(
    query: str,
    limit: int = 20,
    year_start: int = None,
    year_end: int = None,
    max_pages: int = 3,
) -> Dict[str, Any]:
    """
    Search Google Scholar using the scholarly library.

    Args:
        query: Search query
        limit: Maximum number of results to retrieve total
        year_start: Optional start year filter (YYYY)
        year_end: Optional end year filter (YYYY)
        max_pages: Maximum number of pages to fetch

    Returns:
        Dictionary with query, total, pages_retrieved, and results list
    """
    try:
        from scholarly import scholarly
    except ImportError:
        print("Error: scholarly package not installed. Run: pip install scholarly", file=sys.stderr)
        sys.exit(1)

    all_results = []
    pages_retrieved = 0
    total = 0

    try:
        for page_index in range(max_pages):
            if len(all_results) >= limit:
                break

            start_index = page_index * GOOGLE_SCHOLAR_PAGE_SIZE
            page_iterator = scholarly.search_pubs(
                query,
                year_low=year_start,
                year_high=year_end,
                start_index=start_index,
            )

            if page_index == 0:
                raw_total = getattr(page_iterator, "total_results", None)
                total = raw_total if isinstance(raw_total, int) else 0

            page_results = 0
            remaining = limit - len(all_results)

            for i, paper in enumerate(page_iterator):
                if i >= min(GOOGLE_SCHOLAR_PAGE_SIZE, remaining):
                    break

                all_results.append(parse_scholar_result(paper))
                page_results += 1

                if len(all_results) < limit:
                    time.sleep(0.5)

            if page_results == 0:
                break

            pages_retrieved += 1

            if total and start_index + page_results >= total:
                break

    except Exception as e:
        print(f"Error searching Google Scholar: {e}", file=sys.stderr)
        # If we have partial results, return them
        if not all_results:
            raise

    return {
        "query": query,
        "total": total,
        "pages_retrieved": pages_retrieved,
        "results_retrieved": len(all_results),
        "results": all_results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search Google Scholar for academic papers")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results (default: 20)")
    parser.add_argument("--year-start", type=int, help="Filter by publication year (start)")
    parser.add_argument("--year-end", type=int, help="Filter by publication year (end)")
    parser.add_argument("--max-pages", type=int, default=3, help="Maximum pages to fetch (default: 3)")
    parser.add_argument("--output-path", required=True, help="Path to save results (JSON)")
    args = parser.parse_args()

    result = search_google_scholar(
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
