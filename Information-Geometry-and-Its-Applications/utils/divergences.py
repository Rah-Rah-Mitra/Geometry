"""Divergence functions used across the Information Geometry course."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np

Array = np.ndarray


def as_probability_vector(values: Any, *, axis: int = -1, eps: float = 0.0) -> Array:
    array = np.asarray(values, dtype=float)
    if np.any(array < -eps):
        raise ValueError("probabilities must be non-negative")
    array = np.clip(array, eps, None)
    total = array.sum(axis=axis, keepdims=True)
    if np.any(total <= 0):
        raise ValueError("probability vector has zero total mass")
    return array / total


def safe_log(values: Any, *, eps: float = 1e-12) -> Array:
    return np.log(np.clip(np.asarray(values, dtype=float), eps, None))


def kl_divergence(p: Any, q: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, axis=axis, eps=eps)
    q_arr = as_probability_vector(q, axis=axis, eps=eps)
    return np.sum(p_arr * (safe_log(p_arr, eps=eps) - safe_log(q_arr, eps=eps)), axis=axis)


def reverse_kl_divergence(p: Any, q: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    return kl_divergence(q, p, axis=axis, eps=eps)


def js_divergence(p: Any, q: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, axis=axis, eps=eps)
    q_arr = as_probability_vector(q, axis=axis, eps=eps)
    midpoint = 0.5 * (p_arr + q_arr)
    return 0.5 * kl_divergence(p_arr, midpoint, axis=axis, eps=eps) + 0.5 * kl_divergence(q_arr, midpoint, axis=axis, eps=eps)


def chi_square_divergence(p: Any, q: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, axis=axis, eps=eps)
    q_arr = as_probability_vector(q, axis=axis, eps=eps)
    return np.sum((p_arr - q_arr) ** 2 / np.clip(q_arr, eps, None), axis=axis)


def hellinger_distance(p: Any, q: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, axis=axis, eps=eps)
    q_arr = as_probability_vector(q, axis=axis, eps=eps)
    return np.sqrt(0.5 * np.sum((np.sqrt(p_arr) - np.sqrt(q_arr)) ** 2, axis=axis))


def alpha_divergence(p: Any, q: Any, alpha: float, *, axis: int = -1, eps: float = 1e-12) -> Array:
    p_arr = as_probability_vector(p, axis=axis, eps=eps)
    q_arr = as_probability_vector(q, axis=axis, eps=eps)
    if np.isclose(alpha, -1.0):
        return kl_divergence(q_arr, p_arr, axis=axis, eps=eps)
    if np.isclose(alpha, 1.0):
        return kl_divergence(p_arr, q_arr, axis=axis, eps=eps)
    power_p = (1.0 - alpha) / 2.0
    power_q = (1.0 + alpha) / 2.0
    affinity = np.sum(np.power(p_arr, power_p) * np.power(q_arr, power_q), axis=axis)
    return 4.0 * (1.0 - affinity) / (1.0 - alpha**2)


def bregman_divergence(
    theta: Any,
    eta: Any,
    potential: Callable[[Array], float],
    gradient: Callable[[Array], Array],
) -> float:
    x = np.asarray(theta, dtype=float)
    y = np.asarray(eta, dtype=float)
    return float(potential(x) - potential(y) - np.dot(gradient(y), x - y))


def quadratic_bregman(theta: Any, eta: Any, metric: Any | None = None) -> float:
    x = np.asarray(theta, dtype=float)
    y = np.asarray(eta, dtype=float)
    diff = x - y
    if metric is None:
        return float(0.5 * np.dot(diff, diff))
    matrix = np.asarray(metric, dtype=float)
    return float(0.5 * diff @ matrix @ diff)


def itakura_saito(x: Any, y: Any, *, axis: int = -1, eps: float = 1e-12) -> Array:
    x_arr = np.clip(np.asarray(x, dtype=float), eps, None)
    y_arr = np.clip(np.asarray(y, dtype=float), eps, None)
    ratio = x_arr / y_arr
    return np.sum(ratio - np.log(ratio) - 1.0, axis=axis)


def divergence_matrix(points: Any, divergence: Callable[[Array, Array], float]) -> Array:
    values = np.asarray(points, dtype=float)
    n = values.shape[0]
    out = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            out[i, j] = divergence(values[i], values[j])
    return out
