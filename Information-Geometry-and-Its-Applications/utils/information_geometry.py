"""Information-geometry primitives for chapter notebooks."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np
from scipy.special import logsumexp

from .divergences import as_probability_vector, kl_divergence

Array = np.ndarray


def softmax(theta: Any, *, axis: int = -1) -> Array:
    values = np.asarray(theta, dtype=float)
    return np.exp(values - logsumexp(values, axis=axis, keepdims=True))


def log_partition(theta: Any, sufficient_statistics: Any) -> float:
    theta_arr = np.asarray(theta, dtype=float)
    stats = np.asarray(sufficient_statistics, dtype=float)
    return float(logsumexp(stats @ theta_arr))


def expectation_parameter(theta: Any, sufficient_statistics: Any) -> Array:
    stats = np.asarray(sufficient_statistics, dtype=float)
    probs = softmax(stats @ np.asarray(theta, dtype=float))
    return probs @ stats


def fisher_metric_categorical(p: Any, *, coordinates: str = "simplex", eps: float = 1e-12) -> Array:
    probs = as_probability_vector(p, eps=eps)
    if coordinates == "ambient":
        return np.diag(1.0 / np.clip(probs, eps, None))
    if coordinates != "simplex":
        raise ValueError("coordinates must be 'simplex' or 'ambient'")
    base = probs[:-1]
    last = max(float(probs[-1]), eps)
    return np.diag(1.0 / np.clip(base, eps, None)) + np.ones((len(base), len(base))) / last


def e_geodesic(p: Any, q: Any, t: Any, *, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, eps=eps)
    q_arr = as_probability_vector(q, eps=eps)
    tau = np.asarray(t, dtype=float)[..., None]
    log_path = (1.0 - tau) * np.log(np.clip(p_arr, eps, None)) + tau * np.log(np.clip(q_arr, eps, None))
    return softmax(log_path, axis=-1)


def m_geodesic(p: Any, q: Any, t: Any, *, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, eps=eps)
    q_arr = as_probability_vector(q, eps=eps)
    tau = np.asarray(t, dtype=float)[..., None]
    return as_probability_vector((1.0 - tau) * p_arr + tau * q_arr, eps=eps)


def natural_to_mean_gaussian(theta: Any) -> dict[str, float]:
    theta_arr = np.asarray(theta, dtype=float)
    if theta_arr.shape[-1] != 2:
        raise ValueError("one-dimensional Gaussian natural coordinates have length 2")
    precision = -2.0 * theta_arr[..., 1]
    if np.any(precision <= 0):
        raise ValueError("second natural coordinate must be negative")
    mu = theta_arr[..., 0] / precision
    sigma2 = 1.0 / precision
    return {"mu": float(mu), "sigma2": float(sigma2)}


def mean_to_natural_gaussian(mu: float, sigma2: float) -> Array:
    if sigma2 <= 0:
        raise ValueError("sigma2 must be positive")
    return np.array([mu / sigma2, -0.5 / sigma2], dtype=float)


def gaussian_fisher_metric(mu: float, sigma: float) -> Array:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    return np.array([[1.0 / sigma**2, 0.0], [0.0, 2.0 / sigma**2]], dtype=float)


def finite_difference_metric(
    divergence: Callable[[Array, Array], float],
    point: Any,
    *,
    step: float = 1e-4,
) -> Array:
    x = np.asarray(point, dtype=float)
    n = x.size
    metric = np.zeros((n, n), dtype=float)
    for i in range(n):
        ei = np.zeros(n)
        ei[i] = step
        for j in range(n):
            ej = np.zeros(n)
            ej[j] = step
            metric[i, j] = (
                divergence(x + ei, x + ej)
                - divergence(x + ei, x - ej)
                - divergence(x - ei, x + ej)
                + divergence(x - ei, x - ej)
            ) / (4.0 * step**2)
    return 0.5 * (metric + metric.T)


def pythagorean_residual(p: Any, q: Any, r: Any, *, eps: float = 1e-12) -> float:
    return float(kl_divergence(p, r, eps=eps) - kl_divergence(p, q, eps=eps) - kl_divergence(q, r, eps=eps))


def mirror_descent_step(theta: Any, gradient: Any, learning_rate: float, mirror_map_grad_inv: Callable[[Array], Array]) -> Array:
    dual = np.asarray(theta, dtype=float) - learning_rate * np.asarray(gradient, dtype=float)
    return mirror_map_grad_inv(dual)


def simplex_projection(values: Any, *, eps: float = 0.0) -> Array:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1:
        raise ValueError("simplex_projection expects a vector")
    u = np.sort(x)[::-1]
    cssv = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(u) + 1) > (cssv - 1.0))[0]
    if len(rho) == 0:
        return np.full_like(x, 1.0 / len(x))
    k = rho[-1]
    tau = (cssv[k] - 1.0) / float(k + 1)
    return as_probability_vector(np.maximum(x - tau, eps), eps=eps)
