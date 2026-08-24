"""Create and compare reproducible extraction run manifests.

The module deliberately uses only the Python standard library.  It hashes files
as opaque byte streams and never loads dotenv files or credentials.
"""

from __future__ import annotations

import argparse
import copy
import glob
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = 1
REDACTED = "[REDACTED]"
ARTIFACT_KINDS = ("inputs", "config", "prompts", "ontologies")
_SECRET_FILE_NAMES = {
    ".netrc", "credentials", "credentials.json", "id_dsa", "id_ed25519", "id_rsa",
    "secrets", "secrets.json",
}
_SECRET_DIRECTORY_NAMES = {".aws", ".git", ".ssh"}
_SECRET_FILE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}


class ManifestError(ValueError):
    """An actionable manifest input or validation error."""


def stable_json(data: Mapping[str, Any]) -> str:
    """Return the canonical, human-readable serialization used on disk."""

    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _sensitive_key(name: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    segments = set(normalized.split("_"))
    if {"password", "secret", "credential", "credentials", "authorization"} & segments:
        return True
    return (
        normalized in {
            "token", "apikey", "api_key", "private_key", "access_token", "auth_token",
            "bearer_token", "refresh_token",
        }
        or normalized.endswith(("_api_key", "_access_token", "_auth_token", "_bearer_token", "_refresh_token"))
    )


def _secret_bearing_path(path: Path) -> bool:
    for component in path.parts:
        name = component.lower()
        normalized = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
        segments = set(normalized.split("_"))
        if (
            name == ".env"
            or name.startswith(".env.")
            or name in _SECRET_FILE_NAMES
            or name in _SECRET_DIRECTORY_NAMES
            or {"credential", "credentials", "secret", "secrets"} & segments
            or "api_key" in normalized
            or "private_key" in normalized
        ):
            return True
    return path.suffix.lower() in _SECRET_FILE_SUFFIXES


def parse_settings(values: Iterable[str]) -> dict[str, str]:
    """Parse KEY=VALUE settings and redact values whose key looks sensitive."""

    settings: dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise ManifestError(f"setting must be KEY=VALUE, got {item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ManifestError("setting key must not be empty")
        if key in settings:
            raise ManifestError(f"setting {key!r} was supplied more than once")
        settings[key] = REDACTED if _sensitive_key(key) else value
    return dict(sorted(settings.items()))


def _under_base(path: Path, base_dir: Path) -> tuple[Path, str]:
    if path.is_symlink():
        raise ManifestError(f"symbolic links are not supported: {path}")
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(base_dir)
    except ValueError as exc:
        raise ManifestError(f"path is outside --base-dir: {path}") from exc
    if _secret_bearing_path(relative):
        raise ManifestError(f"refusing to read a secret-bearing file: {relative.as_posix()}")
    return resolved, relative.as_posix()


def resolve_file_specs(specs: Iterable[str], base_dir: Path | str) -> list[tuple[Path, str]]:
    """Expand file, directory, and glob specs into a sorted, unique file list.

    Literal missing paths, unmatched globs, empty directories, symlinks, files
    outside ``base_dir``, and obvious credential files are errors.
    """

    base = Path(base_dir).resolve()
    if not base.is_dir():
        raise ManifestError(f"base directory does not exist or is not a directory: {base}")

    found: dict[str, Path] = {}
    for spec in specs:
        candidate = Path(spec)
        pattern = str(candidate if candidate.is_absolute() else base / candidate)
        if glob.has_magic(pattern):
            matches = [Path(item) for item in glob.glob(pattern, recursive=True, include_hidden=True)]
            if not matches:
                raise ManifestError(f"glob matched no paths: {spec}")
        else:
            matches = [Path(pattern)]
            if not matches[0].exists() and not matches[0].is_symlink():
                raise ManifestError(f"path does not exist: {spec}")

        spec_files: list[Path] = []
        for match in matches:
            if match.is_symlink():
                raise ManifestError(f"symbolic links are not supported: {match}")
            if match.is_dir():
                children = sorted(match.rglob("*"), key=lambda item: item.as_posix())
                symlinks = [item for item in children if item.is_symlink()]
                if symlinks:
                    raise ManifestError(f"symbolic links are not supported: {symlinks[0]}")
                spec_files.extend(item for item in children if item.is_file())
            elif match.is_file():
                spec_files.append(match)
            else:
                raise ManifestError(f"path is not a regular file or directory: {match}")
        if not spec_files:
            raise ManifestError(f"path specification contains no files: {spec}")

        for item in spec_files:
            resolved, relative = _under_base(item, base)
            found[relative] = resolved

    return [(found[relative], relative) for relative in sorted(found)]


def sha256_file(path: Path) -> tuple[str, int]:
    """Hash a stable snapshot of a regular file, detecting concurrent writes."""

    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ManifestError(f"file changed while it was being hashed: {path}")
    return digest.hexdigest(), after.st_size


def artifact_records(specs: Iterable[str], base_dir: Path | str) -> list[dict[str, Any]]:
    records = []
    for path, relative in resolve_file_specs(specs, base_dir):
        try:
            checksum, size = sha256_file(path)
        except OSError as exc:
            raise ManifestError(f"cannot hash {relative}: {exc}") from exc
        records.append({"path": relative, "sha256": checksum, "size": size})
    return records


def _git(args: Sequence[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def git_metadata(base_dir: Path | str) -> dict[str, Any]:
    """Capture the containing repository and initialized submodule states."""

    base = Path(base_dir).resolve()
    try:
        root_result = _git(["rev-parse", "--show-toplevel"], base)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {"present": False, "root_revision": None, "dirty": None, "submodules": []}

    root = Path(root_result.stdout.strip()).resolve()
    revision_result = _git(["rev-parse", "--verify", "HEAD"], root, check=False)
    revision = revision_result.stdout.strip() if revision_result.returncode == 0 else None
    status = _git(["status", "--porcelain", "--untracked-files=normal"], root)

    submodules: list[dict[str, Any]] = []
    submodule_status = _git(["submodule", "status", "--recursive"], root, check=False)
    if submodule_status.returncode == 0:
        for line in submodule_status.stdout.splitlines():
            match = re.match(r"^(.)([0-9a-fA-F]{40,64}) (.+?)(?: \(.*\))?$", line)
            if not match:
                continue
            marker, status_revision, relative = match.groups()
            initialized = marker != "-"

            # ``git submodule status`` reports the checked-out revision when it
            # differs from the index. Read the gitlink itself for the expected
            # revision, using an initialized parent for nested submodules.
            parent_records = [
                item for item in submodules
                if item["initialized"] and relative.startswith(item["path"] + "/")
            ]
            parent = max(parent_records, key=lambda item: len(item["path"]), default=None)
            index_root = root / parent["path"] if parent else root
            index_path = relative[len(parent["path"]) + 1:] if parent else relative
            index_result = _git(["ls-files", "--stage", "--", index_path], index_root, check=False)
            expected_revision = status_revision.lower()
            for index_line in index_result.stdout.splitlines():
                fields = index_line.split(maxsplit=3)
                if len(fields) >= 3 and fields[2] == "0":
                    expected_revision = fields[1].lower()
                    break

            record: dict[str, Any] = {
                "dirty": None,
                "expected_revision": expected_revision,
                "initialized": initialized,
                "path": Path(relative).as_posix(),
                "revision": None,
            }
            if initialized:
                sub_root = root / relative
                actual = _git(["rev-parse", "--verify", "HEAD"], sub_root, check=False)
                sub_status = _git(
                    ["status", "--porcelain", "--untracked-files=normal"], sub_root, check=False
                )
                record["revision"] = actual.stdout.strip() if actual.returncode == 0 else None
                record["dirty"] = bool(sub_status.stdout.strip()) if sub_status.returncode == 0 else None
            submodules.append(record)

    return {
        "dirty": bool(status.stdout.strip()),
        "present": True,
        "root_revision": revision,
        "submodules": sorted(submodules, key=lambda item: item["path"]),
    }


def _timestamp(value: str | None = None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ManifestError(f"invalid ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ManifestError(f"timestamp must include a UTC offset: {value}")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def runtime_metadata() -> dict[str, Any]:
    return {
        "platform": {
            "machine": platform.machine(),
            "release": platform.release(),
            "system": platform.system(),
        },
        "python": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
        },
    }


def build_manifest(
    *,
    base_dir: Path | str,
    inputs: Iterable[str],
    config: Iterable[str],
    prompts: Iterable[str],
    ontologies: Iterable[str],
    outputs: Iterable[str] = (),
    provider: str,
    model: str,
    settings: Mapping[str, str] | None = None,
    parser_version: str,
    normalization_version: str,
    created_at: str | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> dict[str, Any]:
    """Build a manifest. Compatibility data is isolated from variable metadata."""

    sanitized_settings = {
        key: REDACTED if _sensitive_key(key) else str(value)
        for key, value in (settings or {}).items()
    }
    timestamps = {"created_at": _timestamp(created_at)}
    if started_at is not None:
        timestamps["run_started_at"] = _timestamp(started_at)
    if finished_at is not None:
        timestamps["run_finished_at"] = _timestamp(finished_at)

    return {
        "compatibility": {
            "artifacts": {
                "config": artifact_records(config, base_dir),
                "inputs": artifact_records(inputs, base_dir),
                "ontologies": artifact_records(ontologies, base_dir),
                "prompts": artifact_records(prompts, base_dir),
            },
            "request": {
                "model": model,
                "provider": provider,
                "settings": dict(sorted(sanitized_settings.items())),
            },
            "versions": {
                "normalization": normalization_version,
                "parser": parser_version,
            },
        },
        "metadata": {
            "git": git_metadata(base_dir),
            "runtime": runtime_metadata(),
            "timestamps": timestamps,
        },
        "outputs": artifact_records(outputs, base_dir),
        "schema_version": SCHEMA_VERSION,
    }


def write_manifest(path: Path | str, manifest: Mapping[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = stable_json(manifest)
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
        os.replace(temporary, destination)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_manifest(path: Path | str) -> dict[str, Any]:
    try:
        with Path(path).open("r", encoding="utf-8") as stream:
            data = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"manifest {path} must contain a JSON object")
    validate_structure(data, str(path))
    return data


def validate_structure(data: Mapping[str, Any], label: str = "manifest") -> None:
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ManifestError(
            f"{label} has unsupported schema_version {data.get('schema_version')!r}; "
            f"expected {SCHEMA_VERSION}"
        )
    compatibility = data.get("compatibility")
    if not isinstance(compatibility, dict):
        raise ManifestError(f"{label} is missing compatibility data")
    artifacts = compatibility.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ManifestError(f"{label} is missing compatibility.artifacts")
    for kind in ARTIFACT_KINDS:
        records = artifacts.get(kind)
        if not isinstance(records, list):
            raise ManifestError(f"{label} is missing compatibility.artifacts.{kind}")
        previous = ""
        for record in records:
            if not isinstance(record, dict) or not all(key in record for key in ("path", "sha256", "size")):
                raise ManifestError(f"{label} has an invalid {kind} artifact record")
            if not isinstance(record["path"], str) or record["path"] <= previous:
                raise ManifestError(f"{label} {kind} artifact paths must be unique and sorted")
            previous = record["path"]
    request = compatibility.get("request")
    versions = compatibility.get("versions")
    if not isinstance(request, dict) or not isinstance(request.get("settings"), dict):
        raise ManifestError(f"{label} is missing compatibility.request settings")
    if not isinstance(versions, dict):
        raise ManifestError(f"{label} is missing compatibility.versions")
    for key, value in request["settings"].items():
        if _sensitive_key(str(key)) and value != REDACTED:
            raise ManifestError(f"{label} contains an unredacted sensitive setting {key!r}")


def _diff_values(reference: Any, candidate: Any, path: str, differences: list[str]) -> None:
    if isinstance(reference, dict) and isinstance(candidate, dict):
        for key in sorted(reference.keys() | candidate.keys()):
            child = f"{path}.{key}" if path else str(key)
            if key not in reference:
                differences.append(f"{child}: added in candidate")
            elif key not in candidate:
                differences.append(f"{child}: missing from candidate")
            else:
                _diff_values(reference[key], candidate[key], child, differences)
    elif isinstance(reference, list) and isinstance(candidate, list):
        for index in range(max(len(reference), len(candidate))):
            child = f"{path}[{index}]"
            if index >= len(reference):
                differences.append(f"{child}: added in candidate")
            elif index >= len(candidate):
                differences.append(f"{child}: missing from candidate")
            else:
                _diff_values(reference[index], candidate[index], child, differences)
    elif reference != candidate:
        differences.append(f"{path}: expected {reference!r}, found {candidate!r}")


def compare_compatibility(reference: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[str]:
    """Compare only resume-compatibility fields, excluding timestamps and outputs."""

    reference_compatibility = reference.get("compatibility", {})
    candidate_compatibility = candidate.get("compatibility", {})
    differences: list[str] = []

    reference_artifacts = reference_compatibility.get("artifacts", {})
    candidate_artifacts = candidate_compatibility.get("artifacts", {})
    for kind in sorted(reference_artifacts.keys() | candidate_artifacts.keys()):
        reference_by_path = {record["path"]: record for record in reference_artifacts.get(kind, [])}
        candidate_by_path = {record["path"]: record for record in candidate_artifacts.get(kind, [])}
        for path in sorted(reference_by_path.keys() | candidate_by_path.keys()):
            label = f"compatibility.artifacts.{kind} {path}"
            if path not in reference_by_path:
                differences.append(f"{label}: added in candidate")
            elif path not in candidate_by_path:
                differences.append(f"{label}: missing from candidate")
            else:
                expected = reference_by_path[path]
                found = candidate_by_path[path]
                if expected["sha256"] != found["sha256"]:
                    differences.append(
                        f"{label}: checksum differs (expected {expected['sha256']}, "
                        f"found {found['sha256']})"
                    )
                if expected["size"] != found["size"]:
                    differences.append(
                        f"{label}: size differs (expected {expected['size']}, found {found['size']})"
                    )

    reference_rest = dict(reference_compatibility)
    candidate_rest = dict(candidate_compatibility)
    reference_rest.pop("artifacts", None)
    candidate_rest.pop("artifacts", None)
    _diff_values(reference_rest, candidate_rest, "compatibility", differences)
    return differences


def validate_current_files(
    manifest: Mapping[str, Any], base_dir: Path | str, *, check_outputs: bool = False
) -> list[str]:
    """Re-hash compatibility artifacts (and optionally outputs) at their recorded paths."""

    base = Path(base_dir).resolve()
    groups: list[tuple[str, Any]] = list(manifest["compatibility"]["artifacts"].items())
    if check_outputs:
        groups.append(("outputs", manifest.get("outputs", [])))
    differences: list[str] = []
    for kind, records in groups:
        for record in records:
            relative = Path(record["path"])
            try:
                path, normalized = _under_base(base / relative, base)
                if normalized != record["path"]:
                    raise ManifestError("path is not normalized")
                if not path.is_file():
                    differences.append(f"{kind} {record['path']}: file is missing")
                    continue
                checksum, size = sha256_file(path)
            except (ManifestError, OSError) as exc:
                differences.append(f"{kind} {record['path']}: cannot validate ({exc})")
                continue
            if checksum != record["sha256"]:
                differences.append(
                    f"{kind} {record['path']}: checksum changed "
                    f"(expected {record['sha256']}, found {checksum})"
                )
            elif size != record["size"]:
                differences.append(
                    f"{kind} {record['path']}: size changed (expected {record['size']}, found {size})"
                )
    return differences


def _print_result(differences: Sequence[str]) -> int:
    if not differences:
        print("compatible")
        return 0
    print(f"incompatible: {len(differences)} mismatch(es)")
    for difference in differences:
        print(f"- {difference}")
    return 1


def _create_command(args: argparse.Namespace) -> int:
    manifest = build_manifest(
        base_dir=args.base_dir,
        inputs=args.input,
        config=args.config,
        prompts=args.prompt,
        ontologies=args.ontology,
        outputs=args.output,
        provider=args.provider,
        model=args.model,
        settings=parse_settings(args.setting),
        parser_version=args.parser_version,
        normalization_version=args.normalization_version,
        created_at=args.created_at,
        started_at=args.started_at,
        finished_at=args.finished_at,
    )
    write_manifest(args.manifest, manifest)
    print(f"wrote {args.manifest}")
    return 0


def _compare_command(args: argparse.Namespace) -> int:
    reference = load_manifest(args.reference)
    candidate = load_manifest(args.candidate)
    return _print_result(compare_compatibility(reference, candidate))


def _validate_command(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.manifest)
    differences = validate_current_files(manifest, args.base_dir, check_outputs=args.check_outputs)

    current = copy.deepcopy(manifest)
    request = current["compatibility"]["request"]
    versions = current["compatibility"]["versions"]
    if args.provider is not None:
        request["provider"] = args.provider
    if args.model is not None:
        request["model"] = args.model
    if args.setting is not None:
        request["settings"] = parse_settings(args.setting)
    if args.parser_version is not None:
        versions["parser"] = args.parser_version
    if args.normalization_version is not None:
        versions["normalization"] = args.normalization_version
    differences.extend(compare_compatibility(manifest, current))
    return _print_result(differences)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and validate deterministic extraction run manifests")
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="create a manifest")
    create.add_argument("--manifest", required=True, help="destination JSON file")
    create.add_argument("--base-dir", default=".", help="root used for paths and Git discovery")
    create.add_argument("--input", action="append", required=True, help="input file, directory, or glob")
    create.add_argument("--config", action="append", required=True, help="parser/config file, directory, or glob")
    create.add_argument("--prompt", action="append", required=True, help="prompt file, directory, or glob")
    create.add_argument("--ontology", action="append", required=True, help="ontology file, directory, or glob")
    create.add_argument("--output", action="append", default=[], help="existing output file, directory, or glob")
    create.add_argument("--provider", required=True)
    create.add_argument("--model", required=True)
    create.add_argument("--setting", action="append", default=[], metavar="KEY=VALUE")
    create.add_argument("--parser-version", required=True)
    create.add_argument("--normalization-version", required=True)
    create.add_argument("--created-at", help="ISO-8601 timestamp; defaults to current UTC time")
    create.add_argument("--started-at", help="optional run start time with UTC offset")
    create.add_argument("--finished-at", help="optional run finish time with UTC offset")
    create.set_defaults(func=_create_command)

    compare = subparsers.add_parser("compare", help="compare resume-compatibility fields")
    compare.add_argument("reference")
    compare.add_argument("candidate")
    compare.set_defaults(func=_compare_command)

    validate = subparsers.add_parser("validate", help="check recorded files and requested resume settings")
    validate.add_argument("manifest")
    validate.add_argument("--base-dir", default=".")
    validate.add_argument("--check-outputs", action="store_true")
    validate.add_argument("--provider")
    validate.add_argument("--model")
    validate.add_argument("--setting", action="append", metavar="KEY=VALUE")
    validate.add_argument("--parser-version")
    validate.add_argument("--normalization-version")
    validate.set_defaults(func=_validate_command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ManifestError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
