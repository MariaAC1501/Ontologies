#!/usr/bin/env python3
"""Build JSONL evidence packages for no-OntoCast LLM baselines.

The CLI joins a gold ``sample_manifest.csv`` with the screened Scopus export by
``corpus_id`` and writes one JSON object per sampled paper.  The output is meant
as the stable input for abstract-only, metadata-augmented, and local full-text
LLM extraction arms. Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_SCOPUS_CSV = Path("extraction_papers/scopus_export_May 26-2026_included.csv")
DEFAULT_OUTPUT = Path("paper/experiments/evidence.jsonl")
RECORD_ID_COLUMNS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")
PDF_COLUMNS = ("pdf_file", "pdf_sha256", "duplicate_sha256_count")
FACTS_COLUMNS = ("facts_file", "facts_sha256", "final_extraction_run", "actual_model")
SAMPLE_METADATA_COLUMNS = (
    "source_title",
    "query_index",
    "extracted_title",
    "extracted_task",
    "extracted_case_count",
    "matched_graph_literal",
    "linkage_method",
    "title_match_score",
    "linkage_confidence",
    "chunks",
    "retry_run_count",
    "sanitization",
    "run_notes",
)
SCOPUS_BIBLIOGRAPHIC_COLUMNS = (
    "Authors",
    "Title",
    "Year",
    "Source title",
    "Volume",
    "Issue",
    "Art. No.",
    "Page start",
    "Page end",
    "DOI",
    "Link",
    "Document Type",
    "Publication Stage",
    "Open Access",
    "EID",
)
SCOPUS_SCREENING_COLUMNS = (
    "screening_decision",
    "screening_reason_category",
    "screening_confidence",
    "screening_notes",
)
KEYWORD_COLUMNS = ("Author Keywords", "Index Keywords")
TEXT_EXTENSIONS = ("txt", "md", "json")
JSON_TEXT_PRIORITY_KEYS = (
    "title",
    "abstract",
    "text",
    "content",
    "markdown",
    "body",
    "full_text",
    "fulltext",
    "main_text",
    "sections",
    "section",
    "pages",
    "page",
    "paragraphs",
    "paragraph",
    "chunks",
    "chunk",
    "lines",
    "line",
)
SECTION_KEYWORDS = (
    "method",
    "methodology",
    "materials",
    "experiment",
    "result",
    "discussion",
    "model",
    "data",
)


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def read_csv(path: Path, label: str) -> Tuple[List[str], List[Tuple[int, Dict[str, str]]]]:
    if not path.exists():
        raise UserError(f"{label} not found: {path}")
    if not path.is_file():
        raise UserError(f"{label} is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise UserError(f"{label} has no header row: {path}")
            fieldnames = [name for name in reader.fieldnames if name is not None]
            rows: List[Tuple[int, Dict[str, str]]] = []
            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise UserError(
                        f"{label} row {row_number} has more values than header columns"
                    )
                rows.append(
                    (row_number, {field: (row.get(field) or "").strip() for field in fieldnames})
                )
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode {label} as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read {label} {path}: {exc}") from exc

    if not rows:
        raise UserError(f"{label} contains no data rows: {path}")
    return fieldnames, rows


def require_column(fieldnames: Sequence[str], column: str, label: str) -> None:
    if column not in fieldnames:
        raise UserError(f"{label} must contain a {column!r} column")


def index_scopus_by_corpus_id(rows: Sequence[Tuple[int, Dict[str, str]]]) -> Dict[str, Tuple[int, Dict[str, str]]]:
    index: Dict[str, Tuple[int, Dict[str, str]]] = {}
    for row_number, row in rows:
        corpus_id = row.get("corpus_id", "").strip()
        if not corpus_id:
            raise UserError(f"Scopus CSV row {row_number} has an empty corpus_id")
        if corpus_id in index:
            first_row_number, _ = index[corpus_id]
            raise UserError(
                f"duplicate corpus_id {corpus_id!r} in Scopus CSV rows "
                f"{first_row_number} and {row_number}"
            )
        index[corpus_id] = (row_number, row)
    return index


def choose_record_id(sample_row: Dict[str, str], row_number: int) -> str:
    for column in RECORD_ID_COLUMNS:
        value = sample_row.get(column, "").strip()
        if value:
            return value
    return f"sample-row-{row_number}"


def first_nonempty(row: Dict[str, str], columns: Sequence[str]) -> str:
    for column in columns:
        value = row.get(column, "").strip()
        if value:
            return value
    return ""


def compact_dict(row: Dict[str, str], columns: Sequence[str]) -> Dict[str, str]:
    return {column: row.get(column, "") for column in columns if row.get(column, "")}


def candidate_paths(value: str, reference_path: Path) -> Iterable[Path]:
    """Yield plausible filesystem paths for a CSV-relative value."""
    normalized = value.strip().replace("\\", os.sep)
    if not normalized:
        return

    candidate = Path(normalized).expanduser()
    if candidate.is_absolute():
        yield candidate
        return

    bases: List[Path] = [Path.cwd(), reference_path.parent]
    bases.extend(reference_path.parent.parents)

    seen = set()
    for base in bases:
        full = (base / candidate).resolve()
        if full not in seen:
            seen.add(full)
            yield full


def resolve_existing_path(value: str, reference_path: Path) -> Tuple[bool, str]:
    for path in candidate_paths(value, reference_path):
        if path.exists() and path.is_file():
            return True, str(path)
    return False, ""


def path_metadata(row: Dict[str, str], path_column: str, sha_column: str, reference_path: Path) -> Dict[str, Any]:
    value = row.get(path_column, "")
    exists = False
    resolved = ""
    if value:
        exists, resolved = resolve_existing_path(value, reference_path)
    return {
        "file": value,
        "sha256": row.get(sha_column, ""),
        "exists": exists if value else None,
        "resolved_path": resolved,
    }


def add_text_warning(text_info: Dict[str, Any], message: str) -> None:
    warnings = text_info.setdefault("warnings", [])
    if message not in warnings:
        warnings.append(message)


def normalized_path_stem(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return ""
    return Path(normalized).stem


def text_candidate_names(sample_row: Dict[str, str]) -> Iterable[str]:
    stems: List[str] = []
    corpus_id = sample_row.get("corpus_id", "").strip()
    if corpus_id:
        stems.append(corpus_id)

    pdf_stem = normalized_path_stem(sample_row.get("pdf_file", ""))
    if pdf_stem:
        stems.append(pdf_stem)

    seen = set()
    for stem in stems:
        for extension in TEXT_EXTENSIONS:
            name = f"{stem}.{extension}"
            if name not in seen:
                seen.add(name)
                yield name


def normalized_json_key(key: Any) -> str:
    return str(key).strip().lower().replace("-", "_").replace(" ", "_")


def json_text_parts(value: Any) -> List[str]:
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            parts.extend(json_text_parts(item))
        return parts
    if isinstance(value, dict):
        parts = []
        used_keys = set()
        normalized_keys: Dict[str, List[Any]] = {}
        for key in value:
            normalized_keys.setdefault(normalized_json_key(key), []).append(key)
        for preferred_key in JSON_TEXT_PRIORITY_KEYS:
            for key in normalized_keys.get(preferred_key, []):
                used_keys.add(key)
                parts.extend(json_text_parts(value[key]))
        for key, child in value.items():
            if key not in used_keys:
                parts.extend(json_text_parts(child))
        return parts
    return []


def extract_json_text(value: Any) -> str:
    return "\n\n".join(json_text_parts(value)).strip()


def read_text_file(path: Path, warnings: List[str]) -> str:
    try:
        raw = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            raw = path.read_bytes().decode("utf-8", errors="replace")
        except OSError as exc:
            warnings.append(f"could not read text file {path}: {exc}")
            return ""
        warnings.append(f"could not decode text file {path} cleanly; replacement characters inserted")
    except OSError as exc:
        warnings.append(f"could not read text file {path}: {exc}")
        return ""

    if path.suffix.lower() != ".json":
        return raw.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        warnings.append(f"could not parse JSON text file {path}: {exc}; using raw contents")
        return raw.strip()

    text = extract_json_text(parsed)
    if not text:
        warnings.append(f"JSON text file {path} did not contain extractable text")
    return text


def build_text_info(
    sample_row: Dict[str, str],
    text_dir: Optional[Path],
    scope: str,
) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "exists": False,
        "resolved_path": "",
        "chars_used": 0,
        "warnings": [],
        "text": "",
    }
    read_required = scope in {"sections", "fulltext"}

    if text_dir is None:
        if read_required:
            add_text_warning(info, "--text-dir not provided; full text unavailable")
        return info

    text_root = text_dir.expanduser()
    if not text_root.is_absolute():
        text_root = (Path.cwd() / text_root).resolve()
    else:
        text_root = text_root.resolve()

    if not text_root.exists():
        add_text_warning(info, f"text-dir not found: {text_root}")
        return info
    if not text_root.is_dir():
        add_text_warning(info, f"text-dir is not a directory: {text_root}")
        return info

    for name in text_candidate_names(sample_row):
        candidate = text_root / name
        if candidate.exists() and candidate.is_file():
            info["exists"] = True
            info["resolved_path"] = str(candidate)
            if read_required:
                info["text"] = read_text_file(candidate, info["warnings"])
                if not info["text"]:
                    add_text_warning(info, f"text file {candidate} was empty after extraction")
            return info

    if read_required:
        corpus_id = sample_row.get("corpus_id", "").strip() or "<missing corpus_id>"
        pdf_stem = normalized_path_stem(sample_row.get("pdf_file", ""))
        details = f"corpus_id={corpus_id}"
        if pdf_stem:
            details += f", pdf_stem={pdf_stem}"
        add_text_warning(info, f"no text file found in {text_root} for {details}")
    return info


def contains_section_keyword(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in SECTION_KEYWORDS)


def looks_like_heading(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return True
    if len(stripped) > 120:
        return False
    if stripped.endswith(":"):
        return True
    first_token = stripped.split(maxsplit=1)[0].rstrip(".")
    if first_token and all(part.isdigit() for part in first_token.split(".") if part):
        return True
    return contains_section_keyword(stripped) and len(stripped.split()) <= 8


def paragraph_blocks(text: str) -> List[str]:
    blocks: List[str] = []
    current: List[str] = []
    for line in text.splitlines():
        if line.strip():
            current.append(line)
        elif current:
            blocks.append("\n".join(current).strip())
            current = []
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block]


def text_blocks(text: str) -> List[str]:
    blocks: List[str] = []
    current: List[str] = []
    saw_heading = False
    for line in text.splitlines():
        if looks_like_heading(line):
            saw_heading = True
            if current:
                block = "\n".join(current).strip()
                if block:
                    blocks.append(block)
            current = [line]
        else:
            if current or line.strip():
                current.append(line)
    if current:
        block = "\n".join(current).strip()
        if block:
            blocks.append(block)

    if saw_heading:
        return blocks

    paragraphs = paragraph_blocks(text)
    if len(paragraphs) <= 1:
        return [line.strip() for line in text.splitlines() if line.strip()]
    return paragraphs


def selected_sections_excerpt(text: str, max_chars: int) -> str:
    selected = [block for block in text_blocks(text) if contains_section_keyword(block)]
    return "\n\n".join(selected).strip()[:max_chars]


def append_section(lines: List[str], label: str, value: str) -> None:
    lines.append(f"{label}: {value}")


def build_evidence_text(
    scope: str,
    sample_row: Dict[str, str],
    scopus_row: Dict[str, str],
    text_info: Dict[str, Any],
    max_fulltext_chars: int,
) -> str:
    title = first_nonempty(scopus_row, ("Title",)) or first_nonempty(
        sample_row, ("source_title", "extracted_title")
    )
    abstract = first_nonempty(scopus_row, ("Abstract",))
    author_keywords = first_nonempty(scopus_row, ("Author Keywords",))
    index_keywords = first_nonempty(scopus_row, ("Index Keywords",))

    lines: List[str] = []
    append_section(lines, "Title", title)
    append_section(lines, "Abstract", abstract)
    append_section(lines, "Author Keywords", author_keywords)
    append_section(lines, "Index Keywords", index_keywords)

    if scope == "metadata":
        lines.extend(["", "Bibliographic metadata:"])
        for column in SCOPUS_BIBLIOGRAPHIC_COLUMNS:
            if column in {"Title"}:
                continue
            append_section(lines, column, scopus_row.get(column, ""))

        lines.extend(["", "Screening metadata:"])
        for column in SCOPUS_SCREENING_COLUMNS:
            append_section(lines, column, scopus_row.get(column, ""))

        lines.extend(["", "PDF/facts metadata:"])
        for column in PDF_COLUMNS + FACTS_COLUMNS + SAMPLE_METADATA_COLUMNS:
            if column in sample_row:
                append_section(lines, column, sample_row.get(column, ""))

    elif scope == "fulltext":
        full_text = str(text_info.get("text", ""))
        excerpt = full_text[:max_fulltext_chars]
        text_info["chars_used"] = len(excerpt)
        if not full_text:
            add_text_warning(text_info, "fulltext scope has no full text; excerpt is empty")
        lines.extend(["", "Full text excerpt:", excerpt])

    elif scope == "sections":
        full_text = str(text_info.get("text", ""))
        if not full_text:
            text_info["chars_used"] = 0
            add_text_warning(text_info, "sections scope used abstract-only evidence because no full text was available")
        else:
            excerpt = selected_sections_excerpt(full_text, max_fulltext_chars)
            text_info["chars_used"] = len(excerpt)
            if excerpt:
                lines.extend(["", "Selected full-text sections:", excerpt])
            else:
                add_text_warning(text_info, "no full-text lines or blocks matched section keywords")

    return "\n".join(lines).strip() + "\n"


def build_metadata(
    record_id: str,
    sample_manifest: Path,
    scopus_csv: Path,
    sample_row_number: int,
    scopus_row_number: int,
    sample_row: Dict[str, str],
    scopus_row: Dict[str, str],
    text_info: Dict[str, Any],
) -> Dict[str, Any]:
    corpus_id = sample_row.get("corpus_id", "")
    pdf = path_metadata(sample_row, "pdf_file", "pdf_sha256", sample_manifest)
    facts = path_metadata(sample_row, "facts_file", "facts_sha256", sample_manifest)
    text_metadata = {
        "exists": bool(text_info.get("exists", False)),
        "resolved_path": str(text_info.get("resolved_path", "")),
        "chars_used": int(text_info.get("chars_used", 0) or 0),
        "warnings": list(text_info.get("warnings", [])),
    }
    return {
        "record_id": record_id,
        "corpus_id": corpus_id,
        "sample_manifest": str(sample_manifest),
        "sample_manifest_row_number": sample_row_number,
        "scopus_csv": str(scopus_csv),
        "scopus_row_number": scopus_row_number,
        "pdf": pdf,
        "facts": facts,
        "text": text_metadata,
        "bibliographic": compact_dict(scopus_row, SCOPUS_BIBLIOGRAPHIC_COLUMNS),
        "keywords": compact_dict(scopus_row, KEYWORD_COLUMNS),
        "screening": compact_dict(scopus_row, SCOPUS_SCREENING_COLUMNS),
        "sample_manifest_fields": compact_dict(
            sample_row, PDF_COLUMNS + FACTS_COLUMNS + SAMPLE_METADATA_COLUMNS
        ),
    }


def build_records(
    sample_manifest: Path,
    sample_rows: Sequence[Tuple[int, Dict[str, str]]],
    scopus_csv: Path,
    scopus_index: Dict[str, Tuple[int, Dict[str, str]]],
    scope: str,
    text_dir: Optional[Path],
    max_fulltext_chars: int,
) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    missing: List[str] = []
    for sample_row_number, sample_row in sample_rows:
        corpus_id = sample_row.get("corpus_id", "").strip()
        if not corpus_id:
            raise UserError(f"sample manifest row {sample_row_number} has an empty corpus_id")
        match = scopus_index.get(corpus_id)
        if match is None:
            missing.append(corpus_id)
            continue
        scopus_row_number, scopus_row = match
        record_id = choose_record_id(sample_row, sample_row_number)
        text_info = build_text_info(sample_row, text_dir, scope)
        evidence_text = build_evidence_text(
            scope=scope,
            sample_row=sample_row,
            scopus_row=scopus_row,
            text_info=text_info,
            max_fulltext_chars=max_fulltext_chars,
        )
        records.append(
            {
                "record_id": record_id,
                "scope": scope,
                "evidence_text": evidence_text,
                "metadata": build_metadata(
                    record_id=record_id,
                    sample_manifest=sample_manifest,
                    scopus_csv=scopus_csv,
                    sample_row_number=sample_row_number,
                    scopus_row_number=scopus_row_number,
                    sample_row=sample_row,
                    scopus_row=scopus_row,
                    text_info=text_info,
                ),
            }
        )

    if missing:
        preview = ", ".join(missing[:10])
        suffix = " ..." if len(missing) > 10 else ""
        raise UserError(
            f"{len(missing)} sample corpus_id values were not found in Scopus CSV: "
            f"{preview}{suffix}"
        )
    return records


def write_jsonl(path: Path, records: Sequence[Dict[str, Any]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise UserError(f"could not write evidence JSONL {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample-manifest",
        type=Path,
        required=True,
        help="Input gold sample_manifest.csv containing corpus_id and PDF/facts metadata.",
    )
    parser.add_argument(
        "--scopus-csv",
        type=Path,
        default=DEFAULT_SCOPUS_CSV,
        help=f"Screened Scopus export to join by corpus_id (default: {DEFAULT_SCOPUS_CSV}).",
    )
    parser.add_argument(
        "--scope",
        choices=("abstract", "metadata", "sections", "fulltext"),
        default="abstract",
        help="Evidence scope label and text layout (default: abstract).",
    )
    parser.add_argument(
        "--text-dir",
        type=Path,
        default=None,
        help=(
            "Optional directory of preconverted .txt/.md/.json full texts named "
            "corpus_id.* or PDF-stem.*."
        ),
    )
    parser.add_argument(
        "--max-fulltext-chars",
        type=int,
        default=30000,
        help="Maximum full-text characters included for fulltext/sections scopes (default: 30000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output evidence JSONL path (default: {DEFAULT_OUTPUT}).",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    if args.max_fulltext_chars < 1:
        raise UserError("--max-fulltext-chars must be at least 1")

    sample_fieldnames, sample_rows = read_csv(args.sample_manifest, "sample manifest")
    scopus_fieldnames, scopus_rows = read_csv(args.scopus_csv, "Scopus CSV")
    require_column(sample_fieldnames, "corpus_id", "sample manifest")
    require_column(scopus_fieldnames, "corpus_id", "Scopus CSV")

    scopus_index = index_scopus_by_corpus_id(scopus_rows)
    records = build_records(
        sample_manifest=args.sample_manifest,
        sample_rows=sample_rows,
        scopus_csv=args.scopus_csv,
        scopus_index=scopus_index,
        scope=args.scope,
        text_dir=args.text_dir,
        max_fulltext_chars=args.max_fulltext_chars,
    )
    write_jsonl(args.output, records)

    text_resolved = sum(1 for record in records if record["metadata"]["text"]["exists"])
    text_chars_used = sum(record["metadata"]["text"]["chars_used"] for record in records)
    text_warning_count = sum(len(record["metadata"]["text"]["warnings"]) for record in records)

    print("Evidence packages prepared")
    print(f"  sample records: {len(sample_rows)}")
    print(f"  joined records: {len(records)}")
    print(f"  scope: {args.scope}")
    print(f"  text files resolved: {text_resolved}")
    print(f"  text chars used: {text_chars_used}")
    print(f"  text warnings: {text_warning_count}")
    print(f"  wrote: {args.output}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args)
    except UserError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
