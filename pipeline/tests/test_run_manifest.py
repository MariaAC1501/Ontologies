import contextlib
import copy
import io
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        secret_keys = [
            "api_token", "github_token", "openaiApiKey", "dbPassword", "auth", "bearer",
            "refreshToken", "access-token", "PRIVATE_KEY", "credentials", "clientSecret",
            "Authorization",
        ]
        parsed = run_manifest.parse_settings(
            ["temperature=0", "max_tokens=20", *[f"{key}=SECRET-{index}" for index, key in enumerate(secret_keys)]]
        )
        self.assertEqual(parsed["temperature"], "0")
        self.assertEqual(parsed["max_tokens"], "20")
        for key in secret_keys:
            self.assertEqual(parsed[key], run_manifest.REDACTED)
        serialized = run_manifest.stable_json({"settings": parsed})
        self.assertNotIn("SECRET-", serialized)
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
            code = run_manifest.main([
                "validate", str(manifest_path), "--base-dir", str(self.base),
                "--provider", "provider", "--model", "other", "--setting", "temperature=0",
                "--parser-version", "parser-1", "--normalization-version", "norm-1",
            ])
        self.assertEqual(code, 1)
        self.assertIn("compatibility.request.model", output.getvalue())

        candidate = json.loads(manifest_path.read_text(encoding="utf-8"))
        candidate["metadata"]["timestamps"]["created_at"] = "2030-01-01T00:00:00Z"
        candidate_path = self.base / "candidate.json"
        run_manifest.write_manifest(candidate_path, candidate)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_manifest.main(["compare", str(manifest_path), str(candidate_path)]), 0)

        integrity_output = io.StringIO()
        with contextlib.redirect_stdout(integrity_output):
            self.assertEqual(
                run_manifest.main(["validate", str(manifest_path), "--base-dir", str(self.base)]), 0
            )
        self.assertIn("file integrity valid", integrity_output.getvalue())
        self.assertNotIn("\ncompatible", "\n" + integrity_output.getvalue())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(
                run_manifest.main(["validate", str(manifest_path), "--model", "partial"]), 2
            )
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_structure_rejects_unredacted_secret_and_unsorted_records(self):
        manifest = self.build()
        manifest["compatibility"]["request"]["settings"]["openaiApiKey"] = "unsafe"
        with self.assertRaisesRegex(run_manifest.ManifestError, "unredacted"):
            run_manifest.validate_structure(manifest)

        manifest = self.build()
        manifest["compatibility"]["artifacts"]["inputs"].reverse()
        with self.assertRaisesRegex(run_manifest.ManifestError, "sorted"):
            run_manifest.validate_structure(manifest)

    def test_structure_fully_rejects_malformed_manifests_at_cli_boundary(self):
        mutations = []
        mutations.append(lambda value: value["compatibility"]["artifacts"].update({"unknown": []}))
        mutations.append(lambda value: value.update({"outputs": {}}))
        mutations.append(lambda value: value["compatibility"]["request"].pop("provider"))
        mutations.append(lambda value: value["compatibility"]["versions"].update({"parser": 7}))
        mutations.append(lambda value: value["metadata"].update({"timestamps": []}))
        mutations.append(lambda value: value["compatibility"]["artifacts"]["inputs"][0].update({"path": "../escape"}))
        mutations.append(lambda value: value["compatibility"]["artifacts"]["inputs"][0].update({"sha256": "bad"}))
        mutations.append(lambda value: value["compatibility"]["artifacts"]["inputs"][0].update({"size": -1}))
        mutations.append(
            lambda value: value["outputs"][0].update(
                {"path": value["compatibility"]["artifacts"]["inputs"][0]["path"]}
            )
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                malformed = self.build()
                mutate(malformed)
                path = self.base / f"malformed-{index}.json"
                path.write_text(json.dumps(malformed), encoding="utf-8")
                stderr = io.StringIO()
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(run_manifest.main(["compare", str(path), str(path)]), 2)
                self.assertNotIn("Traceback", stderr.getvalue())

    def test_directory_symlinks_env_aliases_fifos_and_replacement_races_are_rejected(self):
        dotenv = self.base / ".env"
        dotenv.write_text("SECRET=not-read\n", encoding="utf-8")
        (self.base / ".env-alias").write_text("SECRET=also-not-read\n", encoding="utf-8")
        with self.assertRaisesRegex(run_manifest.ManifestError, "secret-bearing"):
            run_manifest.resolve_file_specs([".env-alias"], self.base)
        try:
            (self.base / "innocent-config").symlink_to(dotenv)
        except (OSError, NotImplementedError):
            pass
        else:
            with self.assertRaisesRegex(run_manifest.ManifestError, "symbolic links"):
                run_manifest.resolve_file_specs(["innocent-config"], self.base)

        real = self.base / "real"
        real.mkdir()
        (real / "inside.txt").write_text("inside", encoding="utf-8")
        try:
            (self.base / "directory-link").symlink_to(real, target_is_directory=True)
        except (OSError, NotImplementedError):
            pass
        else:
            with self.assertRaisesRegex(run_manifest.ManifestError, "symbolic links"):
                run_manifest.resolve_file_specs(["directory-link/inside.txt"], self.base)

        if hasattr(os, "mkfifo"):
            fifo = self.base / "pipe"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(run_manifest.ManifestError, "regular file"):
                run_manifest.sha256_file(fifo.resolve())

        race_dir = self.base / "race"
        race_dir.mkdir()
        victim = race_dir / "victim.txt"
        victim.write_bytes(b"safe snapshot")
        outside = self.base.parent / f"{self.base.name}-outside-race"
        outside.mkdir()
        (outside / "victim.txt").write_bytes(b"outside secret")
        original_read = os.read
        swapped = False

        def replace_ancestor(descriptor, size):
            nonlocal swapped
            chunk = original_read(descriptor, size)
            if not swapped:
                swapped = True
                race_dir.rename(self.base / "old-race")
                try:
                    race_dir.symlink_to(outside, target_is_directory=True)
                except OSError:
                    race_dir.mkdir()
            return chunk

        try:
            with mock.patch.object(run_manifest.os, "read", side_effect=replace_ancestor):
                with self.assertRaises(run_manifest.ManifestError):
                    run_manifest.sha256_file(victim.resolve())
            self.assertTrue(swapped)
        finally:
            if race_dir.is_symlink():
                race_dir.unlink()
            shutil.rmtree(self.base / "old-race", ignore_errors=True)
            shutil.rmtree(outside, ignore_errors=True)

    def test_manifest_destination_cannot_be_selected_by_directory_or_broad_glob(self):
        common = [
            "create", "--base-dir", str(self.base), "--config", "config.toml",
            "--prompt", "prompt.txt", "--ontology", "ontology.ttl", "--provider", "p",
            "--model", "m", "--parser-version", "p1", "--normalization-version", "n1",
        ]
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                run_manifest.main([*common, "--manifest", str(self.base / "corpus/manifest.json"), "--input", "corpus"]),
                2,
            )
        run_dir = self.base / "run"
        run_dir.mkdir()
        (run_dir / "existing.txt").write_text("x", encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(
                run_manifest.main([
                    *common, "--manifest", str(run_dir / "manifest.json"),
                    "--input", "corpus/*.txt", "--output", "run/**/*",
                ]),
                2,
            )

    def test_code_provenance_is_resume_compatible_but_runtime_is_not(self):
        reference = self.build()
        candidate = copy.deepcopy(reference)
        candidate["metadata"]["runtime"]["python"]["version"] = "different"
        self.assertEqual(run_manifest.compare_compatibility(reference, candidate), [])
        candidate["compatibility"]["code"]["present"] = True
        candidate["compatibility"]["code"]["root_revision"] = "a" * 40
        candidate["compatibility"]["code"]["dirty"] = False
        self.assertTrue(any("compatibility.code" in item for item in run_manifest.compare_compatibility(reference, candidate)))


class GitMetadataTests(unittest.TestCase):
    def test_discovery_distinguishes_no_repository_from_git_failure(self):
        no_repo = subprocess.CompletedProcess(
            ["git"], 128, stdout="", stderr="fatal: not a git repository (or any parent)\n"
        )
        with mock.patch.object(run_manifest, "_git", return_value=no_repo):
            self.assertFalse(run_manifest.git_metadata(Path.cwd())["present"])

        denied = subprocess.CompletedProcess(
            ["git"], 128, stdout="", stderr="fatal: cannot open .git/HEAD: Permission denied\n"
        )
        with mock.patch.object(run_manifest, "_git", return_value=denied):
            with self.assertRaisesRegex(run_manifest.ManifestError, "discovery failed"):
                run_manifest.git_metadata(Path.cwd())

    def test_status_and_submodule_failures_are_explicit(self):
        root = subprocess.CompletedProcess(["git"], 0, stdout=str(Path.cwd()) + "\n", stderr="")
        revision = subprocess.CompletedProcess(["git"], 0, stdout="a" * 40 + "\n", stderr="")
        failure = subprocess.CompletedProcess(["git"], 128, stdout="", stderr="corrupt index\n")
        with mock.patch.object(run_manifest, "_git", side_effect=[root, revision, failure]):
            with self.assertRaisesRegex(run_manifest.ManifestError, "status failed"):
                run_manifest.git_metadata(Path.cwd())

        status = subprocess.CompletedProcess(["git"], 0, stdout="", stderr="")
        with mock.patch.object(run_manifest, "_git", side_effect=[root, revision, status, failure]):
            with self.assertRaisesRegex(run_manifest.ManifestError, "submodule discovery failed"):
                run_manifest.git_metadata(Path.cwd())

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
