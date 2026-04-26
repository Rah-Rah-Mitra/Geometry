"""Numerical helpers for Chapter 15 Euclidean construction notebooks.

The routines in this module are deliberately small coordinate shadows of the
conformal model.  They use the common conformal coordinate order
``[e1, e2, e3, no, ni]`` with ``no.ni = -1``.  The helper does not attempt to be
a complete geometric algebra system; instead it provides inspectable functions
for incidence probes, sphere and plane meets, plunge-style constructions,
tangents, round factorization, affine combinations, and a few reusable Plotly
traces.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import plotly.graph_objects as go

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

COLORS = {
    "blue": "#2563eb",
    "cyan": "#0891b2",
    "green": "#16a34a",
    "lime": "#84cc16",
    "orange": "#ea580c",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "pink": "#db2777",
    "gray": "#475569",
    "light_gray": "rgba(148, 163, 184, 0.35)",
    "plane": "rgba(250, 204, 21, 0.28)",
    "sphere": "rgba(37, 99, 235, 0.16)",
}


def as_vector3(vector: Iterable[float]) -> np.ndarray:
    """Return ``vector`` as a finite 3-D float array."""
    value = np.asarray(vector, dtype=float)
    if value.shape != (3,):
        raise ValueError(f"expected a 3-D vector, got shape {value.shape}")
    if not np.all(np.isfinite(value)):
        raise ValueError("vector entries must be finite")
    return value


def as_points(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    """Return an ``(n, 3)`` float array."""
    value = np.asarray(points, dtype=float)
    if value.ndim == 1:
        value = value.reshape(1, 3)
    if value.ndim != 2 or value.shape[1] != 3:
        raise ValueError(f"expected points with shape (n, 3), got {value.shape}")
    if not np.all(np.isfinite(value)):
        raise ValueError("point entries must be finite")
    return value


def normalize(vector: Iterable[float], *, tol: float = EPS) -> np.ndarray:
    """Return a unit vector, raising on near-zero input."""
    value = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(value))
    if length <= tol:
        raise ValueError("cannot normalize a near-zero vector")
    return value / length


def orthonormal_frame(normal: Iterable[float]) -> tuple[np.ndarray, np.ndarray]:
    """Return two unit vectors perpendicular to ``normal`` and to each other."""
    n = normalize(normal)
    seed = np.array([1.0, 0.0, 0.0])
    if abs(float(np.dot(seed, n))) > 0.82:
        seed = np.array([0.0, 1.0, 0.0])
    u = normalize(seed - float(np.dot(seed, n)) * n)
    v = np.cross(n, u)
    return u, v


def cga_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the conformal inner product in the ``[e1,e2,e3,no,ni]`` basis."""
    a_value = np.asarray(a, dtype=float)
    b_value = np.asarray(b, dtype=float)
    if a_value.shape != (5,) or b_value.shape != (5,):
        raise ValueError("conformal vectors must have five coordinates")
    return float(a_value @ METRIC @ b_value)


def cga_norm2(vector: Iterable[float]) -> float:
    """Return the conformal squared norm of a vector."""
    return cga_inner(vector, vector)


def conformal_point(point: Iterable[float]) -> np.ndarray:
    """Embed a Euclidean point as ``x + no + 0.5*|x|^2*ni``."""
    p = as_vector3(point)
    return np.array([p[0], p[1], p[2], 1.0, 0.5 * float(np.dot(p, p))], dtype=float)


def conformal_weight(vector: Iterable[float]) -> float:
    """Return the finite-point weight ``-X.ni``."""
    return -cga_inner(np.asarray(vector, dtype=float), NI)


def recover_point(vector: Iterable[float], *, tol: float = EPS) -> np.ndarray:
    """Recover Euclidean coordinates from a weighted conformal point vector."""
    value = np.asarray(vector, dtype=float)
    if value.shape != (5,):
        raise ValueError("expected a conformal 5-vector")
    weight = conformal_weight(value)
    if abs(weight) <= tol:
        raise ZeroDivisionError("zero-weight vector does not represent a finite point")
    return value[:3] / weight


def normalized_point_vector(vector: Iterable[float], *, tol: float = EPS) -> np.ndarray:
    """Scale a conformal point vector to unit finite weight."""
    value = np.asarray(vector, dtype=float)
    weight = conformal_weight(value)
    if abs(weight) <= tol:
        raise ZeroDivisionError("zero-weight vector cannot be normalized as a point")
    return value / weight


def distance_squared_from_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Recover Euclidean squared distance from two conformal point vectors."""
    a_vec = normalized_point_vector(a if np.asarray(a).shape == (5,) else conformal_point(a))
    b_vec = normalized_point_vector(b if np.asarray(b).shape == (5,) else conformal_point(b))
    return float(-2.0 * cga_inner(a_vec, b_vec))


def dual_sphere_vector(center: Iterable[float], radius_squared: float) -> np.ndarray:
    """Return the dual sphere vector centered at ``center``.

    ``radius_squared`` may be negative, which is useful for visualizing the
    imaginary dual spheres that appear in affine combinations.
    """
    c = as_vector3(center)
    return conformal_point(c) - 0.5 * float(radius_squared) * NI


def dual_plane_vector(normal: Iterable[float], offset: float) -> np.ndarray:
    """Return a unit dual plane vector for ``normal.x = offset``."""
    n = as_vector3(normal)
    length = float(np.linalg.norm(n))
    if length <= EPS:
        raise ValueError("plane normal must be nonzero")
    n = n / length
    h = float(offset) / length
    return np.array([n[0], n[1], n[2], 0.0, h], dtype=float)


def sphere_power(point: Iterable[float], dual_sphere: Iterable[float]) -> float:
    """Return ``|x-c|^2-r^2`` from a dual sphere vector."""
    return -2.0 * cga_inner(conformal_point(point), np.asarray(dual_sphere, dtype=float))


def plane_probe(point: Iterable[float], dual_plane: Iterable[float]) -> float:
    """Return signed distance from ``point`` to a unit dual plane vector."""
    return cga_inner(conformal_point(point), np.asarray(dual_plane, dtype=float))


@dataclass(frozen=True)
class Line3D:
    """A 3-D line represented by one point and one unit direction."""

    point: np.ndarray
    direction: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(self, "point", as_vector3(self.point))
        object.__setattr__(self, "direction", normalize(self.direction))

    @classmethod
    def through(cls, a: Iterable[float], b: Iterable[float]) -> "Line3D":
        """Construct the line through two distinct points."""
        a_vec = as_vector3(a)
        b_vec = as_vector3(b)
        return cls(a_vec, b_vec - a_vec)

    def sample(self, t_min: float = -2.0, t_max: float = 2.0, n: int = 100) -> np.ndarray:
        """Sample points on the line."""
        t = np.linspace(t_min, t_max, n)
        return self.point + t[:, None] * self.direction

    def distance_to_points(self, points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
        """Return perpendicular distances from ``points`` to the line."""
        pts = as_points(points)
        offsets = pts - self.point
        along = offsets @ self.direction
        nearest = self.point + along[:, None] * self.direction
        return np.linalg.norm(pts - nearest, axis=1)


@dataclass(frozen=True)
class Plane3D:
    """A plane represented as ``normal.x = offset`` with unit normal."""

    normal: np.ndarray
    offset: float

    def __post_init__(self) -> None:
        normal = normalize(self.normal)
        object.__setattr__(self, "normal", normal)
        object.__setattr__(self, "offset", float(self.offset))

    @classmethod
    def from_point_normal(cls, point: Iterable[float], normal: Iterable[float]) -> "Plane3D":
        """Construct a plane through ``point`` with the given normal."""
        n = normalize(normal)
        return cls(n, float(np.dot(n, as_vector3(point))))

    @property
    def vector(self) -> np.ndarray:
        """Return the unit dual plane vector."""
        return dual_plane_vector(self.normal, self.offset)

    def signed_distance(self, points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
        """Return signed distances from points to the plane."""
        pts = as_points(points)
        return pts @ self.normal - self.offset

    def project_points(self, points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
        """Orthogonally project points onto the plane."""
        pts = as_points(points)
        return pts - self.signed_distance(pts)[:, None] * self.normal

    def basis(self) -> tuple[np.ndarray, np.ndarray]:
        """Return two unit directions spanning the plane."""
        return orthonormal_frame(self.normal)


@dataclass(frozen=True)
class Sphere3D:
    """A sphere, allowing negative squared radius for imaginary spheres."""

    center: np.ndarray
    radius_squared: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", as_vector3(self.center))
        object.__setattr__(self, "radius_squared", float(self.radius_squared))

    @classmethod
    def real(cls, center: Iterable[float], radius: float) -> "Sphere3D":
        """Construct a real sphere from a nonnegative radius."""
        radius = float(radius)
        if radius < 0:
            raise ValueError("radius must be nonnegative")
        return cls(as_vector3(center), radius * radius)

    @property
    def radius(self) -> float:
        """Return ``sqrt(radius_squared)`` for real spheres."""
        if self.radius_squared < -EPS:
            raise ValueError("imaginary sphere has no real radius")
        return float(np.sqrt(max(0.0, self.radius_squared)))

    @property
    def vector(self) -> np.ndarray:
        """Return the dual sphere vector."""
        return dual_sphere_vector(self.center, self.radius_squared)

    def power(self, points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
        """Return sphere power values ``|x-c|^2-r^2``."""
        pts = as_points(points)
        return np.sum((pts - self.center) ** 2, axis=1) - self.radius_squared


@dataclass(frozen=True)
class Circle3D:
    """A circle stored by center, radius, and oriented carrier normal."""

    center: np.ndarray
    radius: float
    normal: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", as_vector3(self.center))
        radius = float(self.radius)
        if radius < -EPS:
            raise ValueError("circle radius must be nonnegative")
        object.__setattr__(self, "radius", max(0.0, radius))
        object.__setattr__(self, "normal", normalize(self.normal))

    @classmethod
    def through_three_points(
        cls,
        a: Iterable[float],
        b: Iterable[float],
        c: Iterable[float],
    ) -> "Circle3D":
        """Return the circumcircle through three non-collinear points."""
        a_vec = as_vector3(a)
        b_vec = as_vector3(b)
        c_vec = as_vector3(c)
        ab = b_vec - a_vec
        ac = c_vec - a_vec
        n = np.cross(ab, ac)
        n2 = float(np.dot(n, n))
        if n2 <= EPS:
            raise ValueError("circle points are collinear or too close")
        center = a_vec + (
            float(np.dot(ab, ab)) * np.cross(ac, n)
            + float(np.dot(ac, ac)) * np.cross(n, ab)
        ) / (2.0 * n2)
        return cls(center, float(np.linalg.norm(center - a_vec)), n)

    def basis(self) -> tuple[np.ndarray, np.ndarray]:
        """Return two unit directions spanning the carrier plane."""
        return orthonormal_frame(self.normal)

    def sample(self, n: int = 180, endpoint: bool = True) -> np.ndarray:
        """Sample the circle."""
        u, v = self.basis()
        theta = np.linspace(0.0, 2.0 * np.pi, n, endpoint=endpoint)
        return self.center + self.radius * (
            np.cos(theta)[:, None] * u + np.sin(theta)[:, None] * v
        )

    def point_at_angle(self, angle: float) -> np.ndarray:
        """Return a point on the circle at a carrier-frame angle."""
        u, v = self.basis()
        return self.center + self.radius * (np.cos(angle) * u + np.sin(angle) * v)

    def tangent_line_at(self, point: Iterable[float]) -> Line3D:
        """Return the tangent line at a point on the circle."""
        p = as_vector3(point)
        radial = p - self.center
        if np.linalg.norm(radial) <= EPS:
            raise ValueError("cannot form a tangent at the circle center")
        direction = np.cross(self.normal, radial)
        return Line3D(p, direction)

    def residuals(self, points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
        """Return absolute carrier and radius residuals for points."""
        pts = as_points(points)
        plane = carrier_plane(self)
        plane_residual = np.abs(plane.signed_distance(pts))
        radius_residual = np.abs(np.linalg.norm(pts - self.center, axis=1) - self.radius)
        return np.maximum(plane_residual, radius_residual)


@dataclass(frozen=True)
class SphereSphereMeet:
    """Radical circle data for the meet of two spheres."""

    circle: Circle3D
    radius_squared: float
    kind: str
    axis_parameter: float


@dataclass(frozen=True)
class ThreeSphereMeet:
    """The point-pair meet of three spheres, or its imaginary location."""

    points: np.ndarray
    radical_point: np.ndarray
    radical_direction: np.ndarray
    discriminant: float
    kind: str


@dataclass(frozen=True)
class AffineDualSphere:
    """A normalized affine combination of two conformal points."""

    lam: float
    vector: np.ndarray
    center: np.ndarray
    radius_squared: float


def carrier_plane(circle: Circle3D) -> Plane3D:
    """Return the carrier plane of a circle."""
    return Plane3D.from_point_normal(circle.center, circle.normal)


def surround_sphere(circle: Circle3D) -> Sphere3D:
    """Return the smallest sphere containing a circle."""
    return Sphere3D.real(circle.center, circle.radius)


def factorization_residuals(circle: Circle3D, samples: int = 160) -> dict[str, float]:
    """Check that carrier plane and surround sphere recover a circle."""
    pts = circle.sample(samples)
    carrier = carrier_plane(circle)
    surround = surround_sphere(circle)
    return {
        "carrier_plane_max_distance": float(np.max(np.abs(carrier.signed_distance(pts)))),
        "surround_sphere_max_power": float(np.max(np.abs(surround.power(pts)))),
    }


def sphere_sphere_meet(a: Sphere3D, b: Sphere3D, *, tol: float = EPS) -> SphereSphereMeet:
    """Return the radical circle location for the meet of two spheres."""
    delta = b.center - a.center
    distance = float(np.linalg.norm(delta))
    if distance <= tol:
        raise ValueError("concentric spheres do not determine a unique radical circle")
    axis = delta / distance
    t = (a.radius_squared - b.radius_squared + distance * distance) / (2.0 * distance)
    center = a.center + t * axis
    radius_squared = a.radius_squared - t * t
    if radius_squared > tol:
        kind = "real circle"
    elif radius_squared < -tol:
        kind = "imaginary circle"
    else:
        kind = "tangent point"
    circle = Circle3D(center, float(np.sqrt(abs(radius_squared))), axis)
    return SphereSphereMeet(circle=circle, radius_squared=float(radius_squared), kind=kind, axis_parameter=float(t))


def three_sphere_meet(
    a: Sphere3D,
    b: Sphere3D,
    c: Sphere3D,
    *,
    tol: float = EPS,
) -> ThreeSphereMeet:
    """Return the point-pair meet of three spheres by trilateration."""
    centers = np.array([a.center, b.center, c.center], dtype=float)
    radii2 = np.array([a.radius_squared, b.radius_squared, c.radius_squared], dtype=float)
    A = 2.0 * (centers[1:] - centers[0])
    rhs = (
        np.sum(centers[1:] ** 2, axis=1)
        - np.sum(centers[0] ** 2)
        + radii2[0]
        - radii2[1:]
    )
    rank = int(np.linalg.matrix_rank(A, tol=tol))
    if rank < 2:
        raise ValueError("sphere centers do not determine a stable radical line")
    radical_point = np.linalg.lstsq(A, rhs, rcond=None)[0]
    _, _, vh = np.linalg.svd(A)
    direction = normalize(vh[-1])
    offset = radical_point - centers[0]
    bq = 2.0 * float(np.dot(direction, offset))
    cq = float(np.dot(offset, offset) - radii2[0])
    discriminant = bq * bq - 4.0 * cq
    if discriminant > tol:
        root = float(np.sqrt(discriminant))
        ts = np.array([(-bq - root) / 2.0, (-bq + root) / 2.0])
        points = radical_point + ts[:, None] * direction
        kind = "real point pair"
    elif discriminant >= -tol:
        t = -bq / 2.0
        points = (radical_point + t * direction).reshape(1, 3)
        kind = "tangent point"
    else:
        points = np.zeros((0, 3), dtype=float)
        kind = "imaginary point pair"
    return ThreeSphereMeet(
        points=points,
        radical_point=radical_point,
        radical_direction=direction,
        discriminant=float(discriminant),
        kind=kind,
    )


def circle_from_points(points: Iterable[Iterable[float]] | np.ndarray) -> Circle3D:
    """Return the circle through three point samples."""
    pts = as_points(points)
    if pts.shape[0] != 3:
        raise ValueError("expected exactly three points")
    return Circle3D.through_three_points(pts[0], pts[1], pts[2])


def tangent_residual(circle: Circle3D, point: Iterable[float]) -> dict[str, float]:
    """Return simple tangent checks at ``point`` on ``circle``."""
    p = as_vector3(point)
    line = circle.tangent_line_at(p)
    radial = normalize(p - circle.center)
    return {
        "point_on_circle": float(abs(np.linalg.norm(p - circle.center) - circle.radius)),
        "tangent_radial_dot": float(abs(np.dot(line.direction, radial))),
        "tangent_in_carrier_dot": float(abs(np.dot(line.direction, circle.normal))),
    }


def finite_difference_tangent(circle: Circle3D, angle: float, step: float = 1e-5) -> np.ndarray:
    """Return a numerical tangent direction from nearby circle samples."""
    plus = circle.point_at_angle(angle + step)
    minus = circle.point_at_angle(angle - step)
    return normalize((plus - minus) / (2.0 * step))


def affine_dual_sphere(p: Iterable[float], q: Iterable[float], lam: float) -> AffineDualSphere:
    """Return ``lam*P + (1-lam)*Q`` interpreted as a normalized dual sphere."""
    p_vec = conformal_point(p)
    q_vec = conformal_point(q)
    lam = float(lam)
    vector = lam * p_vec + (1.0 - lam) * q_vec
    center, radius_squared = dual_sphere_center_radius_squared(vector)
    return AffineDualSphere(lam=lam, vector=vector, center=center, radius_squared=radius_squared)


def dual_sphere_center_radius_squared(vector: Iterable[float], *, tol: float = EPS) -> tuple[np.ndarray, float]:
    """Decode a normalized dual sphere vector as ``(center, radius_squared)``."""
    value = np.asarray(vector, dtype=float)
    if value.shape != (5,):
        raise ValueError("expected a conformal 5-vector")
    weight = conformal_weight(value)
    if abs(weight) <= tol:
        raise ZeroDivisionError("zero-weight vector is not a finite dual sphere")
    normalized = value / weight
    center = normalized[:3]
    radius_squared = float(np.dot(center, center) - 2.0 * normalized[4])
    return center, radius_squared


def flat_point_interpolation(p: Iterable[float], q: Iterable[float], lam: float) -> np.ndarray:
    """Return the Euclidean location of the affine combination of flat points."""
    p_vec = as_vector3(p)
    q_vec = as_vector3(q)
    lam = float(lam)
    return lam * p_vec + (1.0 - lam) * q_vec


def smallest_sphere_through_two_points(p: Iterable[float], q: Iterable[float]) -> Sphere3D:
    """Return the smallest sphere through two points."""
    p_vec = as_vector3(p)
    q_vec = as_vector3(q)
    center = 0.5 * (p_vec + q_vec)
    radius = 0.5 * float(np.linalg.norm(p_vec - q_vec))
    return Sphere3D.real(center, radius)


def project_points_to_plane(points: Iterable[Iterable[float]] | np.ndarray, plane: Plane3D) -> np.ndarray:
    """Orthogonally project points onto a plane."""
    return plane.project_points(points)


def contour_circle_from_viewpoint(sphere: Sphere3D, eye: Iterable[float]) -> Circle3D:
    """Return the tangent contour circle of a sphere seen from ``eye``."""
    if sphere.radius_squared <= EPS:
        raise ValueError("contour requires a real sphere with positive radius")
    eye_vec = as_vector3(eye)
    delta = eye_vec - sphere.center
    distance2 = float(np.dot(delta, delta))
    if distance2 <= sphere.radius_squared + EPS:
        raise ValueError("eye must be outside the sphere")
    normal = normalize(delta)
    center = sphere.center + (sphere.radius_squared / distance2) * delta
    radius = float(np.sqrt(sphere.radius_squared * (distance2 - sphere.radius_squared) / distance2))
    return Circle3D(center, radius, normal)


def contour_tangent_residuals(sphere: Sphere3D, eye: Iterable[float], circle: Circle3D) -> dict[str, float]:
    """Check that contour points are on the sphere and tangent from the eye."""
    eye_vec = as_vector3(eye)
    pts = circle.sample(96)
    sphere_residual = float(np.max(np.abs(sphere.power(pts))))
    radii = pts - sphere.center
    sight = eye_vec - pts
    tangent_residual = float(np.max(np.abs(np.sum(radii * sight, axis=1))))
    return {
        "sphere_power_max": sphere_residual,
        "radius_sight_dot_max": tangent_residual,
    }


def curve_trace(points: Iterable[Iterable[float]] | np.ndarray, name: str, color: str, width: int = 5) -> go.Scatter3d:
    """Return a Plotly 3-D curve trace."""
    pts = as_points(points)
    return go.Scatter3d(
        x=pts[:, 0],
        y=pts[:, 1],
        z=pts[:, 2],
        mode="lines",
        name=name,
        line={"color": color, "width": width},
    )


def point_trace(
    points: Iterable[Iterable[float]] | np.ndarray,
    labels: Sequence[str] | None,
    color: str,
    size: int = 5,
) -> go.Scatter3d:
    """Return a Plotly point trace."""
    pts = as_points(points)
    text = None if labels is None else list(labels)
    mode = "markers" if text is None else "markers+text"
    return go.Scatter3d(
        x=pts[:, 0],
        y=pts[:, 1],
        z=pts[:, 2],
        mode=mode,
        text=text,
        textposition="top center",
        name="points" if text is None else "labeled points",
        marker={"size": size, "color": color},
    )


def line_trace(
    line: Line3D,
    name: str,
    color: str,
    *,
    t_min: float = -2.0,
    t_max: float = 2.0,
    width: int = 5,
) -> go.Scatter3d:
    """Return a Plotly trace for a sampled line."""
    return curve_trace(line.sample(t_min, t_max), name, color, width)


def circle_trace(circle: Circle3D, name: str, color: str, width: int = 6, samples: int = 180) -> go.Scatter3d:
    """Return a Plotly trace for a circle."""
    return curve_trace(circle.sample(samples), name, color, width)


def plane_surface_trace(
    plane: Plane3D,
    name: str,
    *,
    size: float = 2.2,
    color: str = COLORS["plane"],
) -> go.Surface:
    """Return a translucent Plotly surface for a plane."""
    u, v = plane.basis()
    grid = np.linspace(-size, size, 18)
    uu, vv = np.meshgrid(grid, grid)
    center = plane.offset * plane.normal
    pts = center + uu[..., None] * u + vv[..., None] * v
    return go.Surface(
        x=pts[..., 0],
        y=pts[..., 1],
        z=pts[..., 2],
        name=name,
        showscale=False,
        opacity=0.34,
        surfacecolor=np.zeros_like(uu),
        colorscale=[[0.0, color], [1.0, color]],
    )


def sphere_surface_trace(
    sphere: Sphere3D,
    name: str,
    *,
    color: str = COLORS["sphere"],
    samples: int = 36,
) -> go.Surface:
    """Return a translucent Plotly surface for a real sphere."""
    radius = sphere.radius
    theta = np.linspace(0.0, 2.0 * np.pi, samples)
    phi = np.linspace(0.0, np.pi, samples // 2)
    theta_grid, phi_grid = np.meshgrid(theta, phi)
    x = sphere.center[0] + radius * np.cos(theta_grid) * np.sin(phi_grid)
    y = sphere.center[1] + radius * np.sin(theta_grid) * np.sin(phi_grid)
    z = sphere.center[2] + radius * np.cos(phi_grid)
    return go.Surface(
        x=x,
        y=y,
        z=z,
        name=name,
        showscale=False,
        opacity=0.2,
        surfacecolor=np.zeros_like(x),
        colorscale=[[0.0, color], [1.0, color]],
    )


def finish_figure(fig: go.Figure, title: str, *, height: int = 660) -> go.Figure:
    """Apply consistent notebook styling to a Plotly 3-D figure."""
    fig.update_layout(
        title=title,
        height=height,
        margin={"l": 0, "r": 0, "t": 56, "b": 0},
        legend={"orientation": "h", "y": 0.0},
        scene={
            "aspectmode": "data",
            "xaxis_title": "x",
            "yaxis_title": "y",
            "zaxis_title": "z",
            "xaxis": {"backgroundcolor": "rgb(248,250,252)", "gridcolor": "white"},
            "yaxis": {"backgroundcolor": "rgb(248,250,252)", "gridcolor": "white"},
            "zaxis": {"backgroundcolor": "rgb(248,250,252)", "gridcolor": "white"},
        },
    )
    return fig


def sanity_checks() -> dict[str, float]:
    """Run compact numerical checks used by the chapter notebook."""
    p = np.array([0.25, -0.4, 0.7])
    q = np.array([1.1, 0.35, -0.2])
    P = conformal_point(p)
    Q = conformal_point(q)
    sphere = Sphere3D.real([0.2, -0.1, 0.25], 1.35)
    point_on_sphere = sphere.center + sphere.radius * normalize([1.0, 0.5, -0.25])

    s1 = Sphere3D.real([0.0, 0.0, 0.0], 1.4)
    s2 = Sphere3D.real([1.0, 0.15, 0.0], 1.1)
    s3 = Sphere3D.real([0.35, 1.0, 0.05], 1.0)
    meet = three_sphere_meet(s1, s2, s3)
    meet_power = 0.0
    if meet.points.size:
        powers = np.column_stack([s1.power(meet.points), s2.power(meet.points), s3.power(meet.points)])
        meet_power = float(np.max(np.abs(powers)))

    circle = Circle3D.through_three_points([1.0, 0.0, 0.2], [0.2, 1.1, -0.1], [-0.8, 0.1, 0.35])
    point = circle.point_at_angle(0.7)
    tangent = circle.tangent_line_at(point)
    fd = finite_difference_tangent(circle, 0.7)
    affine = affine_dual_sphere(p, q, 0.35)
    surround = smallest_sphere_through_two_points(p, q)
    plane = Plane3D.from_point_normal([0.2, -0.1, 0.3], [0.4, -0.2, 1.0])
    projected = plane.project_points(circle.sample(40))
    contour_sphere = Sphere3D.real([0.15, -0.2, 0.35], 0.9)
    contour = contour_circle_from_viewpoint(contour_sphere, [2.4, 1.3, 1.6])
    contour_checks = contour_tangent_residuals(contour_sphere, [2.4, 1.3, 1.6], contour)

    return {
        "point_null_residual": abs(cga_norm2(P)),
        "distance_identity_residual": abs(distance_squared_from_inner(P, Q) - float(np.dot(p - q, p - q))),
        "sphere_power_residual": abs(sphere_power(point_on_sphere, sphere.vector)),
        "three_sphere_meet_power_residual": meet_power,
        "tangent_radial_dot": abs(float(np.dot(tangent.direction, normalize(point - circle.center)))),
        "tangent_finite_difference_alignment": 1.0 - abs(float(np.dot(tangent.direction, fd))),
        "factorization_carrier_residual": factorization_residuals(circle)["carrier_plane_max_distance"],
        "factorization_surround_residual": factorization_residuals(circle)["surround_sphere_max_power"],
        "affine_center_residual": float(np.linalg.norm(affine.center - flat_point_interpolation(p, q, 0.35))),
        "affine_radius_squared_residual": abs(
            affine.radius_squared + 0.35 * (1.0 - 0.35) * float(np.dot(p - q, p - q))
        ),
        "affine_surround_orthogonality": abs(cga_inner(affine.vector, surround.vector)),
        "projection_plane_residual": float(np.max(np.abs(plane.signed_distance(projected)))),
        "contour_sphere_residual": contour_checks["sphere_power_max"],
        "contour_tangent_residual": contour_checks["radius_sight_dot_max"],
    }
