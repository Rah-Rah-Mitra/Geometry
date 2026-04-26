"""A compact orthogonal-metric geometric algebra implementation.

The notebook course needs transparent algebra more than raw performance. This module
therefore favors a small dictionary representation: a multivector maps a basis-blade
bitmap to a scalar coefficient. For example, in a 3-D algebra, mask ``0b101`` denotes
``e1^e3``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, sqrt
from typing import Iterable

import numpy as np

EPS = 1e-12


def _grade(mask: int) -> int:
    return int(mask.bit_count())


def _basis_sign(left: int, right: int) -> int:
    """Return the canonical reordering sign for two basis-blade bitmaps."""
    swaps = 0
    a = left
    while a:
        bit = a & -a
        i = bit.bit_length() - 1
        swaps += (right & ((1 << i) - 1)).bit_count()
        a ^= bit
    return -1 if swaps % 2 else 1


@dataclass(frozen=True)
class Algebra:
    """A real geometric algebra with an orthogonal diagonal metric."""

    metric: tuple[float, ...]
    names: tuple[str, ...] | None = None

    def __init__(self, metric: Iterable[float], names: Iterable[str] | None = None) -> None:
        metric_tuple = tuple(float(value) for value in metric)
        if not metric_tuple:
            raise ValueError("an algebra needs at least one basis vector")
        object.__setattr__(self, "metric", metric_tuple)
        if names is None:
            names_tuple = tuple(f"e{i + 1}" for i in range(len(metric_tuple)))
        else:
            names_tuple = tuple(names)
            if len(names_tuple) != len(metric_tuple):
                raise ValueError("basis name count must match the metric dimension")
        object.__setattr__(self, "names", names_tuple)

    @property
    def dimension(self) -> int:
        return len(self.metric)

    def scalar(self, value: float) -> "Multivector":
        return Multivector(self, {0: float(value)})

    def blade(self, mask: int, value: float = 1.0) -> "Multivector":
        self._check_mask(mask)
        return Multivector(self, {mask: float(value)})

    def basis_vector(self, index: int) -> "Multivector":
        if index < 0 or index >= self.dimension:
            raise IndexError(index)
        return self.blade(1 << index)

    def basis(self) -> tuple["Multivector", ...]:
        return tuple(self.basis_vector(i) for i in range(self.dimension))

    def vector(self, coordinates: Iterable[float]) -> "Multivector":
        terms: dict[int, float] = {}
        for i, value in enumerate(coordinates):
            if i >= self.dimension:
                raise ValueError("too many coordinates for this algebra")
            if abs(float(value)) > EPS:
                terms[1 << i] = float(value)
        return Multivector(self, terms)

    def pseudoscalar(self) -> "Multivector":
        return self.blade((1 << self.dimension) - 1)

    def grade(self, mask: int) -> int:
        self._check_mask(mask)
        return _grade(mask)

    def _check_mask(self, mask: int) -> None:
        if mask < 0 or mask >= (1 << self.dimension):
            raise ValueError(f"basis mask {mask!r} is outside this algebra")

    def _basis_gp(self, left: int, right: int) -> tuple[int, float]:
        self._check_mask(left)
        self._check_mask(right)
        coeff = float(_basis_sign(left, right))
        common = left & right
        bitset = common
        while bitset:
            bit = bitset & -bitset
            index = bit.bit_length() - 1
            coeff *= self.metric[index]
            bitset ^= bit
        return left ^ right, coeff

    def basis_name(self, mask: int) -> str:
        self._check_mask(mask)
        if mask == 0:
            return "1"
        return "^".join(name for i, name in enumerate(self.names or ()) if mask & (1 << i))


class Multivector:
    """Dictionary-backed multivector."""

    def __init__(self, algebra: Algebra, terms: dict[int, float] | None = None) -> None:
        self.algebra = algebra
        cleaned: dict[int, float] = {}
        for mask, value in (terms or {}).items():
            algebra._check_mask(mask)
            value = float(value)
            if abs(value) > EPS:
                cleaned[mask] = cleaned.get(mask, 0.0) + value
        self.terms = {mask: value for mask, value in cleaned.items() if abs(value) > EPS}

    def __repr__(self) -> str:
        if not self.terms:
            return "0"
        pieces = []
        for mask in sorted(self.terms, key=lambda item: (_grade(item), item)):
            coeff = self.terms[mask]
            name = self.algebra.basis_name(mask)
            if mask == 0:
                pieces.append(f"{coeff:g}")
            elif abs(coeff - 1.0) < EPS:
                pieces.append(name)
            elif abs(coeff + 1.0) < EPS:
                pieces.append(f"-{name}")
            else:
                pieces.append(f"{coeff:g}{name}")
        return " + ".join(pieces).replace("+ -", "- ")

    def __bool__(self) -> bool:
        return bool(self.terms)

    def _assert_same_algebra(self, other: "Multivector") -> None:
        if self.algebra != other.algebra:
            raise TypeError("multivectors belong to different algebras")

    def __add__(self, other: "Multivector | float") -> "Multivector":
        other = self._coerce(other)
        self._assert_same_algebra(other)
        terms = dict(self.terms)
        for mask, value in other.terms.items():
            terms[mask] = terms.get(mask, 0.0) + value
        return Multivector(self.algebra, terms)

    __radd__ = __add__

    def __sub__(self, other: "Multivector | float") -> "Multivector":
        return self + (-self._coerce(other))

    def __rsub__(self, other: "Multivector | float") -> "Multivector":
        return self._coerce(other) + (-self)

    def __neg__(self) -> "Multivector":
        return Multivector(self.algebra, {mask: -value for mask, value in self.terms.items()})

    def __mul__(self, other: float) -> "Multivector":
        if isinstance(other, Multivector):
            raise TypeError("use .gp(), .wedge(), or contractions for multivector products")
        return Multivector(self.algebra, {mask: value * float(other) for mask, value in self.terms.items()})

    def __rmul__(self, other: float) -> "Multivector":
        return self * other

    def __truediv__(self, other: float) -> "Multivector":
        if abs(float(other)) < EPS:
            raise ZeroDivisionError("division by a near-zero scalar")
        return self * (1.0 / float(other))

    def _coerce(self, value: "Multivector | float") -> "Multivector":
        if isinstance(value, Multivector):
            return value
        return self.algebra.scalar(float(value))

    def copy(self) -> "Multivector":
        return Multivector(self.algebra, dict(self.terms))

    def grades(self) -> set[int]:
        return {_grade(mask) for mask in self.terms}

    def grade(self, grade: int) -> "Multivector":
        return Multivector(
            self.algebra,
            {mask: value for mask, value in self.terms.items() if _grade(mask) == grade},
        )

    def scalar_value(self) -> float:
        non_scalar = [mask for mask in self.terms if mask != 0]
        if non_scalar:
            raise ValueError(f"not a scalar: {self!r}")
        return self.terms.get(0, 0.0)

    def norm2(self) -> float:
        return self.scalar_product(self).scalar_value()

    def norm(self) -> float:
        return sqrt(abs(self.norm2()))

    def almost_equal(self, other: "Multivector", tol: float = 1e-9) -> bool:
        self._assert_same_algebra(other)
        masks = set(self.terms) | set(other.terms)
        return all(abs(self.terms.get(mask, 0.0) - other.terms.get(mask, 0.0)) <= tol for mask in masks)

    def gp(self, other: "Multivector | float") -> "Multivector":
        other = self._coerce(other)
        self._assert_same_algebra(other)
        terms: dict[int, float] = {}
        for left_mask, left_value in self.terms.items():
            for right_mask, right_value in other.terms.items():
                mask, coeff = self.algebra._basis_gp(left_mask, right_mask)
                value = left_value * right_value * coeff
                terms[mask] = terms.get(mask, 0.0) + value
        return Multivector(self.algebra, terms)

    def wedge(self, other: "Multivector | float") -> "Multivector":
        other = self._coerce(other)
        self._assert_same_algebra(other)
        terms: dict[int, float] = {}
        for left_mask, left_value in self.terms.items():
            for right_mask, right_value in other.terms.items():
                if left_mask & right_mask:
                    continue
                mask, coeff = self.algebra._basis_gp(left_mask, right_mask)
                terms[mask] = terms.get(mask, 0.0) + left_value * right_value * coeff
        return Multivector(self.algebra, terms)

    def left_contract(self, other: "Multivector | float") -> "Multivector":
        other = self._coerce(other)
        self._assert_same_algebra(other)
        terms: dict[int, float] = {}
        for left_mask, left_value in self.terms.items():
            r = _grade(left_mask)
            for right_mask, right_value in other.terms.items():
                s = _grade(right_mask)
                if r > s:
                    continue
                mask, coeff = self.algebra._basis_gp(left_mask, right_mask)
                if _grade(mask) == s - r:
                    terms[mask] = terms.get(mask, 0.0) + left_value * right_value * coeff
        return Multivector(self.algebra, terms)

    def right_contract(self, other: "Multivector | float") -> "Multivector":
        other = self._coerce(other)
        self._assert_same_algebra(other)
        terms: dict[int, float] = {}
        for left_mask, left_value in self.terms.items():
            r = _grade(left_mask)
            for right_mask, right_value in other.terms.items():
                s = _grade(right_mask)
                if r < s:
                    continue
                mask, coeff = self.algebra._basis_gp(left_mask, right_mask)
                if _grade(mask) == r - s:
                    terms[mask] = terms.get(mask, 0.0) + left_value * right_value * coeff
        return Multivector(self.algebra, terms)

    def scalar_product(self, other: "Multivector | float") -> "Multivector":
        return self.gp(self._coerce(other)).grade(0)

    def reverse(self) -> "Multivector":
        return Multivector(
            self.algebra,
            {
                mask: value * ((-1) ** (_grade(mask) * (_grade(mask) - 1) // 2))
                for mask, value in self.terms.items()
            },
        )

    def grade_involution(self) -> "Multivector":
        return Multivector(
            self.algebra,
            {mask: value * ((-1) ** _grade(mask)) for mask, value in self.terms.items()},
        )

    def clifford_conjugate(self) -> "Multivector":
        return Multivector(
            self.algebra,
            {
                mask: value * ((-1) ** (_grade(mask) * (_grade(mask) + 1) // 2))
                for mask, value in self.terms.items()
            },
        )

    def inverse_blade(self) -> "Multivector":
        rev = self.reverse()
        denom = self.gp(rev).scalar_value()
        if abs(denom) < EPS:
            raise ZeroDivisionError(f"blade has no stable inverse: {self!r}")
        return rev / denom

    def dual(self) -> "Multivector":
        return self.gp(self.algebra.pseudoscalar().inverse_blade())

    def undual(self) -> "Multivector":
        return self.gp(self.algebra.pseudoscalar())

    def meet(self, other: "Multivector") -> "Multivector":
        """Regressive product in a nondegenerate full space."""
        return self.dual().wedge(other.dual()).undual()

    def sandwich(self, operator: "Multivector") -> "Multivector":
        return operator.gp(self).gp(operator.reverse())

    def coordinates(self) -> np.ndarray:
        """Return grade-1 coordinates."""
        vector = np.zeros(self.algebra.dimension)
        for i in range(self.algebra.dimension):
            vector[i] = self.terms.get(1 << i, 0.0)
        if any(_grade(mask) != 1 for mask in self.terms):
            raise ValueError(f"not a pure vector: {self!r}")
        return vector


def unit_rotor(plane_bivector: Multivector, angle: float) -> Multivector:
    """Return ``cos(theta/2) - B sin(theta/2)`` for a unit Euclidean bivector."""
    scale = plane_bivector.norm()
    if scale < EPS:
        raise ValueError("rotor plane must be nonzero")
    B = plane_bivector / scale
    return plane_bivector.algebra.scalar(cos(angle / 2.0)) - B * sin(angle / 2.0)
