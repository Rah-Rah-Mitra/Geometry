"""Reproducible visual and invariant builders for the Hodge course."""

from __future__ import annotations

import csv
import hashlib
import html
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .artifacts import ensure_artifact_dirs, write_json
from .course_data import Chapter


PALETTE = {
    "ink": "#20242c",
    "muted": "#687384",
    "paper": "#f7f4ed",
    "blue": "#2f6f9f",
    "green": "#3b8f6f",
    "rose": "#b5525c",
    "gold": "#c08a2d",
    "violet": "#7257a4",
    "teal": "#2d8c90",
}


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def _axis_clean(ax: plt.Axes) -> None:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _short(text: str, max_len: int = 24) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "."


def _draw_hodge_diamond(ax: plt.Axes, chapter: Chapter, highlight_diagonal: bool = False) -> None:
    rows = chapter.hodge_numbers
    max_len = max(len(row) for row in rows)
    y_mid = (len(rows) - 1) / 2
    for r, row in enumerate(rows):
        y = y_mid - r
        start = -(len(row) - 1) / 2
        for c, value in enumerate(row):
            x = start + c
            color = PALETTE["blue"]
            if highlight_diagonal and c == len(row) // 2:
                color = PALETTE["gold"]
            ax.scatter([x], [y], s=1050, color=color, alpha=0.16, edgecolor=color, linewidth=1.8)
            ax.text(x, y + 0.05, str(value), ha="center", va="center", fontsize=13, color=PALETTE["ink"], weight="bold")
            p = c
            q = r - c
            if 0 <= p <= max_len and q >= 0:
                ax.text(x, y - 0.28, f"({p},{q})", ha="center", va="center", fontsize=7, color=PALETTE["muted"])
    ax.set_aspect("equal")
    ax.set_xlim(-max_len / 2 - 0.4, max_len / 2 + 0.4)
    ax.set_ylim(-y_mid - 0.7, y_mid + 0.8)
    _axis_clean(ax)


def render_concept_map(chapter: Chapter, paths: dict[str, Path]) -> Path:
    graph = nx.DiGraph()
    concepts = list(chapter.concepts[:7])
    for concept in concepts:
        graph.add_node(concept)
    for left, right in zip(concepts, concepts[1:]):
        graph.add_edge(left, right)
    if len(concepts) >= 4:
        graph.add_edge(concepts[0], concepts[3])
    if len(concepts) >= 6:
        graph.add_edge(concepts[2], concepts[5])

    fig, ax = plt.subplots(figsize=(9, 5.4))
    pos = nx.spring_layout(graph, seed=sum(ord(ch) for ch in chapter.id), k=1.2)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", edge_color="#aeb7c4", width=1.6)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#eef5f6", edgecolors=PALETTE["teal"], node_size=1850, linewidths=1.5)
    labels = {node: "\n".join(_short(part, 18) for part in node.split(" ")) for node in graph.nodes}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8, font_color=PALETTE["ink"], ax=ax)
    ax.set_title(f"{chapter.number}. {chapter.title}: concept route", loc="left", fontsize=14, weight="bold", color=PALETTE["ink"])
    ax.text(0.0, -0.08, chapter.visual_focus, transform=ax.transAxes, fontsize=9, color=PALETTE["muted"])
    _axis_clean(ax)
    return _save(fig, paths["figures"] / f"{chapter.id}-concept-route.png")


def render_primary_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    kind = chapter.visual_kind
    if kind in {"hodge-lefschetz", "hodge-diamond", "cycle-class"}:
        return _render_hodge_visual(chapter, paths)
    if kind in {"spectral-sequence"}:
        return _render_spectral_sequence(chapter, paths)
    if kind in {"kahler-identities", "laplacian-hodge"}:
        return _render_operator_visual(chapter, paths)
    if kind in {"period-map", "family-deformation"}:
        return _render_period_visual(chapter, paths)
    if kind in {"abel-jacobi"}:
        return _render_torus_visual(chapter, paths)
    if kind in {"monodromy", "lefschetz-pencil"}:
        return _render_monodromy_visual(chapter, paths)
    if kind in {"morse-lefschetz"}:
        return _render_morse_visual(chapter, paths)
    if kind in {"filtration", "chow-filtration"}:
        return _render_filtration_visual(chapter, paths)
    if kind in {"cycle-correspondence", "diagonal-decomposition", "connectivity", "resolution-ladder", "theme-triangle"}:
        return _render_correspondence_visual(chapter, paths)
    if kind in {"complex-atlas", "polydisc-cauchy"}:
        return _render_local_geometry_visual(chapter, paths)
    return _render_hodge_visual(chapter, paths)


def _render_hodge_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8), gridspec_kw={"width_ratios": [1, 1.1]})
    _draw_hodge_diamond(axes[0], chapter, highlight_diagonal=chapter.visual_kind == "cycle-class")
    axes[0].set_title("Hodge-number ledger", fontsize=12, weight="bold")
    ax = axes[1]
    _axis_clean(ax)
    levels = [0, 1, 2, 3, 4]
    betti = [sum(row) for row in chapter.hodge_numbers]
    for degree, value in zip(levels, betti):
        ax.barh(degree, value, color=PALETTE["green"], alpha=0.25, edgecolor=PALETTE["green"])
        ax.text(value + 0.2, degree, f"b{degree}={value}", va="center", fontsize=9, color=PALETTE["ink"])
    for degree in range(3):
        ax.annotate("", xy=(betti[degree + 2] * 0.8, degree + 2), xytext=(betti[degree] * 0.8, degree),
                    arrowprops={"arrowstyle": "->", "lw": 1.6, "color": PALETTE["gold"]})
    ax.set_ylim(-0.7, 4.7)
    ax.set_xlim(0, max(betti) + 4)
    ax.set_title("Lefschetz-style degree raising", loc="left", fontsize=12, weight="bold")
    ax.text(0, -0.45, "Inspect how type data and degree-raising operators constrain the same cohomology.", fontsize=9, color=PALETTE["muted"])
    fig.suptitle(f"{chapter.number}. {chapter.title}", x=0.02, y=1.02, ha="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-{chapter.visual_kind}.png")


def _render_spectral_sequence(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.9))
    for page, ax in zip(("E1/E2 page", "survivors after degeneration"), axes):
        ax.set_title(page, fontsize=12, weight="bold")
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xlabel("p")
        ax.set_ylabel("q")
        ax.grid(color="#e6e2d8", linewidth=0.8)
        for p in range(5):
            for q in range(5):
                rank = max(0, (p + 2 * q + len(chapter.id)) % 5 - 1)
                if page.startswith("survivors"):
                    rank = rank if (p + q) % 2 == 0 else 0
                if rank:
                    ax.scatter([p], [q], s=250 + 70 * rank, color=PALETTE["blue"], alpha=0.16, edgecolor=PALETTE["blue"])
                    ax.text(p, q, str(rank), ha="center", va="center", fontsize=10, weight="bold")
        if page.startswith("E1"):
            ax.annotate("", xy=(3, 2), xytext=(1, 3), arrowprops={"arrowstyle": "->", "lw": 2, "color": PALETTE["rose"]})
            ax.annotate("", xy=(4, 1), xytext=(2, 2), arrowprops={"arrowstyle": "->", "lw": 2, "color": PALETTE["rose"]})
        ax.set_aspect("equal")
    fig.suptitle(f"{chapter.number}. {chapter.title}: filtered-complex bookkeeping", x=0.02, ha="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-spectral-sequence.png")


def _render_operator_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    _axis_clean(ax)
    nodes = {
        "forms": (0, 1.8),
        "d": (1.8, 2.8),
        "partial": (1.8, 1.8),
        "dbar": (1.8, 0.8),
        "adjoints": (3.7, 1.8),
        "laplacian": (5.6, 1.8),
        "harmonic": (7.6, 1.8),
    }
    labels = {
        "forms": "forms",
        "d": "d",
        "partial": "partial",
        "dbar": "dbar",
        "adjoints": "formal\nadjoints",
        "laplacian": "Delta",
        "harmonic": "harmonic\nclasses",
    }
    colors = [PALETTE["blue"], PALETTE["teal"], PALETTE["green"], PALETTE["green"], PALETTE["gold"], PALETTE["rose"], PALETTE["violet"]]
    for (key, (x, y)), color in zip(nodes.items(), colors):
        ax.scatter([x], [y], s=1450, color=color, alpha=0.14, edgecolor=color, linewidth=1.7)
        ax.text(x, y, labels[key], ha="center", va="center", fontsize=10, weight="bold", color=PALETTE["ink"])
    arrows = [("forms", "d"), ("forms", "partial"), ("forms", "dbar"), ("d", "adjoints"), ("partial", "adjoints"), ("dbar", "adjoints"), ("adjoints", "laplacian"), ("laplacian", "harmonic")]
    for left, right in arrows:
        ax.annotate("", xy=nodes[right], xytext=nodes[left], arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#9aa6b4"})
    ax.text(2.85, 0.15, "Kahler compatibility compares the Laplacians; harmonic representatives then split by type.", fontsize=9.5, color=PALETTE["muted"])
    ax.set_xlim(-0.8, 8.5)
    ax.set_ylim(-0.2, 3.5)
    ax.set_title(f"{chapter.number}. {chapter.title}: operator identity board", loc="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-operator-identities.png")


def _render_period_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    _axis_clean(ax)
    theta = np.linspace(0, 2 * np.pi, 220)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["blue"], lw=2)
    base_points = np.array([[math.cos(t), math.sin(t)] for t in np.linspace(0.3, 2.4, 5)])
    ax.scatter(base_points[:, 0], base_points[:, 1], color=PALETTE["blue"], s=45)
    target_x = np.linspace(3.2, 7.2, 120)
    target_y = 0.35 * np.sin(1.8 * target_x)
    ax.plot(target_x, target_y, color=PALETTE["green"], lw=2.2)
    ax.scatter(target_x[::25], target_y[::25], color=PALETTE["green"], s=45)
    for point, idx in zip(base_points[::2], [10, 45, 85]):
        ax.annotate("", xy=(target_x[idx], target_y[idx]), xytext=point, arrowprops={"arrowstyle": "->", "lw": 1.4, "color": "#9aa6b4"})
    ax.annotate("", xy=(5.55, 0.35 * np.cos(1.8 * 5.4)), xytext=(5.0, 0.35 * np.sin(1.8 * 5.0)),
                arrowprops={"arrowstyle": "->", "lw": 2.2, "color": PALETTE["gold"]})
    ax.text(-1.25, -1.35, "base with locally constant topology", fontsize=9, color=PALETTE["muted"])
    ax.text(3.05, -1.35, "period-domain slice; gold arrow is horizontal direction", fontsize=9, color=PALETTE["muted"])
    ax.set_xlim(-1.6, 7.7)
    ax.set_ylim(-1.55, 1.45)
    ax.set_title(f"{chapter.number}. {chapter.title}: variation and period movement", loc="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-period-variation.png")


def _render_torus_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(7.2, 6.2))
    ax.set_aspect("equal")
    _axis_clean(ax)
    for x in np.linspace(0, 1, 6):
        ax.plot([x, x], [0, 1], color="#e3e0d7", lw=1)
        ax.plot([0, 1], [x, x], color="#e3e0d7", lw=1)
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, ec=PALETTE["ink"], lw=1.7))
    phase = (sum(ord(ch) for ch in chapter.id) % 17) / 17
    amplitude = 0.42 + 0.04 * (chapter.volume - 1)
    t = np.linspace(0, 1, 140)
    x = (0.12 + 0.78 * t + 0.05 * phase) % 1.0
    y = (0.18 + amplitude * np.sin(np.pi * (t + 0.2 * phase)) + 0.25 * t) % 1.0
    ax.plot(x, y, color=PALETTE["rose"], lw=2.4)
    ax.scatter([x[-1]], [y[-1]], s=110, color=PALETTE["rose"], label="Abel-Jacobi point")
    ax.arrow(0.08, 0.08, 0.34, 0.22, width=0.006, color=PALETTE["gold"], length_includes_head=True)
    ax.text(0.08, 1.08, f"{chapter.id}: intermediate Jacobian = vector space / (Hodge subspace + lattice)", fontsize=10, color=PALETTE["ink"])
    ax.text(0.05, -0.12, "Changing the bounding chain shifts by a lattice vector, so the torus point is unchanged.", fontsize=9, color=PALETTE["muted"])
    return _save(fig, paths["figures"] / f"{chapter.id}-abel-jacobi-torus.png")


def _render_monodromy_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.8))
    ax = axes[0]
    _axis_clean(ax)
    theta = np.linspace(0, 2 * np.pi, 240)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["blue"], lw=2)
    critical = np.array([[0.2, 0.15], [-0.45, 0.35], [0.35, -0.4]])
    ax.scatter(critical[:, 0], critical[:, 1], s=80, color=PALETTE["rose"])
    loop = 0.25 * np.array([np.cos(theta), np.sin(theta)]).T + critical[0]
    ax.plot(loop[:, 0], loop[:, 1], color=PALETTE["gold"], lw=2)
    ax.text(-1.15, -1.22, "Loops around critical values act on the fiber cohomology.", fontsize=9, color=PALETTE["muted"])
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.25)
    ax.set_title("base and critical values", fontsize=12, weight="bold")
    ax = axes[1]
    _axis_clean(ax)
    for r in [0.6, 1.0]:
        ax.plot(r * np.cos(theta), 0.55 * r * np.sin(theta), color="#cfd7dc", lw=1.5)
    ax.plot(0.65 * np.cos(theta), 0.12 * np.sin(theta), color=PALETTE["rose"], lw=3)
    ax.annotate("", xy=(1.1, 0.25), xytext=(-1.1, -0.25), arrowprops={"arrowstyle": "->", "lw": 2, "color": PALETTE["green"]})
    ax.text(-1.25, -0.95, "vanishing cycle transvection preserves the intersection form", fontsize=9, color=PALETTE["muted"])
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-1.15, 1.15)
    ax.set_title("fiber cycle action", fontsize=12, weight="bold")
    fig.suptitle(f"{chapter.number}. {chapter.title}: monodromy laboratory", x=0.02, ha="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-monodromy-action.png")


def _render_morse_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(8.8, 5.2))
    _axis_clean(ax)
    xs = np.linspace(-2.5, 2.5, 300)
    for level, shift in zip([-1.0, -0.25, 0.45, 1.1], [0.0, 0.15, -0.1, 0.05]):
        ys = 0.22 * xs**2 + level + shift * np.sin(2 * xs)
        ax.plot(xs, ys, color=PALETTE["blue"], lw=1.5)
    critical = [(-1.1, -0.15), (0.0, 0.45), (1.2, 1.15)]
    ax.scatter([p[0] for p in critical], [p[1] for p in critical], s=95, color=PALETTE["rose"])
    ax.axvline(0.85, color=PALETTE["gold"], lw=2, linestyle="--")
    ax.text(0.9, -1.35, "hyperplane section", rotation=90, fontsize=9, color=PALETTE["gold"])
    ax.text(-2.45, 1.75, "Crossing a critical level attaches a handle; index controls which degree changes.", fontsize=9, color=PALETTE["muted"])
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-1.5, 2.0)
    ax.set_title(f"{chapter.number}. {chapter.title}: Morse handles behind Lefschetz", loc="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-morse-hyperplane.png")


def _render_filtration_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(8.6, 5.4))
    _axis_clean(ax)
    labels = ["F0", "F1", "F2", "F3", "F4"]
    widths = [7.0, 5.8, 4.6, 3.4, 2.2]
    for i, (label, width) in enumerate(zip(labels, widths)):
        y = i * 0.72
        ax.add_patch(plt.Rectangle((0.4 + i * 0.35, y), width, 0.45, facecolor=PALETTE["blue"], alpha=0.12, edgecolor=PALETTE["blue"], lw=1.5))
        ax.text(0.12, y + 0.23, label, va="center", ha="left", fontsize=10, weight="bold", color=PALETTE["ink"])
    ax.annotate("", xy=(6.3, 0.1), xytext=(7.4, 3.1), arrowprops={"arrowstyle": "->", "lw": 2, "color": PALETTE["gold"]})
    ax.text(4.9, 3.8, "nested dimensions and graded pieces", fontsize=10, color=PALETTE["muted"])
    ax.set_xlim(0, 8.2)
    ax.set_ylim(-0.2, 4.2)
    ax.set_title(f"{chapter.number}. {chapter.title}: filtration ladder", loc="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-filtration-ladder.png")


def _render_correspondence_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    graph = nx.DiGraph()
    names = list(chapter.concepts[:5])
    for name in names:
        graph.add_node(name)
    for i in range(len(names)):
        graph.add_edge(names[i], names[(i + 1) % len(names)])
    if len(names) > 3:
        graph.add_edge(names[0], names[3])
    fig, ax = plt.subplots(figsize=(8.9, 5.2))
    pos = nx.circular_layout(graph)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, edge_color="#a8b0ba", width=1.6, arrowstyle="-|>")
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#f8efe8", edgecolors=PALETTE["rose"], node_size=1700, linewidths=1.5)
    nx.draw_networkx_labels(graph, pos, labels={n: _short(n, 20) for n in graph.nodes}, ax=ax, font_size=8)
    ax.set_title(f"{chapter.number}. {chapter.title}: correspondence and dependency view", loc="left", fontsize=14, weight="bold")
    ax.text(-1.15, -1.18, chapter.visual_focus, fontsize=9, color=PALETTE["muted"])
    _axis_clean(ax)
    return _save(fig, paths["figures"] / f"{chapter.id}-correspondence-view.png")


def _render_local_geometry_visual(chapter: Chapter, paths: dict[str, Path]) -> Path:
    fig, ax = plt.subplots(figsize=(8.8, 5.4))
    ax.set_aspect("equal")
    _axis_clean(ax)
    theta = np.linspace(0, 2 * np.pi, 180)
    centers = [(-0.45, 0), (0.45, 0.15)]
    colors = [PALETTE["blue"], PALETTE["green"]]
    for center, color in zip(centers, colors):
        cx, cy = center
        ax.plot(cx + 0.78 * np.cos(theta), cy + 0.5 * np.sin(theta), color=color, lw=2)
        ax.scatter([cx], [cy], color=color, s=45)
    ax.arrow(-1.1, -0.85, 0.6, 0.45, color=PALETTE["gold"], width=0.015, length_includes_head=True)
    ax.arrow(0.1, -0.72, 0.55, 0.52, color=PALETTE["rose"], width=0.015, length_includes_head=True)
    ax.text(-1.25, 0.88, "local charts, contours, and type-splitting are inspected before global Hodge theory begins", fontsize=9, color=PALETTE["muted"])
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.05, 1.05)
    ax.set_title(f"{chapter.number}. {chapter.title}: local analytic geometry", loc="left", fontsize=14, weight="bold")
    return _save(fig, paths["figures"] / f"{chapter.id}-local-geometry.png")


def write_interactive_stub(chapter: Chapter, paths: dict[str, Path]) -> Path:
    payload = {
        "chapter": chapter.id,
        "title": chapter.title,
        "inspection_target": chapter.visual_focus,
        "parameters": {
            "filtration_step": [0, 1, 2, 3],
            "monodromy_angle": [0, 90, 180, 270],
            "period_coordinate": [0.0, 0.33, 0.66, 1.0],
        },
    }
    body = html.escape(str(payload))
    path = paths["interactive"] / f"{chapter.id}-inspection-panel.html"
    path.write_text(
        "<!doctype html><meta charset='utf-8'><title>Inspection panel</title>"
        "<style>body{font-family:system-ui;margin:2rem;line-height:1.5;color:#20242c}"
        ".bar{height:18px;background:#2d8c90;margin:.5rem 0;width:65%}"
        ".bar:nth-child(2){width:45%;background:#c08a2d}.bar:nth-child(3){width:82%;background:#b5525c}"
        "code{white-space:pre-wrap}</style>"
        f"<h1>{html.escape(chapter.title)}</h1><p>{html.escape(chapter.visual_focus)}</p>"
        "<div class='bar'></div><div class='bar'></div><div class='bar'></div>"
        f"<h2>Structured payload</h2><code>{body}</code>",
        encoding="utf-8",
    )
    return path


def chapter_numeric_checks(chapter: Chapter) -> dict[str, Any]:
    rows = [list(row) for row in chapter.hodge_numbers]
    betti = [sum(row) for row in rows]
    symmetry = all(row == list(reversed(row)) for row in rows)

    d0 = np.array([[1, 0], [0, 1], [1, -1]], dtype=float)
    d1 = np.array([[1, -1, -1]], dtype=float)
    boundary_residual = float(np.linalg.norm(d1 @ d0))
    laplacian = d0 @ d0.T + d1.T @ d1
    eigvals = np.linalg.eigvalsh(laplacian)

    j = np.array([[0, 1], [-1, 0]], dtype=int)
    transvection = np.array([[1, 1], [0, 1]], dtype=int)
    symplectic_residual = int(np.max(np.abs(transvection.T @ j @ transvection - j)))

    filtration = np.array([10, 7, 4, 2, 0])
    filtration_nested = bool(np.all(np.diff(filtration) <= 0))

    fourier = np.array([[1, 1], [1, -1]], dtype=float) / math.sqrt(2)
    fourier_unitary_residual = float(np.linalg.norm(fourier.T @ fourier - np.eye(2)))

    checks = {
        "chapter_id": chapter.id,
        "hodge_symmetry": bool(symmetry),
        "toy_betti_numbers": betti,
        "odd_betti_even_for_toy_kahler": all(betti[i] % 2 == 0 for i in range(1, len(betti), 2)),
        "boundary_squared_norm": boundary_residual,
        "laplacian_min_eigenvalue": float(eigvals.min()),
        "symplectic_monodromy_residual": symplectic_residual,
        "filtration_nested": filtration_nested,
        "fourier_unitary_residual": fourier_unitary_residual,
    }
    return checks


def write_chapter_tables(chapter: Chapter, paths: dict[str, Path]) -> Path:
    path = paths["tables"] / f"{chapter.id}-hodge-ledger.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["degree", "hodge_row", "betti"])
        for degree, row in enumerate(chapter.hodge_numbers):
            writer.writerow([degree, " ".join(map(str, row)), sum(row)])
    return path


def ensure_chapter_artifacts(chapter: Chapter, course_root: Path | None = None) -> dict[str, str]:
    paths = ensure_artifact_dirs(chapter, course_root)
    artifacts = {
        "concept_map": render_concept_map(chapter, paths),
        "primary_visual": render_primary_visual(chapter, paths),
        "interactive": write_interactive_stub(chapter, paths),
        "hodge_ledger": write_chapter_tables(chapter, paths),
    }
    source_payload = {
        "chapter_id": chapter.id,
        "title": chapter.title,
        "volume": chapter.volume,
        "pdf_file": chapter.pdf_file,
        "printed_pages": [chapter.printed_start, chapter.printed_end],
        "pdf_pages": [chapter.pdf_start, chapter.pdf_end],
        "sections": list(chapter.sections),
        "copyright_note": "Original notebook prose and generated visuals only; no copied textbook text, screenshots, crops, or figures.",
    }
    storyboard_payload = {
        "chapter_goal": chapter.goal,
        "visual_focus": chapter.visual_focus,
        "concept_inventory": list(chapter.concepts),
        "proof_moves": list(chapter.proof_moves),
        "pitfalls": list(chapter.pitfalls),
        "library_routes": list(chapter.library_routes),
        "checks": list(chapter.checks),
        "lab": chapter.lab,
    }
    checks = chapter_numeric_checks(chapter)
    artifacts["source_span"] = write_json(paths["checks"] / "source-span.json", source_payload)
    artifacts["visual_storyboard"] = write_json(paths["checks"] / "visual-storyboard.json", storyboard_payload)
    artifacts["invariants"] = write_json(paths["checks"] / f"{chapter.id}-invariants.json", checks)
    final_sanity = {
        "chapter_id": chapter.id,
        "artifacts": {key: str(value.relative_to(paths["base"])) for key, value in artifacts.items()},
        "nonzero_artifacts": {key: value.stat().st_size for key, value in artifacts.items()},
        "checks": checks,
    }
    artifacts["final_sanity"] = write_json(paths["checks"] / "final-sanity.json", final_sanity)
    return {key: str(value) for key, value in artifacts.items()}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
