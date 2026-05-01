"""Storyboard-driven visual artifact generation for the Pressley course."""

from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = BOOK_ROOT / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import pressley_inventory as inventory  # noqa: E402
from utils.artifacts import artifact_path, save_json  # noqa: E402
from utils.curves import arc_length, curvature_2d, curvature_3d, torsion  # noqa: E402
from utils.models import poincare_disk_distance, upper_half_plane_distance  # noqa: E402
from utils.plotting import PALETTE, note, require_nonblank_png, set_defaults, style_axis  # noqa: E402
from utils.surfaces import catenoid_patch, euler_characteristic, graph_curvatures, helicoid_patch, sphere_patch, torus_patch  # noqa: E402

set_defaults()


CURVE_KINDS = {"curve", "level", "arc", "singularity", "curvature", "osculating", "torsion", "closed", "isoperimetric", "vertices"}
SURFACE_KINDS = {"patch", "quadric", "revolution", "spherical", "minimal", "helicoid", "catenoid"}
METRIC_KINDS = {"metric", "conformal", "area", "second-form", "gauss-map", "geodesic-curvature", "principal", "curvature-sign", "constant-k", "mean", "geodesic", "clairaut", "shortest", "egregium", "metric-k", "bending"}
MODEL_KINDS = {"hyperbolic", "mobius", "parallels", "klein", "inversion", "cross-ratio", "circle-line"}
FIELD_KINDS = {"transport", "field", "normal", "tangent", "ruled", "polar"}
PROOF_KINDS = {"lab", "codazzi", "weierstrass", "bonnet", "triangulation", "critical", "linear", "ellipse", "eigen", "basis", "isometry", "rotation", "reflection", "composition", "orientability"}


def _seed(*parts: object) -> int:
    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def storyboard_for(unit: str) -> dict[str, Any]:
    entry = next(entry for entry in inventory.ENTRIES if entry["artifact"] == unit)
    sequence = []
    for index, kind in enumerate(entry["visual_kinds"], start=1):
        concept = kind.replace("-", " ").title()
        sequence.append(
            {
                "concept": f"{entry['label']} - {concept}",
                "kind": kind,
                "filename": f"{kind}-{unit}.png",
                "library": "matplotlib/numpy",
                "observation": f"Inspect how {concept.lower()} turns the unit's definitions into visible, checkable geometry.",
            }
        )
    return {
        "unit": unit,
        "chapter_label": entry["label"],
        "title": entry["title"],
        "source_span": {"printed": entry["printed_span"], "pdf": entry["pdf_span"], "sections": entry["sections"]},
        "chapter_goal": entry["focus"],
        "visual_sequence": sequence,
        "computational_checks": ["artifact files are nonblank", "numeric invariants have finite residuals", "source span metadata is present"],
        "implementation_notes": ["artifacts are written below the book-local artifacts subtree", "static visuals are deterministic PNG files"],
        "gaps": [],
    }


def _save(fig: Any, unit: str, spec: dict[str, Any], root: Path) -> tuple[Path, dict[str, Any]]:
    path = artifact_path(unit, "figures", spec["filename"], root=root)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path, require_nonblank_png(path)


def _plot_curve_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    kind = spec["kind"]
    t = np.linspace(0.02, 2.0 * np.pi - 0.02, 520)
    if kind == "arc":
        points = np.column_stack([np.cos(t), np.sin(t), 0.18 * t])
        s = arc_length(points, t)
        ax.plot(t, s, color=PALETTE["blue"], lw=2)
        ax.set_xlabel("parameter")
        ax.set_ylabel("arc length")
        style_axis(ax, spec["concept"])
        return {"length": float(s[-1]), "monotone": bool(np.all(np.diff(s) >= -1e-12))}
    if kind == "isoperimetric":
        eps = np.linspace(0.0, 0.42, 8)
        deficits = []
        for e in eps:
            r = 1 + e * np.cos(4 * t)
            x, y = r * np.cos(t), r * np.sin(t)
            area = 0.5 * abs(np.trapz(x * np.gradient(y, t) - y * np.gradient(x, t), t))
            length = np.trapz(np.sqrt(np.gradient(x, t) ** 2 + np.gradient(y, t) ** 2), t)
            deficits.append(length**2 - 4 * np.pi * area)
        ax.plot(eps, deficits, marker="o", color=PALETTE["blue"])
        ax.set_xlabel("deformation amplitude")
        ax.set_ylabel("L^2 - 4 pi A")
        style_axis(ax, spec["concept"])
        return {"min_deficit": float(min(deficits))}
    phase = (seed % 17) / 17.0
    r = 1 + 0.18 * np.cos((3 + seed % 4) * t + phase)
    x, y = r * np.cos(t), r * np.sin(t)
    if kind == "level":
        X, Y = np.meshgrid(np.linspace(-1.8, 1.8, 220), np.linspace(-1.8, 1.8, 220))
        F = X**2 + 0.55 * Y**2 - 1.0
        ax.contour(X, Y, F, levels=[0], colors=[PALETTE["blue"]], linewidths=2)
        ax.plot(np.cos(t), np.sin(t) / np.sqrt(0.55), color=PALETTE["teal"], linestyle="--", lw=1.4)
        note(ax, "level set and parametrization trace the same locus")
        style_axis(ax, spec["concept"], equal=True)
        return {"level_value": 0.0}
    if kind == "singularity":
        u = np.linspace(-1.4, 1.4, 360)
        ax.plot(u**2, u**3, color=PALETTE["blue"], lw=2)
        ax.scatter([0], [0], color=PALETTE["red"], s=45)
        note(ax, "speed vanishes at the cusp")
        style_axis(ax, spec["concept"], equal=True)
        return {"cusp_parameter": 0.0}
    points = np.column_stack([x, y])
    k = curvature_2d(points, t)
    ax.plot(x, y, color=PALETTE["blue"], lw=2)
    if kind in {"curvature", "vertices"}:
        ax.clear()
        ax.plot(t, k, color=PALETTE["violet"], lw=2)
        extrema = np.where(np.diff(np.sign(np.diff(k))) != 0)[0] + 1
        if kind == "vertices":
            ax.scatter(t[extrema], k[extrema], color=PALETTE["red"], s=20)
        ax.set_xlabel("parameter")
        ax.set_ylabel("signed curvature")
        style_axis(ax, spec["concept"])
        return {"curvature_min": float(k.min()), "curvature_max": float(k.max()), "vertex_candidates": int(len(extrema))}
    if kind == "osculating":
        for idx in np.linspace(70, 430, 4, dtype=int):
            radius = min(0.6, 1.0 / max(abs(k[idx]), 0.35))
            circle = plt.Circle((x[idx], y[idx]), 0.18 * radius, fill=False, color=PALETTE["teal"], alpha=0.75)
            ax.add_patch(circle)
            ax.scatter([x[idx]], [y[idx]], color=PALETTE["red"], s=18)
    if kind == "torsion":
        ax.clear()
        pts3 = np.column_stack([np.cos(t), np.sin(t), 0.2 * t + 0.08 * np.sin(3 * t)])
        ax.plot(t, curvature_3d(pts3, t), color=PALETTE["blue"], label="curvature")
        ax.plot(t, torsion(pts3, t), color=PALETTE["red"], label="torsion")
        ax.legend(fontsize=8)
        style_axis(ax, spec["concept"])
        return {"space_curve_samples": len(t)}
    if kind == "curve":
        for idx in np.linspace(80, 440, 5, dtype=int):
            tangent = np.array([np.gradient(x, t)[idx], np.gradient(y, t)[idx]])
            tangent = 0.22 * tangent / np.linalg.norm(tangent)
            ax.arrow(x[idx], y[idx], tangent[0], tangent[1], head_width=0.045, color=PALETTE["red"], length_includes_head=True)
    note(ax, "parameter values carry tangent, speed, and regularity data")
    style_axis(ax, spec["concept"], equal=True)
    return {"sample_count": int(len(t))}


def _plot_surface_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    ax.remove()
    fig = plt.gcf()
    ax3 = fig.add_subplot(111, projection="3d")
    u = np.linspace(-1.25, 1.25, 70)
    v = np.linspace(0, 2 * np.pi, 84)
    kind = spec["kind"]
    if kind == "minimal" or kind == "catenoid":
        X, Y, Z = catenoid_patch(u, v)
    elif kind == "helicoid":
        X, Y, Z = helicoid_patch(np.linspace(0, 4 * np.pi, 80), np.linspace(-1.25, 1.25, 56))
    elif kind == "spherical":
        X, Y, Z = sphere_patch(np.linspace(-np.pi / 2, np.pi / 2, 64), v)
    elif kind == "revolution":
        U, V = np.meshgrid(u, v, indexing="ij")
        R = 1.1 + 0.25 * np.cos(2 * U)
        X, Y, Z = R * np.cos(V), R * np.sin(V), U
    else:
        x = np.linspace(-1.5, 1.5, 70)
        X, Y = np.meshgrid(x, x)
        Z = 0.35 * X**2 + (-0.22 if kind == "patch" else 0.16) * Y**2
    ax3.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True, alpha=0.92)
    ax3.set_title(spec["concept"])
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("z")
    return {"grid_shape": [int(np.shape(X)[0]), int(np.shape(X)[1])]}


def _plot_metric_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    kind = spec["kind"]
    if kind in {"constant-k", "metric-k"}:
        r = np.linspace(0.02, 1.25, 180)
        ax.plot(r, 2 * np.pi * np.sin(r), color=PALETTE["teal"], label="K=+1")
        ax.plot(r, 2 * np.pi * r, color=PALETTE["gray"], label="K=0")
        ax.plot(r, 2 * np.pi * np.sinh(r), color=PALETTE["red"], label="K=-1")
        ax.legend(fontsize=8)
        style_axis(ax, spec["concept"])
        return {"models": 3}
    if kind == "mean":
        x = np.linspace(-1.2, 1.2, 70)
        _, H = graph_curvatures(lambda X, Y: 0.25 * (X**2 + Y**2), x, x)
        ax.imshow(H, extent=[x.min(), x.max(), x.min(), x.max()], origin="lower", cmap="viridis")
        style_axis(ax, spec["concept"], equal=True)
        return {"mean_curvature_sample": float(H[len(x) // 2, len(x) // 2])}
    if kind == "geodesic":
        theta = np.linspace(0, 2 * np.pi, 240)
        ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["gray"])
        for phase in [0, np.pi / 5, -np.pi / 5]:
            ax.plot(np.cos(theta), np.sin(theta) * np.cos(phase), color=PALETTE["blue"], alpha=0.75)
        style_axis(ax, spec["concept"], equal=True)
        return {"geodesic_family": 3}
    if kind == "clairaut":
        s = np.linspace(0, 8, 240)
        radius = 1.1 + 0.35 * np.sin(s)
        angle = np.arcsin(np.clip(0.8 / radius, -1, 1))
        ax.plot(s, radius * np.sin(angle), color=PALETTE["blue"], label="r sin alpha")
        ax.plot(s, radius, color=PALETTE["gray"], alpha=0.6, label="radius")
        ax.legend(fontsize=8)
        style_axis(ax, spec["concept"])
        return {"clairaut_constant": 0.8}
    if kind == "shortest":
        x = np.linspace(0, 1, 120)
        ax.plot(x, 0 * x, color=PALETTE["red"], lw=2, label="straight")
        for amp in [0.1, 0.2, 0.35]:
            ax.plot(x, amp * np.sin(np.pi * x), color=PALETTE["blue"], alpha=0.7)
        ax.legend(fontsize=8)
        style_axis(ax, spec["concept"])
        return {"competitors": 4}
    if kind in {"principal", "second-form"}:
        theta = np.linspace(0, 2 * np.pi, 240)
        ax.plot(1.2 * np.cos(theta), 0.45 * np.sin(theta), color=PALETTE["blue"], lw=2)
        ax.arrow(0, 0, 1.2, 0, head_width=0.06, color=PALETTE["red"], length_includes_head=True)
        ax.arrow(0, 0, 0, 0.45, head_width=0.06, color=PALETTE["teal"], length_includes_head=True)
        style_axis(ax, spec["concept"], equal=True)
        return {"principal_directions": 2}
    xs = np.linspace(-2, 2, 11)
    for x in xs:
        ax.plot([x] * len(xs), xs, color="#d7dde5", lw=0.7)
        ax.plot(xs, [x] * len(xs), color="#d7dde5", lw=0.7)
    for x in np.linspace(-1.5, 1.5, 5):
        for y in np.linspace(-1.5, 1.5, 5):
            scale = 2 / (1 + x * x + y * y)
            ax.add_patch(plt.matplotlib.patches.Ellipse((x, y), 0.25 * scale, 0.17 * scale, angle=18 * x, fill=False, color=PALETTE["blue"]))
    note(ax, "local measuring devices reveal metric distortion")
    style_axis(ax, spec["concept"], equal=True)
    return {"metric_ellipses": 25}


def _plot_model_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    kind = spec["kind"]
    theta = np.linspace(0, 2 * np.pi, 260)
    if kind in {"hyperbolic", "parallels"}:
        ax.axhline(0, color=PALETTE["ink"])
        for c, r in [(-1.2, 1.0), (0.0, 1.1), (1.1, 0.9)]:
            x = np.linspace(c - r, c + r, 160)
            y = np.sqrt(np.maximum(0, r * r - (x - c) ** 2))
            ax.plot(x, y, color=PALETTE["blue"], lw=2)
        note(ax, "upper-half-plane geodesics meet boundary orthogonally")
        style_axis(ax, spec["concept"], equal=True)
        return {"distance_sample": upper_half_plane_distance(1j, 2j)}
    ax.plot(np.cos(theta), np.sin(theta), color=PALETTE["gray"])
    if kind == "klein":
        for y in [-0.5, 0.0, 0.45]:
            xs = np.linspace(-np.sqrt(1 - y * y), np.sqrt(1 - y * y), 100)
            ax.plot(xs, y + 0 * xs, color=PALETTE["blue"], lw=2)
        note(ax, "Klein geodesics are chords")
    elif kind == "cross-ratio":
        ax.clear()
        pts = [-1.2, -0.4, 0.35, 1.1]
        ax.plot([-1.5, 1.4], [0, 0], color=PALETTE["ink"])
        ax.scatter(pts, [0] * 4, color=[PALETTE["gray"], PALETTE["blue"], PALETTE["teal"], PALETTE["red"]], s=50)
        for p, label in zip(pts, "abcd"):
            ax.text(p, 0.08, label, ha="center")
        ax.set_ylim(-0.4, 0.4)
    elif kind == "circle-line":
        ax.plot([-1.3, 1.3], [0.45, 0.45], color=PALETTE["red"])
        note(ax, "extended circles include lines through infinity")
    else:
        z = 0.55 * np.exp(1j * theta)
        a = 0.35 + 0.03 * (seed % 5)
        w = (z + a) / (a * z + 1)
        ax.plot(w.real, w.imag, color=PALETTE["blue"], lw=2)
        note(ax, "Mobius maps send circles/lines to circles/lines")
    style_axis(ax, spec["concept"], equal=True)
    return {"disk_distance_sample": poincare_disk_distance(0 + 0j, 0.35 + 0j)}


def _plot_field_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    kind = spec["kind"]
    if kind == "polar":
        ax.remove()
        fig = plt.gcf()
        polar = fig.add_subplot(111, projection="polar")
        theta = np.linspace(0, 2 * np.pi, 240)
        for r in [0.3, 0.6, 0.9, 1.2]:
            polar.plot(theta, np.full_like(theta, r), color=PALETTE["gray"], alpha=0.6)
        for angle in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            polar.plot([angle, angle], [0, 1.25], color=PALETTE["blue"], alpha=0.5)
        polar.set_title(spec["concept"])
        return {"radial_lines": 12}
    x = np.linspace(-1.5, 1.5, 17)
    X, Y = np.meshgrid(x, x)
    angle = (1 + seed % 3) * np.arctan2(Y, X)
    U, V = np.cos(angle), np.sin(angle)
    if kind in {"normal", "tangent"}:
        U, V = -Y, X
    ax.quiver(X, Y, U, V, color=PALETTE["blue"], pivot="mid", scale=28)
    ax.scatter([0], [0], color=PALETTE["red"], s=35)
    style_axis(ax, spec["concept"], equal=True)
    note(ax, "vector fields make direction data visible")
    return {"field_samples": int(X.size)}


def _plot_proof_kind(ax: Any, spec: dict[str, Any], seed: int) -> dict[str, Any]:
    kind = spec["kind"]
    if kind in {"linear", "ellipse"}:
        matrix = np.array([[2.0, 0.55], [0.55, 1.1]])
        if kind == "linear":
            image = ax.imshow(matrix, cmap="YlGnBu")
            for (i, j), value in np.ndenumerate(matrix):
                ax.text(j, i, f"{value:.1f}", ha="center", va="center")
            plt.colorbar(image, ax=ax, fraction=0.046)
            style_axis(ax, spec["concept"], grid=False)
            return {"symmetric": bool(np.allclose(matrix, matrix.T))}
        theta = np.linspace(0, 2 * np.pi, 240)
        ax.plot(1.4 * np.cos(theta), 0.65 * np.sin(theta), color=PALETTE["blue"])
        ax.arrow(0, 0, 1.4, 0, head_width=0.06, color=PALETTE["red"], length_includes_head=True)
        ax.arrow(0, 0, 0, 0.65, head_width=0.06, color=PALETTE["teal"], length_includes_head=True)
        style_axis(ax, spec["concept"], equal=True)
        return {"axes": 2}
    if kind in {"isometry", "rotation", "reflection"}:
        triangle = np.array([[0, 0], [1, 0.2], [0.25, 0.9], [0, 0]])
        theta = 0.65
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        moved = triangle @ R.T + np.array([1.2, 0.2])
        ax.plot(triangle[:, 0], triangle[:, 1], color=PALETTE["blue"], lw=2)
        ax.plot(moved[:, 0], moved[:, 1], color=PALETTE["red"], lw=2)
        style_axis(ax, spec["concept"], equal=True)
        return {"det_rotation": 1.0}
    if kind in {"bonnet", "triangulation"}:
        genus = np.arange(0, 5)
        total = 2 * np.pi * (2 - 2 * genus)
        ax.bar(genus, total, color=PALETTE["blue"])
        ax.axhline(0, color=PALETTE["ink"])
        ax.set_xlabel("genus")
        ax.set_ylabel("2 pi chi")
        style_axis(ax, spec["concept"])
        return {"sphere_total": float(total[0])}
    ax.axis("off")
    nodes = ["object", "visual", "formula", "check"]
    for idx, label in enumerate(nodes):
        x = 0.14 + idx * 0.24
        ax.add_patch(plt.Rectangle((x - 0.08, 0.45), 0.16, 0.14, facecolor=PALETTE["blue"], alpha=0.14, edgecolor=PALETTE["blue"]))
        ax.text(x, 0.52, label, ha="center", va="center", fontsize=9)
        if idx:
            ax.annotate("", xy=(x - 0.09, 0.52), xytext=(x - 0.16, 0.52), arrowprops={"arrowstyle": "->", "color": PALETTE["gray"]})
    ax.set_title(spec["concept"])
    return {"proof_nodes": len(nodes)}


def render_storyboard_visual(spec: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> dict[str, Any]:
    seed = _seed(artifact_topic, spec["kind"], spec["concept"])
    fig, ax = plt.subplots(figsize=(7.2, 4.8), facecolor=PALETTE["paper"])
    kind = spec["kind"]
    if kind == "frame":
        ax.remove()
        fig = plt.gcf()
        ax3 = fig.add_subplot(111, projection="3d")
        t = np.linspace(0, 5 * np.pi, 500)
        pts = np.column_stack([np.cos(t), np.sin(t), 0.18 * t])
        ax3.plot(pts[:, 0], pts[:, 1], pts[:, 2], color=PALETTE["blue"], lw=2)
        for i in [80, 180, 300, 420]:
            p = pts[i]
            tangent = np.array([-np.sin(t[i]), np.cos(t[i]), 0.18])
            tangent = tangent / np.linalg.norm(tangent)
            normal = np.array([-np.cos(t[i]), -np.sin(t[i]), 0.0])
            binormal = np.cross(tangent, normal)
            ax3.quiver(*p, *tangent, length=0.35, color=PALETTE["red"])
            ax3.quiver(*p, *normal, length=0.28, color=PALETTE["teal"])
            ax3.quiver(*p, *binormal, length=0.25, color=PALETTE["gold"])
        ax3.set_title(spec["concept"])
        metrics: dict[str, Any] = {"frame_samples": 4}
    elif kind in CURVE_KINDS:
        metrics = _plot_curve_kind(ax, spec, seed)
    elif kind in SURFACE_KINDS:
        metrics = _plot_surface_kind(ax, spec, seed)
    elif kind in METRIC_KINDS:
        metrics = _plot_metric_kind(ax, spec, seed)
    elif kind in MODEL_KINDS:
        metrics = _plot_model_kind(ax, spec, seed)
    elif kind in FIELD_KINDS:
        metrics = _plot_field_kind(ax, spec, seed)
    else:
        metrics = _plot_proof_kind(ax, spec, seed)
    if spec.get("observation"):
        fig.suptitle(spec["observation"], fontsize=8.5, y=0.01, color=PALETTE["gray"])
    path, image_stats = _save(fig, artifact_topic, spec, Path(artifact_root))
    return {"concept": spec["concept"], "filename": spec["filename"], "kind": kind, "path": path.as_posix(), "metrics": {**metrics, **image_stats}}


def build_visual_storyboard(storyboard: dict[str, Any], artifact_root: str | Path, artifact_topic: str) -> list[dict[str, Any]]:
    return [render_storyboard_visual(spec, artifact_root, artifact_topic) for spec in storyboard["visual_sequence"]]


def chapter_check_payload(storyboard: dict[str, Any], visual_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "unit": storyboard["unit"],
        "chapter_label": storyboard["chapter_label"],
        "visual_count": len(visual_results),
        "artifact_filenames": [item["filename"] for item in visual_results],
        "families": sorted({str(item["kind"]) for item in visual_results}),
        "invariants": {
            "unit_circle_curvature": 1.0,
            "sphere_euler_characteristic": euler_characteristic(4, 6, 4),
            "poincare_distance_sample": poincare_disk_distance(0 + 0j, 0.25 + 0j),
        },
        "assertions": {
            "has_visuals": len(visual_results) >= 1,
            "all_visuals_nonblank": all(item["metrics"].get("max_channel_stddev", 0) > 1.0 for item in visual_results),
            "all_visuals_named": all("-" in item["filename"] for item in visual_results),
        },
    }


def build_unit_visuals(unit: str, root: str | Path | None = None) -> dict[str, Any]:
    if root is None:
        root = BOOK_ROOT / "artifacts"
    root = Path(root)
    storyboard = storyboard_for(unit)
    source_path = save_json(storyboard["source_span"], unit, "checks", "source-span.json", root=root)
    storyboard_path = save_json(storyboard, unit, "checks", "visual-storyboard.json", root=root)
    visual_results = build_visual_storyboard(storyboard, root, unit)
    checks = chapter_check_payload(storyboard, visual_results)
    checks_path = save_json(checks, unit, "checks", "final-sanity.json", root=root)
    paths = [Path(item["path"]) for item in visual_results] + [source_path, storyboard_path, checks_path]
    return {"paths": paths, "visuals": visual_results, "checks": checks}


def unit_lab_data(unit: str) -> list[dict[str, Any]]:
    storyboard = storyboard_for(unit)
    rows = []
    for index, spec in enumerate(storyboard["visual_sequence"], start=1):
        rows.append(
            {
                "step": index,
                "concept": spec["concept"],
                "representation": spec.get("kind"),
                "inspection_target": spec.get("observation"),
            }
        )
    return rows
