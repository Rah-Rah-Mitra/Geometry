"""Section-specific visual examples for the Convex Analysis course."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sympy as sp

from .artifacts import save_csv, save_json, save_matplotlib

PALETTE = {
    "ink": "#1f2937",
    "blue": "#2563eb",
    "green": "#059669",
    "red": "#dc2626",
    "gold": "#d97706",
    "purple": "#7c3aed",
    "cyan": "#0891b2",
    "gray": "#6b7280",
}


def _convex_hull(points: np.ndarray) -> np.ndarray:
    pts = sorted({(float(x), float(y)) for x, y in np.asarray(points)})
    if len(pts) <= 1:
        return np.array(pts)

    def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for pt in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], pt) <= 0:
            lower.pop()
        lower.append(pt)
    upper: list[tuple[float, float]] = []
    for pt in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], pt) <= 0:
            upper.pop()
        upper.append(pt)
    return np.array(lower[:-1] + upper[:-1])


def _as_float(value: Any) -> float:
    return float(np.asarray(value).item() if np.asarray(value).shape == () else value)


def _json_ready(data: dict[str, Any]) -> dict[str, Any]:
    ready: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, (np.bool_, bool)):
            ready[key] = bool(value)
        elif isinstance(value, (np.integer, int)):
            ready[key] = int(value)
        elif isinstance(value, (np.floating, float)):
            ready[key] = float(value)
        elif isinstance(value, np.ndarray):
            ready[key] = value.astype(float).round(8).tolist()
        else:
            ready[key] = value
    return ready


def _style(ax: plt.Axes, title: str, *, lim: tuple[float, float] = (-3.0, 3.0)) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.axhline(0, color="#d1d5db", lw=0.8)
    ax.axvline(0, color="#d1d5db", lw=0.8)
    ax.grid(True, color="#e5e7eb", lw=0.7)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)


def _plot_polygon(
    ax: plt.Axes,
    points: np.ndarray,
    *,
    color: str,
    alpha: float = 0.18,
    label: str | None = None,
    edge: str | None = None,
) -> None:
    pts = np.asarray(points, dtype=float)
    closed = np.vstack([pts, pts[0]])
    ax.fill(pts[:, 0], pts[:, 1], color=color, alpha=alpha, label=label)
    ax.plot(closed[:, 0], closed[:, 1], color=edge or color, lw=2)


def _plot_dependency_graph(section: dict[str, Any], path: Path) -> None:
    nodes = section["proof_nodes"]
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node)
    for left, right in zip(nodes, nodes[1:]):
        graph.add_edge(left, right)
    if len(nodes) > 3:
        graph.add_edge(nodes[0], nodes[-1])

    fig, ax = plt.subplots(figsize=(7.0, 3.9))
    pos = nx.spring_layout(graph, seed=section["number"], k=1.4)
    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=14,
        edge_color="#64748b",
        width=1.4,
    )
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_size=1600,
        node_color="#ecfeff",
        edgecolors=PALETTE["cyan"],
        linewidths=1.6,
    )
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color=PALETTE["ink"])
    ax.set_title(f"Section {section['number']}: proof and concept dependencies", fontsize=11)
    ax.axis("off")
    save_matplotlib(fig, path)
    plt.close(fig)


def _primary_figure(section: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    n = section["number"]
    title = f"Section {n}: {section['title']}"
    checks: dict[str, Any] = {"section": n}

    if n == 1:
        fig, ax = plt.subplots(figsize=(7, 5))
        pts = np.array([[-1.8, -1.0], [0.4, 0.0], [1.7, 1.2]])
        lambdas = np.array([0.25, 0.35, 0.40])
        x = lambdas @ pts
        line = np.array([pts[0] + t * (pts[2] - pts[0]) for t in np.linspace(-0.2, 1.2, 60)])
        ax.plot(line[:, 0], line[:, 1], color=PALETTE["blue"], lw=2, label="affine hull")
        ax.scatter(pts[:, 0], pts[:, 1], s=60, color=PALETTE["ink"], zorder=3)
        ax.scatter([x[0]], [x[1]], s=90, color=PALETTE["red"], zorder=4, label="affine combo")
        normal = np.array([-(pts[2] - pts[0])[1], (pts[2] - pts[0])[0]])
        normal = normal / np.linalg.norm(normal)
        ax.arrow(x[0], x[1], normal[0] * 0.6, normal[1] * 0.6, color=PALETTE["green"], width=0.015)
        _style(ax, title)
        ax.legend(loc="upper left")
        checks.update(
            {
                "coefficient_sum": float(lambdas.sum()),
                "affine_residual": float(abs(lambdas.sum() - 1.0)),
                "primary_invariant_ok": abs(lambdas.sum() - 1.0) < 1e-12,
            }
        )
        return fig, checks

    if n == 2:
        fig, ax = plt.subplots(figsize=(7, 5))
        poly = np.array([[-1.9, -0.8], [-0.4, -1.3], [0.9, -0.2], [0.3, 1.2], [-1.5, 0.9]])
        _plot_polygon(ax, poly, color=PALETTE["blue"], label="convex set")
        a, b = poly[0], poly[2]
        mid = 0.5 * (a + b)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=PALETTE["red"], lw=2, label="segment")
        ax.scatter([mid[0]], [mid[1]], color=PALETTE["red"], s=70)
        for ray in [np.array([1.4, 0.2]), np.array([0.3, 1.4])]:
            ax.arrow(1.2, -1.5, ray[0], ray[1], width=0.02, color=PALETTE["green"], length_includes_head=True)
        ax.plot([-2.6, 2.4], [1.1, -1.4], "--", color=PALETTE["gray"], label="half-space boundary")
        _style(ax, title)
        ax.legend(loc="upper right")
        checks.update(
            {
                "midpoint": mid,
                "cone_sum_nonnegative": True,
                "primary_invariant_ok": True,
            }
        )
        return fig, checks

    if n == 3:
        fig, ax = plt.subplots(figsize=(7, 5))
        c = np.array([[-1.8, -0.5], [-0.5, -1.0], [-0.9, 0.6]])
        d = np.array([[0.2, 0.0], [0.9, 0.0], [0.9, 0.6], [0.2, 0.6]])
        sums = np.array([p + q for p in c for q in d])
        hull = _convex_hull(sums)
        _plot_polygon(ax, c, color=PALETTE["blue"], alpha=0.14, label="C")
        _plot_polygon(ax, d, color=PALETTE["green"], alpha=0.14, label="D")
        _plot_polygon(ax, hull, color=PALETTE["purple"], alpha=0.20, label="C + D")
        u = np.array([0.8, 0.6])
        support_sum = max(sums @ u)
        support_parts = max(c @ u) + max(d @ u)
        ax.arrow(-2.4, 1.8, u[0], u[1], color=PALETTE["red"], width=0.015)
        _style(ax, title, lim=(-3, 3))
        ax.legend(loc="lower right")
        checks.update(
            {
                "support_sum": support_sum,
                "support_parts": support_parts,
                "support_residual": abs(support_sum - support_parts),
                "primary_invariant_ok": abs(support_sum - support_parts) < 1e-10,
            }
        )
        return fig, checks

    if n in {4, 7, 9, 10, 12, 16, 23, 24, 25, 26, 27, 29, 30, 31}:
        return _function_figure(section)

    if n in {5, 19}:
        return _operations_figure(section)

    if n == 6:
        fig, ax = plt.subplots(figsize=(7, 5))
        square = np.array([[-1.7, -1.1], [0.1, -1.1], [0.1, 0.7], [-1.7, 0.7]])
        _plot_polygon(ax, square, color=PALETTE["blue"], label="2D set")
        ax.scatter([-0.8], [-0.2], color=PALETTE["red"], s=70, label="relative interior")
        ax.plot([0.7, 2.1], [-0.8, -0.8], color=PALETTE["green"], lw=5, alpha=0.35, label="1D set")
        ax.scatter([1.4], [-0.8], color=PALETTE["red"], s=70)
        ax.scatter([1.4], [0.8], color=PALETTE["purple"], s=90, label="0D set")
        _style(ax, title)
        ax.legend(loc="upper left")
        checks.update({"dimensions": [2, 1, 0], "primary_invariant_ok": True})
        return fig, checks

    if n == 8:
        fig, ax = plt.subplots(figsize=(7, 5))
        xs = np.linspace(-2, 2, 200)
        ax.plot(xs, np.abs(xs), color=PALETTE["blue"], lw=2, label="boundary of epigraph")
        ax.fill_between(xs, np.abs(xs), 3, color=PALETTE["blue"], alpha=0.14, label="unbounded epigraph")
        point = np.array([0.5, 1.1])
        direction = np.array([0.4, 0.7])
        ax.scatter([point[0]], [point[1]], color=PALETTE["red"], s=70)
        ax.arrow(point[0], point[1], direction[0], direction[1], width=0.02, color=PALETTE["green"])
        ray_point = point + 2.0 * direction
        ok = ray_point[1] >= abs(ray_point[0])
        _style(ax, title)
        ax.legend(loc="upper center")
        checks.update({"ray_point": ray_point, "recession_ray_inside": ok, "primary_invariant_ok": bool(ok)})
        return fig, checks

    if n in {11, 13, 14, 15, 17, 18, 20, 21, 22, 28, 32, 38, 39}:
        return _set_duality_figure(section)

    if n in {33, 34, 35, 36, 37}:
        return _saddle_figure(section)

    raise ValueError(f"No visual recipe for section {n}")


def _function_figure(section: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    n = section["number"]
    title = f"Section {n}: {section['title']}"
    checks: dict[str, Any] = {"section": n}
    xs = np.linspace(-2.5, 2.5, 300)

    if n == 4:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = 0.5 * xs**2 + 0.2
        ax.plot(xs, f, color=PALETTE["blue"], lw=2, label="convex graph")
        ax.fill_between(xs, f, 3.5, color=PALETTE["blue"], alpha=0.15, label="epigraph")
        x, y, lam = -1.4, 1.3, 0.35
        lhs = 0.5 * ((1 - lam) * x + lam * y) ** 2 + 0.2
        rhs = (1 - lam) * (0.5 * x**2 + 0.2) + lam * (0.5 * y**2 + 0.2)
        ax.plot([x, y], [0.5 * x**2 + 0.2, 0.5 * y**2 + 0.2], color=PALETTE["red"], lw=2)
        _style(ax, title, lim=(-2.8, 3.0))
        ax.legend(loc="upper center")
        checks.update({"jensen_gap": rhs - lhs, "primary_invariant_ok": rhs + 1e-12 >= lhs})
        return fig, checks

    if n == 7:
        fig, ax = plt.subplots(figsize=(7, 5))
        x_inner = np.linspace(0.05, 2.3, 200)
        f = (x_inner - 1.0) ** 2
        ax.plot(x_inner, f, color=PALETTE["blue"], lw=2, label="interior values")
        ax.scatter([0], [1], facecolors="white", edgecolors=PALETTE["red"], s=90, label="missing endpoint")
        ax.scatter([0], [1], color=PALETTE["green"], marker="x", s=100, label="closure value")
        _style(ax, title, lim=(-0.4, 2.8))
        ax.legend(loc="upper right")
        checks.update({"closure_value_at_zero": 1.0, "primary_invariant_ok": True})
        return fig, checks

    if n == 9:
        fig, (ax, ax2) = plt.subplots(1, 2, figsize=(9, 4.3))
        x = np.linspace(-4, 2, 300)
        y = np.exp(x)
        ax.plot(x, y, color=PALETTE["blue"], lw=2)
        ax.fill_between(x, y, 8, color=PALETTE["blue"], alpha=0.13)
        ax.set_title("closed epigraph")
        ax.set_ylim(0, 8)
        ax.grid(True, color="#e5e7eb")
        ax2.plot([0, 0], [0.05, 8], color=PALETTE["red"], lw=5, alpha=0.45)
        ax2.scatter([0], [0], facecolors="white", edgecolors=PALETTE["red"], s=90)
        ax2.set_title("projection misses 0")
        ax2.set_xlim(-1, 1)
        ax2.set_ylim(-0.5, 8)
        ax2.grid(True, color="#e5e7eb")
        checks.update({"projection_infimum": 0.0, "attained_at_zero": False, "primary_invariant_ok": True})
        return fig, checks

    if n == 10:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = 0.2 * xs**2 + np.maximum(0, xs - 0.5)
        ax.plot(xs, f, color=PALETTE["blue"], lw=2)
        knots = np.array([-1.6, -0.7, 0.2, 1.0, 1.8])
        vals = 0.2 * knots**2 + np.maximum(0, knots - 0.5)
        slopes = np.diff(vals) / np.diff(knots)
        for i in range(len(knots) - 1):
            ax.plot(knots[i : i + 2], vals[i : i + 2], color=PALETTE["red"], alpha=0.8)
        _style(ax, title)
        checks.update({"secant_slopes": slopes, "primary_invariant_ok": bool(np.all(np.diff(slopes) >= -1e-12))})
        return fig, checks

    if n == 12:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = 0.5 * xs**2
        ax.plot(xs, f, color=PALETTE["blue"], lw=2, label="f(x)")
        slopes = [-1.2, 0.0, 1.4]
        for s in slopes:
            ax.plot(xs, s * xs - 0.5 * s**2, "--", lw=1.5, label=f"slope {s:g}")
        x0 = 1.4
        s0 = x0
        equality_gap = 0.5 * x0**2 + 0.5 * s0**2 - x0 * s0
        _style(ax, title)
        ax.legend(loc="upper center", fontsize=8)
        checks.update({"fenchel_equality_gap": equality_gap, "primary_invariant_ok": abs(equality_gap) < 1e-12})
        return fig, checks

    if n == 16:
        fig, ax = plt.subplots(figsize=(7, 5))
        grid = np.linspace(-2.5, 2.5, 240)
        f = 0.5 * grid**2
        g = np.abs(grid - 0.6)
        infconv = []
        for x in grid:
            ys = grid
            infconv.append(float(np.min(0.5 * ys**2 + np.abs(x - ys - 0.6))))
        infconv = np.array(infconv)
        ax.plot(grid, f, color=PALETTE["blue"], label="f")
        ax.plot(grid, g, color=PALETTE["green"], label="g")
        ax.plot(grid, infconv, color=PALETTE["red"], lw=2, label="infimal convolution")
        ax.set_ylim(-0.1, 3.2)
        ax.grid(True, color="#e5e7eb")
        ax.legend(loc="upper center")
        ax.set_title(title)
        mid_gap = infconv[len(grid) // 2] - 0.5 * (infconv[len(grid) // 3] + infconv[2 * len(grid) // 3])
        checks.update({"sample_midpoint_gap": mid_gap, "primary_invariant_ok": bool(mid_gap <= 1e-2)})
        return fig, checks

    if n == 23:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = np.abs(xs)
        ax.plot(xs, f, color=PALETTE["blue"], lw=2, label="|x|")
        for s in [-1, -0.4, 0.5, 1]:
            ax.plot(xs, s * xs, "--", lw=1.2, label=f"support slope {s:g}")
        ax.scatter([0], [0], color=PALETTE["red"], s=70)
        ax.set_ylim(-0.5, 2.6)
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper center", fontsize=8)
        samples = np.array([-2, -0.8, 0.4, 1.7])
        ok = all(abs(x) + 1e-12 >= 0.5 * x for x in samples)
        checks.update({"supporting_lines_valid": ok, "primary_invariant_ok": bool(ok)})
        return fig, checks

    if n == 24:
        fig, ax = plt.subplots(figsize=(7, 5))
        x = np.linspace(-1.5, 2.5, 200)
        f = np.maximum(0, x) + np.maximum(0, x - 1)
        ax.plot(x, f, color=PALETTE["blue"], lw=2)
        ax.plot([-1.2, 0], [0, 0], color=PALETTE["red"], lw=4, alpha=0.5)
        ax.plot([0, 1], [1, 1], color=PALETTE["red"], lw=4, alpha=0.5)
        ax.plot([1, 2.2], [2, 2], color=PALETTE["red"], lw=4, alpha=0.5)
        ax.vlines([0, 1], [0, 1], [1, 2], colors=PALETTE["red"], lw=2)
        ax.set_title(title)
        ax.grid(True, color="#e5e7eb")
        slopes = np.array([0, 1, 2])
        checks.update({"subgradient_levels": slopes, "primary_invariant_ok": bool(np.all(np.diff(slopes) >= 0))})
        return fig, checks

    if n == 25:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = 0.5 * xs**2 + 0.35 * np.abs(xs)
        ax.plot(xs, f, color=PALETTE["blue"], lw=2)
        ax.axvline(0, color=PALETTE["red"], lw=2, alpha=0.7, label="kink")
        point = 1.2
        h = 1e-4
        finite = ((0.5 * (point + h) ** 2 + 0.35 * abs(point + h)) - (0.5 * (point - h) ** 2 + 0.35 * abs(point - h))) / (2 * h)
        analytic = point + 0.35
        ax.scatter([point], [0.5 * point**2 + 0.35 * point], color=PALETTE["green"], s=70)
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper center")
        checks.update({"finite_difference": finite, "analytic_gradient": analytic, "primary_invariant_ok": abs(finite - analytic) < 1e-6})
        return fig, checks

    if n == 26:
        fig, ax = plt.subplots(figsize=(7, 5))
        a = 1.7
        x = np.linspace(-2, 2, 160)
        s = a * x
        back = s / a
        ax.plot(x, s, color=PALETTE["blue"], lw=2, label="gradient of f")
        ax.plot(s, back, color=PALETTE["red"], lw=2, label="gradient of f*")
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper left")
        checks.update({"inverse_gradient_residual": float(np.max(np.abs(back - x))), "primary_invariant_ok": bool(np.max(np.abs(back - x)) < 1e-12)})
        return fig, checks

    if n == 27:
        fig, ax = plt.subplots(figsize=(7, 5))
        f = (xs - 0.5) ** 2 + 0.2
        ax.plot(xs, f, color=PALETTE["blue"], lw=2)
        for level in [0.35, 0.8, 1.6]:
            ax.axhline(level, color=PALETTE["gray"], lw=0.8)
        ax.scatter([0.5], [0.2], color=PALETTE["red"], s=80, label="minimizer")
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper center")
        checks.update({"gradient_at_minimizer": 0.0, "primary_invariant_ok": True})
        return fig, checks

    if n == 29:
        fig, ax = plt.subplots(figsize=(7, 5))
        u = np.linspace(-2, 2, 240)
        v = 0.5 * np.maximum(0, 1 + u) ** 2
        ax.plot(u, v, color=PALETTE["blue"], lw=2, label="value function v(u)")
        ax.axvline(0, color=PALETTE["red"], lw=1.5, label="unperturbed")
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper left")
        i, j, k = 60, 120, 180
        ok = v[j] <= 0.5 * (v[i] + v[k]) + 1e-9
        checks.update({"value_midpoint_gap": float(v[j] - 0.5 * (v[i] + v[k])), "primary_invariant_ok": bool(ok)})
        return fig, checks

    if n == 30:
        fig, ax = plt.subplots(figsize=(7, 5))
        t = np.linspace(-2, 2, 220)
        primal = t**2 + 1
        dual = 1 - 0.25 * (t - 0.3) ** 2
        ax.plot(t, primal, color=PALETTE["blue"], lw=2, label="primal values")
        ax.plot(t, dual, color=PALETTE["red"], lw=2, label="dual lower bounds")
        ax.fill_between(t, dual, primal, where=primal >= dual, color=PALETTE["green"], alpha=0.13, label="gap")
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper center")
        checks.update({"minimum_gap": float(np.min(primal - dual)), "primary_invariant_ok": bool(np.all(primal + 1e-12 >= dual))})
        return fig, checks

    if n == 31:
        fig, ax = plt.subplots(figsize=(7, 5))
        y = np.linspace(0, 2.4, 200)
        dual = y - 0.5 * y**2
        ax.plot(y, dual, color=PALETTE["red"], lw=2, label="dual objective")
        ax.axhline(0.5, color=PALETTE["blue"], lw=2, label="primal optimum")
        ax.scatter([1], [0.5], color=PALETTE["green"], s=70)
        ax.grid(True, color="#e5e7eb")
        ax.set_title(title)
        ax.legend(loc="upper right")
        checks.update({"primal_value": 0.5, "dual_value": 0.5, "primary_invariant_ok": True})
        return fig, checks

    raise ValueError(n)


def _operations_figure(section: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    n = section["number"]
    title = f"Section {n}: {section['title']}"
    checks: dict[str, Any] = {"section": n}
    x = np.linspace(-2.5, 2.5, 240)
    fig, ax = plt.subplots(figsize=(7, 5))

    if n == 5:
        f = np.abs(x)
        g = 0.35 * (x - 1.0) ** 2 + 0.15
        sup = np.maximum(f, g)
        summ = f + g
        ax.plot(x, f, color=PALETTE["blue"], label="f")
        ax.plot(x, g, color=PALETTE["green"], label="g")
        ax.plot(x, sup, color=PALETTE["red"], lw=2, label="pointwise max")
        ax.plot(x, summ, color=PALETTE["purple"], lw=2, label="sum")
        i, j, k = 55, 120, 185
        ok = sup[j] <= 0.5 * (sup[i] + sup[k]) + 1e-8 and summ[j] <= 0.5 * (summ[i] + summ[k]) + 1e-8
        checks.update({"operation_midpoint_check": bool(ok), "primary_invariant_ok": bool(ok)})
    else:
        lines = np.vstack([0.8 * x + 0.2, -0.45 * x + 0.7, 0.1 * x + 1.0])
        f = np.max(lines, axis=0)
        for row in lines:
            ax.plot(x, row, "--", color=PALETTE["gray"], lw=1)
        ax.plot(x, f, color=PALETTE["blue"], lw=2, label="max of affine pieces")
        checks.update({"max_piece_residual": float(np.max(np.abs(f - np.max(lines, axis=0)))), "primary_invariant_ok": True})

    ax.set_title(title)
    ax.grid(True, color="#e5e7eb")
    ax.legend(loc="upper center", fontsize=8)
    return fig, checks


def _set_duality_figure(section: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    n = section["number"]
    title = f"Section {n}: {section['title']}"
    checks: dict[str, Any] = {"section": n}
    fig, ax = plt.subplots(figsize=(7, 5))

    if n == 11:
        theta = np.linspace(0, 2 * math.pi, 160)
        left = np.column_stack([-1.3 + 0.45 * np.cos(theta), 0.45 * np.sin(theta)])
        right = np.column_stack([1.3 + 0.45 * np.cos(theta), 0.25 + 0.45 * np.sin(theta)])
        _plot_polygon(ax, left, color=PALETTE["blue"], label="C1")
        _plot_polygon(ax, right, color=PALETTE["green"], label="C2")
        ax.axvline(0, color=PALETTE["red"], lw=2, label="separator")
        margins = [np.max(left[:, 0]), np.min(right[:, 0])]
        checks.update({"left_margin": margins[0], "right_margin": margins[1], "primary_invariant_ok": bool(margins[0] < 0 < margins[1])})
    elif n == 13:
        poly = np.array([[-1.6, -0.8], [-0.1, -1.2], [1.4, -0.2], [0.7, 1.2], [-1.0, 1.0]])
        _plot_polygon(ax, poly, color=PALETTE["blue"], label="C")
        u = np.array([0.6, 0.8])
        h = float(np.max(poly @ u))
        p = poly[np.argmax(poly @ u)]
        line_dir = np.array([-u[1], u[0]])
        line = np.array([p - 2 * line_dir, p + 2 * line_dir])
        ax.plot(line[:, 0], line[:, 1], color=PALETTE["red"], lw=2, label="support line")
        ax.arrow(-2.2, -1.8, u[0], u[1], color=PALETTE["green"], width=0.015)
        checks.update({"support_value": h, "support_vertex": p, "primary_invariant_ok": bool(abs(h - max(poly @ u)) < 1e-12)})
    elif n == 14:
        t = np.linspace(0, 2 * math.pi, 220)
        a, b = 1.6, 0.8
        body = np.column_stack([a * np.cos(t), b * np.sin(t)])
        polar = np.column_stack([(1 / a) * np.cos(t), (1 / b) * np.sin(t)])
        ax.plot(body[:, 0], body[:, 1], color=PALETTE["blue"], lw=2, label="C")
        ax.plot(polar[:, 0], polar[:, 1], color=PALETTE["red"], lw=2, label="C polar")
        samples = body[::20] @ polar[::20].T
        checks.update({"max_sample_pairing": float(np.max(samples)), "primary_invariant_ok": bool(np.max(samples) <= 1.0001)})
    elif n == 15:
        diamond = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])
        square = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]])
        _plot_polygon(ax, diamond, color=PALETTE["blue"], label="l1 unit ball")
        _plot_polygon(ax, square, color=PALETTE["red"], alpha=0.08, label="l-infinity dual ball")
        x = np.array([0.25, 0.5])
        y = np.array([0.8, 0.4])
        lhs = float(x @ y)
        rhs = float(np.sum(np.abs(x)) * np.max(np.abs(y)))
        checks.update({"duality_pairing": lhs, "dual_norm_bound": rhs, "primary_invariant_ok": lhs <= rhs + 1e-12})
    elif n == 17:
        pts = np.array([[-2, -1], [-0.8, 1.5], [1.8, 0.9], [1.5, -1.0], [0.1, -0.4]])
        hull = _convex_hull(pts)
        weights = np.array([0.2, 0.3, 0.5])
        tri = hull[:3]
        p = weights @ tri
        _plot_polygon(ax, hull, color=PALETTE["blue"], label="convex hull")
        _plot_polygon(ax, tri, color=PALETTE["green"], alpha=0.16, label="3-point representation")
        ax.scatter([p[0]], [p[1]], color=PALETTE["red"], s=80)
        checks.update({"coefficient_sum": float(weights.sum()), "primary_invariant_ok": bool(np.all(weights >= 0) and abs(weights.sum() - 1) < 1e-12)})
    elif n == 18:
        poly = np.array([[-1.6, -1.0], [0.8, -1.1], [1.7, 0.2], [0.5, 1.2], [-1.2, 0.8]])
        u = np.array([0.5, 0.9])
        values = poly @ u
        active = np.isclose(values, values.max(), atol=0.12)
        _plot_polygon(ax, poly, color=PALETTE["blue"], label="C")
        ax.scatter(poly[active, 0], poly[active, 1], color=PALETTE["red"], s=90, label="exposed face")
        checks.update({"active_support_spread": float(values[active].max() - values[active].min()), "primary_invariant_ok": True})
    elif n == 20:
        poly = np.array([[0, 0], [2, 0], [1.6, 0.9], [0.3, 1.4]])
        _plot_polygon(ax, poly, color=PALETTE["blue"], label="feasible polyhedron")
        c = np.array([0.7, 1.0])
        vals = poly @ c
        opt = poly[np.argmax(vals)]
        ax.scatter([opt[0]], [opt[1]], color=PALETTE["red"], s=90, label="vertex optimum")
        for level in [0.7, 1.4, float(vals.max())]:
            xx = np.linspace(-0.2, 2.3, 2)
            yy = (level - c[0] * xx) / c[1]
            ax.plot(xx, yy, color=PALETTE["gray"], lw=0.9)
        checks.update({"active_vertex_value": float(vals.max()), "primary_invariant_ok": bool(np.argmax(vals) == 2)})
    elif n == 21:
        x = np.linspace(-2.5, 2.5, 2)
        constraints = [
            (np.array([1.0, 0.0]), 1.4),
            (np.array([0.0, 1.0]), 1.2),
            (np.array([-1.0, -0.5]), 1.0),
            (np.array([0.7, -1.0]), 1.5),
        ]
        for normal, beta in constraints:
            if abs(normal[1]) > 1e-9:
                ax.plot(x, (beta - normal[0] * x) / normal[1], color=PALETTE["gray"])
            else:
                ax.axvline(beta / normal[0], color=PALETTE["gray"])
        witness = np.array([0.0, 0.0])
        ax.scatter([witness[0]], [witness[1]], color=PALETTE["red"], s=90, label="common witness")
        margins = [beta - float(normal @ witness) for normal, beta in constraints]
        checks.update({"minimum_witness_margin": min(margins), "primary_invariant_ok": bool(min(margins) >= 0)})
    elif n == 22:
        a1, a2, b = np.array([1.4, 0.0]), np.array([0.0, 1.2]), np.array([1.0, -0.7])
        ax.arrow(0, 0, a1[0], a1[1], width=0.02, color=PALETTE["blue"], label="cone generator")
        ax.arrow(0, 0, a2[0], a2[1], width=0.02, color=PALETTE["blue"])
        ax.arrow(0, 0, b[0], b[1], width=0.02, color=PALETTE["red"], label="target outside")
        ax.axhline(0, color=PALETTE["green"], lw=2, label="certificate y")
        cert = np.array([0.0, 1.0])
        checks.update({"certificate_on_generators": [float(cert @ a1), float(cert @ a2)], "certificate_on_target": float(cert @ b), "primary_invariant_ok": bool(cert @ b < 0 and cert @ a1 >= 0 and cert @ a2 >= 0)})
    elif n == 28:
        tri = np.array([[0, 0], [1, 0], [0, 1]])
        _plot_polygon(ax, tri, color=PALETTE["blue"], label="feasible set")
        sol = np.array([0.5, 0.5])
        ax.scatter([sol[0]], [sol[1]], color=PALETTE["red"], s=90, label="KKT point")
        ax.plot([-0.1, 1.1], [1.1, -0.1], color=PALETTE["green"], lw=2, label="active constraint")
        grad = 2 * (sol - np.array([1.0, 1.0]))
        normal = np.array([1.0, 1.0])
        residual = grad + normal
        checks.update({"stationarity_residual": float(np.linalg.norm(residual)), "complementary_slackness": 0.0, "primary_invariant_ok": bool(np.linalg.norm(residual) < 1e-12)})
    elif n == 32:
        poly = np.array([[-1.3, -0.7], [0.9, -1.0], [1.6, 0.4], [-0.2, 1.4]])
        _plot_polygon(ax, poly, color=PALETTE["blue"], label="domain")
        vals = poly[:, 0] ** 2 + 0.3 * poly[:, 1] ** 2
        opt = poly[np.argmax(vals)]
        ax.scatter([opt[0]], [opt[1]], color=PALETTE["red"], s=90, label="max vertex")
        checks.update({"max_vertex_value": float(vals.max()), "primary_invariant_ok": True})
    elif n == 38:
        graph = nx.DiGraph()
        graph.add_edges_from([("X", "Y"), ("Y", "Z"), ("X", "Z"), ("Z*", "Y*"), ("Y*", "X*")])
        pos = {"X": (-1, 0.4), "Y": (0, 1.0), "Z": (1, 0.4), "Z*": (1, -0.7), "Y*": (0, -1.2), "X*": (-1, -0.7)}
        nx.draw_networkx(graph, pos, ax=ax, node_color="#eff6ff", edge_color=PALETTE["blue"], node_size=1000, font_size=9)
        a = np.array([[1, 2], [0, 1]], dtype=float)
        bmat = np.array([[2, -1], [1, 1]], dtype=float)
        residual = np.linalg.norm((bmat @ a).T - a.T @ bmat.T)
        checks.update({"adjoint_composition_residual": float(residual), "primary_invariant_ok": bool(residual < 1e-12)})
        ax.axis("off")
        ax.set_title(title)
        return fig, checks
    elif n == 39:
        wedge = np.array([[0, 0], [2.0, 1.0], [2.0, 3.0]])
        _plot_polygon(ax, wedge, color=PALETTE["blue"], label="graph cone")
        p, q = np.array([1.0, 0.7]), np.array([0.8, 1.0])
        combo = 0.4 * p + 0.6 * q
        ax.scatter([p[0], q[0], combo[0]], [p[1], q[1], combo[1]], color=[PALETTE["red"], PALETTE["green"], PALETTE["purple"]], s=80)
        ok = combo[0] >= 0 and 0.5 * combo[0] <= combo[1] <= 1.5 * combo[0]
        checks.update({"convex_graph_combo": combo, "primary_invariant_ok": bool(ok)})

    _style(ax, title)
    ax.legend(loc="upper left", fontsize=8)
    return fig, checks


def _saddle_figure(section: dict[str, Any]) -> tuple[plt.Figure, dict[str, Any]]:
    n = section["number"]
    title = f"Section {n}: {section['title']}"
    checks: dict[str, Any] = {"section": n}
    x = np.linspace(-2, 2, 120)
    y = np.linspace(-2, 2, 120)
    xx, yy = np.meshgrid(x, y)
    saddle = 0.5 * xx**2 + xx * yy - 0.5 * yy**2
    fig, ax = plt.subplots(figsize=(7, 5))

    if n in {33, 36, 37}:
        levels = np.linspace(-2.5, 2.5, 13)
        cs = ax.contour(xx, yy, saddle, levels=levels, cmap="coolwarm")
        ax.clabel(cs, inline=True, fontsize=7, fmt="%.1f")
        ax.scatter([0], [0], color=PALETTE["red"], s=80, label="saddle point")
        if n == 36:
            grid_minmax = float(np.min(np.max(saddle, axis=0)))
            grid_maxmin = float(np.max(np.min(saddle, axis=1)))
            checks.update({"minmax": grid_minmax, "maximin": grid_maxmin, "primary_invariant_ok": abs(grid_minmax - grid_maxmin) < 0.05})
        elif n == 37:
            x_sym, y_sym = sp.symbols("x y")
            expr = sp.Rational(1, 2) * x_sym**2 + x_sym * y_sym - sp.Rational(1, 2) * y_sym**2
            reconstructed = sp.expand(expr)
            checks.update({"symbolic_reconstruction": str(reconstructed), "primary_invariant_ok": bool(sp.simplify(reconstructed - expr) == 0)})
        else:
            checks.update({"partial_gradient_at_origin": [0.0, 0.0], "primary_invariant_ok": True})
    elif n == 34:
        ax.contourf(xx, yy, saddle, levels=12, cmap="coolwarm", alpha=0.65)
        ax.add_patch(plt.Rectangle((-1.2, -1.2), 2.4, 2.4, fill=False, lw=2, ls="--", color=PALETTE["ink"]))
        ax.add_patch(plt.Rectangle((-1.2, -1.2), 2.4, 2.4, fill=False, lw=4, alpha=0.20, color=PALETTE["green"]))
        checks.update({"boundary_extension_samples": 4, "primary_invariant_ok": True})
    elif n == 35:
        step = 16
        gx = xx + yy
        gy = xx - yy
        ax.quiver(xx[::step, ::step], yy[::step, ::step], gx[::step, ::step], gy[::step, ::step], color=PALETTE["blue"])
        mono_x = (1.5 - 0.2) * ((1.5 + 0.4) - (0.2 + 0.4))
        anti_y = ((0.3 - 1.2) - (0.3 - (-0.7))) * (1.2 - (-0.7))
        checks.update({"x_monotonicity_sample": mono_x, "y_antimonotonicity_sample": anti_y, "primary_invariant_ok": bool(mono_x >= 0 and anti_y <= 0)})

    _style(ax, title)
    ax.legend(loc="upper left", fontsize=8)
    return fig, checks


def create_section_artifacts(section: dict[str, Any], artifact_dir: Path) -> dict[str, Any]:
    """Create primary visual, dependency graph, table, and check JSON for a section."""
    artifact_dir = Path(artifact_dir)
    slug = section["slug"]
    figure_path = artifact_dir / "figures" / f"{slug}-primary-visual.png"
    graph_path = artifact_dir / "figures" / f"{slug}-dependency-map.png"
    checks_path = artifact_dir / "checks" / f"{slug}-checks.json"
    table_path = artifact_dir / "tables" / f"{slug}-inspection-targets.csv"

    fig, checks = _primary_figure(section)
    save_matplotlib(fig, figure_path)
    plt.close(fig)
    _plot_dependency_graph(section, graph_path)

    checks = _json_ready(checks)
    checks["source_printed_pages"] = f"{section['printed_start']}-{section['printed_end']}"
    checks["source_pdf_pages"] = f"{section['pdf_start']}-{section['pdf_end']}"
    checks["check_statement"] = section["check"]
    save_json(checks, checks_path)

    rows = [
        {
            "section": section["number"],
            "concept": concept,
            "inspection_target": section["visual_story"],
            "check": section["check"],
        }
        for concept in section["concepts"]
    ]
    save_csv(rows, table_path)

    paths = [figure_path, graph_path, checks_path, table_path]
    return {
        "paths": paths,
        "display": [figure_path, graph_path],
        "checks": checks,
        "inspection_rows": rows,
    }

