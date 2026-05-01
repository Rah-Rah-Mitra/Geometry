"""Kinematic helpers for small, inspectable robot examples."""

from __future__ import annotations

import numpy as np

from utils.lie import adjoint, se3_exp


def poe_space(screw_axes: np.ndarray, thetas: np.ndarray, M: np.ndarray) -> np.ndarray:
    T = np.eye(4)
    for axis, theta in zip(np.asarray(screw_axes, dtype=float), np.asarray(thetas, dtype=float)):
        T = T @ se3_exp(axis * theta)
    return T @ np.asarray(M, dtype=float).reshape(4, 4)


def space_jacobian(screw_axes: np.ndarray, thetas: np.ndarray) -> np.ndarray:
    axes = np.asarray(screw_axes, dtype=float)
    thetas = np.asarray(thetas, dtype=float)
    J = np.zeros((6, len(thetas)))
    T = np.eye(4)
    for i, axis in enumerate(axes):
        if i > 0:
            T = T @ se3_exp(axes[i - 1] * thetas[i - 1])
        J[:, i] = adjoint(T) @ axis
    return J


def body_jacobian(body_axes: np.ndarray, thetas: np.ndarray) -> np.ndarray:
    axes = np.asarray(body_axes, dtype=float)
    thetas = np.asarray(thetas, dtype=float)
    J = np.zeros((6, len(thetas)))
    T = np.eye(4)
    for i in reversed(range(len(thetas))):
        J[:, i] = adjoint(T) @ axes[i]
        T = T @ se3_exp(-axes[i] * thetas[i])
    return J


def planar_arm_points(lengths: np.ndarray, thetas: np.ndarray) -> np.ndarray:
    lengths = np.asarray(lengths, dtype=float)
    thetas = np.asarray(thetas, dtype=float)
    angles = np.cumsum(thetas)
    pts = [np.array([0.0, 0.0])]
    p = np.array([0.0, 0.0])
    for length, angle in zip(lengths, angles):
        p = p + length * np.array([np.cos(angle), np.sin(angle)])
        pts.append(p.copy())
    return np.vstack(pts)


def planar_jacobian(lengths: np.ndarray, thetas: np.ndarray) -> np.ndarray:
    lengths = np.asarray(lengths, dtype=float)
    thetas = np.asarray(thetas, dtype=float)
    angles = np.cumsum(thetas)
    J = np.zeros((2, len(thetas)))
    for j in range(len(thetas)):
        for k in range(j, len(thetas)):
            J[:, j] += lengths[k] * np.array([-np.sin(angles[k]), np.cos(angles[k])])
    return J


def manipulability_measure(J: np.ndarray) -> float:
    J = np.asarray(J, dtype=float)
    return float(np.sqrt(max(np.linalg.det(J @ J.T), 0.0)))


def sample_planar_workspace(lengths: np.ndarray, count: int = 72) -> np.ndarray:
    grid = np.linspace(-np.pi, np.pi, count)
    pts = []
    for t1 in grid:
        for t2 in grid:
            angles = np.array([t1, t2] + [0.0] * max(0, len(lengths) - 2))
            pts.append(planar_arm_points(lengths, angles)[-1])
    return np.asarray(pts)

