from __future__ import annotations

import cmath
import math

import numpy as np


def mobius(z: complex, a: complex, b: complex, c: complex, d: complex) -> complex:
    return (a * z + b) / (c * z + d)


def stereographic_to_sphere(z: complex) -> np.ndarray:
    r2 = z.real * z.real + z.imag * z.imag
    return np.array([2 * z.real / (1 + r2), 2 * z.imag / (1 + r2), (r2 - 1) / (1 + r2)])


def sphere_to_stereographic(point: np.ndarray) -> complex:
    x, y, z = np.asarray(point, dtype=float)
    den = 1 - z
    if abs(den) < 1e-12:
        return complex(math.inf, math.inf)
    return complex(x / den, y / den)


def klein_to_poincare(point: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    r2 = float(p @ p)
    den = 1 + math.sqrt(max(0.0, 1 - r2))
    return p / den


def poincare_to_klein(point: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    r2 = float(p @ p)
    return 2 * p / (1 + r2)


def poincare_distance(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    dpq = float(np.sum((p - q) ** 2))
    pp = float(np.sum(p**2))
    qq = float(np.sum(q**2))
    arg = 1 + 2 * dpq / ((1 - pp) * (1 - qq))
    return float(math.acosh(max(1.0, arg)))


def disk_geodesic_points(angle_a: float, angle_b: float, samples: int = 160) -> np.ndarray:
    a = np.array([math.cos(angle_a), math.sin(angle_a)])
    b = np.array([math.cos(angle_b), math.sin(angle_b)])
    if abs((angle_b - angle_a + math.pi) % (2 * math.pi) - math.pi) < 1e-8:
        ts = np.linspace(-0.96, 0.96, samples)
        return np.outer(ts, a)
    mid = (a + b) / 2
    chord = b - a
    normal = np.array([-chord[1], chord[0]])
    normal /= np.linalg.norm(normal)
    center = mid + normal * ((1 - float(mid @ mid)) / max(1e-12, 2 * float(mid @ normal)))
    radius = np.linalg.norm(a - center)
    theta_a = math.atan2(a[1] - center[1], a[0] - center[0])
    theta_b = math.atan2(b[1] - center[1], b[0] - center[0])
    if theta_b < theta_a:
        theta_b += 2 * math.pi
    if theta_b - theta_a > math.pi:
        theta_a, theta_b = theta_b, theta_a + 2 * math.pi
    ts = np.linspace(theta_a, theta_b, samples)
    return np.column_stack([center[0] + radius * np.cos(ts), center[1] + radius * np.sin(ts)])


def circular_points() -> tuple[np.ndarray, np.ndarray]:
    return np.array([1.0, 1.0j, 0.0], dtype=complex), np.array([1.0, -1.0j, 0.0], dtype=complex)


def complex_roots_on_unit_circle(n: int) -> list[complex]:
    return [cmath.exp(2j * math.pi * k / n) for k in range(n)]

