"""Generate visual and numeric artifacts for the manifold inference course."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon
from scipy.special import i0

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.artifacts import ARTIFACT_ROOT, artifact_path, require_artifacts, save_json, save_matplotlib, save_plotly_html
from utils.course_manifest import CHAPTERS, chapter_by_key
from utils.manifold_stats import (
    bootstrap_sphere_means,
    frechet_values_on_circle,
    normalize_rows,
    projective_distance,
    sphere_exp,
    sphere_extrinsic_mean,
    sphere_log,
    stiefel_project,
)
from utils.shape_spaces import affine_normalize, gram_embedding, preshape, procrustes_align, procrustes_distance, triangle_shape_coordinates


PALETTE = {
    "ink": "#243447",
    "blue": "#386cb0",
    "green": "#1b9e77",
    "orange": "#f28e2b",
    "red": "#d95f02",
    "violet": "#7b3294",
    "gold": "#e6ab02",
}


def rng_for(key: str) -> np.random.Generator:
    seed = sum((i + 1) * ord(c) for i, c in enumerate(key)) % (2**32)
    return np.random.default_rng(seed)


def finalize(fig: plt.Figure, title: str) -> None:
    fig.suptitle(title, fontsize=14, fontweight="bold", color=PALETTE["ink"])
    fig.patch.set_facecolor("white")


def save_fig(fig: plt.Figure, key: str, filename: str) -> Path:
    path = save_matplotlib(fig, key, "figures", filename)
    plt.close(fig)
    return path


def save_checks(key: str, data: dict[str, object]) -> Path:
    return save_json(data, key, "checks", "numeric-checks.json")


def record_final_sanity(key: str, artifact_paths: list[Path], extra: dict[str, object] | None = None) -> Path:
    sizes = require_artifacts(artifact_paths)
    payload = {"artifact_count": len(artifact_paths), "artifact_sizes": sizes}
    if extra:
        payload.update(extra)
    return save_json(payload, key, "checks", "final-sanity.json")


def sphere_points(seed: int, n: int = 36, center: np.ndarray | None = None, spread: float = 0.22) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if center is None:
        center = normalize_rows(np.array([[0.35, 0.25, 0.9]]))[0]
    basis1 = normalize_rows(np.cross(center, [0, 0, 1])[None, :])[0]
    if np.linalg.norm(basis1) < 1e-8:
        basis1 = np.array([1.0, 0.0, 0.0])
    basis2 = np.cross(center, basis1)
    tangents = spread * (rng.normal(size=(n, 1)) * basis1 + rng.normal(size=(n, 1)) * basis2)
    return sphere_exp(center, tangents)


def toy_landmarks() -> np.ndarray:
    return np.array([[-1.0, -0.2], [-0.25, 0.9], [0.8, 0.55], [1.15, -0.45], [0.1, -0.85]])


def draw_shape(ax: plt.Axes, points: np.ndarray, *, color: str, label: str) -> None:
    pts = np.vstack([points, points[0]])
    ax.plot(pts[:, 0], pts[:, 1], "-o", color=color, lw=2, ms=4, label=label)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def ch01() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-01")
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    graph = {
        "landmark table": (0.05, 0.62),
        "group action": (0.24, 0.62),
        "quotient shape": (0.43, 0.62),
        "metric choice": (0.62, 0.62),
        "Frechet mean": (0.81, 0.62),
        "test statistic": (0.81, 0.28),
        "bootstrap cloud": (0.62, 0.28),
        "tangent chart": (0.43, 0.28),
    }
    edges = [
        ("landmark table", "group action"),
        ("group action", "quotient shape"),
        ("quotient shape", "metric choice"),
        ("metric choice", "Frechet mean"),
        ("Frechet mean", "test statistic"),
        ("Frechet mean", "bootstrap cloud"),
        ("metric choice", "tangent chart"),
        ("tangent chart", "bootstrap cloud"),
        ("bootstrap cloud", "test statistic"),
    ]
    for a, b in edges:
        ax.annotate("", graph[b], graph[a], arrowprops={"arrowstyle": "->", "lw": 1.8, "color": PALETTE["ink"]})
    for idx, (name, (x, y)) in enumerate(graph.items()):
        color = [PALETTE["blue"], PALETTE["green"], PALETTE["orange"], PALETTE["violet"]][idx % 4]
        ax.scatter([x], [y], s=700, color=color, alpha=0.18, edgecolors=color, linewidths=2)
        ax.text(x, y, name, ha="center", va="center", fontsize=9, color=PALETTE["ink"])
    ax.axis("off")
    finalize(fig, "Statistical shape inference as a chain of geometric decisions")
    p1 = save_fig(fig, ch.key, "shape-inference-roadmap.png")

    fig, ax = plt.subplots(figsize=(8, 3.8))
    labels = ["translation", "scale", "rotation", "reflection", "affine", "projective"]
    widths = [0.65, 0.58, 0.49, 0.4, 0.3, 0.2]
    for i, (lab, width) in enumerate(zip(labels, widths, strict=True)):
        ax.add_patch(Polygon([[i - width / 2, 0], [i + width / 2, 0], [i + width / 2, 1], [i - width / 2, 1]], fill=True, color=PALETTE["blue"], alpha=0.14 + 0.1 * i))
        ax.text(i, 0.5, lab, rotation=90, ha="center", va="center", fontsize=10)
    ax.plot(range(len(labels)), np.linspace(1.25, 1.55, len(labels)), "o-", color=PALETTE["red"], label="larger orbit")
    ax.plot(range(len(labels)), np.linspace(0.18, 0.05, len(labels)), "o-", color=PALETTE["green"], label="less retained geometry")
    ax.set_xlim(-0.8, len(labels) - 0.2)
    ax.set_ylim(-0.1, 1.75)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_yticks([])
    ax.legend(loc="upper left", frameon=False)
    ax.set_title("Each quotient answers: which transformations should be invisible?")
    p2 = save_fig(fig, ch.key, "quotient-ladder.png")
    checks = {"node_count": 8, "edge_count": len(edges), "quotient_levels": labels}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch02() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-02")
    rng = rng_for(ch.key)
    angles = rng.vonmises(mu=0.8, kappa=2.4, size=40)
    sphere = sphere_points(202, n=45, center=np.array([0.25, -0.2, 0.94]), spread=0.28)
    skull = np.stack([toy_landmarks() + 0.07 * rng.normal(size=toy_landmarks().shape) for _ in range(8)])
    digit = np.array([[np.cos(t), 1.8 * np.sin(t) + 0.2 * np.sin(3 * t)] for t in np.linspace(0, 2 * np.pi, 28)])
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(221, projection="polar")
    ax.scatter(angles, np.ones_like(angles), color=PALETTE["blue"], s=24)
    ax.set_title("circle: wind direction")
    ax.set_yticklabels([])
    ax = fig.add_subplot(222, projection="3d")
    ax.scatter(sphere[:, 0], sphere[:, 1], sphere[:, 2], color=PALETTE["green"], s=22)
    ax.set_title("sphere: paleomagnetic poles")
    ax.set_axis_off()
    ax = fig.add_subplot(223)
    for pts in skull:
        draw_shape(ax, preshape(pts), color=PALETTE["orange"], label="")
    ax.set_title("planar shapes: skull landmarks")
    ax = fig.add_subplot(224)
    draw_shape(ax, digit, color=PALETTE["violet"], label="digit")
    draw_shape(ax, affine_normalize(digit), color=PALETTE["green"], label="affine normalized")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("affine shape: digit outline")
    finalize(fig, "Examples route observations to different sample manifolds")
    p1 = save_fig(fig, ch.key, "application-gallery.png")

    u, v = np.mgrid[0 : 2 * np.pi : 30j, 0 : np.pi : 15j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    fig3 = go.Figure()
    fig3.add_surface(x=x, y=y, z=z, opacity=0.18, colorscale="Blues", showscale=False)
    fig3.add_scatter3d(x=sphere[:, 0], y=sphere[:, 1], z=sphere[:, 2], mode="markers", marker={"size": 4, "color": "#1b9e77"})
    fig3.update_layout(title="Synthetic S2 observations: rotate to inspect directional concentration", scene={"aspectmode": "data"})
    p2 = save_plotly_html(fig3, ch.key, "interactive", "sphere-observations.html")
    checks = {"circle_resultant": float(abs(np.mean(np.exp(1j * angles)))), "sphere_mean_norm": float(np.linalg.norm(np.mean(sphere, axis=0))), "skull_samples": int(len(skull))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch03() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-03")
    rng = rng_for(ch.key)
    angles = np.concatenate([rng.vonmises(-1.0, 8, 16), rng.vonmises(1.25, 5, 14)])
    grid = np.linspace(-np.pi, np.pi, 500)
    values = frechet_values_on_circle(angles, grid)
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(grid, values, color=PALETTE["blue"], lw=2.5)
    ax.scatter(angles, np.full_like(angles, values.min() - 0.07), color=PALETTE["orange"], s=18, label="observations")
    ax.axvline(grid[np.argmin(values)], color=PALETTE["green"], lw=2, label="sample Frechet mean")
    ax.set_xlabel("candidate angle")
    ax.set_ylabel("mean squared geodesic distance")
    ax.legend(frameon=False)
    ax.set_title("A metric-space mean is a minimizer of a loss landscape")
    p1 = save_fig(fig, ch.key, "metric-frechet-landscape.png")

    boot = []
    for _ in range(350):
        sample = rng.choice(angles, size=len(angles), replace=True)
        vals = frechet_values_on_circle(sample, grid)
        boot.append(grid[np.argmin(vals)])
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(boot, bins=34, color=PALETTE["green"], alpha=0.72)
    ax.axvline(np.mean(boot), color=PALETTE["red"], lw=2)
    ax.set_xlabel("bootstrap mean angle")
    ax.set_ylabel("replicates")
    ax.set_title("Bootstrap spread lives on the same metric object")
    p2 = save_fig(fig, ch.key, "circle-bootstrap-bands.png")
    checks = {"min_frechet_value": float(values.min()), "bootstrap_sd": float(np.std(np.unwrap(boot))), "sample_size": int(len(angles))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch04() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-04")
    pts = sphere_points(404, n=50)
    mean_e = pts.mean(axis=0)
    mean_x = sphere_extrinsic_mean(pts)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    u, v = np.mgrid[0 : 2 * np.pi : 40j, 0 : np.pi : 20j]
    ax.plot_surface(np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), np.cos(v), alpha=0.11, color="#d8ecf3", linewidth=0)
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=22, color=PALETTE["blue"], alpha=0.8)
    ax.scatter(*mean_e, s=80, color=PALETTE["orange"], label="ambient mean")
    ax.scatter(*mean_x, s=90, color=PALETTE["green"], label="projected mean")
    ax.plot([mean_e[0], mean_x[0]], [mean_e[1], mean_x[1]], [mean_e[2], mean_x[2]], color=PALETTE["red"], lw=2)
    ax.legend(loc="upper left")
    ax.set_axis_off()
    finalize(fig, "Extrinsic analysis averages after embedding, then projects back")
    p1 = save_fig(fig, ch.key, "sphere-extrinsic-projection.png")

    tangent = sphere_log(mean_x, pts)
    cov = np.cov(tangent.T)
    vals, vecs = np.linalg.eigh(cov[:2, :2])
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    ax.scatter(tangent[:, 0], tangent[:, 1], s=22, color=PALETTE["blue"], alpha=0.75)
    angle = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
    ell = Ellipse((0, 0), 2 * np.sqrt(vals[1]), 2 * np.sqrt(vals[0]), angle=angle, fc="none", ec=PALETTE["red"], lw=2)
    ax.add_patch(ell)
    ax.axhline(0, color="#999", lw=0.8)
    ax.axvline(0, color="#999", lw=0.8)
    ax.set_aspect("equal")
    ax.set_title("Tangent covariance describes first-order extrinsic uncertainty")
    p2 = save_fig(fig, ch.key, "extrinsic-covariance-ellipse.png")
    checks = {"projected_norm": float(np.linalg.norm(mean_x)), "ambient_mean_norm": float(np.linalg.norm(mean_e)), "tangent_cov_trace": float(np.trace(cov))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch05() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-05")
    pts = sphere_points(505, n=42, center=np.array([0.55, 0.1, 0.83]), spread=0.31)
    mean = sphere_extrinsic_mean(pts)
    current = normalize_rows(np.array([[1.0, 0.05, 0.15]]))[0]
    path = [current]
    for _ in range(8):
        logs = sphere_log(current, pts)
        current = sphere_exp(current, 0.55 * logs.mean(axis=0))
        path.append(current)
    path = np.array(path)
    fig = plt.figure(figsize=(7.5, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=22, color=PALETTE["blue"], alpha=0.7)
    ax.plot(path[:, 0], path[:, 1], path[:, 2], "o-", color=PALETTE["red"], lw=2, label="log/exp iteration")
    ax.scatter(*mean, color=PALETTE["green"], s=90, label="reference mean")
    ax.legend()
    ax.set_axis_off()
    finalize(fig, "Intrinsic mean iteration moves by average tangent logs")
    p1 = save_fig(fig, ch.key, "intrinsic-mean-iteration.png")

    boots = bootstrap_sphere_means(pts, n_boot=240, seed=515)
    logs = sphere_log(mean, boots)
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    ax.scatter(logs[:, 0], logs[:, 1], s=16, color=PALETTE["violet"], alpha=0.65)
    ax.set_aspect("equal")
    ax.set_title("Bootstrap means become a local cloud after a log map")
    ax.set_xlabel("tangent coordinate 1")
    ax.set_ylabel("tangent coordinate 2")
    p2 = save_fig(fig, ch.key, "log-map-bootstrap-cloud.png")
    checks = {"iteration_final_distance": float(np.linalg.norm(path[-1] - mean)), "bootstrap_count": int(len(boots)), "mean_norm": float(np.linalg.norm(mean))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch06() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-06")
    base = toy_landmarks()
    centered = base - base.mean(axis=0)
    scaled = preshape(base)
    theta = 0.65
    rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotated = scaled @ rot
    stages = [base, centered, scaled, rotated]
    titles = ["raw k-ad", "centered", "unit centroid size", "same similarity shape"]
    fig, axes = plt.subplots(1, 4, figsize=(10, 3.2))
    for ax, pts, title, color in zip(axes, stages, titles, [PALETTE["blue"], PALETTE["green"], PALETTE["orange"], PALETTE["violet"]], strict=True):
        draw_shape(ax, pts, color=color, label=title)
        ax.set_title(title, fontsize=10)
    finalize(fig, "Landmark shape starts with normalization before quotienting")
    p1 = save_fig(fig, ch.key, "landmark-normalization-pipeline.png")

    fig, ax = plt.subplots(figsize=(7, 5))
    for i, scale in enumerate([0.75, 1.0, 1.25]):
        for theta in np.linspace(0, 2 * np.pi, 9, endpoint=False):
            rr = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
            pts = scale * centered @ rr + np.array([3.2 * (scale - 1.0), 0])
            draw_shape(ax, pts, color=[PALETTE["blue"], PALETTE["green"], PALETTE["orange"]][i], label="")
    ax.set_title("An orbit is the family of configurations declared equivalent")
    p2 = save_fig(fig, ch.key, "group-orbit-comparison.png")
    checks = {"centroid_after_centering": np.round(centered.mean(axis=0), 12).tolist(), "preshape_norm": float(np.linalg.norm(scaled)), "stage_count": 4}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch07() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-07")
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    circle = Circle((0, 0), 1, fill=False, ec=PALETTE["ink"], lw=2)
    ax.add_patch(circle)
    for phase, color in [(0.0, PALETTE["blue"]), (0.9, PALETTE["green"]), (1.8, PALETTE["orange"])]:
        t = np.linspace(phase, phase + 1.15, 40)
        ax.plot(np.cos(t), np.sin(t), color=color, lw=3)
        ax.scatter([np.cos(t[0])], [np.sin(t[0])], color=color, s=45)
    ax.arrow(0, 0, 0.55, 0.2, head_width=0.05, color=PALETTE["red"], length_includes_head=True)
    ax.text(0.62, 0.24, "horizontal\nmove", color=PALETTE["red"])
    ax.text(-0.85, -0.85, "vertical arcs are rotations\nwithin one preshape orbit", fontsize=9)
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "Kendall similarity shape space is a rotation quotient of preshapes")
    p1 = save_fig(fig, ch.key, "preshape-sphere-orbits.png")

    t = np.linspace(0, 1, 100)
    x = np.cos(1.4 * t)
    y = np.sin(1.4 * t) * np.cos(4 * np.pi * t) * 0.35
    z = np.sin(1.4 * t) * np.sin(4 * np.pi * t) * 0.35
    fig3 = go.Figure(go.Scatter3d(x=x, y=y, z=z, mode="lines+markers", marker={"size": 3}, line={"width": 5, "color": "#386cb0"}))
    fig3.update_layout(title="A horizontal geodesic sketch through preshape space", scene={"aspectmode": "data"})
    p2 = save_plotly_html(fig3, ch.key, "interactive", "kendall-geodesic.html")
    checks = {"unit_orbit_radius": 1.0, "geodesic_samples": int(len(t)), "endpoint_chord": float(np.linalg.norm([x[-1] - x[0], y[-1] - y[0], z[-1] - z[0]]))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch08() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-08")
    rng = rng_for(ch.key)
    coords = []
    samples = []
    base = np.array([[-0.8, -0.5], [0.85, -0.45], [0.05, 0.95]])
    for _ in range(140):
        pts = base + rng.normal(scale=0.11, size=base.shape)
        samples.append(pts)
        coords.append(triangle_shape_coordinates(pts))
    coords = np.array(coords)
    fig = plt.figure(figsize=(7.5, 6))
    ax = fig.add_subplot(111, projection="3d")
    unit = normalize_rows(coords)
    ax.scatter(unit[:, 0], unit[:, 1], unit[:, 2], color=PALETTE["blue"], s=18, alpha=0.75)
    ax.set_title("Planar triangle shapes sit on a CP1-style shape sphere")
    ax.set_axis_off()
    p1 = save_fig(fig, ch.key, "planar-shape-sphere.png")

    ref = samples[0]
    aligned = np.array([procrustes_align(ref, pts).ravel() for pts in samples])
    mean_vec = aligned.mean(axis=0).reshape(ref.shape)
    dists = np.array([procrustes_distance(mean_vec, pts) for pts in samples])
    fig, ax = plt.subplots(figsize=(7, 5))
    for pts in samples[:25]:
        draw_shape(ax, procrustes_align(mean_vec, pts), color="#9ecae1", label="")
    draw_shape(ax, mean_vec, color=PALETTE["red"], label="Procrustes mean")
    ax.legend(frameon=False)
    ax.set_title("Aligned bootstrap cloud reveals mean-shape uncertainty")
    p2 = save_fig(fig, ch.key, "procrustes-bootstrap.png")
    checks = {"mean_procrustes_distance": float(dists.mean()), "shape_coordinate_norm_mean": float(np.mean(np.linalg.norm(unit, axis=1))), "sample_count": len(samples)}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch09() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-09")
    base = toy_landmarks()
    mirror = base.copy()
    mirror[:, 0] *= -1
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.4))
    draw_shape(axes[0], preshape(base), color=PALETTE["blue"], label="shape")
    axes[0].set_title("oriented")
    draw_shape(axes[1], preshape(mirror), color=PALETTE["orange"], label="reflected")
    axes[1].set_title("reflected")
    draw_shape(axes[2], preshape(base), color=PALETTE["blue"], label="shape")
    draw_shape(axes[2], preshape(mirror), color=PALETTE["orange"], label="reflection")
    axes[2].set_title("same reflection shape")
    finalize(fig, "Reflection shape quotients out handedness")
    p1 = save_fig(fig, ch.key, "reflection-quotient-diagnostic.png")

    rng = rng_for(ch.key)
    spectra = []
    for _ in range(40):
        pts = base + rng.normal(scale=0.18, size=base.shape)
        spectra.append(np.linalg.eigvalsh(gram_embedding(pts))[::-1][:4])
    spectra = np.array(spectra)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(spectra.T, color="#9ecae1", alpha=0.55)
    ax.plot(spectra.mean(axis=0), "o-", color=PALETTE["red"], lw=2, label="mean spectrum")
    ax.set_xlabel("Gram eigenvalue index")
    ax.set_ylabel("eigenvalue")
    ax.legend(frameon=False)
    ax.set_title("Gram spectra are unchanged by reflection")
    p2 = save_fig(fig, ch.key, "gram-embedding-spectrum.png")
    checks = {"gram_reflection_error": float(np.linalg.norm(np.sort(np.linalg.eigvalsh(gram_embedding(base))) - np.sort(np.linalg.eigvalsh(gram_embedding(mirror))))), "spectra_count": int(len(spectra))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch10() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-10")
    rng = rng_for(ch.key)
    mat = np.eye(3)[:, :2] + 0.28 * rng.normal(size=(3, 2))
    proj = stiefel_project(mat)
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, projection="3d")
    origin = np.zeros(3)
    for vec, color, label in [(mat[:, 0], PALETTE["orange"], "raw"), (mat[:, 1], PALETTE["orange"], ""), (proj[:, 0], PALETTE["blue"], "projected"), (proj[:, 1], PALETTE["blue"], "")]:
        ax.quiver(*origin, *vec, color=color, linewidth=2, arrow_length_ratio=0.08, label=label)
    ax.legend()
    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-0.4, 1.2)
    ax.set_zlim(-0.4, 1.2)
    ax.set_title("Polar projection returns a noisy frame to the Stiefel manifold")
    p1 = save_fig(fig, ch.key, "stiefel-frame-projection.png")

    residuals = []
    for scale in np.linspace(0, 0.5, 12):
        noisy = np.eye(3)[:, :2] + scale * rng.normal(size=(3, 2))
        projected = stiefel_project(noisy)
        residuals.append(np.linalg.norm(projected.T @ projected - np.eye(2)))
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.bar(np.arange(len(residuals)), residuals, color=PALETTE["green"])
    ax.set_xlabel("noise level index")
    ax.set_ylabel("||Q^T Q - I||")
    ax.set_title("Projection check: orthogonality residuals stay numerical")
    p2 = save_fig(fig, ch.key, "orthogonality-residuals.png")
    checks = {"projection_residual": float(np.linalg.norm(proj.T @ proj - np.eye(2))), "max_sweep_residual": float(max(residuals))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch11() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-11")
    rng = rng_for(ch.key)
    base = np.array([[0, 0], [0.3, 1.2], [0.8, 1.5], [1.0, 0.3], [0.65, -0.8], [0.1, -0.7]])
    transform = np.array([[1.7, 0.55], [0.2, 0.65]])
    raw = base @ transform.T + np.array([1.2, -0.4])
    normed = affine_normalize(raw)
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))
    draw_shape(axes[0], base, color=PALETTE["blue"], label="template")
    axes[0].set_title("template")
    draw_shape(axes[1], raw, color=PALETTE["orange"], label="affine view")
    axes[1].set_title("affine view")
    draw_shape(axes[2], normed, color=PALETTE["green"], label="normalized")
    axes[2].set_title("whitened affine shape")
    finalize(fig, "Affine shape keeps incidences while discarding shear and stretch")
    p1 = save_fig(fig, ch.key, "affine-normalization-grid.png")

    curves = []
    labels = []
    for kind in range(2):
        for _ in range(22):
            t = np.linspace(0, 2 * np.pi, 36, endpoint=False)
            r = 1 + (0.2 + 0.18 * kind) * np.sin(2 * t) + 0.05 * rng.normal(size=t.shape)
            pts = np.column_stack([r * np.cos(t), (1.25 - 0.3 * kind) * r * np.sin(t)])
            curves.append(affine_normalize(pts).ravel()[:12])
            labels.append(kind)
    curves = np.array(curves)
    u, s, vh = np.linalg.svd(curves - curves.mean(axis=0), full_matrices=False)
    score = u[:, :2] * s[:2]
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.scatter(score[np.array(labels) == 0, 0], score[np.array(labels) == 0, 1], color=PALETTE["blue"], label="loop A")
    ax.scatter(score[np.array(labels) == 1, 0], score[np.array(labels) == 1, 1], color=PALETTE["red"], label="loop B")
    ax.legend(frameon=False)
    ax.set_title("Digit-like affine features separate after quotient normalization")
    p2 = save_fig(fig, ch.key, "digit-shape-affine-features.png")
    checks = {"affine_cov_trace": float(np.trace(normed.T @ normed)), "feature_gap": float(abs(score[np.array(labels) == 0, 0].mean() - score[np.array(labels) == 1, 0].mean()))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch12() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-12")
    angles = np.linspace(0, 2 * np.pi, 80)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(np.cos(angles), np.sin(angles), color=PALETTE["ink"], lw=1.5)
    for theta, color in [(0.4, PALETTE["blue"]), (1.35, PALETTE["green"]), (2.2, PALETTE["orange"])]:
        x, y = np.cos(theta), np.sin(theta)
        ax.plot([x, -x], [y, -y], "o--", color=color, lw=2)
        ax.text(1.1 * x, 1.1 * y, "line", color=color, ha="center", va="center")
    ax.set_aspect("equal")
    ax.axis("off")
    finalize(fig, "Real projective space identifies antipodal unit vectors")
    p1 = save_fig(fig, ch.key, "projective-antipodal-quotient.png")

    a = np.linspace(-1, 1, 60)
    xx, yy = np.meshgrid(a, a)
    z = np.zeros_like(xx)
    ref = np.array([1.0, 0.0, 0.0])
    for i in range(xx.shape[0]):
        for j in range(xx.shape[1]):
            v = normalize_rows(np.array([[1.0, xx[i, j], yy[i, j]]]))[0]
            z[i, j] = projective_distance(ref, v)
    fig3 = go.Figure(go.Surface(x=xx, y=yy, z=z, colorscale="Viridis"))
    fig3.update_layout(title="Projective distance is blind to sign", scene={"xaxis_title": "chart u", "yaxis_title": "chart v", "zaxis_title": "distance"})
    p2 = save_plotly_html(fig3, ch.key, "interactive", "projective-distance-field.html")
    checks = {"antipodal_distance": projective_distance(np.array([1, 0, 0]), np.array([-1, 0, 0])), "orthogonal_distance": projective_distance(np.array([1, 0, 0]), np.array([0, 1, 0]))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch13() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-13")
    grid = np.linspace(-np.pi, np.pi, 500)
    atoms = np.array([-2.2, -0.35, 1.25, 2.55])
    weights = np.array([0.18, 0.34, 0.28, 0.20])
    kappa = np.array([5.0, 11.0, 7.0, 3.2])
    density = sum(w * np.exp(k * np.cos(grid - a)) / (2 * np.pi * i0(k)) for w, a, k in zip(weights, atoms, kappa, strict=True))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(grid, density, color=PALETTE["blue"], lw=2.5)
    ax.scatter(atoms, np.zeros_like(atoms), s=weights * 600, color=PALETTE["orange"], alpha=0.75, label="DP mixture atoms")
    ax.set_xlabel("circle coordinate")
    ax.set_ylabel("density")
    ax.legend(frameon=False)
    ax.set_title("A random mixture can adapt to multimodal manifold density")
    p1 = save_fig(fig, ch.key, "manifold-density-mixture.png")

    from pyriemann.utils.mean import mean_riemann

    mats = np.stack(
        [
            np.array([[1.8, 0.3], [0.3, 0.8]]),
            np.array([[1.2, -0.25], [-0.25, 1.5]]),
            np.array([[0.75, 0.1], [0.1, 1.1]]),
        ]
    )
    mean = mean_riemann(mats, maxiter=30, tol=1e-8)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    theta = np.linspace(0, 2 * np.pi, 160)
    circle = np.stack([np.cos(theta), np.sin(theta)])
    for mat, color in zip(mats, [PALETTE["blue"], PALETTE["green"], PALETTE["orange"]], strict=True):
        vals, vecs = np.linalg.eigh(mat)
        ell = vecs @ (np.sqrt(vals)[:, None] * circle)
        ax.plot(ell[0], ell[1], color=color, alpha=0.55)
    vals, vecs = np.linalg.eigh(mean)
    ell = vecs @ (np.sqrt(vals)[:, None] * circle)
    ax.plot(ell[0], ell[1], color=PALETTE["red"], lw=3, label="PyRiemann mean")
    ax.set_aspect("equal")
    ax.legend(frameon=False)
    ax.set_title("SPD covariance observations form another statistical manifold")
    p2 = save_fig(fig, ch.key, "spd-riemannian-mean.png")
    checks = {"density_integral": float(np.trapezoid(density, grid)), "spd_mean_min_eigenvalue": float(np.min(np.linalg.eigvalsh(mean))), "pyriemann_used": True}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def ch14() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("chapter-14")
    rng = rng_for(ch.key)
    x = rng.uniform(-np.pi, np.pi, 90)
    y = (np.sin(x) + 0.35 * rng.normal(size=len(x)) > 0).astype(int)
    grid = np.linspace(-np.pi, np.pi, 300)
    bandwidth = 0.55
    score0 = np.zeros_like(grid)
    score1 = np.zeros_like(grid)
    for xi, yi in zip(x, y, strict=True):
        kern = np.exp(np.cos(grid - xi) / bandwidth)
        if yi:
            score1 += kern
        else:
            score0 += kern
    prob = score1 / (score0 + score1)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(grid, prob, color=PALETTE["blue"], lw=2.5)
    ax.scatter(x, 0.08 + 0.84 * y, c=np.where(y, PALETTE["red"], PALETTE["green"]), s=24, alpha=0.75)
    ax.axhline(0.5, color="#777", lw=1, ls="--")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("manifold coordinate")
    ax.set_ylabel("posterior class probability")
    ax.set_title("Product-kernel classifiers smooth along the manifold")
    p1 = save_fig(fig, ch.key, "manifold-kernel-classifier.png")

    thresholds = np.linspace(0.05, 0.95, 19)
    rejection = np.array([(prob > t).mean() for t in thresholds])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(thresholds, rejection, "o-", color=PALETTE["violet"])
    ax.set_xlabel("posterior probability threshold")
    ax.set_ylabel("region size")
    ax.set_title("Bayes tests report how much manifold support crosses a threshold")
    p2 = save_fig(fig, ch.key, "posterior-test-calibration.png")
    checks = {"probability_range": [float(prob.min()), float(prob.max())], "decision_region_half": float((prob > 0.5).mean())}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def appendix_a() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("appendix-a")
    u = np.linspace(-1.2, 1.2, 120)
    v = np.tanh(u)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(u, v, color=PALETTE["blue"], lw=2.5)
    ax.plot(u, u, color="#aaa", ls="--", label="identity chart")
    ax.set_xlabel("chart coordinate u")
    ax.set_ylabel("transition coordinate v")
    ax.legend(frameon=False)
    ax.set_title("A chart transition is smooth where both charts are valid")
    p1 = save_fig(fig, ch.key, "atlas-transition-map.png")
    fig, ax = plt.subplots(figsize=(6.5, 5))
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), color=PALETTE["ink"])
    point = np.array([np.cos(0.75), np.sin(0.75)])
    tangent = np.array([-np.sin(0.75), np.cos(0.75)])
    ax.arrow(*point, *(0.45 * tangent), color=PALETTE["red"], width=0.01, length_includes_head=True)
    ax.arrow(*(2 * point), *(0.9 * tangent), color=PALETTE["green"], width=0.015, length_includes_head=True)
    ax.text(point[0], point[1] + 0.15, "tangent")
    ax.text(2 * point[0], 2 * point[1] + 0.2, "pushforward")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("A smooth map pushes tangent vectors forward")
    p2 = save_fig(fig, ch.key, "tangent-pushforward.png")
    checks = {"transition_derivative_at_zero": 1.0, "pushforward_scale": 2.0}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def appendix_b() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("appendix-b")
    base = normalize_rows(np.array([[0.0, 0.0, 1.0]]))[0]
    tangent = np.array([0.75, 0.28, 0.0])
    path = np.array([sphere_exp(base, s * tangent) for s in np.linspace(0, 1, 40)])
    logs = sphere_log(base, path)
    fig = plt.figure(figsize=(7, 5.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(path[:, 0], path[:, 1], path[:, 2], color=PALETTE["blue"], lw=3)
    ax.scatter(*base, color=PALETTE["green"], s=90, label="base")
    ax.scatter(*path[-1], color=PALETTE["red"], s=90, label="exp(v)")
    ax.legend()
    ax.set_axis_off()
    ax.set_title("Exp and log turn local tangent vectors into geodesic moves")
    p1 = save_fig(fig, ch.key, "riemannian-exp-log-map.png")

    from pyriemann.utils.mean import mean_riemann

    mats = np.stack([np.diag([1.0, 2.0]), np.array([[1.4, 0.35], [0.35, 0.9]])])
    mean = mean_riemann(mats, maxiter=30, tol=1e-8)
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    xs = np.linspace(0, 1, 30)
    eigs = np.array([np.linalg.eigvalsh((1 - s) * mats[0] + s * mats[1]) for s in xs])
    ax.plot(xs, eigs[:, 0], color=PALETTE["blue"], label="linear min eig")
    ax.plot(xs, eigs[:, 1], color=PALETTE["orange"], label="linear max eig")
    ax.axhline(np.min(np.linalg.eigvalsh(mean)), color=PALETTE["green"], ls="--", label="Riemannian mean min eig")
    ax.legend(frameon=False)
    ax.set_title("SPD metrics keep positive eigenvalues visible")
    p2 = save_fig(fig, ch.key, "spd-geodesic-comparison.png")
    checks = {"log_exp_roundtrip": float(np.linalg.norm(logs[-1] - tangent)), "spd_mean_min_eigenvalue": float(np.min(np.linalg.eigvalsh(mean)))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def appendix_c() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("appendix-c")
    rng = rng_for(ch.key)
    beta = rng.beta(1, 4, size=18)
    weights = beta * np.concatenate([[1], np.cumprod(1 - beta[:-1])])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(np.arange(len(weights)), weights, color=PALETTE["blue"])
    ax.set_xlabel("atom index")
    ax.set_ylabel("stick weight")
    ax.set_title("Stick-breaking makes a random discrete probability measure")
    p1 = save_fig(fig, ch.key, "stick-breaking-measure.png")

    colors = []
    counts: dict[int, int] = {}
    alpha = 1.6
    for i in range(80):
        probs = [counts.get(k, 0) for k in range(len(counts))]
        probs.append(alpha)
        probs = np.array(probs, dtype=float) / (i + alpha)
        choice = rng.choice(len(probs), p=probs)
        if choice == len(counts):
            counts[choice] = 0
        counts[choice] += 1
        colors.append(choice)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.scatter(np.arange(len(colors)), colors, c=colors, cmap="tab20", s=24)
    ax.set_xlabel("draw")
    ax.set_ylabel("cluster")
    ax.set_title("Polya urn reinforcement creates repeated atoms")
    p2 = save_fig(fig, ch.key, "polya-urn-clusters.png")
    checks = {"stick_sum_first_18": float(weights.sum()), "cluster_count": int(len(counts)), "largest_cluster": int(max(counts.values()))}
    save_checks(ch.key, checks)
    return [p1, p2], checks


def appendix_d() -> tuple[list[Path], dict[str, object]]:
    ch = chapter_by_key("appendix-d")
    theta = np.linspace(-np.pi, np.pi, 400)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for k, color in zip([0.5, 2.0, 8.0], [PALETTE["blue"], PALETTE["green"], PALETTE["red"]], strict=True):
        dens = np.exp(k * np.cos(theta)) / (2 * np.pi * i0(k))
        ax.plot(theta, dens, color=color, lw=2, label=f"kappa={k}")
    ax.legend(frameon=False)
    ax.set_xlabel("spherical/circular coordinate slice")
    ax.set_ylabel("density")
    ax.set_title("Parametric directional models tune concentration explicitly")
    p1 = save_fig(fig, ch.key, "sphere-parametric-family.png")

    rng = rng_for(ch.key)
    base = np.array([[-0.8, -0.5], [0.85, -0.45], [0.05, 0.95]])
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    for sigma, color in zip([0.04, 0.11, 0.2], [PALETTE["green"], PALETTE["orange"], PALETTE["violet"]], strict=True):
        coords = []
        for _ in range(55):
            coords.append(triangle_shape_coordinates(base + rng.normal(scale=sigma, size=base.shape)))
        coords = normalize_rows(np.array(coords))
        ax.scatter(coords[:, 0], coords[:, 1], s=16, alpha=0.6, color=color, label=f"sigma={sigma}")
    ax.legend(frameon=False)
    ax.set_aspect("equal")
    ax.set_title("Planar shape baselines concentrate around a template")
    p2 = save_fig(fig, ch.key, "shape-space-parametric-baseline.png")
    checks = {"vmf_slice_integral": float(np.trapezoid(np.exp(2.0 * np.cos(theta)) / (2 * np.pi * i0(2.0)), theta)), "shape_samples_per_level": 55}
    save_checks(ch.key, checks)
    return [p1, p2], checks


BUILDERS = {
    "chapter-01": ch01,
    "chapter-02": ch02,
    "chapter-03": ch03,
    "chapter-04": ch04,
    "chapter-05": ch05,
    "chapter-06": ch06,
    "chapter-07": ch07,
    "chapter-08": ch08,
    "chapter-09": ch09,
    "chapter-10": ch10,
    "chapter-11": ch11,
    "chapter-12": ch12,
    "chapter-13": ch13,
    "chapter-14": ch14,
    "appendix-a": appendix_a,
    "appendix-b": appendix_b,
    "appendix-c": appendix_c,
    "appendix-d": appendix_d,
}


def main() -> None:
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, object] = {}
    for chapter in CHAPTERS:
        paths, checks = BUILDERS[chapter.key]()
        record_final_sanity(chapter.key, paths, {"source_pdf_pages": chapter.pdf_pages, "checks": checks})
        summary[chapter.key] = {
            "title": chapter.title,
            "artifacts": [str(path.relative_to(BOOK_ROOT)) for path in paths],
            "checks": checks,
        }
    (ARTIFACT_ROOT / "artifact-manifest.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Generated artifacts for {len(summary)} chapters/appendices")


if __name__ == "__main__":
    main()
