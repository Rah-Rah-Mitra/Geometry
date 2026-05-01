"""Plotting helpers for course notebooks."""

from __future__ import annotations

import math
from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon


ENEG_COLORS = {
    "ink": "#1f2933",
    "blue": "#235789",
    "teal": "#1b998b",
    "gold": "#d7a62b",
    "red": "#c44900",
    "violet": "#6d597a",
    "gray": "#7a869a",
    "green": "#3a7d44",
}


def setup_figure(
    *,
    width: float = 7.2,
    height: float = 5.0,
    title: str | None = None,
    equal: bool = True,
    grid: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(width, height))
    if equal:
        ax.set_aspect("equal", adjustable="box")
    if grid:
        ax.grid(True, alpha=0.2, linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=8)
    if title:
        ax.set_title(title, fontsize=12, weight="bold")
    return fig, ax


def equal_limits(ax: plt.Axes, points: Sequence[Sequence[float]], margin: float = 0.4) -> None:
    arr = np.asarray(points, dtype=float)
    xmin, ymin = arr.min(axis=0)
    xmax, ymax = arr.max(axis=0)
    span = max(float(xmax - xmin), float(ymax - ymin), 1.0)
    cx = (xmax + xmin) / 2
    cy = (ymax + ymin) / 2
    half = span / 2 + margin
    ax.set_xlim(cx - half, cx + half)
    ax.set_ylim(cy - half, cy + half)


def draw_points(ax: plt.Axes, pts: dict[str, Sequence[float]], *, color: str = ENEG_COLORS["ink"]) -> None:
    for label, point in pts.items():
        x, y = point
        ax.scatter([x], [y], s=42, color=color, zorder=4)
        ax.text(x + 0.05, y + 0.05, label, fontsize=10, weight="bold")


def draw_segment(
    ax: plt.Axes,
    p: Sequence[float],
    q: Sequence[float],
    *,
    color: str = ENEG_COLORS["blue"],
    label: str | None = None,
    linewidth: float = 2.0,
) -> None:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, linewidth=linewidth, label=label)


def draw_line(
    ax: plt.Axes,
    p: Sequence[float],
    q: Sequence[float],
    *,
    color: str = ENEG_COLORS["blue"],
    label: str | None = None,
    linewidth: float = 1.8,
) -> None:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    direction = q - p
    t = np.linspace(-4, 4, 2)
    pts = p + np.outer(t, direction)
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth, label=label)


def draw_circle(
    ax: plt.Axes,
    center: Sequence[float],
    radius: float,
    *,
    color: str = ENEG_COLORS["teal"],
    label: str | None = None,
    fill: bool = False,
    alpha: float = 1.0,
) -> Circle:
    patch = Circle(center, radius, edgecolor=color, facecolor=color if fill else "none", alpha=alpha, linewidth=2)
    ax.add_patch(patch)
    if label:
        ax.text(center[0] + radius * 0.7, center[1] + radius * 0.7, label, color=color, fontsize=9)
    return patch


def draw_angle_arc(
    ax: plt.Axes,
    vertex: Sequence[float],
    p: Sequence[float],
    q: Sequence[float],
    *,
    radius: float = 0.45,
    color: str = ENEG_COLORS["red"],
    label: str | None = None,
) -> Arc:
    vertex = np.asarray(vertex, dtype=float)
    p = np.asarray(p, dtype=float) - vertex
    q = np.asarray(q, dtype=float) - vertex
    a0 = math.degrees(math.atan2(p[1], p[0]))
    a1 = math.degrees(math.atan2(q[1], q[0]))
    if a1 < a0:
        a1 += 360
    if a1 - a0 > 180:
        a0, a1 = a1, a0 + 360
    arc = Arc(vertex, 2 * radius, 2 * radius, theta1=a0, theta2=a1, color=color, linewidth=2)
    ax.add_patch(arc)
    if label:
        mid = math.radians((a0 + a1) / 2)
        ax.text(vertex[0] + radius * math.cos(mid), vertex[1] + radius * math.sin(mid), label, color=color, fontsize=9)
    return arc


def draw_polygon(
    ax: plt.Axes,
    vertices: Sequence[Sequence[float]],
    *,
    edgecolor: str = ENEG_COLORS["blue"],
    facecolor: str = "#dbeafe",
    alpha: float = 0.24,
    label: str | None = None,
) -> Polygon:
    patch = Polygon(vertices, closed=True, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidth=2)
    ax.add_patch(patch)
    if label:
        arr = np.asarray(vertices, dtype=float)
        center = arr.mean(axis=0)
        ax.text(center[0], center[1], label, ha="center", va="center", fontsize=10)
    return patch

