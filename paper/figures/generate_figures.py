#!/usr/bin/env python3
"""Genera las figuras del manuscrito a partir del experimento V12 corregido."""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
STATS = ROOT / "paper" / "supplement" / "statistics"
AUDIT = ROOT / "paper" / "supplement" / "audit"
RESULTS = ROOT / "paper" / "supplement" / "results"
OUT = Path(__file__).resolve().parent

COLORS = {"base": "#4C78A8", "mmr": "#E45756", "ild": "#54A24B"}
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "figure.dpi": 160,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.pdf")
    fig.savefig(OUT / f"{stem}.png", dpi=300)
    plt.close(fig)


def global_metrics() -> None:
    data = {r["metric_id"]: r for r in rows(STATS / "paired_metric_summary.csv") if r["task"] == "ALL"}
    specs = [
        ("mean_similarity_top5", "Similitud media top-5", (0.545, 0.565), 4),
        ("unique_models_top5", "Firmas de modelos únicas", (4.65, 5.04), 3),
        ("intra_list_dissimilarity", "Disimilitud intra-lista", (0.39, 0.56), 4),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.15, 3.05))
    for ax, (key, title, ylim, decimals) in zip(axes, specs):
        r = data[key]
        y = [float(r["baseline_mean"]), float(r["diverse_mean"])]
        ax.plot([0, 1], y, color="#777777", lw=1.2, zorder=1)
        ax.scatter([0], [y[0]], s=55, color=COLORS["base"], label="CBR", zorder=2)
        ax.scatter([1], [y[1]], s=55, color=COLORS["mmr"], label="CBR+MMR", zorder=2)
        ax.set_xticks([0, 1], ["CBR", "CBR+MMR"])
        ax.set_xlim(-0.35, 1.35)
        ax.set_ylim(*ylim)
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.2)
        change = float(r["mean_change"])
        lo = float(r["ci95_mean_change_low"])
        hi = float(r["ci95_mean_change_high"])
        ax.text(
            0.5,
            0.04,
            f"Δ={change:.{decimals}f}\nIC95% [{lo:.{decimals}f}, {hi:.{decimals}f}]",
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=8.5,
        )
    axes[0].set_ylabel("Media algorítmica")
    fig.suptitle("Efecto pareado del reranking (n=1.821 consultas)", y=1.03, fontsize=10.5)
    fig.tight_layout()
    save(fig, "metricas_globales")


def lambda_tradeoff() -> None:
    data = rows(STATS / "sensitivity_lambda_overview.csv")
    lam = np.array([float(r["lambda_relevance"]) for r in data])
    sim = np.array([float(r["mean_similarity_top5"]) for r in data])
    ild = np.array([float(r["mean_intra_list_dissimilarity"]) for r in data])

    fig, ax1 = plt.subplots(figsize=(5.3, 3.0))
    ax2 = ax1.twinx()
    ax1.plot(lam, sim, marker="o", lw=1.8, color=COLORS["base"], label="Similitud media top-5")
    ax2.plot(lam, ild, marker="s", lw=1.8, color=COLORS["ild"], label="Disimilitud intra-lista")
    ax1.axvline(0.7, color="#777777", ls="--", lw=1, alpha=0.8)
    ax1.text(0.705, sim.min() + 0.0003, "configuración principal", rotation=90, va="bottom", fontsize=7.5)
    ax1.set_xlabel(r"Peso de relevancia $\lambda$")
    ax1.set_ylabel("Similitud media top-5", color=COLORS["base"])
    ax2.set_ylabel("Disimilitud intra-lista", color=COLORS["ild"])
    ax1.tick_params(axis="y", labelcolor=COLORS["base"])
    ax2.tick_params(axis="y", labelcolor=COLORS["ild"])
    ax1.set_xticks(lam)
    ax1.grid(alpha=0.2)
    lines = ax1.get_lines()[:1] + ax2.get_lines()[:1]
    ax1.legend(lines, [line.get_label() for line in lines], loc="center left", frameon=False)
    fig.tight_layout()
    save(fig, "sensibilidad_lambda")


def field_coverage() -> None:
    selected = {
        "Task": "Tarea",
        "Case study": "Activo",
        "Input type": "Variables de entrada",
        "Models": "Modelos",
        "Model Type": "Tipo de modelo",
        "Study title": "Título",
        "Publication identifier": "Identificador",
        "Input for the model": "Modalidad de entrada",
        "Online/Off-line": "Sincronización",
        "Performance": "Desempeño",
    }
    data = {row["field"]: row for row in rows(AUDIT / "field_coverage_19cols.csv")}
    labels = list(selected.values())
    values = np.array([float(data[field]["informative_percent"]) for field in selected])
    order = np.argsort(values)
    fig, ax = plt.subplots(figsize=(6.6, 3.65))
    ax.barh(np.arange(len(values)), values[order], color=COLORS["base"], alpha=0.9)
    ax.set_yticks(np.arange(len(values)), np.array(labels)[order])
    ax.set_xlabel("Artefactos con valor informativo (%)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=0.2)
    for y, value in enumerate(values[order]):
        ax.text(min(value + 1.2, 96), y, f"{value:.1f}%", va="center", fontsize=8)
    fig.tight_layout()
    save(fig, "cobertura_campos")


def delta_distributions() -> None:
    import pandas as pd

    data = pd.read_csv(RESULTS / "per_query.csv", sep=";")
    delta_sim = data["diverse_mean_similarity"] - data["baseline_mean_similarity"]
    delta_ild = data["diverse_intra_list_dissimilarity"] - data["baseline_intra_list_dissimilarity"]
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 2.75))
    axes[0].hist(delta_sim, bins=45, color=COLORS["base"], alpha=0.9)
    axes[0].axvline(0, color="#333333", lw=0.8)
    axes[0].set_xlabel("Cambio de similitud media top-5")
    axes[0].set_ylabel("Consultas")
    axes[1].hist(delta_ild, bins=45, color=COLORS["ild"], alpha=0.9)
    axes[1].axvline(0, color="#333333", lw=0.8)
    axes[1].set_xlabel("Cambio de disimilitud intra-lista")
    for ax in axes:
        ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, "distribucion_cambios")


def pool_sensitivity() -> None:
    import pandas as pd

    data = pd.read_csv(AUDIT / "extended_mmr_sensitivity.csv")
    data = data[(data["method"] == "MMR") & (data["top_k"] == 5) & (data["lambda"] == 0.7) & (data["keep_top1"] == True)]
    data = data[data["pool_size"].isin([10, 15, 20, 30])].sort_values("pool_size")
    fig, ax1 = plt.subplots(figsize=(5.3, 3.0))
    ax2 = ax1.twinx()
    ax1.plot(data["pool_size"], data["mean_similarity"], marker="o", color=COLORS["base"], label="Similitud")
    ax2.plot(data["pool_size"], data["ild_main_weights"], marker="s", color=COLORS["ild"], label="Disimilitud")
    ax1.set_xlabel("Tamaño del pool candidato")
    ax1.set_ylabel("Similitud media top-5", color=COLORS["base"])
    ax2.set_ylabel("Disimilitud intra-lista", color=COLORS["ild"])
    ax1.set_xticks(data["pool_size"])
    ax1.grid(alpha=0.2)
    fig.tight_layout()
    save(fig, "sensibilidad_pool")


def task_deltas() -> None:
    translations = {
        "Fault detection": "Detección de fallas",
        "Fault feature extraction": "Extracción de características",
        "Fault identification": "Identificación de fallas",
        "Health assessment": "Evaluación de salud",
        "Health modelling": "Modelado de salud",
        "Multiple steps future state forecast": "Pronóstico multihorizonte",
        "One step future state forecast": "Pronóstico a un paso",
        "Remaining useful life estimation": "Estimación de vida útil remanente",
    }
    data = [
        r
        for r in rows(STATS / "task_stratified_metric_summary.csv")
        if r["metric_id"] == "intra_list_dissimilarity"
    ]
    data.sort(key=lambda r: float(r["mean_change"]))
    labels = [f"{translations[r['task']]} (n={r['n']})" for r in data]
    mean = np.array([float(r["mean_change"]) for r in data])
    lo = np.array([float(r["ci95_mean_change_low"]) for r in data])
    hi = np.array([float(r["ci95_mean_change_high"]) for r in data])
    y = np.arange(len(data))

    fig, ax = plt.subplots(figsize=(6.9, 3.65))
    ax.barh(y, mean, color=COLORS["ild"], alpha=0.88)
    ax.errorbar(mean, y, xerr=[mean - lo, hi - mean], fmt="none", ecolor="#222222", capsize=2.5, lw=0.9)
    ax.axvline(0, color="#444444", lw=0.8)
    ax.set_yticks(y, labels)
    ax.set_xlabel("Cambio medio de disimilitud intra-lista (MMR − CBR)")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    save(fig, "delta_ild_por_tarea")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    global_metrics()
    lambda_tradeoff()
    field_coverage()
    delta_distributions()
    pool_sensitivity()
    task_deltas()
    print(f"Figuras generadas en {OUT}")
