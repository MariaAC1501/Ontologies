#!/usr/bin/env python3
"""Generate and verify the fixed extraction profile from authoritative OPMAD.

The profile is a deterministic, import-free projection.  OPMAD statements are
copied (never rewritten) from OPMAD.owl.  Small external declarations are
marked as support declarations and do not define or extend OPMAD.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterable

from rdflib import BNode, Graph, Literal, OWL, RDF, RDFS, URIRef
from rdflib.compare import to_canonical_graph

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.extraction_schema import CCO, OBO, OPMAD, PredictiveMaintenanceCase, TASK_CLASS_IRIS

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT
    / "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl"
)
DEFAULT_OUTPUT = ROOT / "pipeline/seed_ontology/opmad_seed.ttl"
ONTOLOGY_IRI = URIRef(OPMAD.removesuffix("#"))
OPMAD_BASE = str(ONTOLOGY_IRI)
LEGACY_SEED_NAMESPACE = f"{OPMAD_BASE}/seed#"
DECLARATION_TYPES = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty}
SCHEMA_IRI_PATTERN = re.compile(
    rf"(?:{re.escape(OPMAD)}|{re.escape(CCO)}|{re.escape(OBO)})[A-Za-z0-9_]+"
)
BUILTIN_NAMESPACES = (
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://www.w3.org/2002/07/owl#",
)
SUPPORT_COMMENT = (
    "Support declaration only. The term is defined by an external ontology "
    "imported by authoritative OPMAD or is an external extraction relation; "
    "this profile does not redefine it."
)
def _string_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _string_values(item)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _string_values(item)


def schema_iris() -> set[URIRef]:
    """Return all ontology IRIs explicitly carried by extraction metadata."""

    values: set[str] = set(TASK_CLASS_IRIS.values())
    for field in PredictiveMaintenanceCase.model_fields.values():
        values.update(_string_values(field.json_schema_extra or {}))
    # Include prose references too, so documentation cannot silently drift from
    # metadata. These are the three domain namespaces used by the schema.
    for text in _string_values(PredictiveMaintenanceCase.model_json_schema()):
        values.update(SCHEMA_IRI_PATTERN.findall(text))
    return {URIRef(value) for value in values if value.startswith("http")}


def schema_external_declarations() -> dict[URIRef, URIRef]:
    """Classify non-OPMAD extraction relations without guessing their axioms."""

    result: dict[URIRef, URIRef] = {}
    for field in PredictiveMaintenanceCase.model_fields.values():
        extra = field.json_schema_extra or {}
        for key, value in extra.items():
            if not isinstance(value, str) or value.startswith(OPMAD) or not value.startswith("http"):
                continue
            if key.endswith("data_property_iri"):
                result[URIRef(value)] = OWL.DatatypeProperty
            elif key.endswith("object_property_iri"):
                result[URIRef(value)] = OWL.ObjectProperty
    return result


def authoritative_declarations(graph: Graph) -> dict[URIRef, URIRef]:
    declarations: dict[URIRef, URIRef] = {}
    for declaration_type in DECLARATION_TYPES:
        for term in graph.subjects(RDF.type, declaration_type):
            if isinstance(term, URIRef) and str(term).startswith(OPMAD):
                declarations[term] = declaration_type
    return declarations


def _copy_subject_closure(source: Graph, roots: set[URIRef]) -> Graph:
    """Copy complete descriptions, blank-node axioms, and OPMAD dependencies."""

    output = Graph()
    seen: set[URIRef | BNode] = set()
    pending: list[URIRef | BNode] = sorted(roots, key=str, reverse=True)
    while pending:
        subject = pending.pop()
        if subject in seen:
            continue
        seen.add(subject)
        for triple in source.triples((subject, None, None)):
            output.add(triple)
            obj = triple[2]
            if isinstance(obj, BNode) and obj not in seen:
                pending.append(obj)
            elif isinstance(obj, URIRef) and str(obj).startswith(OPMAD) and obj not in seen:
                pending.append(obj)
    return output


def _external_support_declarations(profile: Graph) -> dict[URIRef, URIRef]:
    """Infer only the declaration kind needed to parse copied OPMAD structure."""

    support = schema_external_declarations()
    for subject, obj in profile.subject_objects(RDFS.subClassOf):
        if isinstance(obj, URIRef) and not str(obj).startswith(OPMAD):
            support.setdefault(obj, OWL.Class)
    for subject, obj in profile.subject_objects(RDFS.subPropertyOf):
        if not isinstance(obj, URIRef) or str(obj).startswith(OPMAD):
            continue
        subject_types = set(profile.objects(subject, RDF.type))
        declaration = OWL.DatatypeProperty if OWL.DatatypeProperty in subject_types else OWL.ObjectProperty
        support.setdefault(obj, declaration)
    for restriction, prop in profile.subject_objects(OWL.onProperty):
        if not isinstance(prop, URIRef) or str(prop).startswith(OPMAD):
            continue
        # OPMAD's external restriction properties in this projection are object
        # properties. Schema-provided declarations above take precedence.
        support.setdefault(prop, OWL.ObjectProperty)
    return {
        term: declaration
        for term, declaration in support.items()
        if not str(term).startswith(BUILTIN_NAMESPACES)
    }


def build_profile(source: Graph) -> Graph:
    declarations = authoritative_declarations(source)
    required_opmad = {term for term in schema_iris() if str(term).startswith(OPMAD)}
    missing = sorted(required_opmad - declarations.keys(), key=str)
    if missing:
        raise ValueError(
            "Extraction schema uses undeclared authoritative OPMAD term(s): "
            + ", ".join(map(str, missing))
        )

    profile = _copy_subject_closure(source, required_opmad)
    ontology_declaration = (ONTOLOGY_IRI, RDF.type, OWL.Ontology)
    if ontology_declaration not in source:
        raise ValueError(f"Authoritative source does not declare expected ontology IRI {ONTOLOGY_IRI}")
    profile.add(ontology_declaration)

    for term, declaration_type in sorted(_external_support_declarations(profile).items(), key=lambda item: str(item[0])):
        profile.add((term, RDF.type, declaration_type))
        profile.add((term, RDFS.comment, Literal(SUPPORT_COMMENT, lang="en")))
    return profile


def validate_profile(source: Graph, profile: Graph) -> None:
    """Reject namespace drift and OPMAD vocabulary not declared by the source."""

    declarations = authoritative_declarations(source)
    required_opmad = {term for term in schema_iris() if str(term).startswith(OPMAD)}
    missing_schema = sorted(required_opmad - declarations.keys(), key=str)
    if missing_schema:
        raise ValueError("Schema OPMAD terms absent from authoritative ontology: " + ", ".join(map(str, missing_schema)))

    profile_opmad = {
        node
        for triple in profile
        for node in triple
        if isinstance(node, URIRef) and str(node).startswith(OPMAD)
    }
    unauthorized = sorted(profile_opmad - declarations.keys(), key=str)
    if unauthorized:
        raise ValueError("Unauthorized OPMAD IRI(s) in profile: " + ", ".join(map(str, unauthorized)))

    missing_profile = sorted(required_opmad - profile_opmad, key=str)
    if missing_profile:
        raise ValueError("Schema OPMAD term(s) missing from profile: " + ", ".join(map(str, missing_profile)))

    all_iris = {str(node) for triple in profile for node in triple if isinstance(node, URIRef)}
    drifted = sorted(
        iri
        for iri in all_iris
        if iri.startswith(f"{OPMAD_BASE}/") and iri != OPMAD_BASE
    )
    if drifted:
        raise ValueError("Non-authoritative OPMAD domain namespace is forbidden: " + ", ".join(drifted))

    for term in profile_opmad:
        expected = declarations[term]
        if (term, RDF.type, expected) not in profile:
            raise ValueError(f"Profile does not preserve authoritative declaration for {term}")


def serialize_deterministic(graph: Graph) -> str:
    """Serialize canonical RDF as an N-Triples subset of Turtle."""

    canonical = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in canonical)
    header = (
        "# GENERATED FILE - DO NOT EDIT.\n"
        "# Source: external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl\n"
        "# Command: python3 pipeline/generate_opmad_profile.py\n"
        "# N-Triples is valid Turtle; full IRIs make namespace auditing explicit.\n\n"
    )
    return header + "\n".join(lines) + "\n"


def load_source(path: Path) -> Graph:
    if not path.is_file():
        raise FileNotFoundError(
            f"Authoritative OPMAD source not found at {path}. Initialize the CBR ontology submodule first."
        )
    return Graph().parse(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="verify the committed profile is current; do not write")
    args = parser.parse_args(argv)

    try:
        source = load_source(args.source)
        profile = build_profile(source)
        validate_profile(source, profile)
        rendered = serialize_deterministic(profile)
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")

    if args.check:
        if not args.output.is_file():
            parser.exit(1, f"error: generated profile is missing: {args.output}\n")
        if args.output.read_text(encoding="utf-8") != rendered:
            parser.exit(1, f"error: {args.output} is stale; run python3 pipeline/generate_opmad_profile.py\n")
        print(f"Verified {args.output} ({len(profile)} triples)")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"Generated {args.output} ({len(profile)} triples)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
