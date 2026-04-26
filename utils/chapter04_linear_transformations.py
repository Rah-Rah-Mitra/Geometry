"""Helpers for Chapter 4 linear-transformation notebook labs.

The functions here use column-vector convention: a matrix ``M`` maps a vector
``x`` to ``M @ x``. Blade coordinates are listed by increasing basis-index
combinations, so a 3-D bivector uses ``(e12, e13, e23)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import cos, sin

import numpy as np

EPS = 1e-10


def rotation2(angle: float) -> np.ndarray:
    """Return a 2-D counterclockwise rotation matrix."""
    c = cos(angle)
    s = sin(angle)
    return np.array([[c, -s], [s, c]], dtype=float)


def shear2(amount: float) -> np.ndarray:
    """Return a horizontal 2-D shear matrix."""
    return np.array([[1.0, amount], [0.0, 1.0]], dtype=float)


def scale2(sx: float, sy: float) -> np.ndarray:
    """Return a 2-D anisotropic scaling matrix."""
    return np.diag([float(sx), float(sy)])


def demo_matrix(angle: float = 0.45, sx: float = 1.35, sy: float = 0.75, shear: float = 0.25) -> np.ndarray:
    """A compact family of non-orthogonal linear maps for examples."""
    return rotation2(angle) @ shear2(shear) @ scale2(sx, sy)


def apply_matrix(matrix: np.ndarray, vectors: np.ndarray) -> np.ndarray:
    """Apply a column-vector matrix to one vector or a stack of row vectors."""
    matrix = np.asarray(matrix, dtype=float)
    values = np.asarray(vectors, dtype=float)
    if values.ndim == 1:
        return matrix @ values
    return values @ matrix.T


def blade_basis(dimension: int, grade: int) -> list[tuple[int, ...]]:
    """Return ordered basis-index tuples for k-blades in R^n."""
    if grade < 0 or grade > dimension:
        return []
    return list(combinations(range(dimension), grade))


def wedge_vectors(*vectors: np.ndarray) -> np.ndarray:
    """Coordinates of the blade spanned by the supplied vectors."""
    if not vectors:
        return np.array([1.0])
    columns = np.column_stack([np.asarray(vector, dtype=float) for vector in vectors])
    dimension, grade = columns.shape
    coords = []
    for rows in blade_basis(dimension, grade):
        coords.append(float(np.linalg.det(columns[np.ix_(rows, range(grade))])))
    return np.array(coords)


def exterior_power_matrix(matrix: np.ndarray, grade: int) -> np.ndarray:
    """Matrix for the grade-k outermorphism induced by ``matrix``."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("outermorphism matrix must be square")
    dimension = matrix.shape[0]
    basis = blade_basis(dimension, grade)
    if grade == 0:
        return np.ones((1, 1), dtype=float)
    result = np.zeros((len(basis), len(basis)), dtype=float)
    for col, input_blade in enumerate(basis):
        image_vectors = [matrix[:, axis] for axis in input_blade]
        result[:, col] = wedge_vectors(*image_vectors)
    return result


def adjoint_matrix(matrix: np.ndarray, metric: np.ndarray | None = None) -> np.ndarray:
    """Return the adjoint matrix for the supplied symmetric metric."""
    matrix = np.asarray(matrix, dtype=float)
    if metric is None:
        return matrix.T
    metric = np.asarray(metric, dtype=float)
    return np.linalg.solve(metric, matrix.T @ metric)


def inverse_adjoint_matrix(matrix: np.ndarray, metric: np.ndarray | None = None) -> np.ndarray:
    """Return the inverse of the adjoint transformation."""
    return np.linalg.inv(adjoint_matrix(matrix, metric))


def transformed_metric(matrix: np.ndarray, metric: np.ndarray | None = None) -> np.ndarray:
    """Metric pulled back to the source coordinates by a linear map."""
    matrix = np.asarray(matrix, dtype=float)
    if metric is None:
        metric = np.eye(matrix.shape[0])
    metric = np.asarray(metric, dtype=float)
    return matrix.T @ metric @ matrix


def bivector_to_normal(bivector: np.ndarray) -> np.ndarray:
    """Dual of a 3-D bivector in ``(e12, e13, e23)`` coordinates."""
    b12, b13, b23 = np.asarray(bivector, dtype=float)
    return np.array([b23, -b13, b12], dtype=float)


def normal_to_bivector(normal: np.ndarray) -> np.ndarray:
    """Inverse of ``bivector_to_normal`` for 3-D Euclidean space."""
    nx, ny, nz = np.asarray(normal, dtype=float)
    return np.array([nz, -ny, nx], dtype=float)


def left_contract_vector_bivector(vector: np.ndarray, bivector: np.ndarray) -> np.ndarray:
    """Compute ``vector contracted into bivector`` in 3-D Euclidean space."""
    a1, a2, a3 = np.asarray(vector, dtype=float)
    b12, b13, b23 = np.asarray(bivector, dtype=float)
    return np.array(
        [
            -a2 * b12 - a3 * b13,
            a1 * b12 - a3 * b23,
            a1 * b13 + a2 * b23,
        ],
        dtype=float,
    )


def normal_transform(matrix: np.ndarray, normal: np.ndarray) -> np.ndarray:
    """Transform a normal vector through the dual-bivector law."""
    matrix = np.asarray(matrix, dtype=float)
    return float(np.linalg.det(matrix)) * np.linalg.solve(matrix.T, np.asarray(normal, dtype=float))


def unit(vector: np.ndarray) -> np.ndarray:
    """Return a unit vector, rejecting near-zero inputs."""
    vector = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(vector))
    if length < EPS:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def project_vector_to_subspace(vector: np.ndarray, basis_vectors: np.ndarray) -> np.ndarray:
    """Orthogonally project a vector onto the span of the basis-vector rows."""
    vector = np.asarray(vector, dtype=float)
    basis_vectors = np.asarray(basis_vectors, dtype=float)
    gram = basis_vectors @ basis_vectors.T
    coefficients = np.linalg.solve(gram, basis_vectors @ vector)
    return coefficients @ basis_vectors


def directional_line_projection(vector: np.ndarray, line: np.ndarray, along: np.ndarray) -> np.ndarray:
    """Project a 2-D vector onto ``span(line)`` along ``along``."""
    frame = np.column_stack([np.asarray(line, dtype=float), np.asarray(along, dtype=float)])
    alpha, _beta = np.linalg.solve(frame, np.asarray(vector, dtype=float))
    return alpha * np.asarray(line, dtype=float)


def scalar_product_blades(left_factors: np.ndarray, right_factors: np.ndarray) -> float:
    """Scalar product of equal-grade blades from their vector factors."""
    left = np.asarray(left_factors, dtype=float)
    right = np.asarray(right_factors, dtype=float)
    if left.shape != right.shape:
        raise ValueError("factor arrays must have matching shape")
    return float(np.linalg.det(left @ right.T))


def orthographic_project(points: np.ndarray) -> np.ndarray:
    """Project 3-D points to a tidy 2-D drawing plane."""
    points = np.asarray(points, dtype=float)
    x = points[..., 0] - 0.45 * points[..., 1]
    y = -0.32 * points[..., 0] - 0.20 * points[..., 1] + 0.95 * points[..., 2]
    return np.stack([x, y], axis=-1)


def _svg_polyline(points: np.ndarray, stroke: str, width: float = 3.0, fill: str = "none", opacity: float = 1.0) -> str:
    encoded = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polygon points="{encoded}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" opacity="{opacity}" />'
    )


def _svg_line(start: np.ndarray, end: np.ndarray, stroke: str, width: float = 3.0, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{start[0]:.2f}" y1="{start[1]:.2f}" x2="{end[0]:.2f}" y2="{end[1]:.2f}" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"{dash_attr} />'
    )


def _svg_circle(center: np.ndarray, radius: float, fill: str, stroke: str = "#111827") -> str:
    return (
        f'<circle cx="{center[0]:.2f}" cy="{center[1]:.2f}" r="{radius:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2" />'
    )


def _fit_points(points: np.ndarray, width: int, height: int, margin: int = 54) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    lo = points.min(axis=0)
    hi = points.max(axis=0)
    span = np.maximum(hi - lo, EPS)
    scale = min((width - 2 * margin) / span[0], (height - 2 * margin) / span[1])
    fitted = (points - (lo + hi) / 2.0) * scale + np.array([width / 2.0, height / 2.0])
    return fitted


def svg_linear_map(matrix: np.ndarray, width: int = 720, height: int = 440) -> str:
    """SVG showing a square and its transformed parallelogram."""
    matrix = np.asarray(matrix, dtype=float)
    square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    mapped = apply_matrix(matrix, square)
    axes = np.array([[-0.25, 0.0], [1.35, 0.0], [0.0, -0.25], [0.0, 1.35]])
    all_points = np.vstack([square, mapped, axes])
    fitted = _fit_points(all_points * np.array([1.0, -1.0]), width, height)
    square_f = fitted[:4]
    mapped_f = fitted[4:8]
    axes_f = fitted[8:]
    det = float(np.linalg.det(matrix))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Linear map of a unit square">
<rect width="100%" height="100%" fill="#f8fafc" />
{_svg_line(axes_f[0], axes_f[1], "#94a3b8", 2)}
{_svg_line(axes_f[2], axes_f[3], "#94a3b8", 2)}
{_svg_polyline(square_f, "#2563eb", 3, "rgba(37,99,235,0.14)", 1)}
{_svg_polyline(mapped_f, "#dc2626", 4, "rgba(220,38,38,0.18)", 1)}
<text x="26" y="34" font-family="Arial, sans-serif" font-size="18" fill="#0f172a">unit square and transformed blade</text>
<text x="26" y="60" font-family="Arial, sans-serif" font-size="14" fill="#334155">det(M) = {det:.3f}</text>
<text x="{square_f[1,0]:.1f}" y="{square_f[1,1]-10:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#2563eb">source</text>
<text x="{mapped_f[1,0]:.1f}" y="{mapped_f[1,1]-10:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#dc2626">image</text>
</svg>"""


def svg_projection_lab(point: np.ndarray, width: int = 760, height: int = 480) -> str:
    """SVG for a 3-D orthogonal projection onto a fixed plane."""
    point = np.asarray(point, dtype=float)
    u = np.array([1.4, 0.15, 0.25])
    v = np.array([0.25, 1.15, -0.15])
    projection = project_vector_to_subspace(point, np.vstack([u, v]))
    normal = unit(np.cross(u, v))
    corners = np.array([-u - v, u - v, u + v, -u + v])
    dropped = np.vstack([point, projection])
    normal_segment = np.vstack([projection, projection + 0.8 * normal])
    scene = np.vstack([corners, dropped, normal_segment])
    flat = orthographic_project(scene)
    fitted = _fit_points(flat * np.array([1.0, -1.0]), width, height)
    corners_f = fitted[:4]
    point_f = fitted[4]
    projection_f = fitted[5]
    normal_f = fitted[6:8]
    distance = float(np.linalg.norm(point - projection))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Projection of a point onto a plane">
<rect width="100%" height="100%" fill="#f8fafc" />
{_svg_polyline(corners_f, "#0891b2", 3, "rgba(8,145,178,0.18)", 1)}
{_svg_line(point_f, projection_f, "#64748b", 3, "8 7")}
{_svg_line(normal_f[0], normal_f[1], "#7c3aed", 4)}
{_svg_circle(point_f, 7, "#f97316")}
{_svg_circle(projection_f, 7, "#10b981")}
<text x="24" y="34" font-family="Arial, sans-serif" font-size="18" fill="#0f172a">orthogonal projection from contraction geometry</text>
<text x="24" y="60" font-family="Arial, sans-serif" font-size="14" fill="#334155">distance to plane = {distance:.3f}</text>
<text x="{point_f[0]+10:.1f}" y="{point_f[1]-8:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#f97316">x</text>
<text x="{projection_f[0]+10:.1f}" y="{projection_f[1]+18:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#059669">proj(x)</text>
</svg>"""


def svg_normal_transform_lab(sx: float = 1.7, sy: float = 0.7, shear: float = 0.45, width: int = 760, height: int = 500) -> str:
    """SVG contrasting direct vector normal transform with the dual-bivector law."""
    triangle = np.array(
        [
            [-0.9, -0.7, 0.2],
            [1.0, -0.4, 0.15],
            [-0.25, 0.95, -0.05],
        ],
        dtype=float,
    )
    matrix = np.array(
        [
            [sx, shear, 0.0],
            [0.0, sy, 0.0],
            [0.0, 0.0, 1.05],
        ],
        dtype=float,
    )
    u = triangle[1] - triangle[0]
    v = triangle[2] - triangle[0]
    bivector = wedge_vectors(u, v)
    normal = unit(bivector_to_normal(bivector))
    mapped = apply_matrix(matrix, triangle)
    center = mapped.mean(axis=0)
    tangent_u = mapped[1] - mapped[0]
    tangent_v = mapped[2] - mapped[0]
    tangent_bivector = wedge_vectors(tangent_u, tangent_v)
    good = unit(bivector_to_normal(tangent_bivector))
    formula_good = unit(normal_transform(matrix, normal))
    if np.dot(good, formula_good) < 0:
        formula_good = -formula_good
    bad = unit(apply_matrix(matrix, normal))
    scale = 0.75
    scene = np.vstack(
        [
            triangle,
            mapped,
            center,
            center + scale * good,
            center,
            center + scale * bad,
        ]
    )
    flat = orthographic_project(scene)
    fitted = _fit_points(flat * np.array([1.0, -1.0]), width, height)
    source_f = fitted[:3]
    mapped_f = fitted[3:6]
    good_f = fitted[6:8]
    bad_f = fitted[8:10]
    good_dot_u = float(abs(np.dot(formula_good, tangent_u)))
    bad_dot_u = float(abs(np.dot(bad, tangent_u)))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Transformed normals on a transformed triangle">
<rect width="100%" height="100%" fill="#f8fafc" />
{_svg_polyline(source_f, "#2563eb", 2, "rgba(37,99,235,0.10)", 0.65)}
{_svg_polyline(mapped_f, "#111827", 4, "rgba(15,23,42,0.12)", 1)}
{_svg_line(good_f[0], good_f[1], "#16a34a", 5)}
{_svg_line(bad_f[0], bad_f[1], "#dc2626", 5)}
<text x="24" y="34" font-family="Arial, sans-serif" font-size="18" fill="#0f172a">normal vectors transform as dual bivectors</text>
<text x="24" y="60" font-family="Arial, sans-serif" font-size="14" fill="#334155">good |n dot tangent| = {good_dot_u:.3e}; direct-vector |n dot tangent| = {bad_dot_u:.3e}</text>
<text x="{good_f[1,0]+10:.1f}" y="{good_f[1,1]:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#16a34a">dual law</text>
<text x="{bad_f[1,0]+10:.1f}" y="{bad_f[1,1]:.1f}" font-family="Arial, sans-serif" font-size="14" fill="#dc2626">direct map</text>
</svg>"""


@dataclass(frozen=True)
class CheckResult:
    """Small record for invariant-check summaries."""

    name: str
    passed: bool
    residual: float


def run_invariant_checks() -> list[CheckResult]:
    """Run numerical checks for the chapter notebook."""
    checks: list[CheckResult] = []

    matrix = np.array([[1.2, -0.35, 0.15], [0.25, 0.9, -0.2], [0.05, 0.4, 1.1]], dtype=float)
    other = np.array([[0.8, 0.1, -0.25], [-0.15, 1.1, 0.3], [0.2, -0.05, 0.95]], dtype=float)
    a = np.array([0.7, -0.2, 1.1])
    b = np.array([-0.4, 0.9, 0.25])
    c = np.array([1.0, 0.35, -0.6])

    lhs = wedge_vectors(apply_matrix(matrix, a), apply_matrix(matrix, b))
    rhs = exterior_power_matrix(matrix, 2) @ wedge_vectors(a, b)
    residual = float(np.linalg.norm(lhs - rhs))
    checks.append(CheckResult("outermorphism preserves wedge", residual < 1e-9, residual))

    volume_source = wedge_vectors(a, b, c)[0]
    volume_image = wedge_vectors(apply_matrix(matrix, a), apply_matrix(matrix, b), apply_matrix(matrix, c))[0]
    residual = abs(volume_image - np.linalg.det(matrix) * volume_source)
    checks.append(CheckResult("determinant scales trivectors", bool(residual < 1e-9), float(residual)))

    adj = adjoint_matrix(matrix)
    residual = abs(np.dot(apply_matrix(matrix, a), b) - np.dot(a, apply_matrix(adj, b)))
    checks.append(CheckResult("adjoint transfers scalar product", bool(residual < 1e-9), float(residual)))

    pullback = transformed_metric(matrix)
    residual = abs(np.dot(apply_matrix(matrix, a), apply_matrix(matrix, b)) - a @ pullback @ b)
    checks.append(CheckResult("transformed scalar product uses pullback metric", bool(residual < 1e-9), float(residual)))

    bivector = wedge_vectors(b, c)
    left = apply_matrix(matrix, left_contract_vector_bivector(a, bivector))
    right = left_contract_vector_bivector(inverse_adjoint_matrix(matrix) @ a, exterior_power_matrix(matrix, 2) @ bivector)
    residual = float(np.linalg.norm(left - right))
    checks.append(CheckResult("contraction transform needs inverse adjoint", residual < 1e-9, residual))

    source_normal = bivector_to_normal(bivector)
    transformed_bivector = exterior_power_matrix(matrix, 2) @ bivector
    left = bivector_to_normal(transformed_bivector)
    right = normal_transform(matrix, source_normal)
    residual = float(np.linalg.norm(left - right))
    checks.append(CheckResult("dual bivectors transform normals", residual < 1e-9, residual))

    left = exterior_power_matrix(matrix @ other, 2)
    right = exterior_power_matrix(matrix, 2) @ exterior_power_matrix(other, 2)
    residual = float(np.linalg.norm(left - right))
    checks.append(CheckResult("outermorphism matrices compose", residual < 1e-9, residual))

    return checks


def checks_as_dicts(checks: list[CheckResult]) -> list[dict[str, float | str | bool]]:
    """JSON-friendly representation of invariant checks."""
    return [{"name": item.name, "passed": item.passed, "residual": item.residual} for item in checks]
