"""Special-function wrappers for directional distributions."""

from __future__ import annotations

import numpy as np
from scipy import optimize, special


def modified_bessel(order: float, x: np.ndarray | float) -> np.ndarray:
    return special.iv(order, x)


def bessel_ratio(order: float, x: np.ndarray | float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return special.iv(order + 1, x) / np.maximum(special.iv(order, x), 1e-300)


def inverse_bessel_ratio(order: float, r: float) -> float:
    r = float(np.clip(r, 1e-9, 0.999999))
    root = optimize.root_scalar(lambda k: float(bessel_ratio(order, k) - r), bracket=[1e-8, 1e4])
    return float(root.root)


def kummer(a: float, b: float, x: np.ndarray | float) -> np.ndarray:
    return special.hyp1f1(a, b, x)


def small_kappa_A1(kappa: np.ndarray | float) -> np.ndarray:
    k = np.asarray(kappa, dtype=float)
    return k / 2 - k**3 / 16 + k**5 / 96


def large_kappa_A1(kappa: np.ndarray | float) -> np.ndarray:
    k = np.asarray(kappa, dtype=float)
    return 1 - 1 / (2 * k) - 1 / (8 * k**2)
