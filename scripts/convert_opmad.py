#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["rdflib==7.6.0"]
# ///
"""Convert OPMAD and its local dependencies to verified Turtle, using local files.

Run: uv run scripts/convert_opmad.py
See ontologies/opmad-ontocast/README.md for provenance and OntoCast usage.
"""

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from io import BytesIO
from pathlib import Path

import rdflib
from rdflib import BNode, Graph, Literal, OWL, RDF, URIRef
from rdflib.compare import to_isomorphic
from rdflib.plugins.serializers.turtle import TurtleSerializer

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = (
    ROOT
    / "external/CBR-Ontology-For-Predictive-Maintenance"
    / "CBR-Ontology/CBRproject/data"
)
OPMAD = URIRef("http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD")
# Use an explicit list so the populated OPMADdatabase.owl never enters the bundle.
SOURCES = (
    "OPMAD.owl",
    "CCOmerged.owl",
    "ArtifactOntology.ttl",
    "EventOntology.ttl",
    "ExtendedRelationOntology.ttl",
    "GeospatialOntology.ttl",
    "InformationEntityOntology.ttl",
    "TimeOntology.ttl",
    "ro-import.ttl",
)
BFO_IMPORTS = (
    "http://purl.obolibrary.org/obo/bfo.owl",
    "http://purl.obolibrary.org/obo/bfo/2019-08-26/bfo.owl",
)


class LosslessTurtleSerializer(TurtleSerializer):
    """Keep literal spelling; RDFLib's numeric shorthand can change it."""

    def label(self, node, position):
        if not isinstance(node, Literal):
            return super().label(node, position)
        # JSON string escapes are also valid Turtle string escapes.
        text = json.dumps(str(node), ensure_ascii=False)
        if node.language:
            return f"{text}@{node.language}"
        if node.datatype is not None:
            return f"{text}^^{node.datatype.n3()}"
        return text


def load_sources(directory: Path) -> tuple[Graph, list[dict], dict[str, str]]:
    merged = Graph()
    records = []
    providers = {}
    for name in SOURCES:
        path = directory / name
        content = path.read_bytes()
        graph = Graph().parse(
            data=content,
            publicID=path.as_uri(),
            format="xml" if path.suffix == ".owl" else "turtle",
        )
        if name == "OPMAD.owl" and set(graph.subjects(RDF.type, OWL.Ontology)) != {OPMAD}:
            raise ValueError("OPMAD.owl must declare the expected OPMAD ontology IRI")
        if name == "CCOmerged.owl":
            bfo_entity = URIRef("http://purl.obolibrary.org/obo/BFO_0000001")
            if (bfo_entity, RDF.type, OWL.Class) not in graph:
                raise ValueError("CCOmerged.owl does not contain the bundled BFO classes")
            # The bundled merged release includes BFO but has no separate BFO header.
            providers.update(dict.fromkeys(BFO_IMPORTS, name))
        for ontology in graph.subjects(RDF.type, OWL.Ontology):
            providers[str(ontology)] = name
            for version in graph.objects(ontology, OWL.versionIRI):
                providers[str(version)] = name
        for prefix, namespace in graph.namespaces():
            merged.bind(prefix, namespace)

        # Blank-node labels belong to one document. Never merge nodes merely
        # because two source files happen to use the same label.
        blank_nodes = {}

        def scoped(node):
            if isinstance(node, BNode):
                if node not in blank_nodes:
                    blank_nodes[node] = BNode()
                return blank_nodes[node]
            return node

        for triple in graph:
            merged.add(tuple(scoped(node) for node in triple))
        records.append(
            {"file": name, "sha256": hashlib.sha256(content).hexdigest(), "triples": len(graph)}
        )

    imports = {str(iri) for iri in merged.objects(None, OWL.imports)}
    unresolved = imports - providers.keys()
    if unresolved:
        raise ValueError("Imports without a local provider: " + ", ".join(sorted(unresolved)))
    merged.bind("opmad", str(OPMAD) + "#")
    return merged, records, {iri: providers[iri] for iri in sorted(imports)}


def rdf_signature(graph: Graph) -> tuple[set, Counter]:
    """Compare fixed terms and the multiset of blank-node connected components.

    IRIs and literals cannot be renamed. Blank-node components joined only by
    those fixed terms can be canonicalized independently. This avoids a very
    slow global search among the repeated axioms in the bundled CCO files.
    """
    neighbors = defaultdict(set)
    for triple in graph:
        nodes = [node for node in triple if isinstance(node, BNode)]
        for node in nodes:
            neighbors[node].update(nodes)
    roots = {}
    for start in neighbors:
        if start in roots:
            continue
        pending = [start]
        while pending:
            node = pending.pop()
            if node in roots:
                continue
            roots[node] = start
            pending.extend(neighbors[node] - roots.keys())

    grounded = set()
    components = defaultdict(Graph)
    for triple in graph:
        node = next((term for term in triple if isinstance(term, BNode)), None)
        if node is None:
            grounded.add(triple)
        else:
            components[roots[node]].add(triple)
    return grounded, Counter(
        to_isomorphic(component).graph_digest() for component in components.values()
    )


def encode_checked(graph: Graph) -> bytes:
    stream = BytesIO()
    LosslessTurtleSerializer(graph).serialize(stream, encoding="utf-8")
    content = stream.getvalue()
    decoded = Graph().parse(data=content, format="turtle")
    if rdf_signature(graph) != rdf_signature(decoded):
        raise ValueError("Turtle round-trip changed the RDF graph; no output was written")
    return content


def convert(source: Path, output: Path) -> None:
    # Keep lexical forms such as "01"^^xsd:integer during both parsing passes.
    rdflib.NORMALIZE_LITERALS = False
    merged, inputs, imports = load_sources(source)
    view = Graph()
    view += merged
    removed = Graph()
    for ontology in set(view.subjects(RDF.type, OWL.Ontology)) - {OPMAD}:
        declaration = (ontology, RDF.type, OWL.Ontology)
        view.remove(declaration)
        removed.add(declaration)

    # Verify the serialization before creating or replacing the output file.
    content = encode_checked(view)
    restored = Graph().parse(data=content, format="turtle")
    # Only these declarations are approved for removal; keep the check in memory.
    restored += removed
    if rdf_signature(merged) != rdf_signature(restored):
        raise ValueError("OntoCast view changed RDF beyond the approved ontology declarations")

    output.mkdir(parents=True, exist_ok=True)
    path = output / "OPMAD-ontocast.ttl"
    path.write_bytes(content)
    print(f"{path}: {len(view):,} triples; round-trip and approved-loss checks passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-dir", type=Path, default=DEFAULT_SOURCE,
        help="CBRproject/data directory (default: bundled CBR repository)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "ontologies/opmad-ontocast",
        help="output directory (default: ontologies/opmad-ontocast under this repository)",
    )
    args = parser.parse_args()
    try:
        convert(args.source_dir.expanduser().resolve(), args.output_dir.expanduser().resolve())
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Conversion failed: {exc}\n")


if __name__ == "__main__":
    main()
