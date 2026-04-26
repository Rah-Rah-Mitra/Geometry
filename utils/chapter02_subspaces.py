"""Coordinate and plotting helpers for Chapter 2 oriented subspaces.

The chapter is intentionally nonmetric in its algebraic story, but notebook
visualizations need coordinates. These helpers keep that coordinate work small
and explicit so the notebook can focus on the outer product, orientation, and
grade bookkeeping.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.patches import Polygon

EPS = 1e-10

COLORS = {
    "line": "#1f77b4",
    "line_alt": "#ff7f0e",
    "bivector_pos": "#2ca02c",
    "bivector_neg": "#d62728",
    "volume": "#9467bd",
    "front": "#2374ab",
    "back": "#d1495b",
    "neutral": "#444444",
    "surface": "rgba(35, 116, 171, 0.35)",
    "volume_rgba": "rgba(148, 103, 189, 0.18)",
}


@dataclass(frozen=True)
class Bivector3D:
    """A 3-D bivector in the ordered basis (e12, e23, e31)."""

    e12: float
    e23: float
    e31: float

    @property
    def coordinates(self) -> np.ndarray:
        return np.array([self.e12, self.e23, self.e31], dtype=float)

    @property
    def normal_coordinates(self) -> np.ndarray:
        """Return the Euclidean dual normal coordinates for drawing only."""

        return np.array([self.e23, self.e31, self.e12], dtype=float)

    @property
    def weight(self) -> float:
        return float(np.linalg.norm(self.normal_coordinates))


def as_vector(value: np.ndarray | list[float] | tuple[float, ...], dim: int | None = None) -> np.ndarray:
    vector = np.asarray(value, dtype=float)
    if vector.ndim != 1:
        raise ValueError(f"expected a vector, got shape {vector.shape}")
    if dim is not None and vector.shape != (dim,):
        raise ValueError(f"expected a {dim}-vector, got shape {vector.shape}")
    return vector


def normalize(value: np.ndarray, *, eps: float = EPS) -> np.ndarray:
    vector = as_vector(value)
    length = np.linalg.norm(vector)
    if length < eps:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def wedge2(a: np.ndarray, b: np.ndarray) -> float:
    """Return the e12 coefficient of the 2-D outer product a wedge b."""

    a = as_vector(a, 2)
    b = as_vector(b, 2)
    return float(a[0] * b[1] - a[1] * b[0])


def wedge3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Return the e123 coefficient of the 3-D outer product a wedge b wedge c."""

    return float(np.linalg.det(np.column_stack([as_vector(a, 3), as_vector(b, 3), as_vector(c, 3)])))


def wedge_vector_vector_3d(a: np.ndarray, b: np.ndarray) -> Bivector3D:
    """Return a wedge b in the basis (e12, e23, e31)."""

    a = as_vector(a, 3)
    b = as_vector(b, 3)
    return Bivector3D(
        e12=float(a[0] * b[1] - a[1] * b[0]),
        e23=float(a[1] * b[2] - a[2] * b[1]),
        e31=float(a[2] * b[0] - a[0] * b[2]),
    )


def solve_in_basis_2d(x: np.ndarray, a: np.ndarray, b: np.ndarray) -> dict[str, np.ndarray | float]:
    """Decompose x = alpha a + beta b using ratios of oriented areas."""

    x = as_vector(x, 2)
    a = as_vector(a, 2)
    b = as_vector(b, 2)
    denominator = wedge2(a, b)
    if abs(denominator) < EPS:
        raise ValueError("a and b do not span a stable 2-D basis")

    alpha = wedge2(x, b) / denominator
    beta = wedge2(x, a) / wedge2(b, a)
    reconstructed = alpha * a + beta * b
    return {"alpha": float(alpha), "beta": float(beta), "reconstructed": reconstructed}


def intersect_lines_2d(
    p: np.ndarray,
    u: np.ndarray,
    q: np.ndarray,
    v: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """Intersect p + s u with q + t v by the Chapter 2 bivector-ratio formula."""

    p = as_vector(p, 2)
    u = as_vector(u, 2)
    q = as_vector(q, 2)
    v = as_vector(v, 2)
    denominator = wedge2(u, v)
    if abs(denominator) < EPS:
        raise ValueError("parallel or nearly parallel lines do not have a stable finite intersection")

    u_coeff = wedge2(q, v) / denominator
    v_coeff = wedge2(p, u) / wedge2(v, u)
    point = u_coeff * u + v_coeff * v
    return {"point": point, "u_coeff": float(u_coeff), "v_coeff": float(v_coeff)}


def triangle_orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    """Signed projected triangle area, positive for counterclockwise vertex order."""

    a = as_vector(a, 2)
    b = as_vector(b, 2)
    c = as_vector(c, 2)
    return wedge2(b - a, c - a) / 2.0


def face_orientations(vertices2d: np.ndarray, faces: np.ndarray) -> np.ndarray:
    vertices2d = np.asarray(vertices2d, dtype=float)
    faces = np.asarray(faces, dtype=int)
    return np.array([triangle_orientation(vertices2d[i], vertices2d[j], vertices2d[k]) for i, j, k in faces])


def front_face_mask(vertices2d: np.ndarray, faces: np.ndarray) -> np.ndarray:
    return face_orientations(vertices2d, faces) > 0.0


def line_points(point: np.ndarray, direction: np.ndarray, span: float = 3.0, n: int = 80) -> np.ndarray:
    point = as_vector(point, 2)
    direction = normalize(as_vector(direction, 2))
    t = np.linspace(-span, span, n)
    return point + t[:, None] * direction


def parallelogram_vertices_2d(a: np.ndarray, b: np.ndarray, origin: np.ndarray | None = None) -> np.ndarray:
    a = as_vector(a, 2)
    b = as_vector(b, 2)
    origin = np.zeros(2) if origin is None else as_vector(origin, 2)
    return np.vstack([origin, origin + a, origin + a + b, origin + b])


def parallelogram_vertices_3d(a: np.ndarray, b: np.ndarray, origin: np.ndarray | None = None) -> np.ndarray:
    a = as_vector(a, 3)
    b = as_vector(b, 3)
    origin = np.zeros(3) if origin is None else as_vector(origin, 3)
    return np.vstack([origin, origin + a, origin + a + b, origin + b])


def parallelepiped_vertices(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    a = as_vector(a, 3)
    b = as_vector(b, 3)
    c = as_vector(c, 3)
    return np.array(
        [
            [0.0, 0.0, 0.0],
            a,
            b,
            a + b,
            c,
            a + c,
            b + c,
            a + b + c,
        ]
    )


def basis_blade_counts(max_dimension: int = 5) -> list[list[int]]:
    return [[comb(n, k) for k in range(n + 1)] for n in range(max_dimension + 1)]


def vector_trace_3d(vector: np.ndarray, name: str, color: str, origin: np.ndarray | None = None) -> go.Scatter3d:
    vector = as_vector(vector, 3)
    origin = np.zeros(3) if origin is None else as_vector(origin, 3)
    tip = origin + vector
    return go.Scatter3d(
        x=[origin[0], tip[0]],
        y=[origin[1], tip[1]],
        z=[origin[2], tip[2]],
        mode="lines+markers",
        name=name,
        line={"color": color, "width": 7},
        marker={"size": [2, 5], "color": color},
    )


def parallelogram_mesh_3d(
    a: np.ndarray,
    b: np.ndarray,
    name: str,
    color: str,
    opacity: float = 0.45,
) -> go.Mesh3d:
    vertices = parallelogram_vertices_3d(a, b)
    return go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color=color,
        opacity=opacity,
        name=name,
        hoverinfo="name",
        showscale=False,
    )


def parallelepiped_mesh_3d(
    a: np.ndarray,
    b: np.ndarray,
    c: np.ndarray,
    name: str = "a wedge b wedge c",
) -> go.Mesh3d:
    vertices = parallelepiped_vertices(a, b, c)
    faces = np.array(
        [
            [0, 1, 3],
            [0, 3, 2],
            [4, 6, 7],
            [4, 7, 5],
            [0, 4, 5],
            [0, 5, 1],
            [2, 3, 7],
            [2, 7, 6],
            [0, 2, 6],
            [0, 6, 4],
            [1, 5, 7],
            [1, 7, 3],
        ]
    )
    return go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=faces[:, 0],
        j=faces[:, 1],
        k=faces[:, 2],
        color=COLORS["volume"],
        opacity=0.16,
        name=name,
        hoverinfo="name",
        showscale=False,
    )


def finish_scene(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        width=980,
        height=720,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        scene={
            "aspectmode": "data",
            "xaxis_title": "e1",
            "yaxis_title": "e2",
            "zaxis_title": "e3",
            "camera": {"eye": {"x": 1.6, "y": -1.8, "z": 1.25}},
        },
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.72)"},
    )
    return fig


def subspace_scene(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> go.Figure:
    """Draw vectors, their bivector, and their trivector in one Plotly scene."""

    fig = go.Figure()
    fig.add_trace(vector_trace_3d(a, "a", COLORS["line"]))
    fig.add_trace(vector_trace_3d(b, "b", COLORS["line_alt"]))
    fig.add_trace(vector_trace_3d(c, "c", COLORS["neutral"]))
    fig.add_trace(parallelogram_mesh_3d(a, b, "a wedge b", COLORS["bivector_pos"]))
    fig.add_trace(parallelepiped_mesh_3d(a, b, c))
    volume = wedge3(a, b, c)
    bivector = wedge_vector_vector_3d(a, b)
    title = (
        "Oriented line, bivector, and trivector "
        f"(B=[{bivector.e12:.2f}, {bivector.e23:.2f}, {bivector.e31:.2f}], "
        f"T={volume:.2f})"
    )
    return finish_scene(fig, title)


def bivector_grid_figure(rows: int = 4, cols: int = 6) -> plt.Figure:
    """Render a small lab grid of e1 wedge v(theta) as parallelograms."""

    fig, ax = plt.subplots(figsize=(11, 7))
    angles = np.linspace(0, 2 * np.pi, rows * cols, endpoint=False)
    e1 = np.array([0.78, 0.0])
    for idx, theta in enumerate(angles):
        row, col = divmod(idx, cols)
        center = np.array([col * 2.25, -row * 2.0])
        v = 0.78 * np.array([np.cos(theta), np.sin(theta)])
        verts = parallelogram_vertices_2d(e1, v, center)
        area = wedge2(e1, v)
        color = COLORS["bivector_pos"] if area >= 0 else COLORS["bivector_neg"]
        alpha = min(0.75, 0.22 + 0.75 * abs(area) / 0.61)
        ax.add_patch(Polygon(verts, closed=True, facecolor=color, edgecolor=color, alpha=alpha))
        ax.arrow(center[0], center[1], e1[0], e1[1], width=0.015, color=COLORS["line"], length_includes_head=True)
        ax.arrow(center[0], center[1], v[0], v[1], width=0.015, color=COLORS["line_alt"], length_includes_head=True)
        ax.text(center[0] + 0.12, center[1] - 0.86, f"{area:+.2f}", fontsize=9)

    ax.set_title("Bivector drawing lab: sign and weight of e1 wedge v(theta)")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.margins(0.08)
    return fig


def line_intersection_figure(
    p: np.ndarray,
    u: np.ndarray,
    q: np.ndarray,
    v: np.ndarray,
) -> tuple[plt.Figure, dict[str, np.ndarray | float]]:
    result = intersect_lines_2d(p, u, q, v)
    x = result["point"]
    fig, ax = plt.subplots(figsize=(8, 7))
    for point, direction, color, label in [
        (p, u, COLORS["line"], "L = p + s u"),
        (q, v, COLORS["line_alt"], "M = q + t v"),
    ]:
        pts = line_points(point, direction, span=2.6)
        ax.plot(pts[:, 0], pts[:, 1], color=color, lw=2.6, label=label)
        ax.arrow(
            point[0],
            point[1],
            normalize(direction)[0] * 0.65,
            normalize(direction)[1] * 0.65,
            color=color,
            width=0.015,
            length_includes_head=True,
        )
    ax.scatter([p[0], q[0], x[0]], [p[1], q[1], x[1]], c=[COLORS["line"], COLORS["line_alt"], "black"], s=[70, 70, 90])
    ax.text(p[0] + 0.06, p[1] + 0.06, "p")
    ax.text(q[0] + 0.06, q[1] + 0.06, "q")
    ax.text(x[0] + 0.06, x[1] + 0.06, "x")
    ax.axhline(0, color="#cccccc", lw=0.8)
    ax.axvline(0, color="#cccccc", lw=0.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Line intersection from bivector ratios")
    ax.legend(loc="upper left")
    ax.grid(True, color="#eeeeee")
    return fig, result


def pascal_ladder_figure(max_dimension: int = 5) -> plt.Figure:
    counts = basis_blade_counts(max_dimension)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    for n, row in enumerate(counts):
        y = max_dimension - n
        x0 = -0.62 * n
        for k, value in enumerate(row):
            ax.text(x0 + 1.24 * k, y, str(value), ha="center", va="center", fontsize=13)
    ax.text(0, max_dimension + 0.75, "Number of basis k-blades in n dimensions", ha="center", fontsize=14)
    ax.text(-1.1, max_dimension + 0.25, "n", ha="center", fontsize=10)
    ax.text(1.1, max_dimension + 0.25, "grade k", ha="center", fontsize=10)
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-0.8, max_dimension + 1.2)
    return fig


def rotation_matrix_xyz(angles: tuple[float, float, float]) -> np.ndarray:
    ax, ay, az = angles
    cx, sx = np.cos(ax), np.sin(ax)
    cy, sy = np.cos(ay), np.sin(ay)
    cz, sz = np.cos(az), np.sin(az)
    rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return rz @ ry @ rx


def torus_mesh(
    major_count: int = 14,
    minor_count: int = 7,
    major_radius: float = 2.0,
    minor_radius: float = 0.62,
) -> tuple[np.ndarray, np.ndarray]:
    vertices: list[list[float]] = []
    for i in range(major_count):
        u = 2 * np.pi * i / major_count
        for j in range(minor_count):
            v = 2 * np.pi * j / minor_count
            radius = major_radius + minor_radius * np.cos(v)
            vertices.append([radius * np.cos(u), radius * np.sin(u), minor_radius * np.sin(v)])

    def index(i: int, j: int) -> int:
        return (i % major_count) * minor_count + (j % minor_count)

    faces: list[list[int]] = []
    for i in range(major_count):
        for j in range(minor_count):
            a = index(i, j)
            b = index(i + 1, j)
            c = index(i + 1, j + 1)
            d = index(i, j + 1)
            faces.append([a, b, c])
            faces.append([a, c, d])
    return np.asarray(vertices, dtype=float), np.asarray(faces, dtype=int)


def project_vertices(
    vertices3d: np.ndarray,
    angles: tuple[float, float, float] = (0.85, -0.35, 0.22),
) -> tuple[np.ndarray, np.ndarray]:
    rotated = np.asarray(vertices3d, dtype=float) @ rotation_matrix_xyz(angles).T
    return rotated[:, :2], rotated[:, 2]


def backface_culling_figure(vertices2d: np.ndarray, faces: np.ndarray) -> go.Figure:
    """Create a Plotly lab with buttons for all/front/back projected faces."""

    vertices2d = np.asarray(vertices2d, dtype=float)
    faces = np.asarray(faces, dtype=int)
    front = front_face_mask(vertices2d, faces)
    fig = go.Figure()
    visibility_all: list[bool] = []
    visibility_front: list[bool] = []
    visibility_back: list[bool] = []

    for idx, (face, is_front) in enumerate(zip(faces, front, strict=True)):
        polygon = vertices2d[np.r_[face, face[0]]]
        color = COLORS["front"] if is_front else COLORS["back"]
        name = "front-facing" if is_front else "back-facing"
        fig.add_trace(
            go.Scatter(
                x=polygon[:, 0],
                y=polygon[:, 1],
                mode="lines",
                fill="toself",
                fillcolor=color,
                opacity=0.34 if is_front else 0.20,
                line={"color": color, "width": 1},
                name=name,
                legendgroup=name,
                showlegend=idx == int(np.argmax(front)) if is_front else idx == int(np.argmax(~front)),
                hovertemplate=f"face {idx}<br>{name}<extra></extra>",
            )
        )
        visibility_all.append(True)
        visibility_front.append(bool(is_front))
        visibility_back.append(not bool(is_front))

    fig.update_layout(
        title="Backface culling lab: projected triangle orientation",
        width=900,
        height=760,
        xaxis={"scaleanchor": "y", "title": "projected e1"},
        yaxis={"title": "projected e2"},
        margin={"l": 20, "r": 20, "t": 70, "b": 20},
        updatemenus=[
            {
                "type": "buttons",
                "direction": "right",
                "x": 0.01,
                "y": 1.08,
                "buttons": [
                    {"label": "all", "method": "update", "args": [{"visible": visibility_all}]},
                    {"label": "front only", "method": "update", "args": [{"visible": visibility_front}]},
                    {"label": "back only", "method": "update", "args": [{"visible": visibility_back}]},
                ],
            }
        ],
    )
    return fig


def cube_surface_mesh(
    center: np.ndarray = np.zeros(3),
    half_width: float = 1.0,
    grid: int = 5,
) -> tuple[np.ndarray, np.ndarray]:
    """Triangulate a cube surface with outward-oriented triangles."""

    if grid < 1:
        raise ValueError("grid must be at least 1")
    center = as_vector(center, 3)
    coords = np.linspace(-half_width, half_width, grid + 1)
    points: list[np.ndarray] = []
    faces: list[list[int]] = []

    for fixed_axis in range(3):
        free_axes = [axis for axis in range(3) if axis != fixed_axis]
        for sign in (-1.0, 1.0):
            face_indices = np.empty((grid + 1, grid + 1), dtype=int)
            for i, u in enumerate(coords):
                for j, v in enumerate(coords):
                    point = center.copy()
                    point[fixed_axis] += sign * half_width
                    point[free_axes[0]] += u
                    point[free_axes[1]] += v
                    face_indices[i, j] = len(points)
                    points.append(point)
            normal = np.zeros(3)
            normal[fixed_axis] = sign
            for i in range(grid):
                for j in range(grid):
                    for tri in [
                        [face_indices[i, j], face_indices[i + 1, j], face_indices[i + 1, j + 1]],
                        [face_indices[i, j], face_indices[i + 1, j + 1], face_indices[i, j + 1]],
                    ]:
                        tri_points = [points[index] for index in tri]
                        tri_normal = np.cross(tri_points[1] - tri_points[0], tri_points[2] - tri_points[0])
                        if np.dot(tri_normal, normal) < 0:
                            tri[1], tri[2] = tri[2], tri[1]
                        faces.append(tri)

    return np.asarray(points, dtype=float), np.asarray(faces, dtype=int)


def radial_field(point: np.ndarray, singularity: np.ndarray = np.zeros(3), scales: np.ndarray | None = None) -> np.ndarray:
    point = as_vector(point, 3)
    singularity = as_vector(singularity, 3)
    scales = np.ones(3) if scales is None else as_vector(scales, 3)
    return scales * (point - singularity)


def helix_gradient_field(point: np.ndarray) -> np.ndarray:
    """Gradient field with a helical zero set x=cos(z), y=sin(z)."""

    x, y, z = as_vector(point, 3)
    dx = x - np.cos(z)
    dy = y - np.sin(z)
    return np.array([2.0 * dx, 2.0 * dy, 2.0 * (dx * np.sin(z) - dy * np.cos(z))])


def singularity_score(
    field: Callable[[np.ndarray], np.ndarray],
    center: np.ndarray,
    half_width: float = 0.75,
    grid: int = 5,
) -> float:
    """Approximate the mapped-sphere volume test for a vector-field singularity."""

    points, faces = cube_surface_mesh(center=center, half_width=half_width, grid=grid)
    values = np.array([as_vector(field(point), 3) for point in points])
    norms = np.linalg.norm(values, axis=1)
    if np.any(norms < EPS):
        return float("nan")
    unit = values / norms[:, None]
    volume = 0.0
    for i, j, k in faces:
        volume += wedge3(unit[i], unit[j], unit[k]) / 6.0
    sphere_volume = 4.0 * np.pi / 3.0
    return float(volume / sphere_volume)


def scan_singularity_scores(
    field: Callable[[np.ndarray], np.ndarray],
    centers: np.ndarray,
    half_width: float = 0.55,
    grid: int = 4,
) -> np.ndarray:
    centers = np.asarray(centers, dtype=float)
    return np.array([singularity_score(field, center, half_width=half_width, grid=grid) for center in centers])


def helix_points(z_min: float = -2.5, z_max: float = 2.5, n: int = 180) -> np.ndarray:
    z = np.linspace(z_min, z_max, n)
    return np.column_stack([np.cos(z), np.sin(z), z])


def singularity_scan_figure(centers: np.ndarray, scores: np.ndarray) -> go.Figure:
    centers = np.asarray(centers, dtype=float)
    scores = np.asarray(scores, dtype=float)
    helix = helix_points(float(np.min(centers[:, 2]) - 0.5), float(np.max(centers[:, 2]) + 0.5))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=helix[:, 0],
            y=helix[:, 1],
            z=helix[:, 2],
            mode="lines",
            name="zero set of helix field",
            line={"color": "black", "width": 5},
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=centers[:, 0],
            y=centers[:, 1],
            z=centers[:, 2],
            mode="markers",
            name="sample cube centers",
            marker={
                "size": 6 + 18 * np.nan_to_num(np.abs(scores), nan=0.0),
                "color": np.nan_to_num(np.abs(scores), nan=0.0),
                "colorscale": "Viridis",
                "cmin": 0,
                "cmax": 1,
                "colorbar": {"title": "|score|"},
                "opacity": 0.82,
            },
            text=[f"score={score:+.3f}" for score in scores],
            hovertemplate="%{text}<extra></extra>",
        )
    )
    return finish_scene(fig, "Singularity lab: trivector volume score around a helix")


def chapter_invariant_report() -> dict[str, float | bool]:
    a = np.array([1.3, -0.4])
    b = np.array([0.2, 1.1])
    x = np.array([0.7, 0.9])
    solved = solve_in_basis_2d(x, a, b)
    p = np.array([1.0, 0.0])
    u = np.array([0.0, 1.0])
    q = np.array([0.0, 1.0])
    v = np.array([1.0, 1.0])
    intersection = intersect_lines_2d(p, u, q, v)["point"]
    radial_inside = singularity_score(lambda point: radial_field(point), np.array([0.0, 0.0, 0.0]), grid=5)
    radial_outside = singularity_score(lambda point: radial_field(point), np.array([2.2, 0.0, 0.0]), grid=5)
    return {
        "wedge2_antisymmetry": abs(wedge2(a, b) + wedge2(b, a)) < 1e-12,
        "wedge2_self_zero": abs(wedge2(a, a)) < 1e-12,
        "basis_reconstruction_error": float(np.linalg.norm(solved["reconstructed"] - x)),
        "line_intersection_error": float(np.linalg.norm(intersection - np.array([1.0, 2.0]))),
        "radial_singularity_center_score": float(radial_inside),
        "radial_empty_cube_score": float(radial_outside),
    }
