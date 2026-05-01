"""Shared plotting helpers for differential geometry notebooks."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

COURSE_COLORS = {
    "ink": "#17202a",
    "blue": "#2563eb",
    "red": "#dc2626",
    "green": "#059669",
    "gold": "#b7791f",
    "violet": "#7c3aed",
    "slate": "#475569",
}


def set_course_style() -> None:
    """Apply a quiet plotting style that works in notebooks and saved PNGs."""

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#cbd5e1",
            "axes.labelcolor": COURSE_COLORS["ink"],
            "axes.titleweight": "bold",
            "axes.grid": True,
            "grid.color": "#e2e8f0",
            "grid.linewidth": 0.8,
            "font.size": 10,
            "legend.frameon": False,
            "savefig.facecolor": "white",
        }
    )


def equalize_3d_axes(ax: Any, xs: Iterable[float], ys: Iterable[float], zs: Iterable[float], pad: float = 0.05) -> None:
    """Set equal 3D axis limits around the supplied coordinates."""

    arrays = [np.asarray(list(values), dtype=float) for values in (xs, ys, zs)]
    centers = [float(np.nanmean(values)) for values in arrays]
    spans = [float(np.nanmax(values) - np.nanmin(values)) for values in arrays]
    radius = max(spans) * (0.5 + pad)
    for setter, center in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), centers, strict=True):
        setter(center - radius, center + radius)


def finish_axes(ax: Any, title: str, xlabel: str = "x", ylabel: str = "y") -> None:
    """Apply common labels and title to 2D axes."""

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_aspect("equal", adjustable="box")


def surface_colors(values: np.ndarray, cmap: str = "viridis") -> Any:
    """Map scalar values to Matplotlib RGBA colors."""

    normed = values - np.nanmin(values)
    span = float(np.nanmax(normed)) or 1.0
    return plt.get_cmap(cmap)(normed / span)
