"""Polyhedra meshes and diagnostics for the Euclid and Beyond course."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Mesh:
    vertices: np.ndarray
    faces: list[tuple[int, ...]]


def tetrahedron() -> Mesh:
    vertices = np.array(
        [
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
        ],
        dtype=float,
    )
    faces = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
    return Mesh(normalize(vertices), faces)


def cube() -> Mesh:
    vertices = np.array(
        [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],
        ],
        dtype=float,
    )
    faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return Mesh(normalize(vertices), faces)


def octahedron() -> Mesh:
    vertices = np.array(
        [
            [1, 0, 0],
            [-1, 0, 0],
            [0, 1, 0],
            [0, -1, 0],
            [0, 0, 1],
            [0, 0, -1],
        ],
        dtype=float,
    )
    faces = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    return Mesh(vertices, faces)


def icosahedron() -> Mesh:
    phi = (1 + math.sqrt(5)) / 2
    vertices = np.array(
        [
            [-1, phi, 0],
            [1, phi, 0],
            [-1, -phi, 0],
            [1, -phi, 0],
            [0, -1, phi],
            [0, 1, phi],
            [0, -1, -phi],
            [0, 1, -phi],
            [phi, 0, -1],
            [phi, 0, 1],
            [-phi, 0, -1],
            [-phi, 0, 1],
        ],
        dtype=float,
    )
    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
    ]
    return Mesh(normalize(vertices), faces)


def normalize(vertices: np.ndarray) -> np.ndarray:
    radius = np.max(np.linalg.norm(vertices, axis=1))
    return vertices / radius


def edges(faces: list[tuple[int, ...]]) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for face in faces:
        for a, b in zip(face, face[1:] + face[:1]):
            result.add(tuple(sorted((a, b))))
    return result


def euler_characteristic(mesh: Mesh) -> int:
    return int(len(mesh.vertices) - len(edges(mesh.faces)) + len(mesh.faces))


def named_meshes() -> dict[str, Mesh]:
    return {
        "tetrahedron": tetrahedron(),
        "cube": cube(),
        "octahedron": octahedron(),
        "icosahedron": icosahedron(),
    }
