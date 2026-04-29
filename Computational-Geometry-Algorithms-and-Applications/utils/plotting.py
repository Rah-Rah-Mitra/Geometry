"""Plotting helpers with stable styling for CGAA notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

from .artifacts import save_matplotlib


COLORS = {
    "ink": "#202124",
    "blue": "#2f6fed",
    "teal": "#0f9d8f",
    "orange": "#d97706",
    "red": "#c2410c",
    "green": "#3f7d20",
    "purple": "#6d5bd0",
    "gray": "#6b7280",
    "light": "#f3f4f6",
}


def new_axes(*, figsize: tuple[float, float] = (7.2, 5.2), title: str | None = None):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_facecolor("#ffffff")
    for spine in ax.spines.values():
        spine.set_color("#d1d5db")
    if title:
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    return fig, ax


def finish_axes(ax, *, margin: float = 0.8) -> None:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y0 - margin, y1 + margin)
    ax.tick_params(labelsize=8)


def plot_points(ax, points: np.ndarray, *, labels: Iterable[str] | None = None, color: str = COLORS["blue"], size: int = 42) -> None:
    pts = np.asarray(points, dtype=float)
    ax.scatter(pts[:, 0], pts[:, 1], s=size, c=color, edgecolor="white", linewidth=0.8, zorder=5)
    if labels is not None:
        for point, label in zip(pts, labels):
            ax.text(point[0] + 0.05, point[1] + 0.05, str(label), fontsize=8, color=COLORS["ink"])


def plot_polyline(ax, points: np.ndarray, *, closed: bool = False, color: str = COLORS["ink"], linewidth: float = 2.2, label: str | None = None) -> None:
    pts = np.asarray(points, dtype=float)
    if closed:
        pts = np.vstack([pts, pts[0]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth, label=label)


def plot_segments(ax, segments, *, color: str = COLORS["ink"], linewidth: float = 2.0, alpha: float = 1.0) -> None:
    for start, end in segments:
        xs = [start[0], end[0]]
        ys = [start[1], end[1]]
        ax.plot(xs, ys, color=color, linewidth=linewidth, alpha=alpha)


def annotate(ax, text: str, xy: tuple[float, float], *, color: str = COLORS["ink"]) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=(xy[0] + 0.15, xy[1] + 0.2),
        fontsize=8,
        color=color,
        arrowprops={"arrowstyle": "->", "color": color, "linewidth": 0.8},
    )


def save_figure(fig, path: Path) -> Path:
    result = save_matplotlib(fig, path)
    plt.close(fig)
    return result
