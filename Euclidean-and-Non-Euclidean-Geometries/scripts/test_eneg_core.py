"""Smoke tests for ENEG course helpers."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.geometry_helpers import Line, angle_between, circle_from_three_points, line_intersection, reflect_point_across_line  # noqa: E402
from utils.hyperbolic import angle_of_parallelism, klein_to_poincare, poincare_distance, poincare_to_klein  # noqa: E402
from utils.validation import SOURCE_MAP  # noqa: E402
from utils.chapter_visuals import chapter_sanity  # noqa: E402


def test_source_map_covers_course_units() -> None:
    assert len(SOURCE_MAP) == 13
    assert SOURCE_MAP[0]["folder"] == "chapter-00-introduction"
    assert SOURCE_MAP[-1]["number"] == "B"


def test_euclidean_helpers() -> None:
    line_a = Line.through((0, 0), (1, 0))
    line_b = Line.through((0, 0), (0, 1))
    intersection = line_intersection(line_a, line_b)
    assert intersection is not None
    assert np.allclose(intersection, [0, 0])
    assert math.isclose(angle_between((1, 0), (0, 1)), math.pi / 2)
    reflected = reflect_point_across_line((1, 2), line_a)
    assert np.allclose(reflected, [1, -2])
    center, radius = circle_from_three_points((1, 0), (0, 1), (-1, 0))
    assert np.allclose(center, [0, 0])
    assert math.isclose(radius, 1)


def test_hyperbolic_helpers() -> None:
    p = np.array([0.2, 0.1])
    assert np.allclose(klein_to_poincare(poincare_to_klein(p)), p)
    assert math.isclose(poincare_distance((0, 0), (0, 0)), 0)
    assert 0 < angle_of_parallelism(1.0) < math.pi / 2


def test_chapter_sanity_is_specific() -> None:
    fano = chapter_sanity("fano-plane")
    transformations = chapter_sanity("transformations")
    assert fano["incidences"] == 21
    assert transformations["reflection_reverses_orientation"] is True
    assert set(fano) != set(transformations)
