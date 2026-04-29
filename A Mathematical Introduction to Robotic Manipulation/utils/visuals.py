"""Deterministic concept visuals for the robotics manipulation notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import networkx as nx
import numpy as np
from PIL import Image

from utils.artifacts import artifact_path
from utils.robots import planar_arm_points, planar_workspace

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


def _stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {"width": image.width, "height": image.height, "file_size": path.stat().st_size, "pixel_std": float(arr.std())}


def _note(ax: Any, text: str) -> None:
    ax.text(0.02, 0.97, text, transform=ax.transAxes, va="top", fontsize=8, color=PALETTE["ink"], bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92})


def _plot_network(ax: Any, labels: list[str], edges: list[tuple[str, str]], title: str) -> None:
    graph = nx.DiGraph()
    graph.add_nodes_from(labels)
    graph.add_edges_from(edges)
    pos = nx.spring_layout(graph, seed=7)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color="#e0f2fe", edgecolors=PALETTE["blue"], node_size=1100)
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, edge_color=PALETTE["gray"], width=1.4, arrowsize=12)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8)
    ax.set_axis_off()
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])


def _plot_timeline(ax: Any, title: str) -> dict[str, Any]:
    events = ["teleop", "CNC", "sensors", "industrial", "hands", "planning"]
    x = np.arange(len(events))
    ax.plot(x, np.zeros_like(x), color=PALETTE["gray"], lw=2)
    ax.scatter(x, np.zeros_like(x), s=120, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["green"], PALETTE["red"], PALETTE["violet"]])
    for i, event in enumerate(events):
        ax.text(i, 0.12 if i % 2 == 0 else -0.18, event, ha="center", fontsize=9)
    ax.set_ylim(-0.45, 0.45)
    ax.set_yticks([])
    _style(ax, title)
    _note(ax, "abstract redraw: no textbook photos")
    return {"event_count": len(events)}


def _plot_taxonomy(ax: Any, title: str) -> dict[str, Any]:
    labels = ["rigid body", "serial arm", "hand", "mobile base", "contact", "nonholonomic"]
    edges = [("rigid body", "serial arm"), ("rigid body", "hand"), ("hand", "contact"), ("mobile base", "nonholonomic"), ("contact", "nonholonomic")]
    _plot_network(ax, labels, edges, title)
    return {"node_count": len(labels), "edge_count": len(edges)}


def _plot_dependency(ax: Any, title: str) -> dict[str, Any]:
    labels = ["SE(3)", "POE", "Jacobian", "Dynamics", "Grasp", "Nonholonomic", "Planning"]
    edges = [("SE(3)", "POE"), ("POE", "Jacobian"), ("Jacobian", "Dynamics"), ("Jacobian", "Grasp"), ("SE(3)", "Nonholonomic"), ("Nonholonomic", "Planning")]
    _plot_network(ax, labels, edges, title)
    return {"acyclic": True, "node_count": len(labels)}


def _plot_frames(ax: Any, title: str) -> dict[str, Any]:
    ax.arrow(0, 0, 1, 0, head_width=0.06, color=PALETTE["blue"])
    ax.arrow(0, 0, 0, 1, head_width=0.06, color=PALETTE["teal"])
    angle = 0.55
    origin = np.array([1.2, 0.55])
    R = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    for vec, color, label in [(R[:, 0], PALETTE["red"], "x'"), (R[:, 1], PALETTE["gold"], "y'")]:
        ax.arrow(origin[0], origin[1], vec[0], vec[1], head_width=0.06, color=color)
        ax.text(*(origin + 1.08 * vec), label, fontsize=9)
    pts = np.array([[0.2, 0.25], [0.7, 0.2], [0.35, 0.7]])
    moved = pts @ R.T + origin
    ax.plot(*pts.T, "o-", color=PALETTE["blue"], label="body points")
    ax.plot(*moved.T, "o-", color=PALETTE["red"], label="same distances")
    ax.legend(fontsize=8)
    ax.set_xlim(-0.25, 2.6)
    ax.set_ylim(-0.25, 2.0)
    _style(ax, title, equal=True)
    return {"distance_preserved": True}


def _plot_screw(ax: Any, title: str) -> dict[str, Any]:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    t = np.linspace(0, 4 * np.pi, 220)
    ax3.plot(np.cos(t), np.sin(t), 0.12 * t, color=PALETTE["blue"], lw=2)
    ax3.plot([0, 0], [0, 0], [0, 1.6], color=PALETTE["red"], lw=2, label="screw axis")
    for z in np.linspace(0, 1.4, 5):
        ax3.quiver(0, 0, z, 0.4, 0, 0, color=PALETTE["teal"], length=0.35)
    ax3.set_title(title, fontsize=11)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("translation")
    return {"pitch": 0.12}


def _plot_wrench(ax: Any, title: str) -> dict[str, Any]:
    ax.arrow(-1, 0, 2, 0.35, head_width=0.08, color=PALETTE["blue"], length_includes_head=True)
    ax.arrow(0, 0, -0.25, 0.75, head_width=0.08, color=PALETTE["red"], length_includes_head=True)
    theta = np.linspace(0, 2 * np.pi, 120)
    ax.plot(0.2 * np.cos(theta), 0.2 * np.sin(theta), color=PALETTE["gold"], lw=2)
    ax.text(-0.9, 0.38, "force line", fontsize=9)
    ax.text(-0.55, 0.7, "twist", fontsize=9)
    _style(ax, title, equal=True)
    _note(ax, "power = wrench dot twist")
    return {"power_pairing": True}


def _plot_manipulator(ax: Any, title: str) -> dict[str, Any]:
    pts = planar_arm_points([0.7, -1.1, 0.55], (1.0, 0.75, 0.45))
    ax.plot(pts[:, 0], pts[:, 1], "o-", color=PALETTE["blue"], lw=3)
    for i, p in enumerate(pts[:-1]):
        ax.add_patch(plt.Circle(p, 0.08, fill=False, color=PALETTE["red"], lw=1.5))
        ax.text(p[0] + 0.05, p[1] + 0.08, f"S{i+1}", fontsize=8)
    ax.scatter([pts[-1, 0]], [pts[-1, 1]], s=80, color=PALETTE["gold"], label="tool")
    ax.legend(fontsize=8)
    ax.set_xlim(-0.2, 2.3)
    ax.set_ylim(-0.6, 1.6)
    _style(ax, title, equal=True)
    return {"joint_count": 3}


def _plot_workspace(ax: Any, title: str) -> dict[str, Any]:
    pts = planar_workspace((1.0, 0.75), samples=54)
    ax.scatter(pts[:, 0], pts[:, 1], s=2, color=PALETTE["blue"], alpha=0.35)
    ax.add_patch(Ellipse((0.9, 0.65), 0.55, 0.18, angle=35, fill=False, color=PALETTE["red"], lw=2))
    _style(ax, title, equal=True)
    _note(ax, "velocity ellipsoid collapses near singular poses")
    return {"sample_count": int(len(pts))}


def _plot_singularity(ax: Any, title: str) -> dict[str, Any]:
    for i, q2 in enumerate([0.05, 0.5, 1.4]):
        base = np.array([i * 1.25, 0.0])
        pts = planar_arm_points([0.0, q2], (0.65, 0.55)) + base
        ax.plot(pts[:, 0], pts[:, 1], "o-", lw=2, color=[PALETTE["red"], PALETTE["gold"], PALETTE["teal"]][i])
        ax.text(base[0], -0.25, f"rank cue {i+1}", fontsize=8)
    ax.set_xlim(-0.25, 3.2)
    ax.set_ylim(-0.45, 1.1)
    _style(ax, title, equal=True)
    return {"cases": 3}


def _plot_dynamics(ax: Any, title: str) -> dict[str, Any]:
    q1 = np.linspace(-np.pi, np.pi, 80)
    q2 = np.linspace(-np.pi, np.pi, 80)
    Q1, Q2 = np.meshgrid(q1, q2)
    Z = 1.5 + 0.6 * np.cos(Q2) + 0.15 * np.sin(Q1)
    img = ax.contourf(Q1, Q2, Z, levels=18, cmap="viridis")
    plt.colorbar(img, ax=ax, fraction=0.045, pad=0.03, label="M11")
    ax.set_xlabel("q1")
    ax.set_ylabel("q2")
    _style(ax, title)
    return {"min_inertia": float(Z.min()), "max_inertia": float(Z.max())}


def _plot_phase(ax: Any, title: str) -> dict[str, Any]:
    x = np.linspace(-2, 2, 24)
    y = np.linspace(-2, 2, 24)
    X, Y = np.meshgrid(x, y)
    U, V = Y, -3 * X - 1.1 * Y
    speed = np.hypot(U, V)
    ax.streamplot(X, Y, U, V, color=speed, cmap="plasma", density=1.1)
    ax.contour(X, Y, 0.5 * Y**2 + 1.5 * X**2, levels=8, colors="white", linewidths=0.6)
    _style(ax, title, equal=True)
    return {"max_speed": float(speed.max())}


def _plot_geometric_phase(ax: Any, title: str) -> dict[str, Any]:
    theta = np.linspace(0, 2 * np.pi, 240)
    radius = 0.82
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    ax.plot(x, y, color=PALETTE["blue"], lw=2, label="contact loop")
    ax.fill(x, y, color="#dbeafe", alpha=0.55, label="enclosed area")
    for index in np.linspace(0, len(theta) - 1, 10, dtype=int):
        p = np.array([x[index], y[index]])
        tangent = np.array([-np.sin(theta[index]), np.cos(theta[index])])
        normal = np.array([np.cos(theta[index]), np.sin(theta[index])])
        v = 0.17 * tangent + 0.08 * normal
        ax.arrow(p[0], p[1], v[0], v[1], head_width=0.035, color=PALETTE["teal"], length_includes_head=True)
    ax.arrow(0.0, 0.0, 0.45, 0.0, head_width=0.045, color=PALETTE["red"], length_includes_head=True)
    ax.text(-0.55, -1.05, "rolling loop: orientation change tracks signed area", fontsize=9)
    ax.legend(fontsize=8, loc="upper right")
    _style(ax, title, equal=True)
    return {"loop_area": float(np.pi * radius**2), "transport_arrows": 10}


def _plot_control(ax: Any, title: str) -> dict[str, Any]:
    t = np.linspace(0, 5, 300)
    pd = np.exp(-0.65 * t) * np.cos(2.4 * t)
    ct = np.exp(-1.2 * t) * np.cos(1.1 * t)
    ax.plot(t, pd, color=PALETTE["gold"], label="PD error")
    ax.plot(t, ct, color=PALETTE["blue"], label="computed torque error")
    ax.axhline(0, color=PALETTE["gray"], lw=1)
    ax.legend(fontsize=8)
    ax.set_xlabel("time")
    ax.set_ylabel("tracking error")
    _style(ax, title)
    return {"final_error": float(abs(ct[-1]))}


def _plot_cone(ax: Any, title: str) -> dict[str, Any]:
    ax.add_patch(plt.Rectangle((-0.9, -0.25), 1.8, 0.5, fill=False, edgecolor=PALETTE["ink"], lw=2))
    for x in [-0.55, 0.55]:
        ax.scatter([x], [0.25], color=PALETTE["red"], s=50)
        ax.plot([x, x - 0.45], [0.25, 0.9], color=PALETTE["blue"])
        ax.plot([x, x + 0.45], [0.25, 0.9], color=PALETTE["blue"])
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-0.45, 1.15)
    _style(ax, title, equal=True)
    return {"contact_count": 2}


def _plot_grasp(ax: Any, title: str) -> dict[str, Any]:
    angles = np.linspace(0, 2 * np.pi, 7, endpoint=False)
    x, y = np.cos(angles), np.sin(angles)
    ax.scatter(x, y, c=np.linspace(0, 1, len(x)), cmap="viridis", s=80)
    for xi, yi in zip(x, y):
        ax.arrow(0, 0, 0.75 * xi, 0.75 * yi, head_width=0.05, color=PALETTE["blue"], alpha=0.65)
    ax.scatter([0], [0], color=PALETTE["red"], s=60, label="origin")
    ax.legend(fontsize=8)
    _style(ax, title, equal=True)
    _note(ax, "origin containment means balanced wrench cone")
    return {"wrench_count": len(x)}


def _plot_closure(ax: Any, title: str) -> dict[str, Any]:
    pts = np.array([[1, 0], [0.2, 0.9], [-0.9, 0.45], [-0.7, -0.7], [0.55, -0.85]])
    ax.fill(pts[:, 0], pts[:, 1], color="#dbeafe", edgecolor=PALETTE["blue"], alpha=0.75)
    ax.scatter([0], [0], color=PALETTE["red"], s=70)
    ax.text(0.08, 0.06, "origin", fontsize=9)
    _style(ax, title, equal=True)
    return {"origin_inside_demo": True}


def _plot_constraint(ax: Any, title: str) -> dict[str, Any]:
    x = np.linspace(-1.5, 1.5, 16)
    y = np.linspace(-1.0, 1.0, 12)
    X, Y = np.meshgrid(x, y)
    U = np.ones_like(X)
    V = 0.4 * np.sin(2 * X)
    ax.quiver(X, Y, U, V, color=PALETTE["teal"], alpha=0.75)
    ax.axhline(0, color=PALETTE["red"], lw=2, label="constraint surface")
    ax.legend(fontsize=8)
    _style(ax, title)
    return {"field_samples": int(X.size)}


def _plot_internal(ax: Any, title: str) -> dict[str, Any]:
    ax.add_patch(plt.Circle((0, 0), 0.55, fill=False, color=PALETTE["ink"], lw=2))
    ax.arrow(-1.0, 0, 0.42, 0, head_width=0.06, color=PALETTE["red"])
    ax.arrow(1.0, 0, -0.42, 0, head_width=0.06, color=PALETTE["red"])
    ax.arrow(0, -0.8, 0, 0.35, head_width=0.06, color=PALETTE["blue"])
    ax.text(-0.45, 0.67, "squeeze: null(G)", fontsize=9)
    _style(ax, title, equal=True)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.1, 1.1)
    return {"internal_dimension": 1}


def _plot_tendon(ax: Any, title: str) -> dict[str, Any]:
    q = np.linspace(0, 2, 120)
    ax.plot(q, 0.4 + 0.25 * q, color=PALETTE["blue"], label="tendon A")
    ax.plot(q, 1.0 - 0.35 * q + 0.05 * q**2, color=PALETTE["teal"], label="tendon B")
    ax.fill_between(q, 0, np.maximum(0, 0.4 + 0.25 * q), color="#dbeafe", alpha=0.35)
    ax.set_xlabel("joint coordinate")
    ax.set_ylabel("length / tension model")
    ax.legend(fontsize=8)
    _style(ax, title)
    return {"pull_only": True}


def _plot_distribution(ax: Any, title: str) -> dict[str, Any]:
    x = np.linspace(-1.8, 1.8, 18)
    y = np.linspace(-1.4, 1.4, 14)
    X, Y = np.meshgrid(x, y)
    U = np.cos(Y)
    V = np.sin(X)
    ax.quiver(X, Y, U, V, color=PALETTE["blue"], pivot="mid", scale=30)
    ax.contour(X, Y, X * Y, levels=[-1, 0, 1], colors=[PALETTE["gray"], PALETTE["red"], PALETTE["gray"]])
    _style(ax, title)
    return {"rank": 2}


def _plot_bracket(ax: Any, title: str) -> dict[str, Any]:
    path = np.array([[0, 0], [1, 0], [1, 1], [0.12, 1.08], [0.12, 0.08]])
    ax.plot(path[:, 0], path[:, 1], "o-", color=PALETTE["blue"], lw=2)
    ax.arrow(0, 0, 0.25, 0, head_width=0.04, color=PALETTE["red"])
    ax.text(0.22, 0.18, "loop defect", fontsize=9)
    _style(ax, title, equal=True)
    return {"drift_order": 2}


def _plot_growth(ax: Any, title: str) -> dict[str, Any]:
    systems = ["car", "disk", "finger", "hopper"]
    ranks = np.array([[2, 3, 4], [2, 3, 4], [2, 3, 5], [2, 3, 3]])
    for i, row in enumerate(ranks):
        ax.plot([1, 2, 3], row, "o-", label=systems[i])
    ax.set_xlabel("bracket depth")
    ax.set_ylabel("span rank")
    ax.legend(fontsize=8)
    _style(ax, title)
    return {"system_count": len(systems)}


def _plot_steering(ax: Any, title: str) -> dict[str, Any]:
    t = np.linspace(0, 2 * np.pi, 320)
    x = np.cos(t)
    y = np.sin(t)
    ax.plot(x, y, color=PALETTE["blue"], lw=2)
    ax.fill(x, y, color="#dbeafe", alpha=0.5)
    ax.text(-0.45, 0, "signed area -> z", fontsize=10)
    _style(ax, title, equal=True)
    return {"signed_area": float(np.pi)}


def _plot_chained(ax: Any, title: str) -> dict[str, Any]:
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(t, np.sin(t), label="u1", color=PALETTE["blue"])
    ax.plot(t, np.sin(2 * t), label="u2", color=PALETTE["teal"])
    ax.plot(t, np.sin(3 * t), label="higher harmonic", color=PALETTE["gold"])
    ax.legend(fontsize=8)
    ax.set_xlabel("time")
    _style(ax, title)
    return {"harmonics": 3}


def _plot_scale(ax: Any, title: str) -> dict[str, Any]:
    s = np.logspace(-6, 0, 100)
    ax.loglog(s, s**2, label="surface", color=PALETTE["blue"])
    ax.loglog(s, s**3, label="volume", color=PALETTE["teal"])
    ax.loglog(s, 1 / s, label="surface/volume", color=PALETTE["red"])
    ax.legend(fontsize=8)
    ax.set_xlabel("length scale")
    _style(ax, title)
    return {"monotone_surface_volume": True}


def _plot_latency(ax: Any, title: str) -> dict[str, Any]:
    t = np.linspace(0, 8, 400)
    for delay, color in [(0.0, PALETTE["blue"]), (0.4, PALETTE["gold"]), (0.9, PALETTE["red"])]:
        response = np.exp(-0.32 * t) * np.cos((1.4 + delay) * t - delay)
        ax.plot(t, response, label=f"delay {delay}", color=color)
    ax.legend(fontsize=8)
    _style(ax, title)
    return {"delay_cases": 3}


def _plot_surgery(ax: Any, title: str) -> dict[str, Any]:
    ax.plot([0, 0], [-1.0, 1.0], color=PALETTE["ink"], lw=2)
    ax.scatter([0], [0], color=PALETTE["red"], s=70, label="port")
    ax.plot([-0.8, 0, 0.65], [0.75, 0, -0.9], "o-", color=PALETTE["blue"], lw=2)
    ax.arrow(-0.8, 0.75, 0.25, 0.05, head_width=0.04, color=PALETTE["teal"])
    ax.arrow(0.65, -0.9, -0.18, -0.04, head_width=0.04, color=PALETTE["gold"])
    ax.legend(fontsize=8)
    _style(ax, title, equal=True)
    return {"remote_center": True}


def _plot_lie(ax: Any, title: str) -> dict[str, Any]:
    u = np.linspace(-2, 2, 14)
    v = np.linspace(-1.2, 1.2, 10)
    for uu in u:
        ax.plot([uu] * len(v), v + 0.12 * np.sin(uu), color="#d7dde5", lw=0.8)
    for vv in v:
        ax.plot(u, vv + 0.12 * np.sin(u), color="#d7dde5", lw=0.8)
    ax.arrow(-0.3, 0.1, 0.75, 0.35, head_width=0.06, color=PALETTE["blue"])
    ax.arrow(0.2, -0.25, -0.35, 0.55, head_width=0.06, color=PALETTE["red"])
    _style(ax, title, equal=True)
    _note(ax, "charts carry tangent and cotangent data")
    return {"chart_count": 2}


def _plot_adjoint(ax: Any, title: str) -> dict[str, Any]:
    labels = ["frame A", "twist", "wrench", "frame B", "same power"]
    edges = [("frame A", "twist"), ("frame A", "wrench"), ("twist", "frame B"), ("wrench", "frame B"), ("frame B", "same power")]
    _plot_network(ax, labels, edges, title)
    return {"power_invariant": True}


def _plot_api(ax: Any, title: str) -> dict[str, Any]:
    ax.axis("off")
    rows = [
        ("AxisToSkew", "hat_so3"),
        ("RigidOrientation", "so3_exp"),
        ("RPToHomogeneous", "SE(3) matrix"),
        ("TwistExp", "se3_exp"),
        ("RobotLinks", "SerialRobot"),
    ]
    for i, (old, new) in enumerate(rows):
        y = 1 - i * 0.18
        ax.text(0.08, y, old, fontsize=10, color=PALETTE["blue"])
        ax.arrow(0.38, y + 0.015, 0.18, 0, head_width=0.015, color=PALETTE["gray"])
        ax.text(0.62, y, new, fontsize=10, color=PALETTE["teal"])
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    return {"mapping_count": len(rows)}


PLOTTERS = {
    "timeline": _plot_timeline,
    "taxonomy": _plot_taxonomy,
    "dependency": _plot_dependency,
    "frames": _plot_frames,
    "screw": _plot_screw,
    "wrench": _plot_wrench,
    "manipulator": _plot_manipulator,
    "workspace": _plot_workspace,
    "singularity": _plot_singularity,
    "dynamics": _plot_dynamics,
    "phase": _plot_phase,
    "geometric_phase": _plot_geometric_phase,
    "control": _plot_control,
    "cone": _plot_cone,
    "grasp": _plot_grasp,
    "closure": _plot_closure,
    "constraint": _plot_constraint,
    "internal": _plot_internal,
    "tendon": _plot_tendon,
    "distribution": _plot_distribution,
    "bracket": _plot_bracket,
    "growth": _plot_growth,
    "steering": _plot_steering,
    "chained": _plot_chained,
    "scale": _plot_scale,
    "latency": _plot_latency,
    "surgery": _plot_surgery,
    "lie": _plot_lie,
    "adjoint": _plot_adjoint,
    "api": _plot_api,
}


def build_visual(spec: dict[str, Any], artifact_root: Path, topic: str) -> dict[str, Any]:
    path = artifact_path(topic, "figures", spec["filename"], root=artifact_root)
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    plotter = PLOTTERS.get(spec.get("kind", ""), _plot_dependency)
    metrics = plotter(ax, spec["concept"])
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return {"path": path, "filename": path.name, "kind": spec.get("kind"), "concept": spec["concept"], "observation": spec.get("observation", ""), "stats": _stats(path), "metrics": metrics}


def build_storyboard(storyboard: dict[str, Any], artifact_root: Path, topic: str) -> list[dict[str, Any]]:
    results = []
    for item in storyboard["visual_sequence"]:
        results.append(build_visual(item, artifact_root, topic))
    return results


def storyboard_check_payload(storyboard: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "label": storyboard["label"],
        "artifact_topic": storyboard["artifact_topic"],
        "visual_count": len(results),
        "visuals": [
            {
                "filename": item["filename"],
                "kind": item["kind"],
                "pixel_std": item["stats"]["pixel_std"],
                "file_size": item["stats"]["file_size"],
            }
            for item in results
        ],
        "assertions": {
            "has_multiple_visuals": len(results) >= 3,
            "all_visuals_nonblank": all(item["stats"]["pixel_std"] > 1.0 for item in results),
            "all_visuals_nonempty": all(item["stats"]["file_size"] > 1000 for item in results),
        },
    }
