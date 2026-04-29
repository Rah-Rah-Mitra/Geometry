"""Reusable chapter-specific visual constructors."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np

from utils.curves_surfaces import bezier_curve, torus_grid
from utils.geometry2d import barycentric_coordinates, convex_hull, polygon_area, project_point_segment
from utils.geometry3d import plane_from_points, project_point_plane
from utils.linear_algebra import rotation2d, rotation3d_axis_angle
from utils.plotting import PALETTE, add_note, set_axes_equal_3d, style_axis
from utils.robustness import robust_quadratic_roots


def concept_map_figure(title: str, concepts: list[str], visuals: list[str]):
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_axis_off()
    ax.set_title(f"{title}: concept-to-visual route", fontsize=14, color=PALETTE["ink"], pad=16)
    nodes = ["chapter goal", *[f"concept {i+1}" for i in range(len(concepts))], *[f"visual {i+1}" for i in range(len(visuals))], "sanity checks"]
    angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
    xy = np.c_[np.cos(angles), np.sin(angles)]
    for i, node in enumerate(nodes):
        x, y = xy[i]
        color = PALETTE["blue"] if "concept" in node else PALETTE["teal"] if "visual" in node else PALETTE["gold"]
        ax.scatter([x], [y], s=500, color=color, alpha=0.9, edgecolor="white", linewidth=1.5)
        ax.text(x, y, node, ha="center", va="center", color="white", fontsize=8, weight="bold")
    for i in range(1, len(nodes)):
        ax.plot([xy[0, 0], xy[i, 0]], [xy[0, 1], xy[i, 1]], color="#c7d0dd", linewidth=1)
    text_lines = ["Concepts:"] + [f"- {c}" for c in concepts] + ["", "Visuals:"] + [f"- {v}" for v in visuals]
    ax.text(-1.35, -1.35, "\n".join(text_lines), fontsize=8, va="bottom", color=PALETTE["ink"], wrap=True)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    return fig


def geometry_scene_figure(mode: str, title: str, seed: int):
    rng = np.random.default_rng(seed)
    if mode in {"primitives3d", "distance3d", "intersect3d", "misc3d", "formulas"}:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        if mode == "primitives3d":
            x, y, z = torus_grid()
            ax.plot_surface(x, y, z, alpha=0.55, color=PALETTE["teal"], linewidth=0)
            ax.quiver(0, 0, 0, 1.2, 0.3, 0.6, color=PALETTE["red"], label="plane normal")
            ax.set_title("Parametric torus and spatial frame")
        elif mode == "distance3d":
            tri = np.array([[0, 0, 0], [1.4, 0.2, 0], [0.2, 1.1, 0.25]])
            p = np.array([0.75, 0.45, 1.2])
            normal, d = plane_from_points(*tri)
            q = project_point_plane(p, normal, d)
            ax.plot_trisurf(tri[:, 0], tri[:, 1], tri[:, 2], triangles=[[0, 1, 2]], color=PALETTE["blue"], alpha=0.45)
            ax.scatter([p[0]], [p[1]], [p[2]], color=PALETTE["red"], s=60, label="query point")
            ax.scatter([q[0]], [q[1]], [q[2]], color=PALETTE["green"], s=60, label="plane projection")
            ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=PALETTE["red"], linewidth=2)
            ax.set_title("Point-to-triangle distance scaffold")
        elif mode == "intersect3d":
            corners = np.array([[-1,-1,-1],[-1,-1,1],[-1,1,-1],[-1,1,1],[1,-1,-1],[1,-1,1],[1,1,-1],[1,1,1]], float)
            ax.scatter(corners[:,0], corners[:,1], corners[:,2], color=PALETTE["blue"], s=25)
            ray0 = np.array([-1.8, -0.4, 0.2]); ray1 = np.array([1.6, 0.9, 0.55])
            ax.plot([ray0[0], ray1[0]], [ray0[1], ray1[1]], [ray0[2], ray1[2]], color=PALETTE["red"], linewidth=2, label="ray")
            ax.set_title("Ray-box slab interval geometry")
        elif mode == "misc3d":
            xx, yy = np.meshgrid(np.linspace(-1, 1, 8), np.linspace(-1, 1, 8))
            zz = 0.25 * xx - 0.15 * yy
            ax.plot_surface(xx, yy, zz, alpha=0.45, color=PALETTE["blue"])
            p = np.array([0.5, 0.5, 1.1]); n = np.array([-0.25, 0.15, 1.0]); n = n / np.linalg.norm(n)
            q = p - (np.dot(n, p)) * n
            ax.scatter([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=[PALETTE["red"], PALETTE["green"]], s=60)
            ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=PALETTE["red"])
            ax.set_title("Projection onto a plane")
        else:
            x, y, z = torus_grid(1.2, 0.3)
            ax.plot_surface(x, y, z, alpha=0.55, color=PALETTE["violet"], linewidth=0)
            ax.set_title("Formula atlas surface sample")
        ax.legend(loc="upper left")
        set_axes_equal_3d(ax)
        return fig

    fig, ax = plt.subplots(figsize=(8, 6))
    if mode == "linear":
        grid = np.linspace(-1, 1, 9)
        a = np.array([[1.2, 0.55], [-0.25, 0.8]])
        for g in grid:
            pts = np.array([[g, -1], [g, 1], [-1, g], [1, g]], float)
            out = pts @ a.T
            ax.plot(out[:2, 0], out[:2, 1], color="#b7c3d0", linewidth=0.8)
            ax.plot(out[2:, 0], out[2:, 1], color="#b7c3d0", linewidth=0.8)
        square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float) @ a.T
        ax.plot(square[:,0], square[:,1], color=PALETTE["red"], linewidth=2)
        add_note(ax, f"determinant area scale = {np.linalg.det(a):.3f}")
        style_axis(ax, "Linear map deforms a coordinate grid", equal=True)
    elif mode == "vector":
        tri = np.array([[0, 0], [1.5, 0.2], [0.35, 1.25]])
        p = np.array([0.65, 0.45])
        w = barycentric_coordinates(p, tri)
        ax.fill(tri[:,0], tri[:,1], color=PALETTE["blue"], alpha=0.18)
        ax.scatter(tri[:,0], tri[:,1], color=PALETTE["blue"], s=70)
        ax.scatter([p[0]], [p[1]], color=PALETTE["red"], s=70)
        for v in tri:
            ax.plot([p[0], v[0]], [p[1], v[1]], color="#98a6b3", linestyle="--")
        add_note(ax, "barycentric weights: " + ", ".join(f"{x:.2f}" for x in w))
        style_axis(ax, "Affine coordinates inside a simplex", equal=True)
    elif mode == "transform":
        pts = np.array([[0,0],[1,0],[1,0.6],[0,0.6],[0,0]], float)
        a = rotation2d(0.55) @ np.array([[1.4, 0.35], [0.0, 0.75]])
        out = pts @ a.T + np.array([0.3, 0.2])
        ax.plot(pts[:,0], pts[:,1], color=PALETTE["gray"], linewidth=2, label="source")
        ax.plot(out[:,0], out[:,1], color=PALETTE["red"], linewidth=2, label="transformed")
        ax.quiver([out[1,0]], [out[1,1]], [a[0,0]], [a[0,1]], angles="xy", scale_units="xy", scale=1, color=PALETTE["green"])
        ax.legend()
        style_axis(ax, "Affine transform and tangent direction", equal=True)
    elif mode == "primitives2d":
        control = np.array([[-1, -0.4], [-0.4, 1.1], [0.8, -0.9], [1.2, 0.45]])
        curve = bezier_curve(control)
        theta = np.linspace(0, 2*np.pi, 160)
        ax.plot(np.cos(theta)*0.5-0.6, np.sin(theta)*0.35-0.1, color=PALETTE["gold"], label="conic sample")
        ax.plot(control[:,0], control[:,1], "--o", color=PALETTE["gray"], label="control polygon")
        ax.plot(curve[:,0], curve[:,1], color=PALETTE["blue"], linewidth=2, label="Bezier curve")
        ax.legend()
        style_axis(ax, "2D primitive representations", equal=True)
    elif mode == "distance2d":
        a = np.array([-0.9, -0.35]); b = np.array([1.1, 0.35]); p = np.array([0.2, 1.0])
        q, t = project_point_segment(p, a, b)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=PALETTE["blue"], linewidth=3)
        ax.scatter([p[0], q[0]], [p[1], q[1]], color=[PALETTE["red"], PALETTE["green"]], s=70)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=PALETTE["red"], linestyle="--")
        add_note(ax, f"clamped parameter t = {t:.3f}")
        style_axis(ax, "Closest point on a segment", equal=True)
    elif mode == "intersect2d":
        poly_a = np.array([[-0.8,-0.5],[0.4,-0.7],[0.9,0.2],[-0.2,0.8]])
        poly_b = poly_a @ rotation2d(0.7).T + np.array([0.5, 0.1])
        for poly, color, label in [(poly_a, PALETTE["blue"], "A"), (poly_b, PALETTE["red"], "B")]:
            closed = np.vstack([poly, poly[0]])
            ax.plot(closed[:,0], closed[:,1], color=color, linewidth=2, label=label)
        axis = np.array([0.85, 0.35]); axis = axis / np.linalg.norm(axis)
        ax.arrow(-1.2*axis[0], -1.2*axis[1], 2.4*axis[0], 2.4*axis[1], color=PALETTE["green"], width=0.01)
        ax.legend()
        style_axis(ax, "Separating-axis projection direction", equal=True)
    elif mode == "misc2d":
        c1, c2 = np.array([-0.45, 0.0]), np.array([0.65, 0.05])
        for center, r, color in [(c1, 0.5, PALETTE["blue"]), (c2, 0.35, PALETTE["teal"])]:
            circ = plt.Circle(center, r, fill=False, color=color, linewidth=2)
            ax.add_patch(circ)
        ax.plot([c1[0], c2[0]], [0.5, 0.4], color=PALETTE["red"], linewidth=2, label="external tangent")
        ax.legend()
        style_axis(ax, "Circle tangent construction", equal=True)
    elif mode == "compgeom":
        pts = rng.normal(size=(24, 2))
        pts[:, 0] *= 1.2
        hull = convex_hull(pts)
        closed = np.vstack([hull, hull[0]])
        ax.scatter(pts[:,0], pts[:,1], color=PALETTE["gray"], s=25)
        ax.fill(closed[:,0], closed[:,1], color=PALETTE["blue"], alpha=0.18)
        ax.plot(closed[:,0], closed[:,1], color=PALETTE["blue"], linewidth=2)
        add_note(ax, f"hull vertices = {len(hull)}")
        style_axis(ax, "Convex hull as an extreme-point summary", equal=True)
    elif mode == "numerical":
        x = np.linspace(-2, 2, 300)
        y = (x - 0.15) ** 2 + 0.1 * np.sin(8 * x)
        ax.plot(x, y, color=PALETTE["blue"])
        ax.scatter([x[np.argmin(y)]], [y.min()], color=PALETTE["red"], s=70, label="sample minimum")
        ax.legend()
        style_axis(ax, "Root and minimization diagnostics")
    elif mode == "trig":
        t = np.linspace(-np.pi, np.pi, 300)
        ax.plot(t, np.sin(t), label="sin", color=PALETTE["blue"])
        ax.plot(t, np.cos(t), label="cos", color=PALETTE["red"])
        ax.legend()
        style_axis(ax, "Trigonometric functions as geometric coordinates")
    elif mode == "introduction":
        xs = np.array([1e8, 1.0, -1e8])
        naive = (xs[0] + xs[1]) + xs[2]
        stable = xs[0] + (xs[1] + xs[2])
        ax.bar(["(a+b)+c", "a+(b+c)"], [naive, stable], color=[PALETTE["red"], PALETTE["blue"]])
        ax.axhline(1.0, color=PALETTE["green"], linestyle="--", label="exact real sum")
        ax.legend()
        style_axis(ax, "Floating-point order dependence")
    else:
        tri = np.array([[0,0],[1.2,0.1],[0.25,0.95]])
        area = abs(polygon_area(tri))
        ax.fill(tri[:,0], tri[:,1], color=PALETTE["violet"], alpha=0.25)
        ax.scatter(tri[:,0], tri[:,1], color=PALETTE["violet"])
        add_note(ax, f"determinant area = {area:.3f}")
        style_axis(ax, "Primitive formula diagram", equal=True)
    fig.suptitle(title, fontsize=13, color=PALETTE["ink"])
    return fig


def numerical_experiment_figure(mode: str, title: str, seed: int):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0.02, 1.0, 160)
    if mode == "introduction":
        b = np.linspace(2.1, 80.0, len(x))
        residual = []
        for scale in b:
            roots = robust_quadratic_roots(1.0, -scale, 1.0)
            residual.append(max(abs(r*r - scale*r + 1.0) / (abs(r*r) + abs(scale*r) + 1.0) for r in roots))
        ax.semilogy(b, residual, color=PALETTE["red"])
        ax.set_xlabel("coefficient scale")
        ax.set_ylabel("root residual")
    elif mode in {"linear", "transform"}:
        theta = np.linspace(0, np.pi, len(x))
        dets = 0.4 + 1.2 * np.abs(np.sin(theta + 0.2))
        cond = 1 + 8 * np.abs(np.cos(theta))
        ax.plot(theta, dets, label="area scale", color=PALETTE["blue"])
        ax.plot(theta, cond, label="condition indicator", color=PALETTE["red"])
        ax.legend()
    elif mode in {"distance2d", "distance3d"}:
        t = np.linspace(-0.5, 1.5, len(x))
        dist = (np.clip(t, 0, 1) - 0.42) ** 2 + 0.12
        ax.plot(t, dist, color=PALETTE["blue"])
        ax.axvspan(0, 1, alpha=0.12, color=PALETTE["green"], label="valid parameter domain")
        ax.legend()
    elif mode in {"intersect2d", "intersect3d"}:
        time = np.linspace(0, 1, len(x))
        sep = 0.35 - np.sin(np.pi * time) * 0.55
        ax.plot(time, sep, color=PALETTE["red"])
        ax.axhline(0, color=PALETTE["ink"], linestyle="--", label="contact threshold")
        ax.legend()
    elif mode == "trig":
        t = np.linspace(0, 2 * np.pi, len(x))
        ax.plot(t, np.sin(t) ** 2 + np.cos(t) ** 2, color=PALETTE["blue"])
        ax.set_ylim(0.95, 1.05)
    else:
        n = np.arange(3, 3 + len(x))
        error = 1 / (n ** 1.3)
        ax.loglog(n, error, color=PALETTE["teal"])
        ax.set_xlabel("sample count")
        ax.set_ylabel("diagnostic error")
    style_axis(ax, f"{title}: numeric diagnostic")
    return fig


def storyboard_gallery_figure(mode: str, title: str, visuals: list[str], seed: int):
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    rng = np.random.default_rng(seed + 100)
    t = np.linspace(0, 1, 120)
    for index, (ax, label) in enumerate(zip(axes.ravel(), visuals)):
        phase = 0.6 * index + 0.2 * seed
        if "3d" in mode or mode in {"primitives3d", "distance3d", "intersect3d", "misc3d"}:
            x = np.cos(2 * np.pi * t + phase)
            y = np.sin(2 * np.pi * t + phase)
            ax.plot(x, y, color=PALETTE["blue"], linewidth=2)
            ax.scatter(x[::25], y[::25], color=PALETTE["red"], s=25)
            ax.arrow(0, 0, 0.65 * np.cos(phase), 0.65 * np.sin(phase), color=PALETTE["green"], width=0.015)
        elif mode in {"distance2d", "intersect2d", "misc2d", "primitives2d", "compgeom"}:
            pts = rng.normal(size=(6, 2)) * 0.35
            hull = convex_hull(pts)
            if len(hull) >= 3:
                closed = np.vstack([hull, hull[0]])
                ax.fill(closed[:, 0], closed[:, 1], color=PALETTE["teal"], alpha=0.18)
                ax.plot(closed[:, 0], closed[:, 1], color=PALETTE["teal"], linewidth=2)
            ax.scatter(pts[:, 0], pts[:, 1], color=PALETTE["ink"], s=18)
            ax.plot([-0.8, 0.8], [0.2 * np.sin(phase), -0.2 * np.sin(phase)], color=PALETTE["red"], linestyle="--")
        elif mode == "trig":
            angle = np.linspace(0, 2 * np.pi, 120)
            ax.plot(angle, np.sin(angle + phase), color=PALETTE["blue"])
            ax.plot(angle, np.cos(angle + phase), color=PALETTE["red"], alpha=0.75)
        elif mode == "linear" or mode == "transform":
            square = np.array([[0,0],[1,0],[1,1],[0,1],[0,0]], float) - 0.5
            a = rotation2d(phase) @ np.array([[1.0 + 0.1 * index, 0.25], [0.0, 0.7 + 0.05 * index]])
            out = square @ a.T
            ax.plot(square[:, 0], square[:, 1], color=PALETTE["gray"], linestyle=":")
            ax.plot(out[:, 0], out[:, 1], color=PALETTE["blue"], linewidth=2)
        else:
            y = np.exp(-3 * t) * np.cos(8 * np.pi * t + phase)
            ax.plot(t, y, color=PALETTE["violet"], linewidth=2)
            ax.axhline(0, color="#c7d0dd", linewidth=1)
        style_axis(ax, label[:58], equal=mode not in {"trig", "numerical"})
    fig.suptitle(f"{title}: storyboard gallery", fontsize=13, color=PALETTE["ink"])
    fig.tight_layout()
    return fig


def _segment_intersects(a, b, c, d) -> bool:
    def orient(p, q, r):
        return np.sign((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))

    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    return bool(o1 * o2 <= 0 and o3 * o4 <= 0)


def compute_check_values(mode: str) -> dict[str, float | int | str | bool]:
    tolerance = 1e-9
    if mode == "introduction":
        roots = robust_quadratic_roots(1.0, -1e8, 1.0)
        residual = max(abs(r * r - 1e8 * r + 1.0) / (abs(r * r) + abs(1e8 * r) + 1.0) for r in roots)
        assert residual < 1e-12
        return {"invariant": "stable quadratic relative residual", "max_error": float(residual), "tolerance": 1e-12}

    if mode == "linear":
        a = np.array([[1.2, 0.55], [-0.25, 0.8]])
        unit_square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        mapped = unit_square @ a.T
        area = abs(polygon_area(mapped))
        det_area = abs(np.linalg.det(a))
        error = abs(area - det_area)
        q, r = np.linalg.qr(a)
        reconstruction = np.linalg.norm(q @ r - a)
        assert error < tolerance and reconstruction < tolerance
        return {"invariant": "determinant area and QR reconstruction", "max_error": float(max(error, reconstruction)), "tolerance": tolerance, "rank": int(np.linalg.matrix_rank(a))}

    if mode == "vector":
        tri = np.array([[0, 0], [1, 0], [0.2, 1]])
        point = np.array([0.35, 0.3])
        weights = barycentric_coordinates(point, tri)
        reconstructed = weights @ tri
        error = max(abs(weights.sum() - 1.0), float(np.linalg.norm(reconstructed - point)))
        assert error < tolerance
        return {"invariant": "barycentric reconstruction", "max_error": float(error), "tolerance": tolerance, "min_weight": float(weights.min())}

    if mode == "transform":
        tangent = np.array([1.0, 0.0, 0.0])
        bitangent = np.array([0.0, 1.0, 0.0])
        normal = np.cross(tangent, bitangent)
        a = np.array([[1.4, 0.2, 0.0], [0.0, 0.7, 0.3], [0.1, 0.0, 1.2]])
        transformed_tangent = a @ tangent
        transformed_bitangent = a @ bitangent
        corrected_normal = np.linalg.inv(a).T @ normal
        error = max(abs(np.dot(corrected_normal, transformed_tangent)), abs(np.dot(corrected_normal, transformed_bitangent)))
        assert error < tolerance
        return {"invariant": "inverse-transpose normal remains perpendicular", "max_error": float(error), "tolerance": tolerance}

    if mode == "primitives2d":
        point = np.array([0.25, 0.5])
        line_point = np.array([0.0, 0.0])
        direction = np.array([1.0, 2.0])
        normal = np.array([-direction[1], direction[0]])
        implicit_residual = abs(np.dot(normal, point - line_point))
        control = np.array([[0, 0], [0.2, 0.8], [0.8, -0.2], [1, 0]])
        curve = bezier_curve(control, samples=20)
        endpoint_error = max(float(np.linalg.norm(curve[0] - control[0])), float(np.linalg.norm(curve[-1] - control[-1])))
        assert implicit_residual < tolerance and endpoint_error < tolerance
        return {"invariant": "parametric line and Bezier endpoints", "max_error": float(max(implicit_residual, endpoint_error)), "tolerance": tolerance}

    if mode == "distance2d":
        a = np.array([-1.0, 0.0])
        b = np.array([1.0, 0.0])
        p = np.array([0.25, 0.75])
        q, t = project_point_segment(p, a, b)
        perpendicular_error = abs(np.dot(p - q, b - a))
        assert 0 <= t <= 1 and perpendicular_error < tolerance
        return {"invariant": "closest point is in the segment domain and perpendicular", "max_error": float(perpendicular_error), "tolerance": tolerance, "parameter": float(t)}

    if mode == "intersect2d":
        a = np.array([0.0, 0.0]); b = np.array([1.0, 1.0])
        c = np.array([0.0, 1.0]); d = np.array([1.0, 0.0])
        forward = _segment_intersects(a, b, c, d)
        reverse = _segment_intersects(c, d, a, b)
        assert forward and forward == reverse
        return {"invariant": "segment intersection is symmetric", "max_error": 0.0, "tolerance": tolerance, "symmetric": bool(forward == reverse)}

    if mode == "misc2d":
        pts = np.array([[0.0, 1.0], [-0.8660254, -0.5], [0.8660254, -0.5]])
        center = pts.mean(axis=0)
        radii = np.linalg.norm(pts - center, axis=1)
        error = float(radii.max() - radii.min())
        assert error < 1e-6
        return {"invariant": "constructed circle has equal radii to constraints", "max_error": error, "tolerance": 1e-6}

    if mode == "primitives3d":
        x, y, z = torus_grid(1.4, 0.35, 12, 10)
        radial = np.sqrt(x * x + y * y)
        implicit = (radial - 1.4) ** 2 + z * z - 0.35 ** 2
        error = float(np.max(np.abs(implicit)))
        assert error < 1e-12
        return {"invariant": "torus samples satisfy implicit equation", "max_error": error, "tolerance": 1e-12}

    if mode == "distance3d":
        tri = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
        p = np.array([0.25, 0.25, 1.0])
        n, d = plane_from_points(*tri)
        q = project_point_plane(p, n, d)
        tangential_error = np.linalg.norm(np.cross(p - q, n))
        assert tangential_error < tolerance
        return {"invariant": "point-plane distance residual is normal", "max_error": float(tangential_error), "tolerance": tolerance}

    if mode == "intersect3d":
        ray0 = np.array([-2.0, 0.25, 0.0])
        rayd = np.array([1.0, 0.0, 0.0])
        box_min = np.array([-1.0, -1.0, -1.0])
        box_max = np.array([1.0, 1.0, 1.0])
        t0 = np.max((box_min - ray0) / rayd)
        t1 = np.min((box_max - ray0) / rayd)
        assert t0 <= t1 and abs((ray0 + t0 * rayd)[0] + 1.0) < tolerance
        return {"invariant": "ray-box slab interval is ordered", "max_error": float(abs((ray0 + t0 * rayd)[0] + 1.0)), "tolerance": tolerance, "entry_t": float(t0), "exit_t": float(t1)}

    if mode == "misc3d":
        n = np.array([0.0, 0.0, 1.0])
        p = np.array([0.2, -0.4, 1.3])
        q = project_point_plane(p, n, 0.0)
        projection_error = np.linalg.norm(q[:2] - p[:2]) + abs(q[2])
        assert projection_error < tolerance
        return {"invariant": "plane projection preserves tangential coordinates", "max_error": float(projection_error), "tolerance": tolerance}

    if mode == "compgeom":
        pts = np.array([[0,0], [1,0], [0.7,0.6], [0.2,0.8], [0.4,0.3]])
        hull = convex_hull(pts)
        area = polygon_area(hull)
        shifted_area = polygon_area(np.roll(hull, 1, axis=0))
        error = abs(area - shifted_area)
        assert error < tolerance
        return {"invariant": "polygon area invariant under cyclic vertex shift", "max_error": float(error), "tolerance": tolerance, "hull_vertices": int(len(hull))}

    if mode == "numerical":
        roots = robust_quadratic_roots(1.0, -1e6, 1.0)
        residual = max(abs(r * r - 1e6 * r + 1.0) / (abs(r * r) + abs(1e6 * r) + 1.0) for r in roots)
        matrix = np.array([[3.0, 1.0], [0.0, 0.25]])
        u, s, vt = np.linalg.svd(matrix)
        svd_error = np.linalg.norm(u @ np.diag(s) @ vt - matrix)
        error = max(float(residual), float(svd_error))
        assert error < 1e-10
        return {"invariant": "stable roots and SVD reconstruction", "max_error": error, "tolerance": 1e-10}

    if mode == "trig":
        t = np.linspace(0, 2 * np.pi, 100)
        identity_error = float(np.max(np.abs(np.sin(t) ** 2 + np.cos(t) ** 2 - 1)))
        a, b, gamma = 3.0, 4.0, np.pi / 3
        c = math.sqrt(a*a + b*b - 2*a*b*math.cos(gamma))
        reconstructed = math.acos((a*a + b*b - c*c) / (2*a*b))
        error = max(identity_error, abs(reconstructed - gamma))
        assert error < tolerance
        return {"invariant": "trig identity and law of cosines", "max_error": float(error), "tolerance": tolerance}

    if mode == "formulas":
        tri = np.array([[0, 0], [3, 0], [0, 4]], dtype=float)
        det_area = abs(polygon_area(tri))
        sides = np.array([3.0, 4.0, 5.0])
        semiperimeter = sides.sum() / 2
        heron = math.sqrt(np.prod(semiperimeter - sides) * semiperimeter)
        error = abs(det_area - heron)
        assert error < tolerance
        return {"invariant": "triangle area formulas agree", "max_error": float(error), "tolerance": tolerance}

    raise ValueError(f"unknown chapter visual mode: {mode}")
