"""Tests for small symplectic course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import COURSE_UNITS, PRINTED_TO_PDF_OFFSET
from utils.symplectic_core import harmonic_flow, oscillator_energy, polygon_signed_area, smooth_step, standard_j, symplectic_residual


def test_source_map_offset() -> None:
    assert PRINTED_TO_PDF_OFFSET == 13
    assert len(COURSE_UNITS) == 16
    assert COURSE_UNITS[1].pdf_start == COURSE_UNITS[1].printed_start + 13


def test_standard_j_is_complex_structure() -> None:
    j = standard_j(2)
    assert np.allclose(j @ j, -np.eye(4))
    assert np.allclose(j.T @ j, np.eye(4))


def test_harmonic_flow_preserves_energy_and_area() -> None:
    times = np.linspace(0, 2 * np.pi, 40)
    orbit = harmonic_flow(times, (1.2, 0.3))
    energy = oscillator_energy(orbit)
    assert float(np.max(np.abs(energy - energy[0]))) < 1e-12
    rotation = np.array([[0.0, 1.0], [-1.0, 0.0]])
    assert symplectic_residual(rotation) < 1e-12
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    assert polygon_signed_area(square) == 1.0


def test_smooth_step_bounds() -> None:
    xs = np.array([-1.0, 0.0, 0.5, 1.0, 2.0])
    values = smooth_step(xs)
    assert values[0] == 0.0
    assert values[1] == 0.0
    assert 0.0 < values[2] < 1.0
    assert values[3] == 1.0
    assert values[4] == 1.0
