"""Compact differential-geometry helpers for the VDGF notebook course."""

from __future__ import annotations

from .curves import OsculatingCircle, osculating_circle, plane_curve_curvature
from .models import (
    cartesian_to_spherical,
    hyperbolic_distance,
    hyperboloid_inner,
    hyperboloid_to_poincare_disk,
    poincare_disk_distance,
    poincare_disk_metric,
    poincare_disk_to_hyperboloid,
    sphere_embedding,
    sphere_metric,
    spherical_distance,
    spherical_to_cartesian,
    upper_half_plane_metric,
)
from .relativity import (
    schwarzschild_christoffel_symbols,
    schwarzschild_coordinates,
    schwarzschild_inverse_metric,
    schwarzschild_metric,
    schwarzschild_radius,
)
from .riemannian import (
    christoffel_symbols,
    gaussian_curvature_2d,
    geodesic_rhs,
    metric_tensor,
    parallel_transport_rhs,
    ricci_tensor,
    riemann_tensor,
    shape_operator,
)

__all__ = [
    "OsculatingCircle",
    "cartesian_to_spherical",
    "christoffel_symbols",
    "gaussian_curvature_2d",
    "geodesic_rhs",
    "hyperbolic_distance",
    "hyperboloid_inner",
    "hyperboloid_to_poincare_disk",
    "metric_tensor",
    "osculating_circle",
    "parallel_transport_rhs",
    "plane_curve_curvature",
    "poincare_disk_distance",
    "poincare_disk_metric",
    "poincare_disk_to_hyperboloid",
    "ricci_tensor",
    "riemann_tensor",
    "schwarzschild_christoffel_symbols",
    "schwarzschild_coordinates",
    "schwarzschild_inverse_metric",
    "schwarzschild_metric",
    "schwarzschild_radius",
    "shape_operator",
    "sphere_embedding",
    "sphere_metric",
    "spherical_distance",
    "spherical_to_cartesian",
    "upper_half_plane_metric",
]
