"""Chapter 10 helpers for the vector-space model of directions.

The functions here keep the notebook examples small and inspectable.  They use
ordinary arrays for the computational shadow of the geometric algebra ideas:
unit directions, dual bivector angles, rotors represented as unit quaternions,
finite point-group actions, and camera rays.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from math import atan2, cos, sin
from typing import Iterable

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
    "faint": "rgba(80, 80, 80, 0.24)",
}


def normalize(vector: Iterable[float] | np.ndarray, *, tol: float = EPS) -> np.ndarray:
    """Return a unit vector, raising on near-zero input."""
    value = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(value))
    if length <= tol:
        raise ValueError("cannot normalize a near-zero vector")
    return value / length


def angle_between(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the unoriented angle between two vectors in radians."""
    u = normalize(a)
    v = normalize(b)
    return float(np.arccos(np.clip(u @ v, -1.0, 1.0)))


def signed_area_2d(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the signed 2-D parallelogram area represented by a wedge."""
    ax, ay = np.asarray(a, dtype=float)[:2]
    bx, by = np.asarray(b, dtype=float)[:2]
    return float(ax * by - ay * bx)


def planar_triangle_metrics(vertices: np.ndarray) -> dict[str, float]:
    """Compute side lengths, angles, and oriented area for a planar triangle."""
    pts = np.asarray(vertices, dtype=float)
    if pts.shape != (3, 2):
        raise ValueError("vertices must be a 3-by-2 array")

    a = pts[1] - pts[0]
    b = pts[2] - pts[1]
    c = pts[0] - pts[2]
    side_lengths = np.array([np.linalg.norm(b), np.linalg.norm(c), np.linalg.norm(a)])
    angles = np.array(
        [
            angle_between(a, -c),
            angle_between(b, -a),
            angle_between(c, -b),
        ]
    )
    area = 0.5 * signed_area_2d(a, pts[2] - pts[0])
    return {
        "side_a": float(side_lengths[0]),
        "side_b": float(side_lengths[1]),
        "side_c": float(side_lengths[2]),
        "angle_A": float(angles[0]),
        "angle_B": float(angles[1]),
        "angle_C": float(angles[2]),
        "area_oriented": float(area),
        "angle_sum": float(np.sum(angles)),
        "law_of_sines_spread": float(np.ptp(np.sin(angles) / side_lengths)),
        "law_of_cosines_error": float(
            side_lengths[0] ** 2
            - (
                side_lengths[1] ** 2
                + side_lengths[2] ** 2
                - 2.0 * side_lengths[1] * side_lengths[2] * cos(angles[0])
            )
        ),
    }


def great_circle_arc(start: Iterable[float], end: Iterable[float], steps: int = 64) -> np.ndarray:
    """Return points on the short great-circle arc from start to end."""
    a = normalize(start)
    b = normalize(end)
    omega = angle_between(a, b)
    if omega < EPS:
        return np.repeat(a[None, :], steps, axis=0)
    t = np.linspace(0.0, 1.0, steps)
    return (
        np.sin((1.0 - t)[:, None] * omega) * a[None, :]
        + np.sin(t[:, None] * omega) * b[None, :]
    ) / sin(omega)


def tangent_direction(vertex: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Return the unit tangent at vertex pointing toward target on the sphere."""
    vertex = normalize(vertex)
    target = normalize(target)
    return normalize(target - (target @ vertex) * vertex)


def spherical_triangle_metrics(a: Iterable[float], b: Iterable[float], c: Iterable[float]) -> dict[str, float]:
    """Return side lengths and internal angles for a unit spherical triangle."""
    av = normalize(a)
    bv = normalize(b)
    cv = normalize(c)

    side_a = angle_between(bv, cv)
    side_b = angle_between(cv, av)
    side_c = angle_between(av, bv)

    angle_a = angle_between(tangent_direction(av, bv), tangent_direction(av, cv))
    angle_b = angle_between(tangent_direction(bv, cv), tangent_direction(bv, av))
    angle_c = angle_between(tangent_direction(cv, av), tangent_direction(cv, bv))

    side_cosine_error = cos(side_a) - (
        cos(side_b) * cos(side_c) + sin(side_b) * sin(side_c) * cos(angle_a)
    )
    angle_cosine_error = cos(angle_a) - (
        -cos(angle_b) * cos(angle_c) + sin(angle_b) * sin(angle_c) * cos(side_a)
    )

    return {
        "side_a": float(side_a),
        "side_b": float(side_b),
        "side_c": float(side_c),
        "angle_A": float(angle_a),
        "angle_B": float(angle_b),
        "angle_C": float(angle_c),
        "spherical_excess": float(angle_a + angle_b + angle_c - np.pi),
        "side_cosine_error": float(side_cosine_error),
        "angle_cosine_error": float(angle_cosine_error),
    }


def quaternion_product(left: Iterable[float], right: Iterable[float]) -> np.ndarray:
    """Hamilton product for quaternions stored as (w, x, y, z)."""
    w1, x1, y1, z1 = (float(v) for v in left)
    w2, x2, y2, z2 = (float(v) for v in right)
    return np.array(
        [
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
        ],
        dtype=float,
    )


@dataclass(frozen=True)
class Rotor3D:
    """A 3-D unit rotor represented by the matching unit quaternion."""

    q: np.ndarray

    def __post_init__(self) -> None:
        q = np.asarray(self.q, dtype=float)
        if q.shape != (4,):
            raise ValueError("rotor quaternion must have shape (4,)")
        length = float(np.linalg.norm(q))
        if length <= EPS:
            raise ValueError("cannot build a rotor from a zero quaternion")
        object.__setattr__(self, "q", q / length)

    @staticmethod
    def identity() -> "Rotor3D":
        return Rotor3D(np.array([1.0, 0.0, 0.0, 0.0]))

    @staticmethod
    def from_axis_angle(axis: Iterable[float], angle: float) -> "Rotor3D":
        unit_axis = normalize(axis)
        half = 0.5 * float(angle)
        return Rotor3D(np.r_[cos(half), sin(half) * unit_axis])

    @staticmethod
    def from_log_vector(omega: Iterable[float]) -> "Rotor3D":
        omega = np.asarray(omega, dtype=float)
        angle = float(np.linalg.norm(omega))
        if angle <= EPS:
            return Rotor3D.identity()
        return Rotor3D.from_axis_angle(omega / angle, angle)

    @staticmethod
    def from_two_vectors(source: Iterable[float], target: Iterable[float]) -> "Rotor3D":
        a = normalize(source)
        b = normalize(target)
        dot = float(np.clip(a @ b, -1.0, 1.0))
        if dot < -1.0 + 1e-8:
            helper = np.array([1.0, 0.0, 0.0])
            if abs(a @ helper) > 0.9:
                helper = np.array([0.0, 1.0, 0.0])
            axis = normalize(np.cross(a, helper))
            return Rotor3D.from_axis_angle(axis, np.pi)
        return Rotor3D(np.r_[1.0 + dot, np.cross(a, b)])

    @staticmethod
    def from_matrix(matrix: np.ndarray) -> "Rotor3D":
        """Convert a proper rotation matrix to a rotor."""
        m = np.asarray(matrix, dtype=float)
        if m.shape != (3, 3):
            raise ValueError("rotation matrix must be 3-by-3")
        trace = float(np.trace(m))
        if trace > 0.0:
            s = 2.0 * np.sqrt(trace + 1.0)
            q = np.array(
                [
                    0.25 * s,
                    (m[2, 1] - m[1, 2]) / s,
                    (m[0, 2] - m[2, 0]) / s,
                    (m[1, 0] - m[0, 1]) / s,
                ]
            )
        else:
            idx = int(np.argmax(np.diag(m)))
            if idx == 0:
                s = 2.0 * np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2])
                q = np.array(
                    [
                        (m[2, 1] - m[1, 2]) / s,
                        0.25 * s,
                        (m[0, 1] + m[1, 0]) / s,
                        (m[0, 2] + m[2, 0]) / s,
                    ]
                )
            elif idx == 1:
                s = 2.0 * np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2])
                q = np.array(
                    [
                        (m[0, 2] - m[2, 0]) / s,
                        (m[0, 1] + m[1, 0]) / s,
                        0.25 * s,
                        (m[1, 2] + m[2, 1]) / s,
                    ]
                )
            else:
                s = 2.0 * np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1])
                q = np.array(
                    [
                        (m[1, 0] - m[0, 1]) / s,
                        (m[0, 2] + m[2, 0]) / s,
                        (m[1, 2] + m[2, 1]) / s,
                        0.25 * s,
                    ]
                )
        return Rotor3D(q)

    def canonical(self) -> "Rotor3D":
        """Return the equivalent rotor with nonnegative scalar part."""
        if self.q[0] < 0.0:
            return Rotor3D(-self.q)
        return self

    def inverse(self) -> "Rotor3D":
        w, x, y, z = self.q
        return Rotor3D(np.array([w, -x, -y, -z]))

    def __mul__(self, other: "Rotor3D") -> "Rotor3D":
        return Rotor3D(quaternion_product(self.q, other.q))

    def as_matrix(self) -> np.ndarray:
        w, x, y, z = self.q
        return np.array(
            [
                [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
            ]
        )

    def rotate(self, vector: Iterable[float] | np.ndarray) -> np.ndarray:
        return self.as_matrix() @ np.asarray(vector, dtype=float)

    def log_vector(self) -> np.ndarray:
        """Return the principal axis-angle vector, dual to the bivector log."""
        q = self.canonical().q
        vector = q[1:]
        length = float(np.linalg.norm(vector))
        if length <= EPS:
            return np.zeros(3)
        angle = 2.0 * atan2(length, float(q[0]))
        return vector * (angle / length)

    def power(self, amount: float) -> "Rotor3D":
        return Rotor3D.from_log_vector(float(amount) * self.log_vector())


def interpolate_rotors(source: Rotor3D, target: Rotor3D, amount: float) -> Rotor3D:
    """Shortest-branch rotor interpolation from source to target."""
    end = target
    if float(source.q @ target.q) < 0.0:
        end = Rotor3D(-target.q)
    delta = end * source.inverse()
    return delta.power(amount) * source


def estimate_rotation_from_directions(
    source: np.ndarray,
    target: np.ndarray,
    weights: np.ndarray | None = None,
) -> tuple[Rotor3D, np.ndarray, float]:
    """Estimate R minimizing sum ||R source_i - target_i||^2."""
    src = np.asarray(source, dtype=float)
    dst = np.asarray(target, dtype=float)
    if src.shape != dst.shape or src.ndim != 2 or src.shape[1] != 3:
        raise ValueError("source and target must both be N-by-3 arrays")
    src = np.vstack([normalize(v) for v in src])
    dst = np.vstack([normalize(v) for v in dst])
    if weights is None:
        weights = np.ones(src.shape[0])
    weights = np.asarray(weights, dtype=float)
    h = np.zeros((3, 3))
    for w, a, b in zip(weights, src, dst, strict=True):
        h += w * np.outer(b, a)
    u, singular_values, vt = np.linalg.svd(h)
    correction = np.diag([1.0, 1.0, np.linalg.det(u @ vt)])
    matrix = u @ correction @ vt
    rotor = Rotor3D.from_matrix(matrix)
    residuals = np.linalg.norm((matrix @ src.T).T - dst, axis=1)
    return rotor, singular_values, float(np.sqrt(np.mean(residuals**2)))


def signed_permutation_group(*, proper_only: bool = True) -> list[np.ndarray]:
    """Return the cubic point group as signed permutation matrices."""
    group: list[np.ndarray] = []
    for perm in permutations(range(3)):
        base = np.eye(3)[:, perm]
        for signs in product([-1.0, 1.0], repeat=3):
            matrix = base @ np.diag(signs)
            det = round(float(np.linalg.det(matrix)))
            if proper_only and det != 1:
                continue
            group.append(matrix)
    unique: list[np.ndarray] = []
    for matrix in group:
        if not any(np.allclose(matrix, other) for other in unique):
            unique.append(matrix)
    return unique


def point_group_orbit(point: Iterable[float], *, proper_only: bool = True) -> np.ndarray:
    """Apply the cubic point group to one seed point."""
    p = np.asarray(point, dtype=float)
    return np.vstack([matrix @ p for matrix in signed_permutation_group(proper_only=proper_only)])


@dataclass(frozen=True)
class CameraRayModel:
    """A calibrated camera represented by a center and a local-to-world rotor."""

    name: str
    center: np.ndarray
    rotation: Rotor3D

    def __post_init__(self) -> None:
        center = np.asarray(self.center, dtype=float)
        if center.shape != (3,):
            raise ValueError("camera center must be a 3-vector")
        object.__setattr__(self, "center", center)

    def observe(self, world_point: Iterable[float]) -> np.ndarray:
        """Return the unit camera-frame ray toward a world point."""
        world_point = np.asarray(world_point, dtype=float)
        return normalize(self.rotation.inverse().rotate(world_point - self.center))

    def world_direction(self, local_ray: Iterable[float]) -> np.ndarray:
        """Map a camera-frame ray direction into world coordinates."""
        return normalize(self.rotation.rotate(local_ray))


def look_at_rotation(center: Iterable[float], target: Iterable[float], up: Iterable[float] = (0, 0, 1)) -> Rotor3D:
    """Build a local-to-world camera rotation whose local +z axis looks at target."""
    center = np.asarray(center, dtype=float)
    target = np.asarray(target, dtype=float)
    forward = normalize(target - center)
    up_hint = normalize(up)
    if abs(float(forward @ up_hint)) > 0.95:
        up_hint = np.array([0.0, 1.0, 0.0])
    right = normalize(np.cross(up_hint, forward))
    true_up = normalize(np.cross(forward, right))
    return Rotor3D.from_matrix(np.column_stack([right, true_up, forward]))


def perturb_direction(direction: np.ndarray, rng: np.random.Generator, sigma: float) -> np.ndarray:
    """Add small isotropic noise and renormalize a direction."""
    if sigma <= 0.0:
        return normalize(direction)
    return normalize(direction + rng.normal(scale=sigma, size=3))


def synthetic_camera_scene(
    *,
    noise: float = 0.004,
    seed: int = 10,
) -> tuple[list[CameraRayModel], np.ndarray, np.ndarray]:
    """Return cameras, world points, and noisy camera-frame unit rays."""
    rng = np.random.default_rng(seed)
    centers = [
        np.array([-2.8, -1.7, 1.15]),
        np.array([2.6, -1.35, 1.05]),
        np.array([0.25, 2.9, 1.35]),
    ]
    target = np.array([0.0, 0.15, 0.55])
    cameras = [
        CameraRayModel(f"C{idx}", center, look_at_rotation(center, target))
        for idx, center in enumerate(centers)
    ]
    t = np.linspace(-1.2, 1.25, 18)
    points = np.column_stack(
        [
            0.82 * np.sin(1.25 * t),
            0.54 * np.cos(1.7 * t) + 0.06 * t,
            0.56 + 0.38 * np.sin(2.1 * t + 0.4),
        ]
    )
    observations = np.empty((len(cameras), len(points), 3))
    for cam_idx, camera in enumerate(cameras):
        for point_idx, point in enumerate(points):
            observations[cam_idx, point_idx] = perturb_direction(
                camera.observe(point), rng, noise
            )
    return cameras, points, observations


def triangulate_from_rays(centers: np.ndarray, directions: np.ndarray) -> np.ndarray:
    """Least-squares point nearest to several oriented camera rays."""
    centers = np.asarray(centers, dtype=float)
    directions = np.vstack([normalize(v) for v in directions])
    a = np.zeros((3, 3))
    b = np.zeros(3)
    eye = np.eye(3)
    for center, direction in zip(centers, directions, strict=True):
        projector = eye - np.outer(direction, direction)
        a += projector
        b += projector @ center
    return np.linalg.solve(a, b)


def reconstruct_points(cameras: list[CameraRayModel], observations: np.ndarray) -> np.ndarray:
    """Triangulate one world point for each synchronized marker observation."""
    centers = np.vstack([camera.center for camera in cameras])
    points = []
    for point_idx in range(observations.shape[1]):
        directions = np.vstack(
            [
                camera.world_direction(observations[cam_idx, point_idx])
                for cam_idx, camera in enumerate(cameras)
            ]
        )
        points.append(triangulate_from_rays(centers, directions))
    return np.vstack(points)


def estimate_depths(
    cameras: list[CameraRayModel],
    observations: np.ndarray,
    points: np.ndarray,
) -> np.ndarray:
    """Return the optimal per-camera ray scale for fixed poses and points."""
    depths = np.empty((len(cameras), len(points)))
    for cam_idx, camera in enumerate(cameras):
        for point_idx, point in enumerate(points):
            direction = camera.world_direction(observations[cam_idx, point_idx])
            depths[cam_idx, point_idx] = float((point - camera.center) @ direction)
    return depths


def estimate_translations(
    rotations: list[Rotor3D],
    observations: np.ndarray,
    depths: np.ndarray,
    points: np.ndarray,
) -> np.ndarray:
    """Equation-style translation update: average point minus rotated ray."""
    translations = []
    for cam_idx, rotation in enumerate(rotations):
        predicted = np.vstack(
            [
                rotation.rotate(depths[cam_idx, point_idx] * observations[cam_idx, point_idx])
                for point_idx in range(points.shape[0])
            ]
        )
        translations.append(np.mean(points - predicted, axis=0))
    return np.vstack(translations)


def ray_residuals(
    cameras: list[CameraRayModel],
    observations: np.ndarray,
    points: np.ndarray,
) -> np.ndarray:
    """Per-observation perpendicular distance from a point to its camera ray."""
    residuals = np.empty((len(cameras), len(points)))
    for cam_idx, camera in enumerate(cameras):
        for point_idx, point in enumerate(points):
            direction = camera.world_direction(observations[cam_idx, point_idx])
            offset = point - camera.center
            residuals[cam_idx, point_idx] = np.linalg.norm(offset - (offset @ direction) * direction)
    return residuals


def camera_axes_trace(camera: CameraRayModel, *, scale: float = 0.28) -> list[go.Scatter3d]:
    """Small colored local frame traces for a camera."""
    axes = [
        (np.array([1.0, 0.0, 0.0]), COLORS["red"], f"{camera.name} x"),
        (np.array([0.0, 1.0, 0.0]), COLORS["green"], f"{camera.name} y"),
        (np.array([0.0, 0.0, 1.0]), COLORS["blue"], f"{camera.name} z"),
    ]
    traces: list[go.Scatter3d] = []
    for axis, color, name in axes:
        end = camera.center + scale * camera.rotation.rotate(axis)
        points = np.vstack([camera.center, end])
        traces.append(
            go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode="lines",
                name=name,
                line={"color": color, "width": 5},
                showlegend=False,
            )
        )
    return traces


def crystallography_orbit_figure(points: np.ndarray, *, title: str = "Cubic point-group orbit") -> go.Figure:
    """Build a 3-D Plotly view of a point-group orbit."""
    points = np.asarray(points, dtype=float)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=points[:, 0],
            y=points[:, 1],
            z=points[:, 2],
            mode="markers",
            name="orbit",
            marker={"size": 5, "color": np.arange(len(points)), "colorscale": "Viridis"},
        )
    )
    for axis, color, name in [
        (np.array([1.35, 0.0, 0.0]), COLORS["red"], "e1"),
        (np.array([0.0, 1.35, 0.0]), COLORS["green"], "e2"),
        (np.array([0.0, 0.0, 1.35]), COLORS["blue"], "e3"),
    ]:
        line = np.vstack([np.zeros(3), axis])
        fig.add_trace(
            go.Scatter3d(
                x=line[:, 0],
                y=line[:, 1],
                z=line[:, 2],
                mode="lines",
                name=name,
                line={"color": color, "width": 6},
            )
        )
    fig.update_layout(
        title=title,
        width=860,
        height=660,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        scene={
            "aspectmode": "cube",
            "xaxis": {"range": [-1.5, 1.5], "title": "x"},
            "yaxis": {"range": [-1.5, 1.5], "title": "y"},
            "zaxis": {"range": [-1.5, 1.5], "title": "z"},
        },
    )
    return fig


def camera_calibration_figure(
    cameras: list[CameraRayModel],
    true_points: np.ndarray,
    reconstructed_points: np.ndarray,
    observations: np.ndarray,
) -> go.Figure:
    """Build a 3-D Plotly scene for the synthetic external-calibration example."""
    fig = go.Figure()
    true_points = np.asarray(true_points, dtype=float)
    reconstructed_points = np.asarray(reconstructed_points, dtype=float)
    fig.add_trace(
        go.Scatter3d(
            x=true_points[:, 0],
            y=true_points[:, 1],
            z=true_points[:, 2],
            mode="markers+lines",
            name="true marker path",
            marker={"size": 4, "color": COLORS["gray"]},
            line={"color": COLORS["faint"], "width": 2},
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=reconstructed_points[:, 0],
            y=reconstructed_points[:, 1],
            z=reconstructed_points[:, 2],
            mode="markers",
            name="ray reconstruction",
            marker={"size": 4, "color": COLORS["orange"]},
        )
    )
    for cam_idx, camera in enumerate(cameras):
        fig.add_trace(
            go.Scatter3d(
                x=[camera.center[0]],
                y=[camera.center[1]],
                z=[camera.center[2]],
                mode="markers+text",
                text=[camera.name],
                textposition="top center",
                name=camera.name,
                marker={"size": 7, "color": COLORS["red"]},
            )
        )
        for trace in camera_axes_trace(camera):
            fig.add_trace(trace)
        for point_idx in range(0, observations.shape[1], 4):
            ray = camera.world_direction(observations[cam_idx, point_idx])
            segment = np.vstack([camera.center, camera.center + 2.1 * ray])
            fig.add_trace(
                go.Scatter3d(
                    x=segment[:, 0],
                    y=segment[:, 1],
                    z=segment[:, 2],
                    mode="lines",
                    name=f"{camera.name} sample rays",
                    line={"color": "rgba(196,60,57,0.24)", "width": 2},
                    showlegend=False,
                )
            )
    fig.update_layout(
        title="External calibration as ray-direction bookkeeping",
        width=940,
        height=700,
        margin={"l": 0, "r": 0, "t": 48, "b": 0},
        scene={
            "aspectmode": "data",
            "xaxis": {"title": "x"},
            "yaxis": {"title": "y"},
            "zaxis": {"title": "z"},
            "camera": {"eye": {"x": 1.5, "y": -1.9, "z": 1.15}},
        },
        legend={"x": 0.02, "y": 0.98, "bgcolor": "rgba(255,255,255,0.72)"},
    )
    return fig
