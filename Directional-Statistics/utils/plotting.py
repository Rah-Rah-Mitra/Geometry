"""Plotting defaults and course visual constructors."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageStat

from .circular import A1, circular_cdf_grid, resultant, rose_histogram, sample_vonmises, von_mises_pdf
from .manifolds import grassmann_projection, minkowski_dot, rotation_from_axis_angle, sample_hyperboloid, sample_so3, sample_stiefel
from .shape import procrustes_mean, tangent_shape_coords, triangle_shape_features
from .special_functions import bessel_ratio, large_kappa_A1, small_kappa_A1
from .spherical import inertia_matrix, mean_direction, spherical_sample, uniform_sphere

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


def image_stats(path: str | Path) -> dict[str, float | int | str]:
    p = Path(path)
    with Image.open(p) as image:
        image.load()
        rgb = image.convert("RGB")
        stat = ImageStat.Stat(rgb)
        arr = np.asarray(rgb, dtype=float)
    digest = hashlib.sha256(p.read_bytes()).hexdigest()
    return {
        "path": p.as_posix(),
        "width": int(rgb.width),
        "height": int(rgb.height),
        "bytes": int(p.stat().st_size),
        "sha256": digest,
        "pixel_std": float(arr.std()),
        "max_channel_stddev": float(max(stat.stddev) if stat.stddev else 0.0),
    }


def close(fig: Any) -> None:
    plt.close(fig)


def make_entry_static_figure(entry: dict) -> tuple[Any, dict[str, float]]:
    family = entry["family"]
    seed = int(entry["number"])
    diagnostics: dict[str, float] = {"seed": float(seed)}
    if family == "circular":
        theta = sample_vonmises(seed, 96, mu=seed / 9.0, kappa=1.2 + (seed % 5) * 0.7)
        res = resultant(theta)
        counts, edges = rose_histogram(theta, bins=18)
        grid = np.linspace(-np.pi, np.pi, 360)
        density = von_mises_pdf(grid, res["mean"], max(0.25, 6 * res["R"]))
        fig = plt.figure(figsize=(10, 4.8))
        ax = fig.add_subplot(121, projection="polar")
        widths = np.diff(edges)
        ax.bar(edges[:-1], np.sqrt(counts), width=widths, align="edge", color=PALETTE["teal"], alpha=0.68, edgecolor="white")
        ax.arrow(res["mean"], 0, 0, max(np.sqrt(counts).max(), 1) * res["R"], width=0.02, color=PALETTE["red"], length_includes_head=True)
        ax.set_title(f"{entry['label']}: rose/resultant view")
        ax2 = fig.add_subplot(122)
        ax2.plot(grid, density, color=PALETTE["blue"], label="fitted von Mises sketch")
        g, ecdf = circular_cdf_grid(theta)
        ax2.step(g - np.pi, ecdf, color=PALETTE["gold"], where="post", label="empirical circular CDF")
        style_axis(ax2, "Density and circular CDF")
        ax2.legend(loc="best", fontsize=8)
        diagnostics.update({"R": float(res["R"]), "mean": float(res["mean"]), "density_integral": float(np.trapz(density, grid))})
        return fig, diagnostics
    if family == "spherical":
        points = spherical_sample(seed, 90, concentration=2.5 + (seed % 4))
        md = mean_direction(points)
        inertia = inertia_matrix(points)
        fig = plt.figure(figsize=(10, 4.8))
        ax = fig.add_subplot(121, projection="3d")
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=18, color=PALETTE["blue"], alpha=0.7)
        d = md["direction"]
        ax.quiver(0, 0, 0, d[0], d[1], d[2], length=1.15, color=PALETTE["red"], linewidth=2)
        ax.set_title(f"{entry['label']}: spherical sample")
        ax.set_box_aspect((1, 1, 1))
        ax2 = fig.add_subplot(122)
        vals = np.linalg.eigvalsh(inertia)
        ax2.bar(["lambda1", "lambda2", "lambda3"], vals, color=[PALETTE["teal"], PALETTE["gold"], PALETTE["violet"]])
        style_axis(ax2, "Moment-of-inertia spectrum")
        diagnostics.update({"R": float(md["R"]), "unit_norm_error": float(np.max(np.abs(np.linalg.norm(points, axis=1) - 1))), "inertia_trace": float(np.trace(inertia))})
        return fig, diagnostics
    if family == "manifold":
        rotations = sample_so3(seed, 12)
        frames = sample_stiefel(seed + 20, 3, 2, 12)
        projection = grassmann_projection(frames[0])
        fig = plt.figure(figsize=(10, 4.8))
        ax = fig.add_subplot(121, projection="3d")
        colors = [PALETTE["red"], PALETTE["green"], PALETTE["blue"]]
        for j, color in enumerate(colors):
            ax.quiver(0, 0, 0, rotations[0][0, j], rotations[0][1, j], rotations[0][2, j], color=color, linewidth=2)
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
        ax.set_title("SO(3) frame glyph")
        ax.set_box_aspect((1, 1, 1))
        ax2 = fig.add_subplot(122)
        im = ax2.imshow(projection, cmap="viridis", vmin=-0.05, vmax=1)
        fig.colorbar(im, ax=ax2, fraction=0.046)
        style_axis(ax2, "Grassmann projection matrix")
        diagnostics.update({"rotation_det": float(np.linalg.det(rotations[0])), "stiefel_error": float(np.linalg.norm(frames[0].T @ frames[0] - np.eye(2))), "projection_idempotence": float(np.linalg.norm(projection @ projection - projection))})
        return fig, diagnostics
    if family == "shape":
        rng = np.random.default_rng(seed)
        base = np.array([[0.0, 0.0], [1.2, 0.1], [0.3, 0.95], [-0.15, 0.45]])
        shapes = np.stack([base + rng.normal(scale=0.06, size=base.shape) + [0.05 * i, 0] for i in np.linspace(-1, 1, 28)])
        mean = procrustes_mean(shapes)
        coords = tangent_shape_coords(shapes, mean)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        for shape in shapes[::4]:
            closed = np.vstack([shape, shape[0]])
            axes[0].plot(closed[:, 0], closed[:, 1], color=PALETTE["gray"], alpha=0.45)
        closed_mean = np.vstack([mean, mean[0]])
        axes[0].plot(closed_mean[:, 0], closed_mean[:, 1], color=PALETTE["red"], linewidth=2.5, label="Procrustes mean")
        axes[0].legend(fontsize=8)
        style_axis(axes[0], "Landmark overlay", equal=True)
        axes[1].scatter(coords[:, 0], coords[:, 1], color=PALETTE["teal"], alpha=0.75)
        style_axis(axes[1], "Tangent shape coordinates")
        diagnostics.update({"preshape_norm": float(np.linalg.norm(mean)), "tangent_mean_norm": float(np.linalg.norm(coords.mean(axis=0))), "triangle_feature_norm": float(np.linalg.norm(triangle_shape_features(base[:3])))})
        return fig, diagnostics
    if family == "special":
        x = np.linspace(0.05, 12, 300)
        exact = bessel_ratio(0, x)
        small = small_kappa_A1(x)
        large = large_kappa_A1(x)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
        axes[0].plot(x, exact, color=PALETTE["blue"], label="A1 exact")
        axes[0].plot(x, small, color=PALETTE["green"], linestyle="--", label="small-kappa approx")
        axes[0].plot(x, large, color=PALETTE["gold"], linestyle=":", label="large-kappa approx")
        axes[0].legend(fontsize=8)
        style_axis(axes[0], "Bessel-ratio atlas")
        axes[1].semilogy(x, np.abs(exact - np.clip(large, -2, 2)) + 1e-12, color=PALETTE["red"], label="large error")
        axes[1].semilogy(x, np.abs(exact - small) + 1e-12, color=PALETTE["violet"], label="small error")
        axes[1].legend(fontsize=8)
        style_axis(axes[1], "Approximation error bands")
        diagnostics.update({"A1_start": float(exact[0]), "A1_end": float(exact[-1]), "monotone": float(np.all(np.diff(exact) > 0))})
        return fig, diagnostics
    # notation
    fig, ax = plt.subplots(figsize=(9, 5))
    nodes = ["circle", "sphere", "SO(3)", "Stiefel", "Grassmann", "shape", "tests", "models"]
    angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
    pos = np.column_stack([np.cos(angles), np.sin(angles)])
    for i, node in enumerate(nodes):
        ax.scatter(pos[i, 0], pos[i, 1], s=900, color=PALETTE["blue"], alpha=0.18, edgecolor=PALETTE["blue"])
        ax.text(pos[i, 0], pos[i, 1], node, ha="center", va="center", fontsize=9)
    for i in range(len(nodes)):
        j = (i + 2) % len(nodes)
        ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]], color=PALETTE["gray"], alpha=0.45)
    style_axis(ax, "Notation dependency map", equal=True)
    ax.set_axis_off()
    diagnostics.update({"nodes": float(len(nodes)), "edges": float(len(nodes))})
    return fig, diagnostics


def make_entry_interactive_figure(entry: dict) -> Any:
    family = entry["family"]
    seed = int(entry["number"])
    if family == "circular":
        theta = sample_vonmises(seed + 50, 120, mu=seed / 8.0, kappa=1.0 + seed % 4)
        r = 1 + 0.15 * np.sin(np.arange(len(theta)))
        return go.Figure(
            data=[go.Scatterpolar(theta=np.degrees(theta), r=r, mode="markers", marker={"size": 7, "color": np.arange(len(theta)), "colorscale": "Viridis"})],
            layout=go.Layout(title=f"{entry['label']}: inspect circular phase", polar={"radialaxis": {"visible": True, "range": [0, 1.3]}}),
        )
    if family == "spherical":
        points = spherical_sample(seed + 50, 120, concentration=2.0 + seed % 5)
        return go.Figure(
            data=[go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers", marker={"size": 4, "color": points[:, 2], "colorscale": "Viridis"})],
            layout=go.Layout(title=f"{entry['label']}: rotate the spherical sample", scene={"aspectmode": "cube"}),
        )
    if family == "manifold":
        t = np.linspace(0, np.pi, 40)
        frames = np.array([rotation_from_axis_angle([0.4, 0.6, 1.0], angle)[:, 0] for angle in t])
        return go.Figure(
            data=[go.Scatter3d(x=frames[:, 0], y=frames[:, 1], z=frames[:, 2], mode="lines+markers", marker={"size": 4})],
            layout=go.Layout(title="Axis-angle path of a rotating frame", scene={"aspectmode": "cube"}),
        )
    if family == "shape":
        rng = np.random.default_rng(seed + 80)
        triangles = rng.normal(size=(80, 3, 2))
        feats = np.array([triangle_shape_features(t) for t in triangles])
        return go.Figure(
            data=[go.Scatter3d(x=feats[:, 0], y=feats[:, 1], z=feats[:, 2], mode="markers", marker={"size": 4, "color": feats[:, 0], "colorscale": "Plasma"})],
            layout=go.Layout(title="Triangle shape coordinates", scene={"aspectmode": "cube"}),
        )
    if family == "special":
        x = np.linspace(0.05, 14, 180)
        return go.Figure(
            data=[
                go.Scatter(x=x, y=bessel_ratio(0, x), mode="lines", name="A1"),
                go.Scatter(x=x, y=bessel_ratio(0.5, x), mode="lines", name="A_{3D} analogue"),
            ],
            layout=go.Layout(title="Interactive concentration-to-resultant curves", xaxis_title="kappa", yaxis_title="ratio"),
        )
    points = np.array([[0, 0], [1, 0.2], [0.8, 1], [-0.2, 0.8], [-0.6, 0.1], [0, 0]])
    return go.Figure(
        data=[go.Scatter(x=points[:, 0], y=points[:, 1], mode="lines+markers", text=["sample spaces", "summaries", "models", "tests", "shape", "sample spaces"])],
        layout=go.Layout(title="Notation tour path", xaxis={"visible": False}, yaxis={"visible": False}),
    )
