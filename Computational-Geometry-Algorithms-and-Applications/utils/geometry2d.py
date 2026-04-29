"""Small inspectable 2D geometry primitives for CGAA notebooks."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2
from typing import Iterable

import numpy as np


ArrayLikePoints = Iterable[tuple[float, float]] | np.ndarray


def cross2(u: np.ndarray, v: np.ndarray) -> float:
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    return float(u[0] * v[1] - u[1] * v[0])


def as_points(points: ArrayLikePoints) -> np.ndarray:
    arr = np.asarray(list(points) if not isinstance(points, np.ndarray) else points, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValueError("expected an array of 2D points")
    return arr


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    return cross2(b - a, c - a)


def polygon_area(points: ArrayLikePoints) -> float:
    pts = as_points(points)
    x = pts[:, 0]
    y = pts[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def convex_hull(points: ArrayLikePoints) -> np.ndarray:
    pts = sorted(map(tuple, as_points(points)))
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


def point_in_convex_polygon(point: np.ndarray, polygon: np.ndarray, *, tol: float = 1e-9) -> bool:
    poly = as_points(polygon)
    p = np.asarray(point, dtype=float)
    signs = [orientation(poly[i], poly[(i + 1) % len(poly)], p) for i in range(len(poly))]
    return all(s >= -tol for s in signs) or all(s <= tol for s in signs)


def segment_intersection(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    d: tuple[float, float],
    *,
    tol: float = 1e-9,
) -> tuple[float, float] | None:
    p = np.asarray(a, dtype=float)
    r = np.asarray(b, dtype=float) - p
    q = np.asarray(c, dtype=float)
    s = np.asarray(d, dtype=float) - q
    denom = cross2(r, s)
    if abs(denom) <= tol:
        return None
    t = cross2(q - p, s) / denom
    u = cross2(q - p, r) / denom
    if -tol <= t <= 1 + tol and -tol <= u <= 1 + tol:
        x, y = p + t * r
        return (float(x), float(y))
    return None


def brute_force_intersections(segments: Iterable[tuple[tuple[float, float], tuple[float, float]]]) -> list[tuple[float, float]]:
    segs = list(segments)
    points: list[tuple[float, float]] = []
    for i, (a, b) in enumerate(segs):
        for c, d in segs[i + 1 :]:
            hit = segment_intersection(a, b, c, d)
            if hit is not None:
                rounded = (round(hit[0], 8), round(hit[1], 8))
                if rounded not in points:
                    points.append(rounded)
    return sorted(points)


def clip_polygon_halfplane(polygon: np.ndarray, normal: tuple[float, float], offset: float, *, tol: float = 1e-9) -> np.ndarray:
    poly = as_points(polygon)
    n = np.asarray(normal, dtype=float)

    def inside(point: np.ndarray) -> bool:
        return float(np.dot(n, point) - offset) <= tol

    def intersect(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        direction = b - a
        denom = float(np.dot(n, direction))
        if abs(denom) <= tol:
            return b
        t = float((offset - np.dot(n, a)) / denom)
        return a + t * direction

    output: list[np.ndarray] = []
    for i, current in enumerate(poly):
        previous = poly[i - 1]
        curr_in = inside(current)
        prev_in = inside(previous)
        if curr_in:
            if not prev_in:
                output.append(intersect(previous, current))
            output.append(current)
        elif prev_in:
            output.append(intersect(previous, current))
    return np.asarray(output, dtype=float)


def point_in_triangle(point: np.ndarray, triangle: np.ndarray, *, tol: float = 1e-9) -> bool:
    tri = as_points(triangle)
    p = np.asarray(point, dtype=float)
    areas = [orientation(tri[i], tri[(i + 1) % 3], p) for i in range(3)]
    return all(a >= -tol for a in areas) or all(a <= tol for a in areas)


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    return np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=2)


@dataclass(frozen=True)
class Segment:
    start: tuple[float, float]
    end: tuple[float, float]

    def y_at(self, x: float) -> float:
        x0, y0 = self.start
        x1, y1 = self.end
        if abs(x1 - x0) < 1e-12:
            return min(y0, y1)
        t = (x - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)


def angle_sort(points: np.ndarray, center: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    c = np.asarray(center, dtype=float)
    order = sorted(range(len(pts)), key=lambda i: atan2(pts[i, 1] - c[1], pts[i, 0] - c[0]))
    return pts[order]
