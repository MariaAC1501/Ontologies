from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.extraction_schema import PredictiveMaintenanceCase
from pipeline.facts_to_csv import (
    HEADERS,
    build_cases_from_fact_files,
    cases_to_csv_rows,
    strip_rdf_star_statements,
    write_csv,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FACTS_PATH = REPO_ROOT / "pipeline/test_output/facts_5cc89b5bfaf6.ttl"
ONTOLOGY_PATH = REPO_ROOT / "pipeline/seed_ontology/opmad_seed.ttl"


class FactsToCsvTests(unittest.TestCase):
    def test_strip_rdf_star_statements_removes_reification_blocks(self) -> None:
        raw = FACTS_PATH.read_text(encoding="utf-8")
        cleaned = strip_rdf_star_statements(raw)
        self.assertNotIn("rdf:reifies <<(", cleaned)
        self.assertIn("doc:FactsMachineLearningForPredictiveMaintenance", cleaned)

    def test_real_facts_generate_valid_csv_rows(self) -> None:
        cases = build_cases_from_fact_files([FACTS_PATH], ONTOLOGY_PATH)
        self.assertEqual(len(cases), 1)

        rows = cases_to_csv_rows(cases)
        self.assertEqual(list(rows[0].keys()), HEADERS)

        row = rows[0]
        self.assertEqual(row["Study title"], "Machine Learning for Predictive Maintenance of Industrial Machines using IoT Sensor Data")
        self.assertEqual(row["Case study"], "Slitting Machine")
        self.assertEqual(row["Task"], "One step future state forecast")
        self.assertEqual(row["Online/Off-line"], "Unknown synchronization")
        self.assertIn("ARIMA Model", row["Models"])
        self.assertIn(", ", row["Input type"], "multi-value fields must use ', ' separator")
        self.assertEqual(
            set(PredictiveMaintenanceCase.from_csv_row(row).input_types),
            {"Width", "Tension", "Pressure", "Time Stamp"},
        )

        validated = PredictiveMaintenanceCase.from_csv_row(row)
        self.assertEqual(validated.number_of_input_variables, 4)
        self.assertTrue(validated.data_preprocessing)

    def test_write_csv_uses_semicolon_delimiter(self) -> None:
        rows = cases_to_csv_rows(build_cases_from_fact_files([FACTS_PATH], ONTOLOGY_PATH))
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "cases.csv"
            write_csv(output, rows)
            text = output.read_text(encoding="utf-8")
            self.assertIn(";", text.splitlines()[0])
            with output.open("r", encoding="utf-8", newline="") as handle:
                parsed = list(csv.DictReader(handle, delimiter=";"))
        self.assertEqual(len(parsed), 1)
        validated = PredictiveMaintenanceCase.from_csv_row(parsed[0])
        self.assertEqual(validated.study_title, rows[0]["Study title"])


if __name__ == "__main__":
    unittest.main()
