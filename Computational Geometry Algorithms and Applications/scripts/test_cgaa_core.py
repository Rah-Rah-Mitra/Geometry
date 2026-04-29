"""Smoke tests for CGAA course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.geometry2d import (  # noqa: E402
    brute_force_intersections,
    clip_polygon_halfplane,
    convex_hull,
    orientation,
    point_in_convex_polygon,
    point_in_triangle,
    polygon_area,
)


def test_orientation_and_hull() -> None:
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0.5, 0.5]])
    hull = convex_hull(points)
    assert len(hull) == 4
    assert abs(abs(polygon_area(hull)) - 1.0) < 1e-9
    assert orientation(np.array([0, 0]), np.array([1, 0]), np.array([0, 1])) > 0
    assert all(point_in_convex_polygon(point, hull) for point in points)


def test_segments_and_halfplanes() -> None:
    hits = brute_force_intersections([((0, 0), (1, 1)), ((0, 1), (1, 0)), ((2, 0), (2, 1))])
    assert hits == [(0.5, 0.5)]
    square = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1]], dtype=float)
    clipped = clip_polygon_halfplane(square, (1, 0), 0.25)
    assert clipped[:, 0].max() <= 0.25 + 1e-9


def test_triangle_membership() -> None:
    tri = np.array([[0, 0], [2, 0], [0, 2]], dtype=float)
    assert point_in_triangle(np.array([0.25, 0.25]), tri)
    assert not point_in_triangle(np.array([2.0, 2.0]), tri)
