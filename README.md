# Municipality-Scale Flood Risk Mapping in Colombia

**Using Sentinel-1 SAR and Ensemble Machine Learning (2015–2025)**

Cristian Espinal Maya [![ORCID](https://img.shields.io/badge/ORCID-0009--0000--1009--8388-green)](https://orcid.org/0009-0000-1009-8388) · Santiago Jimenez Londono [![ORCID](https://img.shields.io/badge/ORCID-0009--0007--9862--7133-green)](https://orcid.org/0009-0007-9862-7133)

School of Applied Sciences and Engineering, Universidad EAFIT, Medellin, Colombia

[![License: MIT](https://img.shields.io/badge/Code-MIT-yellow)](LICENSE) · [![License: CC BY 4.0](https://img.shields.io/badge/Manuscript-CC%20BY%204.0-lightgrey)](https://creativecommons.org/licenses/by/4.0/)

---

## Overview

A reproducible, open-access framework that delivers municipality-level flood risk statistics across multiple departments of Colombia. Each department study processes Sentinel-1 C-band SAR scenes (2015–2025) within Google Earth Engine using adaptive Otsu thresholding, then integrates predictor variables into a weighted ensemble of Random Forest, XGBoost, and LightGBM.

## Departments

| Department | Municipalities | Study Area | Ensemble AUC-ROC | Subdirectory |
|---|---|---|---|---|
| Antioquia | 125 | 63,612 km² | 0.94 ± 0.02 | [`departments/antioquia`](departments/antioquia) |
| Bolívar | 46 | 25,978 km² | — | [`departments/bolivar`](departments/bolivar) |
| Cauca | 42 | 29,308 km² | — | [`departments/cauca`](departments/cauca) |
| Chocó | 30 | 46,530 km² | — | [`departments/choco`](departments/choco) |
| Guajira | 15 | 20,848 km² | — | [`departments/guajira`](departments/guajira) |
| Magdalena | 30 | 23,188 km² | — | [`departments/magdalena`](departments/magdalena) |
| Nariño | 64 | 33,268 km² | — | [`departments/narino`](departments/narino) |
| **Total** | **352** | **242,732 km²** | | |

> Guajira includes a specialized **Sand Exclusion Layer** for arid/semi-arid terrain adaptation.

## Repository Structure

```
colombia-flood-risk/
├── README.md
├── departments/
│   ├── antioquia/          # Full pipeline + manuscript
│   ├── bolivar/            # Full pipeline + manuscript
│   ├── cauca/              # Full pipeline + manuscript
│   ├── choco/              # Full pipeline + manuscript
│   ├── guajira/            # Full pipeline + manuscript (arid adaptation)
│   ├── magdalena/          # Full pipeline + manuscript
│   └── narino/             # Full pipeline + manuscript
```

Each department subdirectory contains:
- `scripts/` — Processing and analysis pipeline (SAR water detection, ML susceptibility, population exposure, climate analysis)
- `overleaf/` — Manuscript in LaTeX (preprint format)
- `gee_config.py` — Google Earth Engine configuration
- `requirements.txt` — Python dependencies
- `README.md` — Department-specific results and metrics

## Methodology

1. **SAR Water Detection** — Sentinel-1 scenes processed with adaptive Otsu thresholding → monthly water extent composites at 10 m resolution
2. **Feature Engineering** — 18 predictor variables (HAND, elevation, slope, SAR flood frequency, land cover, population density, etc.)
3. **Ensemble ML** — Weighted ensemble of Random Forest, XGBoost, and LightGBM with spatial five-fold cross-validation
4. **Population Exposure** — Susceptibility surface overlaid with 100 m population data
5. **Climate Analysis** — ENSO influence on flood extent (La Nina vs El Nino)

## Citation

If you use this work, please cite the corresponding department preprint. See each subdirectory's README for specific citation details.
