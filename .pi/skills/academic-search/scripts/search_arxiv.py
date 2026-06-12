#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "arxiv",
# ]
# ///

"""
Search arXiv for preprint papers.

Supports pagination for retrieving large result sets.
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


ARXIV_ID_PATTERN = re.compile(r"([^/]+?)(v\d+)?$")


def build_arxiv_date_filter(year_start: int = None, year_end: int = None) -> str:
    """
    Build arXiv date filter using submittedDate field.

    Args:
        year_start: Optional start year (YYYY)
        year_end: Optional end year (YYYY)

    Returns:
        Date filter string for arXiv query, or empty string if no filters
    """
    if year_start is None and year_end is None:
        return ""

    # Convert years to arXiv date format: YYYYMMDDHHMMSS
    date_parts = []
    if year_start is not None:
        # start of year: Jan 1, 00:00:00
        start_date = f"{year_start}01010000"
        if year_end is not None:
            end_date = f"{year_end}12312359"
            date_parts.append(f"submittedDate:[{start_date} TO {end_date}]")
        else:
            date_parts.append(f"submittedDate:{start_date}*")
    elif year_end is not None:
        # end of year: Dec 31, 23:59:59
        end_date = f"{year_end}12312359"
        date_parts.append(f"submittedDate:[* TO {end_date}]")

    return " AND ".join(date_parts)



def extract_arxiv_id(entry_id: str) -> str:
    match = ARXIV_ID_PATTERN.search(entry_id or "")
    return match.group(1) if match else entry_id



def fetch_total_results(client, query: str) -> int:
    """Fetch the full arXiv hit count from the OpenSearch feed metadata."""
    probe_search = client._format_url(  # noqa: SLF001 - arxiv library exposes no public total-count API
        __import__("arxiv").Search(
            query=query,
            max_results=1,
            sort_by=__import__("arxiv").SortCriterion.Relevance,
        ),
        0,
        1,
    )
    feed = client._parse_feed(probe_search, first_page=True)  # noqa: SLF001
    return int(getattr(feed.feed, "opensearch_totalresults", 0) or 0)



def search_arxiv(
    query: str,
    limit: int = 20,
    year_start: int = None,
    year_end: int = None,
    max_pages: int = 3,
) -> Dict[str, Any]:
    """
    Search arXiv API with pagination support.

    Args:
        query: Search query (will be prefixed with "all:" for all fields)
        limit: Maximum number of results to retrieve total
        year_start: Optional start year filter (YYYY)
        year_end: Optional end year filter (YYYY)
        max_pages: Maximum number of pages to fetch (each page = up to 100 results)

    Returns:
        Dictionary with query, total, pages_retrieved, and results list
    """
    try:
        import arxiv
    except ImportError:
        print("Error: arxiv package not installed. Run: pip install arxiv", file=sys.stderr)
        sys.exit(1)

    all_results = []
    pages_retrieved = 0
    remaining = limit
    offset = 0

    # Build arXiv query with date filters if provided
    arxiv_query = f"all:{query}"
    date_filter = build_arxiv_date_filter(year_start, year_end)
    if date_filter:
        arxiv_query = f"{arxiv_query} AND {date_filter}"

    client = arxiv.Client(
        page_size=100,
        delay_seconds=3.0,  # Be polite to arXiv servers
        num_retries=3,
    )

    try:
        total = fetch_total_results(client, arxiv_query)
    except Exception as e:
        print(f"Warning: Could not fetch full arXiv hit count: {e}", file=sys.stderr)
        total = 0

    while remaining > 0 and pages_retrieved < max_pages and (total == 0 or offset < total):
        try:
            page_size = min(remaining, 100)
            search = arxiv.Search(
                query=arxiv_query,
                max_results=offset + page_size,
                sort_by=arxiv.SortCriterion.Relevance,
            )

            results = list(client.results(search, offset=offset))

            if not results:
                break

            for paper in results:
                doi = paper.doi or ""
                open_access_url = paper.pdf_url
                paper_year = paper.published.year if paper.published else None

                result = {
                    "paperId": extract_arxiv_id(paper.entry_id),
                    "doi": doi,
                    "title": paper.title,
                    "authors": [{"name": author.name} for author in paper.authors],
                    "year": paper_year,
                    "abstract": paper.summary.replace("\n", " "),
                    "citationCount": 0,  # arXiv doesn't provide citation count
                    "openAccess_pdf": {"url": open_access_url} if open_access_url else {},
                }

                all_results.append(result)
                remaining -= 1

                if remaining <= 0:
                    break

            pages_retrieved += 1
            offset += len(results)

            if len(results) < page_size:
                break

        except Exception as e:
            print(f"Error fetching page {pages_retrieved + 1}: {e}", file=sys.stderr)
            # For network/connection errors, don't retry - just break
            if "HTTP" in str(e) or "connection" in str(e).lower():
                print("Connection or HTTP error - stopping search", file=sys.stderr)
                break
            raise

    return {
        "query": query,
        "total": total,
        "pages_retrieved": pages_retrieved,
        "results_retrieved": len(all_results),
        "results": all_results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search arXiv for preprint papers")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results (default: 20)")
    parser.add_argument("--year-start", type=int, help="Filter by publication year (start)")
    parser.add_argument("--year-end", type=int, help="Filter by publication year (end)")
    parser.add_argument("--max-pages", type=int, default=3, help="Maximum pages to fetch (default: 3)")
    parser.add_argument("--output-path", required=True, help="Path to save results (JSON)")
    args = parser.parse_args()

    result = search_arxiv(
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
