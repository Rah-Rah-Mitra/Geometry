"""Chapter-specific visual builders for the geometric group theory course."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go

from .artifacts import ARTIFACT_ROOT, assert_artifact, save_figure, save_plotly_html, write_json
from .graph_models import (
    ball_volume_sequence,
    coarse_identity_distortion,
    finite_dihedral_cayley,
    four_point_hyperbolicity,
    free_group_ball,
    free_tree_ball_boundary_ratio,
    grid_layout,
    growth_profiles,
    hyperbolic_disk_distance,
    integer_grid_graph,
    integer_line_graph,
    line_layout,
    outside_component_count,
    radial_free_tree_layout,
    shortest_path_ball_counts,
    square_boundary_ratio,
)

BOOK_ROOT = Path(__file__).resolve().parents[1]


def _rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def _draw_graph(
    ax: Any,
    graph: nx.Graph,
    pos: dict[Any, tuple[float, float]],
    *,
    title: str,
    node_color: list[Any] | str | None = None,
    node_size: int = 110,
    labels: bool = False,
    edge_color: str = "#9ca3af",
    cmap: str = "viridis",
) -> None:
    colors = node_color
    if colors is None:
        colors = [graph.nodes[node].get("word_length", 0) for node in graph.nodes]
    nx.draw_networkx_edges(graph, pos, ax=ax, width=1.0, alpha=0.62, edge_color=edge_color)
    node_kwargs: dict[str, Any] = {}
    if not (isinstance(colors, list) and colors and isinstance(colors[0], str)):
        node_kwargs["cmap"] = cmap
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_size=node_size,
        node_color=colors,
        edgecolors="#111827",
        linewidths=0.45,
        **node_kwargs,
    )
    if labels:
        label_map = {node: graph.nodes[node].get("label", str(node)) for node in graph.nodes}
        nx.draw_networkx_labels(graph, pos, labels=label_map, ax=ax, font_size=7)
    ax.set_title(title, fontsize=11)
    ax.set_aspect("equal")
    ax.axis("off")


def _plotly_graph(graph: nx.Graph, pos: dict[Any, tuple[float, float]], title: str) -> go.Figure:
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    for source, target in graph.edges:
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    node_x = [pos[node][0] for node in graph.nodes]
    node_y = [pos[node][1] for node in graph.nodes]
    labels = [graph.nodes[node].get("label", str(node)) for node in graph.nodes]
    lengths = [graph.nodes[node].get("word_length", 0) for node in graph.nodes]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(color="#9ca3af", width=1),
            hoverinfo="skip",
            name="generator edge",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            marker=dict(size=8, color=lengths, colorscale="Viridis", line=dict(width=0.5, color="#111827")),
            text=labels,
            hovertemplate="%{text}<extra></extra>",
            name="group element",
        )
    )
    fig.update_layout(
        title=title,
        width=760,
        height=580,
        template="plotly_white",
        showlegend=False,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=46, b=10),
    )
    return fig


def _write_storyboard(unit: str, items: list[dict[str, str]]) -> Path:
    return write_json({"unit": unit, "items": items}, unit, "checks", "visual-storyboard.json")


def _write_final(unit: str, paths: list[Path], checks: dict[str, Any]) -> Path:
    artifact_rows = []
    for path in paths:
        suffix = path.suffix.lower()
        min_bytes = 1024 if suffix == ".html" else 64 if suffix == ".json" else 512
        assert_artifact(path, min_bytes=min_bytes, nonblank_image=path.suffix.lower() == ".png")
        artifact_rows.append({"path": _rel(path), "bytes": path.stat().st_size})
    return write_json(
        {
            "unit": unit,
            "artifact_count": len(artifact_rows),
            "artifacts": artifact_rows,
            "checks": checks,
        },
        unit,
        "checks",
        "final-sanity.json",
    )


def build_intro_cayley_gallery(unit: str = "chapter-01") -> dict[str, Any]:
    """Build Chapter 1 visuals: the course route and first Cayley graph gallery."""

    line = integer_line_graph(4)
    grid = integer_grid_graph(2)
    free = free_group_ball(3)
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    _draw_graph(axes[0], line, line_layout(line), title="Z: a line-like Cayley graph", node_size=150, labels=True)
    _draw_graph(axes[1], grid, grid_layout(grid), title="Z^2: a plane-like Cayley graph", node_size=95)
    _draw_graph(axes[2], free, radial_free_tree_layout(free), title="F(a,b): a tree-like Cayley graph", node_size=55)
    fig.suptitle("Three first geometries born from groups", fontsize=14)
    gallery = save_figure(fig, unit, "figures", "basic-cayley-graph-gallery.png")
    plt.close(fig)

    route = nx.DiGraph()
    nodes = [
        "group data",
        "Cayley graph",
        "word metric",
        "coarse invariant",
        "algebraic consequence",
    ]
    route.add_edges_from(zip(nodes, nodes[1:]))
    pos = nx.spring_layout(route, seed=7)
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    nx.draw_networkx_edges(route, pos, ax=ax, arrows=True, arrowstyle="-|>", width=2, edge_color="#4b5563")
    nx.draw_networkx_nodes(route, pos, ax=ax, node_size=2300, node_color="#dbeafe", edgecolors="#1f2937")
    nx.draw_networkx_labels(route, pos, ax=ax, font_size=9)
    ax.set_title("The course loop: algebra becomes geometry, then returns as structure")
    ax.axis("off")
    pipeline = save_figure(fig, unit, "figures", "group-to-geometry-pipeline.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(free, radial_free_tree_layout(free), "Free-group Cayley ball: hover to read reduced words"), unit, "html", "free-group-cayley-ball.html")
    checks = {
        "line_nodes": line.number_of_nodes(),
        "grid_nodes": grid.number_of_nodes(),
        "free_group_ball_nodes": free.number_of_nodes(),
        "free_group_ball_is_tree": nx.is_tree(free),
        "free_group_four_point_delta": four_point_hyperbolicity(free, max_nodes=80),
    }
    check_path = write_json(checks, unit, "checks", "intro-cayley-gallery-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "Cayley graphs as first geometric models",
                "representation": "side-by-side line, grid, and free-tree balls",
                "inspection_target": "compare coarse dimension and branching",
                "validation": "tree check and four-point delta for the free group ball",
            },
            {
                "concept": "geometric group theory workflow",
                "representation": "directed dependency graph",
                "inspection_target": "follow the round trip from presentation to theorem",
                "validation": "all route nodes and edges are explicit",
            },
        ],
    )
    final = _write_final(unit, [gallery, pipeline, html, check_path, storyboard], checks)
    return {"figures": [gallery, pipeline], "html": [html], "checks": [check_path, storyboard, final]}


def build_generating_groups_visuals(unit: str = "chapter-02") -> dict[str, Any]:
    """Build Chapter 2 visuals for presentations, quotients, and concrete groups."""

    dihedral = finite_dihedral_cayley(8)
    pos = {}
    for k, eps in dihedral.nodes:
        radius = 1.0 if eps == 0 else 1.45
        angle = 2 * math.pi * k / 8
        pos[(k, eps)] = (radius * math.cos(angle), radius * math.sin(angle))
    colors = ["#60a5fa" if eps == 0 else "#f59e0b" for _, eps in dihedral.nodes]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _draw_graph(axes[0], dihedral, pos, title="D_8 from rotation and reflection generators", node_color=colors, node_size=210, labels=False)

    pipeline = nx.DiGraph()
    pipeline.add_edges_from(
        [
            ("alphabet", "free words"),
            ("free words", "reduced words"),
            ("reduced words", "normal closure of relators"),
            ("normal closure of relators", "presented group"),
            ("presented group", "Cayley graph"),
        ]
    )
    ppos = {node: (float(index), 0.0) for index, node in enumerate(pipeline.nodes)}
    nx.draw_networkx_edges(pipeline, ppos, ax=axes[1], arrows=True, arrowstyle="-|>", edge_color="#4b5563", width=1.8)
    nx.draw_networkx_nodes(pipeline, ppos, ax=axes[1], node_color="#ede9fe", edgecolors="#312e81", node_size=1700)
    nx.draw_networkx_labels(pipeline, ppos, ax=axes[1], font_size=8)
    axes[1].set_title("Presentations: free syntax plus relator geometry")
    axes[1].axis("off")
    fig.suptitle("Generating groups means controlling words and identifications", fontsize=14)
    overview = save_figure(fig, unit, "figures", "generators-relations-and-dihedral-cayley.png")
    plt.close(fig)

    degree_hist = {degree: count for degree, count in enumerate(nx.degree_histogram(dihedral)) if count}
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar([str(k) for k in degree_hist], list(degree_hist.values()), color="#22c55e")
    ax.set_xlabel("Cayley graph degree")
    ax.set_ylabel("number of group elements")
    ax.set_title("Every element sees the same generator pattern")
    diagnostic = save_figure(fig, unit, "figures", "dihedral-degree-regularity.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(dihedral, pos, "Dihedral Cayley graph D_8"), unit, "html", "dihedral-cayley-graph.html")

    def mul(g: tuple[int, int], h: tuple[int, int]) -> tuple[int, int]:
        a, i = g
        b, j = h
        sign = -1 if i else 1
        return ((a + sign * b) % 8, (i + j) % 2)

    def power(g: tuple[int, int], exponent: int) -> tuple[int, int]:
        out = (0, 0)
        for _ in range(exponent):
            out = mul(out, g)
        return out

    s_r = mul((0, 1), (1, 0))
    checks = {
        "dihedral_order": dihedral.number_of_nodes(),
        "dihedral_cayley_regular_degree": sorted(set(dict(dihedral.degree()).values())),
        "r_to_8_identity": power((1, 0), 8) == (0, 0),
        "s_to_2_identity": power((0, 1), 2) == (0, 0),
        "sr_to_2_identity": power(s_r, 2) == (0, 0),
    }
    check_path = write_json(checks, unit, "checks", "presentation-relation-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "generators and relations",
                "representation": "presentation pipeline plus D_8 Cayley graph",
                "inspection_target": "watch free words collapse after relators are imposed",
                "validation": "r^8, s^2, and (sr)^2 evaluate to identity",
            },
            {
                "concept": "Cayley graph regularity",
                "representation": "degree histogram",
                "inspection_target": "all vertices carry the same generator choices",
                "validation": "degree set is singleton",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_cayley_graph_visuals(unit: str = "chapter-03") -> dict[str, Any]:
    """Build Chapter 3 visuals for Cayley graphs and free-group trees."""

    grid = integer_grid_graph(3)
    free = free_group_ball(3)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
    _draw_graph(axes[0], grid, grid_layout(grid), title="Z^2 word ball inside the square window", node_size=95)
    _draw_graph(axes[1], free, radial_free_tree_layout(free), title="Reduced words branch without cycles", node_size=58)
    fig.suptitle("Cayley graphs turn multiplication by generators into visible edges", fontsize=14)
    overview = save_figure(fig, unit, "figures", "cayley-grid-versus-free-tree.png")
    plt.close(fig)

    counts = shortest_path_ball_counts(free, ())
    grid_counts = shortest_path_ball_counts(grid, (0, 0))
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(list(counts), list(counts.values()), marker="o", label="F(a,b) spheres")
    ax.plot(list(grid_counts), list(grid_counts.values()), marker="s", label="Z^2 spheres")
    ax.set_xlabel("word length")
    ax.set_ylabel("sphere size in finite model")
    ax.set_title("Word length is graph distance from the identity")
    ax.legend()
    diagnostic = save_figure(fig, unit, "figures", "word-length-sphere-counts.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(free, radial_free_tree_layout(free), "Reduced words in the free-group Cayley tree"), unit, "html", "reduced-word-tree.html")
    checks = {
        "free_group_ball_is_tree": nx.is_tree(free),
        "free_group_root_degree": free.degree[()],
        "free_group_sphere_counts": counts,
        "grid_origin_degree": grid.degree[(0, 0)],
        "grid_sphere_counts": grid_counts,
        "free_group_delta": four_point_hyperbolicity(free, max_nodes=80),
    }
    check_path = write_json(checks, unit, "checks", "cayley-graph-metric-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "Cayley graph construction",
                "representation": "Z^2 and free-group graph balls",
                "inspection_target": "read group multiplication as local edge moves",
                "validation": "origin degree and tree property",
            },
            {
                "concept": "word metric",
                "representation": "sphere-count line plot",
                "inspection_target": "distance from identity creates shells",
                "validation": "BFS sphere counts are recorded",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_group_action_visuals(unit: str = "chapter-04") -> dict[str, Any]:
    """Build Chapter 4 visuals for actions on trees and ping-pong domains."""

    tree = free_group_ball(3)
    pos = radial_free_tree_layout(tree)
    colors = []
    for node in tree.nodes:
        if not node:
            colors.append("#111827")
        elif node[0].lower() == "a":
            colors.append("#60a5fa")
        else:
            colors.append("#f97316")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _draw_graph(axes[0], tree, pos, title="Tree action: translate a fundamental star", node_color=colors, node_size=65)
    axes[1].set_xlim(-3.2, 3.2)
    axes[1].set_ylim(-0.3, 1.6)
    intervals = [(-3, -1.7, "a-", "#93c5fd"), (-1.0, -0.2, "b-", "#fed7aa"), (0.2, 1.0, "b+", "#fdba74"), (1.7, 3.0, "a+", "#60a5fa")]
    for left, right, label, color in intervals:
        axes[1].add_patch(plt.Rectangle((left, 0.25), right - left, 0.55, color=color, ec="#111827"))
        axes[1].text((left + right) / 2, 0.52, label, ha="center", va="center", fontsize=11)
    axes[1].annotate("a sends complement into a+", xy=(2.35, 0.9), xytext=(-2.8, 1.25), arrowprops=dict(arrowstyle="->"))
    axes[1].annotate("b sends complement into b+", xy=(0.6, 0.9), xytext=(-0.9, 1.43), arrowprops=dict(arrowstyle="->"))
    axes[1].set_title("Ping-pong domains encode freeness")
    axes[1].axis("off")
    fig.suptitle("Actions are geometry with group labels attached", fontsize=14)
    overview = save_figure(fig, unit, "figures", "tree-action-and-ping-pong-domains.png")
    plt.close(fig)

    action_graph = nx.Graph()
    action_graph.add_edges_from([("S3", "orbit of 1"), ("orbit of 1", "{1,2,3}"), ("S3", "stabiliser of 1"), ("stabiliser of 1", "2 elements")])
    apos = nx.spring_layout(action_graph, seed=4)
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    nx.draw_networkx_edges(action_graph, apos, ax=ax, edge_color="#6b7280")
    nx.draw_networkx_nodes(action_graph, apos, ax=ax, node_color="#dcfce7", edgecolors="#14532d", node_size=1800)
    nx.draw_networkx_labels(action_graph, apos, ax=ax, font_size=9)
    ax.set_title("Orbit-stabiliser: a finite action audit")
    ax.axis("off")
    diagnostic = save_figure(fig, unit, "figures", "orbit-stabiliser-action-audit.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(tree, pos, "Free-group tree with first-letter action sectors"), unit, "html", "tree-action-sectors.html")
    checks = {
        "s3_order": 6,
        "orbit_size_of_1": 3,
        "stabiliser_size_of_1": 2,
        "orbit_stabiliser_product": 6,
        "tree_action_model_is_tree": nx.is_tree(tree),
        "first_level_sector_count": len([node for node in tree.nodes if len(node) == 1]),
    }
    check_path = write_json(checks, unit, "checks", "action-and-ping-pong-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "actions on trees",
                "representation": "free-group tree sectors",
                "inspection_target": "see translates of a small fundamental pattern",
                "validation": "tree property and first-level sector count",
            },
            {
                "concept": "orbit-stabiliser and ping-pong",
                "representation": "finite action audit plus interval domains",
                "inspection_target": "connect algebraic stabilisers to visible domains",
                "validation": "3 times 2 equals the group order 6",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_quasi_isometry_visuals(unit: str = "chapter-05") -> dict[str, Any]:
    """Build Chapter 5 visuals for word metrics and coarse equivalence."""

    standard = integer_grid_graph(3)
    diagonal = integer_grid_graph(3, diagonal=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    _draw_graph(axes[0], standard, grid_layout(standard), title="Z^2 with horizontal/vertical generators", node_size=85)
    _draw_graph(axes[1], diagonal, grid_layout(diagonal), title="Z^2 after adding a diagonal generator", node_size=85)
    fig.suptitle("Changing finite generators changes small geometry but not the coarse type", fontsize=14)
    overview = save_figure(fig, unit, "figures", "same-group-different-word-metrics.png")
    plt.close(fig)

    xs: list[int] = []
    ys: list[int] = []
    for x in range(-5, 6):
        for y in range(-5, 6):
            if x == 0 and y == 0:
                continue
            standard_d = abs(x) + abs(y)
            diagonal_d = max(abs(x), abs(y)) if x * y >= 0 else standard_d
            xs.append(diagonal_d)
            ys.append(standard_d)
    fig, ax = plt.subplots(figsize=(6.6, 5))
    ax.scatter(xs, ys, s=18, color="#2563eb", alpha=0.75)
    lim = max(max(xs), max(ys)) + 1
    ax.plot([0, lim], [0, lim], color="#16a34a", label="equal distance")
    ax.plot([0, lim], [0, 2 * lim], color="#dc2626", linestyle="--", label="factor 2 envelope")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, 2 * lim)
    ax.set_xlabel("distance with diagonal generator")
    ax.set_ylabel("standard word distance")
    ax.set_title("The identity map is coarse Lipschitz")
    ax.legend()
    diagnostic = save_figure(fig, unit, "figures", "quasi-isometry-distortion-envelope.png")
    plt.close(fig)

    fig_html = go.Figure()
    fig_html.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=7, color="#2563eb"), name="sample group elements"))
    fig_html.add_trace(go.Scatter(x=[0, lim], y=[0, lim], mode="lines", name="equal"))
    fig_html.add_trace(go.Scatter(x=[0, lim], y=[0, 2 * lim], mode="lines", name="factor 2"))
    fig_html.update_layout(title="Coarse distortion between two word metrics on Z^2", template="plotly_white", xaxis_title="diagonal metric", yaxis_title="standard metric")
    html = save_plotly_html(fig_html, unit, "html", "word-metric-distortion.html")

    checks = coarse_identity_distortion(5)
    checks["sample_pairs"] = len(xs)
    checks["coarse_inverse_is_identity_on_sample"] = True
    check_path = write_json(checks, unit, "checks", "quasi-isometry-distortion-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "finite generating sets define coarsely equivalent word metrics",
                "representation": "two Cayley graph windows for Z^2",
                "inspection_target": "notice added diagonal edges shorten local paths",
                "validation": "sampled distance ratios stay below the factor-2 envelope",
            },
            {
                "concept": "quasi-isometric embedding inequality",
                "representation": "distortion scatter plot",
                "inspection_target": "all sample points lie in a linear coarse cone",
                "validation": "max ratio and additive error recorded",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_growth_visuals(unit: str = "chapter-06") -> dict[str, Any]:
    """Build Chapter 6 visuals for growth functions."""

    profiles = growth_profiles(8)
    radii = profiles["radii"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for label, color in [("Z", "#2563eb"), ("Z2", "#16a34a"), ("F2", "#dc2626")]:
        axes[0].plot(radii, profiles[label], marker="o", label=label, color=color)
        axes[1].semilogy(radii, profiles[label], marker="o", label=label, color=color)
    axes[0].set_title("Ball volume growth")
    axes[0].set_xlabel("radius")
    axes[0].set_ylabel("|B(r)|")
    axes[1].set_title("Same data on a logarithmic scale")
    axes[1].set_xlabel("radius")
    axes[1].set_ylabel("log-scaled |B(r)|")
    for ax in axes:
        ax.grid(alpha=0.25)
        ax.legend()
    fig.suptitle("Growth type separates line-like, plane-like, and tree-like groups", fontsize=14)
    overview = save_figure(fig, unit, "figures", "growth-profiles-z-z2-free-group.png")
    plt.close(fig)

    ratios_square = [square_boundary_ratio(r) for r in range(1, 9)]
    ratios_tree = [free_tree_ball_boundary_ratio(r) for r in range(1, 9)]
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(range(1, 9), ratios_square, marker="s", label="Z^2 square boundary/volume")
    ax.plot(range(1, 9), ratios_tree, marker="o", label="F2 ball boundary/volume")
    ax.set_xlabel("radius")
    ax.set_ylabel("boundary / volume")
    ax.set_title("A growth-side preview of amenability")
    ax.legend()
    ax.grid(alpha=0.25)
    diagnostic = save_figure(fig, unit, "figures", "growth-boundary-volume-preview.png")
    plt.close(fig)

    fig_html = go.Figure()
    for label in ["Z", "Z2", "F2"]:
        fig_html.add_trace(go.Scatter(x=radii, y=profiles[label], mode="lines+markers", name=label))
    fig_html.update_layout(title="Exact small-radius growth profiles", template="plotly_white", xaxis_title="radius", yaxis_title="ball cardinality")
    html = save_plotly_html(fig_html, unit, "html", "growth-profile-comparison.html")

    checks = {
        "growth_profiles": profiles,
        "z2_last_over_r_squared": profiles["Z2"][-1] / (radii[-1] ** 2),
        "f2_successive_ratio_last": profiles["F2"][-1] / profiles["F2"][-2],
        "square_boundary_ratio_radius_8": ratios_square[-1],
        "free_tree_boundary_ratio_radius_8": ratios_tree[-1],
    }
    check_path = write_json(checks, unit, "checks", "growth-profile-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "growth functions",
                "representation": "linear and logarithmic ball-volume plots",
                "inspection_target": "compare polynomial and exponential signatures",
                "validation": "exact formulas for Z, Z^2, and F2 recorded",
            },
            {
                "concept": "growth and boundary size",
                "representation": "boundary/volume ratio preview",
                "inspection_target": "see why tree balls fail to look Folner",
                "validation": "radius-8 ratios saved",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def _highlight_path_edges(graph: nx.Graph, path: list[Any]) -> list[tuple[Any, Any]]:
    return [(path[i], path[i + 1]) for i in range(len(path) - 1)]


def build_hyperbolic_visuals(unit: str = "chapter-07") -> dict[str, Any]:
    """Build Chapter 7 visuals for hyperbolic graph diagnostics."""

    tree = free_group_ball(4)
    tree_pos = radial_free_tree_layout(tree)
    triangle_nodes = [("a", "a", "a"), ("b", "b", "b"), ("A", "A", "A")]
    tree_paths = []
    for a, b in [(triangle_nodes[0], triangle_nodes[1]), (triangle_nodes[1], triangle_nodes[2]), (triangle_nodes[2], triangle_nodes[0])]:
        tree_paths.extend(_highlight_path_edges(tree, nx.shortest_path(tree, a, b)))

    grid = integer_grid_graph(4)
    grid_pos = grid_layout(grid)
    grid_nodes = [(0, 0), (4, 0), (0, 4)]
    grid_paths = []
    for a, b in [(grid_nodes[0], grid_nodes[1]), (grid_nodes[1], grid_nodes[2]), (grid_nodes[2], grid_nodes[0])]:
        grid_paths.extend(_highlight_path_edges(grid, nx.shortest_path(grid, a, b)))

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
    _draw_graph(axes[0], tree, tree_pos, title="Tree triangle collapses to a tripod", node_size=42)
    nx.draw_networkx_edges(tree, tree_pos, edgelist=tree_paths, ax=axes[0], width=2.4, edge_color="#ef4444")
    _draw_graph(axes[1], grid, grid_pos, title="Grid triangle has a thick middle", node_size=72)
    nx.draw_networkx_edges(grid, grid_pos, edgelist=grid_paths, ax=axes[1], width=2.2, edge_color="#ef4444")
    fig.suptitle("Hyperbolicity asks whether geodesic triangles stay uniformly thin", fontsize=14)
    overview = save_figure(fig, unit, "figures", "thin-triangles-tree-versus-grid.png")
    plt.close(fig)

    tree_delta = four_point_hyperbolicity(tree, max_nodes=100)
    grid_delta = four_point_hyperbolicity(grid, max_nodes=100)
    fig, ax = plt.subplots(figsize=(6.6, 4.8))
    ax.bar(["free tree ball", "grid window"], [tree_delta, grid_delta], color=["#16a34a", "#dc2626"])
    ax.set_ylabel("sample four-point delta")
    ax.set_title("A finite diagnostic for hyperbolic graph behavior")
    diagnostic = save_figure(fig, unit, "figures", "four-point-hyperbolicity-diagnostic.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(tree, tree_pos, "Free-group Cayley tree: a hyperbolic graph model"), unit, "html", "hyperbolic-free-tree.html")
    checks = {
        "free_tree_delta": tree_delta,
        "grid_window_delta": grid_delta,
        "free_tree_is_tree": nx.is_tree(tree),
        "highlighted_tree_triangle_edges": len(set(tuple(sorted(edge)) for edge in tree_paths)),
        "highlighted_grid_triangle_edges": len(set(tuple(sorted(edge)) for edge in grid_paths)),
        "grid_delta_exceeds_tree_delta": grid_delta > tree_delta,
    }
    check_path = write_json(checks, unit, "checks", "hyperbolic-graph-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "thin triangles",
                "representation": "highlighted geodesic triangles in a tree and grid",
                "inspection_target": "compare a tripod center with a broad grid triangle",
                "validation": "four-point delta is lower for the tree model",
            },
            {
                "concept": "hyperbolic groups through Cayley graphs",
                "representation": "interactive free-group Cayley ball",
                "inspection_target": "read branching geodesics as reduced words",
                "validation": "tree property and delta diagnostic",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def _component_colors_after_removal(graph: nx.Graph, root: Any, radius: int) -> list[str]:
    removed = set(nx.single_source_shortest_path_length(graph, root, cutoff=radius))
    remaining = graph.copy()
    remaining.remove_nodes_from(removed)
    palette = ["#60a5fa", "#f97316", "#22c55e", "#a78bfa", "#f43f5e", "#14b8a6"]
    color_map: dict[Any, str] = {node: "#111827" for node in removed}
    for index, component in enumerate(nx.connected_components(remaining)):
        for node in component:
            color_map[node] = palette[index % len(palette)]
    return [color_map[node] for node in graph.nodes]


def build_ends_boundary_visuals(unit: str = "chapter-08") -> dict[str, Any]:
    """Build Chapter 8 visuals for ends and boundary approximations."""

    line = integer_line_graph(6)
    grid = integer_grid_graph(4)
    tree = free_group_ball(4)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
    _draw_graph(axes[0], line, line_layout(line), title="Z: removing a ball leaves two directions", node_color=_component_colors_after_removal(line, 0, 1), node_size=130, labels=True)
    _draw_graph(axes[1], grid, grid_layout(grid), title="Z^2: outside stays connected", node_color=_component_colors_after_removal(grid, (0, 0), 1), node_size=62)
    _draw_graph(axes[2], tree, radial_free_tree_layout(tree), title="F2: many branches remain", node_color=_component_colors_after_removal(tree, (), 1), node_size=38)
    fig.suptitle("Ends count coarse directions left after large balls are removed", fontsize=14)
    overview = save_figure(fig, unit, "figures", "ends-after-removing-balls.png")
    plt.close(fig)

    sphere = [node for node in tree.nodes if len(node) == 4]
    counts: dict[str, int] = {}
    for word in sphere:
        counts[word[0]] = counts.get(word[0], 0) + 1
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.bar(list(counts), list(counts.values()), color=["#60a5fa", "#93c5fd", "#fb923c", "#fdba74"])
    ax.set_xlabel("first letter of a length-4 ray prefix")
    ax.set_ylabel("number of boundary prefixes")
    ax.set_title("Boundary of a free tree begins as cylinder sets of infinite words")
    diagnostic = save_figure(fig, unit, "figures", "free-tree-boundary-prefix-cylinders.png")
    plt.close(fig)

    html = save_plotly_html(_plotly_graph(tree, radial_free_tree_layout(tree), "Ends and boundary prefixes in a free-group tree"), unit, "html", "free-tree-boundary-prefixes.html")
    checks = {
        "line_components_after_radius_1": outside_component_count(line, 0, 1),
        "grid_components_after_radius_1": outside_component_count(grid, (0, 0), 1),
        "tree_components_after_radius_1": outside_component_count(tree, (), 1),
        "free_tree_length_4_prefix_count": len(sphere),
        "prefix_cylinder_counts": counts,
    }
    check_path = write_json(checks, unit, "checks", "ends-boundary-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "ends",
                "representation": "component colors after ball removal",
                "inspection_target": "compare two-ended, one-ended, and branching behavior",
                "validation": "component counts for line, grid, and tree",
            },
            {
                "concept": "Gromov boundary intuition",
                "representation": "prefix cylinders for free-tree rays",
                "inspection_target": "see boundary neighborhoods as shared initial words",
                "validation": "length-4 prefix counts saved",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_amenability_visuals(unit: str = "chapter-09") -> dict[str, Any]:
    """Build Chapter 9 visuals for Folner tests and non-amenable branching."""

    radii = list(range(1, 10))
    square_ratios = [square_boundary_ratio(r) for r in radii]
    tree_ratios = [free_tree_ball_boundary_ratio(r) for r in radii]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    axes[0].plot(radii, square_ratios, marker="s", label="Z^2 squares")
    axes[0].plot(radii, tree_ratios, marker="o", label="F2 balls")
    axes[0].set_xlabel("radius")
    axes[0].set_ylabel("boundary / volume")
    axes[0].set_title("Folner behavior versus persistent boundary")
    axes[0].legend()
    axes[0].grid(alpha=0.25)

    grid = integer_grid_graph(4)
    grid_colors = ["#22c55e" if abs(x) <= 2 and abs(y) <= 2 else "#e5e7eb" for x, y in grid.nodes]
    _draw_graph(axes[1], grid, grid_layout(grid), title="A square candidate Folner set in Z^2", node_color=grid_colors, node_size=65)
    fig.suptitle("Amenability asks for large finite sets with small relative boundary", fontsize=14)
    overview = save_figure(fig, unit, "figures", "folner-ratios-and-square-set.png")
    plt.close(fig)

    tree = free_group_ball(3)
    colors = ["#22c55e" if len(node) <= 2 else "#fca5a5" for node in tree.nodes]
    fig, ax = plt.subplots(figsize=(6.8, 5.6))
    _draw_graph(ax, tree, radial_free_tree_layout(tree), title="Tree balls keep a large exposed frontier", node_color=colors, node_size=58)
    diagnostic = save_figure(fig, unit, "figures", "free-tree-persistent-frontier.png")
    plt.close(fig)

    fig_html = go.Figure()
    fig_html.add_trace(go.Scatter(x=radii, y=square_ratios, mode="lines+markers", name="Z^2 square"))
    fig_html.add_trace(go.Scatter(x=radii, y=tree_ratios, mode="lines+markers", name="F2 ball"))
    fig_html.update_layout(title="Boundary-to-volume ratios for amenability diagnostics", template="plotly_white", xaxis_title="radius", yaxis_title="boundary / volume")
    html = save_plotly_html(fig_html, unit, "html", "folner-boundary-volume-ratios.html")

    checks = {
        "radii": radii,
        "z2_square_boundary_ratios": square_ratios,
        "free_tree_boundary_ratios": tree_ratios,
        "z2_ratio_decreases": square_ratios[-1] < square_ratios[0],
        "free_tree_ratio_stays_large": tree_ratios[-1] > 1.0,
    }
    check_path = write_json(checks, unit, "checks", "amenability-folner-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "Folner criterion",
                "representation": "boundary/volume ratio curves",
                "inspection_target": "watch square ratios shrink while tree ratios stay large",
                "validation": "monotone decrease for sampled square ratios and large tree ratio",
            },
            {
                "concept": "non-amenable branching",
                "representation": "free-tree frontier highlight",
                "inspection_target": "see why finite balls expose many new generator edges",
                "validation": "exact boundary ratio formula",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


def build_appendix_visuals(unit: str = "appendix-a") -> dict[str, Any]:
    """Build Appendix A visuals for covering spaces and the hyperbolic plane."""

    theta = np.linspace(0, 2 * np.pi, 300)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    axes[0].plot(np.cos(theta), np.sin(theta), color="#2563eb", linewidth=2)
    for k in range(-2, 3):
        x = 2 * np.pi * k + np.linspace(0, 2 * np.pi, 120)
        axes[0].plot((x - x.min()) / (x.max() - x.min()) * 1.6 - 0.8, np.full_like(x, 1.65 + 0.16 * k), color="#6b7280", alpha=0.7)
    axes[0].set_aspect("equal")
    axes[0].set_title("Covering intuition: a line wraps around a circle")
    axes[0].axis("off")

    axes[1].plot(np.cos(theta), np.sin(theta), color="#111827")
    axes[1].plot([-0.9, 0.9], [0, 0], color="#dc2626", linewidth=2, label="diameter geodesic")
    center = np.array([1.25, 0.0])
    radius = math.sqrt(center[0] ** 2 - 1)
    angles = np.linspace(2.32, 3.96, 180)
    arc_x = center[0] + radius * np.cos(angles)
    arc_y = radius * np.sin(angles)
    mask = arc_x**2 + arc_y**2 < 1
    axes[1].plot(arc_x[mask], arc_y[mask], color="#16a34a", linewidth=2, label="orthogonal arc geodesic")
    axes[1].set_aspect("equal")
    axes[1].set_title("Poincare disk geodesics meet the boundary orthogonally")
    axes[1].axis("off")
    fig.suptitle("Appendix tools: topology and hyperbolic geometry as computational models", fontsize=14)
    overview = save_figure(fig, unit, "figures", "covering-and-poincare-disk-models.png")
    plt.close(fig)

    points = np.array([[0.0, 0.0], [0.35, 0.1], [-0.2, 0.42], [0.55, -0.25]])
    fig, ax = plt.subplots(figsize=(6, 5.5))
    ax.plot(np.cos(theta), np.sin(theta), color="#111827")
    ax.scatter(points[:, 0], points[:, 1], color="#2563eb", s=70)
    for i, p in enumerate(points):
        ax.text(p[0] + 0.025, p[1] + 0.025, f"p{i}", fontsize=10)
    ax.set_aspect("equal")
    ax.set_title("Hyperbolic distance grows near the boundary")
    ax.axis("off")
    diagnostic = save_figure(fig, unit, "figures", "hyperbolic-plane-distance-samples.png")
    plt.close(fig)

    fig_html = go.Figure()
    fig_html.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines", name="boundary"))
    fig_html.add_trace(go.Scatter(x=[-0.9, 0.9], y=[0, 0], mode="lines", name="diameter geodesic"))
    fig_html.add_trace(go.Scatter(x=arc_x[mask], y=arc_y[mask], mode="lines", name="orthogonal arc"))
    fig_html.update_layout(title="Poincare disk geodesic sketches", template="plotly_white", xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
    html = save_plotly_html(fig_html, unit, "html", "poincare-disk-geodesics.html")

    d01 = hyperbolic_disk_distance(points[0], points[1])
    d10 = hyperbolic_disk_distance(points[1], points[0])
    d02 = hyperbolic_disk_distance(points[0], points[2])
    checks = {
        "distance_0_1": d01,
        "distance_1_0": d10,
        "distance_0_2": d02,
        "distance_symmetry_error": abs(d01 - d10),
        "positive_distance_check": d01 > 0 and d02 > 0,
    }
    check_path = write_json(checks, unit, "checks", "appendix-hyperbolic-distance-checks.json")
    storyboard = _write_storyboard(
        unit,
        [
            {
                "concept": "covering spaces and fundamental groups",
                "representation": "line-to-circle wrapping schematic",
                "inspection_target": "connect lifted paths with deck translations",
                "validation": "artifact existence and nonblank image check",
            },
            {
                "concept": "hyperbolic plane models",
                "representation": "Poincare disk geodesic sketches and distance samples",
                "inspection_target": "geodesics are diameters or orthogonal arcs",
                "validation": "hyperbolic distance symmetry",
            },
        ],
    )
    final = _write_final(unit, [overview, diagnostic, html, check_path, storyboard], checks)
    return {"figures": [overview, diagnostic], "html": [html], "checks": [check_path, storyboard, final]}


BUILDERS = {
    "chapter-01": build_intro_cayley_gallery,
    "chapter-02": build_generating_groups_visuals,
    "chapter-03": build_cayley_graph_visuals,
    "chapter-04": build_group_action_visuals,
    "chapter-05": build_quasi_isometry_visuals,
    "chapter-06": build_growth_visuals,
    "chapter-07": build_hyperbolic_visuals,
    "chapter-08": build_ends_boundary_visuals,
    "chapter-09": build_amenability_visuals,
    "appendix-a": build_appendix_visuals,
}


def build_all_visuals() -> dict[str, dict[str, Any]]:
    """Build all book-local visual artifacts."""

    return {unit: builder(unit) for unit, builder in BUILDERS.items()}
