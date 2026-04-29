"""Small linear algebra helpers used by the GTCG notebooks."""

from __future__ import annotations

import numpy as np


def rotation2d(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def affine_matrix(linear: np.ndarray, translation: np.ndarray) -> np.ndarray:
    linear = np.asarray(linear, dtype=float)
    translation = np.asarray(translation, dtype=float)
    dim = linear.shape[0]
    mat = np.eye(dim + 1)
    mat[:dim, :dim] = linear
    mat[:dim, dim] = translation
    return mat


def transform_points(points: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    ones = np.ones((len(points), 1))
    hom = np.hstack([points, ones])
    out = hom @ np.asarray(matrix, dtype=float).T
    return out[:, :-1] / out[:, [-1]]


def rotation3d_axis_angle(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    c, s = np.cos(theta), np.sin(theta)
    C = 1 - c
    return np.array([
        [c + x*x*C, x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, c + y*y*C, y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, c + z*z*C],
    ])


def row_reduce(a: np.ndarray, tol: float = 1e-12) -> tuple[np.ndarray, list[int]]:
    m = np.array(a, dtype=float, copy=True)
    pivots: list[int] = []
    row = 0
    for col in range(m.shape[1]):
        pivot = row + int(np.argmax(np.abs(m[row:, col])))
        if abs(m[pivot, col]) <= tol:
            continue
        m[[row, pivot]] = m[[pivot, row]]
        m[row] = m[row] / m[row, col]
        for r in range(m.shape[0]):
            if r != row:
                m[r] -= m[r, col] * m[row]
        pivots.append(col)
        row += 1
        if row == m.shape[0]:
            break
    return m, pivots
