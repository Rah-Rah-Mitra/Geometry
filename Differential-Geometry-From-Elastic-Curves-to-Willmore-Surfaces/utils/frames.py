"""Frame and alignment helpers for space curves."""

from __future__ import annotations

import numpy as np

from utils.curves import unit_tangent

EPS = 1e-12


def rotation_minimizing_frame(points: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pts = np.asarray(points, dtype=float)
    if pts.shape[1] != 3:
        raise ValueError("rotation_minimizing_frame expects 3D points")
    t = unit_tangent(pts)
    seed = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(seed, t[0])) > 0.9:
        seed = np.array([0.0, 1.0, 0.0])
    n0 = seed - np.dot(seed, t[0]) * t[0]
    n0 = n0 / np.linalg.norm(n0)
    normals = [n0]
    binormals = [np.cross(t[0], n0)]
    for i in range(1, len(t)):
        v = normals[-1] - np.dot(normals[-1], t[i]) * t[i]
        if np.linalg.norm(v) <= EPS:
            v = binormals[-1] - np.dot(binormals[-1], t[i]) * t[i]
        v = v / np.linalg.norm(v)
        normals.append(v)
        binormals.append(np.cross(t[i], v))
    return t, np.asarray(normals), np.asarray(binormals)


def torsion_indicator(points: np.ndarray) -> np.ndarray:
    t, n, b = rotation_minimizing_frame(points)
    db = np.gradient(b, axis=0, edge_order=2)
    return -np.einsum("ij,ij->i", db, n)


def kabsch_align(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, float]:
    src = np.asarray(source, dtype=float)
    tgt = np.asarray(target, dtype=float)
    src_center = src.mean(axis=0)
    tgt_center = tgt.mean(axis=0)
    src0 = src - src_center
    tgt0 = tgt - tgt_center
    u, _, vt = np.linalg.svd(src0.T @ tgt0)
    r = u @ vt
    if np.linalg.det(r) < 0:
        u[:, -1] *= -1
        r = u @ vt
    aligned = src0 @ r + tgt_center
    rms = float(np.sqrt(np.mean(np.sum((aligned - tgt) ** 2, axis=1))))
    return aligned, rms


def reconstruct_from_tangent(tangent: np.ndarray, step: float = 1.0) -> np.ndarray:
    tangent = np.asarray(tangent, dtype=float)
    tangent = tangent / np.linalg.norm(tangent, axis=1, keepdims=True)
    pts = np.vstack([np.zeros(tangent.shape[1]), np.cumsum(tangent[:-1] * step, axis=0)])
    return pts
