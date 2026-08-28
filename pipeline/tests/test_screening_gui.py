from __future__ import annotations

import csv
import json
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from screening import gui_server


class ScreeningGuiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.sheet = self.base / "title_abstract_R1.csv"
        self.write_sheet()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def row(self, candidate_id: str, title: str) -> dict[str, str]:
        row = {header: "" for header in gui_server.reviewer_headers()}
        row.update(
            {
                "screening_candidate_id": candidate_id,
                "scopus_paper_id": candidate_id.removeprefix("eid:"),
                "doi": "10.1000/example",
                "title": title,
                "abstract": f"Abstract for {title}.",
                "year": "2026",
                "source_strata": "S1a",
                "source_url": "https://example.test/record",
                "screening_batch_id": "test-batch",
                "source_union_sha256": "0" * 64,
                "protocol_version": "v1",
                "screening_stage": "title_abstract",
                "reviewer_id": "R1",
                "full_text_status": "not_assessed",
                "bibliographic_match": "not_assessed",
            }
        )
        return row

    def write_sheet(self) -> None:
        rows = [self.row("eid:1", "First candidate"), self.row("eid:2", "Second candidate")]
        with self.sheet.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=gui_server.reviewer_headers(), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def test_store_saves_valid_decision_atomically_and_rejects_stale_writes(self) -> None:
        store = gui_server.ScreeningStore(self.sheet, "R1")
        self.assertEqual(store.state()["total"], 2)
        self.assertEqual(store.state()["completed"], 0)

        response = store.update(
            0,
            0,
            {
                "decision": "exclude",
                "primary_exclusion_reason": "out_of_scope_target",
                "exclusion_detail": "clinical_human",
                "confidence": "high",
                "full_text_url": "",
                "full_text_retrieval_date": "",
                "full_text_status": "not_assessed",
                "bibliographic_match": "not_assessed",
                "notes": "Clearly clinical prediction.",
            },
        )
        self.assertEqual(response["revision"], 1)
        self.assertEqual(response["completed"], 1)
        self.assertEqual(response["record"]["decision"], "exclude")
        self.assertEqual(response["record"]["primary_exclusion_reason"], "out_of_scope_target")
        self.assertRegex(response["record"]["decision_date"], r"^\d{4}-\d{2}-\d{2}$")

        with self.sheet.open(encoding="utf-8", newline="") as handle:
            persisted = list(csv.DictReader(handle))
        self.assertEqual(persisted[0]["decision"], "exclude")
        self.assertEqual(persisted[0]["exclusion_detail"], "clinical_human")

        with self.assertRaises(gui_server.RevisionConflict):
            store.update(1, 0, {"decision": "include"})
        with self.assertRaisesRegex(gui_server.ScreeningGuiError, "requires one primary reason"):
            store.update(1, 1, {"decision": "exclude"})
        with self.assertRaisesRegex(gui_server.ScreeningGuiError, "full-text reason"):
            store.update(
                1,
                1,
                {
                    "decision": "exclude",
                    "primary_exclusion_reason": "unavailable_or_mismatched_usable_oa_full_text",
                },
            )

    def test_full_text_sheet_exposes_verification_fields(self) -> None:
        row = self.row("eid:full", "Full-text candidate")
        row.update(
            {
                "screening_stage": "full_text",
                "full_text_url": "https://example.test/full-text",
                "full_text_retrieval_date": "2026-08-25",
                "full_text_status": "usable",
                "bibliographic_match": "yes",
            }
        )
        full_text_sheet = self.base / "full_text_R1.csv"
        with full_text_sheet.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=gui_server.reviewer_headers(), lineterminator="\n")
            writer.writeheader()
            writer.writerow(row)

        store = gui_server.ScreeningStore(full_text_sheet, "R1")
        record = store.record(0)["record"]
        self.assertEqual(record["screening_stage"], "full_text")
        self.assertEqual(record["source_url"], "https://example.test/record")
        self.assertEqual(record["full_text_url"], "https://example.test/full-text")
        self.assertEqual(record["bibliographic_match"], "yes")

    def test_local_http_api_serves_assets_and_updates_single_reviewer_sheet(self) -> None:
        store = gui_server.ScreeningStore(self.sheet, "R1")
        server = gui_server.create_server(store, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base_url = f"http://127.0.0.1:{server.server_port}"
        try:
            with urllib.request.urlopen(f"{base_url}/api/state") as response:
                state = json.loads(response.read())
                self.assertEqual(response.headers["Cache-Control"], "no-store")
            self.assertEqual(state["reviewer_id"], "R1")
            self.assertEqual(len(state["records"]), 2)
            with urllib.request.urlopen(f"{base_url}/api/record/0") as response:
                title_abstract_record = json.loads(response.read())["record"]
            self.assertEqual(title_abstract_record["source_url"], "")
            self.assertEqual(title_abstract_record["doi"], "10.1000/example")

            with urllib.request.urlopen(f"{base_url}/") as response:
                page = response.read().decode("utf-8")
                self.assertIn("Human screening", page)
                self.assertIn("Content-Security-Policy", response.headers)

            payload = {
                "revision": state["revision"],
                "record": {
                    "decision": "include",
                    "primary_exclusion_reason": "",
                    "exclusion_detail": "",
                    "confidence": "medium",
                    "full_text_url": "",
                    "full_text_retrieval_date": "",
                    "full_text_status": "not_assessed",
                    "bibliographic_match": "not_assessed",
                    "notes": "Plausibly eligible.",
                },
            }
            request = urllib.request.Request(
                f"{base_url}/api/record/1",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(request) as response:
                saved = json.loads(response.read())
            self.assertEqual(saved["record"]["decision"], "include")
            self.assertEqual(saved["completed"], 1)

            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen(f"{base_url}/not-a-route")
            self.assertEqual(context.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
