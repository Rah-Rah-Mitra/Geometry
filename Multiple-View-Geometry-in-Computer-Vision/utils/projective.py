"""Small projective-geometry helpers used by MVG notebooks."""

from __future__ import annotations

import numpy as np


def homogenize(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    ones = np.ones((*pts.shape[:-1], 1), dtype=float)
    return np.concatenate([pts, ones], axis=-1)


def dehomogenize(points: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    w = pts[..., -1:]
    safe = np.where(np.abs(w) < eps, np.sign(w) * eps + (w == 0) * eps, w)
    return pts[..., :-1] / safe


def normalize_homogeneous(x: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    arr = np.asarray(x, dtype=float)
    norm = np.linalg.norm(arr, axis=-1, keepdims=True)
    norm = np.where(norm < eps, 1.0, norm)
    return arr / norm


def line_through(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.cross(np.asarray(p, dtype=float), np.asarray(q, dtype=float))


def incidence(line: np.ndarray, point: np.ndarray) -> float:
    return float(np.dot(np.asarray(line, dtype=float), np.asarray(point, dtype=float)))


def apply_homography(H: np.ndarray, points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    hp = homogenize(pts) if pts.shape[-1] == 2 else pts
    mapped = (np.asarray(H, dtype=float) @ hp.T).T
    return dehomogenize(mapped)


def normalize_points_2d(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pts = np.asarray(points, dtype=float)
    if pts.shape[-1] == 3:
        pts = dehomogenize(pts)
    centroid = pts.mean(axis=0)
    centered = pts - centroid
    mean_dist = np.sqrt((centered**2).sum(axis=1)).mean()
    scale = np.sqrt(2.0) / mean_dist if mean_dist > 1e-12 else 1.0
    T = np.array([[scale, 0.0, -scale * centroid[0]], [0.0, scale, -scale * centroid[1]], [0.0, 0.0, 1.0]])
    normalized = (T @ homogenize(pts).T).T
    return normalized, T


def dlt_homography(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    src_n, Ts = normalize_points_2d(src)
    dst_n, Td = normalize_points_2d(dst)
    rows = []
    for x, xp in zip(src_n, dst_n):
        X, Y, W = x
        u, v, w = xp
        rows.append([0, 0, 0, -w * X, -w * Y, -w * W, v * X, v * Y, v * W])
        rows.append([w * X, w * Y, w * W, 0, 0, 0, -u * X, -u * Y, -u * W])
    _, _, vt = np.linalg.svd(np.asarray(rows))
    Hn = vt[-1].reshape(3, 3)
    H = np.linalg.inv(Td) @ Hn @ Ts
    return H / H[-1, -1]


def conic_from_circle(center: tuple[float, float], radius: float) -> np.ndarray:
    cx, cy = center
    return np.array([[1.0, 0.0, -cx], [0.0, 1.0, -cy], [-cx, -cy, cx * cx + cy * cy - radius * radius]])


def plucker_from_points(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    A = np.asarray(a, dtype=float)
    B = np.asarray(b, dtype=float)
    return np.outer(A, B) - np.outer(B, A)
