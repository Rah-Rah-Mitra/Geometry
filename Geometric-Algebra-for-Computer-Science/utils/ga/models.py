"""Model-specific helpers for the geometric algebra notebook course."""

from __future__ import annotations

import numpy as np

EPS = 1e-12


def homogeneous_point(x: float, y: float, w: float = 1.0) -> np.ndarray:
    return np.array([float(x), float(y), float(w)])


def normalize_homogeneous_point(point: np.ndarray) -> np.ndarray:
    point = np.asarray(point, dtype=float)
    if abs(point[-1]) < EPS:
        raise ZeroDivisionError("point at infinity cannot be normalized to affine coordinates")
    return point / point[-1]


def homogeneous_line(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Line through two homogeneous 2-D points."""
    return np.cross(np.asarray(a, dtype=float), np.asarray(b, dtype=float))


def intersect_homogeneous_lines(line_a: np.ndarray, line_b: np.ndarray) -> np.ndarray:
    return np.cross(np.asarray(line_a, dtype=float), np.asarray(line_b, dtype=float))


def plucker_line(point_a: np.ndarray, point_b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return direction and moment coordinates for a 3-D line."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    direction = b - a
    length = np.linalg.norm(direction)
    if length < EPS:
        raise ValueError("two distinct points are required for a Plucker line")
    direction = direction / length
    moment = np.cross(a, direction)
    return direction, moment


def conformal_point(x: np.ndarray) -> np.ndarray:
    """Embed a Euclidean point as x + e0 + 0.5 |x|^2 einf.

    Coordinates are ordered as [e1, e2, e3, e0, einf].
    """
    x = np.asarray(x, dtype=float)
    if x.shape != (3,):
        raise ValueError("conformal_point expects a 3-vector")
    return np.array([x[0], x[1], x[2], 1.0, 0.5 * float(np.dot(x, x))])


def conformal_inner(a: np.ndarray, b: np.ndarray) -> float:
    """Inner product for basis [e1,e2,e3,e0,einf] with e0.einf = -1."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.dot(a[:3], b[:3]) - a[3] * b[4] - a[4] * b[3])


def conformal_distance_squared(a: np.ndarray, b: np.ndarray) -> float:
    return -2.0 * conformal_inner(conformal_point(a), conformal_point(b))


def rotation_matrix(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    length = np.linalg.norm(axis)
    if length < EPS:
        raise ValueError("rotation axis must be nonzero")
    x, y, z = axis / length
    c = np.cos(angle)
    s = np.sin(angle)
    C = 1.0 - c
    return np.array(
        [
            [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
        ]
    )


def ray_sphere_intersection(
    origin: np.ndarray,
    direction: np.ndarray,
    center: np.ndarray,
    radius: float,
) -> float | None:
    """Return the first positive ray parameter for a sphere hit, or None."""
    origin = np.asarray(origin, dtype=float)
    direction = np.asarray(direction, dtype=float)
    center = np.asarray(center, dtype=float)
    direction = direction / np.linalg.norm(direction)
    oc = origin - center
    b = 2.0 * float(np.dot(oc, direction))
    c = float(np.dot(oc, oc) - radius * radius)
    disc = b * b - 4.0 * c
    if disc < 0:
        return None
    root = np.sqrt(disc)
    candidates = [(-b - root) / 2.0, (-b + root) / 2.0]
    positive = [t for t in candidates if t > EPS]
    return min(positive) if positive else None
