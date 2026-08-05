#!/usr/bin/env python3
"""Compare plain CBR retrieval with Diversity-in-CBR-aware MMR reranking.

The comparison uses one CBR query per ``facts_*.ttl`` artifact in a canonical
``ontocast_runs/*/output`` directory under ``extraction_papers``. It deliberately does not call OntoCast or spend API
credits: PDFs without an existing facts artifact are reported as uncovered.

For each facts file, the script derives the first extracted case, normalizes its
query fields to the legacy CBR vocabulary, retrieves a top-k baseline, retrieves
a larger candidate pool, and reranks that pool with
``pipeline.diversity_rerank``.  The latter reads the taxonomy maintained in the
``external/Diversity-Improvement-in-CBR`` submodule.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from statistics import fmean
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.diversity_rerank import (  # noqa: E402
    DEFAULT_WEIGHTS,
    build_taxonomy_index,
    load_casebase,
    load_taxonomy_tree,
    normalize_text,
    parse_float,
    process_file,
    solution_similarity,
)
from pipeline.facts_to_csv import (  # noqa: E402
    cases_to_csv_rows,
    graph_to_cases,
    load_graph_from_ttl,
    parse_ontology_labels,
)

CBR_DATA_RELATIVE = Path(
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data"
)
# The bundled PredictMaint_myCBR.prj contains the 263 cases from V12.
# Use the matching CSV so every retrieved reference has a complete solution
# signature during diversity scoring. V21 remains the 200-row extraction-schema
# validation target documented in pipeline/SCHEMA_MAPPING.md.
CASEBASE_RELATIVE = CBR_DATA_RELATIVE / "CleanedDATA V12-05-2021.csv"
SEED_ONTOLOGY_RELATIVE = Path("pipeline/seed_ontology/opmad_seed.ttl")
QUERY_HEADERS = [
    "Task",
    "w1",
    "Case study type",
    "w2",
    "Case study",
    "w3",
    "Online/Offline",
    "w4",
    "Input for the model",
    "w5",
    "Input type",
    "w6",
    "Query Year",
    "Number of cases to retrieve",
    "Amalgamation function",
]


@dataclass
class QueryRecord:
    query_index: int
    facts_file: str
    extracted_case_count: int
    task: str
    case_study_type: str
    case_study: str
    online_offline: str
    input_for_model: str
    input_type: str
    normalization_notes: str


@dataclass
class ResultMetrics:
    rows: int
    references: list[str]
    top_similarity: float
    mean_similarity: float
    unique_models: int
    has_duplicate_models: bool
    intra_list_dissimilarity: float


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_semicolon_csv(path: Path, *, encoding: str = "utf-8-sig") -> list[dict[str, str]]:
    for candidate_encoding in (encoding, "utf-8", "latin-1", "windows-1252"):
        try:
            with path.open("r", encoding=candidate_encoding, newline="") as handle:
                return list(csv.DictReader(handle, delimiter=";"))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode CSV: {path}")


def write_semicolon_csv(path: Path, headers: Iterable[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(headers), delimiter=";", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_reference_vocabulary(casebase_path: Path) -> dict[str, set[str]]:
    rows = read_semicolon_csv(casebase_path, encoding="latin-1")
    if not rows:
        raise RuntimeError(f"The CBR case base is empty: {casebase_path}")

    def values(field: str) -> set[str]:
        return {row.get(field, "").strip() for row in rows if row.get(field, "").strip()}

    return {
        "task": values("Task"),
        "case_study_type": values("Case study type"),
        "case_study": values("Case study"),
        "online_offline": values("Online/Off-line"),
        "input_for_model": values("Input for the model"),
    }


def is_generated_or_missing(value: str) -> bool:
    normalized = normalize_text(value)
    return not normalized or normalized == "not reported" or normalized.startswith("facts")


def normalize_query(
    case_row: dict[str, str],
    vocabulary: dict[str, set[str]],
    *,
    drop_default_synchronization: bool = False,
) -> tuple[dict[str, str], list[str]]:
    query = {
        "task": case_row.get("Task", "").strip(),
        "case_study_type": case_row.get("Case study type", "").strip(),
        "case_study": case_row.get("Case study", "").strip(),
        "online_offline": case_row.get("Online/Off-line", "").strip(),
        "input_for_model": case_row.get("Input for the model", "").strip(),
        "input_type": case_row.get("Input type", "").strip(),
    }
    notes: list[str] = []

    if query["task"] not in vocabulary["task"]:
        if "future state forecast" in query["task"].lower():
            query["task"] = "One step future state forecast"
            notes.append("task mapped to One step future state forecast")
        else:
            notes.append(f"task dropped: {query['task'] or 'empty'}")
            query["task"] = ""

    # Case study is a free-text similarity attribute in myCBR.  Retain literals
    # such as "Lithium-ion battery" even when the legacy case base has no exact
    # spelling; discard only OntoCast placeholders / generated resource names.
    if query["case_study_type"] not in vocabulary["case_study_type"]:
        if query["case_study_type"]:
            notes.append(f"case-study type dropped: {query['case_study_type']}")
        query["case_study_type"] = ""
    if is_generated_or_missing(query["case_study"]):
        if query["case_study"]:
            notes.append(f"case study dropped: {query['case_study']}")
        query["case_study"] = ""
    if drop_default_synchronization and normalize_text(query["online_offline"]) == "unknown synchronization":
        notes.append("default online/offline dropped: Unknown synchronization")
        query["online_offline"] = ""
    elif query["online_offline"] not in vocabulary["online_offline"]:
        if query["online_offline"]:
            notes.append(f"online/offline dropped: {query['online_offline']}")
        query["online_offline"] = ""

    if query["input_for_model"] not in vocabulary["input_for_model"]:
        mapped = {"data collection": "Signals"}.get(normalize_text(query["input_for_model"]), "")
        if mapped:
            query["input_for_model"] = mapped
            notes.append("input-for-model mapped to Signals")
        else:
            if query["input_for_model"]:
                notes.append(f"input-for-model dropped: {query['input_for_model']}")
            query["input_for_model"] = ""

    input_type_parts = [part.strip() for part in query["input_type"].split(",") if part.strip()]
    try:
        input_variable_count = int(case_row.get("Number of input variables", "0"))
    except ValueError:
        input_variable_count = 0
    # A lone generated resource name carries no query signal.  For multi-input
    # studies, retain the complete list: even when OntoCast names are imperfect,
    # it preserves the source study's dimensionality and matches the existing
    # batch-comparison normalization policy.
    if (
        input_variable_count <= 1
        and input_type_parts
        and all(is_generated_or_missing(part) for part in input_type_parts)
    ):
        notes.append(f"input type dropped: {query['input_type']}")
        query["input_type"] = ""

    return query, notes


def query_csv_row(query: dict[str, str], number_of_cases: int, query_year: int) -> dict[str, str]:
    def weight(value: str) -> str:
        return "1" if value else ""

    return {
        "Task": query["task"],
        "w1": weight(query["task"]),
        "Case study type": query["case_study_type"],
        "w2": weight(query["case_study_type"]),
        "Case study": query["case_study"],
        "w3": weight(query["case_study"]),
        "Online/Offline": query["online_offline"],
        "w4": weight(query["online_offline"]),
        "Input for the model": query["input_for_model"],
        "w5": weight(query["input_for_model"]),
        "Input type": query["input_type"],
        "w6": weight(query["input_type"]),
        "Query Year": str(query_year),
        "Number of cases to retrieve": str(number_of_cases),
        "Amalgamation function": "euclidean",
    }


def derive_queries(
    fact_paths: list[Path],
    ontology_path: Path,
    vocabulary: dict[str, set[str]],
    *,
    drop_default_synchronization: bool = False,
) -> tuple[list[QueryRecord], list[dict[str, str]]]:
    ontology_labels = parse_ontology_labels(ontology_path)
    records: list[QueryRecord] = []
    query_rows: list[dict[str, str]] = []

    for index, fact_path in enumerate(fact_paths, start=1):
        cases = graph_to_cases(load_graph_from_ttl(fact_path), ontology_labels)
        if not cases:
            raise RuntimeError(f"No CBR case could be derived from facts artifact: {fact_path}")
        # Facts can contain cited publications as well as the source study.  Each
        # facts file represents one input PDF, so retain its first deterministic
        # case rather than treating citations as additional papers.
        case_row = cases_to_csv_rows([cases[0]])[0]
        query, notes = normalize_query(
            case_row,
            vocabulary,
            drop_default_synchronization=drop_default_synchronization,
        )
        records.append(
            QueryRecord(
                query_index=index,
                facts_file=repo_relative(fact_path),
                extracted_case_count=len(cases),
                task=case_row["Task"],
                case_study_type=case_row["Case study type"],
                case_study=case_row["Case study"],
                online_offline=case_row["Online/Off-line"],
                input_for_model=case_row["Input for the model"],
                input_type=case_row["Input type"],
                normalization_notes=" | ".join(notes),
            )
        )
        query_rows.append(query)

    return records, query_rows


def ensure_cbr_build(python: str) -> Path:
    subprocess.run([python, str(ROOT / "scripts" / "build_cbr.py")], cwd=ROOT, check=True)
    classpath_path = ROOT / ".build" / "cbr" / "jar-classpath.txt"
    classpath = classpath_path.read_text(encoding="utf-8").strip()
    if not classpath:
        raise RuntimeError(f"Empty CBR classpath file: {classpath_path}")
    return classpath_path


def run_batch_query(classpath_path: Path, data_dir: Path, input_csv: Path, output_prefix: str) -> None:
    classpath = classpath_path.read_text(encoding="utf-8").strip()
    command = [
        "java",
        "-Djava.awt.headless=true",
        "-cp",
        classpath,
        "HeadlessCBR",
        "--data-dir",
        str(data_dir),
        "query-batch",
        str(input_csv),
        output_prefix,
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def result_metrics(
    path: Path,
    *,
    casebase_by_reference: dict[str, dict[str, str]],
    taxonomy_index: dict[str, int],
) -> ResultMetrics:
    rows = read_semicolon_csv(path)
    references = [row.get("Reference", "").strip() for row in rows]
    similarities = [parse_float(row.get("Sim")) for row in rows]
    models = [normalize_text(row.get("Models")) for row in rows if normalize_text(row.get("Models"))]
    pairwise_dissimilarities: list[float] = []
    for left_index, left in enumerate(rows):
        for right in rows[left_index + 1 :]:
            similarity = solution_similarity(
                left,
                right,
                casebase_by_reference,
                taxonomy_index,
                DEFAULT_WEIGHTS,
            )
            pairwise_dissimilarities.append(1.0 - similarity)

    return ResultMetrics(
        rows=len(rows),
        references=references,
        top_similarity=similarities[0] if similarities else 0.0,
        mean_similarity=fmean(similarities) if similarities else 0.0,
        unique_models=len(set(models)),
        has_duplicate_models=len(models) != len(set(models)),
        intra_list_dissimilarity=fmean(pairwise_dissimilarities) if pairwise_dissimilarities else 0.0,
    )


def aggregate(metrics: list[ResultMetrics]) -> dict[str, float | int]:
    successful = [item for item in metrics if item.rows]
    return {
        "queries": len(metrics),
        "successful_queries": len(successful),
        "total_result_rows": sum(item.rows for item in metrics),
        "average_rows": fmean(item.rows for item in successful) if successful else 0.0,
        "average_top_similarity": fmean(item.top_similarity for item in successful) if successful else 0.0,
        "average_mean_similarity": fmean(item.mean_similarity for item in successful) if successful else 0.0,
        "average_unique_models": fmean(item.unique_models for item in successful) if successful else 0.0,
        "queries_with_duplicate_models": sum(item.has_duplicate_models for item in successful),
        "average_intra_list_dissimilarity": fmean(item.intra_list_dissimilarity for item in successful) if successful else 0.0,
    }


def write_report(path: Path, summary: dict[str, object], *, run_dir: Path) -> None:
    coverage = summary["coverage"]
    baseline = summary["baseline"]
    diverse = summary["with_diversity"]
    comparison = summary["comparison"]
    method = summary["method"]
    lines = [
        "# Comparación de diversidad CBR",
        "",
        f"Directorio de ejecución: `{repo_relative(run_dir)}`",
        "",
        "## Cobertura",
        "",
        f"- Archivos PDF de primer nivel en `extraction_papers`: **{coverage['corpus_pdf_files']}**.",
        f"- Documentos PDF únicos por SHA-256: **{coverage['unique_pdf_documents']}**.",
        f"- Archivos duplicados adicionales: **{coverage['duplicate_pdf_files']}**.",
        f"- Artefactos canónicos `facts_*.ttl` disponibles: **{coverage['facts_artifacts']}**.",
        f"- Consultas comparadas (una por artefacto): **{coverage['queries_analyzed']}**.",
        f"- Documentos únicos sin facts canónicos (estimación por conteo): **{coverage['unique_documents_without_facts_estimate']}**.",
        "",
        "La cobertura distingue archivos de documentos únicos para no contar un duplicado exacto como extracción ausente.",
        "",
        "## Método",
        "",
        f"- Sin diversidad: top-{method['top_k']} por similitud de HeadlessCBR.",
        f"- Con diversidad: pool-{method['pool_size']} de HeadlessCBR y MMR top-{method['top_k']} (`lambda={method['lambda_relevance']:.2f}`).",
        f"- La similitud entre soluciones usa enfoque, tipo, modelos y preprocesamiento; la taxonomía contiene {method['taxonomy_terms_loaded']} términos leídos de `external/Diversity-Improvement-in-CBR/Methods2.py`.",
        "",
        "## Resultados",
        "",
        "| Métrica | Sin diversidad | Con diversidad |",
        "|---|---:|---:|",
        f"| Consultas con resultados | {baseline['successful_queries']}/{baseline['queries']} | {diverse['successful_queries']}/{diverse['queries']} |",
        f"| Similitud del primer resultado | {baseline['average_top_similarity']:.4f} | {diverse['average_top_similarity']:.4f} |",
        f"| Similitud media del top-k | {baseline['average_mean_similarity']:.4f} | {diverse['average_mean_similarity']:.4f} |",
        f"| Modelos únicos por lista | {baseline['average_unique_models']:.2f} | {diverse['average_unique_models']:.2f} |",
        f"| Listas con modelos repetidos | {baseline['queries_with_duplicate_models']} | {diverse['queries_with_duplicate_models']} |",
        f"| Disimilitud intra-lista (0–1) | {baseline['average_intra_list_dissimilarity']:.4f} | {diverse['average_intra_list_dissimilarity']:.4f} |",
        "",
        "## Cambios frente al baseline",
        "",
        f"- Orden top-k cambiado: **{comparison['queries_changed_order']}/{comparison['paired_queries']}**.",
        f"- Conjunto de referencias top-k cambiado: **{comparison['queries_changed_reference_set']}/{comparison['paired_queries']}**.",
        f"- Primer resultado preservado: **{comparison['queries_top1_preserved']}/{comparison['paired_queries']}**.",
        "",
        "Los datos por consulta están en `per_query.csv`; las consultas normalizadas en `queries.csv`; y las listas CBR y rerankeadas en `cbr_data/` y `with_diversity/`.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--papers-dir", default="extraction_papers", help="Corpus directory containing PDFs and OntoCast output.")
    parser.add_argument("--facts-glob", default="ontocast_runs/*/output/facts_*.ttl", help="Glob relative to --papers-dir used to discover canonical facts artifacts.")
    parser.add_argument("--ontology", default=str(SEED_ONTOLOGY_RELATIVE), help="OPMAD ontology used to label facts.")
    parser.add_argument(
        "--casebase-csv",
        default=str(CASEBASE_RELATIVE),
        help=(
            "Case-base CSV used for query vocabulary and solution-field enrichment. "
            "It must correspond to the loaded myCBR project (the bundled 263-case "
            "PredictMaint_myCBR.prj corresponds to CleanedDATA V12-05-2021.csv)."
        ),
    )
    parser.add_argument("--output-dir", help="New directory for the comparison artifacts (default: .build/diversity_comparison_<timestamp>).")
    parser.add_argument("--top-k", type=int, default=5, help="Number of baseline and reranked recommendations.")
    parser.add_argument("--pool-size", type=int, default=15, help="CBR candidate pool size before MMR reranking.")
    parser.add_argument("--lambda-relevance", type=float, default=0.70, help="MMR relevance weight in [0, 1].")
    parser.add_argument(
        "--query-year",
        type=int,
        default=datetime.now().year,
        help="Year supplied to myCBR's publication-recency similarity (default: current year).",
    )
    parser.add_argument("--max-facts", type=int, default=0, help="Optional cap for a smoke test; 0 processes every available facts artifact.")
    parser.add_argument(
        "--drop-default-synchronization",
        action="store_true",
        help="Treat the bridge default 'Unknown synchronization' as missing (weight zero) for an ablation.",
    )
    parser.add_argument("--skip-build", action="store_true", help="Use an existing .build/cbr/jar-classpath.txt instead of rebuilding CBR.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.top_k <= 0 or args.pool_size < args.top_k:
        raise SystemExit("--top-k must be positive and --pool-size must be at least --top-k")
    if not 0.0 <= args.lambda_relevance <= 1.0:
        raise SystemExit("--lambda-relevance must be in [0, 1]")

    papers_dir = (ROOT / args.papers_dir).resolve()
    ontology_path = (ROOT / args.ontology).resolve()
    source_data_dir = (ROOT / CBR_DATA_RELATIVE).resolve()
    casebase_path = Path(args.casebase_csv)
    if not casebase_path.is_absolute():
        casebase_path = (ROOT / casebase_path).resolve()
    diversity_dir = (ROOT / "external" / "Diversity-Improvement-in-CBR").resolve()
    if not papers_dir.is_dir():
        raise SystemExit(f"Papers directory does not exist: {papers_dir}")
    if not ontology_path.is_file():
        raise SystemExit(f"Ontology does not exist: {ontology_path}")
    if not source_data_dir.is_dir() or not casebase_path.is_file():
        raise SystemExit(f"CBR data directory or case base is missing: {source_data_dir}")
    if not diversity_dir.is_dir():
        raise SystemExit(f"Diversity submodule is missing: {diversity_dir}")

    fact_paths = sorted(papers_dir.glob(args.facts_glob))
    if args.max_facts > 0:
        fact_paths = fact_paths[: args.max_facts]
    if not fact_paths:
        raise SystemExit(f"No facts artifacts matched {args.facts_glob!r} under {papers_dir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = (ROOT / (args.output_dir or f".build/diversity_comparison_{timestamp}")).resolve()
    if run_dir.exists():
        raise SystemExit(f"Output directory already exists: {run_dir}")
    run_dir.mkdir(parents=True)

    vocabulary = read_reference_vocabulary(casebase_path)
    records, query_data = derive_queries(
        fact_paths,
        ontology_path,
        vocabulary,
        drop_default_synchronization=args.drop_default_synchronization,
    )
    top_queries = [query_csv_row(query, args.top_k, args.query_year) for query in query_data]
    pool_queries = [query_csv_row(query, args.pool_size, args.query_year) for query in query_data]

    query_rows = []
    for record, top_query, pool_query in zip(records, top_queries, pool_queries):
        row = asdict(record)
        row.update({f"normalized_{key}": value for key, value in query_data[record.query_index - 1].items()})
        row["top_k"] = top_query["Number of cases to retrieve"]
        row["pool_size"] = pool_query["Number of cases to retrieve"]
        query_rows.append(row)
    write_semicolon_csv(run_dir / "queries.csv", list(query_rows[0]), query_rows)
    write_semicolon_csv(run_dir / "query_batch_input_topk.csv", QUERY_HEADERS, top_queries)
    write_semicolon_csv(run_dir / "query_batch_input_pool.csv", QUERY_HEADERS, pool_queries)

    if args.skip_build:
        classpath_path = ROOT / ".build" / "cbr" / "jar-classpath.txt"
        if not classpath_path.is_file():
            raise SystemExit(f"Cannot --skip-build; CBR classpath is missing: {classpath_path}")
    else:
        classpath_path = ensure_cbr_build(sys.executable)

    data_dir = run_dir / "cbr_data"
    shutil.copytree(source_data_dir, data_dir)
    print(f"Running {len(records)} baseline CBR queries...")
    run_batch_query(classpath_path, data_dir, run_dir / "query_batch_input_topk.csv", "baseline_results_")
    print(f"Running {len(records)} CBR candidate-pool queries...")
    run_batch_query(classpath_path, data_dir, run_dir / "query_batch_input_pool.csv", "pool_results_")

    casebase_by_reference = load_casebase(casebase_path)
    taxonomy_index = build_taxonomy_index(load_taxonomy_tree(diversity_dir))
    if not taxonomy_index:
        raise RuntimeError(f"No diversity taxonomy terms could be loaded from {diversity_dir}")
    diverse_dir = run_dir / "with_diversity"
    rerank_summaries: list[dict[str, object]] = []
    for index in range(1, len(records) + 1):
        raw_path = data_dir / f"pool_results_{index}.csv"
        if not raw_path.is_file():
            raise RuntimeError(f"CBR did not create expected candidate-pool output: {raw_path}")
        rerank_summaries.append(
            process_file(
                raw_path,
                output_dir=diverse_dir,
                suffix=".diverse.csv",
                top_k=args.top_k,
                lambda_relevance=args.lambda_relevance,
                casebase_by_ref=casebase_by_reference,
                taxonomy_index=taxonomy_index,
                weights=DEFAULT_WEIGHTS,
                keep_top1=True,
                pool_size=args.pool_size,
            )
        )
    (run_dir / "diversity_rerank_summary.json").write_text(json.dumps(rerank_summaries, indent=2), encoding="utf-8")

    baseline_metrics: list[ResultMetrics] = []
    diverse_metrics: list[ResultMetrics] = []
    per_query_rows: list[dict[str, object]] = []
    for record in records:
        index = record.query_index
        baseline_path = data_dir / f"baseline_results_{index}.csv"
        diverse_path = diverse_dir / f"pool_results_{index}.diverse.csv"
        if not baseline_path.is_file() or not diverse_path.is_file():
            raise RuntimeError(f"Missing paired result for query {index}")
        baseline_result = result_metrics(
            baseline_path,
            casebase_by_reference=casebase_by_reference,
            taxonomy_index=taxonomy_index,
        )
        diverse_result = result_metrics(
            diverse_path,
            casebase_by_reference=casebase_by_reference,
            taxonomy_index=taxonomy_index,
        )
        baseline_metrics.append(baseline_result)
        diverse_metrics.append(diverse_result)
        per_query_rows.append(
            {
                "query_index": index,
                "facts_file": record.facts_file,
                "task": record.task,
                "baseline_refs": ",".join(baseline_result.references),
                "diverse_refs": ",".join(diverse_result.references),
                "changed_order": baseline_result.references != diverse_result.references,
                "changed_reference_set": set(baseline_result.references) != set(diverse_result.references),
                "top1_preserved": bool(baseline_result.references and diverse_result.references and baseline_result.references[0] == diverse_result.references[0]),
                "baseline_top_similarity": f"{baseline_result.top_similarity:.6f}",
                "diverse_top_similarity": f"{diverse_result.top_similarity:.6f}",
                "baseline_mean_similarity": f"{baseline_result.mean_similarity:.6f}",
                "diverse_mean_similarity": f"{diverse_result.mean_similarity:.6f}",
                "baseline_unique_models": baseline_result.unique_models,
                "diverse_unique_models": diverse_result.unique_models,
                "baseline_intra_list_dissimilarity": f"{baseline_result.intra_list_dissimilarity:.6f}",
                "diverse_intra_list_dissimilarity": f"{diverse_result.intra_list_dissimilarity:.6f}",
            }
        )
    write_semicolon_csv(run_dir / "per_query.csv", list(per_query_rows[0]), per_query_rows)

    corpus_pdfs = [path for path in papers_dir.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"]
    pdfs_by_hash: dict[str, list[str]] = {}
    for pdf_path in corpus_pdfs:
        pdfs_by_hash.setdefault(file_sha256(pdf_path), []).append(pdf_path.name)
    duplicate_pdf_groups = [sorted(names) for names in pdfs_by_hash.values() if len(names) > 1]
    task_distribution = Counter(record.task for record in records)
    baseline_summary = aggregate(baseline_metrics)
    diverse_summary = aggregate(diverse_metrics)
    summary: dict[str, object] = {
        "run_dir": repo_relative(run_dir),
        "coverage": {
            "papers_dir": repo_relative(papers_dir),
            "corpus_pdf_files": len(corpus_pdfs),
            "unique_pdf_documents": len(pdfs_by_hash),
            "duplicate_pdf_files": len(corpus_pdfs) - len(pdfs_by_hash),
            "duplicate_pdf_groups": duplicate_pdf_groups,
            "facts_artifacts": len(fact_paths),
            "queries_analyzed": len(records),
            "unique_documents_without_facts_estimate": max(0, len(pdfs_by_hash) - len(fact_paths)),
            "note": "Coverage is computed over unique PDF content; exact duplicate files are not treated as missing facts.",
        },
        "method": {
            "baseline": f"HeadlessCBR top-{args.top_k} similarity retrieval",
            "with_diversity": f"HeadlessCBR pool-{args.pool_size} followed by MMR top-{args.top_k}",
            "top_k": args.top_k,
            "pool_size": args.pool_size,
            "lambda_relevance": args.lambda_relevance,
            "query_year": args.query_year,
            "drop_default_synchronization": args.drop_default_synchronization,
            "solution_weights": DEFAULT_WEIGHTS,
            "casebase_csv": repo_relative(casebase_path),
            "casebase_rows_loaded": len(casebase_by_reference),
            "diversity_submodule": repo_relative(diversity_dir),
            "taxonomy_terms_loaded": len(taxonomy_index),
            "first_result_is_preserved": True,
        },
        "baseline": baseline_summary,
        "with_diversity": diverse_summary,
        "comparison": {
            "paired_queries": len(records),
            "queries_changed_order": sum(row["changed_order"] for row in per_query_rows),
            "queries_changed_reference_set": sum(row["changed_reference_set"] for row in per_query_rows),
            "queries_top1_preserved": sum(row["top1_preserved"] for row in per_query_rows),
        },
        "extraction": {
            "additional_cases_in_facts_not_used_as_paper_queries": sum(record.extracted_case_count - 1 for record in records),
            "source_task_distribution": dict(sorted(task_distribution.items())),
        },
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(run_dir / "REPORT.md", summary, run_dir=run_dir)
    print(f"Comparison complete: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
