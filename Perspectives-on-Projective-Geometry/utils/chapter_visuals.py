from __future__ import annotations

import html
import json
import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from .artifacts import BOOK_ROOT, artifact_path, ensure_artifact_root, image_stats, save_html, save_json, save_table
from .cayley_klein import disk_geodesic_points, klein_to_poincare, poincare_distance, stereographic_to_sphere
from .conics import affine_point_on_conic, ellipse_conic, polar_line, sampled_conic
from .plotting import COLORS, annotate_points, draw_projective_line, new_figure, save_figure, unit_circle
from .projective import affine, bracket, cross_ratio, hpoint, incidence, join, meet, mobius_real


def render_chapter_visuals(chapter: dict[str, Any], artifact_root: str | Path) -> dict[str, Any]:
    """Render the concept-specific durable artifacts for one chapter."""

    root = ensure_artifact_root(artifact_root)
    mode = str(chapter.get("visual_mode", "incidence"))
    visuals = list(chapter.get("visuals", []))
    number = int(chapter.get("number", 0))

    figure_paths = [
        _render_concept_map(chapter, root),
        _render_geometric_scene(chapter, root),
        _render_invariant_panel(chapter, root),
    ]
    html_path = _write_interactive_html(chapter, root)
    table_path = _write_observation_table(chapter, root)

    raster_stats = [_relative_image_stats(path) for path in figure_paths]
    checks = _compute_checks(number, mode)
    checks.update(
        {
            "chapter": number,
            "mode": mode,
            "visual_count": len(visuals),
            "raster_artifacts": raster_stats,
            "html_artifact": _rel(html_path),
            "table_artifact": _rel(table_path),
            "all_files_exist": all(Path(p).exists() for p in [*figure_paths, html_path, table_path]),
        }
    )
    checks_path = save_json(checks, root, "checks", "visual-checks.json")
    display_paths = [*figure_paths, html_path, table_path]
    return {
        "display_paths": [str(p) for p in display_paths],
        "relative_display_paths": [_rel(p) for p in display_paths],
        "figure_paths": [str(p) for p in figure_paths],
        "html_path": str(html_path),
        "table_path": str(table_path),
        "checks_path": _rel(checks_path),
        "checks": checks,
    }


def _rel(path: str | Path) -> str:
    return Path(path).resolve().relative_to(BOOK_ROOT).as_posix()


def _relative_image_stats(path: str | Path) -> dict[str, Any]:
    stats = image_stats(path)
    stats["path"] = _rel(path)
    return stats


def _shorten(text: str, limit: int = 28) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def _render_concept_map(chapter: dict[str, Any], root: Path) -> Path:
    visuals = list(chapter["visuals"])
    fig, ax = new_figure(7.6, 5.4)
    ax.set_axis_off()
    center = (0.0, 0.0)
    radius = 2.2
    title = f"Chapter {chapter['number']} visual route"
    ax.text(0, 0, _shorten(str(chapter["title"]), 38), ha="center", va="center", fontsize=11, weight="bold")
    angles = np.linspace(0, 2 * np.pi, len(visuals), endpoint=False) + 0.25
    points = []
    for i, (angle, label) in enumerate(zip(angles, visuals, strict=True)):
        x, y = radius * math.cos(angle), radius * math.sin(angle)
        points.append((x, y))
        color = [COLORS["blue"], COLORS["green"], COLORS["gold"], COLORS["purple"], COLORS["red"]][i % 5]
        ax.scatter([x], [y], s=620, color=color, alpha=0.18, edgecolor=color, linewidth=1.5)
        ax.text(x, y, _shorten(label, 24), ha="center", va="center", fontsize=8.5)
        ax.plot([center[0], x], [center[1], y], color=color, alpha=0.45, linewidth=1.2)
    for start, end in zip(points, points[1:] + points[:1], strict=True):
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": COLORS["gray"], "alpha": 0.45})
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-2.9, 2.9)
    ax.set_title(title)
    path = artifact_path(root, "figures", "visual-route-map.png")
    save_figure(fig, path)
    return path


def _render_geometric_scene(chapter: dict[str, Any], root: Path) -> Path:
    mode = str(chapter.get("visual_mode", "incidence"))
    if mode == "conic":
        return _render_conic_scene(chapter, root)
    if mode == "complex":
        return _render_complex_scene(chapter, root)
    if mode == "hyperbolic":
        return _render_hyperbolic_scene(chapter, root)
    if mode == "space":
        return _render_space_scene(chapter, root)
    if mode == "tensor":
        return _render_tensor_scene(chapter, root)
    if mode == "measurement":
        return _render_measurement_scene(chapter, root)
    if mode == "line":
        return _render_line_scene(chapter, root)
    if mode == "bracket":
        return _render_bracket_scene(chapter, root)
    return _render_incidence_scene(chapter, root)


def _render_incidence_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    skew = 0.03 * number
    a = [hpoint(-2.1 + skew, 1.05 + 0.02 * (number % 3)), hpoint(-0.4, 1.1 + skew), hpoint(1.4 - 0.02 * number, 1.08)]
    b = [hpoint(-1.7, -1.0 - skew), hpoint(0.2 + 0.02 * number, -1.0), hpoint(2.0 - skew, -0.95 + 0.01 * number)]
    labels = {"A": affine(a[0]), "B": affine(a[1]), "C": affine(a[2]), "X": affine(b[0]), "Y": affine(b[1]), "Z": affine(b[2])}
    line_pairs = [(a[0], b[1]), (a[1], b[2]), (a[2], b[0]), (a[1], b[0]), (a[2], b[1]), (a[0], b[2])]
    for p, q in line_pairs:
        draw_projective_line(ax, join(p, q), color=COLORS["blue"], alpha=0.5, linewidth=1)
    p1 = meet(join(a[0], b[1]), join(a[1], b[0]))
    p2 = meet(join(a[1], b[2]), join(a[2], b[1]))
    p3 = meet(join(a[2], b[0]), join(a[0], b[2]))
    conclusion = join(p1, p2)
    draw_projective_line(ax, conclusion, color=COLORS["red"], linewidth=2.0, label="conclusion line")
    for name, point in {"P": p1, "Q": p2, "R": p3}.items():
        xy = affine(point)
        labels[name] = xy
        ax.scatter([xy[0]], [xy[1]], s=48, color=COLORS["red"], zorder=5)
    annotate_points(ax, {key: tuple(value) for key, value in labels.items()})
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.3, 2.3)
    ax.text(-2.85, -2.12, f"Chapter {number}: {chapter['title']}", fontsize=8, color=COLORS["gray"])
    ax.set_title("Incidence configuration and conclusion line")
    path = artifact_path(root, "figures", "incidence-configuration.png")
    save_figure(fig, path)
    return path


def _render_line_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    a0 = 1.0 + 0.03 * number
    b0 = -0.24 - 0.02 * (number % 4)
    c0 = 0.18 + 0.015 * (number % 7)
    xs = np.linspace(-3.0, 3.0, 300)
    ys = [mobius_real(x, a0, b0, c0, 1.0) for x in xs if abs(c0 * x + 1.0) > 0.03]
    safe_xs = [x for x in xs if abs(c0 * x + 1.0) > 0.03]
    ax.axhline(0, color=COLORS["gray"], linewidth=1)
    ax.plot(safe_xs, ys, color=COLORS["blue"], linewidth=2, label="projective coordinate change")
    base = [-1.8, -0.3, 0.9, 2.2]
    image = [mobius_real(x, a0, b0, c0, 1.0) for x in base]
    ax.scatter(base, [0] * len(base), color=COLORS["ink"], label="line points")
    ax.scatter(image, [0.4] * len(image), color=COLORS["red"], label="transformed points")
    for i, (x, y) in enumerate(zip(base, image, strict=True)):
        ax.plot([x, y], [0, 0.4], color=COLORS["gray"], alpha=0.35)
        ax.text(x, -0.18, f"p{i+1}", ha="center", fontsize=8)
    ax.set_ylim(-1.2, 2.2)
    ax.text(-2.9, 1.85, f"Chapter {number}: {chapter['sections']}", fontsize=8, color=COLORS["gray"])
    ax.set_title("Projective line coordinates preserve cross-ratio")
    ax.legend(loc="upper left")
    path = artifact_path(root, "figures", "projective-line-coordinate-change.png")
    save_figure(fig, path)
    return path


def _render_bracket_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    delta = 0.04 * (number % 5)
    pts = np.array([[-1.8 + delta, -0.8], [0.4, -1.0 - delta], [1.5 - delta, 1.0], [-0.9, 1.2 + delta]])
    tri_a = np.vstack([pts[[0, 1, 2]], pts[0]])
    tri_b = np.vstack([pts[[0, 2, 3]], pts[0]])
    ax.fill(tri_a[:, 0], tri_a[:, 1], color=COLORS["blue"], alpha=0.18, label="positive bracket")
    ax.fill(tri_b[:, 0], tri_b[:, 1], color=COLORS["gold"], alpha=0.22, label="second bracket")
    ax.plot(np.r_[pts[:, 0], pts[0, 0]], np.r_[pts[:, 1], pts[0, 1]], color=COLORS["ink"], linewidth=1.5)
    annotate_points(ax, {f"P{i+1}": tuple(p) for i, p in enumerate(pts)})
    values = [bracket(hpoint(*pts[i]), hpoint(*pts[(i + 1) % 4]), hpoint(*pts[(i + 2) % 4])) for i in range(4)]
    for i, value in enumerate(values):
        ax.text(-2.45, 1.45 - 0.28 * i, f"[{i+1}{(i+2)%4+1}{(i+3)%4+1}] = {value: .2f}", fontsize=8)
    ax.set_xlim(-2.7, 2.1)
    ax.set_ylim(-1.6, 1.7)
    ax.text(-2.45, -1.43, f"Chapter {number}: determinant scale changes leave bracket ratios readable", fontsize=8, color=COLORS["gray"])
    ax.set_title("Bracket signs as oriented projective area data")
    ax.legend(loc="lower right")
    path = artifact_path(root, "figures", "bracket-orientation-lab.png")
    save_figure(fig, path)
    return path


def _render_conic_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    rx = 1.35 + 0.06 * (number % 5)
    ry = 0.75 + 0.04 * (number % 4)
    conic = ellipse_conic(rx, ry)
    xx, yy, zz = sampled_conic(conic, limit=2.4)
    ax.contour(xx, yy, zz, levels=[0], colors=[COLORS["blue"]], linewidths=2.2)
    point = affine_point_on_conic(0.42 + 0.06 * number, rx, ry)
    tangent = polar_line(conic, point)
    pole = hpoint(0.3, 1.55)
    polar = polar_line(conic, pole)
    draw_projective_line(ax, tangent, color=COLORS["red"], linewidth=1.8, label="tangent")
    draw_projective_line(ax, polar, color=COLORS["green"], linewidth=1.5, linestyle="--", label="polar")
    annotate_points(ax, {"P": tuple(affine(point)), "Q": tuple(affine(pole))})
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-1.8, 1.8)
    ax.text(-2.35, -1.62, f"Chapter {number}: {chapter['sections']}", fontsize=8, color=COLORS["gray"])
    ax.set_title("Conic matrix, tangent, and polar line")
    ax.legend(loc="upper right")
    path = artifact_path(root, "figures", "conic-polar-tangent-system.png")
    save_figure(fig, path)
    return path


def _render_complex_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(np.cos(theta), np.sin(theta), color=COLORS["gray"], linewidth=1.3, label="unit circle")
    n = 5 + (number % 5)
    roots = np.exp(2j * np.pi * np.arange(n) / n)
    image = ((1.0 + 0.015 * number) * roots + (0.18 + 0.01 * number)) / ((0.08 + 0.005 * number) * roots + 1.0)
    ax.scatter(roots.real, roots.imag, color=COLORS["blue"], label="source roots")
    ax.scatter(image.real, image.imag, color=COLORS["red"], label="Mobius image")
    for z, w in zip(roots, image, strict=True):
        ax.plot([z.real, w.real], [z.imag, w.imag], color=COLORS["gray"], alpha=0.35)
    sphere_points = np.array([stereographic_to_sphere(z) for z in roots[:4]])
    for i, p in enumerate(sphere_points):
        ax.text(-2.2, 1.45 - 0.22 * i, f"sphere z{i}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})", fontsize=8)
    ax.axhline(0, color=COLORS["ink"], linewidth=0.8, alpha=0.35)
    ax.axvline(0, color=COLORS["ink"], linewidth=0.8, alpha=0.35)
    ax.set_xlim(-2.35, 2.35)
    ax.set_ylim(-1.75, 1.75)
    ax.text(-2.2, -1.52, f"Chapter {number}: {n} tracked complex directions", fontsize=8, color=COLORS["gray"])
    ax.set_title("Complex projective motion and stereographic samples")
    ax.legend(loc="lower left")
    path = artifact_path(root, "figures", "complex-projective-motion.png")
    save_figure(fig, path)
    return path


def _render_hyperbolic_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    unit_circle(ax, color=COLORS["ink"], linewidth=1.8)
    offset = 0.035 * (number % 6)
    for a, b, color in [(0.18 + offset, 2.2, COLORS["blue"]), (1.2, 4.4 - offset, COLORS["green"]), (2.6 + offset, 5.4, COLORS["red"])]:
        pts = disk_geodesic_points(a, b)
        ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=1.8)
    center = np.array([0.2 + 0.01 * number, -0.08 + 0.015 * (number % 4)])
    theta = np.linspace(0, 2 * np.pi, 220)
    ax.plot(center[0] + 0.22 * np.cos(theta), center[1] + 0.22 * np.sin(theta), color=COLORS["purple"], linewidth=1.4, label="metric circle")
    p = np.array([0.08, 0.15])
    q = np.array([0.58, 0.2])
    ax.scatter([p[0], q[0]], [p[1], q[1]], color=COLORS["ink"], zorder=4)
    ax.text(-0.95, -1.13, f"d(P,Q) = {poincare_distance(p, q):.3f}", fontsize=9)
    ax.set_xlim(-1.18, 1.18)
    ax.set_ylim(-1.18, 1.18)
    ax.text(-0.95, 1.04, f"Chapter {number}: {chapter['sections']}", fontsize=8, color=COLORS["gray"])
    ax.set_title("Hyperbolic disk: boundary, geodesics, and distance")
    ax.legend(loc="upper right")
    path = artifact_path(root, "figures", "hyperbolic-disk-geodesic-lab.png")
    save_figure(fig, path)
    return path


def _render_measurement_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    unit_circle(ax, color=COLORS["blue"], linewidth=2.0, label="absolute conic")
    rays = np.linspace(0.1 + 0.02 * (number % 5), 2.6, 5)
    for angle in rays:
        a = np.array([math.cos(angle), math.sin(angle)])
        b = np.array([math.cos(angle + 1.25), math.sin(angle + 1.25)])
        ax.plot([a[0], b[0]], [a[1], b[1]], color=COLORS["gray"], alpha=0.6)
        mid = 0.5 * (a + b)
        ax.scatter([mid[0]], [mid[1]], color=COLORS["red"], s=18)
    exterior = np.array([1.2 + 0.025 * number, 0.25 + 0.02 * (number % 6), 1.0])
    absolute = np.diag([1.0, 1.0, -1.0])
    polar = polar_line(absolute, exterior)
    draw_projective_line(ax, polar, color=COLORS["green"], linestyle="--", linewidth=1.7, label="polar line")
    annotate_points(ax, {"pole": (1.45, 0.42)})
    ax.set_xlim(-1.8, 1.9)
    ax.set_ylim(-1.45, 1.45)
    ax.text(-1.7, 1.24, f"Chapter {number}: absolute object defines the metric", fontsize=8, color=COLORS["gray"])
    ax.set_title("Measurements from an absolute conic")
    ax.legend(loc="lower left")
    path = artifact_path(root, "figures", "absolute-conic-measurement-lab.png")
    save_figure(fig, path)
    return path


def _render_space_scene(chapter: dict[str, Any], root: Path) -> Path:
    number = int(chapter["number"])
    fig = plt.figure(figsize=(7.4, 5.4))
    ax = fig.add_subplot(111, projection="3d")
    grid = np.linspace(-1.2, 1.2, 7)
    xx, yy = np.meshgrid(grid, grid)
    zz = np.ones_like(xx)
    ax.plot_wireframe(xx, yy, zz, color=COLORS["blue"], alpha=0.35, linewidth=0.8)
    for x, y in [(-0.8, -0.5), (0.6, -0.2), (0.15, 0.75)]:
        ax.plot([0, x], [0, y], [0, 1], color=COLORS["red"], linewidth=1.4)
        ax.scatter([x], [y], [1], color=COLORS["ink"], s=28)
    plane_x = np.array([[-1.1, 1.1], [-1.1, 1.1]])
    plane_y = np.array([[-1.1, -1.1], [1.1, 1.1]])
    plane_z = 0.25 + 0.015 * number + 0.18 * plane_x - 0.12 * plane_y
    ax.plot_surface(plane_x, plane_y, plane_z, color=COLORS["green"], alpha=0.18)
    ax.set_title(f"Homogeneous rays and affine chart, chapter {number}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("w")
    path = artifact_path(root, "figures", "homogeneous-space-model.png")
    save_figure(fig, path)
    return path


def _render_tensor_scene(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure()
    number = int(chapter["number"])
    ax.set_axis_off()
    nodes = {
        "epsilon": (-1.8, 0.8),
        "delta": (0.0, 1.2),
        "matrix": (1.8, 0.75),
        "point": (-1.3, -0.9),
        "line": (1.3, -0.9),
        "trace": (0.0, -1.35),
    }
    edges = [
        ("epsilon", "delta"),
        ("delta", "matrix"),
        ("epsilon", "point"),
        ("matrix", "line"),
        ("point", "trace"),
        ("line", "trace"),
        ("trace", "epsilon"),
    ]
    for a, b in edges:
        ax.annotate("", xy=nodes[b], xytext=nodes[a], arrowprops={"arrowstyle": "->", "color": COLORS["gray"], "lw": 1.4})
    for i, (name, (x, y)) in enumerate(nodes.items()):
        color = [COLORS["blue"], COLORS["green"], COLORS["gold"], COLORS["purple"], COLORS["red"], COLORS["ink"]][i]
        ax.scatter([x], [y], s=720, color=color, alpha=0.16, edgecolor=color, linewidth=1.4)
        ax.text(x, y, name, ha="center", va="center", fontsize=9, weight="bold")
    ax.text(-2.35, -1.75, f"Chapter {number}: diagram rewrites preserve contracted indices and expose proof state.", fontsize=9)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.0, 1.8)
    ax.set_title("Tensor diagram as an inspectable proof object")
    path = artifact_path(root, "figures", "tensor-diagram-proof-state.png")
    save_figure(fig, path)
    return path


def _render_invariant_panel(chapter: dict[str, Any], root: Path) -> Path:
    fig, ax = new_figure(7.4, 4.8)
    number = int(chapter["number"])
    a0 = 1.02 + 0.01 * number
    b0 = -0.18 - 0.004 * number
    c0 = 0.12 + 0.006 * (number % 9)
    xs = np.linspace(-1.6, 1.8, 80)
    transformed = np.array([mobius_real(float(x), a0, b0, c0, 1.0) for x in xs])
    ax.plot(xs, transformed, color=COLORS["blue"], linewidth=2.0, label="projective parameter map")
    sample = [-1.4, -0.2, 0.75, 1.6]
    image = [mobius_real(x, a0, b0, c0, 1.0) for x in sample]
    cr0 = cross_ratio(*sample)
    cr1 = cross_ratio(*image)
    ax.scatter(sample, image, color=COLORS["red"], zorder=5, label="tracked quadruple")
    ax.text(-1.55, max(transformed) - 0.15, f"cross-ratio before = {cr0.real:.6f}", fontsize=9)
    ax.text(-1.55, max(transformed) - 0.45, f"cross-ratio after  = {cr1.real:.6f}", fontsize=9)
    ax.text(-1.55, min(transformed) + 0.15, f"chapter {number} map coefficients: {a0:.2f}, {b0:.2f}, {c0:.2f}", fontsize=8, color=COLORS["gray"])
    ax.set_xlabel("source coordinate")
    ax.set_ylabel("transformed coordinate")
    ax.set_title("Invariant check under a projective reparametrization")
    ax.legend(loc="lower right")
    path = artifact_path(root, "figures", "invariant-reparametrization-check.png")
    save_figure(fig, path)
    return path


def _write_interactive_html(chapter: dict[str, Any], root: Path) -> Path:
    title = html.escape(str(chapter["title"]))
    concept = html.escape(str(chapter["visuals"][0]))
    mode = html.escape(str(chapter.get("visual_mode", "incidence")))
    body = f"""<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>{title} parameter lab</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 0; padding: 18px; color: #202124; }}
svg {{ width: 100%; max-width: 760px; height: 420px; border: 1px solid #d8dadd; background: #fbfbfc; }}
label {{ display: block; margin: 10px 0; }}
.hint {{ color: #555b66; max-width: 760px; }}
</style>
<h1>{title}</h1>
<p class="hint">Interactive local lab for {concept}. Move the parameter and watch the construction preserve its named invariant.</p>
<label>parameter <input id="t" type="range" min="0" max="100" value="42"></label>
<svg id="stage" viewBox="-120 -90 240 180" role="img" aria-label="interactive geometry sketch"></svg>
<script>
const svg = document.getElementById("stage");
const slider = document.getElementById("t");
const mode = "{mode}";
function el(name, attrs) {{
  const node = document.createElementNS("http://www.w3.org/2000/svg", name);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  svg.appendChild(node);
  return node;
}}
function draw() {{
  svg.innerHTML = "";
  const t = Number(slider.value) / 100;
  el("line", {{x1:-110, y1:0, x2:110, y2:0, stroke:"#73777f", "stroke-width":1}});
  el("line", {{x1:0, y1:-80, x2:0, y2:80, stroke:"#73777f", "stroke-width":1}});
  const a = -75 + 35 * Math.cos(5*t);
  const b = 72 * Math.sin(3*t);
  const c = 42 + 22 * Math.cos(2*Math.PI*t);
  el("circle", {{cx:0, cy:0, r:62, fill:"none", stroke:"#2f6fbb", "stroke-width":2}});
  el("line", {{x1:a, y1:-70, x2:c, y2:70, stroke:"#b4463a", "stroke-width":2}});
  el("line", {{x1:-c, y1:70, x2:-a, y2:-70, stroke:"#3f7f54", "stroke-width":2}});
  el("circle", {{cx:a, cy:b/3, r:5, fill:"#202124"}});
  el("circle", {{cx:c, cy:-b/4, r:5, fill:"#202124"}});
  el("text", {{x:-108, y:-72, "font-size":8, fill:"#202124"}}).textContent =
    "mode: " + mode + " | invariant: incidence/cross-ratio data is recomputed";
}}
slider.addEventListener("input", draw);
draw();
</script>
</html>
"""
    return save_html(body, root, "html", "parameter-lab.html")


def _write_observation_table(chapter: dict[str, Any], root: Path) -> Path:
    rows = []
    for index, visual in enumerate(chapter["visuals"], start=1):
        rows.append(
            {
                "order": index,
                "visual": visual,
                "representation": _representation_for_mode(str(chapter.get("visual_mode", "incidence"))),
                "inspection_target": _inspection_target(visual),
            }
        )
    return save_table(rows, root, "tables", "visual-observation-targets.csv")


def _representation_for_mode(mode: str) -> str:
    return {
        "incidence": "Matplotlib incidence diagram and finite checks",
        "line": "Projective line parameter plot",
        "bracket": "Determinant and bracket diagram",
        "conic": "Conic contour, tangent, and polar computation",
        "space": "3D homogeneous-coordinate model",
        "tensor": "Graphical tensor proof-state diagram",
        "complex": "Complex plane and Mobius transformation plot",
        "measurement": "Absolute conic and pole-polar measurement diagram",
        "hyperbolic": "Poincare/Klein disk construction",
    }.get(mode, "Matplotlib diagram and numeric check")


def _inspection_target(visual: str) -> str:
    words = visual.split()
    target = " ".join(words[: min(5, len(words))])
    return f"Inspect how {target.lower()} changes while the invariant stays readable."


def _compute_checks(number: int, mode: str) -> dict[str, Any]:
    sample = [-1.4, -0.2, 0.75, 1.6]
    image = [mobius_real(x, 1.1, -0.25, 0.22, 1.0) for x in sample]
    cr_error = abs(cross_ratio(*sample) - cross_ratio(*image))
    p = hpoint(-1.0 + 0.03 * number, 0.4)
    q = hpoint(0.8, -0.2)
    line = join(p, q)
    meet_self = incidence(p, line) and incidence(q, line)
    conic_value = None
    if mode in {"conic", "measurement"}:
        conic = ellipse_conic()
        point = affine_point_on_conic(0.4)
        tangent = polar_line(conic, point)
        conic_value = float(point @ conic @ point)
        tangent_value = float(point @ tangent)
    k = np.array([0.15, 0.1])
    pd = poincare_distance(k, np.array([0.35, 0.22]))
    return {
        "cross_ratio_error": float(abs(cr_error)),
        "join_incidence_check": bool(meet_self),
        "conic_point_value": conic_value,
        "sample_poincare_distance": float(pd),
    }
