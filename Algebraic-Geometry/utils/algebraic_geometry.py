"""Small exact helpers used by several Algebraic Geometry notebooks."""

from __future__ import annotations

from itertools import product
from typing import Iterable

import sympy as sp


def homogeneous_scale_check(poly: sp.Expr, variables: Iterable[sp.Symbol], scale: sp.Symbol) -> sp.Expr:
    """Return the difference f(lambda*x)-lambda^d*f(x) for a homogeneous polynomial."""
    vars_tuple = tuple(variables)
    degree = sp.Poly(poly, *vars_tuple).total_degree()
    scaled = poly.subs({var: scale * var for var in vars_tuple})
    return sp.expand(scaled - scale**degree * poly)


def projective_points_fq(q: int, n: int) -> list[tuple[int, ...]]:
    """Enumerate P^n(F_q) using the first nonzero coordinate normalized to 1."""
    points: list[tuple[int, ...]] = []
    for coords in product(range(q), repeat=n + 1):
        if all(value == 0 for value in coords):
            continue
        first = next(idx for idx, value in enumerate(coords) if value != 0)
        inv = pow(coords[first], -1, q)
        normalized = tuple((value * inv) % q for value in coords)
        if normalized not in points:
            points.append(normalized)
    return points


def count_projective_hypersurface_fq(poly: sp.Expr, variables: Iterable[sp.Symbol], q: int) -> int:
    vars_tuple = tuple(variables)
    count = 0
    for point in projective_points_fq(q, len(vars_tuple) - 1):
        value = int(poly.subs(dict(zip(vars_tuple, point, strict=True)))) % q
        if value == 0:
            count += 1
    return count


def cech_delta_zero_check(values: tuple[sp.Expr, sp.Expr, sp.Expr]) -> sp.Expr:
    """For a three-open cover toy model, check the alternating sum on triple overlap."""
    a01, a02, a12 = values
    return sp.simplify(a12 - a02 + a01)


def divisor_degree(coefficients: dict[str, int]) -> int:
    return sum(coefficients.values())

