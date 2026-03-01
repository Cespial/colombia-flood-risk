"""
Central configuration for the Cauca Flood Risk Assessment project.
All parameters, constants, and GEE asset paths are defined here.

Replicated from the Antioquia framework — adapted for the Department of Cauca.
"""

import os
import ee
from dotenv import load_dotenv

load_dotenv()

# --- GEE Initialization ---
try:
    ee.Initialize(project=os.getenv('GEE_PROJECT_ID', 'ee-maestria-tesis'))
except Exception:
    ee.Authenticate()
    ee.Initialize(project=os.getenv('GEE_PROJECT_ID', 'ee-maestria-tesis'))

# ============================================================================
# STUDY AREA: Department of Cauca, Colombia
# ============================================================================

# Administrative boundaries from FAO GAUL Level 1
ADMIN_DATASET = 'FAO/GAUL/2015/level1'
DEPARTMENT_NAME = 'Cauca'
COUNTRY_NAME = 'Colombia'

# Municipal boundaries from FAO GAUL Level 2
MUNICIPAL_DATASET = 'FAO/GAUL/2015/level2'

# HydroSHEDS basin boundaries
HYDROBASINS_L5 = 'WWF/HydroSHEDS/v1/Basins/hybas_sa_lev05_v1c'
HYDROBASINS_L7 = 'WWF/HydroSHEDS/v1/Basins/hybas_sa_lev07_v1c'

# ============================================================================
# 7 SUBREGIONS OF CAUCA — VERIFIED AGAINST FAO GAUL 2015 (level2)
# ============================================================================
#
# GAUL 2015 contains 40 entries for Cauca (ADM2_CODE 13719-13758).
# Of these, 3 are insular territories (Gorgona, Guapi islands, Timbiqui islands)
# and 37 are continental municipalities.
#
# 5 modern municipalities are ABSENT from GAUL 2015 because they were either
# created after the GAUL reference date or not recognized as separate units:
#   - Guachene (segregated from Caloto, 2006) — included in 'Caloto' geometry
#   - Villa Rica (segregated from Caloto, 1998) — included in 'Caloto' geometry
#   - Piamonte (created from Santa Rosa, 1993) — included in 'Santa Rosa' geometry
#   - Totoro (old municipality) — missing from GAUL, may be merged with Silvia/Inza
#   - Sucre (old municipality) — missing from GAUL, may be merged with Bolivar
#
# Strategy: Use GAUL names exactly as they appear. Municipalities missing from
# GAUL are commented out and their territory is covered by their parent municipality.
# The insular entries are grouped under Pacifico for completeness.
#
# Verified 2026-03-01 via:
#   ee.FeatureCollection('FAO/GAUL/2015/level2')
#     .filter(ee.Filter.eq('ADM1_NAME', 'Cauca'))
#     .aggregate_array('ADM2_NAME').getInfo()

SUBREGIONS = {
    'Centro': [
        'Popayan', 'Cajibio', 'El Tambo', 'Morales',
        'Piendamo', 'Purace', 'Silvia', 'Timbio'
    ],
    'Norte': [
        'Buenos Aires', 'Caloto', 'Corinto', 'Jambalo',
        'Miranda', 'Padilla', 'Puerto Tejada',
        'Santander De Quilichao', 'Suarez', 'Toribio',
        'Caldono',
        # 'Guachene' — not in GAUL 2015, territory within 'Caloto'
        # 'Villa Rica' — not in GAUL 2015, territory within 'Caloto'
    ],
    'Oriente': [
        'Inza', 'Paez',
        # 'Totoro' — not in GAUL 2015, territory likely within Inza/Silvia
    ],
    'Pacifico': [
        'Lopez De Micay', 'Timbiqui', 'Guapi',
        'Gorgona (is.)', 'Guapi (is.)', 'Timbiqui (is.)',  # Insular territories
    ],
    'Sur': [
        'Argelia', 'Balboa', 'Bolivar', 'Patia (el Bordo)',
        'Florencia', 'Mercaderes',
        # 'Sucre' — not in GAUL 2015, territory likely within Bolivar
    ],
    'Macizo': [
        'Sotara', 'La Vega', 'Almaguer', 'La Sierra', 'Rosas'
    ],
    'Bota Caucana': [
        'San Sebastian', 'Santa Rosa',
        # 'Piamonte' — not in GAUL 2015, territory within 'Santa Rosa'
    ],
}

# GAUL contains 40 entries; 37 continental municipalities + 3 insular territories
# 5 modern municipalities are absent (territory covered by parent municipalities)
EXPECTED_MUNICIPALITY_COUNT = 40  # Matches GAUL 2015 entries for Cauca

# Mapping of modern municipality names to their GAUL parent (for reference/reporting)
GAUL_MISSING_MUNICIPALITIES = {
    'Guachene': 'Caloto',           # Segregated 2006, within Caloto in GAUL
    'Villa Rica': 'Caloto',         # Segregated 1998, within Caloto in GAUL
    'Piamonte': 'Santa Rosa',       # Created 1993, within Santa Rosa in GAUL
    'Totoro': None,                 # Old municipality, missing from GAUL
    'Sucre': None,                  # Old municipality, missing from GAUL
}
EXPECTED_AREA_KM2 = 29308  # Official area of Department of Cauca

# ============================================================================
# TEMPORAL CONFIGURATION
# ============================================================================

# Full analysis period: 2015-2025 (Sentinel-1 era)
ANALYSIS_START = '2015-01-01'
ANALYSIS_END = '2025-12-31'

# Sentinel-1 availability
S1_START = '2014-10-03'  # Sentinel-1A launch
S1B_FAILURE = '2021-12-23'  # Sentinel-1B failure
S1C_LAUNCH = '2024-04-25'  # Sentinel-1C launch

# Seasonal periods for Colombia (bimodal precipitation)
# NOTE: The Andean interior of Cauca follows the bimodal pattern.
# The Pacific subregion (Guapi, Timbiqui, Lopez de Micay) has continuous
# rainfall year-round (5,000-13,000 mm/yr) with no distinct dry season.
# This bimodal definition applies to ~85% of the department area.
SEASONS = {
    'DJF': {'months': [12, 1, 2], 'label': 'Dry season 1'},
    'MAM': {'months': [3, 4, 5], 'label': 'Wet season 1 (first rains)'},
    'JJA': {'months': [6, 7, 8], 'label': 'Dry season 2 (veranillo)'},
    'SON': {'months': [9, 10, 11], 'label': 'Wet season 2 (peak floods)'},
}

# Annual analysis windows
ANNUAL_WINDOWS = {year: {
    'start': f'{year}-01-01',
    'end': f'{year}-12-31',
} for year in range(2015, 2026)}

# ============================================================================
# ENSO CLASSIFICATION (2015-2025)
# ============================================================================
# Source: NOAA ONI (Oceanic Nino Index)
# https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php

ENSO_YEARS = {
    'El Nino': [2015, 2016, 2023, 2024],
    'La Nina': [2020, 2021, 2022],
    'Neutral': [2017, 2018, 2019, 2025],
}

# ============================================================================
# SATELLITE DATA SOURCES
# ============================================================================

# Sentinel-1 SAR GRD (Ground Range Detected)
S1_COLLECTION = 'COPERNICUS/S1_GRD'
S1_PARAMS = {
    'instrumentMode': 'IW',  # Interferometric Wide swath
    'resolution': 10,  # meters
    'polarization': ['VV', 'VH'],  # Dual-pol
    'orbitProperties_pass': 'DESCENDING',  # Consistent geometry
    'resolution_meters': 10,
}
# NOTE for Cauca: Consider testing ASCENDING pass as well, especially for
# the steep Andean valleys (Central and Western Cordillera). Descending pass
# may produce shadow/layover artifacts in narrow E-W oriented valleys.

# Water detection thresholds for SAR (VV polarization)
SAR_WATER_THRESHOLDS = {
    'otsu_adaptive': True,  # Use Otsu automatic thresholding
    'vv_default': -15.0,  # dB, fallback threshold
    'vv_range': (-20.0, -12.0),  # Valid range for water detection
    'vh_default': -22.0,  # dB, fallback for VH
    'min_water_area_ha': 1.0,  # Minimum mappable water body
    'speckle_filter_radius': 50,  # meters, focal median radius
}
# NOTE for Cauca:
# - Pacific coast: Consider increasing min_water_area_ha to 2.0 ha to
#   filter tidal noise in coastal areas (Guapi, Timbiqui, Lopez de Micay)
# - Mountainous terrain: SAR accuracy will be lower in steep valleys (~60-70%)
# - The Salvajina Dam reservoir should be masked as permanent water

# JRC Global Surface Water v1.4
JRC_GSW = 'JRC/GSW1_4/GlobalSurfaceWater'
JRC_GSW_MONTHLY = 'JRC/GSW1_4/MonthlyHistory'
JRC_GSW_YEARLY = 'JRC/GSW1_4/YearlyHistory'

# JRC GLOFAS Flood Hazard
GLOFAS_FLOOD_HAZARD = 'JRC/CEMS_GLOFAS/FloodHazard/v1'

# SRTM Digital Elevation Model (30m)
SRTM = 'USGS/SRTMGL1_003'

# MERIT Hydro (90m) - pre-computed hydrological layers
MERIT_HYDRO = 'MERIT/Hydro/v1_0_1'

# HAND (Height Above Nearest Drainage) - derived from SRTM
HAND_DATASET = 'users/gaborimbre/HAND_30m_SA'  # South America HAND

# CHIRPS Daily Precipitation (5.5km)
CHIRPS = 'UCSB-CHG/CHIRPS/DAILY'

# ERA5-Land Monthly (11km)
ERA5_LAND = 'ECMWF/ERA5_LAND/MONTHLY_AGGR'

# MODIS LST (1km)
MODIS_LST = 'MODIS/061/MOD11A2'

# WorldPop Population Density (100m)
WORLDPOP = 'WorldPop/GP/100m/pop'

# ESA WorldCover (10m land cover)
WORLDCOVER = 'ESA/WorldCover/v200'

# OpenStreetMap-based roads
GRIP_ROADS = 'projects/sat-io/open-datasets/GRIP4/Africa-Caribbean'

# ============================================================================
# FLOOD RISK MODEL PARAMETERS
# ============================================================================

# HAND thresholds for flood susceptibility
HAND_CLASSES = {
    'very_high': {'range': (0, 5), 'label': 'Very High', 'color': '#d73027'},
    'high': {'range': (5, 15), 'label': 'High', 'color': '#fc8d59'},
    'moderate': {'range': (15, 30), 'label': 'Moderate', 'color': '#fee08b'},
    'low': {'range': (30, 60), 'label': 'Low', 'color': '#d9ef8b'},
    'very_low': {'range': (60, 9999), 'label': 'Very Low', 'color': '#1a9850'},
}

# Flood frequency classes (based on JRC occurrence)
FLOOD_FREQUENCY_CLASSES = {
    'permanent': {'range': (75, 100), 'label': 'Permanent water', 'color': '#08306b'},
    'very_frequent': {'range': (50, 75), 'label': 'Very frequent', 'color': '#2171b5'},
    'frequent': {'range': (25, 50), 'label': 'Frequent flooding', 'color': '#6baed6'},
    'occasional': {'range': (10, 25), 'label': 'Occasional flooding', 'color': '#bdd7e7'},
    'rare': {'range': (1, 10), 'label': 'Rare flooding', 'color': '#eff3ff'},
}

# ML Model parameters
ML_PARAMS = {
    'random_forest': {
        'n_estimators': 500,
        'max_depth': 15,
        'min_samples_split': 10,
        'min_samples_leaf': 5,
        'random_state': 42,
        'n_jobs': -1,
    },
    'xgboost': {
        'n_estimators': 500,
        'max_depth': 8,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
        'eval_metric': 'auc',
    },
    'lightgbm': {
        'n_estimators': 500,
        'max_depth': 8,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': 42,
        'metric': 'auc',
        'verbose': -1,
    },
}

# Flood susceptibility features (predictors)
SUSCEPTIBILITY_FEATURES = [
    'elevation',            # SRTM 30m
    'slope',                # Derived from SRTM
    'aspect',               # Derived from SRTM
    'curvature',            # Plan curvature
    'hand',                 # Height Above Nearest Drainage
    'twi',                  # Topographic Wetness Index
    'spi',                  # Stream Power Index
    'dist_rivers',          # Distance to nearest river
    'dist_roads',           # Distance to nearest road
    'drainage_density',     # River density per unit area
    'rainfall_annual',      # Mean annual precipitation (CHIRPS)
    'rainfall_max_monthly', # Max monthly precipitation
    'land_cover',           # ESA WorldCover 2021
    'ndvi_mean',            # Mean annual NDVI
    'soil_moisture',        # ERA5-Land soil moisture
    'pop_density',          # WorldPop 100m
    'flood_frequency_jrc',  # JRC water occurrence
    'sar_water_frequency',  # Sentinel-1 derived water frequency
]

# Cross-validation parameters
# Spatial 5-fold CV using subregion-based groupings
# Fold assignments for Cauca's 7 subregions:
CV_PARAMS = {
    'n_splits': 5,  # Stratified spatial K-fold
    'test_size': 0.3,
    'random_state': 42,
}

# Spatial CV fold groupings (group 7 subregions into 5 folds)
CV_FOLD_GROUPS = {
    0: ['Centro'],                    # Fold 0: Central highlands
    1: ['Norte'],                     # Fold 1: Flat Cauca valley
    2: ['Pacifico', 'Sur'],           # Fold 2: Pacific coast + Southern
    3: ['Oriente', 'Macizo'],         # Fold 3: Eastern mountains + Massif
    4: ['Bota Caucana'],              # Fold 4: Amazonian piedmont
}

# Training sample parameters
SAMPLES_PER_CLASS = 5000  # 5,000 per class (flood/non-flood)
# NOTE: Cauca is ~46% the size of Antioquia (29,308 vs 63,612 km2).
# If training sample quality is low, consider reducing to 3,000-4,000.

# ============================================================================
# RISK CLASSIFICATION
# ============================================================================

RISK_CLASSES = {
    'Very Low':  {'range': (0.0, 0.2), 'color': '#1a9850'},
    'Low':       {'range': (0.2, 0.4), 'color': '#91cf60'},
    'Moderate':  {'range': (0.4, 0.6), 'color': '#fee08b'},
    'High':      {'range': (0.6, 0.8), 'color': '#fc8d59'},
    'Very High': {'range': (0.8, 1.0), 'color': '#d73027'},
}

# Flood Risk Index (FRI) weights
FRI_WEIGHTS = {
    'pop_normalized': 0.4,
    'pct_high_area': 0.3,
    'mean_susceptibility': 0.3,
}

# ============================================================================
# VISUALIZATION PARAMETERS
# ============================================================================

# Color palettes
WATER_PALETTE = ['#ffffff', '#bdd7e7', '#6baed6', '#2171b5', '#08306b']
RISK_PALETTE = ['#1a9850', '#91cf60', '#d9ef8b', '#fee08b',
                '#fc8d59', '#d73027']
SUBREGION_PALETTE = [
    '#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00',
    '#ffff33', '#a65628'
]  # 7 colors for 7 subregions

# Map center for Cauca
MAP_CENTER = {'lat': 2.3, 'lon': -76.6}
MAP_ZOOM = 9  # Slightly more zoomed than Antioquia (smaller area)

# Figure DPI for publication
FIGURE_DPI = 600
FIGURE_FORMAT = ['pdf', 'png']

# ============================================================================
# SPECIAL CONSIDERATIONS FOR CAUCA
# ============================================================================

# Salvajina Dam (completed 1985) — must be masked as permanent water
# Location: Municipality of Suarez, on the Cauca River
SALVAJINA_DAM = {
    'lat': 2.95,
    'lon': -76.68,
    'year_completed': 1985,
    'reservoir_length_km': 31,
    'capacity_mw': 270,
    'note': 'Mask reservoir as permanent water body in SAR analysis',
}

# Key flood-prone municipalities (for prioritized analysis)
# Names match GAUL ADM2_NAME exactly
HIGH_FLOOD_RISK_MUNICIPALITIES = [
    'Puerto Tejada',           # Flat Cauca valley, frequent flooding
    'Caloto',                  # Cauca River floodplain (includes Guachene + Villa Rica territory)
    'Miranda',                 # Cauca River floodplain
    'Corinto',                 # Cauca River tributary floods
    'Padilla',                 # Flat valley
    'Santander De Quilichao',  # Cauca River influence
    'Buenos Aires',            # Cauca River, post-Salvajina
    'Guapi',                   # Pacific coast, continuous rainfall
    'Timbiqui',                # Pacific coast
    'Lopez De Micay',          # Pacific coast, extreme rainfall (>13,000 mm/yr)
    'Popayan',                 # Molino River flooding
]

# Volcanic features (for geomorphological context)
VOLCANIC_FEATURES = {
    'Purace': {'lat': 2.32, 'lon': -76.40, 'elevation_m': 4650},
    'Sotara': {'lat': 2.11, 'lon': -76.59, 'elevation_m': 4580},
}

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Export scale (meters)
EXPORT_SCALE = 30

# Google Drive export folder
DRIVE_EXPORT_FOLDER = 'cauca_flood_risk'

# GEE asset path for susceptibility map
GEE_SUSCEPTIBILITY_ASSET = 'projects/ee-maestria-tesis/assets/cauca_flood_susceptibility_ensemble'

# Project paths
import pathlib
PROJECT_ROOT = pathlib.Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
FIGURES_DIR = OUTPUTS_DIR / 'figures'
TABLES_DIR = OUTPUTS_DIR / 'tables'
OVERLEAF_DIR = PROJECT_ROOT / 'overleaf'
LOGS_DIR = PROJECT_ROOT / 'logs'
