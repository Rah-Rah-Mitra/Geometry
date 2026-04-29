"""Nonholonomic control helpers for Lie bracket and steering demos."""

from __future__ import annotations

import numpy as np
import sympy as sp


def lie_bracket_sympy(f: list[sp.Expr], g: list[sp.Expr], coords: list[sp.Symbol]) -> list[sp.Expr]:
    fvec = sp.Matrix(f)
    gvec = sp.Matrix(g)
    x = sp.Matrix(coords)
    return list(gvec.jacobian(x) * fvec - fvec.jacobian(x) * gvec)


def brockett_rhs(state: np.ndarray, control: np.ndarray) -> np.ndarray:
    x, y, _z = np.asarray(state, dtype=float)
    u1, u2 = np.asarray(control, dtype=float)
    return np.array([u1, u2, x * u2 - y * u1])


def integrate_brockett(controls: np.ndarray, dt: float = 0.01, x0: np.ndarray | None = None) -> np.ndarray:
    state = np.zeros(3) if x0 is None else np.asarray(x0, dtype=float).copy()
    hist = [state.copy()]
    for u in np.asarray(controls, dtype=float):
        state = state + dt * brockett_rhs(state, u)
        hist.append(state.copy())
    return np.asarray(hist)


def sinusoid_controls(steps: int = 800, amplitude: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    t = np.linspace(0, 2 * np.pi, steps, endpoint=False)
    controls = amplitude * np.column_stack([np.cos(t), np.sin(t)])
    return t, controls


def bracket_loop(eps: float = 0.1) -> np.ndarray:
    state = np.zeros(3)
    sequence = [np.array([1, 0]), np.array([0, 1]), np.array([-1, 0]), np.array([0, -1])]
    for u in sequence:
        state = state + eps * brockett_rhs(state, u)
    return state
