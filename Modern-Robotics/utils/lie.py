"""Small SO(3)/SE(3) helpers used by Modern Robotics notebooks."""

from __future__ import annotations

import numpy as np


def hat_so3(w: np.ndarray) -> np.ndarray:
    wx, wy, wz = np.asarray(w, dtype=float).reshape(3)
    return np.array([[0.0, -wz, wy], [wz, 0.0, -wx], [-wy, wx, 0.0]])


def vee_so3(W: np.ndarray) -> np.ndarray:
    W = np.asarray(W, dtype=float).reshape(3, 3)
    return np.array([W[2, 1], W[0, 2], W[1, 0]])


def so3_exp(w: np.ndarray) -> np.ndarray:
    w = np.asarray(w, dtype=float).reshape(3)
    theta = np.linalg.norm(w)
    W = hat_so3(w)
    if theta < 1e-12:
        return np.eye(3) + W
    return np.eye(3) + np.sin(theta) / theta * W + (1 - np.cos(theta)) / theta**2 * (W @ W)


def so3_log(R: np.ndarray) -> np.ndarray:
    R = np.asarray(R, dtype=float).reshape(3, 3)
    cos_theta = np.clip((np.trace(R) - 1) / 2, -1.0, 1.0)
    theta = float(np.arccos(cos_theta))
    if theta < 1e-12:
        return vee_so3(R - R.T) / 2
    return theta / (2 * np.sin(theta)) * vee_so3(R - R.T)


def left_jacobian_so3(w: np.ndarray) -> np.ndarray:
    w = np.asarray(w, dtype=float).reshape(3)
    theta = np.linalg.norm(w)
    W = hat_so3(w)
    if theta < 1e-12:
        return np.eye(3) + 0.5 * W + (W @ W) / 6
    return np.eye(3) + (1 - np.cos(theta)) / theta**2 * W + (theta - np.sin(theta)) / theta**3 * (W @ W)


def hat_se3(xi: np.ndarray) -> np.ndarray:
    xi = np.asarray(xi, dtype=float).reshape(6)
    X = np.zeros((4, 4))
    X[:3, :3] = hat_so3(xi[:3])
    X[:3, 3] = xi[3:]
    return X


def vee_se3(X: np.ndarray) -> np.ndarray:
    X = np.asarray(X, dtype=float).reshape(4, 4)
    return np.r_[vee_so3(X[:3, :3]), X[:3, 3]]


def se3_exp(xi: np.ndarray) -> np.ndarray:
    xi = np.asarray(xi, dtype=float).reshape(6)
    w, v = xi[:3], xi[3:]
    T = np.eye(4)
    T[:3, :3] = so3_exp(w)
    T[:3, 3] = left_jacobian_so3(w) @ v
    return T


def se3_log(T: np.ndarray) -> np.ndarray:
    T = np.asarray(T, dtype=float).reshape(4, 4)
    w = so3_log(T[:3, :3])
    v = np.linalg.solve(left_jacobian_so3(w), T[:3, 3])
    return np.r_[w, v]


def adjoint(T: np.ndarray) -> np.ndarray:
    T = np.asarray(T, dtype=float).reshape(4, 4)
    R, p = T[:3, :3], T[:3, 3]
    Ad = np.zeros((6, 6))
    Ad[:3, :3] = R
    Ad[3:, 3:] = R
    Ad[3:, :3] = hat_so3(p) @ R
    return Ad


def coadjoint(T: np.ndarray) -> np.ndarray:
    return np.linalg.inv(adjoint(T)).T


def transform_from(R: np.ndarray | None = None, p: np.ndarray | None = None) -> np.ndarray:
    T = np.eye(4)
    if R is not None:
        T[:3, :3] = np.asarray(R, dtype=float).reshape(3, 3)
    if p is not None:
        T[:3, 3] = np.asarray(p, dtype=float).reshape(3)
    return T


def screw_axis(point: np.ndarray, direction: np.ndarray, pitch: float = 0.0) -> np.ndarray:
    q = np.asarray(point, dtype=float).reshape(3)
    s = np.asarray(direction, dtype=float).reshape(3)
    s = s / np.linalg.norm(s)
    v = -np.cross(s, q) + pitch * s
    return np.r_[s, v]


def wrench_power(twist: np.ndarray, wrench: np.ndarray) -> float:
    twist = np.asarray(twist, dtype=float).reshape(6)
    wrench = np.asarray(wrench, dtype=float).reshape(6)
    return float(twist @ wrench)

