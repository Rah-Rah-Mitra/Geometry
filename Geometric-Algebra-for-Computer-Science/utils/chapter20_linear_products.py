"""Linear-product helpers for the Chapter 20 notebook.

The module keeps the implementation deliberately small and inspectable. Basis
blades are encoded as bit masks, multivectors are coordinate arrays in a chosen
basis order, and every product matrix is built from basis-blade structure
coefficients.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

EPS = 1e-10

COLORS = {
    "blue": "#2f6fbb",
    "orange": "#d9822b",
    "green": "#348f50",
    "red": "#c43c39",
    "purple": "#7a4db3",
    "gray": "#4b5563",
    "light": "#e5e7eb",
    "ink": "#111827",
}

PRODUCT_KINDS = {
    "geometric",
    "outer",
    "left_contraction",
    "right_contraction",
    "scalar",
    "commutator",
}


def grade(mask: int) -> int:
    """Return the grade of a basis blade encoded as a bit mask."""
    return int(mask).bit_count()


def basis_order(dimension: int) -> tuple[int, ...]:
    """Return basis masks ordered by grade and then by bitmap value."""
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    masks = range(1 << dimension)
    return tuple(sorted(masks, key=lambda value: (grade(value), value)))


def bitmap_indices(mask: int) -> tuple[int, ...]:
    """Return zero-based basis-vector indices present in ``mask``."""
    mask = int(mask)
    if mask < 0:
        raise ValueError("mask must be nonnegative")
    indices: list[int] = []
    cursor = mask
    while cursor:
        bit = cursor & -cursor
        indices.append(bit.bit_length() - 1)
        cursor ^= bit
    return tuple(indices)


def mask_to_label(mask: int, names: Sequence[str] | None = None) -> str:
    """Return a compact ASCII label such as ``e1e3`` for a basis blade."""
    mask = int(mask)
    if mask == 0:
        return "1"
    if names is None:
        names = tuple(f"e{i + 1}" for i in range(max(mask.bit_length(), 1)))
    parts = [names[index] for index in bitmap_indices(mask)]
    return "".join(parts)


def basis_table_rows(dimension: int, names: Sequence[str] | None = None) -> list[dict[str, object]]:
    """Return notebook-friendly rows describing every basis blade."""
    names = tuple(names) if names is not None else tuple(f"e{i + 1}" for i in range(dimension))
    return [
        {
            "index": index,
            "mask": mask,
            "binary": format(mask, f"0{dimension}b"),
            "grade": grade(mask),
            "label": mask_to_label(mask, names),
        }
        for index, mask in enumerate(basis_order(dimension))
    ]


def _validate_mask(mask: int, dimension: int) -> int:
    mask = int(mask)
    if not 0 <= mask < (1 << dimension):
        raise ValueError("basis-blade mask is outside this algebra")
    return mask


def _add_term(terms: dict[int, float], mask: int, coefficient: float, *, tol: float = EPS) -> None:
    if abs(coefficient) <= tol:
        return
    updated = terms.get(int(mask), 0.0) + float(coefficient)
    if abs(updated) <= tol:
        terms.pop(int(mask), None)
    else:
        terms[int(mask)] = updated


def simplify_terms(terms: Mapping[int, float], *, tol: float = EPS) -> dict[int, float]:
    """Merge duplicate masks and remove tiny coefficients."""
    simplified: dict[int, float] = {}
    for mask, coefficient in terms.items():
        if int(mask) < 0:
            raise ValueError("term masks must be nonnegative")
        _add_term(simplified, int(mask), float(coefficient), tol=tol)
    return simplified


def vector_left_product_terms(
    index: int,
    terms: Mapping[int, float],
    metric: np.ndarray,
    *,
    tol: float = EPS,
) -> dict[int, float]:
    """Left-multiply a sparse multivector by one basis vector."""
    metric = np.asarray(metric, dtype=float)
    if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
        raise ValueError("metric must be a square matrix")
    if not 0 <= int(index) < metric.shape[0]:
        raise ValueError("basis-vector index is outside the metric")

    result: dict[int, float] = {}
    bit = 1 << int(index)
    for mask, coefficient in simplify_terms(terms, tol=tol).items():
        _validate_mask(mask, metric.shape[0])

        if not (mask & bit):
            lower_count = (mask & (bit - 1)).bit_count()
            outer_sign = -1.0 if lower_count % 2 else 1.0
            _add_term(result, mask | bit, coefficient * outer_sign, tol=tol)

        for position, basis_index in enumerate(bitmap_indices(mask)):
            metric_value = float(metric[index, basis_index])
            if abs(metric_value) <= tol:
                continue
            contraction_sign = -1.0 if position % 2 else 1.0
            _add_term(
                result,
                mask ^ (1 << basis_index),
                coefficient * contraction_sign * metric_value,
                tol=tol,
            )
    return result


def basis_blade_geometric_product_terms(
    left_mask: int,
    right_mask: int,
    metric: np.ndarray,
    *,
    tol: float = EPS,
) -> dict[int, float]:
    """Return the geometric product of two basis blades as sparse terms."""
    metric = np.asarray(metric, dtype=float)
    if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
        raise ValueError("metric must be a square matrix")
    if not np.allclose(metric, metric.T, atol=tol):
        raise ValueError("metric must be symmetric")
    left_mask = _validate_mask(left_mask, metric.shape[0])
    right_mask = _validate_mask(right_mask, metric.shape[0])

    terms: dict[int, float] = {right_mask: 1.0}
    for index in reversed(bitmap_indices(left_mask)):
        terms = vector_left_product_terms(index, terms, metric, tol=tol)
    return simplify_terms(terms, tol=tol)


def grade_project_terms(
    terms: Mapping[int, float],
    target_grade: int,
    *,
    tol: float = EPS,
) -> dict[int, float]:
    """Keep only sparse terms of one grade."""
    if target_grade < 0:
        return {}
    return simplify_terms(
        {mask: coefficient for mask, coefficient in terms.items() if grade(mask) == target_grade},
        tol=tol,
    )


def product_terms(
    left_mask: int,
    right_mask: int,
    metric: np.ndarray,
    *,
    kind: str = "geometric",
    tol: float = EPS,
) -> dict[int, float]:
    """Return one basis-blade product, optionally with grade selection."""
    if kind not in PRODUCT_KINDS:
        raise ValueError(f"unknown product kind: {kind}")

    left_grade = grade(left_mask)
    right_grade = grade(right_mask)
    if kind == "commutator":
        ab = basis_blade_geometric_product_terms(left_mask, right_mask, metric, tol=tol)
        ba = basis_blade_geometric_product_terms(right_mask, left_mask, metric, tol=tol)
        result: dict[int, float] = {}
        for mask, coefficient in ab.items():
            _add_term(result, mask, 0.5 * coefficient, tol=tol)
        for mask, coefficient in ba.items():
            _add_term(result, mask, -0.5 * coefficient, tol=tol)
        return simplify_terms(result, tol=tol)

    gp = basis_blade_geometric_product_terms(left_mask, right_mask, metric, tol=tol)
    if kind == "geometric":
        return gp
    if kind == "outer":
        return grade_project_terms(gp, left_grade + right_grade, tol=tol)
    if kind == "left_contraction":
        if left_grade > right_grade:
            return {}
        return grade_project_terms(gp, right_grade - left_grade, tol=tol)
    if kind == "right_contraction":
        if left_grade < right_grade:
            return {}
        return grade_project_terms(gp, left_grade - right_grade, tol=tol)
    return grade_project_terms(gp, 0, tol=tol)


def format_terms(
    terms: Mapping[int, float],
    names: Sequence[str] | None = None,
    *,
    precision: int = 3,
    tol: float = EPS,
) -> str:
    """Format sparse multivector terms for compact notebook tables."""
    simplified = simplify_terms(terms, tol=tol)
    if not simplified:
        return "0"

    pieces: list[tuple[str, str]] = []
    for mask in sorted(simplified, key=lambda value: (grade(value), value)):
        coefficient = simplified[mask]
        label = mask_to_label(mask, names)
        magnitude = abs(coefficient)
        if abs(magnitude - 1.0) <= 10 ** (-precision) and label != "1":
            body = label
        else:
            body = f"{magnitude:.{precision}g}"
            if label != "1":
                body = f"{body} {label}"
        pieces.append(("-" if coefficient < 0 else "+", body))

    first_sign, first_body = pieces[0]
    output = first_body if first_sign == "+" else f"-{first_body}"
    for sign, body in pieces[1:]:
        output += f" {sign} {body}"
    return output


def _json_safe(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json_safe(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value


@dataclass(frozen=True)
class LinearProductAlgebra:
    """Coordinate model for constructing linear GA product matrices."""

    metric: Sequence[Sequence[float]] | np.ndarray
    names: tuple[str, ...] | None = None
    order: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        metric = np.asarray(self.metric, dtype=float)
        if metric.ndim != 2 or metric.shape[0] != metric.shape[1]:
            raise ValueError("metric must be a square matrix")
        if not np.allclose(metric, metric.T, atol=EPS):
            raise ValueError("metric must be symmetric")
        dimension = int(metric.shape[0])
        names = self.names if self.names is not None else tuple(f"e{i + 1}" for i in range(dimension))
        if len(names) != dimension:
            raise ValueError("names must match the metric dimension")
        order = self.order if self.order is not None else basis_order(dimension)
        if tuple(sorted(order)) != tuple(range(1 << dimension)):
            raise ValueError("order must contain every basis-blade mask exactly once")

        object.__setattr__(self, "metric", metric)
        object.__setattr__(self, "names", tuple(names))
        object.__setattr__(self, "order", tuple(int(mask) for mask in order))
        object.__setattr__(self, "_index_by_mask", {mask: i for i, mask in enumerate(order)})

    @classmethod
    def from_signature(
        cls,
        signature: Iterable[float],
        names: tuple[str, ...] | None = None,
    ) -> "LinearProductAlgebra":
        """Build an algebra from diagonal basis-vector squares."""
        signature = tuple(float(value) for value in signature)
        return cls(np.diag(signature), names=names)

    @property
    def dimension(self) -> int:
        """Return the vector-space dimension."""
        return int(self.metric.shape[0])

    @property
    def size(self) -> int:
        """Return the dense coordinate count."""
        return 1 << self.dimension

    @property
    def blade_names(self) -> list[str]:
        """Return basis-blade labels in dense coordinate order."""
        return [mask_to_label(mask, self.names) for mask in self.order]

    @property
    def grades(self) -> list[int]:
        """Return basis-blade grades in dense coordinate order."""
        return [grade(mask) for mask in self.order]

    def index(self, mask: int) -> int:
        """Return the dense coordinate index for a basis-blade mask."""
        return int(self._index_by_mask[_validate_mask(mask, self.dimension)])

    def dense(self, coefficients: Iterable[float]) -> np.ndarray:
        """Return a validated dense coordinate vector."""
        coefficients = np.asarray(coefficients, dtype=float)
        if coefficients.shape != (self.size,):
            raise ValueError(f"expected {self.size} coefficients")
        return coefficients

    def scalar(self, value: float) -> np.ndarray:
        """Return a scalar multivector."""
        result = np.zeros(self.size, dtype=float)
        result[self.index(0)] = float(value)
        return result

    def basis_dense(self, mask: int, coefficient: float = 1.0) -> np.ndarray:
        """Return one weighted basis blade as a dense vector."""
        result = np.zeros(self.size, dtype=float)
        result[self.index(mask)] = float(coefficient)
        return result

    def vector(self, coordinates: Iterable[float]) -> np.ndarray:
        """Encode vector coordinates as a dense multivector."""
        coordinates = np.asarray(coordinates, dtype=float)
        if coordinates.shape != (self.dimension,):
            raise ValueError("vector coordinates must match the dimension")
        result = np.zeros(self.size, dtype=float)
        for basis_index, value in enumerate(coordinates):
            result[self.index(1 << basis_index)] = value
        return result

    def dense_to_sparse(self, value: Iterable[float], *, tol: float = EPS) -> dict[int, float]:
        """Convert dense coordinates to a sparse mask-to-coefficient dictionary."""
        value = self.dense(value)
        return {
            mask: float(value[index])
            for index, mask in enumerate(self.order)
            if abs(float(value[index])) > tol
        }

    def sparse_to_dense(self, terms: Mapping[int, float], *, tol: float = EPS) -> np.ndarray:
        """Convert sparse mask-to-coefficient terms into dense coordinates."""
        result = np.zeros(self.size, dtype=float)
        for mask, coefficient in simplify_terms(terms, tol=tol).items():
            result[self.index(mask)] += coefficient
        return result

    def basis_product_terms(
        self,
        left_mask: int,
        right_mask: int,
        *,
        kind: str = "geometric",
        tol: float = EPS,
    ) -> dict[int, float]:
        """Return one basis-blade product in this algebra."""
        return product_terms(left_mask, right_mask, self.metric, kind=kind, tol=tol)

    def sparse_product(
        self,
        left: Mapping[int, float],
        right: Mapping[int, float],
        *,
        kind: str = "geometric",
        tol: float = EPS,
    ) -> dict[int, float]:
        """Distribute a linear product over sparse multivectors."""
        result: dict[int, float] = {}
        left = simplify_terms(left, tol=tol)
        right = simplify_terms(right, tol=tol)
        for left_mask, left_coefficient in left.items():
            _validate_mask(left_mask, self.dimension)
            for right_mask, right_coefficient in right.items():
                _validate_mask(right_mask, self.dimension)
                terms = self.basis_product_terms(left_mask, right_mask, kind=kind, tol=tol)
                for result_mask, product_coefficient in terms.items():
                    _add_term(
                        result,
                        result_mask,
                        left_coefficient * right_coefficient * product_coefficient,
                        tol=tol,
                    )
        return simplify_terms(result, tol=tol)

    def dense_product(
        self,
        left: Iterable[float],
        right: Iterable[float],
        *,
        kind: str = "geometric",
        tol: float = EPS,
    ) -> np.ndarray:
        """Compute a linear product from dense coordinates using sparse distribution."""
        return self.sparse_to_dense(
            self.sparse_product(
                self.dense_to_sparse(left, tol=tol),
                self.dense_to_sparse(right, tol=tol),
                kind=kind,
                tol=tol,
            ),
            tol=tol,
        )

    def left_operator_matrix(
        self,
        left: Iterable[float],
        *,
        kind: str = "geometric",
        tol: float = EPS,
    ) -> np.ndarray:
        """Return matrix ``M`` such that ``M @ B`` equals ``left product B``."""
        left_sparse = self.dense_to_sparse(left, tol=tol)
        matrix = np.zeros((self.size, self.size), dtype=float)
        for column, right_mask in enumerate(self.order):
            column_terms = self.sparse_product(left_sparse, {right_mask: 1.0}, kind=kind, tol=tol)
            for result_mask, coefficient in column_terms.items():
                matrix[self.index(result_mask), column] += coefficient
        return matrix

    def grade_projection_matrix(self, target_grade: int) -> np.ndarray:
        """Return the diagonal matrix that keeps one grade."""
        diagonal = [1.0 if grade(mask) == target_grade else 0.0 for mask in self.order]
        return np.diag(diagonal)

    def unary_sign_matrix(self, operation: str) -> np.ndarray:
        """Return the diagonal matrix for a grade-dependent unary operation."""
        signs: list[float] = []
        for mask in self.order:
            blade_grade = grade(mask)
            if operation == "reversion":
                exponent = blade_grade * (blade_grade - 1) // 2
            elif operation == "grade_involution":
                exponent = blade_grade
            elif operation == "clifford_conjugation":
                exponent = blade_grade * (blade_grade + 1) // 2
            else:
                raise ValueError(f"unknown unary operation: {operation}")
            signs.append(-1.0 if exponent % 2 else 1.0)
        return np.diag(signs)

    def project_grade(self, value: Iterable[float], target_grade: int) -> np.ndarray:
        """Keep only the coordinates of one grade."""
        return self.grade_projection_matrix(target_grade) @ self.dense(value)

    def reverse(self, value: Iterable[float]) -> np.ndarray:
        """Return the reversion of a dense multivector."""
        return self.unary_sign_matrix("reversion") @ self.dense(value)

    def grade_involution(self, value: Iterable[float]) -> np.ndarray:
        """Return the grade involution of a dense multivector."""
        return self.unary_sign_matrix("grade_involution") @ self.dense(value)

    def coefficient_rows(
        self,
        value: Iterable[float],
        *,
        precision: int = 6,
        tol: float = EPS,
    ) -> list[dict[str, object]]:
        """Return nonzero coefficient rows for display."""
        value = self.dense(value)
        rows: list[dict[str, object]] = []
        for index, (mask, coefficient) in enumerate(zip(self.order, value, strict=True)):
            if abs(float(coefficient)) <= tol:
                continue
            rows.append(
                {
                    "index": index,
                    "mask": mask,
                    "label": mask_to_label(mask, self.names),
                    "grade": grade(mask),
                    "coefficient": round(float(coefficient), precision),
                }
            )
        return rows

    def product_table_rows(self, *, kind: str = "geometric") -> list[dict[str, object]]:
        """Return basis-by-basis product rows."""
        rows: list[dict[str, object]] = []
        for left_mask in self.order:
            for right_mask in self.order:
                terms = self.basis_product_terms(left_mask, right_mask, kind=kind)
                rows.append(
                    {
                        "left": mask_to_label(left_mask, self.names),
                        "right": mask_to_label(right_mask, self.names),
                        "product": format_terms(terms, self.names),
                    }
                )
        return rows

    def structure_coefficient_rows(self, *, kind: str = "geometric") -> list[dict[str, object]]:
        """Return rows describing nonzero basis-product structure coefficients."""
        rows: list[dict[str, object]] = []
        for left_slot, left_mask in enumerate(self.order):
            for right_slot, right_mask in enumerate(self.order):
                terms = self.basis_product_terms(left_mask, right_mask, kind=kind)
                for output_mask, coefficient in terms.items():
                    rows.append(
                        {
                            "left_slot": left_slot,
                            "left": mask_to_label(left_mask, self.names),
                            "right_slot": right_slot,
                            "right": mask_to_label(right_mask, self.names),
                            "output_slot": self.index(output_mask),
                            "output": mask_to_label(output_mask, self.names),
                            "coefficient": float(coefficient),
                        }
                    )
        return rows


def matrix_density(matrix: np.ndarray, *, tol: float = EPS) -> float:
    """Return the fraction of nonzero entries in a matrix."""
    matrix = np.asarray(matrix, dtype=float)
    return float(np.count_nonzero(np.abs(matrix) > tol) / matrix.size)


def matrix_entry_rows(
    algebra: LinearProductAlgebra,
    matrix: np.ndarray,
    *,
    tol: float = EPS,
    precision: int = 6,
) -> list[dict[str, object]]:
    """Return nonzero matrix entries using basis labels."""
    matrix = np.asarray(matrix, dtype=float)
    rows: list[dict[str, object]] = []
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            value = float(matrix[row, column])
            if abs(value) <= tol:
                continue
            rows.append(
                {
                    "row": row,
                    "column": column,
                    "output": algebra.blade_names[row],
                    "input": algebra.blade_names[column],
                    "value": round(value, precision),
                }
            )
    return rows


def product_table_figure(algebra: LinearProductAlgebra, *, kind: str = "geometric") -> go.Figure:
    """Build an interactive basis-product table as a heatmap."""
    labels = algebra.blade_names
    z = np.zeros((algebra.size, algebra.size), dtype=float)
    hover: list[list[str]] = []
    for row, left_mask in enumerate(algebra.order):
        hover_row: list[str] = []
        for column, right_mask in enumerate(algebra.order):
            terms = algebra.basis_product_terms(left_mask, right_mask, kind=kind)
            text = format_terms(terms, algebra.names)
            if terms:
                weighted = sum(coefficient * (grade(mask) + 1) for mask, coefficient in terms.items())
                z[row, column] = weighted
            hover_row.append(f"{labels[row]} {kind} {labels[column]} = {text}")
        hover.append(hover_row)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels,
            y=labels,
            customdata=hover,
            colorscale=[
                [0.0, COLORS["red"]],
                [0.5, "#f8fafc"],
                [1.0, COLORS["blue"]],
            ],
            hovertemplate="%{customdata}<extra></extra>",
            showscale=False,
        )
    )
    fig.update_layout(
        title=f"Basis-blade {kind.replace('_', ' ')} table",
        width=760,
        height=680,
        xaxis_title="right factor",
        yaxis_title="left factor",
        margin={"l": 75, "r": 25, "t": 55, "b": 75},
    )
    return fig


def operator_heatmap_figure(
    algebra: LinearProductAlgebra,
    matrix: np.ndarray,
    *,
    title: str,
) -> go.Figure:
    """Build a heatmap for a dense operator matrix."""
    matrix = np.asarray(matrix, dtype=float)
    labels = algebra.blade_names
    zmax = max(float(np.max(np.abs(matrix))), EPS)
    hover = [
        [f"{labels[row]} from {labels[column]}: {matrix[row, column]:.4g}" for column in range(algebra.size)]
        for row in range(algebra.size)
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=labels,
            y=labels,
            zmin=-zmax,
            zmax=zmax,
            customdata=hover,
            colorscale=[
                [0.0, COLORS["red"]],
                [0.5, "#f8fafc"],
                [1.0, COLORS["blue"]],
            ],
            hovertemplate="%{customdata}<extra></extra>",
        )
    )
    fig.update_layout(
        title=title,
        width=760,
        height=680,
        xaxis_title="input coordinate",
        yaxis_title="output coordinate",
        margin={"l": 75, "r": 25, "t": 55, "b": 75},
    )
    return fig


def sparsity_comparison_figure(
    algebra: LinearProductAlgebra,
    matrices: Mapping[str, np.ndarray],
) -> go.Figure:
    """Build side-by-side binary sparsity plots for product matrices."""
    titles = list(matrices)
    fig = make_subplots(rows=1, cols=len(titles), subplot_titles=titles, horizontal_spacing=0.06)
    labels = algebra.blade_names
    for col, title in enumerate(titles, start=1):
        pattern = (np.abs(np.asarray(matrices[title], dtype=float)) > EPS).astype(float)
        fig.add_trace(
            go.Heatmap(
                z=pattern,
                x=labels,
                y=labels,
                colorscale=[[0.0, "#f8fafc"], [1.0, COLORS["green"]]],
                showscale=False,
                hovertemplate="row %{y}<br>col %{x}<br>nonzero %{z}<extra></extra>",
            ),
            row=1,
            col=col,
        )
    fig.update_layout(
        title="Sparsity patterns of linear product matrices",
        width=300 * len(titles),
        height=430,
        margin={"l": 65, "r": 20, "t": 75, "b": 70},
    )
    return fig


def coefficient_bar_figure(
    algebra: LinearProductAlgebra,
    value: Iterable[float],
    *,
    title: str,
) -> plt.Figure:
    """Draw dense multivector coordinates as a bar chart."""
    value = algebra.dense(value)
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    colors = [COLORS["orange"] if abs(coefficient) > EPS else COLORS["light"] for coefficient in value]
    ax.bar(algebra.blade_names, value, color=colors)
    ax.axhline(0.0, color=COLORS["ink"], linewidth=0.8)
    ax.set_title(title)
    ax.set_ylabel("coefficient")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    return fig


def grade_projection_figure(
    algebra: LinearProductAlgebra,
    value: Iterable[float],
    *,
    title: str,
) -> plt.Figure:
    """Draw grade-separated coordinate energy for a multivector."""
    value = algebra.dense(value)
    energies = []
    for target_grade in range(algebra.dimension + 1):
        projected = algebra.project_grade(value, target_grade)
        energies.append(float(np.linalg.norm(projected)))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.bar(range(algebra.dimension + 1), energies, color=COLORS["blue"])
    ax.set_title(title)
    ax.set_xlabel("grade")
    ax.set_ylabel("coordinate norm")
    ax.set_xticks(range(algebra.dimension + 1))
    fig.tight_layout()
    return fig


def operation_profile_rows(
    algebra: LinearProductAlgebra,
    left: Iterable[float],
    right: Iterable[float],
    *,
    kinds: Sequence[str] = ("geometric", "outer", "left_contraction", "right_contraction"),
) -> list[dict[str, object]]:
    """Return operation profiles contrasting matrix and sparse views."""
    left = algebra.dense(left)
    right = algebra.dense(right)
    left_sparse = algebra.dense_to_sparse(left)
    right_sparse = algebra.dense_to_sparse(right)
    rows: list[dict[str, object]] = []
    for kind in kinds:
        matrix = algebra.left_operator_matrix(left, kind=kind)
        output = algebra.dense_product(left, right, kind=kind)
        rows.append(
            {
                "kind": kind,
                "matrix_slots": int(matrix.size),
                "matrix_nonzeros": int(np.count_nonzero(np.abs(matrix) > EPS)),
                "matrix_density": round(matrix_density(matrix), 4),
                "sparse_pairs_checked": int(len(left_sparse) * len(right_sparse)),
                "output_terms": int(len(algebra.dense_to_sparse(output))),
            }
        )
    return rows


def operation_profile_figure(rows: Sequence[Mapping[str, object]]) -> go.Figure:
    """Draw a grouped bar chart for operation profile rows."""
    labels = [str(row["kind"]).replace("_", " ") for row in rows]
    fig = go.Figure()
    for key, name, color in [
        ("matrix_nonzeros", "operator nonzeros", COLORS["purple"]),
        ("sparse_pairs_checked", "sparse blade pairs", COLORS["orange"]),
        ("output_terms", "output terms", COLORS["green"]),
    ]:
        fig.add_trace(
            go.Bar(
                x=labels,
                y=[int(row[key]) for row in rows],
                name=name,
                marker={"color": color},
            )
        )
    fig.update_layout(
        title="Linear products: matrix entries versus sparse work",
        width=820,
        height=450,
        barmode="group",
        yaxis_title="count",
        margin={"l": 65, "r": 25, "t": 60, "b": 70},
    )
    return fig


def storage_growth_rows(max_dimension: int = 8, active_terms: int = 6) -> list[dict[str, int]]:
    """Return rough storage counts for dense matrices and sparse lists."""
    rows: list[dict[str, int]] = []
    for dimension in range(1, max_dimension + 1):
        dense_terms = 1 << dimension
        rows.append(
            {
                "dimension": dimension,
                "dense_multivector": dense_terms,
                "dense_operator_matrix": dense_terms * dense_terms,
                "example_sparse_terms": min(active_terms, dense_terms),
            }
        )
    return rows


def storage_growth_figure(rows: Sequence[Mapping[str, int]]) -> go.Figure:
    """Draw storage growth for dense and sparse representations."""
    dimensions = [int(row["dimension"]) for row in rows]
    fig = go.Figure()
    for key, name, color in [
        ("dense_multivector", "dense multivector", COLORS["blue"]),
        ("dense_operator_matrix", "dense product matrix", COLORS["red"]),
        ("example_sparse_terms", "sparse list example", COLORS["green"]),
    ]:
        fig.add_trace(
            go.Scatter(
                x=dimensions,
                y=[int(row[key]) for row in rows],
                mode="lines+markers",
                name=name,
                line={"color": color, "width": 3},
            )
        )
    fig.update_layout(
        title="Storage choices for linear products",
        width=830,
        height=470,
        yaxis={"title": "stored scalar slots", "type": "log"},
        xaxis_title="vector-space dimension",
        hovermode="x unified",
        margin={"l": 70, "r": 25, "t": 60, "b": 60},
    )
    return fig


def save_plotly_html(figure: go.Figure, path: str | Path) -> Path:
    """Save a Plotly figure to HTML and return the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.write_html(path, include_plotlyjs="cdn", full_html=True)
    return path


def save_matplotlib_png(figure: plt.Figure, path: str | Path, *, dpi: int = 160) -> Path:
    """Save a Matplotlib figure to PNG and return the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(figure)
    return path


def save_json(data: object, path: str | Path) -> Path:
    """Save JSON data and return the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(data), indent=2, sort_keys=True), encoding="utf-8")
    return path


def sanity_checks() -> dict[str, float]:
    """Run numerical invariants used by the notebook quality gate."""
    algebra = LinearProductAlgebra.from_signature((1.0, 1.0, 1.0))
    rng = np.random.default_rng(20)
    left = rng.normal(size=algebra.size)
    right = rng.normal(size=algebra.size)

    errors: dict[str, float] = {}
    for kind in ("geometric", "outer", "left_contraction", "right_contraction", "scalar"):
        matrix_result = algebra.left_operator_matrix(left, kind=kind) @ right
        sparse_result = algebra.dense_product(left, right, kind=kind)
        errors[f"{kind}_matrix_sparse_error"] = float(np.linalg.norm(matrix_result - sparse_result))

    projection_sum = sum(algebra.project_grade(left, target) for target in range(algebra.dimension + 1))
    errors["grade_projection_reconstruction_error"] = float(np.linalg.norm(projection_sum - left))

    reversion = algebra.unary_sign_matrix("reversion")
    errors["reversion_involution_error"] = float(np.linalg.norm(reversion @ reversion - np.eye(algebra.size)))

    vector = algebra.vector([0.5, -1.2, 0.7])
    blade = 1.3 * algebra.basis_dense(0b011) - 0.4 * algebra.basis_dense(0b101)
    vector_blade_error = np.linalg.norm(
        algebra.dense_product(vector, blade, kind="geometric")
        - algebra.dense_product(vector, blade, kind="left_contraction")
        - algebra.dense_product(vector, blade, kind="outer")
    )
    errors["vector_blade_split_error"] = float(vector_blade_error)

    first_gp_column = algebra.left_operator_matrix(left, kind="geometric")[:, algebra.index(0)]
    first_outer_column = algebra.left_operator_matrix(left, kind="outer")[:, algebra.index(0)]
    first_left_contraction = algebra.left_operator_matrix(left, kind="left_contraction")[:, algebra.index(0)]
    expected_left_contraction = np.zeros(algebra.size)
    expected_left_contraction[algebra.index(0)] = left[algebra.index(0)]
    errors["first_gp_column_error"] = float(np.linalg.norm(first_gp_column - left))
    errors["first_outer_column_error"] = float(np.linalg.norm(first_outer_column - left))
    errors["first_left_contraction_column_error"] = float(
        np.linalg.norm(first_left_contraction - expected_left_contraction)
    )

    skew_metric = np.array(
        [
            [1.0, 0.25, 0.0],
            [0.25, 1.0, -0.15],
            [0.0, -0.15, 1.0],
        ]
    )
    nonorthogonal = LinearProductAlgebra(skew_metric)
    nonorth_left = rng.normal(size=nonorthogonal.size)
    nonorth_right = rng.normal(size=nonorthogonal.size)
    errors["nondiagonal_metric_matrix_sparse_error"] = float(
        np.linalg.norm(
            nonorthogonal.left_operator_matrix(nonorth_left) @ nonorth_right
            - nonorthogonal.dense_product(nonorth_left, nonorth_right)
        )
    )
    return errors
