"""Planar grasp and force-closure helpers."""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog
from scipy.linalg import null_space


def planar_wrench(point: np.ndarray, force: np.ndarray) -> np.ndarray:
    p = np.asarray(point, dtype=float).reshape(2)
    f = np.asarray(force, dtype=float).reshape(2)
    tau = p[0] * f[1] - p[1] * f[0]
    return np.r_[f, tau]


def friction_cone_edges(normal: np.ndarray, mu: float) -> np.ndarray:
    n = np.asarray(normal, dtype=float).reshape(2)
    n = n / np.linalg.norm(n)
    t = np.array([-n[1], n[0]])
    edges = [n + mu * t, n - mu * t]
    return np.asarray([e / np.linalg.norm(e) for e in edges])


def grasp_wrenches(points: list[np.ndarray], normals: list[np.ndarray], mu: float = 0.5) -> np.ndarray:
    columns = []
    for point, normal in zip(points, normals):
        for force in friction_cone_edges(normal, mu):
            columns.append(planar_wrench(point, force))
    return np.asarray(columns).T


def origin_in_convex_hull(columns: np.ndarray, tol: float = 1e-8) -> bool:
    W = np.asarray(columns, dtype=float)
    n = W.shape[1]
    A_eq = np.vstack([W, np.ones((1, n))])
    b_eq = np.r_[np.zeros(W.shape[0]), 1.0]
    result = linprog(np.zeros(n), A_eq=A_eq, b_eq=b_eq, bounds=[(0, None)] * n, method="highs")
    return bool(result.success and np.linalg.norm(A_eq @ result.x - b_eq) <= tol * 100)


def internal_force_basis(G: np.ndarray) -> np.ndarray:
    return null_space(np.asarray(G, dtype=float))
