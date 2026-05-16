"""Landmark and shape-space helpers kept small enough for notebooks to inspect."""

from __future__ import annotations

import numpy as np


def center_landmarks(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    return points - points.mean(axis=0, keepdims=True)


def preshape(points: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    centered = center_landmarks(points)
    scale = np.linalg.norm(centered)
    if scale <= eps:
        raise ValueError("Degenerate landmark configuration has zero centroid size")
    return centered / scale


def procrustes_align(reference: np.ndarray, moving: np.ndarray) -> np.ndarray:
    """Rotate moving landmarks to best match reference after preshape normalization."""

    ref = preshape(reference)
    mov = preshape(moving)
    u, _, vh = np.linalg.svd(mov.T @ ref)
    rotation = u @ vh
    return mov @ rotation


def procrustes_distance(a: np.ndarray, b: np.ndarray) -> float:
    aligned = procrustes_align(a, b)
    return float(np.linalg.norm(preshape(a) - aligned))


def gram_embedding(points: np.ndarray) -> np.ndarray:
    z = preshape(points)
    return z @ z.T


def affine_normalize(points: np.ndarray) -> np.ndarray:
    """Center and whiten landmarks so affine information is quotiented out."""

    centered = center_landmarks(points)
    cov = centered.T @ centered / max(len(centered) - 1, 1)
    vals, vecs = np.linalg.eigh(cov)
    inv_sqrt = vecs @ np.diag(1.0 / np.sqrt(np.maximum(vals, 1e-9))) @ vecs.T
    return centered @ inv_sqrt


def triangle_shape_coordinates(points: np.ndarray) -> np.ndarray:
    """A simple planar triangle-shape coordinate used for CP1-style pictures."""

    z = preshape(points)
    side_lengths = np.array(
        [
            np.linalg.norm(z[1] - z[2]),
            np.linalg.norm(z[0] - z[2]),
            np.linalg.norm(z[0] - z[1]),
        ]
    )
    side_lengths = side_lengths / np.linalg.norm(side_lengths)
    x = side_lengths[1] - side_lengths[0]
    y = (2 * side_lengths[2] - side_lengths[0] - side_lengths[1]) / np.sqrt(3)
    area = 0.5 * np.cross(z[1] - z[0], z[2] - z[0])
    return np.array([x, y, area])
