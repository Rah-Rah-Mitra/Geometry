"""Tiny rendering helpers for teaching notebooks."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .graphics_math import normalize, stable_quadratic_roots


@dataclass(frozen=True)
class Ray:
    origin: np.ndarray
    direction: np.ndarray

    def at(self, t: float) -> np.ndarray:
        return np.asarray(self.origin, dtype=float) + t * np.asarray(self.direction, dtype=float)


def reflect(v: np.ndarray, normal: np.ndarray) -> np.ndarray:
    v = normalize(v)
    n = normalize(normal)
    return v - 2.0 * np.dot(v, n) * n


def sphere_intersect(ray: Ray, center: np.ndarray, radius: float) -> tuple[float, float] | None:
    oc = np.asarray(ray.origin, dtype=float) - np.asarray(center, dtype=float)
    d = np.asarray(ray.direction, dtype=float)
    return stable_quadratic_roots(float(np.dot(d, d)), float(2.0 * np.dot(oc, d)), float(np.dot(oc, oc) - radius * radius))


def lambert(normal: np.ndarray, light_dir: np.ndarray, color: np.ndarray) -> np.ndarray:
    return np.asarray(color, dtype=float) * max(0.0, float(np.dot(normalize(normal), normalize(light_dir))))


def blinn_phong(normal: np.ndarray, light_dir: np.ndarray, view_dir: np.ndarray, color: np.ndarray, *, shininess: float = 40.0, ks: float = 0.45) -> np.ndarray:
    n = normalize(normal)
    l = normalize(light_dir)
    v = normalize(view_dir)
    h = normalize(l + v)
    return lambert(n, l, color) + ks * max(0.0, float(np.dot(n, h))) ** shininess


def shaded_sphere_image(size: int = 220, *, light: np.ndarray | None = None, color: np.ndarray | None = None, specular: bool = True) -> np.ndarray:
    light = normalize(np.array([-0.35, 0.45, 1.0]) if light is None else light)
    color = np.array([0.35, 0.58, 0.82]) if color is None else np.asarray(color, dtype=float)
    y, x = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
    r2 = x * x + y * y
    mask = r2 <= 1.0
    z = np.sqrt(np.clip(1.0 - r2, 0.0, 1.0))
    normals = np.dstack([x, y, z])
    diffuse = np.clip(normals @ light, 0.0, 1.0)[..., None] * color
    if specular:
        view = np.array([0.0, 0.0, 1.0])
        h = normalize(light + view)
        diffuse += 0.55 * np.clip(normals @ h, 0.0, 1.0)[..., None] ** 70
    image = np.ones((size, size, 3)) * np.array([0.96, 0.97, 0.98])
    image[mask] = np.clip(0.08 + diffuse[mask], 0.0, 1.0)
    return image


def simple_path_trace_samples(count: int = 256, seed: int = 7) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    u = rng.random(count)
    v = rng.random(count)
    cos_theta = np.sqrt(1.0 - u)
    estimate = float(np.mean(cos_theta / (1.0 / (2.0 * np.pi))))
    return {"sample_count": count, "hemisphere_cosine_integral_estimate": estimate, "target": float(np.pi)}
