#!/usr/bin/env python3
"""Conceptual Figure 1 v2 — clean subplot-based layout."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np

OUT = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")


def main() -> int:
    fig = plt.figure(figsize=(15, 8.5))
    gs = fig.add_gridspec(2, 3, height_ratios=[3, 0.9], width_ratios=[1, 1, 1],
                            hspace=0.32, wspace=0.30,
                            left=0.04, right=0.97, top=0.91, bottom=0.06)

    fig.suptitle("A hidden sensor-family imbalance in the global soil-moisture benchmark",
                  fontsize=15, fontweight="bold", y=0.97)

    # --- Panel 1: ISMN archive composition ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor("#fdf2f1")
    for spine in ax1.spines.values():
        spine.set_edgecolor("#c0392b"); spine.set_linewidth(1.6)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.text(0.5, 0.96, "1.  ISMN archive: the global\nsoil-moisture 'truth' (n = 1,625)",
              ha="center", va="top", transform=ax1.transAxes,
              fontsize=12, fontweight="bold")
    sizes = [1274, 130, 95, 65, 59]
    colors = ["#c0392b", "#7f8c8d", "#27ae60", "#2980b9", "#f39c12"]
    labels = ["HydraProbe (78%)", "other (8%)", "Decagon/METER (6%)",
               "Campbell (4%)", "ThetaProbe (4%)"]
    wedges, _ = ax1.pie(sizes, colors=colors, startangle=90,
                          radius=0.62, center=(0.5, 0.46),
                          wedgeprops=dict(edgecolor="white", linewidth=1.4),
                          frame=False)
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1)
    ax1.text(0.5, 0.46, "1,625", ha="center", va="center",
              fontsize=11, fontweight="bold", color="white")
    # Legend below pie
    lgd_y = -0.02
    for i, (lab, c) in enumerate(zip(labels, colors)):
        row = i // 2; col = i % 2
        ax1.text(0.06 + col * 0.50, lgd_y - row * 0.05, "■",
                  color=c, fontsize=12, va="center")
        ax1.text(0.10 + col * 0.50, lgd_y - row * 0.05, lab,
                  fontsize=8, va="center")

    # --- Panel 2: family residual bars ---
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor("#eaf4fc")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#2980b9"); spine.set_linewidth(1.6)
    ax2.set_title("2.  ISMN − ERA5 residual\nby sensor family",
                   fontsize=12, fontweight="bold", pad=2)
    fams = ["HydraProbe", "Decagon/METER", "Campbell", "ThetaProbe", "other"]
    rs = [-0.097, +0.068, -0.065, -0.039, -0.056]
    cs = ["#c0392b", "#27ae60", "#2980b9", "#f39c12", "#7f8c8d"]
    y = np.arange(len(fams))
    bars = ax2.barh(y, rs, color=cs, edgecolor="black", linewidth=0.4, height=0.6)
    for yi, v in zip(y, rs):
        ax2.text(v + (0.006 if v > 0 else -0.006), yi,
                  f"{v:+.3f}", ha="left" if v > 0 else "right",
                  va="center", fontsize=9, fontweight="bold")
    ax2.set_yticks(y); ax2.set_yticklabels(fams, fontsize=9)
    ax2.invert_yaxis()
    ax2.axvline(0, color="k", lw=0.7)
    ax2.set_xlim(-0.15, 0.12)
    ax2.set_xlabel("ISMN − ERA5 (m³/m³)", fontsize=9)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.text(0.5, -0.18, "0.17 m³/m³ swing across families",
              ha="center", va="top", transform=ax2.transAxes,
              fontsize=9, style="italic", color="#2980b9")

    # --- Panel 3: downstream consequences ---
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_facecolor("#fcf8e3")
    for spine in ax3.spines.values():
        spine.set_edgecolor("#d4ac0d"); spine.set_linewidth(1.6)
    ax3.set_xticks([]); ax3.set_yticks([])
    ax3.text(0.5, 0.96, "3.  Downstream consequences",
              ha="center", va="top", transform=ax3.transAxes,
              fontsize=12, fontweight="bold")
    bullets = [
        "•  Validation RMSD shifts up to 41%\n   under non-HP sub-sample",
        "•  SMAP L3$_{\\rm E}$ bias correction\n   flips sign by sensor family",
        "•  Product ranking flips:\n   SMAP-SMI ↔ SMAP L3$_{\\rm E}$\n   under non-HP reweighting",
        "•  Reference-discordant dry\n   classification: 4.3× higher\n   absolute load from HP family",
    ]
    yb = 0.84
    for b in bullets:
        ax3.text(0.05, yb, b, ha="left", va="top",
                  transform=ax3.transAxes, fontsize=9.5)
        yb -= 0.21

    # --- Bottom row: CRNS attribution ---
    axB = fig.add_subplot(gs[1, :])
    axB.set_facecolor("#ecf9ec")
    for spine in axB.spines.values():
        spine.set_edgecolor("#27ae60"); spine.set_linewidth(1.6)
    axB.set_xticks([]); axB.set_yticks([])
    axB.text(0.5, 0.78,
              "4.  Dielectric-free CRNS attribution across four archives, three continents",
              ha="center", va="center", transform=axB.transAxes,
              fontsize=12, fontweight="bold")
    axB.text(0.5, 0.30,
              "USA (COSMOS-USA, n=56 pairs, t=+3.6, p=10$^{-3}$)    "
              "Europe (COSMOS-Europe, n=31, t=+2.6, p=0.02)    "
              "UK (on-site CRNS−TDT, n=49)    "
              "Australia (CosmOz, directional only)",
              ha="center", va="center", transform=axB.transAxes,
              fontsize=10)

    # Arrows between panels (using fig.add_artist with figure coords)
    for x_start in [0.355, 0.685]:
        fig.add_artist(plt.matplotlib.patches.FancyArrow(
            x_start, 0.55, 0.025, 0,
            width=0.005, head_width=0.018, head_length=0.012,
            length_includes_head=True, color="black", linewidth=0,
            transform=fig.transFigure))

    fig.savefig(OUT / "paper_fig1_conceptual.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT / 'paper_fig1_conceptual.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
