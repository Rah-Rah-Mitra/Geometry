"""Small geometric algebra toolkit used by the notebook course."""

from .core import Algebra, Multivector, unit_rotor
from .models import (
    conformal_distance_squared,
    conformal_inner,
    conformal_point,
    homogeneous_line,
    homogeneous_point,
    intersect_homogeneous_lines,
    normalize_homogeneous_point,
    plucker_line,
    ray_sphere_intersection,
    rotation_matrix,
)

__all__ = [
    "Algebra",
    "Multivector",
    "unit_rotor",
    "conformal_distance_squared",
    "conformal_inner",
    "conformal_point",
    "homogeneous_line",
    "homogeneous_point",
    "intersect_homogeneous_lines",
    "normalize_homogeneous_point",
    "plucker_line",
    "ray_sphere_intersection",
    "rotation_matrix",
]
