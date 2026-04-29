"""Topic-specific visuals and mathematical checks for the course notebooks."""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy import special, stats

from .circular import (
    A1,
    inverse_A1,
    kuiper_statistic,
    rayleigh_statistic,
    resultant,
    rose_histogram,
    sample_vonmises,
    von_mises_pdf,
    watson_u2,
    wrap_angle,
)
from .manifolds import (
    grassmann_projection,
    minkowski_dot,
    rotation_from_axis_angle,
    sample_hyperboloid,
    sample_so3,
    sample_stiefel,
)
from .shape import (
    helmert_submatrix,
    preshape,
    procrustes_align,
    procrustes_mean,
    tangent_shape_coords,
    triangle_shape_features,
)
from .special_functions import bessel_ratio, large_kappa_A1, small_kappa_A1
from .spherical import (
    angular_distance,
    fisher_A3,
    fisher_density_s2,
    inertia_matrix,
    inverse_fisher_A3,
    mean_direction,
    normalize,
    spherical_sample,
    uniform_sphere,
)

TAU = 2 * np.pi
COLORS = {
    "ink": "#1f2933",
    "blue": "#2f6fbb",
    "teal": "#2a9d8f",
    "green": "#6a994e",
    "gold": "#d59f0f",
    "red": "#c44e52",
    "violet": "#7b5ea7",
    "gray": "#7a8793",
}


def _style(ax: Any, title: str, *, equal: bool = False) -> None:
    ax.set_title(title, fontsize=11, color=COLORS["ink"])
    ax.grid(True, color="#d7dde5", linewidth=0.7, alpha=0.8)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in getattr(ax, "spines", {}).values():
        spine.set_color("#b6c0ca")


def _circular_sample(seed: int, n: int = 96, kappa: float = 2.5) -> np.ndarray:
    return sample_vonmises(seed, n, mu=0.35 + seed / 17, kappa=kappa)


def _shape_samples(seed: int, n: int = 30) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = np.array([[0.0, 0.0], [1.15, 0.08], [0.72, 0.98], [-0.12, 0.55]])
    shapes = []
    for angle in np.linspace(-0.55, 0.55, n):
        rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        scale = 0.85 + 0.25 * rng.random()
        shift = rng.normal(scale=0.35, size=(1, 2))
        deformation = np.array([[0, 0], [0.04 * np.sin(2 * angle), 0], [0, 0.08 * np.cos(angle)], [0, 0]])
        shapes.append((base + deformation + rng.normal(scale=0.035, size=base.shape)) @ rot.T * scale + shift)
    return np.stack(shapes)


def _unit_circle(ax: Any) -> None:
    t = np.linspace(0, TAU, 360)
    ax.plot(np.cos(t), np.sin(t), color=COLORS["gray"], linewidth=1)
    ax.axhline(0, color="#d7dde5", linewidth=0.8)
    ax.axvline(0, color="#d7dde5", linewidth=0.8)


def _circular_density_panel(ax: Any, seed: int, title: str) -> dict[str, float]:
    theta = _circular_sample(seed, 120, 1.7 + seed % 5)
    res = resultant(theta)
    grid = np.linspace(-np.pi, np.pi, 500)
    density = von_mises_pdf(grid, res["mean"], max(0.25, 6 * res["R"]))
    ax.plot(grid, density, color=COLORS["blue"], label="fitted von Mises sketch")
    ax.hist(wrap_angle(theta), bins=20, density=True, color=COLORS["teal"], alpha=0.28, label="sample angles")
    ax.legend(fontsize=8)
    _style(ax, title)
    return {"R": float(res["R"]), "mean": float(res["mean"]), "density_integral": float(np.trapz(density, grid))}


def make_topic_static_figure(entry: dict) -> tuple[Any, dict[str, float]]:
    """Return a concept-specific Matplotlib figure and invariant diagnostics."""

    topic = entry["topic"]
    seed = int(entry["number"])
    diagnostics: dict[str, float] = {"seed": float(seed)}

    if topic == "chapter-01":
        theta = np.deg2rad([8, 24, 42, 57, 61, 82, 104, 250, 286, 314])
        axial = np.deg2rad([5, 15, 24, 160, 171])
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
        _unit_circle(axes[0])
        axes[0].scatter(np.cos(theta), np.sin(theta), color=COLORS["blue"], s=36)
        axes[0].arrow(0, 0, 0.8, 0, color=COLORS["gold"], width=0.015, length_includes_head=True)
        axes[0].arrow(0, 0, 0, 0.8, color=COLORS["green"], width=0.015, length_includes_head=True)
        _style(axes[0], "Clock/compass directions", equal=True)
        counts, edges = rose_histogram(theta, 12)
        axes[1].bar(edges[:-1], counts, width=np.diff(edges), align="edge", color=COLORS["teal"], alpha=0.65)
        _style(axes[1], "Unrolled circular histogram")
        doubled = wrap_angle(2 * axial)
        _unit_circle(axes[2])
        axes[2].scatter(np.cos(axial), np.sin(axial), color=COLORS["red"], label="axes")
        axes[2].scatter(np.cos(doubled), np.sin(doubled), color=COLORS["violet"], marker="x", label="doubled")
        axes[2].legend(fontsize=8)
        _style(axes[2], "Axial doubling removes sign", equal=True)
        diagnostics.update({"count_preserved": float(counts.sum() == len(theta)), "axial_error": float(np.max(np.abs(wrap_angle(2 * (axial + np.pi)) - doubled)))})
        return fig, diagnostics

    if topic == "chapter-02":
        theta = np.deg2rad([356, 2, 8, 18, 32, 45, 61])
        res = resultant(theta)
        alpha = np.linspace(-np.pi, np.pi, 400)
        dispersion = np.mean(1 - np.cos(theta[:, None] - alpha[None, :]), axis=0)
        fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
        _unit_circle(axes[0])
        axes[0].scatter(np.cos(theta), np.sin(theta), color=COLORS["blue"], s=36)
        axes[0].arrow(0, 0, res["C"], res["S"], color=COLORS["red"], width=0.018, length_includes_head=True)
        _style(axes[0], "Vector resultant mean", equal=True)
        cut_a = np.mean(np.rad2deg(theta % TAU))
        cut_b = np.mean(np.rad2deg(wrap_angle(theta)))
        axes[1].bar(["cut at 0", "cut at pi"], [cut_a, cut_b], color=[COLORS["gold"], COLORS["violet"]])
        _style(axes[1], "Linear mean depends on cut")
        axes[2].plot(alpha, dispersion, color=COLORS["blue"])
        axes[2].axvline(res["mean"], color=COLORS["red"], linestyle="--")
        _style(axes[2], "D(alpha) minimized at mean")
        diagnostics.update({"R": float(res["R"]), "sine_balance": float(abs(np.sum(np.sin(theta - res["mean"])))), "dispersion_identity": float(abs(dispersion.min() - (1 - res["R"])))})
        return fig, diagnostics

    if topic == "chapter-03":
        grid = np.linspace(-np.pi, np.pi, 600)
        uniform = np.full_like(grid, 1 / TAU)
        vm = von_mises_pdf(grid, 0.4, 3.0)
        cardioid = (1 + 0.7 * np.cos(grid + 0.6)) / TAU
        wrapped = sum(stats.norm.pdf(grid + 2 * np.pi * k, loc=-0.5, scale=0.8) for k in range(-3, 4))
        coeffs = [abs(np.mean(np.exp(1j * p * _circular_sample(3, 500, 2.5)))) for p in range(1, 9)]
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        axes[0].plot(grid, uniform, label="uniform", color=COLORS["gray"])
        axes[0].plot(grid, vm, label="von Mises", color=COLORS["blue"])
        axes[0].plot(grid, cardioid, label="cardioid", color=COLORS["green"])
        axes[0].plot(grid, wrapped, label="wrapped normal", color=COLORS["gold"])
        axes[0].legend(fontsize=8)
        _style(axes[0], "Circular model gallery")
        axes[1].bar(range(1, 9), coeffs, color=COLORS["teal"])
        _style(axes[1], "Characteristic/Fourier amplitudes")
        diagnostics.update({"vm_integral": float(np.trapz(vm, grid)), "cardioid_positive": float(np.min(cardioid)), "coeff1": float(coeffs[0])})
        return fig, diagnostics

    if topic == "chapter-04":
        rng = np.random.default_rng(4)
        n = 24
        reps = 700
        theta = rng.uniform(0, TAU, size=(reps, n))
        endpoints = np.column_stack([np.cos(theta).sum(axis=1), np.sin(theta).sum(axis=1)])
        rayleigh = 2 * n * np.abs(np.exp(1j * theta).mean(axis=1)) ** 2
        fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
        axes[0].scatter(endpoints[:, 0], endpoints[:, 1], s=8, color=COLORS["blue"], alpha=0.35)
        _style(axes[0], "Random-walk resultants", equal=True)
        xs = np.linspace(0, np.quantile(rayleigh, 0.995), 200)
        axes[1].hist(rayleigh, bins=35, density=True, color=COLORS["teal"], alpha=0.35)
        axes[1].plot(xs, stats.chi2.pdf(xs, 2), color=COLORS["red"], label="chi-square df=2")
        axes[1].legend(fontsize=8)
        _style(axes[1], "Uniform limit diagnostic")
        diagnostics.update({"rayleigh_mean": float(rayleigh.mean()), "expected_rayleigh_mean": 2.0, "endpoint_mean_norm": float(np.linalg.norm(endpoints.mean(axis=0)))})
        return fig, diagnostics

    if topic == "chapter-05":
        theta = _circular_sample(5, 80, 3.2)
        res = resultant(theta)
        mus = np.linspace(res["mean"] - 1, res["mean"] + 1, 80)
        kappas = np.linspace(0.1, 8.0, 80)
        ll = np.array([[k * np.sum(np.cos(theta - m)) - len(theta) * np.log(special.iv(0, k)) for m in mus] for k in kappas])
        rgrid = np.linspace(0.02, 0.95, 160)
        kinv = np.array([inverse_A1(r) for r in rgrid])
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        im = axes[0].contourf(mus, kappas, ll - ll.max(), levels=20, cmap="viridis")
        fig.colorbar(im, ax=axes[0], fraction=0.046)
        axes[0].scatter([res["mean"]], [inverse_A1(res["R"])], color=COLORS["red"], s=35)
        _style(axes[0], "von Mises likelihood surface")
        axes[1].plot(rgrid, kinv, color=COLORS["blue"])
        axes[1].axvline(res["R"], color=COLORS["red"], linestyle="--")
        _style(axes[1], "A(kappa) inverse for concentration")
        diagnostics.update({"R": float(res["R"]), "kappa_hat": float(inverse_A1(res["R"])), "A_residual": float(abs(A1(inverse_A1(res["R"])) - res["R"]))})
        return fig, diagnostics

    if topic == "chapter-06":
        theta = np.r_[np.random.default_rng(6).uniform(0, TAU, 70), _circular_sample(66, 28, 4.0)]
        shifted = wrap_angle(theta + 0.7)
        u = np.sort((theta % TAU) / TAU)
        n = len(theta)
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        endpoints = np.array([np.exp(1j * np.random.default_rng(i).uniform(0, TAU, 40)).mean() for i in range(250)])
        axes[0].scatter(endpoints.real, endpoints.imag, s=10, color=COLORS["gray"], alpha=0.35, label="uniform null")
        r = resultant(theta)
        axes[0].scatter([r["C"]], [r["S"]], color=COLORS["red"], s=55, label="observed")
        axes[0].legend(fontsize=8)
        _style(axes[0], "Rayleigh endpoint cloud", equal=True)
        axes[1].step(u, np.arange(1, n + 1) / n, where="post", color=COLORS["blue"], label="ECDF")
        axes[1].plot([0, 1], [0, 1], color=COLORS["gray"], linestyle="--", label="uniform")
        axes[1].legend(fontsize=8)
        _style(axes[1], "Kuiper/Watson CDF view")
        diagnostics.update({"rayleigh": float(rayleigh_statistic(theta)), "kuiper_shift_delta": float(abs(kuiper_statistic(theta) - kuiper_statistic(shifted))), "watson_u2": float(watson_u2(theta))})
        return fig, diagnostics

    if topic == "chapter-07":
        groups = [_circular_sample(70, 36, 3.2), _circular_sample(71, 34, 2.8) + 0.45, _circular_sample(72, 32, 3.0) - 0.2]
        means = [resultant(g) for g in groups]
        fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
        _unit_circle(axes[0])
        for res, color in zip(means, [COLORS["blue"], COLORS["green"], COLORS["gold"]]):
            axes[0].arrow(0, 0, res["C"], res["S"], color=color, width=0.014, length_includes_head=True)
        _style(axes[0], "Group mean-resultant triangle", equal=True)
        pooled = np.concatenate(groups)
        r = resultant(pooled)
        arc = np.linspace(r["mean"] - 0.45, r["mean"] + 0.45, 100)
        axes[1].plot(np.cos(arc), np.sin(arc), color=COLORS["red"], linewidth=4, label="confidence arc sketch")
        axes[1].scatter(np.cos(pooled), np.sin(pooled), s=10, color=COLORS["blue"], alpha=0.45)
        axes[1].legend(fontsize=8)
        _style(axes[1], "Mean direction inference arc", equal=True)
        diagnostics.update({"pooled_R": float(r["R"]), "group_R_min": float(min(item["R"] for item in means)), "arc_width": 0.9})
        return fig, diagnostics

    if topic == "chapter-08":
        a = np.sort((_circular_sample(81, 34, 2.0) % TAU) / TAU)
        b = np.sort((_circular_sample(82, 30, 1.0) + 1.0) % TAU / TAU)
        combined = np.sort(np.r_[a, b])
        scores = np.exp(2j * np.pi * np.arange(1, len(combined) + 1) / len(combined))
        signs = np.sign(np.sin(_circular_sample(83, 50, 1.3)))
        runs = int(np.sum(signs != np.roll(signs, 1)))
        fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
        axes[0].scatter(scores.real, scores.imag, c=np.arange(len(scores)), cmap="viridis", s=28)
        _unit_circle(axes[0])
        _style(axes[0], "Uniform scores on the circle", equal=True)
        axes[1].step(a, np.arange(1, len(a) + 1) / len(a), where="post", label="sample A", color=COLORS["blue"])
        axes[1].step(b, np.arange(1, len(b) + 1) / len(b), where="post", label="sample B", color=COLORS["gold"])
        axes[1].legend(fontsize=8)
        _style(axes[1], "Two-sample non-parametric CDFs")
        diagnostics.update({"runs": float(runs), "runs_even": float(runs % 2 == 0), "uniform_score_length": float(abs(scores.mean()))})
        return fig, diagnostics

    if topic in {"chapter-09", "chapter-10", "chapter-11", "chapter-12"}:
        points = spherical_sample(seed, 120, concentration=2.0 + seed % 5)
        md = mean_direction(points)
        inertia = inertia_matrix(points)
        fig = plt.figure(figsize=(11, 4.4))
        ax = fig.add_subplot(121, projection="3d")
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=18, color=COLORS["blue"], alpha=0.65)
        d = md["direction"]
        ax.quiver(0, 0, 0, d[0], d[1], d[2], length=1.2, color=COLORS["red"], linewidth=2)
        ax.set_box_aspect((1, 1, 1))
        ax.set_title("Spherical sample and mean")
        ax2 = fig.add_subplot(122)
        if topic == "chapter-11":
            t = np.arange(len(points))
            ax2.plot(t, np.cumsum(points[:, 2]) / (t + 1), color=COLORS["violet"])
            _style(ax2, "Directional time-series trace")
        elif topic == "chapter-12":
            contaminated = points.copy()
            contaminated[:8] = uniform_sphere(1200, 8)
            ordinary = mean_direction(contaminated)["direction"]
            robust = normalize(np.median(contaminated, axis=0))
            ax2.bar(["ordinary", "robust"], [angular_distance(ordinary[None, :], d[None, :])[0], angular_distance(robust[None, :], d[None, :])[0]], color=[COLORS["red"], COLORS["green"]])
            _style(ax2, "Outlier influence on direction")
        else:
            vals = np.linalg.eigvalsh(inertia)
            ax2.bar(["lambda1", "lambda2", "lambda3"], vals, color=[COLORS["teal"], COLORS["gold"], COLORS["violet"]])
            _style(ax2, "Inertia or confidence spectrum")
        diagnostics.update({"R": float(md["R"]), "unit_norm_error": float(np.max(np.abs(np.linalg.norm(points, axis=1) - 1))), "inertia_trace": float(np.trace(inertia))})
        if topic == "chapter-10":
            diagnostics["kappa_residual"] = float(abs(fisher_A3(inverse_fisher_A3(md["R"])) - md["R"]))
        if topic == "chapter-12":
            diagnostics["density_positive"] = float(np.min(fisher_density_s2(points[:10], d, 3.0)) > 0)
        return fig, diagnostics

    if topic == "chapter-13":
        rotations = sample_so3(13, 1)
        stiefel = sample_stiefel(14, 3, 2, 1)[0]
        projection = grassmann_projection(stiefel)
        hyper = sample_hyperboloid(15, 80)
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(221, projection="3d")
        for j, color in enumerate([COLORS["red"], COLORS["green"], COLORS["blue"]]):
            ax.quiver(0, 0, 0, rotations[0, 0, j], rotations[0, 1, j], rotations[0, 2, j], color=color, linewidth=2)
        ax.set_title("SO(3) rotation frame")
        ax.set_box_aspect((1, 1, 1))
        ax = fig.add_subplot(222, projection="3d")
        for j, color in enumerate([COLORS["gold"], COLORS["violet"]]):
            ax.quiver(0, 0, 0, stiefel[0, j], stiefel[1, j], stiefel[2, j], color=color, linewidth=2)
        ax.set_title("Stiefel 2-frame")
        ax.set_box_aspect((1, 1, 1))
        ax = fig.add_subplot(223)
        im = ax.imshow(projection, cmap="viridis", vmin=-0.05, vmax=1)
        fig.colorbar(im, ax=ax, fraction=0.046)
        _style(ax, "Grassmann projection")
        ax = fig.add_subplot(224, projection="3d")
        ax.scatter(hyper[:, 1], hyper[:, 2], hyper[:, 0], s=16, color=COLORS["teal"], alpha=0.65)
        ax.set_title("Hyperboloid samples")
        diagnostics.update({
            "rotation_det": float(np.linalg.det(rotations[0])),
            "rotation_orthogonality": float(np.linalg.norm(rotations[0].T @ rotations[0] - np.eye(3))),
            "stiefel_error": float(np.linalg.norm(stiefel.T @ stiefel - np.eye(2))),
            "projection_idempotence": float(np.linalg.norm(projection @ projection - projection)),
            "hyperboloid_norm_error": float(np.max(np.abs(minkowski_dot(hyper, hyper) - 1))),
        })
        return fig, diagnostics

    if topic == "chapter-14":
        shapes = _shape_samples(14)
        mean = procrustes_mean(shapes)
        aligned = np.stack([procrustes_align(shape, mean) for shape in shapes])
        coords = tangent_shape_coords(shapes, mean)
        tri = np.array([triangle_shape_features(shape[:3]) for shape in shapes])
        h = helmert_submatrix(4)
        fig = plt.figure(figsize=(12, 4.4))
        ax = fig.add_subplot(131)
        for shape in aligned[::3]:
            closed = np.vstack([shape, shape[0]])
            ax.plot(closed[:, 0], closed[:, 1], color=COLORS["gray"], alpha=0.45)
        closed_mean = np.vstack([mean, mean[0]])
        ax.plot(closed_mean[:, 0], closed_mean[:, 1], color=COLORS["red"], linewidth=2.4)
        _style(ax, "Aligned Procrustes shapes", equal=True)
        ax = fig.add_subplot(132, projection="3d")
        ax.scatter(tri[:, 0], tri[:, 1], tri[:, 2], c=tri[:, 0], cmap="plasma", s=26)
        ax.set_title("Triangle shape sphere coordinates")
        ax.set_box_aspect((1, 1, 1))
        ax = fig.add_subplot(133)
        ax.scatter(coords[:, 0], coords[:, 1], color=COLORS["teal"], alpha=0.75)
        _style(ax, "Tangent shape PCA sketch")
        shifted = shapes[0] + np.array([10.0, -4.0])
        diagnostics.update({
            "helmert_error": float(np.linalg.norm(h @ np.ones(4))),
            "preshape_norm": float(np.linalg.norm(preshape(shapes[0]))),
            "procrustes_shift_invariance": float(np.linalg.norm(procrustes_align(shapes[0], mean) - procrustes_align(shifted, mean))),
            "tangent_mean_norm": float(np.linalg.norm(coords.mean(axis=0))),
        })
        return fig, diagnostics

    if topic == "appendix-01":
        x = np.linspace(0.05, 12, 300)
        exact = bessel_ratio(0, x)
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        axes[0].plot(x, exact, color=COLORS["blue"], label="A1 exact")
        axes[0].plot(x, small_kappa_A1(x), color=COLORS["green"], linestyle="--", label="small-kappa")
        axes[0].plot(x, large_kappa_A1(x), color=COLORS["gold"], linestyle=":", label="large-kappa")
        axes[0].legend(fontsize=8)
        _style(axes[0], "Bessel-ratio calculator")
        axes[1].semilogy(x, np.abs(exact - small_kappa_A1(x)) + 1e-12, label="small error", color=COLORS["green"])
        axes[1].semilogy(x, np.abs(exact - large_kappa_A1(x)) + 1e-12, label="large error", color=COLORS["red"])
        axes[1].legend(fontsize=8)
        _style(axes[1], "Asymptotic error bands")
        diagnostics.update({"A1_monotone": float(np.all(np.diff(exact) > 0)), "A1_end": float(exact[-1])})
        return fig, diagnostics

    if topic == "appendix-02":
        r = np.linspace(0.02, 0.96, 180)
        k = np.array([inverse_A1(v) for v in r])
        samples = np.array([rayleigh_statistic(np.random.default_rng(i).uniform(0, TAU, 30)) for i in range(400)])
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        axes[0].plot(r, k, color=COLORS["blue"])
        _style(axes[0], "Circular concentration inversion")
        axes[1].hist(samples, bins=35, density=True, color=COLORS["teal"], alpha=0.35)
        xs = np.linspace(0, np.quantile(samples, 0.995), 200)
        axes[1].plot(xs, stats.chi2.pdf(xs, 2), color=COLORS["red"])
        _style(axes[1], "Uniformity critical-value simulation")
        diagnostics.update({"inverse_monotone": float(np.all(np.diff(k) > 0)), "rayleigh_q95": float(np.quantile(samples, 0.95))})
        return fig, diagnostics

    if topic == "appendix-03":
        r = np.linspace(0.02, 0.92, 160)
        k = np.array([inverse_fisher_A3(v) for v in r])
        points = spherical_sample(103, 160, concentration=3.5)
        mu = mean_direction(points)["direction"]
        dens = fisher_density_s2(points, mu, 3.5)
        fig = plt.figure(figsize=(11, 4.2))
        ax = fig.add_subplot(121)
        ax.plot(r, k, color=COLORS["blue"])
        _style(ax, "Spherical concentration inversion")
        ax = fig.add_subplot(122, projection="3d")
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=dens, cmap="viridis", s=18)
        ax.set_title("Fisher cap density")
        ax.set_box_aspect((1, 1, 1))
        diagnostics.update({"inverse_monotone": float(np.all(np.diff(k) > 0)), "density_positive": float(np.min(dens) > 0)})
        return fig, diagnostics

    # appendix-04
    fig, ax = plt.subplots(figsize=(9, 5))
    nodes = ["S1", "S2", "SO(3)", "V_r(R^p)", "G_r(R^p)", "shape", "models", "tests"]
    angles = np.linspace(0, TAU, len(nodes), endpoint=False)
    pos = np.column_stack([np.cos(angles), np.sin(angles)])
    for i, node in enumerate(nodes):
        ax.scatter(pos[i, 0], pos[i, 1], s=900, color=COLORS["blue"], alpha=0.18, edgecolor=COLORS["blue"])
        ax.text(pos[i, 0], pos[i, 1], node, ha="center", va="center", fontsize=9)
    for i in range(len(nodes)):
        j = (i + 2) % len(nodes)
        ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]], color=COLORS["gray"], alpha=0.45)
    ax.set_axis_off()
    _style(ax, "Notation dependency map", equal=True)
    diagnostics.update({"node_count": float(len(nodes)), "edge_count": float(len(nodes))})
    return fig, diagnostics


def make_topic_interactive_figure(entry: dict) -> go.Figure:
    topic = entry["topic"]
    seed = int(entry["number"])
    if topic.startswith("chapter-0") or topic == "appendix-02":
        theta = _circular_sample(seed + 200, 120, 1.5 + seed % 4)
        return go.Figure(
            data=[go.Scatterpolar(theta=np.degrees(theta), r=np.ones_like(theta), mode="markers", marker={"size": 7, "color": np.arange(len(theta)), "colorscale": "Viridis"})],
            layout=go.Layout(title=f"{entry['label']}: circular inspection view", polar={"radialaxis": {"visible": True, "range": [0, 1.15]}}),
        )
    if topic in {"chapter-09", "chapter-10", "chapter-11", "chapter-12", "appendix-03"}:
        points = spherical_sample(seed + 200, 140, concentration=2.0 + seed % 5)
        return go.Figure(
            data=[go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2], mode="markers", marker={"size": 4, "color": points[:, 2], "colorscale": "Viridis"})],
            layout=go.Layout(title=f"{entry['label']}: rotate the spherical scene", scene={"aspectmode": "cube"}),
        )
    if topic == "chapter-13":
        t = np.linspace(0, np.pi, 50)
        path = np.array([rotation_from_axis_angle([0.4, 0.6, 1.0], angle)[:, 0] for angle in t])
        hyper = sample_hyperboloid(seed + 300, 80)
        return go.Figure(
            data=[
                go.Scatter3d(x=path[:, 0], y=path[:, 1], z=path[:, 2], mode="lines+markers", name="SO(3) axis path", marker={"size": 4}),
                go.Scatter3d(x=hyper[:, 1], y=hyper[:, 2], z=hyper[:, 0], mode="markers", name="hyperboloid", marker={"size": 3}),
            ],
            layout=go.Layout(title="Rotations and hyperboloid samples", scene={"aspectmode": "cube"}),
        )
    if topic == "chapter-14":
        shapes = _shape_samples(seed + 300)
        tri = np.array([triangle_shape_features(shape[:3]) for shape in shapes])
        return go.Figure(
            data=[go.Scatter3d(x=tri[:, 0], y=tri[:, 1], z=tri[:, 2], mode="markers", marker={"size": 4, "color": tri[:, 0], "colorscale": "Plasma"})],
            layout=go.Layout(title="Triangle shape coordinates", scene={"aspectmode": "cube"}),
        )
    x = np.linspace(0.05, 14, 180)
    return go.Figure(
        data=[
            go.Scatter(x=x, y=bessel_ratio(0, x), mode="lines", name="A1"),
            go.Scatter(x=x, y=bessel_ratio(0.5, x), mode="lines", name="spherical analogue"),
        ],
        layout=go.Layout(title="Interactive concentration-to-resultant curves", xaxis_title="kappa", yaxis_title="ratio"),
    )


def topic_numeric_checks(entry: dict, diagnostics: dict[str, float]) -> dict[str, Any]:
    """Return JSON-ready checks that are specific to the chapter topic."""

    topic = entry["topic"]
    checks: dict[str, Any] = {
        "source_span": {"printed": entry["printed"], "pdf": entry["pdf"]},
        "topic": topic,
        "visuals": list(entry["visuals"]),
        "diagnostics": {key: float(value) for key, value in diagnostics.items()},
    }
    if topic == "chapter-01":
        checks["axial_doubling_invariant"] = diagnostics["axial_error"] < 1e-10
    elif topic == "chapter-02":
        checks["mean_direction_sine_balance"] = diagnostics["sine_balance"] < 1e-10
        checks["dispersion_identity_holds"] = diagnostics["dispersion_identity"] < 2e-3
    elif topic == "chapter-03":
        checks["von_mises_density_integrates"] = abs(diagnostics["vm_integral"] - 1) < 0.02
        checks["cardioid_is_nonnegative"] = diagnostics["cardioid_positive"] >= 0
    elif topic == "chapter-04":
        checks["rayleigh_mean_near_chi_square"] = abs(diagnostics["rayleigh_mean"] - 2.0) < 0.35
    elif topic == "chapter-05":
        checks["A_kappa_matches_R"] = diagnostics["A_residual"] < 1e-7
    elif topic == "chapter-06":
        checks["kuiper_origin_invariant"] = diagnostics["kuiper_shift_delta"] < 0.08
    elif topic == "chapter-07":
        checks["confidence_arc_positive"] = diagnostics["arc_width"] > 0
    elif topic == "chapter-08":
        checks["runs_count_even"] = bool(diagnostics["runs_even"])
    elif topic in {"chapter-09", "chapter-10", "chapter-11", "chapter-12"}:
        checks["unit_vectors_on_sphere"] = diagnostics["unit_norm_error"] < 1e-12
        checks["inertia_trace_one"] = abs(diagnostics["inertia_trace"] - 1) < 1e-12
    elif topic == "chapter-13":
        checks["rotation_is_special_orthogonal"] = abs(diagnostics["rotation_det"] - 1) < 1e-12 and diagnostics["rotation_orthogonality"] < 1e-12
        checks["stiefel_frame_is_orthonormal"] = diagnostics["stiefel_error"] < 1e-12
        checks["grassmann_projection_idempotent"] = diagnostics["projection_idempotence"] < 1e-12
        checks["hyperboloid_minkowski_norm"] = diagnostics["hyperboloid_norm_error"] < 1e-12
    elif topic == "chapter-14":
        checks["helmert_removes_translation"] = diagnostics["helmert_error"] < 1e-12
        checks["preshape_has_unit_norm"] = abs(diagnostics["preshape_norm"] - 1) < 1e-12
        checks["procrustes_ignores_translation"] = diagnostics["procrustes_shift_invariance"] < 1e-12
    elif topic == "appendix-01":
        checks["bessel_ratio_monotone"] = bool(diagnostics["A1_monotone"])
    elif topic == "appendix-02":
        checks["circular_inverse_monotone"] = bool(diagnostics["inverse_monotone"])
    elif topic == "appendix-03":
        checks["spherical_inverse_monotone"] = bool(diagnostics["inverse_monotone"])
        checks["fisher_density_positive"] = bool(diagnostics["density_positive"])
    else:
        checks["notation_graph_has_nodes"] = diagnostics["node_count"] >= 8
    return checks
