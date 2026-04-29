"""Affine-variety helpers for domains, tangent spaces, and toy dictionaries."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np
import sympy as sp


def vi_correspondence_examples() -> list[dict[str, str]]:
    return [
        {"ideal": "(x)", "locus": "y-axis", "order": "larger ideal, smaller set"},
        {"ideal": "(xy)", "locus": "two coordinate axes", "order": "product gives union"},
        {"ideal": "(x, y)", "locus": "origin", "order": "maximal ideal, single point"},
    ]


def rational_domain_mask(denominator: Callable[[np.ndarray, np.ndarray], np.ndarray], xs: np.ndarray, ys: np.ndarray, *, tol: float = 1e-8) -> np.ndarray:
    xgrid, ygrid = np.meshgrid(xs, ys)
    return np.abs(denominator(xgrid, ygrid)) > tol


def standard_open_samples(h: Callable[[np.ndarray, np.ndarray], np.ndarray], xs: np.ndarray, ys: np.ndarray) -> dict[str, int]:
    mask = rational_domain_mask(h, xs, ys)
    return {"sample_count": int(mask.size), "open_sample_count": int(mask.sum())}


def jacobian_matrix_at(polys: Sequence[sp.Expr], variables: Sequence[sp.Symbol], point: dict[sp.Symbol, object]) -> sp.Matrix:
    return sp.Matrix([[sp.diff(poly, var).subs(point) for var in variables] for poly in polys])


def tangent_space_dimension(polys: Sequence[sp.Expr], variables: Sequence[sp.Symbol], point: dict[sp.Symbol, object]) -> int:
    jac = jacobian_matrix_at(polys, variables, point)
    return int(len(variables) - jac.rank())


def blowup_chart_transform(poly: sp.Expr, x: sp.Symbol, y: sp.Symbol, chart: str = "x") -> sp.Expr:
    u, v = sp.symbols("u v")
    if chart == "x":
        return sp.factor(poly.subs({x: u, y: u * v}))
    if chart == "y":
        return sp.factor(poly.subs({x: u * v, y: v}))
    raise ValueError("chart must be 'x' or 'y'")
