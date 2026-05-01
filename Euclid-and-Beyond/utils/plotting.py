"""Plotting helpers shared by the Euclid and Beyond notebooks."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "ink": "#233044",
    "blue": "#2b6cb0",
    "green": "#2f855a",
    "gold": "#b7791f",
    "red": "#c53030",
    "purple": "#6b46c1",
    "gray": "#718096",
    "paper": "#f8fafc",
}


def new_figure(width: float = 7.0, height: float = 5.0) -> tuple[Any, Any]:
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_facecolor("white")
    return fig, ax


def set_equal_axes(ax: Any, margin: float = 0.15) -> None:
    """Make a 2D axis equal-aspect with a small margin."""

    ax.set_aspect("equal", adjustable="box")
    ax.margins(margin)
    ax.grid(True, color="#e2e8f0", linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def label_point(ax: Any, point: Sequence[float], label: str, *, offset: tuple[float, float] = (0.04, 0.04)) -> None:
    x, y = point
    ax.scatter([x], [y], s=42, color=PALETTE["ink"], zorder=4)
    ax.text(x + offset[0], y + offset[1], label, fontsize=10, color=PALETTE["ink"])


def draw_segment(
    ax: Any,
    a: Sequence[float],
    b: Sequence[float],
    *,
    label: str | None = None,
    color: str = PALETTE["blue"],
    linewidth: float = 2.2,
    linestyle: str = "-",
) -> None:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, linewidth=linewidth, linestyle=linestyle)
    if label:
        mid = (np.asarray(a, dtype=float) + np.asarray(b, dtype=float)) / 2
        ax.text(mid[0], mid[1], label, fontsize=9, color=color)


def draw_circle(
    ax: Any,
    center: Sequence[float],
    radius: float,
    *,
    label: str | None = None,
    color: str = PALETTE["green"],
    linewidth: float = 1.8,
    linestyle: str = "-",
) -> None:
    circle = plt.Circle(center, radius, fill=False, edgecolor=color, linewidth=linewidth, linestyle=linestyle)
    ax.add_patch(circle)
    if label:
        ax.text(center[0] + radius, center[1], label, fontsize=9, color=color)


def draw_polygon(
    ax: Any,
    points: Iterable[Sequence[float]],
    *,
    closed: bool = True,
    color: str = PALETTE["blue"],
    fill: str | None = None,
    label: str | None = None,
    linewidth: float = 2.0,
) -> None:
    pts = np.asarray(list(points), dtype=float)
    if closed:
        pts = np.vstack([pts, pts[0]])
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth)
    if fill:
        ax.fill(pts[:, 0], pts[:, 1], color=fill, alpha=0.18)
    if label:
        centroid = pts[:-1].mean(axis=0) if closed else pts.mean(axis=0)
        ax.text(centroid[0], centroid[1], label, fontsize=10, color=color, ha="center")


def draw_arrow(
    ax: Any,
    start: Sequence[float],
    end: Sequence[float],
    *,
    color: str = PALETTE["red"],
    label: str | None = None,
) -> None:
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={"arrowstyle": "->", "linewidth": 1.8, "color": color},
    )
    if label:
        mid = (np.asarray(start, dtype=float) + np.asarray(end, dtype=float)) / 2
        ax.text(mid[0], mid[1], label, fontsize=9, color=color)
