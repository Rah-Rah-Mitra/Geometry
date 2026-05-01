"""Small knot and presentation helpers."""

from __future__ import annotations

import sympy as sp


def trefoil_alexander_matrix() -> sp.Matrix:
    t = sp.symbols("t")
    return sp.Matrix([[1 - t, -1], [t, 1 - t]])


def trefoil_alexander_polynomial() -> sp.Expr:
    t = sp.symbols("t")
    return sp.expand(trefoil_alexander_matrix().det())


def presentation_to_text(generators: list[str], relators: list[str]) -> str:
    return "<" + ", ".join(generators) + " | " + ", ".join(relators) + ">"
