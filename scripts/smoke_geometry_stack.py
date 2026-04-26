"""Smoke test for the Geometry notebook environment.

This script intentionally writes small artifacts that notebooks can later load
without embedding large outputs in notebook cells.
"""

# ruff: noqa: E402

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib

matplotlib.use("Agg")

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import pyvista as pv
import shapely.geometry as geom
import trimesh

from utils.artifacts import artifact_dir, save_json, save_matplotlib, save_plotly_html


MODULES = [
    "cv2",
    "ezdxf",
    "fiona",
    "folium",
    "geomloss",
    "geomstats",
    "gpytoolbox",
    "imageio",
    "kornia",
    "manifold3d",
    "mapbox_earcut",
    "meshio",
    "networkx",
    "osmnx",
    "pandas",
    "polars",
    "potpourri3d",
    "pyarrow",
    "pycolmap",
    "pydeck",
    "pyogrio",
    "pyproj",
    "pyriemann",
    "rasterio",
    "robust_laplacian",
    "scipy",
    "skimage",
    "sklearn",
    "statsmodels",
    "sympy",
    "taichi",
    "torch",
    "torchvision",
    "xarray",
    "xatlas",
    "zarr",
]


def import_smoke() -> dict[str, str]:
    versions: dict[str, str] = {}
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        versions[module_name] = str(getattr(module, "__version__", "unknown"))
    return versions


def write_matplotlib_artifact() -> Path:
    t = np.linspace(0, 2 * np.pi, 200)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(np.cos(t), np.sin(t), label="unit circle")
    ax.set_aspect("equal")
    ax.set_title("Geometry smoke test")
    ax.legend(loc="upper right")
    path = save_matplotlib(fig, "smoke-test", "plots", "unit-circle.png")
    plt.close(fig)
    return path


def write_plotly_artifact() -> Path:
    theta = np.linspace(0, 2 * np.pi, 80)
    fig = px.line_3d(
        x=np.cos(theta),
        y=np.sin(theta),
        z=theta / (2 * np.pi),
        title="Helix smoke test",
    )
    return save_plotly_html(fig, "smoke-test", "plots", "helix.html")


def write_mesh_artifact() -> Path:
    sphere = trimesh.creation.icosphere(subdivisions=2, radius=1.0)
    mesh = pv.wrap(sphere)
    out_dir = artifact_dir("smoke-test", "meshes")
    path = out_dir / "icosphere.ply"
    mesh.save(path)
    return path


def write_gis_artifact() -> Path:
    frame = gpd.GeoDataFrame(
        {"name": ["origin-buffer"], "value": [1.0]},
        geometry=[geom.Point(0, 0).buffer(1.0)],
        crs="EPSG:4326",
    )
    out_dir = artifact_dir("smoke-test", "gis")
    path = out_dir / "origin-buffer.geojson"
    frame.to_file(path, driver="GeoJSON")
    return path


def main() -> None:
    versions = import_smoke()
    artifacts = {
        "matplotlib_png": str(write_matplotlib_artifact()),
        "plotly_html": str(write_plotly_artifact()),
        "mesh_ply": str(write_mesh_artifact()),
        "gis_geojson": str(write_gis_artifact()),
    }
    metadata_path = save_json(
        {"versions": versions, "artifacts": artifacts},
        "smoke-test",
        "metadata",
        "environment.json",
    )

    print(json.dumps({"status": "ok", "metadata": str(metadata_path), "artifacts": artifacts}, indent=2))


if __name__ == "__main__":
    main()
