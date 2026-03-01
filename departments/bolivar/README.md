# Municipality-Scale Flood Risk Mapping in Bolivar, Colombia

**Using Sentinel-1 SAR and Ensemble Machine Learning (2015--2025)**

Cristian Espinal Maya [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--1009--8388-green)](https://orcid.org/0009-0000-1009-8388) · Santiago Jimenez Londono [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9862--7133-green)](https://orcid.org/0009-0007-9862-7133)

School of Applied Sciences and Engineering, Universidad EAFIT, Medellin, Colombia

[![SSRN](https://img.shields.io/badge/Preprint-SSRN-blue)](https://www.ssrn.com/) · [![License: MIT](https://img.shields.io/badge/Code-MIT-yellow)](LICENSE) · [![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

---

## Abstract

We present a reproducible, open-access framework that delivers municipality-level flood risk statistics for all 46 municipalities of the Department of Bolivar, Colombia (25,978 km²; ~2.2 million inhabitants). Bolivar encompasses some of Colombia's most flood-vulnerable landscapes: the Depresion Momposina (~3,400 km² of wetlands at the confluence of the Magdalena, Cauca, and San Jorge rivers), the Canal del Dique corridor, and the La Mojana wetland system. We process Sentinel-1 C-band SAR scenes (2015-2025) within Google Earth Engine using adaptive Otsu thresholding to produce monthly water extent maps at 10 m resolution. Eighteen predictor variables are integrated into a weighted ensemble of Random Forest, XGBoost, and LightGBM. The susceptibility surface is overlaid with 100 m population data to quantify exposure per municipality and risk class.

## Study Area Context

Bolivar is one of Colombia's most flood-affected departments, with predominantly flat lowland terrain that facilitates extensive lateral flooding:

- **Depresion Momposina**: Internal delta where the Magdalena, Cauca, San Jorge, and Cesar rivers converge; floods reach up to 7 m depth seasonally
- **Canal del Dique**: 115 km man-made distributary from Calamar to the Bay of Cartagena; catastrophic breach during 2010-2011 La Nina flooded 35,000 ha
- **La Mojana**: Trans-departmental wetland system; recurring dam failures (Cara de Gato) affect thousands
- **2010-2011 La Nina**: Bolivar was the most affected department nationally (~60,000 households impacted)

## Repository Structure

```
.
├── overleaf/                  # Manuscript (preprint format)
│   ├── main.tex               # Main LaTeX source
│   ├── arxiv.sty              # Preprint style file
│   ├── references.bib         # Bibliography
│   └── figures/               # All figure PDFs
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
└── README.md
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

## Reproducing the Analysis

### Requirements

- Python 3.10+
- Google Earth Engine account ([sign up](https://signup.earthengine.google.com/))
- Libraries: `earthengine-api`, `scikit-learn`, `xgboost`, `lightgbm`, `shap`, `matplotlib`, `geopandas`

### Setup

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Authenticate with GEE
earthengine authenticate
```

### Pipeline

```bash
# 1. SAR water detection (runs on GEE, ~3h for Bolivar)
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

# 8. Generate tables
python scripts/08_generate_tables.py

# 9. Quality control
python scripts/09_quality_control.py
```

## Methodological Adaptations for Bolivar

Compared to the original Antioquia framework, the following parameters were adjusted for Bolivar's flat lowland terrain:

| Parameter | Antioquia | Bolivar | Rationale |
|-----------|-----------|---------|-----------|
| HAND flood threshold | < 5 m | < 10 m | Broader floodplains, lower relief |
| HAND non-flood threshold | >= 30 m | >= 40 m | Higher separation needed in flat areas |
| Slope non-flood threshold | > 10 deg | > 5 deg | Most terrain below 5 deg slope |
| Min water area | 1.0 ha | 2.0 ha | Filter tidal noise near coast |
| HAND class boundaries | 0-5-15-30-60 | 0-10-20-40-70 | Relaxed for flat topography |
| Drainage density radius | 1 km | 2 km | Wider floodplain networks |

## Special Considerations

1. **Cienagas**: Seasonal wetlands that expand/contract require multi-temporal SAR compositing
2. **Tidal influence**: Microtidal regime near Cartagena; min_water_area filter mitigates false detections
3. **Vegetation-water interaction**: Flooded forest/palm in Momposina may cause double-bounce scattering
4. **Permanent vs seasonal water**: JRC baseline masking essential for flood change detection

## Key References

- Angarita, H. et al. (2018). Basin-scale impacts of hydropower development on the Mompos Depression wetlands, Colombia. *HESS*, 22, 2839-2865.
- Hoyos, N. et al. (2013). Impact of the 2010-2011 La Nina phenomenon in Colombia. *Applied Geography*, 39, 16-25.
- Urrea, V. et al. (2019). Seasonality of Rainfall in Colombia. *Water Resources Research*, 55(5).
- Pekel, J.-F. et al. (2016). High-resolution mapping of global surface water. *Nature*, 540, 418-422.

## Citation

If you use this work, please cite:

```bibtex
@article{EspinalMaya2026bolivar,
  author  = {Espinal Maya, Cristian and Jim\'enez Londo\~no, Santiago},
  title   = {Municipality-Scale Flood Risk Mapping in {Bol\'ivar}, {Colombia},
             Using {Sentinel-1} {SAR} and Ensemble Machine Learning (2015--2025)},
  year    = {2026},
  note    = {Available at SSRN}
}
```

## License

Source code: [MIT License](LICENSE). Manuscript and figures: CC BY 4.0.
