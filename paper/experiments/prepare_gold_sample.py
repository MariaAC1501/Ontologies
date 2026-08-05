#!/usr/bin/env python3
"""Prepare a reproducible expert-annotation gold sample.

Reads an extraction manifest CSV, optionally filters to rows whose PDFs exist,
performs seeded stratified sampling, and writes:
  * sample_manifest.csv: sampled manifest rows
  * gold_template.jsonl: one JSON object per sampled row with an empty `gold` dict

Only the Python standard library is used.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DEFAULT_MANIFEST = Path("paper/supplement/protocol/extraction_manifest.csv")
DEFAULT_OUTPUT_DIR = Path("paper/experiments/gold_sample")
INTERNAL_ROW_NUMBER = "__manifest_row_number"

# Logical strata requested for RQ1/RQ3 and common manifest aliases.
STRATA_ALIASES: Dict[str, Tuple[str, ...]] = {
    "task": ("task", "extracted_task", "prediction_task", "maintenance_task"),
    "model": ("model", "actual_model", "final_model", "llm_model"),
    "linkage": ("linkage", "linkage_method", "linkage_confidence"),
}
DEFAULT_STRATA_ORDER = ("task", "model", "linkage")
RECORD_ID_COLUMNS = ("record_id", "corpus_id", "paper_id", "doc_id", "id")


class UserError(Exception):
    """Raised for user-facing CLI errors."""


def parse_column_list(raw: Optional[Sequence[str]]) -> Optional[List[str]]:
    """Parse comma/whitespace-separated columns from one or more CLI tokens.

    Returns None when the argument was omitted. Returns [] for explicit values
    such as "none", "off", or an empty string, allowing users to disable
    stratification.
    """
    if raw is None:
        return None
    text = " ".join(raw).strip()
    if not text or text.casefold() in {"none", "off", "false", "no"}:
        return []
    columns: List[str] = []
    for comma_part in text.split(","):
        for part in comma_part.split():
            col = part.strip()
            if col and col not in columns:
                columns.append(col)
    return columns


def read_manifest(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        raise UserError(f"manifest not found: {path}")
    if not path.is_file():
        raise UserError(f"manifest is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise UserError(f"manifest has no header row: {path}")
            fieldnames = [name for name in reader.fieldnames if name is not None]
            rows: List[Dict[str, str]] = []
            for row_number, row in enumerate(reader, start=2):
                if None in row:
                    raise UserError(
                        f"manifest row {row_number} has more values than header columns"
                    )
                clean = {field: (row.get(field) or "") for field in fieldnames}
                clean[INTERNAL_ROW_NUMBER] = str(row_number)
                rows.append(clean)
    except UnicodeDecodeError as exc:
        raise UserError(f"could not decode manifest as UTF-8: {path}: {exc}") from exc
    except OSError as exc:
        raise UserError(f"could not read manifest {path}: {exc}") from exc

    if not rows:
        raise UserError(f"manifest contains no data rows: {path}")
    return fieldnames, rows


def resolve_strata_columns(
    fieldnames: Sequence[str], requested: Optional[List[str]]
) -> List[str]:
    """Resolve explicit/default strata columns against manifest columns."""
    available = set(fieldnames)

    def resolve_one(name: str) -> str:
        if name in available:
            return name
        logical = name.casefold()
        if logical in STRATA_ALIASES:
            for alias in STRATA_ALIASES[logical]:
                if alias in available:
                    return alias
        raise UserError(
            f"strata column {name!r} not found in manifest. "
            f"Available columns include: {', '.join(fieldnames[:20])}"
            + (" ..." if len(fieldnames) > 20 else "")
        )

    if requested is not None:
        resolved: List[str] = []
        for name in requested:
            column = resolve_one(name)
            if column not in resolved:
                resolved.append(column)
        return resolved

    resolved = []
    for logical in DEFAULT_STRATA_ORDER:
        for alias in STRATA_ALIASES[logical]:
            if alias in available:
                resolved.append(alias)
                break
    return resolved


def candidate_paths(value: str, manifest_path: Path) -> Iterable[Path]:
    """Yield plausible filesystem paths for a manifest-relative value."""
    normalized = value.strip().replace("\\", os.sep)
    if not normalized:
        return

    candidate = Path(normalized).expanduser()
    if candidate.is_absolute():
        yield candidate
        return

    bases: List[Path] = [Path.cwd(), manifest_path.parent]
    bases.extend(manifest_path.parent.parents)

    seen = set()
    for base in bases:
        full = (base / candidate).resolve()
        if full not in seen:
            seen.add(full)
            yield full


def existing_path(value: str, manifest_path: Path) -> Optional[Path]:
    for path in candidate_paths(value, manifest_path):
        if path.exists():
            return path
    return None


def filter_rows_with_existing_pdfs(
    rows: Sequence[Dict[str, str]], fieldnames: Sequence[str], manifest_path: Path
) -> Tuple[List[Dict[str, str]], int]:
    if "pdf_file" not in fieldnames:
        raise UserError("--require-pdf-exists was set, but manifest has no pdf_file column")

    kept: List[Dict[str, str]] = []
    skipped = 0
    for row in rows:
        pdf_file = row.get("pdf_file", "")
        if pdf_file and existing_path(pdf_file, manifest_path):
            kept.append(row)
        else:
            skipped += 1
    if not kept:
        raise UserError("no rows remain after requiring existing PDFs")
    return kept, skipped


def make_stratum_key(row: Dict[str, str], strata_cols: Sequence[str]) -> Tuple[str, ...]:
    return tuple((row.get(col, "").strip() or "<EMPTY>") for col in strata_cols)


def allocate_remaining(
    quotas: Dict[Tuple[str, ...], int],
    capacities: Dict[Tuple[str, ...], int],
    remaining: int,
    rng: random.Random,
) -> None:
    """Distribute remaining quota proportionally by capacity, in-place."""
    if remaining <= 0:
        return
    total_capacity = sum(max(0, capacity) for capacity in capacities.values())
    if total_capacity <= 0:
        return

    remainders: List[Tuple[float, float, Tuple[str, ...]]] = []
    assigned = 0
    for key, capacity in list(capacities.items()):
        capacity = max(0, capacity)
        ideal = remaining * capacity / total_capacity
        base = min(capacity, int(math.floor(ideal)))
        quotas[key] += base
        capacities[key] = capacity - base
        assigned += base
        remainders.append((ideal - base, rng.random(), key))

    left = remaining - assigned
    remainders.sort(key=lambda item: (-item[0], item[1], item[2]))
    while left > 0:
        changed = False
        for _, _, key in remainders:
            if left <= 0:
                break
            if capacities[key] > 0:
                quotas[key] += 1
                capacities[key] -= 1
                left -= 1
                changed = True
        if not changed:
            break


def stratified_sample(
    rows: Sequence[Dict[str, str]], strata_cols: Sequence[str], n: int, seed: int
) -> List[Dict[str, str]]:
    if n < 0:
        raise UserError("--n must be non-negative")
    if n > len(rows):
        raise UserError(f"--n {n} exceeds available rows {len(rows)}")
    if n == 0:
        return []

    rng = random.Random(seed)
    if not strata_cols:
        pool = list(rows)
        rng.shuffle(pool)
        return pool[:n]

    groups: Dict[Tuple[str, ...], List[Dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(make_stratum_key(row, strata_cols), []).append(row)

    keys = list(groups)
    quotas = {key: 0 for key in keys}

    if n >= len(keys):
        # Guarantee representation from every non-empty stratum when possible.
        for key in keys:
            quotas[key] = 1
        remaining = n - len(keys)
        capacities = {key: len(groups[key]) - 1 for key in keys}
        allocate_remaining(quotas, capacities, remaining, rng)
    else:
        capacities = {key: len(groups[key]) for key in keys}
        allocate_remaining(quotas, capacities, n, rng)

    selected: List[Dict[str, str]] = []
    for key in keys:
        quota = min(quotas[key], len(groups[key]))
        if quota <= 0:
            continue
        pool = list(groups[key])
        rng.shuffle(pool)
        selected.extend(pool[:quota])

    # Allocation should hit n, but trim defensively if rounding/ties overshoot.
    rng.shuffle(selected)
    return selected[:n]


def choose_record_id(row: Dict[str, str], fallback_index: int) -> str:
    for column in RECORD_ID_COLUMNS:
        value = row.get(column, "").strip()
        if value:
            return value
    row_number = row.get(INTERNAL_ROW_NUMBER, str(fallback_index + 1))
    return f"manifest-row-{row_number}"


def write_sample_manifest(
    path: Path, fieldnames: Sequence[str], rows: Sequence[Dict[str, str]]
) -> None:
    try:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    except OSError as exc:
        raise UserError(f"could not write sample manifest {path}: {exc}") from exc


def write_gold_template(
    path: Path,
    fieldnames: Sequence[str],
    rows: Sequence[Dict[str, str]],
    strata_cols: Sequence[str],
) -> None:
    try:
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            for index, row in enumerate(rows):
                manifest_row = {field: row.get(field, "") for field in fieldnames}
                record = {
                    "record_id": choose_record_id(row, index),
                    "corpus_id": row.get("corpus_id", ""),
                    "source_title": row.get("source_title", ""),
                    "pdf_file": row.get("pdf_file", ""),
                    "facts_file": row.get("facts_file", ""),
                    "strata": {col: row.get(col, "") for col in strata_cols},
                    "manifest": manifest_row,
                    "gold": {},
                    "annotator_notes": "",
                }
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except OSError as exc:
        raise UserError(f"could not write gold template {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a reproducible stratified gold-annotation sample."
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help=f"Input extraction manifest CSV (default: {DEFAULT_MANIFEST})",
    )
    parser.add_argument("--n", type=int, required=True, help="Number of rows to sample")
    parser.add_argument("--seed", type=int, default=13, help="Random seed (default: 13)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--strata-cols",
        nargs="*",
        default=None,
        help=(
            "Optional comma/space-separated strata columns. Logical names "
            "task, model, linkage resolve to manifest aliases when needed. "
            "Use 'none' to disable stratification."
        ),
    )
    parser.add_argument(
        "--require-pdf-exists",
        action="store_true",
        help="Filter to manifest rows whose pdf_file path exists.",
    )
    return parser


def run(args: argparse.Namespace) -> int:
    manifest_path = args.manifest
    fieldnames, rows = read_manifest(manifest_path)

    skipped_missing_pdf = 0
    if args.require_pdf_exists:
        rows, skipped_missing_pdf = filter_rows_with_existing_pdfs(
            rows, fieldnames, manifest_path
        )

    strata_cols = resolve_strata_columns(fieldnames, parse_column_list(args.strata_cols))
    selected = stratified_sample(rows, strata_cols, args.n, args.seed)

    try:
        args.output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise UserError(f"could not create output directory {args.output_dir}: {exc}") from exc

    sample_manifest_path = args.output_dir / "sample_manifest.csv"
    gold_template_path = args.output_dir / "gold_template.jsonl"
    write_sample_manifest(sample_manifest_path, fieldnames, selected)
    write_gold_template(gold_template_path, fieldnames, selected, strata_cols)

    print("Gold sample prepared")
    print(f"  input rows: {len(rows) + skipped_missing_pdf}")
    if args.require_pdf_exists:
        print(f"  skipped missing PDFs: {skipped_missing_pdf}")
    print(f"  sampled rows: {len(selected)}")
    print(f"  seed: {args.seed}")
    print(f"  strata columns: {', '.join(strata_cols) if strata_cols else '(none)'}")
    print(f"  wrote: {sample_manifest_path}")
    print(f"  wrote: {gold_template_path}")
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
