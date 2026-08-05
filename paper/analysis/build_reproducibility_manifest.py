#!/usr/bin/env python3
"""Registra versiones y SHA-256 de entradas/código del manuscrito."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper" / "supplement" / "repro"
FILES = [
    "requirements.txt",
    "pipeline/diversity_rerank.py",
    "pipeline/extraction_schema.py",
    "pipeline/facts_to_csv.py",
    "pipeline/seed_ontology/opmad_seed.ttl",
    "scripts/compare_diversity_all_papers.py",
    "tools/cbr/HeadlessCBR.java",
    "paper/analysis/statistical_protocol.py",
    "paper/analysis/statistical_analysis.py",
    "paper/analysis/revision_audit.py",
    "paper/analysis/extended_reranking_analysis.py",
    "paper/analysis/cbr_ablation_analysis.py",
    "paper/analysis/corpus_bias_analysis.py",
    "paper/analysis/shacl_validation.py",
    "paper/analysis/preserve_rdfstar_provenance.py",
    "paper/analysis/build_reproducibility_manifest.py",
    "paper/figures/generate_figures.py",
    "paper/main.tex",
    "paper/references.bib",
    "paper/supplement/protocol/extraction_manifest.csv",
    "paper/supplement/protocol/opmad_extraction_shapes.ttl",
    "paper/supplement/protocol/literature_update_log.md",
    "paper/supplement/results/per_query.csv",
    "paper/supplement/results/queries.csv",
    "paper/supplement/audit/extended_mmr_sensitivity.csv",
    "paper/supplement/audit/cbr_attribute_year_ablations.csv",
    "external/CBR-Ontology-For-Predictive-Maintenance/CBR-Ontology/CBRproject/data/CleanedDATA V12-05-2021.csv",
]
PACKAGES = ["numpy", "pandas", "scipy", "rdflib", "pydantic", "pyshacl", "matplotlib", "python-Levenshtein"]


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command(*args: str) -> str:
    try:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
        return (result.stdout or result.stderr).strip()
    except Exception as exc:
        return f"unavailable: {exc}"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    versions = {}
    for package in PACKAGES:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "not installed"
    file_records = []
    for relative in FILES:
        path = ROOT / relative
        file_records.append({
            "path": relative,
            "exists": path.exists(),
            "bytes": path.stat().st_size if path.exists() else None,
            "sha256": hash_file(path) if path.exists() else None,
        })
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": sys.version,
        "java": command("java", "-version"),
        "latexmk": command("latexmk", "-v").splitlines()[0],
        "git_commit": command("git", "rev-parse", "HEAD"),
        "git_submodules": command("git", "submodule", "status", "--recursive"),
        "packages": versions,
        "files": file_records,
        "model_runtime_note": "LLM extraction is version-dependent; canonical TTL artifacts and their hashes are the reproducible experimental input.",
    }
    (OUT / "software_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "environment.txt").write_text(
        "\n".join([f"{name}=={version}" for name, version in sorted(versions.items())]) + "\n",
        encoding="utf-8",
    )
    print(OUT / "software_manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
