"""Chapter-specific storyboard visual helpers for the VDGF notebooks.

The functions in this module are intentionally small teaching tools.  They
render concept-labeled diagrams from per-notebook storyboards; the storyboard
chooses the mathematics, while the shared code handles deterministic plotting,
artifact paths, and basic image statistics.
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from utils.artifacts import artifact_path


PALETTE = {
    "ink": "#1d2733",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
    "paper": "#fbfcfe",
}


def _seed(*parts: object) -> int:
    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _style(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#b6c0ca")


def _note(ax: Any, text: str) -> None:
    ax.text(
        0.02,
        0.98,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        color=PALETTE["ink"],
        bbox={"boxstyle": "round,pad=0.28", "facecolor": "white", "edgecolor": "#d0d7de", "alpha": 0.92},
    )


def _stats(path: Path) -> dict[str, Any]:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=float)
    return {
        "width": int(image.width),
        "height": int(image.height),
        "pixel_std": float(arr.std()),
        "file_size": int(path.stat().st_size),
    }


def _plot_limit(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    t = np.linspace(0.08, 1.1, 180)
    ratio = np.tan(t) / t
    chord = 2 * np.sin(t / 2) / t
    ax.plot(t, ratio, color=PALETTE["blue"], label="tan(theta) / theta")
    ax.plot(t, chord, color=PALETTE["teal"], label="chord / arc")
    ax.axhline(1, color=PALETTE["gray"], linestyle="--", linewidth=1)
    ax.set_xlabel("theta")
    ax.set_ylabel("dimensionless ratio")
    ax.legend(fontsize=8)
    _style(ax, spec["concept"])
    _note(ax, "limit ratios expose the geometric invariant")
    return {"limit_ratio_error": float(abs(ratio[0] - 1)), "first_theta": float(t[0])}


def _plot_geometry(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    angle = np.linspace(0, math.pi / 2, 90)
    ax.plot([0, 1, 0.25, 0], [0, 0, 0.82, 0], color=PALETTE["blue"], lw=2, label="flat triangle")
    ax.plot(1.55 + np.cos(angle), np.sin(angle), color=PALETTE["teal"], lw=2, label="spherical geodesic")
    disk = plt.Circle((3.45, 0.45), 0.75, fill=False, color=PALETTE["gray"], lw=1.3)
    ax.add_patch(disk)
    x = np.linspace(-0.58, 0.58, 120)
    ax.plot(3.45 + x, 0.45 + 0.62 * (1 - x**2), color=PALETTE["red"], lw=2, label="hyperbolic geodesic")
    ax.text(0.28, 0.18, "angle sum = pi", fontsize=8)
    ax.text(1.73, 0.85, "excess > 0", fontsize=8)
    ax.text(3.2, 1.18, "defect < 0", fontsize=8)
    ax.set_xlim(-0.2, 4.4)
    ax.set_ylim(-0.18, 1.45)
    ax.legend(fontsize=8, loc="lower right")
    _style(ax, spec["concept"], equal=True)
    return {"model_count": 3, "spherical_excess_sign": 1, "hyperbolic_excess_sign": -1}


def _plot_curvature(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    r = np.linspace(0.03, 1.25, 180)
    for k, color, label in [(1.0, PALETTE["teal"], "K=+1"), (0.0, PALETTE["gray"], "K=0"), (-1.0, PALETTE["red"], "K=-1")]:
        if k > 0:
            c = 2 * math.pi * np.sin(r)
            area = 2 * math.pi * (1 - np.cos(r))
        elif k < 0:
            c = 2 * math.pi * np.sinh(r)
            area = 2 * math.pi * (np.cosh(r) - 1)
        else:
            c = 2 * math.pi * r
            area = math.pi * r**2
        ax.plot(r, c - 2 * math.pi * r, color=color, lw=2, label=f"{label} circumference")
        ax.plot(r, area - math.pi * r**2, color=color, lw=1, linestyle="--", alpha=0.8)
    ax.set_xlabel("geodesic radius")
    ax.set_ylabel("defect from flat formula")
    ax.legend(fontsize=8)
    _style(ax, spec["concept"])
    return {"sample_radius": float(r[12]), "positive_defect_sign": -1, "negative_defect_sign": 1}


def _plot_metric(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    xs = np.linspace(-2.0, 2.0, 11)
    ys = np.linspace(-2.0, 2.0, 11)
    for x in xs:
        ax.plot([x] * len(ys), ys, color="#d7dde5", lw=0.7)
    for y in ys:
        ax.plot(xs, [y] * len(xs), color="#d7dde5", lw=0.7)
    scales = []
    for x in np.linspace(-1.55, 1.55, 5):
        for y in np.linspace(-1.55, 1.55, 5):
            scale = 2 / (1 + x * x + y * y)
            scales.append(scale)
            ellipse = plt.matplotlib.patches.Ellipse((x, y), 0.24 * scale, 0.16 * scale, angle=18 * x, fill=False, color=PALETTE["blue"], lw=1.1)
            ax.add_patch(ellipse)
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-2.25, 2.25)
    _style(ax, spec["concept"], equal=True)
    _note(ax, "metric coefficients turn coordinate steps into lengths")
    return {"min_scale": float(min(scales)), "max_scale": float(max(scales))}


def _plot_surface(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    x = np.linspace(-1.6, 1.6, 70)
    y = np.linspace(-1.6, 1.6, 70)
    X, Y = np.meshgrid(x, y)
    chapter = int(spec.get("chapter", 1))
    Z = 0.45 * np.sin((chapter % 4 + 1) * X) + 0.35 * np.cos((chapter % 5 + 1) * Y) + 0.18 * (X**2 - Y**2)
    filled = ax.contourf(X, Y, Z, levels=18, cmap="viridis", alpha=0.9)
    ax.contour(X, Y, Z, levels=9, colors="white", linewidths=0.45, alpha=0.8)
    ax.quiver([0], [0], [0.8], [0.28], color=PALETTE["red"], angles="xy", scale_units="xy", scale=1)
    plt.colorbar(filled, ax=ax, fraction=0.046, pad=0.04, label="height / potential")
    _style(ax, spec["concept"], equal=True)
    return {"height_min": float(Z.min()), "height_max": float(Z.max())}


def _plot_curve(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    t = np.linspace(-2.5, 2.5, 260)
    y = np.sin(t) + 0.25 * np.sin(2 * t + 0.1 * int(spec.get("chapter", 1)))
    ax.plot(t, y, color=PALETTE["blue"], lw=2, label="curve")
    for idx in np.linspace(40, 220, 5, dtype=int):
        dy = np.cos(t[idx]) + 0.5 * np.cos(2 * t[idx] + 0.1 * int(spec.get("chapter", 1)))
        ddy = -np.sin(t[idx]) - np.sin(2 * t[idx] + 0.1 * int(spec.get("chapter", 1)))
        kappa = abs(ddy) / (1 + dy * dy) ** 1.5
        radius = min(0.65, 1 / max(kappa, 0.4))
        ax.add_patch(plt.Circle((t[idx], y[idx]), 0.12 * radius, fill=False, color=PALETTE["teal"], alpha=0.75))
        ax.scatter([t[idx]], [y[idx]], color=PALETTE["red"], s=18)
    ax.set_xlabel("parameter")
    ax.set_ylabel("position")
    ax.legend(fontsize=8)
    _style(ax, spec["concept"])
    return {"sample_count": 260, "curvature_samples": 5}


def _plot_frame(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    t = np.linspace(0, 4 * math.pi, 260)
    ax3.plot(np.cos(t), np.sin(t), t / (2 * math.pi), color=PALETTE["blue"], lw=2)
    for idx in [35, 95, 155, 215]:
        p = np.array([np.cos(t[idx]), np.sin(t[idx]), t[idx] / (2 * math.pi)])
        tangent = np.array([-np.sin(t[idx]), np.cos(t[idx]), 1 / (2 * math.pi)])
        tangent = tangent / np.linalg.norm(tangent)
        normal = np.array([-np.cos(t[idx]), -np.sin(t[idx]), 0.0])
        binormal = np.cross(tangent, normal)
        ax3.quiver(*p, *tangent, length=0.35, color=PALETTE["red"])
        ax3.quiver(*p, *normal, length=0.28, color=PALETTE["teal"])
        ax3.quiver(*p, *binormal, length=0.25, color=PALETTE["gold"])
    ax3.set_title(spec["concept"], fontsize=11)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("height")
    return {"frame_samples": 4, "has_tangent_normal_binormal": True}


def _plot_topology(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    genus = np.arange(0, 5)
    chi = 2 - 2 * genus
    total = 2 * math.pi * chi
    ax.bar(genus, total, color=[PALETTE["teal"], PALETTE["blue"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]])
    ax.axhline(0, color=PALETTE["ink"], lw=1)
    for g, value in zip(genus, total):
        ax.text(g, value + (0.35 if value >= 0 else -0.75), f"chi={2-2*g}", ha="center", fontsize=8)
    ax.set_xlabel("genus")
    ax.set_ylabel("2 pi chi")
    _style(ax, spec["concept"])
    return {"genus_values": genus.tolist(), "euler_values": chi.tolist()}


def _plot_field(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    x = np.linspace(-1.6, 1.6, 18)
    y = np.linspace(-1.6, 1.6, 18)
    X, Y = np.meshgrid(x, y)
    power = 1 + (_seed(spec["concept"]) % 4)
    angle = power * np.arctan2(Y, X)
    U, V = np.cos(angle), np.sin(angle)
    ax.quiver(X, Y, U, V, color=PALETTE["blue"], pivot="mid", scale=30)
    ax.scatter([0], [0], color=PALETTE["red"], s=45)
    circle = plt.Circle((0, 0), 1.15, fill=False, color=PALETTE["gold"], lw=1.5)
    ax.add_patch(circle)
    _style(ax, spec["concept"], equal=True)
    _note(ax, f"loop winding sample: index {power}")
    return {"winding_index_model": power}


def _plot_transport(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    theta = np.linspace(0, 2 * math.pi, 260)
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["gray"], lw=1.4)
    phase = 0.12 * (int(spec.get("chapter", 1)) + spec.get("index", 0))
    for t in np.linspace(0, 2 * math.pi, 14, endpoint=False):
        p = np.array([np.cos(t), np.sin(t)])
        tangent = np.array([-np.sin(t), np.cos(t)])
        normal = np.array([np.cos(t + phase), np.sin(t + phase)])
        v = 0.18 * tangent + 0.12 * normal
        ax.arrow(p[0], p[1], v[0], v[1], head_width=0.045, color=PALETTE["teal"], length_includes_head=True)
    ax.fill_between(np.cos(theta[:80]), np.sin(theta[:80]), 0, color=PALETTE["gold"], alpha=0.18)
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.35, 1.35)
    _style(ax, spec["concept"], equal=True)
    _note(ax, "transport around a loop measures curvature")
    return {"transport_arrows": 14, "phase": float(phase)}


def _plot_forms(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    x = np.linspace(-2.0, 2.0, 160)
    offsets = np.linspace(-2.0, 2.0, 7)
    for b in offsets:
        ax.plot(x, -0.65 * x + b, color=PALETTE["blue"], alpha=0.75)
    ax.arrow(-1.45, -0.8, 1.25, 0.9, head_width=0.08, color=PALETTE["red"], length_includes_head=True)
    ax.arrow(0.25, -1.2, 0.55, 1.35, head_width=0.08, color=PALETTE["teal"], length_includes_head=True)
    ax.text(-1.35, -1.05, "vector input", fontsize=8)
    ax.text(0.35, 0.25, "measured slices", fontsize=8)
    _style(ax, spec["concept"], equal=True)
    return {"level_sets": len(offsets), "test_vectors": 2}


def _plot_tensor(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    matrix = np.array([[2.0, 0.55, -0.15], [0.55, 1.2, 0.35], [-0.15, 0.35, 0.8]])
    image = ax.imshow(matrix, cmap="YlGnBu")
    for (i, j), value in np.ndenumerate(matrix):
        ax.text(j, i, f"{value:.2g}", ha="center", va="center", fontsize=9, color=PALETTE["ink"])
    ax.set_xticks(range(3), ["slot 1", "slot 2", "slot 3"], fontsize=8)
    ax.set_yticks(range(3), ["basis a", "basis b", "basis c"], fontsize=8)
    plt.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    _style(ax, spec["concept"])
    return {"matrix_trace": float(np.trace(matrix)), "symmetric": bool(np.allclose(matrix, matrix.T))}


def _plot_spacetime(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    x = np.linspace(-1.5, 1.5, 160)
    ax.plot(x, x, color=PALETTE["gold"], lw=2, label="light cone")
    ax.plot(x, -x, color=PALETTE["gold"], lw=2)
    ax.plot(x, 0.45 * x**2 - 0.2, color=PALETTE["blue"], lw=2, label="free-fall worldline")
    ax.fill_between(x, -abs(x), abs(x), color=PALETTE["gold"], alpha=0.12)
    ax.set_xlabel("space")
    ax.set_ylabel("time")
    ax.legend(fontsize=8)
    _style(ax, spec["concept"], equal=True)
    return {"light_cone_slope": 1, "worldline_samples": len(x)}


def _plot_proof(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    ax.axis("off")
    nodes = ["object", "visual", "formula", "check"]
    xs = [0.1, 0.36, 0.62, 0.86]
    colors = [PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["red"]]
    for idx, (label, x, color) in enumerate(zip(nodes, xs, colors)):
        rect = plt.Rectangle((x - 0.09, 0.42), 0.18, 0.18, facecolor=color, alpha=0.18, edgecolor=color, lw=1.5)
        ax.add_patch(rect)
        ax.text(x, 0.51, label, ha="center", va="center", fontsize=9, color=PALETTE["ink"])
        if idx:
            ax.annotate("", xy=(x - 0.11, 0.51), xytext=(xs[idx - 1] + 0.11, 0.51), arrowprops={"arrowstyle": "->", "color": PALETTE["gray"]})
    ax.text(0.5, 0.28, spec.get("observation", "proof state made inspectable"), ha="center", fontsize=9, color=PALETTE["ink"])
    ax.set_title(spec["concept"], fontsize=11, color=PALETTE["ink"])
    return {"proof_nodes": nodes}


def _plot_lab(ax: Any, spec: dict[str, Any]) -> dict[str, Any]:
    ax.axis("off")
    rows = [
        ("construct", "choose an inspectable model"),
        ("measure", "compute length/area/turning"),
        ("compare", "check invariant or defect"),
        ("perturb", "change a parameter and rerun"),
    ]
    for i, (left, right) in enumerate(rows):
        y = 0.82 - i * 0.18
        ax.add_patch(plt.Rectangle((0.08, y - 0.055), 0.22, 0.1, facecolor=PALETTE["teal"], alpha=0.16, edgecolor=PALETTE["teal"]))
        ax.add_patch(plt.Rectangle((0.34, y - 0.055), 0.56, 0.1, facecolor=PALETTE["blue"], alpha=0.10, edgecolor=PALETTE["blue"]))
        ax.text(0.19, y, left, ha="center", va="center", fontsize=9)
        ax.text(0.62, y, right, ha="center", va="center", fontsize=9)
    ax.set_title(spec["concept"], fontsize=11, color=PALETTE["ink"])
    return {"lab_steps": len(rows)}


PLOTTERS = {
    "limit": _plot_limit,
    "geometry": _plot_geometry,
    "curvature": _plot_curvature,
    "metric": _plot_metric,
    "surface": _plot_surface,
    "mesh": _plot_surface,
    "curve": _plot_curve,
    "frame": _plot_frame,
    "topology": _plot_topology,
    "field": _plot_field,
    "transport": _plot_transport,
    "forms": _plot_forms,
    "tensor": _plot_tensor,
    "spacetime": _plot_spacetime,
    "proof": _plot_proof,
    "lab": _plot_lab,
}


def render_storyboard_visual(spec: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> tuple[Path, dict[str, Any]]:
    """Render one storyboard visual and return its path plus metrics."""

    filename = spec["filename"]
    if Path(filename).suffix.lower() != ".png":
        raise ValueError(f"storyboard visual helper writes PNG artifacts, got {filename!r}")

    plotter = PLOTTERS.get(str(spec.get("kind", "proof")), _plot_proof)
    fig, ax = plt.subplots(figsize=(7.2, 4.8), facecolor=PALETTE["paper"])
    metrics = plotter(ax, spec)
    caption = spec.get("observation", "")
    if caption:
        fig.suptitle(caption, fontsize=8.5, y=0.01, color=PALETTE["gray"])
    path = artifact_path(artifact_topic, "figures", filename, root=artifact_root)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    image_metrics = _stats(path)
    if image_metrics["file_size"] <= 1000 or image_metrics["pixel_std"] <= 1.0:
        raise ValueError(f"visual artifact looks blank or too small: {path}")
    return path, {**metrics, **image_metrics}


def build_visual_storyboard(storyboard: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> list[dict[str, Any]]:
    """Render every visual in a chapter storyboard."""

    results: list[dict[str, Any]] = []
    for index, spec in enumerate(storyboard["visual_sequence"], start=1):
        full_spec = {**spec, "chapter": storyboard.get("chapter_number", 0), "index": index}
        path, metrics = render_storyboard_visual(full_spec, artifact_root, artifact_topic)
        results.append(
            {
                "concept": spec["concept"],
                "filename": spec["filename"],
                "path": path.as_posix(),
                "relative_path": path.relative_to(Path(artifact_root).parent).as_posix()
                if Path(artifact_root).parent in path.parents
                else path.as_posix(),
                "kind": spec.get("kind", "proof"),
                "inspection_target": spec.get("observation", ""),
                "metrics": metrics,
            }
        )
    return results


def chapter_check_payload(storyboard: dict[str, Any], visual_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Return lightweight chapter-specific numeric checks for final sanity cells."""

    chapter_number = int(storyboard.get("chapter_number", 0))
    visual_count = len(visual_results)
    genus = np.arange(0, 4)
    euler = (2 - 2 * genus).astype(int)
    theta = np.linspace(0.05, 0.4, 8)
    limit_errors = np.abs(np.tan(theta) / theta - 1)
    wedge_matrix = np.array([[1.0, 2.0], [3.0, 5.0]])
    determinant = float(np.linalg.det(wedge_matrix))
    payload = {
        "chapter_number": chapter_number,
        "chapter_label": storyboard.get("chapter_label"),
        "visual_count": visual_count,
        "artifact_filenames": [item["filename"] for item in visual_results],
        "families": sorted({item["kind"] for item in visual_results}),
        "invariants": {
            "limit_error_decreases_near_zero": bool(limit_errors[0] < limit_errors[-1]),
            "spherical_octant_excess": math.pi / 2,
            "gauss_bonnet_chi_values": euler.tolist(),
            "gauss_bonnet_totals": (2 * math.pi * euler).tolist(),
            "wedge_determinant_sample": determinant,
            "unit_circle_curvature": 1.0,
            "poincare_radial_distance_sample": float(2 * np.arctanh(0.25)),
        },
        "assertions": {
            "has_multiple_visuals": visual_count >= 3,
            "all_visuals_nonblank": all(item["metrics"]["pixel_std"] > 1.0 for item in visual_results),
            "all_visuals_named": all("-" in item["filename"] for item in visual_results),
            "euler_sphere_is_two": int(euler[0]) == 2,
            "wedge_orientation_nonzero": abs(determinant) > 0,
            "limit_sample_is_small": float(limit_errors[0]) < 0.01,
        },
    }
    return payload
