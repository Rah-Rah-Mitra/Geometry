"""Chapter 11 helpers for homogeneous-model notebooks.

The arrays in this module use the coordinate order ``[x, y, w]`` in 2-D
homogeneous space and ``[x, y, z, w]`` in 3-D homogeneous space. That is the
standard column-vector convention for computer graphics; the textbook's
distinguished vector ``e0`` is represented by the final coordinate.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import cos, sin
from typing import Iterable

import numpy as np

EPS = 1e-10


def normalize(vector: Iterable[float] | np.ndarray, *, tol: float = EPS) -> np.ndarray:
    """Return a Euclidean unit vector."""
    value = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(value))
    if length <= tol:
        raise ValueError("cannot normalize a near-zero vector")
    return value / length


def hpoint2(x: float, y: float, w: float = 1.0) -> np.ndarray:
    """Return a homogeneous point in the projective plane."""
    return np.array([float(x), float(y), float(w)], dtype=float)


def hpoint3(x: float, y: float, z: float, w: float = 1.0) -> np.ndarray:
    """Return a homogeneous point in projective 3-space."""
    return np.array([float(x), float(y), float(z), float(w)], dtype=float)


def point_at_infinity2(direction: Iterable[float] | np.ndarray) -> np.ndarray:
    """Return the improper point that carries a 2-D direction."""
    direction = np.asarray(direction, dtype=float)
    if direction.shape != (2,):
        raise ValueError("direction must be a 2-vector")
    if np.linalg.norm(direction) <= EPS:
        raise ValueError("direction cannot be zero")
    return np.array([direction[0], direction[1], 0.0], dtype=float)


def point_at_infinity3(direction: Iterable[float] | np.ndarray) -> np.ndarray:
    """Return the improper point that carries a 3-D direction."""
    direction = np.asarray(direction, dtype=float)
    if direction.shape != (3,):
        raise ValueError("direction must be a 3-vector")
    if np.linalg.norm(direction) <= EPS:
        raise ValueError("direction cannot be zero")
    return np.array([direction[0], direction[1], direction[2], 0.0], dtype=float)


def weight(point: Iterable[float] | np.ndarray) -> float:
    """Return the homogeneous weight of a point representative."""
    return float(np.asarray(point, dtype=float)[-1])


def is_infinite(point: Iterable[float] | np.ndarray, *, tol: float = EPS) -> bool:
    """Return whether a homogeneous point has zero weight."""
    return abs(weight(point)) <= tol


def affine_location(point: Iterable[float] | np.ndarray, *, tol: float = EPS) -> np.ndarray:
    """Return the Euclidean location represented by a finite homogeneous point."""
    point = np.asarray(point, dtype=float)
    w = float(point[-1])
    if abs(w) <= tol:
        raise ZeroDivisionError("point at infinity has no finite affine location")
    return point[:-1] / w


def normalize_hpoint(point: Iterable[float] | np.ndarray, *, tol: float = EPS) -> np.ndarray:
    """Scale a finite homogeneous point to unit weight."""
    point = np.asarray(point, dtype=float)
    return np.r_[affine_location(point, tol=tol), 1.0]


def weighted_average(points: Iterable[Iterable[float] | np.ndarray]) -> np.ndarray:
    """Add homogeneous point representatives and normalize the finite result."""
    total = np.sum(np.asarray(list(points), dtype=float), axis=0)
    return normalize_hpoint(total)


def join_points(point_a: Iterable[float], point_b: Iterable[float]) -> np.ndarray:
    """Return the dual line through two 2-D homogeneous points."""
    line = np.cross(np.asarray(point_a, dtype=float), np.asarray(point_b, dtype=float))
    if np.linalg.norm(line) <= EPS:
        raise ValueError("two distinct points are required to define a line")
    return line


def meet_lines(line_a: Iterable[float], line_b: Iterable[float]) -> np.ndarray:
    """Return the homogeneous point where two 2-D lines meet."""
    point = np.cross(np.asarray(line_a, dtype=float), np.asarray(line_b, dtype=float))
    if np.linalg.norm(point) <= EPS:
        raise ValueError("two distinct lines are required to define a meet")
    return point


def point_line_residual(point: Iterable[float], line: Iterable[float]) -> float:
    """Evaluate the point-line incidence equation."""
    return float(np.asarray(line, dtype=float) @ np.asarray(point, dtype=float))


def line_direction(line: Iterable[float]) -> np.ndarray:
    """Return a Euclidean direction vector for a 2-D line."""
    a, b, _c = np.asarray(line, dtype=float)
    return normalize(np.array([-b, a], dtype=float))


def line_offset(line: Iterable[float]) -> float:
    """Return the signed offset of a normalized 2-D line from the origin."""
    a, b, c = np.asarray(line, dtype=float)
    scale = float(np.hypot(a, b))
    if scale <= EPS:
        raise ValueError("invalid finite line")
    return c / scale


def line_through_point_direction(point: Iterable[float], direction: Iterable[float]) -> np.ndarray:
    """Construct a 2-D line from a finite point and an improper direction."""
    return join_points(point, point_at_infinity2(direction))


def parallel_line_through(point: Iterable[float], line: Iterable[float]) -> np.ndarray:
    """Return the line through ``point`` with the same direction as ``line``."""
    return join_points(point, point_at_infinity2(line_direction(line)))


def blade_basis(dimension: int, grade: int) -> list[tuple[int, ...]]:
    """Return ordered basis-index tuples for k-blades in R^n."""
    if grade < 0 or grade > dimension:
        return []
    return list(combinations(range(dimension), grade))


def wedge_coordinates(*vectors: Iterable[float] | np.ndarray) -> np.ndarray:
    """Return Plucker-style coordinates of the blade spanned by vectors."""
    if not vectors:
        return np.array([1.0])
    matrix = np.column_stack([np.asarray(vector, dtype=float) for vector in vectors])
    dimension, grade = matrix.shape
    return np.array(
        [
            float(np.linalg.det(matrix[np.ix_(rows, range(grade))]))
            for rows in blade_basis(dimension, grade)
        ],
        dtype=float,
    )


def exterior_power_matrix(matrix: Iterable[Iterable[float]] | np.ndarray, grade: int) -> np.ndarray:
    """Return the grade-k outermorphism matrix induced by a linear map."""
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
        result[:, col] = wedge_coordinates(*image_vectors)
    return result


def affine2(linear: Iterable[Iterable[float]], translation: Iterable[float]) -> np.ndarray:
    """Return a 2-D homogeneous affine matrix for column vectors."""
    linear = np.asarray(linear, dtype=float)
    translation = np.asarray(translation, dtype=float)
    if linear.shape != (2, 2) or translation.shape != (2,):
        raise ValueError("expected a 2x2 linear part and 2-vector translation")
    matrix = np.eye(3)
    matrix[:2, :2] = linear
    matrix[:2, 2] = translation
    return matrix


def translation2(dx: float, dy: float) -> np.ndarray:
    """Return a 2-D homogeneous translation matrix."""
    return affine2(np.eye(2), np.array([dx, dy], dtype=float))


def rotation2(angle: float) -> np.ndarray:
    """Return a 2-D homogeneous rotation about the origin."""
    c = cos(angle)
    s = sin(angle)
    return affine2(np.array([[c, -s], [s, c]], dtype=float), np.zeros(2))


def scale2(sx: float, sy: float) -> np.ndarray:
    """Return a 2-D homogeneous anisotropic scale."""
    return affine2(np.diag([float(sx), float(sy)]), np.zeros(2))


def apply_homography(matrix: Iterable[Iterable[float]], points: np.ndarray) -> np.ndarray:
    """Apply a homogeneous matrix to one point or a row stack of points."""
    matrix = np.asarray(matrix, dtype=float)
    points = np.asarray(points, dtype=float)
    if points.ndim == 1:
        return matrix @ points
    return points @ matrix.T


def transform_line_dual(matrix: Iterable[Iterable[float]], line: Iterable[float]) -> np.ndarray:
    """Transform a dual line by the inverse-adjoint rule."""
    matrix = np.asarray(matrix, dtype=float)
    return np.linalg.solve(matrix.T, np.asarray(line, dtype=float))


def transform_conic(matrix: Iterable[Iterable[float]], conic: Iterable[Iterable[float]]) -> np.ndarray:
    """Transform a point conic ``x.T C x = 0`` by a homography."""
    matrix = np.asarray(matrix, dtype=float)
    conic = np.asarray(conic, dtype=float)
    inverse = np.linalg.inv(matrix)
    return inverse.T @ conic @ inverse


def projective_tilt2(ax: float, ay: float) -> np.ndarray:
    """Return a simple non-affine homography whose last row changes weight."""
    return np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [float(ax), float(ay), 1.0]])


def homogeneous_inner_points(
    point_a: Iterable[float],
    point_b: Iterable[float],
    *,
    e0_square: float = 1.0,
) -> float:
    """Naive inner product in the representation space for two point vectors."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("points must have matching dimensions")
    return float(a[:-1] @ b[:-1] + e0_square * a[-1] * b[-1])


def euclidean_distance(point_a: Iterable[float], point_b: Iterable[float]) -> float:
    """Return the Euclidean distance between finite homogeneous points."""
    return float(np.linalg.norm(affine_location(point_a) - affine_location(point_b)))


def basis_coordinates_on_line(
    basis_a: Iterable[float],
    basis_b: Iterable[float],
    point: Iterable[float],
) -> tuple[float, float]:
    """Express a collinear homogeneous point in the projective basis ``A, B``."""
    frame = np.column_stack([np.asarray(basis_a, dtype=float), np.asarray(basis_b, dtype=float)])
    coefficients, *_ = np.linalg.lstsq(frame, np.asarray(point, dtype=float), rcond=None)
    residual = np.linalg.norm(frame @ coefficients - np.asarray(point, dtype=float))
    if residual > 1e-7:
        raise ValueError("point is not on the projective line spanned by the basis points")
    return float(coefficients[0]), float(coefficients[1])


def cross_ratio_collinear(
    point_a: Iterable[float],
    point_b: Iterable[float],
    point_c: Iterable[float],
    point_d: Iterable[float],
    *,
    tol: float = EPS,
) -> float:
    """Return the projective cross ratio ``(A, B; C, D)`` for collinear points."""
    alpha_c, beta_c = basis_coordinates_on_line(point_a, point_b, point_c)
    alpha_d, beta_d = basis_coordinates_on_line(point_a, point_b, point_d)
    if abs(alpha_c) <= tol or abs(alpha_d) <= tol or abs(beta_d) <= tol:
        raise ZeroDivisionError("chosen cross-ratio basis produced a point at a pole")
    return float((beta_c / alpha_c) / (beta_d / alpha_d))


def conic_from_five_points(points: Iterable[Iterable[float]]) -> np.ndarray:
    """Fit the exact homogeneous conic through five points."""
    rows = []
    for point in points:
        x, y, w = np.asarray(point, dtype=float)
        rows.append([x * x, 2 * x * y, 2 * x * w, y * y, 2 * y * w, w * w])
    matrix = np.asarray(rows, dtype=float)
    if matrix.shape != (5, 6):
        raise ValueError("exact conic construction requires five points")
    *_u, _values, vh = np.linalg.svd(matrix)
    coeff = vh[-1]
    conic = np.array(
        [
            [coeff[0], coeff[1], coeff[2]],
            [coeff[1], coeff[3], coeff[4]],
            [coeff[2], coeff[4], coeff[5]],
        ],
        dtype=float,
    )
    scale = float(np.linalg.norm(conic))
    if scale <= EPS:
        raise ValueError("degenerate conic fit")
    return conic / scale


def evaluate_conic(conic: Iterable[Iterable[float]], points: np.ndarray) -> np.ndarray:
    """Evaluate ``x.T C x`` for one point or a row stack of points."""
    conic = np.asarray(conic, dtype=float)
    points = np.asarray(points, dtype=float)
    if points.ndim == 1:
        return np.array(float(points @ conic @ points))
    return np.einsum("...i,ij,...j->...", points, conic, points)


def conic_grid(
    conic: Iterable[Iterable[float]],
    *,
    bounds: tuple[float, float, float, float] = (-3.0, 3.0, -2.5, 2.5),
    resolution: int = 320,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a finite affine grid for contouring a conic."""
    xmin, xmax, ymin, ymax = bounds
    xs = np.linspace(xmin, xmax, resolution)
    ys = np.linspace(ymin, ymax, resolution)
    xx, yy = np.meshgrid(xs, ys)
    points = np.stack([xx, yy, np.ones_like(xx)], axis=-1)
    return xx, yy, evaluate_conic(conic, points)


@dataclass(frozen=True)
class PluckerLine:
    """A 3-D line represented by direction and moment coordinates."""

    direction: np.ndarray
    moment: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(self, "direction", np.asarray(self.direction, dtype=float))
        object.__setattr__(self, "moment", np.asarray(self.moment, dtype=float))
        if self.direction.shape != (3,) or self.moment.shape != (3,):
            raise ValueError("Plucker direction and moment must be 3-vectors")

    def side_operator(self) -> float:
        """Return the Plucker validity scalar ``direction dot moment``."""
        return float(self.direction @ self.moment)


def plucker_from_points(point_a: Iterable[float], point_b: Iterable[float]) -> PluckerLine:
    """Return direction and moment for the oriented line through two finite 3-D points."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    direction = b - a
    if np.linalg.norm(direction) <= EPS:
        raise ValueError("two distinct points are required")
    moment = np.cross(a, direction)
    return PluckerLine(direction, moment)


def plucker_closest_to_origin(line: PluckerLine) -> np.ndarray:
    """Return the point on a Plucker line closest to the origin."""
    denom = float(line.direction @ line.direction)
    if denom <= EPS:
        raise ValueError("line has zero direction")
    return np.cross(line.direction, line.moment) / denom


@dataclass(frozen=True)
class Plane3D:
    """A finite 3-D plane represented by ``normal dot x = offset``."""

    normal: np.ndarray
    offset: float

    def __post_init__(self) -> None:
        normal = np.asarray(self.normal, dtype=float)
        length = float(np.linalg.norm(normal))
        if length <= EPS:
            raise ValueError("plane normal cannot be zero")
        object.__setattr__(self, "normal", normal / length)
        object.__setattr__(self, "offset", float(self.offset) / length)

    def residual(self, point: Iterable[float]) -> float:
        """Evaluate signed point-plane incidence for a finite 3-D point."""
        return float(self.normal @ np.asarray(point, dtype=float) - self.offset)

    def point(self) -> np.ndarray:
        """Return the plane point nearest the origin."""
        return self.offset * self.normal

    def frame(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return an origin point and two orthonormal in-plane axes."""
        reference = np.array([1.0, 0.0, 0.0])
        if abs(reference @ self.normal) > 0.85:
            reference = np.array([0.0, 1.0, 0.0])
        u = normalize(np.cross(self.normal, reference))
        v = normalize(np.cross(self.normal, u))
        return self.point(), u, v


def plane_from_points(point_a: Iterable[float], point_b: Iterable[float], point_c: Iterable[float]) -> Plane3D:
    """Return the plane through three finite 3-D points."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    c = np.asarray(point_c, dtype=float)
    normal = np.cross(b - a, c - a)
    return Plane3D(normal, float(normal @ a))


def plane_dual_vector(plane: Plane3D) -> np.ndarray:
    """Return dual plane coordinates ``[nx, ny, nz, -offset]``."""
    return np.r_[plane.normal, -plane.offset]


def point_plane_residual(point: Iterable[float], plane_dual: Iterable[float]) -> float:
    """Evaluate homogeneous point-plane incidence in 3-D."""
    return float(np.asarray(plane_dual, dtype=float) @ np.asarray(point, dtype=float))


def line_plane_intersection(
    point_a: Iterable[float],
    point_b: Iterable[float],
    plane: Plane3D,
    *,
    tol: float = EPS,
) -> tuple[str, np.ndarray | None, float | None]:
    """Classify and meet a finite 3-D line segment carrier with a plane."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    direction = b - a
    denom = float(plane.normal @ direction)
    signed = plane.residual(a)
    if abs(denom) <= tol:
        return ("contained" if abs(signed) <= tol else "parallel", None, None)
    t = -signed / denom
    return "point", a + t * direction, float(t)


def plane_project(point: Iterable[float], plane: Plane3D) -> tuple[np.ndarray, np.ndarray]:
    """Return the closest plane point and its 2-D coordinates in a plane frame."""
    point = np.asarray(point, dtype=float)
    origin, u, v = plane.frame()
    projected = point - plane.residual(point) * plane.normal
    coords = np.array([(projected - origin) @ u, (projected - origin) @ v], dtype=float)
    return projected, coords


def cube_vertices(size: float = 1.0, center: Iterable[float] = (0.0, 0.0, 0.0)) -> np.ndarray:
    """Return vertices of a cube used for projection examples."""
    c = np.asarray(center, dtype=float)
    s = float(size) / 2.0
    vertices = []
    for x in (-s, s):
        for y in (-s, s):
            for z in (-s, s):
                vertices.append(c + np.array([x, y, z], dtype=float))
    return np.asarray(vertices)


def cube_edges() -> list[tuple[int, int]]:
    """Return edge indices matching ``cube_vertices`` ordering."""
    edges: list[tuple[int, int]] = []
    vertices = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)])
    for i, a in enumerate(vertices):
        for j, b in enumerate(vertices):
            if i < j and np.sum(np.abs(a - b)) == 1:
                edges.append((i, j))
    return edges


def perspective_project_points(
    points: np.ndarray,
    camera: Iterable[float],
    plane: Plane3D,
    *,
    tol: float = EPS,
) -> tuple[np.ndarray, np.ndarray]:
    """Project 3-D points from a camera center onto a finite image plane."""
    points = np.asarray(points, dtype=float)
    camera = np.asarray(camera, dtype=float)
    origin, u, v = plane.frame()
    projected = []
    plane_coords = []
    for point in points:
        direction = point - camera
        denom = float(plane.normal @ direction)
        if abs(denom) <= tol:
            projected.append(np.full(3, np.nan))
            plane_coords.append(np.full(2, np.nan))
            continue
        t = (plane.offset - float(plane.normal @ camera)) / denom
        hit = camera + t * direction
        projected.append(hit)
        plane_coords.append(np.array([(hit - origin) @ u, (hit - origin) @ v], dtype=float))
    return np.asarray(projected), np.asarray(plane_coords)


def orthographic_project_points(points: np.ndarray, plane: Plane3D) -> tuple[np.ndarray, np.ndarray]:
    """Orthogonally project 3-D points onto a finite image plane."""
    projected = []
    coords = []
    for point in np.asarray(points, dtype=float):
        hit, uv = plane_project(point, plane)
        projected.append(hit)
        coords.append(uv)
    return np.asarray(projected), np.asarray(coords)


def finite_polygon_area(points: np.ndarray) -> float:
    """Return signed area of a 2-D polygon."""
    points = np.asarray(points, dtype=float)
    x = points[:, 0]
    y = points[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))
