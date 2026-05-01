"""Geometry helpers and chapter visualization builders for GMAM."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageStat

from .artifacts import save_matplotlib
from .plotting import (
    PALETTE,
    angle_degrees,
    annotate_point,
    draw_angle_arc,
    draw_circle,
    draw_polygon,
    draw_ray,
    draw_segment,
    new_figure,
    set_equal,
)


def orientation(a, b, c) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    return float(np.cross(b - a, c - a))


def triangle_area(a, b, c) -> float:
    return abs(orientation(a, b, c)) / 2


def shoelace_area(points) -> float:
    pts = np.asarray(points, dtype=float)
    x = pts[:, 0]
    y = pts[:, 1]
    return float(0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def affine_parameter(a, b, p) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    p = np.asarray(p, dtype=float)
    v = b - a
    return float(np.dot(p - a, v) / np.dot(v, v))


def is_between(a, b, p, *, tol: float = 1e-9) -> bool:
    t = affine_parameter(a, b, p)
    return -tol <= t <= 1 + tol and abs(orientation(a, b, p)) <= tol


def angle_measure(a, o, b) -> float:
    return angle_degrees(np.asarray(a) - np.asarray(o), np.asarray(b) - np.asarray(o))


def hyperbolic_distance_disk(z, w) -> float:
    z = complex(z)
    w = complex(w)
    num = 2 * abs(z - w) ** 2
    den = (1 - abs(z) ** 2) * (1 - abs(w) ** 2)
    return float(math.acosh(1 + num / den))


def image_stats(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        stat = ImageStat.Stat(image.convert("RGB"))
    return {
        "path": path.as_posix(),
        "width": width,
        "height": height,
        "bytes": path.stat().st_size,
        "max_channel_stddev": max(stat.stddev) if stat.stddev else 0.0,
    }


def render_visuals(artifact_root: Path, specs: list[dict[str, Any]]) -> tuple[list[Path], list[dict[str, Any]]]:
    paths: list[Path] = []
    stats: list[dict[str, Any]] = []
    for index, spec in enumerate(specs):
        fig = build_visual(spec, index)
        path = Path(artifact_root) / "figures" / spec["filename"]
        save_matplotlib(fig, path)
        plt.close(fig)
        paths.append(path)
        stats.append(image_stats(path))
    return paths, stats


def build_visual(spec: dict[str, Any], index: int):
    kind = spec.get("kind", "coordinate")
    if kind == "proof_graph":
        return proof_graph_visual(spec, index)
    if kind == "incidence":
        return incidence_visual(spec, index)
    if kind == "partition":
        return partition_visual(spec, index)
    if kind == "mapping":
        return mapping_visual(spec, index)
    if kind == "metric":
        return metric_visual(spec, index)
    if kind == "coordinate":
        return coordinate_visual(spec, index)
    if kind == "affine_line":
        return affine_line_visual(spec, index)
    if kind == "betweenness":
        return betweenness_visual(spec, index)
    if kind == "separation":
        return separation_visual(spec, index)
    if kind == "pasch":
        return pasch_visual(spec, index)
    if kind == "angle":
        return angle_visual(spec, index)
    if kind == "molton":
        return molton_visual(spec, index)
    if kind == "poincare":
        return poincare_visual(spec, index)
    if kind == "congruence":
        return congruence_visual(spec, index)
    if kind == "circle":
        return circle_visual(spec, index)
    if kind == "parallel":
        return parallel_visual(spec, index)
    if kind == "saccheri":
        return saccheri_visual(spec, index)
    if kind == "function_plot":
        return function_plot_visual(spec, index)
    if kind == "hyperbolic_triangle":
        return hyperbolic_triangle_visual(spec, index)
    if kind == "euclidean_parallel":
        return euclidean_parallel_visual(spec, index)
    if kind == "similarity":
        return similarity_visual(spec, index)
    if kind == "scissors":
        return scissors_visual(spec, index)
    if kind == "isometry":
        return isometry_visual(spec, index)
    if kind == "reflection":
        return reflection_visual(spec, index)
    if kind == "pencil":
        return pencil_visual(spec, index)
    if kind == "area":
        return area_visual(spec, index)
    return coordinate_visual(spec, index)


def proof_graph_visual(spec, index):
    fig, ax = new_figure(spec["title"], figsize=(8.2, 5.2))
    graph = nx.DiGraph()
    nodes = ["primitive terms", "axioms", "definitions", "lemmas", "theorems", "models", "checks"]
    graph.add_nodes_from(nodes)
    graph.add_edges_from([
        ("primitive terms", "axioms"),
        ("axioms", "definitions"),
        ("definitions", "lemmas"),
        ("lemmas", "theorems"),
        ("models", "checks"),
        ("axioms", "checks"),
        ("checks", "theorems"),
    ])
    pos = nx.spring_layout(graph, seed=37 + index)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", width=1.8, edge_color="#777777")
    node_colors = [PALETTE[i % len(PALETTE)] for i in range(len(nodes))]
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=1450, alpha=0.95)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=9)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9, va="bottom")
    ax.axis("off")
    return fig


def incidence_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.8))
    fig.suptitle(spec["title"], fontsize=13)
    pts = np.array([[0.1, 0.1], [1.0, 0.15], [0.35, 0.95], [1.2, 0.9]])
    lines = [(0, 1), (0, 2), (1, 3), (2, 3)]
    for ax, shift, title in zip(axes, [0.0, 0.18], ["candidate A", "candidate B"]):
        moved = pts + np.array([shift, 0.0])
        for i, j in lines:
            draw_segment(ax, moved[i], moved[j], color="#2f6fbb")
        for i, p in enumerate(moved):
            annotate_point(ax, p, f"P{i+1}", color=PALETTE[i % len(PALETTE)])
        ax.set_title(title)
        ax.set_xlim(-0.15, 1.65)
        ax.set_ylim(-0.1, 1.25)
        set_equal(ax)
    axes[0].text(0.0, -0.22, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def partition_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    xs = np.arange(12)
    residues = xs % 4
    for r in range(4):
        mask = residues == r
        ax.scatter(xs[mask], np.zeros(mask.sum()) + r * 0.18, s=110, color=PALETTE[r], label=f"class {r}")
        for x in xs[mask]:
            ax.text(x, r * 0.18 + 0.08, str(x), ha="center", fontsize=9)
    for r in range(4):
        members = xs[residues == r]
        ax.plot(members, np.zeros_like(members) + r * 0.18, color=PALETTE[r], lw=3, alpha=0.35)
    ax.set_yticks([])
    ax.set_xlabel("integers sampled from one set")
    ax.legend(loc="upper right")
    ax.text(0.01, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def mapping_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    left = np.array([[0, 0], [0, 1], [0, 2], [0, 3]], dtype=float)
    right = np.array([[3, 0.3], [3, 1.3], [3, 2.3]], dtype=float)
    mapping = [0, 1, 1, 2]
    for i, p in enumerate(left):
        annotate_point(ax, p, f"x{i}", color="#2f6fbb")
    for j, p in enumerate(right):
        annotate_point(ax, p, f"y{j}", color="#d95f02")
    for i, j in enumerate(mapping):
        ax.annotate("", xy=right[j], xytext=left[i], arrowprops={"arrowstyle": "->", "lw": 1.7, "color": "#555555"})
    ax.text(1.45, 3.05, "fiber collision at y1", ha="center", fontsize=10)
    ax.set_xlim(-0.6, 3.7)
    ax.set_ylim(-0.4, 3.5)
    ax.axis("off")
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def metric_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6))
    fig.suptitle(spec["title"], fontsize=13)
    for ax, metric_name, scale in zip(axes, ["Euclidean radius", "Poincare visual radius"], [1.0, 0.55]):
        draw_circle(ax, (0, 0), 1.0, color="#bbbbbb")
        draw_circle(ax, (0.15, 0.05), 0.45 * scale, color="#2f6fbb", fill=True)
        annotate_point(ax, (0.15, 0.05), "center")
        ax.set_title(metric_name)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        set_equal(ax)
    axes[0].text(0.0, -0.2, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def coordinate_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.linspace(0, 2 * np.pi, 240)
    ax.plot(np.cos(theta), np.sin(theta), color="#777777", lw=1.5, label="unit disk chart")
    point = np.array([0.58, 0.42])
    annotate_point(ax, point, "P")
    draw_segment(ax, (0, 0), point, color="#2f6fbb", label="polar radius")
    ax.axhline(0, color="#aaaaaa")
    ax.axvline(0, color="#aaaaaa")
    ax.text(point[0], 0.02, "x", color="#555555")
    ax.text(0.02, point[1], "y", color="#555555")
    ax.legend()
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def affine_line_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2, 3, 100)
    y = 0.55 * x + 0.5
    ax.plot(x, y, color="#2f6fbb", lw=2.5, label="implicit: ax + by + c = 0")
    ax.axvline(1.25, color="#d95f02", lw=2.2, label="vertical: x = constant")
    annotate_point(ax, (-1, -0.05), "A")
    annotate_point(ax, (2, 1.6), "B")
    ax.legend()
    ax.set_xlim(-2.2, 3.2)
    ax.set_ylim(-1.2, 2.8)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def betweenness_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    a = np.array([-1.5, -0.4])
    c = np.array([1.8, 0.8])
    ts = [-0.35, 0.0, 0.35, 0.7, 1.0, 1.25]
    draw_segment(ax, a, c, color="#2f6fbb", lw=3)
    for t in ts:
        p = (1 - t) * a + t * c
        color = "#1b9e77" if 0 <= t <= 1 else "#d95f02"
        annotate_point(ax, p, f"t={t:g}", color=color)
    ax.set_xlim(-2.2, 2.4)
    ax.set_ylim(-1.2, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def separation_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2.5, 2.5, 100)
    y = 0.35 * x + 0.2
    ax.plot(x, y, color="#222222", lw=2.4, label="separating line")
    pts = np.array([[-1.8, 1.2], [-0.6, 0.8], [1.7, 1.5], [-1.5, -1.4], [0.4, -0.8], [1.9, -0.5]])
    side = pts[:, 1] - (0.35 * pts[:, 0] + 0.2)
    for p, s in zip(pts, side):
        color = "#2f6fbb" if s > 0 else "#d95f02"
        annotate_point(ax, p, "+" if s > 0 else "-", color=color)
    ax.legend()
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.0, 2.0)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def pasch_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = [(-1.8, -1.0), (1.8, -0.75), (-0.25, 1.35)]
    draw_polygon(ax, tri, color="#7570b3")
    for label, p in zip(["A", "B", "C"], tri):
        annotate_point(ax, p, label)
    draw_segment(ax, (-2.0, 0.6), (1.2, -1.25), color="#d95f02", label="transversal")
    annotate_point(ax, (-0.78, -0.1), "crosses AC", color="#d95f02")
    annotate_point(ax, (0.92, -0.82), "crosses AB", color="#d95f02")
    ax.legend()
    ax.set_xlim(-2.4, 2.2)
    ax.set_ylim(-1.6, 1.8)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def angle_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    o = np.array([0.0, 0.0])
    u = np.array([1.0, 0.15])
    v = np.array([0.25, 1.0])
    draw_ray(ax, o, u, color="#2f6fbb", label="ray 1")
    draw_ray(ax, o, v, color="#d95f02", label="ray 2")
    draw_angle_arc(ax, o, 0.75, math.degrees(math.atan2(u[1], u[0])), math.degrees(math.atan2(v[1], v[0])), color="#1b9e77")
    annotate_point(ax, o, "O")
    ax.text(0.5, 0.35, f"{angle_degrees(u, v):.1f} deg", color="#1b9e77", fontsize=11)
    ax.set_xlim(-0.4, 2.5)
    ax.set_ylim(-0.4, 2.5)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def molton_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    for slope in [-1.0, -0.35, 0.35, 1.0]:
        xs1 = np.linspace(-2.2, 0, 40)
        xs2 = np.linspace(0, 2.2, 40)
        ax.plot(xs1, slope * xs1, color="#2f6fbb", lw=1.8)
        ax.plot(xs2, (1.7 * slope if slope > 0 else slope) * xs2, color="#d95f02", lw=1.8)
    ax.axvline(0, color="#777777", lw=1)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def poincare_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.linspace(0, 2 * np.pi, 360)
    ax.plot(np.cos(theta), np.sin(theta), color="#222222", lw=2)
    ax.plot([-0.9, 0.9], [0.0, 0.0], color="#2f6fbb", lw=2.2, label="diameter geodesic")
    for center, radius, t0, t1, color in [((0.0, 1.55), 1.25, 220, 320, "#d95f02"), ((1.35, 0.0), 1.05, 135, 225, "#1b9e77")]:
        ang = np.radians(np.linspace(t0, t1, 120))
        ax.plot(center[0] + radius * np.cos(ang), center[1] + radius * np.sin(ang), color=color, lw=2.2)
    annotate_point(ax, (0.0, 0.0), "O")
    ax.legend(loc="upper right")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def congruence_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = np.array([[0, 0], [2.0, 0.1], [0.7, 1.4]])
    angle = np.radians(28)
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    tri2 = tri @ rot.T + np.array([0.2, -0.1])
    draw_polygon(ax, tri, color="#2f6fbb")
    draw_polygon(ax, tri2, color="#d95f02")
    for label, p in zip(["A", "B", "C"], tri):
        annotate_point(ax, p, label, color="#2f6fbb")
    for label, p in zip(["A'", "B'", "C'"], tri2):
        annotate_point(ax, p, label, color="#d95f02")
    ax.set_xlim(-0.8, 2.6)
    ax.set_ylim(-0.7, 2.3)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def circle_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    center = np.array([0.0, 0.0])
    p = np.array([0.72, 0.69])
    draw_circle(ax, center, 1.0, color="#1b9e77")
    annotate_point(ax, center, "C")
    annotate_point(ax, p, "T")
    draw_segment(ax, center, p, color="#2f6fbb", label="radius")
    tangent = np.array([-p[1], p[0]])
    tangent = tangent / np.linalg.norm(tangent)
    draw_segment(ax, p - 1.2 * tangent, p + 1.2 * tangent, color="#d95f02", label="tangent")
    ax.legend()
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def parallel_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2.5, 2.5, 160)
    ax.plot(x, 0.4 * x - 0.6, color="#2f6fbb", lw=2.2, label="reference")
    ax.plot(x, 0.4 * x + 0.7, color="#2f6fbb", lw=2.2, label="Euclidean parallel")
    for a in [-0.6, 0.0, 0.6]:
        ax.plot(x, np.tanh(x + a) + 0.2 * a, color="#d95f02", alpha=0.8, lw=1.8)
    annotate_point(ax, (0.0, 1.25), "exterior point", color="#1b9e77")
    ax.legend()
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.8, 2.0)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def saccheri_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    pts = np.array([[-1.2, -0.8], [1.2, -0.8], [0.9, 0.9], [-0.9, 0.9]])
    draw_polygon(ax, pts, color="#7570b3")
    for label, p in zip(["A", "B", "C", "D"], pts):
        annotate_point(ax, p, label)
    draw_segment(ax, pts[0], pts[3], color="#d95f02")
    draw_segment(ax, pts[1], pts[2], color="#d95f02")
    ax.text(0, -1.05, "base right angles and equal legs", ha="center", fontsize=10)
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.3, 1.4)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def function_plot_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(0, 3, 200)
    ax.plot(x, x, label="Euclidean linear comparison", color="#2f6fbb")
    ax.plot(x, np.sinh(x) / np.sinh(3) * 3, label="curved model growth", color="#d95f02")
    ax.plot(x, np.tanh(x), label="bounded critical profile", color="#1b9e77")
    ax.set_xlabel("parameter")
    ax.set_ylabel("measured response")
    ax.legend()
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def hyperbolic_triangle_visual(spec, index):
    fig = poincare_visual({**spec, "title": spec["title"]}, index)
    ax = fig.axes[0]
    pts = np.array([[0.0, 0.0], [0.65, 0.05], [0.15, 0.7]])
    draw_polygon(ax, pts, color="#e7298a")
    for label, p in zip(["A", "B", "C"], pts):
        annotate_point(ax, p, label, color="#e7298a")
    ax.text(-0.95, -0.95, "angle sum < pi gives defect", fontsize=10)
    return fig


def euclidean_parallel_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    x = np.linspace(-2, 2, 100)
    ax.plot(x, 0 * x, color="#222222", lw=2)
    ax.plot(x, 0 * x + 1.0, color="#2f6fbb", lw=2)
    draw_segment(ax, (-1.4, -0.25), (1.0, 1.35), color="#d95f02", label="transversal")
    ax.text(-1.8, 0.15, "alternate interior angles", fontsize=10)
    ax.text(0.7, 0.55, "sum = 180 deg", fontsize=10)
    ax.legend()
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-0.6, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def similarity_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    tri = np.array([[0, 0], [1.2, 0], [0.35, 0.9]])
    draw_polygon(ax, tri, color="#2f6fbb")
    draw_polygon(ax, 1.7 * tri + np.array([1.7, 0.15]), color="#d95f02")
    ax.text(0.35, -0.25, "scale 1", ha="center")
    ax.text(2.5, -0.25, "scale 1.7", ha="center")
    ax.set_xlim(-0.4, 4.1)
    ax.set_ylim(-0.5, 2.1)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def area_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    poly = np.array([[-1.4, -0.9], [1.3, -0.7], [1.6, 0.7], [-0.3, 1.3], [-1.5, 0.2]])
    draw_polygon(ax, poly, color="#2f6fbb")
    anchor = poly[0]
    for i in range(1, len(poly) - 1):
        draw_segment(ax, anchor, poly[i + 1], color="#d95f02", lw=1.5)
    ax.text(-0.25, -1.25, f"shoelace area = {shoelace_area(poly):.2f}", fontsize=10)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.6, 1.7)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def scissors_visual(spec, index):
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    fig.suptitle(spec["title"], fontsize=13)
    pieces = [
        np.array([[0, 0], [1.5, 0], [0.4, 0.8]]),
        np.array([[1.5, 0], [2.0, 1.0], [0.4, 0.8]]),
    ]
    for ax, title, offset in zip(axes, ["before cut", "after rearrangement"], [np.array([0, 0]), np.array([0.25, -0.15])]):
        for i, piece in enumerate(pieces):
            draw_polygon(ax, piece + offset + np.array([0.35 * i, 0.25 * i]), color=PALETTE[i])
        ax.set_title(title)
        ax.set_xlim(-0.4, 3.0)
        ax.set_ylim(-0.4, 1.8)
        set_equal(ax)
    axes[0].text(0.0, -0.2, spec["inspection"], transform=axes[0].transAxes, fontsize=9)
    return fig


def isometry_visual(spec, index):
    fig, axes = plt.subplots(2, 2, figsize=(8.8, 6.2))
    fig.suptitle(spec["title"], fontsize=13)
    pts = np.array([[0, 0], [1, 0], [0.3, 0.8]])
    transforms = [
        ("translate", pts + np.array([0.5, 0.3])),
        ("rotate", pts @ np.array([[0, -1], [1, 0]])),
        ("reflect", pts * np.array([-1, 1])),
        ("glide-like", pts * np.array([1, -1]) + np.array([0.6, 0.2])),
    ]
    for ax, (title, moved) in zip(axes.ravel(), transforms):
        draw_polygon(ax, pts, color="#bbbbbb")
        draw_polygon(ax, moved, color="#2f6fbb")
        ax.set_title(title)
        ax.set_xlim(-1.4, 2.1)
        ax.set_ylim(-1.2, 1.6)
        set_equal(ax)
    axes.ravel()[0].text(0.0, -0.22, spec["inspection"], transform=axes.ravel()[0].transAxes, fontsize=9)
    return fig


def reflection_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    theta = np.radians(35)
    line1 = np.array([np.cos(theta), np.sin(theta)])
    line2 = np.array([np.cos(-theta), np.sin(-theta)])
    draw_segment(ax, -2 * line1, 2 * line1, color="#2f6fbb", label="mirror 1")
    draw_segment(ax, -2 * line2, 2 * line2, color="#d95f02", label="mirror 2")
    p = np.array([1.0, 0.45])
    annotate_point(ax, p, "P")
    annotate_point(ax, np.array([0.25, 1.05]), "after two reflections", color="#1b9e77")
    draw_angle_arc(ax, (0, 0), 0.55, -35, 35, color="#222222")
    ax.legend()
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.6, 1.6)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def pencil_visual(spec, index):
    fig, ax = new_figure(spec["title"])
    for r, color in zip([0.45, 0.75, 1.05, 1.35], PALETTE):
        draw_circle(ax, (0.2, 0.0), r, color=color)
    for angle in [-35, 0, 35]:
        d = np.array([np.cos(np.radians(angle)), np.sin(np.radians(angle))])
        draw_segment(ax, -1.8 * d + np.array([0.2, 0]), 1.8 * d + np.array([0.2, 0]), color="#555555", lw=1.4)
    annotate_point(ax, (0.2, 0.0), "common center")
    ax.set_xlim(-1.7, 2.1)
    ax.set_ylim(-1.6, 1.6)
    set_equal(ax)
    ax.text(0.02, 0.02, spec["inspection"], transform=ax.transAxes, fontsize=9)
    return fig


def build_parameter_lab(meta: dict[str, Any]):
    chapter = int(meta["number"])
    t = np.linspace(0.05, 2.5, 160)
    if chapter in {7, 8}:
        y1 = np.tanh(t)
        y2 = np.sinh(t) / np.sinh(2.5)
        title = "Parallel and hyperbolic growth parameter lab"
        ytitle = "normalized separation"
    elif chapter == 10:
        y1 = 0.5 * t * (2.5 - t)
        y2 = np.maximum(0, np.pi - (1.0 + 0.25 * t + 0.4))
        title = "Area and defect parameter lab"
        ytitle = "area-like response"
    elif chapter == 11:
        y1 = np.cos(t)
        y2 = np.sin(t)
        title = "Isometry composition parameter lab"
        ytitle = "matrix entry"
    else:
        y1 = t
        y2 = t**2 / t.max()
        title = f"Chapter {chapter} parameter lab"
        ytitle = "computed response"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y1, mode="lines", name="primary invariant"))
    fig.add_trace(go.Scatter(x=t, y=y2, mode="lines", name="comparison"))
    fig.update_layout(title=title, xaxis_title="parameter", yaxis_title=ytitle, template="plotly_white", height=420)
    return fig


def chapter_numeric_checks(meta: dict[str, Any], visual_stats: list[dict[str, Any]]) -> dict[str, Any]:
    a = np.array([0.0, 0.0])
    b = np.array([2.0, 0.0])
    c = np.array([0.5, 1.25])
    midpoint = (a + b) / 2
    checks = {
        "chapter": int(meta["number"]),
        "triangle_area": triangle_area(a, b, c),
        "midpoint_between": is_between(a, b, midpoint),
        "angle_A_degrees": angle_measure(b, a, c),
        "shoelace_area_square": shoelace_area(np.array([[0, 0], [1, 0], [1, 1], [0, 1]])),
        "visual_count": len(visual_stats),
        "minimum_visual_stddev": min(item["max_channel_stddev"] for item in visual_stats) if visual_stats else 0.0,
    }
    if int(meta["number"]) in {8, 10}:
        checks["sample_disk_distance"] = hyperbolic_distance_disk(0.1 + 0.0j, 0.45 + 0.2j)
        checks["sample_angle_defect"] = math.pi - (0.9 + 0.8 + 0.7)
    if int(meta["number"]) == 11:
        theta = math.radians(30)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        checks["rotation_determinant"] = float(np.linalg.det(rot))
    return checks
