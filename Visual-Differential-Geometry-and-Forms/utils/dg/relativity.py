"""Schwarzschild-coordinate helpers."""

from __future__ import annotations

from collections.abc import Sequence

import sympy as sp

from .riemannian import christoffel_symbols

DEFAULT_MASS = sp.Symbol("M", positive=True)


def schwarzschild_coordinates() -> tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol]:
    """Return standard Schwarzschild coordinates ``(t, r, theta, phi)``."""

    return sp.symbols("t r theta phi", real=True)


def schwarzschild_radius(
    mass: sp.Expr = DEFAULT_MASS,
    *,
    G: sp.Expr = 1,
    c: sp.Expr = 1,
) -> sp.Expr:
    """Return the Schwarzschild radius ``2 G M / c^2``."""

    return sp.simplify(2 * sp.sympify(G) * sp.sympify(mass) / sp.sympify(c) ** 2)


def schwarzschild_metric(
    coords: Sequence[sp.Symbol] | None = None,
    mass: sp.Expr = DEFAULT_MASS,
    *,
    G: sp.Expr = 1,
    c: sp.Expr = 1,
) -> sp.Matrix:
    """Return the Schwarzschild metric with signature ``(-, +, +, +)``."""

    if coords is None:
        coords = schwarzschild_coordinates()
    _, radius, theta, _ = tuple(coords)
    light_speed = sp.sympify(c)
    lapse = sp.simplify(1 - schwarzschild_radius(mass, G=G, c=c) / radius)
    return sp.diag(
        -lapse * light_speed**2,
        1 / lapse,
        radius**2,
        radius**2 * sp.sin(theta) ** 2,
    )


def schwarzschild_inverse_metric(
    coords: Sequence[sp.Symbol] | None = None,
    mass: sp.Expr = DEFAULT_MASS,
    *,
    G: sp.Expr = 1,
    c: sp.Expr = 1,
) -> sp.Matrix:
    """Return the inverse Schwarzschild metric."""

    return sp.simplify(schwarzschild_metric(coords, mass, G=G, c=c).inv())


def schwarzschild_christoffel_symbols(
    coords: Sequence[sp.Symbol] | None = None,
    mass: sp.Expr = DEFAULT_MASS,
    *,
    G: sp.Expr = 1,
    c: sp.Expr = 1,
) -> sp.ImmutableDenseNDimArray:
    """Return Levi-Civita connection symbols for the Schwarzschild metric."""

    if coords is None:
        coords = schwarzschild_coordinates()
    return christoffel_symbols(schwarzschild_metric(coords, mass, G=G, c=c), coords)
