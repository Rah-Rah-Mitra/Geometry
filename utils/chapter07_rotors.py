"""Chapter 7 helpers for rotors, reflections, and versors.

The notebook uses these functions as a thin convenience layer over the small
dictionary-backed geometric algebra in ``utils.ga``. They intentionally favor
transparent formulas over broad coverage.
"""

from __future__ import annotations

from math import atan2, cos, sin
from typing import Iterable

import numpy as np

from utils.ga import Algebra, Multivector

EPS = 1e-10

E2 = Algebra([1, 1], names=["e1", "e2"])
E3 = Algebra([1, 1, 1], names=["e1", "e2", "e3"])
E4 = Algebra([1, 1, 1, 1], names=["e1", "e2", "e3", "e4"])


def coords_to_vector(coordinates: Iterable[float], algebra: Algebra = E3) -> Multivector:
    """Create a grade-1 multivector from coordinates."""
    return algebra.vector(coordinates)


def vector_to_coords(vector: Multivector) -> np.ndarray:
    """Return coordinates of a pure vector."""
    return vector.grade(1).coordinates()


def pure_grade(multivector: Multivector) -> int:
    """Return the single occupied grade, treating zero as grade 0."""
    grades = multivector.grades()
    if not grades:
        return 0
    if len(grades) != 1:
        raise ValueError(f"expected one grade, got {sorted(grades)}")
    return next(iter(grades))


def unit_vector(coordinates: Iterable[float], algebra: Algebra = E3) -> Multivector:
    """Create a unit vector from coordinates."""
    vector = coords_to_vector(coordinates, algebra)
    norm = vector.norm()
    if norm < EPS:
        raise ValueError("cannot normalize a zero vector")
    return vector / norm


def inverse_versor(versor: Multivector) -> Multivector:
    """Return the inverse of a vector-product versor."""
    reverse = versor.reverse()
    denominator = versor.gp(reverse).scalar_value()
    if abs(denominator) < EPS:
        raise ZeroDivisionError(f"versor has no stable inverse: {versor!r}")
    return reverse / denominator


def normalize_versor(versor: Multivector) -> Multivector:
    """Scale a versor so that V reverse(V) is +1 or -1 in magnitude."""
    denominator = abs(versor.gp(versor.reverse()).scalar_value())
    if denominator < EPS:
        raise ZeroDivisionError(f"versor has no stable norm: {versor!r}")
    return versor / np.sqrt(denominator)


def rotor_from_plane_angle(plane_bivector: Multivector, angle: float) -> Multivector:
    """Return the Euclidean rotor ``cos(angle/2) - B sin(angle/2)``."""
    if pure_grade(plane_bivector) != 2:
        raise ValueError("rotor plane must be a bivector")
    scale = plane_bivector.norm()
    if scale < EPS:
        raise ValueError("rotor plane must be nonzero")
    unit_plane = plane_bivector / scale
    return plane_bivector.algebra.scalar(cos(angle / 2.0)) - unit_plane * sin(angle / 2.0)


def rotor_exp(generator_bivector: Multivector) -> Multivector:
    """Return ``exp(-B/2)`` for a Euclidean bivector angle ``B``."""
    if not generator_bivector:
        return generator_bivector.algebra.scalar(1.0)
    return rotor_from_plane_angle(generator_bivector, generator_bivector.norm())


def rotor_log(rotor: Multivector) -> Multivector:
    """Return a principal Euclidean bivector angle ``B`` with ``R = exp(-B/2)``."""
    scalar = rotor.grade(0).scalar_value()
    bivector = rotor.grade(2)
    bivector_norm = bivector.norm()
    if bivector_norm < EPS:
        return rotor.algebra.scalar(0.0)
    half_angle = atan2(bivector_norm, scalar)
    return bivector * (-2.0 * half_angle / bivector_norm)


def rotor_power(rotor: Multivector, amount: float) -> Multivector:
    """Raise a unit Euclidean rotor to a real power along its principal branch."""
    return rotor_exp(rotor_log(rotor) * amount)


def rotor_from_two_vectors(source: Multivector, target: Multivector) -> Multivector:
    """Build a unit rotor that rotates one nonzero vector direction to another."""
    a = source / source.norm()
    b = target / target.norm()
    dot = a.scalar_product(b).scalar_value()
    if dot < -1.0 + EPS:
        basis = source.algebra.basis()
        helper = min(basis, key=lambda item: abs(item.scalar_product(a).scalar_value()))
        plane = a.wedge(helper)
        return rotor_from_plane_angle(plane, np.pi)
    return normalize_versor(b.gp(a) + 1.0)


def apply_rotor(element: Multivector, rotor: Multivector) -> Multivector:
    """Apply a unit rotor by the sandwich product."""
    return rotor.gp(element).gp(rotor.reverse())


def apply_even_versor(element: Multivector, versor: Multivector) -> Multivector:
    """Apply an even versor by ``V X V^{-1}``."""
    return versor.gp(element).gp(inverse_versor(versor))


def apply_odd_versor(element: Multivector, versor: Multivector) -> Multivector:
    """Apply an odd hyperplane-reflection versor by ``V grade_involution(X) V^{-1}``."""
    return versor.gp(element.grade_involution()).gp(inverse_versor(versor))


def reflect_in_line(element: Multivector, direction: Multivector) -> Multivector:
    """Reflect an element in a vector line through the origin."""
    return direction.gp(element).gp(inverse_versor(direction))


def reflect_in_hyperplane(element: Multivector, normal: Multivector) -> Multivector:
    """Reflect an element in the hyperplane with the supplied normal vector."""
    return apply_odd_versor(element, normal)


def reflect_vector_in_subspace(vector: Multivector, blade: Multivector) -> Multivector:
    """Reflect a vector in the direct subspace represented by an invertible blade."""
    sign = (-1) ** (pure_grade(blade) + 1)
    return (sign * blade.gp(vector).gp(blade.inverse_blade())).grade(1)


def rotor_to_matrix(rotor: Multivector) -> np.ndarray:
    """Return the matrix whose columns are the rotated Euclidean basis vectors."""
    basis = rotor.algebra.basis()
    return np.column_stack([vector_to_coords(apply_rotor(vector, rotor).grade(1)) for vector in basis])


def rotor_to_quaternion_wxyz(rotor: Multivector) -> np.ndarray:
    """Map a 3-D rotor to quaternion coordinates ``(w, x, y, z)``."""
    if rotor.algebra.dimension != 3:
        raise ValueError("quaternion coordinates are only used for 3-D rotors")
    terms = rotor.terms
    return np.array(
        [
            terms.get(0, 0.0),
            -terms.get(0b110, 0.0),
            terms.get(0b101, 0.0),
            -terms.get(0b011, 0.0),
        ]
    )


def quaternion_wxyz_to_rotor(quaternion: Iterable[float], algebra: Algebra = E3) -> Multivector:
    """Map quaternion coordinates ``(w, x, y, z)`` to the equivalent 3-D rotor."""
    if algebra.dimension != 3:
        raise ValueError("quaternion coordinates are only used for 3-D rotors")
    w, x, y, z = (float(value) for value in quaternion)
    e1, e2, e3 = algebra.basis()
    e12 = e1.wedge(e2)
    e13 = e1.wedge(e3)
    e23 = e2.wedge(e3)
    return algebra.scalar(w) - x * e23 + y * e13 - z * e12


def quaternion_product(left: Iterable[float], right: Iterable[float]) -> np.ndarray:
    """Return the Hamilton product for ``(w, x, y, z)`` coordinates."""
    w1, x1, y1, z1 = (float(value) for value in left)
    w2, x2, y2, z2 = (float(value) for value in right)
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ]
    )


def real_vector_julia(
    width: int = 360,
    height: int = 260,
    *,
    c: tuple[float, float] = (-0.72, 0.19),
    extent: float = 1.65,
    max_iter: int = 48,
    escape_radius: float = 12.0,
) -> np.ndarray:
    """Compute a 2-D Julia escape image using the real-vector update x e x + c."""
    xs = np.linspace(-extent, extent, width)
    ys = np.linspace(-extent * height / width, extent * height / width, height)
    x, y = np.meshgrid(xs, ys)
    counts = np.zeros_like(x, dtype=float)
    alive = np.ones_like(x, dtype=bool)
    cx, cy = c
    for step in range(max_iter):
        with np.errstate(over="ignore", invalid="ignore"):
            x_next = x * x - y * y + cx
            y_next = 2.0 * x * y + cy
        x, y = x_next, y_next
        with np.errstate(over="ignore", invalid="ignore"):
            radius2 = x * x + y * y
        escaped = alive & (radius2 > escape_radius * escape_radius)
        counts[escaped] = step + 1
        alive &= ~escaped
        x = np.where(alive, x, 0.0)
        y = np.where(alive, y, 0.0)
    counts[alive] = max_iter
    return counts
