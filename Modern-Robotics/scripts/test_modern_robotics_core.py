"""Smoke tests for Modern Robotics course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(BOOK_ROOT))
sys.path.insert(0, str(SCRIPT_ROOT))

from modern_robotics_inventory import CHAPTERS, PDF_FILENAME
from utils.kinematics import planar_arm_points, planar_jacobian
from utils.lie import so3_exp, so3_log
from utils.planning import dijkstra_grid


def test_inventory_shape() -> None:
    assert len(CHAPTERS) == 17
    assert PDF_FILENAME == "Mordern Robotics.pdf"
    assert CHAPTERS[0].pdf_start == 19


def test_so3_round_trip() -> None:
    w = np.array([0.2, -0.1, 0.3])
    np.testing.assert_allclose(so3_log(so3_exp(w)), w, atol=1e-10)


def test_planar_jacobian_rank() -> None:
    pts = planar_arm_points(np.array([1.0, 0.8]), np.array([0.4, -0.7]))
    J = planar_jacobian(np.array([1.0, 0.8]), np.array([0.4, -0.7]))
    assert pts.shape == (3, 2)
    assert np.linalg.matrix_rank(J) == 2


def test_grid_planner_finds_path() -> None:
    cost = np.ones((8, 8))
    cost[3, 1:7] = np.inf
    cost[3, 4] = 1.0
    path = dijkstra_grid(cost, (7, 0), (0, 7))
    assert path[0] == (7, 0)
    assert path[-1] == (0, 7)

