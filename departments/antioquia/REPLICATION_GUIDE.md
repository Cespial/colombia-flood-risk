# Replication Guide: Municipality-Scale Flood Risk Mapping

**How to replicate this research framework for any Colombian department (or tropical region)**

Cristian Espinal Maya & Santiago Jimenez Londono — Universidad EAFIT, 2026

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Account Setup & Credentials](#2-account-setup--credentials)
3. [Environment Setup](#3-environment-setup)
4. [Configuration: Adapting to a New Department](#4-configuration-adapting-to-a-new-department)
5. [Pipeline Step-by-Step](#5-pipeline-step-by-step)
6. [Parameter Reference](#6-parameter-reference)
7. [GEE Asset IDs (Global — No Changes Needed)](#7-gee-asset-ids-global--no-changes-needed)
8. [Department-Specific Data to Update](#8-department-specific-data-to-update)
9. [Expected Outputs](#9-expected-outputs)
10. [Troubleshooting](#10-troubleshooting)
11. [Estimated Computation Times](#11-estimated-computation-times)
12. [Recommendations for Different Regions](#12-recommendations-for-different-regions)
13. [Quality Control Checklist](#13-quality-control-checklist)
14. [Publication Workflow](#14-publication-workflow)

---

## 1. Prerequisites

### Software

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Pipeline execution |
| Git | 2.30+ | Version control |
| LaTeX (TeX Live / MiKTeX) | 2023+ | Manuscript compilation |
| Google Chrome | Latest | GEE Code Editor access |

### Python Libraries

```bash
pip install earthengine-api google-auth google-cloud-storage \
            scikit-learn==1.5.2 xgboost==2.1.3 lightgbm==4.5.0 \
            shap==0.45 matplotlib==3.9 seaborn==0.13 \
            geopandas==0.14 pandas==2.2 numpy==1.26 \
            pymannkendall scipy rasterio shapely \
            python-dotenv joblib
```

### Hardware

- **Minimum:** Any laptop with 8 GB RAM and internet connection (GEE does the heavy processing)
- **Recommended:** 16 GB RAM for ML training with large sample sets
- **Storage:** ~5 GB for exports, figures, and models

---

## 2. Account Setup & Credentials

### 2.1 Google Earth Engine (Required)

1. Go to [signup.earthengine.google.com](https://signup.earthengine.google.com/)
2. Sign up with a Google account (institutional email recommended for faster approval)
3. Create a GEE Cloud Project:
   - Go to [console.cloud.google.com](https://console.cloud.google.com/)
   - Create a new project (e.g., `ee-flood-risk-{department}`)
   - Enable the Earth Engine API: **APIs & Services > Enable APIs > Earth Engine API**
4. Note your **Project ID** (e.g., `ee-flood-risk-valle`)

### 2.2 Authentication

```bash
# First-time authentication
earthengine authenticate

# Test connection
python -c "import ee; ee.Initialize(project='YOUR_PROJECT_ID'); print('OK')"
```

### 2.3 Environment Variables

Create a `.env` file in the project root:

```env
GEE_PROJECT_ID=ee-flood-risk-{department}
```

### 2.4 Google Drive (for exports)

GEE exports rasters and tables to Google Drive. Ensure you have at least **10 GB free** in the Drive associated with your GEE account. Exports go to a folder named `{department}_flood_risk/`.

### 2.5 GitHub (Optional, for publication)

```bash
gh auth login
gh repo create {username}/{department}-flood-risk --public
```

### 2.6 SSRN / arXiv (for preprint publication)

- **SSRN:** [ssrn.com](https://www.ssrn.com/) — No endorsement needed, upload PDF directly
- **arXiv:** [arxiv.org](https://arxiv.org/) — Requires endorsement from an existing author in the chosen category

---

## 3. Environment Setup

### 3.1 Clone the Template Repository

```bash
git clone https://github.com/Cespial/antioquia-flood-risk.git {department}-flood-risk
cd {department}-flood-risk
```

### 3.2 Project Structure

```
.
├── gee_config.py              # <-- MAIN FILE TO MODIFY
├── scripts/
│   ├── 01_sar_water_detection.py
│   ├── 02_jrc_water_analysis.py
│   ├── 03_flood_susceptibility_features.py
│   ├── 04_ml_flood_susceptibility.py
│   ├── 05_population_exposure.py
│   ├── 06_climate_analysis.py
│   ├── 07_visualization.py
│   ├── 08_generate_tables.py
│   └── 09_quality_control.py
├── overleaf/                  # Manuscript
├── data/                      # Downloaded data (auto-created)
├── outputs/                   # Results (auto-created)
└── .env                       # Credentials
```

### 3.3 Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

---

## 4. Configuration: Adapting to a New Department

> **The only file you MUST modify is `gee_config.py`.** All scripts read parameters from this central config.

### 4.1 Study Area (CRITICAL)

```python
# gee_config.py — Lines to change:

# Administrative boundaries
ADMIN_DATASET = 'FAO/GAUL/2015/level1'       # Keep as-is (global dataset)
DEPARTMENT_NAME = 'Valle del Cauca'            # <-- YOUR DEPARTMENT
COUNTRY_NAME = 'Colombia'                      # <-- YOUR COUNTRY

# Municipal boundaries
MUNICIPAL_DATASET = 'FAO/GAUL/2015/level2'    # Keep as-is
```

### 4.2 Subregions (CRITICAL)

Define the subregions and their municipalities. This is department-specific. For Colombian departments, consult [DANE territorial division](https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion).

```python
SUBREGIONS = {
    'Subregion A': ['Municipality1', 'Municipality2', ...],
    'Subregion B': ['Municipality3', 'Municipality4', ...],
    # ...
}
```

**How to find municipality names in GEE:**
```python
import ee
ee.Initialize(project='YOUR_PROJECT_ID')
dept = ee.FeatureCollection('FAO/GAUL/2015/level2') \
    .filter(ee.Filter.eq('ADM1_NAME', 'Valle del Cauca'))
names = dept.aggregate_array('ADM2_NAME').getInfo()
print(sorted(names))
```

### 4.3 Temporal Configuration

```python
# Adjust if you want a different study period
ANALYSIS_START = '2015-01-01'  # Sentinel-1 available from Oct 2014
ANALYSIS_END = '2025-12-31'    # Or your desired end date
```

### 4.4 Map Center

```python
MAP_CENTER = {'lat': 3.4, 'lon': -76.5}  # Center of your department
MAP_ZOOM = 9                               # Adjust for area size
```

### 4.5 GEE Project ID

```python
ee.Initialize(project=os.getenv('GEE_PROJECT_ID', 'ee-flood-risk-valle'))
```

### 4.6 Export Folder

Search and replace `"antioquia_flood_risk"` with `"{department}_flood_risk"` across all scripts:

```bash
# From the project root:
grep -rn "antioquia_flood_risk" scripts/
# Then replace in each file, or use:
sed -i '' 's/antioquia_flood_risk/valle_flood_risk/g' scripts/*.py
```

### 4.7 GEE Asset Paths

If you export assets to GEE (susceptibility maps), update the asset ID:

```python
# In 05_population_exposure.py, update:
"projects/ee-maestria-tesis/assets/antioquia_flood_susceptibility_ensemble"
# To:
"projects/YOUR_PROJECT_ID/assets/{department}_flood_susceptibility_ensemble"
```

---

## 5. Pipeline Step-by-Step

### Step 1: SAR Water Detection (~4 hours on GEE)

```bash
python scripts/01_sar_water_detection.py
```

**What it does:**
- Filters all Sentinel-1 GRD scenes for the study area (2015-2025)
- Applies focal-median speckle filter (50 m kernel)
- Computes adaptive Otsu threshold per scene on VV band
- Generates monthly binary water masks (132 composites)
- Creates annual maximum flood extent maps
- Computes multi-year water frequency

**Outputs (to Google Drive):**
- `{dept}_sar_flood_max_{year}.tif` (11 annual maps)
- `{dept}_sar_water_frequency.tif` (1 frequency map)

**Monitor progress:** [code.earthengine.google.com](https://code.earthengine.google.com/) > Tasks tab

### Step 2: JRC Water Analysis (~30 min on GEE)

```bash
python scripts/02_jrc_water_analysis.py
```

**What it does:**
- Loads JRC Global Surface Water layers (occurrence, seasonality, change, transitions)
- Classifies flood frequency into 5 categories
- Computes seasonal water dynamics (DJF, MAM, JJA, SON)
- Calculates water trend (increasing/decreasing/stable)
- Validates SAR detection against JRC (confusion matrix, Kappa, F1)

**Outputs:**
- JRC layers exported to Drive
- Validation metrics (CSV)
- Municipal-level JRC statistics

### Step 3: Feature Engineering (~2 hours on GEE)

```bash
python scripts/03_flood_susceptibility_features.py
```

**What it does:**
- Computes 18 predictor variables from 10 datasets:

| # | Feature | Source | Resolution |
|---|---------|--------|-----------|
| 1 | Elevation | SRTM | 30 m |
| 2 | Slope | SRTM | 30 m |
| 3 | Aspect | SRTM | 30 m |
| 4 | Plan curvature | SRTM (Laplacian 3x3) | 30 m |
| 5 | HAND | MERIT Hydro | 90 m (resampled to 30 m) |
| 6 | TWI | SRTM + MERIT Hydro | 30 m |
| 7 | SPI (Stream Power) | SRTM + MERIT Hydro | 30 m |
| 8 | Distance to rivers | JRC occurrence >= 75% | 30 m |
| 9 | Drainage density | JRC (1 km focal mean) | 30 m |
| 10 | Annual rainfall | CHIRPS 2015-2025 mean | 5.5 km |
| 11 | Max monthly rainfall | CHIRPS highest month mean | 5.5 km |
| 12 | Soil moisture | ERA5-Land 2015-2025 mean | 11 km |
| 13 | Land cover | ESA WorldCover 2021 | 10 m |
| 14 | NDVI | Sentinel-2 2021 mean | 10 m |
| 15 | Distance to roads | Oxford/MAP friction surface | 1 km |
| 16 | Population density | WorldPop 2020 | 100 m |
| 17 | JRC occurrence | JRC GSW v1.4 | 30 m |
| 18 | SAR water frequency | This study (Step 1) | 10 m |

- Generates training samples (5,000 per class, stratified by subregion)
- Exports feature stack and training CSV to Drive

**Training Label Criteria:**
- **Flood-positive:** JRC occurrence >= 25% OR HAND < 5 m
- **Flood-negative:** JRC occurrence < 5% AND HAND >= 30 m AND slope > 10 deg

### Step 4: ML Model Training (<30 min on laptop)

```bash
python scripts/04_ml_flood_susceptibility.py
```

**What it does:**
- Loads training samples CSV from Drive
- Trains 3 models: Random Forest, XGBoost, LightGBM
- Performs spatial 5-fold cross-validation (subregion-based folds)
- Computes SHAP feature importance
- Generates ensemble susceptibility map on GEE
- Exports municipal-level risk statistics

**Model Hyperparameters (from gee_config.py):**

| Model | n_estimators | max_depth | learning_rate | Other |
|-------|-------------|-----------|---------------|-------|
| Random Forest | 500 | 15 | — | min_samples_leaf=5 |
| XGBoost | 500 | 8 | 0.05 | subsample=0.8, colsample=0.8 |
| LightGBM | 500 | 8 | 0.05 | num_leaves=63 |

**Ensemble:** Weighted average proportional to each model's AUC-ROC:
```
w_k = AUC_k / sum(AUC_j)
```

**Outputs:**
- Trained models: `outputs/phase3_risk_model/*.joblib`
- Metrics: `model_metrics_summary.json`
- SHAP importance: `shap_importance_{model}.csv`
- Susceptibility map exported to GEE asset

### Step 5: Population Exposure (~1 hour)

```bash
python scripts/05_population_exposure.py
```

**What it does:**
- Overlays susceptibility map with WorldPop 2020 population
- Cross-tabulates land cover x risk class
- Computes per-municipality: % area per risk class, mean susceptibility
- Generates composite Flood Risk Index (FRI):
  ```
  FRI = 0.4 * pop_normalized + 0.3 * pct_high_area + 0.3 * mean_susceptibility
  ```
- Ranks all municipalities by FRI
- Computes temporal exposure 2015-2025

**Risk Class Thresholds:**

| Class | Probability Range |
|-------|-------------------|
| Very Low | 0.0 — 0.2 |
| Low | 0.2 — 0.4 |
| Moderate | 0.4 — 0.6 |
| High | 0.6 — 0.8 |
| Very High | 0.8 — 1.0 |

### Step 6: Climate Analysis (~1 hour)

```bash
python scripts/06_climate_analysis.py
```

**What it does:**
- Computes annual and seasonal precipitation trends (CHIRPS)
- Mann-Kendall trend test with Sen's slope estimator
- SPI-3, SPI-6, SPI-12 drought/wet indices
- Identifies extreme precipitation months (>95th percentile)
- Correlates precipitation with flood extent (Pearson, Spearman, 1-2 month lag)
- ENSO phase stratification and Kruskal-Wallis test

**ENSO Years (update for your study period):**

```python
# In 06_climate_analysis.py — MUST UPDATE for your study period
ENSO_YEARS = {
    'El Nino': [2015, 2016, 2023, 2024],
    'La Nina': [2020, 2021, 2022],
    'Neutral': [2017, 2018, 2019, 2025],
}
```

**Source for ENSO classification:** [NOAA ONI data](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php)

### Step 7: Visualization (~20 min)

```bash
python scripts/07_visualization.py
```

Generates 10-12 publication-quality figures (PDF + PNG at 600 DPI).

### Step 8: Tables (~5 min)

```bash
python scripts/08_generate_tables.py
```

Generates 7 tables as CSV and LaTeX (booktabs format).

### Step 9: Quality Control (~10 min)

```bash
python scripts/09_quality_control.py
```

Automated QC checks:
- All output files exist and are non-empty
- Area sums match expected department area (+-10%)
- Municipality count matches expected
- ML metrics in valid ranges (AUC >= 0.70, Kappa >= 0.60)
- SHAP values non-negative
- Population exposure <= total population per municipality
- Risk scores in [0, 1]

---

## 6. Parameter Reference

### Thresholds That May Need Adjustment by Region

| Parameter | Default | Adjust When | Location |
|-----------|---------|-------------|----------|
| `vv_default` | -15.0 dB | Different terrain/vegetation | `gee_config.py:132` |
| `vv_range` | (-20, -12) dB | Very wet or very arid regions | `gee_config.py:133` |
| `speckle_filter_radius` | 50 m | Higher noise in steep terrain | `gee_config.py:136` |
| `min_water_area_ha` | 1.0 ha | Smaller/larger water bodies needed | `gee_config.py:135` |
| Flood label JRC threshold | >= 25% | Drier regions with less flooding | `03:563` |
| Flood label HAND threshold | < 5 m | Different fluvial regimes | `03:563` |
| Non-flood HAND threshold | >= 30 m | Flatter terrain | `03:566` |
| Slope mask | > 30 deg | Steeper/flatter terrain | `01` |
| Risk class boundaries | 0.2 steps | Skewed susceptibility distribution | `05:726-732` |
| FRI weights | 0.4/0.3/0.3 | Different policy priorities | `05:461-465` |
| SAMPLES_PER_CLASS | 5,000 | Smaller study area (<10,000 km2) | `03:62` |

### Parameters That Should NOT Change

| Parameter | Value | Reason |
|-----------|-------|--------|
| S1 instrument mode | IW | Only mode with global coverage |
| S1 polarization | VV (primary) | Best for water detection |
| Otsu adaptive | True | Always preferred over fixed threshold |
| CV n_splits | 5 | Standard in spatial CV literature |
| Random state | 42 | Reproducibility |
| Export scale | 30 m | Matches DEM resolution |
| Figure DPI | 600 | Publication standard |

---

## 7. GEE Asset IDs (Global — No Changes Needed)

These datasets are globally available in GEE and require NO modification:

```python
S1_COLLECTION   = 'COPERNICUS/S1_GRD'
JRC_GSW         = 'JRC/GSW1_4/GlobalSurfaceWater'
JRC_GSW_MONTHLY = 'JRC/GSW1_4/MonthlyHistory'
JRC_GSW_YEARLY  = 'JRC/GSW1_4/YearlyHistory'
SRTM            = 'USGS/SRTMGL1_003'
MERIT_HYDRO     = 'MERIT/Hydro/v1_0_1'
CHIRPS          = 'UCSB-CHG/CHIRPS/DAILY'
ERA5_LAND       = 'ECMWF/ERA5_LAND/MONTHLY_AGGR'
MODIS_LST       = 'MODIS/061/MOD11A2'
WORLDPOP        = 'WorldPop/GP/100m/pop'
WORLDCOVER      = 'ESA/WorldCover/v200'
ADMIN_L1        = 'FAO/GAUL/2015/level1'
ADMIN_L2        = 'FAO/GAUL/2015/level2'
```

**Sentinel-2 (for NDVI):** `COPERNICUS/S2_SR_HARMONIZED`
**Friction surface (accessibility):** `projects/malariaatlasproject/assets/accessibility/friction_surface/2019_v5_1`

---

## 8. Department-Specific Data to Update

### Checklist for a New Department

- [ ] **`DEPARTMENT_NAME`** in `gee_config.py`
- [ ] **`SUBREGIONS`** dictionary with all municipalities
- [ ] **`MAP_CENTER`** (lat, lon) and **`MAP_ZOOM`**
- [ ] **`ENSO_YEARS`** in `06_climate_analysis.py` (if study period changes)
- [ ] **Export folder name** in all scripts (`sed` replace)
- [ ] **GEE asset ID** for susceptibility map in `05_population_exposure.py`
- [ ] **Expected area (km2)** in `09_quality_control.py`
- [ ] **Expected municipality count** in `09_quality_control.py`
- [ ] **SAR flood event coordinates** in `regenerate_all_figures_nature.py` (for Figure 2 example)
- [ ] **Spatial CV fold groupings** in `04_ml_flood_susceptibility.py` (group subregions into 5 folds)

### Colombian Departments — Quick Reference

| Department | Area (km2) | Municipalities | Capital | Flood-prone areas |
|------------|-----------|----------------|---------|-------------------|
| Antioquia | 63,612 | 125 | Medellin | Bajo Cauca, Uraba, Magdalena Medio |
| Valle del Cauca | 22,140 | 42 | Cali | Pacifico, Rio Cauca floodplain |
| Bolivar | 25,978 | 46 | Cartagena | Canal del Dique, Depresion Momposina |
| Choco | 46,530 | 30 | Quibdo | Atrato, San Juan basins |
| Magdalena | 23,188 | 30 | Santa Marta | Cienaga Grande, Rio Magdalena delta |
| Cesar | 22,905 | 25 | Valledupar | Rio Cesar, Cienaga de Zapatosa |
| Cordoba | 25,020 | 30 | Monteria | Rio Sinu, Cienaga de Ayapel |
| Sucre | 10,917 | 26 | Sincelejo | Mojana, San Jorge basin |
| Cauca | 29,308 | 42 | Popayan | Rio Cauca upper, Pacifico |
| Narino | 33,268 | 64 | Pasto | Pacifico, Rio Patia |

### Seasons (Adjust for Non-Colombian Regions)

Colombia's bimodal pattern (DJF dry, MAM wet, JJA dry, SON wet) applies to most of the Andean and Caribbean regions. Adjust `SEASONS` in `gee_config.py` if:

- **Pacific coast (Choco):** Near-continuous rainfall, no distinct dry season
- **Amazon/Orinoquia:** Unimodal (wet Apr-Nov, dry Dec-Mar)
- **Non-Colombian tropical regions:** Consult local climate data

```python
# Example for unimodal Amazon region:
SEASONS = {
    'Dry': {'months': [12, 1, 2, 3], 'label': 'Dry season'},
    'Transition1': {'months': [4, 5], 'label': 'Dry-wet transition'},
    'Wet': {'months': [6, 7, 8, 9], 'label': 'Wet season'},
    'Transition2': {'months': [10, 11], 'label': 'Wet-dry transition'},
}
```

---

## 9. Expected Outputs

### Directory Structure After Full Pipeline

```
outputs/
├── phase1_sar/
│   ├── annual_max_extent_2015-2025/    # 11 GeoTIFFs
│   └── water_frequency/                # 1 GeoTIFF
├── phase2_jrc/
│   ├── jrc_layers/                     # Occurrence, seasonality, etc.
│   ├── validation_metrics.csv
│   └── municipal_jrc_stats.csv
├── phase3_risk_model/
│   ├── flood_susceptibility_rf.joblib
│   ├── flood_susceptibility_xgb.joblib
│   ├── flood_susceptibility_lgbm.joblib
│   ├── model_metrics_summary.json
│   └── shap_importance_*.csv
├── phase4_exposure/
│   ├── population_exposure.csv
│   ├── area_exposure_by_landcover.csv
│   ├── municipal_risk_ranking.csv
│   └── temporal_exposure.csv
├── phase5_qc/
│   ├── qc_report.md
│   └── qc_summary.csv
├── figures/                            # 10-12 PDFs + PNGs
└── tables/                             # 7 CSVs + LaTeX files
```

### Key Metrics to Report

| Metric | Expected Range | If Outside Range |
|--------|---------------|------------------|
| AUC-ROC (ensemble) | 0.85 - 0.97 | Check label quality, feature engineering |
| Kappa (ensemble) | 0.65 - 0.90 | Check class balance, spatial CV folds |
| SAR-JRC Pearson r | 0.70 - 0.95 | Check SAR thresholds, cloud contamination |
| HAND SHAP rank | Top 1-3 | Expected; if low, check MERIT Hydro quality |
| Population exposed | 10-40% typical | Varies by geography; check threshold |

---

## 10. Troubleshooting

### GEE Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Computation timed out` | Area too large for single export | Split into tiles or reduce scale |
| `User memory limit exceeded` | Too many pixels in reduceRegion | Increase `scale` or use `bestEffort: True` |
| `No Sentinel-1 images found` | Wrong orbit pass for region | Try `ASCENDING` instead of `DESCENDING` |
| `Asset not found` | Wrong project ID in asset path | Update to your GEE project ID |
| `Quota exceeded` | Too many concurrent exports | Wait for tasks to finish, max ~20 concurrent |

### ML Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `NaN in features` | Missing data in some pixels | Check for NaN in training CSV, drop or impute |
| Low AUC (<0.80) | Poor label quality or features | Review labelling thresholds, check feature distributions |
| Overfitting (train>>test) | Random CV instead of spatial CV | Ensure spatial CV with subregion-based folds |
| SHAP error | Too many samples | Reduce `max_samples` to 1000-2000 |

### Common Issues

| Issue | Solution |
|-------|----------|
| No municipalities found in GAUL | Check exact spelling: `print(dept.aggregate_array('ADM2_NAME').getInfo())` |
| Subregion names don't match | GAUL uses ASCII names (no accents). Use `'Medellin'` not `'Medellín'` |
| Drive export stuck at 0% | Cancel and resubmit; check GEE quotas |
| Figures look wrong | Check `MAP_CENTER` and `MAP_ZOOM` for new department |
| Area validation fails | Update expected area in `09_quality_control.py` |

---

## 11. Estimated Computation Times

| Step | GEE Time | Local Time | Notes |
|------|----------|------------|-------|
| 01 SAR detection | ~4 hours | — | Depends on area size and S1 scene count |
| 02 JRC analysis | ~30 min | — | Mostly pre-computed by JRC |
| 03 Feature engineering | ~2 hours | — | 18 features at 30 m |
| 04 ML training | — | <30 min | On standard laptop (8-core) |
| 05 Population exposure | ~1 hour | 10 min | GEE zonal statistics |
| 06 Climate analysis | ~1 hour | 20 min | CHIRPS temporal aggregation |
| 07 Visualization | — | 20 min | Matplotlib rendering |
| 08 Tables | — | 5 min | CSV + LaTeX generation |
| 09 QC | — | 10 min | Automated checks |
| **Total** | **~8.5 hours** | **~1.5 hours** | **~10 hours end-to-end** |

For smaller departments (<20,000 km2), expect ~40% less GEE time.

---

## 12. Recommendations for Different Regions

### Flat Lowlands (e.g., Bolivar, Sucre, Cordoba)

- HAND threshold can be relaxed to <10 m (broader floodplains)
- Slope masking threshold can be lowered to 15 deg
- Drainage density radius can increase to 2 km
- Expect higher SAR accuracy (less terrain distortion)

### Mountainous Terrain (e.g., Narino, Cauca highlands)

- HAND threshold should stay strict (<5 m)
- Slope masking at 30 deg will exclude significant area; document this
- Consider dual-orbit (ASCENDING + DESCENDING) to reduce shadow/layover
- SAR accuracy will be lower in steep valleys (~60-70% detection)
- HAND and elevation will dominate SHAP even more strongly

### Coastal Regions (e.g., Choco Pacific, Uraba)

- Tidal influence may cause false water detections
- Consider adding tidal height as a feature
- JRC occurrence may overestimate flooding (tidal flats)
- Min water area threshold can increase to 2 ha to filter tidal noise

### Arid/Semi-arid Regions (e.g., La Guajira, parts of Cesar)

- Fewer flood events = fewer positive training samples
- Reduce SAMPLES_PER_CLASS to 2,000-3,000
- JRC flood threshold can be lowered to >= 10%
- Consider adding NDWI (Normalized Difference Water Index) as feature

### Non-Colombian Tropical Regions

- Update `COUNTRY_NAME` in config
- Use GADM v4.1 boundaries instead of FAO GAUL if better coverage
- WorldPop: filter by country code
- CHIRPS: available globally between 50N-50S
- Sentinel-1: check availability at [scihub.copernicus.eu](https://scihub.copernicus.eu/)
- ENSO years: same globally, but local impact varies

---

## 13. Quality Control Checklist

Before submitting results or manuscript, verify:

### Data Integrity
- [ ] Total area matches official department area (+-5%)
- [ ] Municipality count matches expected
- [ ] No duplicate municipalities in subregion assignments
- [ ] Training samples balanced (flood ~= non-flood count)
- [ ] No NaN values in final feature stack

### Model Quality
- [ ] AUC-ROC >= 0.85 under spatial CV
- [ ] Inter-fold AUC range < 0.10 (consistency)
- [ ] Confusion matrix: TP + FP + FN + TN = test set size
- [ ] F1 = 2*P*R / (P+R) matches reported value
- [ ] SHAP values sum to model output (within tolerance)
- [ ] Ablation experiment: model performs reasonably without SAR frequency

### Exposure Analysis
- [ ] Exposed population <= total population for every municipality
- [ ] Risk scores in [0, 1] range
- [ ] Area per risk class sums to total department area
- [ ] FRI ranking stable under threshold sensitivity (rho > 0.90)

### Figures
- [ ] All maps have scale bar, north arrow, coordinate labels
- [ ] Colorbars have units and labels
- [ ] Font sizes readable at publication size (>= 6pt)
- [ ] Color palettes are colorblind-safe
- [ ] No clipping or cropping of study area

### Manuscript
- [ ] All figures and tables referenced in text
- [ ] All citations in bibliography (zero orphans, zero missing)
- [ ] Numerical consistency across abstract, text, and tables
- [ ] Limitations section addresses SAR circularity
- [ ] Data availability statement includes GitHub URL

---

## 14. Publication Workflow

### 14.1 Manuscript Preparation

The `overleaf/` directory contains a LaTeX template in arXiv preprint format. To adapt:

1. Update title, authors, affiliations, ORCIDs
2. Replace "Antioquia" references with your department
3. Update all tables with your results
4. Replace figures in `overleaf/figures/`
5. Update `references.bib` (keep foundational references, add local ones)
6. Compile: `pdflatex main && bibtex main && pdflatex main && pdflatex main`

### 14.2 SSRN Submission (Recommended for First-Time Authors)

1. Go to [ssrn.com](https://www.ssrn.com/) > Submit a Paper
2. Upload the compiled PDF
3. Fill metadata:
   - **Title, Authors, Abstract** from manuscript
   - **Keywords:** flood susceptibility, Sentinel-1 SAR, ensemble machine learning, HAND, Google Earth Engine, [your department]
   - **Network:** Engineering (ERN) or Environmental Science
4. Research Integrity:
   - **Declaration of Interest:** "The authors declare no known competing financial interests or personal relationships that could have influenced this work."
   - **Funder:** "This research received no external funding. All data and computational resources are open-access (Google Earth Engine, Copernicus/ESA Sentinel-1)."
   - **Ethics:** "Not applicable. This study uses only publicly available satellite imagery and aggregated population datasets."
5. Submit — published in 1-3 business days with DOI

### 14.3 arXiv Submission

1. Prepare flat zip: `main.tex`, `main.bbl`, `arxiv.sty`, `figures/`
2. Replace `\bibliography{references}` with `\input{main.bbl}` in the zip's `main.tex`
3. Upload at [arxiv.org/submit](https://arxiv.org/submit)
4. Categories: `cs.LG`, `eess.IV`, or `stat.AP`
5. Requires endorsement from existing arXiv author in the chosen category

### 14.4 Journal Submission

Target journals for this type of research:

| Journal | IF (2024) | Turnaround | Notes |
|---------|-----------|------------|-------|
| *Remote Sensing of Environment* | 13.5 | 3-6 months | Top remote sensing journal |
| *Journal of Hydrology* | 6.4 | 2-4 months | Strong hydrology audience |
| *Natural Hazards and Earth System Sciences* | 4.6 | 3-5 months | Open access, EGU |
| *International Journal of Disaster Risk Reduction* | 4.2 | 2-4 months | Policy-oriented |
| *Remote Sensing (MDPI)* | 5.0 | 1-2 months | Fast turnaround, open access |
| *GIScience & Remote Sensing* | 6.0 | 2-3 months | Good for GEE-based studies |

---

## Quick Start: Replicate for Valle del Cauca in 5 Minutes

```bash
# 1. Clone
git clone https://github.com/Cespial/antioquia-flood-risk.git valle-flood-risk
cd valle-flood-risk

# 2. Configure
# Edit gee_config.py:
#   DEPARTMENT_NAME = 'Valle del Cauca'
#   MAP_CENTER = {'lat': 3.4, 'lon': -76.5}
#   SUBREGIONS = { ... }  # Define Valle del Cauca subregions

# 3. Replace export folder names
sed -i '' 's/antioquia_flood_risk/valle_flood_risk/g' scripts/*.py

# 4. Set credentials
echo "GEE_PROJECT_ID=ee-flood-risk-valle" > .env

# 5. Run pipeline
python scripts/01_sar_water_detection.py  # Wait ~3h
python scripts/02_jrc_water_analysis.py
python scripts/03_flood_susceptibility_features.py  # Wait ~1.5h
python scripts/04_ml_flood_susceptibility.py
python scripts/05_population_exposure.py
python scripts/06_climate_analysis.py
python scripts/07_visualization.py
python scripts/08_generate_tables.py
python scripts/09_quality_control.py
```

---

*Guide prepared for the research project "Municipality-Scale Flood Risk Mapping" — Universidad EAFIT, 2026.*
*Original framework: [github.com/Cespial/antioquia-flood-risk](https://github.com/Cespial/antioquia-flood-risk)*
