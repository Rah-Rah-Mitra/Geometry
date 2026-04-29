"""Curve calculations used by the notebooks."""

from __future__ import annotations

import numpy as np
from scipy.interpolate import interp1d

EPS = 1e-12


def as_points(points: np.ndarray) -> np.ndarray:
    arr = np.asarray(points, dtype=float)
    if arr.ndim != 2:
        raise ValueError("points must be an array of shape (n, dim)")
    return arr


def derivatives(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts = as_points(points)
    if parameter is None:
        return np.gradient(pts, axis=0, edge_order=2)
    return np.gradient(pts, np.asarray(parameter, dtype=float), axis=0, edge_order=2)


def speed(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    return np.linalg.norm(derivatives(points, parameter), axis=1)


def length(points: np.ndarray) -> float:
    pts = as_points(points)
    return float(np.linalg.norm(np.diff(pts, axis=0), axis=1).sum())


def arclength(points: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    ds = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    return np.concatenate([[0.0], np.cumsum(ds)])


def resample_by_arclength(points: np.ndarray, samples: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    pts = as_points(points)
    s = arclength(pts)
    if samples is None:
        samples = len(pts)
    target = np.linspace(0.0, float(s[-1]), samples)
    cols = [interp1d(s, pts[:, i], kind="linear")(target) for i in range(pts.shape[1])]
    return np.column_stack(cols), target


def unit_tangent(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    d = derivatives(points, parameter)
    n = np.linalg.norm(d, axis=1, keepdims=True)
    if np.any(n <= EPS):
        raise ValueError("unit tangent is undefined where speed vanishes")
    return d / n


def plane_curvature(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts = as_points(points)
    if pts.shape[1] != 2:
        raise ValueError("plane curvature expects 2D points")
    d1 = derivatives(pts, parameter)
    d2 = derivatives(d1, parameter)
    cross = d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]
    denom = np.linalg.norm(d1, axis=1) ** 3
    return cross / np.maximum(denom, EPS)


def bending_energy(points: np.ndarray, parameter: np.ndarray | None = None) -> float:
    pts = as_points(points)
    if pts.shape[1] == 2:
        kappa = plane_curvature(pts, parameter)
    else:
        t = unit_tangent(pts, parameter)
        dt = derivatives(t, parameter)
        spd = speed(pts, parameter)
        kappa = np.linalg.norm(dt, axis=1) / np.maximum(spd, EPS)
    s = arclength(pts)
    return float(0.5 * np.trapz(kappa * kappa, s))


def signed_area(points: np.ndarray) -> float:
    pts = as_points(points)
    if pts.shape[1] != 2:
        raise ValueError("signed area expects 2D points")
    x, y = pts[:, 0], pts[:, 1]
    return float(0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]))


def tangent_winding(points: np.ndarray) -> float:
    t = unit_tangent(points)
    if t.shape[1] != 2:
        raise ValueError("winding expects a plane curve")
    angle = np.unwrap(np.arctan2(t[:, 1], t[:, 0]))
    return float((angle[-1] - angle[0]) / (2 * np.pi))
