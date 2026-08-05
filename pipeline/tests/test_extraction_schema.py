from __future__ import annotations

import sys
import unittest
from pathlib import Path

from pydantic import ValidationError

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.extraction_schema import PredictiveMaintenanceCase


VALID_ROW = {
    "Reference": "7",
    "Publication Year": "2024",
    "Task": "Fault detection",
    "Case study": "Pump",
    "Case study type": "Rotating equipment",
    "Input for the model": "Signals",
    "Number of input variables": "2",
    "Input type": "Vibration, Temperature",
    "Data Pre-processing": "yes",
    "Model Approach": "Single model",
    "Model Type": "Classifier, Tree model",
    "Models": "Random forest, Decision tree",
    "Online/Off-line": "Online",
    "Number of failure modes": "1",
    "Performance indicator": "Accuracy",
    "Performance": "0.95",
    "Complementary notes": "Unit test row",
    "Study title": "Schema unit test",
    "Publication identifier": "doi:10.0000/schema",
}


def row_with(**updates: str) -> dict[str, str]:
    row = dict(VALID_ROW)
    row.update(updates)
    return row


class PredictiveMaintenanceCaseSchemaTests(unittest.TestCase):
    def test_from_csv_row_parses_scalars_lists_and_boolean(self) -> None:
        case = PredictiveMaintenanceCase.from_csv_row(VALID_ROW)

        self.assertEqual(case.reference, 7)
        self.assertEqual(case.publication_year, 2024)
        self.assertEqual(case.input_types, ["Vibration", "Temperature"])
        self.assertEqual(case.model_types, ["Classifier", "Tree model"])
        self.assertEqual(case.models, ["Random forest", "Decision tree"])
        self.assertTrue(case.data_preprocessing)
        self.assertEqual(case.module_synchronization, "Online")

    def test_boolean_parser_accepts_supported_values(self) -> None:
        truthy = ["yes", "y", "true", "1", " YES "]
        falsy = ["no", "n", "false", "0", " No "]

        for raw in truthy:
            with self.subTest(raw=raw):
                self.assertTrue(PredictiveMaintenanceCase._parse_bool(raw))
        for raw in falsy:
            with self.subTest(raw=raw):
                self.assertFalse(PredictiveMaintenanceCase._parse_bool(raw))

    def test_boolean_parser_rejects_unknown_values(self) -> None:
        with self.assertRaises(ValueError):
            PredictiveMaintenanceCase.from_csv_row(row_with(**{"Data Pre-processing": "maybe"}))

    def test_rejects_invalid_task(self) -> None:
        with self.assertRaises(ValidationError):
            PredictiveMaintenanceCase.from_csv_row(row_with(Task="Unsupported task"))

    def test_rejects_empty_multi_value_fields(self) -> None:
        with self.assertRaises(ValidationError):
            PredictiveMaintenanceCase.from_csv_row(row_with(**{"Input type": " , "}))

    def test_rejects_publication_year_outside_supported_range(self) -> None:
        with self.assertRaises(ValidationError):
            PredictiveMaintenanceCase.from_csv_row(row_with(**{"Publication Year": "1800"}))

    def test_missing_csv_header_fails_fast(self) -> None:
        row = dict(VALID_ROW)
        del row["Task"]
        with self.assertRaises(KeyError):
            PredictiveMaintenanceCase.from_csv_row(row)

    def test_direct_model_construction_forbids_extra_fields(self) -> None:
        case_data = PredictiveMaintenanceCase.from_csv_row(VALID_ROW).model_dump()
        with self.assertRaises(ValidationError):
            PredictiveMaintenanceCase(**case_data, unexpected="value")


if __name__ == "__main__":
    unittest.main()
