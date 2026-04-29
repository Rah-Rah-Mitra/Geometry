"""Small topology ledgers for the surface chapters."""

from __future__ import annotations


def euler_from_boundary_pieces(k: int, n: int) -> int:
    return 2 * k - n


def genus_from_gluing(k: int, n: int, m: int) -> float:
    return n / 2 - k + m


def total_gaussian_curvature_from_chi(chi: float) -> float:
    import math

    return 2 * math.pi * chi


def is_involution(mapping: dict[int, int]) -> bool:
    return all(mapping.get(mapping.get(key)) == key for key in mapping)
