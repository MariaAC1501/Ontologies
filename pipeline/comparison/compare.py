#!/usr/bin/env python3
"""Side-by-side comparison of fixed OPMAD vs evolved ontology extraction.

Loads facts (and optionally ontology) from both extraction modes and computes
structured metrics: triple counts, class coverage, entity overlap, and
unique entities per mode.

Sample invocation:
    python pipeline/comparison/compare.py \
      --fixed-facts pipeline/test_output/facts_*.ttl \
      --evolved-facts pipeline/full_mode/test_output/facts_*.ttl \
      --evolved-ontology pipeline/full_mode/test_output/ontology_*.ttl \
      --seed-ontology pipeline/seed_ontology/opmad_seed.ttl \
      --output pipeline/comparison/COMPARISON_RESULTS.md
"""

from __future__ import annotations

import argparse
import glob
import re
import sys
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_rdf_star_statements(text: str) -> str:
    cleaned = re.sub(
        r"(?ms)^_:[^\n]*rdf:reifies <<\([^\n]*>>\s*;\s*\n\s*prov:wasDerivedFrom [^\n]*\.\s*\n?",
        "",
        text,
    )
    cleaned = re.sub(r"(?m)^_:[^\n]*\s+prov:wasDerivedFrom [^\n]*\.\s*\n?", "", cleaned)
    return cleaned if cleaned.endswith("\n") else cleaned + "\n"


def load_graph(paths: list[Path]) -> Graph:
    g = Graph()
    for p in paths:
        text = p.read_text(encoding="utf-8")
        g.parse(data=strip_rdf_star_statements(text), format="turtle")
    return g


def resolve_globs(patterns: list[str]) -> list[Path]:
    paths = []
    for pattern in patterns:
        expanded = glob.glob(pattern)
        paths.extend(Path(p) for p in sorted(expanded))
    return paths


def local_name(uri: str) -> str:
    """Extract local name from a URI."""
    if "#" in uri:
        return uri.rsplit("#", 1)[-1]
    return uri.rstrip("/").rsplit("/", 1)[-1]


# Skip infrastructure/meta classes
SKIP_PREFIXES = (
    "http://www.w3.org/",
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/ns/prov#",
)


def is_domain_class(uri: str) -> bool:
    return not any(uri.startswith(p) for p in SKIP_PREFIXES)


def extract_metrics(g: Graph, label: str) -> dict:
    """Extract structured metrics from a graph."""
    all_classes = set()
    domain_classes = set()
    instances = set()
    properties = set()
    named_entities = {}  # local_name -> set of types

    for s, p, o in g:
        properties.add(str(p))
        if p == RDF.type:
            cls = str(o)
            all_classes.add(cls)
            if is_domain_class(cls):
                domain_classes.add(cls)
                inst = str(s)
                instances.add(inst)
                name = local_name(inst)
                if name not in named_entities:
                    named_entities[name] = set()
                named_entities[name].add(local_name(cls))

    # Get labels for entities
    entity_labels = {}
    for s, p, o in g.triples((None, RDFS.label, None)):
        entity_labels[str(s)] = str(o)
    for s, p, o in g:
        ns = "http://schema.org/name"
        if str(p) in (ns, "https://schema.org/name"):
            entity_labels[str(s)] = str(o)

    return {
        "label": label,
        "triples": len(g),
        "all_classes": all_classes,
        "domain_classes": domain_classes,
        "instances": instances,
        "properties": properties,
        "named_entities": named_entities,
        "entity_labels": entity_labels,
    }


def generate_report(
    fixed: dict,
    evolved: dict,
    seed_classes: set[str] | None = None,
) -> str:
    """Generate a markdown comparison report."""
    lines = [
        "# Comparison: Fixed OPMAD vs Evolved Ontology Extraction",
        "",
        "## Summary Metrics",
        "",
        "| Metric | Fixed OPMAD | Evolved Ontology |",
        "|--------|------------|------------------|",
        f"| Total triples | {fixed['triples']} | {evolved['triples']} |",
        f"| Domain classes used | {len(fixed['domain_classes'])} | {len(evolved['domain_classes'])} |",
        f"| Instances extracted | {len(fixed['instances'])} | {len(evolved['instances'])} |",
        f"| Unique properties | {len(fixed['properties'])} | {len(evolved['properties'])} |",
        f"| Named entities | {len(fixed['named_entities'])} | {len(evolved['named_entities'])} |",
        "",
    ]

    # Classes
    lines.extend([
        "## Domain Classes",
        "",
        "### Fixed OPMAD classes",
        "",
    ])
    for cls in sorted(fixed["domain_classes"]):
        lines.append(f"- `{local_name(cls)}`")

    lines.extend(["", "### Evolved ontology classes", ""])
    for cls in sorted(evolved["domain_classes"]):
        lines.append(f"- `{local_name(cls)}`")

    # Entity overlap
    fixed_names = set(fixed["named_entities"].keys())
    evolved_names = set(evolved["named_entities"].keys())
    overlap = fixed_names & evolved_names
    only_fixed = fixed_names - evolved_names
    only_evolved = evolved_names - fixed_names

    lines.extend([
        "",
        "## Entity Overlap Analysis",
        "",
        f"- Entities found by **both**: {len(overlap)}",
        f"- Entities **only in fixed OPMAD**: {len(only_fixed)}",
        f"- Entities **only in evolved ontology**: {len(only_evolved)}",
        "",
    ])

    if overlap:
        lines.extend(["### Entities found by both", ""])
        for name in sorted(overlap):
            ftypes = ", ".join(sorted(fixed["named_entities"][name]))
            etypes = ", ".join(sorted(evolved["named_entities"][name]))
            lines.append(f"- **{name}**: fixed=`{ftypes}` / evolved=`{etypes}`")
        lines.append("")

    if only_fixed:
        lines.extend(["### Entities only in fixed OPMAD extraction", ""])
        for name in sorted(only_fixed):
            types = ", ".join(sorted(fixed["named_entities"][name]))
            lines.append(f"- `{name}` ({types})")
        lines.append("")

    if only_evolved:
        lines.extend(["### Entities only in evolved ontology extraction", ""])
        for name in sorted(only_evolved):
            types = ", ".join(sorted(evolved["named_entities"][name]))
            lines.append(f"- `{name}` ({types})")
        lines.append("")

    # Seed ontology coverage (if provided)
    if seed_classes:
        seed_names = {local_name(c) for c in seed_classes}
        evolved_class_names = {local_name(c) for c in evolved["domain_classes"]}
        seed_covered = seed_names & evolved_class_names
        seed_missed = seed_names - evolved_class_names
        evolved_novel = evolved_class_names - seed_names

        lines.extend([
            "## Seed Ontology Coverage",
            "",
            f"- OPMAD seed classes: {len(seed_names)}",
            f"- Covered by evolved ontology: {len(seed_covered)}",
            f"- Missed by evolved ontology: {len(seed_missed)}",
            f"- Novel classes in evolved: {len(evolved_novel)}",
            "",
        ])
        if seed_missed:
            lines.extend(["### OPMAD classes not discovered by evolution", ""])
            for name in sorted(seed_missed):
                lines.append(f"- `{name}`")
            lines.append("")

        if evolved_novel:
            lines.extend(["### Novel classes discovered by evolution (not in OPMAD)", ""])
            for name in sorted(evolved_novel):
                lines.append(f"- `{name}`")
            lines.append("")

    lines.extend([
        "## Interpretation",
        "",
        "This comparison was generated automatically from the extraction outputs.",
        "See `pipeline/comparison/compare.py` for methodology.",
        "",
    ])

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Compare fixed OPMAD vs evolved ontology extraction"
    )
    parser.add_argument("--fixed-facts", nargs="+", required=True)
    parser.add_argument("--evolved-facts", nargs="+", required=True)
    parser.add_argument("--evolved-ontology", nargs="*", default=[])
    parser.add_argument("--seed-ontology", default=None)
    parser.add_argument("--output", default=None, help="Output markdown file")
    args = parser.parse_args()

    fixed_paths = resolve_globs(args.fixed_facts)
    evolved_fact_paths = resolve_globs(args.evolved_facts)
    evolved_onto_paths = resolve_globs(args.evolved_ontology)

    if not fixed_paths:
        parser.error("No fixed-facts files found")
    if not evolved_fact_paths:
        parser.error("No evolved-facts files found")

    print(f"Loading fixed-mode facts from {len(fixed_paths)} file(s)...", file=sys.stderr)
    fixed_g = load_graph(fixed_paths)

    print(f"Loading evolved-mode output from {len(evolved_fact_paths) + len(evolved_onto_paths)} file(s)...", file=sys.stderr)
    evolved_g = load_graph(evolved_fact_paths + evolved_onto_paths)

    fixed_metrics = extract_metrics(fixed_g, "Fixed OPMAD")
    evolved_metrics = extract_metrics(evolved_g, "Evolved Ontology")

    # Load seed ontology classes if provided
    seed_classes = None
    if args.seed_ontology and Path(args.seed_ontology).exists():
        seed_g = Graph()
        seed_g.parse(args.seed_ontology, format="turtle")
        seed_classes = set()
        for s in seed_g.subjects(RDF.type, RDFS.Class):
            seed_classes.add(str(s))
        for s in seed_g.subjects(RDF.type, OWL.Class):
            seed_classes.add(str(s))

    report = generate_report(fixed_metrics, evolved_metrics, seed_classes)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
