"""
Central configuration for the Bolivar Flood Risk Assessment project.
All parameters, constants, and GEE asset paths are defined here.

Adapted from the Antioquia framework for the Department of Bolivar, Colombia.
Bolivar is predominantly flat lowland terrain with extensive floodplains
(Depresion Momposina, Canal del Dique, La Mojana), requiring adjusted
thresholds for HAND, slope masking, and drainage density.
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
# STUDY AREA: Department of Bolivar, Colombia
# ============================================================================

# Administrative boundaries from FAO GAUL Level 1
ADMIN_DATASET = 'FAO/GAUL/2015/level1'
DEPARTMENT_NAME = 'Bolivar'
COUNTRY_NAME = 'Colombia'

# Municipal boundaries from FAO GAUL Level 2
MUNICIPAL_DATASET = 'FAO/GAUL/2015/level2'

# HydroSHEDS basin boundaries
HYDROBASINS_L5 = 'WWF/HydroSHEDS/v1/Basins/hybas_sa_lev05_v1c'
HYDROBASINS_L7 = 'WWF/HydroSHEDS/v1/Basins/hybas_sa_lev07_v1c'

# 6 ZODES (Zonas de Desarrollo Economico y Social) of Bolivar
# with their municipalities (ASCII names for FAO GAUL compatibility)
SUBREGIONS = {
    'Dique': [
        'Cartagena de Indias', 'Turbaco', 'Arjona', 'Mahates',
        'San Estanislao', 'Soplaviento', 'Calamar', 'Santa Rosa',
        'Turbana', 'Villanueva', 'Santa Catalina', 'Clemencia',
        'San Cristobal', 'Arroyohondo',
    ],
    'Montes de Maria': [
        'El Carmen de Bolivar', 'San Jacinto', 'San Juan Nepomuceno',
        'El Guamo', 'Zambrano', 'Cordoba', 'Maria la Baja',
    ],
    'Mojana': [
        'Magangue', 'Achi', 'Montecristo', 'San Jacinto del Cauca',
        'Tiquisio', 'Pinillos',
    ],
    'Depresion Momposina': [
        'Mompos', 'San Fernando', 'Margarita', 'Talaigua Nuevo',
        'Cicuco', 'Hatillo de Loba',
    ],
    'Loba': [
        'San Martin de Loba', 'Barranco de Loba', 'El Penon',
        'Altos del Rosario', 'Regidor', 'Rio Viejo',
    ],
    'Magdalena Medio': [
        'San Pablo', 'Simiti', 'Santa Rosa del Sur',
        'Morales', 'Arenal', 'Cantagallo', 'Norosi',
    ],
}

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

# Seasonal periods for Colombia (bimodal precipitation - Caribbean pattern)
# Bolivar follows the bimodal Caribbean pattern with dry and wet seasons
SEASONS = {
    'DJF': {'months': [12, 1, 2], 'label': 'Dry season 1'},
    'MAM': {'months': [3, 4, 5], 'label': 'Transition / first rains'},
    'JJA': {'months': [6, 7, 8], 'label': 'Dry season 2 (veranillo de San Juan)'},
    'SON': {'months': [9, 10, 11], 'label': 'Wet season (peak floods)'},
}

# Annual analysis windows
ANNUAL_WINDOWS = {year: {
    'start': f'{year}-01-01',
    'end': f'{year}-12-31',
} for year in range(2015, 2026)}

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

# Water detection thresholds for SAR (VV polarization)
# ADJUSTED for Bolivar: flat terrain = better SAR accuracy, fewer layover issues
SAR_WATER_THRESHOLDS = {
    'otsu_adaptive': True,  # Use Otsu automatic thresholding
    'vv_default': -15.0,  # dB, fallback threshold
    'vv_range': (-20.0, -12.0),  # Valid range for water detection
    'vh_default': -22.0,  # dB, fallback for VH
    'min_water_area_ha': 2.0,  # Increased to filter tidal noise near coast
    'speckle_filter_radius': 50,  # meters, focal median radius
}

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

# OpenStreetMap-based roads (via GEE community)
GRIP_ROADS = 'projects/sat-io/open-datasets/GRIP4/Africa-Caribbean'

# ============================================================================
# FLOOD RISK MODEL PARAMETERS
# ============================================================================

# HAND thresholds for flood susceptibility
# ADJUSTED for Bolivar: relaxed thresholds for flat lowland terrain
# (broader floodplains, lower elevations throughout)
HAND_CLASSES = {
    'very_high': {'range': (0, 10), 'label': 'Very High', 'color': '#d73027'},
    'high': {'range': (10, 20), 'label': 'High', 'color': '#fc8d59'},
    'moderate': {'range': (20, 40), 'label': 'Moderate', 'color': '#fee08b'},
    'low': {'range': (40, 70), 'label': 'Low', 'color': '#d9ef8b'},
    'very_low': {'range': (70, 9999), 'label': 'Very Low', 'color': '#1a9850'},
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
        'num_leaves': 63,
        'min_child_samples': 20,
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
CV_PARAMS = {
    'n_splits': 5,  # Stratified spatial K-fold
    'test_size': 0.3,
    'random_state': 42,
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
    '#a65628',
]

# Map center for Bolivar
# Centered approximately on the department's geographic center
MAP_CENTER = {'lat': 8.6, 'lon': -74.1}
MAP_ZOOM = 8

# Figure DPI for publication
FIGURE_DPI = 600
FIGURE_FORMAT = ['pdf', 'png']

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Export scale (meters)
EXPORT_SCALE = 30

# Project paths
import pathlib
PROJECT_ROOT = pathlib.Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
FIGURES_DIR = OUTPUTS_DIR / 'figures'
TABLES_DIR = OUTPUTS_DIR / 'tables'
OVERLEAF_DIR = PROJECT_ROOT / 'overleaf'
LOGS_DIR = PROJECT_ROOT / 'logs'
