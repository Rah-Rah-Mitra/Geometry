"""Color, tone, and perception helpers."""

from __future__ import annotations

import numpy as np

SRGB_TO_XYZ = np.array(
    [
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ]
)
XYZ_TO_SRGB = np.linalg.inv(SRGB_TO_XYZ)
D65 = np.array([0.95047, 1.0, 1.08883])


def srgb_encode(linear: np.ndarray) -> np.ndarray:
    linear = np.clip(np.asarray(linear, dtype=float), 0.0, 1.0)
    return np.where(linear <= 0.0031308, 12.92 * linear, 1.055 * linear ** (1 / 2.4) - 0.055)


def srgb_decode(encoded: np.ndarray) -> np.ndarray:
    encoded = np.clip(np.asarray(encoded, dtype=float), 0.0, 1.0)
    return np.where(encoded <= 0.04045, encoded / 12.92, ((encoded + 0.055) / 1.055) ** 2.4)


def rgb_to_xyz(rgb: np.ndarray) -> np.ndarray:
    return np.asarray(rgb, dtype=float) @ SRGB_TO_XYZ.T


def xyz_to_rgb(xyz: np.ndarray) -> np.ndarray:
    return np.asarray(xyz, dtype=float) @ XYZ_TO_SRGB.T


def luminance(rgb: np.ndarray) -> np.ndarray:
    return rgb_to_xyz(rgb)[..., 1]


def reinhard_tone_map(rgb: np.ndarray, exposure: float = 1.0) -> np.ndarray:
    hdr = np.asarray(rgb, dtype=float) * exposure
    return hdr / (1.0 + hdr)


def xy_chromaticity(xyz: np.ndarray) -> np.ndarray:
    xyz = np.asarray(xyz, dtype=float)
    denom = np.maximum(np.sum(xyz, axis=-1, keepdims=True), 1e-12)
    return xyz[..., :2] / denom


def lab_f(t: np.ndarray) -> np.ndarray:
    delta = 6 / 29
    return np.where(t > delta**3, np.cbrt(t), t / (3 * delta * delta) + 4 / 29)


def xyz_to_lab(xyz: np.ndarray, white: np.ndarray = D65) -> np.ndarray:
    ratio = np.asarray(xyz, dtype=float) / white
    f = lab_f(ratio)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], axis=-1)


def contrast_sensitivity(frequency: np.ndarray) -> np.ndarray:
    f = np.asarray(frequency, dtype=float)
    return 2.6 * (0.0192 + 0.114 * f) * np.exp(-(0.114 * f) ** 1.1)
