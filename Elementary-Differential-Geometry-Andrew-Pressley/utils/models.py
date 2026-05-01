"""Spherical and hyperbolic model helpers for the Pressley course."""

from __future__ import annotations

import numpy as np


def stereographic(point: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    denom = 1.0 - p[..., 2]
    return p[..., :2] / np.maximum(denom[..., None], 1e-12)


def inverse_stereographic(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    r2 = np.sum(z**2, axis=-1)
    denom = 1.0 + r2
    return np.stack([2.0 * z[..., 0] / denom, 2.0 * z[..., 1] / denom, (r2 - 1.0) / denom], axis=-1)


def mobius(z: np.ndarray | complex, a: complex, b: complex, c: complex, d: complex) -> np.ndarray | complex:
    return (a * z + b) / (c * z + d)


def cross_ratio(a: complex, b: complex, c: complex, d: complex) -> complex:
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def poincare_disk_distance(z: complex, w: complex) -> float:
    numerator = abs(z - w) ** 2
    denominator = (1.0 - abs(z) ** 2) * (1.0 - abs(w) ** 2)
    return float(np.arccosh(1.0 + 2.0 * numerator / denominator))


def upper_half_plane_distance(z: complex, w: complex) -> float:
    numerator = abs(z - w) ** 2
    denominator = 2.0 * z.imag * w.imag
    return float(np.arccosh(1.0 + numerator / denominator))


def poincare_to_klein(z: complex) -> complex:
    return 2.0 * z / (1.0 + abs(z) ** 2)


def klein_to_poincare(z: complex) -> complex:
    r2 = abs(z) ** 2
    if r2 == 0:
        return 0j
    return z / (1.0 + np.sqrt(max(0.0, 1.0 - r2)))
