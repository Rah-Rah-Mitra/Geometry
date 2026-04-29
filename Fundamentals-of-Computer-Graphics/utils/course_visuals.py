"""Chapter-specific visual builders for the FCG course notebooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy import signal

from .artifacts import save_image, save_json, save_matplotlib
from .color_perception import contrast_sensitivity, reinhard_tone_map, srgb_decode, srgb_encode, xy_chromaticity, rgb_to_xyz
from .curves_animation import bezier_curve, catmull_rom, quaternion_slerp
from .graphics_math import barycentric_2d, normalize, signed_area2, stable_quadratic_roots, triangle_area
from .meshes import cube_mesh, mesh_summary, tiled_index
from .plotting import PALETTE, add_note, arrow2, close, style_axis
from .raster import alpha_over, checkerboard, gamma_decode, gamma_encode, gradient, quantize
from .rendering import Ray, blinn_phong, reflect, shaded_sphere_image, simple_path_trace_samples, sphere_intersect
from .sampling import disk_samples, estimate_integral, hemisphere_samples, radial_cdf_error
from .transforms import homogeneous_divide, look_at, perspective, rotation2, scale2, shear2, translate


def concept_map(title: str, concepts: list[str], topic: str) -> Path:
    graph = nx.Graph()
    graph.add_node(title)
    for index, concept in enumerate(concepts):
        graph.add_edge(title, concept)
        if index:
            graph.add_edge(concepts[index - 1], concept)
    pos = nx.spring_layout(graph, seed=11, k=1.15)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.set_facecolor(PALETTE["paper"])
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="#b7c0cd", width=1.5)
    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_color=[PALETTE["gold"] if node == title else PALETTE["blue"] for node in graph.nodes],
        node_size=[1800 if node == title else 980 for node in graph.nodes],
        alpha=0.92,
    )
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_color="white")
    ax.set_title(f"{title}: concept dependencies", fontsize=12)
    ax.axis("off")
    path = save_matplotlib(fig, topic, "concept-dependency-map.png")
    close(fig)
    return path


def create_chapter_visuals(chapter: int, title: str, concepts: list[str], topic: str) -> dict[str, Any]:
    paths = [concept_map(title, concepts, topic)]
    checks: dict[str, Any] = {"chapter": chapter, "title": title, "concept_count": len(concepts)}
    domain_path, domain_checks = _domain_visual(chapter, title, topic)
    paths.append(domain_path)
    checks.update(domain_checks)
    check_path = save_json(checks, topic, "numeric-checks.json")
    return {"paths": paths, "checks": checks, "check_path": check_path}


def _domain_visual(chapter: int, title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    if chapter == 1:
        return _pipeline_debug_visual(title, topic)
    if chapter == 2:
        return _math_barycentric_visual(title, topic)
    if chapter == 3:
        return _raster_visual(title, topic)
    if chapter in {4, 5, 14}:
        return _rendering_visual(chapter, title, topic)
    if chapter == 6:
        return _linear_algebra_visual(title, topic)
    if chapter in {7, 8}:
        return _transform_view_visual(chapter, title, topic)
    if chapter in {9, 17}:
        return _rasterizer_visual(chapter, title, topic)
    if chapter == 10:
        return _signal_visual(title, topic)
    if chapter == 11:
        return _texture_visual(title, topic)
    if chapter == 12:
        return _mesh_visual(title, topic)
    if chapter == 13:
        return _sampling_visual(title, topic)
    if chapter == 15:
        return _curve_visual(title, topic)
    if chapter == 16:
        return _animation_visual(title, topic)
    if chapter == 18:
        return _color_visual(title, topic)
    if chapter == 19:
        return _perception_visual(title, topic)
    if chapter == 20:
        return _tone_visual(title, topic)
    if chapter == 21:
        return _implicit_visual(title, topic)
    if chapter == 22:
        return _games_visual(title, topic)
    return _visualization_visual(title, topic)


def _pipeline_debug_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    stages = ["model", "transform", "clip", "rasterize", "shade", "display"]
    for i, stage in enumerate(stages):
        axes[0].add_patch(plt.Rectangle((i, 0.35), 0.8, 0.3, color=PALETTE["blue"], alpha=0.85))
        axes[0].text(i + 0.4, 0.5, stage, ha="center", va="center", color="white", fontsize=8)
        if i < len(stages) - 1:
            axes[0].arrow(i + 0.82, 0.5, 0.12, 0, head_width=0.04, color=PALETTE["ink"])
    axes[0].set_xlim(-0.2, len(stages))
    axes[0].set_ylim(0, 1)
    axes[0].axis("off")
    axes[0].set_title("graphics pipeline as data flow")
    y, x = np.mgrid[-1:1:120j, -1:1:160j]
    debug = np.dstack([(x + 1) / 2, (y + 1) / 2, np.clip(1 - x * x - y * y, 0, 1)])
    axes[1].imshow(debug)
    axes[1].set_title("debug image: normal/work channels")
    axes[1].axis("off")
    path = save_matplotlib(fig, topic, "pipeline-debug-views.png")
    close(fig)
    return path, {"pipeline_stage_count": len(stages), "nan_comparison_false": bool(not (np.nan > 0))}


def _math_barycentric_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    tri = np.array([[0.08, 0.1], [0.92, 0.2], [0.35, 0.88]])
    p = np.array([0.45, 0.42])
    bary = barycentric_2d(p, *tri)
    roots = stable_quadratic_roots(1.0, -2.0, -3.0)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].triplot(tri[:, 0], tri[:, 1], [[0, 1, 2]], color=PALETTE["ink"])
    axes[0].scatter([p[0]], [p[1]], color=PALETTE["red"], zorder=3)
    for label, point, weight in zip(["alpha", "beta", "gamma"], tri, bary):
        axes[0].text(point[0], point[1], f"{label}={weight:.2f}", fontsize=9)
    style_axis(axes[0], "barycentric reconstruction", equal=True)
    x = np.linspace(-4, 4, 300)
    axes[1].plot(x, x * x - 2 * x - 3, color=PALETTE["blue"])
    axes[1].axhline(0, color=PALETTE["ink"], linewidth=1)
    axes[1].scatter(roots, [0, 0], color=PALETTE["red"])
    style_axis(axes[1], "quadratic roots as intersections", xlabel="x", ylabel="f(x)")
    path = save_matplotlib(fig, topic, "barycentric-quadratic-checks.png")
    close(fig)
    return path, {"barycentric_sum": float(bary.sum()), "quadratic_roots": list(roots or [])}


def _raster_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    ramp = gradient(256, 80)
    encoded = gamma_encode(ramp)
    quant = quantize(ramp, 8)
    fg = np.zeros_like(ramp) + np.array([0.2, 0.45, 0.85])
    bg = checkerboard(256, 80, 12)
    alpha = np.linspace(0, 1, 256)[None, :]
    comp = alpha_over(fg, bg, alpha)
    image = np.concatenate([ramp, encoded, quant, comp], axis=0)
    path = save_image(image, topic, "gamma-quantization-alpha.png")
    return path, {"gamma_roundtrip_error": float(np.max(np.abs(gamma_decode(encoded) - ramp))), "alpha_identity": float(np.max(np.abs(alpha_over(fg, bg, 0.0) - bg)))}


def _rendering_visual(chapter: int, title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.5))
    lights = [
        np.array([-0.6, 0.3 + 0.03 * chapter, 1.0]),
        np.array([0.25, 0.8, 1.0 + 0.02 * chapter]),
        np.array([0.8, -0.2 + 0.01 * chapter, 1.0]),
    ]
    color = np.array([0.28 + 0.02 * (chapter % 5), 0.62, 0.75 - 0.015 * (chapter % 4)])
    for ax, light in zip(axes, lights):
        ax.imshow(shaded_sphere_image(180, light=light, color=color, specular=chapter != 4))
        ax.axis("off")
        ax.set_title(f"light {normalize(light)[:2].round(2)}")
    path = save_matplotlib(fig, topic, "ray-light-transport-gallery.png")
    close(fig)
    ray = Ray(np.array([0.0, 0.0, 3.0]), np.array([0.0, 0.0, -1.0]))
    roots = sphere_intersect(ray, np.zeros(3), 1.0)
    pbr = simple_path_trace_samples(512)
    return path, {"sphere_hit_near": float(roots[0]), "reflection_norm": float(np.linalg.norm(reflect(np.array([0, -1, -1]), np.array([0, 0, 1])))), "path_trace_estimate": pbr["hemisphere_cosine_integral_estimate"]}


def _linear_algebra_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    angles = np.linspace(0, 2 * np.pi, 220)
    circle = np.column_stack([np.cos(angles), np.sin(angles)])
    a = np.array([[1.4, 0.75], [0.15, 0.7]])
    ellipse = circle @ a.T
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].plot(circle[:, 0], circle[:, 1], color=PALETTE["gray"])
    axes[0].plot(ellipse[:, 0], ellipse[:, 1], color=PALETTE["blue"])
    style_axis(axes[0], "matrix sends unit circle to ellipse", equal=True)
    arrow2(axes[1], np.zeros(2), a[:, 0], color=PALETTE["teal"], label="A e1")
    arrow2(axes[1], np.zeros(2), a[:, 1], color=PALETTE["gold"], label="A e2")
    style_axis(axes[1], "columns are transformed basis vectors", equal=True)
    path = save_matplotlib(fig, topic, "determinant-svd-geometry.png")
    close(fig)
    return path, {"determinant": float(np.linalg.det(a)), "det_product_check": float(np.linalg.det(a @ a) - np.linalg.det(a) ** 2)}


def _transform_view_visual(chapter: int, title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    square = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]], dtype=float)
    transform = rotation2(np.radians(32 + chapter)) @ shear2(0.35, 0.0) @ scale2(1.0, 0.55)
    moved = square @ transform.T
    view, basis = look_at(np.array([3, 2, 4]), np.zeros(3), np.array([0, 1, 0]))
    proj = perspective(45, 1.2, 1.0, 20.0)
    cube, _ = cube_mesh()
    clip = (proj @ view @ np.column_stack([cube, np.ones(len(cube))]).T).T
    ndc = homogeneous_divide(clip)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    axes[0].plot(square[:, 0], square[:, 1], "--", color=PALETTE["gray"])
    axes[0].plot(moved[:, 0], moved[:, 1], color=PALETTE["blue"])
    style_axis(axes[0], "composition changes shape and frame", equal=True)
    axes[1].scatter(ndc[:, 0], ndc[:, 1], c=ndc[:, 2], cmap="viridis")
    style_axis(axes[1], "projected cube in normalized device coordinates", equal=True)
    path = save_matplotlib(fig, topic, "transform-viewing-projection.png")
    close(fig)
    return path, {"camera_basis_dot_uv": float(np.dot(basis["u"], basis["v"])), "transformed_area": abs(signed_area2(moved[:-1]))}


def _rasterizer_visual(chapter: int, title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    offset = 0 if chapter == 9 else 10
    tri = np.array([[14 + offset, 12], [108, 30 + offset], [42, 98]], dtype=float)
    h = w = 128
    y, x = np.mgrid[0:h, 0:w]
    pts = np.dstack([x + 0.5, y + 0.5]).reshape(-1, 2)
    bary = np.array([barycentric_2d(p, *tri) for p in pts])
    inside = np.all(bary >= -1e-9, axis=1).reshape(h, w)
    rgb = np.zeros((h, w, 3)) + 0.96
    rgb[inside] = np.clip(bary.reshape(h, w, 3)[inside], 0, 1)
    path = save_image(rgb, topic, "barycentric-rasterization.png")
    return path, {"covered_pixels": int(inside.sum()), "barycentric_center_sum": float(bary[inside.reshape(-1)][0].sum())}


def _signal_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    t = np.linspace(0, 1, 256, endpoint=False)
    x = np.sin(2 * np.pi * 13 * t)
    kernel = signal.windows.gaussian(31, std=5)
    kernel = kernel / kernel.sum()
    filtered = np.convolve(x, kernel, mode="same")
    spectrum = np.abs(np.fft.rfft(x))
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    axes[0].plot(t, x, color=PALETTE["blue"])
    axes[0].plot(t, filtered, color=PALETTE["red"])
    style_axis(axes[0], "signal and filtered signal")
    axes[1].stem(kernel, linefmt=PALETTE["teal"], markerfmt="o", basefmt=" ")
    style_axis(axes[1], "normalized Gaussian kernel")
    axes[2].plot(spectrum, color=PALETTE["violet"])
    style_axis(axes[2], "FFT magnitude")
    path = save_matplotlib(fig, topic, "sampling-convolution-spectrum.png")
    close(fig)
    return path, {"kernel_sum": float(kernel.sum()), "fft_peak": int(np.argmax(spectrum[1:]) + 1)}


def _texture_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    tex = checkerboard(240, 240, 12)
    y, x = np.mgrid[0:180, 0:240]
    u_affine = x / 239
    v_affine = y / 179
    w = 0.45 + 0.55 * (y / 179)
    u_persp = np.clip(u_affine / w, 0, 1)
    v_persp = np.clip(v_affine / w, 0, 1)
    affine = tex[(v_affine * 239).astype(int), (u_affine * 239).astype(int)]
    persp = tex[(v_persp * 239).astype(int), (u_persp * 239).astype(int)]
    image = np.concatenate([affine, persp], axis=1)
    path = save_image(image, topic, "affine-vs-perspective-texture.png")
    return path, {"uv_min": float(min(u_persp.min(), v_persp.min())), "uv_max": float(max(u_persp.max(), v_persp.max()))}


def _mesh_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    vertices, faces = cube_mesh()
    summary = mesh_summary(vertices, faces)
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(121, projection="3d")
    for face in faces:
        loop = np.vstack([vertices[face], vertices[face[0]]])
        ax.plot(loop[:, 0], loop[:, 1], loop[:, 2], color=PALETTE["blue"])
    ax.set_title("indexed cube mesh adjacency")
    ax2 = fig.add_subplot(122)
    values = [summary["vertices"], summary["faces"], summary["edges"], summary["boundary_edges"]]
    ax2.bar(["V", "F", "E", "boundary"], values, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["red"]])
    style_axis(ax2, "topology counts")
    path = save_matplotlib(fig, topic, "mesh-topology-summary.png")
    close(fig)
    return path, summary


def _sampling_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    samples = disk_samples(800, seed=13)
    hemi = hemisphere_samples(800, seed=13)
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].scatter(samples[:, 0], samples[:, 1], s=5, alpha=0.45, color=PALETTE["blue"])
    style_axis(axes[0], "area-uniform disk samples", equal=True)
    axes[1].hist(hemi[:, 2], bins=24, color=PALETTE["teal"], alpha=0.85)
    style_axis(axes[1], "cosine hemisphere z distribution")
    path = save_matplotlib(fig, topic, "disk-hemisphere-sampling.png")
    close(fig)
    integral = estimate_integral(lambda x: x * x, n=3000, seed=13)
    return path, {"disk_radial_cdf_error": radial_cdf_error(samples), "x_squared_estimate": integral["estimate"]}


def _curve_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    controls = np.array([[0, 0], [0.2, 0.95], [0.75, -0.25], [1.0, 0.72]])
    curve = bezier_curve(controls)
    speed = np.linalg.norm(np.diff(curve, axis=0), axis=1)
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].plot(controls[:, 0], controls[:, 1], "--o", color=PALETTE["gray"])
    axes[0].plot(curve[:, 0], curve[:, 1], color=PALETTE["blue"])
    style_axis(axes[0], "Bezier curve and control polygon", equal=True)
    axes[1].plot(speed, color=PALETTE["red"])
    style_axis(axes[1], "speed is not uniform in parameter")
    path = save_matplotlib(fig, topic, "bezier-parameter-speed.png")
    close(fig)
    return path, {"endpoint_error": float(np.linalg.norm(curve[0] - controls[0]) + np.linalg.norm(curve[-1] - controls[-1])), "arc_length_estimate": float(speed.sum())}


def _animation_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    keys = np.array([[-1.2, 0.0], [-0.4, 0.9], [0.35, -0.1], [1.0, 0.7], [1.4, 0.0]])
    path_pts = catmull_rom(keys)
    ts = np.linspace(0, 1, 8)
    q0 = np.array([1, 0, 0, 0], dtype=float)
    q1 = normalize(np.array([0.2, 0.0, 0.0, 0.98]))
    qs = np.array([quaternion_slerp(q0, q1, t) for t in ts])
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].plot(path_pts[:, 0], path_pts[:, 1], color=PALETTE["blue"])
    axes[0].scatter(keys[:, 0], keys[:, 1], color=PALETTE["red"])
    style_axis(axes[0], "keyframes and interpolated motion path", equal=True)
    axes[1].plot(ts, qs[:, 0], label="w", color=PALETTE["blue"])
    axes[1].plot(ts, qs[:, 3], label="z", color=PALETTE["teal"])
    axes[1].legend()
    style_axis(axes[1], "slerp stays on unit quaternion sphere")
    path = save_matplotlib(fig, topic, "keyframe-slerp-motion.png")
    close(fig)
    return path, {"max_quaternion_norm_error": float(np.max(np.abs(np.linalg.norm(qs, axis=1) - 1.0))), "key_count": int(len(keys))}


def _color_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    rgb = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1], [1, 0.7, 0.2]], dtype=float)
    xyz = rgb_to_xyz(rgb)
    xy = xy_chromaticity(xyz)
    ramp = np.linspace(0, 1, 256)
    encoded = srgb_encode(ramp)
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].scatter(xy[:, 0], xy[:, 1], c=rgb, s=160, edgecolor="black")
    style_axis(axes[0], "sRGB primaries in xy chromaticity")
    axes[1].plot(ramp, encoded, color=PALETTE["blue"], label="encode")
    axes[1].plot(ramp, srgb_decode(encoded), color=PALETTE["red"], label="decode(encode)")
    axes[1].legend()
    style_axis(axes[1], "sRGB transfer curve")
    path = save_matplotlib(fig, topic, "chromaticity-transfer-curve.png")
    close(fig)
    return path, {"srgb_roundtrip_error": float(np.max(np.abs(srgb_decode(encoded) - ramp))), "white_xy_sum": float(xy[3].sum())}


def _perception_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    freq = np.linspace(0.5, 40, 240)
    csf = contrast_sensitivity(freq)
    base = np.linspace(0.25, 0.75, 220)
    illusion = np.tile(base, (90, 1))
    illusion[:, 70:150] = illusion[:, 70:150] * 0.65 + 0.18
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].plot(freq, csf, color=PALETTE["blue"])
    style_axis(axes[0], "contrast sensitivity vs spatial frequency")
    axes[1].imshow(illusion, cmap="gray", vmin=0, vmax=1)
    axes[1].axis("off")
    axes[1].set_title("context changes perceived lightness")
    path = save_matplotlib(fig, topic, "contrast-lightness-perception.png")
    close(fig)
    return path, {"peak_sensitivity_frequency": float(freq[np.argmax(csf)]), "stimulus_min": float(illusion.min()), "stimulus_max": float(illusion.max())}


def _tone_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    x = np.linspace(0, 6, 256)
    hdr = np.dstack([np.tile(np.exp(x)[None, :], (80, 1)), np.tile(np.exp(x / 1.5)[None, :], (80, 1)), np.tile(np.exp(x / 2)[None, :], (80, 1))])
    mapped = reinhard_tone_map(hdr / hdr.max() * 8)
    curves = x / (1 + x)
    image = np.concatenate([mapped, np.repeat(curves[None, :, None], 80, axis=0).repeat(3, axis=2)], axis=0)
    path = save_image(image, topic, "hdr-tone-mapping-curves.png")
    return path, {"tone_min": float(mapped.min()), "tone_max": float(mapped.max()), "monotone_curve": bool(np.all(np.diff(curves) >= 0))}


def _implicit_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    x, y = np.mgrid[-1.6:1.6:180j, -1.2:1.2:140j]
    f1 = (x + 0.45) ** 2 + y**2 - 0.5
    f2 = (x - 0.45) ** 2 + y**2 - 0.5
    union = np.minimum(f1, f2)
    blend = np.exp(-4 * ((x + 0.45) ** 2 + y**2)) + np.exp(-4 * ((x - 0.45) ** 2 + y**2))
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].contourf(x, y, union, levels=25, cmap="coolwarm")
    axes[0].contour(x, y, union, levels=[0], colors="black")
    style_axis(axes[0], "CSG union as min field", equal=True)
    axes[1].contourf(x, y, blend, levels=25, cmap="viridis")
    axes[1].contour(x, y, blend, levels=[0.72], colors="white")
    style_axis(axes[1], "soft skeletal blend", equal=True)
    path = save_matplotlib(fig, topic, "implicit-field-blending.png")
    close(fig)
    return path, {"union_negative_fraction": float(np.mean(union < 0)), "blend_max": float(blend.max())}


def _games_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    lod_triangles = np.array([18000, 6000, 1800, 420])
    frame_ms = np.array([3.2, 2.1, 1.2, 0.6])
    memory = np.array([96, 42, 18, 7])
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4))
    axes[0].plot(lod_triangles, frame_ms, "o-", color=PALETTE["blue"])
    axes[0].invert_xaxis()
    style_axis(axes[0], "LOD triangle count vs frame cost", xlabel="triangles", ylabel="ms")
    axes[1].bar(["ultra", "high", "medium", "low"], memory, color=PALETTE["teal"])
    style_axis(axes[1], "texture budget by quality tier", ylabel="MB")
    path = save_matplotlib(fig, topic, "frame-budget-lod-dashboard.png")
    close(fig)
    return path, {"best_frame_ms": float(frame_ms.min()), "memory_ratio_ultra_low": float(memory[0] / memory[-1])}


def _visualization_visual(title: str, topic: str) -> tuple[Path, dict[str, Any]]:
    graph = nx.barbell_graph(5, 2)
    pos = nx.spring_layout(graph, seed=23)
    values = np.array([graph.degree(node) for node in graph.nodes])
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    nx.draw_networkx(graph, pos, ax=axes[0], node_color=values, cmap="viridis", with_labels=True, font_size=7)
    axes[0].axis("off")
    axes[0].set_title("network data as node-link encoding")
    bars = ["position", "length", "angle", "area", "color"]
    scores = [5, 4, 3, 2, 2]
    axes[1].bar(bars, scores, color=[PALETTE["blue"], PALETTE["teal"], PALETTE["gold"], PALETTE["red"], PALETTE["violet"]])
    axes[1].tick_params(axis="x", rotation=30)
    style_axis(axes[1], "encoding precision sketch", ylabel="relative precision")
    path = save_matplotlib(fig, topic, "visual-encoding-task-map.png")
    close(fig)
    return path, {"node_count": graph.number_of_nodes(), "edge_count": graph.number_of_edges(), "degree_sum": int(values.sum())}
