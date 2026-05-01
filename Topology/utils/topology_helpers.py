"""Small topology helpers used by the Topology course notebooks."""

from __future__ import annotations

from itertools import combinations, product
from typing import Hashable, Iterable


def powerset(items: Iterable[Hashable]) -> list[frozenset[Hashable]]:
    values = list(items)
    return [frozenset(combo) for r in range(len(values) + 1) for combo in combinations(values, r)]


def is_topology(space: set[Hashable], opens: Iterable[Iterable[Hashable]]) -> bool:
    open_sets = {frozenset(item) for item in opens}
    if frozenset() not in open_sets or frozenset(space) not in open_sets:
        return False
    for a in list(open_sets):
        for b in list(open_sets):
            if a & b not in open_sets:
                return False
            if a | b not in open_sets:
                return False
    return True


def topology_from_basis(space: set[Hashable], basis: Iterable[Iterable[Hashable]]) -> set[frozenset[Hashable]]:
    basis_sets = [frozenset(b) for b in basis]
    opens = {frozenset()}
    for mask in range(1, 1 << len(basis_sets)):
        union = frozenset().union(*(basis_sets[i] for i in range(len(basis_sets)) if mask & (1 << i)))
        opens.add(union)
    opens.add(frozenset(space))
    return opens


def continuous_preimage_check(
    domain_opens: Iterable[Iterable[Hashable]],
    codomain_opens: Iterable[Iterable[Hashable]],
    mapping: dict[Hashable, Hashable],
) -> bool:
    domain_open_sets = {frozenset(item) for item in domain_opens}
    for target_open in [frozenset(item) for item in codomain_opens]:
        preimage = frozenset(point for point, value in mapping.items() if value in target_open)
        if preimage not in domain_open_sets:
            return False
    return True


def quotient_classes(points: Iterable[Hashable], relation: Iterable[tuple[Hashable, Hashable]]) -> list[set[Hashable]]:
    parent = {p: p for p in points}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in relation:
        union(a, b)
    classes: dict[Hashable, set[Hashable]] = {}
    for point in points:
        classes.setdefault(find(point), set()).add(point)
    return list(classes.values())


def euler_characteristic(vertices: int, edges: int, faces: int) -> int:
    return vertices - edges + faces


def polygon_schema_edges(word: str) -> list[tuple[str, int]]:
    result: list[tuple[str, int]] = []
    for token in word.split():
        if token.endswith("-"):
            result.append((token[:-1], -1))
        else:
            result.append((token, 1))
    return result


def winding_number(samples: list[complex], point: complex = 0j) -> int:
    import math

    angles = [math.atan2((z - point).imag, (z - point).real) for z in samples]
    total = 0.0
    for a, b in zip(angles, angles[1:] + angles[:1]):
        delta = b - a
        while delta <= -math.pi:
            delta += 2 * math.pi
        while delta > math.pi:
            delta -= 2 * math.pi
        total += delta
    return round(total / (2 * math.pi))


def covering_grid(width: int = 5, height: int = 3) -> list[tuple[int, int]]:
    return list(product(range(-width, width + 1), range(-height, height + 1)))
