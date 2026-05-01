"""Tiny dynamics models for teaching robot mass, torque, and energy geometry."""

from __future__ import annotations

import numpy as np


def two_link_mass_matrix(theta2: float, *, m1: float = 1.0, m2: float = 0.8, l1: float = 1.0, l2: float = 0.8) -> np.ndarray:
    c2 = np.cos(theta2)
    a = m1 * l1**2 / 3 + m2 * (l1**2 + l2**2 / 3)
    b = m2 * l1 * l2 / 2
    d = m2 * l2**2 / 3
    return np.array([[a + 2 * b * c2, d + b * c2], [d + b * c2, d]])


def kinetic_energy(M: np.ndarray, qdot: np.ndarray) -> float:
    qdot = np.asarray(qdot, dtype=float)
    return float(0.5 * qdot @ np.asarray(M, dtype=float) @ qdot)


def simulate_second_order(
    *,
    kp: float,
    kd: float,
    inertia: float = 1.0,
    target: float = 1.0,
    dt: float = 0.01,
    steps: int = 600,
) -> tuple[np.ndarray, np.ndarray]:
    t = np.arange(steps) * dt
    x = np.zeros((steps, 2))
    for k in range(1, steps):
        q, qd = x[k - 1]
        torque = kp * (target - q) - kd * qd
        qdd = torque / inertia
        x[k, 1] = qd + dt * qdd
        x[k, 0] = q + dt * x[k, 1]
    return t, x


def apparent_inertia_curve(gear_ratios: np.ndarray, motor_inertia: float = 0.02, load_inertia: float = 1.0) -> np.ndarray:
    ratios = np.asarray(gear_ratios, dtype=float)
    return load_inertia + ratios**2 * motor_inertia

