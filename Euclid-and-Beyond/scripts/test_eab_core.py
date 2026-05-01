"""Smoke tests for Euclid and Beyond helpers and inventory."""

from __future__ import annotations

import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = BOOK_ROOT / "scripts"
for path in [BOOK_ROOT, SCRIPT_ROOT]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from eab_inventory import ENTRIES  # noqa: E402
from utils.euclidean import circle_circle_intersections, distance, regular_polygon  # noqa: E402
from utils.hyperbolic import disk_rotation, poincare_distance  # noqa: E402
from utils.polyhedra import euler_characteristic, named_meshes  # noqa: E402


def test_inventory_has_expected_units() -> None:
    assert len(ENTRIES) == 10
    assert ENTRIES[0]["artifact"] == "introduction"
    assert ENTRIES[-1]["artifact"] == "appendix-brief-euclid"


def test_equilateral_construction() -> None:
    a, b = (0.0, 0.0), (1.0, 0.0)
    c = circle_circle_intersections(a, 1.0, b, 1.0)[0]
    assert abs(distance(a, b) - distance(a, c)) < 1e-12
    assert abs(distance(a, b) - distance(b, c)) < 1e-12


def test_regular_polygon_sides_match() -> None:
    polygon = regular_polygon(17)
    sides = [distance(polygon[i], polygon[(i + 1) % 17]) for i in range(17)]
    assert max(sides) - min(sides) < 1e-12


def test_poincare_rotation_preserves_distance() -> None:
    a, b = (-0.4, 0.1), (0.45, 0.25)
    assert abs(poincare_distance(a, b) - poincare_distance(disk_rotation(a, 0.7), disk_rotation(b, 0.7))) < 1e-12


def test_polyhedra_euler_characteristic() -> None:
    for mesh in named_meshes().values():
        assert euler_characteristic(mesh) == 2
