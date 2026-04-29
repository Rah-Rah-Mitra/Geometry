"""Circular statistics helpers used by course notebooks."""

from __future__ import annotations

import numpy as np
from scipy import optimize, special, stats

TAU = 2.0 * np.pi


def wrap_angle(theta: np.ndarray | float, center: float = 0.0) -> np.ndarray:
    return (np.asarray(theta) - center + np.pi) % TAU - np.pi + center


def axial_double(theta: np.ndarray) -> np.ndarray:
    return wrap_angle(2.0 * np.asarray(theta), 0.0)


def unit_vectors(theta: np.ndarray) -> np.ndarray:
    theta = np.asarray(theta)
    return np.column_stack([np.cos(theta), np.sin(theta)])


def resultant(theta: np.ndarray) -> dict[str, float]:
    z = np.exp(1j * np.asarray(theta))
    mean_z = z.mean()
    return {
        "C": float(mean_z.real),
        "S": float(mean_z.imag),
        "R": float(abs(mean_z)),
        "mean": float(np.angle(mean_z)),
    }


def circular_mean(theta: np.ndarray) -> float:
    return resultant(theta)["mean"]


def trig_moment(theta: np.ndarray, p: int = 1, center: float = 0.0) -> complex:
    return complex(np.mean(np.exp(1j * p * wrap_angle(np.asarray(theta) - center))))


def circular_variance(theta: np.ndarray) -> float:
    return 1.0 - resultant(theta)["R"]


def circular_standard_deviation(theta: np.ndarray) -> float:
    r = max(resultant(theta)["R"], 1e-12)
    return float(np.sqrt(-2.0 * np.log(r)))


def circular_median(theta: np.ndarray, grid_size: int = 720) -> float:
    theta = wrap_angle(theta)
    grid = np.linspace(-np.pi, np.pi, grid_size, endpoint=False)
    distances = np.abs(wrap_angle(theta[:, None] - grid[None, :]))
    return float(grid[np.argmin(distances.sum(axis=0))])


def rose_histogram(theta: np.ndarray, bins: int = 16) -> tuple[np.ndarray, np.ndarray]:
    counts, edges = np.histogram(wrap_angle(theta, 0.0) % TAU, bins=bins, range=(0, TAU))
    return counts.astype(float), edges


def A1(kappa: np.ndarray | float) -> np.ndarray:
    kappa = np.asarray(kappa, dtype=float)
    return special.iv(1, kappa) / np.maximum(special.iv(0, kappa), 1e-300)


def inverse_A1(r: float) -> float:
    r = float(np.clip(r, 1e-9, 0.999999))
    if r < 0.53:
        guess = 2 * r + r**3 + 5 * r**5 / 6
    elif r < 0.85:
        guess = -0.4 + 1.39 * r + 0.43 / (1 - r)
    else:
        guess = 1 / (r**3 - 4 * r**2 + 3 * r)
    root = optimize.root_scalar(lambda k: float(A1(k) - r), bracket=[1e-8, max(guess * 3, 10.0)])
    return float(root.root)


def von_mises_pdf(theta: np.ndarray, mu: float = 0.0, kappa: float = 1.0) -> np.ndarray:
    return np.exp(kappa * np.cos(wrap_angle(theta - mu))) / (TAU * special.iv(0, kappa))


def rayleigh_statistic(theta: np.ndarray) -> float:
    theta = np.asarray(theta)
    return float(2 * len(theta) * resultant(theta)["R"] ** 2)


def kuiper_statistic(theta: np.ndarray) -> float:
    u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
    n = len(u)
    i = np.arange(1, n + 1)
    return float(np.max(i / n - u) + np.max(u - (i - 1) / n))


def watson_u2(theta: np.ndarray) -> float:
    u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
    n = len(u)
    i = np.arange(1, n + 1)
    centered = u - (2 * i - 1) / (2 * n)
    return float(np.sum((centered - centered.mean()) ** 2) + 1 / (12 * n))


def sample_vonmises(seed: int, n: int, mu: float, kappa: float) -> np.ndarray:
    return np.random.default_rng(seed).vonmises(mu, kappa, n)


def circular_cdf_grid(theta: np.ndarray, grid_size: int = 256) -> tuple[np.ndarray, np.ndarray]:
    u = np.sort((wrap_angle(theta, 0.0) % TAU) / TAU)
    grid = np.linspace(0, 1, grid_size)
    ecdf = np.searchsorted(u, grid, side="right") / len(u)
    return grid * TAU, ecdf


def uniform_reference_pvalue_rayleigh(theta: np.ndarray) -> float:
    return float(stats.chi2.sf(rayleigh_statistic(theta), df=2))
