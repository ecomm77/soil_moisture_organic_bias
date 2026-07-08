#!/usr/bin/env python3
"""Vertical (portrait) version of the talk figure for poster / tall slide."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")


def main() -> int:
    fig = plt.figure(figsize=(9, 16))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.05, 0.95, 0.85],
                            left=0.07, right=0.97, top=0.91, bottom=0.05,
                            hspace=0.40)

    fig.suptitle("The global benchmark for satellite soil moisture\n"
                  "is dominated by one sensor family\n"
                  "— and it reads systematically drier",
                  fontsize=18, fontweight="bold", y=0.97, color="#222")

    # ---------- (a) pie composition ----------
    ax1 = fig.add_subplot(gs[0])
    ax1.set_xticks([]); ax1.set_yticks([])
    for s in ax1.spines.values(): s.set_visible(False)
    sizes = [1274, 130, 95, 65, 59, 2]
    colors = ["#c0392b", "#7f8c8d", "#27ae60", "#2980b9", "#f39c12", "#8e44ad"]
    labels = ["HydraProbe\n78%", "other\n8%", "Decagon/METER\n6%",
               "Campbell\n4%", "ThetaProbe\n4%", ""]
    wedges, texts = ax1.pie(sizes, colors=colors,
                              startangle=90, counterclock=False,
                              labels=labels, labeldistance=1.20,
                              radius=1.0, center=(0, 0),
                              wedgeprops=dict(edgecolor="white", linewidth=2.5),
                              textprops=dict(fontsize=12))
    ax1.text(0, 0.05, "1,625", ha="center", va="center",
              fontsize=28, fontweight="bold", color="white")
    ax1.text(0, -0.18, "ISMN station-sensors\n(2020–2023)", ha="center", va="center",
              fontsize=11, color="white", fontweight="bold")
    ax1.set_title("(a) The global validation archive is manufacturer-asymmetric",
                   fontsize=14, fontweight="bold", pad=14)
    ax1.set_xlim(-1.55, 1.55); ax1.set_ylim(-1.4, 1.4)
    ax1.set_aspect("equal")

    # ---------- (b) family residual bars ----------
    ax2 = fig.add_subplot(gs[1])
    fams = ["HydraProbe", "other", "Campbell CS6xx", "ThetaProbe", "Decagon/METER TDR"]
    rs = [-0.097, -0.056, -0.065, -0.039, +0.068]
    cs = ["#c0392b", "#7f8c8d", "#2980b9", "#f39c12", "#27ae60"]
    order = np.argsort(rs)
    fams = [fams[i] for i in order]; rs = [rs[i] for i in order]; cs = [cs[i] for i in order]
    y = np.arange(len(fams))
    ax2.barh(y, rs, color=cs, edgecolor="black", linewidth=0.6, height=0.65)
    for yi, v in zip(y, rs):
        ax2.text(v + (0.005 if v > 0 else -0.005), yi,
                  f"{v:+.3f}", ha="left" if v > 0 else "right",
                  va="center", fontsize=13, fontweight="bold")
    ax2.set_yticks(y); ax2.set_yticklabels(fams, fontsize=12)
    ax2.invert_yaxis()
    ax2.axvline(0, color="k", lw=1.0)
    ax2.set_xlim(-0.16, 0.13)
    ax2.set_xlabel("ISMN − ERA5-Land residual (m³/m³)", fontsize=12)
    ax2.tick_params(axis="x", labelsize=11)
    ax2.set_title("(b) Sensor-family residual against ERA5-Land\n"
                   "0.17 m³/m³ swing — larger than typical satellite product targets",
                   fontsize=14, fontweight="bold", pad=10)
    # swing arrow below bars
    ax2.annotate("", xy=(0.075, 4.9), xytext=(-0.105, 4.9),
                  arrowprops=dict(arrowstyle="<->", color="#c0392b", lw=2.5),
                  annotation_clip=False)
    ax2.text(-0.015, 5.25, "0.17 m³/m³ family swing",
              ha="center", va="bottom", fontsize=12, fontweight="bold",
              color="#c0392b", clip_on=False)
    for s in ("top", "right"): ax2.spines[s].set_visible(False)

    # ---------- (c) downstream consequences ----------
    axB = fig.add_subplot(gs[2])
    axB.set_xticks([]); axB.set_yticks([])
    for s in axB.spines.values():
        s.set_edgecolor("#34495e"); s.set_linewidth(1.5)
    axB.set_facecolor("#f8f9fa")
    axB.set_title("(c) Downstream consequences", fontsize=14, fontweight="bold", pad=10)

    items = [
        ("Validation RMSD shifts up to +41 %",
         "(non-HP sub-sample)", "#c0392b"),
        ("SMAP L3$_{\\rm E}$ bias correction FLIPS sign",
         "(by sensor family)", "#2980b9"),
        ("Product ranking FLIPS:\nSMAP-SMI ↔ SMAP L3$_{\\rm E}$",
         "(under non-HP reweighting)", "#27ae60"),
        ("4 dielectric-free CRNS archives on 3 continents",
         "(USA, EU, UK, AU — direction confirmed)", "#d4ac0d"),
    ]
    n = len(items)
    box_h = 0.16; gap = (1.0 - n*box_h) / (n + 1)
    for i, (head, sub, col) in enumerate(items):
        y0 = 1.0 - gap - (i + 1) * (box_h + gap) + (i + 1) * gap - box_h * (1)
        # row position from top
        y0 = 1.0 - gap - (i + 1) * box_h - i * gap
        axB.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (0.04, y0), 0.92, box_h, transform=axB.transAxes,
            boxstyle="round,pad=0.005",
            facecolor="white", edgecolor=col, linewidth=2.0))
        axB.text(0.50, y0 + box_h * 0.62, head, ha="center", va="center",
                  transform=axB.transAxes, fontsize=13, fontweight="bold", color=col)
        axB.text(0.50, y0 + box_h * 0.22, sub, ha="center", va="center",
                  transform=axB.transAxes, fontsize=11, style="italic", color="#34495e")

    fig.text(0.5, 0.018,
              "Park et al. — Sensor-family composition shapes global soil-moisture product validation",
              ha="center", va="bottom", fontsize=10, style="italic", color="#555")

    fig.savefig(OUT / "talk_figure_vertical.png", dpi=160, bbox_inches="tight",
                 facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT / 'talk_figure_vertical.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
