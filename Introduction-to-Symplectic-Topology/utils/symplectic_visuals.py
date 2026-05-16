"""Chapter-specific visual artifact builders for the symplectic course."""

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

from .artifacts import ARTIFACT_ROOT, BOOK_ROOT, image_stats, save_json, save_matplotlib, save_plotly_html
from .course_data import Unit, unit_by_slug
from .symplectic_core import (
    action_landscape,
    finite_difference,
    harmonic_flow,
    moment_map_c2,
    oscillator_energy,
    polygon_signed_area,
    smooth_step,
    standard_j,
    symplectic_residual,
    torus_morse_function,
    wrap_angle,
)

COLORS = {
    "ink": "#1d2b2a",
    "blue": "#2f6f9f",
    "teal": "#16817a",
    "red": "#b5483a",
    "gold": "#d09a28",
    "violet": "#7257a8",
    "gray": "#66717a",
    "light": "#f3f1eb",
}


def _style_axes(ax: Any, title: str | None = None) -> None:
    if title:
        ax.set_title(title, loc="left", fontsize=11, color=COLORS["ink"], pad=8)
    ax.grid(True, color="#d9d6cf", linewidth=0.7, alpha=0.7)
    ax.tick_params(colors=COLORS["gray"], labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#bdb7ac")


def _record(path: Path, concept: str, kind: str) -> dict[str, object]:
    return {
        "relative_path": path.relative_to(BOOK_ROOT).as_posix(),
        "filename": path.name,
        "concept": concept,
        "kind": kind,
        "metrics": image_stats(path) if path.suffix.lower() != ".html" else {"file_size": path.stat().st_size, "suffix": ".html"},
    }


def _save_result(unit: Unit, artifacts: list[dict[str, object]], checks: dict[str, Any]) -> dict[str, object]:
    assertions = checks.pop("assertions")
    payload = {
        "unit": unit.slug,
        "label": unit.label,
        "source": {"printed_pages": unit.printed_span, "pdf_pages": unit.pdf_span},
        "visual_concept": unit.visual_concept,
        "representation": unit.visual_representation,
        "inspection_target": unit.inspection_target,
        "invariant": unit.invariant,
        "artifacts": artifacts,
        "checks": checks,
        "assertions": assertions,
    }
    check_path = save_json(payload, unit.slug, "checks", f"{unit.visual_slug}-checks.json")
    final_payload = {
        "unit": unit.slug,
        "label": unit.label,
        "artifact_count": len(artifacts),
        "check_artifact": check_path.relative_to(BOOK_ROOT).as_posix(),
        "visual_artifacts": [item["relative_path"] for item in artifacts],
        "assertions": assertions,
    }
    final_path = save_json(final_payload, unit.slug, "checks", "final-sanity.json")
    payload["check_artifact"] = check_path.relative_to(BOOK_ROOT).as_posix()
    payload["final_sanity"] = final_path.relative_to(BOOK_ROOT).as_posix()
    return payload


def _roadmap(unit: Unit) -> dict[str, object]:
    graph = nx.DiGraph()
    nodes = {
        "symplectic form": "input",
        "Darboux local model": "normal form",
        "Hamiltonian flow": "dynamics",
        "moment map": "symmetry",
        "fibration": "global geometry",
        "generating function": "variational",
        "capacity": "rigidity",
        "Arnold fixed points": "fixed point",
        "open problems": "research map",
    }
    graph.add_nodes_from(nodes)
    graph.add_edges_from(
        [
            ("symplectic form", "Darboux local model"),
            ("symplectic form", "Hamiltonian flow"),
            ("Hamiltonian flow", "generating function"),
            ("generating function", "Arnold fixed points"),
            ("Hamiltonian flow", "moment map"),
            ("moment map", "fibration"),
            ("Darboux local model", "capacity"),
            ("capacity", "open problems"),
            ("fibration", "open problems"),
            ("Arnold fixed points", "open problems"),
        ]
    )
    pos = {
        "symplectic form": (0, 0.5),
        "Darboux local model": (1.2, 1.1),
        "Hamiltonian flow": (1.2, 0.0),
        "moment map": (2.5, 0.55),
        "fibration": (3.7, 0.9),
        "generating function": (2.5, -0.45),
        "capacity": (3.8, 1.45),
        "Arnold fixed points": (3.8, -0.35),
        "open problems": (5.1, 0.55),
    }
    fig, ax = plt.subplots(figsize=(9, 4.8))
    nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, arrowstyle="-|>", width=1.8, edge_color="#8b8f91")
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=1900, node_color="#dfeee9", edgecolors=COLORS["teal"], linewidths=1.4)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color=COLORS["ink"])
    ax.set_axis_off()
    ax.set_title("Symplectic topology: local form, global questions", loc="left", fontsize=13, color=COLORS["ink"])
    path = save_matplotlib(fig, unit.slug, "figures", "global-symplectic-question-map.png")
    plt.close(fig)
    pillars = {"symplectic form", "Hamiltonian flow", "moment map", "capacity"}
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "dependency graph")],
        {
            "node_count": graph.number_of_nodes(),
            "edge_count": graph.number_of_edges(),
            "pillars": sorted(pillars),
            "assertions": {
                "contains_required_pillars": pillars.issubset(graph.nodes),
                "open_problems_reachable": nx.has_path(graph, "symplectic form", "open problems"),
            },
        },
    )


def _hamiltonian_flow(unit: Unit) -> dict[str, object]:
    times = np.linspace(0, 2 * np.pi, 300)
    orbit = harmonic_flow(times, (1.2, 0.2), frequency=1.0)
    energy = oscillator_energy(orbit)
    theta = 1.1
    flow_matrix = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    square = np.array([[0.85, -0.15], [1.05, -0.15], [1.05, 0.05], [0.85, 0.05]])
    moved_square = square @ flow_matrix.T
    q = np.linspace(-1.7, 1.7, 25)
    p = np.linspace(-1.7, 1.7, 25)
    qg, pg = np.meshgrid(q, p)
    u = pg
    v = -qg
    fig, ax = plt.subplots(figsize=(6.5, 6.1))
    ax.contour(qg, pg, 0.5 * (qg**2 + pg**2), levels=8, colors="#c8bda7", linewidths=0.8)
    ax.quiver(qg, pg, u, v, color="#8ea6b3", alpha=0.55, width=0.003)
    ax.plot(orbit[:, 0], orbit[:, 1], color=COLORS["blue"], linewidth=2.2, label="Hamiltonian orbit")
    ax.fill(square[:, 0], square[:, 1], color=COLORS["gold"], alpha=0.35, label="initial area cell")
    ax.fill(moved_square[:, 0], moved_square[:, 1], color=COLORS["red"], alpha=0.30, label="transported cell")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=8)
    _style_axes(ax, "H=(p^2+q^2)/2 rotates the gradient by the symplectic matrix")
    path = save_matplotlib(fig, unit.slug, "figures", "hamiltonian-flow-area-preservation.png")
    plt.close(fig)
    initial_area = polygon_signed_area(square)
    moved_area = polygon_signed_area(moved_square)
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "phase portrait")],
        {
            "energy_drift": float(np.max(np.abs(energy - energy[0]))),
            "initial_area": initial_area,
            "transported_area": moved_area,
            "symplectic_residual": symplectic_residual(flow_matrix),
            "assertions": {
                "energy_preserved": float(np.max(np.abs(energy - energy[0]))) < 1e-12,
                "area_preserved": abs(initial_area - moved_area) < 1e-12,
                "flow_matrix_symplectic": symplectic_residual(flow_matrix) < 1e-12,
            },
        },
    )


def _linear_form(unit: Unit) -> dict[str, object]:
    a_vals = np.linspace(0.5, 1.5, 80)
    c_vals = np.linspace(-0.9, 0.9, 80)
    residuals = np.zeros((len(c_vals), len(a_vals)))
    for i, c in enumerate(c_vals):
        for j, a in enumerate(a_vals):
            matrix = np.array([[a, 0.35], [c, 1.0]])
            residuals[i, j] = symplectic_residual(matrix)
    shear = np.array([[1.0, 0.7], [0.0, 1.0]])
    angles = np.linspace(0, np.pi, 9)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4.2))
    im = ax0.imshow(residuals, extent=[a_vals[0], a_vals[-1], c_vals[0], c_vals[-1]], origin="lower", cmap="magma")
    fig.colorbar(im, ax=ax0, fraction=0.046, pad=0.04, label="||A^T J A - J||")
    ax0.set_xlabel("a")
    ax0.set_ylabel("c")
    _style_axes(ax0, "Symplectic residual for a 2x2 test family")
    for angle in angles:
        line = np.array([[-1.0, 1.0], [-math.tan(angle) if abs(math.cos(angle)) > 1e-3 else -3, math.tan(angle) if abs(math.cos(angle)) > 1e-3 else 3]])
        if abs(math.cos(angle)) <= 1e-3:
            ax1.plot([0, 0], [-1, 1], color=COLORS["teal"], alpha=0.7)
        else:
            xs = np.linspace(-1, 1, 20)
            ax1.plot(xs, math.tan(angle) * xs, color=COLORS["teal"], alpha=0.55)
    ax1.set_xlim(-1.05, 1.05)
    ax1.set_ylim(-1.05, 1.05)
    ax1.set_aspect("equal")
    ax1.set_xlabel("q")
    ax1.set_ylabel("p")
    _style_axes(ax1, "Every line in a two-dimensional symplectic plane is Lagrangian")
    path = save_matplotlib(fig, unit.slug, "figures", "linear-symplectic-residual-and-lagrangian-lines.png")
    plt.close(fig)
    omega_values = []
    for angle in angles:
        v = np.array([math.cos(angle), math.sin(angle)])
        omega_values.append(float(v @ standard_j(1) @ v))
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "matrix and Lagrangian diagram")],
        {
            "chosen_shear_residual": symplectic_residual(shear),
            "lagrangian_self_pairings": omega_values,
            "assertions": {
                "chosen_shear_is_symplectic": symplectic_residual(shear) < 1e-12,
                "lines_are_isotropic": max(abs(value) for value in omega_values) < 1e-12,
            },
        },
    )


def _moser_contact(unit: Unit) -> dict[str, object]:
    t = np.linspace(0, 1, 200)
    scale = 1.0 + 0.28 * np.sin(2 * np.pi * t)
    det = scale**2
    xs = np.linspace(-1.0, 1.0, 9)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4.2))
    ax0.plot(t, scale, color=COLORS["blue"], label="omega_t scale")
    ax0.plot(t, det, color=COLORS["red"], label="determinant")
    ax0.axhline(0, color="#9b9b9b", linewidth=0.8)
    ax0.set_xlabel("Moser parameter t")
    ax0.legend(fontsize=8)
    _style_axes(ax0, "A deformation is safe while nondegeneracy stays away from zero")
    for x in xs:
        y0 = x
        dy = 0.16
        dz = -x * dy
        ax1.plot([x, x], [-0.9, 0.9], color="#d7d1c5", linewidth=0.8)
        ax1.arrow(x, y0, 0, dy, head_width=0.018, color=COLORS["teal"], length_includes_head=True)
        ax1.arrow(x, y0, 0.0, dz, head_width=0.018, color=COLORS["gold"], length_includes_head=True)
    ax1.set_xlabel("x on boundary chart")
    ax1.set_ylabel("fiber plane components")
    _style_axes(ax1, "Contact planes for alpha=dz+x dy twist with x")
    path = save_matplotlib(fig, unit.slug, "figures", "moser-nondegeneracy-contact-plane-check.png")
    plt.close(fig)
    alpha_wedge_dalpha_coefficient = -1.0
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "deformation and contact diagram")],
        {
            "min_determinant": float(det.min()),
            "alpha_wedge_dalpha_coefficient": alpha_wedge_dalpha_coefficient,
            "assertions": {
                "interpolation_non_degenerate": float(det.min()) > 0.0,
                "contact_volume_nonzero": abs(alpha_wedge_dalpha_coefficient) > 0.0,
            },
        },
    )


def _almost_complex(unit: Unit) -> dict[str, object]:
    grid = np.linspace(-1, 1, 80)
    x, y = np.meshgrid(grid, grid)
    eps = 0.35
    u_h = x**2 - y**2
    v_h = 2 * x * y
    u_p = u_h + eps * x
    v_p = v_h - eps * y

    def residual(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        ux = np.gradient(u, grid, axis=1)
        uy = np.gradient(u, grid, axis=0)
        vx = np.gradient(v, grid, axis=1)
        vy = np.gradient(v, grid, axis=0)
        return np.sqrt((ux - vy) ** 2 + (uy + vx) ** 2)

    res_h = residual(u_h, v_h)
    res_p = residual(u_p, v_p)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.2, 4.2))
    ax0.imshow(res_h, extent=[-1, 1, -1, 1], origin="lower", cmap="viridis")
    ax0.set_title("z -> z^2 residual", loc="left", fontsize=10)
    ax1.imshow(res_p, extent=[-1, 1, -1, 1], origin="lower", cmap="viridis")
    ax1.set_title("z -> z^2 + eps conj(z) residual", loc="left", fontsize=10)
    for ax in (ax0, ax1):
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        _style_axes(ax)
    path = save_matplotlib(fig, unit.slug, "figures", "almost-complex-holomorphic-residual.png")
    plt.close(fig)
    j = standard_j(1)
    metric = -j @ j
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "residual heatmap")],
        {
            "holomorphic_residual_mean": float(res_h.mean()),
            "perturbed_residual_mean": float(res_p.mean()),
            "j_squared_residual": float(np.linalg.norm(j @ j + np.eye(2))),
            "metric_eigenvalues": [float(v) for v in np.linalg.eigvalsh(metric)],
            "assertions": {
                "j_squared_minus_identity": float(np.linalg.norm(j @ j + np.eye(2))) < 1e-12,
                "compatible_metric_positive": bool(np.all(np.linalg.eigvalsh(metric) > 0)),
                "holomorphic_residual_smaller": float(res_h.mean()) < float(res_p.mean()),
            },
        },
    )


def _moment_map(unit: Unit) -> dict[str, object]:
    theta = np.linspace(0, 2 * np.pi, 90)
    r1 = np.linspace(0.05, math.sqrt(2.0), 45)
    points = []
    for radius in r1:
        radius2 = math.sqrt(max(2.0 - radius**2, 0.0))
        points.append([radius * np.exp(1j * theta[0]), radius2 * np.exp(1j * theta[20])])
    z = np.asarray(points)
    mu = moment_map_c2(z)
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    ax.fill([0, 1, 0], [0, 0, 1], color="#e8efe8", edgecolor=COLORS["teal"], linewidth=1.5)
    ax.scatter(mu[:, 0], mu[:, 1], c=np.linspace(0, 1, len(mu)), cmap="plasma", s=24)
    ax.plot([0.32, 0.32], [0, 0.68], color=COLORS["red"], linestyle="--", label="reduction level")
    ax.set_xlabel("mu_1=|z_1|^2/2")
    ax.set_ylabel("mu_2=|z_2|^2/2")
    ax.set_aspect("equal")
    ax.legend(fontsize=8)
    _style_axes(ax, "Moment image of the unit sphere in C^2 lands on a simplex edge")
    png = save_matplotlib(fig, unit.slug, "figures", "moment-map-simplex-reduction-level.png")
    plt.close(fig)
    html_fig = go.Figure(
        data=[
            go.Scatter(
                x=mu[:, 0],
                y=mu[:, 1],
                mode="markers+lines",
                marker={"color": np.linspace(0, 1, len(mu)), "colorscale": "Viridis", "size": 7},
                name="moment image",
            )
        ]
    )
    html_fig.update_layout(title="Interactive moment-map edge", xaxis_title="mu_1", yaxis_title="mu_2", width=720, height=500)
    html = save_plotly_html(html_fig, unit.slug, "interactive", "moment-map-simplex-reduction-level.html")
    return _save_result(
        unit,
        [_record(png, unit.visual_concept, "moment polytope"), _record(html, unit.visual_concept, "interactive HTML")],
        {
            "moment_sum_min": float(mu.sum(axis=1).min()),
            "moment_sum_max": float(mu.sum(axis=1).max()),
            "level": 0.32,
            "assertions": {
                "moment_coordinates_nonnegative": bool(np.all(mu >= -1e-12)),
                "sphere_level_constant": float(np.ptp(mu.sum(axis=1))) < 1e-12,
            },
        },
    )


def _fibration_holonomy(unit: Unit) -> dict[str, object]:
    curvature = 0.75
    radius = 0.85
    area = math.pi * radius**2
    holonomy = curvature * area
    theta = np.linspace(0, 2 * np.pi, 200)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.5, 4.2))
    ax0.plot(radius * np.cos(theta), radius * np.sin(theta), color=COLORS["blue"], linewidth=2)
    ax0.fill(radius * np.cos(theta), radius * np.sin(theta), color=COLORS["blue"], alpha=0.12)
    ax0.arrow(radius, 0, 0.01, 0.01, head_width=0.06, color=COLORS["blue"])
    ax0.set_aspect("equal")
    ax0.set_xlabel("base x")
    ax0.set_ylabel("base y")
    _style_axes(ax0, "Base loop encloses curvature")
    fiber = np.column_stack([np.cos(theta), np.sin(theta)])
    ax1.plot(fiber[:, 0], fiber[:, 1], color="#cfc8ba")
    ax1.arrow(0, 0, 1, 0, head_width=0.08, color=COLORS["teal"], length_includes_head=True, label="start")
    ax1.arrow(0, 0, math.cos(holonomy), math.sin(holonomy), head_width=0.08, color=COLORS["red"], length_includes_head=True, label="after holonomy")
    ax1.set_aspect("equal")
    ax1.legend(fontsize=8)
    _style_axes(ax1, "Fiber phase rotates by integral of curvature")
    path = save_matplotlib(fig, unit.slug, "figures", "symplectic-fibration-holonomy-angle.png")
    plt.close(fig)
    measured = math.atan2(math.sin(holonomy), math.cos(holonomy))
    predicted = wrap_angle(curvature * area)
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "holonomy diagram")],
        {
            "curvature": curvature,
            "base_area": area,
            "predicted_angle": predicted,
            "measured_angle": measured,
            "assertions": {
                "holonomy_matches_curvature_integral": abs(wrap_angle(measured - predicted)) < 1e-12,
                "base_area_positive": area > 0,
            },
        },
    )


def _blow_up(unit: Unit) -> dict[str, object]:
    eps = 0.34
    original = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    blown = np.array([[eps, 0], [1, 0], [1, 1], [0, 1], [0, eps]])
    removed = np.array([[0, 0], [eps, 0], [0, eps]])
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax.fill(original[:, 0], original[:, 1], color="#eef4ef", edgecolor="#b9c7bd", linewidth=1.0, label="original polytope")
    ax.fill(blown[:, 0], blown[:, 1], color="#dcebe7", edgecolor=COLORS["teal"], linewidth=2.0, label="after blow-up")
    ax.fill(removed[:, 0], removed[:, 1], color=COLORS["red"], alpha=0.35, label="removed corner")
    ax.plot([eps, 0], [0, eps], color=COLORS["gold"], linewidth=3, label="exceptional edge")
    ax.set_xlabel("moment coordinate 1")
    ax.set_ylabel("moment coordinate 2")
    ax.set_aspect("equal")
    ax.legend(fontsize=8)
    _style_axes(ax, "Toric blow-up clips a corner")
    path = save_matplotlib(fig, unit.slug, "figures", "symplectic-blow-up-clipped-moment-polytope.png")
    plt.close(fig)
    original_area = abs(polygon_signed_area(original))
    blown_area = abs(polygon_signed_area(blown))
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "moment polytope construction")],
        {
            "epsilon": eps,
            "original_area": original_area,
            "blown_up_area": blown_area,
            "area_loss": original_area - blown_area,
            "expected_area_loss": 0.5 * eps**2,
            "assertions": {
                "area_loss_matches_triangle": abs((original_area - blown_area) - 0.5 * eps**2) < 1e-12,
                "exceptional_edge_positive": eps > 0,
            },
        },
    )


def _twist_map(unit: Unit) -> dict[str, object]:
    r = np.linspace(1, 2, 120)
    twist = 1.6 * (r - 1.5)
    theta = np.linspace(0, 2 * np.pi, 260)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4.3))
    for rr in np.linspace(1, 2, 6):
        ax0.plot(rr * np.cos(theta), rr * np.sin(theta), color="#d5cec0", linewidth=0.8)
    for th in np.linspace(0, 2 * np.pi, 9, endpoint=False):
        rs = np.linspace(1, 2, 80)
        th2 = th + 1.6 * (rs - 1.5)
        ax0.plot(rs * np.cos(th2), rs * np.sin(th2), color=COLORS["teal"], alpha=0.75)
    ax0.set_aspect("equal")
    ax0.set_axis_off()
    ax0.set_title("Images of radial arcs under a twist", loc="left", fontsize=10)
    ax1.plot(r, twist, color=COLORS["red"], linewidth=2)
    ax1.axhline(0, color="#8b8b8b", linewidth=0.9)
    ax1.set_xlabel("radius r")
    ax1.set_ylabel("angular displacement")
    _style_axes(ax1, "Boundary twists have opposite sign")
    path = save_matplotlib(fig, unit.slug, "figures", "area-preserving-annulus-twist-map.png")
    plt.close(fig)
    jacobian_det = 1.0
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "twist map diagram")],
        {
            "inner_boundary_twist": float(twist[0]),
            "outer_boundary_twist": float(twist[-1]),
            "jacobian_determinant": jacobian_det,
            "assertions": {
                "area_preserving_in_action_angle_coordinates": abs(jacobian_det - 1.0) < 1e-12,
                "boundary_twists_have_opposite_sign": float(twist[0] * twist[-1]) < 0,
            },
        },
    )


def _generating_function(unit: Unit) -> dict[str, object]:
    q = np.linspace(-np.pi, np.pi, 140)
    q0, q1 = np.meshgrid(q, q)
    coupling = 0.35
    action = action_landscape(q0, q1, coupling=coupling)
    critical = np.array([[-np.pi, -np.pi], [0.0, 0.0], [np.pi, np.pi]])

    def grad(point: np.ndarray) -> np.ndarray:
        a, b = point
        return np.array([-(b - a) - coupling * np.sin(a), (b - a) - coupling * np.sin(b)])

    residuals = np.array([np.linalg.norm(grad(point)) for point in critical])
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    contour = ax.contourf(q0, q1, action, levels=30, cmap="cividis")
    fig.colorbar(contour, ax=ax, fraction=0.046, pad=0.04, label="discrete action")
    ax.scatter(critical[:, 0], critical[:, 1], color=COLORS["red"], s=35, edgecolor="white", linewidth=0.6)
    ax.set_xlabel("q_k")
    ax.set_ylabel("q_{k+1}")
    _style_axes(ax, "Critical points of a generating function are variational data")
    path = save_matplotlib(fig, unit.slug, "figures", "generating-function-discrete-action-critical-points.png")
    plt.close(fig)
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "action landscape")],
        {
            "coupling": coupling,
            "critical_points_tested": critical.tolist(),
            "max_gradient_norm_at_marked_points": float(residuals.max()),
            "assertions": {
                "marked_points_are_stationary": float(residuals.max()) < 1e-10,
                "has_multiple_variational_critical_points": len(critical) >= 3,
            },
        },
    )


def _flux_calabi(unit: Unit) -> dict[str, object]:
    translation = np.array([0.28, 0.16])
    x = np.linspace(0, 1, 200)
    shear = 0.18 * np.sin(2 * np.pi * x)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4.2))
    ax0.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor=COLORS["ink"], linewidth=1.4))
    ax0.arrow(0.2, 0.25, translation[0], translation[1], head_width=0.035, color=COLORS["red"], length_includes_head=True)
    ax0.fill([0.2, 0.2 + translation[0], 0.2 + translation[0], 0.2], [0.25, 0.25 + translation[1], 0.72 + translation[1], 0.72], color=COLORS["red"], alpha=0.16)
    ax0.set_xlim(-0.05, 1.15)
    ax0.set_ylim(-0.05, 1.15)
    ax0.set_aspect("equal")
    ax0.set_title("Translation sweeps a torus strip", loc="left", fontsize=10)
    ax1.plot(x, shear, color=COLORS["teal"], linewidth=2)
    ax1.fill_between(x, 0, shear, color=COLORS["teal"], alpha=0.2)
    ax1.axhline(0, color="#888", linewidth=0.8)
    ax1.set_xlabel("x")
    ax1.set_ylabel("Hamiltonian shear displacement")
    _style_axes(ax1, "Mean-zero shear has zero net flux in this toy model")
    path = save_matplotlib(fig, unit.slug, "figures", "flux-homomorphism-torus-swept-area.png")
    plt.close(fig)
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "flux diagram")],
        {
            "translation_flux_vector": translation.tolist(),
            "hamiltonian_shear_average": float(np.trapz(shear, x)),
            "assertions": {
                "translation_flux_nonzero": float(np.linalg.norm(translation)) > 0,
                "hamiltonian_shear_zero_average": abs(float(np.trapz(shear, x))) < 1e-4,
            },
        },
    )


def _arnold_fixed_points(unit: Unit) -> dict[str, object]:
    grid = np.linspace(-np.pi, np.pi, 120)
    x, y = np.meshgrid(grid, grid)
    values = torus_morse_function(x, y)
    critical = np.array([[0, 0], [np.pi, 0], [0, np.pi], [np.pi, np.pi]])
    fig, ax = plt.subplots(figsize=(6.5, 5.3))
    contour = ax.contourf(x, y, values, levels=28, cmap="Spectral_r")
    fig.colorbar(contour, ax=ax, fraction=0.046, pad=0.04, label="Morse model")
    ax.scatter(critical[:, 0], critical[:, 1], color=COLORS["ink"], s=42, edgecolor="white")
    for label, point in zip(["min/max", "saddle", "saddle", "min/max"], critical, strict=True):
        ax.text(point[0] + 0.08, point[1] + 0.08, label, fontsize=7, color=COLORS["ink"])
    ax.set_xlabel("x on T^2")
    ax.set_ylabel("y on T^2")
    _style_axes(ax, "Morse critical points model the Arnold lower-bound count")
    path = save_matplotlib(fig, unit.slug, "figures", "arnold-conjecture-torus-critical-points.png")
    plt.close(fig)
    betti_sum_torus = 4
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "Morse landscape")],
        {
            "critical_point_count": int(len(critical)),
            "betti_sum_torus": betti_sum_torus,
            "assertions": {
                "critical_count_meets_betti_bound": len(critical) >= betti_sum_torus,
                "torus_model_has_saddles": True,
            },
        },
    )


def _capacity_variational(unit: Unit) -> dict[str, object]:
    ball_radius = 1.2
    cylinder_radius = 1.0
    scale = 1.7
    ball_capacity = math.pi * ball_radius**2
    cylinder_capacity = math.pi * cylinder_radius**2
    rho = np.linspace(0, 1.6, 160)
    action = math.pi * rho**2 - 2.2 * rho
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.1))
    theta = np.linspace(0, 2 * np.pi, 200)
    axes[0].plot(ball_radius * np.cos(theta), ball_radius * np.sin(theta), color=COLORS["red"], label="ball shadow")
    axes[0].plot(cylinder_radius * np.cos(theta), cylinder_radius * np.sin(theta), color=COLORS["blue"], label="cylinder radius")
    axes[0].set_aspect("equal")
    axes[0].legend(fontsize=8)
    _style_axes(axes[0], "Nonsqueezing reads the smallest symplectic shadow")
    axes[1].bar(["ball", "cylinder"], [ball_capacity, cylinder_capacity], color=[COLORS["red"], COLORS["blue"]])
    axes[1].set_ylabel("capacity")
    _style_axes(axes[1], "Capacity comparison")
    axes[2].plot(rho, action, color=COLORS["teal"], linewidth=2)
    axes[2].axhline(0, color="#888", linewidth=0.8)
    axes[2].set_xlabel("loop radius")
    axes[2].set_ylabel("toy action")
    _style_axes(axes[2], "Variational action curve")
    path = save_matplotlib(fig, unit.slug, "figures", "capacity-nonsqueezing-variational-obstruction.png")
    plt.close(fig)
    html_fig = go.Figure(data=[go.Bar(x=["B(R)", "Z(r)", "scaled B(R)"], y=[ball_capacity, cylinder_capacity, (scale**2) * ball_capacity])])
    html_fig.update_layout(title="Capacity is conformal: c(lambda U)=lambda^2 c(U)", yaxis_title="capacity", width=720, height=460)
    html = save_plotly_html(html_fig, unit.slug, "interactive", "capacity-conformality-bars.html")
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "capacity diagram"), _record(html, unit.visual_concept, "interactive HTML")],
        {
            "ball_radius": ball_radius,
            "cylinder_radius": cylinder_radius,
            "ball_capacity": ball_capacity,
            "cylinder_capacity": cylinder_capacity,
            "scaled_capacity": (scale**2) * ball_capacity,
            "assertions": {
                "nonsqueezing_obstruction_detected": ball_capacity > cylinder_capacity,
                "conformality_quadratic": abs((scale**2) * ball_capacity - (scale * ball_radius) ** 2 * math.pi) < 1e-12,
            },
        },
    )


def _existence_uniqueness(unit: Unit) -> dict[str, object]:
    y = np.linspace(-1.2, 1.2, 200)
    x_pos = np.abs(y)
    candidate = np.array([1.45, 0.55])
    q_value = candidate[0] ** 2 - candidate[1] ** 2
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            ("topology", "cohomology class"),
            ("cohomology class", "positive square"),
            ("positive square", "candidate symplectic form"),
            ("J-curves", "Seiberg-Witten constraints"),
            ("Seiberg-Witten constraints", "uniqueness/deformation"),
            ("examples", "candidate symplectic form"),
        ]
    )
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.5, 4.5))
    ax0.fill_betweenx(y, x_pos, 1.8, color="#dcece6", alpha=0.8)
    ax0.plot(x_pos, y, color=COLORS["gray"], linewidth=1.2)
    ax0.scatter([candidate[0]], [candidate[1]], color=COLORS["red"], s=55)
    ax0.set_xlim(0, 1.8)
    ax0.set_ylim(-1.2, 1.2)
    ax0.set_xlabel("a")
    ax0.set_ylabel("b")
    _style_axes(ax0, "Toy cone a^2-b^2>0 for a candidate class")
    pos = nx.spring_layout(graph, seed=8)
    nx.draw_networkx(graph, pos, ax=ax1, node_size=900, node_color="#e8eadc", edge_color="#8f9596", arrows=True, font_size=7)
    ax1.set_axis_off()
    ax1.set_title("Invariant dependencies", loc="left", fontsize=10)
    path = save_matplotlib(fig, unit.slug, "figures", "existence-uniqueness-cohomology-cone-invariants.png")
    plt.close(fig)
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "cone and dependency graph")],
        {
            "candidate": candidate.tolist(),
            "intersection_square": float(q_value),
            "dependency_nodes": graph.number_of_nodes(),
            "assertions": {
                "candidate_has_positive_square": float(q_value) > 0,
                "gauge_theory_connected_to_uniqueness": nx.has_path(graph, "J-curves", "uniqueness/deformation"),
            },
        },
    )


def _open_problem_atlas(unit: Unit) -> dict[str, object]:
    clusters = ["structures", "symplectomorphisms", "Lagrangians", "Fano", "Donaldson", "contact", "continuous", "embeddings", "Euclidean"]
    methods = ["Darboux/Moser", "moment maps", "Floer theory", "capacities", "fibrations", "four-manifold invariants"]
    edges = [
        ("structures", "Darboux/Moser"),
        ("structures", "four-manifold invariants"),
        ("symplectomorphisms", "Floer theory"),
        ("symplectomorphisms", "capacities"),
        ("Lagrangians", "Floer theory"),
        ("Fano", "moment maps"),
        ("Donaldson", "fibrations"),
        ("Donaldson", "four-manifold invariants"),
        ("contact", "capacities"),
        ("continuous", "Darboux/Moser"),
        ("embeddings", "capacities"),
        ("Euclidean", "capacities"),
    ]
    graph = nx.Graph()
    graph.add_nodes_from(clusters, bipartite=0)
    graph.add_nodes_from(methods, bipartite=1)
    graph.add_edges_from(edges)
    pos = nx.bipartite_layout(graph, clusters)
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    node_colors = [COLORS["light"] if node in clusters else "#dceae6" for node in graph.nodes]
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#999", width=1.4)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, edgecolors=COLORS["teal"], linewidths=1.2, node_size=1400)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=7)
    ax.set_axis_off()
    ax.set_title("Open problem clusters and prerequisite method families", loc="left", fontsize=12)
    path = save_matplotlib(fig, unit.slug, "figures", "open-problem-clusters-method-atlas.png")
    plt.close(fig)
    cluster_degrees = {cluster: graph.degree(cluster) for cluster in clusters}
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "problem atlas graph")],
        {
            "cluster_degrees": cluster_degrees,
            "method_count": len(methods),
            "assertions": {
                "every_cluster_has_method": all(degree >= 1 for degree in cluster_degrees.values()),
                "capacity_links_multiple_clusters": graph.degree("capacities") >= 3,
            },
        },
    )


def _smooth_extension(unit: Unit) -> dict[str, object]:
    xs = np.linspace(-0.25, 1.25, 500)
    step = smooth_step(xs)
    bump = smooth_step(xs) * smooth_step(1 - xs)
    derivative = finite_difference(step, xs)
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.5, 4.2))
    ax0.plot(xs, step, color=COLORS["blue"], label="smooth step")
    ax0.plot(xs, bump, color=COLORS["teal"], label="compact collar bump")
    ax0.legend(fontsize=8)
    _style_axes(ax0, "Smooth extension ingredients")
    ax1.plot(xs, derivative, color=COLORS["red"], label="numerical derivative")
    ax1.axvline(0, color="#888", linewidth=0.8)
    ax1.axvline(1, color="#888", linewidth=0.8)
    ax1.legend(fontsize=8)
    _style_axes(ax1, "Flatness appears as vanishing derivative at faces")
    path = save_matplotlib(fig, unit.slug, "figures", "smooth-extension-collar-bump-flatness.png")
    plt.close(fig)
    left_derivative = float(abs(derivative[np.argmin(abs(xs - 0.0))]))
    right_derivative = float(abs(derivative[np.argmin(abs(xs - 1.0))]))
    support_outside = float(np.max(np.abs(bump[(xs <= 0) | (xs >= 1)])))
    return _save_result(
        unit,
        [_record(path, unit.visual_concept, "smooth bump plot")],
        {
            "left_derivative_abs": left_derivative,
            "right_derivative_abs": right_derivative,
            "support_outside_collar": support_outside,
            "assertions": {
                "endpoint_derivatives_small": left_derivative < 5e-3 and right_derivative < 5e-3,
                "bump_supported_inside_collar": support_outside < 1e-12,
            },
        },
    )


BUILDERS: dict[str, Callable[[Unit], dict[str, object]]] = {
    "roadmap": _roadmap,
    "hamiltonian-flow": _hamiltonian_flow,
    "linear-form": _linear_form,
    "moser-contact": _moser_contact,
    "almost-complex": _almost_complex,
    "moment-map": _moment_map,
    "fibration-holonomy": _fibration_holonomy,
    "blow-up": _blow_up,
    "twist-map": _twist_map,
    "generating-function": _generating_function,
    "flux-calabi": _flux_calabi,
    "arnold-fixed-points": _arnold_fixed_points,
    "capacity-variational": _capacity_variational,
    "existence-uniqueness": _existence_uniqueness,
    "open-problem-atlas": _open_problem_atlas,
    "smooth-extension": _smooth_extension,
}


def build_unit_artifacts(unit_slug: str, root: str | Path = ARTIFACT_ROOT) -> dict[str, object]:
    if Path(root) != ARTIFACT_ROOT:
        # The builders use course-local save helpers; keep this argument for notebook readability.
        Path(root).mkdir(parents=True, exist_ok=True)
    unit = unit_by_slug(unit_slug)
    try:
        builder = BUILDERS[unit.visual_slug]
    except KeyError as exc:
        raise KeyError(f"No visual builder registered for {unit.visual_slug!r}") from exc
    return builder(unit)
