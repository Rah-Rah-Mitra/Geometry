"""Estimation helpers used across the MVG course."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


def reprojection_rmse(observed: np.ndarray, predicted: np.ndarray) -> float:
    residual = np.asarray(observed, dtype=float) - np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean(np.sum(residual**2, axis=-1))))


def monte_carlo_covariance(samples: np.ndarray) -> np.ndarray:
    samples = np.asarray(samples, dtype=float)
    return np.cov(samples.T)


def finite_difference_jacobian(fn: Callable[[np.ndarray], np.ndarray], x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    y0 = np.asarray(fn(x), dtype=float).ravel()
    J = np.zeros((y0.size, x.size))
    for j in range(x.size):
        step = np.zeros_like(x)
        step[j] = eps
        J[:, j] = (np.asarray(fn(x + step)).ravel() - np.asarray(fn(x - step)).ravel()) / (2 * eps)
    return J


def simple_ransac(sample_count: int, fit_fn, residual_fn, threshold: float, *, trials: int = 128, rng: np.random.Generator | None = None):
    if rng is None:
        rng = np.random.default_rng(0)
    best_model = None
    best_inliers = np.array([], dtype=int)
    n = residual_fn(None, probe=True)
    for _ in range(trials):
        sample = rng.choice(n, size=sample_count, replace=False)
        model = fit_fn(sample)
        residuals = residual_fn(model)
        inliers = np.flatnonzero(residuals < threshold)
        if inliers.size > best_inliers.size:
            best_model = model
            best_inliers = inliers
    return best_model, best_inliers
