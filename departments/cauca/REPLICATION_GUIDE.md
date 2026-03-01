# Replication Guide: Cauca Department — Flood Risk Mapping

**Adaptations and notes for replicating the Antioquia framework to the Department of Cauca**

Cristian Espinal Maya & Santiago Jimenez Londono — Universidad EAFIT, 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Key Differences: Antioquia vs Cauca](#2-key-differences-antioquia-vs-cauca)
3. [Configuration Changes Made](#3-configuration-changes-made)
4. [Terrain-Specific Adaptations](#4-terrain-specific-adaptations)
5. [Pipeline Notes by Step](#5-pipeline-notes-by-step)
6. [Salvajina Dam Handling](#6-salvajina-dam-handling)
7. [Pacific Coast Considerations](#7-pacific-coast-considerations)
8. [Spatial CV Fold Design](#8-spatial-cv-fold-design)
9. [Expected Computation Times](#9-expected-computation-times)
10. [Quality Control Adjustments](#10-quality-control-adjustments)
11. [Known Challenges](#11-known-challenges)

---

## 1. Overview

This project replicates the Antioquia municipality-scale flood risk mapping framework for the **Department of Cauca**. The original methodology, full pipeline documentation, and general replication instructions are in the Antioquia project's `REPLICATION_GUIDE.md`.

This document focuses on **Cauca-specific adaptations** and considerations.

---

## 2. Key Differences: Antioquia vs Cauca

| Attribute | Antioquia | Cauca |
|-----------|-----------|-------|
| Area | 63,612 km2 | 29,308 km2 (~46% of Antioquia) |
| Municipalities | 125 | 42 |
| Subregions | 9 | 7 |
| Capital | Medellin (1,495 m) | Popayan (1,728 m) |
| Population | ~6.8 million | ~1.6 million |
| Elevation range | 0-3,300 m | 0-4,700 m (more extreme) |
| Major rivers | Cauca (middle), Magdalena | Cauca (upper), Patia, Pacific rivers |
| Pacific coast | Yes (Uraba) | Yes (Guapi, Timbiqui, Lopez de Micay) |
| Key infrastructure | None (dams upstream) | Salvajina Dam (on Cauca River) |
| Volcanic features | None | Purace (4,650 m), Sotara (4,580 m) |
| Max rainfall | ~4,000 mm/yr (Uraba) | >13,000 mm/yr (Lopez de Micay) |
| Rural population | ~20% | ~65% (much higher vulnerability) |
| Flood mechanisms | Fluvial, flash floods | Fluvial, flash, tidal, lahar, cascading |

### Key Implications

1. **Smaller area** = faster GEE processing (~40% less time)
2. **More extreme topography** = greater SAR limitations in steep valleys
3. **Salvajina Dam** = must mask reservoir as permanent water
4. **Pacific coast extreme rainfall** = SAR change detection challenging (no dry baseline)
5. **Higher rural population** = exposure analysis has different characteristics
6. **Fewer municipalities** = smaller training sample pool per subregion

---

## 3. Configuration Changes Made

All changes are in `gee_config.py`. The following parameters were modified from the Antioquia version:

```python
# Study area
DEPARTMENT_NAME = 'Cauca'           # was 'Antioquia'
EXPECTED_MUNICIPALITY_COUNT = 42    # was 125
EXPECTED_AREA_KM2 = 29308          # was 63612

# Subregions: 7 subregions with 42 municipalities (see gee_config.py)

# Map center
MAP_CENTER = {'lat': 2.3, 'lon': -76.6}  # was {'lat': 6.9, 'lon': -75.6}
MAP_ZOOM = 9                               # was 8 (slightly more zoom for smaller area)

# Subregion palette: 7 colors instead of 9

# GEE project
GEE_PROJECT_ID = 'ee-flood-risk-cauca'

# Export folder
DRIVE_EXPORT_FOLDER = 'cauca_flood_risk'   # was 'antioquia_flood_risk'

# GEE asset path
GEE_SUSCEPTIBILITY_ASSET = 'projects/ee-flood-risk-cauca/assets/cauca_flood_susceptibility_ensemble'
```

### Additional Cauca-specific config added:

- `SALVAJINA_DAM` dictionary with coordinates and metadata
- `HIGH_FLOOD_RISK_MUNICIPALITIES` list for prioritized analysis
- `VOLCANIC_FEATURES` dictionary for Purace and Sotara
- `CV_FOLD_GROUPS` for 7 subregions into 5 folds
- `FRI_WEIGHTS` and `RISK_CLASSES` made explicit
- `ENSO_YEARS` classification

---

## 4. Terrain-Specific Adaptations

### 4.1 Mountainous Terrain (Oriente, Macizo, Centro, Bota Caucana)

These subregions have steep terrain (Central and Western Cordillera, Colombian Massif):

- **HAND threshold:** Keep strict at <5 m (narrow floodplains)
- **Slope masking:** 30 deg will exclude significant area — document this limitation
- **SAR:** Consider dual-orbit (ASCENDING + DESCENDING) to reduce shadow/layover
- **Expected SAR accuracy:** ~60-70% in steep valleys
- **HAND and elevation will dominate SHAP rankings even more than in Antioquia**

### 4.2 Flat Cauca Valley (Norte subregion)

The flat valley north of Popayan resembles Antioquia's Bajo Cauca:

- **HAND threshold:** Can potentially relax to <10 m (broader floodplains)
- **Drainage density:** Consider increasing focal radius to 2 km
- **SAR accuracy:** Expected to be higher (less terrain distortion)
- **This subregion will likely contain the most flood-positive training samples**

### 4.3 Pacific Coast (Pacifico subregion)

See [Section 7](#7-pacific-coast-considerations) for detailed notes.

### 4.4 Amazonian Piedmont (Bota Caucana)

- Transitional terrain from Andes to Amazon lowlands
- Unimodal rainfall pattern (wetter Apr-Nov)
- Small area (3 municipalities) — may have limited training samples
- Consider grouping with Macizo for spatial CV

---

## 5. Pipeline Notes by Step

### Step 1: SAR Water Detection

```bash
python scripts/01_sar_water_detection.py
```

**Cauca-specific notes:**
- Expected ~2,500-3,000 Sentinel-1 scenes (vs 4,762 for Antioquia)
- **Salvajina Dam reservoir must be masked** before water frequency computation
- Pacific coast municipalities may need `min_water_area_ha = 2.0` to filter tidal noise
- Check both ASCENDING and DESCENDING passes for optimal coverage
- Monitor for persistent cloud contamination in Pacific coast SAR data

### Step 2: JRC Water Analysis

No major modifications needed. JRC data is global and pre-computed.

### Step 3: Feature Engineering

**Training label considerations:**
- **Flood-positive:** JRC occurrence >= 25% OR HAND < 5 m (same as Antioquia)
- **Flood-negative:** JRC occurrence < 5% AND HAND >= 30 m AND slope > 10 deg
- **SAMPLES_PER_CLASS = 5,000** — may need to reduce to 3,000-4,000 if quality is low due to smaller area
- Ensure stratification by subregion maintains adequate representation from all 7 subregions

### Step 4: ML Model Training

**Spatial CV fold groupings for 7 subregions:**

| Fold | Subregions | Rationale |
|------|-----------|-----------|
| 0 | Centro | Central highlands around Popayan |
| 1 | Norte | Flat Cauca valley (distinct terrain) |
| 2 | Pacifico + Sur | Pacific/southern (extreme rainfall + Patia basin) |
| 3 | Oriente + Macizo | Eastern mountains + Colombian Massif |
| 4 | Bota Caucana | Amazonian piedmont (distinct terrain) |

**Potential issue:** Fold 4 (Bota Caucana) has only 3 municipalities and may have too few training samples. Monitor fold-specific AUC for imbalance.

### Step 5: Population Exposure

- Total population ~1.6 million (vs 6.8 million for Antioquia)
- 65% rural population means exposure patterns will differ significantly
- Indigenous and Afro-Colombian communities in flood-prone areas add equity dimension
- Salvajina Dam displacement (2,124 ha) is a relevant historical context

### Step 6: Climate Analysis

- ENSO years are identical (global phenomenon)
- Pacific coast rainfall should be analyzed separately from Andean interior
- Consider noting that bimodal seasonality applies to ~85% of department area
- The Pacifico subregion is effectively aseasonal

### Step 7-9: Visualization, Tables, QC

- Update expected municipality count to 42
- Update expected area to 29,308 km2
- Adjust figure coordinates and zoom level
- 7 subregion colors instead of 9

---

## 6. Salvajina Dam Handling

The Salvajina Dam (1985) on the Cauca River in Suarez municipality requires special treatment:

### In SAR Analysis (Step 1)

```python
# Mask Salvajina reservoir as permanent water
# Use JRC occurrence >= 90% AND known dam coordinates to define mask
salvajina_point = ee.Geometry.Point(-76.68, 2.95)
# Buffer ~5 km radius to capture full reservoir extent
salvajina_buffer = salvajina_point.buffer(5000)
```

### In Feature Engineering (Step 3)

- Reservoir pixels should be labeled as permanent water, NOT flood-positive
- This prevents the model from learning reservoir backwater as "flooding"

### In Results Interpretation

- Post-1985 flood regime is fundamentally different from pre-dam conditions
- The dam reduced flood peak flows but La Nina events can still overwhelm
- The 2010-2011 La Nina caused flooding despite dam regulation

---

## 7. Pacific Coast Considerations

The Pacifico subregion (Guapi, Timbiqui, Lopez de Micay) presents the greatest methodological challenge:

### 7.1 Extreme Rainfall

- Annual precipitation: 5,000-13,000 mm/yr
- No distinct dry season — the landscape is almost permanently saturated
- This means SAR change detection (wet vs dry) is less effective
- **Recommendation:** Weight JRC occurrence more heavily for training labels in this subregion

### 7.2 SAR Limitations

- Mangrove forests create high SAR backscatter similar to non-water surfaces
- Tidal influence causes daily water level variations
- Consider increasing `min_water_area_ha` to 2.0 ha for Pacific coast pixels
- SAR-JRC validation may show lower agreement in this subregion

### 7.3 Optical Data Unavailability

- Near-permanent cloud cover renders Sentinel-2/Landsat unusable most of the year
- NDVI feature will have high uncertainty — consider documenting this
- SAR is the only viable remote sensing option

### 7.4 Practical Recommendation

Consider running the analysis in two phases:
1. **Andean Cauca** (6 subregions, ~85% of area) — standard methodology
2. **Pacific Cauca** (1 subregion, ~15% of area) — adapted thresholds

Or, treat the Pacific subregion results with additional caveats in the manuscript.

---

## 8. Spatial CV Fold Design

### Rationale

Cauca has 7 subregions vs Antioquia's 9. To maintain 5-fold CV:

| Fold | Subregions | Approx. Area (km2) | Key Terrain |
|------|-----------|-------------------|-------------|
| 0 | Centro | ~5,500 | Andean highlands |
| 1 | Norte | ~4,200 | Flat Cauca valley |
| 2 | Pacifico + Sur | ~9,000 | Pacific coast + Patia |
| 3 | Oriente + Macizo | ~6,800 | Mountains + Massif |
| 4 | Bota Caucana | ~3,800 | Amazonian piedmont |

### Balance Assessment

- Folds are reasonably balanced by area (3,800-9,000 km2)
- Fold 1 (Norte) is the most flood-prone — keeping it separate ensures generalizability
- Fold 2 combines Pacific and Sur (both have western drainage)
- Fold 4 is smallest but terrain is distinct enough to justify separation

---

## 9. Expected Computation Times

| Step | GEE Time | Local Time | Notes |
|------|----------|------------|-------|
| 01 SAR detection | ~2.5 hours | — | ~46% of Antioquia area, ~40% less time |
| 02 JRC analysis | ~20 min | — | Pre-computed data |
| 03 Feature engineering | ~1.5 hours | — | 18 features at 30 m |
| 04 ML training | — | <25 min | Fewer training samples possible |
| 05 Population exposure | ~40 min | 10 min | Smaller area |
| 06 Climate analysis | ~40 min | 15 min | CHIRPS aggregation |
| 07 Visualization | — | 15 min | Fewer municipalities |
| 08 Tables | — | 5 min | CSV + LaTeX |
| 09 QC | — | 10 min | Automated checks |
| **Total** | **~5.5 hours** | **~1.5 hours** | **~7 hours end-to-end** |

---

## 10. Quality Control Adjustments

Update these values in `09_quality_control.py`:

```python
EXPECTED_AREA_KM2 = 29308      # was 63612
EXPECTED_MUNICIPALITY_COUNT = 42  # was 125
AREA_TOLERANCE = 0.10           # +/- 10%
```

### Cauca-specific QC checks:

- [ ] Salvajina reservoir correctly masked as permanent water
- [ ] Municipality count = 42 (verify no duplicates across subregions)
- [ ] Pacific coast subregion flagged with reduced SAR confidence
- [ ] No municipality has exposed population > total population
- [ ] Risk scores in [0, 1] range
- [ ] Spatial CV fold 4 (Bota Caucana) has sufficient training samples
- [ ] ENSO stratification shows La Nina > Neutral > El Nino flood extent

---

## 11. Known Challenges

| Challenge | Impact | Mitigation |
|-----------|--------|------------|
| Extreme topography (0-4,700 m) | SAR shadow/layover in steep valleys | Dual-orbit, document limitations |
| Pacific coast no-dry-baseline | Lower SAR change detection accuracy | Weight JRC labels, separate analysis |
| Salvajina Dam | Artificial permanent water body | Explicit reservoir masking |
| Small Bota Caucana subregion | CV fold imbalance | Monitor fold-specific AUC |
| High rural population (65%) | Different exposure patterns | Adapt FRI interpretation |
| Tidal influence on coast | False water detections | Increase min_water_area_ha |
| Mangrove backscatter | SAR misclassification | Consider VH band for mangrove areas |
| Fewer municipalities (42 vs 125) | Smaller sample space for statistics | May need to reduce SAMPLES_PER_CLASS |

---

*Guide prepared for the replication study — Universidad EAFIT, 2026.*
*Original framework: [github.com/Cespial/antioquia-flood-risk](https://github.com/Cespial/antioquia-flood-risk)*
