# Data dictionary

All soil-moisture residuals and RMSD values use volumetric units, m3/m3.

## `source_data/family_composition.csv`

- `family`: harmonized sensor-manufacturer family.
- `n_station_sensors`: retained ISMN station-sensor records.
- `share_percent`: percentage of the retained 1,625 station-sensor archive.
- `notes`: grouping or scope note.

## `source_data/family_reference_residuals.csv`

- `family`: harmonized sensor family.
- `n`: retained station-sensors in the family.
- `era5_mean`, `smap_l3e_mean`, `smap_smi_mean`: mean ISMN minus reference residual.
- `era5_std`: standard deviation of the ERA5-Land residual within family.
- `*_n`: available station-sensor count for that reference overlay.

## `source_data/validation_metrics_by_subset.csv`

- `reference`: product used as the comparison field.
- `full_RMSD`, `hydraprobe_RMSD`, `non_hydraprobe_RMSD`: mean-state RMSD by ISMN subset.
- `*_N`: sample size for that subset and product.
- `full_bias`, `hydraprobe_bias`, `non_hydraprobe_bias`: mean ISMN minus reference residual.

## `source_data/bias_corrections_by_subset.csv`

- `ismn_subset`: full, HydraProbe-only, or non-HydraProbe subset.
- `reference`: product used as the comparison field.
- `n`: sample size.
- `mean_ISMN_minus_ref`: mean residual; sign convention is ISMN minus product.

## `source_data/reweighting_sensitivity.csv`

- `reference`: product used as the comparison field.
- `full_bias`, `hydraprobe_bias`, `non_hydraprobe_bias`: mean ISMN minus reference residual from the subset metric table.
- `equal_HP_nonHP_bias`: simple 50/50 HydraProbe/non-HydraProbe reweighted bias.
- `delta_equal_HP_nonHP_minus_full`: change relative to the full-archive bias.

## `source_data/temporal_metrics_2021_by_family.csv`

- Real 2021 SMAP L3 SM_P (AM) overpass-matched validation metrics by sensor family.
- `n_stations`: retained station-sensors with at least 20 matched days.
- `bias_med`, `ubrmse_med`, `R_med`, `Ranom_med`: station-sensor median temporal metrics.
- `*_lo`, `*_hi`: 95% network-cluster bootstrap confidence interval bounds.

## `source_data/temporal_hp_vs_nonhp_2021.csv`

- HydraProbe versus non-HydraProbe contrast for the real 2021 temporal check.
- `HP_median`, `nonHP_median`: station-sensor medians by subset.
- `welch_t`, `welch_p`: Welch test on per-station metrics.

## `source_data/colocated_pair_summary.csv`

- `effect_nonhydraprobe_minus_hydraprobe_m3m3`: paired family contrast at co-located ISMN pairs.
- `ci_low_m3m3`, `ci_high_m3m3`: reported confidence interval bounds.

## `source_data/crns_cross_check_summary.csv`

- `hydraprobe_residual_mean_m3m3`: CRNS-reference residual for HydraProbe-family pairs.
- `nonhydraprobe_residual_mean_m3m3`: CRNS-reference residual for non-HydraProbe pairs.
- `contrast_hydraprobe_minus_nonhydraprobe_m3m3`: pooled CRNS family contrast.
- `ci_network_*`, `ci_site_*`, `ci_archive_*`: 95% bootstrap CI bounds when clustering by ISMN network, CRNS site, or archive.
- `welch_t`, `p_value`: pooled Welch test summary.
