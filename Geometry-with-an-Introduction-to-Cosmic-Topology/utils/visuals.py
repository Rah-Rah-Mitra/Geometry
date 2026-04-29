"""Deterministic visual builders for the GICT notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle

from utils.artifacts import image_stats, save_html, save_matplotlib
from utils.complex_plane import complex_grid, unit_circle
from utils.cosmic_topology import pair_distances, sphere_intersection_circle_radius, torus_catalog
from utils.mobius import disk_automorphism, invert_in_circle
from utils.models import angle_of_parallelism, circumference_k, disk_area_k, unified_right_hypotenuse
from utils.surfaces import classify_catalog, torus_images


PALETTE = {
    "ink": "#1f2933",
    "blue": "#3269a8",
    "teal": "#258f86",
    "green": "#5b8a3c",
    "gold": "#c79020",
    "red": "#bd4b4b",
    "violet": "#6d5aa8",
    "gray": "#718096",
    "light": "#eef3f7",
}


def _style(ax: Any, title: str, *, equal: bool = True) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d7dee8", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b8c2cc")


def _plot_unit_disk(ax: Any) -> None:
    ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"], linewidth=1.5))
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)


def _plot_torus(ax: Any, spec: dict[str, Any]) -> None:
    w, h = 4.0, 2.6
    for i in range(-1, 2):
        for j in range(-1, 2):
            ax.add_patch(Rectangle((i * w, j * h), w, h, fill=False, edgecolor="#b8c2cc", linewidth=0.9))
    p = np.array([1.0, 0.8])
    q = np.array([3.4, 2.1])
    images = torus_images(tuple(q), w, h, radius=1)
    ax.scatter(images[:, 0], images[:, 1], s=28, color=PALETTE["teal"], label="object images")
    ax.scatter([p[0]], [p[1]], s=48, color=PALETTE["red"], label="observer")
    ax.arrow(3.75, 1.3, 0.7, 0, width=0.02, color=PALETTE["blue"], length_includes_head=True)
    ax.arrow(0.25, 1.3, -0.7, 0, width=0.02, color=PALETTE["blue"], length_includes_head=True)
    ax.set_xlim(-0.7, w + 0.7)
    ax.set_ylim(-0.5, h + 0.5)
    ax.legend(fontsize=8, loc="upper right")
    _style(ax, spec["title"])


def _plot_sphere(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 24)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax3.plot_surface(x, y, z, color="#dceaf7", edgecolor="#ffffff", linewidth=0.2, alpha=0.8)
    t = np.linspace(0, np.pi / 2, 80)
    ax3.plot(np.cos(t), np.sin(t), 0 * t, color=PALETTE["blue"], linewidth=2)
    ax3.plot(np.cos(t) * 0, np.sin(t), np.cos(t), color=PALETTE["red"], linewidth=2)
    ax3.plot(np.cos(t), 0 * t, np.sin(t), color=PALETTE["teal"], linewidth=2)
    ax3.set_title(spec["title"], fontsize=11)
    ax3.set_box_aspect((1, 1, 1))
    ax3.set_axis_off()


def _plot_parallel(ax: Any, spec: dict[str, Any]) -> None:
    ax.set_xlim(-0.2, 6.4)
    ax.set_ylim(-1.2, 1.4)
    labels = ["Euclidean: one", "Hyperbolic: many", "Elliptic: none"]
    offsets = [0, 2.2, 4.4]
    for label, ox in zip(labels, offsets):
        ax.plot([ox, ox + 1.6], [0, 0], color=PALETTE["ink"], linewidth=1.6)
        ax.scatter([ox + 0.8], [0.75], color=PALETTE["red"], s=24)
        if "Euclidean" in label:
            ax.plot([ox, ox + 1.6], [0.75, 0.75], color=PALETTE["blue"], linewidth=1.5)
        elif "Hyperbolic" in label:
            xs = np.linspace(ox, ox + 1.6, 80)
            ax.plot(xs, 0.75 + 0.25 * (xs - ox - 0.8) ** 2, color=PALETTE["blue"])
            ax.plot(xs, 0.75 - 0.25 * (xs - ox - 0.8) ** 2, color=PALETTE["teal"])
        else:
            theta = np.linspace(0.2, 2.95, 80)
            ax.plot(ox + 0.8 + 0.8 * np.cos(theta), -0.05 + 0.8 * np.sin(theta), color=PALETTE["blue"])
            ax.plot(ox + 0.8 + 0.8 * np.cos(theta), 0.75 - 0.8 * np.sin(theta), color=PALETTE["teal"])
        ax.text(ox + 0.8, -0.75, label, ha="center", fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_cone(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0, 1.55 * np.pi, 120)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["blue"], linewidth=2, label="cone sector")
    theta2 = np.linspace(0, 2.45 * np.pi, 160)
    ax.plot(1.45 + np.cos(theta2) * 0.55, np.sin(theta2) * 0.55, color=PALETTE["red"], linewidth=2, label="saddle sector")
    ax.plot([0, 1], [0, 0], color=PALETTE["ink"])
    ax.plot([0, np.cos(theta[-1])], [0, np.sin(theta[-1])], color=PALETTE["ink"])
    ax.text(-0.3, -0.35, "C = theta r", fontsize=9)
    ax.legend(fontsize=8)
    _style(ax, spec["title"])


def _plot_hexagon(ax: Any, spec: dict[str, Any]) -> None:
    angles = np.linspace(0, 2 * np.pi, 7)[:-1] + np.pi / 6
    pts = np.c_[np.cos(angles), np.sin(angles)]
    ax.add_patch(Polygon(pts, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
    labels = ["a", "b", "c", "a", "b", "c"]
    for i, label in enumerate(labels):
        p = (pts[i] + pts[(i + 1) % 6]) / 2
        ax.text(p[0] * 1.08, p[1] * 1.08, label, ha="center", va="center", fontsize=10, color=PALETTE["blue"])
    for i in range(0, 6, 2):
        ax.plot([pts[i, 0], pts[(i + 3) % 6, 0]], [pts[i, 1], pts[(i + 3) % 6, 1]], "--", color=PALETTE["gray"], alpha=0.7)
    ax.text(0, -1.35, "corner-pair total: 2 x 120 deg in the plane", ha="center", fontsize=8)
    _style(ax, spec["title"])


def _plot_erlangen(ax: Any, spec: dict[str, Any]) -> None:
    names = ["translation", "rotation", "scale", "Mobius"]
    props = ["distance", "angle", "line", "circle"]
    data = np.array([[1, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1], [0, 1, 0.5, 1]])
    ax.imshow(data, cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(len(props)), props, rotation=30, ha="right")
    ax.set_yticks(range(len(names)), names)
    for i in range(len(names)):
        for j in range(len(props)):
            ax.text(j, i, "yes" if data[i, j] == 1 else ("case" if data[i, j] else "no"), ha="center", va="center", fontsize=8)
    ax.set_title(spec["title"], fontsize=11)


def _plot_complex_vectors(ax: Any, spec: dict[str, Any]) -> None:
    z, w = 2 + 1j, -1 + 1.4j
    for value, color, label in [(z, PALETTE["blue"], "z"), (w, PALETTE["teal"], "w"), (z + w, PALETTE["red"], "z+w")]:
        ax.arrow(0, 0, value.real, value.imag, color=color, width=0.02, length_includes_head=True)
        ax.text(value.real, value.imag, label, fontsize=9)
    ax.plot([w.real, z.real], [w.imag, z.imag], "--", color=PALETTE["gold"], label="z-w")
    ax.set_xlim(-1.8, 2.6)
    ax.set_ylim(-0.5, 3.0)
    ax.legend(fontsize=8)
    _style(ax, spec["title"])


def _plot_conjugate(ax: Any, spec: dict[str, Any]) -> None:
    z = 1.5 + 1.2j
    circle = Circle((0, 0), abs(z), fill=False, color=PALETTE["gray"], linestyle="--")
    ax.add_patch(circle)
    ax.scatter([z.real, z.real], [z.imag, -z.imag], color=[PALETTE["blue"], PALETTE["red"]])
    ax.plot([z.real, z.real], [z.imag, -z.imag], color=PALETTE["teal"])
    ax.axhline(0, color=PALETTE["ink"])
    ax.text(z.real + 0.05, z.imag, "z")
    ax.text(z.real + 0.05, -z.imag, "conj(z)")
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.8, 1.8)
    _style(ax, spec["title"])


def _plot_polar(ax: Any, spec: dict[str, Any]) -> None:
    theta = 0.72
    r = 1.6
    z = r * np.exp(1j * theta)
    ax.add_patch(Circle((0, 0), r, fill=False, color=PALETTE["gray"], linestyle="--"))
    ax.arrow(0, 0, z.real, z.imag, color=PALETTE["blue"], width=0.02, length_includes_head=True)
    arc = np.linspace(0, theta, 50)
    ax.plot(0.5 * np.cos(arc), 0.5 * np.sin(arc), color=PALETTE["red"], linewidth=2)
    ax.text(0.55, 0.18, "theta")
    ax.text(z.real, z.imag, "r exp(i theta)")
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1.6, 1.8)
    _style(ax, spec["title"])


def _plot_multiplication(ax: Any, spec: dict[str, Any]) -> None:
    z = 1.2 * np.exp(0.45j)
    w = 1.35 * np.exp(0.85j)
    zw = z * w
    for value, color, label in [(z, PALETTE["blue"], "z"), (w, PALETTE["teal"], "w"), (zw, PALETTE["red"], "zw")]:
        ax.arrow(0, 0, value.real, value.imag, color=color, width=0.015, length_includes_head=True)
        ax.text(value.real, value.imag, label)
    ax.set_xlim(-0.5, 2.2)
    ax.set_ylim(-0.2, 1.8)
    _style(ax, spec["title"])


def _plot_angle(ax: Any, spec: dict[str, Any]) -> None:
    v = np.array([0.0, 0.0])
    u = np.array([1.8, 0.25])
    w = np.array([0.7, 1.55])
    ax.plot([v[0], u[0]], [v[1], u[1]], color=PALETTE["blue"], linewidth=2)
    ax.plot([v[0], w[0]], [v[1], w[1]], color=PALETTE["red"], linewidth=2)
    ax.scatter([v[0], u[0], w[0]], [v[1], u[1], w[1]], color=PALETTE["ink"])
    ax.text(0.2, 0.25, "arg((w-v)/(u-v))", fontsize=9)
    ax.set_xlim(-0.3, 2.1)
    ax.set_ylim(-0.2, 1.9)
    _style(ax, spec["title"])


def _plot_region(ax: Any, spec: dict[str, Any]) -> None:
    xs = np.linspace(-2, 2, 180)
    ys = np.linspace(-2, 2, 180)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    mask = (np.abs(Z - 0.5) < 1.0) & (Y > X - 0.7)
    ax.contourf(X, Y, mask.astype(float), levels=[-0.1, 0.5, 1.1], colors=["#ffffff", "#d6f0ed"])
    ax.contour(X, Y, np.abs(Z - 0.5), levels=[1.0], colors=[PALETTE["blue"]])
    ax.plot(xs, xs - 0.7, color=PALETTE["red"])
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    _style(ax, spec["title"])


def _plot_affine_grid(ax: Any, spec: dict[str, Any]) -> None:
    a = 0.75 * np.exp(0.7j)
    b = 0.5 + 0.4j
    for line in complex_grid(1.5, 7):
        transformed = a * line + b
        ax.plot(line.real, line.imag, color="#c9d4df", linewidth=0.7)
        ax.plot(transformed.real, transformed.imag, color=PALETTE["blue"], linewidth=0.9)
    ax.set_xlim(-2.0, 2.2)
    ax.set_ylim(-1.8, 2.1)
    _style(ax, spec["title"])


def _plot_reflection(ax: Any, spec: dict[str, Any]) -> None:
    ax.axhline(0, color=PALETTE["ink"], linewidth=1.2)
    pts = np.array([[0.4, 0.9], [1.2, 0.5], [-0.8, 0.7]])
    ax.scatter(pts[:, 0], pts[:, 1], color=PALETTE["blue"], label="points")
    ax.scatter(pts[:, 0], -pts[:, 1], color=PALETTE["red"], label="reflections")
    for x, y in pts:
        ax.plot([x, x], [y, -y], "--", color=PALETTE["gray"])
    ax.legend(fontsize=8)
    ax.set_xlim(-1.5, 1.8)
    ax.set_ylim(-1.2, 1.2)
    _style(ax, spec["title"])


def _plot_inversion(ax: Any, spec: dict[str, Any]) -> None:
    ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"], linewidth=1.4))
    for r in [0.35, 0.65, 1.35]:
        theta = np.linspace(0, 2 * np.pi, 240)
        z = 0.15 + r * np.exp(1j * theta)
        inv = invert_in_circle(z)
        ax.plot(z.real, z.imag, color="#c9d4df", linewidth=0.8)
        ax.plot(inv.real, inv.imag, color=PALETTE["blue"], linewidth=0.9)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    _style(ax, spec["title"])


def _plot_clines(ax: Any, spec: dict[str, Any]) -> None:
    ax.add_patch(Circle((0, 0), 1, fill=False, color=PALETTE["ink"]))
    theta = np.linspace(0, 2 * np.pi, 240)
    for c, r, color in [(0.45 + 0.2j, 0.55, PALETTE["blue"]), (-0.2 + 0.0j, 0.75, PALETTE["teal"])]:
        z = c + r * np.exp(1j * theta)
        inv = invert_in_circle(z)
        ax.plot(z.real, z.imag, color=color, alpha=0.45)
        ax.plot(inv.real, inv.imag, color=color, linewidth=2)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    _style(ax, spec["title"])


def _plot_stereographic(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 24)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))
    ax3.plot_surface(x, y, z, alpha=0.35, color="#d6e6f5", edgecolor="white", linewidth=0.2)
    t = np.linspace(-1.5, 1.5, 80)
    ax3.plot(t, 0 * t, -1 + 0 * t, color=PALETTE["gray"])
    ax3.scatter([0], [0], [1], color=PALETTE["red"], s=40)
    ax3.plot([0, 0.7], [0, 0.45], [1, -1], color=PALETTE["blue"], linewidth=2)
    ax3.set_title(spec["title"])
    ax3.set_axis_off()


def _plot_mobius_dynamics(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(0, 2 * np.pi, 240)
    for radius, color in [(0.25, PALETTE["blue"]), (0.5, PALETTE["teal"]), (0.75, PALETTE["gold"])]:
        z = radius * np.exp(1j * theta)
        w = disk_automorphism(z, 0.35)
        ax.plot(w.real, w.imag, color=color, linewidth=1.4)
    ax.scatter([0.35, -0.35], [0, 0], color=[PALETTE["red"], PALETTE["violet"]], s=35)
    _style(ax, spec["title"])


def _plot_orbit(ax: Any, spec: dict[str, Any]) -> None:
    base = 0.75 + 0.25j
    orbit = np.array([base * np.exp(1j * k * np.pi / 2) for k in range(4)])
    ax.scatter(orbit.real, orbit.imag, color=PALETTE["blue"], s=50)
    for z in orbit:
        ax.plot([0, z.real], [0, z.imag], color=PALETTE["gray"], linewidth=0.8)
    ax.add_patch(Circle((0, 0), abs(base), fill=False, color=PALETTE["teal"], linestyle="--"))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    _style(ax, spec["title"])


def _plot_euclidean_invariants(ax: Any, spec: dict[str, Any]) -> None:
    tri = np.array([[0, 0], [1.2, 0.1], [0.35, 0.9]])
    angle = 0.65
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    moved = tri @ rot.T + np.array([1.4, 0.45])
    ax.add_patch(Polygon(tri, fill=False, edgecolor=PALETTE["blue"], linewidth=2, label="original"))
    ax.add_patch(Polygon(moved, fill=False, edgecolor=PALETTE["red"], linewidth=2, label="moved"))
    ax.legend(fontsize=8)
    ax.set_xlim(-0.3, 2.7)
    ax.set_ylim(-0.2, 1.9)
    _style(ax, spec["title"])


def _plot_homogeneity(ax: Any, spec: dict[str, Any]) -> None:
    groups = ["translations", "rotations", "euclidean", "mobius"]
    props = ["point move", "direction move", "distance"]
    data = np.array([[1, 0, 1], [0, 1, 1], [1, 1, 1], [1, 1, 0]])
    ax.imshow(data, cmap="PuBuGn", vmin=0, vmax=1)
    ax.set_xticks(range(3), props, rotation=25, ha="right")
    ax.set_yticks(range(4), groups)
    for i in range(4):
        for j in range(3):
            ax.text(j, i, "yes" if data[i, j] else "no", ha="center", va="center", fontsize=8)
    ax.set_title(spec["title"], fontsize=11)


def _plot_mobius_distance(ax: Any, spec: dict[str, Any]) -> None:
    xs = np.array([0.45, 0.7, 1.1])
    ys = np.zeros_like(xs)
    inv = 1 / xs
    ax.scatter(xs, ys + 0.3, color=PALETTE["blue"], label="before")
    ax.scatter(inv, ys - 0.3, color=PALETTE["red"], label="after 1/z")
    for x, y in zip(xs, inv):
        ax.plot([x, y], [0.3, -0.3], "--", color=PALETTE["gray"])
    ax.legend(fontsize=8)
    ax.set_xlim(0, 2.5)
    ax.set_ylim(-0.8, 0.8)
    _style(ax, spec["title"], equal=False)


def _plot_hyperbolic_disk(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(0, 2 * np.pi, 240)
    for c, r in [(0.45, 0.55), (-0.35, 0.65), (0, 0)]:
        if r == 0:
            ax.plot([-0.9, 0.9], [0, 0], color=PALETTE["blue"], linewidth=1.5)
        else:
            z = c + r * np.exp(1j * theta)
            mask = np.abs(z) <= 1.001
            ax.plot(z.real[mask], z.imag[mask], color=PALETTE["blue"], linewidth=1.3)
    _style(ax, spec["title"])


def _plot_hyperbolic_parallel(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    ax.plot([-0.9, 0.9], [0, 0], color=PALETTE["ink"], linewidth=1.4)
    p = np.array([0.0, 0.45])
    ax.scatter([p[0]], [p[1]], color=PALETTE["red"], s=35)
    xs = np.linspace(-0.85, 0.85, 120)
    for bend, color in [(0.35, PALETTE["blue"]), (0.65, PALETTE["teal"]), (0.9, PALETTE["gold"])]:
        y = p[1] + bend * (xs**2 - 0.1)
        mask = xs**2 + y**2 < 1
        ax.plot(xs[mask], y[mask], color=color)
    _style(ax, spec["title"])


def _plot_metric_density(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(0, 0.96, 200)
    ax.plot(r, 2 / (1 - r**2), color=PALETTE["red"], label="hyperbolic density")
    ax.plot(r, 2 / (1 + r**2), color=PALETTE["blue"], label="elliptic density")
    ax.set_xlabel("Euclidean radius")
    ax.set_ylabel("metric density")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_hyperbolic_circle(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    center = 0.35 + 0.15j
    for radius, color in [(0.25, PALETTE["blue"]), (0.45, PALETTE["teal"]), (0.65, PALETTE["gold"])]:
        theta = np.linspace(0, 2 * np.pi, 180)
        z = center + radius * np.exp(1j * theta)
        z = z[np.abs(z) < 0.98]
        ax.plot(z.real, z.imag, color=color)
    ax.scatter([center.real], [center.imag], color=PALETTE["red"])
    _style(ax, spec["title"])


def _plot_triangle_defect(ax: Any, spec: dict[str, Any]) -> None:
    sums = np.linspace(0.1, np.pi - 0.05, 180)
    area = np.pi - sums
    ax.plot(sums, area, color=PALETTE["red"], linewidth=2, label="hyperbolic area")
    ax.plot(np.pi + sums * 0.5, sums * 0.5, color=PALETTE["blue"], linewidth=2, label="elliptic excess")
    ax.axvline(np.pi, color=PALETTE["gray"], linestyle="--")
    ax.set_xlabel("angle sum")
    ax.set_ylabel("area scale")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_halfplane(ax: Any, spec: dict[str, Any]) -> None:
    ax.axhline(0, color=PALETTE["ink"], linewidth=1.5)
    xs = np.linspace(-2, 2, 240)
    for c, r in [(-0.8, 0.8), (0.5, 1.0), (1.6, 0.55)]:
        theta = np.linspace(0, np.pi, 120)
        ax.plot(c + r * np.cos(theta), r * np.sin(theta), color=PALETTE["blue"])
    ax.plot([0, 0], [0, 2.0], color=PALETTE["teal"])
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-0.1, 2.2)
    _style(ax, spec["title"])


def _plot_antipodes(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    pts = np.array([0.35 + 0.25j, -0.4 + 0.55j, 0.7 - 0.15j])
    for z in pts:
        za = -1 / np.conjugate(z)
        ax.scatter([z.real], [z.imag], color=PALETTE["blue"])
        ax.scatter([za.real], [za.imag], color=PALETTE["red"], marker="x")
        ax.plot([z.real, za.real], [z.imag, za.imag], "--", color=PALETTE["gray"])
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    _style(ax, spec["title"])


def _plot_elliptic_clines(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(0, 2 * np.pi, 240)
    for angle, color in [(0, PALETTE["blue"]), (0.7, PALETTE["teal"]), (1.4, PALETTE["gold"])]:
        ax.plot(np.cos(angle) * np.linspace(-1, 1, 100), np.sin(angle) * np.linspace(-1, 1, 100), color=color)
    ax.plot(0.25 + 0.95 * np.cos(theta), 0.1 + 0.95 * np.sin(theta), color=PALETTE["red"], alpha=0.8)
    _style(ax, spec["title"])


def _plot_projective_disk(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(0, 2 * np.pi, 16, endpoint=False)
    for t in theta[::2]:
        ax.arrow(np.cos(t), np.sin(t), -0.001 * np.cos(t), -0.001 * np.sin(t), color=PALETTE["blue"], head_width=0.08)
        ax.plot([np.cos(t), -np.cos(t)], [np.sin(t), -np.sin(t)], "--", color="#d0d7de", linewidth=0.7)
    path = np.array([[0, 0], [0.5, 0.3], [0.9, 0.2], [-0.9, -0.2], [-0.4, -0.5]])
    ax.plot(path[:, 0], path[:, 1], color=PALETTE["red"], linewidth=2)
    _style(ax, spec["title"])


def _plot_elliptic_distance(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(0, 2 * np.pi, 240)
    for r, color in [(0.25, PALETTE["blue"]), (0.55, PALETTE["teal"]), (0.9, PALETTE["gold"])]:
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=color)
    ax.text(-0.9, -1.05, "large elliptic circles fold through antipodes", fontsize=8)
    _style(ax, spec["title"])


def _plot_lune(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    theta = np.linspace(-0.55, 0.95, 120)
    ax.fill_between(np.cos(theta), np.sin(theta), -np.sin(theta), color="#d6f0ed", alpha=0.7)
    ax.plot([0, 1], [0, 0], color=PALETTE["blue"], linewidth=2)
    ax.plot([0, np.cos(0.95)], [0, np.sin(0.95)], color=PALETTE["red"], linewidth=2)
    ax.text(0.15, 0.25, "lune area = 2 alpha", fontsize=9)
    _style(ax, spec["title"])


def _plot_elliptic_trig(ax: Any, spec: dict[str, Any]) -> None:
    tri = np.array([[0.0, 0.0], [0.65, 0.1], [0.2, 0.7]])
    _plot_unit_disk(ax)
    ax.add_patch(Polygon(tri, fill=False, edgecolor=PALETTE["blue"], linewidth=2))
    ax.scatter(tri[:, 0], tri[:, 1], color=PALETTE["red"])
    ax.text(-0.9, -1.05, "cos(c) = cos(a)cos(b)+sin(a)sin(b)cos(gamma)", fontsize=8)
    _style(ax, spec["title"])


def _plot_curvature_growth(ax: Any, spec: dict[str, Any]) -> None:
    r = np.linspace(0.04, 1.35, 220)
    for k, color, label in [(-1, PALETTE["red"], "k=-1"), (0, PALETTE["gray"], "k=0"), (1, PALETTE["blue"], "k=+1")]:
        ratio = circumference_k(r, k) / (2 * np.pi * r)
        ax.plot(r, ratio, color=color, label=label)
    ax.axhline(1, color=PALETTE["ink"], linestyle="--")
    ax.set_xlabel("geodesic radius")
    ax.set_ylabel("C/(2*pi*r)")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_scaled_models(ax: Any, spec: dict[str, Any]) -> None:
    for radius, color, label in [(0.7, PALETTE["blue"], "k=+2"), (1.0, PALETTE["gray"], "k=0 scale"), (1.35, PALETTE["red"], "k=-0.55")]:
        ax.add_patch(Circle((0, 0), radius, fill=False, color=color, linewidth=1.8, label=label))
    ax.legend(fontsize=8)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    _style(ax, spec["title"])


def _plot_parallel_angle(ax: Any, spec: dict[str, Any]) -> None:
    d = np.linspace(0, 4, 180)
    for k, color in [(-0.25, PALETTE["blue"]), (-1, PALETTE["red"]), (-4, PALETTE["gold"])]:
        ax.plot(d, [angle_of_parallelism(float(x), k) for x in d], color=color, label=f"k={k}")
    ax.set_xlabel("distance")
    ax.set_ylabel("angle")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_surface_classifier(ax: Any, spec: dict[str, Any]) -> None:
    rows = [classify_catalog("sphere", True, 0), classify_catalog("torus", True, 1), classify_catalog("two-holed torus", True, 2), classify_catalog("projective plane", False, 1), classify_catalog("Klein bottle", False, 2), classify_catalog("C3", False, 3)]
    ax.axis("off")
    text = "surface              chi   geometry\n" + "\n".join(f"{r.name:<20} {r.euler:>3}   {r.geometry}" for r in rows)
    ax.text(0.02, 0.95, text, va="top", family="monospace", fontsize=10, color=PALETTE["ink"])
    ax.set_title(spec["title"], fontsize=11)


def _plot_gauss_bonnet(ax: Any, spec: dict[str, Any]) -> None:
    genus = np.arange(0, 6)
    ax.plot(genus, [2 - 2 * g for g in genus], "o-", color=PALETTE["blue"], label="H_g")
    ax.plot(np.arange(1, 7), [2 - g for g in range(1, 7)], "s-", color=PALETTE["red"], label="C_g")
    ax.axhline(0, color=PALETTE["gray"], linestyle="--")
    ax.set_xlabel("genus")
    ax.set_ylabel("Euler characteristic")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_dirichlet(ax: Any, spec: dict[str, Any]) -> None:
    w, h = 3.0, 2.0
    base = np.array([0.8, 0.7])
    images = torus_images(tuple(base), w, h, radius=1)
    ax.scatter(images[:, 0], images[:, 1], color=PALETTE["blue"], s=22)
    ax.add_patch(Rectangle((0, 0), w, h, fill=False, edgecolor=PALETTE["ink"], linewidth=1.5))
    ax.add_patch(Rectangle((base[0] - w / 2, base[1] - h / 2), w, h, fill=False, edgecolor=PALETTE["red"], linestyle="--", linewidth=1.6))
    ax.set_xlim(-1.2, 4.2)
    ax.set_ylim(-1.1, 3.1)
    _style(ax, spec["title"])


def _plot_three_geometries(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    t = np.linspace(-1, 1, 80)
    ax3.plot(t, 0 * t, 0 * t, color=PALETTE["blue"], label="Euclidean line")
    ax3.plot(np.sin(t), np.cos(t), t * 0.4, color=PALETTE["teal"], label="curved geodesic view")
    ax3.scatter([0], [0], [0], color=PALETTE["red"])
    ax3.legend(fontsize=7)
    ax3.set_title(spec["title"])
    ax3.set_axis_off()


def _plot_three_torus(ax: Any, spec: dict[str, Any]) -> None:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    r = [0, 1]
    for x in r:
        for y in r:
            ax3.plot([x, x], [y, y], [0, 1], color=PALETTE["ink"])
    for x in r:
        for z in r:
            ax3.plot([x, x], [0, 1], [z, z], color=PALETTE["ink"])
    for y in r:
        for z in r:
            ax3.plot([0, 1], [y, y], [z, z], color=PALETTE["ink"])
    ax3.text(0.5, -0.1, 0.5, "opposite faces identified", fontsize=8)
    ax3.set_title(spec["title"])
    ax3.set_axis_off()


def _plot_dodecahedron(ax: Any, spec: dict[str, Any]) -> None:
    theta = np.linspace(0, 2 * np.pi, 6)[:-1] + np.pi / 5
    outer = np.c_[np.cos(theta), np.sin(theta)]
    inner = 0.45 * outer
    for i in range(5):
        poly = np.vstack([outer[i], outer[(i + 1) % 5], inner[(i + 1) % 5], inner[i]])
        ax.add_patch(Polygon(poly, fill=True, alpha=0.35, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]][i]))
    ax.add_patch(Polygon(inner, fill=False, edgecolor=PALETTE["ink"], linewidth=1.5))
    ax.text(0, 0, "opposite-face\n36 deg or 108 deg twist", ha="center", va="center", fontsize=8)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    _style(ax, spec["title"])


def _plot_psh(ax: Any, spec: dict[str, Any]) -> None:
    rng = np.random.default_rng(3)
    simple = rng.random((50, 2)) * 8
    torus = torus_catalog(seed=5, base_count=8, width=3.0, height=2.2, copies=1)
    ax.hist(pair_distances(simple), bins=28, alpha=0.55, label="simply connected", color=PALETTE["gray"])
    ax.hist(pair_distances(torus), bins=28, alpha=0.55, label="torus images", color=PALETTE["blue"])
    ax.set_xlabel("pair separation")
    ax.set_ylabel("count")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_lss(ax: Any, spec: dict[str, Any]) -> None:
    _plot_unit_disk(ax)
    sep = 1.25
    r_obs = 0.85
    circle_radius = sphere_intersection_circle_radius(r_obs, sep)
    ax.add_patch(Circle((-sep / 2, 0), r_obs, fill=False, edgecolor=PALETTE["blue"], linewidth=1.4))
    ax.add_patch(Circle((sep / 2, 0), r_obs, fill=False, edgecolor=PALETTE["teal"], linewidth=1.4))
    ax.plot([0, 0], [-circle_radius, circle_radius], color=PALETTE["red"], linewidth=2, label="matching circle slice")
    ax.legend(fontsize=8)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.1, 1.1)
    _style(ax, spec["title"])


def _plot_friedmann(ax: Any, spec: dict[str, Any]) -> None:
    omega_m = np.linspace(0, 1, 100)
    omega_l = 1 - omega_m
    ax.fill_between(omega_m, 0, omega_l, color="#d6f0ed", alpha=0.8)
    ax.plot(omega_m, omega_l, color=PALETTE["blue"], label="Omega_k = 0")
    ax.scatter([0.28], [0.72], color=PALETTE["red"], s=50, label="chapter-era near-flat point")
    ax.set_xlabel("Omega_M")
    ax.set_ylabel("Omega_Lambda")
    ax.legend(fontsize=8)
    _style(ax, spec["title"], equal=False)


def _plot_glossary_map(ax: Any, spec: dict[str, Any]) -> None:
    labels = ["C", "Mobius", "D/H", "P2/S", "X_k", "chi", "Omega"]
    theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    pts = np.c_[np.cos(theta), np.sin(theta)]
    for i, label in enumerate(labels):
        ax.scatter([pts[i, 0]], [pts[i, 1]], s=160, color=PALETTE["blue"])
        ax.text(pts[i, 0], pts[i, 1], label, color="white", ha="center", va="center", fontsize=8)
        ax.plot([0, pts[i, 0]], [0, pts[i, 1]], color="#c9d4df")
    ax.text(0, 0, "course\nnotation", ha="center", va="center", fontsize=9)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    _style(ax, spec["title"])


PLOTTERS = {
    "torus": _plot_torus,
    "sphere": _plot_sphere,
    "parallel": _plot_parallel,
    "cone": _plot_cone,
    "hexagon": _plot_hexagon,
    "erlangen": _plot_erlangen,
    "complex_vectors": _plot_complex_vectors,
    "conjugate": _plot_conjugate,
    "polar": _plot_polar,
    "multiplication": _plot_multiplication,
    "angle": _plot_angle,
    "region": _plot_region,
    "affine_grid": _plot_affine_grid,
    "reflection": _plot_reflection,
    "inversion": _plot_inversion,
    "clines": _plot_clines,
    "stereographic": _plot_stereographic,
    "mobius_dynamics": _plot_mobius_dynamics,
    "orbit": _plot_orbit,
    "euclidean_invariants": _plot_euclidean_invariants,
    "homogeneity": _plot_homogeneity,
    "mobius_distance": _plot_mobius_distance,
    "hyperbolic_disk": _plot_hyperbolic_disk,
    "hyperbolic_parallel": _plot_hyperbolic_parallel,
    "metric_density": _plot_metric_density,
    "hyperbolic_circle": _plot_hyperbolic_circle,
    "triangle_defect": _plot_triangle_defect,
    "halfplane": _plot_halfplane,
    "antipodes": _plot_antipodes,
    "elliptic_clines": _plot_elliptic_clines,
    "projective_disk": _plot_projective_disk,
    "elliptic_distance": _plot_elliptic_distance,
    "lune": _plot_lune,
    "elliptic_trig": _plot_elliptic_trig,
    "curvature_growth": _plot_curvature_growth,
    "scaled_models": _plot_scaled_models,
    "parallel_angle": _plot_parallel_angle,
    "surface_classifier": _plot_surface_classifier,
    "gauss_bonnet": _plot_gauss_bonnet,
    "dirichlet": _plot_dirichlet,
    "three_geometries": _plot_three_geometries,
    "three_torus": _plot_three_torus,
    "dodecahedron": _plot_dodecahedron,
    "psh": _plot_psh,
    "lss": _plot_lss,
    "friedmann": _plot_friedmann,
    "glossary_map": _plot_glossary_map,
}


def render_visuals(artifact_root: str | Path, specs: list[dict[str, Any]]) -> tuple[list[Path], list[dict[str, Any]]]:
    paths: list[Path] = []
    stats: list[dict[str, Any]] = []
    for spec in specs:
        fig = plt.figure(figsize=(7.0, 4.8))
        ax = fig.add_subplot(111)
        plotter = PLOTTERS[spec["kind"]]
        plotter(ax, spec)
        fig.suptitle(spec.get("note", ""), y=0.02, fontsize=8, color=PALETTE["gray"])
        path = save_matplotlib(fig, artifact_root, "figures", spec["filename"])
        plt.close(fig)
        paths.append(path)
        stats.append(image_stats(path))
    return paths, stats


def build_parameter_lab_html(chapter: dict[str, Any], specs: list[dict[str, Any]]) -> str:
    visual_rows = "\n".join(
        f"<li><strong>{item['title']}</strong>: {item['note']}</li>" for item in specs
    )
    return f"""<!doctype html>
<html lang=\"en\">
<meta charset=\"utf-8\">
<title>{chapter['title']} parameter lab</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 1.5rem; color: #1f2933; }}
.panel {{ border: 1px solid #cbd5df; border-radius: 6px; padding: 1rem; max-width: 900px; }}
input {{ width: 100%; }}
code {{ background: #eef3f7; padding: 0.1rem 0.25rem; border-radius: 3px; }}
</style>
<body>
<div class=\"panel\">
  <h1>{chapter['title']}: parameter lab</h1>
  <p>{chapter['goal']}</p>
  <label>Parameter <code>t</code>: <span id=\"value\">0.50</span></label>
  <input id=\"slider\" type=\"range\" min=\"0\" max=\"1\" step=\"0.01\" value=\"0.5\">
  <p id=\"output\"></p>
  <h2>Visual inspection targets</h2>
  <ul>{visual_rows}</ul>
</div>
<script>
const slider = document.getElementById('slider');
const value = document.getElementById('value');
const output = document.getElementById('output');
function render() {{
  const t = Number(slider.value);
  value.textContent = t.toFixed(2);
  const curved = Math.sinh(t * 2) / 2;
  const circular = Math.sin(t * Math.PI / 2);
  output.textContent = `Euclidean parameter: ${{t.toFixed(3)}}; hyperbolic-like response: ${{curved.toFixed(3)}}; elliptic-like response: ${{circular.toFixed(3)}}.`;
}}
slider.addEventListener('input', render);
render();
</script>
</body>
</html>"""


def chapter_numeric_checks(chapter_number: int) -> dict[str, float | str]:
    values: dict[str, float | str] = {"chapter": float(chapter_number)}
    values["complex_product_residual"] = float(abs((1 + 2j) * (3 - 1j) - (5 + 5j)))
    values["hyperbolic_distance_positive"] = float((2 * np.arctanh(0.4)) > 0)
    values["curvature_zero_circumference"] = float(abs(circumference_k(0.8, 0) - 2 * np.pi * 0.8))
    values["disk_area_positive"] = float(disk_area_k(0.7, -1) > 0)
    values["right_hypotenuse_euclidean"] = float(abs(unified_right_hypotenuse(1.0, 0) - math.sqrt(2)))
    values["lss_circle_radius"] = float(sphere_intersection_circle_radius(1.0, 1.2))
    values["status"] = "ok"
    return values
