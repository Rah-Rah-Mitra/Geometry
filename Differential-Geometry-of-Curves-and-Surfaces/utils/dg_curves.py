"""Numerical helpers for curves in R2 and R3."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

Array = np.ndarray
Curve = Callable[[Array], Array]


def finite_difference(values: Array, t: Array, order: int = 1) -> Array:
    """Differentiate sampled vector values with respect to the parameter."""

    result = np.asarray(values, dtype=float)
    for _ in range(order):
        result = np.gradient(result, t, axis=0, edge_order=2)
    return result


def speed(samples: Array, t: Array) -> Array:
    """Return speed from sampled curve values."""

    velocity = finite_difference(samples, t)
    return np.linalg.norm(velocity, axis=1)


def cumulative_arc_length(samples: Array, t: Array) -> Array:
    """Return trapezoidal cumulative arc length for sampled curve values."""

    v = speed(samples, t)
    increments = 0.5 * (v[1:] + v[:-1]) * np.diff(t)
    return np.concatenate([[0.0], np.cumsum(increments)])


def curvature_3d(samples: Array, t: Array) -> Array:
    """Estimate curvature for a sampled R3 curve."""

    r1 = finite_difference(samples, t)
    r2 = finite_difference(samples, t, order=2)
    numerator = np.linalg.norm(np.cross(r1, r2), axis=1)
    denominator = np.linalg.norm(r1, axis=1) ** 3
    return np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator > 1e-12)


def torsion_3d(samples: Array, t: Array) -> Array:
    """Estimate torsion using do Carmo's Frenet sign convention.

    With B = T x N, do Carmo writes B' = tau N. This is the negative of the
    determinant convention used by many texts for the standard right-handed
    helix parametrization.
    """

    r1 = finite_difference(samples, t)
    r2 = finite_difference(samples, t, order=2)
    r3 = finite_difference(samples, t, order=3)
    cross = np.cross(r1, r2)
    numerator = np.einsum("ij,ij->i", cross, r3)
    denominator = np.einsum("ij,ij->i", cross, cross)
    return -np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator > 1e-12)


def frenet_frame(samples: Array, t: Array) -> tuple[Array, Array, Array]:
    """Estimate tangent, normal, and binormal frames for a sampled R3 curve."""

    velocity = finite_difference(samples, t)
    tangent = velocity / np.linalg.norm(velocity, axis=1, keepdims=True)
    tangent_derivative = finite_difference(tangent, t)
    normal_norm = np.linalg.norm(tangent_derivative, axis=1, keepdims=True)
    normal = np.divide(tangent_derivative, normal_norm, out=np.zeros_like(tangent_derivative), where=normal_norm > 1e-12)
    binormal = np.cross(tangent, normal)
    return tangent, normal, binormal


def osculating_circle(center_point: Array, tangent: Array, normal: Array, radius: float, samples: int = 200) -> Array:
    """Sample the osculating circle in the tangent-normal plane."""

    theta = np.linspace(0.0, 2.0 * np.pi, samples)
    center = center_point + radius * normal
    return center + radius * (np.cos(theta)[:, None] * (-normal) + np.sin(theta)[:, None] * tangent)
