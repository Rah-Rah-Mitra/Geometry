"""Geometry and plotting helpers for the Chapter 1 GA notebook."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go

EPS = 1e-10

COLORS = {
    "circle": "#2ca02c",
    "rotated": "#1f77b4",
    "line": "#d62728",
    "plane": "#f2c14e",
    "reflected": "#9467bd",
    "sphere": "#e07a5f",
    "light_green": "rgba(44, 160, 44, 0.28)",
    "light_blue": "rgba(31, 119, 180, 0.30)",
}


def as_vec(value: np.ndarray | list[float] | tuple[float, ...]) -> np.ndarray:
    vector = np.asarray(value, dtype=float)
    if vector.shape != (3,):
        raise ValueError(f"expected a 3-vector, got shape {vector.shape}")
    return vector


def as_points(value: np.ndarray) -> tuple[np.ndarray, bool]:
    points = np.asarray(value, dtype=float)
    single = points.ndim == 1
    if single:
        points = points[None, :]
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError(f"expected points with shape (n, 3), got {points.shape}")
    return points, single


def normalize(value: np.ndarray) -> np.ndarray:
    vector = np.asarray(value, dtype=float)
    length = np.linalg.norm(vector)
    if length < EPS:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    x, y, z = normalize(axis)
    c = np.cos(angle)
    s = np.sin(angle)
    one_minus_c = 1.0 - c
    return np.array(
        [
            [
                c + x * x * one_minus_c,
                x * y * one_minus_c - z * s,
                x * z * one_minus_c + y * s,
            ],
            [
                y * x * one_minus_c + z * s,
                c + y * y * one_minus_c,
                y * z * one_minus_c - x * s,
            ],
            [
                z * x * one_minus_c - y * s,
                z * y * one_minus_c + x * s,
                c + z * z * one_minus_c,
            ],
        ]
    )


@dataclass
class Line3D:
    point: np.ndarray
    direction: np.ndarray

    def __post_init__(self) -> None:
        self.point = as_vec(self.point)
        self.direction = normalize(as_vec(self.direction))

    @classmethod
    def through(cls, a: np.ndarray, b: np.ndarray) -> "Line3D":
        a = as_vec(a)
        b = as_vec(b)
        return cls(a, b - a)

    def point_at(self, t: float) -> np.ndarray:
        return self.point + t * self.direction

    def sample(self, t_min: float = -2.5, t_max: float = 2.5, n: int = 80) -> np.ndarray:
        t = np.linspace(t_min, t_max, n)
        return self.point + t[:, None] * self.direction

    def distance_to_points(self, points: np.ndarray) -> np.ndarray:
        points, single = as_points(points)
        distances = np.linalg.norm(np.cross(points - self.point, self.direction), axis=1)
        return distances[0] if single else distances


@dataclass
class Plane3D:
    point: np.ndarray
    normal: np.ndarray

    def __post_init__(self) -> None:
        self.point = as_vec(self.point)
        self.normal = normalize(as_vec(self.normal))

    def signed_distance(self, points: np.ndarray) -> np.ndarray:
        points, single = as_points(points)
        distances = (points - self.point) @ self.normal
        return distances[0] if single else distances

    def reflect_points(self, points: np.ndarray) -> np.ndarray:
        points, single = as_points(points)
        distances = self.signed_distance(points)
        reflected = points - 2.0 * distances[:, None] * self.normal
        return reflected[0] if single else reflected

    def reflect_line(self, line: Line3D) -> Line3D:
        p0 = self.reflect_points(line.point)
        p1 = self.reflect_points(line.point + line.direction)
        return Line3D(p0, p1 - p0)

    def basis(self) -> tuple[np.ndarray, np.ndarray]:
        reference = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(reference, self.normal)) > 0.85:
            reference = np.array([0.0, 1.0, 0.0])
        u = normalize(np.cross(self.normal, reference))
        v = normalize(np.cross(self.normal, u))
        return u, v

    def grid(self, span: float = 2.4, n: int = 16) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        u, v = self.basis()
        coords = np.linspace(-span, span, n)
        a, b = np.meshgrid(coords, coords)
        points = self.point + a[..., None] * u + b[..., None] * v
        return points[..., 0], points[..., 1], points[..., 2]


@dataclass
class Sphere3D:
    center: np.ndarray
    radius: float

    def __post_init__(self) -> None:
        self.center = as_vec(self.center)
        if self.radius <= 0:
            raise ValueError("sphere radius must be positive")

    def invert_points(self, points: np.ndarray) -> np.ndarray:
        points, single = as_points(points)
        shifted = points - self.center
        norm2 = np.sum(shifted * shifted, axis=1)
        if np.any(norm2 < EPS):
            raise ValueError("sphere inversion is singular at the sphere center")
        inverted = self.center + (self.radius**2 / norm2)[:, None] * shifted
        return inverted[0] if single else inverted

    def surface(self, n_theta: int = 36, n_phi: int = 18) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        theta = np.linspace(0, 2 * np.pi, n_theta)
        phi = np.linspace(0, np.pi, n_phi)
        theta, phi = np.meshgrid(theta, phi)
        x = self.center[0] + self.radius * np.cos(theta) * np.sin(phi)
        y = self.center[1] + self.radius * np.sin(theta) * np.sin(phi)
        z = self.center[2] + self.radius * np.cos(phi)
        return x, y, z


@dataclass
class Circle3D:
    center: np.ndarray
    radius: float
    u: np.ndarray
    v: np.ndarray

    def __post_init__(self) -> None:
        self.center = as_vec(self.center)
        self.u = normalize(as_vec(self.u))
        self.v = normalize(as_vec(self.v))
        self.v = normalize(self.v - np.dot(self.v, self.u) * self.u)
        if self.radius <= 0:
            raise ValueError("circle radius must be positive")

    @property
    def normal(self) -> np.ndarray:
        return normalize(np.cross(self.u, self.v))

    @classmethod
    def through_three_points(cls, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> "Circle3D":
        a = as_vec(a)
        b = as_vec(b)
        c = as_vec(c)
        e1 = normalize(b - a)
        plane_normal = normalize(np.cross(b - a, c - a))
        e2 = normalize(np.cross(plane_normal, e1))

        bx, by = np.dot(b - a, e1), np.dot(b - a, e2)
        cx, cy = np.dot(c - a, e1), np.dot(c - a, e2)
        matrix = np.array([[2.0 * bx, 2.0 * by], [2.0 * cx, 2.0 * cy]])
        rhs = np.array([bx * bx + by * by, cx * cx + cy * cy])
        ux, uy = np.linalg.solve(matrix, rhs)

        center = a + ux * e1 + uy * e2
        radius = np.linalg.norm(center - a)
        return cls(center=center, radius=radius, u=e1, v=e2)

    def sample(self, n: int = 160, endpoint: bool = True) -> np.ndarray:
        theta = np.linspace(0, 2 * np.pi, n, endpoint=endpoint)
        return self.center + self.radius * (
            np.cos(theta)[:, None] * self.u + np.sin(theta)[:, None] * self.v
        )


def rotate_points_about_line(points: np.ndarray, line: Line3D, angle: float) -> np.ndarray:
    points, single = as_points(points)
    matrix = rotation_matrix(line.direction, angle)
    rotated = line.point + (points - line.point) @ matrix.T
    return rotated[0] if single else rotated


def rotate_line_about_line(line: Line3D, axis: Line3D, angle: float) -> Line3D:
    p0 = rotate_points_about_line(line.point, axis, angle)
    p1 = rotate_points_about_line(line.point + line.direction, axis, angle)
    return Line3D(p0, p1 - p0)


def curve_trace(points: np.ndarray, name: str, color: str, width: int = 6) -> go.Scatter3d:
    points = np.asarray(points)
    return go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode="lines",
        name=name,
        line={"color": color, "width": width},
    )


def line_trace(
    line: Line3D,
    name: str,
    color: str,
    t_min: float = -2.7,
    t_max: float = 2.7,
    width: int = 7,
) -> go.Scatter3d:
    return curve_trace(line.sample(t_min, t_max, 80), name, color, width)


def segment_trace(
    points: np.ndarray,
    name: str,
    color: str,
    width: int = 5,
    marker_size: int = 4,
    dash: str | None = None,
) -> go.Scatter3d:
    points = np.asarray(points, dtype=float)
    line: dict[str, object] = {"color": color, "width": width}
    if dash:
        line["dash"] = dash
    return go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode="lines+markers",
        name=name,
        line=line,
        marker={"color": color, "size": marker_size},
    )


def point_trace(points: np.ndarray, labels: list[str], color: str) -> go.Scatter3d:
    points = np.asarray(points)
    return go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode="markers+text",
        text=labels,
        textposition="top center",
        name="control points",
        marker={"color": color, "size": 5},
        showlegend=False,
    )


def circle_point_errors(circle: Circle3D, points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    points, single = as_points(points)
    centered = points - circle.center
    radial_errors = np.linalg.norm(centered, axis=1) - circle.radius
    plane_errors = centered @ circle.normal
    if single:
        return radial_errors[0], plane_errors[0]
    return radial_errors, plane_errors


def plane_surface_trace(plane: Plane3D, name: str = "plane") -> go.Surface:
    x, y, z = plane.grid(span=2.6, n=18)
    return go.Surface(
        x=x,
        y=y,
        z=z,
        name=name,
        showscale=False,
        opacity=0.24,
        colorscale=[[0, COLORS["plane"]], [1, COLORS["plane"]]],
        hoverinfo="skip",
    )


def sphere_surface_trace(sphere: Sphere3D, name: str = "sphere") -> go.Surface:
    x, y, z = sphere.surface()
    return go.Surface(
        x=x,
        y=y,
        z=z,
        name=name,
        showscale=False,
        opacity=0.18,
        colorscale=[[0, COLORS["sphere"]], [1, COLORS["sphere"]]],
        hoverinfo="skip",
    )


def finish_figure(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(
        title=title,
        width=1000,
        height=720,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        scene={
            "aspectmode": "data",
            "xaxis_title": "x",
            "yaxis_title": "y",
            "zaxis_title": "z",
            "camera": {"eye": {"x": 1.55, "y": -1.85, "z": 1.2}},
        },
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.65)"},
    )
    return fig
