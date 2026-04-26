"""Numerical helpers for Chapter 13 conformal-model notebooks.

The routines use the common conformal coordinate order ``[e1, e2, e3, no, ni]``.
The Euclidean basis vectors square to ``+1`` and the two null basis vectors obey
``no.ni = -1``. This module is deliberately small: it exposes the metric,
point embedding, dual point/plane/sphere probes, rigid conformal matrices, and
plain Euclidean versions of the screw and reflection calculations used in the
notebook.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy.linalg import expm, logm
from scipy.spatial.transform import Rotation

EPS = 1e-10

METRIC = np.array(
    [
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, -1.0],
        [0.0, 0.0, 0.0, -1.0, 0.0],
    ],
    dtype=float,
)
NO = np.array([0.0, 0.0, 0.0, 1.0, 0.0], dtype=float)
NI = np.array([0.0, 0.0, 0.0, 0.0, 1.0], dtype=float)


def as_vector3(vector: Iterable[float]) -> np.ndarray:
    """Return ``vector`` as a finite 3-D float array."""
    array = np.asarray(vector, dtype=float)
    if array.shape != (3,):
        raise ValueError("expected a 3-D vector")
    return array


def normalize(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Return a unit vector, raising if the input is too small."""
    array = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(array))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return array / length


def conformal_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the conformal inner product in the ``[e1,e2,e3,no,ni]`` basis."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != (5,) or b.shape != (5,):
        raise ValueError("conformal vectors must have five coordinates")
    return float(a @ METRIC @ b)


def conformal_norm2(vector: Iterable[float]) -> float:
    """Return the conformal squared norm."""
    return conformal_inner(vector, vector)


def conformal_point(point: Iterable[float]) -> np.ndarray:
    """Embed a Euclidean point as ``x + no + 0.5*|x|^2*ni``."""
    point = as_vector3(point)
    return np.array(
        [point[0], point[1], point[2], 1.0, 0.5 * float(np.dot(point, point))],
        dtype=float,
    )


def conformal_weight(vector: Iterable[float]) -> float:
    """Return the point weight ``-X.ni``."""
    return -conformal_inner(vector, NI)


def recover_point(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Recover Euclidean coordinates from a weighted conformal point vector."""
    vector = np.asarray(vector, dtype=float)
    weight = conformal_weight(vector)
    if abs(weight) <= eps:
        raise ZeroDivisionError("cannot recover a finite point from zero weight")
    return vector[:3] / weight


def normalized_point_vector(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Scale a conformal point vector to unit weight."""
    vector = np.asarray(vector, dtype=float)
    weight = conformal_weight(vector)
    if abs(weight) <= eps:
        raise ZeroDivisionError("cannot normalize a zero-weight point")
    return vector / weight


def distance_squared_from_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Recover Euclidean squared distance from two point representatives."""
    a_vec = normalized_point_vector(a if np.asarray(a).shape == (5,) else conformal_point(a))
    b_vec = normalized_point_vector(b if np.asarray(b).shape == (5,) else conformal_point(b))
    return float(-2.0 * conformal_inner(a_vec, b_vec))


def dual_plane(normal: Iterable[float], offset: float) -> np.ndarray:
    """Return the dual plane vector for ``normal.x = offset``.

    The normal is unitized. The offset is scaled by the same length, so the
    returned plane has unit Euclidean normal and ``X.plane`` is signed distance.
    """
    normal = as_vector3(normal)
    length = float(np.linalg.norm(normal))
    if length <= EPS:
        raise ValueError("plane normal must be nonzero")
    normal = normal / length
    offset = float(offset) / length
    return np.array([normal[0], normal[1], normal[2], 0.0, offset], dtype=float)


def dual_sphere(center: Iterable[float], radius: float) -> np.ndarray:
    """Return the dual sphere vector centered at ``center`` with ``radius``."""
    if radius < 0:
        raise ValueError("sphere radius must be nonnegative")
    return conformal_point(center) - 0.5 * float(radius) ** 2 * NI


def point_probe(point: Iterable[float], anchor: Iterable[float]) -> float:
    """Return squared distance to ``anchor`` using a conformal point probe."""
    return distance_squared_from_inner(conformal_point(point), conformal_point(anchor))


def plane_probe(point: Iterable[float], plane: Iterable[float]) -> float:
    """Return signed distance from ``point`` to a unit dual plane vector."""
    return conformal_inner(conformal_point(point), plane)


def sphere_probe(point: Iterable[float], sphere: Iterable[float]) -> float:
    """Return sphere power ``|x-c|^2-r^2`` from a dual sphere vector."""
    return -2.0 * conformal_inner(conformal_point(point), sphere)


def probe_table(
    points: Iterable[Iterable[float]],
    *,
    anchor: Iterable[float],
    plane: Iterable[float],
    sphere: Iterable[float],
) -> list[dict[str, float]]:
    """Evaluate point, plane, and sphere probes at a collection of points."""
    rows: list[dict[str, float]] = []
    for point in points:
        point = as_vector3(point)
        rows.append(
            {
                "x": float(point[0]),
                "y": float(point[1]),
                "z": float(point[2]),
                "point_distance_squared": point_probe(point, anchor),
                "plane_signed_distance": plane_probe(point, plane),
                "sphere_power": sphere_probe(point, sphere),
            }
        )
    return rows


def rotation_matrix(axis: Iterable[float], angle: float) -> np.ndarray:
    """Return a 3-D Rodrigues rotation matrix."""
    axis = normalize(axis)
    x, y, z = axis
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    C = 1.0 - c
    return np.array(
        [
            [c + x * x * C, x * y * C - z * s, x * z * C + y * s],
            [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C],
        ],
        dtype=float,
    )


def rigid_cga_matrix(
    rotation: Iterable[Iterable[float]] | None = None,
    translation: Iterable[float] = (0.0, 0.0, 0.0),
) -> np.ndarray:
    """Return the 5-by-5 conformal matrix for ``x -> R*x + t``."""
    R = np.eye(3) if rotation is None else np.asarray(rotation, dtype=float)
    if R.shape != (3, 3):
        raise ValueError("rotation must be a 3-by-3 matrix")
    t = as_vector3(translation)
    matrix = np.zeros((5, 5), dtype=float)
    matrix[:3, :3] = R
    matrix[:3, 3] = t
    matrix[3, 3] = 1.0
    matrix[4, :3] = t @ R
    matrix[4, 3] = 0.5 * float(np.dot(t, t))
    matrix[4, 4] = 1.0
    return matrix


def apply_cga_matrix(matrix: Iterable[Iterable[float]], vector: Iterable[float]) -> np.ndarray:
    """Apply a conformal linear operator to a conformal vector."""
    matrix = np.asarray(matrix, dtype=float)
    vector = np.asarray(vector, dtype=float)
    if matrix.shape != (5, 5) or vector.shape != (5,):
        raise ValueError("expected a 5-by-5 matrix and a 5-vector")
    return matrix @ vector


def apply_rigid(points: Iterable[Iterable[float]], rotation: np.ndarray, translation: Iterable[float]) -> np.ndarray:
    """Apply ``x -> R*x + t`` to an array of Euclidean points."""
    points = np.asarray(list(points), dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("expected an array of 3-D points")
    return (np.asarray(rotation, dtype=float) @ points.T).T + as_vector3(translation)


def metric_error(matrix: Iterable[Iterable[float]]) -> float:
    """Return ``||M.T*G*M - G||`` for the conformal metric matrix."""
    matrix = np.asarray(matrix, dtype=float)
    return float(np.linalg.norm(matrix.T @ METRIC @ matrix - METRIC))


def infinity_error(matrix: Iterable[Iterable[float]]) -> float:
    """Return ``||M*ni - ni||``."""
    return float(np.linalg.norm(np.asarray(matrix, dtype=float) @ NI - NI))


def reflection_rt(normal: Iterable[float], offset: float) -> tuple[np.ndarray, np.ndarray]:
    """Return Euclidean ``(R,t)`` for reflection in ``normal.x = offset``."""
    normal = as_vector3(normal)
    length = float(np.linalg.norm(normal))
    if length <= EPS:
        raise ValueError("plane normal must be nonzero")
    n = normal / length
    h = float(offset) / length
    R = np.eye(3) - 2.0 * np.outer(n, n)
    t = 2.0 * h * n
    return R, t


def reflect_points(points: Iterable[Iterable[float]], normal: Iterable[float], offset: float) -> np.ndarray:
    """Reflect Euclidean points in the plane ``normal.x = offset``."""
    R, t = reflection_rt(normal, offset)
    return apply_rigid(points, R, t)


@dataclass(frozen=True)
class Line3D:
    """A Euclidean line stored as unit direction and Plucker moment."""

    direction: np.ndarray
    moment: np.ndarray

    def point_nearest_origin(self) -> np.ndarray:
        """Return the finite point on the line closest to the origin."""
        return np.cross(self.moment, self.direction)


def line_from_points(a: Iterable[float], b: Iterable[float]) -> Line3D:
    """Return Plucker-style line data from two finite points."""
    a = as_vector3(a)
    b = as_vector3(b)
    direction = normalize(b - a)
    moment = np.cross(a, direction)
    return Line3D(direction, moment)


def transform_line(line: Line3D, rotation: np.ndarray, translation: Iterable[float]) -> Line3D:
    """Transform a Plucker line by a rigid motion."""
    R = np.asarray(rotation, dtype=float)
    t = as_vector3(translation)
    direction = R @ line.direction
    moment = R @ line.moment + np.cross(t, direction)
    return Line3D(direction, moment)


def homogeneous_transform(rotation: np.ndarray, translation: Iterable[float]) -> np.ndarray:
    """Return a 4-by-4 homogeneous rigid transform."""
    matrix = np.eye(4, dtype=float)
    matrix[:3, :3] = np.asarray(rotation, dtype=float)
    matrix[:3, 3] = as_vector3(translation)
    return matrix


def split_homogeneous(matrix: Iterable[Iterable[float]]) -> tuple[np.ndarray, np.ndarray]:
    """Split a 4-by-4 homogeneous transform into ``(R,t)``."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError("expected a 4-by-4 homogeneous transform")
    return matrix[:3, :3], matrix[:3, 3]


def fractional_transform(rotation: np.ndarray, translation: Iterable[float], fraction: float) -> tuple[np.ndarray, np.ndarray]:
    """Return the screw-interpolated fractional rigid transform."""
    T = homogeneous_transform(rotation, translation)
    partial = expm(float(fraction) * logm(T))
    partial = np.real_if_close(partial, tol=1000).astype(float)
    return split_homogeneous(partial)


def screw_transform(
    axis: Iterable[float],
    point_on_axis: Iterable[float],
    angle: float,
    pitch: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Construct a screw motion from axis, one axis point, angle, and pitch."""
    axis = normalize(axis)
    q = as_vector3(point_on_axis)
    R = rotation_matrix(axis, angle)
    displacement = float(pitch) * float(angle)
    t = (np.eye(3) - R) @ q + displacement * axis
    return R, t


def screw_parameters(rotation: np.ndarray, translation: Iterable[float]) -> dict[str, object]:
    """Return Chasles-style screw data for a proper rigid motion."""
    R = np.asarray(rotation, dtype=float)
    t = as_vector3(translation)
    rotvec = Rotation.from_matrix(R).as_rotvec()
    angle = float(np.linalg.norm(rotvec))
    if angle <= EPS:
        displacement = float(np.linalg.norm(t))
        axis = normalize(t) if displacement > EPS else np.array([1.0, 0.0, 0.0])
        return {
            "kind": "translation",
            "axis": axis,
            "angle": 0.0,
            "axis_point": np.zeros(3),
            "parallel_displacement": displacement,
            "pitch": np.inf,
        }
    axis = rotvec / angle
    parallel_displacement = float(np.dot(axis, t))
    rhs = t - parallel_displacement * axis
    axis_point = np.linalg.lstsq(np.eye(3) - R, rhs, rcond=None)[0]
    return {
        "kind": "screw",
        "axis": axis,
        "angle": angle,
        "axis_point": axis_point,
        "parallel_displacement": parallel_displacement,
        "pitch": parallel_displacement / angle,
    }


def rotating_plane(
    hinge_axis: Iterable[float],
    base_normal: Iterable[float],
    hinge_point: Iterable[float],
    angle: float,
) -> tuple[np.ndarray, float]:
    """Return ``(normal, offset)`` for a plane rotating about a fixed hinge line."""
    axis = normalize(hinge_axis)
    normal = rotation_matrix(axis, angle) @ normalize(base_normal)
    offset = float(np.dot(normal, as_vector3(hinge_point)))
    return normal, offset


def reflection_velocity(
    points: Iterable[Iterable[float]],
    hinge_axis: Iterable[float],
    base_normal: Iterable[float],
    hinge_point: Iterable[float],
    angle: float,
) -> np.ndarray:
    """Analytic derivative of reflected points as a mirror plane rotates."""
    points = np.asarray(list(points), dtype=float)
    axis = normalize(hinge_axis)
    n0 = normalize(base_normal)
    q = as_vector3(hinge_point)
    R = rotation_matrix(axis, angle)
    n = R @ n0
    n_dot = np.cross(axis, n)
    h = float(np.dot(n, q))
    h_dot = float(np.dot(n_dot, q))
    signed = points @ n - h
    signed_dot = points @ n_dot - h_dot
    return -2.0 * (signed_dot[:, None] * n[None, :] + signed[:, None] * n_dot[None, :])


def finite_difference_reflection_velocity(
    points: Iterable[Iterable[float]],
    hinge_axis: Iterable[float],
    base_normal: Iterable[float],
    hinge_point: Iterable[float],
    angle: float,
    step: float = 1e-5,
) -> np.ndarray:
    """Central-difference derivative for the rotating mirror calculation."""
    n_plus, h_plus = rotating_plane(hinge_axis, base_normal, hinge_point, angle + step)
    n_minus, h_minus = rotating_plane(hinge_axis, base_normal, hinge_point, angle - step)
    plus = reflect_points(points, n_plus, h_plus)
    minus = reflect_points(points, n_minus, h_minus)
    return (plus - minus) / (2.0 * step)


def sanity_checks() -> dict[str, float]:
    """Run compact numerical checks used by the notebook quality gate."""
    a = np.array([0.25, -0.5, 0.75])
    b = np.array([1.5, 0.25, -0.25])
    A = conformal_point(a)
    B = conformal_point(b)
    R, t = screw_transform([0.0, 0.0, 1.0], [0.4, -0.2, 0.0], 0.7, pitch=0.15)
    M = rigid_cga_matrix(R, t)
    plane = dual_plane([0.0, 1.0, 0.0], 0.3)
    reflected = reflect_points([a], [0.0, 1.0, 0.0], 0.3)[0]
    unreflected = reflect_points([reflected], [0.0, 1.0, 0.0], 0.3)[0]
    points = np.array([[0.5, -0.1, 0.2], [1.0, 0.4, -0.3]])
    analytic = reflection_velocity(points, [0, 0, 1], [1, 0, 0], [0.2, 0.1, 0], 0.4)
    numeric = finite_difference_reflection_velocity(points, [0, 0, 1], [1, 0, 0], [0.2, 0.1, 0], 0.4)
    return {
        "point_null_residual": abs(conformal_norm2(A)),
        "distance_identity_residual": abs(distance_squared_from_inner(A, B) - float(np.dot(a - b, a - b))),
        "metric_preservation_error": metric_error(M),
        "infinity_preservation_error": infinity_error(M),
        "plane_probe_after_reflection": abs(plane_probe(reflected, plane) + plane_probe(a, plane)),
        "reflection_involution_error": float(np.linalg.norm(unreflected - a)),
        "differential_reflection_error": float(np.linalg.norm(analytic - numeric)),
    }
