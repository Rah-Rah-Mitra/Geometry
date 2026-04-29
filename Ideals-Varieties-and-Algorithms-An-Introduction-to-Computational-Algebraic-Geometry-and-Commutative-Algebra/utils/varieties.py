"""Small variety sampling helpers for IVA notebooks."""

from __future__ import annotations

import numpy as np
import sympy as sp


def residual_grid(expr: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol], *, limit: float = 2.0, samples: int = 101):
    x, y = variables
    xs = np.linspace(-limit, limit, samples)
    ys = np.linspace(-limit, limit, samples)
    xx, yy = np.meshgrid(xs, ys)
    fn = sp.lambdify((x, y), expr, "numpy")
    return xx, yy, np.asarray(fn(xx, yy), dtype=float)


def twisted_cubic_samples(samples: int = 80):
    t = np.linspace(-2.0, 2.0, samples)
    return t, t**2, t**3


def finite_fiber_samples(seed: int) -> dict[str, int]:
    x = sp.symbols("x")
    polynomial = x**2 - (seed % 4 + 1)
    roots = sp.solve(polynomial, x)
    return {"polynomial_degree": int(sp.degree(polynomial)), "fiber_count_over_complex": len(roots)}
