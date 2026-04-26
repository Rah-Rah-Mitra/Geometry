"""Helpers for Chapter 22: specializing geometric algebra code.

The module keeps the machinery intentionally small and inspectable. It is not a
full geometric algebra package; it is a notebook companion for comparing generic
multivector code with generated kernels for known algebra/type specifications.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from math import cos, sin, sqrt
from time import perf_counter
from typing import Callable, Mapping, Sequence

import numpy as np
import sympy as sp

EPS = 1e-12


def _as_tuple(value: Sequence[object]) -> tuple[object, ...]:
    return tuple(value)


@dataclass(frozen=True)
class AlgebraSpec:
    """A minimal algebra specification for generated-code experiments."""

    names: tuple[str, ...]
    metric: np.ndarray
    name: str = "algebra"

    def __post_init__(self) -> None:
        names = tuple(str(name) for name in self.names)
        metric = np.asarray(self.metric, dtype=float)
        if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
            raise ValueError("metric must be a square matrix")
        if metric.shape[0] != len(names):
            raise ValueError("metric shape must match the number of basis names")
        if not np.allclose(metric, metric.T, atol=EPS):
            raise ValueError("metric must be symmetric")
        object.__setattr__(self, "names", names)
        object.__setattr__(self, "metric", metric)

    @classmethod
    def euclidean3(cls) -> "AlgebraSpec":
        """Return the 3-D Euclidean algebra used for product checks."""

        return cls(("e1", "e2", "e3"), np.eye(3), "Euclidean 3D")

    @classmethod
    def conformal_like_3d(cls) -> "AlgebraSpec":
        """Return a 5-D null-basis specification used for storage examples."""

        metric = np.diag([1.0, 1.0, 1.0, 0.0, 0.0])
        metric[3, 4] = -1.0
        metric[4, 3] = -1.0
        return cls(("e1", "e2", "e3", "o", "inf"), metric, "3D conformal-style null basis")

    @property
    def dim(self) -> int:
        return len(self.names)

    @property
    def blade_count(self) -> int:
        return 1 << self.dim

    def label(self, bitmap: int) -> str:
        return bitmap_to_label(bitmap, self.names)

    def labels(self) -> list[str]:
        return [self.label(bitmap) for bitmap in range(self.blade_count)]


@dataclass(frozen=True)
class SpecializedType:
    """A generated multivector type with stored and constant coordinates."""

    name: str
    stored: tuple[int, ...]
    constants: Mapping[int, float] = field(default_factory=dict)
    note: str = ""

    def __post_init__(self) -> None:
        stored = tuple(int(bitmap) for bitmap in self.stored)
        constants = {int(bitmap): float(value) for bitmap, value in self.constants.items()}
        if len(set(stored)) != len(stored):
            raise ValueError("stored coordinate bitmaps must be unique")
        overlap = set(stored).intersection(constants)
        if overlap:
            raise ValueError(f"stored and constant coordinates overlap: {sorted(overlap)}")
        if any(bitmap < 0 for bitmap in stored) or any(bitmap < 0 for bitmap in constants):
            raise ValueError("basis bitmaps must be nonnegative")
        object.__setattr__(self, "stored", stored)
        object.__setattr__(self, "constants", constants)

    @property
    def coordinate_count(self) -> int:
        return len(self.stored)

    @property
    def active_bitmaps(self) -> tuple[int, ...]:
        return self.stored + tuple(self.constants)

    def sparse_terms(self, coordinates: Sequence[float]) -> dict[int, float]:
        """Return sparse multivector terms from stored coordinates plus constants."""

        if len(coordinates) != len(self.stored):
            raise ValueError(f"{self.name} expects {len(self.stored)} coordinates")
        terms = {bitmap: float(value) for bitmap, value in zip(self.stored, coordinates)}
        terms.update(self.constants)
        return simplify_terms(terms)

    def dense_array(self, coordinates: Sequence[float], spec: AlgebraSpec) -> np.ndarray:
        """Return a dense coordinate array for this specialized value."""

        dense = np.zeros(spec.blade_count, dtype=float)
        for bitmap, value in self.sparse_terms(coordinates).items():
            dense[bitmap] = value
        return dense


@dataclass(frozen=True)
class SymbolicKernel:
    """A symbolic generated kernel for a specialized product."""

    name: str
    product: str
    left_type: SpecializedType
    right_type: SpecializedType
    expressions: Mapping[int, sp.Expr]
    left_symbols: tuple[tuple[int, sp.Symbol], ...]
    right_symbols: tuple[tuple[int, sp.Symbol], ...]

    @property
    def output_bitmaps(self) -> tuple[int, ...]:
        return tuple(sorted(self.expressions, key=lambda bitmap: (bitmap.bit_count(), bitmap)))

    @property
    def operation_count(self) -> int:
        return int(sum(sp.count_ops(expr) for expr in self.expressions.values()))

    def rows(self, spec: AlgebraSpec) -> list[dict[str, object]]:
        """Return notebook-friendly rows for the generated expressions."""

        rows: list[dict[str, object]] = []
        for bitmap in self.output_bitmaps:
            expr = sp.simplify(self.expressions[bitmap])
            rows.append(
                {
                    "bitmap": bitmap,
                    "label": spec.label(bitmap),
                    "grade": bitmap.bit_count(),
                    "expression": str(expr),
                    "ops": int(sp.count_ops(expr)),
                }
            )
        return rows

    def emit_python(self, spec: AlgebraSpec, function_name: str | None = None) -> str:
        """Emit readable Python-like code for the generated kernel."""

        function_name = function_name or self.name
        replacements: list[tuple[str, str]] = []
        for index, (_, symbol) in enumerate(self.left_symbols):
            replacements.append((str(symbol), f"x[{index}]"))
        for index, (_, symbol) in enumerate(self.right_symbols):
            replacements.append((str(symbol), f"y[{index}]"))
        replacements.sort(key=lambda pair: len(pair[0]), reverse=True)

        lines = [
            f"def {function_name}(x, y):",
            f"    # {self.left_type.name} stored order: "
            + ", ".join(spec.label(bitmap) for bitmap, _ in self.left_symbols),
            f"    # {self.right_type.name} stored order: "
            + ", ".join(spec.label(bitmap) for bitmap, _ in self.right_symbols),
            "    return np.array([",
        ]
        for bitmap in self.output_bitmaps:
            code = sp.pycode(sp.simplify(self.expressions[bitmap]))
            for symbol_name, replacement in replacements:
                code = code.replace(symbol_name, replacement)
            lines.append(f"        {code},  # {spec.label(bitmap)}")
        lines.append("    ], dtype=float)")
        return "\n".join(lines)


def bitmap_to_indices(bitmap: int) -> tuple[int, ...]:
    """Return zero-based basis-vector indices in a bitmap."""

    if bitmap < 0:
        raise ValueError("bitmap must be nonnegative")
    indices: list[int] = []
    cursor = int(bitmap)
    while cursor:
        bit = cursor & -cursor
        indices.append(bit.bit_length() - 1)
        cursor ^= bit
    return tuple(indices)


def bitmap_to_label(bitmap: int, names: Sequence[str], wedge: str = "^") -> str:
    """Return a compact label such as ``e1^e3``."""

    indices = bitmap_to_indices(bitmap)
    if not indices:
        return "1"
    if indices[-1] >= len(names):
        raise ValueError("not enough basis names for bitmap")
    return wedge.join(str(names[index]) for index in indices)


def basis_rows(spec: AlgebraSpec) -> list[dict[str, object]]:
    """Return table rows describing every basis blade."""

    return [
        {
            "bitmap": bitmap,
            "binary": format(bitmap, f"0{spec.dim}b"),
            "grade": bitmap.bit_count(),
            "label": spec.label(bitmap),
        }
        for bitmap in range(spec.blade_count)
    ]


def reordering_sign(left_bitmap: int, right_bitmap: int) -> int:
    """Return the sign needed to put concatenated basis vectors in canonical order."""

    swaps = 0
    for left_index in bitmap_to_indices(left_bitmap):
        for right_index in bitmap_to_indices(right_bitmap):
            if left_index > right_index:
                swaps += 1
    return -1 if swaps % 2 else 1


def simplify_terms(terms: Mapping[int, float], *, eps: float = EPS) -> dict[int, float]:
    """Remove tiny numeric coefficients from a sparse multivector."""

    result: dict[int, float] = {}
    for bitmap, value in terms.items():
        value = float(value)
        if abs(value) <= eps:
            continue
        updated = result.get(int(bitmap), 0.0) + value
        if abs(updated) <= eps:
            result.pop(int(bitmap), None)
        else:
            result[int(bitmap)] = updated
    return result


def _add_numeric(terms: dict[int, float], bitmap: int, value: float, *, eps: float = EPS) -> None:
    if abs(value) <= eps:
        return
    updated = terms.get(bitmap, 0.0) + float(value)
    if abs(updated) <= eps:
        terms.pop(bitmap, None)
    else:
        terms[bitmap] = updated


def outer_product_terms(
    left: Mapping[int, float],
    right: Mapping[int, float],
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Compute the outer product of two sparse numeric multivectors."""

    result: dict[int, float] = {}
    for left_bitmap, left_value in simplify_terms(left, eps=eps).items():
        for right_bitmap, right_value in simplify_terms(right, eps=eps).items():
            if left_bitmap & right_bitmap:
                continue
            sign = reordering_sign(left_bitmap, right_bitmap)
            _add_numeric(result, left_bitmap ^ right_bitmap, sign * left_value * right_value, eps=eps)
    return simplify_terms(result, eps=eps)


def vector_left_product(
    index: int,
    terms: Mapping[int, float],
    spec: AlgebraSpec,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Left-multiply a sparse multivector by one basis vector."""

    if index < 0 or index >= spec.dim:
        raise ValueError("basis-vector index is outside the algebra")
    result: dict[int, float] = {}
    bit = 1 << index
    for bitmap, coefficient in simplify_terms(terms, eps=eps).items():
        if bitmap >= spec.blade_count:
            raise ValueError("term bitmap is outside the algebra")
        if not (bitmap & bit):
            lower_count = (bitmap & (bit - 1)).bit_count()
            outer_sign = -1.0 if lower_count % 2 else 1.0
            _add_numeric(result, bitmap | bit, coefficient * outer_sign, eps=eps)
        for position, basis_index in enumerate(bitmap_to_indices(bitmap)):
            metric_value = float(spec.metric[index, basis_index])
            if abs(metric_value) <= eps:
                continue
            contraction_sign = -1.0 if position % 2 else 1.0
            _add_numeric(
                result,
                bitmap ^ (1 << basis_index),
                coefficient * contraction_sign * metric_value,
                eps=eps,
            )
    return simplify_terms(result, eps=eps)


def basis_blade_geometric_product(
    left_bitmap: int,
    right_bitmap: int,
    spec: AlgebraSpec,
    *,
    left_scale: float = 1.0,
    right_scale: float = 1.0,
    eps: float = EPS,
) -> dict[int, float]:
    """Compute a basis-blade geometric product in an arbitrary symmetric metric."""

    if abs(left_scale) <= eps or abs(right_scale) <= eps:
        return {}
    if max(left_bitmap.bit_length(), right_bitmap.bit_length()) > spec.dim:
        raise ValueError("basis bitmap is outside the algebra")

    terms: dict[int, float] = {right_bitmap: float(right_scale)}
    for index in reversed(bitmap_to_indices(left_bitmap)):
        terms = vector_left_product(index, terms, spec, eps=eps)
    for bitmap in list(terms):
        terms[bitmap] *= float(left_scale)
    return simplify_terms(terms, eps=eps)


def geometric_product_terms(
    left: Mapping[int, float],
    right: Mapping[int, float],
    spec: AlgebraSpec,
    *,
    eps: float = EPS,
) -> dict[int, float]:
    """Distribute the geometric product over sparse numeric multivectors."""

    result: dict[int, float] = {}
    for left_bitmap, left_value in simplify_terms(left, eps=eps).items():
        for right_bitmap, right_value in simplify_terms(right, eps=eps).items():
            product = basis_blade_geometric_product(
                left_bitmap,
                right_bitmap,
                spec,
                left_scale=left_value,
                right_scale=right_value,
                eps=eps,
            )
            for bitmap, value in product.items():
                _add_numeric(result, bitmap, value, eps=eps)
    return simplify_terms(result, eps=eps)


def reverse_terms(terms: Mapping[int, float]) -> dict[int, float]:
    """Return the reverse of a sparse multivector."""

    return {
        bitmap: float(value) * (-1 if ((bitmap.bit_count() * (bitmap.bit_count() - 1) // 2) % 2) else 1)
        for bitmap, value in simplify_terms(terms).items()
    }


def scale_terms(terms: Mapping[int, float], scale: float) -> dict[int, float]:
    """Scale a sparse multivector."""

    return simplify_terms({bitmap: scale * value for bitmap, value in terms.items()})


def add_terms(*items: Mapping[int, float]) -> dict[int, float]:
    """Add sparse multivectors."""

    result: dict[int, float] = {}
    for terms in items:
        for bitmap, value in terms.items():
            _add_numeric(result, int(bitmap), float(value))
    return simplify_terms(result)


def format_multivector(terms: Mapping[int, float], spec: AlgebraSpec, precision: int = 4) -> str:
    """Format a sparse multivector in basis-label order."""

    simplified = simplify_terms(terms)
    if not simplified:
        return "0"
    parts: list[str] = []
    for bitmap in sorted(simplified, key=lambda item: (item.bit_count(), item)):
        value = simplified[bitmap]
        label = spec.label(bitmap)
        magnitude = abs(value)
        if label != "1" and abs(magnitude - 1.0) <= 10 ** (-precision):
            body = label
        else:
            body = f"{magnitude:.{precision}g}" if label == "1" else f"{magnitude:.{precision}g} {label}"
        parts.append(("-" if value < 0 else "+", body))
    first_sign, first_body = parts[0]
    text = first_body if first_sign == "+" else f"-{first_body}"
    for sign, body in parts[1:]:
        text += f" {sign} {body}"
    return text


def type_from_grades(name: str, spec: AlgebraSpec, grades: Sequence[int], note: str = "") -> SpecializedType:
    """Create a specialized type from a list of grades."""

    grade_set = {int(grade) for grade in grades}
    stored = tuple(bitmap for bitmap in range(spec.blade_count) if bitmap.bit_count() in grade_set)
    return SpecializedType(name=name, stored=stored, note=note)


def storage_layout_rows(
    spec: AlgebraSpec,
    specialized_types: Sequence[SpecializedType],
) -> list[dict[str, object]]:
    """Return per-basis-coordinate storage categories for specialized types."""

    rows: list[dict[str, object]] = []
    for type_spec in specialized_types:
        stored = set(type_spec.stored)
        constants = set(type_spec.constants)
        for bitmap in range(spec.blade_count):
            if bitmap in stored:
                status = "stored"
            elif bitmap in constants:
                status = "constant"
            else:
                status = "zero"
            rows.append(
                {
                    "type": type_spec.name,
                    "bitmap": bitmap,
                    "label": spec.label(bitmap),
                    "grade": bitmap.bit_count(),
                    "status": status,
                }
            )
    return rows


def storage_summary(
    spec: AlgebraSpec,
    specialized_types: Sequence[SpecializedType],
) -> list[dict[str, object]]:
    """Summarize dense, stored, constant, and zero coordinates by type."""

    rows: list[dict[str, object]] = []
    for type_spec in specialized_types:
        active = len(set(type_spec.stored).union(type_spec.constants))
        rows.append(
            {
                "type": type_spec.name,
                "dense_coordinates": spec.blade_count,
                "stored_coordinates": len(type_spec.stored),
                "constant_coordinates": len(type_spec.constants),
                "known_zero_coordinates": spec.blade_count - active,
                "compression_ratio": spec.blade_count / max(1, len(type_spec.stored)),
            }
        )
    return rows


def _symbolic_terms_for_type(
    type_spec: SpecializedType,
    prefix: str,
) -> tuple[dict[int, sp.Expr], tuple[tuple[int, sp.Symbol], ...]]:
    terms: dict[int, sp.Expr] = {}
    symbols: list[tuple[int, sp.Symbol]] = []
    for index, bitmap in enumerate(type_spec.stored):
        symbol = sp.Symbol(f"{prefix}_{index}")
        terms[bitmap] = symbol
        symbols.append((bitmap, symbol))
    for bitmap, value in type_spec.constants.items():
        terms[bitmap] = sp.nsimplify(value)
    return terms, tuple(symbols)


def _add_symbolic(terms: dict[int, sp.Expr], bitmap: int, value: sp.Expr) -> None:
    value = sp.simplify(value)
    if value == 0:
        return
    updated = sp.simplify(terms.get(bitmap, sp.Integer(0)) + value)
    if updated == 0:
        terms.pop(bitmap, None)
    else:
        terms[bitmap] = updated


def symbolic_outer_product(
    left: Mapping[int, sp.Expr],
    right: Mapping[int, sp.Expr],
) -> dict[int, sp.Expr]:
    """Compute an outer-product expression from symbolic sparse terms."""

    result: dict[int, sp.Expr] = {}
    for left_bitmap, left_value in left.items():
        for right_bitmap, right_value in right.items():
            if left_bitmap & right_bitmap:
                continue
            sign = reordering_sign(left_bitmap, right_bitmap)
            _add_symbolic(result, left_bitmap ^ right_bitmap, sign * left_value * right_value)
    return {bitmap: sp.simplify(value) for bitmap, value in result.items()}


def _symbolic_vector_left_product(
    index: int,
    terms: Mapping[int, sp.Expr],
    spec: AlgebraSpec,
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    bit = 1 << index
    for bitmap, coefficient in terms.items():
        if not (bitmap & bit):
            lower_count = (bitmap & (bit - 1)).bit_count()
            outer_sign = -1 if lower_count % 2 else 1
            _add_symbolic(result, bitmap | bit, coefficient * outer_sign)
        for position, basis_index in enumerate(bitmap_to_indices(bitmap)):
            metric_value = sp.nsimplify(spec.metric[index, basis_index])
            if metric_value == 0:
                continue
            contraction_sign = -1 if position % 2 else 1
            _add_symbolic(
                result,
                bitmap ^ (1 << basis_index),
                coefficient * contraction_sign * metric_value,
            )
    return result


def symbolic_geometric_product(
    left: Mapping[int, sp.Expr],
    right: Mapping[int, sp.Expr],
    spec: AlgebraSpec,
) -> dict[int, sp.Expr]:
    """Compute a symbolic geometric product by distributing basis products."""

    result: dict[int, sp.Expr] = {}
    for left_bitmap, left_value in left.items():
        for right_bitmap, right_value in right.items():
            terms: dict[int, sp.Expr] = {right_bitmap: right_value}
            for index in reversed(bitmap_to_indices(left_bitmap)):
                terms = _symbolic_vector_left_product(index, terms, spec)
            for bitmap, value in terms.items():
                _add_symbolic(result, bitmap, left_value * value)
    return {bitmap: sp.simplify(value) for bitmap, value in result.items()}


def generate_product_kernel(
    name: str,
    left_type: SpecializedType,
    right_type: SpecializedType,
    spec: AlgebraSpec,
    *,
    product: str = "outer",
) -> SymbolicKernel:
    """Generate a symbolic product kernel for two specialized types."""

    left_terms, left_symbols = _symbolic_terms_for_type(left_type, "x")
    right_terms, right_symbols = _symbolic_terms_for_type(right_type, "y")
    if product == "outer":
        expressions = symbolic_outer_product(left_terms, right_terms)
    elif product == "geometric":
        expressions = symbolic_geometric_product(left_terms, right_terms, spec)
    else:
        raise ValueError("product must be 'outer' or 'geometric'")
    return SymbolicKernel(
        name=name,
        product=product,
        left_type=left_type,
        right_type=right_type,
        expressions=expressions,
        left_symbols=left_symbols,
        right_symbols=right_symbols,
    )


def normalized_flat_point_type() -> SpecializedType:
    """Return the Chapter 22 example type: stored e_i^inf plus constant o^inf."""

    return SpecializedType(
        "normalized_flat_point",
        stored=(17, 18, 20),
        constants={24: 1.0},
        note="three stored direction-at-infinity coordinates plus constant o^inf",
    )


def dual_plane_type() -> SpecializedType:
    """Return a small dual-plane stand-in with Euclidean normal coordinates."""

    return SpecializedType("dual_plane", stored=(1, 2, 4), note="normal coordinates")


def line_from_flat_point_plane_type() -> SpecializedType:
    """Return the six-coordinate output type for the notebook kernel."""

    return SpecializedType(
        "line_from_flat_point_plane",
        stored=(19, 21, 22, 25, 26, 28),
        note="three direction moments and three constant-coordinate terms",
    )


def flat_point_terms(coordinates: Sequence[float]) -> dict[int, float]:
    """Sparse terms for the normalized flat-point stand-in."""

    return normalized_flat_point_type().sparse_terms(coordinates)


def dual_plane_terms(coordinates: Sequence[float]) -> dict[int, float]:
    """Sparse terms for the dual-plane stand-in."""

    return dual_plane_type().sparse_terms(coordinates)


def flat_point_plane_direct(coordinates_x: Sequence[float], coordinates_y: Sequence[float]) -> np.ndarray:
    """Direct six-coordinate kernel for the flat-point/dual-plane outer product."""

    x0, x1, x2 = (float(value) for value in coordinates_x)
    y0, y1, y2 = (float(value) for value in coordinates_y)
    return np.array(
        [
            x1 * y0 - x0 * y1,
            x2 * y0 - x0 * y2,
            x2 * y1 - x1 * y2,
            y0,
            y1,
            y2,
        ],
        dtype=float,
    )


def flat_point_plane_dense_inputs(
    coordinates_x: Sequence[float],
    coordinates_y: Sequence[float],
    spec: AlgebraSpec,
) -> tuple[np.ndarray, np.ndarray]:
    """Return dense arrays for the flat-point/dual-plane example."""

    return (
        normalized_flat_point_type().dense_array(coordinates_x, spec),
        dual_plane_type().dense_array(coordinates_y, spec),
    )


def generic_outer_dense(left: Sequence[float], right: Sequence[float], dim: int) -> np.ndarray:
    """A deliberately generic dense outer product over all basis coordinates."""

    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.shape != right.shape or left.shape[0] != (1 << dim):
        raise ValueError("dense inputs must both have length 2**dim")
    result = np.zeros_like(left)
    for left_bitmap, left_value in enumerate(left):
        for right_bitmap, right_value in enumerate(right):
            if left_bitmap & right_bitmap:
                continue
            sign = reordering_sign(left_bitmap, right_bitmap)
            result[left_bitmap ^ right_bitmap] += sign * left_value * right_value
    return result


def benchmark_flatpoint_plane(
    spec: AlgebraSpec,
    *,
    samples: int = 1200,
    seed: int = 22,
) -> list[dict[str, float | str]]:
    """Time dense, sparse, and direct kernels for the same outer product."""

    rng = np.random.default_rng(seed)
    xs = rng.normal(size=(samples, 3))
    ys = rng.normal(size=(samples, 3))
    dense_inputs = [flat_point_plane_dense_inputs(x, y, spec) for x, y in zip(xs, ys)]
    sparse_inputs = [(flat_point_terms(x), dual_plane_terms(y)) for x, y in zip(xs, ys)]
    output_bitmaps = line_from_flat_point_plane_type().stored

    def time_call(label: str, fn: Callable[[], float]) -> dict[str, float | str]:
        start = perf_counter()
        checksum = fn()
        elapsed = perf_counter() - start
        return {"kernel": label, "seconds": elapsed, "checksum": checksum}

    def dense_work() -> float:
        checksum = 0.0
        for left, right in dense_inputs:
            result = generic_outer_dense(left, right, spec.dim)
            checksum += float(np.sum(result[list(output_bitmaps)]))
        return checksum

    def sparse_work() -> float:
        checksum = 0.0
        for left, right in sparse_inputs:
            result = outer_product_terms(left, right)
            checksum += float(sum(result.get(bitmap, 0.0) for bitmap in output_bitmaps))
        return checksum

    def direct_work() -> float:
        checksum = 0.0
        for x, y in zip(xs, ys):
            checksum += float(np.sum(flat_point_plane_direct(x, y)))
        return checksum

    rows = [
        time_call("dense generic 32x32 loop", dense_work),
        time_call("sparse generic active loop", sparse_work),
        time_call("specialized direct kernel", direct_work),
    ]
    fastest = min(float(row["seconds"]) for row in rows)
    for row in rows:
        row["relative_to_fastest"] = float(row["seconds"]) / fastest
        row["samples"] = samples
    return rows


def normalize_vector(vector: Sequence[float]) -> np.ndarray:
    """Return a unit vector."""

    vector = np.asarray(vector, dtype=float)
    norm = float(np.linalg.norm(vector))
    if norm <= EPS:
        raise ValueError("cannot normalize a zero vector")
    return vector / norm


def rotor_from_axis_angle(axis: Sequence[float], angle: float) -> np.ndarray:
    """Return quaternion-style rotor coefficients [s, x, y, z]."""

    axis = normalize_vector(axis)
    half = 0.5 * float(angle)
    return np.concatenate(([cos(half)], axis * sin(half)))


def quaternion_multiply(left: Sequence[float], right: Sequence[float]) -> np.ndarray:
    """Multiply quaternion-style rotor coefficients."""

    a0, a1, a2, a3 = (float(value) for value in left)
    b0, b1, b2, b3 = (float(value) for value in right)
    return np.array(
        [
            a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0,
        ],
        dtype=float,
    )


def quaternion_conjugate(rotor: Sequence[float]) -> np.ndarray:
    """Return the reverse/conjugate of quaternion-style rotor coefficients."""

    rotor = np.asarray(rotor, dtype=float)
    return np.array([rotor[0], -rotor[1], -rotor[2], -rotor[3]], dtype=float)


def rotate_vector_by_rotor(vector: Sequence[float], rotor: Sequence[float]) -> np.ndarray:
    """Rotate a 3-D vector by a unit rotor."""

    vector_quaternion = np.concatenate(([0.0], np.asarray(vector, dtype=float)))
    rotated = quaternion_multiply(
        quaternion_multiply(rotor, vector_quaternion),
        quaternion_conjugate(rotor),
    )
    return rotated[1:]


def rotor_to_matrix(rotor: Sequence[float]) -> np.ndarray:
    """Build the grade-1 outermorphism matrix induced by a rotor."""

    basis = np.eye(3)
    return np.column_stack([rotate_vector_by_rotor(basis[:, index], rotor) for index in range(3)])


def rotate_points_by_rotor(points: np.ndarray, rotor: Sequence[float]) -> np.ndarray:
    """Rotate many points by repeated rotor application."""

    return np.vstack([rotate_vector_by_rotor(point, rotor) for point in np.asarray(points, dtype=float)])


def exterior_power_matrix(matrix: np.ndarray, grade: int) -> np.ndarray:
    """Return the matrix of the induced outermorphism on k-blades."""

    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be square")
    if grade < 0 or grade > matrix.shape[0]:
        raise ValueError("grade must be between 0 and the matrix dimension")
    combos = list(combinations(range(matrix.shape[0]), grade))
    if grade == 0:
        return np.ones((1, 1), dtype=float)
    result = np.zeros((len(combos), len(combos)), dtype=float)
    for row_index, row_combo in enumerate(combos):
        for col_index, col_combo in enumerate(combos):
            minor = matrix[np.ix_(row_combo, col_combo)]
            result[row_index, col_index] = float(np.linalg.det(minor))
    return result


def wedge_coordinates(*vectors: Sequence[float]) -> np.ndarray:
    """Return coordinates of the outer product of input vectors."""

    if not vectors:
        return np.array([1.0])
    matrix = np.column_stack([np.asarray(vector, dtype=float) for vector in vectors])
    dim, grade = matrix.shape
    values = []
    for rows in combinations(range(dim), grade):
        values.append(float(np.linalg.det(matrix[np.ix_(rows, range(grade))])))
    return np.asarray(values, dtype=float)


def rotor_terms_from_bivector_coefficients(
    scalar: float,
    e12: float,
    e13: float,
    e23: float,
) -> dict[int, float]:
    """Return even 3-D multivector terms from scalar and bivector coefficients."""

    return simplify_terms({0: scalar, 3: e12, 5: e13, 6: e23})


def versor_inverse(terms: Mapping[int, float], spec: AlgebraSpec) -> dict[int, float]:
    """Invert a versor-like multivector by reverse divided by scalar norm."""

    reverse = reverse_terms(terms)
    denominator = geometric_product_terms(terms, reverse, spec)
    nonscalar = {bitmap: value for bitmap, value in denominator.items() if bitmap != 0}
    if nonscalar:
        raise ValueError("reverse product was not scalar; value is not versor-like here")
    scalar = denominator.get(0, 0.0)
    if abs(scalar) <= EPS:
        raise ZeroDivisionError("versor norm is zero")
    return scale_terms(reverse, 1.0 / scalar)


def multivector_power(
    terms: Mapping[int, float],
    exponent: int,
    spec: AlgebraSpec,
) -> dict[int, float]:
    """Raise a sparse multivector to a nonnegative integer power."""

    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    result: dict[int, float] = {0: 1.0}
    for _ in range(exponent):
        result = geometric_product_terms(result, terms, spec)
    return result


def exp_series(
    terms: Mapping[int, float],
    spec: AlgebraSpec,
    *,
    order: int = 16,
) -> dict[int, float]:
    """Compute a truncated exponential series for a sparse multivector."""

    result: dict[int, float] = {}
    power: dict[int, float] = {0: 1.0}
    factorial = 1.0
    for k in range(order + 1):
        if k > 0:
            power = geometric_product_terms(power, terms, spec)
            factorial *= k
        result = add_terms(result, scale_terms(power, 1.0 / factorial))
    return simplify_terms(result)


def bivector_exp_closed_form(
    bivector: Mapping[int, float],
    spec: AlgebraSpec,
) -> dict[int, float]:
    """Use the scalar-square special case for the exponential of a bivector."""

    square = geometric_product_terms(bivector, bivector, spec)
    nonscalar = {bitmap: value for bitmap, value in square.items() if bitmap != 0}
    if nonscalar:
        raise ValueError("closed form requires the square to be scalar")
    scalar_square = square.get(0, 0.0)
    if scalar_square > EPS:
        raise ValueError("this helper handles bivectors with negative scalar square")
    theta = sqrt(max(0.0, -scalar_square))
    if theta <= EPS:
        return add_terms({0: 1.0}, bivector)
    return add_terms({0: cos(theta)}, scale_terms(bivector, sin(theta) / theta))


def max_term_error(left: Mapping[int, float], right: Mapping[int, float]) -> float:
    """Return the largest coefficient difference between two sparse multivectors."""

    bitmaps = set(left).union(right)
    if not bitmaps:
        return 0.0
    return max(abs(float(left.get(bitmap, 0.0)) - float(right.get(bitmap, 0.0))) for bitmap in bitmaps)
