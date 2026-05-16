"""Small graph and metric models for geometric group theory notebooks."""

from __future__ import annotations

from collections import deque
from itertools import combinations
from math import cos, pi, sin
from typing import Iterable

import networkx as nx
import numpy as np


def integer_line_graph(radius: int) -> nx.Graph:
    """Return the radius-r word ball in the Cayley graph of Z with generator 1."""

    graph = nx.Graph()
    for x in range(-radius, radius + 1):
        graph.add_node(x, word_length=abs(x))
    for x in range(-radius, radius):
        graph.add_edge(x, x + 1, generator="t")
    return graph


def integer_grid_graph(radius: int, *, diagonal: bool = False) -> nx.Graph:
    """Return a finite Cayley ball model for Z^2."""

    graph = nx.Graph()
    generators = [(1, 0), (0, 1)]
    if diagonal:
        generators.append((1, 1))
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            word_length = min(abs(x) + abs(y), max(abs(x), abs(y)) if diagonal else abs(x) + abs(y))
            graph.add_node((x, y), word_length=word_length)
    nodes = set(graph.nodes)
    for x, y in list(nodes):
        for dx, dy in generators:
            neighbor = (x + dx, y + dy)
            if neighbor in nodes:
                graph.add_edge((x, y), neighbor, generator=f"{dx},{dy}")
    return graph


def free_group_ball(radius: int, generators: tuple[str, ...] = ("a", "b")) -> nx.Graph:
    """Return the radius-r ball in a free group's Cayley tree."""

    alphabet = tuple(generators) + tuple(g.upper() for g in generators)
    inverse = {g: g.upper() for g in generators} | {g.upper(): g for g in generators}
    root: tuple[str, ...] = ()
    graph = nx.Graph()
    graph.add_node(root, word_length=0, label="e")
    queue: deque[tuple[str, ...]] = deque([root])
    while queue:
        word = queue.popleft()
        if len(word) >= radius:
            continue
        for letter in alphabet:
            if word and inverse[letter] == word[-1]:
                continue
            child = word + (letter,)
            if child not in graph:
                graph.add_node(child, word_length=len(child), label=reduced_word_label(child))
                queue.append(child)
            graph.add_edge(word, child, generator=letter.lower())
    return graph


def reduced_word_label(word: tuple[str, ...]) -> str:
    """Return a compact label for a reduced word tuple."""

    return "e" if not word else "".join(word)


def radial_free_tree_layout(graph: nx.Graph) -> dict[tuple[str, ...], tuple[float, float]]:
    """Place a free-group ball by word length and lexicographic angular order."""

    levels: dict[int, list[tuple[str, ...]]] = {}
    for node in graph.nodes:
        levels.setdefault(len(node), []).append(node)
    positions: dict[tuple[str, ...], tuple[float, float]] = {(): (0.0, 0.0)}
    for level, nodes in sorted(levels.items()):
        if level == 0:
            continue
        ordered = sorted(nodes)
        count = len(ordered)
        for index, node in enumerate(ordered):
            angle = 2 * pi * index / count + (level % 2) * pi / count
            positions[node] = (level * cos(angle), level * sin(angle))
    return positions


def grid_layout(graph: nx.Graph) -> dict[object, tuple[float, float]]:
    """Use integer tuple nodes as planar coordinates."""

    return {node: (float(node[0]), float(node[1])) for node in graph.nodes if isinstance(node, tuple) and len(node) == 2}


def line_layout(graph: nx.Graph) -> dict[object, tuple[float, float]]:
    """Use integer nodes as line coordinates."""

    return {node: (float(node), 0.0) for node in graph.nodes if isinstance(node, int)}


def finite_dihedral_cayley(n: int = 8) -> nx.Graph:
    """Return the Cayley graph of the dihedral group D_n with generators r and s."""

    graph = nx.Graph()
    nodes = [(k, eps) for k in range(n) for eps in (0, 1)]
    graph.add_nodes_from(nodes)

    def mul(g: tuple[int, int], h: tuple[int, int]) -> tuple[int, int]:
        a, i = g
        b, j = h
        sign = -1 if i else 1
        return ((a + sign * b) % n, (i + j) % 2)

    for node in nodes:
        graph.add_edge(node, mul(node, (1, 0)), generator="r")
        graph.add_edge(node, mul(node, (0, 1)), generator="s")
    nx.set_node_attributes(graph, {node: f"r^{node[0]}{'s' if node[1] else ''}" for node in nodes}, "label")
    return graph


def shortest_path_ball_counts(graph: nx.Graph, root: object) -> dict[int, int]:
    """Count nodes by graph distance from root."""

    distances = nx.single_source_shortest_path_length(graph, root)
    counts: dict[int, int] = {}
    for distance in distances.values():
        counts[distance] = counts.get(distance, 0) + 1
    return dict(sorted(counts.items()))


def ball_volume_sequence(graph: nx.Graph, root: object) -> list[int]:
    """Return cumulative ball volumes around root."""

    counts = shortest_path_ball_counts(graph, root)
    total = 0
    volumes: list[int] = []
    for radius in range(max(counts) + 1):
        total += counts.get(radius, 0)
        volumes.append(total)
    return volumes


def four_point_hyperbolicity(graph: nx.Graph, *, max_nodes: int = 34) -> float:
    """Estimate graph hyperbolicity by the four-point condition."""

    nodes = list(graph.nodes)
    if len(nodes) > max_nodes:
        step = max(1, len(nodes) // max_nodes)
        nodes = nodes[::step][:max_nodes]
    lengths = dict(nx.all_pairs_shortest_path_length(graph.subgraph(nodes)))
    delta = 0.0
    for a, b, c, d in combinations(nodes, 4):
        if b not in lengths[a] or c not in lengths[a] or d not in lengths[a]:
            continue
        sums = sorted(
            (
                lengths[a][b] + lengths[c][d],
                lengths[a][c] + lengths[b][d],
                lengths[a][d] + lengths[b][c],
            )
        )
        delta = max(delta, (sums[-1] - sums[-2]) / 2)
    return float(delta)


def outside_component_count(graph: nx.Graph, root: object, radius: int) -> int:
    """Count components that remain after removing a closed ball."""

    distances = nx.single_source_shortest_path_length(graph, root, cutoff=radius)
    remaining = graph.copy()
    remaining.remove_nodes_from(distances.keys())
    return nx.number_connected_components(remaining)


def square_boundary_ratio(radius: int) -> float:
    """Boundary/volume ratio for a square Folner set in Z^2."""

    side = 2 * radius + 1
    volume = side * side
    boundary_edges = 4 * side
    return boundary_edges / volume


def free_tree_ball_boundary_ratio(radius: int, rank: int = 2) -> float:
    """Boundary/volume ratio for a free-group ball in the regular Cayley tree."""

    if radius == 0:
        return 2 * rank
    sphere = 2 * rank * (2 * rank - 1) ** radius
    volume = 1 + 2 * rank * ((2 * rank - 1) ** radius - 1) // (2 * rank - 2)
    boundary_edges = (2 * rank - 1) * sphere
    return boundary_edges / volume


def growth_profiles(max_radius: int = 7) -> dict[str, list[int]]:
    """Return exact small-radius growth profiles for model groups."""

    radii = list(range(max_radius + 1))
    z = [2 * r + 1 for r in radii]
    z2 = [(2 * r * r + 2 * r + 1) for r in radii]
    f2 = [1 if r == 0 else 1 + 4 * (3**r - 1) // 2 for r in radii]
    return {"radii": radii, "Z": z, "Z2": z2, "F2": f2}


def coarse_identity_distortion(radius: int = 4) -> dict[str, float]:
    """Compare two word metrics on Z^2: standard generators versus adding a diagonal."""

    ratios: list[float] = []
    additive_errors: list[float] = []
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            if x == 0 and y == 0:
                continue
            standard = abs(x) + abs(y)
            diagonal = max(abs(x), abs(y)) if x * y >= 0 else abs(x) + abs(y)
            ratios.append(standard / max(diagonal, 1))
            additive_errors.append(abs(standard - diagonal))
    return {
        "sample_radius": radius,
        "max_standard_over_diagonal": float(max(ratios)),
        "max_additive_error": float(max(additive_errors)),
        "coarse_lipschitz_constant": 2.0,
    }


def hyperbolic_disk_distance(p: Iterable[float], q: Iterable[float]) -> float:
    """Compute Poincare disk distance for points strictly inside the unit disk."""

    p_arr = np.asarray(tuple(p), dtype=float)
    q_arr = np.asarray(tuple(q), dtype=float)
    diff2 = float(np.sum((p_arr - q_arr) ** 2))
    norm_p2 = float(np.sum(p_arr**2))
    norm_q2 = float(np.sum(q_arr**2))
    argument = 1 + 2 * diff2 / ((1 - norm_p2) * (1 - norm_q2))
    return float(np.arccosh(argument))

