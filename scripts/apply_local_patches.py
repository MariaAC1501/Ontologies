#!/usr/bin/env python3
"""Apply Diversity-in-CBR patches and validate the unpatched dependencies."""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


DEPENDENCIES = ("all", "ontocast", "cbr", "diversity")


class PatchError(RuntimeError):
    """Raised when a required patch anchor or submodule is missing."""


@dataclass(frozen=True)
class PatchResult:
    dependency: str
    path: Path
    label: str
    status: str


class LocalPatcher:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.results: list[PatchResult] = []
        self.notes: list[str] = []

    def rel(self, path: Path) -> Path:
        try:
            return path.resolve().relative_to(self.root)
        except ValueError:
            return path

    def require_submodule(self, dependency: str, rel_path: str) -> Path:
        path = self.root / rel_path
        if not path.is_dir() or not (path / ".git").exists():
            raise PatchError(
                f"[{dependency}] Missing initialized submodule: {path}. "
                f"Run: git submodule update --init --recursive {rel_path}"
            )
        self.notes.append(f"[{dependency}] validated submodule: {self.rel(path)}")
        return path

    def replace_exact(
        self,
        dependency: str,
        path: Path,
        old: str,
        new: str,
        label: str,
    ) -> None:
        """Replace exact anchors idempotently, retaining the file's line endings."""
        if not path.is_file():
            raise PatchError(f"[{dependency}] Missing file required by patch: {path}")
        raw = path.read_bytes().decode("utf-8")
        crlf_count = raw.count("\r\n")
        newline = "\r\n" if crlf_count > raw.count("\n") - crlf_count else "\n"
        text = raw.replace("\r\n", "\n").replace("\r", "\n")
        rel_path = self.rel(path)
        if new in text:
            self.results.append(PatchResult(dependency, rel_path, label, "already"))
            return
        if old not in text:
            raise PatchError(
                f"[{dependency}] Expected patch anchor not found in {rel_path} "
                f"for '{label}'. Anchor preview:\n{old[:500]}"
            )
        replacement = text.replace(old, new)
        if newline != "\n":
            replacement = replacement.replace("\n", newline)
        path.write_bytes(replacement.encode("utf-8"))
        self.results.append(PatchResult(dependency, rel_path, label, "patched"))

    def changed_files(self) -> list[Path]:
        return sorted({result.path for result in self.results if result.status == "patched"})


def locate_repo_root() -> Path:
    for start in (Path(__file__).resolve().parent, Path.cwd().resolve()):
        for candidate in (start, *start.parents):
            if (candidate / ".git").exists() and (candidate / ".gitmodules").exists():
                return candidate
    raise PatchError("Could not locate repository root (expected .git and .gitmodules).")


def validate_ontocast(patcher: LocalPatcher) -> None:
    patcher.require_submodule("ontocast", "external/ontocast")
    patcher.notes.append(
        "[ontocast] stock upstream; no source patches. The subscription proxy "
        "uses LLM_BASE_URL and a non-secret LLM_API_KEY placeholder."
    )


def apply_diversity(patcher: LocalPatcher) -> None:
    submodule = patcher.require_submodule(
        "diversity", "external/Diversity-Improvement-in-CBR"
    )

    patcher.replace_exact(
        "diversity",
        submodule / "Methods.py",
        "import gensim.downloader as api\nfrom numpy import dot\nfrom numpy.linalg import norm\nimport Levenshtein\n#API for text semantic text similarity\nword2vec_model = api.load(\"glove-wiki-gigaword-50\")\n#Case Base comes from an Excel provided by the supervisor\npath = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\CleanedDATA V12-05-2021.csv'\ndf = pd.read_csv(path, sep=';', encoding='windows-1252')\n",
        "try:\n    import gensim.downloader as api\nexcept ImportError:  # Optional; only needed by the unused semantic similarity helper.\n    api = None\nfrom numpy import dot\nfrom numpy.linalg import norm\nimport Levenshtein\nfrom pathlib import Path\n#API for text semantic text similarity\nword2vec_model = None\n#Case Base comes from an Excel provided by the supervisor\n_SUBMODULE_DIR = Path(__file__).resolve().parent\npath = _SUBMODULE_DIR / \"Datasets\" / \"CleanedDATA V12-05-2021.csv\"\ndf = pd.read_csv(path, sep=';', encoding='windows-1252')\n",
        "Methods dataset path relative and optional gensim",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Methods2.py",
        "import random\n#API for text semantic text similarity\n#word2vec_model = api.load(\"glove-wiki-gigaword-50\")\n\n#Case Base comes from an Excel provided by the supervisor\npath = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\CleanedDATA V12-05-2021.csv'\npath_performance = r'C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\performance_normalized_averaged.csv'\n",
        "import random\nfrom pathlib import Path\n#API for text semantic text similarity\n#word2vec_model = api.load(\"glove-wiki-gigaword-50\")\n\n#Case Base comes from an Excel provided by the supervisor\n_SUBMODULE_DIR = Path(__file__).resolve().parent\npath = _SUBMODULE_DIR / \"Datasets\" / \"CleanedDATA V12-05-2021.csv\"\npath_performance = _SUBMODULE_DIR / \"Datasets\" / \"performance_normalized_averaged.csv\"\n",
        "Methods2 dataset paths relative to submodule",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Methods2.py",
        "        if DistFin>=6:\n            Sim=0.1\n        elif (DistFin<5 and DistFin>2):\n            Sim=0.5\n        elif DistFin<2:\n            Sim=0.8\n        elif DistFin==0:\n            Sim=1\n        return Sim\n",
        "        if DistFin==0:\n            Sim=1\n        elif DistFin>=6:\n            Sim=0.1\n        elif (DistFin<5 and DistFin>2):\n            Sim=0.5\n        elif DistFin<2:\n            Sim=0.8\n        return Sim\n",
        "SimTaxon exact match returns 1",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Validation.py",
        "        solutions_condensed,descriptions_condensed=apply_CNN(sol, des, CaseBase_Train, weights_description, weights_solution)\n",
        "        solutions_condensed,descriptions_condensed=apply_CNN(des, sol, CaseBase_Train, weights_description, weights_solution)\n",
        "Validation apply_CNN threshold order",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Validation.py",
        "            diversity=retrieval_for_ModCNN(solutions_condensed,descriptions_condensed,query)\n",
        "            diversity=retrieval_for_ModCNN(solutions_condensed,descriptions_condensed,query,weights_description,weights_solution)\n",
        "Validation retrieval_for_ModCNN passes weights",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Modified_Condensed_Nearest_Neighbors.py",
        "    for most_similar in similar_GC:\n        for generalized_solution in solutions_store:\n            if generalized_solution.parent_description == most_similar[0]:\n                list_solution.append(generalized_solution)\n                if len(list_solution) >= amount:\n                    return list_solution\n\n\ndef compute_diversity(candidates,weights):\n",
        "    for most_similar in similar_GC:\n        for generalized_solution in solutions_store:\n            if generalized_solution.parent_description == most_similar[0]:\n                list_solution.append(generalized_solution)\n                if len(list_solution) >= amount:\n                    return list_solution\n    return list_solution\n\n\ndef compute_diversity(candidates,weights):\n",
        "search_solutions_from_descriptions returns partial results",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "import re\n\n#Nuevo\nimport pandas as pd\nfrom sklearn import preprocessing\n",
        "import re\nfrom pathlib import Path\n\n#Nuevo\nimport pandas as pd\nfrom sklearn import preprocessing\n",
        "Performance generator imports pathlib",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "path = r\"C:\\Users\\emman\\Documents\\TEC\\Diversity-Improvement-in-CBR\\Datasets\\Performance_cleaned.xlsx\"\ndf = pd.read_excel(path)\n",
        "_SUBMODULE_DIR = Path(__file__).resolve().parent\n_DATASET_DIR = _SUBMODULE_DIR / \"Datasets\"\npath = _DATASET_DIR / \"Performance_cleaned.xlsx\"\ndf = pd.read_excel(path)\n",
        "Performance generator input path relative to submodule",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_excel('Performance.xlsx', index=False)\n",
        "Performance.to_excel(_DATASET_DIR / 'Performance.xlsx', index=False)\n",
        "Performance generator writes cleaned workbook under Datasets",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_excel('performance_normalized.xlsx', index=False)\n",
        "Performance.to_excel(_DATASET_DIR / 'performance_normalized.xlsx', index=False)\n",
        "Performance generator writes normalized workbook under Datasets",
    )
    patcher.replace_exact(
        "diversity",
        submodule / "Performance_Dataset_Generation.py",
        "Performance.to_csv('performance_normalized_averaged.csv', index=False)\n",
        "Performance.to_csv(_DATASET_DIR / 'performance_normalized_averaged.csv', index=False)\n",
        "Performance generator writes normalized csv under Datasets",
    )


def validate_cbr(patcher: LocalPatcher) -> None:
    patcher.require_submodule("cbr", "external/CBR-Ontology-For-Predictive-Maintenance")
    patcher.notes.append("[cbr] no local patches registered; existence validation only")


def selected_dependencies(value: str) -> tuple[str, ...]:
    return ("ontocast", "cbr", "diversity") if value == "all" else (value,)


def print_summary(patcher: LocalPatcher, dependencies: tuple[str, ...]) -> None:
    print(f"Local patch root: {patcher.root}")
    print(f"Dependencies requested: {', '.join(dependencies)}")
    for note in patcher.notes:
        print(f"  - {note}")
    for result in patcher.results:
        print(f"  - [{result.dependency}] {result.status:7} {result.path} :: {result.label}")
    print("Changed files:")
    for path in patcher.changed_files():
        print(f"  - {path}")
    if not patcher.changed_files():
        print("  - none (already patched or validation-only run)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dependency", choices=DEPENDENCIES, default="all")
    args = parser.parse_args(argv)
    try:
        patcher = LocalPatcher(locate_repo_root())
        dependencies = selected_dependencies(args.dependency)
        actions = {
            "ontocast": validate_ontocast,
            "cbr": validate_cbr,
            "diversity": apply_diversity,
        }
        for dependency in dependencies:
            actions[dependency](patcher)
        print_summary(patcher, dependencies)
        return 0
    except PatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
