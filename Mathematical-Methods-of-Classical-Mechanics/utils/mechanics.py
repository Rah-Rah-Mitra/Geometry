"""Small numerical mechanics helpers used by the Arnold notebooks."""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
from scipy.integrate import solve_ivp


def symplectic_matrix(n: int) -> np.ndarray:
    """Return the canonical symplectic matrix for coordinates (q, p)."""
    zero = np.zeros((n, n))
    ident = np.eye(n)
    return np.block([[zero, ident], [-ident, zero]])


def harmonic_solution(t: np.ndarray, q0: float = 1.0, p0: float = 0.0, omega: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    q = q0 * np.cos(omega * t) + p0 / omega * np.sin(omega * t)
    p = -omega * q0 * np.sin(omega * t) + p0 * np.cos(omega * t)
    return q, p


def pendulum_energy(theta: np.ndarray, momentum: np.ndarray) -> np.ndarray:
    return 0.5 * momentum**2 + 1.0 - np.cos(theta)


def kepler_orbit(eccentricity: float = 0.5, semi_latus: float = 1.0, samples: int = 600) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    angle = np.linspace(0, 2 * np.pi, samples)
    radius = semi_latus / (1 + eccentricity * np.cos(angle))
    return radius * np.cos(angle), radius * np.sin(angle), radius


def solve_planar(
    rhs: Callable[[float, np.ndarray], np.ndarray],
    y0: np.ndarray,
    t_end: float,
    samples: int = 800,
    *,
    rtol: float = 1e-9,
    atol: float = 1e-11,
) -> tuple[np.ndarray, np.ndarray]:
    t_eval = np.linspace(0.0, t_end, samples)
    sol = solve_ivp(rhs, (0.0, t_end), y0, t_eval=t_eval, rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.t, sol.y


def euler_top(inertia: tuple[float, float, float], omega0: tuple[float, float, float], t_end: float = 35.0) -> tuple[np.ndarray, np.ndarray]:
    i1, i2, i3 = inertia

    def rhs(_t: float, w: np.ndarray) -> np.ndarray:
        w1, w2, w3 = w
        return np.array(
            [
                ((i2 - i3) / i1) * w2 * w3,
                ((i3 - i1) / i2) * w3 * w1,
                ((i1 - i2) / i3) * w1 * w2,
            ]
        )

    return solve_planar(rhs, np.array(omega0, dtype=float), t_end, samples=900)


def standard_map(kick: float, q0: float, p0: float, steps: int = 500) -> tuple[np.ndarray, np.ndarray]:
    q = np.empty(steps)
    p = np.empty(steps)
    q[0] = q0 % (2 * np.pi)
    p[0] = p0 % (2 * np.pi)
    for idx in range(1, steps):
        p[idx] = (p[idx - 1] + kick * np.sin(q[idx - 1])) % (2 * np.pi)
        q[idx] = (q[idx - 1] + p[idx]) % (2 * np.pi)
    return q, p


def polygon_area(x: np.ndarray, y: np.ndarray) -> float:
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def verlet_oscillator(q0: float, p0: float, step: float, steps: int, omega: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    q = np.empty(steps + 1)
    p = np.empty(steps + 1)
    q[0], p[0] = q0, p0
    for idx in range(steps):
        p_half = p[idx] - 0.5 * step * omega**2 * q[idx]
        q[idx + 1] = q[idx] + step * p_half
        p[idx + 1] = p_half - 0.5 * step * omega**2 * q[idx + 1]
    return q, p


def explicit_euler_oscillator(q0: float, p0: float, step: float, steps: int, omega: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    q = np.empty(steps + 1)
    p = np.empty(steps + 1)
    q[0], p[0] = q0, p0
    for idx in range(steps):
        q[idx + 1] = q[idx] + step * p[idx]
        p[idx + 1] = p[idx] - step * omega**2 * q[idx]
    return q, p


def torus_winding(omega: tuple[float, float], samples: int = 900, turns: float = 40.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t = np.linspace(0.0, turns, samples)
    u = (omega[0] * t) % (2 * np.pi)
    v = (omega[1] * t) % (2 * np.pi)
    return t, u, v


def mathieu_tongue(delta: np.ndarray, epsilon: np.ndarray) -> np.ndarray:
    d, e = np.meshgrid(delta, epsilon)
    return np.maximum(0.0, e**2 - (d - 1.0) ** 2)


def kdv_soliton(x: np.ndarray, t: float, speed: float = 1.0, x0: float = 0.0) -> np.ndarray:
    arg = 0.5 * math.sqrt(speed) * (x - speed * t - x0)
    return 0.5 * speed / np.cosh(arg) ** 2


def fold_caustic(parameter: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return parameter**2, parameter


def cusp_caustic(parameter: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return 3 * parameter**2, 2 * parameter**3


def confocal_ellipse(a: float, b: float, samples: int = 400) -> tuple[np.ndarray, np.ndarray]:
    angle = np.linspace(0, 2 * np.pi, samples)
    return a * np.cos(angle), b * np.sin(angle)
