"""Seeded simulation helpers."""

from __future__ import annotations

import numpy as np


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def quantile_summary(values: np.ndarray, probs: tuple[float, ...] = (0.05, 0.5, 0.95)) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    return {f"q{int(p * 100):02d}": float(np.quantile(values, p)) for p in probs}


def monte_carlo_resultants(seed: int, n: int, reps: int) -> np.ndarray:
    gen = np.random.default_rng(seed)
    theta = gen.uniform(0, 2 * np.pi, size=(reps, n))
    return np.abs(np.exp(1j * theta).mean(axis=1))
