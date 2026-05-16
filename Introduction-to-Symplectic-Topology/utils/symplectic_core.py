"""Small numerical models used by the symplectic topology notebooks."""

from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np


def standard_j(n: int = 1) -> np.ndarray:
    """Return the standard complex/symplectic matrix in q,p coordinates."""
    eye = np.eye(n)
    zero = np.zeros((n, n))
    return np.block([[zero, eye], [-eye, zero]])


def omega_matrix(n: int = 1) -> np.ndarray:
    """Matrix for omega(v,w)=v^T J w in q,p coordinates."""
    return standard_j(n)


def symplectic_residual(matrix: np.ndarray, n: int | None = None) -> float:
    matrix = np.asarray(matrix, dtype=float)
    if n is None:
        n = matrix.shape[0] // 2
    j = omega_matrix(n)
    return float(np.linalg.norm(matrix.T @ j @ matrix - j, ord="fro"))


def is_symplectic(matrix: np.ndarray, tol: float = 1e-9) -> bool:
    return symplectic_residual(matrix) < tol


def harmonic_flow(times: np.ndarray, initial: Iterable[float] = (1.0, 0.0), frequency: float = 1.0) -> np.ndarray:
    """Exact Hamiltonian flow for H=(p^2+w^2 q^2)/2 in one degree of freedom."""
    q0, p0 = np.asarray(tuple(initial), dtype=float)
    times = np.asarray(times, dtype=float)
    q = q0 * np.cos(frequency * times) + p0 / frequency * np.sin(frequency * times)
    p = p0 * np.cos(frequency * times) - frequency * q0 * np.sin(frequency * times)
    return np.column_stack([q, p])


def oscillator_energy(points: np.ndarray, frequency: float = 1.0) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    return 0.5 * (points[:, 1] ** 2 + (frequency * points[:, 0]) ** 2)


def polygon_signed_area(points: np.ndarray) -> float:
    points = np.asarray(points, dtype=float)
    x = points[:, 0]
    y = points[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def linear_hamiltonian_matrix(kq: float = 1.0, kp: float = 1.0) -> np.ndarray:
    """Hamiltonian matrix X=J grad H for H=(kq q^2+kp p^2)/2."""
    return np.array([[0.0, kp], [-kq, 0.0]])


def moment_map_c2(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=complex)
    return 0.5 * np.abs(z) ** 2


def smooth_step(x: np.ndarray) -> np.ndarray:
    """C-infinity step from 0 to 1 on (0,1), evaluated stably."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    out[x >= 1.0] = 1.0
    mask = (x > 0.0) & (x < 1.0)
    a = np.exp(-1.0 / x[mask])
    b = np.exp(-1.0 / (1.0 - x[mask]))
    out[mask] = a / (a + b)
    return out


def finite_difference(values: np.ndarray, xs: np.ndarray) -> np.ndarray:
    return np.gradient(np.asarray(values, dtype=float), np.asarray(xs, dtype=float), edge_order=2)


def wrap_angle(angle: float) -> float:
    return float((angle + math.pi) % (2 * math.pi) - math.pi)


def torus_morse_function(x: np.ndarray, y: np.ndarray, eps: float = 0.18) -> np.ndarray:
    return np.cos(x) + np.cos(y) + eps * np.cos(x + y)


def action_landscape(q0: np.ndarray, q1: np.ndarray, coupling: float = 0.35) -> np.ndarray:
    return 0.5 * (q1 - q0) ** 2 + coupling * (np.cos(q0) + np.cos(q1))
