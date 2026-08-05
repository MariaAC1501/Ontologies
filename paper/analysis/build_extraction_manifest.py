#!/usr/bin/env python3
"""Build the auditable PDF-to-facts manifest shipped with the paper."""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment
from rapidfuzz import fuzz, process
from rdflib import Literal

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from pipeline.facts_to_csv import (  # noqa: E402
    cases_to_csv_rows, graph_to_cases, load_graph_from_ttl, parse_ontology_labels,
)

PAPERS = ROOT / "extraction_papers"
RUNS = PAPERS / "ontocast_runs"
OUT = ROOT / "paper/supplement/protocol/extraction_manifest.csv"
RUN_ORDER = [
    "run_100_20260611_194110", "run_500_20260710_185042",
    "run_500_more_20260721_105503",
    "run_remaining_500_gpt-5.6-luna_20260723_010000",
    "run_remaining_222_gpt-5.6-luna_20260723_010000",
    "run_retry_paper3215_gpt-5.6-luna_20260725_220000",
    "run_retry_failed_106_gpt-5.6-luna_20260725_220000",
    "run_retry_final_17_gpt-5.6-luna_20260726_040000",
    "run_retry_final_8_sanitized_gpt-5.6-luna_20260726_090000",
]
META = {
    RUN_ORDER[0]: ("gpt-5-mini", 3, "direct"),
    RUN_ORDER[1]: ("gpt-5-mini", 3, "direct_with_internal_retries"),
    RUN_ORDER[2]: ("gpt-5.4-mini", 3, "proxy; OntoCast alias gpt-5-mini"),
    RUN_ORDER[3]: ("gpt-5.6-luna", 3, "direct"),
    RUN_ORDER[4]: ("gpt-5.6-luna", 3, "direct"),
    RUN_ORDER[5]: ("gpt-5.6-luna", 1, "retry"),
    RUN_ORDER[6]: ("gpt-5.6-luna", 3, "retry"),
    RUN_ORDER[7]: ("gpt-5.6-luna", 1, "retry_invalid_iri"),
    RUN_ORDER[8]: ("gpt-5.6-luna", 1, "retry_sanitized_control_characters"),
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower().replace("–", "-")))


def similarity(a: str, b: str) -> float:
    a, b = normalize(a), normalize(b)
    if not a or not b or a.startswith("untitled extracted case"):
        return 0.0
    if a == b:
        return 1.0
    sa, sb = set(a.split()), set(b.split())
    jaccard = len(sa & sb) / len(sa | sb)
    sequence = SequenceMatcher(None, a, b, autojunk=False).ratio()
    containment = min(len(a), len(b)) / max(len(a), len(b)) if a in b or b in a else 0.0
    return max(jaccard, sequence, containment)


def csv_rows(path: Path, delimiter: str = ",") -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))


metadata = {r["corpus_id"]: r for r in csv_rows(PAPERS / "scopus_export_May 26-2026_screened.csv")}
pdf_by_id = {p.name.split("_", 1)[0]: p for p in PAPERS.glob("paper-*.pdf")}
history: dict[str, list[str]] = defaultdict(list)
for run in RUN_ORDER:
    for row in csv_rows(RUNS / run / "manifest.csv"):
        history[row["corpus_id"]].append(run)
final_run = {cid: runs[-1] for cid, runs in history.items()}
ids_by_run: dict[str, list[str]] = defaultdict(list)
for cid, run in final_run.items():
    ids_by_run[run].append(cid)

query_by_fact: dict[str, dict[str, str]] = {}
for row in csv_rows(ROOT / ".build/diversity_comparison_1821_v12_no_default_sync/queries.csv", ";"):
    query_by_fact[Path(row["facts_file"]).resolve().as_posix().lower()] = row

labels = parse_ontology_labels(ROOT / "pipeline/seed_ontology/opmad_seed.ttl")
fact_info: dict[Path, dict[str, str]] = {}
for run in RUN_ORDER:
    for fact in sorted((RUNS / run / "output").glob("facts_*.ttl")):
        graph = load_graph_from_ttl(fact)
        cases = graph_to_cases(graph, labels)
        first = cases_to_csv_rows(cases[:1])[0]
        candidates = sorted({str(obj) for obj in graph.objects() if isinstance(obj, Literal) and len(str(obj).split()) >= 4})
        fact_info[fact] = {
            "extracted_title": first["Study title"], "extracted_task": first["Task"],
            "extracted_case_count": str(len(cases)), "_candidates": candidates,
        }

# corpus_id -> (facts, link method, title score)
links: dict[str, tuple[Path, str, float]] = {}
coverage = csv_rows(RUNS / RUN_ORDER[1] / "final_coverage_manifest.csv")
for row in coverage:
    cid = row["corpus_id"]
    fact = RUNS / RUN_ORDER[1] / "output" / row["facts_file"]
    links[cid] = (fact, "historical_final_coverage_manifest", 1.0)

# Older logs did not preserve PDF->facts identifiers. Reconstruct within each
# final run by globally optimal title assignment and expose the score.
for run in RUN_ORDER:
    ids = sorted(cid for cid in ids_by_run[run] if cid not in links)
    facts = sorted(f for f in fact_info if f.parent.parent.name == run)
    if not ids:
        continue
    if len(ids) != len(facts):
        raise RuntimeError(f"{run}: {len(ids)} PDFs vs {len(facts)} facts")
    matrix = np.array([[similarity(metadata[cid]["Title"], fact_info[f]["extracted_title"]) for f in facts] for cid in ids])
    flat_candidates: list[str] = []
    candidate_fact: list[int] = []
    for j, fact in enumerate(facts):
        for candidate in fact_info[fact]["_candidates"]:
            flat_candidates.append(normalize(candidate)); candidate_fact.append(j)
    for i, cid in enumerate(ids):
        title = normalize(metadata[cid]["Title"])
        for _, score, candidate_index in process.extract(title, flat_candidates, scorer=fuzz.ratio, limit=100):
            j = candidate_fact[candidate_index]
            matrix[i, j] = max(matrix[i, j], score / 100.0)
    rows, cols = linear_sum_assignment(-matrix)
    for i, j in zip(rows, cols, strict=True):
        links[ids[i]] = (facts[j], "reconstructed_bipartite_title_match", float(matrix[i, j]))

fields = [
    "corpus_id", "source_title", "pdf_file", "pdf_sha256", "duplicate_sha256_count",
    "final_extraction_run", "actual_model", "chunks", "retry_run_count",
    "sanitization", "run_notes", "facts_file", "facts_sha256", "query_index",
    "extracted_title", "extracted_task", "extracted_case_count", "matched_graph_literal", "linkage_method",
    "title_match_score", "linkage_confidence",
]
pdf_hashes = {cid: digest(path) for cid, path in pdf_by_id.items()}
hash_counts = Counter(pdf_hashes.values())
out_rows: list[dict[str, object]] = []
for cid in sorted(pdf_by_id, key=lambda x: int(x.split("-")[1])):
    run = final_run[cid]
    fact, method, score = links[cid]
    model, chunks, notes = META[run]
    if cid == "paper-2261":
        chunks, notes = 1, notes + "; head1 retry"
    sanitized = run == RUN_ORDER[8] or cid == "paper-0712"
    query = query_by_fact.get(fact.resolve().as_posix().lower(), {})
    candidates = fact_info[fact]["_candidates"]
    matched = process.extractOne(metadata[cid]["Title"], candidates, scorer=fuzz.ratio)[0] if candidates else ""
    confidence = "exact_or_near_exact" if method.startswith("historical") or score >= .98 else ("high" if score >= .9 else "medium" if score >= .7 else "low")
    public_info = {key: value for key, value in fact_info[fact].items() if not key.startswith("_")}
    out_rows.append({
        "corpus_id": cid, "source_title": metadata[cid]["Title"],
        "pdf_file": pdf_by_id[cid].relative_to(ROOT).as_posix(), "pdf_sha256": pdf_hashes[cid],
        "duplicate_sha256_count": hash_counts[pdf_hashes[cid]], "final_extraction_run": run,
        "actual_model": model, "chunks": chunks, "retry_run_count": len(history[cid]) - 1,
        "sanitization": str(sanitized).lower(), "run_notes": notes,
        "facts_file": fact.relative_to(ROOT).as_posix(), "facts_sha256": digest(fact),
        "query_index": query.get("query_index", ""), **public_info, "matched_graph_literal": matched, "linkage_method": method,
        "title_match_score": f"{score:.6f}", "linkage_confidence": confidence,
    })
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader(); writer.writerows(out_rows)
print(f"Wrote {len(out_rows)} rows to {OUT}")
print("Confidence:", Counter(r["linkage_confidence"] for r in out_rows))
print("Queries linked:", sum(bool(r["query_index"]) for r in out_rows))
