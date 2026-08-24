from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

from rdflib import Graph

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.extraction_schema import PredictiveMaintenanceCase
from pipeline.facts_to_csv import (
    HEADERS,
    build_cases_from_fact_files,
    cases_to_csv_rows,
    graph_to_cases,
    parse_ontology_labels,
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

    def test_arbitrary_namespace_cannot_impersonate_opmad_classes(self) -> None:
        graph = Graph().parse(
            data="""
                @prefix evil: <https://attacker.example/ontology#> .
                @prefix ex: <https://attacker.example/entities/> .
                @prefix schema: <http://schema.org/> .

                ex:article a evil:Predictive_Maintenance_Article ;
                    schema:name "Poisoned article" .
                ex:item a evil:Maintainable_item ; schema:name "Poisoned item" .
                ex:variable a evil:Data_variable ; schema:name "Poisoned variable" .
                ex:model a evil:Predictive_maintenance_model ; schema:name "Poisoned model" .
                ex:detail a evil:Design_detail ; schema:name "Poisoned preprocessing" .
                ex:task a evil:Fault_detection .
            """,
            format="turtle",
        )

        case = graph_to_cases(graph, {"Fault_detection": "Fault detection"})[0]
        self.assertEqual(case.study_title, "Untitled extracted case")
        self.assertEqual(case.case_study, "Not reported")
        self.assertEqual(case.input_types, ["Not reported"])
        self.assertEqual(case.models, ["Not reported"])
        self.assertFalse(case.data_preprocessing)
        self.assertEqual(case.task, "One step future state forecast")

    def test_unrelated_ontology_label_cannot_override_opmad_task_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ontology = Path(tmpdir) / "poisoned-labels.ttl"
            ontology.write_text(
                """
@prefix opmad: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#> .
@prefix seed: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD/seed#> .
@prefix evil: <https://attacker.example/ontology#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
seed:Fault_detection rdfs:label "Fault detection" .
opmad:Fault_detection rdfs:label "Fault detection" .
evil:Fault_detection rdfs:label "Health assessment" .
""",
                encoding="utf-8",
            )
            labels = parse_ontology_labels(ontology)

        self.assertEqual(labels["Fault_detection"], "Fault detection")
        self.assertNotIn("Health assessment", labels.values())

    def test_authoritative_ontology_label_wins_over_legacy_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            ontology = Path(tmpdir) / "compatible-labels.ttl"
            ontology.write_text(
                """
@prefix opmad: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#> .
@prefix seed: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD/seed#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
seed:Fault_detection rdfs:label "Legacy spelling" .
opmad:Fault_detection rdfs:label "Fault detection" .
""",
                encoding="utf-8",
            )
            labels = parse_ontology_labels(ontology)

        self.assertEqual(labels["Fault_detection"], "Fault detection")

    def test_historical_seed_namespace_remains_compatible(self) -> None:
        graph = Graph().parse(
            data="""
                @prefix seed: <http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD/seed#> .
                @prefix ex: <https://example.test/entities/> .
                @prefix schema: <http://schema.org/> .

                ex:article a seed:Predictive_Maintenance_Article ; schema:name "Legacy article" .
                ex:model a seed:Predictive_maintenance_model ; schema:name "Legacy model" .
                ex:task a seed:Fault_detection .
            """,
            format="turtle",
        )

        case = graph_to_cases(graph, {"Fault_detection": "Fault detection"})[0]
        self.assertEqual(case.study_title, "Legacy article")
        self.assertEqual(case.models, ["Legacy model"])
        self.assertEqual(case.task, "Fault detection")

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
