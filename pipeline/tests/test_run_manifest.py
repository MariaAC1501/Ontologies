import contextlib
import copy
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from pipeline import run_manifest


class RunManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        (self.base / "corpus").mkdir()
        (self.base / "corpus" / "b.txt").write_text("beta\n", encoding="utf-8")
        (self.base / "corpus" / "a.txt").write_text("alpha\n", encoding="utf-8")
        (self.base / "config.toml").write_text("mode = 'fixed'\n", encoding="utf-8")
        (self.base / "prompt.txt").write_text("Extract facts.\n", encoding="utf-8")
        (self.base / "ontology.ttl").write_text("@prefix x: <urn:x:> .\n", encoding="utf-8")
        (self.base / "output.json").write_text("{}\n", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def build(self, **overrides):
        arguments = {
            "base_dir": self.base,
            "inputs": ["corpus/*.txt"],
            "config": ["config.toml"],
            "prompts": ["prompt.txt"],
            "ontologies": ["ontology.ttl"],
            "outputs": ["output.json"],
            "provider": "example-provider",
            "model": "example-model",
            "settings": {"temperature": "0", "max_tokens": "4096", "api_key": "do-not-emit"},
            "parser_version": "parser-v2",
            "normalization_version": "norm-v1",
            "created_at": "2026-01-02T03:04:05+00:00",
        }
        arguments.update(overrides)
        return run_manifest.build_manifest(**arguments)

    def test_manifest_is_stably_ordered_and_redacts_sensitive_settings(self):
        # This file is neither requested nor implicitly loaded.
        (self.base / ".env").write_text("API_KEY=super-secret-value\n", encoding="utf-8")
        manifest = self.build()

        paths = [item["path"] for item in manifest["compatibility"]["artifacts"]["inputs"]]
        self.assertEqual(paths, ["corpus/a.txt", "corpus/b.txt"])
        request = manifest["compatibility"]["request"]
        self.assertEqual(request["settings"]["api_key"], run_manifest.REDACTED)
        self.assertEqual(request["settings"]["max_tokens"], "4096")
        serialized = run_manifest.stable_json(manifest)
        self.assertNotIn("do-not-emit", serialized)
        self.assertNotIn("super-secret-value", serialized)
        self.assertEqual(serialized, run_manifest.stable_json(json.loads(serialized)))
        self.assertEqual(manifest["metadata"]["timestamps"]["created_at"], "2026-01-02T03:04:05Z")

    def test_equivalent_argument_order_produces_identical_manifest_bytes(self):
        first = self.build(inputs=["corpus/b.txt", "corpus/a.txt"])
        second = self.build(inputs=["corpus/a.txt", "corpus/b.txt"])
        self.assertEqual(run_manifest.stable_json(first), run_manifest.stable_json(second))

    def test_checksums_outputs_and_deduplicates_overlapping_specs(self):
        records = run_manifest.artifact_records(["corpus", "corpus/a.txt"], self.base)
        self.assertEqual([record["path"] for record in records], ["corpus/a.txt", "corpus/b.txt"])
        self.assertEqual(
            records[0]["sha256"],
            "b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060",
        )
        manifest = self.build()
        self.assertEqual(manifest["outputs"][0]["path"], "output.json")
        self.assertEqual(manifest["outputs"][0]["size"], 3)

    def test_missing_unmatched_empty_outside_symlink_and_secret_files_are_explicit_errors(self):
        (self.base / "empty").mkdir()
        outside = self.base.parent / f"{self.base.name}-outside.txt"
        outside.write_text("outside", encoding="utf-8")
        (self.base / "credentials.json").write_text("{}", encoding="utf-8")
        (self.base / ".env").write_text("API_KEY=must-not-be-read\n", encoding="utf-8")
        try:
            cases = ["missing.txt", "*.does-not-exist", "empty", str(outside), "credentials.json", ".env"]
            for spec in cases:
                with self.subTest(spec=spec), self.assertRaises(run_manifest.ManifestError):
                    run_manifest.resolve_file_specs([spec], self.base)
            with self.assertRaisesRegex(run_manifest.ManifestError, "refusing to read"):
                run_manifest.resolve_file_specs([".env"], self.base)
            try:
                (self.base / "linked.txt").symlink_to(self.base / "prompt.txt")
            except (OSError, NotImplementedError):
                pass
            else:
                with self.assertRaisesRegex(run_manifest.ManifestError, "symbolic links"):
                    run_manifest.resolve_file_specs(["linked.txt"], self.base)
        finally:
            outside.unlink()

    def test_parse_settings_rejects_bad_or_duplicate_values(self):
        self.assertEqual(
            run_manifest.parse_settings(["temperature=0", "access_token=secret", "max_tokens=20"]),
            {"access_token": run_manifest.REDACTED, "max_tokens": "20", "temperature": "0"},
        )
        with self.assertRaises(run_manifest.ManifestError):
            run_manifest.parse_settings(["temperature"])
        with self.assertRaises(run_manifest.ManifestError):
            run_manifest.parse_settings(["temperature=0", "temperature=1"])

    def test_compare_ignores_variable_metadata_and_outputs(self):
        reference = self.build()
        candidate = copy.deepcopy(reference)
        candidate["metadata"]["timestamps"]["created_at"] = "2099-01-01T00:00:00Z"
        candidate["metadata"]["git"]["dirty"] = not candidate["metadata"]["git"]["dirty"]
        candidate["outputs"] = []
        self.assertEqual(run_manifest.compare_compatibility(reference, candidate), [])

        candidate["compatibility"]["request"]["model"] = "different-model"
        candidate["compatibility"]["versions"]["normalization"] = "norm-v2"
        candidate["compatibility"]["artifacts"]["ontologies"][0]["sha256"] = "0" * 64
        differences = run_manifest.compare_compatibility(reference, candidate)
        self.assertTrue(any("request.model" in item and "different-model" in item for item in differences))
        self.assertTrue(any("versions.normalization" in item for item in differences))
        self.assertTrue(any("ontologies ontology.ttl: checksum differs" in item for item in differences))

    def test_validate_detects_ontology_drift_missing_inputs_and_optional_output_drift(self):
        manifest = self.build()
        self.assertEqual(run_manifest.validate_current_files(manifest, self.base), [])

        (self.base / "ontology.ttl").write_text("changed\n", encoding="utf-8")
        (self.base / "corpus" / "a.txt").unlink()
        (self.base / "output.json").write_text("changed output\n", encoding="utf-8")
        differences = run_manifest.validate_current_files(manifest, self.base)
        self.assertTrue(any("ontologies ontology.ttl: checksum changed" in item for item in differences))
        self.assertTrue(any("inputs corpus/a.txt: file is missing" in item for item in differences))
        self.assertFalse(any("output.json" in item for item in differences))
        with_outputs = run_manifest.validate_current_files(manifest, self.base, check_outputs=True)
        self.assertTrue(any("outputs output.json: checksum changed" in item for item in with_outputs))

    def test_cli_create_validate_and_compare_exit_codes(self):
        manifest_path = self.base / "manifest.json"
        create_args = [
            "create", "--manifest", str(manifest_path), "--base-dir", str(self.base),
            "--input", "corpus/*.txt", "--config", "config.toml", "--prompt", "prompt.txt",
            "--ontology", "ontology.ttl", "--output", "output.json", "--provider", "provider",
            "--model", "model", "--setting", "temperature=0", "--parser-version", "parser-1",
            "--normalization-version", "norm-1", "--created-at", "2026-02-03T04:05:06Z",
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_manifest.main(create_args), 0)
        self.assertTrue(manifest_path.is_file())

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = run_manifest.main(["validate", str(manifest_path), "--base-dir", str(self.base), "--model", "other"])
        self.assertEqual(code, 1)
        self.assertIn("compatibility.request.model", output.getvalue())

        candidate = json.loads(manifest_path.read_text(encoding="utf-8"))
        candidate["metadata"]["timestamps"]["created_at"] = "2030-01-01T00:00:00Z"
        candidate_path = self.base / "candidate.json"
        run_manifest.write_manifest(candidate_path, candidate)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_manifest.main(["compare", str(manifest_path), str(candidate_path)]), 0)

    def test_structure_rejects_unredacted_secret_and_unsorted_records(self):
        manifest = self.build()
        manifest["compatibility"]["request"]["settings"]["api_key"] = "unsafe"
        with self.assertRaisesRegex(run_manifest.ManifestError, "unredacted"):
            run_manifest.validate_structure(manifest)

        manifest = self.build()
        manifest["compatibility"]["artifacts"]["inputs"].reverse()
        with self.assertRaisesRegex(run_manifest.ManifestError, "sorted"):
            run_manifest.validate_structure(manifest)


class GitMetadataTests(unittest.TestCase):
    def git(self, cwd, *args):
        return subprocess.run(
            ["git", *args], cwd=cwd, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()

    def init_repository(self, path):
        path.mkdir(parents=True)
        self.git(path, "init")
        self.git(path, "config", "user.email", "tests@example.invalid")
        self.git(path, "config", "user.name", "Manifest Tests")

    @unittest.skipUnless(shutil.which("git"), "git is required")
    def test_clean_dirty_and_initialized_and_uninitialized_submodules(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            child = temporary_path / "child"
            root = temporary_path / "root"
            self.init_repository(child)
            (child / "tracked.txt").write_text("child\n", encoding="utf-8")
            self.git(child, "add", "tracked.txt")
            self.git(child, "commit", "-m", "child")

            self.init_repository(root)
            (root / "tracked.txt").write_text("root\n", encoding="utf-8")
            self.git(root, "add", "tracked.txt")
            self.git(root, "commit", "-m", "root")
            self.git(root, "-c", "protocol.file.allow=always", "submodule", "add", str(child), "external/child")
            self.git(root, "commit", "-am", "add submodule")

            metadata = run_manifest.git_metadata(root)
            self.assertTrue(metadata["present"])
            self.assertFalse(metadata["dirty"])
            self.assertEqual(metadata["root_revision"], self.git(root, "rev-parse", "HEAD"))
            self.assertEqual(len(metadata["submodules"]), 1)
            initialized = metadata["submodules"][0]
            self.assertTrue(initialized["initialized"])
            self.assertEqual(initialized["revision"], self.git(child, "rev-parse", "HEAD"))
            self.assertFalse(initialized["dirty"])

            (root / "untracked.txt").write_text("dirty\n", encoding="utf-8")
            self.assertTrue(run_manifest.git_metadata(root)["dirty"])
            (root / "untracked.txt").unlink()

            submodule_checkout = root / "external" / "child"
            self.git(submodule_checkout, "config", "user.email", "tests@example.invalid")
            self.git(submodule_checkout, "config", "user.name", "Manifest Tests")
            (submodule_checkout / "tracked.txt").write_text("new child revision\n", encoding="utf-8")
            self.git(submodule_checkout, "commit", "-am", "advance child")
            moved = run_manifest.git_metadata(root)["submodules"][0]
            self.assertEqual(moved["expected_revision"], initialized["expected_revision"])
            self.assertNotEqual(moved["revision"], moved["expected_revision"])
            self.assertFalse(moved["dirty"])
            self.git(submodule_checkout, "checkout", initialized["expected_revision"])

            self.git(root, "submodule", "deinit", "-f", "external/child")
            uninitialized = run_manifest.git_metadata(root)["submodules"][0]
            self.assertFalse(uninitialized["initialized"])
            self.assertIsNone(uninitialized["revision"])
            self.assertIsNone(uninitialized["dirty"])
            self.assertEqual(uninitialized["expected_revision"], initialized["expected_revision"])


if __name__ == "__main__":
    unittest.main()
