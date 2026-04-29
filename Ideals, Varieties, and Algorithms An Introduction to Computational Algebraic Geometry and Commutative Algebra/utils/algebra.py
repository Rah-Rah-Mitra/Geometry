"""Small exact algebra helpers for IVA notebooks."""

from __future__ import annotations

from typing import Any

import sympy as sp


def division_trace(seed: int) -> dict[str, Any]:
    x = sp.symbols("x")
    divisor = x - 1
    polynomial = x**3 + (seed % 5 - 2) * x**2 + (seed + 1) * x + seed
    quotient, remainder = sp.div(polynomial, divisor, domain=sp.QQ)
    identity_ok = sp.expand(quotient * divisor + remainder - polynomial) == 0
    return {
        "polynomial": str(polynomial),
        "divisor": str(divisor),
        "quotient": str(quotient),
        "remainder": str(remainder),
        "identity_ok": bool(identity_ok),
    }


def chapter_symbolic_checks(seed: int) -> dict[str, Any]:
    x, y, z, t = sp.symbols("x y z t")
    groebner = sp.groebner([x - y, y - z], x, y, z, order="lex")
    normal_form = groebner.reduce(x - z)[1]
    resultant = sp.resultant(t**2 - (seed % 5 + 1), t - x, t)
    jacobian = sp.Matrix([x**2 + y**2 - 1, x - y]).jacobian([x, y])
    rank_at_sample = jacobian.subs({x: sp.sqrt(sp.Rational(1, 2)), y: sp.sqrt(sp.Rational(1, 2))}).rank()
    div = division_trace(seed)
    homogeneous = x**2 + x * y + y**2
    lam = sp.symbols("lambda")
    scaling_ok = sp.expand(homogeneous.subs({x: lam * x, y: lam * y}) - lam**2 * homogeneous) == 0
    return {
        "groebner_normal_form_zero": bool(normal_form == 0),
        "resultant": str(sp.factor(resultant)),
        "jacobian_rank_sample": int(rank_at_sample),
        "division_identity_ok": div["identity_ok"],
        "homogeneous_scaling_ok": bool(scaling_ok),
        "exact_zero": bool(normal_form == 0 and div["identity_ok"] and scaling_ok),
    }


def finite_field_table() -> list[dict[str, int]]:
    rows = []
    for value in [0, 1]:
        rows.append({"a": value, "a_squared_minus_a_mod_2": (value * value - value) % 2})
    return rows
