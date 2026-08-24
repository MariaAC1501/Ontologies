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
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = 2
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


def _key_words(name: str) -> list[str]:
    # Split separators and camelCase/acronym boundaries (openaiApiKey, DBPassword).
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    separated = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", separated)
    return [word for word in re.sub(r"[^A-Za-z0-9]+", "_", separated).lower().split("_") if word]


def _sensitive_key(name: str) -> bool:
    words = _key_words(name)
    segments = set(words)
    if segments & {
        "auth", "authentication", "authorization", "bearer", "credential", "credentials",
        "key", "keys", "oauth", "passphrase", "password", "passwords", "passwd", "pat",
        "pats", "pwd", "secret", "secrets", "token",
    }:
        return True
    # Recognize common unseparated spellings without treating an arbitrary word
    # ending in (for example) "key" as a credential name ("monkey", "hockey").
    compound_prefixes = (
        "api", "access", "client", "github", "gitlab", "openai", "private", "secret",
        "signing", "ssh",
    )
    compound_suffixes = ("auth", "key", "password", "pat", "token")
    return any(
        segment == prefix + suffix
        for segment in segments
        for prefix in compound_prefixes
        for suffix in compound_suffixes
    )


def _secret_bearing_path(path: Path) -> bool:
    for component in path.parts:
        name = component.lower()
        stem = Path(component).stem
        if (
            name == ".env"
            or name.startswith((".env.", ".env-", ".env_"))
            or name in _SECRET_FILE_NAMES
            or stem.lower() in _SECRET_FILE_NAMES
            or name in _SECRET_DIRECTORY_NAMES
            or _sensitive_key(stem)
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


def _absolute_base(base_dir: Path | str) -> Path:
    supplied = Path(base_dir)
    if supplied.is_symlink():
        raise ManifestError(f"--base-dir must not be a symbolic link: {supplied}")
    try:
        # Canonicalize platform-level aliases above the selected base (for
        # example macOS /var -> /private/var). In-base components remain lexical.
        base = supplied.resolve(strict=True)
    except OSError as exc:
        raise ManifestError(f"cannot inspect --base-dir {supplied}: {exc}") from exc
    try:
        mode = base.lstat().st_mode
    except OSError as exc:
        raise ManifestError(f"cannot inspect --base-dir {base}: {exc}") from exc
    if not stat.S_ISDIR(mode):
        raise ManifestError(f"base directory does not exist or is not a directory: {base}")
    return base


def _under_base(path: Path, base_dir: Path) -> tuple[Path, str]:
    """Apply lexical containment/secret checks, then reject every in-base symlink."""

    absolute = Path(os.path.abspath(path))
    try:
        relative = absolute.relative_to(base_dir)
    except ValueError:
        try:
            absolute = absolute.resolve(strict=True)
            relative = absolute.relative_to(base_dir)
        except (OSError, ValueError) as exc:
            raise ManifestError(f"path is outside --base-dir: {path}") from exc
    if relative == Path(".") or any(part in ("", ".", "..") for part in relative.parts):
        raise ManifestError(f"path is not a normalized relative path: {path}")
    if _secret_bearing_path(relative):
        raise ManifestError(f"refusing to read a secret-bearing file: {relative.as_posix()}")
    current = base_dir
    for component in relative.parts:
        current = current / component
        try:
            mode = current.lstat().st_mode
        except OSError as exc:
            raise ManifestError(f"cannot inspect path component {current}: {exc}") from exc
        if stat.S_ISLNK(mode):
            raise ManifestError(f"symbolic links are not supported: {current}")
    return absolute, relative.as_posix()


def resolve_file_specs(specs: Iterable[str], base_dir: Path | str) -> list[tuple[Path, str]]:
    """Expand specs into sorted regular files without accepting symlink ancestors."""

    base = _absolute_base(base_dir)
    found: dict[str, Path] = {}
    for spec in specs:
        raw = Path(spec)
        if any(part == ".." for part in raw.parts):
            raise ManifestError(f"parent path components are not supported: {spec}")
        if _secret_bearing_path(raw):
            raise ManifestError(f"refusing to read a secret-bearing file: {spec}")
        pattern = str(raw if raw.is_absolute() else base / raw)
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
            safe_match, _ = _under_base(match, base)
            mode = safe_match.lstat().st_mode
            if stat.S_ISDIR(mode):
                children = sorted(safe_match.rglob("*"), key=lambda item: item.as_posix())
                for child in children:
                    safe_child, _ = _under_base(child, base)
                    child_mode = safe_child.lstat().st_mode
                    if stat.S_ISREG(child_mode):
                        spec_files.append(safe_child)
                    elif not stat.S_ISDIR(child_mode):
                        raise ManifestError(f"path is not a regular file or directory: {child}")
            elif stat.S_ISREG(mode):
                spec_files.append(safe_match)
            else:
                raise ManifestError(f"path is not a regular file or directory: {match}")
        if not spec_files:
            raise ManifestError(f"path specification contains no files: {spec}")

        for item in spec_files:
            safe, relative = _under_base(item, base)
            found[relative] = safe

    return [(found[relative], relative) for relative in sorted(found)]


def _snapshot(metadata: os.stat_result) -> tuple[int, int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        stat.S_IFMT(metadata.st_mode),
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def sha256_file(path: Path) -> tuple[str, int]:
    """Hash one descriptor-pinned regular-file snapshot without following links."""

    absolute = Path(os.path.abspath(path))
    components = absolute.parts
    if not absolute.is_absolute() or len(components) < 2:
        raise ManifestError(f"cannot securely open non-absolute path: {path}")
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    cloexec = getattr(os, "O_CLOEXEC", 0)
    nonblock = getattr(os, "O_NONBLOCK", 0)
    directory = getattr(os, "O_DIRECTORY", 0)
    descriptors: list[int] = []
    ancestors: list[tuple[int, str, tuple[int, int, int]]] = []
    try:
        current_fd = os.open(components[0], os.O_RDONLY | directory | cloexec)
        descriptors.append(current_fd)
        for component in components[1:-1]:
            before = os.stat(component, dir_fd=current_fd, follow_symlinks=False)
            if not stat.S_ISDIR(before.st_mode):
                raise ManifestError(f"path ancestor is not a directory: {path}")
            child_fd = os.open(component, os.O_RDONLY | directory | nofollow | cloexec, dir_fd=current_fd)
            opened = os.fstat(child_fd)
            identity = (before.st_dev, before.st_ino, stat.S_IFMT(before.st_mode))
            if identity != (opened.st_dev, opened.st_ino, stat.S_IFMT(opened.st_mode)):
                raise ManifestError(f"path ancestor was replaced while opening: {path}")
            ancestors.append((current_fd, component, identity))
            descriptors.append(child_fd)
            current_fd = child_fd

        name = components[-1]
        path_before = os.stat(name, dir_fd=current_fd, follow_symlinks=False)
        if not stat.S_ISREG(path_before.st_mode):
            raise ManifestError(f"path is not a regular file: {path}")
        file_fd = os.open(
            name, os.O_RDONLY | nofollow | cloexec | nonblock, dir_fd=current_fd
        )
        descriptors.append(file_fd)
        descriptor_before = os.fstat(file_fd)
        if _snapshot(path_before) != _snapshot(descriptor_before):
            raise ManifestError(f"file was replaced while opening: {path}")

        digest = hashlib.sha256()
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)

        descriptor_after = os.fstat(file_fd)
        path_after = os.stat(name, dir_fd=current_fd, follow_symlinks=False)
        if not stat.S_ISREG(path_after.st_mode) or not (
            _snapshot(path_before) == _snapshot(descriptor_before)
            == _snapshot(descriptor_after) == _snapshot(path_after)
        ):
            raise ManifestError(f"file changed or was replaced while it was being hashed: {path}")
        for parent_fd, component, identity in ancestors:
            after = os.stat(component, dir_fd=parent_fd, follow_symlinks=False)
            if identity != (after.st_dev, after.st_ino, stat.S_IFMT(after.st_mode)):
                raise ManifestError(f"path ancestor was replaced while hashing: {path}")
        return digest.hexdigest(), descriptor_after.st_size
    except ManifestError:
        raise
    except OSError as exc:
        raise ManifestError(f"cannot securely hash {path}: {exc}") from exc
    finally:
        for descriptor in reversed(descriptors):
            try:
                os.close(descriptor)
            except OSError:
                pass


def artifact_records(specs: Iterable[str], base_dir: Path | str) -> list[dict[str, Any]]:
    records = []
    for path, relative in resolve_file_specs(specs, base_dir):
        try:
            checksum, size = sha256_file(path)
        except OSError as exc:
            raise ManifestError(f"cannot hash {relative}: {exc}") from exc
        records.append({"path": relative, "sha256": checksum, "size": size})
    return records


def _git(args: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "LANG": "C"})
    try:
        return subprocess.run(
            ["git", *args], cwd=cwd, check=False, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, env=environment,
        )
    except OSError as exc:
        raise ManifestError(f"cannot run Git command {' '.join(args)!r}: {exc}") from exc


def _git_required(args: Sequence[str], cwd: Path, purpose: str) -> subprocess.CompletedProcess[str]:
    result = _git(args, cwd)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise ManifestError(f"Git {purpose} failed: {detail}")
    return result


def git_metadata(base_dir: Path | str) -> dict[str, Any]:
    """Capture Git state; only a definite 'not a repository' means absent."""

    base = _absolute_base(base_dir)
    root_result = _git(["rev-parse", "--show-toplevel"], base)
    if root_result.returncode != 0:
        detail = (root_result.stderr + root_result.stdout).lower()
        if "not a git repository" in detail:
            return {"present": False, "root_revision": None, "dirty": None, "submodules": []}
        message = root_result.stderr.strip() or root_result.stdout.strip() or f"exit {root_result.returncode}"
        raise ManifestError(f"Git repository discovery failed: {message}")

    root_text = root_result.stdout.strip()
    if not root_text:
        raise ManifestError("Git repository discovery returned an empty root")
    root = Path(root_text)
    revision = _git_required(["rev-parse", "--verify", "HEAD"], root, "HEAD discovery").stdout.strip()
    if not re.fullmatch(r"[0-9a-fA-F]{40,64}", revision):
        raise ManifestError(f"Git returned an invalid HEAD revision: {revision!r}")
    status = _git_required(
        ["status", "--porcelain", "--untracked-files=normal"], root, "status"
    )
    submodule_status = _git_required(
        ["submodule", "status", "--recursive"], root, "submodule discovery"
    )

    submodules: list[dict[str, Any]] = []
    for line in submodule_status.stdout.splitlines():
        match = re.fullmatch(r"(.)([0-9a-fA-F]{40,64}) (.+?)(?: \(.*\))?", line)
        if not match:
            raise ManifestError(f"Git returned malformed submodule status: {line!r}")
        marker, status_revision, relative = match.groups()
        if marker not in (" ", "-", "+", "U"):
            raise ManifestError(f"Git returned unknown submodule marker {marker!r}")
        initialized = marker != "-"
        parent_records = [
            item for item in submodules
            if item["initialized"] and relative.startswith(item["path"] + "/")
        ]
        parent = max(parent_records, key=lambda item: len(item["path"]), default=None)
        index_root = root / parent["path"] if parent else root
        index_path = relative[len(parent["path"]) + 1:] if parent else relative
        index_result = _git_required(
            ["ls-files", "--stage", "--", index_path], index_root, "submodule index lookup"
        )
        expected_revision = None
        for index_line in index_result.stdout.splitlines():
            fields = index_line.split(maxsplit=3)
            if len(fields) >= 3 and fields[0] == "160000" and fields[2] == "0":
                expected_revision = fields[1].lower()
                break
        if expected_revision is None:
            raise ManifestError(f"Git index has no stage-0 gitlink for submodule {relative!r}")

        record: dict[str, Any] = {
            "dirty": None, "expected_revision": expected_revision,
            "initialized": initialized, "path": Path(relative).as_posix(), "revision": None,
        }
        if initialized:
            sub_root = root / relative
            actual = _git_required(
                ["rev-parse", "--verify", "HEAD"], sub_root, f"HEAD discovery for {relative}"
            ).stdout.strip()
            if not re.fullmatch(r"[0-9a-fA-F]{40,64}", actual):
                raise ManifestError(f"Git returned an invalid revision for submodule {relative!r}")
            sub_status = _git_required(
                ["status", "--porcelain", "--untracked-files=normal"],
                sub_root, f"status for {relative}",
            )
            record["revision"] = actual.lower()
            record["dirty"] = bool(sub_status.stdout.strip())
        submodules.append(record)

    return {
        "dirty": bool(status.stdout.strip()), "present": True,
        "root_revision": revision.lower(),
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

    required_strings = {
        "provider": provider, "model": model, "parser_version": parser_version,
        "normalization_version": normalization_version,
    }
    for label, value in required_strings.items():
        if not isinstance(value, str) or not value:
            raise ManifestError(f"{label} must be a non-empty string")
    sanitized_settings: dict[str, str] = {}
    for key, value in (settings or {}).items():
        if not isinstance(key, str) or not key:
            raise ManifestError("setting keys must be non-empty strings")
        sanitized_settings[key] = REDACTED if _sensitive_key(key) else str(value)
    timestamps = {"created_at": _timestamp(created_at)}
    if started_at is not None:
        timestamps["run_started_at"] = _timestamp(started_at)
    if finished_at is not None:
        timestamps["run_finished_at"] = _timestamp(finished_at)

    git = git_metadata(base_dir)
    manifest = {
        "compatibility": {
            "artifacts": {
                "config": artifact_records(config, base_dir),
                "inputs": artifact_records(inputs, base_dir),
                "ontologies": artifact_records(ontologies, base_dir),
                "prompts": artifact_records(prompts, base_dir),
            },
            "code": copy.deepcopy(git),
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
            "git": git,
            "runtime": runtime_metadata(),
            "timestamps": timestamps,
        },
        "outputs": artifact_records(outputs, base_dir),
        "schema_version": SCHEMA_VERSION,
    }
    validate_structure(manifest, "generated manifest")
    return manifest


def write_manifest(path: Path | str, manifest: Mapping[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    validate_structure(manifest, "manifest to write")
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
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"manifest {path} must contain a JSON object")
    validate_structure(data, str(path))
    return data


def _validate_git(value: Any, label: str) -> None:
    if not isinstance(value, dict) or set(value) != {"present", "root_revision", "dirty", "submodules"}:
        raise ManifestError(f"{label} has invalid Git metadata")
    if not isinstance(value["present"], bool) or not isinstance(value["submodules"], list):
        raise ManifestError(f"{label} has invalid Git metadata types")
    if value["present"]:
        if not isinstance(value["dirty"], bool) or not isinstance(value["root_revision"], str) or not re.fullmatch(
            r"[0-9a-fA-F]{40,64}", value["root_revision"]
        ):
            raise ManifestError(f"{label} has invalid repository revision/state")
    elif value["dirty"] is not None or value["root_revision"] is not None or value["submodules"]:
        raise ManifestError(f"{label} absent repository metadata must use null state and no submodules")
    previous = ""
    for record in value["submodules"]:
        expected_keys = {"dirty", "expected_revision", "initialized", "path", "revision"}
        if not isinstance(record, dict) or set(record) != expected_keys:
            raise ManifestError(f"{label} has invalid submodule metadata")
        path = record["path"]
        if not _safe_relative_path(path) or path <= previous:
            raise ManifestError(f"{label} submodule paths must be safe, unique, and sorted")
        previous = path
        if not isinstance(record["initialized"], bool) or not isinstance(record["expected_revision"], str) or not re.fullmatch(
            r"[0-9a-fA-F]{40,64}", record["expected_revision"]
        ):
            raise ManifestError(f"{label} has invalid submodule revision/state")
        if record["initialized"]:
            if not isinstance(record["dirty"], bool) or not isinstance(record["revision"], str) or not re.fullmatch(
                r"[0-9a-fA-F]{40,64}", record["revision"]
            ):
                raise ManifestError(f"{label} has invalid initialized submodule state")
        elif record["dirty"] is not None or record["revision"] is not None:
            raise ManifestError(f"{label} has invalid uninitialized submodule state")


def _safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and value == path.as_posix() and all(
        part not in ("", ".", "..") for part in path.parts
    )


def _validate_records(records: Any, label: str, all_paths: set[str]) -> None:
    if not isinstance(records, list):
        raise ManifestError(f"{label} must be a list")
    previous = ""
    for record in records:
        if not isinstance(record, dict) or set(record) != {"path", "sha256", "size"}:
            raise ManifestError(f"{label} has an invalid artifact record")
        path = record["path"]
        if not _safe_relative_path(path) or _secret_bearing_path(Path(path)):
            raise ManifestError(f"{label} contains an unsafe artifact path {path!r}")
        if path <= previous:
            raise ManifestError(f"{label} artifact paths must be unique and sorted")
        if path in all_paths:
            raise ManifestError(f"{label} duplicates artifact path {path!r}")
        previous = path
        all_paths.add(path)
        if not isinstance(record["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", record["sha256"]):
            raise ManifestError(f"{label} has an invalid SHA-256 for {path!r}")
        if isinstance(record["size"], bool) or not isinstance(record["size"], int) or record["size"] < 0:
            raise ManifestError(f"{label} has an invalid size for {path!r}")


def validate_structure(data: Mapping[str, Any], label: str = "manifest") -> None:
    if not isinstance(data, dict) or set(data) != {"schema_version", "compatibility", "metadata", "outputs"}:
        raise ManifestError(f"{label} must contain exactly schema_version, compatibility, metadata, and outputs")
    if type(data.get("schema_version")) is not int or data.get("schema_version") != SCHEMA_VERSION:
        raise ManifestError(
            f"{label} has unsupported schema_version {data.get('schema_version')!r}; expected {SCHEMA_VERSION}"
        )
    compatibility = data["compatibility"]
    if not isinstance(compatibility, dict) or set(compatibility) != {"artifacts", "code", "request", "versions"}:
        raise ManifestError(f"{label} has invalid compatibility data")
    artifacts = compatibility["artifacts"]
    if not isinstance(artifacts, dict) or set(artifacts) != set(ARTIFACT_KINDS):
        raise ManifestError(f"{label} compatibility.artifacts must contain only {', '.join(ARTIFACT_KINDS)}")
    all_paths: set[str] = set()
    for kind in ARTIFACT_KINDS:
        _validate_records(artifacts[kind], f"{label} compatibility.artifacts.{kind}", all_paths)
    _validate_records(data["outputs"], f"{label} outputs", all_paths)

    request = compatibility["request"]
    if not isinstance(request, dict) or set(request) != {"model", "provider", "settings"}:
        raise ManifestError(f"{label} has invalid compatibility.request")
    for field in ("provider", "model"):
        if not isinstance(request[field], str) or not request[field]:
            raise ManifestError(f"{label} compatibility.request.{field} must be a non-empty string")
    settings = request["settings"]
    if not isinstance(settings, dict):
        raise ManifestError(f"{label} compatibility.request.settings must be an object")
    for key, value in settings.items():
        if not isinstance(key, str) or not key or not isinstance(value, str):
            raise ManifestError(f"{label} settings keys and values must be strings")
        if _sensitive_key(key) and value != REDACTED:
            raise ManifestError(f"{label} contains an unredacted sensitive setting {key!r}")

    versions = compatibility["versions"]
    if not isinstance(versions, dict) or set(versions) != {"normalization", "parser"}:
        raise ManifestError(f"{label} has invalid compatibility.versions")
    for field in ("normalization", "parser"):
        if not isinstance(versions[field], str) or not versions[field]:
            raise ManifestError(f"{label} compatibility.versions.{field} must be a non-empty string")
    _validate_git(compatibility["code"], f"{label} compatibility.code")

    metadata = data["metadata"]
    if not isinstance(metadata, dict) or set(metadata) != {"git", "runtime", "timestamps"}:
        raise ManifestError(f"{label} has invalid metadata")
    _validate_git(metadata["git"], f"{label} metadata.git")
    if metadata["git"] != compatibility["code"]:
        raise ManifestError(f"{label} compatibility.code and metadata.git must match")
    runtime = metadata["runtime"]
    if not isinstance(runtime, dict) or set(runtime) != {"platform", "python"}:
        raise ManifestError(f"{label} has invalid metadata.runtime")
    expected_runtime = {"platform": {"machine", "release", "system"}, "python": {"implementation", "version"}}
    for group, keys in expected_runtime.items():
        if not isinstance(runtime[group], dict) or set(runtime[group]) != keys or not all(
            isinstance(value, str) for value in runtime[group].values()
        ):
            raise ManifestError(f"{label} has invalid metadata.runtime.{group}")
    timestamps = metadata["timestamps"]
    allowed_timestamps = {"created_at", "run_started_at", "run_finished_at"}
    if not isinstance(timestamps, dict) or "created_at" not in timestamps or not set(timestamps) <= allowed_timestamps:
        raise ManifestError(f"{label} has invalid metadata.timestamps")
    for key, value in timestamps.items():
        if not isinstance(value, str) or _timestamp(value) != value:
            raise ManifestError(f"{label} metadata.timestamps.{key} is not canonical UTC ISO-8601")


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


def _code_state_is_dirty(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    if value.get("dirty") is True:
        return True
    submodules = value.get("submodules", [])
    return isinstance(submodules, list) and any(
        isinstance(record, dict) and record.get("dirty") is True for record in submodules
    )


def compare_compatibility(reference: Mapping[str, Any], candidate: Mapping[str, Any]) -> list[str]:
    """Compare only resume-compatibility fields, excluding timestamps and outputs."""

    reference_compatibility = reference.get("compatibility", {})
    candidate_compatibility = candidate.get("compatibility", {})
    differences: list[str] = []
    dirty_sides = [
        label for label, compatibility in (
            ("reference", reference_compatibility), ("candidate", candidate_compatibility)
        )
        if _code_state_is_dirty(compatibility.get("code", {}))
    ]
    if dirty_sides:
        differences.append(
            "compatibility.code: resume compatibility is fail-closed because "
            + " and ".join(dirty_sides)
            + " code state is dirty"
        )

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

    base = _absolute_base(base_dir)
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
                checksum, size = sha256_file(path)
            except (ManifestError, OSError) as exc:
                if "No such file or directory" in str(exc):
                    differences.append(f"{kind} {record['path']}: file is missing")
                else:
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


def _print_result(
    differences: Sequence[str], *, success: str = "compatible", failure: str = "incompatible"
) -> int:
    if not differences:
        print(success)
        return 0
    print(f"{failure}: {len(differences)} mismatch(es)")
    for difference in differences:
        print(f"- {difference}")
    return 1


def _glob_variants(pattern: str) -> set[str]:
    variants = {pattern}
    while True:
        expanded = set(variants)
        for item in variants:
            if "**/" in item:
                expanded.add(item.replace("**/", "", 1))
        if expanded == variants:
            return variants
        variants = expanded


def _same_existing_path(first: Path, second: Path) -> bool:
    try:
        return os.path.samefile(first, second)
    except (FileNotFoundError, OSError):
        return False


def _directory_is_case_insensitive(directory: Path) -> bool:
    """Detect the containing filesystem's case behavior without creating a probe."""

    current = directory
    while True:
        name = current.name
        alias = name.swapcase()
        if name and alias != name and _same_existing_path(current, current.with_name(alias)):
            return True
        if current.parent == current:
            break
        current = current.parent
    try:
        children = list(directory.iterdir())
    except OSError:
        return False
    for child in children:
        alias = child.name.swapcase()
        if alias != child.name and _same_existing_path(child, child.with_name(alias)):
            return True
    return False


def _relative_to_base_by_identity(path: Path, base: Path) -> str | None:
    """Relativize a possibly aliased spelling by finding the base directory inode."""

    absolute = Path(os.path.abspath(path))
    try:
        return absolute.relative_to(base).as_posix()
    except ValueError:
        pass
    suffix: list[str] = []
    current = absolute
    while current.parent != current:
        if _same_existing_path(current, base):
            return PurePosixPath(*reversed(suffix)).as_posix()
        suffix.append(current.name)
        current = current.parent
    return None


def _same_destination(first: Path, second: Path) -> bool:
    """Compare existing paths by identity and missing leaf paths by parent identity."""

    if _same_existing_path(first, second):
        return True
    if not _same_existing_path(first.parent, second.parent):
        return False
    if first.name == second.name:
        return True
    return first.name.casefold() == second.name.casefold() and _directory_is_case_insensitive(first.parent)


def _destination_under_directory(destination: Path, directory: Path) -> bool:
    current = destination
    while current.parent != current:
        if _same_destination(current, directory):
            return True
        current = current.parent
    return False


def _destination_matches_glob_by_identity(
    destination: Path, pattern: Path, *, case_insensitive: bool
) -> bool:
    """Match the glob tail after identifying its non-magic parent directory."""

    parts = pattern.parts
    magic_index = next((index for index, part in enumerate(parts) if glob.has_magic(part)), None)
    if magic_index is None:
        return False
    prefix = Path(*parts[:magic_index])
    if not prefix.is_dir():
        return False
    relative = _relative_to_base_by_identity(destination, prefix)
    if relative is None:
        return False
    relative_pattern = PurePosixPath(*parts[magic_index:]).as_posix()
    if case_insensitive:
        relative = relative.casefold()
        relative_pattern = relative_pattern.casefold()
    return any(PurePosixPath(relative).match(item) for item in _glob_variants(relative_pattern))


def _destination_is_selected(destination: Path | str, specs: Iterable[str], base_dir: Path | str) -> bool:
    base = _absolute_base(base_dir)
    absolute = Path(os.path.abspath(destination))
    relative = _relative_to_base_by_identity(absolute, base)
    if relative is None:
        return False
    case_insensitive = _directory_is_case_insensitive(base)
    for spec in specs:
        raw = Path(spec)
        pattern_path = raw if raw.is_absolute() else base / raw
        pattern = Path(os.path.abspath(pattern_path))
        if raw.is_absolute():
            relative_pattern = _relative_to_base_by_identity(pattern, base)
        else:
            relative_pattern = raw.as_posix()
        if relative_pattern is None:
            continue
        if glob.has_magic(str(pattern_path)):
            destination_match = relative.casefold() if case_insensitive else relative
            pattern_match = relative_pattern.casefold() if case_insensitive else relative_pattern
            if any(
                PurePosixPath(destination_match).match(item)
                for item in _glob_variants(pattern_match)
            ) or _destination_matches_glob_by_identity(
                absolute, pattern, case_insensitive=case_insensitive
            ):
                return True
        elif _same_destination(absolute, pattern) or (
            pattern.is_dir() and _destination_under_directory(absolute, pattern)
        ):
            return True
    return False


def _create_command(args: argparse.Namespace) -> int:
    all_specs = [*args.input, *args.config, *args.prompt, *args.ontology, *args.output]
    if _destination_is_selected(args.manifest, all_specs, args.base_dir):
        raise ManifestError("manifest destination is included in a selected artifact specification")
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
    # A manifest inside the repository may itself change dirty state. Capture
    # the post-write state and rewrite once; that state is then stable.
    post_write_git = git_metadata(args.base_dir)
    if post_write_git != manifest["compatibility"]["code"]:
        manifest["compatibility"]["code"] = copy.deepcopy(post_write_git)
        manifest["metadata"]["git"] = post_write_git
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
    settings_supplied = args.setting is not None or args.no_settings
    proposed = (
        args.provider, args.model, settings_supplied, args.parser_version, args.normalization_version
    )
    supplied = [value is not None and value is not False for value in proposed]
    if any(supplied) and not all(supplied):
        raise ManifestError(
            "resume compatibility requires --provider, --model, either --setting (repeat as needed) "
            "or --no-settings, --parser-version, and --normalization-version together"
        )
    if not any(supplied):
        return _print_result(
            differences, success="file integrity valid (resume compatibility not checked)",
            failure="file integrity mismatch",
        )

    for label, value in (
        ("provider", args.provider), ("model", args.model),
        ("parser version", args.parser_version),
        ("normalization version", args.normalization_version),
    ):
        if not value:
            raise ManifestError(f"proposed {label} must be a non-empty string")
    current = copy.deepcopy(manifest)
    request = current["compatibility"]["request"]
    versions = current["compatibility"]["versions"]
    request["provider"] = args.provider
    request["model"] = args.model
    request["settings"] = parse_settings(args.setting or [])
    versions["parser"] = args.parser_version
    versions["normalization"] = args.normalization_version
    current_git = git_metadata(args.base_dir)
    current["compatibility"]["code"] = current_git
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
    settings_group = validate.add_mutually_exclusive_group()
    settings_group.add_argument("--setting", action="append", metavar="KEY=VALUE")
    settings_group.add_argument("--no-settings", action="store_true", help="proposed request has no settings")
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
