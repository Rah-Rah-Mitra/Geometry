from __future__ import annotations

import math
from itertools import product

import numpy as np


def hpoint(x: float, y: float, w: float = 1.0) -> np.ndarray:
    return np.array([x, y, w], dtype=float)


def normalize_h(vector: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    arr = np.asarray(vector, dtype=float)
    idx = int(np.argmax(np.abs(arr)))
    if abs(arr[idx]) < tol:
        return arr.copy()
    return arr / arr[idx]


def join(p: np.ndarray, q: np.ndarray) -> np.ndarray:
    return np.cross(np.asarray(p, dtype=float), np.asarray(q, dtype=float))


def meet(line_a: np.ndarray, line_b: np.ndarray) -> np.ndarray:
    return np.cross(np.asarray(line_a, dtype=float), np.asarray(line_b, dtype=float))


def affine(point: np.ndarray, tol: float = 1e-12) -> np.ndarray:
    arr = np.asarray(point, dtype=float)
    if abs(arr[2]) < tol:
        raise ValueError("point at infinity")
    return arr[:2] / arr[2]


def incidence(point: np.ndarray, line: np.ndarray, tol: float = 1e-9) -> bool:
    return abs(float(np.dot(np.asarray(point, dtype=float), np.asarray(line, dtype=float)))) < tol


def bracket(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    return float(np.linalg.det(np.column_stack([a, b, c])))


def cross_ratio(a: complex, b: complex, c: complex, d: complex) -> complex:
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def mobius_real(x: float, a: float, b: float, c: float, d: float) -> float:
    den = c * x + d
    if abs(den) < 1e-12:
        return math.inf
    return float((a * x + b) / den)


def mobius_complex(z: complex, a: complex, b: complex, c: complex, d: complex) -> complex:
    return (a * z + b) / (c * z + d)


def apply_projective(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    mat = np.asarray(matrix, dtype=float)
    pts = np.asarray(points, dtype=float)
    if pts.ndim == 1:
        return mat @ pts
    return (mat @ pts.T).T


def line_parameter(point_a: np.ndarray, point_b: np.ndarray, steps: int = 100) -> np.ndarray:
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    ts = np.linspace(0, 1, steps)
    return np.array([(1 - t) * a + t * b for t in ts])


def fano_plane() -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    points = [
        tuple(v)
        for v in product([0, 1], repeat=3)
        if v != (0, 0, 0)
    ]
    lines: list[tuple[int, int, int]] = []
    for coeff in points:
        line = tuple(i for i, p in enumerate(points) if sum(c * x for c, x in zip(coeff, p)) % 2 == 0)
        if len(line) == 3 and line not in lines:
            lines.append(line)
    return points, lines

