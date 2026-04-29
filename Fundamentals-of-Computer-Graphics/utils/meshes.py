"""Mesh and spatial-structure helpers."""

from __future__ import annotations

from collections import Counter

import numpy as np


def cube_mesh() -> tuple[np.ndarray, np.ndarray]:
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
    faces = np.array(
        [
            [0, 1, 2], [0, 2, 3], [4, 6, 5], [4, 7, 6],
            [0, 4, 5], [0, 5, 1], [1, 5, 6], [1, 6, 2],
            [2, 6, 7], [2, 7, 3], [3, 7, 4], [3, 4, 0],
        ],
        dtype=int,
    )
    return vertices, faces


def edge_counts(faces: np.ndarray) -> Counter[tuple[int, int]]:
    counts: Counter[tuple[int, int]] = Counter()
    for face in np.asarray(faces, dtype=int):
        for a, b in [(face[0], face[1]), (face[1], face[2]), (face[2], face[0])]:
            counts[tuple(sorted((int(a), int(b))))] += 1
    return counts


def mesh_summary(vertices: np.ndarray, faces: np.ndarray) -> dict[str, int | float]:
    counts = edge_counts(faces)
    boundary = sum(1 for value in counts.values() if value == 1)
    nonmanifold = sum(1 for value in counts.values() if value > 2)
    mins = np.min(vertices, axis=0)
    maxs = np.max(vertices, axis=0)
    return {
        "vertices": int(len(vertices)),
        "faces": int(len(faces)),
        "edges": int(len(counts)),
        "boundary_edges": int(boundary),
        "nonmanifold_edges": int(nonmanifold),
        "bbox_diagonal": float(np.linalg.norm(maxs - mins)),
    }


def tiled_index(x: int, y: int, width: int, tile: int) -> int:
    tiles_per_row = (width + tile - 1) // tile
    tile_x, local_x = divmod(x, tile)
    tile_y, local_y = divmod(y, tile)
    return (tile_y * tiles_per_row + tile_x) * tile * tile + local_y * tile + local_x
