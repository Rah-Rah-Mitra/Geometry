"""Smoke tests for Arnold course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.mechanics import explicit_euler_oscillator, polygon_area, standard_map, symplectic_matrix, verlet_oscillator


def test_symplectic_matrix_is_skew() -> None:
    matrix = symplectic_matrix(3)
    assert matrix.shape == (6, 6)
    assert np.allclose(matrix.T, -matrix)


def test_standard_map_preserves_small_cell_area() -> None:
    square = np.array([[1.0, 1.0], [1.03, 1.0], [1.03, 1.03], [1.0, 1.03]])
    mapped = []
    for q, p in square:
        p_new = p + 0.4 * np.sin(q)
        q_new = q + p_new
        mapped.append([q_new, p_new])
    mapped = np.array(mapped)
    assert abs(abs(polygon_area(square[:, 0], square[:, 1])) - abs(polygon_area(mapped[:, 0], mapped[:, 1]))) < 1e-12


def test_verlet_has_less_energy_drift_than_explicit_euler() -> None:
    qv, pv = verlet_oscillator(1.0, 0.0, 0.05, 400)
    qe, pe = explicit_euler_oscillator(1.0, 0.0, 0.05, 400)
    ev = 0.5 * (qv**2 + pv**2)
    ee = 0.5 * (qe**2 + pe**2)
    assert np.ptp(ev) < np.ptp(ee)
