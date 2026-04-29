"""Spherical statistics helpers."""

from __future__ import annotations

import numpy as np
from scipy import optimize


def normalize(vectors: np.ndarray) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=float)
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    return vectors / np.maximum(norms, 1e-15)


def spherical_sample(seed: int, n: int, pole: np.ndarray | None = None, concentration: float = 8.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    pole = normalize(np.asarray(pole if pole is not None else [0.2, 0.3, 1.0]))
    noise = rng.normal(size=(n, 3))
    samples = noise + concentration * pole
    return normalize(samples)


def uniform_sphere(seed: int, n: int, dim: int = 3) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return normalize(rng.normal(size=(n, dim)))


def mean_direction(vectors: np.ndarray) -> dict[str, float | np.ndarray]:
    vectors = np.asarray(vectors, dtype=float)
    mean = vectors.mean(axis=0)
    length = float(np.linalg.norm(mean))
    direction = mean / max(length, 1e-15)
    return {"mean": mean, "direction": direction, "R": length}


def inertia_matrix(vectors: np.ndarray) -> np.ndarray:
    vectors = np.asarray(vectors, dtype=float)
    return vectors.T @ vectors / len(vectors)


def fisher_A3(kappa: np.ndarray | float) -> np.ndarray:
    kappa = np.asarray(kappa, dtype=float)
    return 1.0 / np.tanh(np.maximum(kappa, 1e-10)) - 1.0 / np.maximum(kappa, 1e-10)


def inverse_fisher_A3(r: float) -> float:
    r = float(np.clip(r, 1e-8, 0.999999))
    root = optimize.root_scalar(lambda k: float(fisher_A3(k) - r), bracket=[1e-8, 1e4])
    return float(root.root)


def fisher_density_s2(points: np.ndarray, mu: np.ndarray, kappa: float) -> np.ndarray:
    points = normalize(points)
    mu = normalize(np.asarray(mu))
    if kappa < 1e-8:
        c = 1.0 / (4 * np.pi)
    else:
        c = kappa / (4 * np.pi * np.sinh(kappa))
    return c * np.exp(kappa * (points @ mu))


def angular_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = normalize(a)
    b = normalize(b)
    dots = np.clip(np.sum(a * b, axis=-1), -1.0, 1.0)
    return np.arccos(dots)


def confidence_cone_radius(n: int, rbar: float, alpha: float = 0.05) -> float:
    value = max(1e-9, alpha ** (1.0 / max(n - 1, 1)))
    return float(np.arccos(np.clip(1 - (n - rbar * n) / (rbar * n) * (1 / value - 1), -1, 1)))
