#!/usr/bin/env python3
"""ED Fig 4 with cartopy coastlines."""
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
from phase1_impact_figures import sensor_family

BASE = Path("/Volumes/Recovery/Dropbox/Data/soil_moisture_organic_bias/data/phase1")


def main() -> int:
    df = pd.read_csv(BASE / "ismn_allrefs_merged.csv")
    df["family"] = df["sensor"].fillna("").map(sensor_family)
    df["is_hp"] = df["family"] == "HydraProbe"

    # Match downstream_impact.py: each variable dry-threshold uses its own
    # (mean - 0.5 * std), not the ISMN archive threshold.
    ismn_thresh = df["sm_mean"].mean() - 0.5 * df["sm_mean"].std()
    df["ismn_dry"] = df["sm_mean"] < ismn_thresh
    ref_dry = np.zeros(len(df), dtype=bool)
    for ref in ["ref_era5", "ref_smap", "ref_somo"]:
        if ref not in df.columns: df[ref] = np.nan
        t = df[ref].mean() - 0.5 * df[ref].std()
        ref_dry = ref_dry | (df[ref] < t).fillna(False)
    df["any_ref_dry"] = ref_dry
    df["ref_discordant_dry"] = df["ismn_dry"] & ~df["any_ref_dry"]

    flags = df[df["ismn_dry"]].copy()

    proj = ccrs.PlateCarree()
    fig = plt.figure(figsize=(13, 10))

    # Panel (a)
    ax = fig.add_subplot(2, 1, 1, projection=proj)
    ax.set_extent([-180, 180, -60, 82], crs=proj)
    ax.add_feature(cfeature.LAND.with_scale("110m"), facecolor="#f5f5f5",
                    edgecolor="none", zorder=0)
    ax.add_feature(cfeature.OCEAN.with_scale("110m"), facecolor="#eaf3f8",
                    edgecolor="none", zorder=0)
    ax.add_feature(cfeature.COASTLINE.with_scale("110m"),
                    edgecolor="#7f8c8d", linewidth=0.5)
    ax.add_feature(cfeature.BORDERS.with_scale("110m"),
                    edgecolor="#bdc3c7", linewidth=0.3, linestyle=":")

    hp_a = flags[flags["is_hp"] & flags["any_ref_dry"]]
    hp_d = flags[flags["is_hp"] & ~flags["any_ref_dry"]]
    nh_a = flags[~flags["is_hp"] & flags["any_ref_dry"]]
    nh_d = flags[~flags["is_hp"] & ~flags["any_ref_dry"]]
    ax.scatter(hp_a["lon"], hp_a["lat"], s=10, c="#c0392b", marker="o",
                alpha=0.5, edgecolor="none", transform=proj,
                label=f"HP, ref agrees (n={len(hp_a)})")
    ax.scatter(hp_d["lon"], hp_d["lat"], s=28, c="#c0392b", marker="x",
                linewidth=1.4, transform=proj,
                label=f"HP, ref disagrees (n={len(hp_d)})")
    ax.scatter(nh_a["lon"], nh_a["lat"], s=10, c="#27ae60", marker="o",
                alpha=0.5, edgecolor="none", transform=proj,
                label=f"non-HP, ref agrees (n={len(nh_a)})")
    ax.scatter(nh_d["lon"], nh_d["lat"], s=28, c="#27ae60", marker="x",
                linewidth=1.4, transform=proj,
                label=f"non-HP, ref disagrees (n={len(nh_d)})")
    ax.set_title("(a) Spatial pattern of ISMN dry flags and reference agreement",
                  fontsize=11)
    ax.legend(loc="lower left", fontsize=8)
    ax.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4,
                  color="#95a5a6", linestyle="--")

    # Panel (b)
    ax2 = fig.add_subplot(2, 1, 2, projection=proj)
    ax2.set_extent([-180, 180, -60, 82], crs=proj)
    ax2.add_feature(cfeature.LAND.with_scale("110m"), facecolor="#f5f5f5",
                     edgecolor="none", zorder=0)
    ax2.add_feature(cfeature.OCEAN.with_scale("110m"), facecolor="#eaf3f8",
                     edgecolor="none", zorder=0)
    ax2.add_feature(cfeature.COASTLINE.with_scale("110m"),
                     edgecolor="#7f8c8d", linewidth=0.5)
    ax2.add_feature(cfeature.BORDERS.with_scale("110m"),
                     edgecolor="#bdc3c7", linewidth=0.3, linestyle=":")

    disc = flags[flags["ref_discordant_dry"]]
    for fam, color in [("HydraProbe", "#c0392b"),
                         ("Decagon/METER TDR", "#27ae60"),
                         ("Campbell CS6xx", "#2980b9"),
                         ("ThetaProbe", "#f39c12"),
                         ("other", "#7f8c8d")]:
        sub = disc[disc["family"] == fam]
        if len(sub) == 0: continue
        ax2.scatter(sub["lon"], sub["lat"], s=36, c=color, marker="s",
                     alpha=0.75, edgecolor="black", linewidth=0.3, transform=proj,
                     label=f"{fam} (n={len(sub)})")
    ax2.set_title("(b) Reference-discordant ISMN dry flags, stratified by sensor family",
                   fontsize=11)
    ax2.legend(loc="lower left", fontsize=8)
    ax2.gridlines(draw_labels=True, linewidth=0.3, alpha=0.4,
                   color="#95a5a6", linestyle="--")

    fig.suptitle("Extended Data Fig 4 — Geography of reference-discordant "
                  "ISMN dry classification by sensor family",
                  fontsize=12, y=0.995)
    fig.tight_layout()
    fig.savefig(BASE / "ed_fig4_drought_map.png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {BASE / 'ed_fig4_drought_map.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
