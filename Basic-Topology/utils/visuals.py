"""Visualization builders for the Basic Topology notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sympy as sp
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon

from .artifacts import save_json, save_matplotlib, save_plotly_html
from .knots import trefoil_alexander_polynomial
from .plotting import PALETTE, draw_arrow, draw_polygon, draw_segment, new_figure, set_equal_axes
from .simplicial import barycentric_triangle, boundary_matrix, rank
from .topology import euler_characteristic, reduce_word, surface_chi, winding_number, word_reduction_trace

UNIT_TOPICS: dict[str, list[str]] = {
    "chapter-01": ["Euler characteristic", "equivalence", "surfaces", "classification", "invariants"],
    "chapter-02": ["open sets", "preimages", "continuity", "Peano stages", "extension"],
    "chapter-03": ["compactness", "finite subcovers", "products", "connectedness", "paths"],
    "chapter-04": ["quotients", "gluing", "Mobius strip", "groups", "orbits"],
    "chapter-05": ["homotopy", "loops", "pi_1", "winding", "fixed points"],
    "chapter-06": ["simplexes", "complexes", "subdivision", "edge loops", "orbit triangulations"],
    "chapter-07": ["classification", "orientability", "Euler characteristic", "surgery", "symbols"],
    "chapter-08": ["chains", "cycles", "boundaries", "homology", "invariance"],
    "chapter-09": ["degree", "Euler-Poincare", "Borsuk-Ulam", "Lefschetz", "dimension"],
    "chapter-10": ["knots", "presentations", "Seifert surfaces", "coverings", "Alexander polynomial"],
    "appendix-generators-and-relations": ["free words", "relations", "presentations", "free products", "matrices"],
}


def _close(fig: Any) -> None:
    plt.close(fig)


def _concept_map(unit: str, title: str) -> Path:
    topics = UNIT_TOPICS[unit]
    graph = nx.Graph()
    graph.add_node(title)
    for topic in topics:
        graph.add_edge(title, topic)
    for a, b in zip(topics, topics[1:]):
        graph.add_edge(a, b)
    fig, ax = new_figure(8.2, 5.2)
    pos = nx.spring_layout(graph, seed=sum(ord(c) for c in unit), k=1.0)
    colors = [PALETTE["gold"] if node == title else PALETTE["blue"] for node in graph.nodes]
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#94a3b8", width=1.6)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=colors, node_size=1700, edgecolors="white", linewidths=2)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=9, font_color="white")
    ax.set_title(f"{title}: dependency map", fontsize=13)
    ax.axis("off")
    path = save_matplotlib(fig, unit, "figures", "concept-dependency-map.png")
    _close(fig)
    return path


def _save_check(unit: str, data: dict[str, Any]) -> Path:
    data = {"unit": unit, **data}
    return save_json(data, unit, "checks", "sanity-checks.json")


def _chapter01(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Introduction")]
    polyhedra = pd.DataFrame(
        [
            {"space": "tetrahedron", "vertices": 4, "edges": 6, "faces": 4},
            {"space": "cube", "vertices": 8, "edges": 12, "faces": 6},
            {"space": "octahedron", "vertices": 6, "edges": 12, "faces": 8},
            {"space": "torus cell model", "vertices": 1, "edges": 2, "faces": 1},
        ]
    )
    polyhedra["chi"] = polyhedra.apply(lambda row: euler_characteristic(row.vertices, row.edges, row.faces), axis=1)
    fig, ax = new_figure(8.0, 4.8)
    x = np.arange(len(polyhedra))
    width = 0.2
    ax.bar(x - width, polyhedra.vertices, width, label="vertices", color=PALETTE["blue"])
    ax.bar(x, polyhedra.edges, width, label="edges", color=PALETTE["red"])
    ax.bar(x + width, polyhedra.faces, width, label="faces", color=PALETTE["green"])
    ax.plot(x, polyhedra.chi, color=PALETTE["ink"], marker="o", linewidth=2.5, label="chi")
    ax.set_xticks(x, polyhedra.space, rotation=18, ha="right")
    ax.set_title("Cell counts change; Euler characteristic is the invariant to inspect")
    ax.legend(ncols=4, fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "euler-characteristic-counts.png"))
    _close(fig)

    fig = plt.figure(figsize=(8, 4.8))
    ax = fig.add_subplot(111, projection="3d")
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, 2 * np.pi, 24)
    u, v = np.meshgrid(u, v)
    R, r = 1.5, 0.42
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_surface(x, y, z, color="#80b1d3", alpha=0.88, linewidth=0)
    ax.set_title("A torus is locally surface-like but globally different from a sphere")
    ax.set_axis_off()
    pngs.append(save_matplotlib(fig, unit, "figures", "torus-local-global-surface.png"))
    _close(fig)
    checks = [_save_check(unit, {"polyhedra": polyhedra.to_dict("records"), "sphere_chi_values": polyhedra.chi[:3].tolist(), "torus_chi": int(polyhedra.chi.iloc[3])})]
    return pngs, [], checks, {"stable_chi_for_convex_examples": int(polyhedra.chi[:3].nunique()) == 1}


def _chapter02(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Continuity")]
    fig, ax = new_figure(8, 4.5)
    xs = np.linspace(-3, 3, 600)
    ys = np.sin(xs) + 0.2 * xs
    band = (ys > -0.45) & (ys < 0.55)
    ax.plot(xs, ys, color=PALETTE["blue"], linewidth=2.2, label="f(x)")
    ax.fill_between(xs, -0.45, 0.55, color=PALETTE["gold"], alpha=0.16, label="target open band")
    ax.scatter(xs[band][::12], ys[band][::12], s=8, color=PALETTE["red"], label="preimage samples")
    ax.set_title("Continuity as inverse-image control")
    ax.legend(fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "preimage-continuity-test.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 6.0)
    t = np.linspace(0, 1, 256)
    x = np.mod(8 * t, 1)
    y = np.floor(8 * t) / 7
    ax.plot(x, y, color=PALETTE["purple"], linewidth=1.6)
    ax.scatter(x[::16], y[::16], s=18, color=PALETTE["ink"])
    ax.set_title("A stage approximation to a square-filling path")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "space-filling-curve-stage.png"))
    _close(fig)
    checks = [_save_check(unit, {"preimage_sample_count": int(band.sum()), "curve_samples": int(len(t)), "band_bounds": [-0.45, 0.55]})]
    return pngs, [], checks, {"preimage_is_nonempty": bool(band.any())}


def _chapter03(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Compactness and connectedness")]
    fig, ax = new_figure(8, 3.5)
    intervals = [(-0.05, 0.32), (0.2, 0.58), (0.47, 0.83), (0.72, 1.05)]
    ax.plot([0, 1], [0, 0], color=PALETTE["ink"], linewidth=5, solid_capstyle="round")
    for i, (a, b) in enumerate(intervals):
        ax.plot([a, b], [0.25 + i * 0.15] * 2, color=[PALETTE["blue"], PALETTE["green"], PALETTE["gold"], PALETTE["red"]][i], linewidth=9, solid_capstyle="round")
        ax.text((a + b) / 2, 0.35 + i * 0.15, f"U{i+1}", ha="center", fontsize=9)
    ax.set_xlim(-0.12, 1.12)
    ax.set_ylim(-0.2, 1.1)
    ax.axis("off")
    ax.set_title("A compact interval admits a finite visible subcover")
    pngs.append(save_matplotlib(fig, unit, "figures", "finite-subcover-interval.png"))
    _close(fig)

    fig, ax = new_figure(7, 4.6)
    xs = np.linspace(0.02, 1, 900)
    ax.plot(xs, np.sin(1 / xs), color=PALETTE["blue"], linewidth=1.2, label="oscillating graph")
    ax.plot([0, 0], [-1, 1], color=PALETTE["red"], linewidth=3, label="limit segment")
    ax.set_title("A connected closure where paths require extra care")
    ax.legend(fontsize=8)
    pngs.append(save_matplotlib(fig, unit, "figures", "connected-not-path-connected-model.png"))
    _close(fig)
    checks = [_save_check(unit, {"finite_subcover_size": len(intervals), "cover_left": min(a for a, _ in intervals), "cover_right": max(b for _, b in intervals), "oscillation_samples": int(len(xs))})]
    return pngs, [], checks, {"covers_unit_interval": min(a for a, _ in intervals) <= 0 and max(b for _, b in intervals) >= 1}


def _chapter04(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Identification spaces")]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.6))
    labels = [("cylinder", "a", "a"), ("Mobius strip", "a", "A"), ("torus", "a,b", "a,b")]
    for ax, (title, left, right) in zip(axes, labels):
        ax.add_patch(Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], closed=True, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
        draw_arrow(ax, (0, 0.18), (0, 0.82), color=PALETTE["blue"], label=left)
        if right == "A":
            draw_arrow(ax, (1, 0.82), (1, 0.18), color=PALETTE["red"], label=right)
        else:
            draw_arrow(ax, (1, 0.18), (1, 0.82), color=PALETTE["blue"], label=right)
        if title == "torus":
            draw_arrow(ax, (0.18, 0), (0.82, 0), color=PALETTE["green"], label="b")
            draw_arrow(ax, (0.18, 1), (0.82, 1), color=PALETTE["green"], label="b")
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "edge-identification-gallery.png"))
    _close(fig)

    theta = np.linspace(0, 2 * np.pi, 160)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines", name="orbit circle"))
    fig.add_trace(go.Scatter(x=np.cos(theta[::20]), y=np.sin(theta[::20]), mode="markers", name="sample representatives"))
    fig.update_layout(title="Orbit representatives for a rotation action", width=700, height=480)
    htmls = [save_plotly_html(fig, unit, "html", "rotation-orbit-representatives.html")]
    checks = [_save_check(unit, {"edge_models": [item[0] for item in labels], "html_artifacts": [path.name for path in htmls], "orbit_sample_count": int(len(theta[::20]))})]
    return pngs, htmls, checks, {"has_nonorientable_model": True}


def _chapter05(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "The fundamental group")]
    fig, ax = new_figure(6.5, 6.0)
    theta = np.linspace(0, 2 * np.pi, 400)
    for radius, color, label in [(1.2, PALETTE["blue"], "loop before"), (0.75, PALETTE["green"], "loop after")]:
        pts = np.column_stack([radius * np.cos(theta), radius * np.sin(theta)])
        ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=2.2, label=label)
    ax.scatter([0], [0], s=90, color=PALETTE["red"], label="puncture")
    ax.set_title("Homotopic loops around the same puncture preserve winding")
    ax.legend(fontsize=8)
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "loop-homotopy-winding.png"))
    _close(fig)

    fig, ax = new_figure(8, 4.0)
    radii = np.linspace(0.2, 1.1, 8)
    for r in radii:
        ax.add_patch(Circle((0, 0), r, fill=False, edgecolor=PALETTE["purple"], alpha=0.22 + 0.06 * r, linewidth=1.5))
    ax.scatter([0], [0], color=PALETTE["ink"], s=70)
    ax.set_title("Deformation retraction: annulus loops slide to a core circle")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "deformation-retraction-annulus.png"))
    _close(fig)
    sample = np.column_stack([np.cos(theta), np.sin(theta)])
    checks = [_save_check(unit, {"winding_number_unit_loop": winding_number(sample), "loop_samples": int(len(theta)), "radii_count": int(len(radii))})]
    return pngs, [], checks, {"unit_loop_winds_once": winding_number(sample) == 1}


def _chapter06(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Triangulations")]
    vertices, triangles = barycentric_triangle()
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    base = np.array([[0, 0], [1, 0], [0.35, 0.9]])
    axes[0].add_patch(Polygon(base, closed=True, fill=True, facecolor="#dbeafe", edgecolor=PALETTE["blue"], linewidth=2))
    axes[0].set_title("one 2-simplex")
    axes[0].set_aspect("equal")
    axes[0].axis("off")
    for tri in triangles:
        axes[1].add_patch(Polygon(vertices[list(tri)], closed=True, fill=True, facecolor="#dcfce7", edgecolor=PALETTE["green"], linewidth=1.5, alpha=0.75))
    axes[1].scatter(vertices[:, 0], vertices[:, 1], color=PALETTE["ink"], s=22)
    axes[1].set_title("barycentric subdivision")
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "barycentric-subdivision-triangle.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 4.8)
    graph_edges = [(0, 1), (1, 2), (2, 0), (1, 3), (3, 4), (4, 1)]
    graph = nx.Graph(graph_edges)
    pos = {0: (0, 0), 1: (1, 0), 2: (0.5, 0.8), 3: (1.8, 0), 4: (1.4, 0.75)}
    nx.draw_networkx(graph, pos, ax=ax, node_color="#fde68a", edge_color=PALETTE["ink"], node_size=550, font_size=9)
    ax.set_title("Edge loops are words in a triangulated graph")
    ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "edge-loop-complex.png"))
    _close(fig)
    chi_before = euler_characteristic(3, 3, 1)
    chi_after = euler_characteristic(len(vertices), 12, len(triangles))
    checks = [_save_check(unit, {"chi_before_subdivision": chi_before, "chi_after_subdivision": chi_after, "subdivision_triangles": len(triangles)})]
    return pngs, [], checks, {"subdivision_preserves_chi": chi_before == chi_after}


def _chapter07(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Surfaces")]
    surfaces = pd.DataFrame(
        [
            {"surface": "sphere", "kind": "sphere", "parameter": 0},
            {"surface": "torus", "kind": "orientable", "parameter": 1},
            {"surface": "double torus", "kind": "orientable", "parameter": 2},
            {"surface": "projective plane", "kind": "nonorientable", "parameter": 1},
            {"surface": "Klein bottle", "kind": "nonorientable", "parameter": 2},
        ]
    )
    surfaces["chi"] = surfaces.apply(lambda row: surface_chi(row.kind, row.parameter), axis=1)
    fig, ax = new_figure(8, 4.5)
    ax.bar(surfaces.surface, surfaces.chi, color=[PALETTE["green"], PALETTE["blue"], PALETTE["blue"], PALETTE["red"], PALETTE["red"]])
    ax.axhline(0, color=PALETTE["ink"], linewidth=1)
    ax.set_title("Euler characteristic separates many closed surfaces")
    ax.set_ylabel("chi")
    ax.tick_params(axis="x", rotation=18)
    pngs.append(save_matplotlib(fig, unit, "figures", "surface-classification-chi-table.png"))
    _close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8))
    for ax, word, title in [(axes[0], "a b A B", "torus word"), (axes[1], "a a b b", "Klein-style word")]:
        ax.add_patch(Polygon([[0, 0], [1, 0], [1, 1], [0, 1]], closed=True, fill=False, edgecolor=PALETTE["ink"], linewidth=2))
        ax.text(0.5, -0.08, word.split()[0], ha="center", color=PALETTE["blue"])
        ax.text(1.08, 0.5, word.split()[1], va="center", color=PALETTE["green"])
        ax.text(0.5, 1.06, word.split()[2], ha="center", color=PALETTE["blue"])
        ax.text(-0.08, 0.5, word.split()[3], va="center", color=PALETTE["green"])
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "surface-symbol-edge-words.png"))
    _close(fig)
    checks = [_save_check(unit, {"surfaces": surfaces.to_dict("records"), "torus_chi": int(surfaces.loc[surfaces.surface == "torus", "chi"].iloc[0])})]
    return pngs, [], checks, {"torus_chi_zero": int(surfaces.loc[surfaces.surface == "torus", "chi"].iloc[0]) == 0}


def _chapter08(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Simplicial homology")]
    vertices = [(0,), (1,), (2,)]
    edges = [(0, 1), (1, 2), (0, 2)]
    triangles = [(0, 1, 2)]
    d1 = boundary_matrix(edges, vertices)
    d2 = boundary_matrix(triangles, edges)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].imshow(d1, cmap="coolwarm", vmin=-1, vmax=1)
    axes[0].set_title("boundary d1: edges to vertices")
    axes[0].set_xlabel("edges")
    axes[0].set_ylabel("vertices")
    axes[1].imshow(d2, cmap="coolwarm", vmin=-1, vmax=1)
    axes[1].set_title("boundary d2: triangle to edges")
    axes[1].set_xlabel("triangle")
    axes[1].set_ylabel("edges")
    pngs.append(save_matplotlib(fig, unit, "figures", "boundary-matrices-simplex.png"))
    _close(fig)

    fig, ax = new_figure(6, 5)
    pts = np.array([[0, 0], [1, 0], [0.45, 0.82]])
    draw_polygon(ax, pts, color=PALETTE["blue"], fill="#dbeafe", label="2-chain")
    for i, label in enumerate(["v0", "v1", "v2"]):
        ax.text(pts[i, 0], pts[i, 1] + 0.06, label, ha="center")
    ax.set_title("The boundary of a filled triangle is a cycle")
    set_equal_axes(ax)
    pngs.append(save_matplotlib(fig, unit, "figures", "cycle-as-boundary-triangle.png"))
    _close(fig)
    composition = d1 @ d2
    checks = [_save_check(unit, {"d1": d1.tolist(), "d2": d2.tolist(), "d1_d2": composition.tolist(), "rank_d1": rank(d1), "rank_d2": rank(d2)})]
    return pngs, [], checks, {"boundary_squared_zero": bool(np.all(composition == 0))}


def _chapter09(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Degree and Lefschetz number")]
    theta = np.linspace(0, 2 * np.pi, 500)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    for ax, degree in zip(axes, [1, 2, -1]):
        ax.plot(np.cos(theta), np.sin(theta), color="#e5e7eb", linewidth=3)
        ax.plot(np.cos(degree * theta), np.sin(degree * theta), color=PALETTE["blue"], linewidth=1.5)
        ax.set_title(f"circle map degree {degree}")
        ax.set_aspect("equal")
        ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "circle-map-degrees.png"))
    _close(fig)

    fig, ax = new_figure(6.5, 4.5)
    x = np.linspace(-2, 2, 400)
    f = 0.55 * x**3 - x + 0.25
    ax.plot(x, f, color=PALETTE["blue"], label="f(x)")
    ax.plot(x, x, color=PALETTE["ink"], linestyle="--", label="identity")
    roots = np.roots([0.55, 0, -2, 0.25])
    real_roots = [root.real for root in roots if abs(root.imag) < 1e-8 and -2 <= root.real <= 2]
    ax.scatter(real_roots, real_roots, color=PALETTE["red"], zorder=4, label="fixed points")
    ax.legend(fontsize=8)
    ax.set_title("Fixed points appear where graph and identity meet")
    pngs.append(save_matplotlib(fig, unit, "figures", "lefschetz-fixed-point-sketch.png"))
    _close(fig)
    checks = [_save_check(unit, {"degrees": [1, 2, -1], "fixed_point_samples": [float(v) for v in real_roots], "fixed_point_count": len(real_roots)})]
    return pngs, [], checks, {"found_fixed_points": len(real_roots) >= 1}


def _chapter10(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Knots and covering spaces")]
    t = np.linspace(0, 2 * np.pi, 800)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    fig = plt.figure(figsize=(8, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot3D(x, y, z, color=PALETTE["blue"], linewidth=2)
    ax.set_title("Trefoil-style parametrized knot for spatial inspection")
    ax.set_axis_off()
    pngs.append(save_matplotlib(fig, unit, "figures", "trefoil-parametric-knot.png"))
    _close(fig)

    t_symbol = sp.symbols("t")
    matrix = sp.Matrix([[1 - t_symbol, -1], [t_symbol, 1 - t_symbol]])
    fig, ax = new_figure(5.8, 4.8)
    ax.imshow(np.array([[1, -1], [1, 1]], dtype=float), cmap="coolwarm", vmin=-1, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", fontsize=14, color=PALETTE["ink"])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Presentation matrix behind the trefoil Alexander polynomial")
    pngs.append(save_matplotlib(fig, unit, "figures", "trefoil-alexander-matrix.png"))
    _close(fig)
    polynomial = sp.expand(trefoil_alexander_polynomial())
    checks = [_save_check(unit, {"alexander_polynomial": str(polynomial), "trefoil_samples": int(len(t)), "matrix_determinant": str(matrix.det())})]
    return pngs, [], checks, {"trefoil_polynomial": str(polynomial)}


def _appendix(unit: str) -> tuple[list[Path], list[Path], list[Path], dict[str, Any]]:
    pngs = [_concept_map(unit, "Generators and relations")]
    word = list("abBAcCAb")
    trace = word_reduction_trace(word)
    fig, ax = new_figure(8, 4.8)
    lengths = [len(item) for item in trace]
    ax.step(range(len(lengths)), lengths, where="post", color=PALETTE["blue"], linewidth=2.5)
    ax.scatter(range(len(lengths)), lengths, color=PALETTE["red"], s=30)
    ax.set_title("Free-word reduction as cancellation over time")
    ax.set_xlabel("letters read")
    ax.set_ylabel("reduced length")
    pngs.append(save_matplotlib(fig, unit, "figures", "free-word-reduction-trace.png"))
    _close(fig)

    fig, ax = new_figure(7, 4.5)
    graph = nx.Graph()
    graph.add_edges_from([("free group", "generators"), ("free group", "reduced words"), ("presentation", "relations"), ("presentation", "quotient"), ("free product", "universal property")])
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx(graph, pos, ax=ax, node_color="#c7d2fe", edge_color=PALETTE["ink"], node_size=1500, font_size=9)
    ax.set_title("Algebra objects used by edge and knot groups")
    ax.axis("off")
    pngs.append(save_matplotlib(fig, unit, "figures", "presentation-algebra-map.png"))
    _close(fig)
    checks = [_save_check(unit, {"word": "".join(word), "reduced": "".join(reduce_word(word)), "trace_lengths": lengths})]
    return pngs, [], checks, {"reduced_word": "".join(reduce_word(word))}


BUILDERS = {
    "chapter-01": _chapter01,
    "chapter-02": _chapter02,
    "chapter-03": _chapter03,
    "chapter-04": _chapter04,
    "chapter-05": _chapter05,
    "chapter-06": _chapter06,
    "chapter-07": _chapter07,
    "chapter-08": _chapter08,
    "chapter-09": _chapter09,
    "chapter-10": _chapter10,
    "appendix-generators-and-relations": _appendix,
}


def build_unit_visuals(unit: str, *, force: bool = True) -> dict[str, list[Path]]:
    if unit not in BUILDERS:
        raise KeyError(f"unknown Basic Topology unit: {unit}")
    pngs, htmls, checks, _ = BUILDERS[unit](unit)
    return {"png": pngs, "html": htmls, "checks": checks}


def run_unit_lab(unit: str) -> dict[str, Any]:
    if unit == "chapter-01":
        return {"chi_tetrahedron": euler_characteristic(4, 6, 4), "chi_torus_cell_model": euler_characteristic(1, 2, 1)}
    if unit == "chapter-02":
        xs = np.linspace(-2, 2, 200)
        return {"samples": len(xs), "preimage_count": int(((xs**2 > 0.25) & (xs**2 < 1.5)).sum())}
    if unit == "chapter-03":
        intervals = [(-0.05, 0.32), (0.2, 0.58), (0.47, 0.83), (0.72, 1.05)]
        return {"finite_subcover_size": len(intervals), "covers_unit_interval": min(a for a, _ in intervals) <= 0 and max(b for _, b in intervals) >= 1}
    if unit == "chapter-04":
        return {"quotient_models": ["cylinder", "Mobius strip", "torus"], "nonorientable_example": "Mobius strip"}
    if unit == "chapter-05":
        theta = np.linspace(0, 2 * np.pi, 300)
        loop = np.column_stack([np.cos(theta), np.sin(theta)])
        return {"winding_number": winding_number(loop), "loop_samples": len(theta)}
    if unit == "chapter-06":
        return {"chi_before": euler_characteristic(3, 3, 1), "chi_after": euler_characteristic(7, 12, 6)}
    if unit == "chapter-07":
        return {"sphere_chi": surface_chi("sphere"), "genus_2_chi": surface_chi("orientable", 2), "klein_chi": surface_chi("nonorientable", 2)}
    if unit == "chapter-08":
        d1 = boundary_matrix([(0, 1), (1, 2), (0, 2)], [(0,), (1,), (2,)])
        d2 = boundary_matrix([(0, 1, 2)], [(0, 1), (1, 2), (0, 2)])
        return {"boundary_squared_zero": bool(np.all(d1 @ d2 == 0)), "rank_d1": rank(d1), "rank_d2": rank(d2)}
    if unit == "chapter-09":
        return {"circle_map_degrees": [1, 2, -1], "lefschetz_identity_on_circle": 0}
    if unit == "chapter-10":
        return {"trefoil_alexander_polynomial": str(trefoil_alexander_polynomial())}
    if unit == "appendix-generators-and-relations":
        word = list("abBAcCAb")
        return {"word": "".join(word), "reduced": "".join(reduce_word(word))}
    raise KeyError(unit)
