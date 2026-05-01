"""Small Euclidean construction and measurement helpers."""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np

Point = tuple[float, float]


def as_point(value: Sequence[float]) -> np.ndarray:
    return np.asarray(value, dtype=float)


def distance(a: Sequence[float], b: Sequence[float]) -> float:
    return float(np.linalg.norm(as_point(a) - as_point(b)))


def midpoint(a: Sequence[float], b: Sequence[float]) -> Point:
    p = (as_point(a) + as_point(b)) / 2
    return float(p[0]), float(p[1])


def orientation(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    pa, pb, pc = as_point(a), as_point(b), as_point(c)
    return float(np.cross(pb - pa, pc - pa))


def polygon_area(points: Sequence[Sequence[float]]) -> float:
    pts = np.asarray(points, dtype=float)
    x, y = pts[:, 0], pts[:, 1]
    return float(0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def regular_polygon(n: int, *, radius: float = 1.0, center: Sequence[float] = (0.0, 0.0), phase: float = 0.0) -> np.ndarray:
    angles = phase + np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    c = as_point(center)
    return np.column_stack([c[0] + radius * np.cos(angles), c[1] + radius * np.sin(angles)])


def angle(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    """Return the angle ABC in radians."""

    ba = as_point(a) - as_point(b)
    bc = as_point(c) - as_point(b)
    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom == 0:
        raise ValueError("angle is undefined for coincident points")
    cosine = float(np.clip(np.dot(ba, bc) / denom, -1.0, 1.0))
    return math.acos(cosine)


def line_circle_intersections(
    a: Sequence[float],
    b: Sequence[float],
    center: Sequence[float],
    radius: float,
) -> list[Point]:
    """Intersect an infinite line through `a`, `b` with a circle."""

    p = as_point(a)
    d = as_point(b) - p
    c = as_point(center)
    qa = float(np.dot(d, d))
    qb = 2.0 * float(np.dot(d, p - c))
    qc = float(np.dot(p - c, p - c) - radius * radius)
    disc = qb * qb - 4.0 * qa * qc
    if disc < -1e-12:
        return []
    if abs(disc) < 1e-12:
        ts = [-qb / (2.0 * qa)]
    else:
        root = math.sqrt(max(0.0, disc))
        ts = [(-qb - root) / (2.0 * qa), (-qb + root) / (2.0 * qa)]
    points = [p + t * d for t in ts]
    return [(float(x), float(y)) for x, y in points]


def circle_circle_intersections(
    c0: Sequence[float],
    r0: float,
    c1: Sequence[float],
    r1: float,
) -> list[Point]:
    p0, p1 = as_point(c0), as_point(c1)
    d = float(np.linalg.norm(p1 - p0))
    if d == 0 or d > r0 + r1 + 1e-12 or d < abs(r0 - r1) - 1e-12:
        return []
    a = (r0 * r0 - r1 * r1 + d * d) / (2.0 * d)
    h2 = r0 * r0 - a * a
    base = p0 + a * (p1 - p0) / d
    if abs(h2) < 1e-12:
        return [(float(base[0]), float(base[1]))]
    h = math.sqrt(max(0.0, h2))
    perp = np.array([-(p1 - p0)[1], (p1 - p0)[0]]) / d
    pts = [base + h * perp, base - h * perp]
    return [(float(x), float(y)) for x, y in pts]


def construct_equilateral(a: Sequence[float], b: Sequence[float]) -> tuple[Point, Point]:
    """Return the two third vertices of equilateral triangles on segment AB."""

    return tuple(circle_circle_intersections(a, distance(a, b), b, distance(a, b)))  # type: ignore[return-value]


def affine_map(points: Sequence[Sequence[float]], matrix: Sequence[Sequence[float]], offset: Sequence[float] = (0.0, 0.0)) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    mat = np.asarray(matrix, dtype=float)
    off = as_point(offset)
    return pts @ mat.T + off
