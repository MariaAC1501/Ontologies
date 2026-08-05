from __future__ import annotations

import unittest

from scripts.compare_diversity_all_papers import normalize_query, query_csv_row


class CompareDiversityNormalizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.vocabulary = {
            "task": {"Fault detection"},
            "case_study_type": {"Rotary machines"},
            "case_study": set(),
            "online_offline": {"Online", "Off-line", "Both", "Unknown synchronization"},
            "input_for_model": {"Signals", "Time series"},
        }
        self.case_row = {
            "Task": "Fault detection",
            "Case study type": "Maintainable item",
            "Case study": "bearing",
            "Online/Off-line": "Unknown synchronization",
            "Input for the model": "Not reported",
            "Input type": "vibration",
            "Number of input variables": "1",
        }

    def test_unknown_synchronization_is_retained_by_default(self) -> None:
        query, _ = normalize_query(self.case_row, self.vocabulary)
        self.assertEqual(query["online_offline"], "Unknown synchronization")

    def test_unknown_synchronization_can_be_dropped_as_missing(self) -> None:
        query, notes = normalize_query(
            self.case_row,
            self.vocabulary,
            drop_default_synchronization=True,
        )
        self.assertEqual(query["online_offline"], "")
        self.assertIn("default online/offline dropped", " | ".join(notes))

    def test_query_year_is_serialized_for_reproducibility(self) -> None:
        query, _ = normalize_query(
            self.case_row,
            self.vocabulary,
            drop_default_synchronization=True,
        )
        row = query_csv_row(query, number_of_cases=5, query_year=2026)
        self.assertEqual(row["Query Year"], "2026")
        self.assertEqual(row["w4"], "")
        self.assertEqual(row["Number of cases to retrieve"], "5")


if __name__ == "__main__":
    unittest.main()
