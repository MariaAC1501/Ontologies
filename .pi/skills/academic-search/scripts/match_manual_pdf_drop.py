#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pypdf",
# ]
# ///

"""Match raw user-downloaded PDFs in manual-pdf-drop/ to corpus entries."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

from pypdf import PdfReader

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
TITLE_WORD_RE = re.compile(r"[a-z0-9]+")


@dataclass
class CorpusEntry:
    corpus_id: str
    title: str
    year: str
    doi: str
    screening_tier: str
    raw: dict


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def slugify(text: str, max_len: int = 90) -> str:
    words = TITLE_WORD_RE.findall(normalize_text(text))
    slug = "-".join(words)[:max_len].strip("-")
    return slug or "untitled"


def extract_pdf_signals(pdf_path: Path) -> dict:
    info = {
        "metadata_title": "",
        "text_title": "",
        "doi": "",
        "first_page_excerpt": "",
        "page_count": None,
        "error": None,
    }
    try:
        reader = PdfReader(str(pdf_path))
        info["page_count"] = len(reader.pages)
        meta_title = getattr(reader.metadata, "title", "") if reader.metadata else ""
        if meta_title:
            info["metadata_title"] = str(meta_title).strip()

        first_page_text = ""
        if reader.pages:
            try:
                first_page_text = reader.pages[0].extract_text() or ""
            except Exception:
                first_page_text = ""

        first_page_text = first_page_text.strip()
        info["first_page_excerpt"] = first_page_text[:1500]

        doi_match = DOI_RE.search(first_page_text)
        if not doi_match and info["metadata_title"]:
            doi_match = DOI_RE.search(info["metadata_title"])
        if doi_match:
            info["doi"] = doi_match.group(0).rstrip(".);,")

        lines = [re.sub(r"\s+", " ", line).strip() for line in first_page_text.splitlines()]
        lines = [line for line in lines if len(line) >= 20]
        title_line = ""
        for line in lines[:12]:
            low = line.lower()
            if any(bad in low for bad in ["abstract", "introduction", "keywords", "author", "doi:"]):
                continue
            if len(line) > 220:
                continue
            title_line = line
            break
        if title_line:
            info["text_title"] = title_line
    except Exception as exc:
        info["error"] = str(exc)
    return info


def load_corpus(corpus_path: Path) -> list[CorpusEntry]:
    data = json.loads(corpus_path.read_text())
    results = data.get("results", data)
    entries: list[CorpusEntry] = []
    for item in results:
        entries.append(
            CorpusEntry(
                corpus_id=str(item.get("corpus_id") or item.get("id") or ""),
                title=str(item.get("title") or "").strip(),
                year=str(item.get("year") or ""),
                doi=str(item.get("doi") or "").strip(),
                screening_tier=str(item.get("screening_tier") or "supporting"),
                raw=item,
            )
        )
    return entries


def title_similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def stable_pdf_name(entry: CorpusEntry) -> str:
    return f"{entry.corpus_id}_{entry.year}_{slugify(entry.title)}.pdf"


def choose_match(signals: dict, filename: str, entries: list[CorpusEntry]) -> tuple[CorpusEntry | None, str, float]:
    doi = (signals.get("doi") or "").lower().strip()
    if doi:
        for entry in entries:
            if entry.doi and entry.doi.lower().strip() == doi:
                return entry, "doi", 1.0

    candidates = [signals.get("metadata_title") or "", signals.get("text_title") or "", Path(filename).stem]
    best_entry = None
    best_score = 0.0
    best_source = ""
    for candidate in candidates:
        if not candidate:
            continue
        for entry in entries:
            score = title_similarity(candidate, entry.title)
            if score > best_score:
                best_score = score
                best_entry = entry
                best_source = "title"

    if best_entry and best_score >= 0.92:
        return best_entry, best_source, best_score
    if best_entry and best_score >= 0.80:
        return best_entry, "needs_review", best_score
    return None, "unmatched", best_score


def main() -> None:
    parser = argparse.ArgumentParser(description="Match raw PDFs in manual-pdf-drop/ to corpus entries and normalize them into papers/.")
    parser.add_argument("--corpus", required=True, help="Path to corpus.json")
    parser.add_argument("--manual-dir", required=True, help="Path to manual-pdf-drop/")
    parser.add_argument("--papers-dir", required=True, help="Path to normalized papers/")
    parser.add_argument("--report-path", required=True, help="Path to write JSON report")
    parser.add_argument("--copy", action="store_true", help="Copy matched files into papers/ (default behavior).")
    parser.add_argument("--move", action="store_true", help="Move matched files into papers/ instead of copying.")
    args = parser.parse_args()

    corpus_path = Path(args.corpus).expanduser()
    manual_dir = Path(args.manual_dir).expanduser()
    papers_dir = Path(args.papers_dir).expanduser()
    report_path = Path(args.report_path).expanduser()

    entries = load_corpus(corpus_path)
    papers_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    raw_pdfs = sorted([p for p in manual_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])
    matched = []
    needs_review = []
    unmatched = []
    matched_ids = set()

    for pdf_path in raw_pdfs:
        signals = extract_pdf_signals(pdf_path)
        entry, mode, score = choose_match(signals, pdf_path.name, entries)
        record = {
            "raw_file": pdf_path.name,
            "signals": signals,
            "match_mode": mode,
            "score": round(score, 4),
        }
        if entry is None:
            unmatched.append(record)
            continue

        record.update(
            {
                "corpus_id": entry.corpus_id,
                "title": entry.title,
                "screening_tier": entry.screening_tier,
                "normalized_pdf": stable_pdf_name(entry),
            }
        )
        if mode == "needs_review":
            needs_review.append(record)
            continue

        destination = papers_dir / stable_pdf_name(entry)
        if args.move:
            shutil.move(str(pdf_path), str(destination))
        else:
            shutil.copy2(str(pdf_path), str(destination))
        matched_ids.add(entry.corpus_id)
        record["destination"] = str(destination)
        matched.append(record)

    still_missing = []
    for entry in entries:
        expected = papers_dir / stable_pdf_name(entry)
        if entry.corpus_id not in matched_ids and not expected.exists():
            still_missing.append(
                {
                    "corpus_id": entry.corpus_id,
                    "title": entry.title,
                    "screening_tier": entry.screening_tier,
                    "expected_pdf": str(expected),
                }
            )

    report = {
        "corpus_path": str(corpus_path),
        "manual_dir": str(manual_dir),
        "papers_dir": str(papers_dir),
        "matched": matched,
        "needs_review": needs_review,
        "unmatched": unmatched,
        "still_missing": still_missing,
        "summary": {
            "raw_pdfs": len(raw_pdfs),
            "matched": len(matched),
            "needs_review": len(needs_review),
            "unmatched": len(unmatched),
            "still_missing": len(still_missing),
        },
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
