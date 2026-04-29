"""Small graphics math helpers used across chapters."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def normalize(v: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    norm = np.linalg.norm(arr)
    if norm < eps:
        raise ValueError("cannot normalize a near-zero vector")
    return arr / norm


def stable_quadratic_roots(a: float, b: float, c: float) -> tuple[float, float] | None:
    disc = b * b - 4.0 * a * c
    if disc < 0:
        return None
    sqrt_disc = float(np.sqrt(disc))
    q = -0.5 * (b + np.copysign(sqrt_disc, b if b != 0 else 1.0))
    if q == 0:
        root = -b / (2.0 * a)
        return root, root
    roots = (q / a, c / q)
    return tuple(sorted(float(r) for r in roots))


def barycentric_2d(p: np.ndarray, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    p, a, b, c = [np.asarray(x, dtype=float)[:2] for x in (p, a, b, c)]
    mat = np.column_stack((a - c, b - c))
    alpha, beta = np.linalg.solve(mat, p - c)
    gamma = 1.0 - alpha - beta
    return np.array([alpha, beta, gamma])


def triangle_area(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    a, b, c = [np.asarray(x, dtype=float) for x in (a, b, c)]
    return 0.5 * float(np.linalg.norm(np.cross(b - a, c - a)))


def signed_area2(points: np.ndarray) -> float:
    pts = np.asarray(points, dtype=float)
    x = pts[:, 0]
    y = pts[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


@dataclass(frozen=True)
class Interval:
    lo: float
    hi: float

    def intersect(self, other: "Interval") -> "Interval | None":
        lo = max(self.lo, other.lo)
        hi = min(self.hi, other.hi)
        return Interval(lo, hi) if lo <= hi else None

    def contains(self, x: float) -> bool:
        return self.lo <= x <= self.hi
