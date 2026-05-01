"""Core tests for Geometry I helper utilities."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.geometry import barycentric_coordinates, cross_ratio, invert_points, rotation_matrix  # noqa: E402


def test_barycentric_coordinates_reconstruct_point() -> None:
    vertices = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0]])
    point = np.array([0.5, 0.75])
    weights = barycentric_coordinates(vertices, point)
    assert np.isclose(weights.sum(), 1.0)
    assert np.allclose(weights @ vertices, point)


def test_cross_ratio_is_homography_invariant() -> None:
    values = [-1.5, -0.2, 0.7, 1.8]
    transformed = [(x + 0.3) / (0.08 * x + 1.0) for x in values]
    assert np.isclose(cross_ratio(*values), cross_ratio(*transformed))


def test_rotation_preserves_norm() -> None:
    vector = np.array([1.0, -0.25])
    rotated = rotation_matrix(0.93) @ vector
    assert np.isclose(np.linalg.norm(vector), np.linalg.norm(rotated))


def test_inversion_radius_product() -> None:
    points = np.array([[2.0, 0.0], [0.0, -4.0]])
    inverted = invert_points(points, radius=3.0)
    products = np.linalg.norm(points, axis=1) * np.linalg.norm(inverted, axis=1)
    assert np.allclose(products, 9.0)

