"""Poincare disk and inversion helpers for non-Euclidean geometry notebooks."""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np


def as_point(value: Sequence[float]) -> np.ndarray:
    return np.asarray(value, dtype=float)


def inside_unit_disk(point: Sequence[float], *, eps: float = 1e-12) -> bool:
    return float(np.dot(as_point(point), as_point(point))) < 1.0 - eps


def poincare_distance(a: Sequence[float], b: Sequence[float]) -> float:
    """Return distance in the unit Poincare disk."""

    pa, pb = as_point(a), as_point(b)
    aa = float(np.dot(pa, pa))
    bb = float(np.dot(pb, pb))
    diff = float(np.dot(pa - pb, pa - pb))
    arg = 1.0 + 2.0 * diff / ((1.0 - aa) * (1.0 - bb))
    return float(math.acosh(max(1.0, arg)))


def invert_in_circle(point: Sequence[float], center: Sequence[float] = (0.0, 0.0), radius: float = 1.0) -> np.ndarray:
    p = as_point(point)
    c = as_point(center)
    v = p - c
    norm2 = float(np.dot(v, v))
    if norm2 == 0:
        raise ValueError("circle inversion is undefined at the center")
    return c + (radius * radius / norm2) * v


def geodesic_circle(a: Sequence[float], b: Sequence[float]) -> tuple[np.ndarray | None, float | None]:
    """Return the Euclidean circle for a disk geodesic, or None for a diameter."""

    pa, pb = as_point(a), as_point(b)
    if abs(np.cross(pa, pb)) < 1e-10:
        return None, None
    matrix = np.vstack([2.0 * pa, 2.0 * pb])
    rhs = np.array([float(np.dot(pa, pa)) + 1.0, float(np.dot(pb, pb)) + 1.0])
    center = np.linalg.solve(matrix, rhs)
    radius = math.sqrt(max(0.0, float(np.dot(center, center)) - 1.0))
    return center, radius


def geodesic_arc_points(a: Sequence[float], b: Sequence[float], samples: int = 160) -> np.ndarray:
    """Sample a Poincare geodesic arc between two points."""

    pa, pb = as_point(a), as_point(b)
    center, radius = geodesic_circle(pa, pb)
    if center is None or radius is None:
        return np.column_stack(
            [
                np.linspace(pa[0], pb[0], samples),
                np.linspace(pa[1], pb[1], samples),
            ]
        )
    theta0 = math.atan2(pa[1] - center[1], pa[0] - center[0])
    theta1 = math.atan2(pb[1] - center[1], pb[0] - center[0])
    delta = (theta1 - theta0 + math.pi) % (2.0 * math.pi) - math.pi
    angles = theta0 + np.linspace(0.0, delta, samples)
    pts = center + radius * np.column_stack([np.cos(angles), np.sin(angles)])
    inside = np.sum(np.linalg.norm(pts, axis=1) < 1.0)
    alt_angles = theta0 + np.linspace(0.0, delta - math.copysign(2.0 * math.pi, delta), samples)
    alt = center + radius * np.column_stack([np.cos(alt_angles), np.sin(alt_angles)])
    if np.sum(np.linalg.norm(alt, axis=1) < 1.0) > inside:
        return alt
    return pts


def disk_rotation(point: Sequence[float], angle: float) -> np.ndarray:
    p = as_point(point)
    rot = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
    return rot @ p
