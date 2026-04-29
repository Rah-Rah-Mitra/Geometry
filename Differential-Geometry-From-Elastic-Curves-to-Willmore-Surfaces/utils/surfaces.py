"""Surface metric and curvature helpers."""

from __future__ import annotations

import numpy as np

EPS = 1e-12


def graph_surface(u: np.ndarray, v: np.ndarray, kind: str = "saddle") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if kind == "sphere":
        z = np.sqrt(np.maximum(1.0 - 0.15 * u * u - 0.15 * v * v, 0.0))
    elif kind == "bump":
        z = 0.35 * np.exp(-(u * u + v * v))
    elif kind == "cylinder":
        z = v
        return np.cos(u), np.sin(u), z
    else:
        z = 0.25 * (u * u - v * v)
    return u, v, z


def partials(x: np.ndarray, y: np.ndarray, z: np.ndarray, u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    fu = np.stack([np.gradient(x, axis=1), np.gradient(y, axis=1), np.gradient(z, axis=1)], axis=-1)
    fv = np.stack([np.gradient(x, axis=0), np.gradient(y, axis=0), np.gradient(z, axis=0)], axis=-1)
    return fu, fv


def normal_from_partials(fu: np.ndarray, fv: np.ndarray) -> np.ndarray:
    n = np.cross(fu, fv)
    return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), EPS)


def first_fundamental_form(fu: np.ndarray, fv: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    e = np.einsum("...i,...i->...", fu, fu)
    f = np.einsum("...i,...i->...", fu, fv)
    g = np.einsum("...i,...i->...", fv, fv)
    return e, f, g


def area_density(e: np.ndarray, f: np.ndarray, g: np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(e * g - f * f, 0.0))


def graph_curvature(z: np.ndarray, du: float, dv: float) -> tuple[np.ndarray, np.ndarray]:
    zx = np.gradient(z, du, axis=1, edge_order=2)
    zy = np.gradient(z, dv, axis=0, edge_order=2)
    zxx = np.gradient(zx, du, axis=1, edge_order=2)
    zyy = np.gradient(zy, dv, axis=0, edge_order=2)
    zxy = np.gradient(zx, dv, axis=0, edge_order=2)
    q = 1.0 + zx * zx + zy * zy
    h = ((1 + zy * zy) * zxx - 2 * zx * zy * zxy + (1 + zx * zx) * zyy) / (2 * q ** 1.5)
    k = (zxx * zyy - zxy * zxy) / (q * q)
    return h, k


def metric_j(e: float, f: float, g: float) -> np.ndarray:
    det = e * g - f * f
    root = np.sqrt(det)
    return np.array([[-f / root, -g / root], [e / root, f / root]])


def christoffel_placeholder(e: np.ndarray, f: np.ndarray, g: np.ndarray) -> np.ndarray:
    return np.stack([np.gradient(e, axis=0), np.gradient(f, axis=1), np.gradient(g, axis=0)], axis=0)
