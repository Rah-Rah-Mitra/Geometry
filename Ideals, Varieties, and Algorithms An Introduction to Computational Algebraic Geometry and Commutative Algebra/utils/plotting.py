"""Visualization helpers for IVA notebooks."""

from __future__ import annotations

import math
from collections.abc import Sequence

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go


def configure_matplotlib() -> None:
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.grid": True,
        "grid.alpha": 0.25,
        "font.size": 10,
    })


def concept_graph_figure(labels: Sequence[str], title: str):
    configure_matplotlib()
    graph = nx.DiGraph()
    root = title.split(":")[0]
    graph.add_node(root)
    for index, label in enumerate(labels):
        short = label.split(" with ")[0].split(" and ")[0][:34]
        graph.add_edge(root, short)
        if index:
            graph.add_edge(labels[index - 1].split(" with ")[0].split(" and ")[0][:34], short)
    pos = nx.spring_layout(graph, seed=len(labels) * 17 + len(title), k=1.1)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", width=1.2, alpha=0.55)
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_color=["#274c77" if node == root else "#8fb3cf" for node in graph.nodes],
        edgecolors="#17324d",
        node_size=[1350 if node == root else 1050 for node in graph.nodes],
    )
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color="#111111")
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    return fig


def monomial_lattice_figure(seed: int, title: str):
    configure_matplotlib()
    limit = 8 + seed % 4
    gens = [(2 + seed % 3, 1), (1, 2 + (seed + 1) % 3), (3 + seed % 2, 3)]
    points = []
    in_ideal = []
    for a in range(limit + 1):
        for b in range(limit + 1):
            points.append((a, b))
            in_ideal.append(any(a >= g0 and b >= g1 for g0, g1 in gens))
    xs, ys = zip(*points)
    colors = ["#b23a48" if flag else "#3a7ca5" for flag in in_ideal]
    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    ax.scatter(xs, ys, c=colors, s=48, edgecolor="white", linewidth=0.6)
    for g0, g1 in gens:
        ax.scatter([g0], [g1], marker="s", c="#111111", s=95)
        ax.annotate(f"x^{g0} y^{g1}", (g0, g1), textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.set_xlabel("x exponent")
    ax.set_ylabel("y exponent")
    ax.set_title(title)
    ax.set_aspect("equal", adjustable="box")
    summary = {"limit": limit, "generators": gens, "monomials_in_ideal": int(sum(in_ideal))}
    fig.tight_layout()
    return fig, summary


def polynomial_surface_figure(seed: int, title: str):
    grid = np.linspace(-2.0, 2.0, 55)
    x, y = np.meshgrid(grid, grid)
    z = np.sin((seed % 5 + 1) * x / 3.0) + np.cos((seed % 4 + 2) * y / 4.0) + 0.15 * x * y
    surface = go.Surface(x=x, y=y, z=z, colorscale="Viridis", showscale=False, opacity=0.9)
    curve_t = np.linspace(-2, 2, 90)
    curve = go.Scatter3d(
        x=curve_t,
        y=np.sin(curve_t * (seed % 3 + 1)),
        z=np.cos(curve_t) + 0.1 * seed,
        mode="lines",
        line={"color": "#e4572e", "width": 5},
        name="sample algebraic trace",
    )
    fig = go.Figure(data=[surface, curve])
    fig.update_layout(
        title=title,
        scene={"xaxis_title": "x", "yaxis_title": "y", "zaxis_title": "value"},
        margin={"l": 0, "r": 0, "t": 42, "b": 0},
        height=520,
    )
    return fig


def lab_curve_figure(seed: int, title: str):
    configure_matplotlib()
    t = np.linspace(-2.2, 2.2, 400)
    x = t
    y = (t**2 - 1) * (0.35 + 0.04 * seed) + 0.08 * np.sin((seed % 5 + 1) * t)
    dy = np.gradient(y, t)
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.plot(x, y, color="#22577a", label="sample variety slice")
    ax.plot(x, dy / max(1.0, np.max(np.abs(dy))), color="#c1121f", label="scaled derivative/check")
    ax.axhline(0, color="#222222", linewidth=0.8)
    ax.set_xlabel("parameter or chart coordinate")
    ax.set_ylabel("observable")
    ax.set_title(title)
    ax.legend(loc="best")
    summary = {
        "seed": seed,
        "critical_count": int(np.sum(np.diff(np.signbit(dy)) != 0)),
        "max_abs_y": float(np.max(np.abs(y))),
    }
    fig.tight_layout()
    return fig, summary
