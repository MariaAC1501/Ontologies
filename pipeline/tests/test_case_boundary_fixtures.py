from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.review_export import build_review_records


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class CaseBoundaryFixtureTests(unittest.TestCase):
    def test_one_article_one_case_fixture_yields_one_linked_record(self) -> None:
        records = build_review_records([FIXTURES / "review_one_article_one_case.ttl"])

        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["case_article_link"]["resolution"], "resolved")
        self.assertEqual(record["fields"]["study_title"]["value"], "One-case article")
        self.assertEqual(record["fields"]["models"]["value"], ["One-case model"])
        self.assertEqual(record["fields"]["case_study"]["value"], "Hydraulic pump")
        self.assertEqual(record["fields"]["input_types"]["value"], ["Pressure"])

    def test_one_article_multiple_cases_fixture_keeps_equal_labels_separate(self) -> None:
        records = build_review_records([FIXTURES / "review_one_article_multiple_cases.ttl"])

        self.assertEqual(len(records), 2)
        by_case = {record["case_identity"]["value"].rsplit(":", 1)[-1]: record for record in records}
        diagnostic = by_case["DiagnosticCase"]
        prognostic = by_case["PrognosticCase"]

        self.assertEqual(diagnostic["fields"]["models"]["value"], ["Repeated model label"])
        self.assertEqual(prognostic["fields"]["models"]["value"], ["Repeated model label"])
        self.assertEqual(
            diagnostic["fields"]["models"]["source_nodes"],
            ["urn:review-fixture:multiple-cases:DiagnosticModel"],
        )
        self.assertEqual(
            prognostic["fields"]["models"]["source_nodes"],
            ["urn:review-fixture:multiple-cases:PrognosticModel"],
        )
        self.assertEqual(diagnostic["fields"]["input_types"]["value"], ["Current"])
        self.assertEqual(prognostic["fields"]["input_types"]["value"], ["Vibration"])
        self.assertEqual(diagnostic["fields"]["task"]["value"], "Fault detection")
        self.assertEqual(prognostic["fields"]["task"]["value"], "Remaining useful life estimation")

    def test_one_case_multiple_models_fixture_retains_the_model_set(self) -> None:
        records = build_review_records([FIXTURES / "review_one_case_multiple_models.ttl"])

        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record["case_article_link"]["resolution"], "resolved")
        self.assertEqual(record["fields"]["model_approach"]["value"], "Coordinated model set")
        self.assertEqual(record["fields"]["models"]["value"], ["Fault classifier", "Temporal encoder"])
        self.assertEqual(
            set(record["fields"]["models"]["source_nodes"]),
            {
                "urn:review-fixture:multiple-models:Classifier",
                "urn:review-fixture:multiple-models:Encoder",
            },
        )
        self.assertEqual(record["fields"]["input_types"]["value"], ["Temperature"])

    def test_repeated_entity_iris_across_papers_do_not_merge_graphs(self) -> None:
        records = build_review_records([
            FIXTURES / "review_repeated_entity_paper_a.ttl",
            FIXTURES / "review_repeated_entity_paper_b.ttl",
        ])

        self.assertEqual(len(records), 2)
        by_source = {record["source_document"]["facts_filename"]: record for record in records}
        paper_a = by_source["review_repeated_entity_paper_a.ttl"]
        paper_b = by_source["review_repeated_entity_paper_b.ttl"]

        self.assertEqual(paper_a["case_identity"]["value"], paper_b["case_identity"]["value"])
        self.assertEqual(
            paper_a["fields"]["models"]["source_nodes"],
            paper_b["fields"]["models"]["source_nodes"],
        )
        self.assertEqual(paper_a["fields"]["models"]["value"], ["Repeated model"])
        self.assertEqual(paper_b["fields"]["models"]["value"], ["Repeated model"])
        self.assertEqual(paper_a["fields"]["case_study"]["value"], "Repeated pump")
        self.assertEqual(paper_b["fields"]["case_study"]["value"], "Repeated pump")
        self.assertEqual(paper_a["fields"]["input_types"]["value"], ["Paper A temperature"])
        self.assertEqual(paper_b["fields"]["input_types"]["value"], ["Paper B vibration"])
        self.assertNotEqual(paper_a["record_id"], paper_b["record_id"])
        self.assertNotEqual(
            paper_a["source_document"]["source_identity"],
            paper_b["source_document"]["source_identity"],
        )
        self.assertNotIn("Paper B vibration", json.dumps(paper_a))
        self.assertNotIn("Paper A temperature", json.dumps(paper_b))


if __name__ == "__main__":
    unittest.main()
