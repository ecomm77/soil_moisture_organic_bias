# Phase 1 — Downstream impact quantification (sensor-family frame)

## A. Residual by sensor family × reference product

| family            |    n |   era5_mean |   era5_std |   era5_n |   smap_mean |   smap_n |   somo_mean |   somo_n |
|:------------------|-----:|------------:|-----------:|---------:|------------:|---------:|------------:|---------:|
| Campbell          |   65 |      -0.065 |      0.083 |       48 |       0.019 |       63 |      -0.024 |       65 |
| Decagon_METER     |   95 |       0.068 |      0.205 |       95 |       0.006 |       62 |      -0.074 |       95 |
| HydraProbe_family | 1274 |      -0.097 |      0.11  |     1231 |      -0.025 |      626 |      -0.037 |     1228 |
| TRIME             |    2 |      -0.179 |      0.001 |        2 |     nan     |        0 |      -0.086 |        2 |
| ThetaProbe        |   59 |      -0.039 |      0.087 |       59 |       0.001 |       59 |      -0.001 |       59 |
| other             |  130 |      -0.056 |      0.139 |      124 |       0.003 |       55 |      -0.022 |      124 |

## B. Counterfactual SMAP / ERA5 RMSD under ISMN sub-populations

| reference   |   full_RMSD |   full_N |   hydraprobe_RMSD |   hydraprobe_N |   non_hydraprobe_RMSD |   non_hydraprobe_N |   full_bias |   hydraprobe_bias |   non_hydraprobe_bias |
|:------------|------------:|---------:|------------------:|---------------:|----------------------:|-------------------:|------------:|------------------:|----------------------:|
| ERA5-Land   |      0.1493 |     1559 |            0.1467 |           1231 |                0.1587 |                328 |     -0.0809 |           -0.0973 |               -0.0192 |
| SMAP L3_E   |      0.1249 |      865 |            0.122  |            626 |                0.1323 |                239 |     -0.0163 |           -0.0254 |                0.0076 |
| SMAP-SMI    |      0.1093 |     1573 |            0.0989 |           1228 |                0.1401 |                345 |     -0.0364 |           -0.0372 |               -0.0336 |

## C. Implied ISMN-reference bias by sub-population

| ismn_subset     | reference   |    n |   mean_ISMN_minus_ref |
|:----------------|:------------|-----:|----------------------:|
| full ISMN       | ERA5-Land   | 1559 |               -0.0809 |
| full ISMN       | SMAP L3_E   |  865 |               -0.0163 |
| full ISMN       | SMAP-SMI    | 1573 |               -0.0364 |
| HydraProbe-only | ERA5-Land   | 1231 |               -0.0973 |
| HydraProbe-only | SMAP L3_E   |  626 |               -0.0254 |
| HydraProbe-only | SMAP-SMI    | 1228 |               -0.0372 |
| non-HydraProbe  | ERA5-Land   |  328 |               -0.0192 |
| non-HydraProbe  | SMAP L3_E   |  239 |                0.0076 |
| non-HydraProbe  | SMAP-SMI    |  345 |               -0.0336 |

## Headline for main paper

- HydraProbe-family residual against ERA5-Land: **-0.097~m³/m³** (n=1,231).
- Non-HydraProbe residual against ERA5-Land: **-0.019~m³/m³** (n=328).
- Family swing: **-0.078~m³/m³**.
- Full-ISMN RMSD vs ERA5-Land: 0.149~m³/m³; HydraProbe-only: 0.147; non-HydraProbe-only: 0.159.
- Interpretation: the conventional global RMSD reported in SMAP / ERA5 validation studies primarily reflects the HydraProbe sub-population because HydraProbe dominates the ISMN archive by 3:1.  Any product bias-corrected against the full ISMN inherits the HydraProbe-family dry bias in clay- and OM-rich settings.