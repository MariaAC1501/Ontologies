from __future__ import annotations

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from rdflib import Graph, OWL, RDF, URIRef
from rdflib.compare import isomorphic

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.extraction_schema import OPMAD
from pipeline import generate_opmad_profile as generator
from pipeline.generate_opmad_profile import (
    DEFAULT_OUTPUT,
    DEFAULT_SOURCE,
    DEFAULT_SOURCE_SUBMODULE_COMMIT,
    EXPECTED_DEFAULT_SOURCE_SHA256,
    LEGACY_SEED_NAMESPACE,
    authoritative_declarations,
    build_profile,
    schema_external_declarations,
    load_source,
    main,
    schema_iris,
    serialize_deterministic,
    source_provenance,
    validate_profile,
)


class OpmadExtractionProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.provenance = source_provenance(DEFAULT_SOURCE)
        cls.source = load_source(cls.provenance)
        cls.profile = Graph().parse(DEFAULT_OUTPUT, format="turtle")

    def test_namespace_is_authoritative_and_stable(self) -> None:
        self.assertEqual(
            OPMAD,
            "http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD#",
        )
        iris = {
            str(node)
            for triple in self.profile
            for node in triple
            if isinstance(node, URIRef)
        }
        self.assertFalse(any(iri.startswith(LEGACY_SEED_NAMESPACE) for iri in iris))

    def test_every_schema_opmad_term_is_authoritatively_declared(self) -> None:
        declarations = authoritative_declarations(self.source)
        required = {iri for iri in schema_iris() if str(iri).startswith(OPMAD)}

        self.assertTrue(required)
        self.assertEqual(set(), required - declarations.keys())
        for term in required:
            for declaration_type in declarations[term]:
                self.assertIn((term, RDF.type, declaration_type), self.profile)

    def test_external_schema_relations_are_explicit_support_declarations(self) -> None:
        for term, declaration_type in schema_external_declarations().items():
            self.assertIn((term, RDF.type, declaration_type), self.profile)

    def test_external_restriction_classes_are_support_declarations(self) -> None:
        calendar_year = URIRef("http://www.ontologyrepository.com/CommonCoreOntologies/CalendarYear")
        self.assertTrue(any(self.profile.subjects(OWL.onClass, calendar_year)))
        self.assertIn((calendar_year, RDF.type, OWL.Class), self.profile)

    def test_profile_has_no_unauthorized_opmad_vocabulary(self) -> None:
        # The validator checks OPMAD IRIs in every RDF position, not just subjects.
        validate_profile(self.source, self.profile)

        poisoned = Graph()
        for triple in self.profile:
            poisoned.add(triple)
        poisoned.add((URIRef(f"{OPMAD}Invented_extraction_class"), RDF.type, OWL.Class))
        with self.assertRaisesRegex(ValueError, "Unauthorized OPMAD IRI"):
            validate_profile(self.source, poisoned)

        drifted = build_profile(self.source)
        drifted.add((URIRef(f"{OPMAD.removesuffix('#')}/seed#Bad"), RDF.type, OWL.Class))
        with self.assertRaisesRegex(ValueError, "Non-authoritative OPMAD domain namespace"):
            validate_profile(self.source, drifted)

    def test_wrong_declaration_kind_for_existing_term_is_rejected(self) -> None:
        poisoned = build_profile(self.source)
        term = URIRef(f"{OPMAD}Predictive_Maintenance_Article")
        self.assertIn((term, RDF.type, OWL.Class), poisoned)
        poisoned.add((term, RDF.type, OWL.ObjectProperty))
        with self.assertRaisesRegex(ValueError, "declaration kinds.*do not match"):
            validate_profile(self.source, poisoned)

    def test_source_provenance_is_pinned_and_custom_sources_require_opt_in(self) -> None:
        provenance = source_provenance(DEFAULT_SOURCE)
        self.assertTrue(provenance.authoritative)
        self.assertEqual(provenance.sha256, EXPECTED_DEFAULT_SOURCE_SHA256)
        self.assertEqual(hashlib.sha256(provenance.content).hexdigest(), provenance.sha256)
        self.assertIn(DEFAULT_SOURCE_SUBMODULE_COMMIT, provenance.identity)

        with tempfile.TemporaryDirectory() as tmpdir:
            custom_source = Path(tmpdir) / "altered.owl"
            custom_source.write_bytes(DEFAULT_SOURCE.read_bytes() + b"\n")
            output = Path(tmpdir) / "profile.ttl"
            output.write_text("existing output", encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as raised:
                    main(["--source", str(custom_source), "--output", str(output)])
            self.assertEqual(raised.exception.code, 1)
            self.assertIn("requires --allow-custom-source", stderr.getvalue())
            self.assertEqual(output.read_text(encoding="utf-8"), "existing output")

            with contextlib.redirect_stdout(io.StringIO()):
                result = main(
                    [
                        "--source",
                        str(custom_source),
                        "--allow-custom-source",
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(result, 0)
            rendered = output.read_text(encoding="utf-8")
            self.assertIn("Source identity: custom source (not authoritative OPMAD submodule)", rendered)
            self.assertIn(f"Source path: {custom_source.resolve()}", rendered)
            self.assertIn(f"Source SHA-256: {hashlib.sha256(custom_source.read_bytes()).hexdigest()}", rendered)

    def test_modified_default_source_is_rejected_by_the_explicit_pin(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            modified_default = Path(tmpdir) / "OPMAD.owl"
            modified_default.write_bytes(self.provenance.content + b"\n")
            modified_hash = hashlib.sha256(modified_default.read_bytes()).hexdigest()

            with mock.patch.object(generator, "DEFAULT_SOURCE", modified_default):
                with self.assertRaisesRegex(
                    ValueError,
                    rf"SHA-256 mismatch.*expected {EXPECTED_DEFAULT_SOURCE_SHA256}, found {modified_hash}.*source-pin update",
                ):
                    source_provenance(modified_default)

    def test_replacement_after_single_read_cannot_split_digest_and_parse_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_source = Path(tmpdir) / "custom.owl"
            replacement = Path(tmpdir) / "replacement.owl"
            original_bytes = self.provenance.content
            custom_source.write_bytes(original_bytes)
            replacement.write_bytes(b"not RDF/XML")
            original_read_bytes = Path.read_bytes
            source_reads = 0

            def read_then_replace(path: Path) -> bytes:
                nonlocal source_reads
                content = original_read_bytes(path)
                if path.resolve() == custom_source.resolve():
                    source_reads += 1
                    replacement.replace(custom_source)
                return content

            with mock.patch.object(Path, "read_bytes", read_then_replace):
                provenance = source_provenance(custom_source, allow_custom_source=True)

            self.assertEqual(source_reads, 1)
            self.assertEqual(custom_source.read_bytes(), b"not RDF/XML")
            self.assertEqual(provenance.sha256, hashlib.sha256(original_bytes).hexdigest())
            source = load_source(provenance)
            profile = build_profile(source)
            validate_profile(source, profile)
            rendered = serialize_deterministic(profile, provenance)
            self.assertIn(f"# Source SHA-256: {hashlib.sha256(original_bytes).hexdigest()}", rendered)

    def test_parser_error_is_actionable_and_does_not_overwrite_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            malformed = Path(tmpdir) / "malformed.owl"
            malformed.write_text("<rdf:RDF><broken>", encoding="utf-8")
            output = Path(tmpdir) / "profile.ttl"
            output.write_text("keep me", encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as raised:
                    main(
                        [
                            "--source",
                            str(malformed),
                            "--allow-custom-source",
                            "--output",
                            str(output),
                        ]
                    )
            self.assertEqual(raised.exception.code, 1)
            self.assertIn("Could not parse OPMAD source", stderr.getvalue())
            self.assertIn("Verify that the file contains valid RDF/XML", stderr.getvalue())
            self.assertEqual(output.read_text(encoding="utf-8"), "keep me")

    def test_committed_profile_is_exact_generated_projection(self) -> None:
        generated = build_profile(self.source)
        validate_profile(self.source, generated)
        self.assertTrue(isomorphic(generated, self.profile))
        rendered = serialize_deterministic(generated, self.provenance)
        self.assertEqual(rendered, DEFAULT_OUTPUT.read_text(encoding="utf-8"))
        self.assertIn(
            f"# Source identity: authoritative CBR ontology submodule OPMAD.owl at {DEFAULT_SOURCE_SUBMODULE_COMMIT}",
            rendered,
        )
        self.assertIn(f"# Source SHA-256: {EXPECTED_DEFAULT_SOURCE_SHA256}", rendered)


if __name__ == "__main__":
    unittest.main()
