#!/usr/bin/env python3
"""Export nullable, evidence-preserving review records from OntoCast facts.

Unlike :mod:`pipeline.facts_to_csv`, this command is an analytical export.  It
never fills values required only by the legacy CBR CSV and never combines input
RDF graphs.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Sequence

from rdflib import Graph, Literal, RDF, RDFS, URIRef

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from pipeline.extraction_schema import OPMAD, TASK_CLASS_IRIS
    from pipeline.facts_to_csv import local_name, strip_rdf_star_statements
except ImportError:
    from .extraction_schema import OPMAD, TASK_CLASS_IRIS
    from .facts_to_csv import local_name, strip_rdf_star_statements

SCHEMA_VERSION = "strict-review-export/1.0"
STATUSES = ("present", "not_reported", "unclear", "not_applicable", "extraction_failure")

SCHEMA_NAMES = (
    URIRef("http://schema.org/name"),
    URIRef("https://schema.org/name"),
)
SCHEMA_IDENTIFIERS = (
    URIRef("http://schema.org/identifier"),
    URIRef("https://schema.org/identifier"),
)
SCHEMA_DATES = (
    URIRef("http://schema.org/datePublished"),
    URIRef("https://schema.org/datePublished"),
)
SCHEMA_VALUES = (
    URIRef("http://schema.org/value"),
    URIRef("https://schema.org/value"),
)
ARTICLE_CLASS = "Predictive_Maintenance_Article"
CASE_CLASS = "Predictive_maintenance_case"
TASK_LABELS = {local_name(iri): label for label, iri in TASK_CLASS_IRIS.items()}
# Authoritative OPMAD is preferred.  The old generated seed namespace remains
# accepted so existing fixed-mode artifacts can still be reviewed, but an
# unrelated ontology cannot opt in merely by reusing an OPMAD local name.
ACCEPTED_OPMAD_CLASS_PREFIXES = (
    OPMAD,
    f"{OPMAD.removesuffix('#')}/seed#",
)

# Every traversable relation is identified by its complete IRI.  Local-name
# matching here would let an unrelated vocabulary attach arbitrary nodes to a
# case (for example evil:has_input).  The OPMAD list is the set of object
# properties in the unchanged ontology; the historical seed namespace carries
# the same terms for compatibility with old fixed-mode artifacts.
OPMAD_RELATION_NAMES = {
    "describes_configuration", "describes_type", "explained_in", "explains",
    "has_design_detail", "has_identifier", "has_predictive_maintenance_function",
    "has_publication_year", "has_synchronization", "has_title", "implies",
    "is_implied_by", "is_predictive_maintenance_function_of", "type_described_by",
}
OPMAD_RELATIONS = frozenset(
    URIRef(f"{namespace}{name}")
    for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
    for name in OPMAD_RELATION_NAMES
)
SCHEMA_RELATION_NAMES = {
    "about", "subjectOf", "object", "instrument", "monitors", "uses",
    "usedIn", "usedFor", "isPartOf", "hasPart",
}
SCHEMA_RELATIONS = frozenset(
    URIRef(f"{namespace}{name}")
    for namespace in ("http://schema.org/", "https://schema.org/")
    for name in SCHEMA_RELATION_NAMES
)
CCO_RELATIONS = frozenset(
    URIRef(f"http://www.ontologyrepository.com/CommonCoreOntologies/{name}")
    for name in ("described_by", "describes", "designates", "is_about")
)
OBO_RELATIONS = frozenset(
    URIRef(f"http://purl.obolibrary.org/obo/{name}")
    for name in (
        "BFO_0000051", "RO_0000079", "RO_0000085", "RO_0000086",
        "RO_0010001", "RO_0010002",
    )
)
DOMAIN_RELATIONS = OPMAD_RELATIONS | SCHEMA_RELATIONS | CCO_RELATIONS | OBO_RELATIONS
OPMAD_TEXT_PREDICATES = tuple(
    URIRef(f"{namespace}has_text_value") for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
)
OPMAD_INTEGER_PREDICATES = tuple(
    URIRef(f"{namespace}has_interger_value") for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
)
OPMAD_TITLE_RELATIONS = tuple(
    URIRef(f"{namespace}has_title") for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
)
OPMAD_IDENTIFIER_RELATIONS = tuple(
    URIRef(f"{namespace}has_identifier") for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
)
OPMAD_PUBLICATION_YEAR_RELATIONS = tuple(
    URIRef(f"{namespace}has_publication_year") for namespace in ACCEPTED_OPMAD_CLASS_PREFIXES
)
CCO_CASE_TARGET_RELATIONS = frozenset({
    URIRef("http://www.ontologyrepository.com/CommonCoreOntologies/designates"),
    URIRef("http://www.ontologyrepository.com/CommonCoreOntologies/is_about"),
})

ANALYTICAL_FIELDS = (
    "publication_year", "task", "case_study", "case_study_type",
    "input_for_model", "number_of_input_variables", "input_types",
    "data_preprocessing", "model_approach", "model_types", "models",
    "module_synchronization", "number_of_failure_modes",
    "performance_indicator", "performance", "complementary_notes",
    "study_title", "publication_identifier",
)


def _field(
    status: str,
    value: Any = None,
    *,
    raw_values: Iterable[str] = (),
    source_nodes: Iterable[str] = (),
    note: str | None = None,
) -> dict[str, Any]:
    if status not in STATUSES:
        raise ValueError(f"Unknown review-export status: {status}")
    result: dict[str, Any] = {
        "status": status,
        "value": value,
        "raw_values": list(dict.fromkeys(str(value) for value in raw_values)),
        "source_nodes": list(dict.fromkeys(str(value) for value in source_nodes)),
    }
    if note:
        result["note"] = note
    return result


def _literals(graph: Graph, subject: URIRef, predicates: Sequence[URIRef] = ()) -> list[Literal]:
    values: list[Literal] = []
    if predicates:
        for predicate in predicates:
            values.extend(obj for obj in graph.objects(subject, predicate) if isinstance(obj, Literal))
    else:
        for predicate in OPMAD_TEXT_PREDICATES:
            values.extend(obj for obj in graph.objects(subject, predicate) if isinstance(obj, Literal))
    return values


def _entity_literals(graph: Graph, entity: URIRef) -> list[Literal]:
    return _literals(graph, entity, (*SCHEMA_NAMES, RDFS.label)) + _literals(graph, entity)


def _clean_literals(values: Iterable[Literal]) -> list[str]:
    return list(dict.fromkeys(text for value in values if (text := str(value).strip())))


def _typed_entities(graph: Graph) -> dict[str, set[URIRef]]:
    result: dict[str, set[URIRef]] = defaultdict(set)
    for subject, class_iri in graph.subject_objects(RDF.type):
        if (
            isinstance(subject, URIRef)
            and isinstance(class_iri, URIRef)
            and str(class_iri).startswith(ACCEPTED_OPMAD_CLASS_PREFIXES)
        ):
            result[local_name(class_iri)].add(subject)
    return result


def _is_domain_relation(predicate: URIRef) -> bool:
    return predicate in DOMAIN_RELATIONS


def _adjacent_domain_nodes(graph: Graph, node: URIRef) -> set[URIRef]:
    adjacent: set[URIRef] = set()
    for predicate, obj in graph.predicate_objects(node):
        if isinstance(predicate, URIRef) and isinstance(obj, URIRef) and _is_domain_relation(predicate):
            adjacent.add(obj)
    for subject, predicate in graph.subject_predicates(node):
        if isinstance(subject, URIRef) and isinstance(predicate, URIRef) and _is_domain_relation(predicate):
            adjacent.add(subject)
    return adjacent


def _case_record_scopes(
    graph: Graph,
    cases: set[URIRef],
    articles: set[URIRef],
) -> tuple[dict[URIRef, set[URIRef]], dict[URIRef, set[URIRef]]]:
    """Partition bounded case neighborhoods and expose unsafe shared nodes.

    Direct case targets are boundary roots.  A traversal cannot enter another
    case's root, even by walking backwards through a shared input or metric.
    Nodes still reachable from more than one case are removed from every scope
    and reported as ambiguous rather than assigned to every record.
    """

    root_owners: dict[URIRef, set[URIRef]] = defaultdict(set)
    for case in cases:
        for node in _adjacent_domain_nodes(graph, case) - cases - articles:
            root_owners[node].add(case)

    shared_roots = {node for node, owners in root_owners.items() if len(owners) > 1}

    def traverse(case: URIRef, barriers: set[URIRef]) -> tuple[set[URIRef], set[URIRef]]:
        seen = {case}
        encountered_barriers: set[URIRef] = set()
        queue: deque[tuple[URIRef, int]] = deque([(case, 0)])
        while queue:
            node, depth = queue.popleft()
            if depth >= 3:
                continue
            for other in _adjacent_domain_nodes(graph, node):
                if other in articles or (other in cases and other != case):
                    continue
                owners = root_owners.get(other, set())
                if owners and case not in owners:
                    continue
                if other in barriers:
                    encountered_barriers.add(other)
                    continue
                if other not in seen:
                    seen.add(other)
                    queue.append((other, depth + 1))
        return seen, encountered_barriers

    provisional = {case: traverse(case, shared_roots)[0] for case in cases}
    reached_by: dict[URIRef, set[URIRef]] = defaultdict(set)
    for case, nodes in provisional.items():
        for node in nodes - {case}:
            reached_by[node].add(case)
    shared_nodes = shared_roots | {node for node, owners in reached_by.items() if len(owners) > 1}

    # Traverse again with every discovered overlap as a barrier.  This prevents
    # a uniquely reachable descendant beyond a shared node from being retained
    # merely because the other case hit the depth limit first.
    scopes: dict[URIRef, set[URIRef]] = {}
    ambiguities: dict[URIRef, set[URIRef]] = {}
    for case in cases:
        scopes[case], ambiguities[case] = traverse(case, shared_nodes)
    return scopes, ambiguities


def _article_only_scope(
    graph: Graph,
    article: URIRef,
    cases: set[URIRef],
    articles: set[URIRef],
) -> set[URIRef]:
    """Traverse an article only when doing so cannot consume case-owned roots."""

    claimed_roots = set().union(*(_adjacent_domain_nodes(graph, case) for case in cases)) if cases else set()
    seen = {article}
    queue: deque[tuple[URIRef, int]] = deque([(article, 0)])
    while queue:
        node, depth = queue.popleft()
        if depth >= 3:
            continue
        for other in _adjacent_domain_nodes(graph, node):
            if other in cases or (other in articles and other != article) or other in claimed_roots:
                continue
            if other not in seen:
                seen.add(other)
                queue.append((other, depth + 1))
    return seen


def _direct_relation_evidence(graph: Graph, left: URIRef, right: URIRef) -> list[str]:
    evidence: list[str] = []
    for subject, predicate, obj in graph.triples((left, None, right)):
        if isinstance(predicate, URIRef) and _is_domain_relation(predicate):
            evidence.append(f"{subject} {predicate} {obj}")
    for subject, predicate, obj in graph.triples((right, None, left)):
        if isinstance(predicate, URIRef) and _is_domain_relation(predicate):
            evidence.append(f"{subject} {predicate} {obj}")
    return evidence


def _article_case_evidence(graph: Graph, article: URIRef, case: URIRef) -> list[str]:
    evidence = _direct_relation_evidence(graph, article, case)
    case_targets = {
        obj for predicate, obj in graph.predicate_objects(case)
        if isinstance(obj, URIRef) and predicate in CCO_CASE_TARGET_RELATIONS
    }
    for target in sorted(case_targets, key=str):
        for predicate in graph.predicates(article, target):
            if isinstance(predicate, URIRef) and _is_domain_relation(predicate):
                evidence.append(f"{case} -> {target} <- {article} (shared explicit target)")
                break
    return list(dict.fromkeys(evidence))


def _case_contexts(
    graph: Graph,
    entities: dict[str, set[URIRef]],
) -> list[tuple[URIRef | None, URIRef | None, dict[str, Any]]]:
    articles = sorted(entities.get(ARTICLE_CLASS, set()), key=str)
    cases = sorted(entities.get(CASE_CLASS, set()), key=str)
    if not cases:
        if articles:
            return [
                (article, None, {
                    "status": "not_reported", "resolution": "unresolved",
                    "evidence": [], "note": "No predictive-maintenance case is asserted in this source graph.",
                })
                for article in articles
            ]
        return [(None, None, {
            "status": "not_reported", "resolution": "unresolved", "evidence": [],
            "note": "Neither an article nor a predictive-maintenance case is asserted.",
        })]

    contexts: list[tuple[URIRef | None, URIRef | None, dict[str, Any]]] = []
    assigned_articles: set[URIRef] = set()
    for case in cases:
        matches: list[tuple[URIRef, list[str]]] = []
        for article in articles:
            evidence = _article_case_evidence(graph, article, case)
            if evidence:
                matches.append((article, evidence))
        if len(matches) == 1:
            article, evidence = matches[0]
            assigned_articles.add(article)
            contexts.append((article, case, {
                "status": "present", "resolution": "resolved", "evidence": evidence,
            }))
        elif len(matches) > 1:
            contexts.append((None, case, {
                "status": "unclear", "resolution": "ambiguous",
                "candidate_article_iris": [str(article) for article, _ in matches],
                "evidence": [item for _, items in matches for item in items],
                "note": "More than one article has explicit RDF linkage to this case; none was selected.",
            }))
        else:
            contexts.append((None, case, {
                "status": "unclear" if articles else "not_applicable", "resolution": "unresolved",
                "candidate_article_iris": [str(article) for article in articles], "evidence": [],
                "note": "The RDF does not establish an article link for this case; no article was guessed.",
            }))

    # Do not silently drop an article merely because cases also occur in the graph.
    for article in articles:
        if article not in assigned_articles:
            contexts.append((article, None, {
                "status": "unclear", "resolution": "unresolved", "evidence": [],
                "note": "This article is not unambiguously linked to a detected case.",
            }))
    return contexts


def _candidate_field(
    graph: Graph,
    entities: dict[str, set[URIRef]],
    scope: set[URIRef],
    ambiguous_scope: set[URIRef],
    class_names: set[str],
    *,
    multi: bool = False,
) -> dict[str, Any]:
    all_candidates = set().union(*(entities.get(name, set()) for name in class_names))
    selected = sorted(all_candidates & scope, key=str)
    ambiguous = sorted(all_candidates & ambiguous_scope, key=str)
    unlinked = sorted(all_candidates - scope - ambiguous_scope, key=str)
    if ambiguous:
        relevant = selected + ambiguous
        raw = list(dict.fromkeys(
            value for node in relevant for value in _clean_literals(_entity_literals(graph, node))
        ))
        return _field(
            "unclear", raw_values=raw, source_nodes=map(str, relevant),
            note="Candidate RDF crosses case boundaries; no value was assigned.",
        )
    if not selected:
        if unlinked:
            return _field(
                "unclear",
                note="Candidate RDF exists elsewhere in this document but is not linked to this record; it was not assigned.",
            )
        return _field("not_reported")

    raw = list(dict.fromkeys(value for node in selected for value in _clean_literals(_entity_literals(graph, node))))
    if not raw:
        return _field(
            "unclear", source_nodes=map(str, selected),
            note="Linked RDF entities have no usable lexical value.",
        )
    if multi:
        return _field("present", raw, raw_values=raw, source_nodes=map(str, selected))
    if len(raw) == 1:
        return _field("present", raw[0], raw_values=raw, source_nodes=map(str, selected))
    return _field(
        "unclear", raw_values=raw, source_nodes=map(str, selected),
        note="Conflicting or multiple values are present for a scalar field; none was selected.",
    )


def _article_text_field(
    graph: Graph,
    article: URIRef | None,
    direct_predicates: Sequence[URIRef],
    linked_predicates: Sequence[URIRef],
) -> dict[str, Any]:
    if article is None:
        return _field("not_applicable", note="This field requires a resolved article.")
    raw = _clean_literals(_literals(graph, article, direct_predicates))
    nodes: list[str] = [str(article)] if raw else []
    for predicate in linked_predicates:
        for obj in graph.objects(article, predicate):
            if isinstance(obj, URIRef):
                raw.extend(_clean_literals(_entity_literals(graph, obj)))
                nodes.append(str(obj))
    raw = list(dict.fromkeys(raw))
    if not raw:
        return _field("not_reported")
    if len(raw) == 1:
        return _field("present", raw[0], raw_values=raw, source_nodes=nodes)
    return _field("unclear", raw_values=raw, source_nodes=nodes, note="Multiple distinct article values were extracted.")


def _publication_year(graph: Graph, article: URIRef | None) -> dict[str, Any]:
    if article is None:
        return _field("not_applicable", note="Publication year requires a resolved article.")
    literals = _literals(graph, article, SCHEMA_DATES)
    nodes = [str(article)] if literals else []
    for predicate in OPMAD_PUBLICATION_YEAR_RELATIONS:
        for obj in graph.objects(article, predicate):
            if isinstance(obj, URIRef):
                nodes.append(str(obj))
                literals.extend(_literals(graph, obj, OPMAD_INTEGER_PREDICATES))
    raw = _clean_literals(literals)
    if not raw:
        return _field("not_reported")
    years: list[int] = []
    invalid: list[str] = []
    for value in raw:
        match = re.match(r"^(19\d{2}|20\d{2}|2100)(?:\D|$)", value)
        if match:
            years.append(int(match.group(1)))
        else:
            invalid.append(value)
    unique = list(dict.fromkeys(years))
    if invalid:
        return _field(
            "extraction_failure", raw_values=raw, source_nodes=nodes,
            note="An asserted publication-year value could not be normalized.",
        )
    if len(unique) == 1:
        return _field("present", unique[0], raw_values=raw, source_nodes=nodes)
    return _field("unclear", raw_values=raw, source_nodes=nodes, note="Conflicting publication years were asserted.")


def _numeric_field(
    graph: Graph,
    entities: dict[str, set[URIRef]],
    scope: set[URIRef],
    ambiguous_scope: set[URIRef],
    class_name: str,
) -> dict[str, Any]:
    candidates = entities.get(class_name, set())
    selected = sorted(candidates & scope, key=str)
    ambiguous = sorted(candidates & ambiguous_scope, key=str)
    unlinked = sorted(candidates - scope - ambiguous_scope, key=str)
    if ambiguous:
        relevant = selected + ambiguous
        raw = [
            str(value) for node in relevant
            for value in _literals(graph, node, OPMAD_INTEGER_PREDICATES)
        ]
        return _field(
            "unclear", raw_values=raw, source_nodes=map(str, relevant),
            note="A numeric fact crosses case boundaries; no count was assigned.",
        )
    if not selected:
        if unlinked:
            return _field(
                "unclear",
                note="A numeric fact exists elsewhere in this document but is not linked to this record; zero was not imputed.",
            )
        return _field("not_reported")
    literals = [
        value for node in selected
        for value in _literals(graph, node, (*OPMAD_INTEGER_PREDICATES, *SCHEMA_VALUES))
    ]
    raw = _clean_literals(literals)
    if not raw:
        return _field("unclear", source_nodes=map(str, selected), note="A linked count entity has no integer value.")
    numbers: list[int] = []
    for value in raw:
        try:
            number = int(value)
        except ValueError:
            return _field("extraction_failure", raw_values=raw, source_nodes=map(str, selected), note="Count is not an integer.")
        if number < 0:
            return _field("extraction_failure", raw_values=raw, source_nodes=map(str, selected), note="Count is negative.")
        numbers.append(number)
    unique = list(dict.fromkeys(numbers))
    if len(unique) == 1:
        return _field("present", unique[0], raw_values=raw, source_nodes=map(str, selected))
    return _field("unclear", raw_values=raw, source_nodes=map(str, selected), note="Conflicting counts were asserted.")


def _task_field(
    graph: Graph,
    entities: dict[str, set[URIRef]],
    scope: set[URIRef],
    ambiguous_scope: set[URIRef],
) -> dict[str, Any]:
    selected: list[tuple[URIRef, str]] = []
    ambiguous: list[tuple[URIRef, str]] = []
    for class_name, label in TASK_LABELS.items():
        selected.extend((node, label) for node in entities.get(class_name, set()) if node in scope)
        ambiguous.extend((node, label) for node in entities.get(class_name, set()) if node in ambiguous_scope)
    if ambiguous:
        relevant = sorted(selected + ambiguous, key=lambda item: str(item[0]))
        return _field(
            "unclear", raw_values=[label for _, label in relevant], source_nodes=[str(node) for node, _ in relevant],
            note="Task evidence crosses case boundaries; no task was assigned.",
        )
    values = list(dict.fromkeys(label for _, label in sorted(selected, key=lambda item: str(item[0]))))
    if len(values) == 1:
        return _field("present", values[0], raw_values=[local_name(node) for node, _ in selected], source_nodes=[str(node) for node, _ in selected])
    if len(values) > 1:
        return _field("unclear", raw_values=values, source_nodes=[str(node) for node, _ in selected], note="Multiple task classes are linked to this record.")

    all_task_nodes = set().union(*(entities.get(name, set()) for name in TASK_LABELS))
    broad = entities.get("Future_state_forecast", set()) & scope
    ambiguous_broad = entities.get("Future_state_forecast", set()) & ambiguous_scope
    if ambiguous_broad:
        return _field(
            "unclear", raw_values=["Future_state_forecast"],
            source_nodes=map(str, sorted(ambiguous_broad, key=str)),
            note="Forecast evidence crosses case boundaries; no task was assigned.",
        )
    if broad:
        return _field(
            "unclear", raw_values=["Future_state_forecast"], source_nodes=map(str, sorted(broad, key=str)),
            note="The RDF does not say whether the forecast is one-step or multiple-step; no task was imputed.",
        )
    if all_task_nodes:
        return _field(
            "unclear",
            note="Task facts exist elsewhere in this document but are not linked to this record.",
        )
    return _field("not_reported")


def _build_fields(
    graph: Graph,
    entities: dict[str, set[URIRef]],
    scope: set[URIRef],
    ambiguous_scope: set[URIRef],
    article: URIRef | None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    fields: dict[str, dict[str, Any]] = {
        "publication_year": _publication_year(graph, article),
        "task": _task_field(graph, entities, scope, ambiguous_scope),
        "case_study": _candidate_field(graph, entities, scope, ambiguous_scope, {"Maintainable_item"}),
        "case_study_type": _candidate_field(graph, entities, scope, ambiguous_scope, {"item_type"}),
        "input_for_model": _candidate_field(graph, entities, scope, ambiguous_scope, {"maintainable_item_record"}),
        "number_of_input_variables": _numeric_field(
            graph, entities, scope, ambiguous_scope, "number_if_input_variables",
        ),
        "input_types": _candidate_field(graph, entities, scope, ambiguous_scope, {"Data_variable"}, multi=True),
        # Unchanged OPMAD has no dedicated preprocessing boolean property.
        # Unsupported minted predicates are ignored rather than normalized.
        "data_preprocessing": _field("not_reported"),
        "model_approach": _candidate_field(graph, entities, scope, ambiguous_scope, {"Model_configuration"}),
        "model_types": _candidate_field(graph, entities, scope, ambiguous_scope, {"Model_type"}, multi=True),
        "models": _candidate_field(
            graph, entities, scope, ambiguous_scope, {"Predictive_maintenance_model"}, multi=True,
        ),
        "module_synchronization": _candidate_field(
            graph, entities, scope, ambiguous_scope, {"Module_synchronization"},
        ),
        "number_of_failure_modes": _numeric_field(
            graph, entities, scope, ambiguous_scope, "Number_of_failure_modes",
        ),
        "performance_indicator": _candidate_field(
            graph, entities, scope, ambiguous_scope, {"Performance_indicator"}, multi=True,
        ),
        "performance": _candidate_field(
            graph, entities, scope, ambiguous_scope, {"Performance_value"}, multi=True,
        ),
        "complementary_notes": _field("not_reported"),
        "study_title": _article_text_field(graph, article, SCHEMA_NAMES, OPMAD_TITLE_RELATIONS),
        "publication_identifier": _article_text_field(
            graph, article, SCHEMA_IDENTIFIERS, OPMAD_IDENTIFIER_RELATIONS,
        ),
    }
    assert tuple(fields) == ANALYTICAL_FIELDS

    design_details = _candidate_field(
        graph, entities, scope, ambiguous_scope, {"Design_detail"}, multi=True,
    )
    if design_details["status"] == "present":
        fields["data_preprocessing"] = _field(
            "unclear",
            raw_values=design_details["raw_values"],
            source_nodes=design_details["source_nodes"],
            note="Design_detail evidence is preserved below but does not establish that preprocessing occurred.",
        ) if fields["data_preprocessing"]["status"] == "not_reported" else fields["data_preprocessing"]
    supplementary = {
        "design_details": design_details,
        "keywords": _article_text_field(
            graph,
            article,
            (URIRef("http://schema.org/keywords"), URIRef("https://schema.org/keywords")),
            (),
        ),
    }
    return fields, supplementary


def _source_identity(path: Path) -> str:
    normalized_path = str(path.expanduser().resolve(strict=False))
    return hashlib.sha256(normalized_path.encode("utf-8")).hexdigest()[:24]


def _source_metadata(path: Path, data: bytes | None, text: str | None, parse_status: str) -> dict[str, Any]:
    digest = hashlib.sha256(data).hexdigest() if data is not None else None
    rdf_star_count = len(
        re.findall(r"(?:[A-Za-z_][\w.-]*:reifies|<[^>]*[/#]reifies>)\s+<<\(", text or "")
    )
    return {
        "facts_filename": path.name,
        "facts_path": str(path),
        "source_identity": _source_identity(path),
        "document_id": digest,
        "sha256": digest,
        "parse_status": parse_status,
        "rdf_star_evidence": {
            "statement_count": rdf_star_count,
            "handling": (
                "RDF-star annotations are not interpreted by this exporter. The original source path and digest are "
                "retained; asserted base triples are parsed after annotations are removed."
            ),
        },
    }


def _record_id(
    source_digest: str | None,
    source_identity: str,
    article: URIRef | None,
    case: URIRef | None,
    ordinal: int,
) -> str:
    material = "|".join(
        (source_digest or "unreadable", source_identity, str(article or ""), str(case or ""), str(ordinal))
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def graph_to_review_records(graph: Graph, path: Path, source: dict[str, Any]) -> list[dict[str, Any]]:
    entities = _typed_entities(graph)
    articles = entities.get(ARTICLE_CLASS, set())
    cases = entities.get(CASE_CLASS, set())
    case_scopes, case_ambiguities = _case_record_scopes(graph, cases, articles)
    contexts = _case_contexts(graph, entities)
    records: list[dict[str, Any]] = []
    for ordinal, (article, case, link) in enumerate(contexts, start=1):
        if case is not None:
            scope = case_scopes[case]
            ambiguous_scope = case_ambiguities[case]
        elif article is not None:
            scope = _article_only_scope(graph, article, cases, articles)
            ambiguous_scope = set()
        else:
            scope = set()
            ambiguous_scope = set()
        fields, supplementary = _build_fields(graph, entities, scope, ambiguous_scope, article)
        has_field_failure = any(field["status"] == "extraction_failure" for field in fields.values())
        record_status = (
            "extraction_failure" if has_field_failure
            else "present" if link["resolution"] == "resolved"
            else "unclear"
        )
        records.append({
            "schema_version": SCHEMA_VERSION,
            "record_id": _record_id(
                source.get("sha256"), source["source_identity"], article, case, ordinal,
            ),
            "record_status": record_status,
            "source_document": source,
            "article_identity": _field(
                "present" if article is not None else ("unclear" if articles else "not_applicable"),
                str(article) if article is not None else None,
                source_nodes=[str(article)] if article is not None else [],
            ),
            "case_identity": _field(
                "present" if case is not None else "not_reported",
                str(case) if case is not None else None,
                source_nodes=[str(case)] if case is not None else [],
            ),
            "case_article_link": link,
            "fields": fields,
            "supplementary_evidence": supplementary,
        })
    return records


def _failure_record(path: Path, data: bytes | None, text: str | None, error: Exception) -> dict[str, Any]:
    source = _source_metadata(path, data, text, "extraction_failure")
    failed_fields = {
        name: _field("extraction_failure", note="The source graph could not be parsed; no value was fabricated.")
        for name in ANALYTICAL_FIELDS
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "record_id": _record_id(source.get("sha256"), source["source_identity"], None, None, 1),
        "record_status": "extraction_failure",
        "source_document": source,
        "article_identity": _field("extraction_failure"),
        "case_identity": _field("extraction_failure"),
        "case_article_link": {
            "status": "extraction_failure", "resolution": "unresolved", "evidence": [],
            "note": "Source graph parsing failed.",
        },
        "fields": failed_fields,
        "supplementary_evidence": {},
        "error": {"type": type(error).__name__, "message": str(error)},
    }


def build_review_records(fact_paths: Iterable[Path]) -> list[dict[str, Any]]:
    """Build records one input graph at a time, retaining parse failures as records."""

    records: list[dict[str, Any]] = []
    for input_path in fact_paths:
        path = Path(input_path)
        data: bytes | None = None
        text: str | None = None
        try:
            data = path.read_bytes()
            text = data.decode("utf-8")
            graph = Graph()
            graph.parse(data=strip_rdf_star_statements(text), format="turtle")
            source = _source_metadata(path, data, text, "present")
            records.extend(graph_to_review_records(graph, path, source))
        except Exception as error:  # A batch export must preserve the failed document as data.
            records.append(_failure_record(path, data, text, error))
    return records


def write_review_records(path: Path, records: Sequence[dict[str, Any]], output_format: str = "jsonl") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        if output_format == "json":
            json.dump(list(records), handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        else:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _expand_review_inputs(patterns: Iterable[str]) -> tuple[list[Path], list[dict[str, Any]]]:
    """Expand review inputs without the legacy helper's missing-path omission.

    Literal arguments are always returned, including missing paths, so normal
    document failure handling emits a record.  An unmatched glob gets its own
    explicit failure record.
    """

    paths: list[Path] = []
    failures: list[dict[str, Any]] = []
    for pattern in patterns:
        literal_path = Path(pattern)
        if literal_path.exists():
            paths.append(literal_path)
        elif glob.has_magic(pattern):
            matches = sorted(Path(match).resolve() for match in glob.glob(pattern))
            if matches:
                paths.extend(matches)
            else:
                error = FileNotFoundError(f"No fact files matched glob pattern: {pattern}")
                failures.append(_failure_record(Path(pattern), None, None, error))
        else:
            paths.append(literal_path)
    return paths, failures


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--facts", nargs="+", required=True, help="Fact TTL path(s) or glob pattern(s)")
    parser.add_argument("--output", required=True, help="Output .jsonl or .json path")
    parser.add_argument("--format", choices=("jsonl", "json"), help="Defaults to json for .json output, otherwise jsonl")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    paths, input_failures = _expand_review_inputs(args.facts)
    records = build_review_records(paths)
    records.extend(input_failures)
    output_format = args.format or ("json" if Path(args.output).suffix.lower() == ".json" else "jsonl")
    write_review_records(Path(args.output), records, output_format)
    return 2 if any(record["record_status"] == "extraction_failure" for record in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
