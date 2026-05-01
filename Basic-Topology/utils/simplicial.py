"""Simplicial-complex helpers for visual and algebraic checks."""

from __future__ import annotations

from itertools import combinations
from typing import Sequence

import numpy as np


def simplex_faces(simplex: Sequence[int]) -> list[tuple[int, ...]]:
    return [tuple(face) for r in range(1, len(simplex)) for face in combinations(simplex, r)]


def boundary_matrix(k_simplices: Sequence[Sequence[int]], faces: Sequence[Sequence[int]]) -> np.ndarray:
    face_index = {tuple(face): i for i, face in enumerate(faces)}
    matrix = np.zeros((len(faces), len(k_simplices)), dtype=int)
    for col, simplex in enumerate(k_simplices):
        simplex = tuple(simplex)
        for i in range(len(simplex)):
            face = simplex[:i] + simplex[i + 1 :]
            row = face_index.get(face)
            sign = -1 if i % 2 else 1
            if row is None:
                reversed_face = tuple(reversed(face))
                row = face_index[reversed_face]
                sign *= -1
            matrix[row, col] = sign
    return matrix


def rank(matrix: np.ndarray, tol: float = 1e-9) -> int:
    if matrix.size == 0:
        return 0
    return int(np.linalg.matrix_rank(matrix.astype(float), tol=tol))


def betti_number(chain_dim: int, boundary_out: np.ndarray, boundary_in: np.ndarray) -> int:
    return chain_dim - rank(boundary_out) - rank(boundary_in)


def barycentric_triangle() -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    vertices = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [0.35, 0.9],
            [0.5, 0.0],
            [0.675, 0.45],
            [0.175, 0.45],
            [0.45, 0.3],
        ]
    )
    triangles = [(0, 3, 6), (3, 1, 6), (1, 4, 6), (4, 2, 6), (2, 5, 6), (5, 0, 6)]
    return vertices, triangles
