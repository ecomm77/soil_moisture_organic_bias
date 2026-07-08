#!/usr/bin/env python3
"""Build three Extended Data figures from existing supplementary CSVs.

  ED Fig 1  -- Temporal invariance: family residual under 2020-2023 vs 2023-only
  ED Fig 2  -- Leave-one-network p-values for the pooled CRNS-vs-ISMN Welch test
  ED Fig 3  -- Mixed-model log_10(SOC) coefficient stability under
                leave-one-network jackknife (per reference)
"""
from __future__ import annotations
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PH1 = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")
PH2 = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase2")
OUT = PH1  # keep Extended Data alongside main figures


def ed1_temporal_invariance():
    df = pd.read_csv(PH1 / "supplement_s4_temporal_invariance.csv")
    families = df["family"].tolist()
    full = df["resid_2020_2023"].values
    only23 = df["resid_2023_only"].values
    x = np.arange(len(families))
    w = 0.4

    fig, ax = plt.subplots(figsize=(9, 5))
    bars1 = ax.bar(x - w/2, full,  width=w, color="#34495e",
                    label="2020–2023 mean",     edgecolor="black", linewidth=0.4)
    bars2 = ax.bar(x + w/2, only23, width=w, color="#f39c12",
                    label="2023 only",           edgecolor="black", linewidth=0.4)
    for xi, v in zip(x - w/2, full):
        ax.text(xi, v - 0.004 if v < 0 else v + 0.002, f"{v:+.3f}",
                 ha="center", va="top" if v < 0 else "bottom", fontsize=8)
    for xi, v in zip(x + w/2, only23):
        ax.text(xi, v - 0.004 if v < 0 else v + 0.002, f"{v:+.3f}",
                 ha="center", va="top" if v < 0 else "bottom", fontsize=8)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{f}\n(n={n})" for f, n in zip(families, df["n"])], fontsize=9)
    ax.set_ylabel("Mean ISMN − ERA5-Land swvl1 residual (m³/m³)")
    ax.set_title("Extended Data Fig 1 — Temporal invariance of family residuals:\n"
                 "2020–2023 vs 2023-only ERA5-Land under a uniform 0.1° swvl1 overlay")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "ed_fig1_temporal_invariance.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / 'ed_fig1_temporal_invariance.png'}")


def ed2_leave_one_network():
    df = pd.read_csv(PH2 / "phase2_robustness_LON.csv").sort_values("p")
    fig, ax = plt.subplots(figsize=(9, 5))
    y = np.arange(len(df))
    ax.barh(y, -np.log10(df["p"].values), color="#16a085",
             edgecolor="black", linewidth=0.4)
    for yi, (p, e, n_hp, n_nhp) in enumerate(zip(df["p"], df["effect"], df["n_hp"], df["n_nhp"])):
        ax.text(-np.log10(p) + 0.05, yi,
                  f"p={p:.1e}  |  Δ={e:+.3f}  |  n={n_hp}/{n_nhp}",
                  va="center", fontsize=8)
    ax.axvline(-np.log10(0.05),  color="#c0392b", lw=0.8, ls="--", label="p = 0.05")
    ax.axvline(-np.log10(0.001), color="#2c3e50", lw=0.8, ls=":",  label="p = 10⁻³")
    ax.set_yticks(y)
    ax.set_yticklabels([f"drop {n}" for n in df["dropped_network"]], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel(r"$-\log_{10}$(pooled Welch's p-value)")
    ax.set_title("Extended Data Fig 2 — Leave-one-network jackknife of the pooled\n"
                 "CRNS vs ISMN HP-minus-non-HP Welch test (92-pair dataset)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    ax.set_xlim(0, max(-np.log10(df["p"].values)) * 1.3)
    fig.tight_layout()
    fig.savefig(OUT / "ed_fig2_leave_one_network.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / 'ed_fig2_leave_one_network.png'}")


def ed3_mixed_model_stability():
    """Jackknife log10(SOC) slope under leave-one-network deletion."""
    lo = pd.read_csv(PH1 / "supplement_s1_leave_one_out.csv").sort_values("slope_log_soc")
    mm = pd.read_csv(PH1 / "supplement_s1_mixed_model.csv")
    # Main-model full-sample slope (ERA5-Land mixed-effects, not the pooled OLS)
    era5_slope = mm.loc[mm["reference"] == "ERA5-Land", "slope_log_soc"].values[0]
    era5_p = mm.loc[mm["reference"] == "ERA5-Land", "slope_log_soc_p"].values[0]
    smap_slope = mm.loc[mm["reference"] == "SMAP L3_E", "slope_log_soc"].values[0]
    smap_p = mm.loc[mm["reference"] == "SMAP L3_E", "slope_log_soc_p"].values[0]
    smi_slope = mm.loc[mm["reference"].str.contains("SMAP-SMI"), "slope_log_soc"].values[0]
    smi_p = mm.loc[mm["reference"].str.contains("SMAP-SMI"), "slope_log_soc_p"].values[0]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # LEFT: jackknife slopes
    ax = axes[0]
    y = np.arange(len(lo))
    ax.barh(y, lo["slope_log_soc"].values, color="#7f8c8d",
             edgecolor="black", linewidth=0.4)
    ax.axvline(lo["slope_log_soc"].mean(), color="#34495e", lw=0.8, ls="--",
                label=f"mean = {lo['slope_log_soc'].mean():+.3f}")
    ax.axvline(0, color="k", lw=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels([f"drop {n}" for n in lo["dropped_network"]], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Pooled OLS slope on log₁₀(SOC) [m³/m³ per decade of SOC]")
    ax.set_title("Leave-one-network jackknife: slope is invariant-sign")
    ax.legend(fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    # RIGHT: mixed-model coefficient across references (texture-controlled)
    ax2 = axes[1]
    refs = ["ERA5-Land", "SMAP L3_E", "SMAP-SMI"]
    slopes = [era5_slope, smap_slope, smi_slope]
    pvals = [era5_p, smap_p, smi_p]
    ses = mm.set_index("reference")["slope_log_soc_se"]
    se_list = [ses.loc["ERA5-Land"], ses.loc["SMAP L3_E"],
                ses.loc[next(r for r in ses.index if "SMAP-SMI" in r)]]
    x = np.arange(len(refs))
    ax2.errorbar(slopes, x, xerr=1.96 * np.array(se_list),
                  fmt="D", color="#2980b9", markersize=11, capsize=5,
                  elinewidth=2.0, markeredgecolor="black")
    for xi, s, p in zip(x, slopes, pvals):
        sig = "***" if p < 1e-3 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        ax2.text(s, xi + 0.18, f"{s:+.3f}  p={p:.2f}  [{sig}]", ha="center", fontsize=9)
    ax2.axvline(0, color="k", lw=0.7)
    ax2.set_yticks(x); ax2.set_yticklabels(refs, fontsize=11)
    ax2.invert_yaxis()
    ax2.set_xlim(-0.10, 0.10)
    ax2.set_xlabel("Mixed-effects log₁₀(SOC) coefficient (95% CI)")
    ax2.set_title("Mixed-model log₁₀(SOC) coefficient collapses after\n"
                   "clay + BD + depth + |lat| controls (per reference)")
    ax2.grid(axis="x", alpha=0.3)

    fig.suptitle("Extended Data Fig 3 — Mixed-model SOC coefficient stability\n"
                  "(left) leave-one-network jackknife  (right) per-reference texture-controlled slope",
                  fontsize=11, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "ed_fig3_mixed_model_stability.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / 'ed_fig3_mixed_model_stability.png'}")


def main() -> int:
    ed1_temporal_invariance()
    ed2_leave_one_network()
    ed3_mixed_model_stability()
    return 0


if __name__ == "__main__":
    sys.exit(main())
