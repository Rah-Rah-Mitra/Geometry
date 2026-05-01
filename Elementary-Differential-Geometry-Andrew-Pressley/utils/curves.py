"""Reusable curve computations for Pressley's elementary differential geometry."""

from __future__ import annotations

import numpy as np


def as_points(points: np.ndarray) -> np.ndarray:
    arr = np.asarray(points, dtype=float)
    if arr.ndim != 2:
        raise ValueError("points must be a two-dimensional array")
    return arr


def derivative(values: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    parameter = np.asarray(parameter, dtype=float)
    return np.gradient(values, parameter, axis=0, edge_order=2)


def speed(points: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    return np.linalg.norm(derivative(as_points(points), parameter), axis=1)


def arc_length(points: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    v = speed(points, parameter)
    ds = 0.5 * (v[1:] + v[:-1]) * np.diff(parameter)
    return np.concatenate([[0.0], np.cumsum(ds)])


def curvature_2d(points: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    if pts.shape[1] != 2:
        raise ValueError("curvature_2d expects planar points")
    d1 = derivative(pts, parameter)
    d2 = derivative(d1, parameter)
    cross = d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]
    denom = np.linalg.norm(d1, axis=1) ** 3
    return np.divide(cross, denom, out=np.zeros_like(cross), where=denom > 1e-12)


def curvature_3d(points: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    if pts.shape[1] != 3:
        raise ValueError("curvature_3d expects space-curve points")
    d1 = derivative(pts, parameter)
    d2 = derivative(d1, parameter)
    numerator = np.linalg.norm(np.cross(d1, d2), axis=1)
    denom = np.linalg.norm(d1, axis=1) ** 3
    return np.divide(numerator, denom, out=np.zeros_like(numerator), where=denom > 1e-12)


def torsion(points: np.ndarray, parameter: np.ndarray) -> np.ndarray:
    pts = as_points(points)
    if pts.shape[1] != 3:
        raise ValueError("torsion expects space-curve points")
    d1 = derivative(pts, parameter)
    d2 = derivative(d1, parameter)
    d3 = derivative(d2, parameter)
    cross = np.cross(d1, d2)
    denom = np.linalg.norm(cross, axis=1) ** 2
    numerator = np.einsum("ij,ij->i", cross, d3)
    return np.divide(numerator, denom, out=np.zeros_like(numerator), where=denom > 1e-12)


def frenet_frame(points: np.ndarray, parameter: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pts = as_points(points)
    d1 = derivative(pts, parameter)
    tangent = d1 / np.maximum(np.linalg.norm(d1, axis=1, keepdims=True), 1e-12)
    dt = derivative(tangent, parameter)
    normal = dt / np.maximum(np.linalg.norm(dt, axis=1, keepdims=True), 1e-12)
    if pts.shape[1] == 3:
        binormal = np.cross(tangent, normal)
    else:
        binormal = np.column_stack([-normal[:, 1], normal[:, 0]])
    return tangent, normal, binormal


def turning_number(points: np.ndarray, parameter: np.ndarray) -> float:
    pts = as_points(points)
    d1 = derivative(pts[:, :2], parameter)
    angles = np.unwrap(np.arctan2(d1[:, 1], d1[:, 0]))
    return float((angles[-1] - angles[0]) / (2.0 * np.pi))
