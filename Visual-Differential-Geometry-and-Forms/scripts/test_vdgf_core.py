"""Core smoke tests for the VDGF course utilities."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.dg import gaussian_curvature_2d, metric_tensor, plane_curve_curvature, sphere_embedding
from utils.forms import CoordinateSystem, basis_form, d, evaluate, hodge_star


def test_plane_curve_curvature_unit_circle() -> None:
    theta = np.linspace(0, 2 * np.pi, 64)
    velocity = np.column_stack([-np.sin(theta), np.cos(theta)])
    acceleration = np.column_stack([-np.cos(theta), -np.sin(theta)])
    kappa = plane_curve_curvature(velocity, acceleration)
    assert np.allclose(kappa, 1.0)


def test_sphere_gaussian_curvature() -> None:
    u, v = sp.symbols("u v", positive=True)
    param = sphere_embedding(u, v)
    metric = metric_tensor(param, [u, v])
    K = gaussian_curvature_2d(metric, [u, v])
    assert sp.simplify(K - 1) == 0


def test_forms_exterior_derivative_squared_zero() -> None:
    coords = CoordinateSystem("R3", "x y z")
    x, y, z = coords.symbols
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    omega = x * dy + y * dz + z * dx
    assert not bool(d(d(omega)))


def test_form_evaluate_and_hodge() -> None:
    coords = CoordinateSystem("R3", "x y z")
    dx, dy, dz = [basis_form(coords, i) for i in range(3)]
    area = dx.wedge(dy)
    assert evaluate(area, [1, 0, 0], [0, 1, 0]) == 1
    assert hodge_star(dx).components == {(1, 2): 1}
