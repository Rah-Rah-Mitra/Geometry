"""Readable 2D geometry helpers."""

from __future__ import annotations

import numpy as np


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    a, b, c = np.asarray(a, float), np.asarray(b, float), np.asarray(c, float)
    return float(np.cross(b - a, c - a))


def polygon_area(points: np.ndarray) -> float:
    p = np.asarray(points, dtype=float)
    x, y = p[:, 0], p[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def barycentric_coordinates(point: np.ndarray, triangle: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    tri = np.asarray(triangle, dtype=float)
    a = np.vstack([tri.T, np.ones(3)])
    b = np.array([p[0], p[1], 1.0])
    return np.linalg.solve(a, b)


def project_point_segment(point: np.ndarray, a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, float]:
    p, a, b = np.asarray(point, float), np.asarray(a, float), np.asarray(b, float)
    ab = b - a
    t = float(np.dot(p - a, ab) / np.dot(ab, ab))
    tc = min(1.0, max(0.0, t))
    return a + tc * ab, tc


def convex_hull(points: np.ndarray) -> np.ndarray:
    pts = sorted(map(tuple, np.asarray(points, dtype=float)))
    if len(pts) <= 1:
        return np.array(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1], dtype=float)
