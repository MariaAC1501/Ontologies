from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.review_export import ANALYTICAL_FIELDS, build_review_records, main

try:
    import jsonschema
except ImportError:  # The deterministic suite does not require this optional package.
    jsonschema = None


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
        status_rule = schema["$defs"]["fieldBase"]["allOf"][0]
        self.assertEqual(status_rule["if"]["properties"]["status"], {"const": "present"})
        self.assertEqual(status_rule["then"]["properties"]["value"], {"not": {"type": "null"}})
        self.assertEqual(status_rule["else"]["properties"]["value"], {"type": "null"})
        list_value = schema["$defs"]["stringListField"]["allOf"][1]["properties"]["value"]
        self.assertEqual(list_value["oneOf"][1]["minItems"], 1)
        self.assertEqual(list_value["oneOf"][1]["items"]["minLength"], 1)
        self.assertEqual(schema["$defs"]["countField"]["allOf"][1]["properties"]["value"]["minimum"], 0)
        year_value = schema["$defs"]["yearField"]["allOf"][1]["properties"]["value"]
        self.assertEqual((year_value["minimum"], year_value["maximum"]), (1900, 2100))

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

    def test_one_article_with_two_cases_does_not_cross_case_models(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "one-article-two-cases.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:name "Combined study" ;
    schema:about doc:ModelA, doc:ModelB .
doc:CaseA a opmad:Predictive_maintenance_case ; cco:designates doc:ModelA .
doc:CaseB a opmad:Predictive_maintenance_case ; cco:designates doc:ModelB .
doc:ModelA a opmad:Predictive_maintenance_model ; schema:name "Case A model" ; opmad:has_input doc:InputA .
doc:ModelB a opmad:Predictive_maintenance_model ; schema:name "Case B model" ; opmad:has_input doc:InputB .
doc:InputA a opmad:Data_variable ; schema:name "Case A temperature" .
doc:InputB a opmad:Data_variable ; schema:name "Case B vibration" .
""",
            )
            records = build_review_records([facts])

        self.assertEqual(len(records), 2)
        by_case = {record["case_identity"]["value"]: record for record in records}
        case_a = by_case["urn:review-test:CaseA"]
        case_b = by_case["urn:review-test:CaseB"]
        self.assertEqual(case_a["fields"]["models"]["value"], ["Case A model"])
        self.assertEqual(case_a["fields"]["input_types"]["value"], ["Case A temperature"])
        self.assertEqual(case_b["fields"]["models"]["value"], ["Case B model"])
        self.assertEqual(case_b["fields"]["input_types"]["value"], ["Case B vibration"])

    def test_shared_input_between_case_pairs_is_ambiguous_not_assigned_twice(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "shared-input.ttl",
                """
doc:ArticleA a opmad:Predictive_Maintenance_Article ; schema:name "Study A" ; schema:about doc:ModelA .
doc:ArticleB a opmad:Predictive_Maintenance_Article ; schema:name "Study B" ; schema:about doc:ModelB .
doc:CaseA a opmad:Predictive_maintenance_case ; cco:designates doc:ModelA .
doc:CaseB a opmad:Predictive_maintenance_case ; cco:designates doc:ModelB .
doc:ModelA a opmad:Predictive_maintenance_model ; schema:name "Model A" ; opmad:has_input doc:SharedInput .
doc:ModelB a opmad:Predictive_maintenance_model ; schema:name "Model B" ; opmad:has_input doc:SharedInput .
doc:SharedInput a opmad:Data_variable ; schema:name "Shared sensor" .
""",
            )
            records = build_review_records([facts])

        self.assertEqual(len(records), 2)
        for record in records:
            self.assertEqual(record["fields"]["input_types"]["status"], "unclear")
            self.assertIsNone(record["fields"]["input_types"]["value"])
            self.assertEqual(record["fields"]["input_types"]["raw_values"], ["Shared sensor"])
        by_title = {record["fields"]["study_title"]["value"]: record for record in records}
        self.assertEqual(by_title["Study A"]["fields"]["models"]["value"], ["Model A"])
        self.assertEqual(by_title["Study B"]["fields"]["models"]["value"], ["Model B"])

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

    def test_invalid_field_values_propagate_failure_to_record_and_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            facts = write_ttl(
                root,
                "invalid-values.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:about doc:Model ; schema:datePublished "year unknown" .
doc:Case a opmad:Predictive_maintenance_case ; cco:designates doc:Model .
doc:Model a opmad:Predictive_maintenance_model ; opmad:has_failure_mode_count doc:Count ;
    opmad:has_data_preprocessing "sometimes" .
doc:Count a opmad:Number_of_failure_modes ; opmad:has_interger_value "many" .
""",
            )
            record = build_review_records([facts])[0]
            output = root / "invalid.jsonl"
            return_code = main(["--facts", str(facts), "--output", str(output)])

        self.assertEqual(record["fields"]["publication_year"]["status"], "extraction_failure")
        self.assertEqual(record["fields"]["number_of_failure_modes"]["status"], "extraction_failure")
        self.assertEqual(record["fields"]["data_preprocessing"]["status"], "extraction_failure")
        self.assertEqual(record["record_status"], "extraction_failure")
        self.assertEqual(return_code, 2)

    def test_missing_literal_and_unmatched_glob_each_emit_explicit_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            valid = write_ttl(root, "valid.ttl", "doc:Article a opmad:Predictive_Maintenance_Article .\n")
            missing = root / "missing.ttl"
            unmatched = str(root / "absent-*.ttl")
            output = root / "review.jsonl"
            return_code = main([
                "--facts", str(valid), str(missing), unmatched, "--output", str(output),
            ])
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]

        self.assertEqual(return_code, 2)
        self.assertEqual(len(records), 3)
        failures = [record for record in records if record["record_status"] == "extraction_failure"]
        self.assertEqual(len(failures), 2)
        self.assertTrue(any(record["source_document"]["facts_path"].endswith("missing.ttl") for record in failures))
        glob_failure = next(record for record in failures if "absent-*" in record["source_document"]["facts_path"])
        self.assertIn("No fact files matched glob pattern", glob_failure["error"]["message"])

    def test_byte_identical_sources_have_distinct_record_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            body = "doc:Article a opmad:Predictive_Maintenance_Article .\n"
            first = write_ttl(root, "copy-a.ttl", body)
            second = write_ttl(root, "copy-b.ttl", body)
            records = build_review_records([first, second])

        self.assertEqual(records[0]["source_document"]["sha256"], records[1]["source_document"]["sha256"])
        self.assertNotEqual(records[0]["source_document"]["source_identity"], records[1]["source_document"]["source_identity"])
        self.assertNotEqual(records[0]["record_id"], records[1]["record_id"])

    def test_non_opmad_local_name_collision_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir),
                "collision.ttl",
                """
doc:Article a opmad:Predictive_Maintenance_Article ; schema:about doc:Model .
doc:Case a opmad:Predictive_maintenance_case ; cco:designates doc:Model .
doc:Model a opmad:Predictive_maintenance_model ; opmad:has_input doc:Collision .
doc:Collision a <urn:unrelated:Data_variable> ; schema:name "Wrong ontology" .
""",
            )
            record = build_review_records([facts])[0]

        self.assertEqual(record["fields"]["input_types"]["status"], "not_reported")

    def test_representative_records_follow_schema_value_status_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            facts = write_ttl(
                Path(tmpdir), "schema.ttl",
                'doc:Article a opmad:Predictive_Maintenance_Article ; schema:name "Schema study" .\n',
            )
            record = build_review_records([facts])[0]

        for field in [record["article_identity"], record["case_identity"], *record["fields"].values()]:
            if field["status"] == "present":
                self.assertIsNotNone(field["value"])
                if isinstance(field["value"], (str, list)):
                    self.assertTrue(field["value"])
            else:
                self.assertIsNone(field["value"])
        if jsonschema is not None:
            schema_path = Path(__file__).resolve().parents[1] / "review_export.schema.json"
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(record, schema)
            invalid = json.loads(json.dumps(record))
            invalid["article_identity"]["value"] = None
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(invalid, schema)
            invalid = json.loads(json.dumps(record))
            invalid["case_identity"]["status"] = "not_reported"
            invalid["case_identity"]["value"] = "urn:should-be-null"
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(invalid, schema)

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
