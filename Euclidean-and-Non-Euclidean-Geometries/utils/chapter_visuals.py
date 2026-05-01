"""Reusable chapter visual builders for the ENEG course."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from .artifacts import save_matplotlib
from .geometry_helpers import Line, angle_between, circle_from_three_points, norm, oriented_area, reflect_point_across_line, rotate
from .hyperbolic import angle_of_parallelism, defect_area, geodesic_circle_center, klein_to_poincare, poincare_distance, poincare_to_klein
from .plotting import (
    ENEG_COLORS,
    draw_angle_arc,
    draw_circle,
    draw_points,
    draw_polygon,
    draw_segment,
    equal_limits,
    setup_figure,
)


def save_relationship_map(labels: list[str], path, title: str):
    fig, ax = setup_figure(width=7.4, height=4.8, title=title, equal=False, grid=False)
    ax.set_xlim(-0.5, len(labels) - 0.5)
    ax.set_ylim(-1.2, 1.4)
    ax.axis("off")
    y_values = [0.6 if index % 2 == 0 else -0.1 for index in range(len(labels))]
    palette = [ENEG_COLORS["blue"], ENEG_COLORS["teal"], ENEG_COLORS["gold"], ENEG_COLORS["violet"], ENEG_COLORS["green"]]
    for index, (label, y) in enumerate(zip(labels, y_values, strict=False)):
        color = palette[index % len(palette)]
        circle = plt.Circle((index, y), 0.28, color=color, alpha=0.18, ec=color, lw=2)
        ax.add_patch(circle)
        ax.text(index, y, label, ha="center", va="center", fontsize=9, weight="bold")
        if index:
            ax.annotate(
                "",
                xy=(index - 0.28, y),
                xytext=(index - 0.72, y_values[index - 1]),
                arrowprops={"arrowstyle": "->", "lw": 1.6, "color": ENEG_COLORS["gray"]},
            )
    ax.text(
        0.02,
        -0.95,
        "Inspection target: read arrows as dependencies or interpretations, not decoration.",
        fontsize=9,
        color=ENEG_COLORS["ink"],
    )
    save_matplotlib(fig, path)
    plt.close(fig)
    return path


def save_scene(kind: str, path):
    if kind == "parallel-regimes":
        fig, ax = setup_figure(width=7.4, height=5.0, title="Three parallel regimes", equal=True, grid=True)
        xs = np.linspace(-2.5, 2.5, 120)
        ax.plot(xs, 0 * xs, color=ENEG_COLORS["ink"], lw=2, label="base line")
        ax.plot(xs, 0.75 + 0 * xs, color=ENEG_COLORS["blue"], lw=2, label="Euclidean unique parallel")
        ax.plot(xs, 0.75 + 0.28 * xs, color=ENEG_COLORS["teal"], lw=1.7, label="hyperbolic-style extra parallels")
        ax.plot(xs, 0.75 - 0.28 * xs, color=ENEG_COLORS["teal"], lw=1.7)
        theta = np.linspace(-1.2, 1.2, 120)
        ax.plot(1.6 * np.cos(theta), -1.2 + 0.55 * np.sin(theta), color=ENEG_COLORS["red"], lw=2, label="elliptic: great circles meet")
        ax.scatter([0], [0.75], color=ENEG_COLORS["red"], zorder=4)
        ax.legend(loc="upper left", fontsize=8)
        ax.set_xlim(-2.7, 2.7)
        ax.set_ylim(-1.9, 1.8)
    elif kind == "euclid-construction":
        fig, ax = setup_figure(width=7.2, height=5.2, title="Postulates as construction permissions")
        a = np.array([-1.0, 0.0])
        b = np.array([1.0, 0.0])
        c = np.array([0.0, np.sqrt(3)])
        draw_segment(ax, a, b, label="given segment")
        draw_circle(ax, a, 2.0, color=ENEG_COLORS["teal"], label="circle centered at A")
        draw_circle(ax, b, 2.0, color=ENEG_COLORS["gold"], label="circle centered at B")
        draw_segment(ax, a, c, color=ENEG_COLORS["red"])
        draw_segment(ax, b, c, color=ENEG_COLORS["red"])
        draw_points(ax, {"A": a, "B": b, "C": c})
        ax.legend(fontsize=8)
        equal_limits(ax, [a, b, c, [-2.4, -0.4], [2.4, 2.2]])
    elif kind == "fano-plane":
        fig, ax = setup_figure(width=6.2, height=5.8, title="Finite incidence model: seven points, seven lines", equal=True, grid=False)
        angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 7, endpoint=False)
        pts = np.c_[np.cos(angles), np.sin(angles)]
        triples = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
        for triple in triples:
            arr = pts[list(triple)]
            ax.plot(arr[:, 0], arr[:, 1], lw=1.4, alpha=0.55)
        for index in range(7):
            ax.scatter(pts[index, 0], pts[index, 1], s=55, color=ENEG_COLORS["blue"])
            ax.text(pts[index, 0] * 1.12, pts[index, 1] * 1.12, f"P{index}", ha="center", va="center", fontsize=9)
        ax.axis("off")
    elif kind == "axiom-dependencies":
        fig, ax = setup_figure(width=7.4, height=5.1, title="Axiom families as proof modules", equal=False, grid=False)
        ax.axis("off")
        positions = {
            "incidence": (0, 1),
            "order": (1.3, 0.4),
            "congruence": (2.6, 1),
            "continuity": (3.9, 0.4),
            "parallelism": (5.2, 1),
            "theorems": (2.6, -0.75),
        }
        for name, (x, y) in positions.items():
            color = ENEG_COLORS["teal"] if name != "theorems" else ENEG_COLORS["gold"]
            ax.scatter([x], [y], s=950, color=color, alpha=0.22, edgecolors=ENEG_COLORS["ink"])
            ax.text(x, y, name.title(), ha="center", va="center", fontsize=9, weight="bold")
        for start in ["incidence", "order", "congruence", "continuity", "parallelism"]:
            ax.annotate("", xy=positions["theorems"], xytext=positions[start], arrowprops={"arrowstyle": "->", "lw": 1.5, "color": ENEG_COLORS["gray"]})
        ax.set_xlim(-0.6, 5.8)
        ax.set_ylim(-1.2, 1.5)
    elif kind == "saccheri":
        fig, ax = setup_figure(width=6.8, height=5.0, title="Saccheri quadrilateral as a neutral-geometry probe")
        a = np.array([-1.4, 0])
        b = np.array([1.4, 0])
        d = np.array([-1.0, 1.7])
        c = np.array([1.0, 1.7])
        draw_polygon(ax, [a, b, c, d], facecolor="#e0f2fe", label="summit case")
        draw_segment(ax, a, d, color=ENEG_COLORS["red"])
        draw_segment(ax, b, c, color=ENEG_COLORS["red"])
        draw_angle_arc(ax, d, a, c, label="summit")
        draw_angle_arc(ax, c, d, b, label="summit")
        draw_points(ax, {"A": a, "B": b, "C": c, "D": d})
        equal_limits(ax, [a, b, c, d])
    elif kind == "history-timeline":
        fig, ax = setup_figure(width=8.0, height=4.7, title="Attempts at the parallel postulate as assumption detectors", equal=False, grid=False)
        years = np.array([450, 1650, 1733, 1766, 1800])
        names = ["Proclus", "Wallis", "Saccheri", "Lambert", "Legendre"]
        y_values = np.array([0.2, 0.65, 0.35, 0.8, 0.5])
        ax.plot(years, np.zeros_like(years), color=ENEG_COLORS["gray"], lw=2)
        for year, name, y in zip(years, names, y_values, strict=False):
            ax.scatter([year], [0], s=45, color=ENEG_COLORS["blue"])
            ax.plot([year, year], [0, y], color=ENEG_COLORS["gray"], lw=1)
            ax.text(year, y + 0.04, name, ha="center", fontsize=9, weight="bold")
        ax.set_yticks([])
        ax.set_xlabel("approximate year")
    elif kind == "poincare-geodesics":
        fig, ax = setup_figure(width=6.5, height=6.0, title="Poincare disk geodesics and limiting parallels", equal=True, grid=False)
        draw_circle(ax, (0, 0), 1.0, color=ENEG_COLORS["ink"])
        pairs = [((-0.75, -0.25), (0.55, 0.55)), ((-0.55, 0.45), (0.75, -0.2)), ((0, -0.8), (0, 0.8))]
        for a_raw, b_raw in pairs:
            a = np.array(a_raw)
            b = np.array(b_raw)
            data = geodesic_circle_center(a, b)
            if data is None:
                ax.plot([a[0], b[0]], [a[1], b[1]], lw=2, color=ENEG_COLORS["blue"])
            else:
                center, radius = data
                theta = np.linspace(0, 2 * np.pi, 500)
                pts = center + radius * np.c_[np.cos(theta), np.sin(theta)]
                mask = np.sum(pts**2, axis=1) < 1.0001
                ax.plot(pts[mask, 0], pts[mask, 1], lw=2, color=ENEG_COLORS["teal"])
            ax.scatter([a[0], b[0]], [a[1], b[1]], color=ENEG_COLORS["red"], s=25)
        ax.axis("off")
    elif kind == "model-comparison":
        fig, ax = setup_figure(width=7.2, height=5.8, title="Klein chords and Poincare arcs view the same hyperbolic line", equal=True, grid=False)
        draw_circle(ax, (0, 0), 1.0, color=ENEG_COLORS["ink"])
        a = np.array([-0.72, -0.15])
        b = np.array([0.52, 0.62])
        ax.plot([a[0], b[0]], [a[1], b[1]], color=ENEG_COLORS["gold"], lw=3, label="Klein chord")
        data = geodesic_circle_center(klein_to_poincare(a), klein_to_poincare(b))
        if data:
            center, radius = data
            theta = np.linspace(0, 2 * np.pi, 500)
            pts = center + radius * np.c_[np.cos(theta), np.sin(theta)]
            mask = np.sum(pts**2, axis=1) < 1.0001
            ax.plot(pts[mask, 0], pts[mask, 1], color=ENEG_COLORS["teal"], lw=2.5, label="Poincare arc")
        ax.legend(fontsize=8)
        ax.axis("off")
    elif kind == "philosophy-map":
        fig, ax = setup_figure(width=7.2, height=5.0, title="Axioms, models, and measurement are different jobs", equal=False, grid=False)
        ax.axis("off")
        nodes = {"Axioms": (0, 1), "Theorems": (2, 1), "Models": (1, 0), "Measurements": (3, 0), "Physical claims": (4, 1)}
        for name, (x, y) in nodes.items():
            ax.scatter([x], [y], s=1100, color=ENEG_COLORS["blue"], alpha=0.16, edgecolors=ENEG_COLORS["ink"])
            ax.text(x, y, name, ha="center", va="center", fontsize=9, weight="bold")
        for start, target in [("Axioms", "Theorems"), ("Axioms", "Models"), ("Models", "Theorems"), ("Models", "Measurements"), ("Measurements", "Physical claims")]:
            ax.annotate("", xy=nodes[target], xytext=nodes[start], arrowprops={"arrowstyle": "->", "lw": 1.5, "color": ENEG_COLORS["gray"]})
        ax.set_xlim(-0.6, 4.6)
        ax.set_ylim(-0.45, 1.45)
    elif kind == "transformations":
        fig, ax = setup_figure(width=7.2, height=5.4, title="Transformations preserve selected invariants")
        tri = np.array([[0, 0], [1.2, 0.2], [0.3, 1.0]])
        transforms = [
            (tri, "original", ENEG_COLORS["ink"]),
            (tri + np.array([2.0, 0.4]), "translation", ENEG_COLORS["blue"]),
            (np.array([[p[0], -p[1]] for p in tri]) + np.array([0, -1.2]), "reflection", ENEG_COLORS["red"]),
            (np.array([rotate(p, 0.75, center=(0, 0)) for p in tri]) + np.array([2.0, -1.1]), "rotation", ENEG_COLORS["teal"]),
        ]
        for verts, label, color in transforms:
            draw_polygon(ax, verts, edgecolor=color, facecolor=color, alpha=0.13, label=label)
            ax.text(verts[:, 0].mean(), verts[:, 1].mean(), label, fontsize=8, ha="center")
        equal_limits(ax, np.vstack([item[0] for item in transforms]))
    elif kind == "pseudosphere":
        fig = plt.figure(figsize=(7.0, 5.6))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title("Pseudosphere patch as a local negative-curvature model", fontsize=11, weight="bold")
        u = np.linspace(0.25, 1.25, 50)
        v = np.linspace(0, 2 * np.pi, 80)
        u_grid, v_grid = np.meshgrid(u, v)
        x = np.sin(u_grid) * np.cos(v_grid)
        y = np.sin(u_grid) * np.sin(v_grid)
        z = np.cos(u_grid) + np.log(np.tan(u_grid / 2))
        ax.plot_surface(x, y, z, cmap="viridis", alpha=0.86, linewidth=0, rstride=1, cstride=1)
        ax.set_axis_off()
        ax.view_init(elev=23, azim=38)
    elif kind == "elliptic-sphere":
        fig = plt.figure(figsize=(7.0, 5.6))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title("Elliptic intuition from great circles on a sphere", fontsize=11, weight="bold")
        u = np.linspace(0, 2 * np.pi, 80)
        v = np.linspace(0, np.pi, 40)
        u_grid, v_grid = np.meshgrid(u, v)
        x = np.cos(u_grid) * np.sin(v_grid)
        y = np.sin(u_grid) * np.sin(v_grid)
        z = np.cos(v_grid)
        ax.plot_surface(x, y, z, color="#dbeafe", alpha=0.45, linewidth=0)
        t = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(t), np.sin(t), 0 * t, color=ENEG_COLORS["blue"], lw=2)
        ax.plot(np.cos(t) * 0.0, np.cos(t), np.sin(t), color=ENEG_COLORS["red"], lw=2)
        ax.scatter([0, 0], [0, 0], [1, -1], color=ENEG_COLORS["ink"], s=35)
        ax.set_axis_off()
        ax.view_init(elev=24, azim=42)
    elif kind == "finite-grid":
        fig, ax = setup_figure(width=6.7, height=5.6, title="Finite geometry keeps incidence but loses continuum intuition")
        pts = []
        for x in range(3):
            for y in range(3):
                pts.append((x, y))
                ax.scatter([x], [y], s=70, color=ENEG_COLORS["blue"])
                ax.text(x + 0.05, y + 0.05, f"{x},{y}", fontsize=8)
        for y in range(3):
            ax.plot([0, 2], [y, y], color=ENEG_COLORS["gray"], lw=1)
        for x in range(3):
            ax.plot([x, x], [0, 2], color=ENEG_COLORS["gray"], lw=1)
        ax.scatter([1.5], [1.0], s=100, facecolors="none", edgecolors=ENEG_COLORS["red"], lw=2, label="missing limit point")
        ax.legend(fontsize=8)
        equal_limits(ax, pts + [(1.5, 1.0)])
    else:
        fig, ax = setup_figure(width=7.2, height=5.0, title="Geometry scene")
        ax.plot([0, 1], [0, 1], color=ENEG_COLORS["blue"])
    save_matplotlib(fig, path)
    plt.close(fig)
    return path


def save_lab(kind: str, path):
    fig, ax = setup_figure(width=7.2, height=4.8, title="Applied lab check", equal=False, grid=True)
    if kind == "model-comparison":
        labels = ["Euclidean", "Hyperbolic", "Elliptic"]
        values = [1, 3, 0]
        ax.bar(labels, values, color=[ENEG_COLORS["blue"], ENEG_COLORS["teal"], ENEG_COLORS["red"]])
        ax.set_ylabel("parallels through an external point")
    elif kind == "diagram-perturbation":
        eps = np.linspace(-0.25, 0.25, 60)
        ax.plot(eps, np.abs(eps) * 4, color=ENEG_COLORS["red"], lw=2)
        ax.set_xlabel("diagram perturbation")
        ax.set_ylabel("proof risk score")
    elif kind == "truth-table":
        ax.imshow([[0, 1, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]], cmap="Blues")
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_title("Truth values as a finite model table")
    elif kind == "betweenness":
        x = np.linspace(0, 1, 100)
        ax.plot(x, x * (1 - x), color=ENEG_COLORS["teal"], lw=2)
        ax.set_xlabel("candidate between parameter")
        ax.set_ylabel("order witness")
    elif kind == "angle-sum":
        defect = np.linspace(0, 0.9, 80)
        ax.plot(defect, np.pi - defect, color=ENEG_COLORS["blue"], lw=2)
        ax.set_xlabel("hyperbolic area for K=-1")
        ax.set_ylabel("triangle angle sum")
    elif kind == "quadrilateral-regimes":
        ax.bar(["acute", "right", "obtuse"], [0.75, 1.0, 1.25], color=[ENEG_COLORS["teal"], ENEG_COLORS["gold"], ENEG_COLORS["red"]])
        ax.set_ylabel("summit-angle regime marker")
    elif kind == "hyperbolic-defect":
        sums = np.linspace(1.2, 3.0, 80)
        ax.plot(sums, np.pi - sums, color=ENEG_COLORS["teal"], lw=2)
        ax.set_xlabel("angle sum")
        ax.set_ylabel("area = pi - angle sum")
    elif kind == "cross-ratio":
        x = np.linspace(-0.8, 0.8, 90)
        ax.plot(x, np.log((1 + x) / (1 - x)), color=ENEG_COLORS["violet"], lw=2)
        ax.set_xlabel("Klein coordinate on a diameter")
        ax.set_ylabel("signed hyperbolic coordinate")
    elif kind == "measurement-noise":
        x = np.linspace(0, 1, 80)
        ax.fill_between(x, x - 0.08, x + 0.08, color=ENEG_COLORS["gold"], alpha=0.25)
        ax.plot(x, x, color=ENEG_COLORS["ink"], lw=2)
        ax.set_xlabel("formal prediction")
        ax.set_ylabel("physical measurement band")
    elif kind == "group-closure":
        table = np.array([[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]])
        ax.imshow(table, cmap="viridis")
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_title("Closure table for a four-motion toy group")
    elif kind == "parallel-angle":
        distance = np.linspace(0, 4, 100)
        ax.plot(distance, [angle_of_parallelism(float(value)) for value in distance], color=ENEG_COLORS["red"], lw=2)
        ax.set_xlabel("distance to line")
        ax.set_ylabel("angle of parallelism")
    elif kind == "metric-ellipses":
        t = np.linspace(0, 2 * np.pi, 200)
        for scale, color in [(1.0, ENEG_COLORS["blue"]), (0.65, ENEG_COLORS["teal"]), (0.35, ENEG_COLORS["red"])]:
            ax.plot(scale * np.cos(t), 0.55 * scale * np.sin(t), color=color, lw=2)
        ax.set_aspect("equal")
        ax.set_xlabel("local dx")
        ax.set_ylabel("local dy")
    elif kind == "missing-limits":
        n = np.arange(1, 9)
        ax.scatter(n, 1 / n, color=ENEG_COLORS["blue"])
        ax.axhline(0, color=ENEG_COLORS["red"], ls="--", label="limit not in finite sample")
        ax.set_xlabel("sequence index")
        ax.set_ylabel("candidate coordinate")
        ax.legend(fontsize=8)
    save_matplotlib(fig, path)
    plt.close(fig)
    return path


def chapter_sanity(kind: str) -> dict[str, object]:
    """Return chapter-specific numerical or structural checks."""

    if kind == "parallel-regimes":
        return {
            "sanity_kind": kind,
            "euclidean_parallel_count": 1,
            "hyperbolic_parallel_count_sample": 3,
            "elliptic_parallel_count": 0,
        }
    if kind == "euclid-construction":
        a = np.array([-1.0, 0.0])
        b = np.array([1.0, 0.0])
        c = np.array([0.0, math.sqrt(3)])
        lengths = [norm(b - a), norm(c - a), norm(c - b)]
        return {
            "sanity_kind": kind,
            "equilateral_side_lengths": [float(value) for value in lengths],
            "max_side_length_error": float(max(abs(value - 2.0) for value in lengths)),
        }
    if kind == "fano-plane":
        triples = [(0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 0), (5, 6, 1), (6, 0, 2)]
        point_counts = {point: 0 for point in range(7)}
        for triple in triples:
            for point in triple:
                point_counts[point] += 1
        return {
            "sanity_kind": kind,
            "point_count": 7,
            "line_count": len(triples),
            "incidences": sum(point_counts.values()),
            "incidences_per_point": sorted(point_counts.values()),
        }
    if kind == "axiom-dependencies":
        return {
            "sanity_kind": kind,
            "axiom_family_count": 5,
            "dependency_edges_to_theorems": 5,
            "parallelism_is_separate_family": True,
        }
    if kind == "saccheri":
        a = np.array([-1.4, 0.0])
        b = np.array([1.4, 0.0])
        d = np.array([-1.0, 1.7])
        c = np.array([1.0, 1.7])
        return {
            "sanity_kind": kind,
            "leg_length_difference": float(abs(norm(d - a) - norm(c - b))),
            "base_length": float(norm(b - a)),
            "summit_length": float(norm(c - d)),
        }
    if kind == "history-timeline":
        years = [450, 1650, 1733, 1766, 1800]
        return {
            "sanity_kind": kind,
            "timeline_is_ordered": years == sorted(years),
            "historical_node_count": len(years),
            "span_years": max(years) - min(years),
        }
    if kind == "poincare-geodesics":
        d1 = poincare_distance((0.0, 0.0), (0.25, 0.0))
        d2 = poincare_distance((0.0, 0.0), (0.5, 0.0))
        return {
            "sanity_kind": kind,
            "origin_to_half_is_farther_than_origin_to_quarter": d2 > d1,
            "sample_defect_area": float(defect_area(2.4)),
            "sample_disk_distance": float(d2),
        }
    if kind == "model-comparison":
        p = np.array([0.22, -0.18])
        roundtrip = klein_to_poincare(poincare_to_klein(p))
        return {
            "sanity_kind": kind,
            "klein_poincare_roundtrip_error": float(np.max(np.abs(roundtrip - p))),
            "diameter_distance_sample": float(poincare_distance((0.0, 0.0), (0.3, 0.0))),
        }
    if kind == "philosophy-map":
        return {
            "sanity_kind": kind,
            "foundation_node_count": 5,
            "formal_to_physical_requires_measurement": True,
            "measurement_band_width": 0.16,
        }
    if kind == "transformations":
        triangle = np.array([[0.0, 0.0], [1.2, 0.2], [0.3, 1.0]])
        reflected = np.array([reflect_point_across_line(point, Line.through((0.0, 0.0), (1.0, 0.0))) for point in triangle])
        original_area = oriented_area(triangle[0], triangle[1], triangle[2])
        reflected_area = oriented_area(reflected[0], reflected[1], reflected[2])
        return {
            "sanity_kind": kind,
            "reflection_preserves_area_magnitude": abs(abs(original_area) - abs(reflected_area)) < 1e-12,
            "reflection_reverses_orientation": original_area * reflected_area < 0,
            "right_angle_check": float(angle_between((1, 0), (0, 1))),
        }
    if kind == "pseudosphere":
        values = [angle_of_parallelism(distance) for distance in [0.0, 1.0, 2.0, 4.0]]
        return {
            "sanity_kind": kind,
            "angle_of_parallelism_values": [float(value) for value in values],
            "angle_of_parallelism_is_decreasing": all(a > b for a, b in zip(values, values[1:], strict=False)),
            "defect_area_for_angle_sum_2_7": float(defect_area(2.7)),
        }
    if kind == "elliptic-sphere":
        center, radius = circle_from_three_points((1, 0), (0, 1), (-1, 0))
        return {
            "sanity_kind": kind,
            "great_circle_sample_radius": float(radius),
            "great_circle_center_norm": float(norm(center)),
            "antipodal_identification_sample": [1.0, -1.0],
        }
    if kind == "finite-grid":
        finite_points = {(x, y) for x in range(3) for y in range(3)}
        return {
            "sanity_kind": kind,
            "finite_point_count": len(finite_points),
            "candidate_limit_point_present": (1.5, 1.0) in finite_points,
            "grid_line_count_visible": 6,
        }
    raise ValueError(f"unknown chapter sanity kind: {kind}")
