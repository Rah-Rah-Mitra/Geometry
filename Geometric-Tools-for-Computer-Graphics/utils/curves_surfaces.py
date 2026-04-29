"""Curve and surface helpers."""

from __future__ import annotations

import numpy as np


def bezier_curve(control: np.ndarray, samples: int = 120) -> np.ndarray:
    control = np.asarray(control, dtype=float)
    t = np.linspace(0.0, 1.0, samples)
    points = np.zeros((samples, control.shape[1]))
    n = len(control) - 1
    from math import comb

    for i, p in enumerate(control):
        basis = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
        points += basis[:, None] * p
    return points


def torus_grid(major: float = 1.4, minor: float = 0.35, nu: int = 50, nv: int = 20) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.linspace(0, 2 * np.pi, nu)
    v = np.linspace(0, 2 * np.pi, nv)
    uu, vv = np.meshgrid(u, v)
    x = (major + minor * np.cos(vv)) * np.cos(uu)
    y = (major + minor * np.cos(vv)) * np.sin(uu)
    z = minor * np.sin(vv)
    return x, y, z
