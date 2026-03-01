# Replication Guide: Bolivar Department Flood Risk Mapping

**Adapted from the Antioquia framework for the Department of Bolivar, Colombia**

Cristian Espinal Maya & Santiago Jimenez Londono — Universidad EAFIT, 2026

---

## Department Profile: Bolivar

| Attribute | Value |
|-----------|-------|
| Area | 25,978 km² |
| Municipalities | 46 |
| Capital | Cartagena de Indias |
| Population | ~2.2 million |
| Subregions (ZODES) | 6: Dique, Montes de Maria, Mojana, Depresion Momposina, Loba, Magdalena Medio |
| Map center | lat=8.6, lon=-74.1 |
| Main rivers | Magdalena, Cauca, San Jorge, Canal del Dique |
| Climate pattern | Bimodal Caribbean: dry DJF+JJA, wet MAM+SON (peak Aug-Nov) |
| Annual rainfall | 1,400 mm (coast) to 2,500+ mm (interior) |
| Terrain type | Predominantly flat lowlands (<200 m a.s.l.) |

## Flood-Prone Areas

### Depresion Momposina
- Confluence of Magdalena, Cauca, San Jorge, and Cesar rivers
- ~3,400 km² of wetlands; floods reach up to 7 m depth
- Municipalities: Mompos, San Fernando, Margarita, Talaigua Nuevo, Cicuco, Hatillo de Loba

### Canal del Dique
- 115 km man-made distributary from Calamar to Bay of Cartagena
- Catastrophic breach during 2010-2011 La Nina flooded 35,000 ha
- USD 835 million restoration project underway

### La Mojana
- Trans-departmental wetland (Bolivar, Sucre, Cordoba, Antioquia)
- Recurring Cara de Gato dam failures affect 38,000+ people
- Key Bolivar municipality: San Jacinto del Cauca

### Historical Flood Events

| Period | Event | Impact |
|--------|-------|--------|
| 2010-2011 | La Nina | 60,000 households; most-affected department nationally |
| 2021-2022 | La Mojana floods | 12,000 affected; Cara de Gato dam failures |
| May 2024 | Severe weather | 7,806 affected; 1,011 damaged houses |
| Jul-Aug 2024 | Dam failure | 38,000+ affected across multiple departments |
| Jan-Feb 2026 | La Nina-like | Urban flooding in Cartagena; Magangue/Mompos overflow |

## Parameter Adjustments for Bolivar

### Flat Terrain Adaptations

Bolivar's predominantly flat terrain (most areas < 200 m a.s.l.) requires relaxed thresholds:

| Parameter | Antioquia Value | Bolivar Value | Rationale |
|-----------|----------------|---------------|-----------|
| HAND flood label | < 5 m | < 10 m | Broader floodplains |
| HAND non-flood label | >= 30 m | >= 40 m | Higher separation for flat areas |
| Slope non-flood mask | > 10 deg | > 5 deg | Very little terrain above 10 deg |
| Min water area | 1.0 ha | 2.0 ha | Filter tidal/coastal noise |
| HAND class "Very High" | 0-5 m | 0-10 m | Wider floodplain classification |
| Drainage density radius | 1 km | 2 km | Broader drainage networks |
| Slope masking | > 30 deg | > 15 deg | Less steep terrain to exclude |

### SAR Detection Advantages
- Flat terrain = fewer layover/shadow artefacts
- Higher SAR accuracy expected (~80-90% detection vs ~60-70% in mountains)
- HAND will remain dominant SHAP predictor

### SAR Detection Challenges
- **Cienagas**: Seasonal wetlands may be misclassified as flood
- **Flooded vegetation**: Double-bounce scattering in Momposina palm forests
- **Tidal influence**: Minimal (microtidal regime) but filter near coast

## ZODES (Subregions) and Municipalities

### Dique (12 municipalities)
Cartagena de Indias, Turbaco, Arjona, Mahates, San Estanislao, Soplaviento,
Calamar, Santa Rosa, Turbana, Villanueva, Santa Catalina, Clemencia,
San Cristobal, Arroyohondo

### Montes de Maria (7 municipalities)
El Carmen de Bolivar, San Jacinto, San Juan Nepomuceno, El Guamo,
Zambrano, Cordoba, Maria la Baja

### Mojana (6 municipalities)
Magangue, Achi, Montecristo, San Jacinto del Cauca, Tiquisio, Pinillos

### Depresion Momposina (6 municipalities)
Mompos, San Fernando, Margarita, Talaigua Nuevo, Cicuco, Hatillo de Loba

### Loba (6 municipalities)
San Martin de Loba, Barranco de Loba, El Penon, Altos del Rosario,
Regidor, Rio Viejo

### Magdalena Medio (7 municipalities)
San Pablo, Simiti, Santa Rosa del Sur, Morales, Arenal, Cantagallo, Norosi

## Pipeline Execution

### Estimated Computation Times

| Step | GEE Time | Local Time | Notes |
|------|----------|------------|-------|
| 01 SAR detection | ~3 hours | — | Smaller area than Antioquia |
| 02 JRC analysis | ~20 min | — | Mostly pre-computed |
| 03 Feature engineering | ~1.5 hours | — | 18 features at 30 m |
| 04 ML training | — | <30 min | On standard laptop |
| 05 Population exposure | ~45 min | 10 min | GEE zonal statistics |
| 06 Climate analysis | ~45 min | 15 min | CHIRPS temporal aggregation |
| 07 Visualization | — | 15 min | Matplotlib rendering |
| 08 Tables | — | 5 min | CSV + LaTeX generation |
| 09 QC | — | 10 min | Automated checks |
| **Total** | **~6 hours** | **~1.5 hours** | **~7.5 hours end-to-end** |

### Quick Start

```bash
# 1. Set credentials
echo "GEE_PROJECT_ID=ee-flood-risk-bolivar" > .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Authenticate
earthengine authenticate

# 4. Run pipeline
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

## Quality Control Checklist

- [ ] Total area matches 25,978 km² (+-5%)
- [ ] Municipality count = 46
- [ ] No duplicate municipalities in ZODES assignments
- [ ] Training samples balanced (flood ~= non-flood count)
- [ ] AUC-ROC >= 0.85 under spatial CV
- [ ] Exposed population <= total population per municipality
- [ ] Risk scores in [0, 1] range
- [ ] All maps have scale bar, north arrow, coordinate labels

## Key References for Bolivar

1. Angarita, H. et al. (2018). Basin-scale impacts of hydropower development on the Mompos Depression wetlands. *HESS*, 22, 2839-2865.
2. Hoyos, N. et al. (2013). Impact of the 2010-2011 La Nina phenomenon in Colombia. *Applied Geography*, 39, 16-25.
3. Urrea, V. et al. (2019). Seasonality of Rainfall in Colombia. *Water Resources Research*, 55(5).
4. E3S Web of Conferences (2016). Flood protection of Canal del Dique restoration.
5. ACAPS (2024). Colombia: Flooding in La Mojana briefing note.
6. Adaptation Fund/UNDP. Reducing Risk in the Depresion Momposina project.

---

*Guide adapted from the Antioquia Flood Risk Assessment framework — Universidad EAFIT, 2026.*
*Original framework: [github.com/Cespial/antioquia-flood-risk](https://github.com/Cespial/antioquia-flood-risk)*
