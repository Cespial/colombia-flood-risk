# Municipality-Scale Flood Risk Mapping in Cauca, Colombia

**Using Sentinel-1 SAR and Ensemble Machine Learning (2015--2025)**

Cristian Espinal Maya [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--1009--8388-green)](https://orcid.org/0009-0000-1009-8388) · Santiago Jimenez Londono [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9862--7133-green)](https://orcid.org/0009-0007-9862-7133)

School of Applied Sciences and Engineering, Universidad EAFIT, Medellin, Colombia

[![SSRN](https://img.shields.io/badge/Preprint-SSRN-blue)](https://www.ssrn.com/) · [![License: MIT](https://img.shields.io/badge/Code-MIT-yellow)](LICENSE) · [![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

---

## Abstract

We replicate and extend the Antioquia flood risk framework to deliver municipality-level flood risk statistics for all **42 municipalities** of the Department of Cauca, Colombia (**29,308 km2; ~1.6 million inhabitants**). The department presents unique challenges including extreme topographic diversity (0–4,700 m a.s.l.), one of Earth's wettest regions on its Pacific coast (>13,000 mm/yr at Lopez de Micay), the Salvajina Dam's influence on the upper Cauca River regime, and cascading volcanic-seismic-flood hazards. We process Sentinel-1 C-band SAR scenes (2015–2025) within Google Earth Engine using adaptive Otsu thresholding to produce monthly water extent maps at 10 m resolution. Eighteen predictor variables are integrated into a weighted ensemble of Random Forest, XGBoost, and LightGBM under spatial five-fold cross-validation. SHAP analysis identifies dominant predictors. The susceptibility surface is overlaid with 100 m WorldPop population data to quantify exposure by municipality.

## Study Area Highlights

| Feature | Description |
|---------|-------------|
| **Department** | Cauca, Colombia |
| **Area** | 29,308 km2 (42 municipalities, 7 subregions) |
| **Capital** | Popayan (1,728 m a.s.l.) |
| **Elevation range** | 0 m (Pacific coast) to ~4,700 m (Purace volcano) |
| **Major basins** | Alto Cauca, Patia, Pacific, Alto Magdalena, Caqueta |
| **Key infrastructure** | Salvajina Dam (1985, 270 MW) |
| **Climate** | Bimodal Andean interior + continuous Pacific rainfall |
| **Flood-prone zones** | Northern Cauca valley, Pacific coast, Popayan urban area |

## Repository Structure

```
.
├── gee_config.py              # Central configuration (Cauca-specific)
├── scripts/                   # Processing and analysis pipeline
│   ├── 01_sar_water_detection.py
│   ├── 02_jrc_water_analysis.py
│   ├── 03_flood_susceptibility_features.py
│   ├── 04_ml_flood_susceptibility.py
│   ├── 05_population_exposure.py
│   ├── 06_climate_analysis.py
│   ├── 07_visualization.py
│   ├── 08_generate_tables.py
│   └── 09_quality_control.py
├── overleaf/                  # Manuscript (preprint format)
│   ├── main.tex
│   ├── arxiv.sty
│   ├── references.bib
│   └── figures/
├── LITERATURE_REVIEW.md       # Bibliographic research for Cauca
├── REPLICATION_GUIDE.md       # Step-by-step replication notes
├── data/                      # Downloaded data (auto-created)
├── outputs/                   # Results (auto-created)
│   ├── phase1_sar/
│   ├── phase2_jrc/
│   ├── phase3_risk_model/
│   ├── phase4_exposure/
│   ├── phase5_qc/
│   ├── figures/
│   └── tables/
├── logs/                      # Processing logs
└── .env                       # GEE credentials
```

## Data Sources

All data are open-access and processed via [Google Earth Engine](https://earthengine.google.com/):

- **Sentinel-1 GRD** (ESA/Copernicus) — 10 m SAR flood detection
- **JRC Global Surface Water** — 38-year water dynamics
- **SRTM DEM v3** — Topographic features (30 m)
- **MERIT Hydro** — HAND computation (90 m)
- **CHIRPS / ERA5-Land** — Precipitation and soil moisture
- **ESA WorldCover / Sentinel-2** — Land cover and NDVI
- **WorldPop** — Population density (100 m)
- **FAO GAUL** — Administrative boundaries

## Special Considerations for Cauca

1. **Mixed terrain:** Andes + Pacific lowlands require multi-scale flood mapping
2. **Pacific coast:** Continuous rainfall (no dry baseline for SAR change detection), tidal influence, mangrove backscatter
3. **Salvajina Dam:** Reservoir masked as permanent water; altered downstream flood regime
4. **Volcanic influence:** Purace and Sotara volcanoes create lahar hazards
5. **Steep valleys:** Dual-orbit SAR (ascending + descending) recommended to reduce shadow/layover
6. **Ethnic vulnerability:** Significant indigenous and Afro-Colombian communities in flood-prone areas

## Reproducing the Analysis

### Requirements

- Python 3.10+
- Google Earth Engine account ([sign up](https://signup.earthengine.google.com/))
- Libraries: `earthengine-api`, `scikit-learn`, `xgboost`, `lightgbm`, `shap`, `matplotlib`, `geopandas`

### Pipeline

```bash
# 1. SAR water detection (runs on GEE, ~3h for 29,308 km2)
python scripts/01_sar_water_detection.py

# 2. JRC validation analysis
python scripts/02_jrc_water_analysis.py

# 3. Feature engineering (18 predictors)
python scripts/03_flood_susceptibility_features.py

# 4. ML model training and evaluation
python scripts/04_ml_flood_susceptibility.py

# 5. Population exposure analysis
python scripts/05_population_exposure.py

# 6. ENSO and seasonal analysis
python scripts/06_climate_analysis.py

# 7. Generate all figures
python scripts/07_visualization.py

# 8. Generate tables (CSV + LaTeX)
python scripts/08_generate_tables.py

# 9. Quality control checks
python scripts/09_quality_control.py
```

## Replicated From

This project replicates the methodology from:

> Espinal Maya, C. & Jimenez Londono, S. (2026). "Municipality-Scale Flood Risk Mapping in Antioquia, Colombia, Using Sentinel-1 SAR and Ensemble Machine Learning (2015–2025)."

Original repository: [github.com/Cespial/antioquia-flood-risk](https://github.com/Cespial/antioquia-flood-risk)

## Citation

```bibtex
@article{EspinalMaya2026Cauca,
  author  = {Espinal Maya, Cristian and Jim\'enez Londo\~no, Santiago},
  title   = {Municipality-Scale Flood Risk Mapping in {Cauca}, {Colombia},
             Using {Sentinel-1} {SAR} and Ensemble Machine Learning (2015--2025)},
  year    = {2026},
  note    = {Available at SSRN}
}
```

## License

Source code: [MIT License](LICENSE). Manuscript and figures: CC BY 4.0.
