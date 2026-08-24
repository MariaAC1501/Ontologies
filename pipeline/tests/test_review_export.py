from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.review_export import ANALYTICAL_FIELDS, build_review_records, main


PREFIXES = """\
@prefix doc: <urn:review-test:> .
@prefix opmad: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#> .
@prefix cco: <http://www.ontologyrepository.com/CommonCoreOntologies/> .
@prefix schema: <https://schema.org/> .
"""


def write_ttl(directory: Path, name: str, body: str) -> Path:
    path = directory / name
    path.write_text(PREFIXES + body, encoding="utf-8")
    return path


class StrictReviewExportTests(unittest.TestCase):
    def test_machine_readable_schema_covers_all_analytical_fields_and_statuses(self) -> None:
        schema_path = Path(__file__).resolve().parents[1] / "review_export.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        field_schema = schema["properties"]["fields"]
        self.assertEqual(tuple(field_schema["required"]), ANALYTICAL_FIELDS)
        self.assertEqual(set(field_schema["properties"]), set(ANALYTICAL_FIELDS))
        self.assertEqual(
            schema["$defs"]["status"]["enum"],
            ["present", "not_reported", "unclear", "not_applicable", "extraction_failure"],
        )

    def test_missing_count_is_null_but_asserted_zero_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            missing = write_ttl(
                root,
                "missing.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:name "Missing count" ; schema:about doc:Module .
doc:Case a opmad:Predictive_maintenance_case ; cco:designates doc:Module .
doc:Module a opmad:Predictive_maintenance_model .
""",
            )
            zero = write_ttl(
                root,
                "zero.ttl",
                """
doc:Article2 a opmad:Predictive_Maintenance_Article ; schema:name "Zero count" ; schema:about doc:Module2 .
doc:Case2 a opmad:Predictive_maintenance_case ; cco:designates doc:Module2 .
doc:Module2 opmad:has_failure_mode_count doc:Count2 .
doc:Count2 a opmad:Number_of_failure_modes ; opmad:has_interger_value 0 .
""",
            )
            records = build_review_records([missing, zero])

        self.assertEqual(len(records), 2)
        missing_field = records[0]["fields"]["number_of_failure_modes"]
        zero_field = records[1]["fields"]["number_of_failure_modes"]
        self.assertEqual(missing_field["status"], "not_reported")
        self.assertIsNone(missing_field["value"])
        self.assertEqual(zero_field["status"], "present")
        self.assertEqual(zero_field["value"], 0)
        self.assertEqual(zero_field["raw_values"], ["0"])

    def test_multiple_files_remain_distinct_and_do_not_receive_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            first = write_ttl(
                root,
                "paper-a.ttl",
                """
doc:A a opmad:Predictive_Maintenance_Article ; schema:name "Paper A" ; schema:datePublished "2020-04-01" .
""",
            )
            second = write_ttl(
                root,
                "paper-b.ttl",
                """
doc:B a opmad:Predictive_Maintenance_Article ; schema:name "Paper B" .
doc:OnlyInB a opmad:Data_variable ; schema:name "B pressure" .
""",
            )
            records = build_review_records([first, second])

        self.assertEqual([record["source_document"]["facts_filename"] for record in records], ["paper-a.ttl", "paper-b.ttl"])
        self.assertEqual(records[0]["fields"]["publication_year"]["value"], 2020)
        self.assertEqual(records[1]["fields"]["publication_year"]["status"], "not_reported")
        self.assertIsNone(records[1]["fields"]["publication_year"]["value"])
        for record in records:
            self.assertIsNone(record["fields"]["task"]["value"])
            self.assertNotEqual(record["fields"]["publication_year"]["value"], 2021)
        self.assertEqual(records[0]["fields"]["input_types"]["status"], "not_reported")
        self.assertEqual(records[1]["fields"]["input_types"]["status"], "unclear")
        self.assertIsNone(records[1]["fields"]["input_types"]["value"])

    def test_multiple_articles_and_cases_are_linked_without_value_leakage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "two-cases.ttl",
                """
doc:ArticleA a opmad:Predictive_Maintenance_Article ; schema:name "Study A" ; schema:about doc:ModuleA .
doc:ArticleB a opmad:Predictive_Maintenance_Article ; schema:name "Study B" ; schema:about doc:ModuleB .
doc:CaseA a opmad:Predictive_maintenance_case ; cco:designates doc:ModuleA .
doc:CaseB a opmad:Predictive_maintenance_case ; cco:designates doc:ModuleB .
doc:ModuleA a opmad:Predictive_maintenance_model, opmad:Fault_detection ; schema:name "Model A" ; opmad:has_input doc:Temperature .
doc:ModuleB a opmad:Predictive_maintenance_model, opmad:Remaining_useful_life_estimation ; schema:name "Model B" ; opmad:has_input doc:Vibration .
doc:Temperature a opmad:Data_variable ; schema:name "Temperature" .
doc:Vibration a opmad:Data_variable ; schema:name "Vibration" .
""",
            )
            records = build_review_records([facts])

        self.assertEqual(len(records), 2)
        by_title = {record["fields"]["study_title"]["value"]: record for record in records}
        self.assertEqual(by_title["Study A"]["case_article_link"]["resolution"], "resolved")
        self.assertEqual(by_title["Study A"]["fields"]["models"]["value"], ["Model A"])
        self.assertEqual(by_title["Study A"]["fields"]["input_types"]["value"], ["Temperature"])
        self.assertEqual(by_title["Study A"]["fields"]["task"]["value"], "Fault detection")
        self.assertEqual(by_title["Study B"]["fields"]["models"]["value"], ["Model B"])
        self.assertEqual(by_title["Study B"]["fields"]["input_types"]["value"], ["Vibration"])
        self.assertEqual(by_title["Study B"]["fields"]["task"]["value"], "Remaining useful life estimation")

    def test_unresolved_case_is_flagged_instead_of_paired_with_article(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "unresolved.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:name "Unlinked article" .
doc:Case a opmad:Predictive_maintenance_case .
""",
            )
            records = build_review_records([facts])

        case_records = [record for record in records if record["case_identity"]["value"]]
        self.assertEqual(len(case_records), 1)
        self.assertEqual(case_records[0]["case_article_link"]["status"], "unclear")
        self.assertEqual(case_records[0]["case_article_link"]["resolution"], "unresolved")
        self.assertIsNone(case_records[0]["article_identity"]["value"])
        self.assertEqual(case_records[0]["fields"]["study_title"]["status"], "not_applicable")

    def test_design_detail_does_not_become_preprocessing_or_notes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "design.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:about doc:Module .
doc:Case a opmad:Predictive_maintenance_case ; cco:designates doc:Module .
doc:Module opmad:has_design_detail doc:Robustness .
doc:Robustness a opmad:Design_detail ; schema:name "Robust to noise" .
""",
            )
            record = build_review_records([facts])[0]

        self.assertIsNone(record["fields"]["data_preprocessing"]["value"])
        self.assertEqual(record["fields"]["data_preprocessing"]["status"], "unclear")
        self.assertEqual(record["fields"]["complementary_notes"]["status"], "not_reported")
        self.assertEqual(record["supplementary_evidence"]["design_details"]["value"], ["Robust to noise"])
        self.assertEqual(record["fields"]["model_approach"]["status"], "not_reported")

    def test_malformed_input_emits_failure_record_and_cli_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            malformed = root / "bad.ttl"
            malformed.write_text("@prefix x: <urn:x:> . x:subject x:predicate [", encoding="utf-8")
            records = build_review_records([malformed])
            output = root / "review.jsonl"
            return_code = main(["--facts", str(malformed), "--output", str(output)])
            written = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["record_status"], "extraction_failure")
        self.assertEqual(records[0]["fields"]["publication_year"]["status"], "extraction_failure")
        self.assertEqual(records[0]["source_document"]["facts_filename"], "bad.ttl")
        self.assertEqual(return_code, 2)
        self.assertEqual(written[0]["record_status"], "extraction_failure")


if __name__ == "__main__":
    unittest.main()
