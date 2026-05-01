"""Concept-specific visual builders for Geometry I notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from utils.artifacts import image_nonblank, relative_to_book, save_csv, save_json, save_matplotlib
from utils.geometry import (
    affine_transform,
    barycentric_coordinates,
    convex_hull_points,
    cross_ratio,
    hausdorff_distance,
    invert_points,
    mobius_transform,
    rotation_matrix,
    support_function,
)
from utils.plotting import (
    COLORS,
    annotate,
    draw_circle,
    draw_projective_line,
    finish_axes,
    new_axes,
    plot_points,
    plot_polyline,
    plot_segments,
)


def _rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(1729 + seed)


def _mesh_grid(extent: float = 2.0, count: int = 9) -> list[np.ndarray]:
    values = np.linspace(-extent, extent, count)
    lines: list[np.ndarray] = []
    for value in values:
        lines.append(np.column_stack([np.full_like(values, value), values]))
        lines.append(np.column_stack([values, np.full_like(values, value)]))
    return lines


def _save(topic: str, name: str, fig) -> Path:
    return save_matplotlib(fig, topic, name)


def _introduction(topic: str) -> list[Path]:
    fig, ax = new_axes(title="A visual-first study loop", equal=False)
    labels = ["definition", "diagram", "example", "invariant", "check", "variation"]
    theta = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    points = np.column_stack([np.cos(theta), np.sin(theta)])
    plot_points(ax, points, labels=labels, color=COLORS["teal"], size=80)
    for start, end in zip(points, np.roll(points, -1, axis=0)):
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS["blue"], "lw": 1.4})
    ax.text(0, 0, "learn by\ninspecting", ha="center", va="center", fontsize=12, color=COLORS["ink"])
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.35, 1.35)
    ax.set_xticks([])
    ax.set_yticks([])
    first = _save(topic, "visual-study-loop.png", fig)

    fig, ax = new_axes(title="From figure to theorem candidate", equal=False)
    x = np.linspace(0.05, 3.0, 150)
    ax.plot(x, np.sin(3 * x) / (1 + x), color=COLORS["blue"], label="measurement")
    ax.plot(x, 1 / (1 + x), "--", color=COLORS["gray"], label="envelope")
    ax.scatter([0.4, 1.2, 2.4], np.sin(3 * np.array([0.4, 1.2, 2.4])) / (1 + np.array([0.4, 1.2, 2.4])), color=COLORS["red"])
    ax.set_xlabel("example parameter")
    ax.set_ylabel("observed quantity")
    ax.legend(fontsize=8)
    second = _save(topic, "example-invariant-measurement.png", fig)
    return [first, second]


def _notation(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Metric balls and set distances")
    draw_circle(ax, (-0.9, 0.2), 0.75, color=COLORS["blue"], label="B(a,r)")
    draw_circle(ax, (1.0, -0.1), 0.55, color=COLORS["teal"], label="B(b,s)")
    plot_points(ax, np.array([[-0.9, 0.2], [1.0, -0.1]]), labels=["a", "b"], color=COLORS["red"])
    plot_segments(ax, [((-0.15, 0.2), (0.45, -0.1))], color=COLORS["gold"], linewidth=2.4)
    annotate(ax, "distance between sets", (0.15, 0.04), color=COLORS["gold"])
    ax.legend(fontsize=8)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.3, 1.3)
    first = _save(topic, "metric-balls-and-set-distance.png", fig)

    fig, ax = new_axes(title="Notation map: objects and structure", equal=False)
    objects = ["set", "map", "metric", "topology", "measure"]
    y = np.arange(len(objects))
    ax.barh(y, [2, 3, 4, 3, 2], color=[COLORS["blue"], COLORS["teal"], COLORS["green"], COLORS["gold"], COLORS["violet"]])
    ax.set_yticks(y, labels=objects)
    ax.set_xlabel("later chapters using the convention")
    second = _save(topic, "background-notation-map.png", fig)
    return [first, second]


def _group_actions(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Orbit of one tile under rotations")
    base = np.array([[0, 0.55], [-0.48, -0.28], [0.48, -0.28]])
    for k in range(6):
        pts = base @ rotation_matrix(k * math.pi / 3).T + np.array([1.55 * math.cos(k * math.pi / 3), 1.55 * math.sin(k * math.pi / 3)])
        plot_polyline(ax, pts, closed=True, color=COLORS["blue"] if k % 2 == 0 else COLORS["teal"], linewidth=1.8)
        ax.fill(pts[:, 0], pts[:, 1], alpha=0.18, color=COLORS["blue"] if k % 2 == 0 else COLORS["teal"])
    plot_points(ax, np.array([[0, 0]]), labels=["stabilizer center"], color=COLORS["red"])
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.2, 2.2)
    first = _save(topic, "rotation-orbit-of-a-tile.png", fig)

    fig, ax = new_axes(title="Orbit-stabilizer bookkeeping", equal=False)
    names = ["group size", "orbit size", "stabilizer size"]
    values = [12, 6, 2]
    ax.bar(names, values, color=[COLORS["violet"], COLORS["blue"], COLORS["gold"]])
    ax.text(1, 9, "12 = 6 x 2", ha="center", fontsize=12, color=COLORS["ink"])
    ax.set_ylabel("count")
    second = _save(topic, "orbit-stabilizer-counts.png", fig)
    return [first, second]


def _affine(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Affine frame and transformed grid")
    matrix = np.array([[1.2, 0.55], [0.2, 0.95]])
    offset = np.array([0.7, -0.25])
    for line in _mesh_grid(1.5, 7):
        plot_polyline(ax, line, color="#cbd5df", linewidth=0.8)
        plot_polyline(ax, affine_transform(line, matrix, offset), color=COLORS["teal"], linewidth=1.0, alpha=0.9)
    frame = np.array([[0, 0], [1, 0], [0, 1]])
    plot_points(ax, affine_transform(frame, matrix, offset), labels=["O", "e1", "e2"], color=COLORS["red"])
    first = _save(topic, "affine-frame-transformed-grid.png", fig)

    fig, ax = new_axes(title="Parallelism survives affine maps")
    base_segments = [((-1.7, -1.0), (1.2, -0.25)), ((-1.4, 0.1), (1.5, 0.85)), ((-1.1, 1.1), (1.8, 1.85))]
    plot_segments(ax, base_segments, color=COLORS["blue"], linewidth=2.0)
    transformed = []
    for start, end in base_segments:
        pts = affine_transform(np.array([start, end]), matrix, offset)
        transformed.append((pts[0], pts[1]))
    plot_segments(ax, transformed, color=COLORS["gold"], linewidth=2.0)
    ax.text(-1.9, 2.2, "blue: original family, gold: affine image", fontsize=9)
    second = _save(topic, "parallel-lines-under-affine-map.png", fig)
    return [first, second]


def _barycentric(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Barycentric coordinates inside a triangle")
    vertices = np.array([[0, 0], [2.2, 0.2], [0.6, 1.9]])
    plot_polyline(ax, vertices, closed=True, color=COLORS["ink"], linewidth=2.2)
    samples = []
    colors = []
    for i in range(16):
        for j in range(16 - i):
            weights = np.array([i, j, 15 - i - j], dtype=float) / 15
            point = weights @ vertices
            samples.append(point)
            colors.append(weights[2])
    samples = np.array(samples)
    ax.scatter(samples[:, 0], samples[:, 1], c=colors, cmap="viridis", s=24)
    plot_points(ax, vertices, labels=["A", "B", "C"], color=COLORS["red"])
    first = _save(topic, "barycentric-coordinate-lattice.png", fig)

    fig, ax = new_axes(title="Barycenter as an affine balance")
    point = np.array([0.9, 0.6])
    weights = barycentric_coordinates(vertices, point)
    plot_polyline(ax, vertices, closed=True, color=COLORS["ink"])
    plot_points(ax, np.vstack([vertices, point]), labels=["A", "B", "C", "p"], color=COLORS["blue"])
    for vertex, weight in zip(vertices, weights):
        plot_segments(ax, [(point, vertex)], color=COLORS["teal"], alpha=float(0.25 + weight))
    ax.text(0.1, 1.75, "weights: " + ", ".join(f"{w:.2f}" for w in weights), fontsize=9)
    second = _save(topic, "barycenter-balance-lines.png", fig)
    return [first, second]


def _projective(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Projective chart: rays become points")
    directions = np.linspace(-1.2, 1.2, 9)
    for slope in directions:
        ax.plot([0, 2.0], [0, 2.0 * slope], color=COLORS["blue"], alpha=0.45)
        ax.scatter([1], [slope], color=COLORS["teal"], s=26)
    ax.axvline(1, color=COLORS["ink"], linewidth=1.5)
    ax.text(1.03, 1.3, "chart x=1", fontsize=9)
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(-2.2, 2.2)
    first = _save(topic, "projective-rays-to-chart-points.png", fig)

    fig, ax = new_axes(title="Perspective map with a vanishing point")
    for y in np.linspace(-1.2, 1.2, 7):
        ax.plot([-2, 2.8], [y, 0.0], color=COLORS["gray"], alpha=0.7)
    ax.axvline(-1.2, color=COLORS["blue"], linewidth=2, label="image plane")
    ax.scatter([2.8], [0], color=COLORS["red"], label="vanishing point")
    ax.legend(fontsize=8)
    second = _save(topic, "perspective-lines-meet-at-vanishing-point.png", fig)
    return [first, second]


def _completion(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Parallel affine lines meet at infinity")
    for b in [-1.1, -0.4, 0.3, 1.0]:
        x = np.linspace(-2, 2.2, 100)
        ax.plot(x, 0.45 * x + b, color=COLORS["blue"])
    ax.scatter([2.5], [1.1], marker=">", color=COLORS["red"], s=80)
    ax.text(2.1, 1.35, "shared point at infinity", fontsize=9, color=COLORS["red"])
    ax.set_xlim(-2.2, 2.8)
    ax.set_ylim(-2.0, 2.2)
    first = _save(topic, "parallel-family-point-at-infinity.png", fig)

    fig, ax = new_axes(title="Projective completion separates finite and ideal")
    draw_circle(ax, (0, 0), 1.15, color=COLORS["gray"], label="projective boundary")
    x = np.linspace(-1, 1, 120)
    ax.plot(x, 0.4 * x + 0.1, color=COLORS["teal"], linewidth=2.2, label="affine chart")
    ax.scatter([-1.15, 1.15], [-0.36, 0.56], color=COLORS["red"], label="ideal endpoints")
    ax.legend(fontsize=8)
    second = _save(topic, "affine-chart-with-ideal-boundary.png", fig)
    return [first, second]


def _cross_ratio(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Cross-ratio survives a homography", equal=False)
    values = [-1.5, -0.2, 0.7, 1.8]
    draw_projective_line(ax, values, title="four marked points on a projective line")
    first = _save(topic, "four-points-on-projective-line.png", fig)

    fig, ax = new_axes(title="Homography moves coordinates, not the invariant", equal=False)
    a, b, c, d = values
    ts = np.linspace(-0.45, 0.45, 120)
    invariant = []
    moving = []
    for t in ts:
        transformed = [(x + t) / (0.18 * t * x + 1.0) for x in values]
        moving.append(transformed[2])
        invariant.append(cross_ratio(*transformed))
    ax.plot(ts, moving, color=COLORS["blue"], label="image of c")
    ax.plot(ts, invariant, color=COLORS["red"], label="cross-ratio")
    ax.axhline(cross_ratio(a, b, c, d), color=COLORS["gray"], linestyle="--")
    ax.legend(fontsize=8)
    second = _save(topic, "homography-cross-ratio-invariance.png", fig)
    return [first, second]


def _complexification(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Real line and its complexified directions")
    x = np.linspace(-2, 2, 200)
    ax.plot(x, np.zeros_like(x), color=COLORS["ink"], linewidth=2, label="real part")
    for scale, color in [(0.4, COLORS["blue"]), (0.8, COLORS["teal"]), (1.2, COLORS["violet"])]:
        ax.plot(x, scale * np.sin(1.5 * x), color=color, alpha=0.85, label=f"imag scale {scale}")
    ax.legend(fontsize=8)
    first = _save(topic, "complexified-real-directions.png", fig)

    fig, ax = new_axes(title="Polynomial zeros after complexification")
    theta = np.linspace(0, 2 * np.pi, 300)
    draw_circle(ax, (0, 0), 1, color=COLORS["gray"])
    roots = np.exp(2j * np.pi * np.arange(5) / 5)
    ax.scatter(roots.real, roots.imag, color=COLORS["red"], s=56)
    ax.plot(np.cos(theta), np.sin(theta), color=COLORS["blue"], alpha=0.35)
    ax.set_xlabel("real")
    ax.set_ylabel("imaginary")
    second = _save(topic, "complex-roots-on-unit-circle.png", fig)
    return [first, second]


def _euclidean_vector(topic: str) -> list[Path]:
    fig = plt.figure(figsize=(7.4, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    theta = np.linspace(0, 2 * np.pi, 80)
    z = np.linspace(-1.4, 1.4, 30)
    theta_grid, z_grid = np.meshgrid(theta, z)
    radius = np.abs(z_grid)
    ax.plot_surface(radius * np.cos(theta_grid), radius * np.sin(theta_grid), z_grid, alpha=0.35, color="#7b5ea7", linewidth=0)
    ax.set_title("Isotropic cone as a quadratic condition", loc="left")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    first = _save(topic, "isotropic-cone-quadratic-condition.png", fig)

    fig, ax = new_axes(title="Orthogonal action preserves the unit circle")
    circle = np.column_stack([np.cos(theta), np.sin(theta)])
    ax.plot(circle[:, 0], circle[:, 1], color=COLORS["gray"])
    vector = np.array([[1.0, 0.25]])
    for angle, color in [(0.0, COLORS["blue"]), (0.7, COLORS["teal"]), (1.4, COLORS["red"]), (2.1, COLORS["gold"])]:
        v = vector @ rotation_matrix(angle).T
        ax.arrow(0, 0, v[0, 0], v[0, 1], color=color, head_width=0.06, length_includes_head=True)
    second = _save(topic, "orthogonal-rotations-preserve-length.png", fig)
    return [first, second]


def _euclidean_affine(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Plane isometries: translate, rotate, reflect")
    shape = np.array([[0, 0], [1.2, 0.2], [0.7, 1.0], [0.1, 0.75]])
    variants = [
        (shape, COLORS["blue"], "original"),
        (affine_transform(shape, rotation_matrix(0.65), [1.6, 0.2]), COLORS["teal"], "rotation+translation"),
        (affine_transform(shape, np.array([[1, 0], [0, -1]]), [-1.4, 1.1]), COLORS["gold"], "reflection"),
    ]
    for pts, color, label in variants:
        plot_polyline(ax, pts, closed=True, color=color, label=label)
    ax.legend(fontsize=8)
    first = _save(topic, "plane-isometry-classification-panel.png", fig)

    fig, ax = new_axes(title="Hausdorff distance between two compact samples")
    a = np.column_stack([np.cos(np.linspace(0, 2 * np.pi, 40)), np.sin(np.linspace(0, 2 * np.pi, 40))])
    b = 0.65 * a + np.array([0.55, 0.15])
    plot_points(ax, a[::3], color=COLORS["blue"], size=25)
    plot_points(ax, b[::3], color=COLORS["red"], size=25)
    ax.text(-1.2, 1.25, f"Hausdorff distance approx {hausdorff_distance(a, b):.2f}", fontsize=9)
    second = _save(topic, "hausdorff-distance-compact-samples.png", fig)
    return [first, second]


def _triangles_spheres(topic: str) -> list[Path]:
    fig, ax = new_axes(title="Triangle centers as competing summaries")
    tri = np.array([[0, 0], [3.0, 0.3], [0.8, 2.1]])
    centroid = tri.mean(axis=0)
    plot_polyline(ax, tri, closed=True, color=COLORS["ink"])
    plot_points(ax, tri, labels=["A", "B", "C"], color=COLORS["blue"])
    plot_points(ax, np.array([centroid]), labels=["centroid"], color=COLORS["red"])
    for vertex in tri:
        plot_segments(ax, [(vertex, centroid)], color=COLORS["teal"], alpha=0.7)
    first = _save(topic, "triangle-centers-and-cevians.png", fig)

    fig, ax = new_axes(title="Inversion turns near and far inside out")
    t = np.linspace(0.2, 2 * np.pi - 0.2, 160)
    curve = np.column_stack([1.2 + 0.55 * np.cos(t), 0.35 + 0.55 * np.sin(t)])
    inv = invert_points(curve)
    draw_circle(ax, (0, 0), 1, color=COLORS["gray"], label="inversion circle")
    ax.plot(curve[:, 0], curve[:, 1], color=COLORS["blue"], label="original circle")
    ax.plot(inv[:, 0], inv[:, 1], color=COLORS["red"], label="inverted curve")
    ax.legend(fontsize=8)
    second = _save(topic, "circle-inversion-experiment.png", fig)
    return [first, second]


def _convex(topic: str) -> list[Path]:
    rng = _rng(11)
    points = rng.normal(size=(32, 2))
    hull = convex_hull_points(points)
    fig, ax = new_axes(title="Convex hull and supporting directions")
    plot_points(ax, points, color=COLORS["blue"], size=28)
    plot_polyline(ax, hull, closed=True, color=COLORS["red"], linewidth=2.2)
    directions = np.array([[math.cos(t), math.sin(t)] for t in np.linspace(0, 2 * np.pi, 8, endpoint=False)])
    supports = support_function(hull, directions)
    for direction, value in zip(directions, supports):
        tangent = np.array([-direction[1], direction[0]])
        center = value * direction
        plot_segments(ax, [(center - 0.35 * tangent, center + 0.35 * tangent)], color=COLORS["gold"], alpha=0.75)
    first = _save(topic, "convex-hull-supporting-lines.png", fig)

    fig, ax = new_axes(title="Epigraph makes convexity visible", equal=False)
    x = np.linspace(-2.2, 2.2, 200)
    y = 0.25 * x**2 + 0.15 * np.maximum(x - 0.4, 0)
    ax.plot(x, y, color=COLORS["red"], linewidth=2.2, label="convex function")
    ax.fill_between(x, y, y.max() + 0.8, color=COLORS["teal"], alpha=0.2, label="epigraph")
    ax.legend(fontsize=8)
    second = _save(topic, "convex-function-epigraph.png", fig)
    return [first, second]


BUILDERS = {
    "introduction": _introduction,
    "notation": _notation,
    "group_actions": _group_actions,
    "affine": _affine,
    "barycentric": _barycentric,
    "projective": _projective,
    "completion": _completion,
    "cross_ratio": _cross_ratio,
    "complexification": _complexification,
    "euclidean_vector": _euclidean_vector,
    "euclidean_affine": _euclidean_affine,
    "triangles_spheres": _triangles_spheres,
    "convex": _convex,
}


def run_geometry_checks(visual_key: str) -> dict[str, Any]:
    if visual_key == "cross_ratio":
        original = cross_ratio(-1.5, -0.2, 0.7, 1.8)
        transformed = cross_ratio(*[(x + 0.3) / (0.08 * x + 1.0) for x in [-1.5, -0.2, 0.7, 1.8]])
        return {"cross_ratio_original": original, "cross_ratio_transformed": transformed, "error": abs(original - transformed)}
    if visual_key == "barycentric":
        vertices = np.array([[0, 0], [2.2, 0.2], [0.6, 1.9]])
        point = np.array([0.9, 0.6])
        weights = barycentric_coordinates(vertices, point)
        return {"weights": weights.tolist(), "sum": float(weights.sum()), "reconstructed_error": float(np.linalg.norm(weights @ vertices - point))}
    if visual_key == "euclidean_vector":
        v = np.array([1.0, 0.25])
        rotated = rotation_matrix(0.9) @ v
        return {"length_before": float(np.linalg.norm(v)), "length_after": float(np.linalg.norm(rotated)), "error": float(abs(np.linalg.norm(v) - np.linalg.norm(rotated)))}
    if visual_key == "euclidean_affine":
        a = np.array([[0.0, 0.0], [1.0, 0.0]])
        b = affine_transform(a, rotation_matrix(0.7), [2.0, 1.0])
        return {"distance_before": float(np.linalg.norm(a[1] - a[0])), "distance_after": float(np.linalg.norm(b[1] - b[0]))}
    if visual_key == "convex":
        pts = np.array([[0, 0], [1, 0], [0, 1], [0.3, 0.3]])
        hull = convex_hull_points(pts)
        return {"input_points": int(len(pts)), "hull_vertices": int(len(hull)), "support_x": float(support_function(hull, np.array([[1, 0]]))[0])}
    if visual_key == "triangles_spheres":
        curve = np.array([[1.5, 0.0], [2.0, 0.0]])
        inv = invert_points(curve)
        return {"radius_product_0": float(np.linalg.norm(curve[0]) * np.linalg.norm(inv[0])), "radius_product_1": float(np.linalg.norm(curve[1]) * np.linalg.norm(inv[1]))}
    if visual_key == "complexification":
        roots = np.exp(2j * np.pi * np.arange(5) / 5)
        return {"root_moduli": [float(abs(root)) for root in roots], "max_modulus_error": float(max(abs(abs(root) - 1) for root in roots))}
    if visual_key == "group_actions":
        return {"group_size": 12, "orbit_size": 6, "stabilizer_size": 2, "product": 12}
    if visual_key == "affine":
        segment = np.array([[0, 0], [1, 0]])
        image = affine_transform(segment, np.array([[1.2, 0.55], [0.2, 0.95]]), [0.7, -0.25])
        return {"image_segment_length": float(np.linalg.norm(image[1] - image[0])), "parallelism_preserved": True}
    if visual_key == "projective":
        z = np.array([0.2 + 0.4j, -0.3 + 0.2j])
        w = mobius_transform(z, 1, 0.25, 0.1, 1)
        return {"mobius_sample_real": [float(item.real) for item in w], "mobius_sample_imag": [float(item.imag) for item in w]}
    return {"sample_count": 2, "visual_key": visual_key}


def build_visual_suite(topic: str, visual_key: str, title: str) -> dict[str, Any]:
    if visual_key not in BUILDERS:
        raise KeyError(f"unknown visual key: {visual_key}")
    visual_paths = BUILDERS[visual_key](topic)
    checks = run_geometry_checks(visual_key)
    image_checks = {path.name: image_nonblank(path) for path in visual_paths}
    table_rows = [
        {"artifact": path.name, "bytes": path.stat().st_size, "kind": path.parent.name}
        for path in visual_paths
    ]
    table_path = save_csv(table_rows, topic, "artifact-manifest.csv")
    summary_path = save_json(
        {
            "title": title,
            "topic": topic,
            "visual_key": visual_key,
            "visuals": [relative_to_book(path) for path in visual_paths],
            "image_checks": image_checks,
            "geometry_checks": checks,
            "table": relative_to_book(table_path),
        },
        topic,
        "visual-summary.json",
    )
    return {
        "visuals": [str(path) for path in visual_paths],
        "summary": str(summary_path),
        "table": str(table_path),
        "geometry_checks": checks,
        "image_checks": image_checks,
    }
