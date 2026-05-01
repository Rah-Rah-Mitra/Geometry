"""Smoke tests for the do Carmo course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.dg_curves import curvature_3d, torsion_3d  # noqa: E402
from utils.dg_surfaces import first_fundamental_form, metric_ellipse  # noqa: E402


def test_helix_curvature_and_torsion_are_stable() -> None:
    t = np.linspace(0, 8 * np.pi, 900)
    a, b = 1.0, 0.25
    samples = np.column_stack([a * np.cos(t), a * np.sin(t), b * t])
    curvature = curvature_3d(samples, t)
    torsion = torsion_3d(samples, t)
    assert np.max(np.abs(curvature[30:-30] - a / (a * a + b * b))) < 5e-3
    assert np.max(np.abs(torsion[40:-40] + b / (a * a + b * b))) < 2e-2


def test_metric_ellipse_satisfies_quadratic_form() -> None:
    metric = np.array([[3.0, 0.4], [0.4, 1.5]])
    ellipse = metric_ellipse(metric)
    values = np.einsum("ij,jk,ik->i", ellipse, metric, ellipse)
    assert np.max(np.abs(values - 1.0)) < 1e-10


def test_first_fundamental_form_positive_for_graph_patch() -> None:
    u = np.linspace(-1, 1, 20)
    v = np.linspace(-1, 1, 20)
    uu, vv = np.meshgrid(u, v, indexing="ij")
    points = np.stack([uu, vv, 0.2 * uu * vv], axis=-1)
    xu = np.gradient(points, u, axis=0, edge_order=2)
    xv = np.gradient(points, v, axis=1, edge_order=2)
    e, f, g = first_fundamental_form(xu, xv)
    assert np.min(e * g - f * f) > 0
