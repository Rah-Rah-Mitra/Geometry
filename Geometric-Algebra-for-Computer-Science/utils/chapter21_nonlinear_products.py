"""Helpers for Chapter 21 nonlinear-product notebooks.

The code intentionally stays small and explicit. It is not a full geometric
algebra package; it is a notebook-sized Euclidean/orthonormal engine that makes
the nonlinear algorithms inspectable: versor inversion, blade factorization,
delta products, and robust meet/join computations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.colors import ListedColormap

EPS = 1e-10

COLORS = {
    "blue": "#2f6fbb",
    "orange": "#d9822b",
    "green": "#348f50",
    "red": "#c43c39",
    "purple": "#7a4db3",
    "gray": "#6b7280",
    "faint_blue": "rgba(47, 111, 187, 0.28)",
    "faint_orange": "rgba(217, 130, 43, 0.30)",
}


def grade(mask: int) -> int:
    """Return the grade of a basis blade encoded as an integer bit mask."""
    return int(mask).bit_count()


def basis_masks(dimension: int) -> list[int]:
    """Return all basis-blade masks in dense-coordinate order."""
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    return list(range(1 << dimension))


def mask_to_name(mask: int, names: Iterable[str] | None = None) -> str:
    """Return a compact ASCII name such as ``e1e3`` for a basis blade."""
    mask = int(mask)
    if mask == 0:
        return "1"
    if names is None:
        names = [f"e{i + 1}" for i in range(max(1, mask.bit_length()))]
    names = tuple(names)
    pieces = [names[i] for i in range(len(names)) if mask & (1 << i)]
    return "".join(pieces)


def _reordering_sign(left_mask: int, right_mask: int) -> float:
    """Return the sign needed to put two bit-mask blades in canonical order."""
    swaps = 0
    right = int(right_mask)
    for bit in range(int(left_mask).bit_length()):
        if left_mask & (1 << bit):
            swaps += (right & ((1 << bit) - 1)).bit_count()
    return -1.0 if swaps % 2 else 1.0


def basis_blade_product(
    left_mask: int,
    right_mask: int,
    signature: Iterable[float],
) -> tuple[float, int]:
    """Multiply two orthonormal basis blades.

    Duplicate basis vectors collapse by their metric square from ``signature``;
    the remaining basis blade is the XOR of the two masks.
    """
    signature = tuple(float(value) for value in signature)
    left_mask = int(left_mask)
    right_mask = int(right_mask)
    sign = _reordering_sign(left_mask, right_mask)
    common = left_mask & right_mask
    metric_factor = 1.0
    for bit, square in enumerate(signature):
        if common & (1 << bit):
            metric_factor *= square
    return sign * metric_factor, left_mask ^ right_mask


def _as_2d_rows(vectors: Iterable[Iterable[float]] | np.ndarray, dimension: int) -> np.ndarray:
    """Return vectors as a row matrix with a known ambient dimension."""
    array = np.asarray(vectors, dtype=float)
    if array.size == 0:
        return np.zeros((0, dimension), dtype=float)
    if array.ndim == 1:
        array = array.reshape(1, -1)
    if array.ndim != 2 or array.shape[1] != dimension:
        raise ValueError(f"expected rows with {dimension} coordinates")
    return array


def _nullspace(matrix: np.ndarray, *, tol: float = EPS) -> tuple[np.ndarray, np.ndarray]:
    """Return an orthonormal nullspace basis as columns and all singular values."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("matrix must be 2-D")
    if matrix.shape[0] == 0:
        return np.eye(matrix.shape[1]), np.zeros(0)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > tol))
    return vh[rank:].T.copy(), singular_values


def orthonormal_rows(matrix: Iterable[Iterable[float]] | np.ndarray, *, tol: float = EPS) -> np.ndarray:
    """Return an orthonormal row basis for the row span of ``matrix``."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2:
        raise ValueError("matrix must be 2-D")
    if matrix.size == 0:
        return np.zeros((0, matrix.shape[1]), dtype=float)
    _, singular_values, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(singular_values > tol))
    return vh[:rank].copy()


@dataclass(frozen=True)
class VersorInverseResult:
    """Diagnostic result for the reverse-over-norm versor inverse."""

    inverse: np.ndarray
    denominator: float
    scalar_residual: float


@dataclass(frozen=True)
class MatrixInverseResult:
    """Diagnostic result for generic multivector inversion by matrix solve."""

    inverse: np.ndarray
    condition_number: float
    identity_error: float


@dataclass(frozen=True)
class FactorizationResult:
    """Result of extracting vector factors from a dense blade."""

    grade: int
    scale: float
    factors: np.ndarray
    reconstructed: np.ndarray
    residual: float
    singular_values: np.ndarray


@dataclass(frozen=True)
class MeetJoinResult:
    """Numerical meet/join result with diagnostic grade information."""

    meet_factors: np.ndarray
    join_factors: np.ndarray
    meet_blade: np.ndarray
    join_blade: np.ndarray
    delta_blade: np.ndarray
    singular_values: np.ndarray
    delta_grade: int
    predicted_meet_grade: int
    predicted_join_grade: int


@dataclass(frozen=True)
class OrthonormalAlgebra:
    """A compact dense-coordinate model for an orthonormal geometric algebra."""

    signature: tuple[float, ...]
    names: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        signature = tuple(float(value) for value in self.signature)
        if any(abs(value) <= EPS for value in signature):
            raise ValueError("basis-vector squares must be nonzero")
        object.__setattr__(self, "signature", signature)
        if self.names is None:
            object.__setattr__(
                self,
                "names",
                tuple(f"e{i + 1}" for i in range(len(signature))),
            )
        else:
            names = tuple(self.names)
            if len(names) != len(signature):
                raise ValueError("names and signature must match in length")
            object.__setattr__(self, "names", names)

    @property
    def dimension(self) -> int:
        """Return the vector-space dimension."""
        return len(self.signature)

    @property
    def size(self) -> int:
        """Return the number of dense multivector coordinates."""
        return 1 << self.dimension

    @property
    def blade_names(self) -> list[str]:
        """Return readable names for all basis blades."""
        return [mask_to_name(mask, self.names) for mask in basis_masks(self.dimension)]

    def dense(self, coefficients: Iterable[float]) -> np.ndarray:
        """Return a validated dense multivector coordinate array."""
        coefficients = np.asarray(coefficients, dtype=float)
        if coefficients.shape != (self.size,):
            raise ValueError(f"expected {self.size} coefficients")
        return coefficients.copy()

    def scalar(self, value: float) -> np.ndarray:
        """Return a scalar multivector."""
        result = np.zeros(self.size, dtype=float)
        result[0] = float(value)
        return result

    def vector(self, coordinates: Iterable[float]) -> np.ndarray:
        """Encode vector coordinates as a dense grade-1 multivector."""
        coordinates = np.asarray(coordinates, dtype=float)
        if coordinates.shape != (self.dimension,):
            raise ValueError(f"expected {self.dimension} vector coordinates")
        result = np.zeros(self.size, dtype=float)
        for bit, value in enumerate(coordinates):
            result[1 << bit] = value
        return result

    def basis_vector(self, index: int) -> np.ndarray:
        """Return the indexed unit basis vector as a multivector."""
        if not 0 <= index < self.dimension:
            raise ValueError("basis-vector index is outside the algebra")
        coordinates = np.zeros(self.dimension, dtype=float)
        coordinates[index] = 1.0
        return self.vector(coordinates)

    def pseudoscalar(self) -> np.ndarray:
        """Return the unit pseudoscalar for the full vector space."""
        result = np.zeros(self.size, dtype=float)
        result[(1 << self.dimension) - 1] = 1.0
        return result

    def basis_blade_product(self, left_mask: int, right_mask: int) -> tuple[float, int]:
        """Multiply two basis blades in this algebra."""
        return basis_blade_product(left_mask, right_mask, self.signature)

    def geometric_product(self, left: Iterable[float], right: Iterable[float]) -> np.ndarray:
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
                factor, result_mask = self.basis_blade_product(left_mask, right_mask)
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
                factor, result_mask = self.basis_blade_product(left_mask, right_mask)
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

    def grade_norms(self, value: Iterable[float]) -> dict[int, float]:
        """Return the coordinate norm carried by each grade."""
        value = self.dense(value)
        norms: dict[int, float] = {}
        for target_grade in range(self.dimension + 1):
            projection = self.grade_projection(value, target_grade)
            norms[target_grade] = float(np.linalg.norm(projection))
        return norms

    def dominant_grade(self, value: Iterable[float], *, tol: float = EPS) -> int:
        """Return the unique occupied grade, raising if more than one is present."""
        norms = self.grade_norms(value)
        occupied = [target_grade for target_grade, norm in norms.items() if norm > tol]
        if not occupied:
            return 0
        if len(occupied) != 1:
            raise ValueError(f"expected one occupied grade, got {occupied}")
        return occupied[0]

    def reverse(self, value: Iterable[float]) -> np.ndarray:
        """Return reversion of a dense multivector."""
        value = self.dense(value)
        result = np.zeros_like(value)
        for mask, coefficient in enumerate(value):
            target_grade = grade(mask)
            sign = -1.0 if (target_grade * (target_grade - 1) // 2) % 2 else 1.0
            result[mask] = sign * coefficient
        return result

    def dual(self, value: Iterable[float]) -> np.ndarray:
        """Return the right dual ``value * I^{-1}``."""
        pseudoscalar_inverse = versor_inverse(self, self.pseudoscalar()).inverse
        return self.geometric_product(value, pseudoscalar_inverse)

    def format_multivector(self, value: Iterable[float], *, tol: float = 1e-9) -> str:
        """Format a dense multivector as a compact coordinate expression."""
        value = self.dense(value)
        pieces = []
        for mask, coefficient in enumerate(value):
            if abs(coefficient) <= tol:
                continue
            label = mask_to_name(mask, self.names)
            if mask == 0:
                pieces.append(f"{coefficient:.5g}")
            else:
                pieces.append(f"{coefficient:.5g} {label}")
        return "0" if not pieces else " + ".join(pieces).replace("+ -", "- ")


def blade_from_vectors(algebra: OrthonormalAlgebra, vectors: Iterable[Iterable[float]]) -> np.ndarray:
    """Return the blade represented by the outer product of row vectors."""
    vectors = _as_2d_rows(vectors, algebra.dimension)
    result = algebra.scalar(1.0)
    for vector in vectors:
        result = algebra.outer_product(result, algebra.vector(vector))
    return result


def versor_from_vectors(algebra: OrthonormalAlgebra, vectors: Iterable[Iterable[float]]) -> np.ndarray:
    """Return the geometric product of row-vector factors."""
    vectors = _as_2d_rows(vectors, algebra.dimension)
    result = algebra.scalar(1.0)
    for vector in vectors:
        result = algebra.geometric_product(result, algebra.vector(vector))
    return result


def versor_inverse(
    algebra: OrthonormalAlgebra,
    versor: Iterable[float],
    *,
    tol: float = EPS,
    require_scalar: bool = True,
) -> VersorInverseResult:
    """Invert a versor by reverse divided by the scalar part of ``V reverse(V)``."""
    versor = algebra.dense(versor)
    reverse = algebra.reverse(versor)
    product = algebra.geometric_product(versor, reverse)
    denominator = float(product[0])
    scalar_residual = float(np.linalg.norm(product - algebra.scalar(denominator)))
    if abs(denominator) <= tol:
        raise ZeroDivisionError("versor has near-zero reverse norm")
    if require_scalar and scalar_residual > max(tol, tol * np.linalg.norm(product)):
        raise ValueError("reverse-over-norm inverse is only valid when V reverse(V) is scalar")
    return VersorInverseResult(reverse / denominator, denominator, scalar_residual)


def left_multiplication_matrix(algebra: OrthonormalAlgebra, value: Iterable[float]) -> np.ndarray:
    """Return the matrix for left multiplication by ``value``."""
    value = algebra.dense(value)
    matrix = np.zeros((algebra.size, algebra.size), dtype=float)
    for column, mask in enumerate(basis_masks(algebra.dimension)):
        basis = np.zeros(algebra.size, dtype=float)
        basis[mask] = 1.0
        matrix[:, column] = algebra.geometric_product(value, basis)
    return matrix


def multivector_inverse_via_matrix(
    algebra: OrthonormalAlgebra,
    value: Iterable[float],
) -> MatrixInverseResult:
    """Invert a dense multivector by solving its left-multiplication matrix."""
    value = algebra.dense(value)
    matrix = left_multiplication_matrix(algebra, value)
    target = algebra.scalar(1.0)
    inverse = np.linalg.solve(matrix, target)
    identity_error = float(np.linalg.norm(algebra.geometric_product(value, inverse) - target))
    return MatrixInverseResult(inverse, float(np.linalg.cond(matrix)), identity_error)


def factor_blade(
    algebra: OrthonormalAlgebra,
    blade: Iterable[float],
    *,
    tol: float = 1e-9,
) -> FactorizationResult:
    """Extract an orthonormal row-factor basis from a nonzero Euclidean blade.

    The vector subspace of a k-blade B is recovered as the nullspace of the
    linear map x -> x wedge B. The returned factors are orthonormal; the blade's
    magnitude and orientation are carried by the separate ``scale`` field.
    """
    blade = algebra.dense(blade)
    target_grade = algebra.dominant_grade(blade, tol=tol)
    if target_grade == 0:
        reconstructed = algebra.scalar(float(blade[0]))
        return FactorizationResult(
            0,
            float(blade[0]),
            np.zeros((0, algebra.dimension), dtype=float),
            reconstructed,
            float(np.linalg.norm(blade - reconstructed)),
            np.zeros(0),
        )

    target_masks = [
        mask for mask in basis_masks(algebra.dimension) if grade(mask) == target_grade + 1
    ]
    wedge_matrix = np.zeros((len(target_masks), algebra.dimension), dtype=float)
    for index in range(algebra.dimension):
        column = algebra.outer_product(algebra.basis_vector(index), blade)
        wedge_matrix[:, index] = column[target_masks]

    nullspace, singular_values = _nullspace(wedge_matrix, tol=tol)
    factors = orthonormal_rows(nullspace.T, tol=tol)
    if factors.shape[0] != target_grade:
        raise ValueError(
            "blade factorization did not find the expected subspace dimension; "
            "the input may not be a simple blade"
        )

    unit_blade = blade_from_vectors(algebra, factors)
    denominator = float(np.dot(unit_blade, unit_blade))
    if abs(denominator) <= tol:
        raise ZeroDivisionError("unit factor blade vanished during reconstruction")
    scale = float(np.dot(blade, unit_blade) / denominator)
    reconstructed = scale * unit_blade
    residual = float(np.linalg.norm(blade - reconstructed) / (np.linalg.norm(blade) + tol))
    return FactorizationResult(target_grade, scale, factors, reconstructed, residual, singular_values)


def highest_grade_part(
    algebra: OrthonormalAlgebra,
    value: Iterable[float],
    *,
    tol: float = 1e-9,
) -> tuple[np.ndarray, int]:
    """Return the nonzero highest-grade part of a multivector."""
    value = algebra.dense(value)
    for target_grade in range(algebra.dimension, -1, -1):
        projection = algebra.grade_projection(value, target_grade)
        if np.linalg.norm(projection) > tol:
            return projection, target_grade
    return algebra.scalar(0.0), 0


def delta_product(
    algebra: OrthonormalAlgebra,
    left: Iterable[float],
    right: Iterable[float],
    *,
    tol: float = 1e-9,
) -> tuple[np.ndarray, int]:
    """Return the blade delta product: the highest-grade part of ``left * right``."""
    product = algebra.geometric_product(left, right)
    return highest_grade_part(algebra, product, tol=tol)


def meet_join_grades(grade_a: int, grade_b: int, delta_grade: int) -> tuple[int, int]:
    """Return meet and join grades implied by input and delta grades."""
    meet_grade = (grade_a + grade_b - delta_grade) // 2
    join_grade = (grade_a + grade_b + delta_grade) // 2
    return int(meet_grade), int(join_grade)


def projection_matrix(factors: Iterable[Iterable[float]] | np.ndarray, dimension: int) -> np.ndarray:
    """Return the orthogonal projection matrix onto a row-factor subspace."""
    rows = orthonormal_rows(_as_2d_rows(factors, dimension))
    if rows.size == 0:
        return np.zeros((dimension, dimension), dtype=float)
    return rows.T @ rows


def subspace_containment_error(
    contained: Iterable[Iterable[float]] | np.ndarray,
    container: Iterable[Iterable[float]] | np.ndarray,
) -> float:
    """Return how far row vectors in ``contained`` fall outside ``container``."""
    contained = np.asarray(contained, dtype=float)
    if contained.size == 0:
        return 0.0
    dimension = contained.shape[1]
    projector = projection_matrix(container, dimension)
    residual = contained - contained @ projector
    return float(np.linalg.norm(residual))


def meet_join_from_blades(
    algebra: OrthonormalAlgebra,
    left: Iterable[float],
    right: Iterable[float],
    *,
    factor_tol: float = 1e-9,
    common_tol: float = 1e-8,
) -> MeetJoinResult:
    """Compute meet and join by factoring blades into stable subspace bases."""
    left_factors = factor_blade(algebra, left, tol=factor_tol)
    right_factors = factor_blade(algebra, right, tol=factor_tol)
    qa = left_factors.factors
    qb = right_factors.factors

    if qa.size == 0 or qb.size == 0:
        meet_factors = np.zeros((0, algebra.dimension), dtype=float)
        singular_values = np.zeros(0)
    else:
        u, singular_values, _ = np.linalg.svd(qa @ qb.T, full_matrices=False)
        common_columns = [index for index, value in enumerate(singular_values) if 1.0 - value <= common_tol]
        if common_columns:
            meet_factors = np.asarray([u[:, index] @ qa for index in common_columns])
            meet_factors = orthonormal_rows(meet_factors, tol=factor_tol)
        else:
            meet_factors = np.zeros((0, algebra.dimension), dtype=float)

    join_factors = orthonormal_rows(np.vstack([qa, qb]), tol=factor_tol)
    meet_blade = blade_from_vectors(algebra, meet_factors)
    join_blade = blade_from_vectors(algebra, join_factors)
    delta_blade, delta_grade = delta_product(algebra, left, right, tol=factor_tol)
    predicted_meet_grade, predicted_join_grade = meet_join_grades(
        left_factors.grade,
        right_factors.grade,
        delta_grade,
    )
    return MeetJoinResult(
        meet_factors,
        join_factors,
        meet_blade,
        join_blade,
        delta_blade,
        singular_values,
        delta_grade,
        predicted_meet_grade,
        predicted_join_grade,
    )


def factorization_bar_figure(
    algebra: OrthonormalAlgebra,
    original: Iterable[float],
    reconstructed: Iterable[float],
) -> plt.Figure:
    """Return a grouped coefficient bar chart for a blade reconstruction."""
    original = algebra.dense(original)
    reconstructed = algebra.dense(reconstructed)
    x = np.arange(algebra.size)
    width = 0.38
    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.bar(x - width / 2, original, width, label="original", color=COLORS["blue"])
    ax.bar(x + width / 2, reconstructed, width, label="reconstructed", color=COLORS["orange"])
    ax.set_xticks(x)
    ax.set_xticklabels(algebra.blade_names, rotation=35, ha="right")
    ax.axhline(0.0, color="#1f2937", linewidth=0.8)
    ax.set_title("Blade factorization reconstructs the same coordinates")
    ax.set_ylabel("coefficient")
    ax.legend()
    fig.tight_layout()
    return fig


def delta_set_figure() -> plt.Figure:
    """Return a Venn-style raster diagram for union, meet, and delta."""
    xs = np.linspace(-2.8, 2.8, 420)
    ys = np.linspace(-1.9, 1.9, 300)
    xx, yy = np.meshgrid(xs, ys)
    a = (xx + 0.72) ** 2 + yy**2 <= 1.35**2
    b = (xx - 0.72) ** 2 + yy**2 <= 1.35**2
    image = np.zeros_like(xx, dtype=int)
    image[np.logical_xor(a, b)] = 1
    image[np.logical_and(a, b)] = 2
    cmap = ListedColormap(["#ffffff", "#f2c14e", "#348f50"])

    fig, ax = plt.subplots(figsize=(8.6, 3.7))
    ax.imshow(
        image,
        extent=(xs.min(), xs.max(), ys.min(), ys.max()),
        origin="lower",
        cmap=cmap,
        interpolation="nearest",
        alpha=0.94,
    )
    ax.contour(xx, yy, a.astype(float), levels=[0.5], colors=[COLORS["blue"]], linewidths=2.3)
    ax.contour(xx, yy, b.astype(float), levels=[0.5], colors=[COLORS["red"]], linewidths=2.3)
    ax.text(-1.45, 1.42, "A only", color="#5f4600", ha="center", fontsize=11)
    ax.text(1.45, 1.42, "B only", color="#5f4600", ha="center", fontsize=11)
    ax.text(0.0, 0.0, "meet", color="white", ha="center", va="center", fontsize=12)
    ax.text(0.0, -1.67, "delta keeps factors appearing in exactly one input", ha="center")
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def _plane_surface(
    factors: np.ndarray,
    *,
    span: float = 1.35,
    samples: int = 16,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mesh coordinates for a plane through the origin."""
    if factors.shape != (2, 3):
        raise ValueError("plane visualization expects two 3-D row factors")
    u = np.linspace(-span, span, samples)
    v = np.linspace(-span, span, samples)
    uu, vv = np.meshgrid(u, v)
    points = uu[..., None] * factors[0] + vv[..., None] * factors[1]
    return points[..., 0], points[..., 1], points[..., 2]


def meet_join_figure(
    left_factors: Iterable[Iterable[float]],
    right_factors: Iterable[Iterable[float]],
    result: MeetJoinResult,
) -> go.Figure:
    """Return a 3-D Plotly figure for two planes and their meet line."""
    left_factors = _as_2d_rows(left_factors, 3)
    right_factors = _as_2d_rows(right_factors, 3)
    left_x, left_y, left_z = _plane_surface(left_factors)
    right_x, right_y, right_z = _plane_surface(right_factors)
    fig = go.Figure()
    fig.add_trace(
        go.Surface(
            x=left_x,
            y=left_y,
            z=left_z,
            name="blade A",
            colorscale=[[0, COLORS["blue"]], [1, COLORS["blue"]]],
            opacity=0.44,
            showscale=False,
        )
    )
    fig.add_trace(
        go.Surface(
            x=right_x,
            y=right_y,
            z=right_z,
            name="blade B",
            colorscale=[[0, COLORS["orange"]], [1, COLORS["orange"]]],
            opacity=0.46,
            showscale=False,
        )
    )
    if result.meet_factors.shape[0] >= 1:
        direction = result.meet_factors[0]
        t = np.linspace(-1.75, 1.75, 60)
        line = t[:, None] * direction
        fig.add_trace(
            go.Scatter3d(
                x=line[:, 0],
                y=line[:, 1],
                z=line[:, 2],
                mode="lines",
                name="meet",
                line={"color": COLORS["green"], "width": 8},
            )
        )
    fig.update_layout(
        title="Meet/join of two plane blades: green line is the meet",
        width=850,
        height=620,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        scene={
            "aspectmode": "cube",
            "xaxis": {"range": [-1.8, 1.8], "title": "e1"},
            "yaxis": {"range": [-1.8, 1.8], "title": "e2"},
            "zaxis": {"range": [-1.8, 1.8], "title": "e3"},
            "camera": {"eye": {"x": 1.65, "y": -1.85, "z": 1.2}},
        },
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.72)"},
    )
    return fig


def robustness_scan(angles_degrees: Iterable[float]) -> list[dict[str, float]]:
    """Return singular-value diagnostics for two nearly coincident planes."""
    rows: list[dict[str, float]] = []
    plane_a = np.eye(3)[:2]
    qa = orthonormal_rows(plane_a)
    for angle_degrees in angles_degrees:
        angle = np.deg2rad(float(angle_degrees))
        plane_b = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, np.cos(angle), np.sin(angle)],
            ]
        )
        qb = orthonormal_rows(plane_b)
        singular_values = np.linalg.svd(qa @ qb.T, compute_uv=False)
        rows.append(
            {
                "angle_degrees": float(angle_degrees),
                "sigma_1": float(singular_values[0]),
                "sigma_2": float(singular_values[1]),
                "gap_from_common": float(1.0 - singular_values[1]),
            }
        )
    return rows


def robustness_scan_figure(rows: list[dict[str, float]], thresholds: Iterable[float]) -> plt.Figure:
    """Return a figure showing when a nearly shared factor becomes ambiguous."""
    angles = np.array([row["angle_degrees"] for row in rows], dtype=float)
    gaps = np.array([row["gap_from_common"] for row in rows], dtype=float)
    fig, ax = plt.subplots(figsize=(8.4, 4.1))
    ax.plot(angles, gaps, color=COLORS["purple"], linewidth=2.7, marker="o", markersize=3.5)
    for threshold in thresholds:
        ax.axhline(float(threshold), linestyle="--", linewidth=1.4, label=f"tol={threshold:g}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("angle between the non-common plane factors, degrees")
    ax.set_ylabel("1 - second principal cosine")
    ax.set_title("Thresholds decide when near-coincident planes count as the same plane")
    ax.grid(True, which="both", alpha=0.28)
    ax.legend()
    fig.tight_layout()
    return fig


def sanity_checks() -> dict[str, float]:
    """Run small invariant checks used by the notebook and validation."""
    algebra = OrthonormalAlgebra((1.0, 1.0, 1.0), names=("e1", "e2", "e3"))
    rng = np.random.default_rng(21)
    vectors = orthonormal_rows(rng.normal(size=(2, 3)))
    blade = blade_from_vectors(algebra, vectors)
    factored = factor_blade(algebra, blade)
    versor = versor_from_vectors(algebra, vectors)
    inverse = versor_inverse(algebra, versor)
    identity_error = np.linalg.norm(algebra.geometric_product(versor, inverse.inverse) - algebra.scalar(1.0))
    plane_a = blade_from_vectors(algebra, [[1, 0, 0], [0, 1, 0]])
    plane_b = blade_from_vectors(algebra, [[1, 0, 0], [0, 0, 1]])
    result = meet_join_from_blades(algebra, plane_a, plane_b)
    meet_in_a = subspace_containment_error(result.meet_factors, [[1, 0, 0], [0, 1, 0]])
    meet_in_b = subspace_containment_error(result.meet_factors, [[1, 0, 0], [0, 0, 1]])
    return {
        "factorization_residual": float(factored.residual),
        "versor_inverse_identity_error": float(identity_error),
        "delta_grade": float(result.delta_grade),
        "predicted_meet_grade": float(result.predicted_meet_grade),
        "predicted_join_grade": float(result.predicted_join_grade),
        "actual_meet_grade": float(result.meet_factors.shape[0]),
        "actual_join_grade": float(result.join_factors.shape[0]),
        "meet_containment_error": float(max(meet_in_a, meet_in_b)),
    }
