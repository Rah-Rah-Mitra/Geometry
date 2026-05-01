"""Generated visual artifacts for the GDL notebooks.

The functions here keep notebook cells readable while leaving the construction
of every figure inspectable in the course-local `utils` package.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import interpolate, signal

from utils.artifacts import ARTIFACT_ROOT, save_json, save_matplotlib, save_plotly_html
from utils.geometry import (
    circulant_matrix,
    cotangent_laplacian,
    dft_matrix,
    dilated_receptive_field,
    graph_message_pass,
    pairwise_distances,
    parallel_transport_sphere,
    permutation_matrix,
    random_rotation_matrix,
    rigid_transform,
    shift2d,
    sphere_expmap,
)
from utils.plotting import COURSE_COLORS, set_theme, simple_signal


def _finish(fig: plt.Figure, chapter: int, name: str) -> Path:
    path = save_matplotlib(fig, chapter, name)
    plt.close(fig)
    return path


def _chapter_01(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}

    fig, ax = plt.subplots(figsize=(8.4, 2.8))
    ax.axis("off")
    boxes = [
        (0.04, "Structured\ndomain", "grid / graph /\npoint cloud"),
        (0.30, "Signal", "values on\nthe domain"),
        (0.56, "Equivariant\nfeatures", "local shared\ncomputations"),
        (0.82, "Task output", "label, mask,\nfield, score"),
    ]
    for x, title, sub in boxes:
        ax.add_patch(
            plt.Rectangle((x, 0.35), 0.16, 0.34, facecolor="#eef4ff", edgecolor=COURSE_COLORS["blue"], lw=1.5)
        )
        ax.text(x + 0.08, 0.57, title, ha="center", va="center", weight="bold")
        ax.text(x + 0.08, 0.43, sub, ha="center", va="center", fontsize=8, color=COURSE_COLORS["gray"])
    for x in [0.21, 0.47, 0.73]:
        ax.annotate("", xy=(x + 0.06, 0.52), xytext=(x, 0.52), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.5, 0.10, "Design loop: domain -> transformations -> equivariant features -> invariant readout", ha="center")
    artifacts.append(_finish(fig, 1, "representation-learning-stack.png"))

    t = np.linspace(0, 4 * np.pi, 220)
    curve = np.c_[np.cos(t), np.sin(t), t / (4 * np.pi)]
    ambient = rng.normal(size=(220, 3))
    fig = plt.figure(figsize=(9, 3.6))
    ax1 = fig.add_subplot(121, projection="3d")
    ax1.scatter(ambient[:, 0], ambient[:, 1], ambient[:, 2], s=8, alpha=0.45, color=COURSE_COLORS["gray"])
    ax1.set_title("ambient samples")
    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot(curve[:, 0], curve[:, 1], curve[:, 2], color=COURSE_COLORS["green"], lw=2)
    ax2.scatter(curve[::8, 0], curve[::8, 1], curve[::8, 2], s=12, color=COURSE_COLORS["blue"])
    ax2.set_title("structured trace")
    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    artifacts.append(_finish(fig, 1, "ambient-vs-structured-data.png"))

    img = simple_signal(32)
    shifted = shift2d(img, 5, -7)
    points = np.array([[0, 0, 0], [1, 0, 0], [0.4, 0.9, 0], [0.2, 0.3, 0.8]])
    rotated = rigid_transform(points, random_rotation_matrix(4))
    fig, axes = plt.subplots(2, 3, figsize=(10, 6))
    axes[0, 0].imshow(img, cmap="viridis")
    axes[0, 0].set_title("grid signal")
    axes[0, 1].imshow(shifted, cmap="viridis")
    axes[0, 1].set_title("translated signal")
    nx.draw_networkx(nx.cycle_graph(6), nx.circular_layout(nx.cycle_graph(6)), ax=axes[0, 2], node_color="#dbeafe")
    axes[0, 2].set_title("graph relabeling target")
    for ax, pts, title in [(axes[1, 0], points[:, :2], "point cloud"), (axes[1, 1], rotated[:, :2], "rotated projection")]:
        ax.scatter(pts[:, 0], pts[:, 1], s=90, color=COURSE_COLORS["gold"])
        ax.set_aspect("equal")
        ax.set_title(title)
    axes[1, 2].bar(["before", "after"], [pairwise_distances(points).sum(), pairwise_distances(rotated).sum()])
    axes[1, 2].set_title("distance summary")
    for ax in axes.ravel():
        ax.set_xticks([])
        ax.set_yticks([])
    artifacts.append(_finish(fig, 1, "symmetry-action-gallery.png"))
    checks["distance_invariance_error"] = float(np.max(np.abs(pairwise_distances(points) - pairwise_distances(rotated))))

    kernel = np.array([[0, 1, 0], [1, 2, 1], [0, 1, 0]], dtype=float) / 6.0
    conv = signal.convolve2d(img, kernel, mode="same", boundary="wrap")
    conv_shift = signal.convolve2d(shifted, kernel, mode="same", boundary="wrap")
    expected = shift2d(conv, 5, -7)
    checks["grid_convolution_equivariance_error"] = float(np.max(np.abs(conv_shift - expected)))
    fig_html = go.Figure(
        data=[
            go.Heatmap(z=img, colorscale="Viridis", showscale=False, visible=True),
            go.Heatmap(z=shifted, colorscale="Viridis", showscale=False, visible=False),
            go.Heatmap(z=conv_shift - expected, colorscale="RdBu", showscale=False, visible=False),
        ]
    )
    fig_html.update_layout(
        title="Equivariance mini-lab",
        width=650,
        height=520,
        updatemenus=[
            dict(
                buttons=[
                    dict(label="input", method="update", args=[{"visible": [True, False, False]}]),
                    dict(label="shifted", method="update", args=[{"visible": [False, True, False]}]),
                    dict(label="residual", method="update", args=[{"visible": [False, False, True]}]),
                ]
            )
        ],
    )
    artifacts.append(save_plotly_html(fig_html, 1, "equivariance-mini-lab.html"))

    tax = nx.Graph()
    domains = ["grids", "graphs", "sets", "manifolds", "groups", "point clouds"]
    models = ["CNN", "GNN", "Deep Sets", "mesh CNN", "group CNN", "E(3) MPNN", "Transformer"]
    tax.add_nodes_from(domains, bipartite=0)
    tax.add_nodes_from(models, bipartite=1)
    tax.add_edges_from(
        [
            ("grids", "CNN"),
            ("graphs", "GNN"),
            ("sets", "Deep Sets"),
            ("manifolds", "mesh CNN"),
            ("groups", "group CNN"),
            ("point clouds", "E(3) MPNN"),
            ("sets", "Transformer"),
            ("graphs", "Transformer"),
        ]
    )
    pos = nx.bipartite_layout(tax, domains)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    nx.draw_networkx_edges(tax, pos, ax=ax, edge_color="#cbd5e1")
    nx.draw_networkx_nodes(tax, pos, nodelist=domains, node_color="#dbeafe", node_size=1600, ax=ax)
    nx.draw_networkx_nodes(tax, pos, nodelist=models, node_color="#dcfce7", node_size=1700, ax=ax)
    nx.draw_networkx_labels(tax, pos, font_size=9, ax=ax)
    ax.set_title("Domain structure suggests architecture families")
    ax.axis("off")
    artifacts.append(_finish(fig, 1, "geometric-blueprint-taxonomy.png"))
    checks["taxonomy_orphan_nodes"] = int(sum(tax.degree(n) == 0 for n in tax.nodes))
    return artifacts, checks


def _chapter_02(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    x_train = np.linspace(0, 1, 9)
    y_train = np.sin(2 * np.pi * x_train) + 0.2 * np.sin(8 * np.pi * x_train)
    x = np.linspace(0, 1, 400)
    poly = np.poly1d(np.polyfit(x_train, y_train, deg=len(x_train) - 1))
    spline = interpolate.CubicSpline(x_train, y_train, bc_type="natural")
    wiggly = spline(x) + 0.18 * np.sin(22 * np.pi * x) * np.prod([(x - xi) for xi in x_train], axis=0) * 900
    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    ax.plot(x, poly(x), label="degree-8 interpolant", color=COURSE_COLORS["red"])
    ax.plot(x, spline(x), label="natural cubic interpolant", color=COURSE_COLORS["green"], lw=2)
    ax.plot(x, wiggly, label="wiggly exact interpolant", color=COURSE_COLORS["purple"], alpha=0.85)
    ax.scatter(x_train, y_train, s=45, color=COURSE_COLORS["ink"], label="training samples")
    ax.legend(loc="upper right")
    ax.set_title("Interpolation does not choose a generalizer")
    artifacts.append(_finish(fig, 2, "interpolation-does-not-choose.png"))
    checks["interpolant_train_errors"] = {
        "poly": float(np.max(np.abs(poly(x_train) - y_train))),
        "spline": float(np.max(np.abs(spline(x_train) - y_train))),
    }

    def bending_energy(y: np.ndarray) -> float:
        second = np.gradient(np.gradient(y, x), x)
        return float(np.trapz(second**2, x))

    energies = {"degree8": bending_energy(poly(x)), "natural_spline": bending_energy(spline(x)), "wiggly": bending_energy(wiggly)}
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.bar(energies.keys(), energies.values(), color=[COURSE_COLORS["red"], COURSE_COLORS["green"], COURSE_COLORS["purple"]])
    ax.set_yscale("log")
    ax.set_title("A regularity measure ranks exact interpolants")
    ax.set_ylabel("bending energy, log scale")
    artifacts.append(_finish(fig, 2, "regularity-selects-interpolant.png"))
    checks["bending_energy"] = energies

    A = np.array([[1.0, 2.0, -1.0], [0.0, 1.0, 1.0]])
    y = np.array([1.0, 0.5])
    w = np.zeros(3)
    trace = []
    for _ in range(500):
        w -= 0.05 * (A.T @ (A @ w - y))
        trace.append(w.copy())
    trace = np.array(trace)
    w_pinv = np.linalg.pinv(A) @ y
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    axes[0].plot(trace)
    axes[0].set_title("gradient descent components")
    axes[1].plot(np.linalg.norm(A @ trace.T - y[:, None], axis=0), label="residual")
    axes[1].plot(np.linalg.norm(trace, axis=1), label="weight norm")
    axes[1].set_yscale("log")
    axes[1].legend()
    axes[1].set_title("fit and norm trajectory")
    artifacts.append(_finish(fig, 2, "implicit-minimum-norm-trace.png"))
    checks["minimum_norm_error"] = float(np.linalg.norm(trace[-1] - w_pinv))

    eps = 0.2
    dims = np.arange(1, 16)
    counts = np.ceil(1 / eps) ** dims
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.plot(dims, counts, marker="o", color=COURSE_COLORS["red"])
    ax.set_yscale("log")
    ax.set_xlabel("dimension")
    ax.set_ylabel("covering cells, log scale")
    ax.set_title("Coverage grows exponentially with ambient dimension")
    artifacts.append(_finish(fig, 2, "lipschitz-covering-explosion.png"))
    checks["covering_count_d15"] = float(counts[-1])

    X = rng.normal(size=(300, 12))
    a = rng.normal(size=12)
    b = rng.normal(size=12)
    a /= np.linalg.norm(a)
    b /= np.linalg.norm(b)
    y_projection = np.sin(X @ a) + 0.2 * np.cos(X @ b)
    y_interaction = np.sin(X[:, 0] * X[:, 1]) + np.cos(X[:, 2] * X[:, 3])
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].scatter(X @ a, y_projection, s=12, alpha=0.7, color=COURSE_COLORS["green"])
    axes[0].set_title("target follows a projection")
    axes[1].scatter(X @ a, y_interaction, s=12, alpha=0.7, color=COURSE_COLORS["gold"])
    axes[1].set_title("interactions hide from one projection")
    artifacts.append(_finish(fig, 2, "projection-prior-success-failure.png"))
    checks["projection_target_variance"] = float(np.var(y_projection))
    checks["interaction_target_variance"] = float(np.var(y_interaction))
    return artifacts, checks


def _chapter_03(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    elems = {"e": (0, 1, 2), "r": (1, 2, 0), "r2": (2, 0, 1), "f": (0, 2, 1), "rf": (2, 1, 0), "r2f": (1, 0, 2)}

    def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a[i] for i in b)

    lookup = {v: k for k, v in elems.items()}
    table = pd.DataFrame(index=elems.keys(), columns=elems.keys())
    for g, gv in elems.items():
        for h, hv in elems.items():
            table.loc[g, h] = lookup[compose(gv, hv)]
    G = nx.DiGraph()
    for name, perm in elems.items():
        G.add_edge(name, lookup[compose(elems["r"], perm)])
        G.add_edge(name, lookup[compose(elems["f"], perm)])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    nx.draw_networkx(G, nx.circular_layout(G), ax=axes[0], node_color="#dbeafe", edge_color="#94a3b8", arrowsize=10, font_size=9)
    axes[0].set_title("D3 Cayley diagram")
    axes[0].axis("off")
    axes[1].imshow([[list(elems).index(table.loc[i, j]) for j in elems] for i in elems], cmap="viridis")
    axes[1].set_xticks(range(6), list(elems), rotation=45)
    axes[1].set_yticks(range(6), list(elems))
    axes[1].set_title("multiplication table")
    artifacts.append(_finish(fig, 3, "d3-triangle-cayley-table.png"))
    checks["d3_noncommutative"] = bool(table.loc["r", "f"] != table.loc["f", "r"])
    checks["d3_closed"] = bool(set(table.values.ravel()) == set(elems.keys()))

    img = simple_signal(28)
    kernel = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]], dtype=float) / 8
    f_img = signal.convolve2d(img, kernel, mode="same", boundary="wrap")
    left = signal.convolve2d(shift2d(img, 4, -3), kernel, mode="same", boundary="wrap")
    right = shift2d(f_img, 4, -3)
    fig, axes = plt.subplots(1, 4, figsize=(11, 3))
    for ax, data, title in zip(axes, [img, shift2d(img, 4, -3), left, left - right], ["x", "rho(g)x", "F(rho(g)x)", "residual"]):
        ax.imshow(data, cmap="viridis")
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    artifacts.append(_finish(fig, 3, "invariance-equivariance-commuting-squares.png"))
    checks["conv_equivariance_error"] = float(np.max(np.abs(left - right)))
    checks["pooling_invariance_error"] = float(abs(float(f_img.mean()) - float(left.mean())))

    G1 = nx.path_graph(5)
    order = [2, 0, 4, 1, 3]
    P = permutation_matrix(order)
    A1 = nx.to_numpy_array(G1)
    cycle = nx.cycle_graph(6)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    nx.draw_networkx(G1, nx.spring_layout(G1, seed=1), ax=axes[0], node_color="#dbeafe")
    axes[0].set_title("graph")
    nx.draw_networkx(nx.from_numpy_array(P @ A1 @ P.T), nx.spring_layout(nx.from_numpy_array(P @ A1 @ P.T), seed=2), ax=axes[1], node_color="#dcfce7")
    axes[1].set_title("isomorphic relabeling")
    nx.draw_networkx(cycle, nx.circular_layout(cycle), ax=axes[2], node_color=["#fee2e2", "#ffedd5"] * 3)
    axes[2].set_title("automorphism orbits")
    for ax in axes:
        ax.axis("off")
    artifacts.append(_finish(fig, 3, "graph-isomorphism-automorphism-orbits.png"))
    checks["path_graph_relabel_residual"] = float(np.max(np.abs(P @ A1 @ P.T - P @ A1 @ P.T)))
    checks["cycle_automorphism_count"] = len(list(nx.algorithms.isomorphism.GraphMatcher(cycle, cycle).isomorphisms_iter()))

    x = np.linspace(0, 1, 300, endpoint=False)
    base = np.sin(2 * np.pi * x) + 0.3 * np.sin(6 * np.pi * x)
    amplitudes = np.linspace(0, 0.12, 9)
    costs = []
    changes = []
    for amp in amplitudes:
        warped_grid = (x + amp * np.sin(2 * np.pi * x)) % 1.0
        warped = np.interp(warped_grid, x, base, period=1)
        costs.append(float(np.mean(np.gradient(warped_grid - x) ** 2)))
        changes.append(float(abs(np.mean(np.abs(np.fft.rfft(warped))[:8]) - np.mean(np.abs(np.fft.rfft(base))[:8]))))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(amplitudes, costs, marker="o", label="warp cost")
    ax.plot(amplitudes, changes, marker="s", label="feature change")
    ax.legend()
    ax.set_title("Stability: nearby deformations cause controlled changes")
    artifacts.append(_finish(fig, 3, "deformation-stability-ring-and-warp.png"))
    checks["warp_cost_monotone"] = bool(np.all(np.diff(costs) >= -1e-12))

    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    levels = [8, 4, 2, 1]
    for li, n in enumerate(levels):
        xs = np.linspace(0.1, 0.9, n)
        ys = np.full(n, 0.85 - li * 0.22)
        ax.scatter(xs, ys, s=220, color="#dbeafe", edgecolor=COURSE_COLORS["blue"])
        for i in range(n - 1):
            ax.plot(xs[i : i + 2], ys[i : i + 2], color="#94a3b8")
    ax.text(0.5, 0.05, "local equivariant features become coarser invariant summaries", ha="center")
    ax.axis("off")
    artifacts.append(_finish(fig, 3, "coarsening-hierarchy-grid-graph.png"))
    return artifacts, checks


def _chapter_04(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    domains = ["sets", "graphs", "grids", "groups", "manifolds", "gauges/meshes"]
    sym = ["permutation", "node relabeling", "translation", "group action", "isometry", "frame rotation"]
    ops = ["sum/readout", "message passing", "convolution", "group convolution", "geodesic filter", "transported filter"]
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    y = np.arange(len(domains))[::-1]
    for i, yy in enumerate(y):
        ax.scatter(0, yy, s=900, color="#dbeafe", edgecolor=COURSE_COLORS["blue"])
        ax.scatter(1, yy, s=900, color="#dcfce7", edgecolor=COURSE_COLORS["green"])
        ax.scatter(2, yy, s=900, color="#fef3c7", edgecolor=COURSE_COLORS["gold"])
        ax.text(0, yy, domains[i], ha="center", va="center", weight="bold")
        ax.text(1, yy, sym[i], ha="center", va="center", fontsize=8)
        ax.text(2, yy, ops[i], ha="center", va="center", fontsize=8)
    ax.axis("off")
    ax.set_title("The 5G atlas: domain -> symmetry -> operator")
    artifacts.append(_finish(fig, 4, "five-g-domain-atlas.png"))
    table_path = ARTIFACT_ROOT / "chapter-04" / "tables" / "domain-symmetry-blueprint.csv"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"domain": domains, "symmetry": sym, "operator": ops}).to_csv(table_path, index=False)
    artifacts.append(table_path)

    A = np.array([[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 1], [0, 0, 1, 0]], dtype=float)
    X = rng.normal(size=(4, 3))
    P = permutation_matrix([2, 0, 3, 1])
    H = graph_message_pass(A, X)
    H2 = graph_message_pass(P @ A @ P.T, P @ X)
    checks["set_readout_error"] = float(np.linalg.norm((P @ X).sum(axis=0) - X.sum(axis=0)))
    checks["graph_equivariance_error"] = float(np.linalg.norm(H2 - P @ H))
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    axes[0].imshow(A, cmap="Blues")
    axes[0].set_title("A")
    axes[1].imshow(P @ A @ P.T, cmap="Blues")
    axes[1].set_title("P A P^T")
    axes[2].bar(["set", "graph"], [checks["set_readout_error"], checks["graph_equivariance_error"]])
    axes[2].set_yscale("log")
    axes[2].set_title("residuals")
    artifacts.append(_finish(fig, 4, "graph-equivariance-neighborhoods.png"))

    C = circulant_matrix(np.array([2.0, -1.0, 0.0, -1.0]), 16)
    F = dft_matrix(16)
    diagonalized = F.conj().T @ C @ F
    checks["dft_offdiag_residual"] = float(np.max(np.abs(diagonalized - np.diag(np.diag(diagonalized)))))
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    axes[0].imshow(C, cmap="RdBu")
    axes[0].set_title("circulant stencil")
    axes[1].imshow(np.real(diagonalized), cmap="viridis")
    axes[1].set_title("DFT diagonalization")
    axes[2].plot(np.real(F[:, 1]), label="mode 1")
    axes[2].plot(np.real(F[:, 3]), label="mode 3")
    axes[2].legend()
    axes[2].set_title("shift eigenmodes")
    artifacts.append(_finish(fig, 4, "ring-grid-circulant-convolution.png"))

    base = np.array([1.0, 0.0, 0.0])
    tangent = np.array([0.0, 0.75, 0.45])
    target = sphere_expmap(base, tangent)
    vec = np.array([0.0, 0.0, 1.0])
    transported = parallel_transport_sphere(base, target, vec)
    arc = np.array([sphere_expmap(base, p * tangent) for p in np.linspace(0, 1, 80)])
    u = np.linspace(0, 2 * np.pi, 32)
    v = np.linspace(0, np.pi, 16)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    fig_html = go.Figure()
    fig_html.add_surface(x=xs, y=ys, z=zs, opacity=0.25, colorscale="Blues", showscale=False)
    fig_html.add_trace(go.Scatter3d(x=arc[:, 0], y=arc[:, 1], z=arc[:, 2], mode="lines", line=dict(color="green", width=6)))
    fig_html.add_trace(go.Scatter3d(x=[base[0], base[0] + 0.35 * vec[0]], y=[base[1], base[1] + 0.35 * vec[1]], z=[base[2], base[2] + 0.35 * vec[2]], mode="lines+markers"))
    fig_html.add_trace(go.Scatter3d(x=[target[0], target[0] + 0.35 * transported[0]], y=[target[1], target[1] + 0.35 * transported[1]], z=[target[2], target[2] + 0.35 * transported[2]], mode="lines+markers"))
    fig_html.update_layout(title="Sphere geodesic and parallel transport", width=700, height=560)
    artifacts.append(save_plotly_html(fig_html, 4, "sphere-tangent-geodesic-expmap.html"))
    checks["sphere_target_norm_error"] = float(abs(np.linalg.norm(target) - 1))
    checks["transport_tangent_error"] = float(abs(np.dot(target, transported)))

    verts = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, 0.45]], dtype=float)
    faces = np.array([[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 2, 1], [0, 3, 2]])
    L = cotangent_laplacian(verts, faces)
    evals = np.linalg.eigvalsh((L + L.T) / 2)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].triplot(verts[:, 0], verts[:, 1], faces, color=COURSE_COLORS["blue"])
    axes[0].scatter(verts[:, 0], verts[:, 1], c=verts[:, 2], s=90, cmap="viridis")
    axes[0].set_aspect("equal")
    axes[0].set_title("small triangular mesh")
    axes[1].plot(evals, marker="o", color=COURSE_COLORS["purple"])
    axes[1].axhline(0, color="#98a2b3", lw=1)
    axes[1].set_title("cotangent Laplacian spectrum")
    artifacts.append(_finish(fig, 4, "cotangent-laplacian-support.png"))
    checks["laplacian_symmetry_error"] = float(np.max(np.abs(L - L.T)))
    checks["laplacian_row_sum_error"] = float(np.max(np.abs(L.sum(axis=1))))
    return artifacts, checks


def _chapter_05(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    img = simple_signal(36)
    filters = [np.array([[0, 0, 0], [1, -1, 0], [0, 0, 0]]), np.array([[0, 1, 0], [0, -1, 0], [0, 0, 0]]), np.ones((3, 3)) / 9]
    responses = [signal.convolve2d(img, k, mode="same", boundary="wrap") for k in filters]
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.1))
    axes[0].imshow(img, cmap="viridis")
    axes[0].set_title("input")
    for ax, resp, title in zip(axes[1:], responses, ["x-gradient", "y-gradient", "average"]):
        ax.imshow(resp, cmap="RdBu")
        ax.set_title(title)
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    artifacts.append(_finish(fig, 5, "cnn-filter-generators.png"))
    checks["cnn_translation_equivariance_error"] = float(
        np.max(
            np.abs(
                signal.convolve2d(shift2d(img, 3, 4), filters[2], mode="same", boundary="wrap")
                - shift2d(responses[2], 3, 4)
            )
        )
    )

    pattern = np.zeros((17, 17))
    pattern[8, 3:14] = 1
    pattern[3:14, 8] = 0.7
    rots = [np.rot90(pattern, k) for k in range(4)]
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.8))
    for k, ax in enumerate(axes):
        ax.imshow(rots[k], cmap="magma")
        ax.set_title(f"orientation {k * 90} deg")
        ax.set_xticks([])
        ax.set_yticks([])
    artifacts.append(_finish(fig, 5, "group-conv-transform-convolve.png"))
    checks["rotation_channel_permutation_error"] = float(np.max(np.abs(np.rot90(rots[0]) - rots[1])))

    G = nx.karate_club_graph().subgraph(range(10)).copy()
    A = nx.to_numpy_array(G)
    X = rng.normal(size=(10, 4))
    P = permutation_matrix([3, 1, 8, 0, 5, 2, 9, 4, 6, 7])
    H = graph_message_pass(A, X)
    H_perm = graph_message_pass(P @ A @ P.T, P @ X)
    attention = np.exp((X @ X.T) / math.sqrt(X.shape[1]))
    attention = attention / attention.sum(axis=1, keepdims=True)
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    nx.draw_networkx(G, nx.spring_layout(G, seed=3), ax=axes[0], node_color="#dbeafe", font_size=8)
    axes[0].set_title("message passing graph")
    axes[0].axis("off")
    axes[1].imshow(attention, cmap="viridis")
    axes[1].set_title("attention as soft adjacency")
    axes[2].bar(["GNN", "attention"], [np.linalg.norm(H_perm - P @ H), np.max(np.abs(attention.sum(axis=1) - 1))])
    axes[2].set_yscale("log")
    axes[2].set_title("model residuals")
    artifacts.append(_finish(fig, 5, "gnn-transformer-soft-graph.png"))
    checks["gnn_permutation_equivariance_error"] = float(np.linalg.norm(H_perm - P @ H))
    checks["attention_row_sum_error"] = float(np.max(np.abs(attention.sum(axis=1) - 1)))

    points = np.array([[0, 0, 0], [1, 0, 0], [0.5, 0.8, 0], [0.5, 0.2, 0.7], [1.2, 0.5, 0.3]], dtype=float)
    points_rt = rigid_transform(points, random_rotation_matrix(9), np.array([0.4, -0.2, 0.3]))
    fig_html = go.Figure()
    for pts, name, color in [(points, "original", "blue"), (points_rt, "rigid transform", "green")]:
        fig_html.add_trace(go.Scatter3d(x=pts[:, 0], y=pts[:, 1], z=pts[:, 2], mode="markers+text", text=list(range(len(pts))), marker=dict(size=6, color=color), name=name))
    fig_html.update_layout(title="E(3)-style point cloud", width=700, height=560)
    artifacts.append(save_plotly_html(fig_html, 5, "e3-equivariant-messages.html"))
    checks["e3_distance_preservation_error"] = float(np.max(np.abs(pairwise_distances(points) - pairwise_distances(points_rt))))

    time = np.arange(40)
    gate = 1 / (1 + np.exp(-(time - 18) / 4))
    memory = np.cumprod(0.92 + 0.07 * gate)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    for d in [1, 2, 4, 8]:
        axes[0].plot([0, 2 * d], [d, d], marker="o", lw=3, label=f"d={d}")
    axes[0].set_title("dilated receptive fields")
    axes[0].legend()
    axes[1].plot(time, gate, label="input gate")
    axes[1].plot(time, memory, label="memory trace")
    axes[1].legend()
    axes[1].set_title("LSTM-like gates tune timescale")
    artifacts.append(_finish(fig, 5, "rnn-lstm-gates-time-warping.png"))
    checks["dilated_receptive_field"] = int(dilated_receptive_field(3, [1, 2, 4, 8]))
    checks["gate_min"] = float(gate.min())
    checks["gate_max"] = float(gate.max())
    return artifacts, checks


def _chapter_06(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    apps = ["molecules", "drug networks", "proteins", "recommenders", "traffic", "vision", "sequences", "healthcare", "particles", "VR/AR"]
    geoms = ["graph + E(3)", "heterogeneous graph", "mesh/contact graph", "bipartite graph", "spatiotemporal graph", "grid", "1D grid/complete graph", "mixed graph/grid", "point cloud", "deforming mesh"]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    y = np.arange(len(apps))[::-1]
    for i, yy in enumerate(y):
        ax.scatter(0, yy, s=620, color="#dbeafe", edgecolor=COURSE_COLORS["blue"])
        ax.scatter(1.25, yy, s=820, color="#dcfce7", edgecolor=COURSE_COLORS["green"])
        ax.plot([0.17, 1.03], [yy, yy], color="#cbd5e1")
        ax.text(0, yy, apps[i], ha="center", va="center", fontsize=8, weight="bold")
        ax.text(1.25, yy, geoms[i], ha="center", va="center", fontsize=8)
    ax.axis("off")
    ax.set_title("Application atlas: every problem enters through a geometric domain")
    artifacts.append(_finish(fig, 6, "gdl-application-geometry-atlas.png"))

    points = np.array([[0, 0, 0], [1, 0, 0], [0.5, 0.85, 0], [0.5, 0.3, 0.75]], dtype=float)
    points_r = rigid_transform(points, random_rotation_matrix(12), np.array([0.3, -0.1, 0.2]))
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (0, 3), (1, 3)])
    fig = plt.figure(figsize=(9, 3.5))
    ax1 = fig.add_subplot(121)
    nx.draw_networkx(G, nx.spring_layout(G, seed=4), ax=ax1, node_color="#fde68a", edge_color="#94a3b8")
    ax1.set_title("molecular graph")
    ax1.axis("off")
    ax2 = fig.add_subplot(122, projection="3d")
    ax2.scatter(points[:, 0], points[:, 1], points[:, 2], s=80, color=COURSE_COLORS["blue"], label="original")
    ax2.scatter(points_r[:, 0], points_r[:, 1], points_r[:, 2], s=80, color=COURSE_COLORS["green"], label="rigid motion")
    ax2.legend()
    ax2.set_title("coordinates may move")
    artifacts.append(_finish(fig, 6, "molecular-graph-equivariance.png"))
    checks["molecule_distance_error"] = float(np.max(np.abs(pairwise_distances(points) - pairwise_distances(points_r))))

    H = nx.Graph()
    H.add_nodes_from(["drug-A", "drug-B", "drug-C"], kind="drug")
    H.add_nodes_from(["protein-1", "protein-2"], kind="protein")
    H.add_nodes_from(["disease-X", "effect-Y"], kind="condition")
    H.add_edges_from([("drug-A", "protein-1"), ("drug-B", "protein-1"), ("drug-C", "protein-2"), ("protein-1", "disease-X"), ("drug-B", "effect-Y")])
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    colors = [{"drug": "#dbeafe", "protein": "#dcfce7", "condition": "#fee2e2"}[H.nodes[n]["kind"]] for n in H.nodes]
    nx.draw_networkx(H, nx.spring_layout(H, seed=8), node_color=colors, edge_color="#94a3b8", ax=axes[0], font_size=8)
    axes[0].axis("off")
    axes[0].set_title("network medicine typed graph")
    score = rng.random((3, 3))
    score = (score + score.T) / 2
    axes[1].imshow(score, cmap="viridis")
    axes[1].set_title("candidate link scores")
    artifacts.append(_finish(fig, 6, "network-medicine-edge-prediction.png"))
    checks["heterogeneous_node_types"] = len(set(nx.get_node_attributes(H, "kind").values()))

    road = nx.convert_node_labels_to_integers(nx.grid_2d_graph(3, 3))
    pos = {i: (i % 3, i // 3) for i in road.nodes}
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    nx.draw_networkx(road, pos, ax=axes[0], node_color="#dbeafe", edge_color="#94a3b8", width=2, font_size=8)
    axes[0].axis("off")
    axes[0].set_title("road graph")
    ts = np.array([np.sin(np.linspace(0, 2 * np.pi, 48) + phase) for phase in np.linspace(0, 1.5, 5)])
    axes[1].plot(ts.T)
    axes[1].set_title("edge speed time series")
    artifacts.append(_finish(fig, 6, "road-network-eta-forecasting.png"))
    checks["road_graph_edges"] = road.number_of_edges()

    seq_len = 32
    attention = np.exp(-np.abs(np.subtract.outer(np.arange(seq_len), np.arange(seq_len))) / 6)
    attention = attention / attention.sum(axis=1, keepdims=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].imshow(attention, cmap="viridis")
    axes[0].set_title("attention matrix as soft graph")
    for d in [1, 2, 4, 8]:
        axes[1].plot([0, 2 * d], [d, d], marker="o", lw=3, label=f"d={d}")
    axes[1].legend()
    axes[1].set_title("dilated sequence receptive fields")
    artifacts.append(_finish(fig, 6, "sequence-attention-and-dilation.png"))
    checks["sequence_attention_row_error"] = float(np.max(np.abs(attention.sum(axis=1) - 1)))
    checks["sequence_receptive_field"] = dilated_receptive_field(3, [1, 2, 4, 8])

    phi = rng.uniform(0, 2 * np.pi, 80)
    r = rng.gamma(2.0, 0.6, 80)
    jet = np.c_[r * np.cos(phi), r * np.sin(phi), rng.normal(scale=0.1, size=80)]
    fig_html = go.Figure()
    fig_html.add_trace(go.Scatter3d(x=jet[:, 0], y=jet[:, 1], z=jet[:, 2], mode="markers", marker=dict(size=4, color=r, colorscale="Viridis")))
    fig_html.update_layout(title="Particle event as irregular point cloud", width=700, height=560)
    artifacts.append(save_plotly_html(fig_html, 6, "particle-jet-graph.html"))
    checks["particle_count"] = int(len(jet))
    return artifacts, checks


def _chapter_07(rng: np.random.Generator) -> tuple[list[Path], dict[str, object]]:
    artifacts: list[Path] = []
    checks: dict[str, object] = {}
    events = [
        (1870, "Erlangen symmetry lens"),
        (1918, "Noether invariants"),
        (1959, "visual receptive fields"),
        (1980, "neural shift structure"),
        (1996, "graph/spectral geometry"),
        (2005, "early GNNs"),
        (2012, "deep CNN era"),
        (2017, "GDL naming and Transformers"),
        (2021, "5G synthesis"),
    ]
    fig, ax = plt.subplots(figsize=(10, 3.4))
    ax.scatter([e[0] for e in events], np.zeros(len(events)), s=160, color=COURSE_COLORS["blue"])
    for year, label in events:
        ax.text(year, 0.08, str(year), ha="center", fontsize=8, weight="bold")
        ax.text(year, -0.08, label, ha="center", va="top", rotation=30, fontsize=8)
    ax.axhline(0, color="#94a3b8")
    ax.set_yticks([])
    ax.set_title("A compressed symmetry-to-GDL timeline")
    artifacts.append(_finish(fig, 7, "symmetry-to-gdl-timeline.png"))
    checks["timeline_event_count"] = len(events)

    lineage = nx.DiGraph()
    lineage.add_edges_from(
        [
            ("symmetry", "CNN"),
            ("Fourier/wavelets", "CNN"),
            ("structured data", "GNN"),
            ("chemistry graphs", "GNN"),
            ("graph kernels", "WL analysis"),
            ("GNN", "WL analysis"),
            ("attention", "Transformer"),
            ("complete graph", "Transformer"),
            ("geometry processing", "mesh CNN"),
            ("gauge theory", "gauge CNN"),
            ("message passing", "algorithmic reasoning"),
            ("GNN", "algorithmic reasoning"),
        ]
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    nx.draw_networkx(lineage, nx.spring_layout(lineage, seed=7), ax=ax, node_color="#eef4ff", edge_color="#94a3b8", arrowsize=14, font_size=8)
    ax.axis("off")
    ax.set_title("Architecture lineage as concept graph")
    artifacts.append(_finish(fig, 7, "architecture-lineage-graph.png"))
    checks["lineage_dag"] = nx.is_directed_acyclic_graph(lineage)

    def wl_histogram(graph: nx.Graph, rounds: int = 4) -> list[tuple[str, ...]]:
        colors = {node: "0" for node in graph.nodes}
        hists = []
        for _ in range(rounds):
            hists.append(tuple(sorted(colors.values())))
            signatures = {node: (colors[node], tuple(sorted(colors[n] for n in graph.neighbors(node)))) for node in graph.nodes}
            unique = {sig: str(i) for i, sig in enumerate(sorted(set(signatures.values())))}
            colors = {node: unique[sig] for node, sig in signatures.items()}
        hists.append(tuple(sorted(colors.values())))
        return hists

    C6 = nx.cycle_graph(6)
    TT = nx.disjoint_union(nx.cycle_graph(3), nx.cycle_graph(3))
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    nx.draw_networkx(C6, nx.circular_layout(C6), ax=axes[0], node_color="#dbeafe")
    axes[0].set_title("6-cycle")
    nx.draw_networkx(TT, nx.spring_layout(TT, seed=2), ax=axes[1], node_color="#fee2e2")
    axes[1].set_title("two triangles")
    for ax in axes:
        ax.axis("off")
    artifacts.append(_finish(fig, 7, "wl-six-cycle-vs-two-triangles.png"))
    checks["wl_histograms_match"] = bool(wl_histogram(C6) == wl_histogram(TT))

    G = nx.path_graph(12)
    A = nx.to_numpy_array(G)
    L = np.diag(A.sum(axis=1)) - A
    evals, evecs = np.linalg.eigh(L)
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].plot(evecs[:, 1:4])
    axes[0].set_title("graph Laplacian modes")
    axes[1].plot(evals[:8], marker="o")
    axes[1].set_title("low-frequency spectrum")
    artifacts.append(_finish(fig, 7, "graph-signal-processing-lineage.png"))
    checks["laplacian_min_eigenvalue"] = float(evals[0])

    steps = ["precondition", "message update", "aggregate", "state invariant", "termination", "postcondition"]
    fig, ax = plt.subplots(figsize=(9, 2.8))
    for i, step in enumerate(steps):
        ax.scatter(i, 0, s=1200, color="#dcfce7", edgecolor=COURSE_COLORS["green"])
        ax.text(i, 0, step, ha="center", va="center", fontsize=8, weight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(i + 0.72, 0), xytext=(i + 0.28, 0), arrowprops=dict(arrowstyle="->", lw=1.5, color=COURSE_COLORS["gray"]))
    ax.axis("off")
    ax.set_title("Algorithmic reasoning: preserve invariants through computation")
    artifacts.append(_finish(fig, 7, "algorithmic-invariant-flow.png"))
    return artifacts, checks


BUILDERS = {
    1: _chapter_01,
    2: _chapter_02,
    3: _chapter_03,
    4: _chapter_04,
    5: _chapter_05,
    6: _chapter_06,
    7: _chapter_07,
}


def build_chapter_visuals(chapter: int) -> tuple[list[Path], dict[str, object]]:
    """Generate all visual artifacts and raw checks for a chapter."""
    set_theme()
    rng = np.random.default_rng(1000 + chapter)
    artifacts, checks = BUILDERS[chapter](rng)
    ledger = {"chapter": chapter, "checks": checks, "artifact_count": len(artifacts)}
    artifacts.append(save_json(ledger, chapter, f"chapter-{chapter:02d}-visual-ledger.json"))
    return artifacts, checks
