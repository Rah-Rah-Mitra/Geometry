"""Small dynamics and control helpers for planar robotics examples."""

from __future__ import annotations

import numpy as np


def two_link_inertia(q: np.ndarray, lengths=(1.0, 0.8), masses=(1.0, 0.8)) -> np.ndarray:
    q1, q2 = np.asarray(q, dtype=float)
    l1, l2 = lengths
    m1, m2 = masses
    lc1, lc2 = l1 / 2, l2 / 2
    I1, I2 = m1 * l1**2 / 12, m2 * l2**2 / 12
    c2 = np.cos(q2)
    M11 = I1 + I2 + m1 * lc1**2 + m2 * (l1**2 + lc2**2 + 2 * l1 * lc2 * c2)
    M12 = I2 + m2 * (lc2**2 + l1 * lc2 * c2)
    M22 = I2 + m2 * lc2**2
    return np.array([[M11, M12], [M12, M22]])


def two_link_coriolis(q: np.ndarray, qdot: np.ndarray, lengths=(1.0, 0.8), masses=(1.0, 0.8)) -> np.ndarray:
    _, q2 = np.asarray(q, dtype=float)
    q1d, q2d = np.asarray(qdot, dtype=float)
    l1, l2 = lengths
    m2 = masses[1]
    lc2 = l2 / 2
    h = -m2 * l1 * lc2 * np.sin(q2)
    return np.array([[h * q2d, h * (q1d + q2d)], [-h * q1d, 0.0]])


def pd_second_order_response(kp: float = 16.0, kd: float = 7.0, x0: float = 1.0, v0: float = 0.0, dt: float = 0.01, steps: int = 500) -> tuple[np.ndarray, np.ndarray]:
    state = np.array([x0, v0], dtype=float)
    hist = []
    for i in range(steps):
        t = i * dt
        hist.append([t, state[0], state[1], 0.5 * state[1] ** 2 + 0.5 * kp * state[0] ** 2])
        acc = -kd * state[1] - kp * state[0]
        state[0] += dt * state[1]
        state[1] += dt * acc
    data = np.asarray(hist)
    return data[:, 0], data[:, 1:]


def lyapunov_grid(samples: int = 40, kp: float = 4.0, kd: float = 1.2) -> dict[str, float]:
    xs = np.linspace(-1.5, 1.5, samples)
    max_vdot = -np.inf
    min_v = np.inf
    for x in xs:
        for v in xs:
            V = 0.5 * v**2 + 0.5 * kp * x**2
            Vdot = v * (-kd * v - kp * x) + kp * x * v
            min_v = min(min_v, V)
            max_vdot = max(max_vdot, Vdot)
    return {"min_V": float(min_v), "max_Vdot": float(max_vdot)}
