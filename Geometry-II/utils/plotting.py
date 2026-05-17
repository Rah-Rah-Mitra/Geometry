"""Plotting helpers with stable styling for Geometry II notebooks."""

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


def new_3d_axes(*, figsize: tuple[float, float] = (7.2, 5.6), title: str | None = None):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#ffffff")
    if title:
        ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    return fig, ax


def finish_axes(ax, *, margin: float = 0.4) -> None:
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    ax.set_xlim(x0 - margin, x1 + margin)
    ax.set_ylim(y0 - margin, y1 + margin)
    ax.tick_params(labelsize=8)


def set_equal_3d(ax, points: np.ndarray | None = None, *, radius: float | None = None) -> None:
    if points is not None:
        pts = np.asarray(points, dtype=float).reshape(-1, 3)
        center = pts.mean(axis=0)
        span = float(np.max(np.ptp(pts, axis=0))) / 2
    else:
        xlim = ax.get_xlim3d()
        ylim = ax.get_ylim3d()
        zlim = ax.get_zlim3d()
        center = np.array([(xlim[0] + xlim[1]) / 2, (ylim[0] + ylim[1]) / 2, (zlim[0] + zlim[1]) / 2])
        span = max(xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]) / 2
    r = radius if radius is not None else max(span, 1e-9)
    ax.set_xlim(center[0] - r, center[0] + r)
    ax.set_ylim(center[1] - r, center[1] + r)
    ax.set_zlim(center[2] - r, center[2] + r)
    ax.set_box_aspect((1, 1, 1))


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


def plot_line(ax, line: np.ndarray, *, xlim: tuple[float, float] = (-2, 2), color: str = COLORS["gray"], label: str | None = None) -> None:
    a, b, c = np.asarray(line, dtype=float)
    xs = np.linspace(xlim[0], xlim[1], 200)
    if abs(b) > 1e-10:
        ys = -(a * xs + c) / b
        ax.plot(xs, ys, color=color, linewidth=1.8, label=label)
    elif abs(a) > 1e-10:
        ax.axvline(-c / a, color=color, linewidth=1.8, label=label)


def plot_unit_circle(ax, *, color: str = COLORS["ink"], label: str | None = None) -> None:
    t = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.cos(t), np.sin(t), color=color, linewidth=2.0, label=label)


def save_figure(fig, path: Path) -> Path:
    result = save_matplotlib(fig, path)
    plt.close(fig)
    return result
