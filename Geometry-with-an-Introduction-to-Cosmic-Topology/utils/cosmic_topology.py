"""Small simulation helpers for cosmic topology notebooks."""

from __future__ import annotations

import math

import numpy as np


def pair_distances(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    dists = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dists.append(float(np.linalg.norm(points[i] - points[j])))
    return np.asarray(dists)


def pair_separation_histogram(points: np.ndarray, bins: int = 32) -> tuple[np.ndarray, np.ndarray]:
    distances = pair_distances(points)
    hist, edges = np.histogram(distances, bins=bins)
    return hist, edges


def torus_catalog(seed: int = 7, base_count: int = 14, width: float = 4.0, height: float = 3.0, copies: int = 1) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = rng.random((base_count, 2)) * np.array([width, height])
    images = []
    for i in range(-copies, copies + 1):
        for j in range(-copies, copies + 1):
            images.append(base + np.array([i * width, j * height]))
    return np.vstack(images)


def sphere_intersection_circle_radius(r_obs: float, separation: float) -> float:
    if separation <= 0 or separation >= 2 * r_obs:
        return 0.0
    return float(math.sqrt(r_obs**2 - (separation / 2) ** 2))


def ccp_score(points: np.ndarray, epsilon: float = 1e-3) -> float:
    distances = np.sort(pair_distances(points))
    if len(distances) < 2:
        return 0.0
    gaps = np.diff(distances)
    return float(np.count_nonzero(gaps < epsilon) / len(gaps))


def omega_geometry(omega_k: float, tol: float = 1e-3) -> str:
    if abs(omega_k) <= tol:
        return "nearly euclidean"
    if omega_k > 0:
        return "hyperbolic convention"
    return "elliptic convention"
