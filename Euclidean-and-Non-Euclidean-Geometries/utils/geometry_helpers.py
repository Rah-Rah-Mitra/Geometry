"""Small Euclidean helpers used by the ENEG notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


ArrayLike = Sequence[float] | np.ndarray


@dataclass(frozen=True)
class Line:
    point: np.ndarray
    direction: np.ndarray

    @classmethod
    def through(cls, p: ArrayLike, q: ArrayLike) -> "Line":
        p_arr = np.asarray(p, dtype=float)
        q_arr = np.asarray(q, dtype=float)
        direction = q_arr - p_arr
        norm = np.linalg.norm(direction)
        if norm == 0:
            raise ValueError("A line needs two distinct points")
        return cls(p_arr, direction / norm)


def vector(p: ArrayLike, q: ArrayLike) -> np.ndarray:
    return np.asarray(q, dtype=float) - np.asarray(p, dtype=float)


def norm(v: ArrayLike) -> float:
    return float(np.linalg.norm(np.asarray(v, dtype=float)))


def unit(v: ArrayLike) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    length = np.linalg.norm(arr)
    if length == 0:
        raise ValueError("zero vector has no direction")
    return arr / length


def angle_between(u: ArrayLike, v: ArrayLike) -> float:
    u_arr = unit(u)
    v_arr = unit(v)
    dot = float(np.clip(np.dot(u_arr, v_arr), -1.0, 1.0))
    return float(math.acos(dot))


def oriented_area(a: ArrayLike, b: ArrayLike, c: ArrayLike) -> float:
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    c_arr = np.asarray(c, dtype=float)
    u = b_arr - a_arr
    v = c_arr - a_arr
    return float((u[0] * v[1] - u[1] * v[0]) / 2)


def line_intersection(line_a: Line, line_b: Line, *, eps: float = 1e-10) -> np.ndarray | None:
    p = line_a.point
    r = line_a.direction
    q = line_b.point
    s = line_b.direction
    cross = r[0] * s[1] - r[1] * s[0]
    if abs(cross) < eps:
        return None
    qp = q - p
    t = (qp[0] * s[1] - qp[1] * s[0]) / cross
    return p + t * r


def reflect_point_across_line(point: ArrayLike, line: Line) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    base = line.point
    direction = line.direction
    projection = base + np.dot(p - base, direction) * direction
    return 2 * projection - p


def rotate(point: ArrayLike, angle: float, *, center: ArrayLike = (0.0, 0.0)) -> np.ndarray:
    p = np.asarray(point, dtype=float) - np.asarray(center, dtype=float)
    c = math.cos(angle)
    s = math.sin(angle)
    result = np.array([c * p[0] - s * p[1], s * p[0] + c * p[1]])
    return result + np.asarray(center, dtype=float)


def circle_from_three_points(a: ArrayLike, b: ArrayLike, c: ArrayLike) -> tuple[np.ndarray, float]:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    c = np.asarray(c, dtype=float)
    matrix = np.array([[2 * (b[0] - a[0]), 2 * (b[1] - a[1])], [2 * (c[0] - a[0]), 2 * (c[1] - a[1])]])
    rhs = np.array([
        b[0] ** 2 + b[1] ** 2 - a[0] ** 2 - a[1] ** 2,
        c[0] ** 2 + c[1] ** 2 - a[0] ** 2 - a[1] ** 2,
    ])
    center = np.linalg.solve(matrix, rhs)
    return center, norm(center - a)
