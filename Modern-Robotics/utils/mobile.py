"""Wheeled mobile robot helpers."""

from __future__ import annotations

import numpy as np


def unicycle_rollout(controls: np.ndarray, *, dt: float = 0.05, q0: np.ndarray | None = None) -> np.ndarray:
    controls = np.asarray(controls, dtype=float)
    q = np.zeros(3) if q0 is None else np.asarray(q0, dtype=float).copy()
    path = [q.copy()]
    for v, w in controls:
        q[0] += dt * w
        q[1] += dt * v * np.cos(q[0])
        q[2] += dt * v * np.sin(q[0])
        path.append(q.copy())
    return np.asarray(path)


def mecanum_wheel_matrix(length: float = 0.35, width: float = 0.25, radius: float = 0.05) -> np.ndarray:
    a = length + width
    return (1 / radius) * np.array(
        [
            [-a, 1.0, -1.0],
            [a, 1.0, 1.0],
            [a, 1.0, -1.0],
            [-a, 1.0, 1.0],
        ]
    )

