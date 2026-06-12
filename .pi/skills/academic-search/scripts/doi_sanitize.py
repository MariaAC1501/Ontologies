#!/usr/bin/env python3
"""
Convert a DOI string to a safe filename for filesystem storage.

Replaces slashes and other problematic characters with underscores.
"""

import argparse
import re


def sanitize_doi(doi: str) -> str:
    """
    Sanitize a DOI string to be used as a filename.

    Args:
        doi: DOI string (e.g., "10.1016/j.elsevier.2023.05.001")

    Returns:
        Sanitized filename-safe string (e.g., "10_1016_j_elsevier_2023_05_001")
    """
    # Remove any URL prefix like https://doi.org/
    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")
    doi = doi.replace("doi.org/", "")

    # Replace slashes and other problematic characters with underscores
    sanitized = re.sub(r'[\/\\:*?"<>|]', '_', doi)

    # Strip leading/trailing underscores and whitespace
    sanitized = sanitized.strip('_').strip()

    return sanitized


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a DOI string to a safe filename"
    )
    parser.add_argument("--doi", required=True, help="DOI string to sanitize")
    args = parser.parse_args()

    print(sanitize_doi(args.doi))
