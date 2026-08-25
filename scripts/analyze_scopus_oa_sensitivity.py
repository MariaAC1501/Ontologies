#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "scikit-learn>=1.3",
# ]
# ///

"""Analyse OA restriction skew for reconciled final Scopus search runs.

The script accepts repeated complete API passes where pagination returned
repeated Scopus Paper IDs. A stratum is usable only when the union of its
unique Paper IDs equals its stable source-reported total. It then compares the
matched OA subset with the complement in the all-access S2 universe.

The output is a metadata-only, pre-screening sensitivity analysis. It does not
make eligibility, full-text, licence, or study-inclusion decisions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tempfile
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold


SUMMARY_SCHEMA_VERSION = "opmad-pdm-oa-sensitivity/v1"
WHITESPACE_RE = re.compile(r"\s+")
TITLE_RE = re.compile(r"[^a-z0-9]+")
TOKEN_RE = re.compile(r"[a-z][a-z0-9]+")
OA_PREFIX = "OPENACCESS(1) AND "
RANDOM_SEED = 20260825

# Generic research and search wording is removed only for profile similarity,
# not from the transparent marker calculations or classifier input.
PROFILE_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "based",
        "by",
        "data",
        "for",
        "from",
        "in",
        "is",
        "method",
        "methods",
        "model",
        "models",
        "of",
        "on",
        "or",
        "predictive",
        "maintenance",
        "proposed",
        "propose",
        "results",
        "study",
        "system",
        "systems",
        "the",
        "this",
        "to",
        "using",
        "with",
    }
)
CLASSIFIER_STOPWORDS = sorted(PROFILE_STOPWORDS | {"paper", "approach", "framework"})

MARKERS: list[tuple[str, str, re.Pattern[str]]] = [
    (
        "rul",
        "RUL / remaining-useful-life terms",
        re.compile(r"\b(?:rul|remaining useful life|remaining useful lifetime)\b", re.I),
    ),
    (
        "life_prognostic",
        "Life-prediction or prognostic terms",
        re.compile(
            r"\b(?:prognos\w*|life prediction|lifetime prediction|remaining service life|residual useful life)\b",
            re.I,
        ),
    ),
    ("fault_diagnosis", "Fault-diagnosis terms", re.compile(r"\bfault\s+diagnos\w*\b", re.I)),
    ("fault_detection", "Fault-detection terms", re.compile(r"\bfault\s+detect\w*\b", re.I)),
    ("anomaly_detection", "Anomaly-detection terms", re.compile(r"\banomal\w*\s+detect\w*\b", re.I)),
    (
        "pm_cbm",
        "Predictive-maintenance or CBM terms",
        re.compile(r"\b(?:predictive maintenance|condition[- ]based maintenance)\b", re.I),
    ),
    ("bearing", "Bearing terms", re.compile(r"\bbearings?\b", re.I)),
    ("transformer", "Transformer terms", re.compile(r"\btransformers?\b", re.I)),
    ("engine", "Engine or turbofan terms", re.compile(r"\b(?:engines?|turbofans?)\b", re.I)),
    ("battery", "Battery terms", re.compile(r"\bbatter(?:y|ies)\b", re.I)),
    ("lithium_ion", "Lithium-ion battery terms", re.compile(r"\blithium[- ]ion\b", re.I)),
    ("wind_turbine", "Wind-turbine terms", re.compile(r"\bwind turbines?\b", re.I)),
    ("motor", "Motor terms", re.compile(r"\bmotors?\b", re.I)),
    ("gearbox", "Gearbox terms", re.compile(r"\bgearboxes?\b", re.I)),
    (
        "cnn",
        "CNN or convolutional-neural-network terms",
        re.compile(r"\b(?:cnn|convolutional neural networks?)\b", re.I),
    ),
    (
        "lstm",
        "LSTM or long-short-term-memory terms",
        re.compile(r"\b(?:lstm|long short[- ]term memory)\b", re.I),
    ),
    ("deep_learning", "Deep-learning terms", re.compile(r"\bdeep learning\b", re.I)),
    (
        "physics_informed",
        "Physics-informed/guided/aware terms",
        re.compile(r"\bphysics[- ](?:informed|guided|aware)\b", re.I),
    ),
    ("transfer_learning", "Transfer-learning terms", re.compile(r"\btransfer learning\b", re.I)),
    (
        "domain_adaptation",
        "Domain-adaptation/generalisation terms",
        re.compile(r"\bdomain (?:adaptation|generalization|generalisation)\b", re.I),
    ),
    ("digital_twin", "Digital-twin terms", re.compile(r"\bdigital twins?\b", re.I)),
    ("cmapss", "C-MAPSS terms", re.compile(r"\bc[- ]?mapss\b", re.I)),
    (
        "case_western",
        "Case-Western terms",
        re.compile(r"\bcase western(?: reserve university)?\b", re.I),
    ),
    ("f1", "F1 terms", re.compile(r"\bf1(?:[- ]score)?\b", re.I)),
    ("rmse", "RMSE terms", re.compile(r"\brmse\b", re.I)),
    (
        "auc",
        "AUC terms",
        re.compile(r"\bauc\b|area under (?:the )?(?:roc|receiver operating characteristic)", re.I),
    ),
]
MARKER_BY_KEY = {key: (label, pattern) for key, label, pattern in MARKERS}


class AnalysisError(ValueError):
    """Raised when source artifacts cannot support the final comparison."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(131_072):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_whitespace(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def normalize_doi(value: Any) -> str:
    text = str(value or "").strip().casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text.rstrip(".,;)")


def normalize_title(value: Any) -> str:
    return TITLE_RE.sub(" ", str(value or "").casefold()).strip()


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AnalysisError(f"Cannot read JSON: {path}") from error
    if not isinstance(value, dict):
        raise AnalysisError(f"Expected a JSON object: {path}")
    return value


def validate_commit_marker(result_path: Path) -> dict[str, Any]:
    marker_path = result_path.with_name(f".{result_path.name}.ACADEMIC_SEARCH_COMMIT.json")
    marker = read_json(marker_path)
    if marker.get("schema") != "academic_search_output_commit_marker_v1":
        raise AnalysisError(f"Unsupported commit marker: {marker_path}")
    json_receipt = marker.get("normalized_json")
    csv_receipt = marker.get("normalized_csv")
    if not isinstance(json_receipt, dict) or not isinstance(csv_receipt, dict):
        raise AnalysisError(f"Incomplete commit marker: {marker_path}")
    if (
        json_receipt.get("sha256") != sha256_file(result_path)
        or json_receipt.get("bytes") != result_path.stat().st_size
    ):
        raise AnalysisError(f"JSON does not match commit marker: {result_path}")
    csv_name = csv_receipt.get("file_name")
    if not isinstance(csv_name, str) or Path(csv_name).name != csv_name:
        raise AnalysisError(f"Unsafe CSV name in marker: {marker_path}")
    csv_path = result_path.with_name(csv_name)
    if (
        not csv_path.is_file()
        or csv_receipt.get("sha256") != sha256_file(csv_path)
        or csv_receipt.get("bytes") != csv_path.stat().st_size
    ):
        raise AnalysisError(f"CSV does not match commit marker: {csv_path}")
    return {
        "commit_marker_file": marker_path.name,
        "commit_marker_sha256": sha256_file(marker_path),
        "commit_marker_bytes": marker_path.stat().st_size,
        "csv_file": csv_path.name,
        "csv_sha256": sha256_file(csv_path),
        "csv_bytes": csv_path.stat().st_size,
    }


def validate_complete_run(
    label: str, result_path: Path, query_path: Path
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    data = read_json(result_path)
    metadata = data.get("output_metadata")
    rows = data.get("results")
    if not isinstance(metadata, dict) or not isinstance(rows, list):
        raise AnalysisError(f"{label} lacks metadata or rows")
    if metadata.get("source") != "Scopus":
        raise AnalysisError(f"{label} is not a Scopus run")
    if metadata.get("status") != "success" or metadata.get("retrieval_complete") is not True:
        raise AnalysisError(f"{label} is not a complete successful run")
    total = data.get("total")
    retrieved = data.get("results_retrieved")
    if not isinstance(total, int) or total < 0 or total != retrieved or total != len(rows):
        raise AnalysisError(f"{label} has inconsistent total/row counts")
    query_text = query_path.read_text(encoding="utf-8")
    executed = data.get("executed_query")
    if not isinstance(executed, str) or normalize_whitespace(executed) != normalize_whitespace(query_text):
        raise AnalysisError(f"{label} query echo does not match archived query")
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict) or not str(row.get("paperId") or "").strip():
            raise AnalysisError(f"{label} row {index} lacks a Scopus Paper ID")
    receipt = {
        "label": label,
        "result_file": result_path.name,
        "result_sha256": sha256_file(result_path),
        "result_bytes": result_path.stat().st_size,
        "query_file": query_path.name,
        "query_sha256": sha256_file(query_path),
        "query_bytes": query_path.stat().st_size,
        "source_reported_total": total,
        "records_retrieved": retrieved,
        "pages_retrieved": data.get("pages_retrieved"),
        "executed_at_utc": metadata.get("extracted_at"),
        "retrieval_complete": True,
        "stopped_reason": metadata.get("stopped_reason"),
        **validate_commit_marker(result_path),
    }
    return rows, receipt


def reconcile_passes(
    label: str, query_path: Path, pass_paths: list[Path]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not pass_paths:
        raise AnalysisError(f"{label} has no retrieval passes")
    pass_rows: list[tuple[list[dict[str, Any]], dict[str, Any]]] = []
    for index, path in enumerate(pass_paths, start=1):
        pass_rows.append(validate_complete_run(f"{label}-pass-{index}", path, query_path))
    totals = {receipt["source_reported_total"] for _, receipt in pass_rows}
    if len(totals) != 1:
        raise AnalysisError(f"{label} source totals changed across passes")
    source_total = totals.pop()
    canonical: dict[str, dict[str, Any]] = {}
    reconciled: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    for rows, receipt in pass_rows:
        ids = [str(row["paperId"]).strip() for row in rows]
        pass_receipt = dict(receipt)
        pass_receipt["unique_scopus_paper_ids"] = len(set(ids))
        pass_receipt["repeated_page_rows"] = len(ids) - len(set(ids))
        receipts.append(pass_receipt)
        for row in rows:
            paper_id = str(row["paperId"]).strip()
            existing = canonical.get(paper_id)
            if existing is None:
                canonical[paper_id] = row
                reconciled.append(row)
            elif normalize_doi(existing.get("doi")) != normalize_doi(row.get("doi")):
                raise AnalysisError(f"{label} has conflicting DOI values for {paper_id}")
    if len(reconciled) != source_total:
        raise AnalysisError(
            f"{label} recovery union has {len(reconciled)} IDs, not source total {source_total}"
        )
    return reconciled, {
        "label": label,
        "source_reported_total": source_total,
        "records_retrieved": len(reconciled),
        "retrieval_complete": True,
        "stopped_reason": "reconciled_complete_passes",
        "reconciliation_mode": "unique_scopus_paper_id_union_of_complete_passes",
        "reconciliation_pass_count": len(receipts),
        "reconciliation_passes": receipts,
    }


def deduplicate_groups(
    groups: list[tuple[str, list[dict[str, Any]]]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Deduplicate EID first, then DOI; record, but do not force, title collisions."""
    by_paper_id: dict[str, dict[str, Any]] = {}
    by_doi: dict[str, dict[str, Any]] = {}
    records: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    for stratum, rows in groups:
        for raw in rows:
            row = dict(raw)
            paper_id = str(row["paperId"]).strip()
            doi = normalize_doi(row.get("doi"))
            existing = by_paper_id.get(paper_id)
            rule = "Scopus Paper ID"
            if existing is None and doi:
                existing = by_doi.get(doi)
                rule = "normalized DOI"
            if existing is None:
                record = {key: deepcopy(value) for key, value in row.items()}
                record["source_strata"] = [stratum]
                record["source_ranks"] = {stratum: [row.get("rank")]}
                record["source_paper_ids"] = {stratum: [paper_id]}
                records.append(record)
                by_paper_id[paper_id] = record
                if doi:
                    by_doi[doi] = record
                continue
            if stratum not in existing["source_strata"]:
                existing["source_strata"].append(stratum)
            ranks = existing["source_ranks"].setdefault(stratum, [])
            if row.get("rank") not in ranks:
                ranks.append(row.get("rank"))
            ids = existing["source_paper_ids"].setdefault(stratum, [])
            if paper_id not in ids:
                ids.append(paper_id)
            events.append(
                {
                    "rule": rule,
                    "canonical_paper_id": existing["paperId"],
                    "duplicate_paper_id": paper_id,
                    "duplicate_stratum": stratum,
                    "doi": doi or None,
                    "normalized_title": normalize_title(row.get("title")) or None,
                    "publication_year": row.get("year") if isinstance(row.get("year"), int) else None,
                }
            )
    return records, events


def match_oa_to_all(
    oa_records: list[dict[str, Any]], all_records: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    all_by_id = {str(record["paperId"]): record for record in all_records}
    all_by_doi = {
        normalize_doi(record.get("doi")): record
        for record in all_records
        if normalize_doi(record.get("doi"))
    }
    matched_oa: list[dict[str, Any]] = []
    unmatched_oa: list[dict[str, Any]] = []
    matched_all_ids: set[str] = set()
    for record in oa_records:
        by_id = all_by_id.get(str(record["paperId"]))
        by_doi = all_by_doi.get(normalize_doi(record.get("doi")))
        if by_id is not None and by_doi is not None and by_id["paperId"] != by_doi["paperId"]:
            raise AnalysisError(f"Conflicting all-access matches for OA Paper ID {record['paperId']}")
        matched = by_id or by_doi
        if matched is None:
            unmatched_oa.append(record)
            continue
        matched_oa.append(record)
        matched_all_ids.add(str(matched["paperId"]))
    complement = [record for record in all_records if str(record["paperId"]) not in matched_all_ids]
    return matched_oa, complement, unmatched_oa


def text_for(record: dict[str, Any]) -> str:
    return " ".join(str(record.get(key) or "") for key in ("title", "abstract"))


def percent(count: int, denominator: int) -> float:
    return 100.0 * count / denominator if denominator else 0.0


def marker_rows(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    oa_text = [text_for(record) for record in oa_records]
    non_text = [text_for(record) for record in non_oa_records]
    for key, label, pattern in MARKERS:
        oa_count = sum(bool(pattern.search(text)) for text in oa_text)
        non_count = sum(bool(pattern.search(text)) for text in non_text)
        output.append(
            {
                "key": key,
                "label": label,
                "oa_count": oa_count,
                "oa_percent": percent(oa_count, len(oa_records)),
                "non_oa_count": non_count,
                "non_oa_percent": percent(non_count, len(non_oa_records)),
                "difference_percentage_points": percent(oa_count, len(oa_records))
                - percent(non_count, len(non_oa_records)),
                "oa_availability_percent": percent(oa_count, oa_count + non_count),
            }
        )
    return output


def profile_tokens(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_RE.findall(text.casefold())
        if len(token) >= 3 and token not in PROFILE_STOPWORDS
    ]


def document_frequency_profile(records: list[dict[str, Any]]) -> Counter[str]:
    profile: Counter[str] = Counter()
    for record in records:
        tokens = profile_tokens(text_for(record))
        terms = set(tokens)
        terms.update(f"{left} {right}" for left, right in zip(tokens, tokens[1:]))
        profile.update(terms)
    return profile


def cosine_similarity(first: Counter[str], second: Counter[str]) -> float:
    keys = set(first) | set(second)
    dot = sum(first[key] * second[key] for key in keys)
    first_norm = math.sqrt(sum(value * value for value in first.values()))
    second_norm = math.sqrt(sum(value * value for value in second.values()))
    return dot / (first_norm * second_norm) if first_norm and second_norm else 0.0


def js_divergence(first: Counter[str], second: Counter[str]) -> float:
    keys = set(first) | set(second)
    first_total = sum(first.values())
    second_total = sum(second.values())
    if not first_total or not second_total:
        return 0.0
    output = 0.0
    for key in keys:
        p = first[key] / first_total
        q = second[key] / second_total
        midpoint = (p + q) / 2.0
        if p:
            output += 0.5 * p * math.log2(p / midpoint)
        if q:
            output += 0.5 * q * math.log2(q / midpoint)
    return output


def classifier_metrics(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> dict[str, Any]:
    texts = [text_for(record) for record in oa_records] + [text_for(record) for record in non_oa_records]
    labels = [1] * len(oa_records) + [0] * len(non_oa_records)
    if min(Counter(labels).values()) < 5:
        return {"available": False, "reason": "fewer_than_five_records_in_a_class"}
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=CLASSIFIER_STOPWORDS,
        ngram_range=(1, 2),
        min_df=2,
        max_features=50_000,
        sublinear_tf=True,
    )
    matrix = vectorizer.fit_transform(texts)
    predictions = [0.0] * len(labels)
    splitter = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    for train, test in splitter.split(matrix, labels):
        model = LogisticRegression(
            max_iter=2_000,
            class_weight="balanced",
            solver="liblinear",
            random_state=RANDOM_SEED,
        )
        model.fit(matrix[train], [labels[index] for index in train])
        probabilities = model.predict_proba(matrix[test])[:, 1]
        for index, probability in zip(test, probabilities):
            predictions[index] = float(probability)
    predicted_labels = [int(probability >= 0.5) for probability in predictions]
    return {
        "available": True,
        "n_oa": len(oa_records),
        "n_non_oa": len(non_oa_records),
        "features": int(matrix.shape[1]),
        "folds": 5,
        "random_seed": RANDOM_SEED,
        "auc": float(roc_auc_score(labels, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(labels, predicted_labels)),
    }


def textual_similarity(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> dict[str, Any]:
    oa_profile = document_frequency_profile(oa_records)
    non_profile = document_frequency_profile(non_oa_records)
    top_oa = [term for term, _ in sorted(oa_profile.items(), key=lambda item: (-item[1], item[0]))]
    top_non = [term for term, _ in sorted(non_profile.items(), key=lambda item: (-item[1], item[0]))]
    return {
        "profile": "unigram_and_bigram_document_frequency_after_generic_term_removal",
        "cosine_similarity": cosine_similarity(oa_profile, non_profile),
        "jensen_shannon_divergence": js_divergence(oa_profile, non_profile),
        "top_20_overlap": len(set(top_oa[:20]) & set(top_non[:20])),
        "top_100_overlap": len(set(top_oa[:100]) & set(top_non[:100])),
        "classifier": classifier_metrics(oa_records, non_oa_records),
    }


def year_rows(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for year in (2025, 2026):
        oa_count = sum(record.get("year") == year for record in oa_records)
        non_count = sum(record.get("year") == year for record in non_oa_records)
        output.append(
            {
                "label": str(year),
                "oa_count": oa_count,
                "oa_percent": percent(oa_count, len(oa_records)),
                "non_oa_count": non_count,
                "non_oa_percent": percent(non_count, len(non_oa_records)),
                "oa_availability_percent": percent(oa_count, oa_count + non_count),
            }
        )
    return output


def source_stratum_rows(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    definitions = [
        ("Maintenance/prognostic-anchor only", frozenset({"S1a"}), frozenset({"S2a"})),
        ("Diagnostic/condition-anchor only", frozenset({"S1b"}), frozenset({"S2b"})),
    ]
    output: list[dict[str, Any]] = []
    for label, oa_labels, all_labels in definitions:
        oa_count = sum(frozenset(record["source_strata"]) == oa_labels for record in oa_records)
        non_count = sum(frozenset(record["source_strata"]) == all_labels for record in non_oa_records)
        output.append(
            {
                "label": label,
                "oa_count": oa_count,
                "oa_percent": percent(oa_count, len(oa_records)),
                "non_oa_count": non_count,
                "non_oa_percent": percent(non_count, len(non_oa_records)),
                "oa_availability_percent": percent(oa_count, oa_count + non_count),
            }
        )
    return output


def doi_prefix(value: Any) -> str:
    doi = normalize_doi(value)
    match = re.match(r"^(10\.\d+)", doi)
    return match.group(1) if match else ""


def doi_prefix_rows(oa_records: list[dict[str, Any]], non_oa_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prefixes = ("10.1109", "10.3390", "10.1016", "10.1007", "10.1038")
    output: list[dict[str, Any]] = []
    for prefix in prefixes:
        oa_count = sum(doi_prefix(record.get("doi")) == prefix for record in oa_records)
        non_count = sum(doi_prefix(record.get("doi")) == prefix for record in non_oa_records)
        all_count = oa_count + non_count
        output.append(
            {
                "prefix": prefix,
                "all_count": all_count,
                "oa_count": oa_count,
                "oa_rate_percent": percent(oa_count, all_count),
                "oa_share_percent": percent(oa_count, len(oa_records)),
                "non_oa_share_percent": percent(non_count, len(non_oa_records)),
            }
        )
    return output


def fmt_count_percent(count: int, total: int) -> str:
    return f"{count:,} ({percent(count, total):.1f}%)"


def markdown_table(headers: list[str], rows: Iterable[Iterable[str]]) -> str:
    output = ["| " + " | ".join(headers) + " |", "|" + "|".join("---:" if index else "---" for index in range(len(headers))) + "|"]
    for row in rows:
        output.append("| " + " | ".join(row) + " |")
    return "\n".join(output)


def render_report(summary: dict[str, Any]) -> str:
    counts = summary["counts"]
    oa_n = counts["matched_oa_records"]
    non_n = counts["non_oa_complement_records"]
    similarity = summary["textual_similarity"]
    marker_map = {row["key"]: row for row in summary["marker_rows"]}
    source_rows = summary["source_stratum_rows"]
    lines = [
        "# Final OA-restriction sensitivity analysis — 2026-08-25",
        "",
        "**Status:** metadata-only, pre-screening sensitivity analysis. It compares the final OA S1 candidate set with the complement of the matched all-access S2 universe. It is not a screened or included-study analysis.",
        "",
        "## Retrieval and reconciliation",
        "",
        "S2a was formed by deleting only the leading `OPENACCESS(1) AND ` predicate from S1a. S2b was formed the same way from S1b, then retrieved as disjoint 2025 and 2026 partitions because the unpartitioned API run hit a 200-page rate ceiling. The partition totals sum to the unpartitioned source total. Repeated API passes were reconciled by Scopus Paper ID only when their unique-ID union equalled the stable source total.",
        "",
        markdown_table(
            ["Stratum", "Source total", "Recovery passes", "Unique reconciled IDs"],
            [
                [run["label"], f"{run['source_reported_total']:,}", str(run.get("reconciliation_pass_count", 1)), f"{run['records_retrieved']:,}"]
                for run in summary["source_runs"]
            ],
        ),
        "",
        "## Matched comparison universe",
        "",
        markdown_table(
            ["Transition", "Records"],
            [
                ["Raw OA S1 source records", f"{counts['raw_oa_source_records']:,}"],
                ["Distinct OA S1 records", f"{counts['oa_unique_records']:,}"],
                ["Raw all-access S2 source records", f"{counts['raw_all_access_source_records']:,}"],
                ["Distinct all-access S2 records", f"{counts['all_access_unique_records']:,}"],
                ["Matched OA records in all-access universe", f"{oa_n:,} ({percent(oa_n, oa_n + non_n):.1f}%)"],
                ["All-access complement (called non-OA here)", f"{non_n:,} ({percent(non_n, oa_n + non_n):.1f}%)"],
                ["Unmatched OA records excluded from comparison", f"{counts['unmatched_oa_records']:,}"],
            ],
        ),
        "",
        "`non-OA` means the complement of the matched OA set in the all-access candidate universe; it is not a separately verified licence classification.",
        "",
        "## Year and retrieval-anchor composition",
        "",
        markdown_table(
            ["Dimension", "OA", "Non-OA", "OA availability"],
            [
                [row["label"], fmt_count_percent(row["oa_count"], oa_n), fmt_count_percent(row["non_oa_count"], non_n), f"{row['oa_availability_percent']:.1f}%"]
                for row in summary["year_rows"] + source_rows
            ],
        ),
        "",
        "The 2026 component remains incomplete because the source was searched before the end of the year.",
        "",
        "## Textual similarity",
        "",
        f"Title-plus-abstract unigram/bigram document-frequency profiles had cosine similarity **{similarity['cosine_similarity']:.3f}** and Jensen--Shannon divergence **{similarity['jensen_shannon_divergence']:.3f}**. Their top-term overlap was {similarity['top_20_overlap']} of 20 and {similarity['top_100_overlap']} of 100.",
        "",
    ]
    classifier = similarity["classifier"]
    if classifier["available"]:
        lines.append(
            f"A five-fold held-out text-only OA-status classifier had AUC **{classifier['auc']:.2f}** and balanced accuracy **{classifier['balanced_accuracy']:.2f}** (0.50 is chance)."
        )
        lines.append("")
    lines.extend(
        [
            "## Title/abstract topic markers",
            "",
            "Markers are transparent multi-label text checks, not screening labels, OPMAD annotations, or evidence of model superiority.",
            "",
            markdown_table(
                ["Marker", "OA", "Non-OA", "Difference (pp)", "OA availability"],
                [
                    [
                        row["label"],
                        fmt_count_percent(row["oa_count"], oa_n),
                        fmt_count_percent(row["non_oa_count"], non_n),
                        f"{row['difference_percentage_points']:+.1f}",
                        f"{row['oa_availability_percent']:.1f}%",
                    ]
                    for row in summary["marker_rows"]
                ],
            ),
            "",
            "## DOI-prefix source/platform proxy",
            "",
            markdown_table(
                ["Prefix", "All access", "OA", "OA rate", "OA / non-OA share"],
                [
                    [
                        row["prefix"],
                        f"{row['all_count']:,}",
                        f"{row['oa_count']:,}",
                        f"{row['oa_rate_percent']:.1f}%",
                        f"{row['oa_share_percent']:.1f}% / {row['non_oa_share_percent']:.1f}%",
                    ]
                    for row in summary["doi_prefix_rows"]
                ],
            ),
            "",
            "## Interpretation",
            "",
            "The comparison characterizes the final retrieved candidate population, not included studies. It supports OA-scoped claims only. Any substantive mapping result must still be based on screened, full-text-verified studies and validated extraction fields.",
            "",
        ]
    )
    return "\n".join(lines)


def write_new(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary_path, path)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def validate_s2_relation(s1_query: Path, s2_query: Path, label: str) -> None:
    s1 = s1_query.read_text(encoding="utf-8")
    s2 = s2_query.read_text(encoding="utf-8")
    if not s1.startswith(OA_PREFIX):
        raise AnalysisError(f"{s1_query} does not start with the OA predicate")
    if normalize_whitespace(s1.removeprefix(OA_PREFIX)) != normalize_whitespace(s2):
        raise AnalysisError(f"{label} is not exactly its S1 query with only OA removed")


def validate_s2b_partition(base_query: Path, partition_query: Path, year: int) -> None:
    base = base_query.read_text(encoding="utf-8")
    partition = partition_query.read_text(encoding="utf-8")
    broad_year = "PUBYEAR > 2024 AND PUBYEAR < 2027"
    replacement = (
        "PUBYEAR > 2024 AND PUBYEAR < 2026"
        if year == 2025
        else "PUBYEAR > 2025 AND PUBYEAR < 2027"
    )
    if partition.count(replacement) != 1 or normalize_whitespace(partition.replace(replacement, broad_year)) != normalize_whitespace(base):
        raise AnalysisError(f"{partition_query} is not the expected {year} S2b partition")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for prefix in ("s1a", "s1b", "s2a", "s2b_2025", "s2b_2026"):
        parser.add_argument(f"--{prefix.replace('_', '-')}-query", required=True, type=Path)
        parser.add_argument(
            f"--{prefix.replace('_', '-')}-pass",
            action="append",
            required=True,
            type=Path,
        )
    parser.add_argument("--s2b-base-query", required=True, type=Path)
    parser.add_argument("--summary-output-path", required=True, type=Path)
    parser.add_argument("--report-output-path", required=True, type=Path)
    args = parser.parse_args()
    if args.summary_output_path.resolve() == args.report_output_path.resolve():
        parser.error("summary and report outputs must differ")

    validate_s2_relation(args.s1a_query, args.s2a_query, "S2a")
    validate_s2_relation(args.s1b_query, args.s2b_base_query, "S2b")
    validate_s2b_partition(args.s2b_base_query, args.s2b_2025_query, 2025)
    validate_s2b_partition(args.s2b_base_query, args.s2b_2026_query, 2026)

    s1a_rows, s1a_receipt = reconcile_passes("S1a", args.s1a_query, args.s1a_pass)
    s1b_rows, s1b_receipt = reconcile_passes("S1b", args.s1b_query, args.s1b_pass)
    s2a_rows, s2a_receipt = reconcile_passes("S2a", args.s2a_query, args.s2a_pass)
    s2b_2025_rows, s2b_2025_receipt = reconcile_passes(
        "S2b-2025", args.s2b_2025_query, args.s2b_2025_pass
    )
    s2b_2026_rows, s2b_2026_receipt = reconcile_passes(
        "S2b-2026", args.s2b_2026_query, args.s2b_2026_pass
    )
    s2b_ids = {str(record["paperId"]) for record in s2b_2025_rows}
    if s2b_ids & {str(record["paperId"]) for record in s2b_2026_rows}:
        raise AnalysisError("S2b year partitions overlap in Scopus Paper IDs")
    s2b_rows = s2b_2025_rows + s2b_2026_rows
    s2b_receipt = {
        "label": "S2b",
        "source_reported_total": s2b_2025_receipt["source_reported_total"]
        + s2b_2026_receipt["source_reported_total"],
        "records_retrieved": len(s2b_rows),
        "retrieval_complete": True,
        "stopped_reason": "reconciled_disjoint_year_partitions",
        "reconciliation_mode": "union_of_2025_and_2026_no_oa_partitions",
        "reconciliation_pass_count": s2b_2025_receipt["reconciliation_pass_count"]
        + s2b_2026_receipt["reconciliation_pass_count"],
        "partitions": [s2b_2025_receipt, s2b_2026_receipt],
    }

    oa_union, oa_events = deduplicate_groups([("S1a", s1a_rows), ("S1b", s1b_rows)])
    all_union, all_events = deduplicate_groups([("S2a", s2a_rows), ("S2b", s2b_rows)])
    matched_oa, non_oa, unmatched_oa = match_oa_to_all(oa_union, all_union)

    s1a_unique, _ = deduplicate_groups([("S1a", s1a_rows)])
    s1b_unique, _ = deduplicate_groups([("S1b", s1b_rows)])
    s2a_unique, _ = deduplicate_groups([("S2a", s2a_rows)])
    s2b_unique, _ = deduplicate_groups([("S2b", s2b_rows)])
    s1a_matched, s2a_non_oa, _ = match_oa_to_all(s1a_unique, s2a_unique)
    s1b_matched, s2b_non_oa, _ = match_oa_to_all(s1b_unique, s2b_unique)

    raw_oa = s1a_receipt["source_reported_total"] + s1b_receipt["source_reported_total"]
    raw_all = s2a_receipt["source_reported_total"] + s2b_receipt["source_reported_total"]
    if raw_oa != 2861:
        raise AnalysisError(f"Unexpected raw OA source count: {raw_oa}")
    if raw_all != 9324:
        raise AnalysisError(f"Unexpected raw all-access source count: {raw_all}")

    summary: dict[str, Any] = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "status": "metadata_only_pre_screening_sensitivity_analysis",
        "generated_at_utc": utc_now(),
        "scope_note": "OA and all-access candidate metadata only; no eligibility screening, full-text verification, or licence verification has occurred.",
        "query_relationship": {
            "s2a": "S1a with only the leading OPENACCESS(1) AND predicate removed",
            "s2b": "S1b with only the leading OPENACCESS(1) AND predicate removed; retrieved as disjoint 2025/2026 partitions solely to avoid the API 200-page rate ceiling",
        },
        "source_runs": [s1a_receipt, s1b_receipt, s2a_receipt, s2b_receipt],
        "counts": {
            "raw_oa_source_records": raw_oa,
            "oa_unique_records": len(oa_union),
            "raw_all_access_source_records": raw_all,
            "all_access_unique_records": len(all_union),
            "matched_oa_records": len(matched_oa),
            "non_oa_complement_records": len(non_oa),
            "unmatched_oa_records": len(unmatched_oa),
            "oa_cross_stratum_duplicates_removed": len(oa_events),
            "all_access_cross_stratum_duplicates_removed": len(all_events),
        },
        "oa_deduplication_events": oa_events,
        "all_access_deduplication_events": all_events,
        "unmatched_oa_records": [
            {
                "paper_id": record["paperId"],
                "doi": record.get("doi"),
                "title": record.get("title"),
                "year": record.get("year"),
            }
            for record in unmatched_oa
        ],
        "year_rows": year_rows(matched_oa, non_oa),
        "source_stratum_rows": source_stratum_rows(matched_oa, non_oa),
        "marker_rows": marker_rows(matched_oa, non_oa),
        "doi_prefix_rows": doi_prefix_rows(matched_oa, non_oa),
        "textual_similarity": textual_similarity(matched_oa, non_oa),
        "within_stratum_classifier": {
            "maintenance_prognostic": classifier_metrics(s1a_matched, s2a_non_oa),
            "diagnostic_condition": classifier_metrics(s1b_matched, s2b_non_oa),
        },
        "analysis_script_sha256": sha256_file(Path(__file__)),
    }
    report = render_report(summary)
    write_new(args.summary_output_path, json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    try:
        write_new(args.report_output_path, report)
    except Exception:
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
