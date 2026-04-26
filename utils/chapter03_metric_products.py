"""Metric-product helpers for the Chapter 3 notebook."""

from __future__ import annotations

from math import acos, sqrt
from typing import Iterable

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

EPS = 1e-10

COLORS = {
    "blue": "#2f6fbb",
    "green": "#2f9d67",
    "red": "#c94c4c",
    "gold": "#d99a20",
    "purple": "#7b5ab6",
    "gray": "#586069",
    "plane": "rgba(47, 111, 187, 0.20)",
    "plane_grid": "rgba(47, 111, 187, 0.35)",
}


def as_vector(value: Iterable[float], dimension: int = 3) -> np.ndarray:
    """Return a real vector with the expected coordinate dimension."""
    vector = np.asarray(value, dtype=float)
    if vector.shape != (dimension,):
        raise ValueError(f"expected shape ({dimension},), got {vector.shape}")
    return vector


def as_frame(value: Iterable[Iterable[float]], dimension: int = 3) -> np.ndarray:
    """Return row-stacked spanning vectors."""
    frame = np.asarray(value, dtype=float)
    if frame.ndim != 2 or frame.shape[1] != dimension:
        raise ValueError(f"expected a row-stacked frame with {dimension} columns, got {frame.shape}")
    return frame


def metric_matrix(metric: Iterable[float] | np.ndarray | None = None, dimension: int = 3) -> np.ndarray:
    """Return a symmetric metric matrix from None, a diagonal, or a full matrix."""
    if metric is None:
        return np.eye(dimension)
    matrix = np.asarray(metric, dtype=float)
    if matrix.ndim == 1:
        if matrix.shape != (dimension,):
            raise ValueError(f"expected {dimension} diagonal entries, got {matrix.shape}")
        return np.diag(matrix)
    if matrix.shape != (dimension, dimension):
        raise ValueError(f"expected metric shape ({dimension}, {dimension}), got {matrix.shape}")
    if not np.allclose(matrix, matrix.T):
        raise ValueError("metric matrix must be symmetric")
    return matrix


def metric_dot(left: Iterable[float], right: Iterable[float], metric: Iterable[float] | np.ndarray | None = None) -> float:
    left_vector = as_vector(left)
    right_vector = as_vector(right)
    matrix = metric_matrix(metric)
    return float(left_vector @ matrix @ right_vector)


def vector_norm(vector: Iterable[float], metric: Iterable[float] | np.ndarray | None = None) -> float:
    return sqrt(abs(metric_dot(vector, vector, metric)))


def unit_vector(vector: Iterable[float], metric: Iterable[float] | np.ndarray | None = None) -> np.ndarray:
    vector = as_vector(vector)
    length = vector_norm(vector, metric)
    if length < EPS:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def vector_angle(
    left: Iterable[float],
    right: Iterable[float],
    metric: Iterable[float] | np.ndarray | None = None,
) -> float:
    denom = vector_norm(left, metric) * vector_norm(right, metric)
    if denom < EPS:
        raise ValueError("angle needs nonzero vectors")
    cosine = np.clip(metric_dot(left, right, metric) / denom, -1.0, 1.0)
    return float(acos(cosine))


def gram_matrix(factors: Iterable[Iterable[float]], metric: Iterable[float] | np.ndarray | None = None) -> np.ndarray:
    frame = as_frame(factors)
    matrix = metric_matrix(metric, frame.shape[1])
    return frame @ matrix @ frame.T


def scalar_product_star(
    left_factors: Iterable[Iterable[float]],
    right_factors: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> float:
    """Textbook star product convention for equal-grade blades from vector factors."""
    left = as_frame(left_factors)
    right = as_frame(right_factors, left.shape[1])
    if left.shape[0] != right.shape[0]:
        return 0.0
    matrix = metric_matrix(metric, left.shape[1])
    comparison = left @ matrix @ right[::-1].T
    return float(np.linalg.det(comparison))


def blade_metric_product(
    left_factors: Iterable[Iterable[float]],
    right_factors: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> float:
    """Reverse-adjusted scalar product used for norms and angle comparisons."""
    left = as_frame(left_factors)
    right = as_frame(right_factors, left.shape[1])
    return scalar_product_star(left, right[::-1], metric)


def blade_norm_squared(
    factors: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> float:
    return blade_metric_product(factors, factors, metric)


def blade_measure(factors: Iterable[Iterable[float]], metric: Iterable[float] | np.ndarray | None = None) -> float:
    return sqrt(abs(blade_norm_squared(factors, metric)))


def blade_cosine(
    left_factors: Iterable[Iterable[float]],
    right_factors: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> float:
    left_norm = blade_measure(left_factors, metric)
    right_norm = blade_measure(right_factors, metric)
    if left_norm < EPS or right_norm < EPS:
        raise ValueError("blade angle needs nonzero blades")
    cosine = blade_metric_product(left_factors, right_factors, metric) / (left_norm * right_norm)
    return float(np.clip(cosine, -1.0, 1.0))


def project_vector_to_span(
    vector: Iterable[float],
    basis: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Orthogonally project a vector onto the span of row-stacked basis vectors."""
    vector = as_vector(vector)
    basis = as_frame(basis)
    matrix = metric_matrix(metric, basis.shape[1])
    gram = basis @ matrix @ basis.T
    rhs = basis @ matrix @ vector
    coeffs = np.linalg.solve(gram, rhs)
    projection = coeffs @ basis
    residual = vector - projection
    return projection, residual, coeffs


def reciprocal_frame(
    frame: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> np.ndarray:
    """Return row-stacked reciprocal vectors r_i with f_j dot r_i = delta_ji."""
    frame = as_frame(frame)
    matrix = metric_matrix(metric, frame.shape[1])
    gram = frame @ matrix @ frame.T
    return np.linalg.solve(gram, frame)


def coordinates_in_frame(
    vector: Iterable[float],
    frame: Iterable[Iterable[float]],
    metric: Iterable[float] | np.ndarray | None = None,
) -> np.ndarray:
    vector = as_vector(vector)
    reciprocal = reciprocal_frame(frame, metric)
    matrix = metric_matrix(metric, vector.shape[0])
    return reciprocal @ matrix @ vector


def reconstruct_from_frame(coords: Iterable[float], frame: Iterable[Iterable[float]]) -> np.ndarray:
    coords = np.asarray(coords, dtype=float)
    frame = as_frame(frame)
    if coords.shape != (frame.shape[0],):
        raise ValueError(f"expected {frame.shape[0]} coordinates, got {coords.shape}")
    return coords @ frame


def cross_from_dual_wedge(left: Iterable[float], right: Iterable[float]) -> np.ndarray:
    """The 3-D cross product as the Euclidean dual of the oriented area blade."""
    return np.cross(as_vector(left), as_vector(right))


def arrow_trace(
    start: Iterable[float],
    end: Iterable[float],
    name: str,
    color: str,
    width: int = 7,
    dash: str | None = None,
    scene: str | None = None,
) -> go.Scatter3d:
    start = as_vector(start)
    end = as_vector(end)
    line = {"color": color, "width": width}
    if dash:
        line["dash"] = dash
    return go.Scatter3d(
        x=[start[0], end[0]],
        y=[start[1], end[1]],
        z=[start[2], end[2]],
        mode="lines+markers",
        name=name,
        line=line,
        marker={"size": [2, 5], "color": color},
        scene=scene,
    )


def plane_patch(
    basis: Iterable[Iterable[float]],
    center: Iterable[float] = (0.0, 0.0, 0.0),
    span: float = 1.4,
    samples: int = 17,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    basis = as_frame(basis)
    if basis.shape[0] != 2:
        raise ValueError("plane patch needs exactly two spanning vectors")
    center = as_vector(center)
    u = unit_vector(basis[0])
    v = basis[1] - np.dot(basis[1], u) * u
    v = unit_vector(v)
    coords = np.linspace(-span, span, samples)
    a, b = np.meshgrid(coords, coords)
    points = center + a[..., None] * u + b[..., None] * v
    return points[..., 0], points[..., 1], points[..., 2]


def _style_scene(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        width=960,
        height=680,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.72)"},
        scene={
            "aspectmode": "data",
            "xaxis_title": "e1",
            "yaxis_title": "e2",
            "zaxis_title": "e3",
            "camera": {"eye": {"x": 1.45, "y": -1.75, "z": 1.18}},
        },
    )
    return fig


def projection_figure(
    vector: Iterable[float] = (1.15, 0.85, 1.05),
    basis: Iterable[Iterable[float]] = ((1.0, 0.0, 0.0), (0.35, 1.0, 0.0)),
) -> go.Figure:
    vector = as_vector(vector)
    basis = as_frame(basis)
    projection, residual, coeffs = project_vector_to_span(vector, basis)
    x, y, z = plane_patch(basis, span=1.45)

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale=[[0, COLORS["plane"]], [1, COLORS["plane"]]],
            showscale=False,
            opacity=0.42,
            name="target subspace",
            hoverinfo="skip",
        )
    )
    fig.add_trace(arrow_trace((0, 0, 0), basis[0], "basis b1", COLORS["gray"], 5))
    fig.add_trace(arrow_trace((0, 0, 0), basis[1], "basis b2", COLORS["gray"], 5))
    fig.add_trace(arrow_trace((0, 0, 0), vector, "x", COLORS["red"], 8))
    fig.add_trace(arrow_trace((0, 0, 0), projection, "projection", COLORS["blue"], 8))
    fig.add_trace(arrow_trace(projection, vector, "orthogonal residual", COLORS["gold"], 6, "dash"))
    fig.add_annotation(
        text=f"projection coefficients: ({coeffs[0]:.3f}, {coeffs[1]:.3f})",
        x=0.02,
        y=0.03,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )
    return _style_scene(fig, "Orthogonal projection onto a 2-blade span")


def contraction_figure(angle_degrees: float = 35.0) -> go.Figure:
    theta = np.deg2rad(angle_degrees)
    vector = np.array([np.cos(theta), 0.55, np.sin(theta)])
    basis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    projection, _, _ = project_vector_to_span(vector, basis)
    contracted = np.array([-vector[1], vector[0], 0.0])
    x, y, z = plane_patch(basis, span=1.25)

    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            colorscale=[[0, COLORS["plane"]], [1, COLORS["plane"]]],
            showscale=False,
            opacity=0.38,
            name="B = e1 wedge e2",
            hoverinfo="skip",
        )
    )
    fig.add_trace(arrow_trace((0, 0, 0), vector, "x", COLORS["red"], 8))
    fig.add_trace(arrow_trace((0, 0, 0), projection, "metric projection of x", COLORS["blue"], 7))
    fig.add_trace(arrow_trace((0, 0, 0), contracted, "x contracted into B", COLORS["green"], 8))
    fig.add_trace(arrow_trace(projection, vector, "rejected part", COLORS["gold"], 5, "dash"))
    return _style_scene(fig, f"Vector-plane contraction, angle={angle_degrees:.1f} degrees")


def reciprocal_frame_figure(
    frame: Iterable[Iterable[float]] = ((1.0, 0.15, 0.05), (0.25, 1.0, 0.2), (0.1, 0.35, 1.0)),
) -> go.Figure:
    frame = as_frame(frame)
    reciprocal = reciprocal_frame(frame)
    fig = go.Figure()
    for i, vector in enumerate(frame, start=1):
        fig.add_trace(arrow_trace((0, 0, 0), vector, f"frame f{i}", COLORS["blue"], 7))
    for i, vector in enumerate(reciprocal, start=1):
        fig.add_trace(arrow_trace((0, 0, 0), vector, f"reciprocal r{i}", COLORS["purple"], 6, "dash"))
    fig.add_annotation(
        text="solid: frame vectors<br>dashed: reciprocal vectors",
        x=0.02,
        y=0.03,
        xref="paper",
        yref="paper",
        showarrow=False,
        align="left",
    )
    return _style_scene(fig, "A nonorthonormal frame and its reciprocal frame")


def rgb_string(color: Iterable[float]) -> str:
    clipped = np.clip(np.asarray(color, dtype=float), 0.0, 1.0)
    red, green, blue = (255 * clipped).round().astype(int)
    return f"rgb({red},{green},{blue})"


def sample_rgb_points() -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0],
            [0.9, 0.45, 0.15],
            [0.25, 0.55, 0.9],
            [0.7, 0.7, 0.7],
            [1.0, 1.0, 1.0],
        ]
    )


def color_space_convert(
    colors: Iterable[Iterable[float]],
    input_frame: Iterable[Iterable[float]],
) -> tuple[np.ndarray, np.ndarray]:
    colors = np.asarray(colors, dtype=float)
    frame = as_frame(input_frame)
    coords = np.array([coordinates_in_frame(color, frame) for color in colors])
    return coords, np.clip(coords, 0.0, 1.0)


def saturated_color_wheel(samples: int = 72, radius: float = 0.42) -> np.ndarray:
    white = unit_vector((1.0, 1.0, 1.0))
    u = unit_vector((1.0, -1.0, 0.0))
    v = unit_vector(np.cross(white, u))
    center = np.array([0.5, 0.5, 0.5])
    angles = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    colors = center + radius * (np.cos(angles)[:, None] * u + np.sin(angles)[:, None] * v)
    return np.clip(colors, 0.0, 1.0)


def color_space_figure(
    input_frame: Iterable[Iterable[float]] = ((1.0, 0.08, 0.02), (0.15, 1.0, 0.10), (0.08, 0.18, 1.0)),
) -> go.Figure:
    frame = as_frame(input_frame)
    source = np.vstack([sample_rgb_points(), saturated_color_wheel(48)])
    coords, converted = color_space_convert(source, frame)
    source_colors = [rgb_string(color) for color in source]
    converted_colors = [rgb_string(color) for color in converted]

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "scene"}, {"type": "scene"}]],
        subplot_titles=("source RGB vectors", "coordinates in reciprocal frame"),
    )
    fig.add_trace(
        go.Scatter3d(
            x=source[:, 0],
            y=source[:, 1],
            z=source[:, 2],
            mode="markers",
            marker={"size": 5, "color": source_colors},
            name="source",
            scene="scene",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter3d(
            x=coords[:, 0],
            y=coords[:, 1],
            z=coords[:, 2],
            mode="markers",
            marker={"size": 5, "color": converted_colors},
            name="converted",
            scene="scene2",
        ),
        row=1,
        col=2,
    )
    for axis, vector in zip(("red frame", "green frame", "blue frame"), frame, strict=True):
        fig.add_trace(arrow_trace((0, 0, 0), vector, axis, COLORS["gray"], 4, scene="scene"), row=1, col=1)
    cube_axis = {
        "xaxis_title": "R",
        "yaxis_title": "G",
        "zaxis_title": "B",
        "aspectmode": "cube",
        "xaxis": {"range": [-0.1, 1.15]},
        "yaxis": {"range": [-0.1, 1.15]},
        "zaxis": {"range": [-0.1, 1.15]},
    }
    fig.update_layout(
        width=1100,
        height=600,
        title="Color-space coordinates computed with a reciprocal frame",
        margin={"l": 0, "r": 0, "t": 64, "b": 0},
        scene=cube_axis,
        scene2=cube_axis,
        legend={"x": 0.01, "y": 0.99, "bgcolor": "rgba(255,255,255,0.70)"},
    )
    return fig
