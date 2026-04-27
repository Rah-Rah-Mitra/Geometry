"""Reusable visual helpers for the VDGF notebooks."""

from __future__ import annotations

import numpy as np


def unit_circle(samples: int = 240) -> tuple[np.ndarray, np.ndarray]:
    theta = np.linspace(0, 2 * np.pi, samples)
    return np.cos(theta), np.sin(theta)


def saddle_grid(samples: int = 40, extent: float = 1.5) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.linspace(-extent, extent, samples)
    y = np.linspace(-extent, extent, samples)
    X, Y = np.meshgrid(x, y)
    return X, Y, X**2 - Y**2


def form_stack_lines(slope: float = 1.0, offsets: int = 6, extent: float = 2.0) -> list[tuple[np.ndarray, np.ndarray]]:
    x = np.linspace(-extent, extent, 100)
    lines = []
    for b in np.linspace(-extent, extent, offsets):
        y = -slope * x + b
        lines.append((x, y))
    return lines
