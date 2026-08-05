#!/usr/bin/env python3
"""Describe el sesgo de disponibilidad de PDF entre registros incluidos."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INCLUDED = ROOT / "extraction_papers" / "scopus_export_May 26-2026_included.csv"
MANIFEST = ROOT / "paper" / "supplement" / "protocol" / "extraction_manifest.csv"
OUT = ROOT / "paper" / "supplement" / "audit"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    included = pd.read_csv(INCLUDED, low_memory=False)
    manifest = pd.read_csv(MANIFEST, keep_default_na=False)
    recovered_ids = set(manifest["corpus_id"].astype(str))
    included["pdf_recovered"] = included["corpus_id"].astype(str).isin(recovered_ids)
    oa_text = included["Open Access"].fillna("").astype(str)
    included["oa_route"] = "other/unspecified"
    included.loc[oa_text.str.contains("Green Open Access", case=False), "oa_route"] = "green"
    included.loc[oa_text.str.contains("Bronze Open Access", case=False), "oa_route"] = "bronze"
    included.loc[oa_text.str.contains("Gold Open Access", case=False), "oa_route"] = "gold"
    included.loc[oa_text.str.contains("Hybrid Gold Open Access", case=False), "oa_route"] = "hybrid_gold"
    included["doi_prefix"] = included["DOI"].fillna("").astype(str).str.extract(r"^(10\.\d+)", expand=False).fillna("no DOI")

    rows: list[dict[str, object]] = []
    dimensions = {
        "year": "Year",
        "open_access_route": "oa_route",
        "screening_confidence": "screening_confidence",
        "screening_reason": "screening_reason_category",
        "doi_prefix": "doi_prefix",
        "source_title": "Source title",
    }
    for dimension, column in dimensions.items():
        for value, group in included.groupby(column, dropna=False):
            if dimension in {"doi_prefix", "source_title"} and len(group) < 10:
                continue
            recovered = int(group["pdf_recovered"].sum())
            rows.append({
                "dimension": dimension,
                "group": str(value),
                "included_n": len(group),
                "pdf_recovered_n": recovered,
                "pdf_unavailable_n": len(group) - recovered,
                "recovery_percent": 100.0 * recovered / len(group),
            })
    result = pd.DataFrame(rows).sort_values(["dimension", "included_n"], ascending=[True, False])
    result.to_csv(OUT / "pdf_availability_bias.csv", index=False)
    included[["corpus_id", "Year", "Source title", "Open Access", "screening_confidence", "screening_reason_category", "pdf_recovered"]].to_csv(OUT / "pdf_availability_per_record.csv", index=False)

    year = result[result["dimension"] == "year"]
    oa = result[result["dimension"] == "open_access_route"]
    lines = [
        "# Sesgo de disponibilidad de texto completo", "",
        f"De {len(included)} registros incluidos, {int(included['pdf_recovered'].sum())} tuvieron PDF recuperado y {int((~included['pdf_recovered']).sum())} no lo tuvieron.", "",
        "## Año", "", "| Año | Incluidos | PDF | Recuperación |", "|---:|---:|---:|---:|",
    ]
    for row in year.itertuples(index=False):
        lines.append(f"| {row.group} | {row.included_n} | {row.pdf_recovered_n} | {row.recovery_percent:.1f}% |")
    lines.extend(["", "## Ruta de acceso abierto registrada por Scopus", "", "| Ruta OA | Incluidos | PDF | Recuperación |", "|---|---:|---:|---:|"])
    for row in oa.itertuples(index=False):
        lines.append(f"| {row.group} | {row.included_n} | {row.pdf_recovered_n} | {row.recovery_percent:.1f}% |")
    lines.extend(["", "La disponibilidad no es una asignación aleatoria; las tasas se reportan como amenaza de selección, no como corrección causal."])
    (OUT / "PDF_AVAILABILITY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print((OUT / "PDF_AVAILABILITY_REPORT.md").read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
