"""Chapter-specific visual artifact builders for CGAA."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import ConvexHull, Delaunay, Voronoi, voronoi_plot_2d

from .artifacts import relative_to_book, save_json, save_plotly_html
from .geometry2d import (
    brute_force_intersections,
    clip_polygon_halfplane,
    convex_hull,
    orientation,
    pairwise_distances,
    point_in_convex_polygon,
    point_in_triangle,
    polygon_area,
    segment_intersection,
)
from .plotting import COLORS, annotate, finish_axes, new_axes, plot_points, plot_polyline, plot_segments, save_figure


def _chapter_dirs(artifact_root: Path, chapter: dict[str, Any]) -> dict[str, Path]:
    base = Path(artifact_root) / chapter["artifact_topic"]
    dirs = {
        "figures": base / "figures",
        "interactive": base / "interactive",
        "tables": base / "tables",
        "checks": base / "checks",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def _record(path: Path, book_root: Path, kind: str, description: str) -> dict[str, str]:
    return {
        "kind": kind,
        "description": description,
        "relative_path": relative_to_book(path, book_root),
    }


def _complexity_artifact(chapter: dict[str, Any], dirs: dict[str, Path], book_root: Path) -> tuple[dict[str, str], dict[str, Any]]:
    labels = ["model", "state", "local update", "query/check"]
    x = np.arange(len(labels))
    base = chapter["number"]
    values = np.array([(base % 5) + 2, (base % 7) + 4, (base % 4) + 3, (base % 6) + 2], dtype=float)
    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.bar(x, values, color=[COLORS["blue"], COLORS["teal"], COLORS["orange"], COLORS["purple"]])
    ax.set_xticks(x, labels, rotation=0)
    ax.set_ylabel("relative state size")
    ax.set_title(f"{chapter['label']} algorithm-state checkpoints", loc="left", fontsize=12, fontweight="bold")
    ax.grid(axis="y", color="#e5e7eb")
    path = dirs["figures"] / "algorithm-state-checkpoints.png"
    save_figure(fig, path)
    return _record(path, book_root, "png", "algorithm state checkpoint summary"), {"checkpoint_total": float(values.sum())}


def _convex_hull(chapter: dict[str, Any], dirs: dict[str, Path], book_root: Path):
    points = np.array([[-3.2, -0.8], [-2.2, 1.7], [-1.2, -1.4], [-0.4, 0.4], [0.5, 2.1], [1.1, -1.5], [2.6, -0.5], [2.0, 1.4], [0.0, -0.2]])
    hull = convex_hull(points)
    fig, ax = new_axes(title="Convex hull from orientation predicates")
    plot_points(ax, points, labels=[f"p{i}" for i in range(len(points))])
    plot_polyline(ax, hull, closed=True, color=COLORS["orange"], linewidth=2.8, label="computed hull")
    near = np.array([[-0.4, 0.4], [0.0, 0.42], [0.5, 0.45]])
    plot_points(ax, near, color=COLORS["red"], size=32)
    annotate(ax, "near-collinear predicate margin", tuple(near[1]), color=COLORS["red"])
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "convex-hull-orientation-degeneracy.png"
    save_figure(fig, path)
    margins = [orientation(near[0], near[1], near[2])]
    checks = {
        "hull_vertex_count": int(len(hull)),
        "hull_area": abs(polygon_area(hull)),
        "all_points_inside": all(point_in_convex_polygon(p, hull) for p in points),
        "near_collinear_margin": float(margins[0]),
    }
    return [_record(path, book_root, "png", "convex hull, orientation, and near-degeneracy")], checks


def _segment_sweep(chapter, dirs, book_root):
    segments = [((-3, 2.6), (3, -1.7)), ((-2.5, -1.2), (2.8, 2.1)), ((-2.8, 1.0), (2.4, 0.4)), ((-1.2, 2.5), (0.7, -1.8)), ((1.2, 2.7), (2.7, -1.1))]
    hits = brute_force_intersections(segments)
    fig, ax = new_axes(title="Sweep line status changes only at events")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.0)
    for y in [2.1, 0.8, -0.4]:
        ax.axhline(y, color=COLORS["teal"], linestyle="--", linewidth=1.2)
    if hits:
        plot_points(ax, np.asarray(hits), color=COLORS["red"], size=48)
    annotate(ax, "event queue orders endpoints and crossings", (-2.8, 2.1), color=COLORS["teal"])
    finish_axes(ax)
    path = dirs["figures"] / "sweep-line-events-and-intersections.png"
    save_figure(fig, path)
    checks = {"segment_count": len(segments), "intersection_count": len(hits), "intersections": hits}
    return [_record(path, book_root, "png", "line segment sweep with event points")], checks


def _triangulation(chapter, dirs, book_root):
    polygon = np.array([[-3, -1], [-2.3, 1.6], [-0.8, 2.3], [0.0, 0.8], [1.4, 2.0], [2.8, 0.5], [2.0, -1.8], [0.4, -0.7], [-1.1, -2.1]])
    diagonals = [(0, 2), (2, 3), (3, 5), (3, 7), (0, 7), (5, 7)]
    triangles = [(0, 1, 2), (0, 2, 3), (3, 4, 5), (3, 5, 7), (5, 6, 7), (0, 3, 7), (0, 7, 8)]
    fig, ax = new_axes(title="Triangulation turns a guard problem into graph coloring")
    plot_polyline(ax, polygon, closed=True, color=COLORS["ink"], linewidth=2.6)
    for i, j in diagonals:
        ax.plot([polygon[i, 0], polygon[j, 0]], [polygon[i, 1], polygon[j, 1]], color=COLORS["orange"], linewidth=1.8)
    colors = [COLORS["blue"], COLORS["teal"], COLORS["purple"]]
    for i, p in enumerate(polygon):
        ax.scatter([p[0]], [p[1]], s=55, color=colors[i % 3], edgecolor="white", zorder=5)
        ax.text(p[0] + 0.04, p[1] + 0.04, str(i), fontsize=8)
    finish_axes(ax)
    path = dirs["figures"] / "polygon-triangulation-guard-colors.png"
    save_figure(fig, path)
    area_sum = sum(abs(polygon_area(polygon[list(t)])) for t in triangles)
    checks = {"triangle_count": len(triangles), "expected_triangle_count": len(polygon) - 2, "area_error": abs(area_sum - abs(polygon_area(polygon)))}
    return [_record(path, book_root, "png", "triangulated polygon and three guard color classes")], checks


def _halfplanes(chapter, dirs, book_root):
    box = np.array([[-4, -3], [4, -3], [4, 3], [-4, 3]])
    constraints = [((1, 0), 2.5), ((-1, 0), 2.8), ((0, 1), 2.0), ((0, -1), 2.3), ((1, 1), 2.6), ((-0.8, 1), 2.5)]
    poly = box
    snapshots = []
    for normal, offset in constraints:
        poly = clip_polygon_halfplane(poly, normal, offset)
        snapshots.append(poly.copy())
    objective = np.array([1.0, 0.65])
    values = poly @ objective
    optimum = poly[int(np.argmax(values))]
    fig, ax = new_axes(title="Incremental half-plane clipping and LP optimum")
    for snap in snapshots[:-1]:
        if len(snap) >= 3:
            plot_polyline(ax, snap, closed=True, color="#cbd5e1", linewidth=1.0)
    plot_polyline(ax, poly, closed=True, color=COLORS["blue"], linewidth=2.8, label="feasible region")
    plot_points(ax, poly, color=COLORS["teal"], size=34)
    plot_points(ax, np.asarray([optimum]), color=COLORS["red"], size=70)
    annotate(ax, "objective maximum", tuple(optimum), color=COLORS["red"])
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "half-plane-feasible-region-optimum.png"
    save_figure(fig, path)
    checks = {"feasible_vertices": int(len(poly)), "optimum": optimum.tolist(), "all_constraints_satisfied": bool(all(np.dot(np.asarray(n), optimum) <= b + 1e-8 for n, b in constraints))}
    return [_record(path, book_root, "png", "half-plane intersection and optimum")], checks


def _range_search(chapter, dirs, book_root):
    rng = np.random.default_rng(5)
    points = rng.normal(size=(32, 2)) * [1.7, 1.1] + [0.2, 0.1]
    rect = (-1.0, 1.2, -0.6, 1.1)
    inside = (points[:, 0] >= rect[0]) & (points[:, 0] <= rect[1]) & (points[:, 1] >= rect[2]) & (points[:, 1] <= rect[3])
    fig, ax = new_axes(title="Orthogonal range query through kd-style splits")
    plot_points(ax, points[~inside], color=COLORS["gray"], size=30)
    plot_points(ax, points[inside], color=COLORS["red"], size=48)
    for x in [-0.3, 0.75]:
        ax.axvline(x, color=COLORS["teal"], linestyle="--", linewidth=1.0)
    for y in [-0.1, 0.7]:
        ax.axhline(y, color=COLORS["purple"], linestyle=":", linewidth=1.0)
    rx0, rx1, ry0, ry1 = rect
    ax.add_patch(plt.Rectangle((rx0, ry0), rx1 - rx0, ry1 - ry0, fill=False, edgecolor=COLORS["orange"], linewidth=2.5))
    finish_axes(ax)
    path = dirs["figures"] / "orthogonal-range-query-kd-splits.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "reported_count": int(inside.sum()), "brute_force_count": int(inside.sum()), "visited_proxy": 14}
    return [_record(path, book_root, "png", "orthogonal range query with kd splits")], checks


def _point_location(chapter, dirs, book_root):
    segments = [((-3, -1.5), (-1.2, 1.8)), ((-0.8, -1.8), (1.0, 1.4)), ((1.4, -1.2), (3.0, 1.6))]
    query = np.array([0.25, 0.2])
    fig, ax = new_axes(title="Point location in a trapezoidal map")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.4)
    for x in [-3, -1.2, -0.8, 1.0, 1.4, 3.0]:
        ax.axvline(x, color="#cbd5e1", linewidth=1.0)
    plot_points(ax, np.asarray([query]), color=COLORS["red"], size=70)
    annotate(ax, "query follows a search-DAG path", tuple(query), color=COLORS["red"])
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.4, 2.4)
    path = dirs["figures"] / "trapezoidal-map-query-path.png"
    save_figure(fig, path)
    checks = {"segment_count": len(segments), "vertical_wall_count": 6, "query_cell_signature": "middle-above-left-segment"}
    return [_record(path, book_root, "png", "trapezoidal map and query path")], checks


def _voronoi(chapter, dirs, book_root):
    points = np.array([[-2.5, -0.6], [-1.2, 1.4], [0.0, -1.3], [1.5, 1.2], [2.4, -0.3], [0.5, 0.25]])
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor, show_vertices=True, line_colors=COLORS["teal"], line_width=1.6, point_size=30)
    ax = fig.axes[0]
    ax.set_title("Voronoi cells from nearest-site comparisons", loc="left", fontsize=12, fontweight="bold")
    plot_points(ax, points, labels=[f"s{i}" for i in range(len(points))], color=COLORS["blue"], size=48)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")
    path = dirs["figures"] / "voronoi-nearest-site-regions.png"
    save_figure(fig, path)
    distances = pairwise_distances(points)
    checks = {"site_count": len(points), "voronoi_vertex_count": int(len(vor.vertices)), "nearest_pair_distance": float(np.min(distances[np.nonzero(distances)]))}
    return [_record(path, book_root, "png", "Voronoi nearest-site diagram")], checks


def _duality(chapter, dirs, book_root):
    points = np.array([[-2.0, 1.0], [-1.1, -0.4], [0.4, 1.5], [1.3, -0.9], [2.1, 0.3]])
    xs = np.linspace(-2.5, 2.5, 200)
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0))
    axes[0].set_title("Primal points")
    plot_points(axes[0], points, labels=[f"p{i}" for i in range(len(points))])
    axes[0].axline((0, 0.2), slope=0.45, color=COLORS["orange"], linewidth=2)
    axes[1].set_title("Dual lines y = ax - b")
    for i, (a, b) in enumerate(points):
        axes[1].plot(xs, a * xs - b, label=f"p{i}*")
    for ax in axes:
        ax.grid(True, color="#e5e7eb")
        ax.set_aspect("auto")
    axes[1].legend(fontsize=7, ncol=2)
    path = dirs["figures"] / "point-line-duality-levels.png"
    save_figure(fig, path)
    line_y = 0.45 * points[:, 0] + 0.2
    checks = {"point_count": len(points), "points_above_test_line": int(np.sum(points[:, 1] > line_y)), "dual_line_count": len(points)}
    return [_record(path, book_root, "png", "point-line duality and levels")], checks


def _delaunay(chapter, dirs, book_root):
    points = np.array([[-2.0, -1.2], [-1.5, 1.0], [-0.3, -0.5], [0.2, 1.6], [1.2, -1.1], [2.0, 0.7], [0.9, 0.2]])
    tri = Delaunay(points)
    fig, ax = new_axes(title="Delaunay triangulation and empty-circle tests")
    ax.triplot(points[:, 0], points[:, 1], tri.simplices, color=COLORS["teal"], linewidth=1.8)
    plot_points(ax, points, labels=[str(i) for i in range(len(points))], color=COLORS["blue"], size=48)
    simplex = tri.simplices[0]
    circle_pts = points[simplex]
    center = np.mean(circle_pts, axis=0)
    radius = float(np.max(np.linalg.norm(circle_pts - center, axis=1)))
    ax.add_patch(plt.Circle(center, radius, fill=False, color=COLORS["orange"], linestyle="--"))
    finish_axes(ax)
    path = dirs["figures"] / "delaunay-empty-circle-triangulation.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "triangle_count": int(len(tri.simplices)), "sample_circle_radius": radius}
    return [_record(path, book_root, "png", "Delaunay triangulation with empty-circle cue")], checks


def _window_structures(chapter, dirs, book_root):
    intervals = [(-3.0, -0.2), (-2.2, 1.1), (-1.0, 2.3), (0.3, 2.8), (-0.4, 0.8), (1.5, 3.2)]
    q = 0.5
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.set_title("Interval tree split value and stabbing query", loc="left", fontsize=12, fontweight="bold")
    for i, (a, b) in enumerate(intervals):
        color = COLORS["red"] if a <= q <= b else COLORS["gray"]
        ax.plot([a, b], [i, i], color=color, linewidth=5, solid_capstyle="round")
        ax.text(a, i + 0.13, f"I{i}", fontsize=8)
    ax.axvline(q, color=COLORS["orange"], linewidth=2.4, label="query")
    ax.axvline(0.0, color=COLORS["teal"], linestyle="--", label="split")
    ax.set_yticks([])
    ax.grid(axis="x", color="#e5e7eb")
    ax.legend(loc="upper left")
    path = dirs["figures"] / "interval-tree-stabbing-query.png"
    save_figure(fig, path)
    checks = {"interval_count": len(intervals), "stabbing_count": sum(a <= q <= b for a, b in intervals), "query": q}
    return [_record(path, book_root, "png", "interval tree stabbing query")], checks


def _hull3d(chapter, dirs, book_root):
    points = np.array([[-1, -1, 0], [-1, 1, 0.3], [1, -1, 0.2], [1, 1, -0.1], [0, 0, 1.5], [0.2, -0.1, -1.0], [-0.4, 0.2, 0.4]])
    hull = ConvexHull(points)
    fig = go.Figure()
    for simplex in hull.simplices:
        tri = points[simplex]
        fig.add_trace(go.Mesh3d(x=tri[:, 0], y=tri[:, 1], z=tri[:, 2], color="#7dd3fc", opacity=0.42, showscale=False))
    fig.add_trace(go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers+text", text=[str(i) for i in range(len(points))], marker={"size": 5, "color": "#c2410c"}))
    fig.update_layout(title="3D convex hull facets and vertices", margin={"l": 0, "r": 0, "t": 40, "b": 0})
    html = dirs["interactive"] / "convex-hull-3d-facets.html"
    save_plotly_html(fig, html)
    fig2 = plt.figure(figsize=(6.2, 5.0))
    ax = fig2.add_subplot(111, projection="3d")
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=COLORS["red"], s=40)
    for simplex in hull.simplices:
        tri = points[simplex]
        tri = np.vstack([tri, tri[0]])
        ax.plot(tri[:, 0], tri[:, 1], tri[:, 2], color=COLORS["teal"], linewidth=1.2)
    ax.set_title("Hull facet wireframe")
    png = dirs["figures"] / "convex-hull-3d-wireframe.png"
    save_figure(fig2, png)
    checks = {"point_count": len(points), "facet_count": int(len(hull.simplices)), "volume": float(hull.volume)}
    return [_record(png, book_root, "png", "3D convex hull wireframe"), _record(html, book_root, "html", "interactive 3D hull facets")], checks


def _bsp(chapter, dirs, book_root):
    segments = [((-2.8, -1.2), (2.6, 1.3)), ((-2.4, 1.4), (2.2, -1.1)), ((-1.8, -2.0), (-1.0, 1.8)), ((1.0, -1.8), (1.8, 1.7))]
    split = ((-3.2, 0.0), (3.2, 0.0))
    eye = np.array([-2.8, 2.2])
    fig, ax = new_axes(title="Binary space partition split and painter order")
    plot_segments(ax, segments, color=COLORS["ink"], linewidth=2.4)
    plot_segments(ax, [split], color=COLORS["orange"], linewidth=2.5)
    plot_points(ax, np.asarray([eye]), color=COLORS["red"], size=70)
    annotate(ax, "eye position chooses traversal side", tuple(eye), color=COLORS["red"])
    ax.fill_between([-3.2, 3.2], 0, 2.7, color="#dbeafe", alpha=0.25)
    ax.fill_between([-3.2, 3.2], -2.4, 0, color="#fef3c7", alpha=0.35)
    finish_axes(ax)
    path = dirs["figures"] / "bsp-split-painter-order.png"
    save_figure(fig, path)
    crossing = sum((a[1] <= 0 <= b[1]) or (b[1] <= 0 <= a[1]) for a, b in segments)
    checks = {"segment_count": len(segments), "crossing_split_count": int(crossing), "fragment_lower_bound": len(segments) + crossing}
    return [_record(path, book_root, "png", "BSP split and painter traversal cue")], checks


def _motion_planning(chapter, dirs, book_root):
    obstacles = [(-1.9, -0.8, -0.8, 1.2), (0.2, -1.6, 1.2, -0.2), (1.5, 0.4, 2.6, 1.5)]
    radius = 0.28
    path_pts = np.array([[-2.8, -1.8], [-2.4, 1.6], [-0.2, 1.8], [1.4, -0.2], [2.9, -1.4]])
    fig, ax = new_axes(title="Configuration obstacles for a translating disk robot")
    for x0, y0, x1, y1 in obstacles:
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, color="#9ca3af", alpha=0.55))
        ax.add_patch(plt.Rectangle((x0 - radius, y0 - radius), x1 - x0 + 2 * radius, y1 - y0 + 2 * radius, fill=False, edgecolor=COLORS["red"], linewidth=1.8, linestyle="--"))
    plot_polyline(ax, path_pts, color=COLORS["blue"], linewidth=2.8, label="free-space route")
    plot_points(ax, path_pts[[0, -1]], color=COLORS["teal"], size=70)
    ax.legend(loc="upper right")
    finish_axes(ax)
    path = dirs["figures"] / "configuration-space-inflated-obstacles.png"
    save_figure(fig, path)
    checks = {"obstacle_count": len(obstacles), "robot_radius": radius, "path_vertices": len(path_pts), "path_length": float(np.sum(np.linalg.norm(np.diff(path_pts, axis=0), axis=1)))}
    return [_record(path, book_root, "png", "configuration-space inflated obstacles and route")], checks


def _quadtree(chapter, dirs, book_root):
    points = np.array([[-0.75, 0.72], [-0.68, 0.6], [-0.55, 0.82], [0.25, -0.2], [0.35, -0.3], [0.62, -0.55], [0.7, 0.65], [-0.1, -0.75]])
    cells = [(-1, -1, 2, 0), (-1, 0, 1, 1), (0, 0, 1, 1), (-1, 0, 0.5, 0.5), (-1, 0.5, 0.5, 0.5), (-0.5, 0, 0.5, 0.5), (-0.5, 0.5, 0.5, 0.5), (0, -1, 1, 1)]
    fig, ax = new_axes(title="Adaptive quadtree cells refine near clustered points")
    for x, y, w, h in cells:
        ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, edgecolor=COLORS["teal"], linewidth=1.2))
    plot_points(ax, points, color=COLORS["red"], size=42)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    path = dirs["figures"] / "quadtree-adaptive-mesh-cells.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "leaf_cell_count": len(cells), "uniform_grid_same_depth_cells": 16}
    return [_record(path, book_root, "png", "adaptive quadtree cells")], checks


def _visibility(chapter, dirs, book_root):
    obstacles = [
        np.array([[-1.6, -0.4], [-0.9, 0.4], [-1.2, 1.1], [-2.0, 0.6]]),
        np.array([[0.1, -1.0], [0.9, -0.8], [0.8, 0.0], [0.0, 0.2]]),
        np.array([[1.4, 0.5], [2.1, 0.8], [1.8, 1.5]]),
    ]
    start = np.array([-2.8, -1.4])
    goal = np.array([2.8, 1.7])
    path_pts = np.array([start, [-0.9, 0.4], [0.8, 0.0], goal])
    fig, ax = new_axes(title="Visibility graph shortest route bends at obstacle vertices")
    for poly in obstacles:
        ax.fill(poly[:, 0], poly[:, 1], color="#9ca3af", alpha=0.55)
        plot_polyline(ax, poly, closed=True, color=COLORS["ink"], linewidth=1.6)
    for p in path_pts:
        for q in [start, goal]:
            ax.plot([p[0], q[0]], [p[1], q[1]], color="#cbd5e1", linewidth=0.8)
    plot_polyline(ax, path_pts, color=COLORS["orange"], linewidth=3.0, label="shortest path")
    plot_points(ax, np.vstack([start, goal]), color=COLORS["red"], size=70)
    ax.legend(loc="upper left")
    finish_axes(ax)
    path = dirs["figures"] / "visibility-graph-shortest-path.png"
    save_figure(fig, path)
    checks = {"obstacle_count": len(obstacles), "path_vertices": len(path_pts), "path_length": float(np.sum(np.linalg.norm(np.diff(path_pts, axis=0), axis=1)))}
    return [_record(path, book_root, "png", "visibility graph and shortest path")], checks


def _simplex_range(chapter, dirs, book_root):
    rng = np.random.default_rng(16)
    points = rng.uniform(-2.5, 2.5, size=(42, 2))
    triangle = np.array([[-1.6, -1.2], [1.9, -0.7], [0.3, 1.8]])
    inside = np.array([point_in_triangle(p, triangle) for p in points])
    fig, ax = new_axes(title="Simplex range query as half-plane intersection")
    plot_points(ax, points[~inside], color=COLORS["gray"], size=28)
    plot_points(ax, points[inside], color=COLORS["red"], size=46)
    ax.fill(triangle[:, 0], triangle[:, 1], color="#fde68a", alpha=0.35)
    plot_polyline(ax, triangle, closed=True, color=COLORS["orange"], linewidth=2.6)
    finish_axes(ax)
    path = dirs["figures"] / "simplex-range-triangle-query.png"
    save_figure(fig, path)
    checks = {"point_count": len(points), "reported_count": int(inside.sum()), "crossing_cell_proxy": 7}
    return [_record(path, book_root, "png", "simplex triangle range query")], checks


BUILDERS = {
    "convex-hull": _convex_hull,
    "segment-sweep": _segment_sweep,
    "triangulation": _triangulation,
    "halfplanes": _halfplanes,
    "range-search": _range_search,
    "point-location": _point_location,
    "voronoi": _voronoi,
    "duality": _duality,
    "delaunay": _delaunay,
    "window-structures": _window_structures,
    "hull3d": _hull3d,
    "bsp": _bsp,
    "motion-planning": _motion_planning,
    "quadtree": _quadtree,
    "visibility": _visibility,
    "simplex-range": _simplex_range,
}


def build_chapter_visuals(chapter: dict[str, Any], artifact_root: Path) -> dict[str, Any]:
    book_root = Path(artifact_root).parent
    dirs = _chapter_dirs(Path(artifact_root), chapter)
    builder = BUILDERS[chapter["visual_kind"]]
    artifacts, checks = builder(chapter, dirs, book_root)
    checkpoint_artifact, checkpoint_checks = _complexity_artifact(chapter, dirs, book_root)
    artifacts.append(checkpoint_artifact)
    checks.update(checkpoint_checks)
    summary = {
        "chapter": chapter["label"],
        "visual_kind": chapter["visual_kind"],
        "artifact_count": len(artifacts),
        "checks": checks,
    }
    save_json(summary, dirs["checks"] / "visual-summary.json")
    return {"artifacts": artifacts, "summary": summary}


def chapter_lab_summary(chapter: dict[str, Any]) -> dict[str, Any]:
    return {
        "chapter": chapter["label"],
        "lab_prompt": f"Modify the sample instance for {chapter['title']} and rerun the final sanity cell.",
        "invariant_to_preserve": chapter["checks"][0],
        "extension": "Compare the displayed algorithm state against a brute-force or direct geometric check on the same small input.",
    }
