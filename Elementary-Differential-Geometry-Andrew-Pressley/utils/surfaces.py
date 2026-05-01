"""Reusable surface computations for the Pressley course."""

from __future__ import annotations

import numpy as np


def sphere_patch(u: np.ndarray, v: np.ndarray, radius: float = 1.0) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    U, V = np.meshgrid(u, v, indexing="ij")
    return (
        radius * np.cos(U) * np.cos(V),
        radius * np.cos(U) * np.sin(V),
        radius * np.sin(U),
    )


def torus_patch(u: np.ndarray, v: np.ndarray, major: float = 2.0, minor: float = 0.65) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    U, V = np.meshgrid(u, v, indexing="ij")
    return (
        (major + minor * np.cos(U)) * np.cos(V),
        (major + minor * np.cos(U)) * np.sin(V),
        minor * np.sin(U),
    )


def catenoid_patch(u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    U, V = np.meshgrid(u, v, indexing="ij")
    return np.cosh(U) * np.cos(V), np.cosh(U) * np.sin(V), U


def helicoid_patch(u: np.ndarray, v: np.ndarray, pitch: float = 0.35) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    U, V = np.meshgrid(u, v, indexing="ij")
    return V * np.cos(U), V * np.sin(U), pitch * U


def partials(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    S = np.stack([X, Y, Z], axis=-1)
    Su = np.gradient(S, u, axis=0, edge_order=2)
    Sv = np.gradient(S, v, axis=1, edge_order=2)
    return Su, Sv


def normals(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    Su, Sv = partials(X, Y, Z, u, v)
    N = np.cross(Su, Sv)
    return N / np.maximum(np.linalg.norm(N, axis=-1, keepdims=True), 1e-12)


def first_fundamental_form(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    Su, Sv = partials(X, Y, Z, u, v)
    E = np.einsum("...i,...i->...", Su, Su)
    F = np.einsum("...i,...i->...", Su, Sv)
    G = np.einsum("...i,...i->...", Sv, Sv)
    return E, F, G


def graph_curvatures(f, x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X, Y = np.meshgrid(x, y, indexing="ij")
    Z = f(X, Y)
    zx = np.gradient(Z, x, axis=0, edge_order=2)
    zy = np.gradient(Z, y, axis=1, edge_order=2)
    zxx = np.gradient(zx, x, axis=0, edge_order=2)
    zxy = np.gradient(zx, y, axis=1, edge_order=2)
    zyy = np.gradient(zy, y, axis=1, edge_order=2)
    K = (zxx * zyy - zxy**2) / (1.0 + zx**2 + zy**2) ** 2
    H = ((1.0 + zy**2) * zxx - 2.0 * zx * zy * zxy + (1.0 + zx**2) * zyy) / (
        2.0 * (1.0 + zx**2 + zy**2) ** 1.5
    )
    return K, H


def clairaut_quantity(radius: np.ndarray, angle: np.ndarray) -> np.ndarray:
    return np.asarray(radius) * np.sin(angle)


def euler_characteristic(vertices: int, edges: int, faces: int) -> int:
    return int(vertices - edges + faces)
