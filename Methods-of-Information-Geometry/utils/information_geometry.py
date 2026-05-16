"""Numerical constructions used by the Methods of Information Geometry notebooks."""

from __future__ import annotations

import numpy as np


def normalize_probability(values: np.ndarray, *, eps: float = 1e-12) -> np.ndarray:
    p = np.asarray(values, dtype=float)
    p = np.maximum(p, eps)
    return p / p.sum()


def simplex_grid(n: int = 31, *, margin: float = 0.04) -> np.ndarray:
    points = []
    for i in range(n):
        p = margin + (1.0 - 3 * margin) * i / max(n - 1, 1)
        for j in range(n):
            q = margin + (1.0 - 3 * margin) * j / max(n - 1, 1)
            r = 1.0 - p - q
            if r > margin:
                points.append((p, q, r))
    return np.array(points, dtype=float)


def barycentric_xy(p: np.ndarray) -> np.ndarray:
    arr = np.asarray(p, dtype=float)
    x = arr[..., 1] + 0.5 * arr[..., 2]
    y = (np.sqrt(3.0) / 2.0) * arr[..., 2]
    return np.stack([x, y], axis=-1)


def categorical_fisher_metric(p: np.ndarray) -> np.ndarray:
    p1, p2, p3 = normalize_probability(np.asarray(p, dtype=float))
    return np.array([[1.0 / p1 + 1.0 / p3, 1.0 / p3], [1.0 / p3, 1.0 / p2 + 1.0 / p3]])


def kl(p: np.ndarray, q: np.ndarray) -> float:
    p = normalize_probability(p)
    q = normalize_probability(q)
    return float(np.sum(p * (np.log(p) - np.log(q))))


def alpha_divergence(p: np.ndarray, q: np.ndarray, alpha: float) -> float:
    p = normalize_probability(p)
    q = normalize_probability(q)
    if np.isclose(alpha, -1.0):
        return kl(q, p)
    if np.isclose(alpha, 1.0):
        return kl(p, q)
    a = (1.0 - alpha) / 2.0
    b = (1.0 + alpha) / 2.0
    return float(4.0 / (1.0 - alpha**2) * (1.0 - np.sum((p**a) * (q**b))))


def alpha_path(p: np.ndarray, q: np.ndarray, alpha: float, t: np.ndarray) -> np.ndarray:
    p = normalize_probability(p)
    q = normalize_probability(q)
    t = np.asarray(t, dtype=float)[:, None]
    if np.isclose(alpha, -1.0):
        raw = (1 - t) * p + t * q
    elif np.isclose(alpha, 1.0):
        raw = np.exp((1 - t) * np.log(p) + t * np.log(q))
    else:
        beta = (1.0 - alpha) / 2.0
        raw = ((1 - t) * (p**beta) + t * (q**beta)) ** (1.0 / beta)
    return raw / raw.sum(axis=1, keepdims=True)


def softmax(theta: np.ndarray) -> np.ndarray:
    theta = np.asarray(theta, dtype=float)
    logits = np.array([theta[0], theta[1], 0.0])
    logits = logits - logits.max()
    weights = np.exp(logits)
    return weights / weights.sum()


def log_partition(theta: np.ndarray) -> float:
    theta = np.asarray(theta, dtype=float)
    logits = np.array([theta[0], theta[1], 0.0])
    m = logits.max()
    return float(m + np.log(np.exp(logits - m).sum()))


def normal_fisher_metric(mu: float, sigma: float) -> np.ndarray:
    del mu
    return np.diag([1.0 / sigma**2, 2.0 / sigma**2])


def normal_kl(mu1: float, sigma1: float, mu2: float, sigma2: float) -> float:
    return float(np.log(sigma2 / sigma1) + (sigma1**2 + (mu1 - mu2) ** 2) / (2 * sigma2**2) - 0.5)


def natural_gradient_step(theta: np.ndarray, grad: np.ndarray, metric: np.ndarray, step: float) -> np.ndarray:
    return np.asarray(theta, dtype=float) - step * np.linalg.solve(metric, np.asarray(grad, dtype=float))


def ar1_spectrum(phi: float, omega: np.ndarray, sigma2: float = 1.0) -> np.ndarray:
    omega = np.asarray(omega, dtype=float)
    return sigma2 / np.maximum(1e-12, 1 + phi**2 - 2 * phi * np.cos(omega))


def ar1_fisher_phi(phi: float) -> float:
    return float(1.0 / max(1e-12, 1.0 - phi**2))


def binary_joint(theta: float, strength: float) -> np.ndarray:
    """A two-by-two joint law with fixed marginals and tunable association."""
    base = np.array([[theta * theta, theta * (1 - theta)], [(1 - theta) * theta, (1 - theta) ** 2]])
    signed = np.array([[1.0, -1.0], [-1.0, 1.0]])
    p = base + strength * theta * (1 - theta) * signed
    return np.maximum(p, 1e-12) / np.maximum(p, 1e-12).sum()


def mutual_information(joint: np.ndarray) -> float:
    p = np.asarray(joint, dtype=float)
    p = p / p.sum()
    row = p.sum(axis=1, keepdims=True)
    col = p.sum(axis=0, keepdims=True)
    return float(np.sum(p * (np.log(p) - np.log(row @ col))))


PAULI_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
PAULI_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
IDENTITY_2 = np.eye(2, dtype=complex)


def density_from_bloch(r: np.ndarray) -> np.ndarray:
    r = np.asarray(r, dtype=float)
    if np.linalg.norm(r) >= 1:
        r = r / (np.linalg.norm(r) + 1e-12) * 0.999
    return 0.5 * (IDENTITY_2 + r[0] * PAULI_X + r[1] * PAULI_Y + r[2] * PAULI_Z)


def matrix_log_spd(mat: np.ndarray) -> np.ndarray:
    vals, vecs = np.linalg.eigh(mat)
    vals = np.maximum(vals.real, 1e-12)
    return (vecs * np.log(vals)) @ vecs.conj().T


def quantum_relative_entropy(rho: np.ndarray, sigma: np.ndarray) -> float:
    return float(np.real(np.trace(rho @ (matrix_log_spd(rho) - matrix_log_spd(sigma)))))

