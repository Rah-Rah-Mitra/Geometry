"""Plane-curve invariants used in visual differential geometry examples."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class OsculatingCircle:
    """Center, radius, and signed curvature of the circle tangent to a curve."""

    center: np.ndarray
    radius: float | np.ndarray
    curvature: float | np.ndarray


def _as_plane_vectors(values: np.ndarray, name: str) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if values.shape[-1:] != (2,):
        raise ValueError(f"{name} must have shape (..., 2)")
    return values


def plane_curve_curvature(
    velocity: np.ndarray,
    acceleration: np.ndarray,
    *,
    signed: bool = True,
) -> float | np.ndarray:
    """Return curvature of a regular plane curve from its first two derivatives.

    The signed convention is positive when the velocity turns counterclockwise.
    Inputs may be individual 2-vectors or arrays with shape ``(..., 2)``.
    """

    velocity = _as_plane_vectors(velocity, "velocity")
    acceleration = _as_plane_vectors(acceleration, "acceleration")
    speed = np.linalg.norm(velocity, axis=-1)
    if np.any(speed <= EPS):
        raise ValueError("curvature is undefined where the curve speed is zero")
    cross = velocity[..., 0] * acceleration[..., 1] - velocity[..., 1] * acceleration[..., 0]
    curvature = cross / speed**3
    if not signed:
        curvature = np.abs(curvature)
    return float(curvature) if np.ndim(curvature) == 0 else curvature


def osculating_circle(
    point: np.ndarray,
    velocity: np.ndarray,
    acceleration: np.ndarray,
) -> OsculatingCircle:
    """Return the oriented osculating circle for a regular, curved plane point."""

    point = _as_plane_vectors(point, "point")
    velocity = _as_plane_vectors(velocity, "velocity")
    curvature = plane_curve_curvature(velocity, acceleration, signed=True)
    curvature_array = np.asarray(curvature, dtype=float)
    if np.any(np.abs(curvature_array) <= EPS):
        raise ValueError("osculating circle is undefined where curvature is zero")

    speed = np.linalg.norm(velocity, axis=-1)
    unit_tangent = velocity / speed[..., np.newaxis]
    left_normal = np.stack([-unit_tangent[..., 1], unit_tangent[..., 0]], axis=-1)
    center = point + left_normal / curvature_array[..., np.newaxis]
    radius = np.abs(1.0 / curvature_array)

    if np.ndim(curvature_array) == 0:
        return OsculatingCircle(center=center, radius=float(radius), curvature=float(curvature_array))
    return OsculatingCircle(center=center, radius=radius, curvature=curvature_array)
