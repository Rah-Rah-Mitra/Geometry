"""Reusable visual helpers for the VDGF notebooks.

The helpers are intentionally deterministic: a chapter visual should be
rebuildable, concept-specific, and easy to audit for nonblank output.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utils.artifacts import save_matplotlib


PALETTE = {
    "ink": "#1d2733",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


def unit_circle(samples: int = 240) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0, 2 * np.pi, samples)
    return np.cos(theta), np.sin(theta)


def saddle_grid(samples: int = 40, extent: float = 1.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-extent, extent, samples)
    y = np.linspace(-extent, extent, samples)
    X, Y = np.meshgrid(x, y)
    return X, Y, X**2 - Y**2


def form_stack_lines(slope: float = 1.0, offsets: int = 6, extent: float = 2.0) -> list[tuple[np.ndarray, np.ndarray]]:
    x = np.linspace(-extent, extent, 100)
    return [(x, -slope * x + b) for b in np.linspace(-extent, extent, offsets)]


def _style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=10, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b6c0ca")


def _figure_stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "width": int(image.width),
        "height": int(image.height),
        "pixel_std": float(arr.std()),
        "file_size": int(path.stat().st_size),
    }


def _add_note(ax: Any, text: str) -> None:
    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.9},
    )


def _plot_limit_lab(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0.2, math.pi * 0.95, 120)
    chord = 2 * np.sin(theta / 2)
    arc = theta
    sector = theta / 2
    ax.plot(theta, arc / chord, label="arc / chord", color=PALETTE["blue"])
    ax.plot(theta, sector / (chord**2 / 2), label="sector / triangle", color=PALETTE["teal"])
    ax.axhline(1, color=PALETTE["gray"], linestyle="--")
    ax.set_xlabel("angle")
    ax.set_ylabel("ratio")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_three_geometries(ax: Any, spec: dict[str, Any]) -> None:
    ax.plot([0, 1, 0.25, 0], [0, 0, 0.8, 0], color=PALETTE["blue"], lw=2, label="Euclidean")
    theta = np.linspace(0, math.pi / 2, 80)
    ax.plot(1.6 + np.cos(theta), np.sin(theta), color=PALETTE["teal"], lw=2, label="spherical arc")
    disk = plt.Circle((3.7, 0.45), 0.75, fill=False, color=PALETTE["gray"], lw=1.2)
    ax.add_patch(disk)
    t = np.linspace(-0.7, 0.7, 100)
    ax.plot(3.7 + t, 0.45 + 0.55 * (1 - t**2), color=PALETTE["red"], lw=2, label="Poincare arc")
    ax.set_xlim(-0.2, 4.7)
    ax.set_ylim(-0.2, 1.45)
    _style_axis(ax, spec["title"], equal=True)
    ax.legend(fontsize=8, loc="lower right")


def _plot_curvature_detectors(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(0.05, 1.3, 140)
    for K, color, label in [(1, PALETTE["teal"], "K=+1"), (0, PALETTE["gray"], "K=0"), (-1, PALETTE["red"], "K=-1")]:
        if K == 0:
            circumference = 2 * math.pi * r
        elif K > 0:
            circumference = 2 * math.pi * np.sin(r)
        else:
            circumference = 2 * math.pi * np.sinh(r)
        ax.plot(r, circumference - 2 * math.pi * r, color=color, label=label)
    ax.set_xlabel("geodesic radius")
    ax.set_ylabel("circumference defect")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_metric_atlas(ax: Any, spec: dict[str, Any]) -> None:
    xs = np.linspace(-2.2, 2.2, 13)
    ys = np.linspace(-2.2, 2.2, 13)
    for x in xs:
        ax.plot([x] * len(ys), ys, color="#d7dde5", lw=0.7)
    for y in ys:
        ax.plot(xs, [y] * len(xs), color="#d7dde5", lw=0.7)
    for x in np.linspace(-1.6, 1.6, 5):
        for y in np.linspace(-1.6, 1.6, 5):
            scale = 2 / (1 + x * x + y * y)
            ellipse = plt.matplotlib.patches.Ellipse((x, y), 0.18 * scale, 0.18 * scale, fill=False, color=PALETTE["blue"], lw=1)
            ax.add_patch(ellipse)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, "Tissot circles shrink with stereographic scale")


def _plot_pseudosphere(ax: Any, spec: dict[str, Any]) -> None:
    x = np.linspace(-2.2, 2.2, 200)
    for center in [-1.2, 0.0, 1.2]:
        radius = 0.9 + abs(center) * 0.2
        xx = np.linspace(center - radius, center + radius, 120)
        yy = np.sqrt(np.maximum(radius**2 - (xx - center) ** 2, 0))
        ax.plot(xx, yy + 0.05, color=PALETTE["red"], lw=1.8)
    ax.axhline(0, color=PALETTE["ink"], lw=1.5)
    t = np.linspace(0.05, 2.4, 160)
    ax.plot(-3 + t - np.tanh(t), 1 / np.cosh(t), color=PALETTE["teal"], lw=2, label="tractrix profile")
    ax.set_xlim(-3.1, 2.4)
    ax.set_ylim(-0.1, 2.0)
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_mobius(ax: Any, spec: dict[str, Any]) -> None:
    circle = plt.Circle((0, 0), 1, fill=False, color=PALETTE["ink"], lw=1.4)
    ax.add_patch(circle)
    theta = np.linspace(0, 2 * np.pi, 200)
    for radius, color in [(0.25, PALETTE["blue"]), (0.5, PALETTE["teal"]), (0.72, PALETTE["gold"])]:
        z = radius * np.exp(1j * theta)
        a = 0.35
        w = (z + a) / (a * z + 1)
        ax.plot(w.real, w.imag, color=color, lw=1.6)
    ax.scatter([0, 0.35], [0, 0], color=[PALETTE["blue"], PALETTE["red"]], s=35)
    _style_axis(ax, spec["title"], equal=True)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)


def _plot_curve(ax: Any, spec: dict[str, Any]) -> None:
    t = np.linspace(-2.4, 2.4, 240)
    y = np.sin(t) + 0.15 * spec["chapter"] * np.cos(0.7 * t) / 40
    ax.plot(t, y, color=PALETTE["blue"], lw=2)
    points = np.linspace(40, 200, 5, dtype=int)
    ax.scatter(t[points], y[points], color=PALETTE["red"], s=30, zorder=3)
    for idx in points:
        radius = 0.18 + 0.02 * ((idx + spec["chapter"]) % 5)
        circ = plt.Circle((t[idx], y[idx]), radius, fill=False, color=PALETTE["teal"], alpha=0.7)
        ax.add_patch(circ)
    _style_axis(ax, spec["title"])
    ax.set_xlabel("parameter")
    ax.set_ylabel("curve")


def _plot_helix(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    t = np.linspace(0, 4 * np.pi, 240)
    ax3.plot(np.cos(t), np.sin(t), t / (2 * np.pi), color=PALETTE["blue"], lw=2)
    for idx in [35, 90, 145, 200]:
        p = np.array([np.cos(t[idx]), np.sin(t[idx]), t[idx] / (2 * np.pi)])
        tangent = np.array([-np.sin(t[idx]), np.cos(t[idx]), 1 / (2 * np.pi)])
        tangent = tangent / np.linalg.norm(tangent)
        ax3.quiver(*p, *tangent, length=0.35, color=PALETTE["red"])
    ax3.set_title(spec["title"], fontsize=10)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("height")


def _plot_rose(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    polar = fig.add_subplot(111, projection="polar")
    theta = np.linspace(0, 2 * np.pi, 360)
    k1 = 0.4 + 0.03 * (spec["chapter"] % 7)
    k2 = -0.25 + 0.02 * (spec["chapter"] % 5)
    curvature = k1 * np.cos(theta) ** 2 + k2 * np.sin(theta) ** 2
    polar.plot(theta, curvature, color=PALETTE["violet"], lw=2)
    polar.set_title(spec["title"], fontsize=10)


def _plot_surface_panel(ax: Any, spec: dict[str, Any]) -> None:
    X, Y, Z = saddle_grid(samples=50)
    contours = ax.contourf(X, Y, Z, levels=16, cmap="viridis", alpha=0.85)
    ax.contour(X, Y, Z, levels=10, colors="white", linewidths=0.5, alpha=0.7)
    ax.quiver([0], [0], [0.75], [0.25], color=PALETTE["red"], angles="xy", scale_units="xy", scale=1)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, "surface patch: color = height, arrow = normal drift")


def _plot_topology(ax: Any, spec: dict[str, Any]) -> None:
    genus = np.arange(0, 5)
    chi = 2 - 2 * genus
    total = 2 * math.pi * chi
    ax.bar(genus, total, color=[PALETTE["teal"], PALETTE["blue"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]])
    ax.axhline(0, color=PALETTE["ink"], lw=1)
    ax.set_xlabel("genus")
    ax.set_ylabel("2 pi chi")
    _style_axis(ax, spec["title"])


def _plot_vector_field(ax: Any, spec: dict[str, Any]) -> None:
    x = np.linspace(-1.5, 1.5, 17)
    y = np.linspace(-1.5, 1.5, 17)
    X, Y = np.meshgrid(x, y)
    power = 1 + spec["chapter"] % 4
    angle = power * np.arctan2(Y, X)
    U, V = np.cos(angle), np.sin(angle)
    ax.quiver(X, Y, U, V, color=PALETTE["blue"], pivot="mid", scale=28)
    ax.scatter([0], [0], color=PALETTE["red"], s=45)
    _style_axis(ax, spec["title"], equal=True)
    _add_note(ax, f"index cue: winding power {power}")


def _plot_transport(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0, 2 * np.pi, 220)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["gray"], lw=1)
    phase = 0.12 * spec["chapter"]
    for t in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        p = np.array([np.cos(t), np.sin(t)])
        v = 0.28 * np.array([np.cos(t + phase), np.sin(t + phase)])
        ax.arrow(p[0], p[1], v[0], v[1], head_width=0.045, color=PALETTE["teal"], length_includes_head=True)
    _style_axis(ax, spec["title"], equal=True)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)


def _plot_jacobi(ax: Any, spec: dict[str, Any]) -> None:
    s = np.linspace(0, 4, 240)
    ax.plot(s, s, color=PALETTE["gray"], label="K=0")
    ax.plot(s, np.sin(s), color=PALETTE["teal"], label="K=+1")
    ax.plot(s, np.sinh(s) / np.sinh(4), color=PALETTE["red"], label="K=-1 scaled")
    ax.set_xlabel("geodesic distance")
    ax.set_ylabel("separation")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def _plot_forms(ax: Any, spec: dict[str, Any]) -> None:
    chapter = spec["chapter"]
    if chapter == 32:
        for x, y in form_stack_lines(slope=0.7):
            ax.plot(x, y, color=PALETTE["blue"], alpha=0.8)
        ax.arrow(-1.4, -0.8, 1.1, 0.9, head_width=0.08, color=PALETTE["red"], length_includes_head=True)
    elif chapter == 33:
        matrix = np.array([[2, 0.6], [0.6, 1.1]])
        ax.imshow(matrix, cmap="YlGnBu")
        for (i, j), value in np.ndenumerate(matrix):
            ax.text(j, i, f"{value:.1f}", ha="center", va="center", color=PALETTE["ink"])
    elif chapter == 34:
        poly = np.array([[0, 0], [1.3, 0.35], [1.7, 1.2], [0.4, 0.85], [0, 0]])
        ax.plot(poly[:, 0], poly[:, 1], color=PALETTE["blue"], lw=2)
        ax.fill(poly[:, 0], poly[:, 1], color=PALETTE["teal"], alpha=0.25)
        ax.arrow(0.2, 0.15, 0.8, 0.22, head_width=0.05, color=PALETTE["red"])
    elif chapter == 35:
        squares = [(0, 0), (0.35, 0.25), (0.7, 0.5)]
        for x0, y0 in squares:
            ax.add_patch(plt.Rectangle((x0, y0), 0.8, 0.8, fill=False, edgecolor=PALETTE["blue"], lw=1.5))
        ax.arrow(0.15, 0.15, 0.8, 0.5, head_width=0.05, color=PALETTE["red"])
    else:
        xs = np.linspace(-2, 2, 200)
        ax.plot(xs, np.sin(xs * (1 + chapter % 3)), color=PALETTE["blue"], label="form")
        ax.plot(xs, np.gradient(np.sin(xs * (1 + chapter % 3)), xs), color=PALETTE["red"], label="d form")
        ax.legend(fontsize=8)
    _style_axis(ax, spec["title"], equal=chapter in {32, 34, 35})


def _plot_dashboard(ax: Any, spec: dict[str, Any]) -> None:
    values = np.array([(spec["chapter"] * i) % 9 + 1 for i in range(1, 10)]).reshape(3, 3)
    ax.imshow(values, cmap="magma")
    for (i, j), value in np.ndenumerate(values):
        ax.text(j, i, str(int(value)), ha="center", va="center", color="white", fontsize=9)
    _style_axis(ax, spec["title"])
    ax.set_xticks([])
    ax.set_yticks([])


def _plot_schwarzschild(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(2.05, 10, 240)
    f = 1 - 2 / r
    ax.plot(r, f, color=PALETTE["blue"], label="1 - 2M/r")
    ax.plot(r, 1 / f, color=PALETTE["red"], label="radial metric factor")
    ax.axvline(2, color=PALETTE["ink"], linestyle="--", label="horizon")
    ax.set_ylim(-0.1, 8)
    ax.set_xlabel("r / M")
    _style_axis(ax, spec["title"])
    ax.legend(fontsize=8)


def build_chapter_visual(spec: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> tuple[Path, dict[str, Any]]:
    """Create, save, and quality-check the chapter-specific static visual."""

    family = spec.get("family", "dashboard")
    fig, ax = plt.subplots(figsize=(7, 4.8))
    if family == "limit":
        _plot_limit_lab(ax, spec)
    elif family == "geometries":
        _plot_three_geometries(ax, spec)
    elif family == "curvature":
        _plot_curvature_detectors(ax, spec)
    elif family == "metric":
        _plot_metric_atlas(ax, spec)
    elif family == "pseudosphere":
        _plot_pseudosphere(ax, spec)
    elif family == "mobius":
        _plot_mobius(ax, spec)
    elif family == "curve":
        _plot_curve(ax, spec)
    elif family == "helix":
        _plot_helix(ax, spec)
    elif family == "rose":
        _plot_rose(ax, spec)
    elif family == "surface":
        _plot_surface_panel(ax, spec)
    elif family == "topology":
        _plot_topology(ax, spec)
    elif family == "vector-field":
        _plot_vector_field(ax, spec)
    elif family == "transport":
        _plot_transport(ax, spec)
    elif family == "jacobi":
        _plot_jacobi(ax, spec)
    elif family == "forms":
        _plot_forms(ax, spec)
    elif family == "schwarzschild":
        _plot_schwarzschild(ax, spec)
    else:
        _plot_dashboard(ax, spec)
    fig.suptitle(spec.get("caption", ""), fontsize=9, y=0.01, color=PALETTE["gray"])
    path = save_matplotlib(fig, artifact_topic, "figures", spec["filename"], root=artifact_root)
    plt.close(fig)
    stats = _figure_stats(path)
    if stats["file_size"] <= 1000 or stats["pixel_std"] <= 1.0:
        raise ValueError(f"visual artifact looks blank or too small: {path}")
    return path, stats
