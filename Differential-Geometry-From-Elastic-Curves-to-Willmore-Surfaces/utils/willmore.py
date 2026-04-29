"""Willmore-energy helpers."""

from __future__ import annotations

import numpy as np


def willmore_density(h: np.ndarray, area: np.ndarray) -> np.ndarray:
    return h * h * area


def conformal_willmore_density(h: np.ndarray, k: np.ndarray, area: np.ndarray) -> np.ndarray:
    return (h * h - k) * area


def sphere_willmore_energy(radius: float = 1.0) -> float:
    import math

    h = 1.0 / radius
    return 4.0 * math.pi * radius * radius * h * h


def invert_points(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    denom = np.sum(pts * pts, axis=-1, keepdims=True)
    return pts / denom
