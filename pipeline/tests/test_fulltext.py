from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pipeline.fulltext import (
    CORPUS_SCHEMA_VERSION,
    ConversionCandidate,
    FullTextError,
    analyze_markdown,
    audit_markdown_files,
    build_source_map,
    load_corpus_manifest,
    prepare_document,
    select_conversion,
    sha256_file,
    validate_source_map,
)
from pipeline.fulltext_run import build_ontocast_command, effective_config


REPO_ROOT = Path(__file__).resolve().parents[2]


def page(number: int, text: str) -> str:
    return f"<!-- PDF_PAGE: {number} -->\n\n{text}\n\n"


def substantial(label: str) -> str:
    return (
        f"{label} evidence-rich predictive-maintenance paragraph with distinct content. "
        * 4
    ).strip()


class FullTextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.pdf = self.root / "paper.pdf"
        self.pdf.write_bytes(b"%PDF-1.7\nfixture\n")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write_manifest(
        self,
        *,
        status: str = "verified",
        frozen: bool = True,
        checksum: str | None = None,
    ) -> Path:
        manifest = {
            "schema_version": CORPUS_SCHEMA_VERSION,
            "base_dir": ".",
            "partition_frozen": frozen,
            "records": [
                {
                    "corpus_id": "paper-0001",
                    "bibliographic_status": status,
                    "partition": "development",
                    "title": "Verified Fixture Study",
                    "doi": "10.1234/fixture.1",
                    "year": 2026,
                    "pdf_path": self.pdf.name,
                    "pdf_sha256": checksum or sha256_file(self.pdf),
                    "source_url": "https://doi.org/10.1234/fixture.1",
                    "licence": "CC BY 4.0",
                }
            ],
        }
        path = self.root / "manifest.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return path

    def test_publication_manifest_requires_verified_frozen_identity_and_pdf_hash(
        self,
    ) -> None:
        path = self.write_manifest()
        _, records, raw = load_corpus_manifest(path)
        self.assertTrue(raw["partition_frozen"])
        self.assertEqual(records["paper-0001"].doi, "10.1234/fixture.1")
        self.assertEqual(records["paper-0001"].title, "Verified Fixture Study")

        with self.assertRaisesRegex(FullTextError, "not human-verified"):
            load_corpus_manifest(self.write_manifest(status="provisional"))
        with self.assertRaisesRegex(FullTextError, "partition_frozen"):
            load_corpus_manifest(self.write_manifest(frozen=False))

        bad_hash = self.write_manifest(checksum="0" * 64)
        _, records, _ = load_corpus_manifest(bad_hash)
        from pipeline.fulltext import resolve_pdf

        with self.assertRaisesRegex(FullTextError, "checksum mismatch"):
            resolve_pdf(self.root, records["paper-0001"])

    def test_source_map_round_trips_pages_sections_paragraphs_and_tables(self) -> None:
        markdown = page(1, "# Introduction\n\n" + substantial("intro")) + page(
            2,
            "## Methods\n\n"
            + substantial("methods")
            + "\n\n<table><tr><th>Model</th><th>Score</th></tr>"
            "<tr><td>A</td><td>0.9</td></tr></table>",
        )
        source_map = build_source_map(markdown, "paper-map")
        validate_source_map(markdown, source_map)

        self.assertEqual(source_map["page_count"], 2)
        self.assertGreaterEqual(source_map["block_count"], 5)
        tables = [block for block in source_map["blocks"] if block["kind"] == "table"]
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0]["page"], 2)
        self.assertEqual(tables[0]["table_shape"], {"rows": 2, "columns": 2})
        methods = next(
            block
            for block in source_map["blocks"]
            if block["kind"] == "paragraph" and block["page"] == 2
        )
        self.assertIn("Methods", methods["section_path"])
        located = markdown[methods["char_start"] : methods["char_end"]]
        self.assertIn("methods evidence-rich", located)
        self.assertNotIn("text", methods)

    def test_quality_checks_detect_missing_duplicate_and_boilerplate_dominance(
        self,
    ) -> None:
        missing = analyze_markdown(page(1, substantial("one")), expected_pages=2)
        self.assertEqual(missing["status"], "fail")
        self.assertEqual(missing["missing_pages"], [2])
        self.assertTrue(missing["truncated"])

        duplicate_body = substantial("duplicated")
        duplicate = analyze_markdown(
            page(1, duplicate_body) + page(2, duplicate_body), 2
        )
        self.assertEqual(duplicate["status"], "fail")
        self.assertIn("duplicated_pages", duplicate["issue_codes"])
        self.assertEqual(duplicate["duplicate_pages"][0]["similarity"], 1.0)

        repeated_line = (
            "Publisher navigation copyright download metrics and article tools " * 8
        )
        boilerplate_text = "".join(
            page(index, repeated_line + "\n" + f"short unique token {index}")
            for index in range(1, 6)
        )
        boilerplate = analyze_markdown(boilerplate_text, 5)
        self.assertEqual(boilerplate["status"], "fail")
        self.assertIn("boilerplate_dominance", boilerplate["issue_codes"])

        parser_error = analyze_markdown(
            page(1, substantial("otherwise readable")),
            1,
            conversion_errors=["page object failed"],
        )
        self.assertEqual(parser_error["status"], "fail")
        self.assertIn("conversion_errors", parser_error["issue_codes"])

    def test_low_quality_conversion_is_retried_with_forced_ocr(self) -> None:
        calls: list[bool] = []

        def fake_converter(
            path: Path, *, force_full_page_ocr: bool, ocr_engine: str
        ) -> ConversionCandidate:
            calls.append(force_full_page_ocr)
            markdown = (
                page(1, substantial("ocr page one"))
                + page(2, substantial("ocr page two"))
                if force_full_page_ocr
                else page(1, "unreadable")
            )
            return ConversionCandidate(
                markdown=markdown,
                expected_pages=2,
                conversion_status="success",
                conversion_errors=(),
                missing_document_pages=(),
                force_full_page_ocr=force_full_page_ocr,
                settings={
                    "ocr_engine": ocr_engine,
                    "force_full_page_ocr": force_full_page_ocr,
                },
            )

        selected, quality, attempts = select_conversion(
            self.pdf, converter=fake_converter
        )
        self.assertEqual(calls, [False, True])
        self.assertTrue(selected.force_full_page_ocr)
        self.assertEqual(quality["status"], "pass")
        self.assertEqual(len(attempts), 2)
        self.assertTrue(attempts[1]["selected"])

    def test_selective_conversion_exception_is_routed_to_forced_ocr(self) -> None:
        calls: list[bool] = []

        def fake_converter(
            path: Path, *, force_full_page_ocr: bool, ocr_engine: str
        ) -> ConversionCandidate:
            calls.append(force_full_page_ocr)
            if not force_full_page_ocr:
                raise RuntimeError("selective parser failed")
            return ConversionCandidate(
                markdown=page(1, substantial("forced OCR recovered the page")),
                expected_pages=1,
                conversion_status="success",
                conversion_errors=(),
                missing_document_pages=(),
                force_full_page_ocr=True,
                settings={"ocr_engine": ocr_engine, "force_full_page_ocr": True},
            )

        selected, quality, attempts = select_conversion(
            self.pdf, converter=fake_converter
        )
        self.assertEqual(calls, [False, True])
        self.assertTrue(selected.force_full_page_ocr)
        self.assertEqual(quality["status"], "pass")
        self.assertIn("conversion_error", attempts[0])
        self.assertTrue(attempts[1]["selected"])

    def test_prepare_writes_authoritative_identity_versions_quality_and_source_map(
        self,
    ) -> None:
        manifest = self.write_manifest()

        def fake_converter(
            path: Path, *, force_full_page_ocr: bool, ocr_engine: str
        ) -> ConversionCandidate:
            markdown = page(1, "# Study\n\n" + substantial("first")) + page(
                2,
                "## Results\n\n"
                + substantial("second")
                + "\n\n<table><tr><td>Model</td><td>F1</td></tr>"
                "<tr><td>X</td><td>0.91</td></tr></table>",
            )
            return ConversionCandidate(
                markdown=markdown,
                expected_pages=2,
                conversion_status="success",
                conversion_errors=(),
                missing_document_pages=(),
                force_full_page_ocr=force_full_page_ocr,
                settings={
                    "parser": "fake-docling",
                    "ocr_engine": ocr_engine,
                    "force_full_page_ocr": force_full_page_ocr,
                    "table_structure_enabled": True,
                    "multi_column_reading_order": "layout-model",
                },
                table_count=1,
            )

        prepared = prepare_document(
            manifest,
            "paper-0001",
            self.root / "prepared",
            converter=fake_converter,
        )
        self.assertEqual(prepared.quality_status, "pass")
        payload = json.loads(prepared.input_json.read_text(encoding="utf-8"))
        bibliography = json.loads(prepared.bibliography.read_text(encoding="utf-8"))
        processing = json.loads(prepared.processing.read_text(encoding="utf-8"))
        source_map = json.loads(prepared.source_map.read_text(encoding="utf-8"))

        self.assertEqual(bibliography["corpus_id"], "paper-0001")
        self.assertEqual(bibliography["title"], "Verified Fixture Study")
        self.assertEqual(bibliography["doi"], "10.1234/fixture.1")
        self.assertEqual(bibliography["year"], 2026)
        self.assertIn("VERIFIED_SOURCE_METADATA", payload["text"])
        self.assertTrue(processing["complete_document"])
        self.assertIsNone(processing["head_chunks"])
        self.assertIn("docling", processing["software_versions"])
        self.assertTrue(processing["selected_settings"]["table_structure_enabled"])
        for output in processing["outputs"].values():
            output_path = prepared.output_dir / output["path"]
            self.assertEqual(output["sha256"], sha256_file(output_path))
            self.assertEqual(output["bytes"], output_path.stat().st_size)
        self.assertEqual(len(source_map["table_blocks"]), 1)
        validate_source_map(payload["text"], source_map)

    def test_publication_command_has_no_chunk_limit_and_uses_run_specific_output(
        self,
    ) -> None:
        command = build_ontocast_command(
            "/venv/bin/ontocast",
            Path("run/ontocast.env"),
            Path("run/input"),
        )
        self.assertNotIn("--head-chunks", command)
        self.assertEqual(command[-2:], ["--input-path", "run/input"])

        config = effective_config(
            "fixed", self.root / "output", "http://127.0.0.1:9000/v1"
        )
        self.assertIn("LLM_BASE_URL=http://127.0.0.1:9000/v1", config)
        self.assertIn(
            f"ONTOCAST_WORKING_DIRECTORY={(self.root / 'output').resolve()}", config
        )
        self.assertIn("ONTOCAST_ONTOLOGY_DIRECTORY=", config)

    def test_tracked_long_and_multicase_markdown_cover_every_page_and_table(
        self,
    ) -> None:
        paths = [
            REPO_ROOT / "markdown" / "10.3390_machines14010026" / "document.md",
            REPO_ROOT / "markdown" / "10.3390_pr14050772" / "document.md",
        ]
        report = audit_markdown_files(paths)
        self.assertEqual(
            report["summary"], {"documents": 2, "passed": 2, "failed": 0, "errors": 0}
        )
        expected_pages = {
            "10.3390_machines14010026": 37,
            "10.3390_pr14050772": 25,
        }
        for document in report["documents"]:
            doi = Path(document["path"]).parent.name
            self.assertEqual(
                document["quality"]["observed_page_markers"],
                list(range(1, expected_pages[doi] + 1)),
            )
            self.assertFalse(document["quality"]["truncated"])
            self.assertGreater(document["source_map_summary"]["blocks"], 100)
            self.assertGreater(document["source_map_summary"]["tables"], 0)

    def test_legacy_wrappers_default_to_complete_documents(self) -> None:
        bash_wrappers = [
            REPO_ROOT / "pipeline" / "run_extraction.sh",
            REPO_ROOT / "pipeline" / "full_mode" / "run_full_extraction.sh",
        ]
        powershell_wrappers = [
            REPO_ROOT / "pipeline" / "run_extraction.ps1",
            REPO_ROOT / "pipeline" / "full_mode" / "run_full_extraction.ps1",
        ]
        for path in bash_wrappers:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("DEFAULT_HEAD_CHUNKS", text)
            self.assertIn("chunks: complete document", text)
            self.assertIn("ontocast_args+=(--head-chunks", text)
        for path in powershell_wrappers:
            text = path.read_text(encoding="utf-8")
            self.assertIn("[int]$HeadChunks = 0", text)
            self.assertIn("chunks: complete document", text)


if __name__ == "__main__":
    unittest.main()
