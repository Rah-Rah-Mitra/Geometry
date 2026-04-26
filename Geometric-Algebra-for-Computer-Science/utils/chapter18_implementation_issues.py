"""Helpers for the Chapter 18 implementation-issues notebook.

The module deliberately uses a small orthonormal geometric algebra engine rather
than a full library.  Its purpose is inspectability: every coordinate encoding,
matrix representation, and product check in the notebook can be traced to a few
plain Python functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from pathlib import Path
from typing import Iterable, Mapping

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

EPS = 1e-10

COLORS = {
    "blue": "#2f6fbb",
    "orange": "#d9822b",
    "green": "#348f50",
    "red": "#c43c39",
    "purple": "#7a4db3",
    "gray": "#6b7280",
    "faint": "rgba(80, 80, 80, 0.22)",
}


def grade(mask: int) -> int:
    """Return the grade of a basis blade encoded as a bit mask."""
    return int(mask).bit_count()


def basis_masks(dimension: int) -> list[int]:
    """Return all basis-blade masks for an ``n``-dimensional vector space."""
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    return list(range(1 << dimension))


def mask_to_name(mask: int, names: Iterable[str] | None = None) -> str:
    """Return a compact ASCII name for a basis-blade bit mask."""
    mask = int(mask)
    if mask == 0:
        return "1"
    if names is None:
        names = [f"e{i + 1}" for i in range(max(mask.bit_length(), 1))]
    names = list(names)
    parts = [names[i] for i in range(len(names)) if mask & (1 << i)]
    return "".join(parts)


def _reordering_sign(left_mask: int, right_mask: int) -> float:
    """Return the sign from canonicalizing two basis-blade bit patterns."""
    swaps = 0
    right = int(right_mask)
    for bit in range(int(left_mask).bit_length()):
        if left_mask & (1 << bit):
            swaps += (right & ((1 << bit) - 1)).bit_count()
    return -1.0 if swaps % 2 else 1.0


def blade_product(left_mask: int, right_mask: int, signature: Iterable[float]) -> tuple[float, int]:
    """Multiply two orthonormal basis blades.

    Basis blades are encoded as bit masks.  The duplicate basis vectors disappear
    by the metric square in ``signature``; the remaining mask is an XOR.
    """
    signature = tuple(float(v) for v in signature)
    left_mask = int(left_mask)
    right_mask = int(right_mask)
    sign = _reordering_sign(left_mask, right_mask)
    common = left_mask & right_mask
    metric_factor = 1.0
    for bit, square in enumerate(signature):
        if common & (1 << bit):
            metric_factor *= square
    return sign * metric_factor, left_mask ^ right_mask


@dataclass(frozen=True)
class OrthonormalAlgebra:
    """A tiny coordinate model for an orthonormal geometric algebra."""

    signature: tuple[float, ...]
    names: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        signature = tuple(float(v) for v in self.signature)
        if any(abs(v) <= EPS for v in signature):
            raise ValueError("basis-vector squares must be nonzero")
        object.__setattr__(self, "signature", signature)
        if self.names is None:
            object.__setattr__(self, "names", tuple(f"e{i + 1}" for i in range(len(signature))))
        else:
            names = tuple(self.names)
            if len(names) != len(signature):
                raise ValueError("names and signature must have the same length")
            object.__setattr__(self, "names", names)

    @property
    def dimension(self) -> int:
        """Return the vector-space dimension."""
        return len(self.signature)

    @property
    def size(self) -> int:
        """Return the dense multivector coordinate length."""
        return 1 << self.dimension

    @property
    def blade_names(self) -> list[str]:
        """Return names for all basis blades in dense coordinate order."""
        return [mask_to_name(mask, self.names) for mask in basis_masks(self.dimension)]

    def blade_product(self, left_mask: int, right_mask: int) -> tuple[float, int]:
        """Multiply two basis blades in this algebra."""
        return blade_product(left_mask, right_mask, self.signature)

    def scalar(self, value: float) -> np.ndarray:
        """Return a dense scalar multivector."""
        result = np.zeros(self.size, dtype=float)
        result[0] = float(value)
        return result

    def vector(self, coordinates: Iterable[float]) -> np.ndarray:
        """Encode a vector as a dense grade-1 multivector."""
        coordinates = np.asarray(coordinates, dtype=float)
        if coordinates.shape != (self.dimension,):
            raise ValueError("coordinates must match the vector-space dimension")
        result = np.zeros(self.size, dtype=float)
        for bit, value in enumerate(coordinates):
            result[1 << bit] = value
        return result

    def dense(self, coefficients: Iterable[float]) -> np.ndarray:
        """Return a validated dense multivector coordinate array."""
        coefficients = np.asarray(coefficients, dtype=float)
        if coefficients.shape != (self.size,):
            raise ValueError(f"expected {self.size} coefficients")
        return coefficients

    def dense_product(self, left: Iterable[float], right: Iterable[float]) -> np.ndarray:
        """Return the geometric product of two dense multivectors."""
        left = self.dense(left)
        right = self.dense(right)
        result = np.zeros(self.size, dtype=float)
        for left_mask, left_value in enumerate(left):
            if abs(left_value) <= EPS:
                continue
            for right_mask, right_value in enumerate(right):
                if abs(right_value) <= EPS:
                    continue
                factor, result_mask = self.blade_product(left_mask, right_mask)
                result[result_mask] += left_value * right_value * factor
        return result

    def outer_product(self, left: Iterable[float], right: Iterable[float]) -> np.ndarray:
        """Return the outer product of two dense multivectors."""
        left = self.dense(left)
        right = self.dense(right)
        result = np.zeros(self.size, dtype=float)
        for left_mask, left_value in enumerate(left):
            if abs(left_value) <= EPS:
                continue
            for right_mask, right_value in enumerate(right):
                if abs(right_value) <= EPS or (left_mask & right_mask):
                    continue
                factor, result_mask = self.blade_product(left_mask, right_mask)
                result[result_mask] += left_value * right_value * factor
        return result

    def grade_projection(self, value: Iterable[float], target_grade: int) -> np.ndarray:
        """Keep only coordinates of one grade."""
        value = self.dense(value)
        result = np.zeros_like(value)
        for mask, coefficient in enumerate(value):
            if grade(mask) == target_grade:
                result[mask] = coefficient
        return result

    def reverse(self, value: Iterable[float]) -> np.ndarray:
        """Return the reversion anti-involution."""
        value = self.dense(value)
        result = np.zeros_like(value)
        for mask, coefficient in enumerate(value):
            g = grade(mask)
            result[mask] = ((-1.0) ** (g * (g - 1) // 2)) * coefficient
        return result

    def norm_squared(self, value: Iterable[float]) -> float:
        """Return the scalar part of ``value * reverse(value)``."""
        return float(self.dense_product(value, self.reverse(value))[0])

    def dense_to_sparse(self, value: Iterable[float], *, tol: float = EPS) -> dict[int, float]:
        """Encode a dense multivector as a sparse mask-to-coefficient dictionary."""
        value = self.dense(value)
        return {mask: float(coefficient) for mask, coefficient in enumerate(value) if abs(coefficient) > tol}

    def sparse_to_dense(self, value: Mapping[int, float]) -> np.ndarray:
        """Encode a sparse mask-to-coefficient dictionary as dense coordinates."""
        result = np.zeros(self.size, dtype=float)
        for mask, coefficient in value.items():
            if not 0 <= int(mask) < self.size:
                raise ValueError("sparse mask is outside this algebra")
            result[int(mask)] += float(coefficient)
        return result

    def sparse_product(
        self,
        left: Mapping[int, float],
        right: Mapping[int, float],
        *,
        tol: float = EPS,
    ) -> dict[int, float]:
        """Return the geometric product of two sparse multivectors."""
        result: dict[int, float] = {}
        for left_mask, left_value in left.items():
            if abs(left_value) <= tol:
                continue
            for right_mask, right_value in right.items():
                if abs(right_value) <= tol:
                    continue
                factor, result_mask = self.blade_product(left_mask, right_mask)
                result[result_mask] = result.get(result_mask, 0.0) + left_value * right_value * factor
        return {mask: value for mask, value in result.items() if abs(value) > tol}

    def format_multivector(self, value: Iterable[float], *, tol: float = 1e-9) -> str:
        """Return a readable coordinate expression."""
        value = self.dense(value)
        terms = []
        for mask, coefficient in enumerate(value):
            if abs(coefficient) <= tol:
                continue
            name = mask_to_name(mask, self.names)
            if mask == 0:
                terms.append(f"{coefficient:.4g}")
            else:
                terms.append(f"{coefficient:.4g} {name}")
        return "0" if not terms else " + ".join(terms).replace("+ -", "- ")


@dataclass(frozen=True)
class FactoredBlade:
    """A blade stored by the vectors whose outer product it represents."""

    factors: np.ndarray

    def __post_init__(self) -> None:
        factors = np.asarray(self.factors, dtype=float)
        if factors.ndim != 2:
            raise ValueError("factors must be a 2-D array")
        object.__setattr__(self, "factors", factors)

    @property
    def grade(self) -> int:
        """Return the number of vector factors."""
        return self.factors.shape[0]

    @property
    def dimension(self) -> int:
        """Return the vector-space dimension."""
        return self.factors.shape[1]

    @property
    def storage_size(self) -> int:
        """Return the number of stored scalar coordinates."""
        return int(self.factors.size)

    def expanded_sparse(self, *, tol: float = EPS) -> dict[int, float]:
        """Expand the factored blade into sparse basis-blade coordinates."""
        return wedge_vectors(self.factors, tol=tol)


def wedge_vectors(vectors: Iterable[Iterable[float]], *, tol: float = EPS) -> dict[int, float]:
    """Expand the outer product of vectors into sparse basis-blade coordinates."""
    vectors = np.asarray(vectors, dtype=float)
    if vectors.ndim != 2:
        raise ValueError("vectors must be a 2-D array")
    k, n = vectors.shape
    if k > n:
        return {}
    if k == 0:
        return {0: 1.0}

    result: dict[int, float] = {}
    for mask in basis_masks(n):
        if grade(mask) != k:
            continue
        columns = [bit for bit in range(n) if mask & (1 << bit)]
        coefficient = float(np.linalg.det(vectors[:, columns]))
        if abs(coefficient) > tol:
            result[mask] = coefficient
    return result


def storage_profile(max_dimension: int = 12, blade_grade: int = 2) -> list[dict[str, int]]:
    """Return a dense/sparse/factored storage profile for simple comparison."""
    rows: list[dict[str, int]] = []
    for n in range(1, max_dimension + 1):
        grade_count = comb(n, blade_grade) if 0 <= blade_grade <= n else 0
        rows.append(
            {
                "dimension": n,
                "dense_multivector": 1 << n,
                "single_grade": grade_count,
                "factored_blade": blade_grade * n if blade_grade <= n else 0,
            }
        )
    return rows


def operation_profile(algebra: OrthonormalAlgebra, left: Iterable[float], right: Iterable[float]) -> dict[str, int]:
    """Return simple operation counts for dense and sparse multiplication loops."""
    left = algebra.dense(left)
    right = algebra.dense(right)
    left_nonzero = int(np.count_nonzero(np.abs(left) > EPS))
    right_nonzero = int(np.count_nonzero(np.abs(right) > EPS))
    return {
        "dense_basis_pairs": algebra.size * algebra.size,
        "sparse_basis_pairs": left_nonzero * right_nonzero,
        "left_nonzero": left_nonzero,
        "right_nonzero": right_nonzero,
    }


def ga2_matrix_basis() -> dict[int, np.ndarray]:
    """Return the real 2-by-2 matrix basis for Euclidean Cl(2,0)."""
    e1 = np.array([[0.0, 1.0], [1.0, 0.0]])
    e2 = np.array([[1.0, 0.0], [0.0, -1.0]])
    return {
        0: np.eye(2),
        1: e1,
        2: e2,
        3: e1 @ e2,
    }


def ga2_to_matrix(coefficients: Iterable[float]) -> np.ndarray:
    """Map a Cl(2,0) multivector to its real 2-by-2 matrix representative."""
    coefficients = np.asarray(coefficients, dtype=float)
    if coefficients.shape != (4,):
        raise ValueError("Cl(2,0) has four dense coefficients")
    basis = ga2_matrix_basis()
    matrix = np.zeros((2, 2), dtype=float)
    for mask, coefficient in enumerate(coefficients):
        matrix += coefficient * basis[mask]
    return matrix


def matrix_to_ga2(matrix: Iterable[Iterable[float]]) -> np.ndarray:
    """Decode the real 2-by-2 Cl(2,0) matrix representative."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (2, 2):
        raise ValueError("expected a 2-by-2 matrix")
    x0 = 0.5 * (matrix[0, 0] + matrix[1, 1])
    x1 = 0.5 * (matrix[0, 1] + matrix[1, 0])
    x2 = 0.5 * (matrix[0, 0] - matrix[1, 1])
    x12 = 0.5 * (matrix[1, 0] - matrix[0, 1])
    return np.array([x0, x1, x2, x12], dtype=float)


def ga2_inverse_via_matrix(coefficients: Iterable[float]) -> np.ndarray:
    """Invert a Cl(2,0) multivector by decoding the inverse matrix."""
    return matrix_to_ga2(np.linalg.inv(ga2_to_matrix(coefficients)))


def ga3_complex_matrix_basis() -> dict[int, np.ndarray]:
    """Return the complex 2-by-2 matrix basis for Euclidean Cl(3,0)."""
    e1 = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    e2 = np.array([[0.0, 1.0j], [-1.0j, 0.0]], dtype=complex)
    e3 = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    vectors = {1: e1, 2: e2, 4: e3}
    basis: dict[int, np.ndarray] = {0: np.eye(2, dtype=complex)}
    for mask in range(1, 8):
        matrix = np.eye(2, dtype=complex)
        for bit in range(3):
            if mask & (1 << bit):
                matrix = matrix @ vectors[1 << bit]
        basis[mask] = matrix
    return basis


def ga3_to_complex_matrix(coefficients: Iterable[float]) -> np.ndarray:
    """Map a Cl(3,0) multivector to the complex 2-by-2 representative."""
    coefficients = np.asarray(coefficients, dtype=float)
    if coefficients.shape != (8,):
        raise ValueError("Cl(3,0) has eight dense coefficients")
    basis = ga3_complex_matrix_basis()
    matrix = np.zeros((2, 2), dtype=complex)
    for mask, coefficient in enumerate(coefficients):
        matrix += coefficient * basis[mask]
    return matrix


def matrix_basis_product_error(algebra: OrthonormalAlgebra, matrix_basis: Mapping[int, np.ndarray]) -> float:
    """Return the maximum basis-product error for a matrix representation."""
    worst = 0.0
    for left_mask in basis_masks(algebra.dimension):
        for right_mask in basis_masks(algebra.dimension):
            factor, result_mask = algebra.blade_product(left_mask, right_mask)
            represented = matrix_basis[left_mask] @ matrix_basis[right_mask]
            expected = factor * matrix_basis[result_mask]
            worst = max(worst, float(np.linalg.norm(represented - expected)))
    return worst


def coefficient_bar_figure(
    algebra: OrthonormalAlgebra,
    value: Iterable[float],
    *,
    title: str,
) -> plt.Figure:
    """Build a compact coefficient bar chart."""
    value = algebra.dense(value)
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    colors = [COLORS["orange"] if abs(v) > EPS else "#d1d5db" for v in value]
    ax.bar(algebra.blade_names, value, color=colors)
    ax.axhline(0.0, color="#1f2937", linewidth=0.8)
    ax.set_title(title)
    ax.set_ylabel("coefficient")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    return fig


def save_coefficient_bar(
    path: Path,
    algebra: OrthonormalAlgebra,
    value: Iterable[float],
    *,
    title: str,
) -> Path:
    """Save a coefficient bar chart and return its path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig = coefficient_bar_figure(algebra, value, title=title)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def product_table_figure(algebra: OrthonormalAlgebra) -> go.Figure:
    """Return an interactive geometric-product table for basis blades."""
    names = algebra.blade_names
    values = np.zeros((algebra.size, algebra.size), dtype=float)
    labels: list[list[str]] = []
    for left_mask in range(algebra.size):
        label_row = []
        for right_mask in range(algebra.size):
            factor, result_mask = algebra.blade_product(left_mask, right_mask)
            values[left_mask, right_mask] = factor * (grade(result_mask) + 1)
            sign = "-" if factor < 0 else ""
            label_row.append(f"{names[left_mask]} * {names[right_mask]} = {sign}{names[result_mask]}")
        labels.append(label_row)
    fig = go.Figure(
        data=go.Heatmap(
            z=values,
            x=names,
            y=names,
            customdata=labels,
            colorscale=[
                [0.0, "#c43c39"],
                [0.5, "#f3f4f6"],
                [1.0, "#2f6fbb"],
            ],
            hovertemplate="%{customdata}<extra></extra>",
            showscale=False,
        )
    )
    fig.update_layout(
        title="Basis-blade geometric product table",
        width=720,
        height=640,
        xaxis_title="right factor",
        yaxis_title="left factor",
        margin={"l": 70, "r": 20, "t": 55, "b": 70},
    )
    return fig


def storage_profile_figure(profile: list[dict[str, int]]) -> go.Figure:
    """Return an interactive storage comparison figure."""
    dimensions = [row["dimension"] for row in profile]
    fig = go.Figure()
    for key, name, color in [
        ("dense_multivector", "dense multivector", COLORS["red"]),
        ("single_grade", "single-grade coordinates", COLORS["blue"]),
        ("factored_blade", "factored blade", COLORS["green"]),
    ]:
        fig.add_trace(
            go.Scatter(
                x=dimensions,
                y=[row[key] for row in profile],
                mode="lines+markers",
                name=name,
                line={"color": color, "width": 3},
            )
        )
    fig.update_layout(
        title="Storage choices change the shape of the problem",
        width=850,
        height=500,
        yaxis={"title": "stored scalar slots", "type": "log"},
        xaxis={"title": "vector-space dimension"},
        hovermode="x unified",
        margin={"l": 70, "r": 20, "t": 55, "b": 55},
    )
    return fig


def level_cost_figure(rows: list[dict[str, float]]) -> go.Figure:
    """Return a grouped bar chart for implementation-level cost signals."""
    labels = [row["level"] for row in rows]
    fig = go.Figure()
    for key, name, color in [
        ("setup_cost", "setup cost", COLORS["purple"]),
        ("runtime_cost", "runtime cost", COLORS["orange"]),
        ("algorithmic_specialization", "specialization pressure", COLORS["blue"]),
    ]:
        fig.add_trace(
            go.Bar(
                x=labels,
                y=[row[key] for row in rows],
                name=name,
                marker={"color": color},
            )
        )
    fig.update_layout(
        title="The four implementation levels pull on different costs",
        width=850,
        height=470,
        barmode="group",
        yaxis={"title": "relative score"},
        margin={"l": 70, "r": 20, "t": 55, "b": 80},
    )
    return fig


def sanity_checks() -> dict[str, float]:
    """Run numerical checks used by the notebook quality gate."""
    ga2 = OrthonormalAlgebra((1.0, 1.0))
    ga3 = OrthonormalAlgebra((1.0, 1.0, 1.0))
    rng = np.random.default_rng(18)
    a2 = rng.normal(size=4)
    b2 = rng.normal(size=4)
    a3 = rng.normal(size=8)
    b3 = rng.normal(size=8)
    gp2 = ga2.dense_product(a2, b2)
    gp3 = ga3.dense_product(a3, b3)
    sparse_product = ga3.sparse_to_dense(
        ga3.sparse_product(ga3.dense_to_sparse(a3), ga3.dense_to_sparse(b3))
    )
    vectors = rng.normal(size=(2, 4))
    wedge_sparse = wedge_vectors(vectors)
    ga4 = OrthonormalAlgebra((1.0, 1.0, 1.0, 1.0))
    wedge_dense = ga4.outer_product(ga4.vector(vectors[0]), ga4.vector(vectors[1]))
    inverse_candidate = np.array([1.2, 0.2, -0.1, 0.35])
    inverse = ga2_inverse_via_matrix(inverse_candidate)
    identity_error = np.linalg.norm(ga2.dense_product(inverse_candidate, inverse) - ga2.scalar(1.0))
    return {
        "ga2_matrix_product_error": float(np.linalg.norm(ga2_to_matrix(gp2) - ga2_to_matrix(a2) @ ga2_to_matrix(b2))),
        "ga2_basis_error": matrix_basis_product_error(ga2, ga2_matrix_basis()),
        "ga3_complex_product_error": float(
            np.linalg.norm(ga3_to_complex_matrix(gp3) - ga3_to_complex_matrix(a3) @ ga3_to_complex_matrix(b3))
        ),
        "ga3_basis_error": matrix_basis_product_error(ga3, ga3_complex_matrix_basis()),
        "dense_sparse_product_error": float(np.linalg.norm(gp3 - sparse_product)),
        "factored_outer_error": float(np.linalg.norm(ga4.sparse_to_dense(wedge_sparse) - wedge_dense)),
        "matrix_inverse_identity_error": float(identity_error),
        "storage_dense_n12": float(storage_profile(12, 2)[-1]["dense_multivector"]),
    }
