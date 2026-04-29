"""Mobius, inversion, and stereographic helpers."""

from __future__ import annotations

import numpy as np


def mobius(z: complex | np.ndarray, a: complex, b: complex, c: complex, d: complex) -> complex | np.ndarray:
    return (a * z + b) / (c * z + d)


def disk_automorphism(z: complex | np.ndarray, a: complex, theta: float = 0.0) -> complex | np.ndarray:
    lam = np.exp(1j * theta)
    return lam * (z - a) / (1 - np.conjugate(a) * z)


def cross_ratio(z1: complex, z2: complex, z3: complex, z4: complex) -> complex:
    return ((z1 - z3) * (z2 - z4)) / ((z1 - z4) * (z2 - z3))


def invert_in_circle(z: complex | np.ndarray, center: complex = 0j, radius: float = 1.0) -> complex | np.ndarray:
    shifted = z - center
    return center + (radius**2) / np.conjugate(shifted)


def antipode(z: complex) -> complex:
    if abs(z) < 1e-12:
        raise ZeroDivisionError("0 is paired with infinity in the extended plane")
    return -1 / np.conjugate(z)


def stereographic(point: np.ndarray) -> complex:
    x, y, z = point
    if abs(1 - z) < 1e-12:
        raise ZeroDivisionError("north pole projects to infinity")
    return complex(x / (1 - z), y / (1 - z))


def inverse_stereographic(z: complex) -> np.ndarray:
    r2 = abs(z) ** 2
    return np.array([2 * z.real / (r2 + 1), 2 * z.imag / (r2 + 1), (r2 - 1) / (r2 + 1)])


def classify_mobius_multiplier(multiplier: complex, tol: float = 1e-8) -> str:
    radius = abs(multiplier)
    angle = abs(np.angle(multiplier))
    if abs(radius - 1) < tol and angle > tol:
        return "elliptic"
    if angle < tol and abs(radius - 1) > tol:
        return "hyperbolic"
    if abs(radius - 1) > tol and angle > tol:
        return "loxodromic"
    return "parabolic-or-identity"
