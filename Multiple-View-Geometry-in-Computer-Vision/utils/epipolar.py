"""Epipolar and triangulation helpers for MVG notebooks."""

from __future__ import annotations

import numpy as np

from .cameras import camera_center, skew
from .projective import homogenize, normalize_points_2d


def enforce_rank2(F: np.ndarray) -> np.ndarray:
    u, s, vt = np.linalg.svd(np.asarray(F, dtype=float))
    s[-1] = 0.0
    Fr = u @ np.diag(s) @ vt
    norm = np.linalg.norm(Fr)
    return Fr / norm if norm else Fr


def fundamental_from_cameras(P1: np.ndarray, P2: np.ndarray) -> np.ndarray:
    C1 = camera_center(P1)
    e2 = P2 @ C1
    F = skew(e2) @ P2 @ np.linalg.pinv(P1)
    return enforce_rank2(F)


def eight_point(points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    p1, T1 = normalize_points_2d(points1)
    p2, T2 = normalize_points_2d(points2)
    rows = []
    for a, b in zip(p1, p2):
        x, y, w = a
        xp, yp, wp = b
        rows.append([xp * x, xp * y, xp * w, yp * x, yp * y, yp * w, wp * x, wp * y, wp * w])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    Fn = vt[-1].reshape(3, 3)
    F = T2.T @ enforce_rank2(Fn) @ T1
    return enforce_rank2(F)


def sampson_errors(F: np.ndarray, points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    x1 = homogenize(points1) if np.asarray(points1).shape[-1] == 2 else np.asarray(points1, dtype=float)
    x2 = homogenize(points2) if np.asarray(points2).shape[-1] == 2 else np.asarray(points2, dtype=float)
    Fx1 = (F @ x1.T).T
    Ftx2 = (F.T @ x2.T).T
    numer = np.sum(x2 * Fx1, axis=1) ** 2
    denom = Fx1[:, 0] ** 2 + Fx1[:, 1] ** 2 + Ftx2[:, 0] ** 2 + Ftx2[:, 1] ** 2
    return numer / np.maximum(denom, 1e-12)


def linear_triangulate(P1: np.ndarray, P2: np.ndarray, points1: np.ndarray, points2: np.ndarray) -> np.ndarray:
    pts = []
    for x1, x2 in zip(points1, points2):
        u1, v1 = x1[:2]
        u2, v2 = x2[:2]
        A = np.vstack([
            u1 * P1[2] - P1[0],
            v1 * P1[2] - P1[1],
            u2 * P2[2] - P2[0],
            v2 * P2[2] - P2[1],
        ])
        _, _, vt = np.linalg.svd(A)
        X = vt[-1]
        pts.append(X[:3] / X[3])
    return np.asarray(pts)
