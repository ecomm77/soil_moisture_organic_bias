# Package manifest

Package: `paper2_GRSL_code_package_20260708`

Version: `v20260708`

Created: 2026-07-08

## Purpose

Curated code and source-data package for the GRSL letter on ISMN sensor-family composition and satellite soil-moisture validation metrics.

## Directory layout

- `README.md`: package overview and quick-start commands.
- `CITATION.cff`: citation metadata.
- `.zenodo.json`: Zenodo deposit metadata template.
- `LICENSE`: review-package reuse and third-party data notice.
- `requirements.txt`: minimal Python dependency list.
- `environment.yml`: conda environment definition.
- `DATA_DICTIONARY.md`: field definitions for included CSV files.
- `REPRODUCIBILITY_NOTES.md`: scope boundary for runnable, provenance, and non-redistributed layers.
- `source_data/`: curated small CSV files supporting the reported family composition, product metrics, pair test, and CRNS cross-check.
- `source_data/reweighting_sensitivity.csv`: equal HydraProbe/non-HydraProbe bias-sensitivity table.
- `source_data/temporal_metrics_2021_by_family.csv`: real 2021 overpass-matched SMAP temporal metrics by family.
- `source_data/temporal_hp_vs_nonhp_2021.csv`: HydraProbe versus non-HydraProbe temporal-metric contrast.
- `scripts/rebuild_grsl_summary_figures.py`: portable script that rebuilds main summary plots from included CSVs.
- `scripts/check_package_integrity.py`: required-file checker.
- `scripts/legacy_project_scripts/real_matchup_2021.py`: local provenance script for the real 2021 SMAP temporal check.
- `scripts/legacy_project_scripts/`: provenance snapshot of local analysis/plotting scripts, excluding patent-facing dielectric-model code.
- `figures/main/`: main manuscript figure files.
- `figures/supplement/`: supplement figure files, including the real 2021 temporal validation figure.
- `manuscript_snapshot/`: GRSL TeX/PDF snapshot.
- `docs/`: original download strategy and downstream metric notes.
- `outputs/`: rebuilt outputs produced by the portable script.

## Required verification commands

```bash
python scripts/rebuild_grsl_summary_figures.py
python scripts/check_package_integrity.py
```

Expected status:

- rebuilt summary figures written under `outputs/`;
- integrity check returns `PASS: required files present`.

## Non-redistributed inputs

Raw public/provider datasets are not bundled. They are listed in `source_data/public_data_sources.csv` and discussed in `REPRODUCIBILITY_NOTES.md`.

## Intellectual-property boundary

Patent-facing dielectric-model implementation files are intentionally not included. This package contains empirical validation summaries and reviewer-facing plotting/check scripts only.
