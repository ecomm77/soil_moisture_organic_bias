# GRSL sensor-family validation code package

Package version: v20260708

This package supports the GRSL letter:

`Sensor-Family Composition of the In-Situ Archive Changes the Apparent Bias and RMSD of Satellite Soil-Moisture Products`

It is a curated review package, not a mirror of all raw public downloads. It includes:

- the GRSL manuscript snapshot used for the package;
- the main and supplement figure files referenced by the manuscript;
- small source-data CSVs for the reported family composition, product metrics, reweighting sensitivity, temporal-check metrics, and robustness summaries;
- a portable script that rebuilds the main summary plots from the included CSVs;
- the real 2021 SMAP L3 SM_P temporal-check outputs and the local provenance script used to generate them;
- legacy project scripts from the local analysis folder for provenance.

## Intellectual-property boundary

This package deliberately excludes the author's patent-facing dielectric-model implementation and any code that encodes the proprietary organic-matter-aware permittivity correction. The package is limited to manuscript-level validation summaries: sensor-family counts, empirical residuals, product RMSD/bias summaries, co-located-pair statistics, CRNS cross-check summaries, and plotting code for those derived tables.

## Quick start

```bash
cd paper2_GRSL_code_package_20260708
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/rebuild_grsl_summary_figures.py
python scripts/check_package_integrity.py
```

The first script writes rebuilt summary outputs into `outputs/`. The integrity script checks required files and reports package size.

The package intentionally excludes `tools/out_demo/` synthetic self-test outputs. The included temporal CSVs under `source_data/` are the real 2021 SMAP L3 SM_P (AM) matchup summaries copied from `tools/real2021/`.

## Important scope note

The full raw-data pipeline depends on public source archives that are not redistributed here: ISMN station records, ERA5-Land, SMAP L3_E, SMAP-SMI Zenodo record 15015557, SoilGrids, COSMOS-Europe, COSMOS-UK, CosmOz, and COSMOS-USA derived tables from the cited HESS supplement. Access details are summarized in `docs/DOWNLOAD_STRATEGY_ORIGINAL.md` and `source_data/public_data_sources.csv`.

The legacy scripts under `scripts/legacy_project_scripts/` are preserved from the working analysis folder only when they support figure/report provenance without disclosing the patent-facing dielectric-model implementation. Some of those scripts use absolute local paths from the original workstation and require the original processed CSVs. The portable script in `scripts/rebuild_grsl_summary_figures.py` is the runnable reviewer entry point for this package.

## Main package contents

- `source_data/family_composition.csv`: ISMN retained station-sensor counts by manufacturer family.
- `source_data/family_reference_residuals.csv`: family mean residuals against ERA5-Land, SMAP L3_E, and SMAP-SMI.
- `source_data/validation_metrics_by_subset.csv`: full, HydraProbe-only, and non-HydraProbe RMSD and bias metrics.
- `source_data/bias_corrections_by_subset.csv`: implied ISMN-reference mean bias by product and subset.
- `source_data/reweighting_sensitivity.csv`: equal HydraProbe/non-HydraProbe bias sensitivity derived from the subset metrics.
- `source_data/temporal_metrics_2021_by_family.csv`: real 2021 overpass-matched SMAP temporal metrics by family.
- `source_data/temporal_hp_vs_nonhp_2021.csv`: HydraProbe versus non-HydraProbe temporal-metric contrast.
- `source_data/colocated_pair_summary.csv`: co-located pair robustness summary.
- `source_data/crns_cross_check_summary.csv`: dielectric-independent CRNS cross-check summary.
- `figures/main/`: GRSL main figure files.
- `figures/supplement/`: supplement figure file.
- `manuscript_snapshot/`: TeX/PDF snapshot used for this package.

## Citation

Public archive:

Zenodo DOI: https://doi.org/10.5281/zenodo.21263063

Public GitHub mirror:

https://github.com/ecomm77/soil_moisture_organic_bias

Package citation:

Park, C.-H. (2026). GRSL sensor-family validation code package, v20260708. Zenodo. https://doi.org/10.5281/zenodo.21263063
