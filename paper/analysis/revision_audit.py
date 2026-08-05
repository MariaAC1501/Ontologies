#!/usr/bin/env python3
"""Auditorías adicionales solicitadas durante la revisión del manuscrito.

Calcula, sin sustituir una anotación humana:
- cobertura y defaults de los 19 campos del puente RDF--CBR;
- pérdida de información durante normalización de consultas;
- resultados por modelo/chunks/confianza de enlace;
- costes de relevancia en posiciones 2--5;
- transición de duplicados y distribución de cambios;
- IC bootstrap por consulta, firma normalizada y patrón de ranking;
- una muestra estratificada y plantilla para validación experta futura.
"""
from __future__ import annotations

import csv
import hashlib
import json
import logging
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd
from rdflib import Literal, RDF, URIRef

logging.getLogger("rdflib.term").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.extraction_schema import TASK_CLASS_IRIS  # noqa: E402
from pipeline.facts_to_csv import (  # noqa: E402
    cases_to_csv_rows,
    graph_to_cases,
    load_graph_from_ttl,
    local_name,
    parse_ontology_labels,
    typed_entities,
)

RUN = ROOT / ".build" / "diversity_comparison_1821_v12_no_default_sync"
SUPPLEMENT = ROOT / "paper" / "supplement"
OUT = SUPPLEMENT / "audit"
ONTOLOGY = ROOT / "pipeline" / "seed_ontology" / "opmad_seed.ttl"
MANIFEST = SUPPLEMENT / "protocol" / "extraction_manifest.csv"
QUERIES = SUPPLEMENT / "results" / "queries.csv"
PER_QUERY = SUPPLEMENT / "results" / "per_query.csv"
SEED = 20260727
BOOTSTRAP_RESAMPLES = 20_000
MISSING_TEXT = {"", "not reported", "unknown", "unknown synchronization", "untitled extracted case"}
TASK_LOCAL_NAMES = {local_name(uri) for uri in TASK_CLASS_IRIS.values()}


def normalize(value: object) -> str:
    return " ".join(str(value or "").strip().lower().split())


def generated_text(value: object) -> bool:
    text = normalize(value)
    return (
        text in MISSING_TEXT
        or text.startswith("facts")
        or text.startswith("urn:ontocast:facts:")
        or text == "maintainable item"
    )


def split_values(value: object) -> list[str]:
    return [part.strip() for part in str(value or "").split(",") if part.strip()]


def informative_list(value: object) -> bool:
    values = split_values(value)
    return bool(values) and any(not generated_text(item) for item in values)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_result_rows(path: Path) -> list[dict[str, str]]:
    for encoding in ("utf-8-sig", "utf-8", "latin-1", "windows-1252"):
        try:
            with path.open(encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle, delimiter=";"))
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode {path}")


def explicit_task_evidence(graph) -> bool:
    entities = typed_entities(graph)
    if any(name in TASK_LOCAL_NAMES for name in entities):
        return True
    for predicate in (
        URIRef("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#describes_type"),
        URIRef("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD/seed#describes_type"),
    ):
        if any(True for _ in graph.triples((None, predicate, None))):
            return True
    return False


def audit_bridge(queries: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ontology_labels = parse_ontology_labels(ONTOLOGY)
    records: list[dict[str, object]] = []
    field_rows: list[dict[str, object]] = []
    rdf_rows: list[dict[str, object]] = []

    field_specs: list[tuple[str, str, Callable[[str, bool], bool], str]] = [
        ("Reference", "identificador técnico asignado por el puente", lambda v, _t: bool(v), "derived_identifier"),
        ("Publication Year", "2021", lambda v, _t: str(v) != "2021", "source_or_default"),
        ("Task", "One step future state forecast si falta evidencia", lambda _v, task: task, "source_or_default"),
        ("Case study", "Not reported/Facts*", lambda v, _t: not generated_text(v), "source"),
        ("Case study type", "Maintainable item", lambda v, _t: normalize(v) != "maintainable item", "source_or_generic"),
        ("Input for the model", "Not reported/Facts*", lambda v, _t: not generated_text(v), "source"),
        ("Number of input variables", "0", lambda v, _t: int(v or 0) > 0, "derived_count"),
        ("Input type", "Not reported/Facts*", lambda v, _t: informative_list(v), "source"),
        ("Data Pre-processing", "no si no hay Design detail", lambda v, _t: normalize(v) == "yes", "derived_from_design_detail"),
        ("Model Approach", "derivado del número de modelos", lambda v, _t: bool(v), "derived_classification"),
        ("Model Type", "Not reported/Facts*", lambda v, _t: informative_list(v), "source"),
        ("Models", "Not reported/Facts*", lambda v, _t: informative_list(v), "source"),
        ("Online/Off-line", "Unknown synchronization", lambda v, _t: normalize(v) != "unknown synchronization", "source_or_default"),
        ("Number of failure modes", "0", lambda v, _t: int(v or 0) > 0, "source_or_default"),
        ("Performance indicator", "Not reported", lambda v, _t: not generated_text(v), "source"),
        ("Performance", "Not reported", lambda v, _t: not generated_text(v), "source"),
        ("Complementary notes", "Not reported", lambda v, _t: not generated_text(v), "source_or_derived"),
        ("Study title", "Untitled/Facts*", lambda v, _t: not generated_text(v), "source"),
        ("Publication identifier", "URN generado", lambda v, _t: bool(v) and not normalize(v).startswith("urn:ontocast:facts:"), "source_or_generated"),
    ]

    per_field_flags: dict[str, list[bool]] = {name: [] for name, *_ in field_specs}
    for item in queries.itertuples(index=False):
        path = ROOT / str(item.facts_file).replace("\\", "/")
        raw = path.read_text(encoding="utf-8")
        rdfstar_blocks = len(re.findall(r"rdf:reifies\s+<<\(", raw))
        graph = load_graph_from_ttl(path)
        task_evidence = explicit_task_evidence(graph)
        cases = graph_to_cases(graph, ontology_labels)
        first = cases_to_csv_rows(cases[:1])[0]
        row: dict[str, object] = {
            "query_index": int(item.query_index),
            "facts_file": str(item.facts_file),
            "case_count": len(cases),
            "additional_cases_not_used": max(0, len(cases) - 1),
            "triples_after_cleanup": len(graph),
            "rdfstar_reification_blocks_removed": rdfstar_blocks,
            "explicit_task_evidence": task_evidence,
        }
        for field, _default, predicate, _kind in field_specs:
            value = first[field]
            flag = bool(predicate(value, task_evidence))
            row[field] = value
            row[f"informative__{field}"] = flag
            per_field_flags[field].append(flag)
        records.append(row)
        namespaces = Counter()
        invalid_typed_literals = 0
        for subject, predicate, obj in graph:
            if isinstance(obj, Literal) and obj.datatype and obj.value is None:
                invalid_typed_literals += 1
            for term in (subject, predicate, obj):
                if isinstance(term, URIRef):
                    text = str(term)
                    if "/OPMAD/seed#" in text:
                        namespaces["OPMAD_seed"] += 1
                    elif "/OPMAD#" in text:
                        namespaces["OPMAD_canonical"] += 1
        rdf_rows.append(
            {
                "query_index": int(item.query_index),
                "facts_file": str(item.facts_file),
                "raw_parse_expected_to_fail_due_rdfstar": rdfstar_blocks > 0,
                "rdfstar_reification_blocks_removed": rdfstar_blocks,
                "triples_after_cleanup": len(graph),
                "invalid_typed_literals": invalid_typed_literals,
                "opmad_canonical_uri_occurrences": namespaces["OPMAD_canonical"],
                "opmad_seed_uri_occurrences": namespaces["OPMAD_seed"],
            }
        )

    for position, (field, default, _predicate, kind) in enumerate(field_specs, start=1):
        informative = sum(per_field_flags[field])
        field_rows.append(
            {
                "column": position,
                "field": field,
                "evidence_kind": kind,
                "bridge_default_or_weak_value": default,
                "n": len(records),
                "informative_n": informative,
                "informative_percent": 100.0 * informative / len(records),
                "default_or_weak_n": len(records) - informative,
                "default_or_weak_percent": 100.0 * (len(records) - informative) / len(records),
            }
        )
    return pd.DataFrame(records), pd.DataFrame(field_rows), pd.DataFrame(rdf_rows)


def audit_normalization(queries: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    fields = [
        "normalized_task",
        "normalized_case_study_type",
        "normalized_case_study",
        "normalized_online_offline",
        "normalized_input_for_model",
        "normalized_input_type",
    ]
    per = queries[["query_index", *fields]].copy()
    for field in fields:
        per[f"active__{field}"] = per[field].astype(str).str.strip().ne("")
    active_cols = [f"active__{field}" for field in fields]
    per["active_content_fields"] = per[active_cols].sum(axis=1)
    per["active_beyond_task"] = per[[col for col in active_cols if col != "active__normalized_task"]].sum(axis=1)
    per["query_information_pattern"] = per[fields].apply(
        lambda row: "+".join(field.removeprefix("normalized_") for field in fields if str(row[field]).strip()) or "year_only",
        axis=1,
    )
    summary_rows = []
    for field in fields:
        n = int(per[f"active__{field}"].sum())
        summary_rows.append(
            {
                "field": field.removeprefix("normalized_"),
                "active_n": n,
                "active_percent": 100.0 * n / len(per),
                "dropped_or_missing_n": len(per) - n,
            }
        )
    patterns = per.groupby("query_information_pattern", as_index=False).size().rename(columns={"size": "n"})
    patterns["percent"] = 100.0 * patterns["n"] / len(per)
    patterns = patterns.sort_values(["n", "query_information_pattern"], ascending=[False, True])
    return per, pd.DataFrame(summary_rows), patterns


def cluster_bootstrap(delta: np.ndarray, groups: pd.Series, *, seed: int) -> tuple[float, float, int, int]:
    frame = pd.DataFrame({"delta": delta, "group": groups.astype(str).to_numpy()})
    agg = frame.groupby("group", sort=False)["delta"].agg(["sum", "count"])
    sums = agg["sum"].to_numpy(float)
    counts = agg["count"].to_numpy(float)
    m = len(agg)
    rng = np.random.default_rng(seed)
    values: list[np.ndarray] = []
    remaining = BOOTSTRAP_RESAMPLES
    while remaining:
        batch = min(500, remaining)
        sampled = rng.integers(0, m, size=(batch, m))
        means = sums[sampled].sum(axis=1) / counts[sampled].sum(axis=1)
        values.append(means)
        remaining -= batch
    samples = np.concatenate(values)
    low, high = np.quantile(samples, [0.025, 0.975])
    return float(low), float(high), m, int(counts.max())


def statistical_audits(queries: pd.DataFrame, per_query: pd.DataFrame, manifest: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    signature_fields = [
        "normalized_task",
        "normalized_case_study_type",
        "normalized_case_study",
        "normalized_online_offline",
        "normalized_input_for_model",
        "normalized_input_type",
    ]
    signatures = queries[signature_fields].fillna("").astype(str).apply(lambda col: col.str.strip().str.lower())
    signature = signatures.agg(" | ".join, axis=1)
    merged = per_query.merge(queries[["query_index"]], on="query_index", validate="one_to_one")
    merged["normalized_signature"] = signature.to_numpy()
    metric_specs = {
        "mean_similarity_top5": ("baseline_mean_similarity", "diverse_mean_similarity"),
        "unique_model_signatures": ("baseline_unique_models", "diverse_unique_models"),
        "intra_list_dissimilarity": ("baseline_intra_list_dissimilarity", "diverse_intra_list_dissimilarity"),
    }
    cluster_rows: list[dict[str, object]] = []
    group_specs = {
        "query": pd.Series(merged["query_index"].astype(str)),
        "normalized_signature": merged["normalized_signature"],
        "baseline_ranking": merged["baseline_refs"],
        "mmr_ranking": merged["diverse_refs"],
    }
    for metric_index, (metric, (base_col, mmr_col)) in enumerate(metric_specs.items()):
        delta = merged[mmr_col].to_numpy(float) - merged[base_col].to_numpy(float)
        for group_index, (unit, groups) in enumerate(group_specs.items()):
            low, high, n_clusters, max_cluster = cluster_bootstrap(delta, groups, seed=SEED + metric_index * 10 + group_index)
            cluster_rows.append(
                {
                    "metric": metric,
                    "resampling_unit": unit,
                    "n_queries": len(delta),
                    "n_clusters": n_clusters,
                    "max_cluster_size": max_cluster,
                    "mean_change": float(delta.mean()),
                    "ci95_low": low,
                    "ci95_high": high,
                    "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
                }
            )

    position_rows: list[dict[str, object]] = []
    transition = Counter()
    delta_rows: list[dict[str, object]] = []
    for item in per_query.itertuples(index=False):
        q = int(item.query_index)
        baseline = read_result_rows(RUN / "cbr_data" / f"pool_results_{q}.csv")[:5]
        diverse = read_result_rows(RUN / "with_diversity" / f"pool_results_{q}.diverse.csv")[:5]
        b_sims = np.array([float(str(row["Sim"]).replace(",", ".")) for row in baseline], dtype=float)
        d_sims = np.array([float(str(row["Sim"]).replace(",", ".")) for row in diverse], dtype=float)
        b_models = [normalize(row.get("Models")) for row in baseline if normalize(row.get("Models"))]
        d_models = [normalize(row.get("Models")) for row in diverse if normalize(row.get("Models"))]
        b_dup = len(b_models) != len(set(b_models))
        d_dup = len(d_models) != len(set(d_models))
        transition[(b_dup, d_dup)] += 1
        position_rows.append(
            {
                "query_index": q,
                "baseline_mean_similarity_positions_2_5": float(b_sims[1:].mean()),
                "mmr_mean_similarity_positions_2_5": float(d_sims[1:].mean()),
                "change_positions_2_5": float(d_sims[1:].mean() - b_sims[1:].mean()),
            }
        )
        delta_rows.append(
            {
                "query_index": q,
                "delta_similarity_top5": float(item.diverse_mean_similarity - item.baseline_mean_similarity),
                "delta_ild": float(item.diverse_intra_list_dissimilarity - item.baseline_intra_list_dissimilarity),
                "delta_unique_signatures": float(item.diverse_unique_models - item.baseline_unique_models),
            }
        )
    positions = pd.DataFrame(position_rows)
    positions_summary = pd.DataFrame(
        [
            {
                "scope": "positions_2_5_top1_excluded",
                "n": len(positions),
                "baseline_mean_similarity": positions["baseline_mean_similarity_positions_2_5"].mean(),
                "mmr_mean_similarity": positions["mmr_mean_similarity_positions_2_5"].mean(),
                "mean_change": positions["change_positions_2_5"].mean(),
                "median_change": positions["change_positions_2_5"].median(),
            }
        ]
    )
    transitions = pd.DataFrame(
        [
            {
                "baseline_has_duplicate": b,
                "mmr_has_duplicate": d,
                "n": transition[(b, d)],
                "percent": 100.0 * transition[(b, d)] / len(per_query),
            }
            for b in (False, True)
            for d in (False, True)
        ]
    )
    deltas = pd.DataFrame(delta_rows)
    quantile_rows = []
    for field in ["delta_similarity_top5", "delta_ild", "delta_unique_signatures"]:
        values = deltas[field]
        quantile_rows.append(
            {
                "metric": field,
                "mean": values.mean(),
                "sd": values.std(ddof=1),
                "min": values.min(),
                "q05": values.quantile(0.05),
                "q25": values.quantile(0.25),
                "median": values.median(),
                "q75": values.quantile(0.75),
                "q95": values.quantile(0.95),
                "max": values.max(),
            }
        )
    return pd.DataFrame(cluster_rows), positions_summary, transitions, pd.DataFrame(quantile_rows)


def subgroup_audits(per_query: pd.DataFrame, manifest: pd.DataFrame, bridge_records: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    linked = manifest.copy()
    linked["query_index"] = pd.to_numeric(linked["query_index"], errors="coerce")
    linked = linked.dropna(subset=["query_index"]).copy()
    linked["query_index"] = linked["query_index"].astype(int)
    linked = linked.sort_values("duplicate_sha256_count").drop_duplicates("query_index", keep="first")
    cols = ["query_index", "actual_model", "chunks", "retry_run_count", "sanitization", "linkage_confidence", "title_match_score"]
    merged = per_query.merge(linked[cols], on="query_index", how="left", validate="one_to_one")
    informative_cols = [col for col in bridge_records.columns if col.startswith("informative__")]
    bridge_summary = bridge_records[["query_index", *informative_cols]].copy()
    bridge_summary["informative_fields_19"] = bridge_summary[informative_cols].sum(axis=1)
    merged = merged.merge(bridge_summary[["query_index", "informative_fields_19"]], on="query_index", validate="one_to_one")
    merged["delta_similarity"] = merged["diverse_mean_similarity"] - merged["baseline_mean_similarity"]
    merged["delta_ild"] = merged["diverse_intra_list_dissimilarity"] - merged["baseline_intra_list_dissimilarity"]
    merged["non_exact_link"] = merged["linkage_confidence"].ne("exact_or_near_exact")

    group_rows: list[dict[str, object]] = []
    for dimension in ["actual_model", "chunks", "retry_run_count", "sanitization", "linkage_confidence"]:
        for value, group in merged.groupby(dimension, dropna=False):
            group_rows.append(
                {
                    "dimension": dimension,
                    "group": str(value),
                    "n": len(group),
                    "mean_informative_fields_19": group["informative_fields_19"].mean(),
                    "baseline_mean_similarity": group["baseline_mean_similarity"].mean(),
                    "mmr_mean_similarity": group["diverse_mean_similarity"].mean(),
                    "mean_similarity_change": group["delta_similarity"].mean(),
                    "baseline_mean_ild": group["baseline_intra_list_dissimilarity"].mean(),
                    "mmr_mean_ild": group["diverse_intra_list_dissimilarity"].mean(),
                    "mean_ild_change": group["delta_ild"].mean(),
                }
            )

    sensitivity_rows = []
    for label, subset in [
        ("all_links", merged),
        ("exact_or_near_exact_only", merged[~merged["non_exact_link"]]),
        ("non_exact_links_only", merged[merged["non_exact_link"]]),
    ]:
        sensitivity_rows.append(
            {
                "scope": label,
                "n": len(subset),
                "mean_similarity_change": subset["delta_similarity"].mean(),
                "mean_ild_change": subset["delta_ild"].mean(),
                "baseline_mean_similarity": subset["baseline_mean_similarity"].mean(),
                "mmr_mean_similarity": subset["diverse_mean_similarity"].mean(),
                "baseline_mean_ild": subset["baseline_intra_list_dissimilarity"].mean(),
                "mmr_mean_ild": subset["diverse_intra_list_dissimilarity"].mean(),
            }
        )
    return pd.DataFrame(group_rows), pd.DataFrame(sensitivity_rows)


def build_expert_validation_template(manifest: pd.DataFrame, bridge_records: pd.DataFrame) -> pd.DataFrame:
    linked = manifest.copy()
    linked["query_index"] = pd.to_numeric(linked["query_index"], errors="coerce")
    linked = linked.dropna(subset=["query_index"]).copy()
    linked["query_index"] = linked["query_index"].astype(int)
    linked = linked.sort_values("duplicate_sha256_count").drop_duplicates("query_index", keep="first")
    candidates = linked.merge(bridge_records, on="query_index", validate="one_to_one")
    candidates["stratum"] = candidates["actual_model"].astype(str) + " | " + candidates["Task"].astype(str)
    sampled = (
        candidates.groupby("stratum", group_keys=False)
        .apply(lambda group: group.sample(n=min(6, len(group)), random_state=SEED), include_groups=False)
        .reset_index(drop=True)
    )
    if len(sampled) > 96:
        sampled = sampled.sample(n=96, random_state=SEED).sort_values("query_index")
    fields = [
        "query_index", "corpus_id", "source_title", "pdf_file", "facts_file_x", "actual_model", "chunks",
        "linkage_confidence", "Task", "Case study", "Input type", "Models", "Study title",
    ]
    existing = [field for field in fields if field in sampled.columns]
    template = sampled[existing].copy()
    template = template.rename(columns={"facts_file_x": "facts_file"})
    for field in ["Task", "Case study", "Input type", "Models", "Study title"]:
        template[f"annotator_1_{field}_correct"] = ""
        template[f"annotator_2_{field}_correct"] = ""
        template[f"adjudicated_{field}"] = ""
    template["annotator_1_notes"] = ""
    template["annotator_2_notes"] = ""
    template["adjudication_notes"] = ""
    return template


def report(field_coverage: pd.DataFrame, norm_summary: pd.DataFrame, cluster: pd.DataFrame, positions: pd.DataFrame, linkage: pd.DataFrame, rdf: pd.DataFrame, bridge: pd.DataFrame) -> str:
    def field(name: str) -> pd.Series:
        return field_coverage[field_coverage["field"] == name].iloc[0]

    active = {row.field: int(row.active_n) for row in norm_summary.itertuples(index=False)}
    cluster_ild = cluster[(cluster["metric"] == "intra_list_dissimilarity") & (cluster["resampling_unit"] == "baseline_ranking")].iloc[0]
    exact = linkage[linkage["scope"] == "exact_or_near_exact_only"].iloc[0]
    lines = [
        "# Auditoría adicional de interoperabilidad y robustez",
        "",
        "Esta auditoría es computacional. Cuantifica cobertura, defaults y sensibilidad, pero no reemplaza una anotación experta de fidelidad factual.",
        "",
        "## Puente RDF--CBR",
        "",
        f"- Se procesaron **{len(bridge):,}** artefactos; todos pudieron parsearse después de la limpieza RDF-star.".replace(",", "."),
        f"- Se retiraron **{int(rdf['rdfstar_reification_blocks_removed'].sum()):,}** bloques de reificación RDF-star; la procedencia a nivel de triple no se conserva en el grafo limpio.".replace(",", "."),
        f"- **{int((bridge['case_count'] > 1).sum())}** artefactos contenían más de un caso y se ignoraron **{int(bridge['additional_cases_not_used'].sum())}** casos adicionales.",
        f"- Sincronización informativa: **{int(field('Online/Off-line')['informative_n'])}/{len(bridge)}**; desempeño: **{int(field('Performance')['informative_n'])}/{len(bridge)}**; modos de falla no cero: **{int(field('Number of failure modes')['informative_n'])}/{len(bridge)}**.",
        "",
        "## Consulta normalizada",
        "",
        f"- Tarea activa: **{active['task']}/{len(bridge)}**; activo: **{active['case_study']}/{len(bridge)}**; variables de entrada: **{active['input_type']}/{len(bridge)}**.",
        f"- Tipo de activo, sincronización e input modality activos: **{active['case_study_type']}**, **{active['online_offline']}** y **{active['input_for_model']}**, respectivamente.",
        "",
        "## Robustez estadística",
        "",
        f"- Al remuestrear patrones de ranking baseline ({int(cluster_ild['n_clusters'])} clústeres), el IC95% del cambio medio de ILD fue [{cluster_ild['ci95_low']:.4f}; {cluster_ild['ci95_high']:.4f}].",
        f"- Excluyendo el top-1 fijado por diseño, la similitud media de las posiciones 2--5 cambió {positions.iloc[0]['mean_change']:.4f}.",
        f"- Al restringir a los {int(exact['n'])} enlaces exactos/casi exactos, el cambio medio de ILD fue {exact['mean_ild_change']:.4f}.",
        "",
        "## Interpretación",
        "",
        "La evidencia sostiene interoperabilidad ejecutable y auditable. La cobertura semántica de varios campos es limitada; por ello, no se afirma interoperabilidad semántica plena, fidelidad factual ni utilidad humana.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    queries = pd.read_csv(QUERIES, sep=";", keep_default_na=False)
    per_query = pd.read_csv(PER_QUERY, sep=";", keep_default_na=False)
    manifest = pd.read_csv(MANIFEST, keep_default_na=False)
    if len(queries) != 1821 or len(per_query) != 1821:
        raise RuntimeError("Expected 1,821 query records")

    bridge, field_coverage, rdf = audit_bridge(queries)
    normalization, norm_summary, patterns = audit_normalization(queries)
    cluster, positions, transitions, quantiles = statistical_audits(queries, per_query, manifest)
    subgroups, linkage = subgroup_audits(per_query, manifest, bridge)
    expert_template = build_expert_validation_template(manifest, bridge)

    outputs = {
        "bridge_per_query.csv": bridge,
        "field_coverage_19cols.csv": field_coverage,
        "rdfstar_cleanup_summary.csv": rdf,
        "query_informativeness_per_query.csv": normalization,
        "normalized_field_coverage.csv": norm_summary,
        "query_information_patterns.csv": patterns,
        "cluster_bootstrap.csv": cluster,
        "positions_2_5_summary.csv": positions,
        "duplicate_transition.csv": transitions,
        "delta_distribution_quantiles.csv": quantiles,
        "extraction_model_batch_effects.csv": subgroups,
        "linkage_confidence_sensitivity.csv": linkage,
        "expert_validation_sample_template.csv": expert_template,
    }
    for name, frame in outputs.items():
        frame.to_csv(OUT / name, index=False, encoding="utf-8")
    (OUT / "AUDIT_REPORT.md").write_text(report(field_coverage, norm_summary, cluster, positions, linkage, rdf, bridge), encoding="utf-8")
    metadata = {
        "seed": SEED,
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "queries": len(queries),
        "input_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in [MANIFEST, QUERIES, PER_QUERY, ONTOLOGY]
        },
        "outputs": list(outputs),
        "human_validation_status": "template_only_not_annotated",
    }
    (OUT / "audit_manifest.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    print((OUT / "AUDIT_REPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
