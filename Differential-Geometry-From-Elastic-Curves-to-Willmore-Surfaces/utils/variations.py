"""Variation and bump-function helpers."""

from __future__ import annotations

import numpy as np


def flat_step(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    mask = x > 0
    out[mask] = np.exp(-1.0 / x[mask])
    return out


def bump(x: np.ndarray, center: float = 0.0, radius: float = 1.0) -> np.ndarray:
    z = 1.0 - ((np.asarray(x, dtype=float) - center) / radius) ** 2
    out = np.zeros_like(z)
    mask = z > 0
    out[mask] = np.exp(-1.0 / z[mask])
    if out.max() > 0:
        out = out / out.max()
    return out


def radial_bump(x: np.ndarray, y: np.ndarray, radius: float = 1.0) -> np.ndarray:
    r2 = (np.asarray(x) ** 2 + np.asarray(y) ** 2) / (radius * radius)
    z = 1.0 - r2
    out = np.zeros_like(z, dtype=float)
    mask = z > 0
    out[mask] = np.exp(-1.0 / z[mask])
    if out.max() > 0:
        out = out / out.max()
    return out


def finite_difference(function, value: float, step: float = 1e-4) -> float:
    return float((function(value + step) - function(value - step)) / (2 * step))
