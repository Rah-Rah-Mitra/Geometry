"""Identity checks for the local geometric algebra core."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = REPO_ROOT / "Geometric-Algebra-for-Computer-Science"
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.ga import (  # noqa: E402
    Algebra,
    conformal_distance_squared,
    conformal_inner,
    conformal_point,
    homogeneous_line,
    homogeneous_point,
    intersect_homogeneous_lines,
    normalize_homogeneous_point,
    plucker_line,
    ray_sphere_intersection,
    unit_rotor,
)


def test_outer_product_antisymmetry() -> None:
    algebra = Algebra([1, 1, 1])
    e1, e2, _ = algebra.basis()
    assert e1.wedge(e1).almost_equal(algebra.scalar(0))
    assert e1.wedge(e2).almost_equal(-e2.wedge(e1))


def test_geometric_product_associativity() -> None:
    algebra = Algebra([1, 1, 1])
    e1, e2, e3 = algebra.basis()
    a = e1 + 2 * e2
    b = -e1 + 0.25 * e3
    c = e2 - e3
    assert a.gp(b).gp(c).almost_equal(a.gp(b.gp(c)))


def test_dual_and_meet() -> None:
    algebra = Algebra([1, 1, 1])
    e1, e2, e3 = algebra.basis()
    line_x = e1
    plane_xy = e1.wedge(e2)
    assert plane_xy.dual().grades() == {1}
    meet = plane_xy.meet(e1.wedge(e3))
    assert meet.grade(1).norm() > 0
    assert line_x.left_contract(plane_xy).grades() <= {1}


def test_rotor_preserves_norm() -> None:
    algebra = Algebra([1, 1, 1])
    e1, e2, e3 = algebra.basis()
    vector = 2 * e1 - e2 + 0.5 * e3
    rotor = unit_rotor(e1.wedge(e2), np.pi / 4)
    rotated = vector.sandwich(rotor).grade(1)
    assert abs(vector.norm2() - rotated.norm2()) < 1e-9


def test_homogeneous_intersection() -> None:
    p = homogeneous_point(0, 0)
    q = homogeneous_point(1, 1)
    r = homogeneous_point(0, 1)
    s = homogeneous_point(1, 0)
    line_a = homogeneous_line(p, q)
    line_b = homogeneous_line(r, s)
    x = normalize_homogeneous_point(intersect_homogeneous_lines(line_a, line_b))
    assert np.allclose(x, np.array([0.5, 0.5, 1.0]))
    assert abs(line_a @ x) < 1e-9
    assert abs(line_b @ x) < 1e-9


def test_conformal_distance_identity() -> None:
    a = np.array([1.0, 2.0, -1.0])
    b = np.array([-2.0, 0.5, 3.0])
    A = conformal_point(a)
    B = conformal_point(b)
    assert abs(conformal_inner(A, A)) < 1e-9
    assert abs(conformal_distance_squared(a, b) - np.sum((a - b) ** 2)) < 1e-9


def test_plucker_and_ray_helpers() -> None:
    direction, moment = plucker_line(np.array([1.0, 0.0, 0.0]), np.array([1.0, 1.0, 0.0]))
    assert abs(np.dot(direction, moment)) < 1e-9
    hit = ray_sphere_intersection(np.array([0, 0, -5]), np.array([0, 0, 1]), np.zeros(3), 1.0)
    assert hit is not None
    assert abs(hit - 4.0) < 1e-9


def main() -> None:
    for test in [
        test_outer_product_antisymmetry,
        test_geometric_product_associativity,
        test_dual_and_meet,
        test_rotor_preserves_norm,
        test_homogeneous_intersection,
        test_conformal_distance_identity,
        test_plucker_and_ray_helpers,
    ]:
        test()
    print("GA core checks passed")


if __name__ == "__main__":
    main()
