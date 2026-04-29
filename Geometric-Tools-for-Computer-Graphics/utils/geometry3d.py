"""Readable 3D geometry helpers."""

from __future__ import annotations

import numpy as np


def plane_from_points(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> tuple[np.ndarray, float]:
    a, b, c = np.asarray(a, float), np.asarray(b, float), np.asarray(c, float)
    normal = np.cross(b - a, c - a)
    normal = normal / np.linalg.norm(normal)
    d = -float(np.dot(normal, a))
    return normal, d


def project_point_plane(point: np.ndarray, normal: np.ndarray, d: float) -> np.ndarray:
    p, n = np.asarray(point, float), np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    return p - (np.dot(n, p) + d) * n


def box_vertices(center: np.ndarray, half_extents: np.ndarray) -> np.ndarray:
    c, h = np.asarray(center, float), np.asarray(half_extents, float)
    signs = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]], dtype=float)
    return c + signs * h
