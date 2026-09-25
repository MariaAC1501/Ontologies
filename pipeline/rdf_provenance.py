"""Parse OntoCast RDF 1.2 provenance without dropping quoted triples.

OntoCast writes statement provenance with ``rdf:reifies <<( s p o )>>``.
``rdflib`` cannot parse RDF 1.2 triple terms, so the publication exporter uses
PyOxigraph to parse the complete facts graph. Ordinary triples are projected to
an ``rdflib.Graph`` for the existing review-field logic. Reified statements,
their annotations, and their ``prov:wasDerivedFrom`` targets are retained as
JSON-safe records alongside that graph.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

from rdflib import BNode, Graph, Literal, URIRef

RDF_REIFIES = "http://www.w3.org/1999/02/22-rdf-syntax-ns#reifies"
PROV_WAS_DERIVED_FROM = "http://www.w3.org/ns/prov#wasDerivedFrom"

HANDLING = (
    "RDF 1.2 statement provenance was parsed with PyOxigraph and retained as "
    "source-scoped assertion records. Ordinary RDF triples were projected to "
    "rdflib for review-field extraction."
)


@dataclass(frozen=True)
class ParsedFacts:
    """An ordinary RDF graph and its separately retained RDF 1.2 provenance."""

    graph: Graph
    rdf_star_evidence: dict[str, Any]


def _load_pyoxigraph() -> Any:
    try:
        import pyoxigraph as ox
    except ImportError as error:  # Keep a failed document visible to the caller.
        raise RuntimeError(
            "Publication review export requires pyoxigraph to parse RDF 1.2 "
            "statement provenance. Install the repository requirements."
        ) from error
    return ox


def _term_record(
    term: Any,
    ox: Any,
    blank_node_labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return an RDF-semantic term record that is safe to place in JSON."""

    if isinstance(term, ox.NamedNode):
        return {"term_type": "iri", "value": term.value}
    if isinstance(term, ox.BlankNode):
        value = (blank_node_labels or {}).get(term.value, term.value)
        return {"term_type": "blank_node", "value": value}
    if isinstance(term, ox.Literal):
        datatype = getattr(term, "datatype", None)
        return {
            "term_type": "literal",
            "value": term.value,
            "datatype": datatype.value if datatype is not None else None,
            "language": term.language or None,
        }
    if isinstance(term, ox.Triple):
        return {
            "term_type": "triple",
            "value": {
                "subject": _term_record(term.subject, ox, blank_node_labels),
                "predicate": _term_record(term.predicate, ox, blank_node_labels),
                "object": _term_record(term.object, ox, blank_node_labels),
            },
        }
    raise TypeError(f"Unsupported PyOxigraph RDF term: {term!r}")


def _canonical(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _raw_term_key(term: Any, ox: Any) -> str:
    """Identify a parser term inside this one parse without exposing its bnode ID."""

    return _canonical(_term_record(term, ox))


def _quad_record(
    quad: Any,
    ox: Any,
    blank_node_labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "subject": _term_record(quad.subject, ox, blank_node_labels),
        "predicate": _term_record(quad.predicate, ox, blank_node_labels),
        "object": _term_record(quad.object, ox, blank_node_labels),
    }


def _quad_key(
    quad: Any,
    ox: Any,
    blank_node_labels: dict[str, str] | None = None,
) -> str:
    return _canonical(_quad_record(quad, ox, blank_node_labels))


def _blank_node_ids(term: Any, ox: Any) -> set[str]:
    if isinstance(term, ox.BlankNode):
        return {term.value}
    if isinstance(term, ox.Triple):
        return (
            _blank_node_ids(term.subject, ox)
            | _blank_node_ids(term.predicate, ox)
            | _blank_node_ids(term.object, ox)
        )
    return set()


def _term_signature(
    term: Any,
    labels: dict[str, str],
    self_id: str,
    ox: Any,
) -> str:
    if isinstance(term, ox.NamedNode):
        return f"I:{term.value}"
    if isinstance(term, ox.BlankNode):
        return "SELF" if term.value == self_id else f"B:{labels[term.value]}"
    if isinstance(term, ox.Literal):
        return f"L:{_canonical(_term_record(term, ox))}"
    if isinstance(term, ox.Triple):
        return "T:(%s,%s,%s)" % (
            _term_signature(term.subject, labels, self_id, ox),
            _term_signature(term.predicate, labels, self_id, ox),
            _term_signature(term.object, labels, self_id, ox),
        )
    raise TypeError(f"Unsupported PyOxigraph RDF term: {term!r}")


def _blank_node_labels(quads: list[Any], ox: Any) -> dict[str, str]:
    """Give parser-generated blank nodes repeatable structural labels.

    PyOxigraph deliberately gives blank nodes fresh internal identifiers on each
    parse. A bounded refinement over their incident RDF terms keeps assertion
    records and IDs repeatable without treating source blank-node labels as
    identifiers. The bound avoids quadratic work for one-reifier-per-fact
    graphs.
    """

    contexts_by_node: dict[str, list[Any]] = defaultdict(list)
    for quad in quads:
        node_ids = set().union(*(
            _blank_node_ids(term, ox)
            for term in (quad.subject, quad.predicate, quad.object)
        ))
        for blank_node in node_ids:
            contexts_by_node[blank_node].append(quad)
    ids = sorted(contexts_by_node)
    if not ids:
        return {}
    labels = {blank_node: "blank_node" for blank_node in ids}
    for _ in range(min(len(ids), 4)):
        next_labels: dict[str, str] = {}
        for blank_node in ids:
            contexts = [
                "|".join(
                    (
                        _term_signature(quad.subject, labels, blank_node, ox),
                        _term_signature(quad.predicate, labels, blank_node, ox),
                        _term_signature(quad.object, labels, blank_node, ox),
                    )
                )
                for quad in contexts_by_node[blank_node]
            ]
            next_labels[blank_node] = hashlib.sha256(
                "\n".join(sorted(contexts)).encode("utf-8")
            ).hexdigest()
        labels = next_labels
    return {
        blank_node: f"bnode-{label}"
        for blank_node, label in labels.items()
    }


def _is_reification_quad(quad: Any, ox: Any) -> bool:
    return (
        not isinstance(quad.subject, ox.Triple)
        and isinstance(quad.predicate, ox.NamedNode)
        and quad.predicate.value == RDF_REIFIES
        and isinstance(quad.object, ox.Triple)
    )


def _contains_triple_term(quad: Any, ox: Any) -> bool:
    return any(
        isinstance(term, ox.Triple)
        for term in (quad.subject, quad.predicate, quad.object)
    )


def _annotation_record(
    quad: Any,
    ox: Any,
    blank_node_labels: dict[str, str] | None = None,
) -> dict[str, Any]:
    return {
        "predicate": _term_record(quad.predicate, ox, blank_node_labels),
        "object": _term_record(quad.object, ox, blank_node_labels),
    }


def _ordinary_graph(quads: list[Any], ox: Any) -> Graph:
    """Project triples that rdflib can represent without changing their terms."""

    graph = Graph()
    for quad in quads:
        if _contains_triple_term(quad, ox):
            continue
        graph.add(
            (
                _to_rdflib_term(quad.subject, ox),
                _to_rdflib_term(quad.predicate, ox),
                _to_rdflib_term(quad.object, ox),
            )
        )
    return graph


def _to_rdflib_term(term: Any, ox: Any) -> URIRef | BNode | Literal:
    if isinstance(term, ox.NamedNode):
        return URIRef(term.value)
    if isinstance(term, ox.BlankNode):
        return BNode(term.value)
    if isinstance(term, ox.Literal):
        if term.language:
            return Literal(term.value, lang=term.language)
        datatype = getattr(term, "datatype", None)
        return Literal(term.value, datatype=URIRef(datatype.value) if datatype is not None else None)
    raise TypeError(f"RDF-star term cannot be projected into rdflib: {term!r}")


def _provenance_records(
    quads: list[Any],
    *,
    document_sha256: str,
    ox: Any,
    blank_node_labels: dict[str, str],
) -> dict[str, Any]:
    """Create source-scoped records for OntoCast's RDF 1.2 reification pattern."""

    reification_quads = [quad for quad in quads if _is_reification_quad(quad, ox)]
    reifier_keys = {_raw_term_key(quad.subject, ox) for quad in reification_quads}
    outgoing: dict[str, list[Any]] = defaultdict(list)
    for quad in quads:
        outgoing[_raw_term_key(quad.subject, ox)].append(quad)

    grouped: dict[str, dict[str, Any]] = {}
    for quad in reification_quads:
        triple = _term_record(quad.object, ox, blank_node_labels)
        triple_key = _canonical(triple)
        group = grouped.setdefault(
            triple_key,
            {
                "triple": triple,
                "reifier_keys": set(),
            },
        )
        group["reifier_keys"].add(_raw_term_key(quad.subject, ox))

    assertions: list[dict[str, Any]] = []
    for triple_key, group in grouped.items():
        annotation_by_key: dict[str, dict[str, Any]] = {}
        derived_by_key: dict[str, dict[str, Any]] = {}
        for reifier_key in group["reifier_keys"]:
            for annotation_quad in outgoing[reifier_key]:
                if _is_reification_quad(annotation_quad, ox):
                    continue
                annotation = _annotation_record(annotation_quad, ox, blank_node_labels)
                annotation_by_key[_canonical(annotation)] = annotation
                if (
                    isinstance(annotation_quad.predicate, ox.NamedNode)
                    and annotation_quad.predicate.value == PROV_WAS_DERIVED_FROM
                ):
                    source = _term_record(annotation_quad.object, ox, blank_node_labels)
                    source_key = _canonical(source)
                    raw_source_key = _raw_term_key(annotation_quad.object, ox)
                    metadata_by_key: dict[str, dict[str, Any]] = {}
                    for metadata_quad in outgoing.get(raw_source_key, []):
                        metadata = _annotation_record(
                            metadata_quad,
                            ox,
                            blank_node_labels,
                        )
                        metadata_by_key[_canonical(metadata)] = metadata
                    derived_by_key[source_key] = {
                        "source": source,
                        "metadata": [
                            metadata_by_key[key] for key in sorted(metadata_by_key)
                        ],
                    }
        assertion_id = hashlib.sha256(
            f"{document_sha256}\0{triple_key}".encode("utf-8")
        ).hexdigest()
        assertions.append(
            {
                "assertion_id": assertion_id,
                "triple": group["triple"],
                "reifier_count": len(group["reifier_keys"]),
                "annotations": [annotation_by_key[key] for key in sorted(annotation_by_key)],
                "derived_from": [derived_by_key[key] for key in sorted(derived_by_key)],
            }
        )

    # RDF-star terms outside OntoCast's rdf:reifies pattern remain visible even
    # when they cannot be represented in the ordinary rdflib projection.
    unprojected_by_key: dict[str, dict[str, Any]] = {}
    for quad in quads:
        if not _contains_triple_term(quad, ox) or _is_reification_quad(quad, ox):
            continue
        if _raw_term_key(quad.subject, ox) in reifier_keys:
            # These annotations are retained on their matching assertion above.
            continue
        record = _quad_record(quad, ox, blank_node_labels)
        unprojected_by_key[_canonical(record)] = record

    assertions.sort(key=lambda assertion: assertion["assertion_id"])
    return {
        "statement_count": len(reification_quads),
        "assertion_count": len(assertions),
        "parser": "pyoxigraph",
        "handling": HANDLING,
        "assertions": assertions,
        "unprojected_rdf_star_quads": [
            unprojected_by_key[key] for key in sorted(unprojected_by_key)
        ],
    }


def parse_turtle_with_provenance(
    text: str,
    *,
    document_sha256: str,
    base_iri: str | None = None,
) -> ParsedFacts:
    """Parse a facts Turtle document and retain its RDF 1.2 provenance.

    ``document_sha256`` scopes assertion IDs to the exact facts bytes.
    ``base_iri`` preserves relative-IRI resolution when a caller needs
    it, although publication facts are expected to use absolute IRIs.
    """

    ox = _load_pyoxigraph()
    store = ox.Store()
    store.load(
        input=text,
        format=ox.RdfFormat.TURTLE,
        base_iri=base_iri,
    )
    quads = list(store)
    blank_node_labels = _blank_node_labels(quads, ox)
    quads.sort(key=lambda quad: _quad_key(quad, ox, blank_node_labels))
    return ParsedFacts(
        graph=_ordinary_graph(quads, ox),
        rdf_star_evidence=_provenance_records(
            quads,
            document_sha256=document_sha256,
            ox=ox,
            blank_node_labels=blank_node_labels,
        ),
    )


def unparsed_rdf_star_evidence(text: str | None) -> dict[str, Any]:
    """Describe an input whose RDF could not be parsed without claiming retention."""

    statement_count = len(
        re.findall(
            r"(?:[A-Za-z_][\w.-]*:reifies|<http://www\.w3\.org/1999/02/22-rdf-syntax-ns#reifies>)\s+<<\(",
            text or "",
        )
    )
    return {
        "statement_count": statement_count,
        "assertion_count": 0,
        "parser": "not_parsed",
        "handling": (
            "The source graph could not be parsed, so RDF 1.2 provenance was "
            "not projected. The original facts path and digest identify the "
            "untouched source bytes."
        ),
        "assertions": [],
        "unprojected_rdf_star_quads": [],
    }
