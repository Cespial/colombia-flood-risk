#!/usr/bin/env python3
"""
07_visualization.py
===================
Publication-quality figure generation for the Bolivar Flood Risk Assessment.

Generates key figures at 600 DPI (PDF + PNG) following journal formatting:
  - Font: Times New Roman / Liberation Serif, 10pt
  - Single column: 89 mm; double column: 183 mm
  - Colorblind-safe palettes (viridis, cividis, custom)
  - Scale bars, north arrows, and proper CRS on all maps

Figures:
  Fig 1  - Study area map (Bolivar, municipalities, rivers, elevation)
  Fig 2  - SAR flood frequency map
  Fig 3  - JRC Global Surface Water occurrence map
  Fig 4  - Flood susceptibility map (ensemble model)
  Fig 5  - Population exposure by municipality (bar chart)
  Fig 6  - SHAP feature importance (bar plot)
  Fig 7  - ENSO comparison (box plot)

Outputs saved to:
  - outputs/figures/ (PDF + PNG)
  - overleaf/figures/ (PDF + PNG)

Usage:
  python scripts/07_visualization.py

Author: Flood Risk Research Project
"""

import sys
import pathlib
import warnings
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib_scalebar.scalebar import ScaleBar
import seaborn as sns

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from gee_config import (
    SUBREGIONS, SUBREGION_PALETTE, RISK_PALETTE, WATER_PALETTE,
    HAND_CLASSES, FLOOD_FREQUENCY_CLASSES,
    FIGURE_DPI, FIGURE_FORMAT,
    SEASONS,
)
from utils import (
    setup_logging, ensure_dirs,
    set_publication_style, save_figure,
    figsize_single, figsize_double,
    load_bolivar_boundary, load_municipalities, load_subregions,
    load_river_basins,
    FIGURES_DIR, TABLES_DIR, OUTPUTS_DIR, OVERLEAF_FIGURES,
    CRS_WGS84, CRS_COLOMBIA,
    SINGLE_COL_MM, DOUBLE_COL_MM, MM_TO_INCH,
)

logger = setup_logging("07_visualization")

# Suppress non-critical warnings from geopandas/matplotlib
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=FutureWarning, module="geopandas")


# ============================================================================
# Map Annotation Helpers
# ============================================================================

def add_north_arrow(ax, x: float = 0.95, y: float = 0.95, size: float = 15) -> None:
    """Add a north arrow to a map axis."""
    ax.annotate(
        "N",
        xy=(x, y),
        xycoords="axes fraction",
        fontsize=size,
        fontweight="bold",
        ha="center", va="center",
        path_effects=[pe.withStroke(linewidth=2, foreground="white")],
    )
    ax.annotate(
        "",
        xy=(x, y - 0.01),
        xytext=(x, y - 0.07),
        xycoords="axes fraction",
        arrowprops=dict(arrowstyle="->", lw=1.5, color="black"),
    )


def add_scalebar(ax, length_km: float = 50, location: str = "lower left") -> None:
    """Add a scale bar to a projected map axis."""
    try:
        sb = ScaleBar(
            1, units="m", location=location,
            length_fraction=0.2, font_properties={"size": 8},
            box_alpha=0.7, pad=0.3, sep=2,
        )
        ax.add_artist(sb)
    except Exception:
        ax.annotate(
            f"{length_km} km", xy=(0.05, 0.05), xycoords="axes fraction",
            fontsize=7, ha="left",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
        )


def _load_or_synthesize_raster(
    phase: str, filename: str, shape: Tuple[int, int] = (500, 400),
    vmin: float = 0, vmax: float = 1,
) -> np.ndarray:
    """Load a raster or return a synthetic placeholder array."""
    path = OUTPUTS_DIR / phase / filename
    if path.exists():
        try:
            import rasterio
            with rasterio.open(path) as src:
                return src.read(1)
        except Exception as exc:
            logger.warning("Failed to read raster %s: %s", path, exc)

    logger.warning("Raster %s/%s not found; using synthetic placeholder.", phase, filename)
    np.random.seed(hash(filename) % (2**31))
    return np.random.uniform(vmin, vmax, size=shape)


def _load_or_synthesize_df(phase: str, filename: str, columns: dict) -> pd.DataFrame:
    """Load a CSV from outputs or generate a synthetic DataFrame."""
    path = OUTPUTS_DIR / phase / filename
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception as exc:
            logger.warning("Failed to read %s: %s", path, exc)
    tpath = TABLES_DIR / filename
    if tpath.exists():
        try:
            return pd.read_csv(tpath)
        except Exception:
            pass
    logger.warning("CSV %s/%s not found; using synthetic placeholder.", phase, filename)
    np.random.seed(42)
    data = {}
    for col_name, (gen_func, kwargs) in columns.items():
        data[col_name] = gen_func(**kwargs)
    return pd.DataFrame(data)


# ============================================================================
# Figure 1: Study Area Map
# ============================================================================

def fig01_study_area() -> None:
    """Study area map showing Bolivar department with municipalities."""
    logger.info("Generating Figure 1: Study area map...")
    set_publication_style()

    bolivar = load_bolivar_boundary("gadm")
    municipalities = load_municipalities("gadm")

    bolivar_proj = bolivar.to_crs(CRS_COLOMBIA)
    municipalities_proj = municipalities.to_crs(CRS_COLOMBIA)

    fig, axes = plt.subplots(
        1, 2, figsize=figsize_double(0.6),
        gridspec_kw={"width_ratios": [1, 2.5]},
    )

    # --- Panel (a): Colombia context ---
    ax_context = axes[0]
    try:
        from utils import BOUNDARIES_DIR
        col_depts = gpd.read_file(
            BOUNDARIES_DIR / "colombia_all_departments_naturalearth.geojson"
        ).to_crs(CRS_COLOMBIA)
        col_depts.plot(ax=ax_context, color="#f0f0f0", edgecolor="#999999", linewidth=0.3)
        bolivar_proj.plot(ax=ax_context, color="#fc8d59", edgecolor="black", linewidth=0.8)
    except Exception:
        bolivar_proj.plot(ax=ax_context, color="#fc8d59", edgecolor="black", linewidth=0.8)

    ax_context.set_title("(a) Location", fontsize=9, fontweight="bold")
    ax_context.set_axis_off()

    # --- Panel (b): Bolivar municipalities ---
    ax_main = axes[1]
    municipalities_proj.plot(
        ax=ax_main, facecolor="#e0ecf4", edgecolor="#666666", linewidth=0.3,
    )
    bolivar_proj.boundary.plot(ax=ax_main, color="black", linewidth=1.2)

    ax_main.set_title("(b) Bolivar municipalities", fontsize=9, fontweight="bold")
    add_north_arrow(ax_main)
    add_scalebar(ax_main, length_km=50)
    ax_main.set_axis_off()

    fig.tight_layout()
    save_figure(fig, "fig01_study_area")
    plt.close(fig)
    logger.info("  Figure 1 saved.")


# ============================================================================
# Figure 2: SAR Flood Frequency Map
# ============================================================================

def fig02_sar_flood_frequency() -> None:
    """SAR-based flood frequency map for Bolivar."""
    logger.info("Generating Figure 2: SAR flood frequency map...")
    set_publication_style()

    bolivar = load_bolivar_boundary("gadm").to_crs(CRS_COLOMBIA)

    flood_freq = _load_or_synthesize_raster(
        "phase2_flood_frequency", "flood_frequency_percent.tif",
        shape=(600, 500), vmin=0, vmax=100,
    )

    class_info = FLOOD_FREQUENCY_CLASSES
    boundaries = [0, 1, 10, 25, 50, 75, 100]
    colors = [v["color"] for v in class_info.values()]
    cmap = ListedColormap(colors)
    norm = BoundaryNorm(boundaries, cmap.N)

    fig, ax = plt.subplots(figsize=figsize_single(1.1))
    bolivar.plot(ax=ax, facecolor="#f0f0f0", edgecolor="black", linewidth=0.8)
    bounds = bolivar.total_bounds
    ax.imshow(
        flood_freq,
        extent=[bounds[0], bounds[2], bounds[1], bounds[3]],
        origin="upper", cmap=cmap, norm=norm, alpha=0.85, aspect="equal",
    )
    bolivar.boundary.plot(ax=ax, color="black", linewidth=1.0)

    legend_patches = [
        mpatches.Patch(color=v["color"], label=v["label"]) for v in class_info.values()
    ]
    ax.legend(
        handles=legend_patches, loc="lower left", fontsize=7,
        title="Flood Frequency", title_fontsize=8,
        frameon=True, framealpha=0.9,
    )
    ax.set_title("Flood Frequency (Sentinel-1 SAR, 2015--2025), Bolivar", fontsize=10)
    add_north_arrow(ax)
    add_scalebar(ax)
    ax.set_axis_off()

    fig.tight_layout()
    save_figure(fig, "fig02_sar_flood_frequency")
    plt.close(fig)
    logger.info("  Figure 2 saved.")


# ============================================================================
# Figure 3: JRC Water Occurrence Map
# ============================================================================

def fig03_jrc_water_occurrence() -> None:
    """JRC Global Surface Water occurrence map for Bolivar."""
    logger.info("Generating Figure 3: JRC water occurrence map...")
    set_publication_style()

    bolivar = load_bolivar_boundary("gadm").to_crs(CRS_COLOMBIA)

    jrc_data = _load_or_synthesize_raster(
        "phase1_water_maps", "jrc_occurrence_bolivar.tif",
        shape=(600, 500), vmin=0, vmax=100,
    )

    fig, ax = plt.subplots(figsize=figsize_single(1.1))
    bolivar.plot(ax=ax, facecolor="#f5f5f5", edgecolor="black", linewidth=0.8)
    bounds = bolivar.total_bounds
    im = ax.imshow(
        jrc_data,
        extent=[bounds[0], bounds[2], bounds[1], bounds[3]],
        origin="upper", cmap="cividis", vmin=0, vmax=100,
        alpha=0.85, aspect="equal",
    )
    bolivar.boundary.plot(ax=ax, color="black", linewidth=1.0)

    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Water occurrence (%)", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    ax.set_title("JRC Global Surface Water Occurrence, Bolivar", fontsize=10)
    add_north_arrow(ax)
    add_scalebar(ax)
    ax.set_axis_off()

    fig.tight_layout()
    save_figure(fig, "fig03_jrc_water_occurrence")
    plt.close(fig)
    logger.info("  Figure 3 saved.")


# ============================================================================
# Figure 4: Flood Susceptibility Map (Ensemble)
# ============================================================================

def fig04_susceptibility_map() -> None:
    """Ensemble flood susceptibility map for Bolivar."""
    logger.info("Generating Figure 4: Flood susceptibility map...")
    set_publication_style()

    bolivar = load_bolivar_boundary("gadm").to_crs(CRS_COLOMBIA)

    suscept = _load_or_synthesize_raster(
        "phase3_risk_model", "flood_susceptibility_ensemble.tif",
        shape=(600, 500), vmin=0, vmax=1,
    )

    fig, ax = plt.subplots(figsize=figsize_single(1.1))
    bolivar.plot(ax=ax, facecolor="#f0f0f0", edgecolor="black", linewidth=0.8)
    bounds = bolivar.total_bounds
    cmap = mpl.colormaps.get_cmap("RdYlGn_r")
    im = ax.imshow(
        suscept,
        extent=[bounds[0], bounds[2], bounds[1], bounds[3]],
        origin="upper", cmap=cmap, vmin=0, vmax=1,
        alpha=0.85, aspect="equal",
    )
    bolivar.boundary.plot(ax=ax, color="black", linewidth=1.0)

    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Flood susceptibility probability", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    ax.set_title("Flood Susceptibility (Ensemble Model), Bolivar", fontsize=10)
    add_north_arrow(ax)
    add_scalebar(ax)
    ax.set_axis_off()

    fig.tight_layout()
    save_figure(fig, "fig04_flood_susceptibility")
    plt.close(fig)
    logger.info("  Figure 4 saved.")


# ============================================================================
# Figure 5: Population Exposure Bar Chart
# ============================================================================

def fig05_population_exposure() -> None:
    """Population exposure bar chart for top 20 municipalities."""
    logger.info("Generating Figure 5: Population exposure...")
    set_publication_style()

    exp_path = OUTPUTS_DIR / "phase4_municipal_stats" / "population_exposure.csv"
    if exp_path.exists():
        exposure = pd.read_csv(exp_path)
    else:
        logger.warning("  Population exposure data not found; using synthetic.")
        municipalities = load_municipalities("gadm")
        name_col = "NAME_2" if "NAME_2" in municipalities.columns else municipalities.columns[0]
        np.random.seed(42)
        exposure = pd.DataFrame({
            "municipality": municipalities[name_col].values,
            "population_total": np.random.randint(5000, 500000, len(municipalities)),
            "population_exposed": np.random.randint(100, 50000, len(municipalities)),
        })
        exposure["exposure_pct"] = (
            exposure["population_exposed"] / exposure["population_total"] * 100
        )

    top20 = exposure.nlargest(20, "population_exposed")

    fig, ax = plt.subplots(figsize=figsize_single(1.3))
    y_pos = range(len(top20))
    ax.barh(
        y_pos, top20["population_exposed"].values,
        color="#d73027", edgecolor="white", linewidth=0.3,
    )
    ax.set_yticks(y_pos)
    ax.set_yticklabels(top20["municipality"].values, fontsize=7)
    ax.set_xlabel("Population exposed to flood risk")
    ax.set_title("Top 20 Municipalities by Exposed Population, Bolivar", fontsize=10)
    ax.invert_yaxis()

    fig.tight_layout()
    save_figure(fig, "fig05_population_exposure")
    plt.close(fig)
    logger.info("  Figure 5 saved.")


# ============================================================================
# Figure 6: SHAP Feature Importance
# ============================================================================

def fig06_shap_importance() -> None:
    """SHAP feature importance bar plot."""
    logger.info("Generating Figure 6: SHAP feature importance...")
    set_publication_style()

    shap_path = OUTPUTS_DIR / "phase3_risk_model" / "shap_importance.csv"
    if shap_path.exists():
        shap_df = pd.read_csv(shap_path)
    else:
        from gee_config import SUSCEPTIBILITY_FEATURES
        logger.warning("  SHAP data not found; using synthetic placeholder.")
        np.random.seed(42)
        importance = np.sort(np.random.exponential(0.05, len(SUSCEPTIBILITY_FEATURES)))[::-1]
        shap_df = pd.DataFrame({
            "feature": SUSCEPTIBILITY_FEATURES,
            "mean_abs_shap": importance,
        })

    shap_df = shap_df.sort_values("mean_abs_shap", ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=figsize_single(1.2))
    ax.barh(
        shap_df["feature"], shap_df["mean_abs_shap"],
        color="#377eb8", edgecolor="white", linewidth=0.3,
    )
    ax.set_xlabel("Mean |SHAP value|")
    ax.set_title("Feature Importance (SHAP), Bolivar", fontsize=10)
    ax.tick_params(axis="y", labelsize=8)

    fig.tight_layout()
    save_figure(fig, "fig06_shap_importance")
    plt.close(fig)
    logger.info("  Figure 6 saved.")


# ============================================================================
# Figure 7: ENSO Comparison
# ============================================================================

def fig07_enso_comparison() -> None:
    """Box plot comparing flood extent by ENSO phase."""
    logger.info("Generating Figure 7: ENSO comparison...")
    set_publication_style()

    combined_path = TABLES_DIR / "enso_flood_combined.csv"
    if combined_path.exists():
        combined_df = pd.read_csv(combined_path)
    else:
        logger.warning("  ENSO-flood data not found; using synthetic.")
        np.random.seed(42)
        years = list(range(2015, 2026))
        enso_phases = ["El Nino", "El Nino", "Neutral", "Neutral", "Neutral",
                       "La Nina", "La Nina", "La Nina", "El Nino", "El Nino", "Neutral"]
        combined_df = pd.DataFrame({
            "year": years,
            "enso_phase": enso_phases,
            "annual_precip_mm": np.random.uniform(800, 2500, len(years)),
            "total_flood_area_km2": np.random.uniform(100, 600, len(years)),
        })

    fig, axes = plt.subplots(1, 2, figsize=figsize_double(0.45))
    order = ["La Nina", "Neutral", "El Nino"]
    palette = {"La Nina": "#2171b5", "Neutral": "#999999", "El Nino": "#d73027"}

    ax = axes[0]
    sns.boxplot(data=combined_df, x="enso_phase", y="annual_precip_mm",
                order=order, palette=palette, ax=ax, width=0.5)
    sns.stripplot(data=combined_df, x="enso_phase", y="annual_precip_mm",
                  order=order, color="k", size=4, ax=ax, alpha=0.7)
    ax.set_xlabel("ENSO Phase")
    ax.set_ylabel("Annual precipitation (mm)")
    ax.set_title("(a) Precipitation by ENSO phase, Bolivar")

    ax = axes[1]
    sns.boxplot(data=combined_df, x="enso_phase", y="total_flood_area_km2",
                order=order, palette=palette, ax=ax, width=0.5)
    sns.stripplot(data=combined_df, x="enso_phase", y="total_flood_area_km2",
                  order=order, color="k", size=4, ax=ax, alpha=0.7)
    ax.set_xlabel("ENSO Phase")
    ax.set_ylabel("Annual flood extent (km$^2$)")
    ax.set_title("(b) Flood extent by ENSO phase, Bolivar")

    fig.tight_layout()
    save_figure(fig, "fig07_enso_flood_comparison")
    plt.close(fig)
    logger.info("  Figure 7 saved.")


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    """Generate all publication-quality figures."""
    logger.info("=" * 70)
    logger.info("PUBLICATION FIGURE GENERATION - BOLIVAR FLOOD RISK ASSESSMENT")
    logger.info("=" * 70)

    ensure_dirs()
    set_publication_style()

    figure_functions = [
        fig01_study_area,
        fig02_sar_flood_frequency,
        fig03_jrc_water_occurrence,
        fig04_susceptibility_map,
        fig05_population_exposure,
        fig06_shap_importance,
        fig07_enso_comparison,
    ]

    for func in figure_functions:
        try:
            func()
        except Exception as exc:
            logger.error("Failed to generate %s: %s", func.__name__, exc, exc_info=True)

    logger.info("=" * 70)
    logger.info("Figure generation complete. Outputs in:")
    logger.info("  - %s", FIGURES_DIR)
    logger.info("  - %s", OVERLEAF_FIGURES)
    logger.info("=" * 70)


if __name__ == "__main__":
    main()
