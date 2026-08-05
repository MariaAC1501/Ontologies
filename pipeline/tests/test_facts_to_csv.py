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


FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
FACTS_PATH = FIXTURES_DIR / "fixed_mode_facts.ttl"
ONTOLOGY_LABELS_PATH = FIXTURES_DIR / "opmad_labels.ttl"

EXPECTED_ROW = {
    "Reference": "1",
    "Publication Year": "2024",
    "Task": "One step future state forecast",
    "Case study": "Hydraulic press",
    "Case study type": "Maintainable item",
    "Input for the model": "SCADA record",
    "Number of input variables": "2",
    "Input type": "Temperature, Vibration",
    "Data Pre-processing": "yes",
    "Model Approach": "Single model",
    "Model Type": "Random forest",
    "Models": "Random forest classifier",
    "Online/Off-line": "Unknown synchronization",
    "Number of failure modes": "0",
    "Performance indicator": "Not reported",
    "Performance": "Not reported",
    "Complementary notes": (
        "Keywords: predictive maintenance, sensors; Design details: Min-max scaling; "
        "Instruments: Vibration sensor"
    ),
    "Study title": "Unit test predictive maintenance study",
    "Publication identifier": "doi:10.0000/unit",
}


class FactsToCsvTests(unittest.TestCase):
    def test_strip_rdf_star_statements_removes_reification_blocks(self) -> None:
        raw = FACTS_PATH.read_text(encoding="utf-8")
        cleaned = strip_rdf_star_statements(raw)
        self.assertNotIn("rdf:reifies <<(", cleaned)
        self.assertNotIn("prov:wasDerivedFrom", cleaned)
        self.assertIn("doc:Paper a opmad:Predictive_Maintenance_Article", cleaned)
        self.assertTrue(cleaned.endswith("\n"))

    def test_fixture_facts_generate_valid_csv_rows(self) -> None:
        cases = build_cases_from_fact_files([FACTS_PATH], ONTOLOGY_LABELS_PATH)
        self.assertEqual(len(cases), 1)

        case = cases[0]
        self.assertEqual(case.reference, 1)
        self.assertEqual(case.publication_year, 2024)
        self.assertEqual(case.task, "One step future state forecast")
        self.assertEqual(case.case_study, "Hydraulic press")
        self.assertEqual(case.input_for_model, "SCADA record")
        self.assertEqual(case.input_types, ["Temperature", "Vibration"])
        self.assertTrue(case.data_preprocessing)
        self.assertEqual(case.model_approach, "Single model")
        self.assertEqual(case.model_types, ["Random forest"])
        self.assertEqual(case.models, ["Random forest classifier"])

        rows = cases_to_csv_rows(cases)
        self.assertEqual(len(rows), 1)
        self.assertEqual(list(rows[0].keys()), HEADERS)
        self.assertEqual(rows[0], EXPECTED_ROW)

        validated = PredictiveMaintenanceCase.from_csv_row(rows[0])
        self.assertEqual(validated.number_of_input_variables, 2)
        self.assertEqual(validated.input_types, ["Temperature", "Vibration"])
        self.assertTrue(validated.data_preprocessing)

    def test_write_csv_uses_semicolon_delimiter_and_stable_headers(self) -> None:
        rows = cases_to_csv_rows(build_cases_from_fact_files([FACTS_PATH], ONTOLOGY_LABELS_PATH))
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "cases.csv"
            write_csv(output, rows)
            text = output.read_text(encoding="utf-8")
            self.assertEqual(text.splitlines()[0], ";".join(HEADERS))
            with output.open("r", encoding="utf-8", newline="") as handle:
                parsed = list(csv.DictReader(handle, delimiter=";"))
        self.assertEqual(parsed, rows)
        validated = PredictiveMaintenanceCase.from_csv_row(parsed[0])
        self.assertEqual(validated.study_title, EXPECTED_ROW["Study title"])


if __name__ == "__main__":
    unittest.main()
