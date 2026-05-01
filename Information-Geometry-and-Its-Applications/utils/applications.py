"""Small application helpers for the Information Geometry notebooks."""

from __future__ import annotations

from typing import Any

import numpy as np

from .divergences import as_probability_vector, kl_divergence
from .information_geometry import simplex_projection, softmax


def bregman_kmeans_step(data: Any, centers: Any) -> dict[str, np.ndarray]:
    x = np.asarray(data, dtype=float)
    c = np.asarray(centers, dtype=float)
    distances = np.sum((x[:, None, :] - c[None, :, :]) ** 2, axis=-1)
    labels = distances.argmin(axis=1)
    new_centers = c.copy()
    for k in range(c.shape[0]):
        if np.any(labels == k):
            new_centers[k] = x[labels == k].mean(axis=0)
    return {"labels": labels, "centers": new_centers, "distances": distances}


def gaussian_mixture_em_step(x: Any, means: Any, variances: Any, weights: Any) -> dict[str, np.ndarray]:
    values = np.asarray(x, dtype=float)[:, None]
    mu = np.asarray(means, dtype=float)[None, :]
    var = np.clip(np.asarray(variances, dtype=float)[None, :], 1e-9, None)
    w = as_probability_vector(weights)
    log_prob = np.log(w)[None, :] - 0.5 * (np.log(2.0 * np.pi * var) + (values - mu) ** 2 / var)
    responsibilities = softmax(log_prob, axis=1)
    nk = responsibilities.sum(axis=0)
    new_weights = nk / len(values)
    new_means = (responsibilities * values).sum(axis=0) / np.clip(nk, 1e-12, None)
    new_variances = (responsibilities * (values - new_means[None, :]) ** 2).sum(axis=0) / np.clip(nk, 1e-12, None)
    return {
        "responsibilities": responsibilities,
        "weights": new_weights,
        "means": new_means,
        "variances": np.clip(new_variances, 1e-9, None),
    }


def natural_gradient_step(theta: Any, gradient: Any, fisher: Any, learning_rate: float = 0.1, damping: float = 1e-6) -> np.ndarray:
    theta_arr = np.asarray(theta, dtype=float)
    grad = np.asarray(gradient, dtype=float)
    metric = np.asarray(fisher, dtype=float) + damping * np.eye(theta_arr.size)
    direction = np.linalg.solve(metric, grad)
    return theta_arr - learning_rate * direction


def replicator_step(weights: Any, scores: Any, learning_rate: float = 0.1) -> np.ndarray:
    w = as_probability_vector(weights)
    centered = np.asarray(scores, dtype=float) - float(np.dot(w, scores))
    return as_probability_vector(w * np.exp(learning_rate * centered))


def mean_field_ising_update(couplings: Any, fields: Any, magnetization: Any, damping: float = 0.0) -> np.ndarray:
    j = np.asarray(couplings, dtype=float)
    h = np.asarray(fields, dtype=float)
    m = np.asarray(magnetization, dtype=float)
    update = np.tanh(h + j @ m)
    return (1.0 - damping) * update + damping * m


def contrastive_divergence_delta(data_expectation: Any, model_expectation: Any) -> np.ndarray:
    return np.asarray(data_expectation, dtype=float) - np.asarray(model_expectation, dtype=float)


def sparse_l1_step(beta: Any, gradient: Any, learning_rate: float, radius: float = 1.0) -> np.ndarray:
    raw = np.asarray(beta, dtype=float) - learning_rate * np.asarray(gradient, dtype=float)
    if np.sum(np.abs(raw)) <= radius:
        return raw
    projected_abs = simplex_projection(np.abs(raw) / radius) * radius
    return np.sign(raw) * projected_abs


def chernoff_curve(p: Any, q: Any, grid: Any | None = None) -> dict[str, np.ndarray]:
    p_arr = as_probability_vector(p)
    q_arr = as_probability_vector(q)
    t = np.linspace(0.0, 1.0, 101) if grid is None else np.asarray(grid, dtype=float)
    values = np.array([-np.log(np.sum(p_arr ** (1.0 - s) * q_arr**s)) for s in t])
    return {"t": t, "information": values, "max_t": np.array([t[int(values.argmax())]]), "max_value": np.array([values.max()])}


def information_loss_by_coarse_graining(p: Any, q: Any, groups: list[list[int]]) -> float:
    p_arr = as_probability_vector(p)
    q_arr = as_probability_vector(q)
    coarse_p = np.array([p_arr[group].sum() for group in groups], dtype=float)
    coarse_q = np.array([q_arr[group].sum() for group in groups], dtype=float)
    return float(kl_divergence(p_arr, q_arr) - kl_divergence(coarse_p, coarse_q))
