"""Stock OntoCast subscription configuration; no live provider requests."""
from __future__ import annotations

import asyncio
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pipeline.fulltext_run import effective_config, run_complete_extraction
from pipeline.subscription_proxy import (
    PROXY_API_KEY,
    SubscriptionProxyError,
    require_subscription_proxy,
    subscription_environment,
    validate_subscription_settings,
)
from scripts.apply_local_patches import LocalPatcher, validate_ontocast
from scripts.install_submodule_stack import install_ontocast


class SubscriptionProxyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = patch.dict(os.environ, {"OPENAI_API_KEY": "", "LLM_API_KEY": ""})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_placeholder_is_allowed_and_child_settings_are_pinned(self) -> None:
        with patch.dict(os.environ, {
            "LLM_API_KEY": PROXY_API_KEY,
            "LLM_PROVIDER": "ollama",
            "ONTOLOGY_CRITIC_PASSES": "5",
        }):
            env = subscription_environment("http://127.0.0.1:9000/v1")
        self.assertEqual(env["LLM_API_KEY"], PROXY_API_KEY)
        self.assertEqual(env["LLM_BASE_URL"], "http://127.0.0.1:9000/v1")
        self.assertEqual(env["LLM_PROVIDER"], "openai")
        self.assertEqual(env["ONTOLOGY_CRITIC_PASSES"], "0")

    def test_real_keys_are_rejected_before_network_access(self) -> None:
        for name in ("OPENAI_API_KEY", "LLM_API_KEY"):
            with self.subTest(name=name), patch.dict(os.environ, {name: "not-a-real-test-key"}):
                with patch("urllib.request.urlopen") as urlopen:
                    with self.assertRaises(SubscriptionProxyError):
                        require_subscription_proxy("http://127.0.0.1:8977/v1")
                    urlopen.assert_not_called()

    def test_only_local_proxy_urls_are_allowed(self) -> None:
        for base in (
            "http://127.0.0.1:8977/v1", "http://localhost:8977/v1/", "http://[::1]:8977/v1"
        ):
            validate_subscription_settings(base)
        for base in (
            "https://api.openai.com/v1", "http://example.com/v1",
            "http://user:secret@127.0.0.1/v1", "http://127.0.0.1/v1?key=x",
            "http://127.0.0.1/v1#fragment", "http://127.0.0.1/wrong",
            "http://[invalid/v1", "http://127.0.0.1:bad/v1",
        ):
            with self.subTest(base=base), self.assertRaises(SubscriptionProxyError):
                validate_subscription_settings(base)

    def test_health_check_requires_the_subscription_provider(self) -> None:
        for provider, accepted in (("openai-codex", True), ("openai", False)):
            response = io.BytesIO(json.dumps({"provider": provider}).encode())
            with patch("urllib.request.urlopen", return_value=response) as urlopen:
                if accepted:
                    require_subscription_proxy("http://127.0.0.1:9000/v1/")
                else:
                    with self.assertRaisesRegex(SubscriptionProxyError, "not the Pi Codex"):
                        require_subscription_proxy("http://127.0.0.1:9000/v1/")
                urlopen.assert_called_once_with("http://127.0.0.1:9000/health", timeout=5)

    def test_unreachable_proxy_has_an_actionable_error(self) -> None:
        with patch("urllib.request.urlopen", side_effect=OSError("offline")):
            with self.assertRaisesRegex(SubscriptionProxyError, "Start pipeline/tools/"):
                require_subscription_proxy("http://127.0.0.1:9000/v1")

    def test_stock_ontocast_calls_the_local_endpoint_with_the_placeholder(self) -> None:
        try:
            from ontocast.config import Config, LLMConfig
            from ontocast.tool.llm import LLMTool
            import langchain_openai  # noqa: F401
        except ImportError:
            self.skipTest("Install the OntoCast openai extra for the SDK integration test")
        requests = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                requests.append((self.path, self.headers.get("Authorization"), body))
                payload = json.dumps({
                    "id": "chatcmpl-offline-test",
                    "object": "chat.completion",
                    "created": 0,
                    "model": body["model"],
                    "choices": [{
                        "index": 0,
                        "message": {"role": "assistant", "content": "subscription-ok"},
                        "finish_reason": "stop",
                    }],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
                }).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base_url = f"http://127.0.0.1:{server.server_port}/v1"
            config = Config()
            config.tool_config.llm_config = LLMConfig(
                provider="openai", model_name="gpt-4o-mini", base_url=base_url,
                api_key=PROXY_API_KEY, cache_enabled=False, max_retries=0,
            )
            config.validate_llm_config()

            async def complete():
                tool = await LLMTool.acreate(config=config.tool_config.llm_config)
                return await tool.complete("Offline compatibility test")

            self.assertEqual(asyncio.run(complete()), "subscription-ok")
            self.assertEqual(requests[0][0], "/v1/chat/completions")
            self.assertEqual(requests[0][1], f"Bearer {PROXY_API_KEY}")
            self.assertEqual(len(requests), 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_both_config_files_pass_the_upstream_audit(self) -> None:
        try:
            from ontocast.config.env_audit import audit_assignments
        except ImportError:
            self.skipTest("Requires OntoCast 0.8.2")
        for condition in ("fixed", "evolved"):
            text = effective_config(condition, "http://127.0.0.1:8977/v1")
            assignments = dict(
                line.split("=", 1) for line in text.splitlines()
                if line and not line.startswith("#")
            )
            self.assertTrue(audit_assignments(assignments).ok, condition)

    @unittest.expectedFailure
    def test_stock_in_memory_store_preserves_rdf12_provenance(self) -> None:
        """T-RUN-10: upstream 0.8.2 rejects triple terms while persisting facts."""
        try:
            from rdflib import RDF, URIRef
            from ontocast.onto.content_unit import ContentUnit
            from ontocast.onto.rdfgraph import RDFGraph
            from ontocast.tool.agg.rewriter import GraphRewriter
            from ontocast.tool.triple_manager.in_memory import InMemoryTripleStoreManager
        except ImportError:
            self.skipTest("Requires OntoCast 0.8.2")
        graph = RDFGraph()
        graph.add((URIRef("https://example.org/pump"), RDF.type, URIRef("https://example.org/Machine")))
        unit = ContentUnit(text="A pump", index=0, doc_iri=URIRef("https://example.org/doc"), graph=graph)
        merged = GraphRewriter().merge_graphs_with_provenance([unit], mapping={})
        InMemoryTripleStoreManager().serialize(merged, graph_uri="https://example.org/facts")

    def test_ontocast_validator_never_changes_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            submodule = root / "external" / "ontocast"
            submodule.mkdir(parents=True)
            (submodule / ".git").touch()
            sentinel = submodule / "config.py"
            sentinel.write_bytes(b"stock upstream\r\n")
            patcher = LocalPatcher(root)
            validate_ontocast(patcher)
            validate_ontocast(patcher)
            self.assertEqual(sentinel.read_bytes(), b"stock upstream\r\n")
            self.assertEqual(patcher.changed_files(), [])

    def test_setup_installs_the_new_cli_and_provider_extras(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "external" / "ontocast").mkdir(parents=True)
            with patch("scripts.install_submodule_stack.uv_pip_install") as install:
                install_ontocast(root, no_deps=False)
            arguments = install.call_args.args[1]
            self.assertIn("[server,openai,doc-processing,semantic-chunking]", arguments[-1])

    @unittest.skipUnless(shutil.which("bash"), "Requires Bash")
    def test_bash_runners_pass_native_flags_and_propagate_failures(self) -> None:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"provider":"openai-codex"}')

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                repo = Path(__file__).resolve().parents[2]
                bin_dir = root / "bin"
                bin_dir.mkdir()
                fake = bin_dir / "ontocast"
                fake.write_text(f"#!{sys.executable}\n" + '''import json, os, sys
from pathlib import Path
args = sys.argv[1:]
Path(os.environ["CAPTURE"]).write_text(json.dumps({
    "args": args, "key": os.environ.get("LLM_API_KEY"),
    "base": os.environ.get("LLM_BASE_URL"),
    "ontology_critic": os.environ.get("ONTOLOGY_CRITIC_PASSES"),
    "provider": os.environ.get("LLM_PROVIDER"),
}))
code = int(os.environ.get("FAKE_EXIT", "0"))
if not code:
    out = Path(args[args.index("--output-dir") + 1])
    (out / "paper.facts.ttl").touch()
    (out / "paper.domain.ontology.ttl").touch()
sys.exit(code)
''', encoding="utf-8")
                fake.chmod(0o755)
                for relative in (
                    "pipeline/subscription_proxy.py", "pipeline/run_extraction.sh",
                    "pipeline/ontocast_config.env", "pipeline/full_mode/run_full_extraction.sh",
                    "pipeline/full_mode/ontocast_full_config.env",
                ):
                    target = root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(repo / relative, target)
                base_url = f"http://127.0.0.1:{server.server_port}/v1"
                (root / ".env").write_text(
                    f"LLM_BASE_URL={base_url}\nLLM_API_KEY=subscription-proxy\nONTOLOGY_CRITIC_PASSES=9\n",
                    encoding="utf-8",
                )
                pdf = root / "paper with spaces.pdf"
                pdf.write_bytes(b"fixture")
                capture = root / "capture.json"
                env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                       "PYTHON_BIN": sys.executable, "CAPTURE": str(capture)}
                for wrapper in ("pipeline/run_extraction.sh", "pipeline/full_mode/run_full_extraction.sh"):
                    result = subprocess.run(
                        ["bash", str(root / wrapper), str(pdf), "2"], env=env,
                        capture_output=True, text=True, timeout=15,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    recorded = json.loads(capture.read_text())
                    self.assertEqual(recorded["key"], PROXY_API_KEY)
                    self.assertEqual(recorded["base"], base_url)
                    self.assertEqual(recorded["ontology_critic"], "0")
                    self.assertEqual(recorded["provider"], "openai")
                    self.assertIn("process", recorded["args"])
                    self.assertIn("--keep-provenance", recorded["args"])
                    self.assertEqual(recorded["args"][-2:], ["--head-chunks", "2"])
                    self.assertEqual(recorded["args"][recorded["args"].index("--exclude-sections") + 1], "")
                    failure = subprocess.run(
                        ["bash", str(root / wrapper), str(pdf)], env={**env, "FAKE_EXIT": "7"},
                        capture_output=True, text=True, timeout=15,
                    )
                    self.assertEqual(failure.returncode, 7)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_publication_runner_detects_upstream_outputs_and_pins_child_env(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "document.json"
            source.write_text('{"text": "fixture"}', encoding="utf-8")
            prepared = SimpleNamespace(quality_status="pass", input_json=source)
            run_dir = root / "run"

            def finish():
                (run_dir / "output" / "document.facts.ttl").touch()
                (run_dir / "output" / "document.domain.ontology.ttl").touch()
                return 0

            with (
                patch("pipeline.fulltext_run.prepare_document", return_value=prepared),
                patch("pipeline.fulltext_run.require_subscription_proxy"),
                patch("pipeline.fulltext_run.subscription_proxy_base", return_value="http://127.0.0.1:9000/v1"),
                patch("pipeline.fulltext_run.shutil.which", return_value="/venv/bin/ontocast"),
                patch("pipeline.fulltext_run.subprocess.Popen") as popen,
            ):
                popen.return_value.stdout = io.StringIO("fixture log\n")
                popen.return_value.wait.side_effect = finish
                result = run_complete_extraction(
                    condition="evolved", manifest=root / "manifest.json", corpus_id="fixture",
                    run_dir=run_dir, ocr_engine="easyocr", require_verified=True,
                    prepare_only=False,
                )
            self.assertEqual(result, 0)
            command = popen.call_args.args[0]
            self.assertIn("process", command)
            self.assertIn("--keep-provenance", command)
            self.assertNotIn("--head-chunks", command)
            self.assertEqual(popen.call_args.kwargs["env"]["LLM_API_KEY"], PROXY_API_KEY)
            self.assertEqual(popen.call_args.kwargs["env"]["ONTOLOGY_CRITIC_PASSES"], "0")
            metadata = json.loads((run_dir / "fulltext-run.json").read_text())
            self.assertEqual(metadata["status"], "completed")
            self.assertEqual(len(metadata["facts"]), 1)
            self.assertEqual(len(metadata["ontologies"]), 1)


if __name__ == "__main__":
    unittest.main()
