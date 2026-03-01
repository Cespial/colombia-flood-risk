#!/usr/bin/env python3
"""
utils.py
========
Shared utility functions for the Bolivar Flood Risk Assessment project.

Provides reusable helpers for:
  - Study area retrieval (department and municipal boundaries from FAO GAUL)
  - SAR speckle filtering
  - Terrain-derived indices (HAND, TWI, SPI)
  - Logging configuration
  - Safe GEE calls and export helpers

Usage:
    from utils import get_study_area, get_municipalities, setup_logging

Author : Bolivar Flood Risk Research Project
Date   : 2026-03
"""

import sys
import logging
import pathlib
import time
from typing import Optional, List, Dict, Any

import ee

# ---------------------------------------------------------------------------
# Resolve project root so we can import gee_config from any working directory
# ---------------------------------------------------------------------------
_SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import gee_config as cfg  # noqa: E402  (after path manipulation)


# ===========================================================================
# LOGGING
# ===========================================================================

def setup_logging(
    name: str,
    level: int = logging.INFO,
    log_dir: Optional[pathlib.Path] = None,
) -> logging.Logger:
    """
    Configure a logger that writes to both the console and a rotating log file.

    Parameters
    ----------
    name : str
        Logger name (typically ``__name__`` of the calling module).
    level : int
        Logging level (default ``logging.INFO``).
    log_dir : pathlib.Path, optional
        Directory for log files.  Defaults to ``<project_root>/logs/``.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    log_dir = log_dir or cfg.LOGS_DIR
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        "%(asctime)s | %(name)-28s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File handler
    log_file = log_dir / f"{name.replace('.', '_')}.log"
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger


_log = setup_logging("utils")


# ===========================================================================
# STUDY AREA HELPERS
# ===========================================================================

def get_study_area() -> ee.FeatureCollection:
    """
    Return the Bolivar department boundary from FAO GAUL Level 1.

    Returns
    -------
    ee.FeatureCollection
        Bolivar department polygon.
    """
    bolivar = (
        ee.FeatureCollection(cfg.ADMIN_DATASET)
        .filter(ee.Filter.eq("ADM0_NAME", cfg.COUNTRY_NAME))
        .filter(ee.Filter.eq("ADM1_NAME", cfg.DEPARTMENT_NAME))
    )
    _log.info("Study area loaded: %s from %s", cfg.DEPARTMENT_NAME, cfg.ADMIN_DATASET)
    return bolivar


def get_study_area_geometry() -> ee.Geometry:
    """
    Return the dissolved geometry of Bolivar as a single ``ee.Geometry``.

    Returns
    -------
    ee.Geometry
        Dissolved Bolivar boundary.
    """
    return get_study_area().geometry().dissolve()


def get_municipalities() -> ee.FeatureCollection:
    """
    Return all municipalities within Bolivar from FAO GAUL Level 2.

    Returns
    -------
    ee.FeatureCollection
        ~46 municipality polygons with properties including ``ADM2_NAME``.
    """
    municipalities = (
        ee.FeatureCollection(cfg.MUNICIPAL_DATASET)
        .filter(ee.Filter.eq("ADM0_NAME", cfg.COUNTRY_NAME))
        .filter(ee.Filter.eq("ADM1_NAME", cfg.DEPARTMENT_NAME))
    )
    _log.info("Municipalities loaded from %s", cfg.MUNICIPAL_DATASET)
    return municipalities


def get_subregion_municipalities(subregion_name: str) -> ee.FeatureCollection:
    """
    Filter municipalities belonging to a specific Bolivar subregion (ZODES).

    Parameters
    ----------
    subregion_name : str
        One of the 6 ZODES defined in ``gee_config.SUBREGIONS``
        (e.g. ``'Dique'``, ``'Mojana'``).

    Returns
    -------
    ee.FeatureCollection
        Municipalities in the requested subregion.

    Raises
    ------
    ValueError
        If *subregion_name* is not found in ``gee_config.SUBREGIONS``.
    """
    if subregion_name not in cfg.SUBREGIONS:
        valid = list(cfg.SUBREGIONS.keys())
        raise ValueError(
            f"Unknown subregion '{subregion_name}'. Valid options: {valid}"
        )

    mun_names = cfg.SUBREGIONS[subregion_name]
    all_municipalities = get_municipalities()
    subregion_fc = all_municipalities.filter(
        ee.Filter.inList("ADM2_NAME", mun_names)
    )
    _log.info(
        "Subregion '%s': filtered %d municipalities",
        subregion_name,
        len(mun_names),
    )
    return subregion_fc


# ===========================================================================
# SAR SPECKLE FILTERING
# ===========================================================================

def apply_speckle_filter(image: ee.Image, radius_m: int = 50) -> ee.Image:
    """
    Apply a focal median speckle filter to a SAR image.

    Parameters
    ----------
    image : ee.Image
        Input SAR image (e.g. Sentinel-1 GRD in dB scale).
    radius_m : int
        Radius of the focal median kernel in **meters** (default 50 m).

    Returns
    -------
    ee.Image
        Speckle-filtered image with the same band names and properties.
    """
    filtered = image.focal_median(
        radius=radius_m,
        kernelType="circle",
        units="meters",
    )
    return filtered.copyProperties(image, image.propertyNames())


# ===========================================================================
# TERRAIN-DERIVED INDICES
# ===========================================================================

def _get_merit_hydro() -> ee.Image:
    """
    Load the MERIT Hydro dataset.

    Returns
    -------
    ee.Image
        MERIT Hydro multi-band image.
    """
    return ee.Image(cfg.MERIT_HYDRO)


def compute_hand(dem: ee.Image, region: ee.Geometry) -> ee.Image:
    """
    Retrieve Height Above Nearest Drainage (HAND) from MERIT Hydro.

    Parameters
    ----------
    dem : ee.Image
        Digital elevation model (unused; kept for API compatibility).
    region : ee.Geometry
        Region of interest.

    Returns
    -------
    ee.Image
        Single-band image named ``'hand'`` in meters.
    """
    merit = _get_merit_hydro()
    hand = merit.select("hnd").rename("hand").clip(region)
    _log.info("HAND loaded from MERIT Hydro (pre-computed)")
    return hand


def compute_twi(dem: ee.Image) -> ee.Image:
    """
    Compute the Topographic Wetness Index (TWI).

    TWI = ln(a / tan(beta))

    Parameters
    ----------
    dem : ee.Image
        Digital elevation model.

    Returns
    -------
    ee.Image
        Single-band image named ``'twi'`` (dimensionless).
    """
    slope_rad = ee.Terrain.slope(dem).multiply(3.14159265 / 180.0)
    slope_clamped = slope_rad.max(0.00873)  # ~0.5 deg

    merit = _get_merit_hydro()
    upstream_area_km2 = merit.select("upa")

    cell_width = 90  # MERIT Hydro resolution in meters
    specific_area = upstream_area_km2.multiply(1e6).divide(cell_width).max(1)

    twi = specific_area.divide(slope_clamped.tan()).log().rename("twi")
    _log.info("TWI computed using MERIT Hydro upstream area")
    return twi


def compute_spi(dem: ee.Image) -> ee.Image:
    """
    Compute the Stream Power Index (SPI).

    SPI = a * tan(beta)

    Parameters
    ----------
    dem : ee.Image
        Digital elevation model.

    Returns
    -------
    ee.Image
        Single-band image named ``'spi'`` (dimensionless).
    """
    slope_rad = ee.Terrain.slope(dem).multiply(3.14159265 / 180.0)

    merit = _get_merit_hydro()
    upstream_area_km2 = merit.select("upa")

    cell_width = 90  # MERIT Hydro resolution in meters
    specific_area = upstream_area_km2.multiply(1e6).divide(cell_width).max(1)

    spi = specific_area.multiply(slope_rad.tan()).rename("spi")
    _log.info("SPI computed using MERIT Hydro upstream area")
    return spi


# ===========================================================================
# SAFE GEE CALLS
# ===========================================================================

def safe_getinfo(
    ee_obj: Any,
    label: str = "object",
    max_retries: int = 3,
    backoff_s: float = 5.0,
) -> Any:
    """
    Safely call ``.getInfo()`` on a GEE object with retries.

    Parameters
    ----------
    ee_obj : ee.ComputedObject
        Any Earth Engine object that supports ``.getInfo()``.
    label : str
        Descriptive label for logging messages.
    max_retries : int
        Maximum number of attempts.
    backoff_s : float
        Initial back-off duration in seconds.

    Returns
    -------
    Any
        The Python-side result of ``.getInfo()``.
    """
    wait = backoff_s
    for attempt in range(1, max_retries + 1):
        try:
            result = ee_obj.getInfo()
            _log.debug("getInfo succeeded for '%s' on attempt %d", label, attempt)
            return result
        except ee.EEException as exc:
            _log.warning(
                "getInfo failed for '%s' (attempt %d/%d): %s",
                label, attempt, max_retries, exc,
            )
            if attempt == max_retries:
                _log.error("All %d retries exhausted for '%s'", max_retries, label)
                raise
            time.sleep(wait)
            wait *= 2


# ===========================================================================
# EXPORT HELPERS
# ===========================================================================

def export_to_drive(
    image: ee.Image,
    description: str,
    region: ee.Geometry,
    scale: int = cfg.EXPORT_SCALE,
    folder: str = "bolivar_flood_risk",
    crs: str = "EPSG:4326",
    max_pixels: int = 1e13,
) -> ee.batch.Task:
    """
    Export an ``ee.Image`` to Google Drive as a GeoTIFF.

    Parameters
    ----------
    image : ee.Image
        Image to export.
    description : str
        Task description (also used as filename prefix).
    region : ee.Geometry
        Export region.
    scale : int
        Spatial resolution in meters.
    folder : str
        Google Drive folder name.
    crs : str
        Coordinate reference system.
    max_pixels : int
        Maximum number of pixels per export.

    Returns
    -------
    ee.batch.Task
        The started export task.
    """
    safe_desc = (
        description.replace(" ", "_")
        .replace(".", "_")
        .replace("/", "_")
    )

    task = ee.batch.Export.image.toDrive(
        image=image,
        description=safe_desc,
        folder=folder,
        region=region,
        scale=scale,
        crs=crs,
        maxPixels=int(max_pixels),
        fileFormat="GeoTIFF",
    )
    task.start()
    _log.info("Export task started: '%s' (scale=%d m, folder='%s')", safe_desc, scale, folder)
    return task


def export_table_to_drive(
    collection: ee.FeatureCollection,
    description: str,
    folder: str = "bolivar_flood_risk",
    file_format: str = "CSV",
) -> ee.batch.Task:
    """
    Export an ``ee.FeatureCollection`` to Google Drive.

    Parameters
    ----------
    collection : ee.FeatureCollection
        Feature collection to export.
    description : str
        Task description / filename prefix.
    folder : str
        Google Drive folder name.
    file_format : str
        ``'CSV'``, ``'GeoJSON'``, or ``'SHP'``.

    Returns
    -------
    ee.batch.Task
        The started export task.
    """
    safe_desc = description.replace(" ", "_").replace(".", "_").replace("/", "_")
    task = ee.batch.Export.table.toDrive(
        collection=collection,
        description=safe_desc,
        folder=folder,
        fileFormat=file_format,
    )
    task.start()
    _log.info("Table export started: '%s' (format=%s)", safe_desc, file_format)
    return task


# ===========================================================================
# MISCELLANEOUS HELPERS
# ===========================================================================

def get_dem() -> ee.Image:
    """
    Load the SRTM 30 m DEM clipped to Bolivar.

    Returns
    -------
    ee.Image
        Elevation image (band ``'elevation'``) in meters.
    """
    region = get_study_area_geometry()
    dem = ee.Image(cfg.SRTM).clip(region)
    return dem


def classify_by_thresholds(
    image: ee.Image,
    band: str,
    thresholds: Dict[str, Dict],
) -> ee.Image:
    """
    Reclassify a continuous image into discrete classes.

    Parameters
    ----------
    image : ee.Image
        Source image.
    band : str
        Band name to classify.
    thresholds : dict
        Mapping of class names to ``{'range': (low, high), ...}`` dicts.

    Returns
    -------
    ee.Image
        Integer-classified image (1-based).
    """
    src = image.select(band)
    classified = ee.Image(0).rename("class")
    for idx, (_, cls) in enumerate(thresholds.items(), start=1):
        low, high = cls["range"]
        mask = src.gte(low).And(src.lt(high))
        classified = classified.where(mask, idx)
    return classified.selfMask()


def monitor_tasks(tasks: List[ee.batch.Task], poll_interval_s: int = 30) -> None:
    """
    Block and print progress until all export tasks complete or fail.

    Parameters
    ----------
    tasks : list[ee.batch.Task]
        List of active GEE export tasks.
    poll_interval_s : int
        Seconds between status checks.
    """
    remaining = list(tasks)
    while remaining:
        still_running = []
        for task in remaining:
            status = task.status()
            state = status.get("state", "UNKNOWN")
            desc = status.get("description", "?")
            if state in ("COMPLETED", "FAILED", "CANCELLED"):
                _log.info("Task '%s' finished with state: %s", desc, state)
            else:
                still_running.append(task)
        remaining = still_running
        if remaining:
            _log.info("%d task(s) still running ...", len(remaining))
            time.sleep(poll_interval_s)
    _log.info("All tasks completed.")


# ===========================================================================
# MODULE SELF-TEST
# ===========================================================================

def _self_test() -> None:
    """Quick smoke test: verify GEE connectivity and study area loading."""
    _log.info("Running utils self-test ...")

    bolivar = get_study_area()
    n_features = safe_getinfo(bolivar.size(), label="bolivar.size()")
    _log.info("Bolivar feature count: %s", n_features)

    munis = get_municipalities()
    n_munis = safe_getinfo(munis.size(), label="municipalities.size()")
    _log.info("Municipality count: %s", n_munis)

    dique = get_subregion_municipalities("Dique")
    n_dique = safe_getinfo(dique.size(), label="dique.size()")
    _log.info("Dique municipalities: %s", n_dique)

    dem = get_dem()
    _log.info("DEM loaded: %s", safe_getinfo(dem.bandNames(), label="dem.bandNames()"))

    _log.info("Self-test passed.")


if __name__ == "__main__":
    _self_test()
