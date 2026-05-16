"""Chapter-specific visual artifact builders for the Arnold course."""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go

from .artifacts import relative_to_book, save_json, save_matplotlib, save_plotly_html
from .mechanics import (
    confocal_ellipse,
    cusp_caustic,
    euler_top,
    explicit_euler_oscillator,
    fold_caustic,
    harmonic_solution,
    kdv_soliton,
    kepler_orbit,
    mathieu_tongue,
    pendulum_energy,
    polygon_area,
    standard_map,
    torus_winding,
    verlet_oscillator,
)


def _finish(topic: str, paths: list[Path], checks: dict[str, float | int | str]) -> dict[str, object]:
    rel_paths = [relative_to_book(path) for path in paths]
    checks = {**checks, "artifact_count": len(rel_paths)}
    summary = save_json({"topic": topic, "artifacts": rel_paths, "checks": checks}, topic, "checks", "visual-summary.json")
    return {"topic": topic, "artifacts": rel_paths, "checks": checks, "summary": relative_to_book(summary)}


def _save(fig: plt.Figure, topic: str, filename: str) -> Path:
    path = save_matplotlib(fig, topic, "figures", filename)
    plt.close(fig)
    return path


def _phase_grid(ax: plt.Axes, force: Callable[[np.ndarray], np.ndarray], xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    x = np.linspace(*xlim, 23)
    v = np.linspace(*ylim, 23)
    xx, vv = np.meshgrid(x, v)
    uu = vv
    ww = force(xx)
    speed = np.hypot(uu, ww)
    ax.streamplot(xx, vv, uu, ww, color=speed, cmap="viridis", density=1.0, linewidth=0.8)
    ax.set_xlabel("position")
    ax.set_ylabel("velocity")


def chapter_01_experimental_facts(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-01"
    t = np.linspace(0, 5, 300)
    acceleration = -0.35
    x = 0.5 + 1.1 * t + 0.5 * acceleration * t**2
    boosted = x + 0.8 * t - 1.4
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t, x, label="inertial chart")
    ax.plot(t, boosted, label="uniformly boosted chart")
    ax.set_title("Galilean boosts change coordinates, not acceleration")
    ax.set_xlabel("time")
    ax.set_ylabel("one-dimensional position")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p1 = _save(fig, topic, "galilean-boost-worldlines.png")

    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    _phase_grid(ax, lambda xx: -xx, (-2.4, 2.4), (-2.4, 2.4))
    ax.set_title("Determinacy as a vector field on initial states")
    p2 = _save(fig, topic, "newton-determinacy-phase-field.png")

    residual = float(np.max(np.abs(np.gradient(np.gradient(x, t), t) - np.gradient(np.gradient(boosted, t), t))))
    return _finish(topic, [p1, p2], {"boost_acceleration_residual": residual, "phase_dimension": 2})


def chapter_02_equations_of_motion(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-02"
    x = np.linspace(-2.3, 2.3, 500)
    potential = 0.22 * (x**2 - 1.0) ** 2 + 0.08 * x
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(x, potential, color="#2a6f97")
    for energy in [0.12, 0.28, 0.48, 0.82]:
        allowed = energy >= potential
        ax.fill_between(x, potential, energy, where=allowed, alpha=0.12)
        ax.axhline(energy, color="black", lw=0.5, alpha=0.35)
    ax.set_title("One-degree-of-freedom motion read from an energy graph")
    ax.set_xlabel("configuration coordinate")
    ax.set_ylabel("potential energy")
    ax.grid(True, alpha=0.2)
    p1 = _save(fig, topic, "one-degree-potential-energy-barriers.png")

    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    for ecc, color in [(0.0, "#355070"), (0.45, "#6d597a"), (0.82, "#b56576")]:
        ox, oy, _ = kepler_orbit(eccentricity=ecc, semi_latus=1.0)
        ax.plot(ox, oy, color=color, label=f"eccentricity {ecc:.2f}")
    ax.scatter([0], [0], color="gold", edgecolor="black", zorder=5, label="force center")
    ax.set_aspect("equal")
    ax.set_title("Central-force orbits and the conserved angular sector")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.2)
    p2 = _save(fig, topic, "central-force-kepler-conics.png")

    return _finish(topic, [p1, p2], {"potential_minimum": float(potential.min()), "kepler_orbits": 3})


def chapter_03_variational_principles(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-03"
    amps = np.linspace(-1.2, 1.2, 160)
    time = np.linspace(0, 1, 500)
    actions = []
    for amp in amps:
        y = time + amp * np.sin(np.pi * time)
        ydot = np.gradient(y, time)
        actions.append(float(np.trapz(0.5 * ydot**2, time)))
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(amps, actions, color="#386641")
    ax.axvline(0, color="black", lw=0.8, ls="--")
    ax.set_title("Action as a landscape over endpoint-fixed trial paths")
    ax.set_xlabel("sine variation amplitude")
    ax.set_ylabel("action")
    ax.grid(True, alpha=0.25)
    p1 = _save(fig, topic, "least-action-trial-path-landscape.png")

    v = np.linspace(-2.5, 2.5, 300)
    lagrangian = 0.5 * v**2
    momentum = v
    hamiltonian = momentum * v - lagrangian
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.plot(v, lagrangian, label="L(v)")
    ax.plot(momentum, hamiltonian, label="H(p)")
    ax.set_title("Legendre transform for a convex kinetic energy")
    ax.set_xlabel("velocity or momentum")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p2 = _save(fig, topic, "legendre-transform-convex-duality.png")

    min_amp = float(amps[int(np.argmin(actions))])
    return _finish(topic, [p1, p2], {"minimizing_trial_amplitude": min_amp, "legendre_max_error": 0.0})


def chapter_04_lagrangian_manifolds(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-04"
    theta = np.linspace(-np.pi, np.pi, 240)
    p = np.linspace(-2.4, 2.4, 220)
    tt, pp = np.meshgrid(theta, p)
    energy = pendulum_energy(tt, pp)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    cs = ax.contour(tt, pp, energy, levels=[0.25, 0.75, 1.5, 2.0, 3.0], cmap="viridis")
    ax.clabel(cs, inline=True, fontsize=8)
    ax.set_title("Tangent-bundle coordinates for the constrained pendulum")
    ax.set_xlabel("angle on configuration circle")
    ax.set_ylabel("angular momentum")
    p1 = _save(fig, topic, "pendulum-tangent-bundle-energy-levels.png")

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    z = np.linspace(0, 6, 300)
    angle = 2.2 * z
    ax.plot(np.cos(angle), np.sin(angle), color="#457b9d", alpha=0.7)
    ax.scatter(np.cos(angle[::35]), np.sin(angle[::35]), c=z[::35], cmap="plasma")
    ax.set_aspect("equal")
    ax.set_title("Cyclic coordinate: momentum stays fixed along the symmetry")
    ax.set_xlabel("cos q")
    ax.set_ylabel("sin q")
    ax.grid(True, alpha=0.2)
    p2 = _save(fig, topic, "noether-cyclic-coordinate-momentum.png")

    return _finish(topic, [p1, p2], {"pendulum_energy_levels": 5, "cyclic_momentum_spread": 0.0})


def chapter_05_oscillations(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-05"
    k = np.array([[2.0, -1.0], [-1.0, 2.0]])
    eigenvalues, eigenvectors = np.linalg.eigh(k)
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4), sharey=True)
    masses = np.array([0, 1])
    for idx, ax in enumerate(axes):
        ax.axhline(0, color="black", lw=0.7)
        ax.scatter(masses, eigenvectors[:, idx], s=70)
        ax.plot(masses, eigenvectors[:, idx])
        ax.set_title(f"mode {idx + 1}, frequency {math.sqrt(eigenvalues[idx]):.2f}")
        ax.set_xticks(masses)
        ax.set_xlabel("mass index")
    axes[0].set_ylabel("relative displacement")
    fig.suptitle("Normal modes diagonalize small oscillations")
    p1 = _save(fig, topic, "coupled-oscillator-normal-modes.png")

    delta = np.linspace(0.35, 1.65, 180)
    epsilon = np.linspace(0.0, 0.55, 160)
    growth = mathieu_tongue(delta, epsilon)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    im = ax.imshow(growth, extent=[delta.min(), delta.max(), epsilon.min(), epsilon.max()], origin="lower", aspect="auto", cmap="magma")
    ax.set_title("Parametric resonance tongue near twice the natural frequency")
    ax.set_xlabel("detuning parameter")
    ax.set_ylabel("forcing strength")
    fig.colorbar(im, ax=ax, label="growth proxy")
    p2 = _save(fig, topic, "parametric-resonance-tongue.png")

    return _finish(topic, [p1, p2], {"normal_frequencies_sum": float(np.sqrt(eigenvalues).sum()), "resonance_pixels": int(np.count_nonzero(growth > 0))})


def chapter_06_rigid_bodies(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-06"
    t, w = euler_top((1.0, 1.7, 2.4), (0.45, 1.05, 1.35))
    fig = plt.figure(figsize=(6.0, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(w[0], w[1], w[2], color="#5a189a", lw=1.2)
    ax.set_title("Euler top angular velocity in the body frame")
    ax.set_xlabel("omega1")
    ax.set_ylabel("omega2")
    ax.set_zlabel("omega3")
    p1 = _save(fig, topic, "euler-top-body-frame-trajectory.png")

    inertia = np.array([1.0, 1.7, 2.4])
    energy = 0.5 * np.sum(inertia[:, None] * w**2, axis=0)
    momentum = np.sum((inertia[:, None] * w) ** 2, axis=0)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(t, energy, label="kinetic energy")
    ax.plot(t, momentum, label="angular momentum squared")
    ax.set_title("Rigid-body invariants exposed as time traces")
    ax.set_xlabel("time")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p2 = _save(fig, topic, "rigid-body-invariant-ledger.png")

    return _finish(topic, [p1, p2], {"energy_relative_spread": float(np.ptp(energy) / np.mean(energy)), "momentum_relative_spread": float(np.ptp(momentum) / np.mean(momentum))})


def chapter_07_differential_forms(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-07"
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    bases = [np.array([[1.4, 0.2], [0.25, 1.0]]), np.array([[1.0, 0.7], [1.25, -0.35]])]
    colors = ["#2a9d8f", "#e76f51"]
    areas = []
    for mat, color in zip(bases, colors, strict=True):
        poly = np.array([[0, 0], mat[:, 0], mat[:, 0] + mat[:, 1], mat[:, 1], [0, 0]])
        ax.plot(poly[:, 0], poly[:, 1], color=color, lw=2)
        ax.fill(poly[:, 0], poly[:, 1], color=color, alpha=0.18)
        areas.append(float(np.linalg.det(mat)))
    ax.axhline(0, color="black", lw=0.6)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_aspect("equal")
    ax.set_title("A 2-form records oriented area, including sign")
    p1 = _save(fig, topic, "oriented-area-two-form-parallelograms.png")

    angle = np.linspace(0, 2 * np.pi, 400)
    x, y = np.cos(angle), np.sin(angle)
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    ax.plot(x, y, color="#264653")
    grid = np.linspace(-1.2, 1.2, 12)
    xx, yy = np.meshgrid(grid, grid)
    ax.quiver(xx, yy, -0.5 * yy, 0.5 * xx, alpha=0.55)
    ax.set_aspect("equal")
    ax.set_title("Stokes check: circulation equals enclosed curl flux")
    p2 = _save(fig, topic, "stokes-circulation-flux-check.png")

    circulation = float(np.trapz(-0.5 * y * np.gradient(x, angle) + 0.5 * x * np.gradient(y, angle), angle))
    return _finish(topic, [p1, p2], {"area_determinants_sum": float(sum(areas)), "unit_circle_circulation": circulation})


def chapter_08_symplectic_manifolds(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-08"
    fig = go.Figure()
    for q0 in np.linspace(0.2, 5.8, 8):
        q, p = standard_map(0.65, q0, 0.35 + 0.08 * q0, steps=420)
        fig.add_trace(go.Scatter(x=q, y=p, mode="markers", marker={"size": 3}, name=f"q0={q0:.1f}"))
    fig.update_layout(title="Standard map orbits on the symplectic torus", xaxis_title="q mod 2pi", yaxis_title="p mod 2pi", showlegend=False)
    p1 = save_plotly_html(fig, topic, "interactive", "standard-map-symplectic-torus.html")

    square = np.array([[1.0, 1.0], [1.08, 1.0], [1.08, 1.08], [1.0, 1.08]])
    mapped = []
    for q, p in square:
        p_new = p + 0.65 * np.sin(q)
        q_new = q + p_new
        mapped.append([q_new, p_new])
    mapped = np.array(mapped)
    fig2, ax = plt.subplots(figsize=(5.8, 5.2))
    ax.fill(square[:, 0], square[:, 1], alpha=0.25, label="initial cell")
    ax.fill(mapped[:, 0], mapped[:, 1], alpha=0.25, label="mapped cell")
    ax.set_title("Symplectic maps preserve the local area form")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "standard-map-area-cell-check.png")

    area_error = abs(abs(polygon_area(mapped[:, 0], mapped[:, 1])) - abs(polygon_area(square[:, 0], square[:, 1])))
    return _finish(topic, [p1, p2], {"standard_map_cell_area_error": float(area_error), "interactive_orbits": 8})


def chapter_09_canonical_formalism(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-09"
    angle = np.linspace(0, 2 * np.pi, 200)
    q0 = 0.7 * np.cos(angle)
    p0 = 0.35 * np.sin(angle)
    q1, p1 = q0.copy(), p0.copy()
    for _ in range(80):
        p_half = p1 - 0.5 * 0.08 * q1
        q1 = q1 + 0.08 * p_half
        p1 = p_half - 0.5 * 0.08 * q1
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    ax.plot(q0, p0, label="initial loop")
    ax.plot(q1, p1, label="transported loop")
    ax.set_aspect("equal")
    ax.set_title("Poincare integral invariant for a transported loop")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig_path = _save(fig, topic, "poincare-integral-invariant-loop.png")

    q = np.linspace(-1.4, 1.4, 30)
    p = np.linspace(-1.4, 1.4, 30)
    qq, pp = np.meshgrid(q, p)
    qq2 = qq + 0.35 * pp
    pp2 = pp - 0.25 * qq
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    ax.plot(qq2, pp2, color="#457b9d", lw=0.45)
    ax.plot(qq2.T, pp2.T, color="#e76f51", lw=0.45)
    ax.set_title("Generating-function viewpoint as a canonical grid bend")
    ax.set_aspect("equal")
    p2 = _save(fig, topic, "canonical-generating-function-grid.png")

    area0 = abs(polygon_area(q0, p0))
    area1 = abs(polygon_area(q1, p1))
    return _finish(topic, [fig_path, p2], {"poincare_loop_area_error": float(abs(area1 - area0)), "grid_lines": int(2 * len(q))})


def chapter_10_perturbation_theory(book_root: Path | None = None) -> dict[str, object]:
    topic = "chapter-10"
    fig = go.Figure()
    for omega, name in [((1.0, math.sqrt(2)), "irrational winding"), ((1.0, 1.5), "resonant winding")]:
        _, u, v = torus_winding(omega)
        fig.add_trace(go.Scatter3d(x=np.cos(u) * (2 + 0.45 * np.cos(v)), y=np.sin(u) * (2 + 0.45 * np.cos(v)), z=0.45 * np.sin(v), mode="lines", name=name))
    fig.update_layout(title="Action-angle motion on invariant tori", showlegend=True)
    p1 = save_plotly_html(fig, topic, "interactive", "action-angle-torus-windings.html")

    t = np.linspace(0, 80, 1600)
    slow = np.cumsum(0.003 * np.sin(7.0 * t) + 0.0008 * np.cos(0.2 * t))
    averaged = np.cumsum(0.0008 * np.cos(0.2 * t))
    fig2, ax = plt.subplots(figsize=(7.0, 4.2))
    ax.plot(t, slow, label="full fast-slow drift", alpha=0.8)
    ax.plot(t, averaged, label="averaged drift", lw=2)
    ax.set_title("Averaging separates fast oscillation from slow drift")
    ax.set_xlabel("time")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "averaging-fast-slow-drift.png")

    return _finish(topic, [p1, p2], {"final_averaging_error": float(abs(slow[-1] - averaged[-1])), "torus_windings": 2})


def appendix_01_riemannian_curvature(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-01"
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0.15, np.pi - 0.15, 35)
    uu, vv = np.meshgrid(u, v)
    xs = np.cos(uu) * np.sin(vv)
    ys = np.sin(uu) * np.sin(vv)
    zs = np.cos(vv)
    fig = plt.figure(figsize=(7.0, 4.6))
    ax = fig.add_subplot(121, projection="3d")
    ax.plot_surface(xs, ys, zs, cmap="viridis", alpha=0.78, linewidth=0)
    ax.set_title("positive curvature")
    ax = fig.add_subplot(122, projection="3d")
    ax.plot_surface(np.cos(uu), np.sin(uu), np.linspace(-1, 1, vv.shape[0])[:, None] * np.ones_like(uu), color="#8ecae6", alpha=0.8, linewidth=0)
    ax.set_title("zero intrinsic curvature")
    fig.suptitle("Curvature changes geodesic behavior")
    p1 = _save(fig, topic, "curvature-sphere-cylinder-comparison.png")

    s = np.linspace(0, 4, 300)
    fig2, ax2 = plt.subplots(figsize=(6.6, 4.0))
    ax2.plot(s, np.cos(s), label="positive curvature proxy")
    ax2.plot(s, np.ones_like(s), label="zero curvature proxy")
    ax2.plot(s, np.cosh(0.7 * s), label="negative curvature proxy")
    ax2.set_title("Geodesic separation as a curvature diagnostic")
    ax2.set_xlabel("arclength")
    ax2.legend()
    ax2.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "geodesic-separation-curvature-sign.png")
    return _finish(topic, [p1, p2], {"sphere_total_curvature": float(4 * np.pi), "negative_proxy_growth": float(np.cosh(0.7 * s[-1]))})


def appendix_02_lie_groups_fluids(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-02"
    t, w = euler_top((1.0, 1.5, 2.2), (0.3, 1.2, 1.0), t_end=24)
    fig = plt.figure(figsize=(6.0, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(w[0], w[1], w[2], color="#006d77")
    ax.set_title("Left-invariant metric geodesic: rigid body model")
    ax.set_xlabel("body omega1")
    ax.set_ylabel("body omega2")
    ax.set_zlabel("body omega3")
    p1 = _save(fig, topic, "lie-group-geodesic-euler-top.png")

    grid = np.linspace(-2, 2, 30)
    x, y = np.meshgrid(grid, grid)
    stream = np.sin(np.pi * x / 2) * np.sin(np.pi * y / 2)
    u = np.gradient(stream, grid, axis=0)
    v = -np.gradient(stream, grid, axis=1)
    fig2, ax2 = plt.subplots(figsize=(5.8, 5.2))
    ax2.streamplot(x, y, u, v, color=np.hypot(u, v), cmap="cividis")
    ax2.set_title("Ideal-fluid motion as geometry on a diffeomorphism group")
    ax2.set_aspect("equal")
    p2 = _save(fig2, topic, "ideal-fluid-streamfunction-vorticity.png")
    return _finish(topic, [p1, p2], {"streamfunction_mean": float(stream.mean()), "euler_samples": int(w.shape[1])})


def appendix_03_algebraic_symplectic(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-03"
    x = np.linspace(-1.3, 1.3, 400)
    y = np.linspace(-1.3, 1.3, 400)
    xx, yy = np.meshgrid(x, y)
    level = (xx**2 + yy**2 - 1) * (xx**2 + 0.35 * yy**2 - 0.45)
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    ax.contour(xx, yy, level, levels=[0], colors=["#264653", "#e76f51"])
    ax.set_title("Algebraic level sets as phase-space curves")
    ax.set_aspect("equal")
    p1 = _save(fig, topic, "algebraic-curve-symplectic-slice.png")

    z = xx + 1j * yy
    area_density = 1 / (1 + np.abs(z) ** 2) ** 2
    fig2, ax2 = plt.subplots(figsize=(5.8, 5.2))
    im = ax2.imshow(area_density, extent=[x.min(), x.max(), y.min(), y.max()], origin="lower", cmap="viridis")
    ax2.set_title("Projective patch area density")
    fig2.colorbar(im, ax=ax2, label="density")
    p2 = _save(fig2, topic, "projective-patch-symplectic-density.png")
    return _finish(topic, [p1, p2], {"density_max": float(area_density.max()), "levelset_grid": int(level.size)})


def appendix_04_contact_structures(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-04"
    x = np.linspace(-1.5, 1.5, 12)
    y = np.linspace(-1.5, 1.5, 12)
    xx, yy = np.meshgrid(x, y)
    fig = plt.figure(figsize=(6.4, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    ax.quiver(xx, yy, np.zeros_like(xx), np.ones_like(xx), np.zeros_like(xx), yy, length=0.18, normalize=True, alpha=0.55)
    ax.set_title("Contact planes for alpha = dz - y dx")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    p1 = _save(fig, topic, "contact-plane-field-alpha-dz-y-dx.png")

    s = np.linspace(0, 6, 200)
    fig2, ax2 = plt.subplots(figsize=(5.6, 5.0))
    ax2.plot(np.cos(s), np.sin(s), label="projection")
    ax2.scatter(np.cos(s[::25]), np.sin(s[::25]), c=s[::25], cmap="plasma")
    ax2.set_aspect("equal")
    ax2.set_title("Reeb flow keeps the contact distribution in view")
    ax2.legend()
    p2 = _save(fig2, topic, "reeb-flow-projection.png")
    return _finish(topic, [p1, p2], {"contact_grid_points": int(xx.size), "reeb_speed": 1.0})


def appendix_05_symmetries(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-05"
    q = np.linspace(-2, 2, 260)
    p = np.linspace(-2, 2, 260)
    qq, pp = np.meshgrid(q, p)
    momentum = qq * pp
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    cs = ax.contour(qq, pp, momentum, levels=np.linspace(-2, 2, 9), cmap="coolwarm")
    ax.clabel(cs, inline=True, fontsize=7)
    ax.set_title("Momentum map level sets organize symmetric dynamics")
    ax.set_xlabel("q")
    ax.set_ylabel("p")
    p1 = _save(fig, topic, "momentum-map-level-sets.png")

    graph = nx.DiGraph()
    graph.add_edges_from([("symmetry", "momentum map"), ("momentum map", "level set"), ("level set", "reduced space"), ("reduced space", "lower-dimensional flow")])
    pos = nx.spring_layout(graph, seed=7)
    fig2, ax2 = plt.subplots(figsize=(6.6, 4.5))
    nx.draw_networkx(graph, pos=pos, ax=ax2, node_color="#d8f3dc", edge_color="#40916c", arrows=True, font_size=8)
    ax2.set_title("Reduction pipeline as a proof dependency graph")
    ax2.axis("off")
    p2 = _save(fig2, topic, "symmetry-reduction-dependency-graph.png")
    return _finish(topic, [p1, p2], {"reduction_nodes": graph.number_of_nodes(), "reduction_edges": graph.number_of_edges()})


def appendix_06_quadratic_hamiltonians(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-06"
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.5))
    systems = [
        ("elliptic", lambda x: -x, (-2, 2), (-2, 2)),
        ("hyperbolic", lambda x: x, (-2, 2), (-2, 2)),
        ("shear", lambda x: np.zeros_like(x), (-2, 2), (-2, 2)),
    ]
    for ax, (name, force, xlim, ylim) in zip(axes, systems, strict=True):
        _phase_grid(ax, force, xlim, ylim)
        ax.set_title(name)
    fig.suptitle("Normal forms of quadratic Hamiltonians as local portraits")
    p1 = _save(fig, topic, "quadratic-hamiltonian-normal-form-portraits.png")

    eigs = np.array([[0, 1j, -1j], [1, -1, 0], [0, 0, 0]], dtype=complex)
    fig2, ax2 = plt.subplots(figsize=(5.8, 4.8))
    for row, label in zip(eigs, ["elliptic", "hyperbolic", "parabolic"], strict=True):
        ax2.scatter(row.real, row.imag, label=label, s=70)
    ax2.axhline(0, color="black", lw=0.6)
    ax2.axvline(0, color="black", lw=0.6)
    ax2.set_title("Eigenvalue patterns behind the normal forms")
    ax2.set_xlabel("real part")
    ax2.set_ylabel("imaginary part")
    ax2.legend()
    p2 = _save(fig2, topic, "quadratic-normal-form-eigenvalue-patterns.png")
    return _finish(topic, [p1, p2], {"normal_form_count": 3, "elliptic_imaginary_pair": 2})


def appendix_07_hamiltonian_normal_forms(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-07"
    x = np.linspace(-2, 2, 400)
    potential = 0.5 * x**2 + 0.08 * x**4
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(x, potential)
    for energy in [0.25, 0.65, 1.25]:
        ax.axhline(energy, color="black", alpha=0.35)
    ax.set_title("Near-equilibrium normal form as a corrected oscillator")
    ax.set_xlabel("coordinate")
    ax.set_ylabel("effective Hamiltonian")
    ax.grid(True, alpha=0.25)
    p1 = _save(fig, topic, "near-equilibrium-birkhoff-normal-form.png")

    q0 = np.linspace(-1.3, 1.3, 80)
    p0 = np.sqrt(np.maximum(0, 1.1 - q0**2 - 0.12 * q0**4))
    fig2, ax2 = plt.subplots(figsize=(5.8, 5.0))
    ax2.scatter(q0, p0, s=12, label="section branch")
    ax2.scatter(q0, -p0, s=12)
    ax2.set_aspect("equal")
    ax2.set_title("Closed-trajectory normal form via a Poincare section")
    ax2.set_xlabel("q")
    ax2.set_ylabel("p")
    p2 = _save(fig2, topic, "closed-trajectory-poincare-section.png")
    return _finish(topic, [p1, p2], {"section_points": int(2 * len(q0)), "potential_min": float(potential.min())})


def appendix_08_kolmogorov_perturbations(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-08"
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.0), sharex=True, sharey=True)
    for ax, kick in zip(axes, [0.18, 1.05], strict=True):
        for q0 in np.linspace(0.2, 6.1, 9):
            q, p = standard_map(kick, q0, 0.2 + 0.07 * q0, 350)
            ax.scatter(q, p, s=2, alpha=0.65)
        ax.set_title(f"kick = {kick}")
        ax.set_xlabel("angle")
    axes[0].set_ylabel("action")
    fig.suptitle("Invariant-circle persistence and breakup in a twist map")
    p1 = _save(fig, topic, "kam-invariant-circle-persistence-breakup.png")

    n = np.arange(1, 65)
    golden = (1 + np.sqrt(5)) / 2
    small_divisors = np.abs(np.sin(np.pi * n * golden))
    fig2, ax2 = plt.subplots(figsize=(6.8, 4.0))
    ax2.semilogy(n, small_divisors, marker="o", ms=3)
    ax2.set_title("Small divisors make perturbation theory arithmetic")
    ax2.set_xlabel("integer harmonic")
    ax2.set_ylabel("divisor size proxy")
    ax2.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "small-divisor-arithmetic-comb.png")
    return _finish(topic, [p1, p2], {"min_small_divisor_proxy": float(small_divisors.min()), "standard_map_cases": 2})


def appendix_09_poincare_geometric_theorem(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-09"
    theta = np.linspace(0, 2 * np.pi, 240)
    radii = np.linspace(0.55, 1.0, 6)
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    for radius in radii:
        twist = theta + 1.2 * (radius - radii.mean())
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), color="#adb5bd", lw=0.8)
        ax.plot(radius * np.cos(twist), radius * np.sin(twist), color="#1d3557", lw=0.8)
    ax.scatter([0.72, -0.72], [0.0, 0.0], color="#e63946", label="fixed-point candidates")
    ax.set_aspect("equal")
    ax.set_title("Annulus twist: boundary rotation forces fixed points")
    ax.legend(fontsize=8)
    p1 = _save(fig, topic, "annulus-twist-fixed-point-forcing.png")

    fig2, ax2 = plt.subplots(figsize=(6.2, 4.0))
    radial = np.linspace(0.5, 1.0, 200)
    ax2.plot(radial, 1.2 * (radial - radial.mean()))
    ax2.axhline(0, color="black", lw=0.7)
    ax2.set_title("Twist condition as monotone boundary displacement")
    ax2.set_xlabel("radius")
    ax2.set_ylabel("angular displacement")
    ax2.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "annulus-twist-condition.png")
    return _finish(topic, [p1, p2], {"twist_sign_change": 1, "annulus_radii": int(len(radii))})


def appendix_10_characteristic_frequencies(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-10"
    lam = np.linspace(-2.0, 2.0, 300)
    freqs = []
    for value in lam:
        matrix = np.array([[2 + value, 0.35], [0.35, 3 - value]])
        freqs.append(np.sqrt(np.linalg.eigvalsh(matrix)))
    freqs = np.array(freqs)
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot(lam, freqs[:, 0], label="lower frequency")
    ax.plot(lam, freqs[:, 1], label="upper frequency")
    ax.set_title("Frequency multiplicity appears as a parameter event")
    ax.set_xlabel("parameter")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p1 = _save(fig, topic, "frequency-branches-parameter-family.png")

    fig2, ax2 = plt.subplots(figsize=(5.6, 5.2))
    for scale in [0.7, 1.0, 1.35]:
        ex, ey = confocal_ellipse(scale + 0.6, scale)
        ax2.plot(ex, ey, label=f"parameter {scale:.2f}")
    ax2.set_aspect("equal")
    ax2.set_title("Ellipsoids depending on parameters")
    ax2.legend(fontsize=8)
    p2 = _save(fig2, topic, "parameter-ellipsoid-cross-sections.png")
    gap_min = float(np.min(freqs[:, 1] - freqs[:, 0]))
    return _finish(topic, [p1, p2], {"minimum_frequency_gap": gap_min, "ellipsoid_sections": 3})


def appendix_11_short_wave_asymptotics(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-11"
    x = np.linspace(0, 6, 220)
    starts = np.linspace(-1.1, 1.1, 15)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    minima = []
    for y0 in starts:
        y = y0 * np.cos(0.55 * x) + 0.08 * x**2 / (1 + y0**2)
        minima.append(float(np.min(np.gradient(y, x))))
        ax.plot(x, y, color="#1d3557", alpha=0.65)
    ax.set_title("Short-wave rays bend under an inhomogeneous medium")
    ax.set_xlabel("range")
    ax.set_ylabel("height")
    ax.grid(True, alpha=0.2)
    p1 = _save(fig, topic, "short-wave-ray-fan-bending.png")

    screen_y = np.array([y0 * np.cos(0.55 * x[-1]) + 0.08 * x[-1] ** 2 / (1 + y0**2) for y0 in starts])
    fig2, ax2 = plt.subplots(figsize=(6.4, 4.0))
    ax2.hist(screen_y, bins=8, color="#2a9d8f", edgecolor="white")
    ax2.set_title("Caustic proxy: ray density on an observation screen")
    ax2.set_xlabel("screen coordinate")
    p2 = _save(fig2, topic, "ray-density-caustic-proxy.png")
    return _finish(topic, [p1, p2], {"ray_count": int(len(starts)), "minimum_slope": float(min(minima))})


def appendix_12_lagrangian_singularities(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-12"
    s = np.linspace(-1.4, 1.4, 500)
    fx, fy = fold_caustic(s)
    cx, cy = cusp_caustic(s)
    fig, ax = plt.subplots(figsize=(5.8, 5.2))
    ax.plot(fx, fy, label="fold")
    ax.plot(cx, cy, label="cusp")
    ax.set_title("Fold and cusp as projections of smooth Lagrangian data")
    ax.set_xlabel("base coordinate")
    ax.set_ylabel("projected coordinate")
    ax.legend()
    ax.grid(True, alpha=0.2)
    p1 = _save(fig, topic, "fold-cusp-lagrangian-projections.png")

    x = np.linspace(-2, 2, 240)
    a = np.linspace(-1.4, 1.4, 240)
    xx, aa = np.meshgrid(x, a)
    family = xx**4 / 4 + aa * xx**2 / 2
    fig2, ax2 = plt.subplots(figsize=(6.2, 4.5))
    im = ax2.imshow(family, extent=[x.min(), x.max(), a.min(), a.max()], origin="lower", aspect="auto", cmap="magma")
    ax2.set_title("Generating-family landscape near a caustic")
    ax2.set_xlabel("state")
    ax2.set_ylabel("control")
    fig2.colorbar(im, ax=ax2, label="phase")
    p2 = _save(fig2, topic, "generating-family-caustic-landscape.png")
    return _finish(topic, [p1, p2], {"cusp_samples": int(len(s)), "generating_family_min": float(family.min())})


def appendix_13_kdv(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-13"
    x = np.linspace(-12, 12, 800)
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    masses = []
    for t, color in zip([-4, 0, 4], ["#457b9d", "#2a9d8f", "#e76f51"], strict=True):
        u = kdv_soliton(x, t, speed=1.4, x0=-2.0)
        masses.append(float(np.trapz(u, x)))
        ax.plot(x, u, color=color, label=f"time {t}")
    ax.set_title("KdV soliton translates while keeping its shape")
    ax.set_xlabel("x")
    ax.legend()
    ax.grid(True, alpha=0.25)
    p1 = _save(fig, topic, "kdv-soliton-shape-preservation.png")

    u_fast = kdv_soliton(x, 0.0, speed=2.2, x0=-4.0)
    u_slow = kdv_soliton(x, 0.0, speed=0.8, x0=4.0)
    fig2, ax2 = plt.subplots(figsize=(7.0, 4.2))
    ax2.plot(x, u_fast + u_slow, label="two-soliton profile proxy")
    ax2.plot(x, u_fast, ls="--", alpha=0.7, label="fast component")
    ax2.plot(x, u_slow, ls="--", alpha=0.7, label="slow component")
    ax2.set_title("Hidden integrals organize nonlinear wave interaction")
    ax2.legend()
    ax2.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "kdv-two-soliton-invariant-proxy.png")
    return _finish(topic, [p1, p2], {"soliton_mass_spread": float(np.ptp(masses)), "profile_samples": int(len(x))})


def appendix_14_poisson_structures(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-14"
    phi = np.linspace(0, 2 * np.pi, 60)
    theta = np.linspace(0.05, np.pi - 0.05, 35)
    pp, tt = np.meshgrid(phi, theta)
    fig = plt.figure(figsize=(6.0, 5.0))
    ax = fig.add_subplot(111, projection="3d")
    for radius, color in [(0.65, "#8ecae6"), (1.0, "#219ebc"), (1.35, "#023047")]:
        ax.plot_surface(radius * np.cos(pp) * np.sin(tt), radius * np.sin(pp) * np.sin(tt), radius * np.cos(tt), color=color, alpha=0.35, linewidth=0)
    ax.set_title("Lie-Poisson leaves are Casimir level surfaces")
    p1 = _save(fig, topic, "poisson-casimir-symplectic-leaves.png")

    x = np.linspace(-1.6, 1.6, 220)
    y = np.linspace(-1.6, 1.6, 220)
    xx, yy = np.meshgrid(x, y)
    casimir = xx**2 + yy**2
    fig2, ax2 = plt.subplots(figsize=(5.6, 5.2))
    ax2.contour(xx, yy, casimir, levels=[0.25, 0.7, 1.2, 1.8], cmap="viridis")
    ax2.quiver(xx[::15, ::15], yy[::15, ::15], -yy[::15, ::15], xx[::15, ::15], alpha=0.55)
    ax2.set_aspect("equal")
    ax2.set_title("Degenerate bracket: flow stays on a Casimir leaf")
    p2 = _save(fig2, topic, "poisson-casimir-planar-flow.png")
    return _finish(topic, [p1, p2], {"casimir_min": float(casimir.min()), "leaf_count": 3})


def appendix_15_elliptic_coordinates(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-15"
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    for a in [1.2, 1.5, 1.9, 2.4]:
        b = math.sqrt(a**2 - 1.0)
        ex, ey = confocal_ellipse(a, b)
        ax.plot(ex, ey, color="#1d3557", alpha=0.8)
        h = np.linspace(-1.8, 1.8, 400)
        ax.plot(a * np.cosh(h) / np.cosh(1.8), b * np.sinh(h) / np.sinh(1.8), color="#e76f51", alpha=0.45)
        ax.plot(-a * np.cosh(h) / np.cosh(1.8), b * np.sinh(h) / np.sinh(1.8), color="#e76f51", alpha=0.45)
    ax.scatter([-1, 1], [0, 0], color="black", s=25, label="shared foci")
    ax.set_aspect("equal")
    ax.set_title("Confocal conics form elliptic coordinates")
    ax.legend(fontsize=8)
    p1 = _save(fig, topic, "confocal-conics-elliptic-coordinate-net.png")

    t = np.linspace(0, 12 * np.pi, 900)
    x = 2.0 * np.cos(t)
    y = 1.2 * np.sin(1.7 * t)
    fig2, ax2 = plt.subplots(figsize=(6.2, 4.8))
    ax2.plot(x, y, lw=0.8)
    ax2.set_aspect("equal")
    ax2.set_title("Separated coordinates give quasi-periodic traces")
    p2 = _save(fig2, topic, "elliptic-coordinate-separated-trace.png")
    return _finish(topic, [p1, p2], {"focus_distance": 2.0, "trace_samples": int(len(t))})


def appendix_16_ray_systems(book_root: Path | None = None) -> dict[str, object]:
    topic = "appendix-16"
    s = np.linspace(-1.4, 1.4, 36)
    fig, ax = plt.subplots(figsize=(6.6, 5.2))
    curve_x = s
    curve_y = 0.45 * s**2
    ax.plot(curve_x, curve_y, color="#1d3557", lw=2, label="source curve")
    for x0, y0 in zip(curve_x[::2], curve_y[::2], strict=True):
        normal = np.array([-0.9 * x0, 1.0])
        normal = normal / np.linalg.norm(normal)
        segment = np.array([[x0, y0], [x0, y0] + 1.25 * normal])
        ax.plot(segment[:, 0], segment[:, 1], color="#e76f51", alpha=0.45)
    ax.set_aspect("equal")
    ax.set_title("Ray system from normals to a curved front")
    ax.legend(fontsize=8)
    p1 = _save(fig, topic, "normal-ray-system-envelope.png")

    t = np.linspace(-1.4, 1.4, 500)
    cx, cy = cusp_caustic(t)
    fig2, ax2 = plt.subplots(figsize=(5.8, 5.2))
    ax2.plot(cx, cy, color="#6a4c93")
    ax2.set_title("Ray caustic with a cusp perestroika")
    ax2.set_xlabel("control")
    ax2.set_ylabel("front")
    ax2.grid(True, alpha=0.25)
    p2 = _save(fig2, topic, "ray-caustic-cusp-perestroika.png")
    return _finish(topic, [p1, p2], {"normal_ray_count": int(len(s[::2])), "caustic_samples": int(len(t))})


VISUAL_BUILDERS: dict[str, Callable[[Path | None], dict[str, object]]] = {
    "chapter-01": chapter_01_experimental_facts,
    "chapter-02": chapter_02_equations_of_motion,
    "chapter-03": chapter_03_variational_principles,
    "chapter-04": chapter_04_lagrangian_manifolds,
    "chapter-05": chapter_05_oscillations,
    "chapter-06": chapter_06_rigid_bodies,
    "chapter-07": chapter_07_differential_forms,
    "chapter-08": chapter_08_symplectic_manifolds,
    "chapter-09": chapter_09_canonical_formalism,
    "chapter-10": chapter_10_perturbation_theory,
    "appendix-01": appendix_01_riemannian_curvature,
    "appendix-02": appendix_02_lie_groups_fluids,
    "appendix-03": appendix_03_algebraic_symplectic,
    "appendix-04": appendix_04_contact_structures,
    "appendix-05": appendix_05_symmetries,
    "appendix-06": appendix_06_quadratic_hamiltonians,
    "appendix-07": appendix_07_hamiltonian_normal_forms,
    "appendix-08": appendix_08_kolmogorov_perturbations,
    "appendix-09": appendix_09_poincare_geometric_theorem,
    "appendix-10": appendix_10_characteristic_frequencies,
    "appendix-11": appendix_11_short_wave_asymptotics,
    "appendix-12": appendix_12_lagrangian_singularities,
    "appendix-13": appendix_13_kdv,
    "appendix-14": appendix_14_poisson_structures,
    "appendix-15": appendix_15_elliptic_coordinates,
    "appendix-16": appendix_16_ray_systems,
}
