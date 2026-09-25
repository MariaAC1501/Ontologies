from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from annotation.gold import AnnotationError, GoldWorkspace, empty_annotation, validate_annotation
from annotation.server import GoldServer
from pipeline.fulltext import build_source_map, sha256_file


class GoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pdf = self.root / "article.pdf"
        self.pdf.write_bytes(b"%PDF-1.7\nfixture\n")
        self.document = "<!-- PDF_PAGE: 1 -->\n\n# Methods\n\nThe pump uses vibration data and a neural network for fault detection.\n\n<!-- PDF_PAGE: 2 -->\n\nThe model and sensor work together.\n"
        prepared = self.root / "prepared" / "paper-1"
        prepared.mkdir(parents=True)
        (prepared / "document.md").write_text(self.document, encoding="utf-8")
        (prepared / "source-map.json").write_text(json.dumps(build_source_map(self.document, "paper-1")), encoding="utf-8")
        (prepared / "quality.json").write_text('{"status":"pass"}', encoding="utf-8")
        (prepared / "bibliographic-identity.json").write_text(json.dumps({
            "corpus_id":"paper-1", "doi":"10.1234/test", "pdf_sha256":sha256_file(self.pdf),
            "title":"Fixture study", "year":2026, "partition":"held_out", "manifest_partition_frozen":True,
        }), encoding="utf-8")
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(json.dumps({"schema_version":"fulltext-corpus-manifest/1.0", "base_dir":".",
            "partition_frozen":True, "records":[{
                "corpus_id":"paper-1", "bibliographic_status":"verified", "partition":"held_out",
                "title":"Fixture study", "doi":"10.1234/test", "year":2026,
                "pdf_path":"article.pdf", "pdf_sha256":sha256_file(self.pdf),
            }]}), encoding="utf-8")
        self.output = self.root / "work"
        self.work = GoldWorkspace(self.manifest, self.root / "prepared", self.output, "R1")

    def assertion(self, wording, quote=None, page=1):
        quote = quote or "The pump uses vibration data and a neural network for fault detection."
        body = self.work.documents["paper-1"][2][page][1]
        index = body.index(quote)
        return {"status":"present", "raw":wording, "normalized":"", "evidence":[
            {"source":"text", "page":page, "section":"Methods", "quote":quote, "start":index, "end":index+len(quote)},
        ]}

    def case(self):
        return {"id":"case-1", "boundary":self.assertion("diagnosis of pump faults"),
                "item":self.assertion("pump"), "function":self.assertion("fault detection"),
                "data":[{"id":"data-1", "value":self.assertion("vibration data")}],
                "models":[{"id":"model-1", "value":self.assertion("neural network")}],
                "configuration":{**self.assertion("single neural network"), "normalized":"single"},
                "notes":""}

    def test_manifest_gates_and_partition(self):
        raw = json.loads(self.manifest.read_text())
        raw["partition_frozen"] = False
        self.manifest.write_text(json.dumps(raw))
        with self.assertRaisesRegex(AnnotationError, "Freeze the partition"):
            GoldWorkspace(self.manifest, self.root / "prepared", self.output, "R2")
        raw["partition_frozen"] = True
        raw["records"][0]["bibliographic_status"] = "provisional"
        self.manifest.write_text(json.dumps(raw))
        with self.assertRaisesRegex(AnnotationError, "verified bibliographic"):
            GoldWorkspace(self.manifest, self.root / "prepared", self.output, "R2")
        raw["records"][0]["bibliographic_status"] = "verified"
        raw["records"][0]["pdf_sha256"] = "0"*64
        self.manifest.write_text(json.dumps(raw))
        with self.assertRaisesRegex(Exception, "checksum mismatch"):
            GoldWorkspace(self.manifest, self.root / "prepared", self.output, "R2")

    def test_independent_drafts_validation_timer_and_lock(self):
        annotation = self.work.get("paper-1")["annotation"]
        annotation["cases"].append(self.case())
        self.work.update("paper-1", 0, annotation=annotation)
        other = GoldWorkspace(self.manifest, self.root / "prepared", self.output, "R2")
        self.assertEqual(other.get("paper-1")["annotation"]["cases"], [])
        with self.assertRaisesRegex(AnnotationError, "Start the timer"):
            self.work.update("paper-1", 1, action="submit")
        self.assertEqual(self.work.get("paper-1")["state"], "draft")
        self.work.update("paper-1", 1, action="start")
        self.work.update("paper-1", 2, action="pause")
        result = self.work.update("paper-1", 3, action="submit")
        self.assertEqual(result["state"], "submitted")
        self.assertEqual(len(result["timer"]["intervals"]), 1)
        with self.assertRaisesRegex(AnnotationError, "cannot be edited"):
            self.work.update("paper-1", 4, annotation=annotation)
        with self.assertRaisesRegex(AnnotationError, "Revision conflict"):
            self.work.update("paper-1", 1, annotation=annotation)

    def test_exact_evidence_status_and_zero_case(self):
        annotation = empty_annotation("paper-1", "R1", self.work.documents["paper-1"][1])
        annotation["cases"] = [self.case()]
        pages = self.work.documents["paper-1"][2]
        validate_annotation(annotation, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        wrong = copy.deepcopy(annotation)
        wrong["cases"][0]["item"]["evidence"][0]["page"] = 2
        with self.assertRaisesRegex(AnnotationError, "exact span"):
            validate_annotation(wrong, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        wrong = copy.deepcopy(annotation)
        wrong["cases"][0]["models"].append({"id":"model-2", "value":self.assertion("second model")})
        with self.assertRaisesRegex(AnnotationError, "configuration conflicts"):
            validate_annotation(wrong, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        wrong = copy.deepcopy(annotation)
        wrong["cases"][0]["models"][0]["value"]["status"] = "not_reported"
        with self.assertRaisesRegex(AnnotationError, "non-present"):
            validate_annotation(wrong, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        blank = empty_annotation("paper-1", "R1", annotation["source_sha256"])
        with self.assertRaisesRegex(AnnotationError, "zero eligible cases"):
            validate_annotation(blank, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        blank["zero_case_reason"] = "No evaluated maintenance case found after full-text check."
        validate_annotation(blank, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        unfinished = copy.deepcopy(annotation)
        evidence = unfinished["cases"][0]["item"]["evidence"][0]
        evidence.update({"quote":"Quote not yet located", "start":None, "end":None})
        validate_annotation(unfinished, "paper-1", "R1", annotation["source_sha256"], pages)
        with self.assertRaisesRegex(AnnotationError, "exact span"):
            validate_annotation(unfinished, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)
        evidence.update({"source":"pdf", "quote":"PDF-only phrase", "start":None, "end":None})
        validate_annotation(unfinished, "paper-1", "R1", annotation["source_sha256"], pages, complete=True)

    def test_http_routes_and_csrf(self):
        server = GoldServer(self.work, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        port = server.server_port
        base = f"http://127.0.0.1:{port}"
        with urlopen(base + "/api/articles") as response:
            info = json.load(response)
        self.assertEqual(len(info["articles"]), 1)
        with urlopen(base + "/api/article/paper-1") as response:
            self.assertEqual(json.load(response)["pages"][0]["number"], 1)
        with urlopen(base + "/api/article/paper-1/pdf") as response:
            self.assertEqual(response.read(), self.pdf.read_bytes())
        payload = json.dumps({"revision":0,"annotation":self.work.get("paper-1")["annotation"]}).encode()
        req = Request(base + "/api/article/paper-1", data=payload, method="PUT",
                      headers={"Origin":base,"X-Annotation-Token":info["token"],"Content-Type":"application/json"})
        with urlopen(req) as response:
            self.assertEqual(json.load(response)["revision"], 1)
        with self.assertRaises(HTTPError) as failed:
            urlopen(req)
        self.assertEqual(failed.exception.code, 409)
        no_token = Request(base + "/api/article/paper-1", data=payload, method="PUT", headers={"Origin":base})
        with self.assertRaises(HTTPError) as failed:
            urlopen(no_token)
        self.assertEqual(failed.exception.code, 403)
        with self.assertRaises(HTTPError) as failed:
            urlopen(base + "/api/article/../paper-1")
        self.assertEqual(failed.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
