#!/usr/bin/env python3
"""Valida los facts limpios con formas SHACL mínimas de interoperabilidad."""
from __future__ import annotations

import csv
import logging
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from pyshacl import validate
from rdflib import Namespace, RDF

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.facts_to_csv import load_graph_from_ttl, local_name, typed_entities  # noqa: E402

logging.getLogger("rdflib.term").setLevel(logging.CRITICAL)
SH = Namespace("http://www.w3.org/ns/shacl#")
QUERIES = ROOT / "paper" / "supplement" / "results" / "queries.csv"
SHAPES = ROOT / "paper" / "supplement" / "protocol" / "opmad_extraction_shapes.ttl"
OUT = ROOT / "paper" / "supplement" / "audit"
TARGETS = {
    "Predictive_Maintenance_Article": "ArticleShape",
    "Predictive_maintenance_model": "PredictiveModelShape",
    "Maintainable_item": "MaintainableItemShape",
    "Data_variable": "DataVariableShape",
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    queries = pd.read_csv(QUERIES, sep=";", keep_default_na=False)
    rows: list[dict[str, object]] = []
    total_targets = Counter()
    total_violations = Counter()
    for item in queries.itertuples(index=False):
        path = ROOT / str(item.facts_file).replace("\\", "/")
        graph = load_graph_from_ttl(path)
        entities = typed_entities(graph)
        targets = {shape: len(entities.get(class_name, set())) for class_name, shape in TARGETS.items()}
        total_targets.update(targets)
        conforms, report_graph, _text = validate(
            data_graph=graph,
            shacl_graph=str(SHAPES),
            inference="none",
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
        )
        violations = Counter()
        for result in report_graph.subjects(RDF.type, SH.ValidationResult):
            source_shape = report_graph.value(result, SH.sourceShape)
            if source_shape is not None:
                violations[local_name(source_shape)] += 1
            else:
                violations["unknown_shape"] += 1
        total_violations.update(violations)
        row: dict[str, object] = {
            "query_index": int(item.query_index),
            "facts_file": str(item.facts_file),
            "conforms": bool(conforms),
            "violations": sum(violations.values()),
        }
        for shape in TARGETS.values():
            row[f"targets__{shape}"] = targets[shape]
            row[f"violations__{shape}"] = violations[shape]
        rows.append(row)
    per_file = pd.DataFrame(rows)
    per_file.to_csv(OUT / "shacl_validation_per_file.csv", index=False)
    summary = []
    for shape in TARGETS.values():
        target_n = total_targets[shape]
        violation_n = total_violations[shape]
        summary.append({
            "shape": shape,
            "target_nodes": target_n,
            "violations": violation_n,
            "violation_percent_of_targets": 100.0 * violation_n / target_n if target_n else 0.0,
        })
    summary_df = pd.DataFrame(summary)
    summary_df.to_csv(OUT / "shacl_validation_summary.csv", index=False)
    lines = [
        "# Validación SHACL mínima", "",
        f"Artefactos conformes: **{int(per_file['conforms'].sum())}/{len(per_file)}**. La validación se ejecutó después de retirar las sentencias RDF-star incompatibles con el parser RDF 1.1.", "",
        "| Forma | Nodos objetivo | Violaciones | % |", "|---|---:|---:|---:|",
    ]
    for row in summary_df.itertuples(index=False):
        lines.append(f"| {row.shape} | {row.target_nodes} | {row.violations} | {row.violation_percent_of_targets:.1f}% |")
    lines.extend(["", "Estas formas prueban requisitos estructurales mínimos, no fidelidad respecto del PDF."])
    (OUT / "SHACL_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print((OUT / "SHACL_REPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
