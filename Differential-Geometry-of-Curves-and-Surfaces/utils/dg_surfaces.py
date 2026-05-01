"""Numerical helpers for parametrized surfaces."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

Array = np.ndarray
Surface = Callable[[Array, Array], tuple[Array, Array, Array]]


def meshgrid(u_range: tuple[float, float], v_range: tuple[float, float], n: int = 80) -> tuple[Array, Array]:
    """Create a rectangular parameter mesh."""

    u = np.linspace(u_range[0], u_range[1], n)
    v = np.linspace(v_range[0], v_range[1], n)
    return np.meshgrid(u, v, indexing="ij")


def stack_surface(surface: Surface, u: Array, v: Array) -> Array:
    """Return an (..., 3) array for a parametrized surface."""

    x, y, z = surface(u, v)
    return np.stack([x, y, z], axis=-1)


def partials(points: Array, u: Array, v: Array) -> tuple[Array, Array]:
    """Estimate coordinate partial derivatives for sampled surface points."""

    du_axis = u[:, 0]
    dv_axis = v[0, :]
    xu = np.gradient(points, du_axis, axis=0, edge_order=2)
    xv = np.gradient(points, dv_axis, axis=1, edge_order=2)
    return xu, xv


def first_fundamental_form(xu: Array, xv: Array) -> tuple[Array, Array, Array]:
    """Return E, F, G coefficients of the first fundamental form."""

    e = np.einsum("...i,...i->...", xu, xu)
    f = np.einsum("...i,...i->...", xu, xv)
    g = np.einsum("...i,...i->...", xv, xv)
    return e, f, g


def unit_normals(xu: Array, xv: Array) -> Array:
    """Return unit normal vectors from coordinate partial derivatives."""

    normal = np.cross(xu, xv)
    norm = np.linalg.norm(normal, axis=-1, keepdims=True)
    return np.divide(normal, norm, out=np.zeros_like(normal), where=norm > 1e-12)


def graph_surface_curvature(x: Array, y: Array, z: Array) -> tuple[Array, Array]:
    """Estimate Gaussian and mean curvature for a graph z=f(x,y)."""

    fx = np.gradient(z, x[:, 0], axis=0, edge_order=2)
    fy = np.gradient(z, y[0, :], axis=1, edge_order=2)
    fxx = np.gradient(fx, x[:, 0], axis=0, edge_order=2)
    fxy = np.gradient(fx, y[0, :], axis=1, edge_order=2)
    fyy = np.gradient(fy, y[0, :], axis=1, edge_order=2)
    denom = 1.0 + fx * fx + fy * fy
    gaussian = (fxx * fyy - fxy * fxy) / (denom * denom)
    mean = ((1 + fy * fy) * fxx - 2 * fx * fy * fxy + (1 + fx * fx) * fyy) / (2 * denom ** 1.5)
    return gaussian, mean


def metric_ellipse(matrix: Array, radius: float = 1.0, samples: int = 240) -> Array:
    """Return vectors v with v^T matrix v = radius^2."""

    theta = np.linspace(0.0, 2.0 * np.pi, samples)
    circle = np.column_stack([np.cos(theta), np.sin(theta)])
    transform = np.linalg.cholesky(np.linalg.inv(matrix))
    return radius * circle @ transform.T


def torus(u: Array, v: Array, major: float = 2.0, minor: float = 0.65) -> tuple[Array, Array, Array]:
    """Standard torus parametrization."""

    x = (major + minor * np.cos(v)) * np.cos(u)
    y = (major + minor * np.cos(v)) * np.sin(u)
    z = minor * np.sin(v)
    return x, y, z


def sphere(u: Array, v: Array, radius: float = 1.0) -> tuple[Array, Array, Array]:
    """Sphere parametrization with polar angle u and azimuth v."""

    x = radius * np.sin(u) * np.cos(v)
    y = radius * np.sin(u) * np.sin(v)
    z = radius * np.cos(u)
    return x, y, z
