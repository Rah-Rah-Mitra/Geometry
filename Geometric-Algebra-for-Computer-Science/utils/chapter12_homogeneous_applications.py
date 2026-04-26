"""Numerical helpers for Chapter 12 homogeneous-model applications.

The functions here keep the coordinates explicit. They are not a full geometric
algebra implementation; they are small bridge routines for Plucker lines,
pinhole cameras, stereo constraints, ray reconstruction, and 4-by-4
homogeneous transforms.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

EPS = 1e-10


def as_point3(point: Iterable[float]) -> np.ndarray:
    """Return a finite 3-D point as a float vector of shape ``(3,)``."""
    point = np.asarray(point, dtype=float)
    if point.shape != (3,):
        raise ValueError("expected a 3-D point")
    return point


def normalize(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Return a unit vector, raising if the input is numerically zero."""
    vector = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(vector))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def skew(vector: Iterable[float]) -> np.ndarray:
    """Return the matrix that computes a cross product with ``vector``."""
    x, y, z = as_point3(vector)
    return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]], dtype=float)


def homogeneous_point(point: Iterable[float], w: float = 1.0) -> np.ndarray:
    """Embed a 3-D point in homogeneous coordinates ``[x, y, z, w]``."""
    point = as_point3(point)
    return np.array([point[0], point[1], point[2], float(w)], dtype=float)


def dehomogenize(point: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Convert a finite homogeneous 3-D point back to affine coordinates."""
    point = np.asarray(point, dtype=float)
    if point.shape != (4,):
        raise ValueError("expected a homogeneous 4-vector")
    if abs(float(point[3])) <= eps:
        raise ZeroDivisionError("point at infinity cannot be dehomogenized")
    return point[:3] / point[3]


@dataclass(frozen=True)
class PluckerLine:
    """Conventional Plucker line coordinates ``(direction, moment)``."""

    direction: np.ndarray
    moment: np.ndarray

    def normalized(self) -> "PluckerLine":
        """Return the same line with unit direction."""
        length = float(np.linalg.norm(self.direction))
        if length <= EPS:
            raise ValueError("Plucker line has zero direction")
        return PluckerLine(self.direction / length, self.moment / length)

    def constraint(self) -> float:
        """Return the Grassmann-Plucker constraint ``direction dot moment``."""
        return float(np.dot(self.direction, self.moment))


def plucker_from_points(a: Iterable[float], b: Iterable[float]) -> PluckerLine:
    """Return Plucker coordinates for the oriented line through two points."""
    a = as_point3(a)
    b = as_point3(b)
    direction = b - a
    if np.linalg.norm(direction) <= EPS:
        raise ValueError("two distinct points are required")
    moment = np.cross(a, direction)
    return PluckerLine(direction, moment)


def point_on_plucker(line: PluckerLine) -> np.ndarray:
    """Return the finite point on the line nearest the origin."""
    denom = float(np.dot(line.direction, line.direction))
    if denom <= EPS:
        raise ValueError("Plucker line has zero direction")
    return np.cross(line.moment, line.direction) / denom


def plucker_side(a: PluckerLine, b: PluckerLine) -> float:
    """Return the reciprocal product that vanishes for coplanar lines."""
    return float(np.dot(a.direction, b.moment) + np.dot(b.direction, a.moment))


def closest_points_on_lines(
    p1: Iterable[float],
    d1: Iterable[float],
    p2: Iterable[float],
    d2: Iterable[float],
    *,
    eps: float = EPS,
) -> dict[str, object]:
    """Compute closest points on two parametric 3-D lines.

    The returned parameters satisfy ``c1 = p1 + t1*d1`` and
    ``c2 = p2 + t2*d2`` for unitized directions.
    """
    p1 = as_point3(p1)
    p2 = as_point3(p2)
    d1 = normalize(d1)
    d2 = normalize(d2)
    cross = np.cross(d1, d2)
    if np.linalg.norm(cross) <= eps:
        return {
            "parallel": True,
            "t1": np.nan,
            "t2": np.nan,
            "point1": p1,
            "point2": p2,
            "distance": float(np.linalg.norm(np.cross(p2 - p1, d1))),
        }

    system = np.array(
        [[np.dot(d1, d1), -np.dot(d1, d2)], [np.dot(d1, d2), -np.dot(d2, d2)]],
        dtype=float,
    )
    rhs = np.array([np.dot(p2 - p1, d1), np.dot(p2 - p1, d2)], dtype=float)
    t1, t2 = np.linalg.solve(system, rhs)
    point1 = p1 + t1 * d1
    point2 = p2 + t2 * d2
    return {
        "parallel": False,
        "t1": float(t1),
        "t2": float(t2),
        "point1": point1,
        "point2": point2,
        "distance": float(np.linalg.norm(point2 - point1)),
    }


def look_at_rotation(
    center: Iterable[float],
    target: Iterable[float],
    up: Iterable[float] = (0.0, 1.0, 0.0),
) -> np.ndarray:
    """Return a world-to-camera rotation with positive camera ``z`` forward."""
    center = as_point3(center)
    target = as_point3(target)
    forward = normalize(target - center)
    right = normalize(np.cross(forward, normalize(up)))
    camera_up = np.cross(right, forward)
    return np.vstack([right, camera_up, forward])


@dataclass(frozen=True)
class PinholeCamera:
    """A minimal calibrated pinhole camera with square pixels."""

    name: str
    center: np.ndarray
    rotation_world_to_camera: np.ndarray
    focal_length: float = 1.0

    @property
    def K(self) -> np.ndarray:
        """Return the intrinsic calibration matrix."""
        f = float(self.focal_length)
        return np.array([[f, 0.0, 0.0], [0.0, f, 0.0], [0.0, 0.0, 1.0]], dtype=float)

    @property
    def matrix(self) -> np.ndarray:
        """Return the 3-by-4 camera projection matrix."""
        translation = -self.rotation_world_to_camera @ self.center
        return self.K @ np.column_stack([self.rotation_world_to_camera, translation])

    def camera_coordinates(self, point: Iterable[float]) -> np.ndarray:
        """Return point coordinates in this camera's local frame."""
        return self.rotation_world_to_camera @ (as_point3(point) - self.center)

    def project(self, point: Iterable[float]) -> np.ndarray:
        """Project a world point to image homogeneous coordinates."""
        camera_point = self.camera_coordinates(point)
        if abs(float(camera_point[2])) <= EPS:
            raise ZeroDivisionError("point lies on the camera horizon")
        image = self.K @ (camera_point / camera_point[2])
        return image / image[2]

    def ray_from_image(self, image_point: Iterable[float]) -> tuple[np.ndarray, np.ndarray]:
        """Return the world-space ray through an image point."""
        image_point = np.asarray(image_point, dtype=float)
        if image_point.shape != (3,):
            raise ValueError("expected homogeneous image point")
        local = np.linalg.inv(self.K) @ image_point
        direction = self.rotation_world_to_camera.T @ local
        return self.center.copy(), normalize(direction)

    def ray_plane_from_image_line(self, image_line: Iterable[float]) -> tuple[np.ndarray, float]:
        """Return world plane ``normal dot X - offset = 0`` from an image line."""
        image_line = np.asarray(image_line, dtype=float)
        if image_line.shape != (3,):
            raise ValueError("expected homogeneous image line")
        normal_camera = self.K.T @ image_line
        normal_world = normalize(self.rotation_world_to_camera.T @ normal_camera)
        offset = float(np.dot(normal_world, self.center))
        return normal_world, offset


def make_camera(
    name: str,
    center: Iterable[float],
    target: Iterable[float],
    *,
    focal_length: float = 1.0,
    up: Iterable[float] = (0.0, 1.0, 0.0),
) -> PinholeCamera:
    """Construct a camera looking from ``center`` toward ``target``."""
    center = as_point3(center)
    rotation = look_at_rotation(center, target, up)
    return PinholeCamera(name, center, rotation, float(focal_length))


def essential_matrix(left: PinholeCamera, right: PinholeCamera) -> np.ndarray:
    """Return the essential matrix mapping left image rays to right epipolar lines."""
    relative_rotation = right.rotation_world_to_camera @ left.rotation_world_to_camera.T
    relative_translation = right.rotation_world_to_camera @ (left.center - right.center)
    return skew(relative_translation) @ relative_rotation


def fundamental_matrix(left: PinholeCamera, right: PinholeCamera) -> np.ndarray:
    """Return the fundamental matrix for the two cameras."""
    essential = essential_matrix(left, right)
    return np.linalg.inv(right.K).T @ essential @ np.linalg.inv(left.K)


def epipolar_residual(matrix: np.ndarray, left_point: Iterable[float], right_point: Iterable[float]) -> float:
    """Evaluate ``right_point.T @ F @ left_point``."""
    left_point = np.asarray(left_point, dtype=float)
    right_point = np.asarray(right_point, dtype=float)
    return float(right_point @ np.asarray(matrix, dtype=float) @ left_point)


def triangulate_two_views(
    left: PinholeCamera,
    left_point: Iterable[float],
    right: PinholeCamera,
    right_point: Iterable[float],
) -> dict[str, object]:
    """Triangulate a point by intersecting the two viewing rays in least squares."""
    origin1, direction1 = left.ray_from_image(left_point)
    origin2, direction2 = right.ray_from_image(right_point)
    closest = closest_points_on_lines(origin1, direction1, origin2, direction2)
    point = 0.5 * (closest["point1"] + closest["point2"])
    return {**closest, "point": point}


def reconstruct_from_rays(rays: Iterable[tuple[Iterable[float], Iterable[float]]]) -> dict[str, object]:
    """Find the least-squares point closest to a collection of viewing rays."""
    lhs = np.zeros((3, 3), dtype=float)
    rhs = np.zeros(3, dtype=float)
    normalized_rays: list[tuple[np.ndarray, np.ndarray]] = []
    for origin, direction in rays:
        origin = as_point3(origin)
        direction = normalize(direction)
        projector = np.eye(3) - np.outer(direction, direction)
        lhs += projector
        rhs += projector @ origin
        normalized_rays.append((origin, direction))
    point = np.linalg.solve(lhs, rhs)
    residuals = [
        float(np.linalg.norm((np.eye(3) - np.outer(direction, direction)) @ (point - origin)))
        for origin, direction in normalized_rays
    ]
    return {
        "point": point,
        "residuals": residuals,
        "rms": float(np.sqrt(np.mean(np.square(residuals)))) if residuals else 0.0,
    }


def view_matrix(camera: PinholeCamera) -> np.ndarray:
    """Return an OpenGL-style homogeneous world-to-camera matrix."""
    matrix = np.eye(4, dtype=float)
    matrix[:3, :3] = camera.rotation_world_to_camera
    matrix[:3, 3] = -camera.rotation_world_to_camera @ camera.center
    return matrix


def transform_points(matrix: np.ndarray, points: Iterable[Iterable[float]]) -> np.ndarray:
    """Apply a 4-by-4 homogeneous transform to affine 3-D points."""
    matrix = np.asarray(matrix, dtype=float)
    points = np.asarray(list(points), dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError("expected a 4-by-4 transform")
    homogeneous = np.column_stack([points, np.ones(len(points))])
    transformed = (matrix @ homogeneous.T).T
    return transformed[:, :3] / transformed[:, 3:4]


def translation_matrix(offset: Iterable[float]) -> np.ndarray:
    """Return a 4-by-4 homogeneous translation matrix."""
    matrix = np.eye(4, dtype=float)
    matrix[:3, 3] = as_point3(offset)
    return matrix


def rotation_z_matrix(angle: float) -> np.ndarray:
    """Return a 4-by-4 homogeneous rotation about the z-axis."""
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    matrix = np.eye(4, dtype=float)
    matrix[:3, :3] = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    return matrix
