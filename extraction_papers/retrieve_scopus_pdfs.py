#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
Batch-retrieve open-access PDFs for entries in scopus_export_May 26-2026.csv.

This intentionally writes normalized PDFs directly into this extraction_papers/
folder, per the user's instruction not to create a separate protocol directory.
It is resumable: rerun it and existing PDFs/status entries are reused.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urljoin, urlparse

import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "scopus_export_May 26-2026.csv"
STATUS_JSON = BASE_DIR / "pdf-retrieval-status.json"
STATUS_MD = BASE_DIR / "pdf-status.md"
FAILED_CANDIDATES_JSON = BASE_DIR / "pdf-retrieval-failed-candidates.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# MDPI resource slugs. Most match the DOI alpha code, but a few do not.
MDPI_SOURCE_SLUG = {
    "AI (Switzerland)": "ai",
    "Actuators": "actuators",
    "Aerospace": "aerospace",
    "AgriEngineering": "agriengineering",
    "Agriculture (Switzerland)": "agriculture",
    "Algorithms": "algorithms",
    "Animals": "animals",
    "Applied Mechanics": "applmech",
    "Applied Microbiology (Switzerland)": "applmicrobiol",
    "Applied Sciences (Switzerland)": "applsci",
    "Applied System Innovation": "asi",
    "Atmosphere": "atmosphere",
    "Automation": "automation",
    "Batteries": "batteries",
    "Big Data and Cognitive Computing": "bdcc",
    "Bioengineering": "bioengineering",
    "Biomimetics": "biomimetics",
    "Brain Sciences": "brainsci",
    "Buildings": "buildings",
    "Catalysts": "catalysts",
    "Chemosensors": "chemosensors",
    "CivilEng": "civileng",
    "Coatings": "coatings",
    "Computation": "computation",
    "Computers": "computers",
    "Crystals": "crystals",
    "Data": "data",
    "Designs": "designs",
    "Diagnostics": "diagnostics",
    "Digital": "digital",
    "Drones": "drones",
    "Electrochem": "electrochem",
    "Electronics (Switzerland)": "electronics",
    "Energies": "energies",
    "Eng": "eng",
    "Engineering Proceedings": "engproc",
    "Entropy": "entropy",
    "Fermentation": "fermentation",
    "Fire": "fire",
    "Fractal and Fractional": "fractalfract",
    "Future Internet": "futureinternet",
    "Future Transportation": "futuretransp",
    "GeoHazards": "geohazards",
    "Hydrology": "hydrology",
    "Informatics": "informatics",
    "Information (Switzerland)": "information",
    "Infrastructures": "infrastructures",
    "Instruments": "instruments",
    "International Journal of Molecular Sciences": "ijms",
    "International Journal of Turbomachinery, Propulsion and Power": "ijtpp",
    "Inventions": "inventions",
    "IoT": "iot",
    "ISPRS International Journal of Geo-Information": "ijgi",
    "Journal of Clinical Medicine": "jcm",
    "Journal of Fungi": "jof",
    "Journal of Manufacturing and Materials Processing": "jmmp",
    "Journal of Marine Science and Engineering": "jmse",
    "Journal of Risk and Financial Management": "jrfm",
    "Journal of Sensor and Actuator Networks": "jsan",
    "Land": "land",
    "Life": "life",
    "Logistics": "logistics",
    "Lubricants": "lubricants",
    "Machine Learning and Knowledge Extraction": "make",
    "Machines": "machines",
    "Materials": "materials",
    "Mathematics": "mathematics",
    "Metals": "metals",
    "Methane": "methane",
    "Metrology": "metrology",
    "Micromachines": "micromachines",
    "Microorganisms": "microorganisms",
    "Mining": "mining",
    "Modelling": "modelling",
    "Multimodal Technologies and Interaction": "mti",
    "Nanomaterials": "nanomaterials",
    "Pediatric Reports": "pediatricrep",
    "Photonics": "photonics",
    "Physchem": "physchem",
    "Polymers": "polymers",
    "Processes": "processes",
    "Remote Sensing": "remotesensing",
    "Robotics": "robotics",
    "Safety": "safety",
    "Sci": "sci",
    "Sensors": "sensors",
    "Sensors (Basel, Switzerland)": "sensors",
    "Signals": "signals",
    "Smart Cities": "smartcities",
    "Surgeries (Switzerland)": "surgeries",
    "Sustainability (Switzerland)": "sustainability",
    "Symmetry": "symmetry",
    "Systems": "systems",
    "Technologies": "technologies",
    "Vehicles": "vehicles",
    "Vibration": "vibration",
    "Water (Switzerland)": "water",
    "World Electric Vehicle Journal": "wevj",
}


def clean_text(s: str | None) -> str:
    return " ".join((s or "").replace("\ufeff", "").split())


def slugify(s: str, max_len: int = 92) -> str:
    s = clean_text(s).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return (s[:max_len].strip("_") or "untitled")


def normalized_pdf_name(index: int, row: dict) -> str:
    return f"paper-{index:04d}_{slugify(row.get('Title', 'untitled'))}.pdf"


def normalized_pdf_path(index: int, row: dict) -> Path:
    return BASE_DIR / normalized_pdf_name(index, row)


def load_rows() -> list[dict]:
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_status() -> dict[str, dict]:
    if STATUS_JSON.exists():
        with STATUS_JSON.open(encoding="utf-8") as f:
            data = json.load(f)
        # Backward-compatible shape: either a list or an object with results.
        if isinstance(data, list):
            return {str(item.get("corpus_id") or item.get("index")): item for item in data}
        return {str(item.get("corpus_id") or item.get("index")): item for item in data.get("results", [])}
    return {}


def save_status(status_by_id: dict[str, dict]) -> None:
    results = [status_by_id[k] for k in sorted(status_by_id, key=lambda x: int(x.split("-")[-1]))]
    payload = {
        "source_csv": str(CSV_PATH),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "results": results,
    }
    tmp = STATUS_JSON.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    tmp.replace(STATUS_JSON)


def int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def unique(seq: Iterable[str]) -> list[str]:
    out = []
    seen = set()
    for item in seq:
        if not item:
            continue
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def mdpi_candidate_urls(row: dict) -> list[str]:
    doi = clean_text(row.get("DOI"))
    if not doi.lower().startswith("10.3390/"):
        return []
    slug = MDPI_SOURCE_SLUG.get(clean_text(row.get("Source title")))
    if not slug:
        # Last-resort inference from source title.
        source = clean_text(row.get("Source title"))
        source = re.sub(r"\s*\([^)]*\)", "", source)
        slug = re.sub(r"[^a-z0-9]+", "", source.lower())
    vol = int_or_none(row.get("Volume"))
    art = int_or_none(row.get("Art. No."))
    if vol is None or art is None:
        return []
    vol_candidates = [str(vol)]
    if vol < 10:
        vol_candidates.append(f"{vol:02d}")
    # A few short-name MDPI journals use zero-padded volume in resource paths.
    if slug in {"ai", "asi", "iot", "eng", "mti", "sci"}:
        vol_candidates = [f"{vol:02d}", str(vol)]
    art_candidates = [f"{art:05d}", str(art)]
    urls = []
    for v in unique(vol_candidates):
        for a in unique(art_candidates):
            stem = f"{slug}-{v}-{a}"
            urls.append(
                f"https://mdpi-res.com/d_attachment/{slug}/{stem}/article_deploy/{stem}.pdf"
            )
    return urls


def publisher_direct_candidate_urls(row: dict) -> list[str]:
    doi = clean_text(row.get("DOI"))
    doi_l = doi.lower()
    suffix = doi.split("/", 1)[1] if "/" in doi else doi
    urls: list[str] = []

    urls.extend(mdpi_candidate_urls(row))

    if doi_l.startswith("10.1038/"):
        urls.append(f"https://www.nature.com/articles/{suffix}.pdf")
    if doi_l.startswith("10.1007/") or doi_l.startswith("10.1186/"):
        urls.append(f"https://link.springer.com/content/pdf/{doi}.pdf")
    if doi_l.startswith("10.1088/"):
        urls.append(f"https://iopscience.iop.org/article/{doi}/pdf")
    if doi_l.startswith("10.1371/"):
        # This corpus contains PLOS ONE entries; the endpoint redirects as needed.
        urls.append(f"https://journals.plos.org/plosone/article/file?id={doi}&type=printable")
    if doi_l.startswith("10.3389/"):
        urls.append(f"https://www.frontiersin.org/articles/{doi}/pdf")
    if doi_l.startswith("10.3390/"):
        # OpenAlex often emits this, but MDPI blocks it from scripts; keep it late.
        pass
    if doi_l.startswith("10.3390/") is False:
        # Generic publisher PDF endpoints that are legal when the article is OA.
        # Many will fail with anti-bot or access-control HTML and then be logged.
        if doi_l.startswith("10.1080/"):
            urls.append(f"https://www.tandfonline.com/doi/pdf/{doi}")
        if doi_l.startswith("10.1002/") or doi_l.startswith("10.1111/"):
            urls.append(f"https://onlinelibrary.wiley.com/doi/pdf/{doi}")
        if doi_l.startswith("10.1177/"):
            urls.append(f"https://journals.sagepub.com/doi/pdf/{doi}")
        if doi_l.startswith("10.1155/"):
            urls.append(f"https://onlinelibrary.wiley.com/doi/pdf/{doi}")
        if doi_l.startswith("10.1093/"):
            urls.append(f"https://academic.oup.com/article-pdf/doi/{doi}")
        if doi_l.startswith("10.1108/"):
            urls.append(f"https://www.emerald.com/insight/content/doi/{doi}/full/pdf")
    return unique(urls)


def extract_pdf_links_from_html(text: str, base_url: str) -> list[str]:
    # Decode HTML entities and escaped slashes, then collect PDF-ish links.
    # Many OJS journals expose article PDFs as /article/view/<id>/<galley>
    # or /article/download/<id>/<galley> without a .pdf suffix.
    text = html.unescape(text).replace("\\/", "/")
    primary: list[str] = []
    secondary: list[str] = []

    def add_candidate(raw: str, bucket: list[str] = primary) -> None:
        if not raw:
            return
        u = raw.strip()
        if u.startswith("data:") or u.startswith("mailto:") or u.startswith("javascript:"):
            return
        u_abs = urljoin(base_url, u)
        lu = u_abs.lower()
        if any(skip in lu for skip in ["citationstylelanguage", "citation%20list", "citation list", "bibtex", "ris?", "pdf.svg", "facebook", "twitter"]):
            return
        # Avoid obvious figures/supplementary PDFs when the article PDF is also present.
        if re.search(r"(?:[-_/](?:f|fig|figure)\d+|high-res|supplement|graphical|cover|toc)", lu):
            bucket = secondary
        bucket.append(u_abs)

    for m in re.finditer(r"(?:https?:)?//[^\s\"'<>]+?\.pdf(?:\?[^\s\"'<>]*)?", text, flags=re.I):
        u = m.group(0)
        if u.startswith("//"):
            u = "https:" + u
        add_candidate(u)
    for m in re.finditer(r"[\"']([^\"']+?\.pdf(?:\?[^\"']*)?)[\"']", text, flags=re.I):
        add_candidate(m.group(1))
    for m in re.finditer(r"(?:href|src)=[\"']([^\"']+)[\"']", text, flags=re.I):
        h = html.unescape(m.group(1))
        lh = h.lower()
        if re.search(r"/article/view/\d+/\d+", lh):
            add_candidate(re.sub(r"/article/view/", "/article/download/", h, flags=re.I))
            add_candidate(h, secondary)
        elif any(token in lh for token in ["/article/download/", "/download/file/fid/", "pdf-", "type=printable"]):
            add_candidate(h)
        elif "download" in lh and "libraryfiles" not in lh:
            add_candidate(h, secondary)
    base_host = urlparse(base_url).netloc.lower()

    def prio(u: str) -> tuple[int, str]:
        lu = u.lower()
        host = urlparse(u).netloc.lower()
        if any(token in lu for token in ["/article/download/", "/download/file/fid/", "/sm_pdf/sm", "pdf-"]):
            return (0, lu)
        if host == base_host:
            return (1, lu)
        return (2, lu)

    return unique(sorted(primary + secondary, key=prio))


def query_openalex_pdf_urls(doi: str, timeout: int = 20) -> list[str]:
    url = "https://api.openalex.org/works"
    params = {
        "filter": f"doi:{doi}",
        "select": "best_oa_location,primary_location,locations,open_access",
        "mailto": "unknown@unknown.com",
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
        if not r.ok:
            return []
        data = r.json()
    except Exception:
        return []
    results = data.get("results") or []
    if not results:
        return []
    work = results[0]
    urls = []
    for key in ("best_oa_location", "primary_location"):
        loc = work.get(key) or {}
        if loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
    for loc in work.get("locations") or []:
        if loc and loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
    return unique(urls)


def query_unpaywall_pdf_urls(doi: str, timeout: int = 20) -> list[str]:
    url = f"https://api.unpaywall.org/v2/{doi}"
    try:
        r = requests.get(url, params={"email": "unknown@unknown.com"}, headers=HEADERS, timeout=timeout)
        if not r.ok:
            return []
        data = r.json()
    except Exception:
        return []
    urls = []
    best = data.get("best_oa_location") or {}
    if best.get("url_for_pdf"):
        urls.append(best["url_for_pdf"])
    for loc in data.get("oa_locations") or []:
        if loc.get("url_for_pdf"):
            urls.append(loc["url_for_pdf"])
    return unique(urls)


def semantic_scholar_pdf_urls(doi: str, timeout: int = 20) -> list[str]:
    # Use DOI: prefix so the slash in the DOI is not interpreted as a path boundary.
    url = f"https://api.semanticscholar.org/graph/v1/paper/{quote('DOI:' + doi, safe='')}"
    try:
        r = requests.get(url, params={"fields": "openAccessPdf"}, headers=HEADERS, timeout=timeout)
        if not r.ok:
            return []
        data = r.json()
    except Exception:
        return []
    pdf = (data.get("openAccessPdf") or {}).get("url")
    return [pdf] if pdf else []


def doi_resolve_and_scrape_pdf_urls(doi: str, timeout: int = 25) -> list[str]:
    try:
        r = requests.get(
            f"https://doi.org/{doi}",
            headers={**HEADERS, "Accept": "text/html,application/xhtml+xml,application/pdf,*/*"},
            timeout=timeout,
            allow_redirects=True,
        )
    except Exception:
        return []
    if not r.ok:
        return []
    ctype = (r.headers.get("content-type") or "").lower()
    if "application/pdf" in ctype or r.url.lower().split("?", 1)[0].endswith(".pdf"):
        return [r.url]
    if not r.text:
        return []
    urls = extract_pdf_links_from_html(r.text[:2_000_000], r.url)
    # TechScience/OJS/Copernicus/etc. pages expose PDF links in HTML.
    return urls


def transform_known_pdf_url(url: str, row: dict) -> list[str]:
    """Add URL variants for known OA hosts whose API PDF URLs are script-hostile."""
    out = [url]
    doi = clean_text(row.get("DOI"))
    # If APIs return an MDPI www.mdpi.com PDF URL, put the mdpi-res URL first.
    if "mdpi.com" in url and doi.lower().startswith("10.3390/"):
        out = mdpi_candidate_urls(row) + out
    return unique(out)


def api_candidate_urls(row: dict) -> list[str]:
    doi = clean_text(row.get("DOI"))
    urls: list[str] = []
    for u in query_openalex_pdf_urls(doi) + query_unpaywall_pdf_urls(doi) + semantic_scholar_pdf_urls(doi):
        urls.extend(transform_known_pdf_url(u, row))
    return unique(urls)


def scrape_candidate_urls(row: dict) -> list[str]:
    doi = clean_text(row.get("DOI"))
    # Avoid expensive/known-hostile generic scraping for publishers that consistently block scripts.
    hostile_prefixes = ("10.1016/", "10.1109/", "10.1080/", "10.1177/", "10.1002/", "10.1111/")
    if not doi.lower().startswith(hostile_prefixes):
        return doi_resolve_and_scrape_pdf_urls(doi)
    # Some non-hostile sites use DOI prefixes that otherwise look generic.
    if doi.lower().startswith("10.32604/"):
        return doi_resolve_and_scrape_pdf_urls(doi)
    return []


def candidate_urls(row: dict, use_apis: bool = True, use_scrape: bool = True) -> list[str]:
    urls = publisher_direct_candidate_urls(row)
    if use_apis:
        urls.extend(api_candidate_urls(row))
    if use_scrape:
        urls.extend(scrape_candidate_urls(row))
    return unique(urls)


def download_pdf(url: str, output_path: Path, timeout: int = 90) -> tuple[bool, str]:
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp.unlink(missing_ok=True)
    headers = dict(HEADERS)
    # Some hosts require a plausible PDF accept header and/or referer.
    headers["Accept"] = "application/pdf,application/octet-stream;q=0.9,text/html;q=0.8,*/*;q=0.7"
    try:
        with requests.get(url, headers=headers, timeout=timeout, stream=True, allow_redirects=True) as r:
            if r.status_code not in (200, 201, 202, 206):
                return False, f"HTTP {r.status_code}"
            iterator = r.iter_content(chunk_size=1024 * 64)
            first = b""
            for first in iterator:
                if first:
                    break
            if not first:
                return False, "empty response"
            if not first.lstrip().startswith(b"%PDF-"):
                ctype = r.headers.get("content-type", "")
                preview = first[:40].replace(b"\n", b" ").replace(b"\r", b" ")
                return False, f"not a PDF (content-type={ctype!r}, starts={preview!r})"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with tmp.open("wb") as f:
                f.write(first)
                for chunk in iterator:
                    if chunk:
                        f.write(chunk)
        if tmp.stat().st_size < 10_000:
            size = tmp.stat().st_size
            tmp.unlink(missing_ok=True)
            return False, f"PDF too small ({size} bytes)"
        tmp.replace(output_path)
        return True, f"downloaded {output_path.stat().st_size} bytes"
    except requests.exceptions.Timeout:
        tmp.unlink(missing_ok=True)
        return False, "timeout"
    except Exception as e:
        tmp.unlink(missing_ok=True)
        return False, f"{type(e).__name__}: {e}"


def retrieve_one(index: int, row: dict, args) -> tuple[str, dict, list[dict]]:
    corpus_id = f"paper-{index:04d}"
    out = normalized_pdf_path(index, row)
    doi = clean_text(row.get("DOI"))
    title = clean_text(row.get("Title"))
    source_title = clean_text(row.get("Source title"))

    base_record = {
        "corpus_id": corpus_id,
        "index": index,
        "title": title,
        "authors": clean_text(row.get("Authors")),
        "year": clean_text(row.get("Year")),
        "source_title": source_title,
        "doi": doi,
        "scopus_link": clean_text(row.get("Link")),
        "eid": clean_text(row.get("EID")),
        "open_access": clean_text(row.get("Open Access")),
        "pdf_path": out.name,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    if out.exists() and out.stat().st_size > 10_000:
        rec = {**base_record, "status": "pdf_ready", "source": "existing_file", "notes": "PDF already present"}
        return corpus_id, rec, []

    failed: list[dict] = []
    attempted = 0
    seen_urls: set[str] = set()

    def try_url_list(urls: list[str], phase: str) -> tuple[bool, str | None, str | None]:
        nonlocal attempted, failed, seen_urls
        if args.max_candidates:
            remaining = max(0, args.max_candidates - attempted)
            urls = urls[:remaining]
        for url in urls:
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            attempted += 1
            ok, reason = download_pdf(url, out, timeout=args.download_timeout)
            if ok:
                return True, url, reason
            failed.append({"phase": phase, "url": url, "reason": reason})
            if args.sleep_between_candidates:
                time.sleep(args.sleep_between_candidates)
            if args.max_candidates and attempted >= args.max_candidates:
                break
        return False, None, None

    phases: list[tuple[str, list[str]]] = []
    try:
        phases.append(("direct", publisher_direct_candidate_urls(row)))
    except Exception as e:
        failed.append({"phase": "direct", "url": None, "reason": f"candidate generation failed: {type(e).__name__}: {e}"})
    if not args.no_api:
        try:
            phases.append(("oa_api", api_candidate_urls(row)))
        except Exception as e:
            failed.append({"phase": "oa_api", "url": None, "reason": f"candidate generation failed: {type(e).__name__}: {e}"})
    if not args.no_scrape:
        try:
            phases.append(("landing_page", scrape_candidate_urls(row)))
        except Exception as e:
            failed.append({"phase": "landing_page", "url": None, "reason": f"candidate generation failed: {type(e).__name__}: {e}"})

    for phase, urls in phases:
        ok, url, reason = try_url_list(urls, phase)
        if ok:
            rec = {
                **base_record,
                "status": "pdf_ready",
                "source": f"automatic_oa_{phase}",
                "pdf_url": url,
                "attempted_candidates": attempted,
                "notes": reason,
            }
            return corpus_id, rec, failed
        if args.max_candidates and attempted >= args.max_candidates:
            break

    rec = {
        **base_record,
        "status": "requires_manual_download",
        "source": "not_retrieved",
        "attempted_candidates": attempted,
        "notes": "No candidate OA PDF URL produced a usable PDF automatically.",
    }
    return corpus_id, rec, failed


def write_markdown_status(status_by_id: dict[str, dict], failed_by_id: dict[str, list[dict]]) -> None:
    rows = [status_by_id[k] for k in sorted(status_by_id, key=lambda x: int(x.split("-")[-1]))]
    total = len(rows)
    ready = [r for r in rows if r.get("status") == "pdf_ready"]
    missing = [r for r in rows if r.get("status") != "pdf_ready"]
    counter = Counter(r.get("status", "unknown") for r in rows)
    src_counter = Counter(r.get("source", "unknown") for r in ready)

    lines = []
    lines.append("# PDF Retrieval Status")
    lines.append("")
    lines.append(f"- Review/extraction folder: `{BASE_DIR}`")
    lines.append(f"- Source CSV: `{CSV_PATH.name}`")
    lines.append(f"- Total CSV entries processed: {total}")
    lines.append(f"- PDFs present in this folder: {len(list(BASE_DIR.glob('paper-*.pdf'))) }")
    lines.append(f"- Retrieved/ready: {len(ready)}")
    lines.append(f"- Still requiring manual download: {len(missing)}")
    lines.append(f"- Updated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Status counts")
    for k, v in counter.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Ready source counts")
    for k, v in src_counter.most_common():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Retrieval summary")
    lines.append("| corpus_id | Year | Source | Title | DOI | Retrieval status | PDF path | Notes |")
    lines.append("|---|---:|---|---|---|---|---|---|")
    for r in rows:
        title = (r.get("title") or "").replace("|", "\\|")
        source = (r.get("source_title") or "").replace("|", "\\|")
        notes = (r.get("notes") or "").replace("|", "\\|")
        lines.append(
            f"| {r.get('corpus_id')} | {r.get('year','')} | {source} | {title} | {r.get('doi','')} | "
            f"{r.get('status','')} | {r.get('pdf_path','')} | {notes} |"
        )
    lines.append("")
    lines.append("## Still missing / manual download candidates")
    if missing:
        lines.append("Download obtainable PDFs for these entries manually if needed, using the DOI/publisher page, and keep the normalized paper IDs when renaming.")
        for r in missing:
            lines.append(f"- {r.get('corpus_id')}: {r.get('title')} — DOI: https://doi.org/{r.get('doi')}")
    else:
        lines.append("- None")

    tmp = STATUS_MD.with_suffix(".md.tmp")
    tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    tmp.replace(STATUS_MD)

    # Keep detailed failed URL diagnostics outside the human-facing markdown.
    tmpj = FAILED_CANDIDATES_JSON.with_suffix(".json.tmp")
    with tmpj.open("w", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(timespec="seconds"), "failed_candidates": failed_by_id}, f, ensure_ascii=False, indent=2)
    tmpj.replace(FAILED_CANDIDATES_JSON)


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve OA PDFs for a Scopus CSV into the same folder.")
    parser.add_argument("--workers", type=int, default=4, help="parallel downloads")
    parser.add_argument("--limit", type=int, default=0, help="process only the first N selected rows")
    parser.add_argument("--start", type=int, default=1, help="1-based row index to start at")
    parser.add_argument("--end", type=int, default=0, help="1-based row index to end at, inclusive")
    parser.add_argument("--retry-missing", action="store_true", help="retry rows previously marked missing")
    parser.add_argument("--no-api", action="store_true", help="skip OpenAlex/Unpaywall/Semantic Scholar API candidates")
    parser.add_argument("--no-scrape", action="store_true", help="skip DOI landing-page scrape candidates")
    parser.add_argument("--max-candidates", type=int, default=0, help="cap candidate URLs per paper (0 = no cap)")
    parser.add_argument("--download-timeout", type=int, default=90)
    parser.add_argument("--sleep-between-candidates", type=float, default=0.0)
    parser.add_argument("--status-every", type=int, default=25)
    args = parser.parse_args()

    print(f"Source CSV: {CSV_PATH}", flush=True)
    print(f"Output folder: {BASE_DIR}", flush=True)
    rows = load_rows()
    prior = load_status()
    status_by_id: dict[str, dict] = dict(prior)
    failed_by_id: dict[str, list[dict]] = {}
    if FAILED_CANDIDATES_JSON.exists():
        try:
            failed_by_id = json.loads(FAILED_CANDIDATES_JSON.read_text(encoding="utf-8")).get("failed_candidates", {})
        except Exception:
            failed_by_id = {}

    tasks = []
    for idx, row in enumerate(rows, start=1):
        if idx < args.start:
            continue
        if args.end and idx > args.end:
            continue
        corpus_id = f"paper-{idx:04d}"
        out = normalized_pdf_path(idx, row)
        prev = status_by_id.get(corpus_id)
        if out.exists() and out.stat().st_size > 10_000:
            status_by_id[corpus_id] = {
                **(prev or {}),
                "corpus_id": corpus_id,
                "index": idx,
                "title": clean_text(row.get("Title")),
                "authors": clean_text(row.get("Authors")),
                "year": clean_text(row.get("Year")),
                "source_title": clean_text(row.get("Source title")),
                "doi": clean_text(row.get("DOI")),
                "scopus_link": clean_text(row.get("Link")),
                "eid": clean_text(row.get("EID")),
                "open_access": clean_text(row.get("Open Access")),
                "pdf_path": out.name,
                "status": "pdf_ready",
                "source": "existing_file",
                "notes": "PDF already present",
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            }
            continue
        if prev and prev.get("status") == "pdf_ready" and not args.retry_missing:
            continue
        if prev and prev.get("status") == "requires_manual_download" and not args.retry_missing:
            continue
        tasks.append((idx, row))
        if args.limit and len(tasks) >= args.limit:
            break

    print(f"Rows in CSV: {len(rows)}", flush=True)
    print(f"Rows queued now: {len(tasks)}", flush=True)
    completed = 0
    if tasks:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
            futures = {ex.submit(retrieve_one, idx, row, args): idx for idx, row in tasks}
            for fut in as_completed(futures):
                idx = futures[fut]
                completed += 1
                try:
                    corpus_id, rec, failed = fut.result()
                except Exception as e:
                    corpus_id = f"paper-{idx:04d}"
                    rec = {
                        "corpus_id": corpus_id,
                        "index": idx,
                        "status": "error",
                        "source": "batch_script",
                        "notes": f"Unhandled error: {type(e).__name__}: {e}",
                        "updated_at": datetime.now().isoformat(timespec="seconds"),
                    }
                    failed = []
                status_by_id[corpus_id] = rec
                failed_by_id[corpus_id] = failed
                marker = "OK" if rec.get("status") == "pdf_ready" else "MISS"
                print(f"[{completed}/{len(tasks)}] {marker} {corpus_id} {rec.get('doi','')} {rec.get('title','')[:80]}", flush=True)
                if completed % max(1, args.status_every) == 0:
                    save_status(status_by_id)
                    write_markdown_status(status_by_id, failed_by_id)
    save_status(status_by_id)
    write_markdown_status(status_by_id, failed_by_id)
    ready = sum(1 for r in status_by_id.values() if r.get("status") == "pdf_ready")
    missing = sum(1 for r in status_by_id.values() if r.get("status") != "pdf_ready")
    print(f"Done. Ready={ready} Missing/other={missing}", flush=True)
    print(f"Status: {STATUS_MD}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
