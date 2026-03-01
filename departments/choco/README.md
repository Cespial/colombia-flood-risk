# Municipality-Scale Flood Risk Mapping in Choco, Colombia

**Using Sentinel-1 SAR and Ensemble Machine Learning (2015--2025)**

Cristian Espinal Maya [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--1009--8388-green)](https://orcid.org/0009-0000-1009-8388) · Santiago Jimenez Londono [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9862--7133-green)](https://orcid.org/0009-0007-9862-7133)

School of Applied Sciences and Engineering, Universidad EAFIT, Medellin, Colombia

[![License: MIT](https://img.shields.io/badge/Code-MIT-yellow)](LICENSE) · [![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

---

## Abstract

The Department of Choco, one of the rainiest and most flood-affected regions on Earth (5,000-13,000 mm/yr), lacks spatially explicit flood risk information at the municipal scale. We present an open-access, reproducible framework that delivers municipality-level flood risk statistics for all 30 municipalities of Choco, Colombia (46,530 km²; ~600,000 inhabitants). Using Sentinel-1 SAR, Google Earth Engine, and an ensemble of Random Forest, XGBoost, and LightGBM, the framework maps flood susceptibility and quantifies population exposure across Choco's predominantly Afro-Colombian and Indigenous communities.

This study extends the [Antioquia flood risk framework](https://github.com/Cespial/antioquia-flood-risk) to Choco's hyper-humid tropical environment, addressing unique challenges including dense tropical forest cover (>85%), extreme precipitation driven by the Choco Low-Level Jet, and limited SAR canopy penetration at C-band.

## Repository Structure

```
.
├── gee_config.py              # Central configuration (Choco-adapted)
├── overleaf/                  # Manuscript (preprint format)
│   ├── main.tex               # Main LaTeX source
│   ├── arxiv.sty              # Preprint style file
│   ├── references.bib         # Bibliography
│   └── figures/               # Figure PDFs
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

## Study Area

| Feature | Value |
|---------|-------|
| Department | Choco, Colombia |
| Area | 46,530 km² |
| Municipalities | 30 |
| Subregions | 5 (Atrato, Darien, San Juan, Pacifico Norte, Pacifico Sur) |
| Population | ~600,000 |
| Capital | Quibdo |
| Major rivers | Atrato (~4,900 m³/s), San Juan (~2,550 m³/s), Baudo |
| Annual precipitation | 5,000 - 13,000+ mm/yr |
| Climate driver | Choco Low-Level Jet (ChocoJet) |

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

## Pipeline

```bash
python scripts/01_sar_water_detection.py       # SAR water detection (~4h on GEE)
python scripts/02_jrc_water_analysis.py         # JRC validation
python scripts/03_flood_susceptibility_features.py  # 18 predictor features (~2h)
python scripts/04_ml_flood_susceptibility.py    # ML training + SHAP (<30min)
python scripts/05_population_exposure.py        # Population exposure
python scripts/06_climate_analysis.py           # ENSO + seasonal analysis
python scripts/07_visualization.py              # Generate figures
python scripts/08_generate_tables.py            # Generate tables
python scripts/09_quality_control.py            # QC checks
```

## Related Work

This study extends the methodology from:

> Espinal Maya, C. & Jimenez Londono, S. (2026). Municipality-Scale Flood Risk Mapping in Antioquia, Colombia, Using Sentinel-1 SAR and Ensemble Machine Learning (2015-2025). Available at SSRN. [GitHub](https://github.com/Cespial/antioquia-flood-risk)

## Citation

```bibtex
@article{EspinalMaya2026Choco,
  author  = {Espinal Maya, Cristian and Jim\'enez Londo\~no, Santiago},
  title   = {Municipality-Scale Flood Risk Mapping in {Choc\'o}, {Colombia},
             Using {Sentinel-1} {SAR} and Ensemble Machine Learning (2015--2025)},
  year    = {2026},
  note    = {Preprint}
}
```

## License

Source code: [MIT License](LICENSE). Manuscript and figures: CC BY 4.0.
