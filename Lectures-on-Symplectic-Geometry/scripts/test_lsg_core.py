"""Core smoke tests for the LSG course utilities and inventory."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_DIR.parent
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from lsg_inventory import ENTRIES, PARTS
from utils.symplectic import (
    delzant_vertex_determinants,
    hamiltonian_vector_field,
    rotation_symplectic,
    standard_omega,
    symplectic_residual,
)


def test_inventory_shape() -> None:
    assert len(PARTS) == 11
    assert len(ENTRIES) == 30
    assert ENTRIES[0]["pdf_span"] == "15-20"
    assert ENTRIES[-1]["pdf_span"] == "203-210"


def test_standard_omega_is_skew_and_nonzero() -> None:
    omega = standard_omega(2)
    assert omega.shape == (4, 4)
    assert np.allclose(omega + omega.T, 0)
    assert np.linalg.det(omega) != 0


def test_rotation_is_symplectic() -> None:
    assert symplectic_residual(rotation_symplectic(0.4)) < 1e-12


def test_hamiltonian_vector_field_preserves_quadratic_energy() -> None:
    grad = np.array([0.4, -0.2])
    field = hamiltonian_vector_field(grad)
    assert abs(float(grad @ field)) < 1e-12


def test_delzant_triangle() -> None:
    determinants = delzant_vertex_determinants([(1, 0), (0, 1), (-1, -1)])
    assert all(abs(det) == 1 for det in determinants)
