# Soil Moisture Organic-Matter Bias Study — Tiered Download Strategy

**Purpose:** Establish that TDR/capacitance-based in-situ soil moisture is biased in organic-rich soils, using independent (non-dielectric) reference data. This document is a self-contained execution plan — it can be opened on any machine and worked through top-to-bottom.

**Local context note:** This is a provenance copy of the original workstation download plan. Replace `PROJECT_ROOT` with a local working directory and configure provider credentials on the machine where the raw-data pipeline is run.

---

## 0. Prerequisites (install once per machine)

### 0.1 System tools
```bash
# macOS
brew install wget curl jq git python@3.11 aria2

# Linux
sudo apt-get install -y wget curl jq git python3.11 python3-pip aria2
```

### 0.2 Python environment
```bash
cd PROJECT_ROOT/soil_moisture_organic_bias
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install earthaccess cdsapi xarray netCDF4 h5py h5netcdf pandas numpy \
            requests pyyaml tqdm beautifulsoup4 lxml pooch \
            ismn cosmoz pykrige scikit-learn
```

### 0.3 Credentials required (register each account ONCE, then save)
| Service | Used for | Register URL | Credential file |
|---|---|---|---|
| NASA Earthdata | SMAP, SMOS-IC, MODIS | https://urs.earthdata.nasa.gov/users/new | `~/.netrc` |
| Copernicus CDS | ERA5-Land | https://cds.climate.copernicus.eu/user/register | `~/.cdsapirc` |
| TERENO DDP | German lysimeters | https://ddp.tereno.net/ddp/ (account request form) | portal login |
| ICOS Carbon Portal | Euro flux sites | https://cpauth.icos-cp.eu/ | OAuth token |
| CEH EIDC | COSMOS-UK | https://eidc.ac.uk/ | portal login |
| PANGAEA | open, no login | https://pangaea.de/ | — |
| ESSD / Zenodo | open | — | — |

**~/.netrc** template (chmod 600):
```
machine urs.earthdata.nasa.gov login YOUR_EARTHDATA_USER password YOUR_EARTHDATA_PASS
```

**~/.cdsapirc** template:
```
url: https://cds.climate.copernicus.eu/api
key: YOUR_UID:YOUR_API_KEY
```

### 0.4 Directory layout (created automatically by the scripts below)
```
soil_moisture_organic_bias/
├── download_strategy.md        ← this file
├── scripts/
│   ├── tier1_lysimeter.sh
│   ├── tier2_crns.sh
│   ├── tier3_gravimetric.py
│   └── tier4_products.py
├── data/
│   ├── tier1_lysimeter/
│   │   ├── TERENO/
│   │   ├── HOAL/
│   │   ├── Rietholzbach/
│   │   ├── USDA_ARS/
│   │   ├── Wageningen/
│   │   ├── FMI_Finland/
│   │   └── JamesHutton_UK/
│   ├── tier2_crns/
│   │   ├── COSMOS_US/
│   │   ├── COSMOS_UK/
│   │   ├── COSMOS_Europe/
│   │   └── CosmOz_AU/
│   ├── tier3_gravimetric/
│   │   ├── literature_metaanalysis/
│   │   ├── NEON_soilcore/
│   │   ├── FLUXNET_soilcore/
│   │   └── PANGAEA_campaigns/
│   └── tier4_products/
│       ├── SMAP_L3_L4/
│       ├── SMOS_IC/
│       ├── ERA5_Land/
│       └── SoMo.ml/
└── logs/
```

---

## TIER 1 — Lysimeter networks (weight-based, GOLD standard)

Lysimeters give continuous time-series of soil water mass; they are immune to the dielectric-permittivity bias that affects TDR/FDR/capacitance sensors. **Priority is sites with high organic-matter horizons (peatland, forest Oa/Oe, wetland).**

### 1.1 TERENO (Germany) — HIGH PRIORITY
- Portal: https://ddp.tereno.net/ddp/
- Access: registered account (free, ~1 business day)
- Organic-rich sites to request first:
  - **Schechenfilz** (Bavarian Alps observatory) — raised bog, >95% organic
  - **Wüstebach** (Eifel/Lower Rhine) — forest with organic Oa horizon
  - **Rollesbroich** — grassland, moderate OM
  - **Bad Lauchstädt** — agricultural reference (low OM, control)
- Variables needed: weighing lysimeter mass (kg), drainage (kg), and the collocated TDR/FDR profile (SMC % vol) — this pairing is what lets you compute the bias directly.
- Temporal coverage: 2010–present (site-dependent)
- Expected size: ~50 GB all sites, all vars, 10-min resolution
- Citation requirement: Zacharias et al. 2011 VZJ + each site's DOI

**Programmatic access after login:** TERENO uses a WebDAV + DOI-linked download model. After registration, each dataset has a persistent DOI with direct NetCDF/CSV endpoints. Keep each `curl` in `scripts/tier1_lysimeter.sh`.

### 1.2 HOAL (Austria) — MEDIUM PRIORITY
- Hydrological Open Air Laboratory Petzenkirchen
- URL: https://hoal.hydrology.at/
- Contact: hoal@tuwien.ac.at (data request — they respond in <1 week)
- Lysimeters: 3 weighing lysimeters with paired TDR profiles
- Organic content: mostly mineral Cambisol but has humic horizons — useful as "low-OM" control cluster

### 1.3 Rietholzbach (Switzerland) — HIGH PRIORITY
- ETH Zurich, Inst. of Atmospheric & Climate Science
- URL: https://iac.ethz.ch/group/land-climate-dynamics/research/rietholzbach.html
- 1976–present (one of the longest weighing-lysimeter records in the world)
- Data access: email Sonia Seneviratne's group or via PANGAEA deposits (search "Rietholzbach lysimeter")
- Published: Seneviratne et al. 2012 JoH; Hirschi et al. 2017

### 1.4 USDA ARS lysimeter sites — LOW PRIORITY (mostly arid, low OM)
- Bushland, TX: https://www.ars.usda.gov/plains-area/bushland-tx/cprl/
- Coshocton, OH: legacy data 1937–2011, higher OM — **include this one**
- Direct data links: request via USDA ARS Data Commons (https://data.nal.usda.gov/)

### 1.5 Wageningen (Netherlands) peat polder lysimeters — HIGH PRIORITY
- Dutch peat meadows: Zegveld, Assendelft, Vlist
- NOBV (Nationaal Onderzoeksprogramma Broeikasgassen Veenweiden) network
- URL: https://www.nobveenweiden.nl/
- Data via 4TU.ResearchData and NOBV data warehouse
- Search DOI: `10.4121` + "peat lysimeter"

### 1.6 Finnish FMI lysimeters (boreal) — HIGH PRIORITY
- Sodankylä, Hyytiälä — both have peat/forest lysimeters
- URL: https://litdb.fmi.fi/
- Sodankylä Arctic Space Centre: https://litdb.fmi.fi/sodsmear.php
- Free download, login optional

### 1.7 James Hutton Institute (Scotland) — HIGH PRIORITY
- Glensaugh, Balruddery peatland lysimeters
- URL: https://www.hutton.ac.uk/research/environment/envcentre
- Data request: open-data@hutton.ac.uk
- Covers blanket peat — exactly the "worst case" for TDR bias

### `scripts/tier1_lysimeter.sh` skeleton
```bash
#!/usr/bin/env bash
set -euo pipefail
BASE="PROJECT_ROOT/soil_moisture_organic_bias/data/tier1_lysimeter"
LOG="PROJECT_ROOT/soil_moisture_organic_bias/logs/tier1.log"
mkdir -p "$BASE"/{TERENO,HOAL,Rietholzbach,USDA_ARS,Wageningen,FMI_Finland,JamesHutton_UK} "$(dirname "$LOG")"

# --- FMI Sodankylä (open) ---
cd "$BASE/FMI_Finland"
wget -c -a "$LOG" "https://litdb.fmi.fi/sodsmear_lys.php?format=csv&start=2010-01-01&end=2025-12-31" -O sodankyla_lysimeter.csv

# --- TERENO (fill in DOIs after DDP account approval) ---
# curl -u "$TERENO_USER:$TERENO_PASS" -o "$BASE/TERENO/schechenfilz.nc" "<DOI landing resolved URL>"

# --- Rietholzbach via PANGAEA ---
python -c "
import pooch, pathlib
out = pathlib.Path('$BASE/Rietholzbach')
out.mkdir(parents=True, exist_ok=True)
# PANGAEA search for active DOI, e.g.
pooch.retrieve('https://doi.pangaea.de/10.1594/PANGAEA.XXXXXX?format=textfile',
              known_hash=None, path=out, fname='rietholzbach.tab')
"
echo 'Remaining sites require portal requests — see download_strategy.md §1.1–1.7'
```

---

## TIER 2 — Cosmic-Ray Neutron Sensors (area-integrated, different bias direction)

CRNS measures fast-neutron flux; hydrogen in soil moisture is the dominant signal, but organic-matter H creates an additive offset that is *calibrated against gravimetric campaigns* at each station. The residual organic-H offset has the opposite sign/shape from TDR's dielectric bias — so **CRNS × TDR disagreement localizes the organic-matter bias in geography.**

### 2.1 COSMOS-US (~60 stations) — HIGH PRIORITY
- URL: https://cosmos.hwr.arizona.edu/Probes/probemap.php
- Direct CSV per station, e.g. level 2 product:
  `https://cosmos.hwr.arizona.edu/Probes/StationDat/<ID>/smcounts.txt`
- Station list: download `sitenames.php` to parse station IDs
- **Organic-rich priority stations:** Howland (ME, spruce forest), Harvard Forest (MA), Silas Little (NJ pine barrens), Park Falls (WI peat-adjacent)

### 2.2 COSMOS-UK (~50 stations) — HIGH PRIORITY
- UKCEH EIDC portal: https://catalogue.ceh.ac.uk/documents/5402b1eb-9656-4bc5-9d87-f86e71a93ffe
- Free after registration; all stations, Level 1, daily + subdaily
- **Priority peatland sites:** Moor House (blanket bog), Auchencorth Moss, Plynlimon, Glensaugh

### 2.3 COSMOS-Europe (unified dataset) — HIGHEST PRIORITY
- Bogena et al. 2022, *Earth System Science Data* — one paper, one dataset, 66 stations harmonized
- DOI: https://doi.org/10.1594/PANGAEA.940829 (verify at download time — Bogena team may have issued updates)
- Fully open, single-tarball download
- This alone gives you pan-European CRNS in one pass

### 2.4 CosmOz (Australia) — MEDIUM PRIORITY
- https://cosmoz.csiro.au/
- CSIRO data access portal, REST API for each station
- Mostly dry, low-OM — but include Tumbarumba (wet-forest) and Daly tropical sites

### 2.5 Individual national nodes to watch
- China: Chinese Academy of Sciences CRNS network (contact via CERN)
- India: ICAR CRNS at Hyderabad — request via IMD
- South Korea: KMA/NIMR CRNS (if any) — local contact

### `scripts/tier2_crns.sh` skeleton
```bash
#!/usr/bin/env bash
set -euo pipefail
BASE="PROJECT_ROOT/soil_moisture_organic_bias/data/tier2_crns"
mkdir -p "$BASE"/{COSMOS_US,COSMOS_UK,COSMOS_Europe,CosmOz_AU}

# COSMOS-Europe single-shot (open)
cd "$BASE/COSMOS_Europe"
wget -c "https://hs.pangaea.de/Projects/COSMOS-Europe/COSMOS-Europe_v1.zip" -O cosmos_europe_v1.zip
unzip -n cosmos_europe_v1.zip

# COSMOS-US: loop through stations
cd "$BASE/COSMOS_US"
curl -s "https://cosmos.hwr.arizona.edu/Probes/sitenames.php" > sitenames.html
python3 - <<'PY'
import re, pathlib, requests
html = pathlib.Path("sitenames.html").read_text()
ids = sorted(set(re.findall(r"StationDat/(\d+)/", html)))
for i in ids:
    url = f"https://cosmos.hwr.arizona.edu/Probes/StationDat/{i}/smcounts.txt"
    r = requests.get(url, timeout=60)
    if r.ok:
        pathlib.Path(f"{i}_smcounts.txt").write_bytes(r.content)
        print("ok", i)
    else:
        print("miss", i, r.status_code)
PY

# CosmOz: API
cd "$BASE/CosmOz_AU"
curl -s "https://esoil.io/cosmoz-rest/rest/site" -o sites.json
# then loop via jq + curl to https://esoil.io/cosmoz-rest/rest/site/<id>/readings
```

---

## TIER 3 — Gravimetric literature meta-analysis + discrete campaigns

For the **mechanism / calibration curve** (TDR bias as a function of organic-matter fraction, bulk density, and temperature), a meta-analysis of paired TDR-vs-gravimetric data from existing papers is more efficient than collecting new samples.

### 3.1 Literature meta-analysis — HIGH PRIORITY
**Databases:** Web of Science, Scopus, Google Scholar.

**Queries (save these verbatim, paste into each database):**
```
TS=("time domain reflectometry" OR "TDR" OR "FDR" OR "capacitance probe")
   AND TS=("organic soil*" OR "peat*" OR "histosol*" OR "organic matter")
   AND TS=("gravimetric" OR "oven-dried" OR "thermogravimetric" OR "calibration")
   AND TS=("soil moisture" OR "water content" OR "θ" OR "volumetric")
Timespan: 1985–present
```

**Key known studies to cite and extract data from (seed list):**
- Roth et al. 1990 WRR — Topp equation for organic soils
- Myllys & Simojoki 1996 — Finnish peat TDR calibration
- Kellner & Lundin 2001 JH — Swedish peatland
- Beckwith et al. 2003 — UK blanket peat TDR bias
- Oleszczuk et al. 2004 — Polish fen
- Bircher et al. 2016 HESS — European site-specific calibrations
- Dettmann et al. 2019 Eur J Soil Sci — calibration function for histosols
- Liu et al. 2020 JoH — China boreal peatland
- Dimitrov et al. 2021 — Canadian peatland FDR vs gravimetric
- Walker et al. 2004 JoH — forest Oa horizon TDR bias

**Extraction workflow:**
1. Export all hits as RIS/BibTeX → Zotero
2. For each paper with paired TDR-gravimetric data, scrape Table 1/2 and Fig. 3-type calibration plots (WebPlotDigitizer)
3. Schema: `paper_id, site, lat, lon, soil_type, OM_percent, bulk_density, sensor_type, theta_TDR, theta_gravimetric, temperature`
4. Save as `data/tier3_gravimetric/literature_metaanalysis/paired_measurements.csv`

### 3.2 NEON soil cores — HIGH PRIORITY
- URL: https://data.neonscience.org/
- Products:
  - DP1.10086.001 Soil physical and chemical properties, periodic
  - DP1.00094.001 Soil water content and water salinity (includes some gravimetric calibration)
- Access: open via the `neonUtilities` R package or `nedownload` Python package
- All NEON sites have collocated TDR + periodic soil cores → direct paired comparison
- Organic-rich NEON sites: BART (Bartlett Experimental Forest NH), HARV (Harvard), DEJU (Delta Junction AK boreal), BONA (Bonanza Creek AK), TOOL (Toolik AK tundra), ORNL (Oak Ridge)

```bash
pip install neonutilities
python -c "
import neonutilities as nu, pathlib
out = pathlib.Path('$PWD/data/tier3_gravimetric/NEON_soilcore')
out.mkdir(parents=True, exist_ok=True)
for prod in ['DP1.10086.001','DP1.00094.001']:
    nu.zips_by_product(dpID=prod, site='all', savepath=str(out), check_size=False)
"
```

### 3.3 FLUXNET site soil cores — MEDIUM PRIORITY
- FLUXNET2015 + AmeriFlux + ICOS-ETC ancillary "BADM" tables often contain gravimetric soil data
- AmeriFlux: https://ameriflux.lbl.gov/data/download-data/
- ICOS ETC: https://www.icos-cp.eu/data-services
- FLUXNET-CH4 local copy, if available — peat-rich sites like Mer Bleue, Stordalen, Degerö

### 3.4 PANGAEA campaign-level gravimetric datasets — HIGH PRIORITY
- Search: https://www.pangaea.de/?q=gravimetric+soil+moisture+peat
- Full-text API: `https://ws.pangaea.de/es/pangaea?q=gravimetric+soil+moisture+peat&size=500`
- Automated harvest via `pangaeapy` package:
  ```bash
  pip install pangaeapy
  ```

### `scripts/tier3_gravimetric.py` skeleton
```python
#!/usr/bin/env python3
"""Harvest gravimetric soil-moisture datasets across NEON, PANGAEA, FLUXNET."""
import pathlib, pangaeapy, neonutilities as nu

BASE = pathlib.Path("PROJECT_ROOT/soil_moisture_organic_bias/data/tier3_gravimetric")

# PANGAEA
pg_out = BASE / "PANGAEA_campaigns"; pg_out.mkdir(parents=True, exist_ok=True)
query = "gravimetric soil moisture peat"
for ds in pangaeapy.PanQuery(query=query, limit=500).result:
    try:
        pangaeapy.PanDataSet(ds['URI']).to_csv(pg_out / f"{ds['ID']}.csv")
    except Exception as e:
        print("skip", ds.get('ID'), e)

# NEON
neon_out = BASE / "NEON_soilcore"; neon_out.mkdir(parents=True, exist_ok=True)
for prod in ["DP1.10086.001", "DP1.00094.001"]:
    nu.zips_by_product(dpID=prod, site="all", savepath=str(neon_out), check_size=False)
```

---

## TIER 4 — Target products to re-validate and re-train (SMAP, SMOS, ERA5-Land, SoMo.ml)

Once Tier 1–3 give the bias function, apply it to correct ISMN, then re-grade these products.

### 4.1 SMAP L3/L4 (NASA)
- NSIDC DAAC: https://nsidc.org/data/smap
- Recommended: L3 SPL3SMP_E (enhanced 9-km), L4 SPL4SMGP (3-hr 9-km)
- Python via `earthaccess`:
  ```python
  import earthaccess
  earthaccess.login()  # uses ~/.netrc
  r = earthaccess.search_data(short_name="SPL3SMP_E", version="005",
                              temporal=("2015-04-01","2025-12-31"))
  earthaccess.download(r, "./data/tier4_products/SMAP_L3_L4/")
  ```

### 4.2 SMOS-IC v2 — INRA/CESBIO
- Catalog: https://www.catds.fr/Products/Available-products-from-CEC-SM/SMOS-IC
- FTP/HTTP tree: https://www.catds.fr/sipad/ (account)
- Product: daily 25-km TB → soil moisture

### 4.3 ERA5-Land
- CDS API:
  ```python
  import cdsapi
  c = cdsapi.Client()
  c.retrieve("reanalysis-era5-land",
             {"variable":["volumetric_soil_water_layer_1",
                          "volumetric_soil_water_layer_2"],
              "year":[str(y) for y in range(1981,2026)],
              "month":[f"{m:02d}" for m in range(1,13)],
              "day":[f"{d:02d}" for d in range(1,32)],
              "time":[f"{h:02d}:00" for h in range(0,24,3)],
              "format":"netcdf"},
             "./data/tier4_products/ERA5_Land/era5land_sm_%Y.nc")
  ```
  (Split per-year to avoid CDS queue caps — use a loop.)

### 4.4 SoMo.ml — O & K Benchmark
- Zenodo: https://zenodo.org/record/5206307 (v1) — check for newer versions
- Direct wget, open access

### 4.5 ESA CCI Soil Moisture
- https://www.esa-soilmoisture-cci.org/
- Combined/active/passive products, 1978–present, 0.25°
- Registration free, bulk FTP available

---

## 5. Cross-cutting data: organic-matter/peat maps (for stratification)

Needed to group stations by organic-matter bin.
| Dataset | Purpose | URL |
|---|---|---|
| SoilGrids 250 m (v2.0) | Global SOC, clay, bulk density | https://www.isric.org/explore/soilgrids |
| WISE30sec | Harmonized soil profile db | https://www.isric.org/explore/wise-databases |
| PEATMAP (Xu et al. 2018) | Global peatland extent | https://archive.researchdata.leeds.ac.uk/251/ |
| Global Peatland Database (IMCG) | Tropical + boreal peat | request via IMCG |
| HWSD v2.0 | FAO Harmonized World Soil Db | https://www.fao.org/soils-portal/data-hub |

Download these once; they are small (<20 GB total) and gate all stratification analyses.

---

## 6. Execution order & budget

| Phase | Tier | Effort | Data volume | Gate |
|---|---|---|---|---|
| Week 1 | §0 setup + §5 ancillary maps | 1 day | 20 GB | prerequisites working |
| Week 1–2 | §2 COSMOS-Europe + §1 FMI (open) | 2 days | ~30 GB | first open wins |
| Week 2–4 | §1 TERENO, Rietholzbach, Wageningen, Hutton (account requests) | parallel waits | ~50 GB | credentials arrive |
| Week 3–6 | §3 meta-analysis extraction | 3 weeks human | 1 GB | calibration curve |
| Week 5–8 | §4 SMAP, ERA5-Land, SoMo.ml | 1 week download, 4 weeks analysis | ~2 TB | corrected products |
| Week 8+ | ML re-training on corrected ISMN | 4 weeks | — | manuscript figures |

Rough total raw data footprint: **≈ 2.5 TB**. Use a large local or external volume and move cold products to external storage only when analysis is frozen.

---

## 7. Validation / QC checklist (to be checked off as each tier lands)

- [ ] §0.3 All credentials verified by a trivial API call
- [ ] §1 At least 3 lysimeter sites with paired TDR time series downloaded and plotted
- [ ] §2 COSMOS-Europe unified dataset opens in xarray, timestamps parse UTC
- [ ] §3 Meta-analysis CSV has ≥ 50 papers, ≥ 1000 paired (θ_TDR, θ_grav) points
- [ ] §4 SMAP L3_E 2015–present volume complete, md5 verified
- [ ] §5 SoilGrids SOC + PEATMAP resampled to SMAP 9-km grid
- [ ] End-to-end: bias function applied to one ISMN organic-soil station, residual shrinks

---

## 8. Contacts log (fill in as you email)

| Date | Person / org | Request | Status |
|---|---|---|---|
|  | TERENO DDP support | account + Schechenfilz, Wüstebach DOIs |  |
|  | HOAL (TU Vienna) | lysimeter + TDR CSV |  |
|  | Sonia Seneviratne group, ETH | Rietholzbach full record |  |
|  | NOBV data warehouse | Zegveld/Assendelft peat lysimeters |  |
|  | James Hutton open-data | Glensaugh/Balruddery peat lysimeter |  |

---

## 9. Notes

- Keep every raw download file immutable; do analysis on copies under `processed/`.
- Log every `wget`/`curl` into `logs/tierN.log` with `-a` so re-runs are idempotent.
- For any dataset where the URL may change, also store the DOI — DOIs are stable, URLs are not.
- When in doubt, choose the dataset with paired TDR+reference measurements at the SAME site — pairing is what makes the bias claim defensible.
