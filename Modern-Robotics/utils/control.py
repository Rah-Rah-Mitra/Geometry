"""Control helpers for Modern Robotics teaching notebooks."""

from __future__ import annotations

import numpy as np


def pd_response(kp: float, kd: float, *, dt: float = 0.01, steps: int = 500, target: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    t = np.arange(steps) * dt
    state = np.zeros((steps, 2))
    for k in range(1, steps):
        q, qd = state[k - 1]
        qdd = kp * (target - q) - kd * qd
        state[k, 1] = qd + dt * qdd
        state[k, 0] = q + dt * state[k, 1]
    return t, state


def impedance_force(stiffness: float, damping: float, position_error: np.ndarray, velocity_error: np.ndarray) -> np.ndarray:
    return stiffness * np.asarray(position_error, dtype=float) + damping * np.asarray(velocity_error, dtype=float)


def hybrid_projection(mask: np.ndarray) -> np.ndarray:
    mask = np.asarray(mask, dtype=float)
    return np.diag(mask)

