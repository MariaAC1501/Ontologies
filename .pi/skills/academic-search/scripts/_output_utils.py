"""Shared utilities for output handling."""
import sys
import json
from typing import Dict, Any, List

# Fields to cap and their maximum lengths
CAP_FIELDS = {
    "abstract": 300,  # Academic abstracts
    "content": 500,   # Web page content
    "snippet": 300,   # Search result snippets
}
CAP_SUFFIX = "..."


def cap_large_fields(item: Dict[str, Any]) -> Dict[str, Any]:
    """Cap large fields in a result item dict.

    Args:
        item: A dictionary representing a result item

    Returns:
        A new dictionary with large fields capped to maximum lengths
    """
    result = item.copy()
    for field, max_len in CAP_FIELDS.items():
        if field in result and isinstance(result[field], str) and len(result[field]) > max_len:
            result[field] = result[field][:max_len] + CAP_SUFFIX
    return result


def print_save_message(path: str):
    """Print save message to stderr (stdout is pure JSON for piping).

    Args:
        path: Path where results were saved
    """
    print(f"# Saved to: {path}", file=sys.stderr)


def print_error_message(message: str):
    """Print error message to stderr.

    Args:
        message: Error message to print
    """
    print(f"Error: {message}", file=sys.stderr)


def print_success_message(message: str):
    """Print success message to stderr.

    Args:
        message: Success message to print
    """
    print(f"Success: {message}", file=sys.stderr)


def print_results_with_capped_fields(results: Dict[str, Any]):
    """Print results to stdout with large fields capped (pure JSON for piping).

    Args:
        results: Results dictionary, either with a 'results' list or a single item
    """
    if "results" in results and isinstance(results["results"], list):
        results = {
            **results,
            "results": [cap_large_fields(r) for r in results["results"]]
        }
    elif any(k in results for k in CAP_FIELDS):
        results = cap_large_fields(results)
    print(json.dumps(results, indent=2, ensure_ascii=False))
