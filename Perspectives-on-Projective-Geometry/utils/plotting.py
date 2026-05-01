from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from .artifacts import image_stats

COLORS = {
    "ink": "#202124",
    "blue": "#2f6fbb",
    "red": "#b4463a",
    "green": "#3f7f54",
    "gold": "#b88a1d",
    "purple": "#6d5aa8",
    "gray": "#73777f",
}


def set_geometry_style() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": (7.2, 5.2),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.18,
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 10,
        }
    )


def new_figure(width: float = 7.2, height: float = 5.2):
    set_geometry_style()
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_aspect("equal", adjustable="box")
    return fig, ax


def save_figure(fig, path: str | Path, min_std: float = 1.0) -> dict[str, float | int | str]:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    stats = image_stats(out)
    if stats["pixel_std"] < min_std:
        raise AssertionError(f"Rendered image appears blank: {out}")
    return stats


def draw_projective_line(ax, line: np.ndarray, xlim=(-3, 3), **kwargs) -> None:
    a, b, c = line
    xs = np.linspace(xlim[0], xlim[1], 200)
    if abs(b) > 1e-12:
        ys = -(a * xs + c) / b
        ax.plot(xs, ys, **kwargs)
    elif abs(a) > 1e-12:
        x = -c / a
        ax.axvline(x, **kwargs)


def annotate_points(ax, points: dict[str, tuple[float, float]], dx: float = 0.04, dy: float = 0.04) -> None:
    for label, (x, y) in points.items():
        ax.scatter([x], [y], s=36, color=COLORS["ink"], zorder=4)
        ax.text(x + dx, y + dy, label, fontsize=9, weight="bold")


def unit_circle(ax, **kwargs) -> None:
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), **kwargs)

