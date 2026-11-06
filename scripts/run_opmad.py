#!/usr/bin/env python3
"""Run OntoCast with fixed OPMAD vocabulary on explicitly selected papers.

Examples (from the repository root):
    .venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 --dry-run
    .venv/bin/python scripts/run_opmad.py --papers OPMAD-S001 --output-dir out/pilot
    .venv/bin/python scripts/run_opmad.py --all --output-dir out/full

Start scripts/subscription-proxy.mjs first when using the default env file.
Run with the Python environment where OntoCast is installed.
"""

import argparse
import csv
import json
import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "papers/opmad_sources.csv"
PDF_DIR = ROOT / "papers/pdfs"
ONTOLOGY = ROOT / "ontologies/opmad-ontocast/OPMAD-ontocast.ttl"
INSTRUCTION = (
    "Extract every predictive maintenance case reported in this paper, not in "
    "other papers cited within it, and all case-related facts expressible using "
    "the supplied ontology."
)
# Exported values take precedence over OntoCast's --env-file settings.
RUN_ENV = {
    "RENDER_MODE": "facts",
    "ONTOLOGY_CONTEXT_MODE": "fixed_single_ontology",
    "ONTOLOGY_CONTEXT_FIXED_ONTOLOGY_ID": (
        "http://www.semanticweb.org/j.montero-jimenez/ontologies/2021/2/OPMAD"
    ),
    "ONTOLOGY_CONTEXT_REQUIRED": "true",
    "WEB_SEARCH_ENABLED": "false",
    "LLM_MAX_INFLIGHT": "1",
    "PARALLEL_WORKERS": "1",
}


@dataclass(frozen=True)
class Paper:
    source_id: str
    doi: str
    title: str
    pdf: Path


def load_papers() -> list[Paper]:
    with SOURCES.open(encoding="utf-8", newline="") as stream:
        papers = []
        for row in csv.DictReader(stream):
            doi = row["doi"].strip().lower()
            source_id = row["source_id"]
            filename = (doi.replace("/", "_") if doi else source_id) + ".pdf"
            papers.append(Paper(source_id, doi, row["title"], PDF_DIR / filename))
    return papers


def select_papers(papers: list[Paper], selectors: list[str] | None) -> list[Paper]:
    if selectors is None:
        return [paper for paper in papers if paper.pdf.is_file()]

    lookup = {
        key.casefold(): paper
        for paper in papers
        for key in (paper.source_id, paper.doi, paper.pdf.name)
        if key
    }
    selected = []
    seen = set()
    for selector in selectors:
        paper = lookup.get(selector.casefold())
        if paper is None:
            raise ValueError(
                f"Unknown paper {selector!r}. Use an exact source ID, DOI, "
                "or PDF filename from papers/opmad_sources.csv and papers/pdfs."
            )
        if not paper.pdf.is_file():
            raise ValueError(f"No PDF for {paper.source_id}: expected {paper.pdf}")
        if paper.source_id not in seen:
            selected.append(paper)
            seen.add(paper.source_id)
    return selected


def load_llm_settings(env_file: Path) -> dict[str, str]:
    # Use the same loader and defaults as OntoCast, including shell overrides.
    try:
        from ontocast.cli.env_files import apply_env_files
        from ontocast.config import LLMConfig
    except ImportError:
        raise ValueError("Run this script with .venv/bin/python, where OntoCast is installed.") from None

    apply_env_files([env_file])
    # Settings are case-insensitive. Remove alternate spellings before pinning.
    for name in list(os.environ):
        if name.upper() in RUN_ENV:
            del os.environ[name]
    os.environ.update(RUN_ENV)
    try:
        llm = LLMConfig()
    except ValueError:
        # Validation errors can contain input values, including credentials.
        raise ValueError("Invalid LLM settings. Check the env file and LLM_* shell variables.") from None
    # Save only model identity, not the configuration containing credentials.
    return {"provider": str(llm.provider), "model_name": str(llm.model_name)}


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument(
        "--papers",
        nargs="+",
        metavar="PAPER",
        help="Exact source IDs, DOIs, or PDF filenames, separated by spaces (no wildcards).",
    )
    selection.add_argument(
        "--all",
        action="store_true",
        help="Run all locally available PDFs listed in papers/opmad_sources.csv.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "out/opmad",
        help=(
            "New output directory; existing directories are never overwritten "
            "(default: out/opmad)."
        ),
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=ROOT / "scripts/ontocast-subscription.env",
        help="OntoCast LLM settings (default: scripts/ontocast-subscription.env).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selection, LLM, and commands without creating files or calling the model.",
    )
    args = parser.parse_args()
    env_file = args.env_file.expanduser().resolve()
    output = args.output_dir.expanduser().resolve()

    try:
        for path in (SOURCES, ONTOLOGY, env_file):
            if not path.is_file():
                raise ValueError(f"Required file not found: {path}")
        papers = load_papers()
        selected = select_papers(papers, args.papers)
        if not selected:
            raise ValueError(f"No local PDFs found in {PDF_DIR}")
        for paper in selected:
            if paper.pdf.stat().st_size == 0:
                raise ValueError(f"PDF is empty: {paper.pdf}")
        if output.exists():
            raise ValueError(
                f"Output directory already exists: {output}. Choose a new --output-dir."
            )
        executable = shutil.which(str(Path(sys.executable).parent / "ontocast"))
        if not executable:
            raise ValueError("Run this script with .venv/bin/python, where OntoCast is installed.")
        llm = load_llm_settings(env_file)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Selected {len(selected)} paper(s). Output: {output}", flush=True)
    print(f"LLM: {llm['provider']}/{llm['model_name']}", flush=True)
    pinned_environment = {
        **RUN_ENV,
        "LLM_PROVIDER": llm["provider"],
        "LLM_MODEL_NAME": llm["model_name"],
    }
    if args.all:
        missing = [paper.source_id for paper in papers if not paper.pdf.is_file()]
        if missing:
            print("Sources without local PDFs (not run): " + ", ".join(missing), flush=True)

    commands = []
    for paper in selected:
        command = [
            executable,
            "--env-file", str(env_file),
            "process",
            "--ontology-dir", str(ONTOLOGY.parent),
            "--input-path", str(paper.pdf),
            "--output-dir", str(output / paper.source_id),
            "--facts-user-instruction", INSTRUCTION,
            "--keep-provenance",
        ]
        commands.append(command)
        print(f"  {paper.source_id}: {paper.pdf.name} — {paper.title}", flush=True)
        if args.dry_run:
            preview = [
                "env", *(f"{key}={value}" for key, value in pinned_environment.items())
            ]
            print(shlex.join([*preview, *command]))
    if args.dry_run:
        return 0

    output.mkdir(parents=True)
    # This records the planned selection, not a claim that every paper finished.
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "instruction": INSTRUCTION,
        "provider": llm["provider"],
        "llm": llm["model_name"],
        "ontology": str(ONTOLOGY),
        "dois": [paper.doi or None for paper in selected],
    }
    (output / "selection.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    environment = {**os.environ, **pinned_environment}
    for index, (paper, command) in enumerate(zip(selected, commands), start=1):
        print(f"\n[{index}/{len(selected)}] Running {paper.source_id}", flush=True)
        result = subprocess.run(command, cwd=ROOT, env=environment)
        if result.returncode:
            print(f"Stopped: OntoCast failed on {paper.source_id}. See {output}", file=sys.stderr)
            return result.returncode if result.returncode > 0 else 1
        facts = output / paper.source_id / f"{paper.pdf.stem}.facts.ttl"
        if not facts.is_file() or facts.stat().st_size == 0:
            print(f"Stopped: no facts file for {paper.source_id}. See {output}", file=sys.stderr)
            return 1
        validation = facts.with_suffix(".validation.json")
        if validation.is_file():
            try:
                report = json.loads(validation.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                print(f"Stopped: unreadable validation report: {validation}", file=sys.stderr)
                return 1
            # Empty renders on non-case material have no stage or reason.
            # Operational failures, such as timeouts, make the paper incomplete
            # even when OntoCast exits zero and writes a partial facts graph.
            failures = [
                failure for failure in report.get("unit_failures", [])
                if failure.get("stage") or failure.get("reason")
            ]
            if failures:
                print(
                    f"Stopped: {paper.source_id} has {len(failures)} failed content "
                    f"unit(s); its facts are incomplete. See {validation}",
                    file=sys.stderr,
                )
                return 1
    print(f"\nFinished {len(selected)} paper(s). Results: {output}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted. Completed papers keep their outputs.", file=sys.stderr)
        sys.exit(130)
    except OSError as exc:
        print(f"Run failed: {exc}", file=sys.stderr)
        sys.exit(1)
