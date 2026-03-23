#!/usr/bin/env python3
"""Unit tests for pipeline/full_mode/sparql_query.py."""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SPARQL_SCRIPT = REPO_ROOT / "pipeline" / "full_mode" / "sparql_query.py"
ONTOLOGY = REPO_ROOT / "pipeline" / "full_mode" / "test_output" / "ontology_brick_1.0.1.ttl"
FACTS = REPO_ROOT / "pipeline" / "full_mode" / "test_output" / "facts_5cc89b5bfaf6.ttl"


def _has_test_output() -> bool:
    return ONTOLOGY.exists() and FACTS.exists()


@unittest.skipUnless(_has_test_output(), "Full-mode test output not available")
class TestSPARQLQuery(unittest.TestCase):
    def _run(self, *extra_args: str) -> subprocess.CompletedProcess:
        cmd = [
            sys.executable, str(SPARQL_SCRIPT),
            "--ontology", str(ONTOLOGY),
            "--facts", str(FACTS),
            *extra_args,
        ]
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    def test_summary(self):
        r = self._run("--preset", "summary")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Total triples", r.stdout)
        self.assertIn("Unique classes", r.stdout)

    def test_classes(self):
        r = self._run("--preset", "classes")
        self.assertEqual(r.returncode, 0, r.stderr)
        # Should find at least a few classes
        self.assertIn("row(s)", r.stderr)

    def test_instances(self):
        r = self._run("--preset", "instances")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_properties(self):
        r = self._run("--preset", "properties")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_models(self):
        r = self._run("--preset", "models")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_predictive_maintenance(self):
        r = self._run("--preset", "predictive-maintenance")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_custom_query(self):
        r = self._run("--query", "SELECT ?s WHERE { ?s a ?t } LIMIT 5")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_csv_format(self):
        r = self._run("--preset", "summary", "--format", "csv")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("metric;value", r.stdout)

    def test_no_args_fails(self):
        r = self._run()
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
