"""Small transparent manifold-statistics helpers used by the notebooks."""

from __future__ import annotations

import numpy as np


def normalize_rows(points: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    norms = np.linalg.norm(points, axis=-1, keepdims=True)
    return points / np.maximum(norms, eps)


def sphere_extrinsic_mean(points: np.ndarray) -> np.ndarray:
    """Project the Euclidean average of unit vectors back to the sphere."""

    mean = np.mean(np.asarray(points, dtype=float), axis=0)
    norm = np.linalg.norm(mean)
    if norm <= 1e-12:
        raise ValueError("Euclidean mean is too close to the origin to project uniquely")
    return mean / norm


def sphere_log(base: np.ndarray, points: np.ndarray) -> np.ndarray:
    """Log map on the unit sphere using elementary vector calculus."""

    base = np.asarray(base, dtype=float)
    points = np.asarray(points, dtype=float)
    dot = np.clip(points @ base, -1.0, 1.0)
    theta = np.arccos(dot)
    tangent = points - dot[..., None] * base
    tangent_norm = np.linalg.norm(tangent, axis=-1)
    scale = np.divide(theta, tangent_norm, out=np.ones_like(theta), where=tangent_norm > 1e-12)
    return tangent * scale[..., None]


def sphere_exp(base: np.ndarray, vectors: np.ndarray) -> np.ndarray:
    """Exponential map on the unit sphere."""

    base = np.asarray(base, dtype=float)
    vectors = np.asarray(vectors, dtype=float)
    theta = np.linalg.norm(vectors, axis=-1)
    cos = np.cos(theta)
    sin_over = np.divide(np.sin(theta), theta, out=np.ones_like(theta), where=theta > 1e-12)
    return normalize_rows(cos[..., None] * base + sin_over[..., None] * vectors)


def frechet_values_on_circle(angles: np.ndarray, grid: np.ndarray) -> np.ndarray:
    """Squared geodesic loss on S1 over a grid of candidate angles."""

    diff = np.angle(np.exp(1j * (grid[:, None] - angles[None, :])))
    return np.mean(diff**2, axis=1)


def bootstrap_sphere_means(points: np.ndarray, *, n_boot: int = 200, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    points = np.asarray(points, dtype=float)
    n = len(points)
    means = []
    for _ in range(n_boot):
        sample = points[rng.integers(0, n, size=n)]
        means.append(sphere_extrinsic_mean(sample))
    return np.array(means)


def projective_distance(x: np.ndarray, y: np.ndarray) -> float:
    """Distance between real projective points represented by unit vectors."""

    x = normalize_rows(np.asarray(x, dtype=float)[None, :])[0]
    y = normalize_rows(np.asarray(y, dtype=float)[None, :])[0]
    return float(np.arccos(np.clip(abs(np.dot(x, y)), 0.0, 1.0)))


def stiefel_project(matrix: np.ndarray) -> np.ndarray:
    """Nearest orthonormal-frame matrix via polar projection."""

    u, _, vh = np.linalg.svd(matrix, full_matrices=False)
    return u @ vh
