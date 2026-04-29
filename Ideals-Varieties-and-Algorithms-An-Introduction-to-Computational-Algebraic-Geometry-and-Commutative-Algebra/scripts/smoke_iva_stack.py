"""Smoke-check the local algebraic-geometry stack used by IVA."""

from __future__ import annotations

import importlib.util

import sympy as sp

REQUIRED = ["numpy", "matplotlib", "plotly", "networkx", "pandas", "PIL", "nbformat", "nbclient", "sympy"]


def main() -> None:
    missing = [name for name in REQUIRED if importlib.util.find_spec(name) is None]
    if missing:
        raise SystemExit(f"missing required packages: {missing}")
    x, y = sp.symbols("x y")
    basis = sp.groebner([x - y, y**2 - 1], x, y, order="lex")
    assert basis.reduce(x**2 - 1)[1] == 0
    print("IVA stack smoke check passed.")


if __name__ == "__main__":
    main()
