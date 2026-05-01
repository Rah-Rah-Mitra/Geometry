"""Disk-model and Klein-model helpers for hyperbolic geometry notebooks."""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


ArrayLike = Sequence[float] | np.ndarray


def _as_point(point: ArrayLike) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    if p.shape != (2,):
        raise ValueError("expected a 2D point")
    return p


def inside_unit_disk(point: ArrayLike, *, eps: float = 1e-12) -> bool:
    return float(np.dot(_as_point(point), _as_point(point))) < 1.0 - eps


def poincare_to_klein(point: ArrayLike) -> np.ndarray:
    p = _as_point(point)
    r2 = float(np.dot(p, p))
    if r2 >= 1:
        raise ValueError("Poincare point must lie inside the unit disk")
    return 2 * p / (1 + r2)


def klein_to_poincare(point: ArrayLike) -> np.ndarray:
    k = _as_point(point)
    r2 = float(np.dot(k, k))
    if r2 >= 1:
        raise ValueError("Klein point must lie inside the unit disk")
    return k / (1 + math.sqrt(1 - r2))


def poincare_distance(a: ArrayLike, b: ArrayLike) -> float:
    a = _as_point(a)
    b = _as_point(b)
    if not inside_unit_disk(a) or not inside_unit_disk(b):
        raise ValueError("points must lie inside the unit disk")
    numerator = 2 * float(np.dot(a - b, a - b))
    denominator = (1 - float(np.dot(a, a))) * (1 - float(np.dot(b, b)))
    return float(math.acosh(1 + numerator / denominator))


def mobius_add(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    a = _as_point(a)
    b = _as_point(b)
    aa = float(np.dot(a, a))
    bb = float(np.dot(b, b))
    ab = float(np.dot(a, b))
    numerator = (1 + 2 * ab + bb) * a + (1 - aa) * b
    denominator = 1 + 2 * ab + aa * bb
    return numerator / denominator


def inversion(point: ArrayLike, *, center: ArrayLike = (0.0, 0.0), radius: float = 1.0) -> np.ndarray:
    p = _as_point(point)
    c = _as_point(center)
    v = p - c
    r2 = float(np.dot(v, v))
    if r2 == 0:
        raise ValueError("cannot invert the center")
    return c + (radius**2 / r2) * v


def geodesic_circle_center(a: ArrayLike, b: ArrayLike) -> tuple[np.ndarray, float] | None:
    """Return the Euclidean circle orthogonal to the unit circle through a and b.

    A diameter geodesic is returned as ``None``.
    """

    a = _as_point(a)
    b = _as_point(b)
    cross = a[0] * b[1] - a[1] * b[0]
    if abs(cross) < 1e-10:
        return None
    matrix = np.array([[a[0], a[1]], [b[0], b[1]]], dtype=float)
    rhs = np.array([(1 + float(np.dot(a, a))) / 2, (1 + float(np.dot(b, b))) / 2])
    center = np.linalg.solve(matrix, rhs)
    radius = math.sqrt(float(np.dot(center, center)) - 1)
    return center, radius


def angle_of_parallelism(distance: float) -> float:
    if distance < 0:
        raise ValueError("distance must be nonnegative")
    return float(2 * math.atan(math.exp(-distance)))


def defect_area(angle_sum: float, curvature: float = -1.0) -> float:
    if curvature >= 0:
        raise ValueError("hyperbolic defect uses negative curvature")
    return float((math.pi - angle_sum) / abs(curvature))

