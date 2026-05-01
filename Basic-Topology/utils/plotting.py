"""Small plotting helpers shared by the Basic Topology notebooks."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "ink": "#273043",
    "blue": "#1f77b4",
    "green": "#2ca25f",
    "gold": "#b8860b",
    "red": "#c23b22",
    "purple": "#6a51a3",
    "teal": "#008080",
    "gray": "#6b7280",
    "paper": "#f8fafc",
}


def new_figure(width: float = 7.0, height: float = 5.0) -> tuple[Any, Any]:
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_facecolor("white")
    return fig, ax


def set_equal_axes(ax: Any, margin: float = 0.12) -> None:
    ax.set_aspect("equal", adjustable="box")
    ax.margins(margin)
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color("#cbd5e1")


def label_point(
    ax: Any,
    point: Sequence[float],
    label: str,
    *,
    offset: tuple[float, float] = (0.04, 0.04),
    color: str = PALETTE["ink"],
) -> None:
    x, y = point
    ax.scatter([x], [y], s=42, color=color, zorder=4)
    ax.text(x + offset[0], y + offset[1], label, fontsize=10, color=color)


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
