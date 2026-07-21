#!/usr/bin/env python3
"""Cross-platform build for the vendored CBR headless jar."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


CBR_REL = Path(
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject"
)
HEADLESS_REL = Path("tools/cbr/HeadlessCBR.java")


class BuildError(RuntimeError):
    """Raised for local build precondition failures."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def display(path: Path) -> str:
    return str(path.resolve())


def argfile_token(path: Path) -> str:
    """Return a javac @argfile-safe path token.

    javac argfiles are whitespace-delimited. Use forward slashes and quote any
    path containing whitespace so checkouts under directories such as
    "C:/Users/Name With Spaces" still work on Windows.
    """

    text = path.resolve().as_posix()
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    if any(char.isspace() for char in text):
        return f'"{text}"'
    return text


def run(command: list[str]) -> None:
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError as exc:
        raise BuildError(f"Required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"Command failed with exit code {exc.returncode}: {command[0]}") from exc


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        raise BuildError(f"Required command not found on PATH: {name}")


def build(root: Path) -> Path:
    cbr_dir = root / CBR_REL
    source_dir = cbr_dir / "src"
    libs_dir = cbr_dir / "external-libs"
    headless_java = root / HEADLESS_REL

    if not source_dir.is_dir():
        raise BuildError(f"Missing CBR source directory: {source_dir}")
    if not libs_dir.is_dir():
        raise BuildError(f"Missing CBR external-libs directory: {libs_dir}")
    if not headless_java.is_file():
        raise BuildError(f"Missing local HeadlessCBR source: {headless_java}")

    require_command("javac")
    require_command("jar")

    build_dir = root / ".build" / "cbr"
    upstream_bin = build_dir / "upstream-bin"
    local_bin = build_dir / "local-bin"
    dist_dir = build_dir / "dist"
    jar_path = dist_dir / "ontologies-cbr-headless.jar"

    for directory in (upstream_bin, local_bin):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    dist_dir.mkdir(parents=True, exist_ok=True)

    jars = sorted(libs_dir.rglob("*.jar"), key=lambda path: path.as_posix())
    if not jars:
        raise BuildError(f"No jar dependencies found below: {libs_dir}")

    upstream_sources = sorted(source_dir.rglob("*.java"), key=lambda path: path.as_posix())
    if not upstream_sources:
        raise BuildError(f"No Java sources found below: {source_dir}")

    classpath = os.pathsep.join(display(path) for path in jars)
    upstream_sources_file = build_dir / "upstream-sources.txt"
    upstream_sources_file.write_text(
        "\n".join(argfile_token(path) for path in upstream_sources) + "\n",
        encoding="utf-8",
    )

    run(
        [
            "javac",
            "-encoding",
            "ISO-8859-1",
            "-cp",
            classpath,
            "-d",
            display(upstream_bin),
            f"@{upstream_sources_file}",
        ]
    )

    local_classpath = os.pathsep.join([display(upstream_bin), classpath])
    run(
        [
            "javac",
            "-encoding",
            "UTF-8",
            "-cp",
            local_classpath,
            "-d",
            display(local_bin),
            display(headless_java),
        ]
    )

    run(
        [
            "jar",
            "--create",
            "--file",
            display(jar_path),
            "-C",
            display(upstream_bin),
            ".",
            "-C",
            display(local_bin),
            ".",
        ]
    )

    (build_dir / "classpath.txt").write_text(
        os.pathsep.join([display(local_bin), display(upstream_bin), classpath]) + "\n",
        encoding="utf-8",
    )
    (build_dir / "jar-classpath.txt").write_text(
        os.pathsep.join([display(jar_path), classpath]) + "\n",
        encoding="utf-8",
    )

    print("Built CBR classes and jar")
    print(f"  upstream:      {upstream_bin}")
    print(f"  local:         {local_bin}")
    print(f"  jar:           {jar_path}")
    print(f"  cp file:       {build_dir / 'classpath.txt'}")
    print(f"  jar cp file:   {build_dir / 'jar-classpath.txt'}")
    return jar_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the CBR Java sources and HeadlessCBR jar."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=repo_root(),
        help="Repository root (default: inferred from this script).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        build(args.root.resolve())
        return 0
    except BuildError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
