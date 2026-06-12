#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv",
#     "zai-sdk",
#     "openai"
# ]
# ///

"""
Retrieve full text of academic papers from multiple sources.

Tries sources in order: arXiv -> OpenAlex -> Semantic Scholar Open Access -> Unpaywall.
If all fail, prompts for manual upload.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name("academic-search.env"))

def progress(message: str) -> None:
    """Print progress message to stderr (doesn't interfere with JSON stdout)."""
    print(message, file=sys.stderr, flush=True)

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from doi_sanitize import sanitize_doi

# Default papers directory (project-specific, local folder)
DEFAULT_PAPERS_DIR = Path("./.academic-qa/papers")

# User-agent headers to work around anti-bot measures (e.g., IEEE)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def download_pdf_with_headers(pdf_url: str, temp_pdf_path: Path) -> bool:
    """
    Download PDF with proper headers to work around anti-bot measures.

    Args:
        pdf_url: URL to download from
        temp_pdf_path: Path to save the PDF locally

    Returns:
        True if successful, False otherwise
    """
    import requests
    import time

    try:
        progress(f"Downloading PDF from {pdf_url}...")
        response = requests.get(pdf_url, headers=HEADERS, timeout=60, stream=True)
        response.raise_for_status()

        # Check if we actually got a PDF (not an HTML response)
        content_type = response.headers.get("content-type", "").lower()
        if "application/pdf" not in content_type:
            return False

        # Get file size for progress
        total_size = int(response.headers.get('content-length', 0))
        temp_pdf_path.parent.mkdir(parents=True, exist_ok=True)

        with open(temp_pdf_path, "wb") as f:
            downloaded = 0
            start_time = time.time()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    # Show progress for large files
                    if total_size > 100 * 1024:  # Only show for files > 100KB
                        percent = (downloaded / total_size) * 100
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            rate = downloaded / elapsed
                            progress(f"  Downloaded {downloaded / 1024 / 1024:.1f}MB / {total_size / 1024 / 1024:.1f}MB ({percent:.1f}%)")

        downloaded_mb = temp_pdf_path.stat().st_size / 1024 / 1024
        progress(f"Downloaded {downloaded_mb:.2f} MB")

        # Verify it's actually a PDF
        with open(temp_pdf_path, "rb") as f:
            header = f.read(4)
            if header != b"%PDF":
                temp_pdf_path.unlink()
                return False

        return True

    except requests.RequestException:
        return False


def pdf_download_error_message(source: str, pdf_url: str) -> str:
    """
    Generate a descriptive error message for PDF download failures.

    Args:
        source: The source (arxiv, openalex, semantic_scholar, unpaywall)
        pdf_url: The PDF URL that was attempted

    Returns:
        Descriptive error message
    """
    return (
        f"Failed to download PDF from {source}.\n"
        f"The URL {pdf_url} returned HTML instead of a PDF. "
        f"This may be due to anti-bot protection, redirect pages, or temporary server issues. "
        f"Please try manually downloading from the publisher website."
    )


def retrieve_from_arxiv(doi: str) -> str:
    """
    Try to retrieve paper from arXiv if it's an arXiv paper.

    Args:
        doi: DOI string

    Returns:
        arXiv ID if found, None otherwise
    """
    import re

    # Check if DOI contains arXiv ID (e.g., 10.48550/arXiv.2301.00001 or direct arXiv ID)
    arxiv_match = re.search(r"arxiv\.?(\d{4}\.\d+)", doi, re.IGNORECASE)
    if arxiv_match:
        return f"arXiv:{arxiv_match.group(1)}"

    # Some DOIs are just arXiv IDs with 10.48550 prefix
    if doi.startswith("10.48550/"):
        suffix = doi.replace("10.48550/", "")
        if suffix.startswith("arXiv."):
            return suffix.replace(".", ":", 1)

    # Check for bare arXiv ID pattern (e.g., "2201.07642")
    bare_arxiv_match = re.match(r"^(\d{4}\.\d{4,})$", doi)
    if bare_arxiv_match:
        return f"arXiv:{bare_arxiv_match.group(1)}"

    return None


def retrieve_from_semantic_scholar(paper_id: str) -> str:
    """
    Try to retrieve open access PDF from Semantic Scholar.

    Args:
        paper_id: Semantic Scholar paper ID or DOI

    Returns:
        PDF URL if found, None otherwise
    """
    import requests

    base_url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "openAccessPdf"}

    try:
        response = requests.get(base_url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get("openAccessPdf") and data["openAccessPdf"].get("url"):
            return data["openAccessPdf"]["url"]

    except requests.RequestException:
        pass

    return None


def retrieve_from_unpaywall(doi: str) -> str:
    """
    Try to retrieve open access version from Unpaywall.

    Args:
        doi: DOI string

    Returns:
        PDF URL if found, None otherwise
    """
    import requests

    url = f"https://api.unpaywall.org/v2/{doi}"
    # Unpaywall requires a valid email format - this is used for rate limiting tracking
    params = {"email": "unknown@unknown.com"}

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)

        if response.ok:
            data = response.json()

            # Check for best OA location with direct PDF
            if (
                data.get("is_oa")
                and data.get("best_oa_location")
                and data["best_oa_location"].get("url_for_pdf")
            ):
                return data["best_oa_location"]["url_for_pdf"]

            # Fallback: check any OA location with PDF (e.g., arXiv copies)
            for location in data.get("oa_locations", []):
                if location.get("url_for_pdf"):
                    return location["url_for_pdf"]

    except requests.RequestException:
        pass

    return None


def retrieve_from_openalex(doi: str) -> str:
    """
    Try to retrieve PDF URL from OpenAlex.

    OpenAlex is a free catalog of the global research system with ~270M works.
    It aggregates open access PDFs from many sources including arXiv, DOAJ,
    PubMed Central, and institutional repositories.

    Args:
        doi: DOI string

    Returns:
        PDF URL if found, None otherwise
    """
    import requests

    url = f"https://api.openalex.org/works"
    params = {
        "filter": f"doi:{doi}",
        "select": "best_oa_location,primary_location,locations,open_access",
    }

    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return None

        work = results[0]

        # Check best open access location first
        best_oa = work.get("best_oa_location")
        if best_oa and best_oa.get("pdf_url"):
            return best_oa["pdf_url"]

        # Fallback to primary location if not open access
        primary = work.get("primary_location")
        if primary and primary.get("pdf_url"):
            return primary["pdf_url"]

        # Check all locations for any PDF
        locations = work.get("locations", [])
        for loc in locations:
            if loc and loc.get("pdf_url"):
                return loc["pdf_url"]

        # Last resort: check for landing page URLs (might have download links)
        for loc in locations:
            if loc and loc.get("landing_page_url"):
                landing = loc["landing_page_url"]
                # Some publishers use predictable PDF URL patterns
                if "nature.com" in landing:
                    return landing.replace("/articles/", "/articles/") + ".pdf"
                elif "frontiersin.org" in landing:
                    return landing + "/full"

    except requests.RequestException:
        pass

    return None


def resolve_landing_page_url(doi: str) -> str | None:
    """
    Resolve a DOI to the publisher landing page URL.

    Args:
        doi: DOI string or direct URL

    Returns:
        Landing page URL if resolved, None otherwise
    """
    import requests

    if doi.startswith("http://") or doi.startswith("https://"):
        return doi

    headers = {
        **HEADERS,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    for resolver_url in (f"https://doi.org/{doi}", f"https://dx.doi.org/{doi}"):
        try:
            response = requests.get(
                resolver_url,
                headers=headers,
                timeout=30,
                allow_redirects=True,
            )
            response.raise_for_status()

            final_url = response.url
            if final_url and "doi.org/" not in final_url.lower():
                return final_url
        except requests.RequestException:
            pass

    return None


def retrieve_paper_pdf(
    doi: str | None = None,
    url: str | None = None,
    output_dir: str | None = None,
    force: bool = False,
) -> dict:
    """
    Retrieve full text of a paper from multiple sources.

    Args:
        doi: DOI string
        url: Direct publisher landing-page URL
        output_dir: Output path - either a directory or full file path ending in .md (default: .academic-qa/papers)
        force: Force re-download even if file exists

    Returns:
        Status dictionary with output path and source info
    """
    paper_ref = url or doi
    if not paper_ref:
        return {
            "status": "error",
            "message": "Either doi or url is required",
        }

    # Determine output PDF file path
    if output_dir:
        output_path_obj = Path(output_dir).expanduser()
        # Accept .md or .pdf — always save as .pdf (conversion is a separate step)
        if output_path_obj.suffix.lower() in ('.md', '.pdf'):
            output_file = output_path_obj.with_suffix('.pdf')
            output_path = output_file.parent
        else:
            # Treat as directory, use DOI/URL as filename
            output_path = output_path_obj
            sanitized_ref = sanitize_doi(paper_ref)
            output_file = output_path / f"{sanitized_ref}.pdf"
    else:
        output_path = DEFAULT_PAPERS_DIR
        sanitized_ref = sanitize_doi(paper_ref)
        output_file = output_path / f"{sanitized_ref}.pdf"

    output_path.mkdir(parents=True, exist_ok=True)

    # Check if PDF already exists
    if output_file.exists() and not force:
        return {
            "doi": doi,
            "url": url,
            "pdf_path": str(output_file),
            "source": "existing_file",
            "status": "pdf_ready",
            "message": "PDF already exists (use --force to re-download). Invoke the pdf-to-markdown skill to convert.",
        }

    pdf_url = None
    source = None
    landing_url = resolve_landing_page_url(paper_ref)

    # DOI-only API retrieval path
    if doi:
        arxiv_id = retrieve_from_arxiv(doi)
        if arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id.replace('arXiv:', '')}.pdf"
            source = "arxiv"

        if not pdf_url:
            pdf_url = retrieve_from_openalex(doi)
            if pdf_url:
                source = "openalex"

        if not pdf_url:
            pdf_url = retrieve_from_semantic_scholar(doi)
            if pdf_url:
                source = "semantic_scholar_open_access"

        if not pdf_url:
            pdf_url = retrieve_from_unpaywall(doi)
            if pdf_url:
                source = "unpaywall"

    # If no API source found, return a manual-download handoff immediately
    if not pdf_url:
        return {
            "doi": doi,
            "url": url,
            "landing_page_url": landing_url or url,
            "status": "requires_manual_upload",
            "message": "Full text not available from open-access APIs. Download manually in your normal browser and place the file in the configured manual PDF drop folder.",
            "suggested_sources": ["publisher website", "university library", "author's personal website"],
        }

    try:
        download_success = download_pdf_with_headers(pdf_url, output_file)

        if not download_success:
            return {
                "doi": doi,
                "url": url,
                "landing_page_url": landing_url or url,
                "status": "error",
                "message": f"{pdf_download_error_message(source, pdf_url)} Download manually in your normal browser and place the file in the configured manual PDF drop folder.",
                "pdf_url": pdf_url,
                "source": source,
            }

        return {
            "doi": doi,
            "url": url,
            "pdf_path": str(output_file),
            "source": source,
            "status": "pdf_ready",
            "message": "PDF downloaded. Invoke the pdf-to-markdown skill to convert.",
        }

    except Exception as e:
        return {
            "doi": doi,
            "url": url,
            "status": "error",
            "message": f"Error retrieving PDF: {e}",
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Retrieve full text of academic papers from multiple sources"
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--doi", help="DOI of the paper")
    source_group.add_argument("--url", help="Direct publisher landing-page URL used for manual-download handoff when OA retrieval fails")
    parser.add_argument("--output-path", help=f"Output PDF file path or directory (default: {DEFAULT_PAPERS_DIR}/{{sanitized_doi}}.pdf)")
    parser.add_argument("--force", action="store_true", help="Force re-download")
    args = parser.parse_args()

    result = retrieve_paper_pdf(
        doi=args.doi,
        url=args.url,
        output_dir=args.output_path,
        force=args.force,
    )

    print(json.dumps(result, indent=2))
