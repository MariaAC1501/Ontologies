#!/usr/bin/env python3
"""SPARQL query interface for OntoCast evolved ontology and facts.

Sample invocations:
    python pipeline/full_mode/sparql_query.py \
      --ontology pipeline/full_mode/test_output/ontology_*.ttl \
      --facts pipeline/full_mode/test_output/facts_*.ttl \
      --preset summary

    python pipeline/full_mode/sparql_query.py \
      --ontology pipeline/full_mode/test_output/ontology_*.ttl \
      --facts pipeline/full_mode/test_output/facts_*.ttl \
      --preset classes

    python pipeline/full_mode/sparql_query.py \
      --ontology pipeline/full_mode/test_output/ontology_*.ttl \
      --facts pipeline/full_mode/test_output/facts_*.ttl \
      --query "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
"""

from __future__ import annotations

import argparse
import csv
import glob
import io
import re
import sys
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL


# ---------------------------------------------------------------------------
# RDF-star stripping (same approach as pipeline/facts_to_csv.py)
# ---------------------------------------------------------------------------

def strip_rdf_star_statements(text: str) -> str:
    """Remove RDF-star reification blocks that rdflib cannot parse."""
    cleaned = re.sub(
        r"(?ms)^_:[^\n]*rdf:reifies <<\([^\n]*>>\s*;\s*\n\s*prov:wasDerivedFrom [^\n]*\.\s*\n?",
        "",
        text,
    )
    cleaned = re.sub(r"(?m)^_:[^\n]*\s+prov:wasDerivedFrom [^\n]*\.\s*\n?", "", cleaned)
    return cleaned if cleaned.endswith("\n") else cleaned + "\n"


def load_graph(paths: list[Path]) -> Graph:
    """Load one or more TTL files into a single graph, stripping RDF-star."""
    g = Graph()
    for p in paths:
        text = p.read_text(encoding="utf-8")
        g.parse(data=strip_rdf_star_statements(text), format="turtle")
    return g


# ---------------------------------------------------------------------------
# Preset queries
# ---------------------------------------------------------------------------

PRESETS: dict[str, str] = {
    "classes": """
        SELECT DISTINCT ?class ?label ?comment WHERE {
            { ?class a rdfs:Class }
            UNION { ?class a owl:Class }
            UNION { ?something a ?class . FILTER(!STRSTARTS(STR(?class), STR(rdf:))) }
            OPTIONAL { ?class rdfs:label ?label }
            OPTIONAL { ?class rdfs:comment ?comment }
        }
        ORDER BY ?class
    """,

    "instances": """
        SELECT DISTINCT ?instance ?type ?label WHERE {
            ?instance a ?type .
            FILTER(!STRSTARTS(STR(?type), STR(rdf:)))
            FILTER(!STRSTARTS(STR(?type), "http://www.w3.org/2002/07/owl#"))
            FILTER(!STRSTARTS(STR(?type), "http://www.w3.org/ns/prov#"))
            FILTER(!STRSTARTS(STR(?type), "https://schema.org/"))
            OPTIONAL { ?instance rdfs:label ?label }
        }
        ORDER BY ?type ?instance
    """,

    "properties": """
        SELECT DISTINCT ?property ?domain ?range ?label WHERE {
            { ?property a rdf:Property }
            UNION { ?property a owl:ObjectProperty }
            UNION { ?property a owl:DatatypeProperty }
            UNION { ?s ?property ?o . FILTER(!STRSTARTS(STR(?property), STR(rdf:)))
                                      FILTER(!STRSTARTS(STR(?property), STR(rdfs:))) }
            OPTIONAL { ?property rdfs:domain ?domain }
            OPTIONAL { ?property rdfs:range ?range }
            OPTIONAL { ?property rdfs:label ?label }
        }
        ORDER BY ?property
    """,

    "models": """
        SELECT DISTINCT ?entity ?type ?label ?comment WHERE {
            ?entity a ?type .
            OPTIONAL { ?entity rdfs:label ?label }
            OPTIONAL { ?entity rdfs:comment ?comment }
            FILTER(
                CONTAINS(LCASE(STR(?type)), "model") ||
                CONTAINS(LCASE(STR(?label)), "model") ||
                CONTAINS(LCASE(STR(?type)), "algorithm") ||
                CONTAINS(LCASE(STR(?type)), "predicti")
            )
        }
        ORDER BY ?type ?entity
    """,

    "predictive-maintenance": """
        SELECT DISTINCT ?entity ?type ?label WHERE {
            ?entity a ?type .
            OPTIONAL { ?entity rdfs:label ?label }
            FILTER(
                CONTAINS(LCASE(STR(?type)), "maintenance") ||
                CONTAINS(LCASE(STR(?type)), "predictive") ||
                CONTAINS(LCASE(STR(?type)), "fault") ||
                CONTAINS(LCASE(STR(?type)), "failure") ||
                CONTAINS(LCASE(STR(?type)), "sensor") ||
                CONTAINS(LCASE(STR(?type)), "signal") ||
                CONTAINS(LCASE(STR(?label)), "maintenance") ||
                CONTAINS(LCASE(STR(?label)), "predictive")
            )
        }
        ORDER BY ?type ?entity
    """,
}


def run_summary(g: Graph) -> list[dict]:
    """Compute summary statistics without SPARQL."""
    classes = set()
    instances = set()
    properties = set()

    for s, p, o in g:
        properties.add(p)
        if p == RDF.type:
            if o in (RDFS.Class, OWL.Class):
                classes.add(s)
            else:
                instances.add(s)
                classes.add(o)

    return [
        {"metric": "Total triples", "value": str(len(g))},
        {"metric": "Unique classes", "value": str(len(classes))},
        {"metric": "Unique instances", "value": str(len(instances))},
        {"metric": "Unique properties", "value": str(len(properties))},
        {"metric": "Unique subjects", "value": str(len(set(g.subjects())))},
        {"metric": "Namespaces", "value": str(len(list(g.namespaces())))},
    ]


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_table(headers: list[str], rows: list[dict]) -> str:
    """Format query results as a readable text table."""
    if not rows:
        return "(no results)\n"

    # Truncate long values for display
    def trunc(val: str, maxlen: int = 80) -> str:
        return val if len(val) <= maxlen else val[: maxlen - 3] + "..."

    col_widths = {h: len(h) for h in headers}
    str_rows = []
    for row in rows:
        str_row = {}
        for h in headers:
            val = trunc(str(row.get(h, "")))
            str_row[h] = val
            col_widths[h] = max(col_widths[h], len(val))
        str_rows.append(str_row)

    sep = "  "
    header_line = sep.join(h.ljust(col_widths[h]) for h in headers)
    divider = sep.join("-" * col_widths[h] for h in headers)
    lines = [header_line, divider]
    for row in str_rows:
        lines.append(sep.join(row[h].ljust(col_widths[h]) for h in headers))
    return "\n".join(lines) + "\n"


def format_csv_output(headers: list[str], rows: list[dict]) -> str:
    """Format query results as CSV."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=headers, delimiter=";", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def resolve_globs(patterns: list[str]) -> list[Path]:
    """Resolve glob patterns to actual file paths."""
    paths = []
    for pattern in patterns:
        expanded = glob.glob(pattern)
        if not expanded:
            print(f"Warning: no files match pattern '{pattern}'", file=sys.stderr)
        paths.extend(Path(p) for p in sorted(expanded))
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="SPARQL query interface for OntoCast evolved ontology output"
    )
    parser.add_argument(
        "--ontology", nargs="*", default=[],
        help="Glob pattern(s) for evolved ontology TTL file(s)"
    )
    parser.add_argument(
        "--facts", nargs="*", default=[],
        help="Glob pattern(s) for facts TTL file(s)"
    )
    parser.add_argument(
        "--preset", choices=list(PRESETS.keys()) + ["summary"],
        help="Run a built-in query preset"
    )
    parser.add_argument(
        "--query",
        help="Custom SPARQL SELECT query"
    )
    parser.add_argument(
        "--query-file",
        help="Path to a file containing a SPARQL query"
    )
    parser.add_argument(
        "--format", choices=["table", "csv"], default="table",
        dest="output_format",
        help="Output format (default: table)"
    )
    args = parser.parse_args()

    if not args.preset and not args.query and not args.query_file:
        parser.error("Provide --preset, --query, or --query-file")

    onto_paths = resolve_globs(args.ontology)
    facts_paths = resolve_globs(args.facts)
    all_paths = onto_paths + facts_paths

    if not all_paths:
        parser.error("No input files found. Provide --ontology and/or --facts.")

    g = load_graph(all_paths)
    print(f"Loaded {len(g)} triples from {len(all_paths)} file(s)\n", file=sys.stderr)

    # Determine query
    if args.preset == "summary":
        rows = run_summary(g)
        headers = ["metric", "value"]
    else:
        if args.preset:
            sparql = PRESETS[args.preset]
        elif args.query_file:
            sparql = Path(args.query_file).read_text(encoding="utf-8")
        else:
            sparql = args.query

        results = g.query(sparql)
        headers = [str(v) for v in results.vars]
        rows = [{str(v): str(row[v]) if row[v] is not None else "" for v in results.vars} for row in results]

    # Format output
    if args.output_format == "csv":
        print(format_csv_output(headers, rows))
    else:
        print(format_table(headers, rows))

    print(f"({len(rows)} row(s))", file=sys.stderr)


if __name__ == "__main__":
    main()
