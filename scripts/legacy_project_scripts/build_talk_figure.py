#!/usr/bin/env python3
"""Compact talk figure — reduced height, no internal whitespace,
plain-language downstream consequences for non-specialist audience."""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")


def main() -> int:
    fig = plt.figure(figsize=(16, 5.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.6, 0.7], width_ratios=[1, 1.45],
                            left=0.04, right=0.98, top=0.96, bottom=0.05,
                            hspace=0.20, wspace=0.10)

    # ---------- (a) pie composition ----------
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xticks([]); ax1.set_yticks([])
    for s in ax1.spines.values(): s.set_visible(False)
    sizes = [1274, 130, 95, 65, 59, 2]
    colors = ["#c0392b", "#7f8c8d", "#27ae60", "#2980b9", "#f39c12", "#8e44ad"]
    labels = ["HydraProbe\n78%", "other\n8%", "Decagon/METER\n6%",
               "Campbell\n4%", "ThetaProbe\n4%", ""]
    ax1.pie(sizes, colors=colors, startangle=90, counterclock=False,
             labels=labels, labeldistance=1.18,
             radius=0.95, center=(0, 0),
             wedgeprops=dict(edgecolor="white", linewidth=2.2),
             textprops=dict(fontsize=10))
    ax1.text(0, 0.04, "1,625", ha="center", va="center",
              fontsize=22, fontweight="bold", color="white")
    ax1.text(0, -0.16, "ISMN station-sensors", ha="center", va="center",
              fontsize=9, color="white", fontweight="bold")
    ax1.set_title("(a) The global validation archive\nis manufacturer-asymmetric",
                   fontsize=13, fontweight="bold", pad=4)
    ax1.set_xlim(-1.45, 1.45); ax1.set_ylim(-1.35, 1.35)
    ax1.set_aspect("equal")

    # ---------- (b) family residual bars ----------
    ax2 = fig.add_subplot(gs[0, 1])
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
                  va="center", fontsize=11, fontweight="bold")
    ax2.set_yticks(y); ax2.set_yticklabels(fams, fontsize=11)
    ax2.invert_yaxis()
    ax2.axvline(0, color="k", lw=1.0)
    ax2.set_xlim(-0.16, 0.12)
    ax2.set_xlabel("ISMN − ERA5-Land residual (m³/m³)", fontsize=11)
    ax2.tick_params(axis="x", labelsize=10)
    ax2.set_title("(b) Family-stratified residual against ERA5-Land\n"
                   "0.17 m³/m³ swing — larger than typical satellite product targets",
                   fontsize=13, fontweight="bold", pad=4)
    ax2.annotate("", xy=(0.075, 4.75), xytext=(-0.105, 4.75),
                  arrowprops=dict(arrowstyle="<->", color="#c0392b", lw=2.5),
                  annotation_clip=False)
    ax2.text(-0.015, 5.05, "0.17 m³/m³ family swing",
              ha="center", va="bottom", fontsize=11, fontweight="bold",
              color="#c0392b", clip_on=False)
    for s in ("top", "right"): ax2.spines[s].set_visible(False)

    # ---------- (c) plain-language downstream consequences ----------
    axB = fig.add_subplot(gs[1, :])
    axB.set_xticks([]); axB.set_yticks([])
    for s in axB.spines.values():
        s.set_edgecolor("#34495e"); s.set_linewidth(1.4)
    axB.set_facecolor("#f8f9fa")
    axB.text(0.5, 0.96,
              "(c) Why this matters in plain terms",
              ha="center", va="top", transform=axB.transAxes,
              fontsize=12, fontweight="bold", color="#222")

    items = [
        ("Satellite 'accuracy scores'\nshift by up to 40%", "#c0392b"),
        ("NASA SMAP bias correction\nreverses direction", "#2980b9"),
        ("Best-ranked satellite product\nflips by sensor choice", "#27ae60"),
        ("Independent cosmic-ray sensors\non 3 continents confirm it", "#d4ac0d"),
    ]
    n = len(items)
    box_w = 0.225; gap = (1.0 - n*box_w) / (n + 1)
    for i, (head, col) in enumerate(items):
        x0 = gap + i * (box_w + gap)
        axB.add_patch(plt.matplotlib.patches.FancyBboxPatch(
            (x0, 0.06), box_w, 0.68, transform=axB.transAxes,
            boxstyle="round,pad=0.005",
            facecolor="white", edgecolor=col, linewidth=1.8))
        axB.text(x0 + box_w/2, 0.40, head, ha="center", va="center",
                  transform=axB.transAxes, fontsize=12, fontweight="bold", color=col)

    fig.savefig(OUT / "talk_figure.png", dpi=170, bbox_inches="tight",
                 facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT / 'talk_figure.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
