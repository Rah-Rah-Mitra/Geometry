"""Chapter 6 helpers for the geometric product notebook.

The functions here keep the notebook code focused on experiments rather than
bookkeeping. They build on the small dictionary-backed algebra in ``utils.ga``.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np

from utils.ga import Algebra, Multivector

EPS = 1e-10
E3 = Algebra([1, 1, 1], names=["e1", "e2", "e3"])


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
        raise ValueError(f"expected a pure-grade multivector, got grades {sorted(grades)}")
    return next(iter(grades))


def vector_inverse(vector: Multivector) -> Multivector:
    """Return the geometric-product inverse of a non-null vector."""
    denominator = vector.gp(vector).scalar_value()
    if abs(denominator) < EPS:
        raise ZeroDivisionError(f"vector is not invertible: {vector!r}")
    return vector / denominator


def right_ratio(source: Multivector, target: Multivector) -> Multivector:
    """Return the right-acting vector ratio ``source^{-1} target``."""
    return vector_inverse(source).gp(target)


def apply_right_ratio(vector: Multivector, source: Multivector, target: Multivector) -> Multivector:
    """Apply the right ratio that maps ``source`` to ``target``."""
    return vector.gp(right_ratio(source, target)).grade(1)


def vector_product_parts(left: Multivector, right: Multivector) -> dict[str, Multivector]:
    """Split a vector geometric product into symmetric and antisymmetric pieces."""
    left_right = left.gp(right)
    right_left = right.gp(left)
    return {
        "geometric": left_right,
        "symmetric": 0.5 * (left_right + right_left),
        "antisymmetric": 0.5 * (left_right - right_left),
        "inner": left_right.grade(0),
        "outer": left_right.grade(2),
    }


def basis_product_table(algebra: Algebra = E3) -> list[dict[str, str]]:
    """Return products of basis vectors as display-ready dictionaries."""
    basis = algebra.basis()
    rows: list[dict[str, str]] = []
    for i, left in enumerate(basis):
        for j, right in enumerate(basis):
            rows.append(
                {
                    "left": algebra.names[i],
                    "right": algebra.names[j],
                    "product": repr(left.gp(right)),
                }
            )
    return rows


def project_onto_blade(vector: Multivector, blade: Multivector) -> Multivector:
    """Project a vector into the subspace represented by an invertible blade."""
    return vector.left_contract(blade).gp(blade.inverse_blade()).grade(1)


def reject_from_blade(vector: Multivector, blade: Multivector) -> Multivector:
    """Return the part of a vector perpendicular to an invertible blade."""
    return vector.wedge(blade).gp(blade.inverse_blade()).grade(1)


def reflect_in_blade(vector: Multivector, blade: Multivector) -> Multivector:
    """Reflect a vector in the subspace represented by an invertible blade."""
    sign = (-1) ** (pure_grade(blade) + 1)
    return (sign * blade.gp(vector).gp(blade.inverse_blade())).grade(1)


def gram_schmidt_ga(vectors: Iterable[Multivector]) -> list[Multivector]:
    """Orthogonalize vectors using blade rejection and geometric division."""
    vectors = list(vectors)
    if not vectors:
        return []

    algebra = vectors[0].algebra
    blade = algebra.scalar(1)
    frame: list[Multivector] = []
    for vector in vectors:
        if vector.algebra != algebra:
            raise TypeError("all vectors must belong to the same algebra")
        candidate_blade = vector.wedge(blade)
        magnitude2 = abs(candidate_blade.gp(candidate_blade.reverse()).scalar_value())
        if magnitude2 < EPS:
            raise ValueError("dependent vectors do not produce an invertible new blade")
        new_vector = candidate_blade.gp(blade.inverse_blade()).grade(1)
        frame.append(new_vector)
        blade = candidate_blade
    return frame


def pairwise_inner_matrix(vectors: Iterable[Multivector]) -> np.ndarray:
    """Return the scalar-product matrix for a vector list."""
    vectors = list(vectors)
    matrix = np.zeros((len(vectors), len(vectors)))
    for i, left in enumerate(vectors):
        for j, right in enumerate(vectors):
            matrix[i, j] = left.scalar_product(right).scalar_value()
    return matrix

