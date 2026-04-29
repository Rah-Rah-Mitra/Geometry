"""Surface topology helpers for polygonal models and quotient domains."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SurfaceSummary:
    name: str
    orientable: bool
    euler: int
    geometry: str


def euler_handlebody(genus: int) -> int:
    return 2 - 2 * genus


def euler_crosscap(genus: int) -> int:
    return 2 - genus


def geometry_from_euler(euler: int, orientable: bool) -> str:
    if euler > 0:
        return "elliptic"
    if euler == 0:
        return "euclidean"
    return "hyperbolic"


def classify_catalog(name: str, orientable: bool, genus: int) -> SurfaceSummary:
    euler = euler_handlebody(genus) if orientable else euler_crosscap(genus)
    return SurfaceSummary(name=name, orientable=orientable, euler=euler, geometry=geometry_from_euler(euler, orientable))


def torus_distance(p: np.ndarray, q: np.ndarray, width: float, height: float) -> float:
    delta = np.asarray(q) - np.asarray(p)
    dx = min(abs(delta[0]), width - abs(delta[0]))
    dy = min(abs(delta[1]), height - abs(delta[1]))
    return float(math.hypot(dx, dy))


def torus_images(point: tuple[float, float], width: float, height: float, radius: int = 1) -> np.ndarray:
    x, y = point
    images = []
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            images.append((x + i * width, y + j * height))
    return np.asarray(images, dtype=float)


def gauss_bonnet_area(euler: int, k: float) -> float:
    if abs(k) < 1e-12:
        if euler != 0:
            raise ValueError("Flat constant-curvature surfaces require chi = 0")
        return math.inf
    return 2 * math.pi * euler / k
