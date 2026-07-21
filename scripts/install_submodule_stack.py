#!/usr/bin/env python3
"""Install/build the submodule-first local stack for this repository."""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import site
import stat
import subprocess
import sys
import sysconfig
from pathlib import Path


SUBMODULES = (
    "external/CBR-Ontology-For-Predictive-Maintenance",
    "external/Diversity-Improvement-in-CBR",
    "external/ontocast",
)
ONTOCAST_EXTRA_DEPS = (
    # Imported by OntoCast 0.3.0 but not declared in its pyproject dependencies.
    "pydantic-settings",
    "python-dotenv",
)
DIVERSITY_DEPS = (
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "python-Levenshtein",
    "openpyxl",
)
CBR_DATA_REL = Path(
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data"
)


class InstallError(RuntimeError):
    """Raised for local installation precondition failures."""


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def stringify_command(command: list[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(command)
    return " ".join(shlex.quote(part) for part in command)


def run(command: list[str | Path], *, cwd: Path, label: str) -> None:
    command_str = [str(part) for part in command]
    print(f"\n==> {label}")
    print(f"$ {stringify_command(command_str)}")
    try:
        subprocess.run(command_str, cwd=str(cwd), check=True)
    except FileNotFoundError as exc:
        raise InstallError(f"Required command not found: {command_str[0]}") from exc
    except subprocess.CalledProcessError as exc:
        raise InstallError(
            f"Step failed with exit code {exc.returncode}: {label}"
        ) from exc


def require_dir(path: Path, description: str) -> None:
    if not path.is_dir():
        raise InstallError(f"Missing {description}: {path}")


def uv_pip_install(root: Path, arguments: list[str | Path], *, label: str) -> None:
    """Install into this interpreter's environment through uv."""
    uv = os.environ.get("UV", "uv")
    if shutil.which(uv) is None:
        raise InstallError(
            "uv is required for dependency installation. Install it from https://docs.astral.sh/uv/"
        )
    run(
        [uv, "pip", "install", "--python", sys.executable, *arguments],
        cwd=root,
        label=label,
    )


def update_submodules(root: Path) -> None:
    run(
        ["git", "submodule", "update", "--init", "--recursive", *SUBMODULES],
        cwd=root,
        label="Update git submodules",
    )


def apply_patches(root: Path) -> None:
    run(
        [sys.executable, root / "scripts" / "apply_local_patches.py"],
        cwd=root,
        label="Apply local submodule patches",
    )


def install_ontocast(root: Path, *, no_deps: bool) -> None:
    ontocast_dir = root / "external" / "ontocast"
    require_dir(ontocast_dir, "ontocast submodule")

    if no_deps:
        print("\n==> Install OntoCast extra Python dependencies")
        print("Skipping uv dependency install because --no-deps was requested")
    else:
        uv_pip_install(
            root,
            list(ONTOCAST_EXTRA_DEPS),
            label="Install OntoCast extra Python dependencies with uv",
        )

    command: list[str | Path] = []
    if no_deps:
        command.append("--no-deps")
    command.extend(["-e", f"{ontocast_dir}[doc-processing]"])
    uv_pip_install(root, command, label="Install ontocast editable with uv")


def site_packages_dir() -> Path:
    purelib = sysconfig.get_path("purelib")
    if purelib:
        return Path(purelib)

    candidates = site.getsitepackages()
    if candidates:
        return Path(candidates[0])

    raise InstallError("Could not determine this Python environment's site-packages")


def install_diversity(root: Path, *, no_deps: bool) -> None:
    diversity_dir = root / "external" / "Diversity-Improvement-in-CBR"
    require_dir(diversity_dir, "Diversity-Improvement-in-CBR submodule")

    if no_deps:
        print("\n==> Install Diversity Python dependencies")
        print("Skipping uv dependency install because --no-deps was requested")
    else:
        uv_pip_install(
            root,
            list(DIVERSITY_DEPS),
            label="Install Diversity Python dependencies with uv",
        )

    target_dir = site_packages_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    pth_path = target_dir / "ontologies_diversity_cbr.pth"
    pth_path.write_text(str(diversity_dir.resolve()) + "\n", encoding="utf-8")
    print(f"\n==> Register Diversity submodule on Python path")
    print(f"Wrote: {pth_path}")


def build_cbr(root: Path) -> None:
    run(
        [sys.executable, root / "scripts" / "build_cbr.py"],
        cwd=root,
        label="Build CBR headless jar",
    )


def batch_literal(value: Path | str) -> str:
    return str(value).replace("%", "%%")


def install_cbr_wrapper(root: Path) -> None:
    scripts_path = sysconfig.get_path("scripts")
    if not scripts_path:
        raise InstallError("Could not determine this Python environment's scripts directory")
    bin_dir = Path(scripts_path)
    bin_dir.mkdir(parents=True, exist_ok=True)

    if os.name == "nt":
        wrapper = bin_dir / "ontologies-cbr.bat"
        root_text = batch_literal(root.resolve())
        data_text = batch_literal((root / CBR_DATA_REL).resolve())
        wrapper.write_text(
            "@echo off\n"
            "setlocal\n"
            f"set \"REPO_ROOT={root_text}\"\n"
            "set \"CP_FILE=%REPO_ROOT%\\.build\\cbr\\jar-classpath.txt\"\n"
            "if not exist \"%CP_FILE%\" (\n"
            "  echo CBR build classpath not found: %CP_FILE% 1>&2\n"
            "  exit /b 1\n"
            ")\n"
            "set /p CBR_CLASSPATH=<\"%CP_FILE%\"\n"
            "if defined ONTOLOGIES_CBR_DATA_DIR (\n"
            "  set \"CBR_DATA_DIR=%ONTOLOGIES_CBR_DATA_DIR%\"\n"
            ") else (\n"
            f"  set \"CBR_DATA_DIR={data_text}\"\n"
            ")\n"
            "java -Djava.awt.headless=true -cp \"%CBR_CLASSPATH%\" HeadlessCBR --data-dir \"%CBR_DATA_DIR%\" %*\n",
            encoding="utf-8",
        )

        # Useful from Git Bash/MSYS, where extensionless commands are preferred.
        posix_launcher = bin_dir / "ontologies-cbr"
        posix_launcher.write_text(
            "#!/usr/bin/env python\n"
            "import os\n"
            "import subprocess\n"
            "import sys\n\n"
            f"repo_root = {str(root.resolve())!r}\n"
            "cp_file = os.path.join(repo_root, '.build', 'cbr', 'jar-classpath.txt')\n"
            "if not os.path.isfile(cp_file):\n"
            "    print(f'CBR build classpath not found: {cp_file}', file=sys.stderr)\n"
            "    raise SystemExit(1)\n"
            "with open(cp_file, encoding='utf-8') as handle:\n"
            "    classpath = handle.read().strip()\n"
            f"default_data_dir = {str((root / CBR_DATA_REL).resolve())!r}\n"
            "data_dir = os.environ.get('ONTOLOGIES_CBR_DATA_DIR') or default_data_dir\n"
            "cmd = ['java', '-Djava.awt.headless=true', '-cp', classpath, 'HeadlessCBR', '--data-dir', data_dir, *sys.argv[1:]]\n"
            "raise SystemExit(subprocess.call(cmd))\n",
            encoding="utf-8",
        )
        posix_launcher.chmod(posix_launcher.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print("\n==> Install CBR wrapper")
        print(f"Wrote: {wrapper}")
        print(f"Wrote: {posix_launcher}")
    else:
        wrapper = bin_dir / "ontologies-cbr"
        root_q = shlex.quote(str(root.resolve()))
        data_q = shlex.quote(str((root / CBR_DATA_REL).resolve()))
        wrapper.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n\n"
            f"REPO_ROOT={root_q}\n"
            f"DEFAULT_CBR_DATA_DIR={data_q}\n"
            "CP_FILE=\"$REPO_ROOT/.build/cbr/jar-classpath.txt\"\n"
            "if [ ! -f \"$CP_FILE\" ]; then\n"
            "  echo \"CBR build classpath not found: $CP_FILE\" >&2\n"
            "  exit 1\n"
            "fi\n"
            "CLASSPATH=$(<\"$CP_FILE\")\n"
            "CBR_DATA_DIR=${ONTOLOGIES_CBR_DATA_DIR:-$DEFAULT_CBR_DATA_DIR}\n"
            "exec java -Djava.awt.headless=true -cp \"$CLASSPATH\" HeadlessCBR --data-dir \"$CBR_DATA_DIR\" \"$@\"\n",
            encoding="utf-8",
        )
        wrapper.chmod(wrapper.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print("\n==> Install CBR wrapper")
        print(f"Wrote: {wrapper}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize submodules, apply local patches, install editable Python "
            "submodules, and build the CBR wrapper stack."
        )
    )
    parser.add_argument(
        "--skip-submodules",
        action="store_true",
        help="Do not run git submodule update --init --recursive.",
    )
    parser.add_argument(
        "--skip-patches",
        action="store_true",
        help="Do not run scripts/apply_local_patches.py.",
    )
    parser.add_argument(
        "--skip-ontocast",
        action="store_true",
        help="Do not install external/ontocast in editable mode with uv.",
    )
    parser.add_argument(
        "--skip-diversity",
        action="store_true",
        help="Do not install Diversity dependencies or create its .pth file.",
    )
    parser.add_argument(
        "--skip-cbr",
        action="store_true",
        help="Do not build the CBR jar or install the ontologies-cbr wrapper.",
    )
    parser.add_argument(
        "--no-deps",
        action="store_true",
        help=(
            "Avoid uv dependency installation. ontocast is still installed "
            "editable with uv --no-deps unless --skip-ontocast is also used."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = repo_root()
    print(f"Repository root: {root}")

    try:
        if args.skip_submodules:
            print("\n==> Update git submodules")
            print("Skipping because --skip-submodules was requested")
        else:
            update_submodules(root)

        if args.skip_patches:
            print("\n==> Apply local submodule patches")
            print("Skipping because --skip-patches was requested")
        else:
            apply_patches(root)

        if args.skip_ontocast:
            print("\n==> Install ontocast editable with uv")
            print("Skipping because --skip-ontocast was requested")
        else:
            install_ontocast(root, no_deps=args.no_deps)

        if args.skip_diversity:
            print("\n==> Install/register Diversity submodule")
            print("Skipping because --skip-diversity was requested")
        else:
            install_diversity(root, no_deps=args.no_deps)

        if args.skip_cbr:
            print("\n==> Build/install CBR")
            print("Skipping because --skip-cbr was requested")
        else:
            build_cbr(root)
            install_cbr_wrapper(root)

        print("\nSubmodule stack setup completed.")
        return 0
    except InstallError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
