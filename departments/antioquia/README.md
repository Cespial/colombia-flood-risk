# Municipality-Scale Flood Risk Mapping in Antioquia, Colombia

**Using Sentinel-1 SAR and Ensemble Machine Learning (2015--2025)**

Cristian Espinal Maya [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--1009--8388-green)](https://orcid.org/0009-0000-1009-8388) · Santiago Jimenez Londono [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9862--7133-green)](https://orcid.org/0009-0007-9862-7133)

School of Applied Sciences and Engineering, Universidad EAFIT, Medellin, Colombia

[![SSRN](https://img.shields.io/badge/Preprint-SSRN-blue)](https://www.ssrn.com/) · [![License: MIT](https://img.shields.io/badge/Code-MIT-yellow)](LICENSE) · [![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

---

## Abstract

We present a reproducible, open-access framework that delivers municipality-level flood risk statistics for all 125 municipalities of the Department of Antioquia, Colombia (63,612 km²; 6.8 million inhabitants). We processed 4,762 Sentinel-1 C-band SAR scenes (2015–2025) within Google Earth Engine using adaptive Otsu thresholding to produce 132 monthly water extent maps at 10 m resolution. Eighteen predictor variables were integrated into a weighted ensemble of Random Forest, XGBoost, and LightGBM, achieving **AUC-ROC = 0.94 ± 0.02** under spatial five-fold cross-validation. HAND, SAR flood frequency, and elevation were identified as dominant predictors via SHAP analysis. Overlaying the susceptibility surface with 100 m population data reveals that **1.47 million people (21.5%)** reside in high or very high susceptibility zones. La Nina years amplify mean flood extent by 34% relative to El Nino years (*p* < 0.001).

## Repository Structure

```
.
├── overleaf/                  # Manuscript (preprint format)
│   ├── main.tex               # Main LaTeX source
│   ├── arxiv.sty              # Preprint style file
│   ├── references.bib         # Bibliography (34 references)
│   └── figures/               # All figure PDFs (10 figures)
├── scripts/                   # Processing and analysis pipeline
│   ├── 01_sar_water_detection.py
│   ├── 02_jrc_water_analysis.py
│   ├── 03_flood_susceptibility_features.py
│   ├── 04_ml_flood_susceptibility.py
│   ├── 05_population_exposure.py
│   ├── 06_climate_analysis.py
│   ├── 07_visualization.py
│   ├── 08_generate_tables.py
│   ├── 09_quality_control.py
│   └── regenerate_all_figures_nature.py
├── arxiv_submission.zip       # Ready-to-upload submission package
└── README.md
```

## Key Results

| Metric | Value |
|--------|-------|
| Sentinel-1 scenes processed | 4,762 |
| Study area | 63,612 km² (125 municipalities) |
| Monthly composites | 132 (2015–2025) |
| Ensemble AUC-ROC | 0.94 ± 0.02 |
| Top predictor (SHAP) | HAND (0.182) |
| Population exposed (high/very high) | 1.47 million (21.5%) |
| La Nina flood amplification | +34% vs El Nino |

## Data Sources

All data are open-access and processed via [Google Earth Engine](https://earthengine.google.com/):

- **Sentinel-1 GRD** (ESA/Copernicus) — 10 m SAR flood detection
- **JRC Global Surface Water** — 38-year water dynamics
- **SRTM DEM v3** — Topographic features (30 m)
- **MERIT Hydro** — HAND computation (90 m)
- **CHIRPS / ERA5-Land** — Precipitation and soil moisture
- **ESA WorldCover / Sentinel-2** — Land cover and NDVI
- **WorldPop** — Population density (100 m)
- **GADM v4.1** — Administrative boundaries

## Reproducing the Analysis

### Requirements

- Python 3.10+
- Google Earth Engine account ([sign up](https://signup.earthengine.google.com/))
- Libraries: `earthengine-api`, `scikit-learn`, `xgboost`, `lightgbm`, `shap`, `matplotlib`, `geopandas`

### Pipeline

```bash
# 1. SAR water detection (runs on GEE)
python scripts/01_sar_water_detection.py

# 2. JRC validation analysis
python scripts/02_jrc_water_analysis.py

# 3. Feature engineering
python scripts/03_flood_susceptibility_features.py

# 4. ML model training and evaluation
python scripts/04_ml_flood_susceptibility.py

# 5. Population exposure analysis
python scripts/05_population_exposure.py

# 6. ENSO and seasonal analysis
python scripts/06_climate_analysis.py

# 7. Generate all figures
python scripts/07_visualization.py
```

## Citation

If you use this work, please cite:

```bibtex
@article{EspinalMaya2026,
  author  = {Espinal Maya, Cristian and Jim\'enez Londo\~no, Santiago},
  title   = {Municipality-Scale Flood Risk Mapping in {Antioquia}, {Colombia},
             Using {Sentinel-1} {SAR} and Ensemble Machine Learning (2015--2025)},
  year    = {2026},
  note    = {Available at SSRN}
}
```

## License

Source code: [MIT License](LICENSE). Manuscript and figures: CC BY 4.0.
