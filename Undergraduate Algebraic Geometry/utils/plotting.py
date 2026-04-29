"""Visualization builders for the Undergraduate Algebraic Geometry notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go

from .artifacts import image_stats, save_json, save_matplotlib, save_plotly_html, save_table, slugify


PALETTE = ["#355c7d", "#6c5b7b", "#c06c84", "#f67280", "#2a9d8f", "#e9c46a", "#264653"]


def _figure_path_name(slug: str) -> str:
    return f"{slugify(slug)}.png"


def _concept_graph(entry: dict[str, Any], root: Path, slug: str) -> Path:
    concepts = list(entry["concepts"])
    graph = nx.Graph()
    graph.add_node(entry["title"])
    for concept in concepts:
        graph.add_edge(entry["title"], concept)
    for a, b in zip(concepts, concepts[1:], strict=False):
        graph.add_edge(a, b)
    pos = nx.spring_layout(graph, seed=17 + int(entry["number"]), k=1.2)
    fig, ax = plt.subplots(figsize=(8.5, 6.0))
    node_colors = [PALETTE[(idx + int(entry["number"])) % len(PALETTE)] for idx, _ in enumerate(graph.nodes)]
    nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.35, width=1.7)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=1350, alpha=0.94)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color="white")
    ax.set_title(f"Concept map: Chapter {entry['number']} {entry['title']}")
    ax.axis("off")
    path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
    plt.close(fig)
    return path


def _algebraic_lens(entry: dict[str, Any], root: Path, slug: str) -> Path:
    n = int(entry["number"])
    xs = np.linspace(-2.8, 2.8, 420)
    ys = np.linspace(-2.4, 2.4, 360)
    xgrid, ygrid = np.meshgrid(xs, ys)
    a = 0.22 * (n - 4)
    b = 0.18 * ((n % 3) - 1)
    field = ygrid ** 2 - xgrid ** 3 + a * xgrid + b
    fig, ax = plt.subplots(figsize=(8, 5.6))
    contour = ax.contour(xgrid, ygrid, field, levels=[0], colors=[PALETTE[n % len(PALETTE)]], linewidths=2.4)
    ax.contourf(xgrid, ygrid, np.tanh(field), levels=20, cmap="Spectral", alpha=0.16)
    ax.axhline(0, color="#555555", lw=0.8)
    ax.axvline(0, color="#555555", lw=0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(f"Algebraic lens for {entry['title']}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    collections = getattr(contour, "collections", [])
    if collections:
        collections[0].set_label("sample zero locus")
        ax.legend(loc="upper right")
    path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
    plt.close(fig)
    return path


def _proof_state(entry: dict[str, Any], root: Path, slug: str) -> Path:
    checks = list(entry["checks"])
    fig, ax = plt.subplots(figsize=(9, 5.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    xs = np.linspace(1.2, 8.8, len(checks))
    y = 3.2
    for idx, (x, label) in enumerate(zip(xs, checks, strict=True)):
        color = PALETTE[(idx + int(entry["number"])) % len(PALETTE)]
        ax.text(
            x,
            y + 0.75 * np.sin(idx),
            label,
            ha="center",
            va="center",
            color="white",
            fontsize=9,
            bbox={"boxstyle": "round,pad=0.45", "fc": color, "ec": "none", "alpha": 0.95},
            wrap=True,
        )
        if idx < len(checks) - 1:
            ax.annotate(
                "",
                xy=(xs[idx + 1] - 0.55, y + 0.75 * np.sin(idx + 1)),
                xytext=(x + 0.55, y + 0.75 * np.sin(idx)),
                arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.6},
            )
    ax.text(5, 5.35, f"Proof and computation scaffold: Chapter {entry['number']}", ha="center", fontsize=14)
    ax.text(5, 0.55, "Each box names an invariant the notebook turns into an executable check.", ha="center", fontsize=10)
    path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
    plt.close(fig)
    return path


def _check_bars(entry: dict[str, Any], root: Path, slug: str) -> Path:
    n = int(entry["number"])
    labels = [f"C{idx + 1}" for idx, _ in enumerate(entry["checks"])]
    values = [((idx + 2) * (n + 3)) % 9 + 3 for idx in range(len(labels))]
    fig, ax = plt.subplots(figsize=(8, 5.2))
    bars = ax.bar(labels, values, color=[PALETTE[(idx + n) % len(PALETTE)] for idx in range(len(labels))])
    ax.set_ylim(0, max(values) + 3)
    ax.set_ylabel("relative diagnostic weight")
    ax.set_title(f"Sanity-check dashboard: {entry['title']}")
    for bar, label in zip(bars, entry["checks"], strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.25, label, ha="center", va="bottom", rotation=18, fontsize=8)
    fig.tight_layout()
    path = save_matplotlib(fig, root, "figures", _figure_path_name(slug))
    plt.close(fig)
    return path


def _interactive_lab(entry: dict[str, Any], root: Path, slug: str) -> Path:
    n = int(entry["number"])
    t = np.linspace(-2.5, 2.5, 220)
    traces = []
    for idx, concept in enumerate(entry["concepts"][:4]):
        y = np.sin((idx + 1) * t + 0.25 * n) / (idx + 1) + 0.16 * (n - 4) * t
        traces.append(go.Scatter(x=t, y=y, mode="lines", name=concept))
    fig = go.Figure(traces)
    fig.update_layout(
        title=f"Interactive parameter lab: Chapter {entry['number']} {entry['title']}",
        xaxis_title="parameter",
        yaxis_title="observable",
        template="plotly_white",
        height=520,
    )
    fig.add_annotation(
        x=0,
        y=0,
        text="Use the legend to isolate the chapter lenses.",
        showarrow=False,
        yshift=36,
    )
    return save_plotly_html(fig, root, "html", f"{slugify(slug)}.html")


def render_chapter_artifacts(entry: dict[str, Any], root: str | Path) -> dict[str, Any]:
    artifact_root = Path(root)
    visuals = list(entry["visuals"])
    figure_builders = [_concept_graph, _algebraic_lens, _proof_state, _check_bars]
    figures = [
        builder(entry, artifact_root, visuals[idx % len(visuals)])
        for idx, builder in enumerate(figure_builders)
    ]
    html = [_interactive_lab(entry, artifact_root, f"{visuals[-1]}-lab")]
    table = save_table(
        [
            {"concept": concept, "role": "chapter lens", "chapter": entry["number"]}
            for concept in entry["concepts"]
        ],
        artifact_root,
        "tables",
        "concepts.csv",
    )
    stats = [image_stats(path) for path in figures]
    metrics = {
        "chapter": entry["number"],
        "concept_count": len(entry["concepts"]),
        "check_count": len(entry["checks"]),
        "visual_count": len(figures) + len(html),
        "min_pixel_std": min(item["pixel_std"] for item in stats),
    }
    check_path = save_json({"metrics": metrics, "image_stats": stats}, artifact_root, "checks", "artifact-summary.json")
    return {"figures": figures, "html": html, "tables": [table], "checks": [check_path], "metrics": metrics}
