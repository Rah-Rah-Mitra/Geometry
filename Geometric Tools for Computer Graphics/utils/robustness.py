"""Numerical robustness helpers."""

from __future__ import annotations

import math
import numpy as np


def robust_quadratic_roots(a: float, b: float, c: float, tol: float = 1e-14) -> tuple[float, ...]:
    if abs(a) <= tol:
        if abs(b) <= tol:
            return tuple()
        return (-c / b,)
    disc_raw = b * b - 4.0 * a * c
    if disc_raw < -tol:
        return tuple()
    disc = max(0.0, disc_raw)
    root = math.sqrt(disc)
    q = -0.5 * (b + math.copysign(root, b if b != 0 else 1.0))
    if abs(q) <= tol:
        repeated = -b / (2.0 * a)
        return (repeated,)
    r1 = q / a
    r2 = c / q
    return (min(r1, r2), max(r1, r2))


def orientation2d(a: np.ndarray, b: np.ndarray, c: np.ndarray, eps: float = 1e-12) -> int:
    det = float(np.cross(np.asarray(b) - np.asarray(a), np.asarray(c) - np.asarray(a)))
    if det > eps:
        return 1
    if det < -eps:
        return -1
    return 0


def clamp_unit(value: float) -> float:
    return min(1.0, max(-1.0, float(value)))
