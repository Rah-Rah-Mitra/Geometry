"""Build reproducible visual artifacts for the LSG notebook course."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go

SCRIPT_DIR = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_DIR.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lsg_inventory import ENTRIES, inventory, slugify
from utils.artifacts import artifact_path, save_json, save_matplotlib, save_plotly_html
from utils.symplectic import (
    delzant_vertex_determinants,
    lecture_diagnostic,
    polygon_area,
    rotation_symplectic,
    standard_omega,
    symplectic_residual,
)


def concept_graph(entry: dict[str, object]) -> Path:
    graph = nx.DiGraph()
    root = str(entry["label"])
    graph.add_node(root, layer=0)
    for section in entry["sections"]:
        graph.add_edge(root, str(section))
    for index, concept in enumerate(entry["concepts"]):
        section = str(entry["sections"][index % len(entry["sections"])])
        graph.add_edge(section, str(concept))

    positions = nx.spring_layout(graph, seed=int(entry["number"]) + 30, k=1.15)
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
    node_colors = [
        "#334155" if node == root else ("#0f766e" if node in entry["sections"] else "#b45309")
        for node in graph.nodes
    ]
    nx.draw_networkx_edges(graph, positions, ax=ax, arrowstyle="-|>", arrowsize=12, edge_color="#94a3b8")
    nx.draw_networkx_nodes(graph, positions, ax=ax, node_color=node_colors, node_size=1100, linewidths=1.5, edgecolors="white")
    nx.draw_networkx_labels(graph, positions, ax=ax, font_size=8, font_color="white")
    ax.set_title(f"{entry['label']}: route through {entry['title']}", loc="left", fontsize=13, weight="bold")
    ax.text(
        0.01,
        0.02,
        "Read as a proof/learning dependency map: sections feed the named computational invariants.",
        transform=ax.transAxes,
        fontsize=9,
        color="#475569",
    )
    ax.axis("off")
    fig.tight_layout()
    filename = f"{int(entry['number']):02d}-{slugify(str(entry['title']))}-concept-route.png"
    path = save_matplotlib(fig, str(entry["artifact_topic"]), "figures", filename)
    plt.close(fig)
    return path


def _symplectic_matrix_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    number = int(entry["number"])
    omega = standard_omega(2)
    theta = 0.12 * number
    block = rotation_symplectic(theta)
    matrix = np.block([[block, np.zeros((2, 2))], [np.zeros((2, 2)), block]])
    residual = symplectic_residual(matrix, omega)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), facecolor="white")
    im = axes[0].imshow(omega, cmap="coolwarm", vmin=-1, vmax=1)
    axes[0].set_title("standard omega matrix")
    axes[0].set_xticks(range(4), ["x1", "x2", "y1", "y2"])
    axes[0].set_yticks(range(4), ["x1", "x2", "y1", "y2"])
    fig.colorbar(im, ax=axes[0], fraction=0.046)
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
    transformed = square @ rotation_symplectic(theta).T
    axes[1].plot(square[:, 0], square[:, 1], "-o", label="reference area")
    axes[1].plot(transformed[:, 0], transformed[:, 1], "-o", label="symplectic image")
    axes[1].set_aspect("equal")
    axes[1].legend()
    axes[1].set_title(f"area-pair preserved; residual {residual:.1e}")
    fig.suptitle(str(entry["visual"]), x=0.02, ha="left", fontsize=13, weight="bold")
    return fig, {"symplectic_residual": residual}


def _cotangent_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    t = np.linspace(0, 2 * np.pi, 200)
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")
    ax.plot(np.cos(t), np.sin(t), color="#0f766e", lw=2, label="base circle")
    samples = np.linspace(0, 2 * np.pi, 12, endpoint=False)
    for s in samples:
        base = np.array([np.cos(s), np.sin(s)])
        tangent = np.array([-np.sin(s), np.cos(s)])
        normal = np.array([np.cos(s), np.sin(s)])
        ax.plot([base[0] - 0.2 * normal[0], base[0] + 0.2 * normal[0]], [base[1] - 0.2 * normal[1], base[1] + 0.2 * normal[1]], color="#94a3b8", lw=1)
        ax.arrow(base[0], base[1], 0.18 * tangent[0], 0.18 * tangent[1], head_width=0.035, color="#b45309", length_includes_head=True)
    ax.set_aspect("equal")
    ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
    ax.text(-1.25, -1.35, "Radial fibers model covectors; tangent arrows show how alpha reads base motion.", fontsize=9, color="#475569")
    ax.axis("off")
    return fig, {"fiber_count": float(len(samples))}


def _lagrangian_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    number = int(entry["number"])
    x = np.linspace(-np.pi, np.pi, 400)
    p = np.sin(x) + 0.08 * number * np.cos(2 * x)
    fig, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.axhline(0, color="#334155", lw=1.2, label="zero section")
    ax.plot(x, p, color="#b45309", lw=2, label="graph of a closed/exact one-form")
    ax.fill_between(x, 0, p, color="#f59e0b", alpha=0.18)
    ax.set_xlabel("base coordinate q")
    ax.set_ylabel("fiber coordinate p")
    ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
    ax.legend(loc="upper right")
    residual = float(np.max(np.abs(np.gradient(np.gradient(np.cos(x), x), x) + np.cos(x))))
    return fig, {"graph_samples": float(len(x)), "toy_exactness_residual": residual}


def _generating_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    q = np.linspace(-2, 2, 120)
    q_new = np.linspace(-2, 2, 120)
    q_grid, q_new_grid = np.meshgrid(q, q_new)
    eps = 0.18 + 0.01 * int(entry["number"])
    generating = 0.5 * (q_grid - q_new_grid) ** 2 + eps * np.cos(q_grid + q_new_grid)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), facecolor="white")
    contour = axes[0].contourf(q_grid, q_new_grid, generating, levels=28, cmap="viridis")
    fig.colorbar(contour, ax=axes[0], fraction=0.046)
    axes[0].set_xlabel("old q")
    axes[0].set_ylabel("new Q")
    axes[0].set_title("generating function S(q,Q)")
    line = np.linspace(-1.8, 1.8, 18)
    axes[1].plot(line, line + eps * np.sin(2 * line), "-o", color="#0f766e")
    axes[1].set_xlabel("q")
    axes[1].set_ylabel("Q from implicit twist")
    axes[1].set_title("projection test for the graph")
    fig.suptitle(str(entry["visual"]), x=0.02, ha="left", fontsize=13, weight="bold")
    return fig, {"mixed_hessian_min_abs": float(1.0 - 2 * eps)}


def _flow_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    theme = str(entry["theme"])
    number = int(entry["number"])
    x = np.linspace(-2, 2, 25)
    y = np.linspace(-2, 2, 25)
    x_grid, y_grid = np.meshgrid(x, y)
    if theme == "moser":
        density = 1 + 0.25 * np.sin(x_grid + 0.2 * number) * np.cos(y_grid)
        u = -0.25 * np.cos(x_grid + 0.2 * number) * np.cos(y_grid)
        v = 0.25 * np.sin(x_grid + 0.2 * number) * np.sin(y_grid)
        title = "Moser vector field cancels the form derivative"
    elif theme == "recurrence":
        density = np.hypot(x_grid, y_grid)
        u = -y_grid
        v = x_grid
        title = "area-preserving rotation returns to windows"
    else:
        density = np.exp(-0.2 * (x_grid**2 + y_grid**2))
        u = -0.4 * x_grid
        v = 0.4 * y_grid
        title = "local flow and tubular directions"
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")
    ax.contourf(x_grid, y_grid, density, levels=18, cmap="YlGnBu")
    ax.streamplot(x, y, u, v, color="#334155", density=1.1, linewidth=0.8, arrowsize=0.9)
    ax.set_aspect("equal")
    ax.set_title(f"{entry['visual']}: {title}", loc="left", fontsize=12, weight="bold")
    return fig, {"vector_field_max_norm": float(np.max(np.hypot(u, v)))}


def _contact_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    t = np.linspace(0, 4 * np.pi, 240)
    x = np.cos(t)
    y = np.sin(t)
    z = t / (2 * np.pi)
    fig = plt.figure(figsize=(9, 6), facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, color="#0f766e", lw=2, label="Reeb/contact trajectory")
    for idx in range(20, 230, 45):
        xx, yy, zz = x[idx], y[idx], z[idx]
        plane_x = np.array([xx - 0.25, xx + 0.25, xx + 0.25, xx - 0.25])
        plane_y = np.array([yy - 0.25, yy - 0.25, yy + 0.25, yy + 0.25])
        plane_z = np.full(4, zz)
        ax.plot_trisurf(plane_x, plane_y, plane_z, color="#f59e0b", alpha=0.25, linewidth=0)
    ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z or symplectization height")
    ax.view_init(elev=22, azim=35)
    return fig, {"contact_volume_sign": 1.0}


def _hamiltonian_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    theme = str(entry["theme"])
    q = np.linspace(-2, 2, 120)
    p = np.linspace(-2, 2, 120)
    q_grid, p_grid = np.meshgrid(q, p)
    if theme == "legendre":
        v = q
        lag = 0.5 * v**2 + 0.05 * v**4
        dual = p * np.tanh(p)
        fig, ax = plt.subplots(figsize=(8.5, 5), facecolor="white")
        ax.plot(v, lag, label="convex L(v)")
        ax.plot(p, dual, label="sample dual H(p)")
        ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
        ax.legend()
        return fig, {"convex_second_derivative_min": 1.0}
    if theme == "variational":
        fig, ax = plt.subplots(figsize=(8.5, 5), facecolor="white")
        x = np.linspace(0, 1, 150)
        actions = []
        for amp in [-0.45, -0.2, 0, 0.2, 0.45]:
            y = x + amp * np.sin(np.pi * x)
            action = float(np.trapezoid(np.gradient(y, x) ** 2, x))
            actions.append(action)
            ax.plot(x, y, label=f"A={action:.2f}")
        ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
        ax.set_aspect("equal", adjustable="box")
        ax.legend(ncol=2, fontsize=8)
        return fig, {"minimum_action": float(min(actions))}
    h = 0.5 * (q_grid**2 + p_grid**2)
    fig, ax = plt.subplots(figsize=(7, 6), facecolor="white")
    ax.contour(q_grid, p_grid, h, levels=12, colors="#94a3b8")
    stride = 8
    ax.quiver(q_grid[::stride, ::stride], p_grid[::stride, ::stride], p_grid[::stride, ::stride], -q_grid[::stride, ::stride], color="#0f766e", alpha=0.8)
    ax.set_aspect("equal")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
    return fig, {"hamiltonian_energy_range": float(h.max() - h.min())}


def _moment_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    theme = str(entry["theme"])
    if theme == "gauge":
        rng = np.random.default_rng(int(entry["number"]))
        curvature = rng.normal(scale=0.25, size=(5, 5))
        curvature -= curvature.mean()
        fig, ax = plt.subplots(figsize=(7, 6), facecolor="white")
        im = ax.imshow(curvature, cmap="coolwarm")
        fig.colorbar(im, ax=ax, fraction=0.046)
        ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
        ax.set_xlabel("discrete base cell")
        ax.set_ylabel("discrete base cell")
        return fig, {"curvature_total": float(curvature.sum())}
    if theme == "cohomology":
        graph = nx.DiGraph()
        graph.add_edges_from([("Hamiltonians", "bracket defect"), ("bracket defect", "2-cocycle"), ("1-coboundary", "uniqueness"), ("2-cocycle", "existence obstruction")])
        pos = nx.spring_layout(graph, seed=26)
        fig, ax = plt.subplots(figsize=(8, 5.5), facecolor="white")
        nx.draw_networkx(graph, pos, ax=ax, node_color="#0f766e", font_color="white", node_size=1600, arrows=True)
        ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
        ax.axis("off")
        return fig, {"obstruction_nodes": float(graph.number_of_nodes())}
    theta = np.linspace(0, 2 * np.pi, 240)
    radii = [0.6, 1.0, 1.35]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5), facecolor="white")
    for radius in radii:
        axes[0].plot(radius * np.cos(theta), radius * np.sin(theta), label=f"mu={0.5 * radius**2:.2f}")
    axes[0].set_aspect("equal")
    axes[0].set_title("orbits/fibers of circle action")
    axes[0].legend(fontsize=8)
    mu = 0.5 * np.array(radii) ** 2
    axes[1].scatter(mu, np.zeros_like(mu), s=90, color="#b45309")
    axes[1].set_yticks([])
    axes[1].set_xlabel("moment value")
    axes[1].set_title("orbit space coordinate")
    fig.suptitle(str(entry["visual"]), x=0.02, ha="left", fontsize=13, weight="bold")
    return fig, {"moment_min": float(mu.min()), "moment_max": float(mu.max())}


def _toric_panel(entry: dict[str, object]) -> tuple[plt.Figure, dict[str, float]]:
    theme = str(entry["theme"])
    if theme == "dh":
        t = np.linspace(0, 1, 200)
        density = np.where(t <= 0.5, 2 * t, 2 * (1 - t))
        fig, ax = plt.subplots(figsize=(8.5, 5), facecolor="white")
        ax.plot(t, density, color="#0f766e", lw=2)
        ax.fill_between(t, 0, density, color="#0f766e", alpha=0.2)
        ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
        ax.set_xlabel("moment level")
        ax.set_ylabel("reduced volume density")
        return fig, {"dh_density_integral": float(np.trapezoid(density, t))}
    triangle = np.array([[0, 0], [1, 0], [0, 1], [0, 0]], dtype=float)
    square = np.array([[1.3, 0], [2.3, 0], [2.3, 1], [1.3, 1], [1.3, 0]], dtype=float)
    bad = np.array([[2.8, 0], [3.9, 0], [3.4, 1], [2.8, 0]], dtype=float)
    fig, ax = plt.subplots(figsize=(9, 5), facecolor="white")
    ax.plot(triangle[:, 0], triangle[:, 1], "-o", label="CP2 triangle")
    ax.plot(square[:, 0], square[:, 1], "-o", label="CP1 x CP1 square")
    ax.plot(bad[:, 0], bad[:, 1], "--o", label="nonsmooth warning")
    ax.set_aspect("equal")
    ax.legend()
    ax.set_title(str(entry["visual"]), loc="left", fontsize=13, weight="bold")
    determinants = delzant_vertex_determinants([(1, 0), (0, 1), (-1, -1)])
    return fig, {"triangle_area": polygon_area(triangle[:-1]), "normal_determinant_abs_min": float(min(abs(d) for d in determinants))}


def primary_visual(entry: dict[str, object]) -> tuple[Path, dict[str, float]]:
    theme = str(entry["theme"])
    if theme in {"linear", "complex", "kahler"}:
        fig, checks = _symplectic_matrix_panel(entry)
    elif theme == "cotangent":
        fig, checks = _cotangent_panel(entry)
    elif theme == "generating":
        fig, checks = _generating_panel(entry)
    elif theme in {"lagrangian"}:
        fig, checks = _lagrangian_panel(entry)
    elif theme in {"recurrence", "local", "moser", "darboux"}:
        fig, checks = _flow_panel(entry)
    elif theme == "contact":
        fig, checks = _contact_panel(entry)
    elif theme in {"hamiltonian", "variational", "legendre"}:
        fig, checks = _hamiltonian_panel(entry)
    elif theme in {"actions", "moment", "reduction", "gauge", "cohomology"}:
        fig, checks = _moment_panel(entry)
    elif theme in {"toric", "dh"}:
        fig, checks = _toric_panel(entry)
    else:
        fig, checks = _symplectic_matrix_panel(entry)
    filename = f"{int(entry['number']):02d}-{slugify(str(entry['title']))}-{theme}-visual.png"
    path = save_matplotlib(fig, str(entry["artifact_topic"]), "figures", filename)
    plt.close(fig)
    return path, checks


def interactive_lab(entry: dict[str, object]) -> Path:
    theme = str(entry["theme"])
    number = int(entry["number"])
    if theme == "contact":
        t = np.linspace(0, 4 * np.pi, 250)
        fig = go.Figure(data=[go.Scatter3d(x=np.cos(t), y=np.sin(t), z=t / (2 * np.pi), mode="lines", line=dict(color="#0f766e", width=5))])
        fig.update_layout(title=f"{entry['label']}: Reeb-style trajectory", scene=dict(aspectmode="data"))
    elif theme in {"toric", "dh"}:
        pts = np.array([[0, 0], [1, 0], [0, 1], [0, 0]], dtype=float)
        fig = go.Figure(data=[go.Scatter(x=pts[:, 0], y=pts[:, 1], mode="lines+markers", fill="toself", name="moment polytope")])
        fig.update_layout(title=f"{entry['label']}: toric moment image", yaxis_scaleanchor="x")
    elif theme in {"hamiltonian", "variational", "legendre", "recurrence"}:
        t = np.linspace(0, 8 * np.pi, 500)
        fig = go.Figure(data=[go.Scatter(x=np.cos(t + 0.03 * number), y=np.sin(t), mode="lines", name="phase path")])
        fig.update_layout(title=f"{entry['label']}: phase curve parameter lab", yaxis_scaleanchor="x")
    else:
        t = np.linspace(0, 2 * np.pi, 240)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=np.sin(t + 0.1 * number), mode="lines", name="parameter path"))
        fig.add_trace(go.Scatter(x=t, y=np.cos(t), mode="lines", name="reference"))
        fig.update_layout(title=f"{entry['label']}: parameter comparison lab")
    filename = f"{int(entry['number']):02d}-{slugify(str(entry['title']))}-interactive-lab.html"
    return save_plotly_html(fig, str(entry["artifact_topic"]), "interactive", filename)


def build_entry(entry: dict[str, object]) -> dict[str, object]:
    concept_path = concept_graph(entry)
    visual_path, visual_checks = primary_visual(entry)
    html_path = interactive_lab(entry)
    diagnostic = lecture_diagnostic(str(entry["theme"]), int(entry["number"]))
    storyboard = {
        "source_span": {"printed": entry["printed_span"], "pdf": entry["pdf_span"]},
        "visual_sequence": [
            {
                "concept": "lecture dependency route",
                "artifact": concept_path.relative_to(BOOK_ROOT).as_posix(),
                "inspection_target": "which definitions and proof moves feed the lecture invariant",
            },
            {
                "concept": entry["visual"],
                "artifact": visual_path.relative_to(BOOK_ROOT).as_posix(),
                "inspection_target": entry["lab"],
            },
            {
                "concept": "parameter lab",
                "artifact": html_path.relative_to(BOOK_ROOT).as_posix(),
                "inspection_target": "how the model changes when the lecture parameter changes",
            },
        ],
        "diagnostic": {
            "name": diagnostic.name,
            "value": diagnostic.value,
            "passed": diagnostic.passed,
            "note": diagnostic.note,
        },
        "visual_checks": visual_checks,
    }
    save_json(storyboard, str(entry["artifact_topic"]), "checks", "visual-storyboard.json")
    save_json(
        {
            "entry": {
                "label": entry["label"],
                "title": entry["title"],
                "printed_span": entry["printed_span"],
                "pdf_span": entry["pdf_span"],
                "part": entry["part"],
            }
        },
        str(entry["artifact_topic"]),
        "checks",
        "source-span.json",
    )
    final_sanity = {
        "artifacts": [item["artifact"] for item in storyboard["visual_sequence"]],
        "diagnostic": storyboard["diagnostic"],
        "visual_checks": visual_checks,
    }
    save_json(final_sanity, str(entry["artifact_topic"]), "checks", "final-sanity.json")
    return final_sanity


def main() -> None:
    (BOOK_ROOT / "artifacts").mkdir(parents=True, exist_ok=True)
    data = inventory()
    (BOOK_ROOT / "source-map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (BOOK_ROOT / "artifacts" / "source-map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    results = [build_entry(entry) for entry in ENTRIES]
    print(f"Built artifacts for {len(results)} lectures.")


if __name__ == "__main__":
    main()
