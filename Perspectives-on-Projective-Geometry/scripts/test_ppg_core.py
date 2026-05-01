from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.cayley_klein import klein_to_poincare, poincare_distance
from utils.conics import affine_point_on_conic, ellipse_conic, polar_line
from utils.projective import cross_ratio, hpoint, incidence, join, meet


def test_join_meet_incidence() -> None:
    p = hpoint(0.0, 0.0)
    q = hpoint(1.0, 1.0)
    r = hpoint(0.0, 1.0)
    s = hpoint(1.0, 0.0)
    line_a = join(p, q)
    line_b = join(r, s)
    x = meet(line_a, line_b)
    assert incidence(p, line_a)
    assert incidence(q, line_a)
    assert incidence(x, line_a)
    assert incidence(x, line_b)


def test_cross_ratio_invariance() -> None:
    sample = [-1.4, -0.2, 0.75, 1.6]
    image = [(1.1 * x - 0.25) / (0.22 * x + 1.0) for x in sample]
    assert abs(cross_ratio(*sample) - cross_ratio(*image)) < 1e-12


def test_conic_tangent_incidence() -> None:
    conic = ellipse_conic()
    point = affine_point_on_conic(0.7)
    tangent = polar_line(conic, point)
    assert abs(point @ tangent) < 1e-12


def test_poincare_distance_positive() -> None:
    p = klein_to_poincare(np.array([0.2, 0.1]))
    q = klein_to_poincare(np.array([0.45, -0.1]))
    assert poincare_distance(p, q) > 0

