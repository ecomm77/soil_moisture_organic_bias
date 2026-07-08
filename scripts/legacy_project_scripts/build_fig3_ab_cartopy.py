#!/usr/bin/env python3
"""Rebuild Main Fig 2 (paper_fig3_AB.png) with cartopy coastlines on panel A.
Panel B is copied from the existing panel_B function."""
from __future__ import annotations
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from phase1_impact_figures import sensor_family, FAMILY_COLOR, panel_B

BASE = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")


def panel_A_cartopy(df: pd.DataFrame, ax):
    proj = ccrs.PlateCarree()
    ax.set_extent([-180, 180, -60, 82], crs=proj)
    ax.add_feature(cfeature.LAND.with_scale("110m"),
                    facecolor="#f5f5f5", edgecolor="none", zorder=0)
    ax.add_feature(cfeature.OCEAN.with_scale("110m"),
                    facecolor="#eaf3f8", edgecolor="none", zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale("110m"),
                    edgecolor="#7f8c8d", linewidth=0.5)
    ax.add_feature(cfeature.BORDERS.with_scale("110m"),
                    edgecolor="#bdc3c7", linewidth=0.3, linestyle=":")
    for fam, color in FAMILY_COLOR.items():
        sub = df[df["family"] == fam]
        if len(sub) == 0: continue
        size = np.abs(sub["resid_era5"].fillna(0)) * 120 + 6
        ax.scatter(sub["lon"], sub["lat"], c=color, s=size, alpha=0.75,
                    edgecolor="black", linewidth=0.2, transform=proj,
                    label=f"{fam} (n={len(sub)})")
    ax.set_title("(a) Global ISMN station-sensors coloured by manufacturer family "
                  "(2020-2023)\n"
                  "marker size ∝ |ISMN − ERA5-Land| residual", fontsize=11)
    ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4,
                  color="#95a5a6", linestyle="--")
    ax.legend(fontsize=7, loc="lower left", ncol=2)


def main() -> int:
    df = pd.read_csv(BASE / "ismn_allrefs_merged.csv")
    df["family"] = df["sensor"].fillna("").map(sensor_family)

    fig = plt.figure(figsize=(20, 7))
    ax1 = fig.add_subplot(1, 2, 1, projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(1, 2, 2)
    plt.subplots_adjust(wspace=0.22)

    panel_A_cartopy(df, ax1)
    panel_B(df.copy(), ax=ax2, standalone=False)

    fig.savefig(BASE / "paper_fig3_AB.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {BASE / 'paper_fig3_AB.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
