"""Landmark shape helpers."""

from __future__ import annotations

import numpy as np
from scipy.linalg import orthogonal_procrustes


def helmert_submatrix(k: int) -> np.ndarray:
    h = np.zeros((k - 1, k))
    for i in range(1, k):
        h[i - 1, :i] = 1 / np.sqrt(i * (i + 1))
        h[i - 1, i] = -i / np.sqrt(i * (i + 1))
    return h


def center_landmarks(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    return points - points.mean(axis=-2, keepdims=True)


def preshape(points: np.ndarray) -> np.ndarray:
    centered = center_landmarks(points)
    norm = np.linalg.norm(centered)
    return centered / max(norm, 1e-15)


def procrustes_align(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    src = center_landmarks(source)
    tgt = center_landmarks(target)
    scale = max(np.linalg.norm(src), 1e-15)
    src = src / scale
    tgt = tgt / max(np.linalg.norm(tgt), 1e-15)
    r, _ = orthogonal_procrustes(src, tgt)
    return src @ r


def procrustes_mean(shapes: np.ndarray, iterations: int = 8) -> np.ndarray:
    mean = preshape(shapes[0])
    for _ in range(iterations):
        aligned = np.stack([procrustes_align(shape, mean) for shape in shapes])
        mean = preshape(aligned.mean(axis=0))
    return mean


def tangent_shape_coords(shapes: np.ndarray, mean: np.ndarray) -> np.ndarray:
    aligned = np.stack([procrustes_align(shape, mean) for shape in shapes])
    residuals = aligned - mean
    return residuals.reshape(len(shapes), -1)


def triangle_shape_features(points: np.ndarray) -> np.ndarray:
    points = center_landmarks(points)
    edges = np.array([
        np.linalg.norm(points[1] - points[0]),
        np.linalg.norm(points[2] - points[1]),
        np.linalg.norm(points[0] - points[2]),
    ])
    edges = edges / max(np.linalg.norm(edges), 1e-15)
    return edges
