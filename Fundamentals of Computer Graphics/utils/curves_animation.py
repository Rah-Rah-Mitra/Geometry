"""Curve and animation helpers."""

from __future__ import annotations

import numpy as np

from .graphics_math import normalize


def de_casteljau(points: np.ndarray, t: float) -> np.ndarray:
    pts = np.asarray(points, dtype=float).copy()
    for r in range(1, len(pts)):
        pts[: len(pts) - r] = (1.0 - t) * pts[: len(pts) - r] + t * pts[1 : len(pts) - r + 1]
    return pts[0]


def bezier_curve(points: np.ndarray, count: int = 120) -> np.ndarray:
    ts = np.linspace(0.0, 1.0, count)
    return np.array([de_casteljau(points, t) for t in ts])


def catmull_rom(points: np.ndarray, count: int = 160) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    result = []
    per_segment = max(8, count // max(1, len(pts) - 3))
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for t in np.linspace(0.0, 1.0, per_segment, endpoint=False):
            t2, t3 = t * t, t * t * t
            result.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    result.append(pts[-2])
    return np.array(result)


def quaternion_slerp(q0: np.ndarray, q1: np.ndarray, t: float) -> np.ndarray:
    q0 = normalize(q0)
    q1 = normalize(q1)
    dot = float(np.dot(q0, q1))
    if dot < 0.0:
        q1 = -q1
        dot = -dot
    if dot > 0.9995:
        return normalize(q0 + t * (q1 - q0))
    theta0 = np.arccos(dot)
    theta = theta0 * t
    q2 = normalize(q1 - q0 * dot)
    return q0 * np.cos(theta) + q2 * np.sin(theta)


def skinning_weights(distance: np.ndarray, falloff: float = 4.0) -> np.ndarray:
    raw = np.exp(-falloff * np.asarray(distance, dtype=float))
    return raw / raw.sum(axis=-1, keepdims=True)
