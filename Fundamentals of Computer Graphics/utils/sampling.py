"""Sampling helpers for graphics experiments."""

from __future__ import annotations

import numpy as np


def rng(seed: int = 7) -> np.random.Generator:
    return np.random.default_rng(seed)


def disk_samples(n: int = 512, seed: int = 7) -> np.ndarray:
    gen = rng(seed)
    r = np.sqrt(gen.random(n))
    theta = 2.0 * np.pi * gen.random(n)
    return np.column_stack([r * np.cos(theta), r * np.sin(theta)])


def hemisphere_samples(n: int = 512, seed: int = 7, cosine: bool = True) -> np.ndarray:
    gen = rng(seed)
    u1 = gen.random(n)
    u2 = gen.random(n)
    r = np.sqrt(u1) if cosine else np.sqrt(1.0 - (1.0 - u1) ** 2)
    phi = 2.0 * np.pi * u2
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    z = np.sqrt(np.clip(1.0 - x * x - y * y, 0.0, 1.0))
    return np.column_stack([x, y, z])


def estimate_integral(func, low: float = 0.0, high: float = 1.0, n: int = 2000, seed: int = 7) -> dict[str, float]:
    gen = rng(seed)
    x = gen.uniform(low, high, n)
    values = func(x)
    estimate = float((high - low) * np.mean(values))
    stderr = float((high - low) * np.std(values) / np.sqrt(n))
    return {"estimate": estimate, "stderr": stderr, "sample_count": int(n)}


def radial_cdf_error(samples: np.ndarray) -> float:
    radii = np.sort(np.linalg.norm(samples[:, :2], axis=1))
    empirical = np.arange(1, len(radii) + 1) / len(radii)
    target = radii * radii
    return float(np.max(np.abs(empirical - target)))
