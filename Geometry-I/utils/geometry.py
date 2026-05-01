"""Small geometric primitives used by the Geometry I notebooks."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np


def affine_combination(points: np.ndarray, weights: Iterable[float]) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    w = np.asarray(list(weights), dtype=float)
    if pts.shape[0] != w.shape[0]:
        raise ValueError("points and weights have incompatible lengths")
    if not np.isclose(w.sum(), 1.0):
        raise ValueError("affine weights must sum to 1")
    return w @ pts


def barycentric_coordinates(vertices: np.ndarray, point: np.ndarray) -> np.ndarray:
    verts = np.asarray(vertices, dtype=float)
    p = np.asarray(point, dtype=float)
    matrix = np.vstack([verts.T, np.ones(verts.shape[0])])
    rhs = np.append(p, 1.0)
    return np.linalg.solve(matrix, rhs)


def homogeneous(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        return np.append(pts, 1.0)
    return np.column_stack([pts, np.ones(len(pts))])


def dehomogeneous(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        if np.isclose(pts[-1], 0.0):
            raise ValueError("point at infinity cannot be dehomogenized")
        return pts[:-1] / pts[-1]
    scale = pts[:, [-1]]
    if np.any(np.isclose(scale, 0.0)):
        raise ValueError("point at infinity cannot be dehomogenized")
    return pts[:, :-1] / scale


def cross_ratio(a: float, b: float, c: float, d: float) -> float:
    """Return the real cross-ratio (a,b;c,d)."""

    return ((c - a) * (d - b)) / ((c - b) * (d - a))


def apply_homography(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    h = homogeneous(points)
    transformed = h @ np.asarray(matrix, dtype=float).T
    return dehomogeneous(transformed)


def mobius_transform(z: np.ndarray, a: complex, b: complex, c: complex, d: complex) -> np.ndarray:
    z = np.asarray(z, dtype=complex)
    denominator = c * z + d
    if np.any(np.isclose(denominator, 0.0)):
        raise ValueError("Mobius denominator vanished")
    return (a * z + b) / denominator


def rotation_matrix(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def reflection_matrix(theta: float = 0.0) -> np.ndarray:
    c, s = math.cos(2 * theta), math.sin(2 * theta)
    return np.array([[c, s], [s, -c]], dtype=float)


def affine_transform(points: np.ndarray, matrix: np.ndarray, offset: Iterable[float]) -> np.ndarray:
    return np.asarray(points, dtype=float) @ np.asarray(matrix, dtype=float).T + np.asarray(offset, dtype=float)


def convex_hull_points(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    if len(pts) <= 2:
        return pts
    try:
        from scipy.spatial import ConvexHull

        hull = ConvexHull(pts)
        return pts[hull.vertices]
    except Exception:
        center = pts.mean(axis=0)
        angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
        return pts[np.argsort(angles)]


def support_function(points: np.ndarray, directions: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    dirs = np.asarray(directions, dtype=float)
    return np.max(pts @ dirs.T, axis=0)


def hausdorff_distance(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    distances = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)
    return float(max(distances.min(axis=1).max(), distances.min(axis=0).max()))


def invert_points(points: np.ndarray, center: Iterable[float] = (0.0, 0.0), radius: float = 1.0) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    c = np.asarray(center, dtype=float)
    shifted = pts - c
    norm2 = np.sum(shifted * shifted, axis=1)
    if np.any(np.isclose(norm2, 0.0)):
        raise ValueError("cannot invert the center of inversion")
    return c + (radius**2) * shifted / norm2[:, None]


def stereographic_project(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    denominator = 1.0 - pts[:, 2]
    if np.any(np.isclose(denominator, 0.0)):
        raise ValueError("north pole projects to infinity")
    return pts[:, :2] / denominator[:, None]


def triangle_area(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    return float(abs(np.cross(b - a, c - a)) / 2.0)

