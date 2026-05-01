"""Core smoke tests for Pressley utilities and inventory."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = BOOK_ROOT / "scripts"
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import pressley_inventory as inventory  # noqa: E402
from utils.curves import arc_length, curvature_2d, curvature_3d, torsion  # noqa: E402
from utils.models import poincare_disk_distance, upper_half_plane_distance  # noqa: E402
from utils.surfaces import catenoid_patch, euler_characteristic, first_fundamental_form  # noqa: E402


def test_inventory_shape() -> None:
    inventory.validate_inventory()
    assert len(inventory.ENTRIES) == 16


def test_circle_curvature_and_arc_length() -> None:
    t = np.linspace(0, 2 * np.pi, 400)
    points = np.column_stack([np.cos(t), np.sin(t)])
    length = arc_length(points, t)[-1]
    kappa = curvature_2d(points, t)
    assert abs(length - 2 * np.pi) < 1e-3
    assert np.nanmean(np.abs(kappa[5:-5] - 1.0)) < 1e-3


def test_helix_curvature_and_torsion_are_finite() -> None:
    t = np.linspace(0, 4 * np.pi, 400)
    a = 0.4
    points = np.column_stack([np.cos(t), np.sin(t), a * t])
    kappa = curvature_3d(points, t)
    tau = torsion(points, t)
    assert np.isfinite(kappa).all()
    assert np.isfinite(tau).all()
    assert abs(float(np.mean(kappa[10:-10])) - 1 / (1 + a * a)) < 1e-2


def test_surface_metric_and_topology_helpers() -> None:
    u = np.linspace(-0.8, 0.8, 20)
    v = np.linspace(0, 2 * np.pi, 30)
    X, Y, Z = catenoid_patch(u, v)
    E, F, G = first_fundamental_form(X, Y, Z, u, v)
    assert E.shape == F.shape == G.shape
    assert np.all(E > 0)
    assert euler_characteristic(4, 6, 4) == 2


def test_hyperbolic_distances() -> None:
    assert poincare_disk_distance(0 + 0j, 0.25 + 0j) > 0
    assert upper_half_plane_distance(1j, 2j) > 0
