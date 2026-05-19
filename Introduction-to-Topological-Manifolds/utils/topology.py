"""Small topology utilities used by multiple ITM notebooks."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, Sequence

import numpy as np
import sympy as sp


def euler_characteristic(vertices: int, edges: int, faces: int = 0) -> int:
    return int(vertices - edges + faces)


def orientability_from_schema(word: Sequence[str]) -> bool:
    """Return True when every edge label appears once in each orientation."""
    signs: dict[str, list[int]] = {}
    for token in word:
        label = token.strip("-")
        signs.setdefault(label, []).append(-1 if token.startswith("-") else 1)
    return all(sorted(values) == [-1, 1] for values in signs.values())


def boundary_matrix(edges: Sequence[tuple[int, int]], vertex_count: int) -> sp.Matrix:
    matrix = sp.zeros(vertex_count, len(edges))
    for j, (tail, head) in enumerate(edges):
        matrix[tail, j] -= 1
        matrix[head, j] += 1
    return matrix


def cycle_rank_for_graph(vertex_count: int, edge_count: int, component_count: int = 1) -> int:
    return int(edge_count - vertex_count + component_count)


def word_reduce(word: Iterable[str]) -> list[str]:
    stack: list[str] = []
    for letter in word:
        if stack and stack[-1] == inverse_letter(letter):
            stack.pop()
        else:
            stack.append(letter)
    return stack


def inverse_letter(letter: str) -> str:
    return letter[:-3] if letter.endswith("^-1") else f"{letter}^-1"


def abelianization_vector(word: Iterable[str], generators: Sequence[str]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for letter in word:
        if letter.endswith("^-1"):
            counts[letter[:-3]] -= 1
        else:
            counts[letter] += 1
    return {generator: int(counts[generator]) for generator in generators}


def simplex_boundary_squared_zero(simplex_count: int = 3) -> bool:
    """Tiny exact check for d_1 d_2 = 0 on one oriented triangle."""
    if simplex_count != 3:
        raise ValueError("This helper models the single 2-simplex triangle.")
    d1 = sp.Matrix([[-1, 0, -1], [1, -1, 0], [0, 1, 1]])
    d2 = sp.Matrix([[1], [1], [-1]])
    return d1 * d2 == sp.zeros(3, 1)


def finite_open_sets(points: Sequence[str], opens: Iterable[Iterable[str]]) -> set[frozenset[str]]:
    universe = frozenset(points)
    topology = {frozenset(item) for item in opens}
    topology.add(frozenset())
    topology.add(universe)
    return topology


def is_topology(points: Sequence[str], opens: Iterable[Iterable[str]]) -> bool:
    topology = finite_open_sets(points, opens)
    finite = list(topology)
    for a in finite:
        for b in finite:
            if a | b not in topology or a & b not in topology:
                return False
    for mask in range(1 << len(finite)):
        union = frozenset().union(*(finite[i] for i in range(len(finite)) if mask & (1 << i)))
        if union not in topology:
            return False
    return True


def sampled_circle(turns: float, samples: int = 240) -> np.ndarray:
    t = np.linspace(0.0, 1.0, samples)
    theta = 2 * np.pi * turns * t
    return np.column_stack([np.cos(theta), np.sin(theta)])
