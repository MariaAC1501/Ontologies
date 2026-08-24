from __future__ import annotations

import sys
import unittest
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef
from rdflib.compare import isomorphic

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pipeline.extraction_schema import OPMAD
from pipeline.generate_opmad_profile import (
    DEFAULT_OUTPUT,
    DEFAULT_SOURCE,
    LEGACY_SEED_NAMESPACE,
    authoritative_declarations,
    build_profile,
    schema_external_declarations,
    schema_iris,
    serialize_deterministic,
    validate_profile,
)


class OpmadExtractionProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = Graph().parse(DEFAULT_SOURCE)
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
            self.assertIn((term, RDF.type, declarations[term]), self.profile)

    def test_external_schema_relations_are_explicit_support_declarations(self) -> None:
        for term, declaration_type in schema_external_declarations().items():
            self.assertIn((term, RDF.type, declaration_type), self.profile)

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

    def test_committed_profile_is_exact_generated_projection(self) -> None:
        generated = build_profile(self.source)
        validate_profile(self.source, generated)
        self.assertTrue(isomorphic(generated, self.profile))
        self.assertEqual(
            serialize_deterministic(generated),
            DEFAULT_OUTPUT.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
