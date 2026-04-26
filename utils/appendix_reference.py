"""Reference helpers for the authored appendix notebooks.

The appendices are short, but they are convention-heavy. This module keeps the
notebooks focused on interpretation by centralizing grade selection, inner-product
variants, metric scans, and appendix artifact writing.
"""

from __future__ import annotations

import csv
import json
import math
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from utils.ga import Algebra, Multivector

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPENDIX_ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "appendices"

SOURCE_SPANS: tuple[dict[str, Any], ...] = (
    {
        "appendix": "A",
        "title": "Metrics and Null Vectors",
        "printed_span": "585-588",
        "text_pdf_pages": [602, 603, 604],
        "missing_or_blank_printed_pages": [588],
        "sections": [
            "A.1 bilinear form",
            "A.2 diagonalization to orthonormal basis",
            "A.3 general metrics",
            "A.4 null vectors and null blades",
            "A.5 rotors in general metrics",
        ],
    },
    {
        "appendix": "B",
        "title": "Contractions and Other Inner Products",
        "printed_span": "589-596",
        "text_pdf_pages": list(range(605, 613)),
        "missing_or_blank_printed_pages": [],
        "sections": [
            "B.1 other inner products",
            "B.2 equivalence of contraction definitions",
            "B.3 proof of the second duality",
            "B.4 projection and the norm of the contraction",
        ],
    },
    {
        "appendix": "C",
        "title": "Subspace Products Retrieved",
        "printed_span": "597-602",
        "text_pdf_pages": list(range(613, 618)),
        "missing_or_blank_printed_pages": [602],
        "sections": [
            "C.1 outer product from geometric product",
            "C.2 contractions from geometric product",
            "C.3 proof of the grade approach",
        ],
    },
    {
        "appendix": "D",
        "title": "Common Equations",
        "printed_span": "603-608",
        "text_pdf_pages": list(range(618, 623)),
        "missing_or_blank_printed_pages": [608],
        "sections": [
            "D.1 product and operation notation",
            "D.2 sign changes",
            "D.3 transformation behavior",
            "D.4 basic GA equations",
            "D.5 exponentials and rotors",
            "D.6 homogeneous and conformal equations",
        ],
    },
)


def appendix_dir(*parts: str) -> Path:
    """Return an appendix artifact directory, creating it if needed."""
    path = APPENDIX_ARTIFACT_ROOT.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json_artifact(parts: Sequence[str], filename: str, data: Any) -> Path:
    """Write a JSON artifact below ``artifacts/appendices``."""
    path = appendix_dir(*parts) / filename
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def write_csv_artifact(parts: Sequence[str], filename: str, rows: Sequence[dict[str, Any]]) -> Path:
    """Write records to a CSV artifact below ``artifacts/appendices``."""
    path = appendix_dir(*parts) / filename
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def source_span_records() -> list[dict[str, Any]]:
    """Return a copy of the verified appendix source-span map."""
    return [dict(record) for record in SOURCE_SPANS]


def metric_signature(metric: Iterable[float], tol: float = 1e-12) -> dict[str, Any]:
    """Classify a diagonal metric by positive, negative, and zero basis squares."""
    values = tuple(float(value) for value in metric)
    positive = sum(value > tol for value in values)
    negative = sum(value < -tol for value in values)
    zero = len(values) - positive - negative
    determinant = 0.0 if zero else float(np.prod(values))
    return {
        "metric": values,
        "dimension": len(values),
        "positive": positive,
        "negative": negative,
        "zero": zero,
        "signature": f"R^{positive},{negative}" + (f" with {zero} degenerate" if zero else ""),
        "nondegenerate": zero == 0,
        "determinant": determinant,
    }


def bilinear(coords_a: Iterable[float], coords_b: Iterable[float], metric: Iterable[float]) -> float:
    """Evaluate a diagonal bilinear form on coordinate vectors."""
    a = np.asarray(tuple(coords_a), dtype=float)
    b = np.asarray(tuple(coords_b), dtype=float)
    g = np.asarray(tuple(metric), dtype=float)
    if a.shape != b.shape or a.shape != g.shape:
        raise ValueError("coordinate and metric dimensions must agree")
    return float(a @ (g * b))


def quadratic_form(coords: Iterable[float], metric: Iterable[float]) -> float:
    """Evaluate the squared norm induced by a diagonal metric."""
    return bilinear(coords, coords, metric)


def gram_matrix(vectors: Sequence[Iterable[float]], metric: Iterable[float]) -> np.ndarray:
    """Return the Gram matrix for coordinate vectors under a diagonal metric."""
    rows = [np.asarray(tuple(vector), dtype=float) for vector in vectors]
    g = np.asarray(tuple(metric), dtype=float)
    return np.array([[float(left @ (g * right)) for right in rows] for left in rows])


def single_grade(multivector: Multivector) -> int:
    """Return the grade of a homogeneous multivector, treating zero as grade 0."""
    grades = multivector.grades()
    if not grades:
        return 0
    if len(grades) != 1:
        raise ValueError(f"expected a homogeneous multivector, got grades {sorted(grades)}")
    return next(iter(grades))


def grade_part_or_zero(multivector: Multivector, grade: int) -> Multivector:
    """Select a grade, returning zero if the requested grade is impossible."""
    if grade < 0 or grade > multivector.algebra.dimension:
        return multivector.algebra.scalar(0.0)
    return multivector.grade(grade)


def basis_blades(algebra: Algebra, *, include_scalar: bool = True) -> dict[str, Multivector]:
    """Return basis blades keyed by printable names, sorted by grade."""
    start = 0 if include_scalar else 1
    masks = sorted(range(start, 1 << algebra.dimension), key=lambda mask: (algebra.grade(mask), mask))
    return {algebra.basis_name(mask): algebra.blade(mask) for mask in masks}


def basis_blade_records(algebra: Algebra) -> list[dict[str, Any]]:
    """Return grade, square, and reverse-sign records for all basis blades."""
    records: list[dict[str, Any]] = []
    for name, blade in basis_blades(algebra).items():
        grade = single_grade(blade)
        square = blade.gp(blade).scalar_value()
        records.append(
            {
                "name": name,
                "grade": grade,
                "square": square,
                "reverse": repr(blade.reverse()),
                "grade_involution": repr(blade.grade_involution()),
                "clifford_conjugate": repr(blade.clifford_conjugate()),
            }
        )
    return records


def wedge_all(factors: Sequence[Multivector], algebra: Algebra | None = None) -> Multivector:
    """Wedge a sequence of multivectors from left to right."""
    if not factors:
        if algebra is None:
            raise ValueError("empty wedge needs an algebra")
        return algebra.scalar(1.0)
    result = factors[0]
    for factor in factors[1:]:
        result = result.wedge(factor)
    return result


def blade_square(blade: Multivector) -> float:
    """Return the scalar square of a blade."""
    return blade.gp(blade).scalar_value()


def inner_scalar(left: Multivector, right: Multivector) -> float:
    """Return the scalar product as a Python float."""
    return left.scalar_product(right).scalar_value()


def minkowski_null_pair() -> dict[str, Any]:
    """Build a reciprocal null pair in a two-dimensional Minkowski plane."""
    algebra = Algebra([-1, 1], names=["e_t", "e_x"])
    e_t, e_x = algebra.basis()
    scale = 1.0 / math.sqrt(2.0)
    n_plus = (e_t + e_x) * scale
    n_minus = (e_x - e_t) * scale
    bivector = n_plus.wedge(n_minus)
    return {
        "algebra": algebra,
        "e_t": e_t,
        "e_x": e_x,
        "n_plus": n_plus,
        "n_minus": n_minus,
        "checks": {
            "n_plus_square": inner_scalar(n_plus, n_plus),
            "n_minus_square": inner_scalar(n_minus, n_minus),
            "mutual_inner": inner_scalar(n_plus, n_minus),
            "pair_blade_square": blade_square(bivector),
            "pair_blade": repr(bivector),
        },
    }


def outer_from_gp(left: Multivector, right: Multivector) -> Multivector:
    """Recover the outer product of homogeneous factors from the geometric product."""
    return grade_part_or_zero(left.gp(right), single_grade(left) + single_grade(right))


def left_contract_from_gp(left: Multivector, right: Multivector) -> Multivector:
    """Recover the left contraction of homogeneous factors from the geometric product."""
    return grade_part_or_zero(left.gp(right), single_grade(right) - single_grade(left))


def right_contract_from_gp(left: Multivector, right: Multivector) -> Multivector:
    """Recover the right contraction of homogeneous factors from the geometric product."""
    return grade_part_or_zero(left.gp(right), single_grade(left) - single_grade(right))


def scalar_from_gp(left: Multivector, right: Multivector) -> Multivector:
    """Recover the scalar product of homogeneous factors from the geometric product."""
    return left.gp(right).grade(0)


def dot_product(left: Multivector, right: Multivector) -> Multivector:
    """Appendix B dot product: contraction from the lower-grade side."""
    left_grade = single_grade(left)
    right_grade = single_grade(right)
    if left_grade <= right_grade:
        return left.left_contract(right)
    return left.right_contract(right)


def hestenes_inner(left: Multivector, right: Multivector) -> Multivector:
    """Hestenes inner product: dot product, except scalar arguments give zero."""
    if single_grade(left) == 0 or single_grade(right) == 0:
        return left.algebra.scalar(0.0)
    return dot_product(left, right)


def vector_contract_blade_recursive(vector: Multivector, factors: Sequence[Multivector]) -> Multivector:
    """Evaluate the vector-on-blade contraction using the alternating recursive sum."""
    if not factors:
        return vector.algebra.scalar(0.0)
    algebra = vector.algebra
    result = algebra.scalar(0.0)
    for index, factor in enumerate(factors):
        coeff = vector.left_contract(factor).scalar_value()
        rest = wedge_all([item for j, item in enumerate(factors) if j != index], algebra)
        result = result + rest * (((-1.0) ** index) * coeff)
    return result


def projection_onto_blade(vector: Multivector, blade: Multivector) -> Multivector:
    """Project a vector onto a non-null blade."""
    return vector.left_contract(blade).gp(blade.inverse_blade())


def rejection_from_blade(vector: Multivector, blade: Multivector) -> Multivector:
    """Reject a vector from a non-null blade."""
    return vector.wedge(blade).gp(blade.inverse_blade())


def operation_records(
    algebra: Algebra,
    left_items: dict[str, Multivector],
    right_items: dict[str, Multivector],
) -> list[dict[str, Any]]:
    """Tabulate product variants for homogeneous inputs."""
    rows: list[dict[str, Any]] = []
    for left_name, left in left_items.items():
        for right_name, right in right_items.items():
            rows.append(
                {
                    "left": left_name,
                    "right": right_name,
                    "left_grade": single_grade(left),
                    "right_grade": single_grade(right),
                    "gp": repr(left.gp(right)),
                    "wedge": repr(left.wedge(right)),
                    "left_contract": repr(left.left_contract(right)),
                    "right_contract": repr(left.right_contract(right)),
                    "dot_product": repr(dot_product(left, right)),
                    "hestenes_inner": repr(hestenes_inner(left, right)),
                }
            )
    return rows


def grade_selection_records(left_name: str, left: Multivector, right_name: str, right: Multivector) -> list[dict[str, Any]]:
    """Describe how a geometric product splits into appendix C products."""
    product = left.gp(right)
    left_grade = single_grade(left)
    right_grade = single_grade(right)
    selections = [
        ("outer", left_grade + right_grade, outer_from_gp(left, right), left.wedge(right)),
        (
            "left_contract",
            right_grade - left_grade,
            left_contract_from_gp(left, right),
            left.left_contract(right),
        ),
        (
            "right_contract",
            left_grade - right_grade,
            right_contract_from_gp(left, right),
            left.right_contract(right),
        ),
        ("scalar_product", 0, scalar_from_gp(left, right), left.scalar_product(right)),
    ]
    rows = []
    for name, target_grade, recovered, direct in selections:
        rows.append(
            {
                "left": left_name,
                "right": right_name,
                "gp": repr(product),
                "selection": name,
                "target_grade": target_grade,
                "recovered": repr(recovered),
                "direct": repr(direct),
                "matches_direct": recovered.almost_equal(direct),
            }
        )
    return rows


def sign_change_table(max_grade: int = 8) -> list[dict[str, Any]]:
    """Return sign multipliers for the three standard involutions."""
    rows = []
    for grade in range(max_grade + 1):
        rows.append(
            {
                "grade": grade,
                "reverse": (-1) ** (grade * (grade - 1) // 2),
                "grade_involution": (-1) ** grade,
                "clifford_conjugation": (-1) ** (grade * (grade + 1) // 2),
            }
        )
    return rows


def shortest_rotor_between_unit_vectors(a: Multivector, b: Multivector) -> Multivector:
    """Return the shortest Euclidean rotor sending unit vector ``a`` to ``b``."""
    dot = inner_scalar(a, b)
    if dot <= -1.0 + 1e-12:
        raise ValueError("the shortest rotor is not unique for opposite vectors")
    return (a.algebra.scalar(1.0) + b.gp(a)) / math.sqrt(2.0 * (1.0 + dot))


def formula_catalog() -> list[dict[str, str]]:
    """A compact, original formula catalog used by Appendix D."""
    return [
        {
            "group": "grade selection",
            "name": "outer product",
            "formula": "<A_r B_s>_{r+s}",
            "check": "equals A_r.wedge(B_s)",
        },
        {
            "group": "grade selection",
            "name": "left contraction",
            "formula": "<A_r B_s>_{s-r}",
            "check": "zero when r > s",
        },
        {
            "group": "grade selection",
            "name": "right contraction",
            "formula": "<A_r B_s>_{r-s}",
            "check": "zero when r < s",
        },
        {
            "group": "operators",
            "name": "projection onto blade",
            "formula": "(x << B) B^{-1}",
            "check": "projection plus rejection recovers x",
        },
        {
            "group": "operators",
            "name": "rejection from blade",
            "formula": "(x wedge B) B^{-1}",
            "check": "rejection is orthogonal to the blade",
        },
        {
            "group": "operators",
            "name": "unit-vector reflection",
            "formula": "-n x n",
            "check": "component along n changes sign",
        },
        {
            "group": "rotors",
            "name": "shortest rotor from a to b",
            "formula": "(1 + b a) / sqrt(2 (1 + a dot b))",
            "check": "R a reverse(R) equals b",
        },
        {
            "group": "involutions",
            "name": "reverse sign",
            "formula": "(-1)^{r(r-1)/2}",
            "check": "bivectors and trivectors reverse sign",
        },
        {
            "group": "metrics",
            "name": "null vector",
            "formula": "x dot x = 0",
            "check": "possible in mixed or degenerate signatures",
        },
        {
            "group": "conformal",
            "name": "normalized point",
            "formula": "P(x) = o + x + 1/2 |x|^2 infinity",
            "check": "P(x) dot P(x) = 0",
        },
    ]
