"""Small symbolic algebra helpers used by the UAG notebooks."""

from __future__ import annotations

from itertools import product
from typing import Iterable, Sequence

import sympy as sp


def _compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for head in range(total + 1):
        for tail in _compositions(total - head, parts - 1):
            yield (head, *tail)


def monomial_basis(variables: Sequence[sp.Symbol], degree: int) -> list[sp.Expr]:
    return [
        sp.prod(var ** exp for var, exp in zip(variables, exponents, strict=True))
        for exponents in _compositions(degree, len(variables))
    ]


def monomials_up_to_degree(variables: Sequence[sp.Symbol], degree: int) -> list[sp.Expr]:
    basis: list[sp.Expr] = []
    for d in range(degree + 1):
        basis.extend(monomial_basis(variables, d))
    return basis


def groebner_membership(poly: sp.Expr, generators: Sequence[sp.Expr], variables: Sequence[sp.Symbol]) -> dict[str, str]:
    basis = sp.groebner(list(generators), *variables)
    remainder = basis.reduce(poly)[1]
    return {"remainder": str(sp.factor(remainder)), "is_member": str(sp.simplify(remainder) == 0)}


def factor_components_2d(poly: sp.Expr) -> list[str]:
    coeff, factors = sp.factor_list(poly)
    components = []
    if coeff != 1:
        components.append(str(coeff))
    components.extend(str(base) for base, _multiplicity in factors)
    return components or [str(sp.factor(poly))]


def resultant_degree(f: sp.Expr, g: sp.Expr, variable: sp.Symbol) -> int:
    result = sp.resultant(f, g, variable)
    poly = sp.Poly(result)
    return int(poly.total_degree())


def matrix_rank(matrix: Sequence[Sequence[object]]) -> int:
    return int(sp.Matrix(matrix).rank())


def nullspace_dimension(matrix: Sequence[Sequence[object]]) -> int:
    mat = sp.Matrix(matrix)
    return int(mat.shape[1] - mat.rank())


def radical_toy_summary(poly: sp.Expr, power: int) -> dict[str, object]:
    return {
        "base": str(sp.factor(poly)),
        "powered": str(sp.factor(poly ** power)),
        "same_zero_set_over_samples": True,
        "changed_multiplicity": power > 1,
    }


def sample_grid_residual(poly: sp.Expr, variables: Sequence[sp.Symbol], samples: Sequence[Sequence[float]]) -> float:
    fn = sp.lambdify(tuple(variables), poly, "numpy")
    values = [abs(float(fn(*point))) for point in samples]
    return max(values) if values else 0.0


def finite_field_points(poly: sp.Expr, variables: Sequence[sp.Symbol], prime: int) -> list[tuple[int, ...]]:
    fn = sp.lambdify(tuple(variables), poly, "math")
    points = []
    for point in product(range(prime), repeat=len(variables)):
        if int(fn(*point)) % prime == 0:
            points.append(tuple(int(v) for v in point))
    return points
