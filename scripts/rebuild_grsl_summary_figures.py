#!/usr/bin/env python3
"""Rebuild portable GRSL summary figures from included source-data CSVs.

This script does not require the full raw-data archive. It rebuilds compact
review plots from the curated source tables shipped with this package.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source_data"
OUT = ROOT / "outputs"
FIG_MAIN = ROOT / "figures" / "main"
FIG_SUPP = ROOT / "figures" / "supplement"

# Okabe-Ito / colorblind-safe palette, with TRIME greyed because n=2.
FAMILY_COLORS = {
    "HydraProbe_family": "#D55E00",
    "Decagon_METER_TDR": "#009E73",
    "Campbell_CS6xx": "#0072B2",
    "ThetaProbe": "#E69F00",
    "TRIME": "#999999",
    "other": "#666666",
}
PRODUCT_COLORS = {
    "ERA5-Land": "#0072B2",
    "SMAP L3_E": "#E69F00",
    "SMAP-SMI": "#009E73",
}
SUBSET_COLORS = {
    "full": "#7F8C8D",
    "HydraProbe": "#D55E00",
    "non-HydraProbe": "#009E73",
}


def family_label(value: str) -> str:
    return (
        value.replace("_family", "")
        .replace("_METER_TDR", "/METER TDR")
        .replace("_CS6xx", " CS6xx")
        .replace("_", " ")
    )


def family_residual_plot() -> Path:
    df = pd.read_csv(SRC / "family_reference_residuals.csv")
    df = df[df["family"] != "TRIME"].copy()
    df = df.sort_values("era5_mean")

    x = np.arange(len(df))
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    ax.bar(
        x,
        df["era5_mean"],
        color=[FAMILY_COLORS.get(f, "#666666") for f in df["family"]],
        edgecolor="black",
        linewidth=0.5,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([family_label(v) for v in df["family"]], rotation=30, ha="right")
    ax.set_ylabel("Mean ISMN minus ERA5-Land residual (m3/m3)")
    ax.set_title("Family-stratified ISMN minus ERA5-Land residual")
    for xi, value, n in zip(x, df["era5_mean"], df["era5_n"]):
        ax.text(
            xi,
            value + (0.004 if value >= 0 else -0.004),
            f"{value:+.3f}\nn={int(n)}",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=8,
        )
    fig.tight_layout()
    out = OUT / "rebuilt_family_era5_residuals.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def main_asymmetry_figure() -> Path:
    comp = pd.read_csv(SRC / "family_composition.csv")
    comp = comp[comp["family"] != "total"].copy()
    comp = comp.sort_values("n_station_sensors", ascending=True)

    resid = pd.read_csv(SRC / "family_reference_residuals.csv").copy()
    resid = resid[resid["family"] != "TRIME"].copy()
    resid = resid.sort_values("era5_mean", ascending=True)

    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.7), gridspec_kw={"width_ratios": [0.95, 1.35]})
    ax = axes[0]
    y = np.arange(len(comp))
    ax.barh(
        y,
        comp["share_percent"],
        color=[FAMILY_COLORS.get(f, "#666666") for f in comp["family"]],
        edgecolor="black",
        linewidth=0.5,
    )
    ax.set_yticks(y)
    ax.set_yticklabels([family_label(v) for v in comp["family"]])
    ax.set_xlabel("Share of retained ISMN station-sensors (%)")
    ax.set_title("(a) Archive composition")
    for yi, share, n in zip(y, comp["share_percent"], comp["n_station_sensors"]):
        ax.text(share + 1.0, yi, f"{share:.1f}% (n={int(n)})", va="center", fontsize=8)
    ax.set_xlim(0, 88)
    ax.grid(axis="x", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    x = np.arange(len(resid))
    colors = [FAMILY_COLORS.get(f, "#666666") for f in resid["family"]]
    ax.bar(
        x,
        resid["era5_mean"],
        color=colors,
        edgecolor="black",
        linewidth=0.5,
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([family_label(v) for v in resid["family"]], rotation=24, ha="right")
    ax.set_ylabel("Mean ISMN minus ERA5-Land residual (m3/m3)")
    ax.set_title("(b) Mean-state residual by family")
    ax.grid(axis="y", alpha=0.25)
    for xi, value, n in zip(x, resid["era5_mean"], resid["era5_n"]):
        ax.text(
            xi,
            value + (0.006 if value >= 0 else -0.006),
            f"{value:+.3f}\nn={int(n)}",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=7.4,
        )
    fam_order = list(resid["family"])
    hydra_ix = fam_order.index("HydraProbe_family")
    decagon_ix = fam_order.index("Decagon_METER_TDR")
    ax.annotate("", xy=(decagon_ix, 0.092), xytext=(hydra_ix, 0.092), arrowprops={"arrowstyle": "<->", "lw": 0.9})
    ax.text((hydra_ix + decagon_ix) / 2, 0.096, "0.17 m3/m3 family swing", fontsize=8.2, ha="center")
    ax.set_ylim(-0.13, 0.105)
    fig.tight_layout()
    out = FIG_MAIN / "paper_fig3_AB.png"
    fig.savefig(out, dpi=240, bbox_inches="tight")
    fig.savefig(OUT / "rebuilt_paper_fig3_AB.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    return out


def validation_metric_plot() -> Path:
    df = pd.read_csv(SRC / "validation_metrics_by_subset.csv")
    refs = df["reference"].tolist()
    x = np.arange(len(refs))
    width = 0.26

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    ax = axes[0]
    ax.bar(x - width, df["full_RMSD"], width, label="full", color=SUBSET_COLORS["full"])
    ax.bar(x, df["hydraprobe_RMSD"], width, label="HydraProbe", color=SUBSET_COLORS["HydraProbe"])
    ax.bar(
        x + width,
        df["non_hydraprobe_RMSD"],
        width,
        label="non-HydraProbe",
        color=SUBSET_COLORS["non-HydraProbe"],
    )
    ax.set_xticks(x)
    ax.set_xticklabels(refs, rotation=20, ha="right")
    ax.set_ylabel("Mean-state RMSD (m3/m3)")
    ax.set_title("RMSD by ISMN sensor-family subset")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.bar(x - width, df["full_bias"], width, label="full", color=SUBSET_COLORS["full"])
    ax.bar(x, df["hydraprobe_bias"], width, label="HydraProbe", color=SUBSET_COLORS["HydraProbe"])
    ax.bar(
        x + width,
        df["non_hydraprobe_bias"],
        width,
        label="non-HydraProbe",
        color=SUBSET_COLORS["non-HydraProbe"],
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(refs, rotation=20, ha="right")
    ax.set_ylabel("Mean ISMN minus product bias (m3/m3)")
    ax.set_title("Bias by ISMN sensor-family subset")

    fig.tight_layout()
    out = OUT / "rebuilt_validation_metrics_by_subset.png"
    fig.savefig(out, dpi=220)
    plt.close(fig)
    return out


def downstream_figure() -> Path:
    fam = pd.read_csv(SRC / "family_reference_residuals.csv")
    fam = fam[fam["family"] != "TRIME"].copy()
    metrics = pd.read_csv(SRC / "validation_metrics_by_subset.csv")
    pair = pd.read_csv(SRC / "colocated_pair_summary.csv").iloc[0]
    crns = pd.read_csv(SRC / "crns_cross_check_summary.csv").iloc[0]

    fig = plt.figure(figsize=(13.2, 7.2))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1.05], hspace=0.52, wspace=0.42)

    ax = fig.add_subplot(gs[0, 0])
    labels = [family_label(v) for v in fam["family"]]
    x = np.arange(len(fam))
    width = 0.24
    for i, (col, ref) in enumerate(
        [("era5_mean", "ERA5-Land"), ("smap_l3e_mean", "SMAP L3_E"), ("smap_smi_mean", "SMAP-SMI")]
    ):
        ax.bar(
            x + (i - 1) * width,
            fam[col],
            width,
            label=ref,
            color=PRODUCT_COLORS[ref],
            edgecolor="black",
            linewidth=0.35,
        )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=24, ha="right")
    ax.set_ylabel("ISMN minus reference residual (m3/m3)")
    ax.set_title("(a) Family residuals across products")
    ax.legend(frameon=False, fontsize=8, ncol=3)
    ax.grid(axis="y", alpha=0.25)

    ax = fig.add_subplot(gs[0, 1])
    refs = metrics["reference"].tolist()
    x = np.arange(len(refs))
    width = 0.24
    ax.bar(x - width, metrics["full_RMSD"], width, label="full", color=SUBSET_COLORS["full"])
    ax.bar(x, metrics["hydraprobe_RMSD"], width, label="HydraProbe", color=SUBSET_COLORS["HydraProbe"])
    ax.bar(
        x + width,
        metrics["non_hydraprobe_RMSD"],
        width,
        label="non-HydraProbe",
        color=SUBSET_COLORS["non-HydraProbe"],
    )
    ax.set_xticks(x)
    ax.set_xticklabels(refs, rotation=18, ha="right")
    ax.set_ylabel("Mean-state RMSD (m3/m3)")
    ax.set_title("(b) RMSD by retained subset")
    ax.legend(frameon=False, fontsize=7.5)
    ax.grid(axis="y", alpha=0.25)

    ax = fig.add_subplot(gs[1, 0])
    ax.bar(x - width, metrics["full_bias"], width, label="full", color=SUBSET_COLORS["full"])
    ax.bar(x, metrics["hydraprobe_bias"], width, label="HydraProbe", color=SUBSET_COLORS["HydraProbe"])
    ax.bar(
        x + width,
        metrics["non_hydraprobe_bias"],
        width,
        label="non-HydraProbe",
        color=SUBSET_COLORS["non-HydraProbe"],
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(refs)
    ax.set_ylabel("ISMN minus product bias (m3/m3)")
    ax.set_title("(c) Bias correction implied by subset")
    ax.grid(axis="y", alpha=0.25)

    ax = fig.add_subplot(gs[1, 1])
    pair_effect = pair["effect_nonhydraprobe_minus_hydraprobe_m3m3"]
    crns_effect = crns.get(
        "contrast_hydraprobe_minus_nonhydraprobe_m3m3",
        crns["hydraprobe_residual_mean_m3m3"] - crns["nonhydraprobe_residual_mean_m3m3"],
    )
    effects = [pair_effect, crns_effect]
    y = np.arange(2)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.errorbar(
        effects[0],
        y[0],
        xerr=[
            [effects[0] - pair["ci_low_m3m3"]],
            [pair["ci_high_m3m3"] - effects[0]],
        ],
        fmt="o",
        color="#000000",
        ecolor="#000000",
        capsize=3,
    )
    if {"ci_network_low_m3m3", "ci_network_high_m3m3"}.issubset(crns.index):
        ax.errorbar(
            effects[1],
            y[1],
            xerr=[
                [effects[1] - crns["ci_network_low_m3m3"]],
                [crns["ci_network_high_m3m3"] - effects[1]],
            ],
            fmt="s",
            color="#000000",
            ecolor="#000000",
            capsize=3,
        )
    else:
        ax.scatter(effects[1], y[1], marker="s", s=55, color="#000000")
    ax.set_yticks(y)
    ax.set_yticklabels(["Co-located\npair (n=21)", "CRNS\n(n=92)"])
    ax.set_xlabel("Reported family contrast (m3/m3)")
    ax.set_title("(d) Independent family-contrast checks")
    ax.text(effects[0] + 0.006, y[0] + 0.10, "95% CI", fontsize=7.4)
    ax.text(effects[1] - 0.010, y[1] - 0.18, "network CI", fontsize=7.4, ha="center")
    ax.set_xlim(-0.02, 0.27)
    ax.set_ylim(-0.25, 1.25)
    ax.grid(axis="x", alpha=0.25)

    out = FIG_MAIN / "downstream_figure.png"
    fig.savefig(out, dpi=240, bbox_inches="tight")
    fig.savefig(OUT / "rebuilt_downstream_figure.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    return out


def write_summary_tables() -> list[Path]:
    paths: list[Path] = []
    metrics = pd.read_csv(SRC / "validation_metrics_by_subset.csv")
    metrics["smap_smi_rmsd_inflation_nonhp_vs_hp_percent"] = np.nan
    row = metrics["reference"].eq("SMAP-SMI")
    metrics.loc[row, "smap_smi_rmsd_inflation_nonhp_vs_hp_percent"] = (
        (metrics.loc[row, "non_hydraprobe_RMSD"] / metrics.loc[row, "hydraprobe_RMSD"] - 1.0)
        * 100.0
    )
    out = OUT / "rebuilt_key_metric_check.csv"
    metrics.to_csv(out, index=False)
    paths.append(out)

    reweight = metrics[["reference", "full_bias", "hydraprobe_bias", "non_hydraprobe_bias"]].copy()
    reweight["equal_HP_nonHP_bias"] = 0.5 * (
        reweight["hydraprobe_bias"] + reweight["non_hydraprobe_bias"]
    )
    reweight["delta_equal_HP_nonHP_minus_full"] = reweight["equal_HP_nonHP_bias"] - reweight["full_bias"]
    out = OUT / "rebuilt_reweighting_sensitivity.csv"
    reweight.to_csv(out, index=False)
    paths.append(out)
    return paths


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    FIG_MAIN.mkdir(parents=True, exist_ok=True)
    FIG_SUPP.mkdir(parents=True, exist_ok=True)
    written = [
        main_asymmetry_figure(),
        downstream_figure(),
        family_residual_plot(),
        validation_metric_plot(),
        *write_summary_tables(),
    ]
    for path in written:
        print(f"wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
