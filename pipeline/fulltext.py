#!/usr/bin/env python3
"""Prepare complete, provenance-aware full text for publication extraction.

The publication path uses Docling through OntoCast's ``doc-processing`` extra.
A normal layout-aware conversion is quality checked first. Low-quality output is
retried with full-page OCR, then the better candidate is retained. No LLM call
is made by this module.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.metadata
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

SCHEMA_VERSION = "fulltext-preparation/1.0"
CORPUS_SCHEMA_VERSION = "fulltext-corpus-manifest/1.0"
PAGE_MARKER_RE = re.compile(r"(?m)^<!--\s*PDF_PAGE:\s*(\d+)\s*-->\s*$")
FRONT_MATTER_PAGE_COUNT_RE = re.compile(r"(?m)^page_count:\s*[\"']?(\d+)[\"']?\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
HTML_TABLE_RE = re.compile(r"<table\b.*?</table\s*>", re.IGNORECASE | re.DOTALL)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_TAG_RE = re.compile(r"<[^>]+>")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class FullTextError(RuntimeError):
    """Raised when a publication full-text invariant is violated."""


@dataclass(frozen=True)
class QualityThresholds:
    min_text_chars_per_page: int = 80
    max_low_text_page_fraction: float = 0.15
    duplicate_similarity: float = 0.985
    min_duplicate_chars: int = 200
    boilerplate_page_fraction: float = 0.60
    max_boilerplate_char_fraction: float = 0.35


@dataclass(frozen=True)
class CorpusRecord:
    corpus_id: str
    bibliographic_status: str
    partition: str
    title: str
    doi: str
    year: int
    pdf_path: str
    pdf_sha256: str
    source_url: str | None = None
    licence: str | None = None


@dataclass(frozen=True)
class ConversionCandidate:
    markdown: str
    expected_pages: int
    conversion_status: str
    conversion_errors: tuple[str, ...]
    missing_document_pages: tuple[int, ...]
    force_full_page_ocr: bool
    settings: dict[str, Any]
    table_count: int = 0


@dataclass(frozen=True)
class PreparedDocument:
    output_dir: Path
    input_json: Path
    markdown: Path
    source_map: Path
    quality: Path
    processing: Path
    bibliography: Path
    quality_status: str
    selected_attempt: str


class _TableShapeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows = 0
        self.current_columns = 0
        self.max_columns = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized = tag.lower()
        if normalized == "tr":
            self.rows += 1
            self.current_columns = 0
        elif normalized in {"td", "th"}:
            colspan = 1
            for name, value in attrs:
                if name.lower() == "colspan" and value:
                    try:
                        colspan = max(1, int(value))
                    except ValueError:
                        colspan = 1
            self.current_columns += colspan
            self.max_columns = max(self.max_columns, self.current_columns)


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def software_versions() -> dict[str, str | None]:
    return {
        "python": sys.version.split()[0],
        "ontocast": package_version("ontocast"),
        "docling": package_version("docling"),
        "docling-core": package_version("docling-core"),
        "docling-parse": package_version("docling-parse"),
        "easyocr": package_version("easyocr"),
        "rapidocr": package_version("rapidocr"),
        "pypdfium2": package_version("pypdfium2"),
    }


def canonical_doi(value: str) -> str:
    doi = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi = doi[len(prefix) :]
            break
    if not DOI_RE.fullmatch(doi) or any(character.isspace() for character in doi):
        raise FullTextError(f"Invalid DOI: {value!r}")
    return doi


def _require_string(record: dict[str, Any], name: str) -> str:
    value = record.get(name)
    if not isinstance(value, str) or not value.strip():
        raise FullTextError(f"Corpus record field {name!r} must be a non-empty string")
    return value.strip()


def parse_corpus_record(raw: dict[str, Any]) -> CorpusRecord:
    allowed = {
        "corpus_id",
        "bibliographic_status",
        "partition",
        "title",
        "doi",
        "year",
        "pdf_path",
        "pdf_sha256",
        "source_url",
        "licence",
    }
    extras = set(raw) - allowed
    if extras:
        raise FullTextError(
            f"Unknown corpus record field(s): {', '.join(sorted(extras))}"
        )
    year = raw.get("year")
    if not isinstance(year, int) or isinstance(year, bool) or not 1900 <= year <= 2100:
        raise FullTextError(
            "Corpus record year must be an integer from 1900 through 2100"
        )
    digest = _require_string(raw, "pdf_sha256").lower()
    if not SHA256_RE.fullmatch(digest):
        raise FullTextError(
            "Corpus record pdf_sha256 must contain 64 lowercase hexadecimal characters"
        )
    status = _require_string(raw, "bibliographic_status")
    if status not in {"provisional", "verified"}:
        raise FullTextError("bibliographic_status must be provisional or verified")
    partition = _require_string(raw, "partition")
    if partition not in {"development", "held_out", "reserve", "unassigned"}:
        raise FullTextError("Unknown corpus partition")
    source_url = raw.get("source_url")
    licence = raw.get("licence")
    if source_url is not None and not isinstance(source_url, str):
        raise FullTextError("source_url must be a string or null")
    if licence is not None and not isinstance(licence, str):
        raise FullTextError("licence must be a string or null")
    return CorpusRecord(
        corpus_id=_require_string(raw, "corpus_id"),
        bibliographic_status=status,
        partition=partition,
        title=_require_string(raw, "title"),
        doi=canonical_doi(_require_string(raw, "doi")),
        year=year,
        pdf_path=_require_string(raw, "pdf_path"),
        pdf_sha256=digest,
        source_url=source_url.strip()
        if isinstance(source_url, str) and source_url.strip()
        else None,
        licence=licence.strip()
        if isinstance(licence, str) and licence.strip()
        else None,
    )


def load_corpus_manifest(
    path: Path,
    *,
    require_verified: bool = True,
) -> tuple[Path, dict[str, CorpusRecord], dict[str, Any]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise FullTextError(
            f"Could not read corpus manifest {path}: {error}"
        ) from error
    if not isinstance(raw, dict):
        raise FullTextError("Corpus manifest must be a JSON object")
    allowed = {"schema_version", "base_dir", "partition_frozen", "records"}
    extras = set(raw) - allowed
    if extras:
        raise FullTextError(
            f"Unknown corpus manifest field(s): {', '.join(sorted(extras))}"
        )
    if raw.get("schema_version") != CORPUS_SCHEMA_VERSION:
        raise FullTextError(
            f"Expected corpus manifest schema_version {CORPUS_SCHEMA_VERSION!r}"
        )
    base_dir_value = raw.get("base_dir", ".")
    if not isinstance(base_dir_value, str) or not base_dir_value.strip():
        raise FullTextError("Corpus manifest base_dir must be a non-empty string")
    base_dir = Path(os.path.realpath(path.resolve().parent / base_dir_value))
    records_raw = raw.get("records")
    if not isinstance(records_raw, list) or not records_raw:
        raise FullTextError("Corpus manifest records must be a non-empty array")
    records: dict[str, CorpusRecord] = {}
    dois: set[str] = set()
    for item in records_raw:
        if not isinstance(item, dict):
            raise FullTextError("Each corpus record must be an object")
        record = parse_corpus_record(item)
        if record.corpus_id in records:
            raise FullTextError(f"Duplicate corpus_id: {record.corpus_id}")
        if record.doi in dois:
            raise FullTextError(f"Duplicate DOI: {record.doi}")
        if require_verified and record.bibliographic_status != "verified":
            raise FullTextError(
                f"Corpus record {record.corpus_id} is not human-verified"
            )
        records[record.corpus_id] = record
        dois.add(record.doi)
    if require_verified and raw.get("partition_frozen") is not True:
        raise FullTextError("Publication preparation requires partition_frozen=true")
    return base_dir, records, raw


def resolve_pdf(base_dir: Path, record: CorpusRecord) -> Path:
    relative = Path(record.pdf_path)
    if relative.is_absolute():
        raise FullTextError(
            f"PDF path must be relative to manifest base_dir: {record.pdf_path}"
        )
    base_dir = Path(os.path.realpath(base_dir))
    candidate = base_dir / relative
    try:
        resolved = Path(os.path.realpath(candidate.resolve(strict=True)))
    except OSError as error:
        raise FullTextError(
            f"PDF for {record.corpus_id} is unavailable: {candidate}"
        ) from error
    try:
        resolved.relative_to(base_dir)
    except ValueError as error:
        raise FullTextError(
            f"PDF path escapes manifest base_dir: {record.pdf_path}"
        ) from error
    current = base_dir
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise FullTextError(f"PDF path contains a symbolic link: {record.pdf_path}")
    if not resolved.is_file():
        raise FullTextError(f"PDF path is not a regular file: {record.pdf_path}")
    digest = sha256_file(resolved)
    if digest != record.pdf_sha256:
        raise FullTextError(
            f"PDF checksum mismatch for {record.corpus_id}: expected {record.pdf_sha256}, got {digest}"
        )
    return resolved


def verified_metadata_header(record: CorpusRecord) -> str:
    fields = {
        "corpus_id": record.corpus_id,
        "doi": record.doi,
        "title": record.title,
        "year": record.year,
    }
    lines = ["<!-- VERIFIED_SOURCE_METADATA"]
    lines.extend(
        f"{name}: {json.dumps(value, ensure_ascii=False)}"
        for name, value in fields.items()
    )
    lines.append("END_VERIFIED_SOURCE_METADATA -->")
    return "\n".join(lines) + "\n\n"


def split_pages(markdown: str) -> tuple[list[int], dict[int, str], list[int]]:
    matches = list(PAGE_MARKER_RE.finditer(markdown))
    observed = [int(match.group(1)) for match in matches]
    pages: dict[int, str] = {}
    repeated: list[int] = []
    for index, match in enumerate(matches):
        page = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[match.end() : end]
        if page in pages:
            repeated.append(page)
            pages[page] += "\n" + body
        else:
            pages[page] = body
    return observed, pages, repeated


def _plain_text(value: str) -> str:
    text = HTML_COMMENT_RE.sub(" ", value)
    text = HTML_TAG_RE.sub(" ", text)
    text = html.unescape(text)
    text = re.sub(r"!\[[^\]]*]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_#>|~=-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _normalized_lines(value: str) -> list[str]:
    result: list[str] = []
    for raw in value.splitlines():
        line = _plain_text(raw).casefold()
        line = re.sub(r"\b\d+\b", "#", line)
        line = re.sub(r"[^\w#]+", " ", line)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) >= 12:
            result.append(line)
    return result


def _normalized_page(value: str, boilerplate: set[str]) -> str:
    lines = [line for line in _normalized_lines(value) if line not in boilerplate]
    return " ".join(lines)


def analyze_markdown(
    markdown: str,
    expected_pages: int,
    *,
    conversion_status: str = "success",
    conversion_errors: Iterable[str] = (),
    missing_document_pages: Iterable[int] = (),
    thresholds: QualityThresholds | None = None,
) -> dict[str, Any]:
    limits = thresholds or QualityThresholds()
    observed, pages, repeated = split_pages(markdown)
    expected = set(range(1, expected_pages + 1))
    observed_set = set(observed)
    missing = sorted(expected - observed_set)
    unexpected = sorted(observed_set - expected)
    out_of_order = observed != sorted(observed) or observed[:1] not in ([], [1])
    parser_missing = sorted(set(int(value) for value in missing_document_pages))

    page_characters = {
        str(page): len(re.sub(r"\s+", "", _plain_text(pages.get(page, ""))))
        for page in range(1, expected_pages + 1)
    }
    low_text_pages = sorted(
        int(page)
        for page, count in page_characters.items()
        if count < limits.min_text_chars_per_page
    )
    low_fraction = len(low_text_pages) / expected_pages if expected_pages else 1.0

    line_pages: dict[str, set[int]] = {}
    line_lengths: dict[str, int] = {}
    for page, body in pages.items():
        for line in set(_normalized_lines(body)):
            line_pages.setdefault(line, set()).add(page)
            line_lengths[line] = len(line)
    boilerplate_min_pages = max(
        2, int(expected_pages * limits.boilerplate_page_fraction + 0.999)
    )
    boilerplate_lines = {
        line
        for line, found_pages in line_pages.items()
        if len(found_pages) >= boilerplate_min_pages
    }
    total_chars = sum(page_characters.values())
    boilerplate_chars = sum(
        line_lengths[line] * len(line_pages[line]) for line in boilerplate_lines
    )
    boilerplate_fraction = (
        min(1.0, boilerplate_chars / total_chars) if total_chars else 1.0
    )

    normalized = {}
    for page, body in pages.items():
        core = _normalized_page(body, boilerplate_lines)
        full = _normalized_page(body, set())
        normalized[page] = core if len(core) >= limits.min_duplicate_chars else full
    duplicate_pairs: list[dict[str, Any]] = []
    page_numbers = sorted(normalized)
    for left_index, left in enumerate(page_numbers):
        left_text = normalized[left]
        if len(left_text) < limits.min_duplicate_chars:
            continue
        for right in page_numbers[left_index + 1 :]:
            right_text = normalized[right]
            if len(right_text) < limits.min_duplicate_chars:
                continue
            if left_text == right_text:
                similarity = 1.0
            else:
                length_ratio = min(len(left_text), len(right_text)) / max(
                    len(left_text), len(right_text)
                )
                if length_ratio < limits.duplicate_similarity:
                    continue
                similarity = SequenceMatcher(
                    None, left_text, right_text, autojunk=False
                ).ratio()
            if similarity >= limits.duplicate_similarity:
                duplicate_pairs.append(
                    {
                        "left_page": left,
                        "right_page": right,
                        "similarity": round(similarity, 6),
                    }
                )

    errors = [str(error) for error in conversion_errors if str(error).strip()]
    truncated = bool(
        missing
        or parser_missing
        or expected_pages <= 0
        or conversion_status.casefold() not in {"success", "partial_success"}
        or any(
            "timeout" in error.casefold() or "truncat" in error.casefold()
            for error in errors
        )
    )
    issue_codes: list[str] = []
    if missing or parser_missing:
        issue_codes.append("missing_pages")
    if repeated:
        issue_codes.append("repeated_page_markers")
    if unexpected:
        issue_codes.append("unexpected_pages")
    if out_of_order:
        issue_codes.append("out_of_order_pages")
    if truncated:
        issue_codes.append("truncated_conversion")
    if low_fraction > limits.max_low_text_page_fraction:
        issue_codes.append("low_text_coverage")
    if duplicate_pairs:
        issue_codes.append("duplicated_pages")
    if boilerplate_fraction > limits.max_boilerplate_char_fraction:
        issue_codes.append("boilerplate_dominance")
    if errors:
        issue_codes.append("conversion_errors")

    fatal_codes = {
        "missing_pages",
        "repeated_page_markers",
        "unexpected_pages",
        "out_of_order_pages",
        "truncated_conversion",
        "low_text_coverage",
        "duplicated_pages",
        "boilerplate_dominance",
        "conversion_errors",
    }
    status = "fail" if fatal_codes.intersection(issue_codes) else "pass"
    rank = [
        len(fatal_codes.intersection(issue_codes)),
        len(missing) + len(parser_missing),
        len(duplicate_pairs),
        len(low_text_pages),
        round(boilerplate_fraction, 6),
        -total_chars,
    ]
    return {
        "schema_version": "fulltext-quality/1.0",
        "status": status,
        "expected_page_count": expected_pages,
        "observed_page_markers": observed,
        "missing_pages": missing,
        "missing_document_pages": parser_missing,
        "repeated_page_markers": sorted(set(repeated)),
        "unexpected_pages": unexpected,
        "out_of_order": out_of_order,
        "truncated": truncated,
        "page_text_characters": page_characters,
        "low_text_pages": low_text_pages,
        "low_text_page_fraction": round(low_fraction, 6),
        "duplicate_pages": duplicate_pairs,
        "boilerplate": {
            "line_count": len(boilerplate_lines),
            "character_fraction": round(boilerplate_fraction, 6),
            "sample_lines": sorted(boilerplate_lines)[:20],
        },
        "conversion_status": conversion_status,
        "conversion_errors": errors,
        "issue_codes": issue_codes,
        "quality_rank": rank,
        "thresholds": asdict(limits),
    }


def _markdown_table_shape(text: str) -> tuple[int, int]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    rows = len(lines)
    columns = 0
    for line in lines:
        if "|" not in line:
            continue
        cells = [cell for cell in line.strip("|").split("|")]
        columns = max(columns, len(cells))
    return rows, columns


def _html_table_shape(text: str) -> tuple[int, int]:
    parser = _TableShapeParser()
    parser.feed(text)
    return parser.rows, parser.max_columns


def _block_kind(text: str) -> str:
    stripped = text.strip()
    if HEADING_RE.match(stripped):
        return "section"
    if HTML_TABLE_RE.search(stripped):
        return "table"
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    if len(lines) >= 2 and all("|" in line for line in lines):
        return "table"
    if stripped.startswith("![") or stripped.startswith("<!-- image"):
        return "image"
    if lines and all(re.match(r"^(?:[-*+] |\d+[.)] )", line) for line in lines):
        return "list"
    return "paragraph"


def build_source_map(markdown: str, corpus_id: str) -> dict[str, Any]:
    matches = list(PAGE_MARKER_RE.finditer(markdown))
    page_ranges: list[tuple[int, int, int]] = []
    for index, match in enumerate(matches):
        page = int(match.group(1))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        page_ranges.append((page, match.end(), end))

    blocks: list[dict[str, Any]] = []
    section_levels: dict[int, str] = {}
    paragraph_index = 0
    for page, page_start, page_end in page_ranges:
        body = markdown[page_start:page_end]
        cursor = page_start
        buffer_start: int | None = None
        buffer_end: int | None = None

        def flush() -> None:
            nonlocal buffer_start, buffer_end, paragraph_index, section_levels
            if buffer_start is None or buffer_end is None:
                return
            start = buffer_start
            end = buffer_end
            while start < end and markdown[start].isspace():
                start += 1
            while end > start and markdown[end - 1].isspace():
                end -= 1
            buffer_start = None
            buffer_end = None
            if start >= end:
                return
            value = markdown[start:end]
            kind = _block_kind(value)
            heading = HEADING_RE.match(value.strip()) if kind == "section" else None
            if heading:
                level = len(heading.group(1))
                section_levels = {
                    key: val for key, val in section_levels.items() if key < level
                }
                section_levels[level] = heading.group(2).strip()
                paragraph = None
            else:
                paragraph_index += 1
                paragraph = paragraph_index
            table_shape: dict[str, int] | None = None
            if kind == "table":
                rows, columns = (
                    _html_table_shape(value)
                    if HTML_TABLE_RE.search(value)
                    else _markdown_table_shape(value)
                )
                table_shape = {"rows": rows, "columns": columns}
            block_number = len(blocks) + 1
            block = {
                "block_id": f"{corpus_id}-b{block_number:06d}",
                "kind": kind,
                "page": page,
                "section_path": [section_levels[key] for key in sorted(section_levels)],
                "paragraph": paragraph,
                "char_start": start,
                "char_end": end,
                "sha256": sha256_bytes(value.encode("utf-8")),
            }
            if table_shape is not None:
                block["table_shape"] = table_shape
            blocks.append(block)

        for line in body.splitlines(keepends=True):
            line_start = cursor
            line_end = cursor + len(line)
            cursor = line_end
            if line.strip():
                if buffer_start is None:
                    buffer_start = line_start
                buffer_end = line_end
            else:
                flush()
        flush()

    for block in blocks:
        start = block["char_start"]
        end = block["char_end"]
        if sha256_bytes(markdown[start:end].encode("utf-8")) != block["sha256"]:
            raise FullTextError(
                f"Source-map character span failed for {block['block_id']}"
            )
    tables = [block["block_id"] for block in blocks if block["kind"] == "table"]
    return {
        "schema_version": "fulltext-source-map/1.0",
        "corpus_id": corpus_id,
        "text_sha256": sha256_bytes(markdown.encode("utf-8")),
        "character_count": len(markdown),
        "page_count": len(page_ranges),
        "block_count": len(blocks),
        "table_blocks": tables,
        "blocks": blocks,
    }


def validate_source_map(markdown: str, source_map: dict[str, Any]) -> None:
    if source_map.get("text_sha256") != sha256_bytes(markdown.encode("utf-8")):
        raise FullTextError("Source-map text checksum does not match prepared Markdown")
    previous_end = 0
    seen_ids: set[str] = set()
    for block in source_map.get("blocks", []):
        block_id = block.get("block_id")
        if not isinstance(block_id, str) or block_id in seen_ids:
            raise FullTextError("Source-map block IDs must be unique strings")
        seen_ids.add(block_id)
        start = block.get("char_start")
        end = block.get("char_end")
        if (
            not isinstance(start, int)
            or not isinstance(end, int)
            or not 0 <= start < end <= len(markdown)
        ):
            raise FullTextError(f"Invalid source-map span for {block_id}")
        if start < previous_end:
            raise FullTextError(f"Overlapping source-map span for {block_id}")
        if sha256_bytes(markdown[start:end].encode("utf-8")) != block.get("sha256"):
            raise FullTextError(f"Source-map text mismatch for {block_id}")
        previous_end = end


def _ocr_options(engine: str, force_full_page_ocr: bool):
    from docling.datamodel.pipeline_options import (
        EasyOcrOptions,
        OcrAutoOptions,
        RapidOcrOptions,
    )

    if engine == "easyocr":
        return EasyOcrOptions(lang=["en"], force_full_page_ocr=force_full_page_ocr)
    if engine == "rapidocr":
        return RapidOcrOptions(force_full_page_ocr=force_full_page_ocr)
    if engine == "auto":
        return OcrAutoOptions(force_full_page_ocr=force_full_page_ocr)
    raise FullTextError(f"Unsupported OCR engine: {engine}")


def convert_with_docling(
    pdf_path: Path,
    *,
    force_full_page_ocr: bool,
    ocr_engine: str = "easyocr",
) -> ConversionCandidate:
    try:
        from docling.datamodel.accelerator_options import AcceleratorDevice
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import (
            PdfPipelineOptions,
            TableFormerMode,
        )
        from docling.document_converter import DocumentConverter, PdfFormatOption
    except ImportError as error:
        raise FullTextError(
            "Docling is unavailable. Install OntoCast's document stack with "
            "uv pip install --python .venv/bin/python -e 'external/ontocast[doc-processing]'."
        ) from error

    options = PdfPipelineOptions()
    options.accelerator_options.device = AcceleratorDevice.CPU
    options.do_ocr = True
    options.ocr_options = _ocr_options(ocr_engine, force_full_page_ocr)
    options.do_table_structure = True
    if hasattr(options.table_structure_options, "mode"):
        options.table_structure_options.mode = TableFormerMode.ACCURATE
    options.generate_parsed_pages = True
    converter = DocumentConverter(
        allowed_formats=[InputFormat.PDF],
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)},
    )
    result = converter.convert(pdf_path)
    expected_pages = int(
        getattr(result.input, "page_count", 0) or len(result.document.pages)
    )
    document_pages = {int(page) for page in result.document.pages}
    missing_pages = tuple(sorted(set(range(1, expected_pages + 1)) - document_pages))
    rendered: list[str] = []
    for page in range(1, expected_pages + 1):
        rendered.append(f"<!-- PDF_PAGE: {page} -->\n")
        if page in document_pages:
            page_text = result.document.export_to_markdown(
                page_no=page,
                compact_tables=False,
                image_placeholder="<!-- image -->",
            ).strip()
            rendered.append(page_text + "\n" if page_text else "\n")
        rendered.append("\n")
    status = str(getattr(result.status, "value", result.status)).lower()
    errors = tuple(
        str(getattr(error, "error_message", error))
        for error in getattr(result, "errors", [])
    )
    settings = {
        "parser": "docling-standard-pdf-pipeline",
        "ocr_enabled": True,
        "ocr_engine": ocr_engine,
        "ocr_languages": ["en"] if ocr_engine == "easyocr" else [],
        "ocr_accelerator": "cpu",
        "force_full_page_ocr": force_full_page_ocr,
        "table_structure_enabled": True,
        "table_structure_mode": "accurate",
        "layout_analysis": "docling-layout-model",
        "multi_column_reading_order": "docling-layout-model",
        "page_markers": "numbered",
        "parsed_pages_retained_during_conversion": True,
    }
    return ConversionCandidate(
        markdown="".join(rendered).rstrip() + "\n",
        expected_pages=expected_pages,
        conversion_status=status,
        conversion_errors=errors,
        missing_document_pages=missing_pages,
        force_full_page_ocr=force_full_page_ocr,
        settings=settings,
        table_count=len(result.document.tables),
    )


def candidate_quality(
    candidate: ConversionCandidate,
    thresholds: QualityThresholds | None = None,
) -> dict[str, Any]:
    return analyze_markdown(
        candidate.markdown,
        candidate.expected_pages,
        conversion_status=candidate.conversion_status,
        conversion_errors=candidate.conversion_errors,
        missing_document_pages=candidate.missing_document_pages,
        thresholds=thresholds,
    )


def select_conversion(
    pdf_path: Path,
    *,
    converter: Callable[..., ConversionCandidate] = convert_with_docling,
    ocr_engine: str = "easyocr",
    thresholds: QualityThresholds | None = None,
) -> tuple[ConversionCandidate, dict[str, Any], list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    normal: ConversionCandidate | None = None
    normal_quality: dict[str, Any] | None = None
    normal_error: Exception | None = None
    try:
        normal = converter(pdf_path, force_full_page_ocr=False, ocr_engine=ocr_engine)
        normal_quality = candidate_quality(normal, thresholds)
        attempts.append(
            {
                "name": "layout_aware_selective_ocr",
                "selected": False,
                "settings": normal.settings,
                "quality": normal_quality,
            }
        )
    except Exception as error:
        normal_error = error
        attempts.append(
            {
                "name": "layout_aware_selective_ocr",
                "selected": False,
                "conversion_error": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            }
        )

    if (
        normal is not None
        and normal_quality is not None
        and normal_quality["status"] == "pass"
    ):
        selected = normal
        selected_quality = normal_quality
    else:
        try:
            forced = converter(
                pdf_path, force_full_page_ocr=True, ocr_engine=ocr_engine
            )
        except Exception as forced_error:
            if normal_error is not None:
                raise FullTextError(
                    "Both selective and forced full-page OCR conversion failed: "
                    f"{normal_error}; {forced_error}"
                ) from forced_error
            raise
        forced_quality = candidate_quality(forced, thresholds)
        attempts.append(
            {
                "name": "layout_aware_forced_full_page_ocr",
                "selected": False,
                "settings": forced.settings,
                "quality": forced_quality,
            }
        )
        if (
            normal is None
            or normal_quality is None
            or tuple(forced_quality["quality_rank"])
            < tuple(normal_quality["quality_rank"])
        ):
            selected = forced
            selected_quality = forced_quality
        else:
            selected = normal
            selected_quality = normal_quality
    selected_name = (
        "layout_aware_forced_full_page_ocr"
        if selected.force_full_page_ocr
        else "layout_aware_selective_ocr"
    )
    for attempt in attempts:
        attempt["selected"] = attempt["name"] == selected_name
    return selected, selected_quality, attempts


def prepare_document(
    manifest_path: Path,
    corpus_id: str,
    output_dir: Path,
    *,
    converter: Callable[..., ConversionCandidate] = convert_with_docling,
    ocr_engine: str = "easyocr",
    require_verified: bool = True,
    thresholds: QualityThresholds | None = None,
) -> PreparedDocument:
    base_dir, records, manifest = load_corpus_manifest(
        manifest_path, require_verified=require_verified
    )
    if corpus_id not in records:
        raise FullTextError(f"Corpus ID {corpus_id!r} is absent from {manifest_path}")
    record = records[corpus_id]
    pdf_path = resolve_pdf(base_dir, record)
    selected, quality, attempts = select_conversion(
        pdf_path,
        converter=converter,
        ocr_engine=ocr_engine,
        thresholds=thresholds,
    )
    text = verified_metadata_header(record) + selected.markdown
    source_map = build_source_map(text, record.corpus_id)
    validate_source_map(text, source_map)

    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / "document.md"
    input_json_path = output_dir / "document.json"
    source_map_path = output_dir / "source-map.json"
    quality_path = output_dir / "quality.json"
    processing_path = output_dir / "processing.json"
    bibliography_path = output_dir / "bibliographic-identity.json"

    bibliography = {
        "schema_version": "verified-bibliographic-identity/1.0",
        **asdict(record),
        "manifest_path": str(manifest_path),
        "manifest_partition_frozen": manifest.get("partition_frozen") is True,
    }
    input_payload = {
        "text": text,
        "url": record.source_url,
        "bibliographic_identity": bibliography,
        "source_map": source_map_path.name,
    }
    selected_name = (
        "layout_aware_forced_full_page_ocr"
        if selected.force_full_page_ocr
        else "layout_aware_selective_ocr"
    )
    processing = {
        "schema_version": SCHEMA_VERSION,
        "prepared_at": utc_now(),
        "corpus_id": record.corpus_id,
        "source_pdf": {
            "path": record.pdf_path,
            "sha256": record.pdf_sha256,
            "bytes": pdf_path.stat().st_size,
        },
        "complete_document": True,
        "head_chunks": None,
        "selected_attempt": selected_name,
        "selected_settings": selected.settings,
        "attempts": attempts,
        "software_versions": software_versions(),
        "outputs": {},
        "table_count_reported_by_parser": selected.table_count,
        "table_count_in_source_map": len(source_map["table_blocks"]),
    }

    markdown_path.write_text(text, encoding="utf-8", newline="\n")
    write_json(input_json_path, input_payload)
    write_json(source_map_path, source_map)
    write_json(quality_path, quality)
    write_json(bibliography_path, bibliography)
    output_paths = {
        "document_markdown": markdown_path,
        "ontocast_input": input_json_path,
        "source_map": source_map_path,
        "quality": quality_path,
        "bibliographic_identity": bibliography_path,
    }
    processing["outputs"] = {
        name: {
            "path": path.name,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for name, path in output_paths.items()
    }
    write_json(processing_path, processing)
    return PreparedDocument(
        output_dir=output_dir,
        input_json=input_json_path,
        markdown=markdown_path,
        source_map=source_map_path,
        quality=quality_path,
        processing=processing_path,
        bibliography=bibliography_path,
        quality_status=quality["status"],
        selected_attempt=selected_name,
    )


def front_matter_page_count(markdown: str) -> int | None:
    match = FRONT_MATTER_PAGE_COUNT_RE.search(markdown)
    return int(match.group(1)) if match else None


def audit_markdown_files(paths: Iterable[Path]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for path in sorted({Path(value) for value in paths}, key=lambda value: str(value)):
        try:
            text = path.read_text(encoding="utf-8")
            expected = front_matter_page_count(text)
            if expected is None:
                observed, _, _ = split_pages(text)
                expected = max(observed, default=0)
            quality = analyze_markdown(text, expected)
            source_map = build_source_map(text, path.parent.name)
            validate_source_map(text, source_map)
            records.append(
                {
                    "path": str(path),
                    "status": quality["status"],
                    "quality": quality,
                    "source_map_summary": {
                        "pages": source_map["page_count"],
                        "blocks": source_map["block_count"],
                        "tables": len(source_map["table_blocks"]),
                    },
                }
            )
        except Exception as error:
            records.append(
                {
                    "path": str(path),
                    "status": "error",
                    "error": {"type": type(error).__name__, "message": str(error)},
                }
            )
    return {
        "schema_version": "fulltext-audit/1.0",
        "created_at": utc_now(),
        "summary": {
            "documents": len(records),
            "passed": sum(record["status"] == "pass" for record in records),
            "failed": sum(record["status"] == "fail" for record in records),
            "errors": sum(record["status"] == "error" for record in records),
        },
        "documents": records,
    }


def _expand_inputs(patterns: Iterable[str]) -> list[Path]:
    import glob

    result: list[Path] = []
    for pattern in patterns:
        path = Path(pattern)
        if path.is_file():
            result.append(path)
            continue
        matches = sorted(Path(value) for value in glob.glob(pattern, recursive=True))
        if not matches:
            raise FullTextError(f"No Markdown files matched: {pattern}")
        result.extend(match for match in matches if match.is_file())
    return list(dict.fromkeys(result))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser(
        "prepare", help="Convert and quality-check one verified PDF"
    )
    prepare.add_argument("--manifest", type=Path, required=True)
    prepare.add_argument("--corpus-id", required=True)
    prepare.add_argument("--output-dir", type=Path, required=True)
    prepare.add_argument(
        "--ocr-engine", choices=("easyocr", "rapidocr", "auto"), default="easyocr"
    )
    prepare.add_argument(
        "--allow-provisional",
        action="store_true",
        help="Development only: allow an unfrozen partition or provisional record",
    )
    prepare.add_argument(
        "--allow-quality-failure",
        action="store_true",
        help="Write failed conversion diagnostics and return success (development only)",
    )

    audit = subparsers.add_parser(
        "audit", help="Audit existing page-delimited Markdown"
    )
    audit.add_argument(
        "--input", nargs="+", required=True, help="Markdown paths or glob patterns"
    )
    audit.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "prepare":
            prepared = prepare_document(
                args.manifest,
                args.corpus_id,
                args.output_dir,
                ocr_engine=args.ocr_engine,
                require_verified=not args.allow_provisional,
            )
            print(f"Prepared {args.corpus_id}: {prepared.output_dir}")
            print(
                f"Quality: {prepared.quality_status}; selected: {prepared.selected_attempt}"
            )
            if prepared.quality_status != "pass" and not args.allow_quality_failure:
                return 2
            return 0
        paths = _expand_inputs(args.input)
        report = audit_markdown_files(paths)
        write_json(args.output, report)
        summary = report["summary"]
        print(
            f"Audited {summary['documents']} document(s): "
            f"{summary['passed']} passed, {summary['failed']} failed, {summary['errors']} errors"
        )
        return 1 if summary["failed"] or summary["errors"] else 0
    except FullTextError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
