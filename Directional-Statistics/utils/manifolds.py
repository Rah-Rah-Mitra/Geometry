"""Helpers for rotations, frames, Grassmann points, and hyperboloids."""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm, polar


def skew(v: np.ndarray) -> np.ndarray:
    x, y, z = np.asarray(v, dtype=float)
    return np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]], dtype=float)


def rotation_from_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    axis = axis / max(np.linalg.norm(axis), 1e-15)
    return expm(skew(axis * angle))


def sample_so3(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    frames = []
    for _ in range(n):
        q, r = np.linalg.qr(rng.normal(size=(3, 3)))
        q *= np.sign(np.diag(r))
        if np.linalg.det(q) < 0:
            q[:, 0] *= -1
        frames.append(q)
    return np.stack(frames)


def sample_stiefel(seed: int, p: int, r: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    frames = []
    for _ in range(n):
        q, _ = np.linalg.qr(rng.normal(size=(p, r)))
        frames.append(q[:, :r])
    return np.stack(frames)


def polar_stiefel(matrix: np.ndarray) -> np.ndarray:
    u, _ = polar(matrix)
    return u


def grassmann_projection(frame: np.ndarray) -> np.ndarray:
    return frame @ frame.T


def sample_hyperboloid(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    xy = rng.normal(scale=0.6, size=(n, 2))
    t = np.sqrt(1 + np.sum(xy**2, axis=1))
    return np.column_stack([t, xy])


def minkowski_dot(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a)
    b = np.asarray(b)
    return a[..., 0] * b[..., 0] - np.sum(a[..., 1:] * b[..., 1:], axis=-1)
