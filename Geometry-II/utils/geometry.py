"""Small geometry primitives used by the Geometry II notebooks."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def as_points(points: Iterable[Iterable[float]] | np.ndarray, dim: int | None = None) -> np.ndarray:
    arr = np.asarray(points, dtype=float)
    if arr.ndim != 2:
        raise ValueError("expected a two-dimensional point array")
    if dim is not None and arr.shape[1] != dim:
        raise ValueError(f"expected points of dimension {dim}")
    return arr


def regular_polygon(n: int, *, radius: float = 1.0, phase: float = 0.0) -> np.ndarray:
    t = np.linspace(0, 2 * np.pi, n, endpoint=False) + phase
    return np.column_stack([radius * np.cos(t), radius * np.sin(t)])


def polygon_area(points: Iterable[Iterable[float]] | np.ndarray) -> float:
    pts = as_points(points, 2)
    x = pts[:, 0]
    y = pts[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def convex_hull_2d(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    pts = sorted(map(tuple, as_points(points, 2)))
    if len(pts) <= 1:
        return np.asarray(pts, dtype=float)

    def cross(o: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> float:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: list[tuple[float, float]] = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)

    upper: list[tuple[float, float]] = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return np.asarray(lower[:-1] + upper[:-1], dtype=float)


def euler_characteristic(vertices: int, edges: int, faces: int) -> int:
    return vertices - edges + faces


def homogeneous(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        return np.append(pts, 1.0)
    return np.column_stack([pts, np.ones(len(pts))])


def dehomogeneous(points: Iterable[Iterable[float]] | np.ndarray, *, tol: float = 1e-12) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        if abs(pts[-1]) <= tol:
            raise ValueError("point at infinity cannot be dehomogenized in this chart")
        return pts[:-1] / pts[-1]
    denom = pts[:, -1]
    if np.any(np.abs(denom) <= tol):
        raise ValueError("some points are at infinity in this chart")
    return pts[:, :-1] / denom[:, None]


def projective_transform(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    hp = homogeneous(points)
    transformed = hp @ np.asarray(matrix, dtype=float).T
    return dehomogeneous(transformed)


def cross_ratio(a: float, b: float, c: float, d: float) -> float:
    return float(((c - a) * (d - b)) / ((c - b) * (d - a)))


def conic_matrix(kind: str = "unit_circle") -> np.ndarray:
    if kind == "unit_circle":
        return np.diag([1.0, 1.0, -1.0])
    if kind == "rectangular_hyperbola":
        return np.array([[0.0, 0.5, 0.0], [0.5, 0.0, 0.0], [0.0, 0.0, -1.0]])
    if kind == "parabola":
        return np.array([[0.0, 0.0, -0.5], [0.0, 1.0, 0.0], [-0.5, 0.0, 0.0]])
    raise ValueError(f"unknown conic kind: {kind}")


def conic_residual(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    hp = homogeneous(points)
    q = np.asarray(matrix, dtype=float)
    return np.einsum("...i,ij,...j->...", hp, q, hp)


def polar_line(matrix: np.ndarray, point_h: np.ndarray) -> np.ndarray:
    return np.asarray(matrix, dtype=float) @ np.asarray(point_h, dtype=float)


def ellipse_points(a: float = 2.0, b: float = 1.0, count: int = 400) -> np.ndarray:
    t = np.linspace(0, 2 * np.pi, count)
    return np.column_stack([a * np.cos(t), b * np.sin(t)])


def hyperbola_points(a: float = 1.0, b: float = 0.7, span: float = 2.0, count: int = 240) -> tuple[np.ndarray, np.ndarray]:
    u = np.linspace(-span, span, count)
    right = np.column_stack([a * np.cosh(u), b * np.sinh(u)])
    left = np.column_stack([-a * np.cosh(u), b * np.sinh(u)])
    return left, right


def quadratic_signature(matrix: np.ndarray, *, tol: float = 1e-9) -> tuple[int, int, int]:
    eig = np.linalg.eigvalsh(np.asarray(matrix, dtype=float))
    pos = int(np.sum(eig > tol))
    neg = int(np.sum(eig < -tol))
    zero = int(len(eig) - pos - neg)
    return pos, neg, zero


def stereographic_project(points: np.ndarray, *, north: bool = True) -> np.ndarray:
    pts = as_points(points, 3)
    denom = 1.0 - pts[:, 2] if north else 1.0 + pts[:, 2]
    return pts[:, :2] / denom[:, None]


def sphere_grid(u_count: int = 72, v_count: int = 36) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.linspace(0, 2 * np.pi, u_count)
    v = np.linspace(0, np.pi, v_count)
    uu, vv = np.meshgrid(u, v)
    return np.cos(uu) * np.sin(vv), np.sin(uu) * np.sin(vv), np.cos(vv)


def spherical_distance(a: np.ndarray, b: np.ndarray) -> float:
    x = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    return float(np.arccos(np.clip(x, -1.0, 1.0)))


def poincare_distance(u: np.ndarray, v: np.ndarray) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    num = 2 * np.linalg.norm(u - v) ** 2
    den = (1 - np.linalg.norm(u) ** 2) * (1 - np.linalg.norm(v) ** 2)
    return float(np.arccosh(1 + num / den))


def disk_rotation(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def oriented_circle_vector(center: tuple[float, float], radius: float) -> np.ndarray:
    x, y = center
    r = float(radius)
    # Lie sphere style coordinates for the equation |p-c|^2 = r^2.
    return np.array([x, y, 0.5 * (x * x + y * y - r * r), 1.0], dtype=float)


def circle_orthogonality(c1: tuple[float, float], r1: float, c2: tuple[float, float], r2: float) -> float:
    center_gap = float(np.linalg.norm(np.asarray(c1, dtype=float) - np.asarray(c2, dtype=float)) ** 2)
    return center_gap - r1 * r1 - r2 * r2
