"""Computational topology helpers used by the Basic Topology notebooks."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Sequence
from math import atan2, pi

import numpy as np


def euler_characteristic(vertices: int, edges: int, faces: int = 0, cells3: int = 0) -> int:
    return vertices - edges + faces - cells3


def graph_euler_characteristic(edge_list: Iterable[tuple[object, object]]) -> int:
    edges = list(edge_list)
    vertices = {item for edge in edges for item in edge}
    return len(vertices) - len(edges)


def surface_chi(kind: str, parameter: int = 0) -> int:
    if kind == "sphere":
        return 2
    if kind == "orientable":
        return 2 - 2 * parameter
    if kind == "nonorientable":
        return 2 - parameter
    raise ValueError(f"unknown surface kind: {kind}")


def winding_number(points: Sequence[Sequence[float]], center: Sequence[float] = (0.0, 0.0)) -> int:
    pts = np.asarray(points, dtype=float)
    c = np.asarray(center, dtype=float)
    shifted = pts - c
    angles = np.unwrap(np.arctan2(shifted[:, 1], shifted[:, 0]))
    total = angles[-1] - angles[0]
    return int(round(total / (2 * pi)))


def reduce_word(letters: Sequence[str]) -> list[str]:
    stack: list[str] = []
    for letter in letters:
        if stack and stack[-1].swapcase() == letter:
            stack.pop()
        else:
            stack.append(letter)
    return stack


def word_reduction_trace(letters: Sequence[str]) -> list[list[str]]:
    trace = [[]]
    stack: list[str] = []
    for letter in letters:
        if stack and stack[-1].swapcase() == letter:
            stack.pop()
        else:
            stack.append(letter)
        trace.append(stack.copy())
    return trace


def count_components(vertices: Sequence[object], edges: Iterable[tuple[object, object]]) -> int:
    parent = {vertex: vertex for vertex in vertices}

    def find(value: object) -> object:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    return len({find(vertex) for vertex in vertices})


def polygon_word_summary(word: str) -> dict[str, object]:
    letters = [char for char in word if char.isalpha()]
    counts = Counter(char.lower() for char in letters)
    orientable = all(word.count(char.lower()) == 1 and word.count(char.upper()) == 1 for char in counts)
    pairs = len(counts)
    chi = 2 - 2 * max(1, pairs // 2) if orientable else 2 - pairs
    return {"word": word, "pairs": pairs, "orientable": orientable, "chi_estimate": chi}
