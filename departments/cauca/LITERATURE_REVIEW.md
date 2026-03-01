# Literature Review: Flood Risk in the Department of Cauca, Colombia

**Compiled for:** Municipality-Scale Flood Risk Mapping in Cauca, Colombia
**Authors:** Cristian Espinal Maya & Santiago Jimenez Londono — Universidad EAFIT, 2026

---

## Table of Contents

1. [Geographic and Hydrographic Context](#1-geographic-and-hydrographic-context)
2. [Major River Basins](#2-major-river-basins)
3. [Subregional Division](#3-subregional-division)
4. [Flood-Prone Areas and Historical Events](#4-flood-prone-areas-and-historical-events)
5. [Climate Patterns and ENSO Influence](#5-climate-patterns-and-enso-influence)
6. [Existing Flood Risk Studies](#6-existing-flood-risk-studies)
7. [Remote Sensing and ML-Based Flood Mapping](#7-remote-sensing-and-ml-based-flood-mapping)
8. [Special Considerations for Cauca](#8-special-considerations-for-cauca)
9. [Population and Socioeconomic Data](#9-population-and-socioeconomic-data)
10. [Institutional Framework](#10-institutional-framework)
11. [References](#11-references)

---

## 1. Geographic and Hydrographic Context

The Department of Cauca is located in southwestern Colombia, spanning both the Andean and Pacific natural regions. It covers **29,308 km2** (approximately 2.56% of the national territory), making it the 13th largest department in Colombia.

### Key Facts

| Attribute | Value |
|-----------|-------|
| Area | 29,308 km2 |
| Capital | Popayan (1,728 m a.s.l.) |
| Municipalities | 42 |
| Elevation range | 0 m (Pacific coast) to ~4,700 m (Purace volcano) |
| Latitude | 0 58'54" N to 3 19'04" N |
| Longitude | 75 47'36" W to 77 57'05" W |
| Population (2026) | ~1,605,145 (DANE projection) |
| Rural population | ~65% (one of the highest in Colombia) |

### Boundaries

- **North:** Valle del Cauca
- **East:** Tolima, Huila, Caqueta
- **South:** Narino, Putumayo
- **West:** Pacific Ocean

The department's topography is extraordinarily diverse, traversed by the Western and Central Cordilleras of the Andes, with the inter-Andean Cauca River valley running between them. The western slopes descend into the Pacific coastal lowlands, one of the wettest regions on Earth.

---

## 2. Major River Basins

Cauca's hydrographic system comprises five major basins:

### 2.1 Alto Cauca (Upper Cauca)

The most important basin. The Cauca River originates in the Colombian Massif near the Sotara volcano and flows northward through the department. Major tributaries include: Palo, Guengue, Negro, Teta, Desbaratado, Quilichao, Mondomo, Ovejas, Pescador, Robles, Piedras, Sucio, Palace, Cofre, Honda, Cajibio, Piendamo, Tunia, Molino, Timbio, and Blanco.

**Salvajina Dam** (1985): Located in the municipality of Suarez. 270 MW capacity, 31 km reservoir length. Fundamentally altered the flood regime of the upper Cauca. Reduced flood peak flows, frequency, and extent during rainy seasons, though extreme La Nina events can still cause downstream flooding.

### 2.2 Patia Basin

Drains the southern portion of the department. Constituted by the Rio Patia and tributaries: Guachinoco, Ismita, Bojoleo, El Guaba, Sambingo, and Mayo. The Patia is one of the few rivers in Colombia that flows westward to the Pacific.

### 2.3 Pacific Basin

Rivers flowing directly to the Pacific Ocean: Guapi, Timbiqui, Saija, Micay, and Naya. This basin represents ~35% of the department's surface area and includes the municipalities of Guapi, Timbiqui, Lopez de Micay, and parts of Argelia and El Tambo.

### 2.4 Alto Magdalena (Upper Magdalena)

Eastern drainage through the Rio Paez and tributaries: San Vicente, Moras, Ullucos, Negro, Negro de Narvaez. Drains the Oriente subregion (Inza, Paez, Totoro).

### 2.5 Caqueta Basin

Drains the Amazonian piedmont in the southeastern corner (Bota Caucana: Piamonte, San Sebastian, Santa Rosa).

---

## 3. Subregional Division

The 42 municipalities are organized into 7 subregions:

| Subregion | Municipalities | Key Characteristics |
|-----------|---------------|---------------------|
| **Centro** (8) | Popayan, Cajibio, El Tambo, Morales, Piendamo, Purace, Silvia, Timbio | Administrative center, Andean highlands, Molino River flooding |
| **Norte** (13) | Buenos Aires, Caloto, Corinto, Jambalo, Miranda, Padilla, Puerto Tejada, Santander de Quilichao, Suarez, Toribio, Villa Rica, Caldono, Guachene | Flat Cauca River valley, highest fluvial flood risk, sugarcane agriculture |
| **Oriente** (3) | Inza, Paez, Totoro | Steep mountainous terrain, Paez River, earthquake/landslide risk |
| **Pacifico** (3) | Lopez de Micay, Timbiqui, Guapi | Pacific coast, extreme rainfall (5,000-13,000 mm/yr), tidal influence |
| **Sur** (7) | Argelia, Balboa, Bolivar, Patia, Florencia, Mercaderes, Sucre | Patia River basin, mixed terrain |
| **Macizo** (5) | Sotara, La Vega, Almaguer, La Sierra, Rosas | Colombian Massif, water source, high-altitude paramo |
| **Bota Caucana** (3) | Piamonte, San Sebastian, Santa Rosa | Amazonian piedmont, Caqueta basin drainage |

---

## 4. Flood-Prone Areas and Historical Events

### 4.1 Most Flood-Prone Zones

**Northern Subregion (flat Cauca River valley):** Puerto Tejada, Caloto, Miranda, Corinto, Guachene, Padilla, Santander de Quilichao, and Buenos Aires are located in the flat valley of the upper Cauca River. The river becomes sinuous with multiple meanders upon entering this open valley, making floodplain inundation common. This is the zone of highest fluvial flood risk in the department.

**Pacific Coast (Pacifico subregion):** Guapi, Timbiqui, and Lopez de Micay experience continuous heavy rainfall exceeding 5,000-13,000 mm annually. Lopez de Micay is one of the wettest places on Earth. These territories are characterized by frequent floods, avalanches, and landslides.

**Centro subregion (Popayan):** The Molino River sub-basin has experienced recurring floods since 1928, with notable events in 1928, 1938, 1986, 1996, 2004, 2011, and December 2013. Informal settlements along flood-prone zones exacerbate vulnerability.

**Oriente subregion (Paez, Inza):** Extremely vulnerable to earthquake-triggered landslides and subsequent flooding due to steep mountainous terrain and volcanic geology.

### 4.2 Major Historical Flood Events

| Year | Event | Impact |
|------|-------|--------|
| **1994** | Paez earthquake (M6.4) + avalanche, June 6 | 1,100 dead, 500 missing, ~40,000 ha devastated. Catastrophic landslides and torrential floods on the Paez River. |
| **1999** | La Nina floods in upper Cauca | Two major flood events in a single year. |
| **2008** | La Nina floods | Two major flood events in upper Cauca valley. |
| **2010-2011** | La Nina extreme event | Nationwide: 4M affected, USD 7.8B losses. In upper Cauca: 41,669 ha flooded. Levee failures and avulsion events. |
| **2013** | Popayan flooding (Dec 24) | Molino River overflow: 100+ landslides, urban area flooding. |
| **2024** | Cauca River overflow | Six municipalities affected, red alerts issued by IDEAM. |
| **2025** | Pacific coast flooding | 20,000+ affected in Guapi, Timbiqui, Lopez de Micay. 840 homes damaged, 18 destroyed. |
| **2026** | Cauca River red alert (Feb) | IDEAM red alert for riverside municipalities due to unusual increase in river levels. |

### 4.3 IDEAM National Classification

According to IDEAM, Cauca is among the departments with the **highest threat from sudden flood events**. Urban flood hazard in Cauca is classified as **HIGH**, meaning potentially damaging and life-threatening urban floods are expected at least once in the next 10 years.

---

## 5. Climate Patterns and ENSO Influence

### 5.1 Rainfall Regimes

Cauca exhibits two distinct rainfall regimes depending on geographic location:

**Bimodal Andean pattern (interior highlands, ~85% of department area):**
- First wet season: March-April-May (MAM)
- Dry interlude: June-August (veranillo)
- Second wet season: September-October-November (SON) — peak floods
- Dry season: December-February (DJF)

**Continuous Pacific pattern (coastal lowlands, ~15% of area):**
- No distinct dry season
- Annual precipitation: 5,000-13,000 mm
- Heavy downpours nearly daily
- Lopez de Micay averages ~13,159 mm/yr

### 5.2 ENSO Impacts

**El Nino (warm phase):**
- Average 16% reduction in total annual rainfall
- Rise in temperature in Andean region
- Drought conditions and lower river levels
- Reduced flood risk

**La Nina (cool phase):**
- Average 23% increase in total annual rainfall
- Primary driver of catastrophic flooding in the Cauca River system
- Nearly all major historical floods associated with La Nina episodes
- The 2010-2011 La Nina was the most devastating in recent history

**ENSO classification for study period (2015-2025):**

| Phase | Years |
|-------|-------|
| El Nino | 2015, 2016, 2023, 2024 |
| La Nina | 2020, 2021, 2022 |
| Neutral | 2017, 2018, 2019, 2025 |

---

## 6. Existing Flood Risk Studies

### 6.1 Studies Specific to the Cauca River System

1. **"Hydrological analysis of historical floods in the upper valley of Cauca river"** — *Ingenieria y Competitividad*, Universidad del Valle, 2016. Identified nine representative flow windows between 1988 and 2011. Found 44% of floods occurred Jan-Jun and 56% Oct-Dec. Nearly all floods associated with La Nina.

2. **"Spatio-Temporal Variability of Hydroclimatology in the Upper Cauca River Basin"** — *Atmosphere* (MDPI), 2021. Analyzed the impact of the Salvajina Dam on hydroclimatological regime.

3. **"Recent Precipitation Trends and Floods in the Colombian Andes"** — *Water* (MDPI), 2019. Analyzed eight extreme climate indices from 1970-2013 in the Upper Cauca Basin and their relation to ENSO.

4. **"Contrasting climate controls on the hydrology of the mountainous Cauca River"** — *Geomorphology* (ScienceDirect), 2020. Climate controls, hydrology, and sedimentary processes.

5. **"Influencia de la variabilidad climatica en la modelacion estadistica de extremos hidrologicos en el Valle Alto del rio Cauca"** — Ruth Karime Sedano, IIAMA-UPV. Statistical modeling of hydrological extremes.

6. **"Simulacion de inundaciones a partir de Cartografia Digital y de Topobatimetria"** — UNICAUCA. Flood simulation using digital cartography for the Cauca region.

7. **"Las redes de politica publica: analisis de la gestion del riesgo ante inundaciones en el Valle alto del rio Cauca"** — *Redalyc*. Public policy networks for flood risk management.

8. **Popayan flood risk study** — University of Cauca, Faculty of Civil Engineering. Technical study on urban and rural flood risks in Popayan.

### 6.2 Gap Analysis

**No published study was found that applies SAR/GEE/ML flood susceptibility mapping specifically to the Department of Cauca.** This represents a significant research gap, as Cauca's complex terrain (Andes + Pacific) and diverse flood mechanisms make it an ideal candidate for multi-sensor, multi-model approaches. Existing studies are predominantly hydrological/statistical analyses focused on the Cauca River mainstream, not municipality-scale spatial susceptibility mapping.

---

## 7. Remote Sensing and ML-Based Flood Mapping

### 7.1 Applicable Methodologies (from literature)

1. **"A methodology for multitemporal analysis of hydraulic dynamics of water bodies using satellite radar imagery"** — *Journal of Hydroinformatics* (IWA), 2025. GEE and SAR in Bajo Cauca region with AI change detection.

2. **"Global Flood Mapper: Google Earth Engine application for rapid flood mapping using Sentinel-1 SAR"** — *Natural Hazards* (Springer), 2022. Web application for S1 SAR flood maps on GEE.

3. **UN-SPIDER Recommended Practice:** Flood mapping using Sentinel-1 SAR change detection in GEE.

4. **"Flood Susceptibility Mapping Using SAR Data and Machine Learning"** — *Remote Sensing* (MDPI), 2024. Integrates S1 SAR with RF, XGBoost, CNN.

5. **"DeepSAR Flood Mapper"** — Taylor & Francis, 2025. Global flood mapping using MLP deep learning with S1 SAR and HAND on GEE.

6. **"Enhancing flood prediction through remote sensing, ML, and GEE"** — *Frontiers in Water*, 2025.

### 7.2 Methodological Foundation (from Antioquia study)

The Antioquia framework (Espinal Maya & Jimenez Londono, 2026) demonstrated:
- AUC-ROC = 0.94 +/- 0.02 with weighted ensemble of RF, XGBoost, LightGBM
- HAND, SAR flood frequency, and elevation as dominant SHAP predictors
- Effective use of spatial 5-fold CV with subregion-based folds
- 4,762 Sentinel-1 scenes processed for 63,612 km2

The Cauca replication can directly apply this framework with terrain-specific adaptations.

---

## 8. Special Considerations for Cauca

### 8.1 Mixed Terrain (Andes + Pacific Lowlands)

Cauca spans from sea level to ~4,700 m, requiring multi-scale flood mapping:
- Flat valley floods in Norte subregion (fluvial, slow-onset)
- Torrential/flash floods in Andean mountain valleys
- Coastal/riverine flooding in Pacific lowlands with continuous rain
- Different SAR backscatter characteristics across terrain types

**Recommendations:**
- Consider dual-orbit (ASCENDING + DESCENDING) to reduce shadow/layover in steep valleys
- HAND threshold should stay strict (<5 m) in mountainous areas
- SAR accuracy will be lower in steep valleys (~60-70% detection)
- Document slope masking impact (30 deg threshold will exclude significant area)

### 8.2 Volcanic Influence (Purace and Sotara)

- Purace (~4,650 m) and Sotara (~4,580 m) create lahar hazards that interact with flooding
- Volcanic soils have different infiltration characteristics
- 1994 Paez earthquake demonstrated seismic-triggered landslide-flood cascading hazards
- Paramo ecosystems at high altitudes serve as critical water regulation zones

### 8.3 Pacific Coast Continuous Rainfall

- 5,000-13,000 mm/yr precipitation means rarely a "dry baseline" for SAR change detection
- Cloud cover nearly permanent, rendering optical imagery largely unusable
- SAR (Sentinel-1) becomes the only viable remote sensing option
- Tidal influences near the coast complicate water detection
- Mangrove ecosystems add SAR backscatter complexity
- Consider increasing min_water_area_ha to 2.0 ha to filter tidal noise

### 8.4 Salvajina Dam

- Completed 1985, fundamentally altered flood regime
- Must mask reservoir as permanent water body
- Post-dam, low-frequency high-magnitude floods still occur during La Nina
- Pre/post-dam analysis important for understanding long-term changes

### 8.5 Upper Cauca River Dynamics

- Flat valley north of Popayan creates extensive floodplains with meandering behavior
- Sugarcane agriculture dominates flat valley (agricultural loss context)
- Levee systems can fail during extreme events (demonstrated 2010-2011)
- Receives contributions from tributaries draining both Central and Western Cordilleras

---

## 9. Population and Socioeconomic Data

### 9.1 Department Population (DANE Projections)

| Year | Total | Urban | Rural |
|------|-------|-------|-------|
| 2018 (Census) | ~1,464,488 | ~513,000 | ~951,000 |
| 2025 | 1,590,171 | 561,251 | 1,028,920 |
| 2026 | 1,605,145 | 564,311 | 1,040,834 |

**Key characteristic:** ~65% rural population, one of the highest ratios in Colombia.

### 9.2 Major Urban Centers

| Municipality | Population (est.) | Flood Risk |
|-------------|-------------------|------------|
| Popayan | ~343,000 | Medium (Molino River) |
| Santander de Quilichao | ~106,000 | High (Cauca valley) |
| El Tambo | ~50,000 | Medium |
| Puerto Tejada | ~47,000 | Very High (flat valley) |
| Piendamo | ~45,000 | Medium |
| Miranda | ~42,000 | High (Cauca valley) |
| Patia | ~40,000 | Medium |
| Corinto | ~35,000 | High (Cauca valley) |
| Guapi | ~30,000 | High (Pacific coast) |

### 9.3 Ethnic Composition

Cauca has significant indigenous (Misak, Nasa/Paez, Yanacona, Coconuco) and Afro-Colombian populations, particularly in the Norte and Pacifico subregions. These communities often occupy flood-prone areas and have heightened vulnerability due to socioeconomic conditions.

---

## 10. Institutional Framework

| Institution | Role |
|-------------|------|
| **IDEAM** | Hydrometeorological monitoring, flood alerts, national zoning maps |
| **CRC** (Corporacion Autonoma Regional del Cauca) | Regional environmental authority, flood defense infrastructure, river monitoring |
| **CVC** (Corporacion Autonoma Regional del Valle del Cauca) | Cauca River corridor flood zoning (shared jurisdiction) |
| **UNGRD** | National disaster risk management coordination |
| **SGC** (Servicio Geologico Colombiano) | Geological and volcanic monitoring |
| **DANE** | Population census and projections |
| **IGAC** | Cartography and topographic data |
| **UNICAUCA** | Academic research on flood simulation |
| **Universidad del Valle** | Hydrological research on upper Cauca |

---

## 11. References

### Flood Studies

1. Universidad del Valle (2016). "Hydrological analysis of historical floods in the upper valley of Cauca river." *Ingenieria y Competitividad*, 18(1). DOI: SciELO S0123-30332016000100005.

2. MDPI (2021). "Spatio-Temporal Variability of Hydroclimatology in the Upper Cauca River Basin in Southwestern Colombia: Pre- and Post-Salvajina Dam Perspective." *Atmosphere*, 12(11), 1527.

3. MDPI (2019). "Recent Precipitation Trends and Floods in the Colombian Andes." *Water*, 11(2), 379.

4. ScienceDirect (2020). "Contrasting climate controls on the hydrology of the mountainous Cauca River." *Geomorphology*.

5. Sedano, R.K. "Influencia de la variabilidad climatica en la modelacion estadistica de extremos hidrologicos en el Valle Alto del rio Cauca, Colombia." IIAMA-UPV.

### Remote Sensing and ML

6. IWA Publishing (2025). "A methodology for multitemporal analysis of hydraulic dynamics of water bodies using satellite radar imagery: Bajo Cauca region." *Journal of Hydroinformatics*, 27(10), 1600.

7. Springer (2022). "Global Flood Mapper: a novel Google Earth Engine application for rapid flood mapping using Sentinel-1 SAR." *Natural Hazards*.

8. UN-SPIDER. "Recommended Practice: Flood Mapping and Damage Assessment Using Sentinel-1 SAR Data in Google Earth Engine."

9. MDPI (2024). "Flood Susceptibility Mapping Using SAR Data and Machine Learning Algorithms." *Remote Sensing*.

10. Taylor & Francis (2025). "DeepSAR Flood Mapper." Global flood mapping using MLP with Sentinel-1 SAR and HAND on GEE.

11. Frontiers (2025). "Enhancing flood prediction through remote sensing, machine learning, and Google Earth Engine." *Frontiers in Water*.

### Baseline Framework

12. Espinal Maya, C. & Jimenez Londono, S. (2026). "Municipality-Scale Flood Risk Mapping in Antioquia, Colombia, Using Sentinel-1 SAR and Ensemble Machine Learning (2015-2025)." Available at SSRN.

### Institutional and Government Sources

13. IDEAM. "Guia Metodologica para la Elaboracion de Mapas de Inundacion." 2024.

14. IDEAM. National flood zoning maps (1:100,000 scale). http://ideam.gov.co/web/agua/amenazas-inundacion

15. CRC (Corporacion Autonoma Regional del Cauca). Flood defense and river monitoring reports.

16. CVC. "Zonificacion Amenaza Inundacion Corredor Rio Cauca." GeoPortal dataset.

17. UNGRD. National disaster event repository and emergency protocols.

18. DANE. Population projections 2018-2026. https://www.dane.gov.co/

19. SGC. Paez earthquake 1994 technical report. https://www2.sgc.gov.co/

### Climate and ENSO

20. NOAA. Oceanic Nino Index (ONI) v5. https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php

21. World Bank. Colombia Climate Risk Profile. Climate Knowledge Portal.

22. ResearchGate (2021). "Rainfall Variability in Southwestern Colombia: Changes in ENSO-Related Features."

23. Wiley (2018). "Seasonality of Rainfall in Colombia." *Water Resources Research*.

### Disaster Events

24. ReliefWeb (2026). Colombia Floods fl-2026-000017-col.

25. El Tiempo (2025). "Mas de 20 mil damnificados en el Pacifico caucano."

26. Infobae (2026). "Emiten alerta en municipios riberenos del rio Cauca por inusual aumento del caudal."

---

*Literature review prepared March 2026 for the Cauca flood risk replication study.*
*Original framework: [github.com/Cespial/antioquia-flood-risk](https://github.com/Cespial/antioquia-flood-risk)*
