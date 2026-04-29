"""Raster image and color-array helpers."""

from __future__ import annotations

import numpy as np


def gamma_encode(linear: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    return np.clip(np.asarray(linear, dtype=float), 0.0, 1.0) ** (1.0 / gamma)


def gamma_decode(encoded: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    return np.clip(np.asarray(encoded, dtype=float), 0.0, 1.0) ** gamma


def alpha_over(fg: np.ndarray, bg: np.ndarray, alpha: np.ndarray | float) -> np.ndarray:
    fg = np.asarray(fg, dtype=float)
    bg = np.asarray(bg, dtype=float)
    a = np.asarray(alpha, dtype=float)
    if a.ndim == fg.ndim - 1:
        a = a[..., None]
    return fg * a + bg * (1.0 - a)


def checkerboard(width: int = 256, height: int = 256, checks: int = 8) -> np.ndarray:
    y, x = np.indices((height, width))
    cells = ((x * checks // width) + (y * checks // height)) % 2
    return np.where(cells[..., None] == 0, np.array([0.92, 0.92, 0.92]), np.array([0.15, 0.18, 0.22]))


def gradient(width: int = 256, height: int = 80) -> np.ndarray:
    ramp = np.linspace(0.0, 1.0, width)
    return np.repeat(ramp[None, :, None], height, axis=0).repeat(3, axis=2)


def quantize(image: np.ndarray, levels: int) -> np.ndarray:
    image = np.clip(np.asarray(image, dtype=float), 0.0, 1.0)
    return np.round(image * (levels - 1)) / max(levels - 1, 1)


def bayer_masks(height: int, width: int) -> dict[str, np.ndarray]:
    y, x = np.indices((height, width))
    return {
        "red": (y % 2 == 0) & (x % 2 == 0),
        "green": ((y + x) % 2 == 1),
        "blue": (y % 2 == 1) & (x % 2 == 1),
    }
