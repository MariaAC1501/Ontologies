#!/usr/bin/env python3
"""Preserva en un sidecar comprimido la procedencia RDF-star retirada al parsear."""
from __future__ import annotations

import csv
import gzip
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
QUERIES = ROOT / "paper" / "supplement" / "results" / "queries.csv"
OUT = ROOT / "paper" / "supplement" / "audit" / "rdfstar_provenance_sidecar.csv.gz"
PATTERN = re.compile(
    r"(?ms)^(_:[^\s]+)\s+rdf:reifies\s+<<\(\s*(.*?)\s*\)>>\s*;\s*\n\s*prov:wasDerivedFrom\s+([^\s]+)\s*\.\s*$"
)


def main() -> int:
    queries = pd.read_csv(QUERIES, sep=";", keep_default_na=False)
    count = 0
    with gzip.open(OUT, "wt", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["query_index", "facts_file", "reification_node", "statement_turtle", "prov_wasDerivedFrom"])
        for item in queries.itertuples(index=False):
            path = ROOT / str(item.facts_file).replace("\\", "/")
            text = path.read_text(encoding="utf-8")
            matches = PATTERN.findall(text)
            for node, statement, source in matches:
                writer.writerow([int(item.query_index), str(item.facts_file), node, " ".join(statement.split()), source])
            count += len(matches)
    if count != 311559:
        raise RuntimeError(f"Expected 311559 RDF-star statements, preserved {count}")
    print(f"Preserved {count} RDF-star provenance records in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
