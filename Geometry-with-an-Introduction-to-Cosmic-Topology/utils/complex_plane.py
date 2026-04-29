"""Complex-plane helpers for GICT notebooks."""

from __future__ import annotations

import math

import numpy as np


def principal_arg(z: complex) -> float:
    return float(np.angle(z))


def angle_mod_2pi(theta: float) -> float:
    return float((theta + np.pi) % (2 * np.pi) - np.pi)


def complex_to_polar(z: complex) -> tuple[float, float]:
    return abs(z), principal_arg(z)


def from_polar(radius: float, theta: float) -> complex:
    return complex(radius * math.cos(theta), radius * math.sin(theta))


def oriented_angle(u: complex, v: complex, w: complex) -> float:
    """Return the oriented angle from ray v->u to ray v->w."""
    return principal_arg((w - v) / (u - v))


def complex_grid(extent: float = 2.0, count: int = 9) -> list[np.ndarray]:
    values = np.linspace(-extent, extent, count)
    lines: list[np.ndarray] = []
    t = np.linspace(-extent, extent, 160)
    for value in values:
        lines.append(t + 1j * value)
        lines.append(value + 1j * t)
    return lines


def unit_circle(samples: int = 240) -> np.ndarray:
    theta = np.linspace(0, 2 * np.pi, samples)
    return np.exp(1j * theta)
