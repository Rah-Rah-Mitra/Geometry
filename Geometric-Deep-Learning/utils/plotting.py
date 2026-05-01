"""Plotting defaults and small drawing helpers."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


COURSE_COLORS = {
    "ink": "#1f2933",
    "blue": "#2a6fbb",
    "green": "#2f8f6f",
    "gold": "#b7791f",
    "red": "#c2413a",
    "purple": "#6d5bd0",
    "gray": "#667085",
}


def set_theme() -> None:
    """Apply a restrained plotting theme."""
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#d0d5dd",
            "axes.labelcolor": COURSE_COLORS["ink"],
            "axes.titlecolor": COURSE_COLORS["ink"],
            "font.size": 10,
            "axes.grid": True,
            "grid.color": "#e4e7ec",
            "grid.linewidth": 0.7,
            "legend.frameon": False,
        }
    )


def simple_signal(n: int = 32) -> np.ndarray:
    """A reusable toy signal with two localized structures."""
    y, x = np.mgrid[:n, :n]
    blob = np.exp(-((x - 10) ** 2 + (y - 13) ** 2) / 24)
    ridge = np.exp(-((x + y - 42) ** 2) / 30)
    return blob + 0.7 * ridge


def close_fig(fig: plt.Figure) -> plt.Figure:
    """Close a figure after saving while returning it for fluent notebook code."""
    plt.close(fig)
    return fig

