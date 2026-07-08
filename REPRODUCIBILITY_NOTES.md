# Reproducibility notes

This package separates three reproducibility layers.

1. Included, directly runnable:
   - `scripts/rebuild_grsl_summary_figures.py`
   - `source_data/*.csv`
   - `figures/main/*.png`
   - `figures/supplement/*.png`

2. Included as provenance:
   - `source_data/temporal_metrics_2021_by_family.csv`
   - `source_data/temporal_hp_vs_nonhp_2021.csv`
   - `figures/supplement/family_temporal_real2021.png`
   - `scripts/legacy_project_scripts/real_matchup_2021.py`
   - `scripts/legacy_project_scripts/*.py`
   - `docs/DOWNLOAD_STRATEGY_ORIGINAL.md`
   - `docs/DOWNSTREAM_SUMMARY_ORIGINAL.md`

3. Not redistributed:
   - raw ISMN station files;
   - ERA5-Land NetCDF files;
   - SMAP L3_E files;
   - SMAP-SMI Zenodo product grids;
   - SoilGrids rasters;
   - raw CRNS archives.

The real 2021 temporal-check summaries are redistributed as derived
station-family metrics, not as raw ISMN or SMAP granules.

The non-redistributed datasets are public or provider-controlled and are listed in `source_data/public_data_sources.csv`.

The original workstation scripts predate this curated package and contain absolute paths. Those scripts are intentionally not rewritten in place, so the provenance snapshot remains faithful. The portable script is the package-level reviewer entry point.

## IP exclusion

The author's patent-facing dielectric-model implementation is intentionally excluded from this package. The included code does not implement the proprietary organic-matter-aware permittivity correction; it only rebuilds summary plots from already-derived validation tables.
