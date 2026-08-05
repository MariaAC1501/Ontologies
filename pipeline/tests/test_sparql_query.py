#!/usr/bin/env python3
"""Unit tests for pipeline/full_mode/sparql_query.py."""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, OWL

REPO_ROOT = Path(__file__).resolve().parents[2]
SPARQL_SCRIPT = REPO_ROOT / "pipeline" / "full_mode" / "sparql_query.py"

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(REPO_ROOT))

from pipeline.full_mode.sparql_query import (  # noqa: E402
    format_csv_output,
    format_table,
    load_graph,
    resolve_globs,
    run_summary,
    strip_rdf_star_statements,
)


ONTOLOGY_TTL = """@prefix ex: <http://example.org/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Equipment a owl:Class ;
    rdfs:label "Equipment" .
ex:PredictiveModel a rdfs:Class .
ex:usesModel a owl:ObjectProperty ;
    rdfs:domain ex:Equipment ;
    rdfs:range ex:PredictiveModel .
"""

FACTS_TTL = """@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

ex:pump1 a ex:Equipment ;
    rdfs:label "Pump 1" ;
    ex:usesModel ex:model1 .
ex:model1 a ex:PredictiveModel ;
    rdfs:label "ARIMA model" .

_:ev1 rdf:reifies <<( ex:pump1 ex:usesModel ex:model1 )>> ;
    prov:wasDerivedFrom ex:paper1 .
"""


class SparqlQueryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.ontology_path = self.tmp_path / "ontology.ttl"
        self.facts_path = self.tmp_path / "facts.ttl"
        self.ontology_path.write_text(ONTOLOGY_TTL, encoding="utf-8")
        self.facts_path.write_text(FACTS_TTL, encoding="utf-8")

    def _run_cli(self, *extra_args: str) -> subprocess.CompletedProcess[str]:
        cmd = [
            sys.executable,
            str(SPARQL_SCRIPT),
            "--ontology",
            str(self.ontology_path),
            "--facts",
            str(self.facts_path),
            *extra_args,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    def test_strip_rdf_star_statements_removes_reification_blocks(self) -> None:
        cleaned = strip_rdf_star_statements(FACTS_TTL)
        self.assertNotIn("rdf:reifies <<(", cleaned)
        self.assertNotIn("prov:wasDerivedFrom", cleaned)
        self.assertIn("ex:pump1 a ex:Equipment", cleaned)
        self.assertTrue(cleaned.endswith("\n"))

    def test_load_graph_parses_multiple_temp_ttls_after_stripping(self) -> None:
        graph = load_graph([self.ontology_path, self.facts_path])
        ex = Namespace("http://example.org/")

        self.assertEqual(len(graph), 11)
        self.assertIn((ex.Equipment, RDF.type, OWL.Class), graph)
        self.assertIn((ex.pump1, RDF.type, ex.Equipment), graph)
        self.assertIn((ex.pump1, ex.usesModel, ex.model1), graph)

    def test_run_summary_counts_core_graph_metrics(self) -> None:
        ex = Namespace("http://example.org/")
        graph = Graph()
        graph.add((ex.Machine, RDF.type, OWL.Class))
        graph.add((ex.Sensor, RDF.type, RDFS.Class))
        graph.add((ex.pump1, RDF.type, ex.Machine))
        graph.add((ex.pump1, ex.usesSensor, ex.sensor1))

        summary = {row["metric"]: row["value"] for row in run_summary(graph)}
        self.assertEqual(summary["Total triples"], "4")
        self.assertEqual(summary["Unique classes"], "2")
        self.assertEqual(summary["Unique instances"], "1")
        self.assertEqual(summary["Unique properties"], "2")
        self.assertEqual(summary["Unique subjects"], "3")
        self.assertIn("Namespaces", summary)

    def test_format_table_and_csv_are_stable(self) -> None:
        headers = ["metric", "value"]
        rows = [{"metric": "Total triples", "value": "2"}]

        self.assertEqual(format_table(headers, []), "(no results)\n")
        table = format_table(headers, rows)
        self.assertIn("metric", table.splitlines()[0])
        self.assertIn("value", table.splitlines()[0])
        self.assertEqual(format_csv_output(headers, rows).splitlines(), ["metric;value", "Total triples;2"])

    def test_resolve_globs_sorts_matches_and_warns_on_missing_patterns(self) -> None:
        (self.tmp_path / "b.ttl").write_text("", encoding="utf-8")
        (self.tmp_path / "a.ttl").write_text("", encoding="utf-8")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            paths = resolve_globs([str(self.tmp_path / "*.ttl"), str(self.tmp_path / "missing*.ttl")])

        self.assertEqual([path.name for path in paths], ["a.ttl", "b.ttl", "facts.ttl", "ontology.ttl"])
        self.assertIn("Warning: no files match pattern", stderr.getvalue())

    def test_cli_summary_outputs_table(self) -> None:
        result = self._run_cli("--preset", "summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Total triples", result.stdout)
        self.assertIn("Unique classes", result.stdout)
        self.assertIn("Loaded 11 triples from 2 file(s)", result.stderr)
        self.assertIn("(6 row(s))", result.stderr)

    def test_cli_custom_query_outputs_csv(self) -> None:
        result = self._run_cli(
            "--query",
            "PREFIX ex: <http://example.org/> SELECT ?s WHERE { ?s a ex:Equipment } ORDER BY ?s",
            "--format",
            "csv",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("s", result.stdout.splitlines()[0])
        self.assertIn("http://example.org/pump1", result.stdout)
        self.assertIn("(1 row(s))", result.stderr)

    def test_cli_no_query_mode_fails(self) -> None:
        result = self._run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Provide --preset, --query, or --query-file", result.stderr)


if __name__ == "__main__":
    unittest.main()
