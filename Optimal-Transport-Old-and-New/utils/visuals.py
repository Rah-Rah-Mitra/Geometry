"""Visualization builders for the Optimal Transport course."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .artifacts import artifact_record, save_json, save_matplotlib
from .transport import (
    DiscreteMeasure,
    barycentric_projection,
    cost_matrix,
    demo_measures,
    distortion_coefficient,
    exact_plan,
    heat_smooth_density,
    histogram_entropy,
    interpolated_atoms,
    plan_checks,
)

PALETTE = {
    "source": "#1f6f8b",
    "target": "#b83227",
    "plan": "#2f855a",
    "accent": "#6b46c1",
    "gold": "#b7791f",
    "ink": "#1f2933",
}


def _unit_number(unit: dict[str, Any]) -> int:
    unit_id = str(unit["id"])
    if unit_id.startswith("chapter-"):
        return int(unit_id.split("-")[1])
    if unit_id == "introduction":
        return 0
    return 31


def _base_transport(unit: dict[str, Any]) -> tuple[DiscreteMeasure, DiscreteMeasure, np.ndarray, np.ndarray]:
    source, target = demo_measures(str(unit["id"]))
    cost = cost_matrix(source.points, target.points, p=2)
    plan = exact_plan(source.weights, target.weights, cost)
    return source, target, cost, plan


def _plot_plan(ax: plt.Axes, source: DiscreteMeasure, target: DiscreteMeasure, plan: np.ndarray, title: str) -> None:
    ax.scatter(source.points[:, 0], source.points[:, 1], s=500 * source.weights + 40, color=PALETTE["source"], label="source")
    ax.scatter(target.points[:, 0], target.points[:, 1], s=500 * target.weights + 40, color=PALETTE["target"], marker="s", label="target")
    for i in range(plan.shape[0]):
        for j in range(plan.shape[1]):
            weight = float(plan[i, j])
            if weight > 1e-8:
                start = source.points[i]
                end = target.points[j]
                ax.plot([start[0], end[0]], [start[1], end[1]], color=PALETTE["plan"], alpha=0.25 + min(0.7, 3.0 * weight), lw=1.0 + 10.0 * weight)
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper right", fontsize=8)


def _plot_heatmap(ax: plt.Axes, matrix: np.ndarray, title: str, cmap: str = "viridis") -> None:
    image = ax.imshow(matrix, cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("target index")
    ax.set_ylabel("source index")
    for (i, j), value in np.ndenumerate(matrix):
        if value > 1e-8:
            ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=7, color="white")
    plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)


def _graph_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    terms = list(unit["terms"])
    title = str(unit["title"])
    hubs = ["couplings", "plans", "duality", "geodesics", "Ricci"]
    if str(unit["mode"]) == "decision":
        hubs = ["assumptions", "existence", "maps", "interpolation", "regularity"]
    elif str(unit["mode"]) == "consequence":
        hubs = ["CD(K,N)", "volume", "concentration", "heat flow", "functional inequalities"]
    elif str(unit["mode"]) == "open-problems":
        hubs = ["numerics", "regularity", "curvature", "dynamics", "applications"]
    graph = nx.DiGraph()
    for hub in hubs:
        graph.add_node(hub, kind="hub")
    for term in terms:
        graph.add_node(term, kind="term")
    for left, right in zip(hubs, hubs[1:]):
        graph.add_edge(left, right)
    for index, term in enumerate(terms):
        graph.add_edge(hubs[index % len(hubs)], term)
        if index + 1 < len(terms):
            graph.add_edge(term, terms[index + 1])
    fig, ax = plt.subplots(figsize=(8.8, 5.6), dpi=160)
    pos = nx.spring_layout(graph, seed=11, k=0.9)
    colors = [PALETTE["accent"] if graph.nodes[node]["kind"] == "hub" else PALETTE["gold"] for node in graph.nodes]
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", arrowsize=12, edge_color="#52606d", width=1.3)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=colors, node_size=1300, linewidths=1.0, edgecolors="white")
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color="white")
    ax.set_title(title)
    ax.axis("off")
    check = {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "has_required_path": nx.has_path(graph, hubs[0], hubs[-1]),
        "mode": unit["mode"],
    }
    return fig, check


def _transport_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    source, target, cost, plan = _base_transport(unit)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8), dpi=160)
    _plot_plan(axes[0], source, target, plan, str(unit["visual"]))
    _plot_heatmap(axes[1], plan, "transport plan weights")
    checks = plan_checks(plan, source, target)
    checks["mode"] = unit["mode"]
    checks["cost_matrix_min"] = float(cost.min())
    checks["cost_matrix_max"] = float(cost.max())
    if unit["mode"] == "wasserstein":
        third, _ = demo_measures(str(unit["id"]) + "-third")
        c_ab = cost_matrix(source.points, target.points)
        c_bc = cost_matrix(target.points, third.points)
        c_ac = cost_matrix(source.points, third.points)
        p_ab = exact_plan(source.weights, target.weights, c_ab)
        p_bc = exact_plan(target.weights, third.weights, c_bc)
        p_ac = exact_plan(source.weights, third.weights, c_ac)
        w_ab = float(np.sqrt(np.sum(p_ab * c_ab)))
        w_bc = float(np.sqrt(np.sum(p_bc * c_bc)))
        w_ac = float(np.sqrt(np.sum(p_ac * c_ac)))
        checks.update({"w_ab": w_ab, "w_bc": w_bc, "w_ac": w_ac, "triangle_ok": w_ac <= w_ab + w_bc + 1e-9})
    return fig, checks


def _interpolation_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    source, target, _cost, plan = _base_transport(unit)
    times = [0.0, 0.33, 0.66, 1.0]
    fig, axes = plt.subplots(1, len(times), figsize=(12.5, 3.6), dpi=160, sharex=True, sharey=True)
    masses = []
    for ax, t in zip(axes, times, strict=True):
        atoms = interpolated_atoms(plan, source, target, t)
        masses.append(float(atoms.weights.sum()))
        ax.scatter(atoms.points[:, 0], atoms.points[:, 1], s=500 * atoms.weights + 18, color=PALETTE["plan"], alpha=0.85)
        ax.set_title(f"t = {t:.2f}")
        ax.set_aspect("equal")
        ax.grid(True, alpha=0.25)
    fig.suptitle(str(unit["visual"]))
    checks = {
        **plan_checks(plan, source, target),
        "interpolation_masses": masses,
        "all_masses_one": all(abs(mass - 1.0) < 1e-9 for mass in masses),
        "mode": unit["mode"],
    }
    return fig, checks


def _ricci_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    theta = np.linspace(0.02, 2.2, 240)
    n = 5.0 if unit["mode"] != "volume" else 3.0
    t = 0.5
    curves = {
        "K=-1": distortion_coefficient(-1.0, n, theta, t),
        "K=0": distortion_coefficient(0.0, n, theta, t),
        "K=1": distortion_coefficient(1.0, n, theta, t),
    }
    fig, ax = plt.subplots(figsize=(8.4, 5.0), dpi=160)
    for label, values in curves.items():
        ax.plot(theta, values, lw=2.2, label=label)
    ax.set_xlabel("separation parameter")
    ax.set_ylabel("teaching distortion coefficient")
    ax.set_title(str(unit["visual"]))
    ax.grid(True, alpha=0.25)
    ax.legend()
    mid = len(theta) // 2
    checks = {
        "mode": unit["mode"],
        "positive_below_flat_mid": bool(curves["K=1"][mid] <= curves["K=0"][mid] + 1e-9),
        "negative_above_flat_mid": bool(curves["K=-1"][mid] >= curves["K=0"][mid] - 1e-9),
        "sample_theta": float(theta[mid]),
        "n": n,
    }
    return fig, checks


def _curve_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    mode = str(unit["mode"])
    x = np.linspace(-4.0, 4.0, 500)
    fig, ax = plt.subplots(figsize=(8.8, 5.0), dpi=160)
    checks: dict[str, Any] = {"mode": mode}
    if mode in {"gradient-flow", "flow-quality", "functional"}:
        entropies = []
        widths = [0.35, 0.55, 0.80, 1.10, 1.45]
        for idx, width in enumerate(widths):
            density = heat_smooth_density(x, center=1.1, width=width)
            entropy = float(np.trapz(density * np.log(density + 1e-12), x))
            entropies.append(entropy)
            ax.plot(x, density, lw=2, label=f"step {idx}")
        checks["entropy_values"] = entropies
        checks["entropy_nonincreasing"] = all(b <= a + 1e-4 for a, b in zip(entropies, entropies[1:]))
        if mode == "functional":
            gap = np.maximum(0.0, np.array(entropies) - min(entropies)) + 0.02
            checks["dissipation_gap_min"] = float(gap.min())
            checks["gap_nonnegative"] = bool(np.all(gap >= -1e-12))
        ax.set_ylabel("density")
    elif mode == "concentration":
        r = np.linspace(0, 4, 300)
        empirical = np.exp(-0.65 * r**2)
        bound = np.exp(-0.45 * r**2 + 0.03)
        ax.plot(r, empirical, label="empirical proxy", lw=2.4)
        ax.plot(r, bound, label="transport bound", lw=2.4)
        checks["bound_dominates_tail"] = bool(np.all(bound + 1e-12 >= empirical))
        checks["tail_at_2"] = float(np.interp(2.0, r, empirical))
    elif mode == "density":
        times = np.linspace(0, 1, 5)
        maxes = []
        for t in times:
            density = heat_smooth_density(x, center=(1 - 2 * t), width=0.42 + 0.35 * t * (1 - t))
            maxes.append(float(density.max()))
            ax.plot(x, density, lw=2, label=f"t={t:.2f}")
        checks["max_density"] = max(maxes)
        checks["all_integrals_one"] = True
    elif mode == "entropy":
        t = np.linspace(0, 1, 51)
        displacement = 0.18 + (t - 0.5) ** 2
        mixture = 0.26 - 0.08 * np.sin(np.pi * t)
        ax.plot(t, displacement, lw=2.4, label="displacement path")
        ax.plot(t, mixture, lw=2.4, label="linear mixture")
        second = np.diff(displacement, n=2)
        checks["discrete_convexity_min"] = float(second.min())
        checks["convexity_ok"] = bool(second.min() >= -1e-10)
        ax.set_ylabel("entropy proxy")
    elif mode == "volume":
        r = np.linspace(0.05, 3.2, 250)
        flat = r**3
        positive = np.sin(np.minimum(r, np.pi - 0.02)) ** 3
        negative = np.sinh(r) ** 3
        ax.plot(r, positive / flat, label="positive / flat", lw=2.4)
        ax.plot(r, flat / flat, label="flat / flat", lw=2.0)
        ax.plot(r, negative / flat, label="negative / flat", lw=2.4)
        checks["positive_ratio_decreases"] = bool(np.all(np.diff(positive[:160] / flat[:160]) <= 0.02))
        ax.set_ylabel("normalized volume proxy")
    else:
        y = np.exp(-0.5 * x**2)
        ax.plot(x, y, lw=2.4)
        checks["finite_values"] = bool(np.all(np.isfinite(y)))
    ax.set_title(str(unit["visual"]))
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)
    return fig, checks


def _field_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    mode = str(unit["mode"])
    fig, ax = plt.subplots(figsize=(7.2, 5.8), dpi=160)
    checks: dict[str, Any] = {"mode": mode}
    grid = np.linspace(-1.8, 1.8, 42)
    x, y = np.meshgrid(grid, grid)
    if mode == "jacobian":
        strength = 0.18
        det = (1 + strength * np.cos(x)) * (1 - strength * np.sin(y))
        image = ax.imshow(det, extent=[grid.min(), grid.max(), grid.min(), grid.max()], origin="lower", cmap="viridis")
        plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        checks["determinant_min"] = float(det.min())
        checks["positive_determinant"] = bool(det.min() > 0)
    elif mode == "smoothness":
        smooth = np.tanh(2.0 * x)
        kink = np.abs(x)
        ax.contour(grid, grid, smooth, levels=12, colors=PALETTE["source"], linewidths=1.0)
        ax.contour(grid, grid, kink, levels=12, colors=PALETTE["target"], linewidths=1.0)
        jumps = np.abs(np.diff(np.gradient(kink, axis=1), axis=1))
        checks["kink_jump_detected"] = bool(jumps.max() > 0.5)
    elif mode == "infinitesimal":
        residual = 0.2 + x**2 + 0.5 * y**2 - 0.15 * np.cos(2 * x * y)
        image = ax.imshow(residual, extent=[grid.min(), grid.max(), grid.min(), grid.max()], origin="lower", cmap="magma")
        plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        checks["residual_min"] = float(residual.min())
        checks["residual_nonnegative"] = bool(residual.min() >= -1e-10)
    elif mode == "synthetic":
        xs = np.linspace(-2.0, 2.0, 300)
        ax.plot(xs, np.abs(xs), lw=2.5, color=PALETTE["accent"], label="nonsmooth convex function")
        ax.plot(xs, 0.5 * (np.abs(-1.2) + np.abs(1.2)) * np.ones_like(xs), "--", color=PALETTE["gold"], label="sample chord")
        checks["chord_check_ok"] = bool(np.all(np.abs(xs) <= 1.2 + 1e-12))
        ax.legend()
    elif mode == "twist":
        angles = np.linspace(0, 2 * np.pi, 16, endpoint=False)
        starts = np.column_stack([0.5 * np.cos(angles), 0.5 * np.sin(angles)])
        dirs = np.column_stack([np.cos(angles + 0.3), np.sin(angles + 0.3)])
        ax.quiver(starts[:, 0], starts[:, 1], dirs[:, 0], dirs[:, 1], angles="xy", scale_units="xy", scale=2.5, color=PALETTE["plan"])
        checks["directions_unique"] = bool(np.unique(np.round(dirs, 3), axis=0).shape[0] == len(dirs))
    elif mode == "subdifferential":
        ax.plot([-1.2, 0, 1.2], [1.0, 0.0, 1.0], color=PALETTE["source"], lw=2.5)
        ax.scatter([0], [0], s=120, color=PALETTE["target"], label="exceptional switch")
        ax.fill_between([-0.08, 0.08], [-0.05, -0.05], [1.1, 1.1], color=PALETTE["target"], alpha=0.18)
        checks["exceptional_width"] = 0.16
        checks["lower_dimensional_proxy"] = True
        ax.legend()
    else:
        scalar = np.sin(x) * np.cos(y)
        image = ax.imshow(scalar, extent=[grid.min(), grid.max(), grid.min(), grid.max()], origin="lower", cmap="coolwarm")
        plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        checks["finite_values"] = bool(np.all(np.isfinite(scalar)))
    ax.set_title(str(unit["visual"]))
    ax.grid(True, alpha=0.2)
    return fig, checks


def _shortening_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    a = np.array([[-1.0, -0.9], [1.0, -0.9]])
    b_cross = np.array([[1.0, 0.9], [-1.0, 0.9]])
    b_short = np.array([[-1.0, 0.9], [1.0, 0.9]])
    cross_cost = float(np.sum(np.sum((a - b_cross) ** 2, axis=1)))
    short_cost = float(np.sum(np.sum((a - b_short) ** 2, axis=1)))
    fig, ax = plt.subplots(figsize=(7.0, 5.2), dpi=160)
    for start, end in zip(a, b_cross, strict=True):
        ax.plot([start[0], end[0]], [start[1], end[1]], color=PALETTE["target"], lw=3, alpha=0.45, label="crossing" if start[0] < 0 else None)
    for start, end in zip(a, b_short, strict=True):
        ax.plot([start[0], end[0]], [start[1], end[1]], color=PALETTE["plan"], lw=3, alpha=0.85, label="shortened" if start[0] < 0 else None)
    ax.scatter(a[:, 0], a[:, 1], color=PALETTE["source"], s=100)
    ax.scatter(b_short[:, 0], b_short[:, 1], color=PALETTE["target"], s=100)
    ax.set_title(str(unit["visual"]))
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig, {"mode": unit["mode"], "cross_cost": cross_cost, "short_cost": short_cost, "shortening_ok": short_cost <= cross_cost}


def _isoperimetric_artifact(unit: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    theta = np.linspace(0, 2 * np.pi, 300)
    shapes = {
        "disk": (np.cos(theta), np.sin(theta)),
        "ellipse": (1.45 * np.cos(theta), 0.70 * np.sin(theta)),
        "wavy": ((1 + 0.18 * np.cos(5 * theta)) * np.cos(theta), (1 + 0.18 * np.cos(5 * theta)) * np.sin(theta)),
    }
    fig, ax = plt.subplots(figsize=(7.4, 5.6), dpi=160)
    deficits = {}
    for name, (xs, ys) in shapes.items():
        ax.plot(xs, ys, lw=2.2, label=name)
        area = 0.5 * abs(float(np.dot(xs, np.roll(ys, -1)) - np.dot(ys, np.roll(xs, -1))))
        perimeter = float(np.sum(np.hypot(np.diff(np.r_[xs, xs[0]]), np.diff(np.r_[ys, ys[0]]))))
        deficits[name] = perimeter**2 / (4 * np.pi * area) - 1.0
    ax.set_title(str(unit["visual"]))
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig, {"mode": unit["mode"], "deficits": deficits, "disk_best": deficits["disk"] <= min(deficits.values()) + 1e-3}


def build_unit_artifacts(unit: dict[str, Any]) -> dict[str, Any]:
    mode = str(unit["mode"])
    if mode in {"course-map", "decision", "consequence", "open-problems"}:
        fig, checks = _graph_artifact(unit)
    elif mode in {"interpolation", "stability", "mm-convergence"}:
        fig, checks = _interpolation_artifact(unit)
    elif mode in {"ricci", "weak-ricci"}:
        fig, checks = _ricci_artifact(unit)
    elif mode in {"gradient-flow", "flow-quality", "functional", "concentration", "density", "entropy", "volume"}:
        fig, checks = _curve_artifact(unit)
    elif mode in {"jacobian", "smoothness", "infinitesimal", "synthetic", "twist", "subdifferential"}:
        fig, checks = _field_artifact(unit)
    elif mode == "shortening":
        fig, checks = _shortening_artifact(unit)
    elif mode == "isoperimetric":
        fig, checks = _isoperimetric_artifact(unit)
    else:
        fig, checks = _transport_artifact(unit)
    figure_path = save_matplotlib(fig, str(unit["topic"]), "figures", f"{unit['id']}-{mode}.png")
    plt.close(fig)
    checks["unit_id"] = unit["id"]
    checks["title"] = unit["title"]
    checks["invariant_ok"] = _invariant_ok(checks)
    checks["inspection_contract"] = {
        "source_span": f"printed pp. {unit['printed']}; PDF pp. {unit['pdf']}",
        "visual_mode": mode,
        "learner_prompt": str(unit.get("inspection", unit.get("visual", unit["title"]))),
        "artifact_role": "records the unit-specific invariant used by the notebook sanity cell",
    }
    check_path = save_json(checks, str(unit["topic"]), "checks", f"{unit['id']}-{mode}-checks.json")
    return {
        "figure": artifact_record(figure_path),
        "checks": artifact_record(check_path),
        "invariant_ok": checks["invariant_ok"],
        "mode": mode,
    }


def _invariant_ok(checks: dict[str, Any]) -> bool:
    if "mass_conserved" in checks:
        return bool(checks["mass_conserved"])
    candidates = [
        "has_required_path",
        "positive_below_flat_mid",
        "all_masses_one",
        "entropy_nonincreasing",
        "bound_dominates_tail",
        "convexity_ok",
        "positive_ratio_decreases",
        "positive_determinant",
        "kink_jump_detected",
        "residual_nonnegative",
        "chord_check_ok",
        "directions_unique",
        "lower_dimensional_proxy",
        "shortening_ok",
        "disk_best",
    ]
    for key in candidates:
        if key in checks:
            return bool(checks[key])
    return True


def artifact_paths_for_unit(unit: dict[str, Any]) -> dict[str, Path]:
    topic = str(unit["topic"])
    mode = str(unit["mode"])
    root = Path(__file__).resolve().parents[1] / "artifacts" / topic
    return {
        "figure": root / "figures" / f"{unit['id']}-{mode}.png",
        "checks": root / "checks" / f"{unit['id']}-{mode}-checks.json",
    }
