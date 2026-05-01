"""Generated visual artifacts for the do Carmo notebook course."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

from .artifacts import ARTIFACT_ROOT, assert_artifact, save_figure, save_plotly_html, write_json
from .dg_curves import cumulative_arc_length, curvature_3d, frenet_frame, osculating_circle, torsion_3d
from .dg_surfaces import (
    first_fundamental_form,
    graph_surface_curvature,
    meshgrid,
    metric_ellipse,
    partials,
    sphere,
    stack_surface,
    torus,
    unit_normals,
)
from .plotting import COURSE_COLORS, equalize_3d_axes, finish_axes, set_course_style, surface_colors


def _finalize(unit: str, paths: dict[str, Path], checks: dict[str, Any]) -> dict[str, Any]:
    sizes = {name: assert_artifact(path).stat().st_size for name, path in paths.items()}
    final = {
        "unit": unit,
        "artifact_count": len(paths),
        "artifact_sizes": sizes,
        "checks": checks,
    }
    paths["final_sanity"] = write_json(final, unit, "checks", "final-sanity.json")
    return {"paths": {key: str(path) for key, path in paths.items()}, "checks": final}


def build_unit_visuals(unit: str, *, root: str | Path = ARTIFACT_ROOT) -> dict[str, Any]:
    """Build visual artifacts and JSON checks for a course unit."""

    set_course_style()
    builders = {
        "chapter-01": _chapter_01,
        "chapter-02": _chapter_02,
        "chapter-03": _chapter_03,
        "chapter-04": _chapter_04,
        "chapter-05": _chapter_05,
    }
    if unit not in builders:
        raise KeyError(f"unknown unit {unit!r}")
    return builders[unit](Path(root))


def _chapter_01(root: Path) -> dict[str, Any]:
    unit = "chapter-01"
    paths: dict[str, Path] = {}
    checks: dict[str, Any] = {}

    t = np.linspace(0, 6 * np.pi, 600)
    a, b = 1.0, 0.28
    helix = np.column_stack([a * np.cos(t), a * np.sin(t), b * t])
    curvature = curvature_3d(helix, t)
    torsion = torsion_3d(helix, t)
    tangent, normal, binormal = frenet_frame(helix, t)
    expected_kappa = a / (a * a + b * b)
    expected_tau = -b / (a * a + b * b)
    checks["helix_curvature_error"] = float(np.max(np.abs(curvature[20:-20] - expected_kappa)))
    checks["helix_torsion_error"] = float(np.max(np.abs(torsion[30:-30] - expected_tau)))

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(helix[:, 0], helix[:, 1], helix[:, 2], color=COURSE_COLORS["blue"], lw=2.0, label="helix")
    for idx in [80, 200, 340, 480]:
        p = helix[idx]
        scale = 0.55
        ax.quiver(*p, *(scale * tangent[idx]), color=COURSE_COLORS["green"], linewidth=1.4)
        ax.quiver(*p, *(scale * normal[idx]), color=COURSE_COLORS["red"], linewidth=1.4)
        ax.quiver(*p, *(scale * binormal[idx]), color=COURSE_COLORS["violet"], linewidth=1.4)
    ax.set_title("Frenet frame along a helix")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    equalize_3d_axes(ax, helix[:, 0], helix[:, 1], helix[:, 2])
    paths["frenet_frame"] = save_figure(fig, unit, "figures", "helix-frenet-frame.png", root=root)
    plt.close(fig)

    s = np.linspace(0, 2 * np.pi, 400)
    curve = np.column_stack([s, np.sin(s), np.zeros_like(s)])
    kappa = curvature_3d(curve, s)
    mid = int(np.argmax(kappa))
    osc = osculating_circle(curve[mid], tangent=np.array([1.0, np.cos(s[mid]), 0.0]) / math.sqrt(1 + np.cos(s[mid]) ** 2), normal=np.array([0.0, -1.0, 0.0]), radius=1 / kappa[mid])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(curve[:, 0], curve[:, 1], color=COURSE_COLORS["blue"], lw=2.0, label="plane curve")
    ax.plot(osc[:, 0], osc[:, 1], color=COURSE_COLORS["red"], ls="--", label="osculating circle")
    ax.scatter([curve[mid, 0]], [curve[mid, 1]], color=COURSE_COLORS["ink"], zorder=3)
    ax.legend(loc="upper right")
    finish_axes(ax, "Osculating circle as curvature made visible", "parameter x", "height y")
    paths["osculating_circle"] = save_figure(fig, unit, "figures", "osculating-circle-curvature.png", root=root)
    plt.close(fig)

    theta = np.linspace(0, 2 * np.pi, 500)
    cardioid = np.column_stack([(1 - np.cos(theta)) * np.cos(theta), (1 - np.cos(theta)) * np.sin(theta), np.zeros_like(theta)])
    arc = cumulative_arc_length(cardioid, theta)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(theta, arc, color=COURSE_COLORS["green"], lw=2.0)
    ax.set_title("Arc length is a new clock for a curve")
    ax.set_xlabel("original parameter")
    ax.set_ylabel("accumulated length")
    checks["arc_length_monotone"] = bool(np.all(np.diff(arc) >= -1e-10))
    paths["arc_clock"] = save_figure(fig, unit, "figures", "arc-length-clock.png", root=root)
    plt.close(fig)

    fig = go.Figure(data=[go.Scatter3d(x=helix[:, 0], y=helix[:, 1], z=helix[:, 2], mode="lines", line={"width": 5})])
    fig.update_layout(title="Rotate the helix: curvature is local, trace is global", scene={"aspectmode": "data"})
    paths["interactive"] = save_plotly_html(fig, unit, "interactive", "helix-trace-and-frame.html", root=root)
    return _finalize(unit, paths, checks)


def _chapter_02(root: Path) -> dict[str, Any]:
    unit = "chapter-02"
    paths: dict[str, Path] = {}
    checks: dict[str, Any] = {}

    u, v = meshgrid((-1.4, 1.4), (-1.4, 1.4), 80)
    z = 0.35 * (u * u - 0.6 * v * v)
    pts = np.stack([u, v, z], axis=-1)
    xu, xv = partials(pts, u, v)
    normals = unit_normals(xu, xv)
    e, f, g = first_fundamental_form(xu, xv)
    area_density = np.sqrt(np.maximum(e * g - f * f, 0.0))
    checks["metric_positive_min"] = float(np.nanmin(e * g - f * f))
    checks["area_density_mean"] = float(np.nanmean(area_density))

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(u, v, z, facecolors=surface_colors(z, "coolwarm"), linewidth=0, antialiased=True, alpha=0.92)
    for i, j in [(28, 28), (40, 44), (54, 35)]:
        p = pts[i, j]
        ax.quiver(*p, *(0.45 * normals[i, j]), color=COURSE_COLORS["ink"], linewidth=1.2)
    ax.set_title("A regular patch carries tangent planes and normals")
    ax.set_xlabel("u")
    ax.set_ylabel("v")
    ax.set_zlabel("z")
    equalize_3d_axes(ax, pts[..., 0].ravel(), pts[..., 1].ravel(), pts[..., 2].ravel())
    paths["surface_patch"] = save_figure(fig, unit, "figures", "regular-surface-patch-normals.png", root=root)
    plt.close(fig)

    metric = np.array([[float(e[48, 42]), float(f[48, 42])], [float(f[48, 42]), float(g[48, 42])]])
    ellipse = metric_ellipse(metric)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(ellipse[:, 0], ellipse[:, 1], color=COURSE_COLORS["blue"], lw=2.0)
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.axvline(0, color="#94a3b8", lw=1)
    finish_axes(ax, "Metric ellipse for the first fundamental form", "du", "dv")
    checks["metric_eigenvalues"] = [float(x) for x in np.linalg.eigvalsh(metric)]
    paths["metric_ellipse"] = save_figure(fig, unit, "figures", "first-fundamental-form-metric-ellipse.png", root=root)
    plt.close(fig)

    ns = np.array([8, 16, 32, 64])
    estimates = []
    for n in ns:
        uu, vv = meshgrid((-1.4, 1.4), (-1.4, 1.4), int(n))
        zz = 0.35 * (uu * uu - 0.6 * vv * vv)
        pp = np.stack([uu, vv, zz], axis=-1)
        pu, pv = partials(pp, uu, vv)
        ee, ff, gg = first_fundamental_form(pu, pv)
        density = np.sqrt(np.maximum(ee * gg - ff * ff, 0.0))
        estimates.append(float(np.trapz(np.trapz(density, vv[0, :], axis=1), uu[:, 0])))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(ns, estimates, marker="o", color=COURSE_COLORS["green"])
    ax.set_title("Area from the metric stabilizes under refinement")
    ax.set_xlabel("grid samples per coordinate")
    ax.set_ylabel("area estimate")
    checks["area_refinement_last_step"] = float(abs(estimates[-1] - estimates[-2]))
    paths["area_refinement"] = save_figure(fig, unit, "figures", "area-density-refinement.png", root=root)
    plt.close(fig)

    fig = go.Figure(data=[go.Surface(x=u, y=v, z=z, colorscale="Viridis", showscale=False)])
    fig.update_layout(title="Regular graph surface as an interactive patch", scene={"aspectmode": "data"})
    paths["interactive"] = save_plotly_html(fig, unit, "interactive", "regular-surface-patch.html", root=root)
    return _finalize(unit, paths, checks)


def _chapter_03(root: Path) -> dict[str, Any]:
    unit = "chapter-03"
    paths: dict[str, Path] = {}
    checks: dict[str, Any] = {}

    u, v = meshgrid((0.0, 2.0 * np.pi), (0.0, 2.0 * np.pi), 90)
    pts = stack_surface(torus, u, v)
    xu, xv = partials(pts, u, v)
    normals = unit_normals(xu, xv)
    major, minor = 2.0, 0.65
    gaussian = np.cos(v) / (minor * (major + minor * np.cos(v)))
    checks["torus_gaussian_min"] = float(np.nanmin(gaussian))
    checks["torus_gaussian_max"] = float(np.nanmax(gaussian))

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(pts[..., 0], pts[..., 1], pts[..., 2], facecolors=surface_colors(gaussian, "Spectral"), linewidth=0, alpha=0.96)
    for i, j in [(10, 15), (25, 50), (55, 20), (75, 65)]:
        p = pts[i, j]
        ax.quiver(*p, *(0.35 * normals[i, j]), color=COURSE_COLORS["ink"], linewidth=1.1)
    ax.set_title("Gauss map samples: normals remember curvature")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    equalize_3d_axes(ax, pts[..., 0].ravel(), pts[..., 1].ravel(), pts[..., 2].ravel())
    paths["gauss_map"] = save_figure(fig, unit, "figures", "torus-gauss-map-normals.png", root=root)
    plt.close(fig)

    x, y = np.meshgrid(np.linspace(-1.4, 1.4, 100), np.linspace(-1.4, 1.4, 100), indexing="ij")
    z = 0.5 * (x * x - y * y)
    k, h = graph_surface_curvature(x, y, z)
    checks["saddle_mean_abs_center"] = float(abs(h[50, 50]))
    checks["saddle_gaussian_center"] = float(k[50, 50])
    fig, ax = plt.subplots(figsize=(7, 5.5))
    image = ax.imshow(k.T, origin="lower", extent=[-1.4, 1.4, -1.4, 1.4], cmap="coolwarm")
    ax.contour(x, y, z, colors="#334155", linewidths=0.5, alpha=0.7)
    fig.colorbar(image, ax=ax, label="Gaussian curvature")
    finish_axes(ax, "Negative curvature on a saddle graph", "x", "y")
    paths["saddle_curvature"] = save_figure(fig, unit, "figures", "saddle-gaussian-curvature-heatmap.png", root=root)
    plt.close(fig)

    uu, vv = meshgrid((-1.6, 1.6), (0.0, 2.0 * np.pi), 70)
    catenoid = np.stack([np.cosh(uu) * np.cos(vv), np.cosh(uu) * np.sin(vv), uu], axis=-1)
    helicoid = np.stack([uu * np.cos(vv), uu * np.sin(vv), vv / np.pi - 3.0], axis=-1)
    checks["minimal_surface_mean_curvature_target"] = 0.0
    fig = go.Figure()
    fig.add_trace(go.Surface(x=catenoid[..., 0], y=catenoid[..., 1], z=catenoid[..., 2], colorscale="Blues", showscale=False, opacity=0.9, name="catenoid"))
    fig.add_trace(go.Surface(x=helicoid[..., 0] + 5.0, y=helicoid[..., 1], z=helicoid[..., 2], colorscale="Reds", showscale=False, opacity=0.9, name="helicoid"))
    fig.update_layout(title="Two minimal surface models: catenoid and helicoid", scene={"aspectmode": "data"})
    paths["interactive"] = save_plotly_html(fig, unit, "interactive", "catenoid-helicoid-minimal-surfaces.html", root=root)
    return _finalize(unit, paths, checks)


def _chapter_04(root: Path) -> dict[str, Any]:
    unit = "chapter-04"
    paths: dict[str, Path] = {}
    checks: dict[str, Any] = {}

    x = np.linspace(-2.0, 2.0, 17)
    y = np.linspace(-2.0, 2.0, 17)
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for value in x:
        axes[0].plot(np.full_like(y, value), y, color=COURSE_COLORS["blue"], alpha=0.5)
        axes[0].plot(x, np.full_like(x, value), color=COURSE_COLORS["green"], alpha=0.5)
    z = np.linspace(-2.0, 2.0, 200)
    for value in np.linspace(-1.6, 1.6, 9):
        w = z + 1j * value
        mapped = np.exp(0.35 * w) * w
        axes[1].plot(mapped.real, mapped.imag, color=COURSE_COLORS["blue"], alpha=0.55)
        w = value + 1j * z
        mapped = np.exp(0.35 * w) * w
        axes[1].plot(mapped.real, mapped.imag, color=COURSE_COLORS["green"], alpha=0.55)
    finish_axes(axes[0], "Euclidean coordinate net", "x", "y")
    finish_axes(axes[1], "Conformal net preserves angles, not lengths", "u", "v")
    checks["conformal_angle_target_degrees"] = 90.0
    paths["conformal_grid"] = save_figure(fig, unit, "figures", "isometry-conformal-grid-comparison.png", root=root)
    plt.close(fig)

    theta = np.linspace(0.0, 1.2, 150)
    phi = np.linspace(0.0, 2.4, 150)
    sphere_paths = []
    for longitude in [0.0, 0.45, -0.45]:
        u = theta
        v = longitude + phi * 0.18
        sphere_paths.append(np.column_stack([np.sin(u) * np.cos(v), np.sin(u) * np.sin(v), np.cos(u)]))
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    uu, vv = meshgrid((0.02, np.pi - 0.02), (0.0, 2 * np.pi), 45)
    sp = stack_surface(sphere, uu, vv)
    ax.plot_surface(sp[..., 0], sp[..., 1], sp[..., 2], color="#dbeafe", linewidth=0, alpha=0.35)
    for path in sphere_paths:
        ax.plot(path[:, 0], path[:, 1], path[:, 2], lw=2.0)
    ax.set_title("Geodesics as straightest available paths")
    equalize_3d_axes(ax, sp[..., 0].ravel(), sp[..., 1].ravel(), sp[..., 2].ravel())
    checks["sphere_geodesic_speed_variation"] = float(np.std(np.linalg.norm(np.gradient(sphere_paths[0], axis=0), axis=1)))
    paths["geodesic_paths"] = save_figure(fig, unit, "figures", "sphere-geodesic-fan.png", root=root)
    plt.close(fig)

    angles = np.array([np.pi / 3, np.pi / 2, np.pi / 2])
    excess = float(np.sum(angles) - np.pi)
    checks["spherical_triangle_excess"] = excess
    checks["spherical_triangle_area_unit_sphere"] = excess
    fig, ax = plt.subplots(figsize=(6, 5.5))
    labels = ["A", "B", "C"]
    xy = np.array([[0.0, 0.0], [1.0, 0.0], [0.45, 0.85]])
    ax.fill(xy[:, 0], xy[:, 1], color="#bfdbfe", alpha=0.65)
    ax.plot(np.r_[xy[:, 0], xy[0, 0]], np.r_[xy[:, 1], xy[0, 1]], color=COURSE_COLORS["blue"], lw=2)
    for label, point, angle in zip(labels, xy, angles, strict=True):
        ax.text(point[0], point[1] + 0.05, f"{label}: {angle / np.pi:.2f} pi", ha="center")
    finish_axes(ax, "Gauss-Bonnet ledger: angle excess equals curvature area", "chart x", "chart y")
    paths["gauss_bonnet"] = save_figure(fig, unit, "figures", "gauss-bonnet-angle-excess-ledger.png", root=root)
    plt.close(fig)

    u, v = meshgrid((0.02, np.pi - 0.02), (0, 2 * np.pi), 60)
    sp = stack_surface(sphere, u, v)
    fig = go.Figure(data=[go.Surface(x=sp[..., 0], y=sp[..., 1], z=sp[..., 2], colorscale="Viridis", showscale=False)])
    fig.update_layout(title="Intrinsic paths on the sphere", scene={"aspectmode": "data"})
    paths["interactive"] = save_plotly_html(fig, unit, "interactive", "intrinsic-sphere-geodesics.html", root=root)
    return _finalize(unit, paths, checks)


def _chapter_05(root: Path) -> dict[str, Any]:
    unit = "chapter-05"
    paths: dict[str, Path] = {}
    checks: dict[str, Any] = {}

    def incomplete_metric(_t: float, y: np.ndarray) -> np.ndarray:
        x, v = y
        return np.array([v, 2 * x * v * v / (1 + x * x)])

    sol = solve_ivp(incomplete_metric, (0, 2.2), np.array([0.0, 1.0]), max_step=0.02, dense_output=True)
    t = sol.t
    x = sol.y[0]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.plot(t, x, color=COURSE_COLORS["red"], lw=2, label="metric edge reached quickly")
    ax.plot(t, t, color=COURSE_COLORS["slate"], ls="--", label="Euclidean reference")
    ax.set_title("Completeness is a global promise, not a local formula")
    ax.set_xlabel("geodesic time")
    ax.set_ylabel("coordinate distance")
    ax.legend()
    checks["incomplete_model_final_coordinate"] = float(x[-1])
    paths["completeness"] = save_figure(fig, unit, "figures", "complete-vs-incomplete-geodesic-clock.png", root=root)
    plt.close(fig)

    s = np.linspace(0.0, 2.0 * np.pi, 300)
    jacobi_positive = np.sin(s)
    jacobi_zero = s
    jacobi_negative = np.sinh(s) / np.sinh(2 * np.pi)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(s, jacobi_positive, label="K = +1: refocus", color=COURSE_COLORS["blue"])
    ax.plot(s, jacobi_zero / np.max(jacobi_zero), label="K = 0: linear spread", color=COURSE_COLORS["green"])
    ax.plot(s, jacobi_negative, label="K = -1: exponential spread", color=COURSE_COLORS["red"])
    ax.axhline(0, color="#94a3b8", lw=1)
    ax.set_title("Jacobi fields turn curvature into separation")
    ax.set_xlabel("geodesic parameter")
    ax.set_ylabel("normalized transverse separation")
    ax.legend()
    checks["jacobi_positive_second_zero"] = float(np.pi)
    paths["jacobi"] = save_figure(fig, unit, "figures", "jacobi-field-curvature-comparison.png", root=root)
    plt.close(fig)

    theta = np.linspace(0.0, 2 * np.pi, 500)
    knot = np.column_stack([(2 + np.cos(3 * theta)) * np.cos(2 * theta), (2 + np.cos(3 * theta)) * np.sin(2 * theta), np.sin(3 * theta)])
    tangent = np.gradient(knot, theta, axis=0)
    tangent = tangent / np.linalg.norm(tangent, axis=1, keepdims=True)
    total_turn = np.trapz(np.linalg.norm(np.gradient(tangent, theta, axis=0), axis=1), theta)
    checks["sample_total_curvature"] = float(total_turn)
    checks["fary_milnor_threshold"] = float(4 * np.pi)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(knot[:, 0], knot[:, 1], knot[:, 2], color=COURSE_COLORS["violet"], lw=2)
    ax.set_title("Total curvature sees global entanglement")
    equalize_3d_axes(ax, knot[:, 0], knot[:, 1], knot[:, 2])
    paths["total_curvature"] = save_figure(fig, unit, "figures", "total-curvature-knot-diagnostic.png", root=root)
    plt.close(fig)

    u, v = meshgrid((-2.0, 2.0), (0.0, 2 * np.pi), 70)
    cone = np.stack([u * np.cos(v), u * np.sin(v), 0.6 * u], axis=-1)
    cylinder = np.stack([np.cos(v) + 4.0, np.sin(v), u], axis=-1)
    fig = go.Figure()
    fig.add_trace(go.Surface(x=cone[..., 0], y=cone[..., 1], z=cone[..., 2], colorscale="Oranges", showscale=False, opacity=0.9))
    fig.add_trace(go.Surface(x=cylinder[..., 0], y=cylinder[..., 1], z=cylinder[..., 2], colorscale="Blues", showscale=False, opacity=0.9))
    fig.update_layout(title="Zero Gaussian curvature models: cone and cylinder", scene={"aspectmode": "data"})
    paths["interactive"] = save_plotly_html(fig, unit, "interactive", "zero-curvature-developable-surfaces.html", root=root)
    return _finalize(unit, paths, checks)
