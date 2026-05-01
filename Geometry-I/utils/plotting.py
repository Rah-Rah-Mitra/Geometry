"""Stable plotting helpers for Geometry I notebooks."""

from __future__ import annotations

from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "ink": "#222831",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#5a8f3c",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
    "light": "#eef2f6",
}


def new_axes(*, figsize: tuple[float, float] = (7.4, 5.2), title: str | None = None, equal: bool = True):
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(True, color="#dfe5ec", linewidth=0.75)
    ax.set_facecolor("#ffffff")
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#bac4cf")
    if title:
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=COLORS["ink"])
    ax.tick_params(labelsize=8, colors=COLORS["gray"])
    return fig, ax


def plot_points(
    ax,
    points: np.ndarray,
    *,
    labels: Iterable[str] | None = None,
    color: str = COLORS["blue"],
    size: int = 46,
) -> None:
    pts = np.asarray(points, dtype=float)
    ax.scatter(pts[:, 0], pts[:, 1], s=size, c=color, edgecolor="white", linewidth=0.8, zorder=5)
    if labels is not None:
        for point, label in zip(pts, labels):
            ax.text(point[0] + 0.05, point[1] + 0.05, str(label), fontsize=8, color=COLORS["ink"])


def plot_polyline(
    ax,
    points: np.ndarray,
    *,
    closed: bool = False,
    color: str = COLORS["ink"],
    linewidth: float = 2.0,
    label: str | None = None,
    alpha: float = 1.0,
) -> None:
    pts = np.asarray(points, dtype=float)
    if closed:
        pts = np.vstack([pts, pts[0]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth, label=label, alpha=alpha)


def plot_segments(
    ax,
    segments: Iterable[tuple[Iterable[float], Iterable[float]]],
    *,
    color: str = COLORS["ink"],
    linewidth: float = 1.8,
    alpha: float = 1.0,
) -> None:
    for start, end in segments:
        s = np.asarray(start, dtype=float)
        e = np.asarray(end, dtype=float)
        ax.plot([s[0], e[0]], [s[1], e[1]], color=color, linewidth=linewidth, alpha=alpha)


def annotate(ax, text: str, xy: tuple[float, float], *, color: str = COLORS["ink"]) -> None:
    ax.annotate(
        text,
        xy=xy,
        xytext=(xy[0] + 0.18, xy[1] + 0.22),
        fontsize=8,
        color=color,
        arrowprops={"arrowstyle": "->", "color": color, "linewidth": 0.9},
    )


def draw_circle(ax, center: tuple[float, float], radius: float, *, color: str = COLORS["blue"], label: str | None = None) -> None:
    circle = plt.Circle(center, radius, fill=False, color=color, linewidth=1.8, label=label)
    ax.add_patch(circle)


def draw_projective_line(ax, values: Iterable[float], *, title: str = "projective line chart") -> None:
    ax.axhline(0, color=COLORS["ink"], linewidth=1.4)
    for value in values:
        ax.scatter([value], [0], color=COLORS["blue"], zorder=5)
        ax.text(value, 0.08, f"{value:g}", ha="center", fontsize=8)
    ax.scatter([3.0], [0], marker=">", color=COLORS["red"], zorder=5)
    ax.text(3.0, 0.08, "infinity", ha="center", fontsize=8, color=COLORS["red"])
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.set_ylim(-0.5, 0.6)
    ax.set_yticks([])


def finish_axes(ax, *, margin: float = 0.35) -> None:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    dx = max(x1 - x0, 1.0)
    dy = max(y1 - y0, 1.0)
    ax.set_xlim(x0 - margin * dx * 0.1, x1 + margin * dx * 0.1)
    ax.set_ylim(y0 - margin * dy * 0.1, y1 + margin * dy * 0.1)

