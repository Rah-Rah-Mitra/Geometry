"""Metric model helpers for elliptic, Euclidean, and hyperbolic geometry."""

from __future__ import annotations

import math

import numpy as np


def hyperbolic_distance(p: complex, q: complex) -> float:
    numerator = abs(p - q) ** 2
    denominator = (1 - abs(p) ** 2) * (1 - abs(q) ** 2)
    return float(np.arccosh(1 + 2 * numerator / denominator))


def elliptic_distance(p: complex, q: complex) -> float:
    numerator = abs(p - q)
    denominator = abs(1 + np.conjugate(p) * q)
    return float(2 * np.arctan2(numerator, denominator))


def circumference_k(radius: float | np.ndarray, k: float) -> float | np.ndarray:
    r = np.asarray(radius)
    if abs(k) < 1e-12:
        return 2 * np.pi * r
    scale = math.sqrt(abs(k))
    if k > 0:
        return 2 * np.pi * np.sin(scale * r) / scale
    return 2 * np.pi * np.sinh(scale * r) / scale


def disk_area_k(radius: float | np.ndarray, k: float) -> float | np.ndarray:
    r = np.asarray(radius)
    if abs(k) < 1e-12:
        return np.pi * r**2
    scale = math.sqrt(abs(k))
    if k > 0:
        return 2 * np.pi * (1 - np.cos(scale * r)) / k
    return 2 * np.pi * (np.cosh(scale * r) - 1) / abs(k)


def triangle_area_from_angles(alpha: float, beta: float, gamma: float, k: float) -> float:
    excess = alpha + beta + gamma - math.pi
    if abs(k) < 1e-12:
        return 0.0
    return excess / k


def angle_of_parallelism(distance: float, k: float = -1.0) -> float:
    if k >= 0:
        raise ValueError("Angle of parallelism belongs to negative curvature")
    return float(2 * np.arctan(np.exp(-math.sqrt(abs(k)) * distance)))


def unified_right_hypotenuse(a: float, k: float) -> float:
    if abs(k) < 1e-12:
        return math.sqrt(2) * a
    scale = math.sqrt(abs(k))
    if k > 0:
        return math.acos(math.cos(scale * a) ** 2) / scale
    return math.acosh(math.cosh(scale * a) ** 2) / scale
