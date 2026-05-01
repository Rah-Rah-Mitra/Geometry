"""Camera helpers for synthetic multiple-view geometry labs."""

from __future__ import annotations

import numpy as np

from .projective import dehomogenize, homogenize


def skew(v: np.ndarray) -> np.ndarray:
    x, y, z = np.asarray(v, dtype=float).reshape(3)
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])


def make_calibration(fx: float = 900.0, fy: float | None = None, cx: float = 0.0, cy: float = 0.0, skew_value: float = 0.0) -> np.ndarray:
    if fy is None:
        fy = fx
    return np.array([[fx, skew_value, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]], dtype=float)


def look_at_rotation(center: np.ndarray, target: np.ndarray = np.zeros(3), up: np.ndarray = np.array([0.0, 1.0, 0.0])) -> np.ndarray:
    center = np.asarray(center, dtype=float)
    target = np.asarray(target, dtype=float)
    forward = target - center
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, up)
    if np.linalg.norm(right) < 1e-9:
        right = np.array([1.0, 0.0, 0.0])
    right = right / np.linalg.norm(right)
    true_up = np.cross(right, forward)
    true_up = true_up / np.linalg.norm(true_up)
    return np.vstack([right, true_up, forward])


def camera_matrix(K: np.ndarray, R: np.ndarray, center: np.ndarray) -> np.ndarray:
    center = np.asarray(center, dtype=float).reshape(3, 1)
    Rt = np.hstack([R, -R @ center])
    return np.asarray(K, dtype=float) @ Rt


def project_points(P: np.ndarray, points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    hp = homogenize(pts) if pts.shape[-1] == 3 else pts
    return dehomogenize((np.asarray(P, dtype=float) @ hp.T).T)


def camera_center(P: np.ndarray) -> np.ndarray:
    _, _, vt = np.linalg.svd(np.asarray(P, dtype=float))
    C = vt[-1]
    return C / C[-1]


def synthetic_cameras() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    K = make_calibration(850.0, 830.0, 320.0, 240.0)
    c1 = np.array([-1.8, 0.4, -4.2])
    c2 = np.array([1.7, 0.6, -4.0])
    P1 = camera_matrix(K, look_at_rotation(c1), c1)
    P2 = camera_matrix(K, look_at_rotation(c2), c2)
    return K, P1, P2


def cube_points(scale: float = 1.0) -> np.ndarray:
    vals = [-scale, scale]
    return np.array([[x, y, z + 3.2] for x in vals for y in vals for z in vals], dtype=float)
