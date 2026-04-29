"""Surface and line-configuration helpers for the UAG notebooks."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import sympy as sp


def line_param_from_points(p: Sequence[object], q: Sequence[object], parameter: sp.Symbol | None = None) -> list[sp.Expr]:
    t = parameter or sp.symbols("t")
    return [sp.expand((1 - t) * sp.sympify(a) + t * sp.sympify(b)) for a, b in zip(p, q, strict=True)]


def line_on_surface_check(poly: sp.Expr, variables: Sequence[sp.Symbol], line: Sequence[sp.Expr], parameter: sp.Symbol | None = None) -> bool:
    t = parameter or sp.symbols("t")
    substituted = sp.expand(poly.subs(dict(zip(variables, line, strict=True))))
    return sp.Poly(substituted, t).is_zero


def plucker_coordinates(p: Sequence[float], q: Sequence[float]) -> np.ndarray:
    p_arr = np.asarray(p, dtype=float)
    q_arr = np.asarray(q, dtype=float)
    coords = []
    for i in range(len(p_arr)):
        for j in range(i + 1, len(p_arr)):
            coords.append(p_arr[i] * q_arr[j] - p_arr[j] * q_arr[i])
    return np.asarray(coords, dtype=float)


def lines_incident(p1: Sequence[float], q1: Sequence[float], p2: Sequence[float], q2: Sequence[float], *, tol: float = 1e-8) -> bool:
    mat = np.vstack([p1, q1, p2, q2]).astype(float)
    return int(np.linalg.matrix_rank(mat, tol=tol)) < 4


def fermat_cubic_line_count() -> int:
    return 27
