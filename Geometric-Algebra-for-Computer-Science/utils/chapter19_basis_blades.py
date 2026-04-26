"""Small basis-blade utilities for Chapter 19 notebooks.

The code is intentionally direct: basis blades are represented by an integer
bitmap plus a scalar weight. The least significant bit is e1, the next bit is
e2, and so on.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class BasisBlade:
    """A weighted basis blade stored as a bitmap and a scalar coefficient."""

    bitmap: int
    scale: float = 1.0

    def __post_init__(self) -> None:
        if not isinstance(self.bitmap, int):
            raise TypeError("bitmap must be an integer")
        if self.bitmap < 0:
            raise ValueError("bitmap must be nonnegative")

    @property
    def grade(self) -> int:
        """Return the number of basis vectors in this blade."""
        return self.bitmap.bit_count()

    @property
    def is_zero(self) -> bool:
        """Return whether this weighted blade has zero scale."""
        return abs(float(self.scale)) <= EPS

    def label(self, names: Sequence[str] | None = None) -> str:
        """Return a compact basis label such as ``e1^e3``."""
        return bitmap_to_label(self.bitmap, names)


def zero_blade() -> BasisBlade:
    """Return the additive zero represented as a zero-scale scalar blade."""
    return BasisBlade(0, 0.0)


def default_names(dim: int) -> tuple[str, ...]:
    """Return basis-vector names e1, e2, ..., edim."""
    if dim < 0:
        raise ValueError("dimension must be nonnegative")
    return tuple(f"e{i + 1}" for i in range(dim))


def bitmap_to_indices(bitmap: int) -> tuple[int, ...]:
    """Return zero-based indices for the set bits in ascending order."""
    if bitmap < 0:
        raise ValueError("bitmap must be nonnegative")
    indices: list[int] = []
    cursor = bitmap
    while cursor:
        bit = cursor & -cursor
        indices.append(bit.bit_length() - 1)
        cursor ^= bit
    return tuple(indices)


def bitmap_string(bitmap: int, width: int | None = None) -> str:
    """Return a binary string with the most significant bit shown on the left."""
    if bitmap < 0:
        raise ValueError("bitmap must be nonnegative")
    if width is None:
        width = max(1, bitmap.bit_length())
    return format(bitmap, f"0{width}b")


def bitmap_to_label(bitmap: int, names: Sequence[str] | None = None, wedge: str = "^") -> str:
    """Return the canonical blade label for a bitmap."""
    if names is None:
        names = default_names(max(1, bitmap.bit_length()))
    indices = bitmap_to_indices(bitmap)
    if not indices:
        return "1"
    if indices[-1] >= len(names):
        raise ValueError("not enough basis names for bitmap")
    return wedge.join(names[i] for i in indices)


def basis_table(dim: int, names: Sequence[str] | None = None) -> list[dict[str, object]]:
    """Return rows describing all basis blades in bitmap order."""
    if dim < 0:
        raise ValueError("dimension must be nonnegative")
    names = tuple(names) if names is not None else default_names(dim)
    rows: list[dict[str, object]] = []
    for bitmap in range(1 << dim):
        rows.append(
            {
                "bitmap": bitmap,
                "binary": bitmap_string(bitmap, dim),
                "grade": bitmap.bit_count(),
                "indices": bitmap_to_indices(bitmap),
                "label": bitmap_to_label(bitmap, names),
            }
        )
    return rows


def swap_pairs(left_bitmap: int, right_bitmap: int) -> tuple[tuple[int, int], ...]:
    """Return inversion pairs that must swap to concatenate blades canonically."""
    pairs: list[tuple[int, int]] = []
    for i in bitmap_to_indices(left_bitmap):
        for j in bitmap_to_indices(right_bitmap):
            if i > j:
                pairs.append((i, j))
    return tuple(pairs)


def canonical_reordering_sign(left_bitmap: int, right_bitmap: int) -> int:
    """Return +1 or -1 from the swaps needed for canonical blade order."""
    return -1 if len(swap_pairs(left_bitmap, right_bitmap)) % 2 else 1


def outer_product_blades(left: BasisBlade, right: BasisBlade) -> BasisBlade:
    """Compute the outer product of two weighted basis blades."""
    if left.is_zero or right.is_zero or (left.bitmap & right.bitmap):
        return zero_blade()
    sign = canonical_reordering_sign(left.bitmap, right.bitmap)
    return BasisBlade(left.bitmap ^ right.bitmap, float(left.scale) * float(right.scale) * sign)


def geometric_product_orthogonal(
    left: BasisBlade,
    right: BasisBlade,
    metric_diag: Sequence[float],
) -> BasisBlade:
    """Compute the geometric product in a diagonal metric."""
    if left.is_zero or right.is_zero:
        return zero_blade()
    common = left.bitmap & right.bitmap
    max_index = max(left.bitmap.bit_length(), right.bitmap.bit_length(), 1) - 1
    if max_index >= len(metric_diag):
        raise ValueError("metric diagonal is too short for these bitmaps")

    metric_scale = 1.0
    for index in bitmap_to_indices(common):
        metric_scale *= float(metric_diag[index])

    sign = canonical_reordering_sign(left.bitmap, right.bitmap)
    scale = float(left.scale) * float(right.scale) * sign * metric_scale
    if abs(scale) <= EPS:
        return zero_blade()
    return BasisBlade(left.bitmap ^ right.bitmap, scale)


def _add_term(terms: dict[int, float], bitmap: int, scale: float, *, eps: float = EPS) -> None:
    if abs(scale) <= eps:
        return
    updated = terms.get(bitmap, 0.0) + float(scale)
    if abs(updated) <= eps:
        terms.pop(bitmap, None)
    else:
        terms[bitmap] = updated


def simplify_terms(terms: Mapping[int, float], *, eps: float = EPS) -> dict[int, float]:
    """Remove tiny coefficients and merge duplicate bitmap keys."""
    simplified: dict[int, float] = {}
    for bitmap, scale in terms.items():
        if bitmap < 0:
            raise ValueError("bitmap keys must be nonnegative")
        _add_term(simplified, int(bitmap), float(scale), eps=eps)
    return simplified


def vector_left_product(
    index: int,
    terms: Mapping[int, float],
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Left-multiply a multivector by one basis vector in an arbitrary metric."""
    if index < 0:
        raise ValueError("basis-vector index must be nonnegative")
    metric = np.asarray(metric, dtype=float)
    if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
        raise ValueError("metric must be a square matrix")
    if index >= metric.shape[0]:
        raise ValueError("basis-vector index is outside the metric")

    result: dict[int, float] = {}
    bit = 1 << index
    for bitmap, coefficient in simplify_terms(terms, eps=eps).items():
        if bitmap >= (1 << metric.shape[0]):
            raise ValueError("term bitmap is outside the metric")

        if not (bitmap & bit):
            lower_count = (bitmap & (bit - 1)).bit_count()
            outer_sign = -1.0 if lower_count % 2 else 1.0
            _add_term(result, bitmap | bit, coefficient * outer_sign, eps=eps)

        for position, basis_index in enumerate(bitmap_to_indices(bitmap)):
            metric_value = float(metric[index, basis_index])
            if abs(metric_value) <= eps:
                continue
            contraction_sign = -1.0 if position % 2 else 1.0
            _add_term(
                result,
                bitmap ^ (1 << basis_index),
                coefficient * contraction_sign * metric_value,
                eps=eps,
            )
    return result


def basis_blade_geometric_product(
    left: BasisBlade,
    right: BasisBlade,
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Compute a basis-blade product in an arbitrary symmetric metric.

    The result may be a sum of basis blades when the metric has off-diagonal
    entries.
    """
    if left.is_zero or right.is_zero:
        return {}
    metric = np.asarray(metric, dtype=float)
    if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
        raise ValueError("metric must be a square matrix")
    if not np.allclose(metric, metric.T, atol=eps):
        raise ValueError("metric must be symmetric")
    if max(left.bitmap.bit_length(), right.bitmap.bit_length()) > metric.shape[0]:
        raise ValueError("blade bitmap is outside the metric")

    terms: dict[int, float] = {right.bitmap: float(right.scale)}
    for index in reversed(bitmap_to_indices(left.bitmap)):
        terms = vector_left_product(index, terms, metric, eps=eps)
    if left.bitmap == 0:
        terms = dict(terms)
    for bitmap in list(terms):
        terms[bitmap] *= float(left.scale)
    return simplify_terms(terms, eps=eps)


def multiply_multivectors(
    left: Mapping[int, float],
    right: Mapping[int, float],
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Distribute the geometric product over two sparse multivectors."""
    result: dict[int, float] = {}
    for left_bitmap, left_scale in simplify_terms(left, eps=eps).items():
        for right_bitmap, right_scale in simplify_terms(right, eps=eps).items():
            product = basis_blade_geometric_product(
                BasisBlade(left_bitmap, left_scale),
                BasisBlade(right_bitmap, right_scale),
                metric,
                eps=eps,
            )
            for bitmap, scale in product.items():
                _add_term(result, bitmap, scale, eps=eps)
    return simplify_terms(result, eps=eps)


def grade_project(terms: Mapping[int, float], grade: int, *, eps: float = EPS) -> dict[int, float]:
    """Keep only terms of a requested grade."""
    if grade < 0:
        return {}
    return simplify_terms(
        {bitmap: scale for bitmap, scale in terms.items() if bitmap.bit_count() == grade},
        eps=eps,
    )


def left_contraction_blades(
    left: BasisBlade,
    right: BasisBlade,
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Return the left contraction of two basis blades by grade selection."""
    if left.grade > right.grade:
        return {}
    product = basis_blade_geometric_product(left, right, metric, eps=eps)
    return grade_project(product, right.grade - left.grade, eps=eps)


def scalar_product_blades(
    left: BasisBlade,
    right: BasisBlade,
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Return the scalar part of a basis-blade geometric product."""
    product = basis_blade_geometric_product(left, right, metric, eps=eps)
    return grade_project(product, 0, eps=eps)


def commutator_blades(
    left: BasisBlade,
    right: BasisBlade,
    metric: np.ndarray,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Return one half of AB - BA for two basis blades."""
    ab = basis_blade_geometric_product(left, right, metric, eps=eps)
    ba = basis_blade_geometric_product(right, left, metric, eps=eps)
    result: dict[int, float] = {}
    for bitmap, scale in ab.items():
        _add_term(result, bitmap, 0.5 * scale, eps=eps)
    for bitmap, scale in ba.items():
        _add_term(result, bitmap, -0.5 * scale, eps=eps)
    return simplify_terms(result, eps=eps)


def reversion_sign(grade: int) -> int:
    """Return the sign multiplier for reversion on a grade."""
    return -1 if ((grade * (grade - 1) // 2) % 2) else 1


def grade_involution_sign(grade: int) -> int:
    """Return the sign multiplier for grade involution on a grade."""
    return -1 if grade % 2 else 1


def clifford_conjugation_sign(grade: int) -> int:
    """Return the sign multiplier for Clifford conjugation on a grade."""
    return -1 if ((grade * (grade + 1) // 2) % 2) else 1


def format_multivector(
    terms: Mapping[int, float],
    names: Sequence[str] | None = None,
    *,
    precision: int = 3,
    eps: float = EPS,
) -> str:
    """Format sparse multivector terms for notebook display."""
    terms = simplify_terms(terms, eps=eps)
    if not terms:
        return "0"

    pieces: list[str] = []
    for bitmap in sorted(terms, key=lambda value: (value.bit_count(), value)):
        coefficient = terms[bitmap]
        label = bitmap_to_label(bitmap, names)
        magnitude = abs(coefficient)
        rounded = round(magnitude, precision)
        if abs(rounded - 1.0) <= 10 ** (-precision) and label != "1":
            body = label
        else:
            body = f"{magnitude:.{precision}g}"
            if label != "1":
                body = f"{body} {label}"
        sign = "-" if coefficient < 0 else "+"
        pieces.append((sign, body))

    first_sign, first_body = pieces[0]
    output = first_body if first_sign == "+" else f"-{first_body}"
    for sign, body in pieces[1:]:
        output += f" {sign} {body}"
    return output


def terms_to_rows(
    terms: Mapping[int, float],
    names: Sequence[str] | None = None,
    *,
    precision: int = 6,
) -> list[dict[str, object]]:
    """Convert sparse multivector terms to notebook-friendly rows."""
    return [
        {
            "bitmap": bitmap,
            "label": bitmap_to_label(bitmap, names),
            "grade": bitmap.bit_count(),
            "coefficient": round(float(scale), precision),
        }
        for bitmap, scale in sorted(simplify_terms(terms).items())
    ]
