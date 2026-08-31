#!/usr/bin/env python3
"""Run one complete-document OntoCast extraction from a verified corpus record."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Sequence

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pipeline.fulltext import FullTextError, prepare_document, stable_json, utc_now

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_TEMPLATES = {
    "fixed": REPO_ROOT / "pipeline" / "ontocast_config.env",
    "evolved": REPO_ROOT / "pipeline" / "full_mode" / "ontocast_full_config.env",
}


def _read_env_value(path: Path, name: str) -> str | None:
    if not path.is_file():
        return None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip('"').strip("'")
    return None


def subscription_proxy_base() -> str:
    return (
        os.environ.get("LLM_BASE_URL")
        or _read_env_value(REPO_ROOT / ".env", "LLM_BASE_URL")
        or "http://127.0.0.1:8977/v1"
    )


def require_subscription_proxy(base_url: str) -> None:
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY"):
        raise FullTextError(
            "Direct OpenAI API keys are disabled. Use the local Pi Codex subscription proxy."
        )
    health = base_url.rstrip("/")
    if health.endswith("/v1"):
        health = health[:-3]
    health += "/health"
    try:
        with urllib.request.urlopen(health, timeout=5) as response:
            if response.status >= 400:
                raise FullTextError(
                    f"Subscription proxy health check returned {response.status}"
                )
    except (OSError, urllib.error.URLError) as error:
        raise FullTextError(
            f"Subscription proxy is not reachable at {health}. Start tools/pi_codex_openai_proxy.mjs."
        ) from error


def effective_config(condition: str, output_dir: Path, proxy_base: str) -> str:
    template = CONFIG_TEMPLATES[condition]
    values: dict[str, str] = {}
    comments: list[str] = []
    for raw_line in template.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            comments.append(raw_line)
            continue
        if "=" in raw_line:
            key, value = raw_line.split("=", 1)
            values[key.strip()] = value.strip()
    values["LLM_BASE_URL"] = proxy_base
    values["ONTOCAST_WORKING_DIRECTORY"] = str(output_dir.resolve())
    if condition == "fixed":
        values["ONTOCAST_ONTOLOGY_DIRECTORY"] = str(
            (REPO_ROOT / "pipeline" / "seed_ontology").resolve()
        )
    else:
        values.pop("ONTOCAST_ONTOLOGY_DIRECTORY", None)
    lines = [f"{key}={value}" for key, value in values.items()]
    if comments:
        lines.extend(["", *comments])
    return "\n".join(lines).rstrip() + "\n"


def build_ontocast_command(
    ontocast_bin: str, config: Path, input_dir: Path
) -> list[str]:
    """Build the publication command. A chunk-limit option is intentionally absent."""

    return [
        ontocast_bin,
        "--env-file",
        str(config),
        "--input-path",
        str(input_dir),
    ]


def _ensure_new_run_dir(path: Path) -> None:
    if path.exists() and any(path.iterdir()):
        raise FullTextError(f"Run directory is not empty: {path}")
    path.mkdir(parents=True, exist_ok=True)


def run_complete_extraction(
    *,
    condition: str,
    manifest: Path,
    corpus_id: str,
    run_dir: Path,
    ocr_engine: str,
    require_verified: bool,
    prepare_only: bool,
) -> int:
    _ensure_new_run_dir(run_dir)
    prepared_dir = run_dir / "fulltext"
    prepared = prepare_document(
        manifest,
        corpus_id,
        prepared_dir,
        ocr_engine=ocr_engine,
        require_verified=require_verified,
    )
    if prepared.quality_status != "pass":
        raise FullTextError(
            f"Prepared full text failed quality checks. Inspect {prepared.quality}; no extraction was run."
        )

    input_dir = run_dir / "input"
    output_dir = run_dir / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    staged_input = input_dir / "document.json"
    shutil.copy2(prepared.input_json, staged_input)

    proxy_base = subscription_proxy_base()
    config_path = run_dir / "ontocast.env"
    config_path.write_text(
        effective_config(condition, output_dir, proxy_base),
        encoding="utf-8",
        newline="\n",
    )
    run_metadata = {
        "schema_version": "complete-fulltext-run/1.0",
        "created_at": utc_now(),
        "condition": condition,
        "corpus_id": corpus_id,
        "complete_document": True,
        "head_chunks": None,
        "prepared_fulltext": str(prepared_dir),
        "staged_input": str(staged_input),
        "effective_config": str(config_path),
        "status": "prepared",
    }
    metadata_path = run_dir / "fulltext-run.json"
    metadata_path.write_text(stable_json(run_metadata), encoding="utf-8", newline="\n")
    if prepare_only:
        print(f"Prepared complete document at {prepared_dir}")
        return 0

    ontocast_bin = shutil.which("ontocast")
    if not ontocast_bin:
        raise FullTextError(
            "OntoCast CLI not found. Activate .venv and run scripts/setup_submodules.* first."
        )
    require_subscription_proxy(proxy_base)
    command = build_ontocast_command(ontocast_bin, config_path, input_dir)
    if "--head-chunks" in command:
        raise FullTextError("Publication extraction must not use --head-chunks")

    log_path = run_dir / "run.log"
    with log_path.open("w", encoding="utf-8", newline="\n") as log:
        process = subprocess.Popen(
            command,
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        assert process.stdout is not None
        for line in process.stdout:
            print(line, end="")
            log.write(line)
        return_code = process.wait()
    if return_code != 0:
        run_metadata["status"] = "failed"
        run_metadata["exit_code"] = return_code
        metadata_path.write_text(
            stable_json(run_metadata), encoding="utf-8", newline="\n"
        )
        return return_code

    facts = sorted(output_dir.glob("facts_*.ttl"))
    ontologies = sorted(output_dir.glob("ontology_*.ttl"))
    if not facts:
        raise FullTextError(f"No facts TTL was produced in {output_dir}")
    if condition == "evolved" and not ontologies:
        raise FullTextError(f"No evolved ontology TTL was produced in {output_dir}")
    run_metadata.update(
        {
            "status": "completed",
            "finished_at": utc_now(),
            "facts": [str(path) for path in facts],
            "ontologies": [str(path) for path in ontologies],
            "log": str(log_path),
        }
    )
    metadata_path.write_text(stable_json(run_metadata), encoding="utf-8", newline="\n")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=("fixed", "evolved"), required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--corpus-id", required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument(
        "--ocr-engine", choices=("easyocr", "rapidocr", "auto"), default="easyocr"
    )
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument(
        "--allow-provisional",
        action="store_true",
        help="Development only: bypass verified/frozen corpus gates",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run_complete_extraction(
            condition=args.condition,
            manifest=args.manifest,
            corpus_id=args.corpus_id,
            run_dir=args.run_dir,
            ocr_engine=args.ocr_engine,
            require_verified=not args.allow_provisional,
            prepare_only=args.prepare_only,
        )
    except FullTextError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
