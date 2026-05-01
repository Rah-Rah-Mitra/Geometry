"""Deterministic visual builders for Modern Robotics notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon
import networkx as nx
import numpy as np

from utils.artifacts import save_json, save_matplotlib
from utils.control import pd_response
from utils.dynamics import apparent_inertia_curve, two_link_mass_matrix
from utils.grasping import friction_cone, grasp_matrix
from utils.kinematics import manipulability_measure, planar_arm_points, planar_jacobian
from utils.mobile import mecanum_wheel_matrix, unicycle_rollout
from utils.planning import cubic_time_scaling, dijkstra_grid, quintic_time_scaling
from utils.validation import image_stats

PALETTE = {
    "ink": "#1f2937",
    "blue": "#2563eb",
    "teal": "#0f766e",
    "green": "#4d7c0f",
    "gold": "#b7791f",
    "red": "#b91c1c",
    "violet": "#7c3aed",
    "gray": "#6b7280",
    "paper": "#fbfdff",
}


def _style(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b6c0ca")


def build_storyboard(chapter: dict[str, Any]) -> list[dict[str, str]]:
    slug = chapter["slug"]
    return [
        {
            "concept": "concept dependency map",
            "representation": "directed graph",
            "artifact": f"artifacts/{slug}/figures/concept-dependency-map.png",
            "inspection": "which definitions feed the chapter's computation",
        },
        {
            "concept": chapter["visual_focus"],
            "representation": chapter["visual_kind"],
            "artifact": f"artifacts/{slug}/figures/{chapter['artifact_stem']}-lab.png",
            "inspection": chapter["inspection_target"],
        },
        {
            "concept": "numeric invariant check",
            "representation": "residual bar chart and JSON summary",
            "artifact": f"artifacts/{slug}/figures/{chapter['artifact_stem']}-checks.png",
            "inspection": "small residuals, positive margins, or rank changes",
        },
    ]


def _concept_graph(chapter: dict[str, Any]) -> Path:
    labels = [chapter["title"]] + chapter["terms"][:7]
    graph = nx.DiGraph()
    graph.add_nodes_from(labels)
    for i, term in enumerate(labels[1:], start=1):
        graph.add_edge(labels[0], term)
        if i > 1:
            graph.add_edge(labels[i - 1], term)
    fig, ax = plt.subplots(figsize=(8.4, 5.2), facecolor=PALETTE["paper"])
    pos = nx.spring_layout(graph, seed=chapter["number"] + 17, k=0.9)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#e0f2fe", edgecolors=PALETTE["blue"], node_size=1450)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, edge_color=PALETTE["gray"], width=1.4, arrowsize=13)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    ax.set_axis_off()
    ax.set_title(f"{chapter['title']}: dependency map", fontsize=12, color=PALETTE["ink"])
    path = save_matplotlib(fig, chapter["slug"], "figures", "concept-dependency-map.png")
    plt.close(fig)
    return path


def _configuration_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    q1 = np.linspace(-math.pi, math.pi, 160)
    q2 = np.linspace(-math.pi, math.pi, 160)
    Q1, Q2 = np.meshgrid(q1, q2)
    reach = np.sqrt(1.0 + 0.8**2 + 2 * 0.8 * np.cos(Q2))
    singular = np.abs(np.sin(Q2))
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.2), facecolor=PALETTE["paper"])
    im = axes[0].imshow(reach, extent=[-math.pi, math.pi, -math.pi, math.pi], origin="lower", cmap="viridis")
    axes[0].set_xlabel("theta1")
    axes[0].set_ylabel("theta2")
    _style(axes[0], "2R reach over joint torus")
    fig.colorbar(im, ax=axes[0], shrink=0.78)
    pts = planar_arm_points(np.array([1.0, 0.8]), np.array([0.75, -1.2]))
    axes[1].plot(pts[:, 0], pts[:, 1], "-o", color=PALETTE["blue"], lw=3)
    axes[1].add_patch(Circle((0, 0), 1.8, fill=False, ls="--", edgecolor=PALETTE["gray"]))
    axes[1].add_patch(Circle((0, 0), 0.2, fill=False, ls=":", edgecolor=PALETTE["red"]))
    axes[1].set_xlim(-2.1, 2.1)
    axes[1].set_ylim(-2.1, 2.1)
    _style(axes[1], "workspace annulus from link lengths", equal=True)
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"min_reach": float(reach.min()), "max_reach": float(reach.max()), "singular_min": float(singular.min())}


def _rigid_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    fig = plt.figure(figsize=(9.2, 5.4), facecolor=PALETTE["paper"])
    ax = fig.add_subplot(111, projection="3d")
    origin = np.array([0.0, 0.0, 0.0])
    axes = np.eye(3)
    colors = [PALETTE["red"], PALETTE["green"], PALETTE["blue"]]
    for vec, color, label in zip(axes, colors, ["x", "y", "z"]):
        ax.quiver(*origin, *vec, color=color, linewidth=2.4, arrow_length_ratio=0.12)
        ax.text(*(1.08 * vec), label, color=color)
    theta = np.linspace(0, 1.6 * math.pi, 160)
    z = np.linspace(0, 1.2, 160)
    radius = 0.62
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, z, color=PALETTE["violet"], lw=2.6, label="screw path")
    ax.quiver(0, 0, 0, 0, 0, 1.2, color=PALETTE["ink"], lw=2, arrow_length_ratio=0.08)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_title(f"{chapter['title']}: screw motion as geometry", color=PALETTE["ink"])
    ax.legend(loc="upper left")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"path_length": float(np.sum(np.linalg.norm(np.diff(np.c_[x, y, z], axis=0), axis=1))), "axis_norm": 1.0}


def _kinematics_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    lengths = np.array([1.0, 0.75, 0.45])
    theta = np.array([0.55, -0.95, 0.72])
    pts = planar_arm_points(lengths, theta)
    J = planar_jacobian(lengths, theta)
    U, s, _ = np.linalg.svd(J)
    fig, ax = plt.subplots(figsize=(7.8, 6.2), facecolor=PALETTE["paper"])
    ax.plot(pts[:, 0], pts[:, 1], "-o", color=PALETTE["blue"], lw=3, label="open chain")
    ell = Ellipse(pts[-1], width=2 * s[0], height=2 * s[1], angle=np.degrees(np.arctan2(U[1, 0], U[0, 0])), alpha=0.26, color=PALETTE["gold"], label="velocity ellipsoid")
    ax.add_patch(ell)
    ax.quiver(pts[-1, 0], pts[-1, 1], U[0, 0] * s[0], U[1, 0] * s[0], color=PALETTE["red"], scale_units="xy", scale=1)
    ax.set_xlim(-2.4, 2.4)
    ax.set_ylim(-2.4, 2.4)
    ax.legend()
    _style(ax, f"{chapter['title']}: chain and Jacobian image", equal=True)
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"manipulability": manipulability_measure(J), "rank": float(np.linalg.matrix_rank(J))}


def _dynamics_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), facecolor=PALETTE["paper"])
    angles = np.linspace(-math.pi, math.pi, 180)
    eigs = np.array([np.linalg.eigvalsh(two_link_mass_matrix(a)) for a in angles])
    axes[0].plot(angles, eigs[:, 0], color=PALETTE["blue"], label="small eigenvalue")
    axes[0].plot(angles, eigs[:, 1], color=PALETTE["red"], label="large eigenvalue")
    axes[0].legend()
    _style(axes[0], "mass matrix eigenvalues")
    t, state = pd_response(16.0, 5.0)
    axes[1].plot(t, state[:, 0], color=PALETTE["teal"], label="position")
    axes[1].plot(t, state[:, 1], color=PALETTE["gold"], label="velocity")
    axes[1].axhline(1.0, color=PALETTE["gray"], ls="--", lw=1)
    axes[1].legend()
    _style(axes[1], "closed-loop response")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"min_mass_eig": float(eigs.min()), "final_error": float(abs(1.0 - state[-1, 0]))}


def _planning_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    cost = np.ones((42, 42))
    cost[12:30, 18:24] = np.inf
    cost[6:12, 5:31] = np.inf
    path_nodes = dijkstra_grid(cost, (36, 4), (5, 36))
    t = np.linspace(0, 1, 200)
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4), facecolor=PALETTE["paper"])
    axes[0].imshow(np.isinf(cost), cmap="Greys", origin="lower")
    if path_nodes:
        rc = np.asarray(path_nodes)
        axes[0].plot(rc[:, 1], rc[:, 0], color=PALETTE["blue"], lw=2.4)
    _style(axes[0], "grid planner with obstacles", equal=True)
    axes[1].plot(t, cubic_time_scaling(t, 1.0), color=PALETTE["teal"], label="cubic")
    axes[1].plot(t, quintic_time_scaling(t, 1.0), color=PALETTE["violet"], label="quintic")
    axes[1].legend()
    _style(axes[1], "time scaling profiles")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"path_nodes": float(len(path_nodes)), "quintic_terminal": float(quintic_time_scaling(np.array([1.0]), 1.0)[0])}


def _contact_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4), facecolor=PALETTE["paper"])
    cone = friction_cone(np.array([0.0, 1.0]), 0.55)
    for ray in cone:
        axes[0].arrow(0, 0, ray[0], ray[1], color=PALETTE["blue"], alpha=0.55, head_width=0.025, length_includes_head=True)
    axes[0].add_patch(Polygon([[-0.75, -0.08], [0.75, -0.08], [0.75, 0.0], [-0.75, 0.0]], color="#e5e7eb"))
    _style(axes[0], "planar friction cone", equal=True)
    points = np.array([[1.0, 0.0], [-0.5, 0.86], [-0.5, -0.86]])
    normals = -points
    G = grasp_matrix(points, normals)
    axes[1].imshow(G, cmap="coolwarm", aspect="auto")
    axes[1].set_xlabel("contact")
    axes[1].set_ylabel("wrench component")
    _style(axes[1], "grasp matrix signs")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"grasp_rank": float(np.linalg.matrix_rank(G)), "cone_rays": float(len(cone))}


def _mobile_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    controls = np.c_[np.ones(180) * 0.7, 0.9 * np.sin(np.linspace(0, 2.4 * math.pi, 180))]
    path_xy = unicycle_rollout(controls)
    H = mecanum_wheel_matrix()
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4), facecolor=PALETTE["paper"])
    axes[0].plot(path_xy[:, 1], path_xy[:, 2], color=PALETTE["blue"], lw=2.6)
    axes[0].quiver(path_xy[::25, 1], path_xy[::25, 2], np.cos(path_xy[::25, 0]), np.sin(path_xy[::25, 0]), color=PALETTE["red"], width=0.006)
    _style(axes[0], "unicycle rollout in SE(2)", equal=True)
    axes[1].imshow(H, cmap="viridis", aspect="auto")
    axes[1].set_xlabel("chassis velocity component")
    axes[1].set_ylabel("wheel")
    _style(axes[1], "mecanum wheel map")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"wheel_rank": float(np.linalg.matrix_rank(H)), "path_distance": float(np.sum(np.linalg.norm(np.diff(path_xy[:, 1:3], axis=0), axis=1)))}


def _appendix_visual(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    theta = np.linspace(0, math.pi * 0.98, 160)
    quat_scalar = np.cos(theta / 2)
    cayley_norm = np.tan(theta / 2)
    ratios = np.linspace(1, 12, 80)
    inertia = apparent_inertia_curve(ratios)
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.4), facecolor=PALETTE["paper"])
    axes[0].plot(theta, quat_scalar, color=PALETTE["blue"], label="quaternion scalar")
    axes[0].plot(theta, np.clip(cayley_norm, 0, 8), color=PALETTE["red"], label="Cayley norm, clipped")
    axes[0].legend()
    _style(axes[0], "rotation parameter behavior")
    axes[1].plot(ratios, inertia, color=PALETTE["teal"])
    _style(axes[1], "quadratic scaling example")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-lab.png")
    plt.close(fig)
    return path, {"max_cayley_norm_clipped": float(np.clip(cayley_norm, 0, 8).max()), "inertia_growth": float(inertia[-1] / inertia[0])}


def _visual_by_theme(chapter: dict[str, Any]) -> tuple[Path, dict[str, float]]:
    theme = chapter["theme"]
    if theme == "configuration":
        return _configuration_visual(chapter)
    if theme == "rigid":
        return _rigid_visual(chapter)
    if theme == "kinematics":
        return _kinematics_visual(chapter)
    if theme == "dynamics":
        return _dynamics_visual(chapter)
    if theme == "planning":
        return _planning_visual(chapter)
    if theme == "contact":
        return _contact_visual(chapter)
    if theme == "mobile":
        return _mobile_visual(chapter)
    return _appendix_visual(chapter)


def _check_visual(chapter: dict[str, Any], metrics: dict[str, float]) -> Path:
    names = list(metrics.keys())
    vals = np.array([abs(float(metrics[name])) for name in names], dtype=float)
    scaled = vals / np.maximum(vals.max(), 1.0)
    fig, ax = plt.subplots(figsize=(8.0, 4.2), facecolor=PALETTE["paper"])
    ax.barh(names, scaled, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["violet"]][: len(names)])
    ax.set_xlim(0, 1.05)
    _style(ax, f"{chapter['title']}: invariant magnitudes")
    path = save_matplotlib(fig, chapter["slug"], "figures", f"{chapter['artifact_stem']}-checks.png")
    plt.close(fig)
    return path


def build_chapter_visuals(chapter: dict[str, Any]) -> dict[str, Any]:
    concept = _concept_graph(chapter)
    lab, metrics = _visual_by_theme(chapter)
    check = _check_visual(chapter, metrics)
    stats = {path.name: image_stats(path) for path in [concept, lab, check]}
    checks = save_json({"metrics": metrics, "image_stats": stats}, chapter["slug"], "checks", "final-sanity.json")
    return {
        "storyboard": build_storyboard(chapter),
        "figures": [concept, lab, check],
        "checks": checks,
        "metrics": metrics,
    }

