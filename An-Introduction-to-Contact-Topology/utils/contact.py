"""Small mathematical helpers used by the contact topology notebooks."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import numpy as np
import sympy as sp


def contact_volume_coefficient_3d(
    p_component: sp.Expr,
    q_component: sp.Expr,
    r_component: sp.Expr,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Expr:
    """Return the dx^dy^dz coefficient of alpha wedge d alpha in R^3."""

    x, y, z = coordinates
    a_xy = sp.diff(q_component, x) - sp.diff(p_component, y)
    a_xz = sp.diff(r_component, x) - sp.diff(p_component, z)
    a_yz = sp.diff(r_component, y) - sp.diff(q_component, z)
    return sp.simplify(p_component * a_yz - q_component * a_xz + r_component * a_xy)


def legendrian_front_invariants(writhe: int, cusps_up: int, cusps_down: int) -> dict[str, float]:
    """Classical front formulas for a generic oriented Legendrian front."""

    total_cusps = cusps_up + cusps_down
    return {
        "writhe": writhe,
        "cusps_up": cusps_up,
        "cusps_down": cusps_down,
        "thurston_bennequin": writhe - total_cusps / 2,
        "rotation": (cusps_down - cusps_up) / 2,
    }


def sampled_rotation_number(points: np.ndarray) -> float:
    """Estimate the turning number of a closed immersed plane curve."""

    points = np.asarray(points, dtype=float)
    if len(points) < 4:
        raise ValueError("at least four sampled points are required")
    velocity = np.gradient(points, axis=0)
    angles = np.unwrap(np.arctan2(velocity[:, 1], velocity[:, 0]))
    return float((angles[-1] - angles[0]) / (2 * math.pi))


def nonzero_artifact_sizes(paths: Iterable[str | Path]) -> dict[str, int]:
    result: dict[str, int] = {}
    for path_like in paths:
        path = Path(path_like)
        if not path.exists():
            raise FileNotFoundError(path)
        size = path.stat().st_size
        if size <= 0:
            raise AssertionError(f"{path} is empty")
        result[path.as_posix()] = size
    return result

