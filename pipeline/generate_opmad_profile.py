#!/usr/bin/env python3
"""Generate and verify the fixed extraction profile from authoritative OPMAD.

The profile is a deterministic, import-free projection.  OPMAD statements are
copied (never rewritten) from OPMAD.owl.  Small external declarations are
marked as support declarations and do not define or extend OPMAD.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from rdflib import BNode, Graph, Literal, OWL, RDF, RDFS, URIRef
from rdflib.compare import to_canonical_graph
from rdflib.util import guess_format

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.extraction_schema import CCO, OBO, OPMAD, PredictiveMaintenanceCase, TASK_CLASS_IRIS

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    ROOT
    / "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/OPMAD.owl"
)
DEFAULT_OUTPUT = ROOT / "pipeline/seed_ontology/opmad_seed.ttl"
# Updating the authoritative artifact requires an explicit review and source-pin
# update here. The gitlink identifies the upstream tree from which it came;
# the digest pins the exact OPMAD.owl bytes consumed by this generator.
DEFAULT_SOURCE_SUBMODULE_COMMIT = "a17841db47190465536dfef30fdb1527135a8f74"
EXPECTED_DEFAULT_SOURCE_SHA256 = "60cb97d62f1e4bc66d2bdc2eaf45d30422414b51a08c47ee24168aa31acb62ac"
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
RESTRICTION_CLASS_PREDICATES = {
    OWL.onClass,
    OWL.someValuesFrom,
    OWL.allValuesFrom,
}


@dataclass(frozen=True)
class SourceProvenance:
    """Metadata and the immutable byte snapshot to which it applies."""

    path: Path
    display_path: str
    identity: str
    sha256: str
    authoritative: bool
    content: bytes = field(repr=False)


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


def authoritative_declarations(graph: Graph) -> dict[URIRef, frozenset[URIRef]]:
    """Return every authoritative declaration kind, including genuine punning."""

    declarations: dict[URIRef, set[URIRef]] = {}
    for declaration_type in DECLARATION_TYPES:
        for term in graph.subjects(RDF.type, declaration_type):
            if isinstance(term, URIRef) and str(term).startswith(OPMAD):
                declarations.setdefault(term, set()).add(declaration_type)
    return {term: frozenset(kinds) for term, kinds in declarations.items()}


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
    for predicate in RESTRICTION_CLASS_PREDICATES:
        for class_iri in profile.objects(None, predicate):
            if isinstance(class_iri, URIRef) and not str(class_iri).startswith(OPMAD):
                support.setdefault(class_iri, OWL.Class)
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
        actual = frozenset(
            declaration_type
            for declaration_type in profile.objects(term, RDF.type)
            if declaration_type in DECLARATION_TYPES
        )
        if actual != expected:
            raise ValueError(
                f"Profile declaration kinds for {term} do not match authoritative source "
                f"(expected {sorted(map(str, expected))}, found {sorted(map(str, actual))})"
            )


def source_provenance(path: Path, *, allow_custom_source: bool = False) -> SourceProvenance:
    """Read one byte snapshot, validate its identity, and record its digest."""

    resolved = path.expanduser().resolve()
    authoritative = resolved == DEFAULT_SOURCE.resolve()
    if not authoritative and not allow_custom_source:
        raise ValueError(
            f"Custom OPMAD source {resolved} requires --allow-custom-source; "
            "custom output is not authoritative"
        )

    try:
        content = resolved.read_bytes()
    except FileNotFoundError:
        if authoritative:
            raise FileNotFoundError(
                f"Authoritative OPMAD source not found at {DEFAULT_SOURCE}. "
                "Initialize the CBR ontology submodule first."
            ) from None
        raise FileNotFoundError(f"Custom OPMAD source not found at {resolved}") from None

    sha256 = hashlib.sha256(content).hexdigest()
    if authoritative and sha256 != EXPECTED_DEFAULT_SOURCE_SHA256:
        raise ValueError(
            f"Authoritative OPMAD source SHA-256 mismatch at {resolved}: expected "
            f"{EXPECTED_DEFAULT_SOURCE_SHA256}, found {sha256}. Refusing to label "
            "these bytes authoritative; updating OPMAD requires an explicit source-pin update."
        )

    if authoritative:
        display_path = DEFAULT_SOURCE.relative_to(ROOT).as_posix()
        identity = (
            "authoritative CBR ontology submodule OPMAD.owl "
            f"at {DEFAULT_SOURCE_SUBMODULE_COMMIT}"
        )
    else:
        display_path = str(resolved)
        identity = "custom source (not authoritative OPMAD submodule)"
    return SourceProvenance(
        path=resolved,
        display_path=display_path,
        identity=identity,
        sha256=sha256,
        authoritative=authoritative,
        content=content,
    )


def serialize_deterministic(
    graph: Graph,
    provenance: SourceProvenance,
) -> str:
    """Serialize canonical RDF as an N-Triples subset of Turtle."""

    canonical = to_canonical_graph(graph)
    lines = sorted(f"{s.n3()} {p.n3()} {o.n3()} ." for s, p, o in canonical)
    command = "python3 pipeline/generate_opmad_profile.py"
    if not provenance.authoritative:
        command += f" --source {provenance.display_path} --allow-custom-source"
    header = (
        "# GENERATED FILE - DO NOT EDIT.\n"
        f"# Source identity: {provenance.identity}\n"
        f"# Source path: {provenance.display_path}\n"
        f"# Source SHA-256: {provenance.sha256}\n"
        f"# Command: {command}\n"
        "# N-Triples is valid Turtle; full IRIs make namespace auditing explicit.\n\n"
    )
    return header + "\n".join(lines) + "\n"


def load_source(provenance: SourceProvenance) -> Graph:
    """Parse the same immutable bytes used for the provenance digest."""

    try:
        return Graph().parse(
            data=provenance.content,
            format=guess_format(provenance.path.name),
            publicID=provenance.path.as_uri(),
        )
    except Exception as exc:
        detail = str(exc).strip().splitlines()[0] if str(exc).strip() else type(exc).__name__
        raise ValueError(
            f"Could not parse OPMAD source {provenance.path}: {detail}. "
            "Verify that the file contains valid RDF/XML (or RDF matching its extension)."
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--allow-custom-source",
        action="store_true",
        help="explicitly permit a non-authoritative --source and label its output as custom",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="verify the committed profile is current; do not write")
    args = parser.parse_args(argv)

    try:
        provenance = source_provenance(args.source, allow_custom_source=args.allow_custom_source)
        source = load_source(provenance)
        profile = build_profile(source)
        validate_profile(source, profile)
        rendered = serialize_deterministic(profile, provenance)
    except (OSError, ValueError) as exc:
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
