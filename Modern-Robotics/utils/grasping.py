"""Contact and grasping helpers for small planar examples."""

from __future__ import annotations

import numpy as np


def friction_cone(normal: np.ndarray, mu: float, samples: int = 15) -> np.ndarray:
    n = np.asarray(normal, dtype=float)
    n = n / np.linalg.norm(n)
    tangent = np.array([-n[1], n[0]])
    alphas = np.linspace(-mu, mu, samples)
    rays = np.array([n + a * tangent for a in alphas])
    return rays / np.linalg.norm(rays, axis=1, keepdims=True)


def planar_contact_wrench(point: np.ndarray, force: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float)
    f = np.asarray(force, dtype=float)
    torque = p[0] * f[1] - p[1] * f[0]
    return np.r_[torque, f]


def grasp_matrix(points: np.ndarray, normals: np.ndarray) -> np.ndarray:
    columns = []
    for p, n in zip(np.asarray(points, dtype=float), np.asarray(normals, dtype=float)):
        columns.append(planar_contact_wrench(p, n))
    return np.column_stack(columns)

