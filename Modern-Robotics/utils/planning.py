"""Planning and trajectory helpers for compact notebook experiments."""

from __future__ import annotations

import heapq
from collections.abc import Iterable

import numpy as np


def cubic_time_scaling(t: np.ndarray, T: float) -> np.ndarray:
    tau = np.clip(np.asarray(t, dtype=float) / T, 0.0, 1.0)
    return 3 * tau**2 - 2 * tau**3


def quintic_time_scaling(t: np.ndarray, T: float) -> np.ndarray:
    tau = np.clip(np.asarray(t, dtype=float) / T, 0.0, 1.0)
    return 10 * tau**3 - 15 * tau**4 + 6 * tau**5


def grid_neighbors(node: tuple[int, int], shape: tuple[int, int]) -> Iterable[tuple[int, int]]:
    r, c = node
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < shape[0] and 0 <= nc < shape[1]:
            yield nr, nc


def dijkstra_grid(cost: np.ndarray, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    cost = np.asarray(cost, dtype=float)
    frontier: list[tuple[float, tuple[int, int]]] = [(0.0, start)]
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    best = {start: 0.0}
    while frontier:
        distance, current = heapq.heappop(frontier)
        if current == goal:
            break
        if distance > best[current]:
            continue
        for nxt in grid_neighbors(current, cost.shape):
            if np.isinf(cost[nxt]):
                continue
            nd = distance + cost[nxt]
            if nd < best.get(nxt, np.inf):
                best[nxt] = nd
                came_from[nxt] = current
                heapq.heappush(frontier, (nd, nxt))
    if goal not in came_from:
        return []
    path = []
    current: tuple[int, int] | None = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    return list(reversed(path))


def rrt_step(nearest: np.ndarray, sample: np.ndarray, step: float) -> np.ndarray:
    nearest = np.asarray(nearest, dtype=float)
    sample = np.asarray(sample, dtype=float)
    direction = sample - nearest
    norm = np.linalg.norm(direction)
    if norm <= step:
        return sample
    return nearest + step * direction / norm

