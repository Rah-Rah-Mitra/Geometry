"""Generated visual storyboards for the Euclid and Beyond notebooks."""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .artifacts import ARTIFACT_ROOT, save_json, save_matplotlib, save_plotly_html
from .euclidean import (
    angle,
    circle_circle_intersections,
    distance,
    line_circle_intersections,
    polygon_area,
    regular_polygon,
)
from .hyperbolic import disk_rotation, geodesic_arc_points, invert_in_circle, poincare_distance
from .plotting import (
    PALETTE,
    draw_arrow,
    draw_circle,
    draw_polygon,
    draw_segment,
    label_point,
    new_figure,
    set_equal_axes,
)
from .polyhedra import Mesh, euler_characteristic, named_meshes


def build_unit_visuals(unit: str, *, root: str | Path = ARTIFACT_ROOT) -> dict[str, Any]:
    """Build all durable visuals for a unit and return paths plus checks."""

    builders: dict[str, Callable[[Path], dict[str, Any]]] = {
        "introduction": _build_introduction,
        "chapter-01": _build_chapter_01,
        "chapter-02": _build_chapter_02,
        "chapter-03": _build_chapter_03,
        "chapter-04": _build_chapter_04,
        "chapter-05": _build_chapter_05,
        "chapter-06": _build_chapter_06,
        "chapter-07": _build_chapter_07,
        "chapter-08": _build_chapter_08,
        "appendix-brief-euclid": _build_appendix,
    }
    if unit not in builders:
        raise KeyError(f"Unknown Euclid and Beyond unit: {unit}")
    result = builders[unit](Path(root))
    paths = [Path(path) for path in result.get("paths", [])]
    checks = dict(result.get("checks", {}))
    checks.update({"unit": unit, "artifact_count": len(paths), "artifacts": [p.as_posix() for p in paths]})
    check_path = save_json(checks, unit, "checks", "visual-checks.json", root=root)
    return {"paths": paths, "checks": checks, "check_path": check_path}


def unit_lab_data(unit: str) -> list[dict[str, Any]]:
    """Return compact numeric examples used by notebooks as applied labs."""

    if unit == "introduction":
        return [
            {"stage": "classical construction", "inspectable_object": "compass-straightedge steps", "course_use": "existence proofs"},
            {"stage": "axiomatic repair", "inspectable_object": "model predicates", "course_use": "hidden assumption tests"},
            {"stage": "algebraic model", "inspectable_object": "field coordinates", "course_use": "constructibility and coordinates"},
            {"stage": "model change", "inspectable_object": "Poincare geodesics", "course_use": "parallel postulate independence"},
        ]
    if unit == "chapter-01":
        a, b = (0.0, 0.0), (1.0, 0.0)
        c = circle_circle_intersections(a, 1.0, b, 1.0)[0]
        return [
            {"measurement": "AB", "value": distance(a, b)},
            {"measurement": "AC", "value": distance(a, c)},
            {"measurement": "BC", "value": distance(b, c)},
            {"measurement": "angle ABC degrees", "value": math.degrees(angle(a, b, c))},
        ]
    if unit == "chapter-02":
        hits = line_circle_intersections((-1.3, -0.45), (1.3, 0.75), (0.0, 0.0), 1.0)
        return [{"intersection": index, "x": x, "y": y} for index, (x, y) in enumerate(hits, start=1)]
    if unit == "chapter-03":
        p = 5
        return [{"x": x, "y=(2x+1) mod 5": (2 * x + 1) % p} for x in range(p)]
    if unit == "chapter-04":
        rows = []
        for x, y in [(1.25, 0.8), (1.6, 0.65), (2.0, 1.1)]:
            rows.append({"x": x, "y": y, "similar_triangle_product": x * y})
        return rows
    if unit == "chapter-05":
        return [
            {"sides": n, "inscribed_unit_circle_area": 0.5 * n * math.sin(2 * math.pi / n), "pi_error": math.pi - 0.5 * n * math.sin(2 * math.pi / n)}
            for n in [6, 8, 12, 24, 48, 96]
        ]
    if unit == "chapter-06":
        rows = []
        for n in range(3, 21):
            phi = sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1)
            power_two = phi > 0 and phi & (phi - 1) == 0
            rows.append({"n": n, "phi(n)": phi, "power_of_two_phi": power_two})
        return rows
    if unit == "chapter-07":
        a, b = (-0.65, -0.2), (0.55, 0.35)
        return [
            {"sample": "base pair", "distance": poincare_distance(a, b)},
            {"sample": "rotated pair", "distance": poincare_distance(disk_rotation(a, math.pi / 6), disk_rotation(b, math.pi / 6))},
        ]
    if unit == "chapter-08":
        return [
            {"solid": name, "vertices": len(mesh.vertices), "faces": len(mesh.faces), "euler": euler_characteristic(mesh)}
            for name, mesh in named_meshes().items()
        ]
    if unit == "appendix-brief-euclid":
        return [
            {"theme": "Book I", "course_checkpoint": "incidence, triangle congruence, parallel reasoning"},
            {"theme": "Books III-IV", "course_checkpoint": "circle facts and regular polygon construction"},
            {"theme": "Books V-VI", "course_checkpoint": "proportion and similarity"},
            {"theme": "Books XI-XIII", "course_checkpoint": "solid geometry and regular polyhedra"},
        ]
    raise KeyError(unit)


def _finish(fig: Any, unit: str, filename: str, root: Path, *, kind: str = "figures") -> Path:
    path = save_matplotlib(fig, unit, kind, filename, root=root)
    plt.close(fig)
    return path


def _draw_dependency_graph(
    graph: nx.DiGraph | nx.Graph,
    positions: dict[str, tuple[float, float]],
    *,
    title: str,
    node_color: str = "#dbeafe",
) -> tuple[Any, Any]:
    fig, ax = plt.subplots(figsize=(9, 5.8))
    directed = isinstance(graph, nx.DiGraph)
    edge_kwargs: dict[str, Any] = {"arrows": directed}
    if directed:
        edge_kwargs.update({"arrowsize": 14, "connectionstyle": "arc3,rad=0.06"})
    nx.draw_networkx_edges(
        graph,
        positions,
        ax=ax,
        edge_color="#64748b",
        width=1.8,
        **edge_kwargs,
    )
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_size=1700,
        node_color=node_color,
        edgecolors=PALETTE["ink"],
        linewidths=1.2,
    )
    nx.draw_networkx_labels(graph, positions, ax=ax, font_size=9)
    ax.set_title(title, loc="left", fontsize=14, color=PALETTE["ink"])
    ax.axis("off")
    return fig, ax


def _build_introduction(root: Path) -> dict[str, Any]:
    graph = nx.DiGraph()
    nodes = [
        "Euclid\nas source",
        "Hidden\nassumptions",
        "Hilbert\naxioms",
        "Fields and\ncoordinates",
        "Constructible\nnumbers",
        "Hyperbolic\nmodels",
        "Polyhedra\nand symmetry",
    ]
    graph.add_edges_from(
        [
            (nodes[0], nodes[1]),
            (nodes[1], nodes[2]),
            (nodes[2], nodes[3]),
            (nodes[3], nodes[4]),
            (nodes[2], nodes[5]),
            (nodes[4], nodes[6]),
            (nodes[5], nodes[6]),
        ]
    )
    positions = {
        nodes[0]: (0.0, 0.0),
        nodes[1]: (1.5, 0.8),
        nodes[2]: (3.0, 0.0),
        nodes[3]: (4.6, 0.85),
        nodes[4]: (6.2, 0.85),
        nodes[5]: (4.7, -0.85),
        nodes[6]: (6.4, -0.05),
    }
    fig, _ = _draw_dependency_graph(graph, positions, title="Course roadmap: classical geometry as executable structure")
    path = _finish(fig, "introduction", "course-roadmap.png", root)
    return {
        "paths": [path],
        "checks": {"node_count": len(nodes), "edge_count": graph.number_of_edges(), "has_hyperbolic_branch": True},
    }


def _build_chapter_01(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    ax = axes[0]
    a, b = (0.0, 0.0), (1.0, 0.0)
    c = circle_circle_intersections(a, 1.0, b, 1.0)[0]
    draw_circle(ax, a, 1.0, label="center A", color=PALETTE["green"])
    draw_circle(ax, b, 1.0, label="center B", color=PALETTE["gold"])
    draw_segment(ax, a, b, label="given segment", color=PALETTE["ink"])
    draw_segment(ax, a, c, color=PALETTE["blue"])
    draw_segment(ax, b, c, color=PALETTE["blue"])
    for point, name in [(a, "A"), (b, "B"), (c, "C")]:
        label_point(ax, point, name)
    ax.set_title("Existence from two circle intersections", loc="left")
    set_equal_axes(ax)

    ax = axes[1]
    pentagon = regular_polygon(5, phase=math.pi / 2)
    draw_circle(ax, (0.0, 0.0), 1.0, label="circumcircle", color=PALETTE["gray"])
    draw_polygon(ax, pentagon, color=PALETTE["purple"], fill="#ede9fe", label="regular pentagon")
    for index, point in enumerate(pentagon, start=1):
        label_point(ax, point, f"P{index}", offset=(0.03, 0.03))
    ax.set_title("Regular pentagon as a construction target", loc="left")
    set_equal_axes(ax)
    fig.suptitle("Euclid's geometry: construction steps become checkable data", x=0.02, ha="left", fontsize=14)
    construction_path = _finish(fig, "chapter-01", "construction-certificates.png", root)

    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            ("Postulates", "Draw line"),
            ("Postulates", "Draw circle"),
            ("Common notions", "Compare lengths"),
            ("Draw circle", "Equilateral triangle"),
            ("Draw line", "Equilateral triangle"),
            ("Compare lengths", "Equilateral triangle"),
            ("Equilateral triangle", "Copy angle"),
            ("Copy angle", "Regular pentagon"),
            ("Circle facts", "Regular pentagon"),
        ]
    )
    positions = {
        "Postulates": (0, 1),
        "Common notions": (0, -1),
        "Draw line": (1.8, 1.4),
        "Draw circle": (1.8, 0.4),
        "Compare lengths": (1.8, -1.0),
        "Equilateral triangle": (3.8, 0.5),
        "Copy angle": (5.6, 0.5),
        "Circle facts": (3.8, -1.1),
        "Regular pentagon": (7.2, 0.0),
    }
    fig, _ = _draw_dependency_graph(graph, positions, title="Proof-state map: constructions depend on explicit permissions", node_color="#dcfce7")
    graph_path = _finish(fig, "chapter-01", "proof-state-dependency-map.png", root)

    sides = [distance(pentagon[i], pentagon[(i + 1) % 5]) for i in range(5)]
    return {
        "paths": [construction_path, graph_path],
        "checks": {
            "equilateral_side_spread": max(distance(a, b), distance(a, c), distance(b, c)) - min(distance(a, b), distance(a, c), distance(b, c)),
            "pentagon_side_spread": max(sides) - min(sides),
            "dependency_edges": graph.number_of_edges(),
        },
    }


def _build_chapter_02(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    ax = axes[0]
    points = {"A": (-1.0, -0.4), "B": (0.2, 0.3), "C": (1.4, 1.0), "D": (1.1, -0.8), "E": (-0.5, 1.0)}
    for name, point in points.items():
        label_point(ax, point, name)
    draw_segment(ax, points["A"], points["C"], label="line AC", color=PALETTE["blue"])
    draw_segment(ax, points["E"], points["D"], label="line ED", color=PALETTE["green"])
    draw_arrow(ax, points["A"], points["B"], label="between test", color=PALETTE["red"])
    ax.set_title("Incidence and betweenness as model predicates", loc="left")
    set_equal_axes(ax)

    ax = axes[1]
    center = (0.0, 0.0)
    radius = 1.0
    line_a, line_b = (-1.3, -0.45), (1.3, 0.75)
    hits = line_circle_intersections(line_a, line_b, center, radius)
    draw_circle(ax, center, radius, label="circle", color=PALETTE["gold"])
    draw_segment(ax, line_a, line_b, label="secant line", color=PALETTE["blue"])
    for index, hit in enumerate(hits, start=1):
        label_point(ax, hit, f"X{index}")
    ax.set_title("Line-circle intersection is an axiom-level demand", loc="left")
    set_equal_axes(ax)
    path = _finish(fig, "chapter-02", "hilbert-plane-model-checks.png", root)

    graph = nx.Graph()
    graph.add_edges_from(
        [
            ("Incidence", "Lines"),
            ("Incidence", "Points"),
            ("Betweenness", "Order"),
            ("Congruence", "Segments"),
            ("Congruence", "Angles"),
            ("Continuity", "Circle intersections"),
            ("Euclidean plane", "Parallel axiom"),
            ("Hilbert plane", "Incidence"),
            ("Hilbert plane", "Betweenness"),
            ("Hilbert plane", "Congruence"),
        ]
    )
    positions = nx.spring_layout(graph, seed=12)
    fig, _ = _draw_dependency_graph(graph, positions, title="Axiom groups as independent model tests", node_color="#e0f2fe")
    graph_path = _finish(fig, "chapter-02", "axiom-group-map.png", root)
    return {
        "paths": [path, graph_path],
        "checks": {"line_circle_intersections": len(hits), "axiom_nodes": graph.number_of_nodes()},
    }


def _build_chapter_03(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
    real_grid = np.linspace(-2, 2, 9)
    xx, yy = np.meshgrid(real_grid, real_grid)
    axes[0].scatter(xx.ravel(), yy.ravel(), s=16, color=PALETTE["blue"])
    axes[0].plot(real_grid, 0.6 * real_grid + 0.3, color=PALETTE["red"], linewidth=2)
    axes[0].set_title("Real Cartesian plane")
    set_equal_axes(axes[0])

    rational_grid = np.array([-2, -1, -0.5, 0, 0.5, 1, 2], dtype=float)
    xx, yy = np.meshgrid(rational_grid, rational_grid)
    axes[1].scatter(xx.ravel(), yy.ravel(), s=18, color=PALETTE["green"])
    axes[1].plot(rational_grid, rational_grid / 2, color=PALETTE["red"], linewidth=2)
    axes[1].set_title("Dense rational sample")
    set_equal_axes(axes[1])

    p = 5
    residues = np.arange(p)
    xx, yy = np.meshgrid(residues, residues)
    axes[2].scatter(xx.ravel(), yy.ravel(), s=24, color=PALETTE["purple"])
    finite_line = [(x, (2 * x + 1) % p) for x in residues]
    axes[2].plot([x for x, _ in finite_line], [y for _, y in finite_line], "o-", color=PALETTE["gold"], linewidth=2)
    axes[2].set_title("Finite field toy plane F5")
    axes[2].set_xlim(-0.5, p - 0.5)
    axes[2].set_ylim(-0.5, p - 0.5)
    axes[2].grid(True, color="#e2e8f0")
    fig.suptitle("Changing the field changes what geometry can mean", x=0.02, ha="left", fontsize=14)
    path = _finish(fig, "chapter-03", "field-plane-comparison.png", root)

    theta = math.radians(32)
    triangle = np.array([[0, 0], [2, 0], [0.6, 1.1]])
    rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
    moved = triangle @ rot.T + np.array([0.7, -0.2])
    fig, ax = new_figure(6, 5)
    draw_polygon(ax, triangle, color=PALETTE["blue"], fill="#dbeafe", label="triangle")
    draw_polygon(ax, moved, color=PALETTE["red"], fill="#fee2e2", label="rigid image")
    ax.set_title("Rigid motion preserves the SAS data", loc="left")
    set_equal_axes(ax)
    rigid_path = _finish(fig, "chapter-03", "rigid-motion-sas-check.png", root)

    original_sides = sorted(distance(triangle[i], triangle[(i + 1) % 3]) for i in range(3))
    moved_sides = sorted(distance(moved[i], moved[(i + 1) % 3]) for i in range(3))
    return {
        "paths": [path, rigid_path],
        "checks": {
            "finite_line_points": len(finite_line),
            "rigid_side_error": float(np.max(np.abs(np.asarray(original_sides) - np.asarray(moved_sides)))),
        },
    }


def _build_chapter_04(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.0))
    ax = axes[0]
    unit, x, y = 1.0, 1.6, 0.65
    origin = (0.0, 0.0)
    draw_segment(ax, origin, (unit, 0), label="1", color=PALETTE["ink"])
    draw_segment(ax, origin, (x, 0), label="x", color=PALETTE["blue"])
    draw_segment(ax, origin, (0, y), label="y", color=PALETTE["green"])
    draw_segment(ax, (unit, 0), (0, y), color=PALETTE["gray"], linestyle="--")
    product = x * y / unit
    draw_segment(ax, (x, 0), (0, product), color=PALETTE["red"], linestyle="--")
    draw_segment(ax, origin, (0, product), label="xy", color=PALETTE["red"])
    for point, name in [((unit, 0), "1"), ((x, 0), "x"), ((0, y), "y"), ((0, product), "xy")]:
        label_point(ax, point, name)
    ax.set_title("Similar triangles implement multiplication", loc="left")
    set_equal_axes(ax)

    ax = axes[1]
    coordinate_basis = np.array([[0, 0], [2.0, 0], [0, 1.3], [2.0, 1.3]])
    draw_polygon(ax, coordinate_basis, color=PALETTE["purple"], fill="#ede9fe", label="coordinate frame")
    draw_arrow(ax, (0, 0), (2.0, 0), label="chosen x unit", color=PALETTE["blue"])
    draw_arrow(ax, (0, 0), (0, 1.3), label="chosen y unit", color=PALETTE["green"])
    label_point(ax, (1.4, 0.9), "P=(a,b)")
    draw_segment(ax, (1.4, 0), (1.4, 0.9), color=PALETTE["gray"], linestyle="--")
    draw_segment(ax, (0, 0.9), (1.4, 0.9), color=PALETTE["gray"], linestyle="--")
    ax.set_title("Coordinates are recovered after arithmetic is built", loc="left")
    set_equal_axes(ax)
    path = _finish(fig, "chapter-04", "segment-arithmetic-machine.png", root)
    return {
        "paths": [path],
        "checks": {"unit": unit, "x": x, "y": y, "constructed_product": product, "expected_product": x * y},
    }


def _build_chapter_05(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.0))
    ax = axes[0]
    rectangle = np.array([[0, 0], [3, 0], [3, 1.6], [0, 1.6]])
    draw_polygon(ax, rectangle, color=PALETTE["ink"], fill="#fef3c7", label="same rectangle")
    draw_segment(ax, rectangle[0], rectangle[2], color=PALETTE["red"], label="dissection")
    ax.fill([0, 3, 3], [0, 0, 1.6], color="#bfdbfe", alpha=0.5)
    ax.fill([0, 3, 0], [0, 1.6, 1.6], color="#bbf7d0", alpha=0.5)
    ax.set_title("Area survives cutting and reassembly", loc="left")
    set_equal_axes(ax)

    ax = axes[1]
    ns = np.array([6, 8, 12, 24, 48, 96])
    areas = 0.5 * ns * np.sin(2 * math.pi / ns)
    ax.plot(ns, areas, "o-", color=PALETTE["purple"], label="inscribed polygon area")
    ax.axhline(math.pi, color=PALETTE["red"], linestyle="--", label="circle area")
    ax.set_xlabel("number of sides")
    ax.set_ylabel("area for unit circle")
    ax.set_title("Quadrature appears as approximation data", loc="left")
    ax.legend()
    ax.grid(True, color="#e2e8f0")
    path = _finish(fig, "chapter-05", "area-dissection-and-quadrature.png", root)
    return {
        "paths": [path],
        "checks": {
            "rectangle_area": polygon_area(rectangle),
            "triangle_area_sum": polygon_area([rectangle[0], rectangle[1], rectangle[2]]) + polygon_area([rectangle[0], rectangle[2], rectangle[3]]),
            "polygon_area_limit_error": float(abs(areas[-1] - math.pi)),
        },
    }


def _build_chapter_06(root: Path) -> dict[str, Any]:
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            ("Q", "quadratic\nextensions"),
            ("quadratic\nextensions", "constructible\nnumbers"),
            ("constructible\nnumbers", "regular\n17-gon"),
            ("cubic\nobstructions", "doubling\ncube"),
            ("angle\ntrisection", "marked\nruler"),
            ("marked\nruler", "cubic\nsolutions"),
            ("finite\nextensions", "degree\nbookkeeping"),
            ("degree\nbookkeeping", "constructible\nnumbers"),
        ]
    )
    positions = {
        "Q": (0, 0),
        "quadratic\nextensions": (1.8, 0.8),
        "constructible\nnumbers": (3.6, 0.8),
        "regular\n17-gon": (5.5, 0.8),
        "finite\nextensions": (1.8, -0.8),
        "degree\nbookkeeping": (3.6, -0.8),
        "cubic\nobstructions": (0.0, -1.9),
        "doubling\ncube": (1.9, -1.9),
        "angle\ntrisection": (3.8, -1.9),
        "marked\nruler": (5.5, -1.3),
        "cubic\nsolutions": (6.9, -1.3),
    }
    fig, _ = _draw_dependency_graph(graph, positions, title="Constructibility as field-degree bookkeeping", node_color="#fef9c3")
    tower_path = _finish(fig, "chapter-06", "field-extension-storyboard.png", root)

    fig, ax = new_figure(6, 6)
    polygon = regular_polygon(17, phase=math.pi / 2)
    draw_circle(ax, (0, 0), 1.0, color=PALETTE["gray"])
    draw_polygon(ax, polygon, color=PALETTE["purple"], fill="#ede9fe", label="17-gon")
    for i in [0, 1, 2, 4, 8, 16]:
        label_point(ax, polygon[i], str(i), offset=(0.02, 0.02))
    ax.set_title("Regular 17-gon: constructible but algebraically delicate", loc="left")
    set_equal_axes(ax)
    polygon_path = _finish(fig, "chapter-06", "regular-17-gon-roots.png", root)
    sides = [distance(polygon[i], polygon[(i + 1) % 17]) for i in range(17)]
    return {
        "paths": [tower_path, polygon_path],
        "checks": {"field_graph_edges": graph.number_of_edges(), "side_spread_17_gon": max(sides) - min(sides)},
    }


def _build_chapter_07(root: Path) -> dict[str, Any]:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
    ax = axes[0]
    boundary = plt.Circle((0, 0), 1, fill=False, edgecolor=PALETTE["ink"], linewidth=2)
    ax.add_patch(boundary)
    pairs = [((-0.65, -0.2), (0.55, 0.35)), ((-0.35, 0.55), (0.62, -0.35)), ((-0.78, 0.05), (0.78, 0.05))]
    for index, (a, b) in enumerate(pairs, start=1):
        arc = geodesic_arc_points(a, b)
        ax.plot(arc[:, 0], arc[:, 1], linewidth=2.2, label=f"geodesic {index}")
        label_point(ax, a, f"A{index}", offset=(0.02, 0.02))
        label_point(ax, b, f"B{index}", offset=(0.02, 0.02))
    ax.set_title("Poincare disk geodesics meet the boundary at right angles", loc="left")
    ax.legend(loc="lower left", fontsize=8)
    set_equal_axes(ax)

    ax = axes[1]
    circle_center = (0.25, 0.05)
    radius = 0.75
    sample = np.array([[0.65, 0.25], [0.48, -0.35], [-0.25, 0.45], [0.1, 0.7]])
    inverted = np.array([invert_in_circle(p, circle_center, radius) for p in sample])
    draw_circle(ax, circle_center, radius, label="inversion circle", color=PALETTE["gold"])
    for p, q in zip(sample, inverted):
        draw_segment(ax, p, q, color=PALETTE["gray"], linestyle="--")
        label_point(ax, p, "P", offset=(0.02, 0.02))
        label_point(ax, q, "P'", offset=(0.02, 0.02))
    ax.set_title("Circle inversion is an involution away from the center", loc="left")
    set_equal_axes(ax)
    path = _finish(fig, "chapter-07", "poincare-and-inversion-labs.png", root)

    plotly_fig = go.Figure()
    theta = np.linspace(0, 2 * math.pi, 240)
    plotly_fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines", name="ideal boundary"))
    for index, (a, b) in enumerate(pairs, start=1):
        arc = geodesic_arc_points(a, b)
        plotly_fig.add_trace(go.Scatter(x=arc[:, 0], y=arc[:, 1], mode="lines+markers", name=f"geodesic {index}"))
    plotly_fig.update_layout(
        title="Interactive Poincare geodesics",
        xaxis={"scaleanchor": "y", "range": [-1.08, 1.08]},
        yaxis={"range": [-1.08, 1.08]},
        template="plotly_white",
        height=560,
    )
    html_path = save_plotly_html(plotly_fig, "chapter-07", "interactive", "poincare-geodesics.html", root=root)
    a, b = pairs[0]
    rotated_a = disk_rotation(a, math.pi / 6)
    rotated_b = disk_rotation(b, math.pi / 6)
    p = np.array([0.46, -0.12])
    reinverted = invert_in_circle(invert_in_circle(p, circle_center, radius), circle_center, radius)
    return {
        "paths": [path, html_path],
        "checks": {
            "rotation_distance_error": abs(poincare_distance(a, b) - poincare_distance(rotated_a, rotated_b)),
            "inversion_involution_error": float(np.linalg.norm(p - reinverted)),
            "geodesic_count": len(pairs),
        },
    }


def _mesh_edges(mesh: Mesh) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for face in mesh.faces:
        for a, b in zip(face, face[1:] + face[:1]):
            result.add(tuple(sorted((a, b))))
    return result


def _triangulated_faces(mesh: Mesh) -> tuple[list[int], list[int], list[int]]:
    i: list[int] = []
    j: list[int] = []
    k: list[int] = []
    for face in mesh.faces:
        for offset in range(1, len(face) - 1):
            i.append(face[0])
            j.append(face[offset])
            k.append(face[offset + 1])
    return i, j, k


def _build_chapter_08(root: Path) -> dict[str, Any]:
    meshes = named_meshes()
    fig = plt.figure(figsize=(12, 8))
    for index, (name, mesh) in enumerate(meshes.items(), start=1):
        ax = fig.add_subplot(2, 2, index, projection="3d")
        verts = mesh.vertices
        polys = [[verts[i] for i in face] for face in mesh.faces]
        collection = Poly3DCollection(polys, alpha=0.45, facecolor="#bfdbfe", edgecolor=PALETTE["ink"], linewidth=0.8)
        ax.add_collection3d(collection)
        for a, b in _mesh_edges(mesh):
            segment = verts[[a, b]]
            ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], color=PALETTE["ink"], linewidth=1)
        ax.scatter(verts[:, 0], verts[:, 1], verts[:, 2], color=PALETTE["red"], s=18)
        ax.set_title(f"{name}: V-E+F={euler_characteristic(mesh)}")
        ax.set_axis_off()
        ax.set_box_aspect((1, 1, 1))
    fig.suptitle("Polyhedra as finite geometry: faces, edges, vertices, and Euler checks", x=0.02, ha="left", fontsize=14)
    path = _finish(fig, "chapter-08", "platonic-mesh-diagnostics.png", root)

    plotly_fig = go.Figure()
    colors = ["#93c5fd", "#86efac", "#fde68a", "#c4b5fd"]
    for offset, ((name, mesh), color) in enumerate(zip(meshes.items(), colors)):
        verts = mesh.vertices + np.array([3.0 * offset, 0, 0])
        i, j, k = _triangulated_faces(mesh)
        plotly_fig.add_trace(
            go.Mesh3d(
                x=verts[:, 0],
                y=verts[:, 1],
                z=verts[:, 2],
                i=i,
                j=j,
                k=k,
                name=name,
                opacity=0.55,
                color=color,
            )
        )
    plotly_fig.update_layout(
        title="Interactive Platonic solids with mesh diagnostics",
        scene={"aspectmode": "data"},
        template="plotly_white",
        height=620,
    )
    html_path = save_plotly_html(plotly_fig, "chapter-08", "interactive", "platonic-solids.html", root=root)
    return {
        "paths": [path, html_path],
        "checks": {
            "euler_values": {name: euler_characteristic(mesh) for name, mesh in meshes.items()},
            "mesh_count": len(meshes),
        },
    }


def _build_appendix(root: Path) -> dict[str, Any]:
    graph = nx.DiGraph()
    books = {
        "I\nFoundations": (0, 0),
        "II\nGeometric algebra": (1.6, 0.8),
        "III-IV\nCircles": (1.6, -0.8),
        "V-VI\nProportion": (3.4, 0.4),
        "XI\nSolids": (5.1, 0.4),
        "XII-XIII\nRegular solids": (6.9, 0.2),
    }
    graph.add_edges_from(
        [
            ("I\nFoundations", "II\nGeometric algebra"),
            ("I\nFoundations", "III-IV\nCircles"),
            ("II\nGeometric algebra", "V-VI\nProportion"),
            ("III-IV\nCircles", "V-VI\nProportion"),
            ("V-VI\nProportion", "XI\nSolids"),
            ("XI\nSolids", "XII-XIII\nRegular solids"),
        ]
    )
    fig, _ = _draw_dependency_graph(graph, books, title="Brief Euclid: book-level themes as a navigation graph", node_color="#fce7f3")
    roadmap_path = _finish(fig, "appendix-brief-euclid", "euclid-book-roadmap.png", root)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    a, b = (0, 0), (1, 0)
    c = circle_circle_intersections(a, 1, b, 1)[0]
    draw_circle(axes[0], a, 1, color=PALETTE["green"])
    draw_circle(axes[0], b, 1, color=PALETTE["gold"])
    draw_polygon(axes[0], [a, b, c], color=PALETTE["blue"], fill="#dbeafe", label="equilateral")
    axes[0].set_title("construct a triangle")
    set_equal_axes(axes[0])
    draw_circle(axes[1], (0, 0), 1, color=PALETTE["gray"])
    pentagon = regular_polygon(5, phase=math.pi / 2)
    draw_polygon(axes[1], pentagon, color=PALETTE["purple"], fill="#ede9fe", label="pentagon")
    axes[1].set_title("organize a polygon")
    set_equal_axes(axes[1])
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    draw_polygon(axes[2], square, color=PALETTE["ink"], fill="#fef3c7", label="unit square")
    draw_segment(axes[2], square[0], square[2], color=PALETTE["red"], label="diagonal")
    axes[2].set_title("compare areas")
    set_equal_axes(axes[2])
    fig.suptitle("Generated construction gallery: compact references, not copied figures", x=0.02, ha="left", fontsize=14)
    gallery_path = _finish(fig, "appendix-brief-euclid", "construction-gallery.png", root)
    return {
        "paths": [roadmap_path, gallery_path],
        "checks": {"euclid_book_nodes": len(books), "roadmap_edges": graph.number_of_edges()},
    }
