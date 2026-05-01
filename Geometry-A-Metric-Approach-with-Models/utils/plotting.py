"""Plotting helpers for metric-approach geometry notebooks."""

from __future__ import annotations

import math
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon


PALETTE = ["#2f6fbb", "#d95f02", "#1b9e77", "#7570b3", "#e7298a", "#66a61e"]


def new_figure(title: str, *, figsize: tuple[float, float] = (8, 5)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=13, pad=12)
    ax.grid(True, color="#e8e8e8", linewidth=0.8)
    ax.set_axisbelow(True)
    return fig, ax


def set_equal(ax, *, pad: float = 0.4) -> None:
    ax.set_aspect("equal", adjustable="box")
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    span = max(x1 - x0, y1 - y0) + pad
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    ax.set_xlim(cx - span / 2, cx + span / 2)
    ax.set_ylim(cy - span / 2, cy + span / 2)


def annotate_point(ax, point, label: str, *, color: str = "#222222", offset=(0.05, 0.05)) -> None:
    p = np.asarray(point, dtype=float)
    ax.scatter([p[0]], [p[1]], s=48, color=color, zorder=4)
    ax.text(p[0] + offset[0], p[1] + offset[1], label, fontsize=10, color=color)


def draw_segment(ax, p, q, *, color: str = "#2f6fbb", label: str | None = None, lw: float = 2.2) -> None:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, label=label)


def draw_ray(ax, origin, direction, *, color: str = "#d95f02", label: str | None = None, length: float = 3.0) -> None:
    origin = np.asarray(origin, dtype=float)
    direction = np.asarray(direction, dtype=float)
    direction = direction / np.linalg.norm(direction)
    end = origin + length * direction
    ax.arrow(origin[0], origin[1], end[0] - origin[0], end[1] - origin[1],
             head_width=0.09, length_includes_head=True, color=color, lw=1.8)
    if label:
        ax.text(end[0], end[1], label, color=color, fontsize=10)


def draw_angle_arc(ax, center, radius: float, start_deg: float, end_deg: float, *, color: str = "#222222") -> None:
    arc = Arc(center, 2 * radius, 2 * radius, theta1=start_deg, theta2=end_deg, color=color, lw=2)
    ax.add_patch(arc)


def draw_circle(ax, center, radius: float, *, color: str = "#1b9e77", fill: bool = False, alpha: float = 0.15) -> None:
    ax.add_patch(Circle(center, radius, edgecolor=color, facecolor=color if fill else "none", lw=2, alpha=alpha if fill else 1.0))


def draw_polygon(ax, points: Iterable[tuple[float, float]], *, color: str = "#7570b3", alpha: float = 0.16) -> None:
    pts = np.asarray(list(points), dtype=float)
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color, alpha=alpha, lw=2))
    ax.plot([*pts[:, 0], pts[0, 0]], [*pts[:, 1], pts[0, 1]], color=color, lw=2)


def angle_degrees(u, v) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    cosang = float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosang))))
