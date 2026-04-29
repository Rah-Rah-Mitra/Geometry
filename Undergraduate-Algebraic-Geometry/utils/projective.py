"""Projective geometry helpers for the UAG notebooks."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import sympy as sp


def homogenize_polynomial(poly: sp.Expr, variables: Sequence[sp.Symbol], homogenizing: sp.Symbol, degree: int | None = None) -> sp.Expr:
    poly_obj = sp.Poly(poly, *variables)
    target_degree = degree if degree is not None else poly_obj.total_degree()
    result = 0
    for powers, coeff in poly_obj.terms():
        term_degree = sum(powers)
        monomial = coeff * sp.prod(var ** exp for var, exp in zip(variables, powers, strict=True))
        result += monomial * homogenizing ** (target_degree - term_degree)
    return sp.expand(result)


def dehomogenize_polynomial(poly: sp.Expr, homogenizing: sp.Symbol, value: int | float = 1) -> sp.Expr:
    return sp.expand(poly.subs(homogenizing, value))


def projective_normalize(coords: Sequence[float], *, tol: float = 1e-12) -> tuple[float, ...]:
    arr = np.asarray(coords, dtype=float)
    for item in arr:
        if abs(float(item)) > tol:
            return tuple((arr / item).tolist())
    raise ValueError("zero vector has no projective point")


def affine_chart(coords: Sequence[float], index: int) -> tuple[float, ...]:
    arr = np.asarray(coords, dtype=float)
    scale = arr[index]
    if abs(scale) < 1e-12:
        raise ValueError("point is not in this affine chart")
    return tuple(np.delete(arr / scale, index).tolist())


def line_through_points(p: Sequence[float], q: Sequence[float]) -> tuple[float, float, float]:
    line = np.cross(np.asarray(p, dtype=float), np.asarray(q, dtype=float))
    return tuple(float(v) for v in line)


def point_on_line(line: Sequence[float], point: Sequence[float], *, tol: float = 1e-9) -> bool:
    return abs(float(np.dot(np.asarray(line, dtype=float), np.asarray(point, dtype=float)))) < tol


def rational_normal_curve(t: float, degree: int) -> list[float]:
    return [float(t ** k) for k in range(degree + 1)]


def segre_embed(u: Sequence[float], v: Sequence[float]) -> np.ndarray:
    return np.outer(np.asarray(u, dtype=float), np.asarray(v, dtype=float))


def veronese_embed(u: Sequence[float]) -> np.ndarray:
    arr = np.asarray(u, dtype=float)
    return np.outer(arr, arr)


def rank_one_minors(matrix: Sequence[Sequence[float]]) -> list[float]:
    mat = np.asarray(matrix, dtype=float)
    minors: list[float] = []
    for i in range(mat.shape[0] - 1):
        for j in range(mat.shape[1] - 1):
            minors.append(float(mat[i, j] * mat[i + 1, j + 1] - mat[i, j + 1] * mat[i + 1, j]))
    return minors
