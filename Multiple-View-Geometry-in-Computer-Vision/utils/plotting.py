"""Stable plotting helpers for the MVG notebooks."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np


COLORS = {
    "ink": "#1f2937",
    "blue": "#2563eb",
    "teal": "#0f766e",
    "green": "#4d7c0f",
    "orange": "#c2410c",
    "red": "#b91c1c",
    "purple": "#6d28d9",
    "gray": "#6b7280",
    "light": "#eef2ff",
}


def style_axis(ax, *, title: str | None = None, equal: bool = True) -> None:
    if title:
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.grid(True, color="#e5e7eb", linewidth=0.8)
    ax.set_facecolor("white")
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#d1d5db")
    ax.tick_params(labelsize=8)


def concept_map_figure(title: str, concepts: list[str], visuals: list[str]):
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold")
    center = np.array([0.5, 0.52])
    ax.scatter([center[0]], [center[1]], s=900, color=COLORS["blue"], alpha=0.92)
    ax.text(center[0], center[1], "MVG\nquestion", color="white", ha="center", va="center", fontsize=10, fontweight="bold")
    items = [(c, COLORS["teal"]) for c in concepts] + [(v, COLORS["orange"]) for v in visuals]
    angles = np.linspace(0.0, 2 * np.pi, len(items), endpoint=False)
    for idx, ((text, color), angle) in enumerate(zip(items, angles)):
        radius = 0.34 + 0.04 * (idx % 2)
        pos = center + radius * np.array([np.cos(angle), np.sin(angle)])
        ax.plot([center[0], pos[0]], [center[1], pos[1]], color="#cbd5e1", linewidth=1.3)
        ax.scatter([pos[0]], [pos[1]], s=260, color=color, alpha=0.92, edgecolor="white", linewidth=1.2)
        wrapped = "\n".join(_wrap_words(text, 22))
        ax.text(pos[0], pos[1], wrapped, ha="center", va="center", fontsize=7.3, color="white")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    return fig


def _wrap_words(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        if sum(len(w) + 1 for w in current) + len(word) > width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines[:4]


def vision_scene_figure(mode: str, title: str, seed: int):
    rng = np.random.default_rng(seed)
    if mode in {"p3", "camera", "camera-estimation", "single-view", "epipolar", "reconstruction", "fundamental-estimation", "triangulation", "plane-homography", "affine-epipolar", "trifocal", "trifocal-estimation", "nlinear", "nview-methods", "autocalibration", "duality", "cheirality", "degenerate"}:
        fig = plt.figure(figsize=(8.2, 6.2))
        ax = fig.add_subplot(111, projection="3d")
        ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
        centers = np.array([[-2.2, 0.1, -3.2], [2.0, 0.3, -3.0], [0.2, 1.6, -3.6]])
        scene = rng.normal(size=(16, 3)) * np.array([1.1, 0.65, 0.85]) + np.array([0.0, 0.1, 2.2])
        ax.scatter(scene[:, 0], scene[:, 1], scene[:, 2], s=34, c=COLORS["teal"], depthshade=True, label="scene points")
        for i, c in enumerate(centers):
            ax.scatter([c[0]], [c[1]], [c[2]], s=70, c=[COLORS["blue"], COLORS["orange"], COLORS["purple"]][i], marker="^", label=f"camera {i+1}")
            for p in scene[:5]:
                ax.plot([c[0], p[0]], [c[1], p[1]], [c[2], p[2]], color="#cbd5e1", linewidth=0.8, alpha=0.75)
        t = np.linspace(-1, 1, 5)
        xx, yy = np.meshgrid(t, t)
        zz = np.full_like(xx, 1.25)
        ax.plot_wireframe(xx, yy, zz, color="#94a3b8", linewidth=0.55, alpha=0.8)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.view_init(elev=20 + seed % 15, azim=-50 + seed % 40)
        ax.legend(loc="upper left", fontsize=7)
        return fig
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    style_axis(ax, title=title)
    xs = np.linspace(-2.0, 2.0, 9)
    ys = np.linspace(-1.4, 1.4, 7)
    H = np.array([[1.0, 0.12 + 0.015 * (seed % 7), 0.2], [-0.08, 1.0, 0.15], [0.06, -0.035, 1.0]])
    for x in xs:
        pts = np.column_stack([np.full_like(ys, x), ys, np.ones_like(ys)])
        mapped = (H @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        ax.plot(mapped[:, 0], mapped[:, 1], color=COLORS["blue"], alpha=0.78, linewidth=1.2)
    for y in ys:
        pts = np.column_stack([xs, np.full_like(xs, y), np.ones_like(xs)])
        mapped = (H @ pts.T).T
        mapped = mapped[:, :2] / mapped[:, 2:]
        ax.plot(mapped[:, 0], mapped[:, 1], color=COLORS["orange"], alpha=0.78, linewidth=1.2)
    ax.scatter([-1.2, 0.4, 1.1], [0.8, -0.2, 0.6], s=50, color=COLORS["teal"], edgecolor="white", zorder=4)
    ax.text(-1.9, -1.75, f"mode: {mode}", fontsize=8, color=COLORS["gray"])
    return fig


def diagnostic_figure(title: str, checks: list[str], seed: int):
    rng = np.random.default_rng(seed)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
    x = np.linspace(0, 1, 80)
    for i, check in enumerate(checks[:4]):
        y = np.exp(-(i + 1) * x) + 0.025 * rng.normal(size=x.size) + 0.04 * i
        axes[0].plot(x, y, linewidth=2, label=f"check {i+1}")
    axes[0].set_title("residual traces", loc="left", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("normalized experiment step")
    axes[0].set_ylabel("diagnostic value")
    axes[0].legend(fontsize=7)
    axes[0].grid(True, color="#e5e7eb")
    A = rng.normal(size=(8, 8))
    heat = A @ A.T
    heat = heat / np.max(np.abs(heat))
    im = axes[1].imshow(heat, cmap="viridis", origin="lower")
    axes[1].set_title(title, loc="left", fontsize=11, fontweight="bold")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    fig.colorbar(im, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    return fig


def constraint_dashboard_figure(title: str, mode: str, seed: int):
    rng = np.random.default_rng(seed)
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    style_axis(ax, title=title, equal=False)
    base = np.sort(np.abs(rng.normal(size=9)))[::-1] + np.linspace(1.0, 0.04, 9)
    if mode in {"epipolar", "fundamental-estimation", "trifocal", "degenerate"}:
        base[-1] *= 0.04
    if mode == "degenerate":
        base[-2:] *= 0.02
    ax.semilogy(np.arange(1, len(base) + 1), base, marker="o", color=COLORS["purple"], linewidth=2)
    ax.fill_between(np.arange(1, len(base) + 1), base, base.min() * 0.5, color=COLORS["purple"], alpha=0.12)
    ax.set_xlabel("singular value index")
    ax.set_ylabel("relative scale")
    ax.text(0.02, 0.08, f"constraint family: {mode}", transform=ax.transAxes, fontsize=9, color=COLORS["ink"])
    return fig


def compute_visual_summary(title: str, mode: str, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(9, 9))
    if mode in {"epipolar", "fundamental-estimation", "degenerate"}:
        A[-1] = A[-2] + 1e-3 * rng.normal(size=9)
    s = np.linalg.svd(A, compute_uv=False)
    residual = float(s[-1] / max(s[0], 1e-12))
    cov = rng.normal(size=(3, 200))
    cov = np.cov(cov)
    return {
        "title": title,
        "mode": mode,
        "seed": seed,
        "rank_estimate": int(np.linalg.matrix_rank(A, tol=1e-8)),
        "smallest_singular_ratio": residual,
        "covariance_min_eigenvalue": float(np.linalg.eigvalsh(cov).min()),
    }
