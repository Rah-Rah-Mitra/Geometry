"""Curve helpers for conics, cubics, and chord-tangent checks."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import sympy as sp


def conic_matrix(coeffs: Sequence[float]) -> np.ndarray:
    a, b, c, d, e, f = [float(v) for v in coeffs]
    return np.array(
        [[a, b / 2.0, d / 2.0], [b / 2.0, c, e / 2.0], [d / 2.0, e / 2.0, f]],
        dtype=float,
    )


def classify_conic_matrix(matrix: Sequence[Sequence[float]], *, tol: float = 1e-9) -> dict[str, object]:
    mat = np.asarray(matrix, dtype=float)
    eigvals = np.linalg.eigvalsh(mat[:2, :2])
    determinant = float(np.linalg.det(mat))
    rank = int(np.linalg.matrix_rank(mat, tol=tol))
    if rank < 3 or abs(determinant) < tol:
        kind = "degenerate"
    elif eigvals[0] * eigvals[1] > 0:
        kind = "ellipse-type"
    elif eigvals[0] * eigvals[1] < 0:
        kind = "hyperbola-type"
    else:
        kind = "parabola-type"
    return {"rank": rank, "determinant": determinant, "kind": kind}


def solve_conic_through_points(points: Sequence[Sequence[float]]) -> np.ndarray:
    rows = []
    for x, y in points:
        rows.append([x * x, x * y, y * y, x, y, 1.0])
    _u, _s, vh = np.linalg.svd(np.asarray(rows, dtype=float))
    return vh[-1, :]


def cubic_singular_points(poly: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> list[dict[sp.Symbol, sp.Expr]]:
    equations = [poly, sp.diff(poly, x), sp.diff(poly, y)]
    return list(sp.solve(equations, (x, y), dict=True))


def hessian_curve(poly: sp.Expr, variables: Sequence[sp.Symbol]) -> sp.Expr:
    return sp.factor(sp.Matrix([[sp.diff(poly, a, b) for a in variables] for b in variables]).det())


def elliptic_add(p: tuple[object, object] | None, q: tuple[object, object] | None, a: object, b: object) -> tuple[sp.Expr, sp.Expr] | None:
    if p is None:
        return q
    if q is None:
        return p
    x1, y1 = map(sp.sympify, p)
    x2, y2 = map(sp.sympify, q)
    a = sp.sympify(a)
    if sp.simplify(x1 - x2) == 0 and sp.simplify(y1 + y2) == 0:
        return None
    if sp.simplify(x1 - x2) == 0 and sp.simplify(y1 - y2) == 0:
        slope = (3 * x1 ** 2 + a) / (2 * y1)
    else:
        slope = (y2 - y1) / (x2 - x1)
    x3 = sp.simplify(slope ** 2 - x1 - x2)
    y3 = sp.simplify(-(y1 + slope * (x3 - x1)))
    return (sp.factor(x3), sp.factor(y3))


def cubic_residual(point: tuple[object, object] | None, a: object, b: object) -> sp.Expr:
    if point is None:
        return sp.Integer(0)
    x, y = map(sp.sympify, point)
    return sp.factor(y ** 2 - x ** 3 - sp.sympify(a) * x - sp.sympify(b))
