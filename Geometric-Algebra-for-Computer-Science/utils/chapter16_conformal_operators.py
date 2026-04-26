"""Numerical helpers for the Chapter 16 conformal-operators notebook.

The notebook stays deliberately lightweight: it uses Euclidean formulas and a small
matrix model of conformal points to make Chapter 16's operators inspectable.  The
conformal coordinate order used here is ``[e1, e2, no, ni]`` with ``no.ni = -1``.
Finite points are embedded as ``x + no + 0.5*|x|^2*ni`` and recovered by dividing
the Euclidean coordinates by the point weight, the ``no`` coefficient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

EPS = 1e-10

METRIC_2D = np.array(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.0],
        [0.0, 0.0, -1.0, 0.0],
    ],
    dtype=float,
)


@dataclass(frozen=True)
class Circle2D:
    """A Euclidean circle represented by center and radius."""

    center: np.ndarray
    radius: float

    def sample(self, count: int = 240, *, start: float = 0.0, stop: float = 2.0 * np.pi) -> np.ndarray:
        """Return points on the circle."""
        theta = np.linspace(start, stop, count)
        return self.center + self.radius * np.column_stack((np.cos(theta), np.sin(theta)))


def as_point2(point: Iterable[float]) -> np.ndarray:
    """Return ``point`` as a finite 2-D float array."""
    array = np.asarray(point, dtype=float)
    if array.shape != (2,):
        raise ValueError("expected a 2-D point")
    return array


def as_points2(points: Iterable[Iterable[float]]) -> np.ndarray:
    """Return ``points`` as an ``(n, 2)`` float array."""
    array = np.asarray(points, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("expected an array with shape (n, 2)")
    return array


def normalize(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Return a unit vector."""
    array = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(array))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return array / length


def rotation2(angle: float) -> np.ndarray:
    """Return the 2-D rotation matrix for ``angle`` radians."""
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    return np.array([[c, -s], [s, c]], dtype=float)


def conformal_point(point: Iterable[float]) -> np.ndarray:
    """Embed a 2-D Euclidean point as a null conformal point vector."""
    point = as_point2(point)
    return np.array(
        [point[0], point[1], 1.0, 0.5 * float(np.dot(point, point))],
        dtype=float,
    )


def conformal_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the conformal inner product in the local 2-D model."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != (4,) or b.shape != (4,):
        raise ValueError("conformal vectors must have four coordinates")
    return float(a @ METRIC_2D @ b)


def conformal_norm2(vector: Iterable[float]) -> float:
    """Return the conformal squared norm."""
    return conformal_inner(vector, vector)


def point_weight(vector: Iterable[float]) -> float:
    """Return the finite point weight, equal to the ``no`` coefficient here."""
    vector = np.asarray(vector, dtype=float)
    if vector.shape != (4,):
        raise ValueError("conformal vectors must have four coordinates")
    return float(vector[2])


def recover_point(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Recover Euclidean coordinates from a weighted conformal point vector."""
    vector = np.asarray(vector, dtype=float)
    weight = point_weight(vector)
    if abs(weight) <= eps:
        raise ZeroDivisionError("cannot recover a finite point from zero weight")
    return vector[:2] / weight


def embed_points(points: Iterable[Iterable[float]]) -> np.ndarray:
    """Embed many Euclidean points as conformal point vectors."""
    points = as_points2(points)
    squared = np.sum(points * points, axis=1)
    return np.column_stack((points, np.ones(len(points)), 0.5 * squared))


def recover_points(vectors: Iterable[Iterable[float]], *, eps: float = EPS) -> np.ndarray:
    """Recover many Euclidean points from weighted conformal vectors."""
    vectors = np.asarray(vectors, dtype=float)
    if vectors.ndim != 2 or vectors.shape[1] != 4:
        raise ValueError("expected an array with shape (n, 4)")
    weights = vectors[:, 2]
    if np.any(np.abs(weights) <= eps):
        raise ZeroDivisionError("cannot recover finite points from zero weights")
    return vectors[:, :2] / weights[:, None]


def distance_squared_from_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Recover squared Euclidean distance from embedded point vectors."""
    a_vec = conformal_point(a) if np.asarray(a).shape == (2,) else np.asarray(a, dtype=float)
    b_vec = conformal_point(b) if np.asarray(b).shape == (2,) else np.asarray(b, dtype=float)
    a_norm = a_vec / point_weight(a_vec)
    b_norm = b_vec / point_weight(b_vec)
    return float(-2.0 * conformal_inner(a_norm, b_norm))


def metric_error(matrix: Iterable[Iterable[float]]) -> float:
    """Return ``||M.T*G*M - G||`` for the local conformal metric matrix."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError("expected a 4-by-4 matrix")
    return float(np.linalg.norm(matrix.T @ METRIC_2D @ matrix - METRIC_2D))


def translation_matrix(offset: Iterable[float]) -> np.ndarray:
    """Return the conformal matrix for ``x -> x + offset``."""
    offset = as_point2(offset)
    matrix = np.zeros((4, 4), dtype=float)
    matrix[:2, :2] = np.eye(2)
    matrix[:2, 2] = offset
    matrix[2, 2] = 1.0
    matrix[3, :2] = offset
    matrix[3, 2] = 0.5 * float(np.dot(offset, offset))
    matrix[3, 3] = 1.0
    return matrix


def scaling_matrix(scale: float) -> np.ndarray:
    """Return the conformal matrix for positive dilation ``x -> scale*x``."""
    scale = float(scale)
    if scale <= 0.0:
        raise ValueError("scale must be positive")
    matrix = np.eye(4, dtype=float)
    matrix[2, 2] = 1.0 / scale
    matrix[3, 3] = scale
    return matrix


def rotation_matrix(angle: float) -> np.ndarray:
    """Return the conformal matrix for a Euclidean rotation around the origin."""
    matrix = np.eye(4, dtype=float)
    matrix[:2, :2] = rotation2(angle)
    return matrix


def apply_conformal_matrix(matrix: Iterable[Iterable[float]], points: Iterable[Iterable[float]]) -> np.ndarray:
    """Apply a local conformal matrix to Euclidean points and recover finite coordinates."""
    matrix = np.asarray(matrix, dtype=float)
    embedded = embed_points(points)
    transformed = embedded @ matrix.T
    return recover_points(transformed)


def similarity_matrix(scale: float, angle: float, translation: Iterable[float]) -> np.ndarray:
    """Return the conformal matrix for ``x -> scale*R*x + translation``."""
    return translation_matrix(translation) @ scaling_matrix(scale) @ rotation_matrix(angle)


def similarity_points(
    points: Iterable[Iterable[float]],
    *,
    scale: float = 1.0,
    angle: float = 0.0,
    translation: Iterable[float] = (0.0, 0.0),
) -> np.ndarray:
    """Apply a positive scale, rotation, and translation to Euclidean points."""
    return apply_conformal_matrix(similarity_matrix(scale, angle, translation), points)


def invert_points(
    points: Iterable[Iterable[float]],
    *,
    center: Iterable[float] = (0.0, 0.0),
    radius: float = 1.0,
    eps: float = EPS,
) -> np.ndarray:
    """Invert points in a circle/sphere, using the 2-D cross-section formula."""
    points = as_points2(points)
    center = as_point2(center)
    radius = float(radius)
    if radius <= 0:
        raise ValueError("radius must be positive")
    shifted = points - center
    squared = np.sum(shifted * shifted, axis=1)
    if np.any(squared <= eps):
        raise ZeroDivisionError("cannot invert the center of inversion")
    return center + (radius * radius) * shifted / squared[:, None]


def inversion_jacobian(
    point: Iterable[float],
    *,
    center: Iterable[float] = (0.0, 0.0),
    radius: float = 1.0,
    eps: float = EPS,
) -> np.ndarray:
    """Return the Jacobian of circle inversion at a finite point."""
    point = as_point2(point)
    center = as_point2(center)
    shifted = point - center
    squared = float(np.dot(shifted, shifted))
    if squared <= eps:
        raise ZeroDivisionError("cannot differentiate inversion at its center")
    unit = shifted / np.sqrt(squared)
    return (float(radius) ** 2 / squared) * (np.eye(2) - 2.0 * np.outer(unit, unit))


def fit_circle(points: Iterable[Iterable[float]]) -> Circle2D:
    """Least-squares fit a circle to 2-D points."""
    points = as_points2(points)
    x = points[:, 0]
    y = points[:, 1]
    design = np.column_stack((2.0 * x, 2.0 * y, np.ones(len(points))))
    rhs = x * x + y * y
    cx, cy, constant = np.linalg.lstsq(design, rhs, rcond=None)[0]
    radius = float(np.sqrt(max(constant + cx * cx + cy * cy, 0.0)))
    return Circle2D(np.array([float(cx), float(cy)]), radius)


def circle_residual(points: Iterable[Iterable[float]], circle: Circle2D) -> float:
    """Return the maximum absolute radial residual for points against ``circle``."""
    points = as_points2(points)
    distances = np.linalg.norm(points - circle.center, axis=1)
    return float(np.max(np.abs(distances - circle.radius)))


def line_points(
    point: Iterable[float],
    direction: Iterable[float],
    parameters: Iterable[float],
) -> np.ndarray:
    """Sample points on a Euclidean line."""
    point = as_point2(point)
    direction = normalize(direction)
    parameters = np.asarray(parameters, dtype=float)
    return point + parameters[:, None] * direction[None, :]


def grid_segments(extent: float = 2.5, count: int = 9, samples: int = 160) -> list[np.ndarray]:
    """Return horizontal and vertical line segments used for inversion plots."""
    values = np.linspace(-extent, extent, count)
    t = np.linspace(-extent, extent, samples)
    segments: list[np.ndarray] = []
    for value in values:
        segments.append(np.column_stack((t, np.full_like(t, value))))
        segments.append(np.column_stack((np.full_like(t, value), t)))
    return segments


def safe_invert_segments(
    segments: Iterable[np.ndarray],
    *,
    center: Iterable[float] = (0.0, 0.0),
    radius: float = 1.0,
    min_distance: float = 0.08,
) -> list[np.ndarray]:
    """Invert line segments, dropping samples too close to the inversion center."""
    center = as_point2(center)
    inverted: list[np.ndarray] = []
    for segment in segments:
        segment = as_points2(segment)
        keep = np.linalg.norm(segment - center, axis=1) > min_distance
        kept_indices = np.flatnonzero(keep)
        if len(kept_indices) < 2:
            continue
        split_points = np.where(np.diff(kept_indices) > 1)[0] + 1
        for run in np.split(kept_indices, split_points):
            if len(run) >= 2:
                inverted.append(invert_points(segment[run], center=center, radius=radius))
    return inverted


def iterate_similarity(
    points: Iterable[Iterable[float]],
    *,
    scale: float,
    angle: float,
    translation: Iterable[float],
    steps: int,
) -> list[np.ndarray]:
    """Return the orbit obtained by repeatedly applying one similarity."""
    current = as_points2(points)
    matrix = similarity_matrix(scale, angle, translation)
    orbit = [current]
    for _ in range(steps):
        current = apply_conformal_matrix(matrix, current)
        orbit.append(current)
    return orbit


def transversion_points(
    points: Iterable[Iterable[float]],
    vector: Iterable[float],
    *,
    eps: float = EPS,
) -> np.ndarray:
    """Apply the special conformal map obtained by inversion-translation-inversion."""
    points = as_points2(points)
    vector = as_point2(vector)
    squared = np.sum(points * points, axis=1)
    denominator = 1.0 + 2.0 * (points @ vector) + float(np.dot(vector, vector)) * squared
    if np.any(np.abs(denominator) <= eps):
        raise ZeroDivisionError("transversion sends at least one sample too close to infinity")
    return (points + squared[:, None] * vector[None, :]) / denominator[:, None]


def loxodrome_plane(theta: Iterable[float], growth: float = 0.18) -> np.ndarray:
    """Return a logarithmic spiral in the stereographic plane."""
    theta = np.asarray(theta, dtype=float)
    radius = np.exp(float(growth) * theta)
    return np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))


def inverse_stereographic(points: Iterable[Iterable[float]]) -> np.ndarray:
    """Map plane points to the unit sphere by inverse stereographic projection."""
    points = as_points2(points)
    x = points[:, 0]
    y = points[:, 1]
    r2 = x * x + y * y
    denom = 1.0 + r2
    return np.column_stack((2.0 * x / denom, 2.0 * y / denom, (r2 - 1.0) / denom))


def stereographic(points: Iterable[Iterable[float]], *, eps: float = EPS) -> np.ndarray:
    """Project unit-sphere points from the north pole to the plane ``z=0``."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("expected an array with shape (n, 3)")
    denom = 1.0 - points[:, 2]
    if np.any(np.abs(denom) <= eps):
        raise ZeroDivisionError("cannot project the north pole")
    return points[:, :2] / denom[:, None]


def loxodrome_sphere(theta: Iterable[float], growth: float = 0.18) -> np.ndarray:
    """Return a loxodrome on the unit sphere via a logarithmic spiral."""
    return inverse_stereographic(loxodrome_plane(theta, growth))


def loxodrome_bearing_angles(theta: Iterable[float], growth: float = 0.18) -> np.ndarray:
    """Return tangent-to-meridian angles for a loxodrome sampled by longitude."""
    theta = np.asarray(theta, dtype=float)
    points = loxodrome_sphere(theta, growth)
    tangents = np.gradient(points, theta, axis=0)
    meridian = np.column_stack(
        (
            -points[:, 2] * np.cos(theta),
            -points[:, 2] * np.sin(theta),
            1.0 - points[:, 2] * points[:, 2],
        )
    )
    meridian /= np.linalg.norm(meridian, axis=1)[:, None]
    tangents /= np.linalg.norm(tangents, axis=1)[:, None]
    dots = np.clip(np.sum(tangents * meridian, axis=1), -1.0, 1.0)
    return np.arccos(np.abs(dots))


def sphere_mesh(count_u: int = 64, count_v: int = 32) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mesh coordinates for a unit sphere."""
    u = np.linspace(0.0, 2.0 * np.pi, count_u)
    v = np.linspace(0.0, np.pi, count_v)
    uu, vv = np.meshgrid(u, v)
    x = np.cos(uu) * np.sin(vv)
    y = np.sin(uu) * np.sin(vv)
    z = np.cos(vv)
    return x, y, z


def torus_mesh(
    *,
    major_radius: float = 1.7,
    minor_radius: float = 0.35,
    count_u: int = 96,
    count_v: int = 28,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a torus mesh, interpreted as a circular orbit of a circle."""
    u = np.linspace(0.0, 2.0 * np.pi, count_u)
    v = np.linspace(0.0, 2.0 * np.pi, count_v)
    uu, vv = np.meshgrid(u, v)
    x = (major_radius + minor_radius * np.cos(vv)) * np.cos(uu)
    y = (major_radius + minor_radius * np.cos(vv)) * np.sin(uu)
    z = minor_radius * np.sin(vv)
    return x, y, z


def torus_orbit_circles(
    *,
    major_radius: float = 1.7,
    minor_radius: float = 0.35,
    count: int = 12,
    samples: int = 120,
) -> list[np.ndarray]:
    """Return a family of circles whose orbit sweeps a torus."""
    circles = []
    v = np.linspace(0.0, 2.0 * np.pi, samples)
    for angle in np.linspace(0.0, 2.0 * np.pi, count, endpoint=False):
        radial = np.array([np.cos(angle), np.sin(angle), 0.0])
        vertical = np.array([0.0, 0.0, 1.0])
        center = major_radius * radial
        circles.append(center + minor_radius * (np.cos(v)[:, None] * radial + np.sin(v)[:, None] * vertical))
    return circles


def torus_residual(points: Iterable[Iterable[float]], *, major_radius: float, minor_radius: float) -> float:
    """Return max implicit torus residual for points on a torus around the z-axis."""
    points = np.asarray(points, dtype=float)
    radial = np.sqrt(points[:, 0] * points[:, 0] + points[:, 1] * points[:, 1])
    residual = (radial - major_radius) ** 2 + points[:, 2] ** 2 - minor_radius**2
    return float(np.max(np.abs(residual)))


def poincare_geodesic_circle(a: Iterable[float], b: Iterable[float], *, eps: float = EPS) -> Circle2D | None:
    """Return the disk geodesic circle through ``a`` and ``b``.

    A ``None`` result means the geodesic is a diameter line through the origin.
    """
    a = as_point2(a)
    b = as_point2(b)
    matrix = 2.0 * np.vstack((a, b))
    rhs = np.array([np.dot(a, a) + 1.0, np.dot(b, b) + 1.0], dtype=float)
    if abs(float(np.linalg.det(matrix))) <= eps:
        return None
    center = np.linalg.solve(matrix, rhs)
    radius = float(np.sqrt(max(np.dot(center, center) - 1.0, 0.0)))
    return Circle2D(center, radius)


def spherical_geodesic_circle(a: Iterable[float], b: Iterable[float], *, eps: float = EPS) -> Circle2D | None:
    """Return the stereographic image of the great circle through ``a`` and ``b``.

    A ``None`` result means the great circle projects to a Euclidean line.
    """
    a = as_point2(a)
    b = as_point2(b)
    matrix = 2.0 * np.vstack((a, b))
    rhs = np.array([np.dot(a, a) - 1.0, np.dot(b, b) - 1.0], dtype=float)
    if abs(float(np.linalg.det(matrix))) <= eps:
        return None
    center = np.linalg.solve(matrix, rhs)
    radius = float(np.sqrt(np.dot(center, center) + 1.0))
    return Circle2D(center, radius)


def poincare_distance(a: Iterable[float], b: Iterable[float]) -> float:
    """Return hyperbolic distance in the Poincare disk."""
    a = as_point2(a)
    b = as_point2(b)
    an = float(np.dot(a, a))
    bn = float(np.dot(b, b))
    if an >= 1.0 or bn >= 1.0:
        raise ValueError("Poincare points must be inside the unit disk")
    argument = 1.0 + 2.0 * float(np.dot(a - b, a - b)) / ((1.0 - an) * (1.0 - bn))
    return float(np.arccosh(max(argument, 1.0)))


def poincare_radial_points(distances: Iterable[float], angle: float = 0.0) -> np.ndarray:
    """Return points at given hyperbolic distances from the disk origin."""
    distances = np.asarray(distances, dtype=float)
    radius = np.tanh(0.5 * distances)
    direction = np.array([np.cos(angle), np.sin(angle)])
    return radius[:, None] * direction[None, :]


def circle_arc_inside_disk(circle: Circle2D, samples: int = 500) -> np.ndarray:
    """Sample the part of a circle lying inside the closed unit disk."""
    points = circle.sample(samples)
    keep = np.linalg.norm(points, axis=1) <= 1.0 + 1e-8
    return points[keep]


def sanity_checks() -> dict[str, float]:
    """Run compact numerical checks used by the notebook quality gate."""
    a = np.array([0.25, -0.45])
    b = np.array([1.1, 0.35])
    A = conformal_point(a)
    B = conformal_point(b)
    t = np.array([0.4, -0.2])
    scale = 1.7
    T = translation_matrix(t)
    S = scaling_matrix(scale)
    points = np.array([[0.2, 0.5], [-0.4, 0.7], [1.0, -0.25]])
    inverted_once = invert_points(points, center=(0.1, -0.2), radius=1.3)
    inverted_twice = invert_points(inverted_once, center=(0.1, -0.2), radius=1.3)
    line = line_points([0.75, 0.35], [1.0, 0.15], np.linspace(-1.3, 1.3, 80))
    inverted_line = invert_points(line, radius=1.0)
    fitted = fit_circle(inverted_line)
    transversion_seed = np.array([[0.15, -0.25], [0.8, 0.2], [-0.25, 0.65]])
    transversion_image = transversion_points(transversion_seed, [0.2, -0.15])
    transversion_round_trip = transversion_points(transversion_image, [-0.2, 0.15])
    theta = np.linspace(-5.0, 5.0, 300)
    bearings = loxodrome_bearing_angles(theta, growth=0.2)[20:-20]
    h_circle = poincare_geodesic_circle([0.2, 0.35], [-0.45, 0.1])
    s_circle = spherical_geodesic_circle([0.2, 0.35], [-0.45, 0.1])
    assert h_circle is not None
    assert s_circle is not None
    torus_points = np.vstack(torus_orbit_circles(major_radius=1.4, minor_radius=0.25, count=8, samples=50))
    return {
        "point_null_residual": abs(conformal_norm2(A)),
        "distance_identity_residual": abs(distance_squared_from_inner(A, B) - float(np.dot(a - b, a - b))),
        "translation_metric_error": metric_error(T),
        "scaling_metric_error": metric_error(S),
        "inversion_involution_error": float(np.max(np.linalg.norm(inverted_twice - points, axis=1))),
        "inverted_line_circle_residual": circle_residual(inverted_line, fitted),
        "transversion_inverse_error": float(np.max(np.linalg.norm(transversion_round_trip - transversion_seed, axis=1))),
        "similarity_noncommutativity_norm": float(
            np.linalg.norm(apply_conformal_matrix(S @ T, points) - apply_conformal_matrix(T @ S, points))
        ),
        "loxodrome_bearing_std": float(np.std(bearings)),
        "hyperbolic_orthogonality_residual": abs(float(np.dot(h_circle.center, h_circle.center) - h_circle.radius**2 - 1.0)),
        "spherical_antipodal_residual": abs(float(s_circle.radius**2 - np.dot(s_circle.center, s_circle.center) - 1.0)),
        "torus_orbit_residual": torus_residual(torus_points, major_radius=1.4, minor_radius=0.25),
    }
