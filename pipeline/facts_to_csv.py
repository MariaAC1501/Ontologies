#!/usr/bin/env python3
"""Convert OntoCast facts Turtle output into the 19-column CBR CSV format.

Sample invocation:
    .tmp-ontocast-test/bin/python3 pipeline/facts_to_csv.py \
      --facts pipeline/test_output/facts_5cc89b5bfaf6.ttl \
      --ontology pipeline/seed_ontology/opmad_seed.ttl \
      --output pipeline/test_output/extracted_cases.csv

Notes:
- OntoCast facts may use either the OPMAD `#` namespace or the `OPMAD/seed#`
  namespace.
- OntoCast facts currently contain RDF-star reification statements that stock
  rdflib cannot parse. This script strips those statements before parsing.
- Missing fields are filled with conservative defaults so the output still
  validates against `pipeline.extraction_schema.PredictiveMaintenanceCase`.
"""

from __future__ import annotations

import argparse
import csv
import glob
import re
from collections import defaultdict
from pathlib import Path
import sys
from typing import Iterable
from urllib.parse import urldefrag

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from pipeline.extraction_schema import PredictiveMaintenanceCase, TASK_CLASS_IRIS
except ImportError:
    from .extraction_schema import PredictiveMaintenanceCase, TASK_CLASS_IRIS

SCHEMA = Namespace("http://schema.org/")
SCHEMA_ALT = Namespace("https://schema.org/")
CCO = Namespace("http://www.ontologyrepository.com/CommonCoreOntologies/")

DEFAULT_PUBLICATION_YEAR = 2021
DEFAULT_PUBLICATION_IDENTIFIER_PREFIX = "urn:ontocast:facts:"
DEFAULT_TASK_FOR_FUTURE_STATE_FORECAST = "One step future state forecast"

HEADERS = [
    PredictiveMaintenanceCase.CSV_HEADERS[field]
    for field in (
        "reference",
        "publication_year",
        "task",
        "case_study",
        "case_study_type",
        "input_for_model",
        "number_of_input_variables",
        "input_types",
        "data_preprocessing",
        "model_approach",
        "model_types",
        "models",
        "module_synchronization",
        "number_of_failure_modes",
        "performance_indicator",
        "performance",
        "complementary_notes",
        "study_title",
        "publication_identifier",
    )
]


def local_name(term: URIRef | str | None) -> str:
    if term is None:
        return ""
    value = str(term)
    value, fragment = urldefrag(value)
    if fragment:
        return fragment
    return value.rstrip("/").rsplit("/", 1)[-1]


def strip_rdf_star_statements(text: str) -> str:
    cleaned = re.sub(
        r"(?ms)^_:[^\n]*rdf:reifies <<\([^\n]*>>\s*;\s*\n\s*prov:wasDerivedFrom [^\n]*\.\s*\n?",
        "",
        text,
    )
    cleaned = re.sub(r"(?m)^_:[^\n]*\s+prov:wasDerivedFrom [^\n]*\.\s*\n?", "", cleaned)
    return cleaned if cleaned.endswith("\n") else cleaned + "\n"


def load_graph_from_ttl(path: Path) -> Graph:
    text = path.read_text(encoding="utf-8")
    graph = Graph()
    graph.parse(data=strip_rdf_star_statements(text), format="turtle")
    return graph


def expand_fact_paths(patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        matches = [Path(match) for match in glob.glob(pattern)]
        if matches:
            paths.extend(matches)
        else:
            maybe_path = Path(pattern)
            if maybe_path.exists():
                paths.append(maybe_path)
    unique = sorted({path.resolve() for path in paths})
    return [Path(path) for path in unique]


def literal_text(graph: Graph, subject: URIRef, *predicates: URIRef) -> list[str]:
    values: list[str] = []
    for predicate in predicates:
        for obj in graph.objects(subject, predicate):
            if isinstance(obj, Literal):
                text = str(obj).strip()
                if text:
                    values.append(text)
    return values


def entity_labels(graph: Graph, subject: URIRef) -> list[str]:
    labels = literal_text(graph, subject, SCHEMA.name, SCHEMA_ALT.name, RDFS.label)
    unique: list[str] = []
    for label in labels:
        if label not in unique:
            unique.append(label)
    if unique:
        return sorted(unique, key=lambda value: (len(value), value.lower()))
    fallback = local_name(subject)
    return [fallback] if fallback else []


def best_label(graph: Graph, subject: URIRef | None, default: str = "") -> str:
    if subject is None:
        return default
    labels = entity_labels(graph, subject)
    return labels[0] if labels else default


def join_multi(values: Iterable[str]) -> str:
    unique: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    return ", ".join(unique)


def parse_ontology_labels(ontology_path: Path | None) -> dict[str, str]:
    if ontology_path is None or not ontology_path.exists():
        return {}
    graph = load_graph_from_ttl(ontology_path)
    labels: dict[str, str] = {}
    for subject in set(graph.subjects(RDFS.label, None)):
        name = local_name(subject)
        label = best_label(graph, subject)
        if name and label:
            labels[name] = label
    return labels


def typed_entities(graph: Graph) -> dict[str, set[URIRef]]:
    entities: dict[str, set[URIRef]] = defaultdict(set)
    for subject, _, class_iri in graph.triples((None, RDF.type, None)):
        if isinstance(subject, URIRef) and isinstance(class_iri, URIRef):
            entities[local_name(class_iri)].add(subject)
    return entities


def find_publication_year(graph: Graph, article: URIRef | None) -> int:
    candidates: list[str] = []
    if article is not None:
        candidates.extend(literal_text(graph, article, SCHEMA.datePublished, SCHEMA_ALT.datePublished))
        candidates.extend(literal_text(graph, article, SCHEMA.identifier, SCHEMA_ALT.identifier))
        candidates.extend(literal_text(graph, article, SCHEMA.name, SCHEMA_ALT.name))
    year_pattern = re.compile(r"\b(19\d{2}|20\d{2}|2100)\b")
    for value in candidates:
        match = year_pattern.search(value)
        if match:
            return int(match.group(1))
    return DEFAULT_PUBLICATION_YEAR


def choose_task(
    graph: Graph,
    entities_by_type: dict[str, set[URIRef]],
    ontology_labels: dict[str, str],
) -> str:
    direct_types = [name for name in entities_by_type if name in {local_name(uri) for uri in TASK_CLASS_IRIS.values()}]
    if direct_types:
        label = ontology_labels.get(direct_types[0], direct_types[0].replace("_", " "))
        if label in TASK_CLASS_IRIS:
            return label

    describes_type_predicates = [
        URIRef("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#describes_type"),
        URIRef("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD/seed#describes_type"),
    ]
    for predicate in describes_type_predicates:
        for _, _, obj in graph.triples((None, predicate, None)):
            type_name = local_name(obj)
            label = ontology_labels.get(type_name, type_name.replace("_", " "))
            if label in TASK_CLASS_IRIS:
                return label
            if type_name == "Future_state_forecast":
                return DEFAULT_TASK_FOR_FUTURE_STATE_FORECAST

    return DEFAULT_TASK_FOR_FUTURE_STATE_FORECAST


def choose_input_record(graph: Graph) -> tuple[str, list[URIRef]]:
    actions = set(graph.subjects(RDF.type, SCHEMA.Action)) | set(graph.subjects(RDF.type, SCHEMA_ALT.Action))
    for action in sorted(actions, key=str):
        instruments = [obj for obj in graph.objects(action, SCHEMA.instrument)] + [obj for obj in graph.objects(action, SCHEMA_ALT.instrument)]
        if instruments:
            return best_label(graph, action, "Not reported"), [obj for obj in instruments if isinstance(obj, URIRef)]
    return "Not reported", []


def choose_model_types(
    graph: Graph,
    model_entities: Iterable[URIRef],
    ontology_labels: dict[str, str],
) -> list[str]:
    values: list[str] = []
    for model in model_entities:
        for obj in list(graph.objects(model, SCHEMA.object)) + list(graph.objects(model, SCHEMA_ALT.object)):
            if isinstance(obj, URIRef):
                values.extend(entity_labels(graph, obj))
        for _, _, class_iri in graph.triples((model, RDF.type, None)):
            if isinstance(class_iri, URIRef):
                class_name = local_name(class_iri)
                if class_name not in {"Predictive_maintenance_model", "Thing"}:
                    label = ontology_labels.get(class_name, class_name.replace("_", " "))
                    values.append(label)
    return [value for value in dict.fromkeys(values) if value]


def choose_publication_identifier(graph: Graph, article: URIRef | None) -> str:
    if article is not None:
        identifiers = literal_text(graph, article, SCHEMA.identifier, SCHEMA_ALT.identifier)
        if identifiers:
            return identifiers[0]
        article_name = local_name(article)
        if article_name:
            return f"{DEFAULT_PUBLICATION_IDENTIFIER_PREFIX}{article_name}"
    return f"{DEFAULT_PUBLICATION_IDENTIFIER_PREFIX}unknown"


def build_complementary_notes(
    graph: Graph,
    article: URIRef | None,
    design_details: list[str],
    instruments: list[str],
) -> str:
    parts: list[str] = []
    if article is not None:
        keywords = literal_text(graph, article, SCHEMA.keywords, SCHEMA_ALT.keywords)
        if keywords:
            parts.append(f"Keywords: {keywords[0]}")
    if design_details:
        parts.append(f"Design details: {join_multi(design_details)}")
    if instruments:
        parts.append(f"Instruments: {join_multi(instruments)}")
    return "; ".join(parts) if parts else "Not reported"


def graph_to_cases(graph: Graph, ontology_labels: dict[str, str]) -> list[PredictiveMaintenanceCase]:
    entities_by_type = typed_entities(graph)

    articles = sorted(entities_by_type.get("Predictive_Maintenance_Article", set()), key=str)
    if not articles:
        articles = [None]

    maintainable_items = sorted(entities_by_type.get("Maintainable_item", set()), key=str)
    case_study = best_label(graph, maintainable_items[0], "Not reported") if maintainable_items else "Not reported"
    case_study_type = ontology_labels.get("Maintainable_item", "Maintainable item")

    input_for_model, instrument_entities = choose_input_record(graph)
    instruments = [best_label(graph, entity) for entity in instrument_entities]

    data_variables = sorted(entities_by_type.get("Data_variable", set()), key=str)
    input_types = [best_label(graph, entity) for entity in data_variables]
    if not input_types:
        input_types = ["Not reported"]

    model_entities = sorted(entities_by_type.get("Predictive_maintenance_model", set()), key=str)
    model_labels = [best_label(graph, entity) for entity in model_entities] or ["Not reported"]
    model_types = choose_model_types(graph, model_entities, ontology_labels) or ["Not reported"]

    design_detail_entities = sorted(entities_by_type.get("Design_detail", set()), key=str)
    design_details = [best_label(graph, entity) for entity in design_detail_entities]

    task = choose_task(graph, entities_by_type, ontology_labels)
    module_synchronization = "Unknown synchronization"
    data_preprocessing = bool(design_details)
    model_approach = "Multi model" if len(model_labels) > 1 else "Single model"

    cases: list[PredictiveMaintenanceCase] = []
    for index, article in enumerate(articles, start=1):
        study_title = best_label(graph, article, "Untitled extracted case") if article is not None else "Untitled extracted case"
        case = PredictiveMaintenanceCase(
            reference=index,
            publication_year=find_publication_year(graph, article),
            task=task,
            case_study=case_study,
            case_study_type=case_study_type,
            input_for_model=input_for_model,
            number_of_input_variables=len([value for value in input_types if value != "Not reported"]),
            input_types=input_types,
            data_preprocessing=data_preprocessing,
            model_approach=model_approach,
            model_types=model_types,
            models=model_labels,
            module_synchronization=module_synchronization,
            number_of_failure_modes=0,
            performance_indicator="Not reported",
            performance="Not reported",
            complementary_notes=build_complementary_notes(graph, article, design_details, instruments),
            study_title=study_title,
            publication_identifier=choose_publication_identifier(graph, article),
        )
        cases.append(case)
    return cases


def cases_to_csv_rows(cases: Iterable[PredictiveMaintenanceCase]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for case in cases:
        rows.append(
            {
                "Reference": str(case.reference),
                "Publication Year": str(case.publication_year),
                "Task": case.task,
                "Case study": case.case_study,
                "Case study type": case.case_study_type,
                "Input for the model": case.input_for_model,
                "Number of input variables": str(case.number_of_input_variables),
                "Input type": join_multi(case.input_types),
                "Data Pre-processing": "yes" if case.data_preprocessing else "no",
                "Model Approach": case.model_approach,
                "Model Type": join_multi(case.model_types),
                "Models": join_multi(case.models),
                "Online/Off-line": case.module_synchronization,
                "Number of failure modes": str(case.number_of_failure_modes),
                "Performance indicator": case.performance_indicator,
                "Performance": case.performance,
                "Complementary notes": case.complementary_notes,
                "Study title": case.study_title,
                "Publication identifier": case.publication_identifier,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def build_cases_from_fact_files(fact_paths: Iterable[Path], ontology_path: Path | None = None) -> list[PredictiveMaintenanceCase]:
    combined = Graph()
    for fact_path in fact_paths:
        combined += load_graph_from_ttl(fact_path)
    ontology_labels = parse_ontology_labels(ontology_path)
    return graph_to_cases(combined, ontology_labels)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--facts", nargs="+", required=True, help="Fact TTL path(s) or glob pattern(s)")
    parser.add_argument("--ontology", help="Optional ontology TTL path used for label lookups")
    parser.add_argument("--output", required=True, help="Output CSV path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fact_paths = expand_fact_paths(args.facts)
    if not fact_paths:
        raise SystemExit("No fact files matched --facts input")
    ontology_path = Path(args.ontology) if args.ontology else None
    cases = build_cases_from_fact_files(fact_paths, ontology_path)
    rows = cases_to_csv_rows(cases)
    write_csv(Path(args.output), rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
