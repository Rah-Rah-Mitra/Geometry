"""Plotting defaults and visual constructors for Information Geometry."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from .applications import chernoff_curve, gaussian_mixture_em_step, mean_field_ising_update, natural_gradient_step
from .divergences import alpha_divergence, divergence_matrix, js_divergence, kl_divergence
from .information_geometry import e_geodesic, fisher_metric_categorical, m_geodesic, softmax

PALETTE = {
    "ink": "#1f2933",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


def style_axis(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in getattr(ax, "spines", {}).values():
        spine.set_color("#b6c0ca")


def simplex_xy(p: Any) -> np.ndarray:
    probs = np.asarray(p, dtype=float)
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, np.sqrt(3.0) / 2.0]])
    return probs @ vertices


def close(fig: Any) -> None:
    plt.close(fig)


def make_entry_static_figure(entry: dict) -> tuple[Any, dict[str, float]]:
    family = entry["family"]
    seed = int(entry["number"])
    rng = np.random.default_rng(seed)
    diagnostics: dict[str, float] = {"seed": float(seed)}
    if family == "dually-flat":
        points = softmax(rng.normal(size=(24, 3)), axis=1)
        ts = np.linspace(0, 1, 60)
        p, q = points[0], points[1]
        m_path = np.array([simplex_xy(x) for x in m_geodesic(p, q, ts)])
        e_path = np.array([simplex_xy(x) for x in e_geodesic(p, q, ts)])
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        tri = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
        axes[0].plot(tri[:, 0], tri[:, 1], color=PALETTE["gray"])
        axes[0].scatter(*simplex_xy(points).T, color=PALETTE["blue"], alpha=0.55)
        axes[0].plot(m_path[:, 0], m_path[:, 1], color=PALETTE["teal"], label="m-geodesic")
        axes[0].plot(e_path[:, 0], e_path[:, 1], color=PALETTE["red"], label="e-geodesic")
        axes[0].legend(fontsize=8)
        style_axis(axes[0], f"{entry['label']}: simplex geodesics", equal=True)
        dmat = divergence_matrix(points[:8], lambda a, b: float(kl_divergence(a, b)))
        im = axes[1].imshow(dmat, cmap="magma")
        fig.colorbar(im, ax=axes[1], fraction=0.046)
        style_axis(axes[1], "Asymmetric KL matrix")
        diagnostics.update({"kl_asymmetry": float(np.abs(dmat - dmat.T).mean()), "path_points": float(len(ts))})
        return fig, diagnostics
    if family == "differential-geometry":
        x = np.linspace(-2.0, 2.0, 120)
        sigma = np.exp(np.linspace(-1.0, 1.0, 120))
        xx, ss = np.meshgrid(x, sigma)
        volume = np.sqrt(2.0) / ss**2
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        contour = axes[0].contourf(xx, ss, volume, levels=20, cmap="viridis")
        fig.colorbar(contour, ax=axes[0], fraction=0.046)
        style_axis(axes[0], "Gaussian Fisher volume")
        theta = np.linspace(0, 2 * np.pi, 200)
        axes[1].plot(np.cos(theta), np.sin(theta), color=PALETTE["blue"])
        for angle in np.linspace(0, 2 * np.pi, 9)[:-1]:
            axes[1].arrow(0, 0, 0.78 * np.cos(angle), 0.78 * np.sin(angle), color=PALETTE["gold"], head_width=0.04, length_includes_head=True)
        style_axis(axes[1], "Parallel transport intuition", equal=True)
        diagnostics.update({"volume_min": float(volume.min()), "volume_max": float(volume.max())})
        return fig, diagnostics
    if family == "statistical-inference":
        x = rng.normal(loc=np.repeat([-1.5, 1.3], 80), scale=0.45)
        state = gaussian_mixture_em_step(x, [-1.0, 1.0], [1.0, 1.0], [0.5, 0.5])
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        axes[0].hist(x, bins=24, density=True, color=PALETTE["gray"], alpha=0.35)
        grid = np.linspace(x.min() - 0.5, x.max() + 0.5, 300)
        for k, color in enumerate([PALETTE["teal"], PALETTE["red"]]):
            density = state["weights"][k] * np.exp(-0.5 * (grid - state["means"][k]) ** 2 / state["variances"][k]) / np.sqrt(2 * np.pi * state["variances"][k])
            axes[0].plot(grid, density, color=color)
        style_axis(axes[0], "One EM step as projection")
        p = softmax(rng.normal(size=6))
        q = softmax(rng.normal(size=6))
        curve = chernoff_curve(p, q)
        axes[1].plot(curve["t"], curve["information"], color=PALETTE["blue"])
        style_axis(axes[1], "Chernoff information curve")
        diagnostics.update({"responsibility_sum_error": float(np.max(np.abs(state["responsibilities"].sum(axis=1) - 1))), "chernoff_max": float(curve["max_value"][0])})
        return fig, diagnostics
    if family == "applications":
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        theta = np.array([1.4, -0.7])
        grad = np.array([2.0, -1.2])
        fisher = np.array([[3.0, 0.8], [0.8, 1.2]])
        path = [theta]
        for _ in range(20):
            path.append(natural_gradient_step(path[-1], grad + 0.25 * path[-1], fisher, learning_rate=0.12))
        path_arr = np.array(path)
        axes[0].plot(path_arr[:, 0], path_arr[:, 1], marker="o", color=PALETTE["teal"], markersize=3)
        style_axis(axes[0], "Natural-gradient trajectory")
        couplings = np.array([[0, 0.8, -0.2], [0.8, 0, 0.5], [-0.2, 0.5, 0]])
        m = np.array([-0.6, 0.1, 0.4])
        states = [m]
        for _ in range(18):
            states.append(mean_field_ising_update(couplings, [0.1, -0.2, 0.05], states[-1], damping=0.15))
        axes[1].plot(np.array(states))
        style_axis(axes[1], "Mean-field fixed-point dynamics")
        diagnostics.update({"path_length": float(len(path)), "mean_field_norm": float(np.linalg.norm(states[-1]))})
        return fig, diagnostics
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    p = softmax(rng.normal(size=4))
    q = softmax(rng.normal(size=4))
    alphas = np.linspace(-0.95, 0.95, 120)
    axes[0].plot(alphas, [alpha_divergence(p, q, a) for a in alphas], color=PALETTE["violet"])
    style_axis(axes[0], "Alpha-divergence path")
    metric = fisher_metric_categorical(p)
    im = axes[1].imshow(metric, cmap="viridis")
    fig.colorbar(im, ax=axes[1], fraction=0.046)
    style_axis(axes[1], "Categorical Fisher metric")
    diagnostics.update({"js": float(js_divergence(p, q)), "metric_trace": float(np.trace(metric))})
    return fig, diagnostics


def make_entry_interactive_figure(entry: dict) -> Any:
    seed = int(entry["number"])
    rng = np.random.default_rng(seed + 100)
    if entry["family"] in {"dually-flat", "divergence"}:
        points = softmax(rng.normal(size=(80, 3)), axis=1)
        xy = simplex_xy(points)
        color = [kl_divergence(p, np.full(3, 1 / 3)) for p in points]
        return go.Figure(
            data=[go.Scatter(x=xy[:, 0], y=xy[:, 1], mode="markers", marker={"size": 8, "color": color, "colorscale": "Viridis"})],
            layout=go.Layout(title=f"{entry['label']}: KL height on the simplex", xaxis={"scaleanchor": "y"}),
        )
    if entry["family"] == "differential-geometry":
        mu = np.linspace(-2, 2, 45)
        sigma = np.exp(np.linspace(-1, 1, 45))
        mm, ss = np.meshgrid(mu, sigma)
        z = np.sqrt(2.0) / ss**2
        return go.Figure(data=[go.Surface(x=mm, y=ss, z=z, colorscale="Viridis")], layout=go.Layout(title="Fisher volume surface for Gaussians"))
    if entry["family"] == "statistical-inference":
        p = softmax(rng.normal(size=5))
        q = softmax(rng.normal(size=5))
        curve = chernoff_curve(p, q)
        return go.Figure(data=[go.Scatter(x=curve["t"], y=curve["information"], mode="lines")], layout=go.Layout(title="Chernoff information across mixture exponents"))
    t = np.linspace(0, 1, 120)
    return go.Figure(
        data=[
            go.Scatter(x=t, y=np.exp(-4 * t) * np.cos(9 * t), mode="lines", name="ordinary gradient"),
            go.Scatter(x=t, y=np.exp(-8 * t) * np.cos(5 * t), mode="lines", name="natural gradient"),
        ],
        layout=go.Layout(title=f"{entry['label']}: learning dynamics sketch", xaxis_title="time", yaxis_title="error mode"),
    )
