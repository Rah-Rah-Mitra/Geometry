"""Spherical and hyperbolic model helpers."""

from __future__ import annotations

import numpy as np
import sympy as sp

EPS = 1e-12


def spherical_to_cartesian(theta: float, phi: float, radius: float = 1.0) -> np.ndarray:
    """Map colatitude ``theta`` and azimuth ``phi`` to a point on a sphere."""

    radius = float(radius)
    return np.array(
        [
            radius * np.sin(theta) * np.cos(phi),
            radius * np.sin(theta) * np.sin(phi),
            radius * np.cos(theta),
        ]
    )


def cartesian_to_spherical(point: np.ndarray) -> tuple[float, float, float]:
    """Return ``(radius, theta, phi)`` with ``theta`` measured from the north pole."""

    point = np.asarray(point, dtype=float)
    if point.shape != (3,):
        raise ValueError("point must be a 3-vector")
    radius = float(np.linalg.norm(point))
    if radius <= EPS:
        raise ValueError("spherical coordinates are undefined at the origin")
    theta = float(np.arccos(np.clip(point[2] / radius, -1.0, 1.0)))
    phi = float(np.arctan2(point[1], point[0]))
    return radius, theta, phi


def spherical_distance(a: np.ndarray, b: np.ndarray, radius: float = 1.0) -> float:
    """Great-circle distance between two nonzero vectors on a sphere."""

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    if a_norm <= EPS or b_norm <= EPS:
        raise ValueError("spherical distance needs nonzero vectors")
    cosine = float(np.dot(a, b) / (a_norm * b_norm))
    return float(radius) * float(np.arccos(np.clip(cosine, -1.0, 1.0)))


def sphere_embedding(theta: sp.Expr, phi: sp.Expr, radius: sp.Expr = 1) -> sp.Matrix:
    """Symbolic embedding of a round sphere in ``R^3``."""

    radius = sp.sympify(radius)
    return sp.Matrix(
        [
            radius * sp.sin(theta) * sp.cos(phi),
            radius * sp.sin(theta) * sp.sin(phi),
            radius * sp.cos(theta),
        ]
    )


def sphere_metric(theta: sp.Expr, radius: sp.Expr = 1) -> sp.Matrix:
    """Metric of a round sphere in coordinates ``(theta, phi)``."""

    radius = sp.sympify(radius)
    return sp.diag(radius**2, radius**2 * sp.sin(theta) ** 2)


def hyperboloid_inner(a: np.ndarray, b: np.ndarray) -> float | np.ndarray:
    """Minkowski inner product ``-x0*y0 + x1*y1 + x2*y2``."""

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape[-1:] != (3,) or b.shape[-1:] != (3,):
        raise ValueError("hyperboloid points must have shape (..., 3)")
    value = -a[..., 0] * b[..., 0] + np.sum(a[..., 1:] * b[..., 1:], axis=-1)
    return float(value) if np.ndim(value) == 0 else value


def hyperbolic_distance(
    a: np.ndarray,
    b: np.ndarray,
    curvature_radius: float = 1.0,
) -> float | np.ndarray:
    """Distance in the hyperboloid model of curvature ``-1 / radius^2``."""

    radius = float(curvature_radius)
    argument = -np.asarray(hyperboloid_inner(a, b), dtype=float) / radius**2
    argument = np.maximum(argument, 1.0)
    argument = np.where(argument - 1.0 <= EPS, 1.0, argument)
    distance = radius * np.arccosh(argument)
    return float(distance) if np.ndim(distance) == 0 else distance


def poincare_disk_to_hyperboloid(
    point: np.ndarray,
    curvature_radius: float = 1.0,
) -> np.ndarray:
    """Map a Poincare disk point to the upper sheet of the hyperboloid."""

    point = np.asarray(point, dtype=float)
    if point.shape[-1:] != (2,):
        raise ValueError("point must have shape (..., 2)")
    radius = float(curvature_radius)
    norm2 = np.sum(point * point, axis=-1)
    if np.any(norm2 >= 1.0 - EPS):
        raise ValueError("Poincare disk points must satisfy |p| < 1")
    denominator = 1.0 - norm2
    time = radius * (1.0 + norm2) / denominator
    space = radius * (2.0 * point) / denominator[..., np.newaxis]
    return np.concatenate([time[..., np.newaxis], space], axis=-1)


def hyperboloid_to_poincare_disk(
    point: np.ndarray,
    curvature_radius: float = 1.0,
) -> np.ndarray:
    """Project a hyperboloid point to the Poincare disk."""

    point = np.asarray(point, dtype=float)
    if point.shape[-1:] != (3,):
        raise ValueError("point must have shape (..., 3)")
    radius = float(curvature_radius)
    denominator = point[..., 0] + radius
    if np.any(denominator <= EPS):
        raise ValueError("point cannot be projected from the lower sheet")
    return point[..., 1:] / denominator[..., np.newaxis]


def poincare_disk_metric(point: np.ndarray, curvature_radius: float = 1.0) -> np.ndarray:
    """Metric matrix in Poincare disk coordinates."""

    point = np.asarray(point, dtype=float)
    if point.shape != (2,):
        raise ValueError("point must be a 2-vector")
    norm2 = float(np.dot(point, point))
    if norm2 >= 1.0 - EPS:
        raise ValueError("Poincare disk points must satisfy |p| < 1")
    scale = (2.0 * float(curvature_radius) / (1.0 - norm2)) ** 2
    return scale * np.eye(2)


def poincare_disk_distance(
    a: np.ndarray,
    b: np.ndarray,
    curvature_radius: float = 1.0,
) -> float:
    """Hyperbolic distance between two points in the Poincare disk."""

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != (2,) or b.shape != (2,):
        raise ValueError("points must be 2-vectors")
    a2 = float(np.dot(a, a))
    b2 = float(np.dot(b, b))
    if a2 >= 1.0 - EPS or b2 >= 1.0 - EPS:
        raise ValueError("Poincare disk points must satisfy |p| < 1")
    numerator = 2.0 * float(np.dot(a - b, a - b))
    denominator = (1.0 - a2) * (1.0 - b2)
    return float(curvature_radius) * float(np.arccosh(1.0 + numerator / denominator))


def upper_half_plane_metric(y: float, curvature_radius: float = 1.0) -> np.ndarray:
    """Metric matrix for upper-half-plane coordinates ``(x, y)`` with ``y > 0``."""

    y = float(y)
    if y <= EPS:
        raise ValueError("upper-half-plane metric requires y > 0")
    scale = (float(curvature_radius) / y) ** 2
    return scale * np.eye(2)
