"""Numerical helpers for Chapter 14: rounds, tangents, and power geometry.

The routines use the conformal coordinate order ``[e1, e2, e3, no, ni]``.
They intentionally keep the implementation small and inspectable: enough
conformal structure to test the chapter claims, plus plain Euclidean recovery
code for spheres, circles, point pairs, power diagrams, fitting, and a simple
kinematics example.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

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


@dataclass(frozen=True)
class PointPair:
    """A directed pair of finite Euclidean points."""

    point_a: np.ndarray
    point_b: np.ndarray
    center: np.ndarray
    radius: float
    direction: np.ndarray


@dataclass(frozen=True)
class Circle3D:
    """A Euclidean circle carried by an oriented plane."""

    center: np.ndarray
    radius: float
    normal: np.ndarray
    u: np.ndarray
    v: np.ndarray
    orientation: float


@dataclass(frozen=True)
class Sphere3D:
    """A Euclidean sphere recovered from conformal round data."""

    center: np.ndarray
    radius: float
    orientation: float


@dataclass(frozen=True)
class SphereIntersection:
    """Intersection of two spheres: real circle, tangent circle, or imaginary circle."""

    kind: str
    center: np.ndarray
    radius: float
    normal: np.ndarray
    signed_radius_squared: float


@dataclass(frozen=True)
class PrimitiveFit:
    """Best conformal dual primitive through a point cloud."""

    kind: str
    vector: np.ndarray
    residual_rms: float
    center: np.ndarray | None = None
    radius: float | None = None
    normal: np.ndarray | None = None
    offset: float | None = None


def as_vector2(vector: Iterable[float]) -> np.ndarray:
    """Return ``vector`` as a finite 2-D float array."""
    array = np.asarray(vector, dtype=float)
    if array.shape != (2,) or not np.all(np.isfinite(array)):
        raise ValueError("expected a finite 2-D vector")
    return array


def as_vector3(vector: Iterable[float]) -> np.ndarray:
    """Return ``vector`` as a finite 3-D float array."""
    array = np.asarray(vector, dtype=float)
    if array.shape != (3,) or not np.all(np.isfinite(array)):
        raise ValueError("expected a finite 3-D vector")
    return array


def normalize(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Return a unit vector, raising when the input is too small."""
    array = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(array))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return array / length


def conformal_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the conformal inner product in the ``[e1, e2, e3, no, ni]`` basis."""
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


def dual_sphere(center: Iterable[float], radius: float) -> np.ndarray:
    """Return the dual sphere vector centered at ``center`` with radius ``radius``."""
    radius = float(radius)
    if radius < 0.0:
        raise ValueError("sphere radius must be nonnegative")
    return conformal_point(center) - 0.5 * radius * radius * NI


def dual_plane(normal: Iterable[float], offset: float) -> np.ndarray:
    """Return the unit dual plane vector for ``normal.x = offset``."""
    normal = as_vector3(normal)
    length = float(np.linalg.norm(normal))
    if length <= EPS:
        raise ValueError("plane normal must be nonzero")
    return np.array(
        [normal[0] / length, normal[1] / length, normal[2] / length, 0.0, float(offset) / length],
        dtype=float,
    )


def sphere_power(point: Iterable[float], sphere: Iterable[float]) -> float:
    """Return ``|x-c|^2-r^2`` by probing a dual sphere with a conformal point."""
    return -2.0 * conformal_inner(conformal_point(point), sphere)


def distance_squared_from_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return Euclidean squared distance from two conformal point representatives."""
    return -2.0 * conformal_inner(conformal_point(a), conformal_point(b))


def point_pair_from_points(a: Iterable[float], b: Iterable[float]) -> PointPair:
    """Recover the Euclidean parameters of the directed point pair through ``a`` and ``b``."""
    a = as_vector3(a)
    b = as_vector3(b)
    center = 0.5 * (a + b)
    delta = b - a
    radius = 0.5 * float(np.linalg.norm(delta))
    direction = normalize(delta)
    return PointPair(a, b, center, radius, direction)


def circle_basis_from_normal(normal: Iterable[float]) -> tuple[np.ndarray, np.ndarray]:
    """Return two unit vectors perpendicular to ``normal``."""
    n = normalize(normal)
    seed = np.array([1.0, 0.0, 0.0])
    if abs(float(np.dot(seed, n))) > 0.82:
        seed = np.array([0.0, 1.0, 0.0])
    u = normalize(np.cross(n, seed))
    v = normalize(np.cross(n, u))
    return u, v


def circle_from_points(
    a: Iterable[float],
    b: Iterable[float],
    c: Iterable[float],
    *,
    eps: float = EPS,
) -> Circle3D:
    """Recover the oriented circle through three noncollinear points."""
    a = as_vector3(a)
    b = as_vector3(b)
    c = as_vector3(c)
    ab = b - a
    ac = c - a
    raw_normal = np.cross(ab, ac)
    normal_length = float(np.linalg.norm(raw_normal))
    if normal_length <= eps:
        raise ValueError("the three points are collinear")
    normal = raw_normal / normal_length

    u0 = normalize(ab)
    v0 = normalize(np.cross(normal, u0))
    d = float(np.linalg.norm(ab))
    x2 = float(np.dot(ac, u0))
    y2 = float(np.dot(ac, v0))
    if abs(y2) <= eps:
        raise ValueError("the three points are numerically collinear")
    ux = 0.5 * d
    uy = (x2 * x2 + y2 * y2 - d * x2) / (2.0 * y2)
    center = a + ux * u0 + uy * v0
    radius = float(np.linalg.norm(center - a))
    u = normalize(a - center)
    v = normalize(np.cross(normal, u))
    orientation = float(np.sign(np.linalg.det(np.vstack([ab, ac, normal])))) or 1.0
    return Circle3D(center, radius, normal, u, v, orientation)


def sphere_from_points(
    a: Iterable[float],
    b: Iterable[float],
    c: Iterable[float],
    d: Iterable[float],
    *,
    eps: float = EPS,
) -> Sphere3D:
    """Recover the oriented sphere through four noncoplanar points."""
    pts = np.asarray([as_vector3(a), as_vector3(b), as_vector3(c), as_vector3(d)], dtype=float)
    p0 = pts[0]
    matrix = 2.0 * (pts[1:] - p0)
    rhs = np.sum(pts[1:] * pts[1:], axis=1) - float(np.dot(p0, p0))
    if abs(float(np.linalg.det(matrix))) <= eps:
        raise ValueError("the four points are coplanar")
    center = np.linalg.solve(matrix, rhs)
    radius = float(np.linalg.norm(center - p0))
    orientation = float(np.sign(np.linalg.det(pts[1:] - p0))) or 1.0
    return Sphere3D(center, radius, orientation)


def sample_circle(circle: Circle3D | SphereIntersection, count: int = 160) -> np.ndarray:
    """Sample points on a real or tangent circle."""
    if isinstance(circle, SphereIntersection):
        u, v = circle_basis_from_normal(circle.normal)
        center = circle.center
        radius = circle.radius
    else:
        u, v = circle.u, circle.v
        center = circle.center
        radius = circle.radius
    t = np.linspace(0.0, 2.0 * np.pi, count)
    return center + radius * (np.cos(t)[:, None] * u + np.sin(t)[:, None] * v)


def sample_sphere_mesh(
    sphere: Sphere3D,
    *,
    u_count: int = 48,
    v_count: int = 24,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return mesh grids for plotting a sphere surface."""
    u = np.linspace(0.0, 2.0 * np.pi, u_count)
    v = np.linspace(0.0, np.pi, v_count)
    uu, vv = np.meshgrid(u, v)
    x = sphere.center[0] + sphere.radius * np.cos(uu) * np.sin(vv)
    y = sphere.center[1] + sphere.radius * np.sin(uu) * np.sin(vv)
    z = sphere.center[2] + sphere.radius * np.cos(vv)
    return x, y, z


def two_sphere_intersection(
    center_a: Iterable[float],
    radius_a: float,
    center_b: Iterable[float],
    radius_b: float,
    *,
    eps: float = EPS,
) -> SphereIntersection:
    """Intersect two spheres and return the carrier circle parameters."""
    center_a = as_vector3(center_a)
    center_b = as_vector3(center_b)
    radius_a = float(radius_a)
    radius_b = float(radius_b)
    if radius_a < 0.0 or radius_b < 0.0:
        raise ValueError("radii must be nonnegative")
    delta = center_b - center_a
    distance = float(np.linalg.norm(delta))
    if distance <= eps:
        raise ValueError("sphere centers must be distinct")
    normal = delta / distance
    offset = (radius_a * radius_a - radius_b * radius_b + distance * distance) / (2.0 * distance)
    center = center_a + offset * normal
    signed_radius_squared = radius_a * radius_a - offset * offset
    if signed_radius_squared > eps:
        kind = "circle"
        radius = float(np.sqrt(signed_radius_squared))
    elif signed_radius_squared >= -eps:
        kind = "tangent"
        signed_radius_squared = 0.0
        radius = 0.0
    else:
        kind = "imaginary_circle"
        radius = float(np.sqrt(-signed_radius_squared))
    return SphereIntersection(kind, center, radius, normal, float(signed_radius_squared))


def tangent_frame_on_sphere(
    center: Iterable[float],
    radius: float,
    theta: float,
    phi: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return a point on a sphere and two tangent unit directions there."""
    center = as_vector3(center)
    radius = float(radius)
    radial = np.array(
        [
            np.cos(theta) * np.sin(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(phi),
        ],
        dtype=float,
    )
    point = center + radius * radial
    d_theta = normalize(np.array([-np.sin(theta), np.cos(theta), 0.0], dtype=float))
    d_phi = normalize(
        np.array(
            [
                np.cos(theta) * np.cos(phi),
                np.sin(theta) * np.cos(phi),
                -np.sin(phi),
            ],
            dtype=float,
        )
    )
    return point, d_theta, d_phi


def paraboloid_grid(
    xlim: tuple[float, float] = (-2.5, 2.5),
    ylim: tuple[float, float] = (-2.5, 2.5),
    count: int = 80,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the representative paraboloid ``z = 0.5*(x^2+y^2)``."""
    x = np.linspace(float(xlim[0]), float(xlim[1]), count)
    y = np.linspace(float(ylim[0]), float(ylim[1]), count)
    xx, yy = np.meshgrid(x, y)
    zz = 0.5 * (xx * xx + yy * yy)
    return xx, yy, zz


def paraboloid_tangent_plane(
    point: Iterable[float],
    xlim: tuple[float, float] = (-2.5, 2.5),
    ylim: tuple[float, float] = (-2.5, 2.5),
    count: int = 16,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the tangent plane to the representative paraboloid at a 2-D point."""
    point = as_vector2(point)
    xx, yy, _ = paraboloid_grid(xlim, ylim, count)
    zz = point[0] * xx + point[1] * yy - 0.5 * float(np.dot(point, point))
    return xx, yy, zz


def circle_plane_on_paraboloid(
    center: Iterable[float],
    radius: float,
    xlim: tuple[float, float] = (-2.5, 2.5),
    ylim: tuple[float, float] = (-2.5, 2.5),
    count: int = 16,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the affine plane whose intersection with the paraboloid is a circle."""
    center = as_vector2(center)
    radius = float(radius)
    xx, yy, _ = paraboloid_grid(xlim, ylim, count)
    zz = center[0] * xx + center[1] * yy + 0.5 * (radius * radius - float(np.dot(center, center)))
    return xx, yy, zz


def power_values(
    points: np.ndarray,
    centers: Iterable[Iterable[float]],
    radii: Iterable[float],
) -> np.ndarray:
    """Evaluate circle powers ``|x-c_i|^2-r_i^2`` at 2-D points."""
    points = np.asarray(points, dtype=float)
    centers = np.asarray(list(centers), dtype=float)
    radii = np.asarray(list(radii), dtype=float)
    if centers.ndim != 2 or centers.shape[1] != 2:
        raise ValueError("centers must be an array of 2-D points")
    if radii.shape != (centers.shape[0],):
        raise ValueError("one radius is required for each center")
    return np.sum((points[..., None, :] - centers) ** 2, axis=-1) - radii * radii


def power_diagram_grid(
    centers: Iterable[Iterable[float]],
    radii: Iterable[float],
    xlim: tuple[float, float] = (-3.0, 3.0),
    ylim: tuple[float, float] = (-2.5, 2.5),
    count: int = 180,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return grid coordinates, winning labels, and powers for a power diagram."""
    x = np.linspace(float(xlim[0]), float(xlim[1]), count)
    y = np.linspace(float(ylim[0]), float(ylim[1]), count)
    xx, yy = np.meshgrid(x, y)
    points = np.stack([xx, yy], axis=-1)
    powers = power_values(points, centers, radii)
    labels = np.argmin(powers, axis=-1)
    return xx, yy, labels, powers


def radical_axis_segment(
    center_i: Iterable[float],
    radius_i: float,
    center_j: Iterable[float],
    radius_j: float,
    xlim: tuple[float, float] = (-3.0, 3.0),
    ylim: tuple[float, float] = (-2.5, 2.5),
    *,
    eps: float = EPS,
) -> np.ndarray:
    """Clip the radical axis of two circles to a rectangular plotting box."""
    ci = as_vector2(center_i)
    cj = as_vector2(center_j)
    normal = 2.0 * (cj - ci)
    constant = float(np.dot(ci, ci) - np.dot(cj, cj) - radius_i * radius_i + radius_j * radius_j)
    points: list[np.ndarray] = []

    for x in xlim:
        if abs(normal[1]) > eps:
            y = -(normal[0] * x + constant) / normal[1]
            if ylim[0] - eps <= y <= ylim[1] + eps:
                points.append(np.array([x, y], dtype=float))
    for y in ylim:
        if abs(normal[0]) > eps:
            x = -(normal[1] * y + constant) / normal[0]
            if xlim[0] - eps <= x <= xlim[1] + eps:
                points.append(np.array([x, y], dtype=float))

    unique: list[np.ndarray] = []
    for point in points:
        if not any(np.linalg.norm(point - other) <= 1e-7 for other in unique):
            unique.append(point)
    if len(unique) < 2:
        return np.empty((0, 2), dtype=float)
    return np.asarray(unique[:2], dtype=float)


def fit_sphere_least_squares(points: Iterable[Iterable[float]]) -> Sphere3D:
    """Fit a sphere by linear least squares in the standard Euclidean equation."""
    points = np.asarray(list(points), dtype=float)
    if points.ndim != 2 or points.shape[1] != 3 or points.shape[0] < 4:
        raise ValueError("expected at least four 3-D points")
    matrix = np.column_stack([points, np.ones(points.shape[0])])
    rhs = -np.sum(points * points, axis=1)
    params, *_ = np.linalg.lstsq(matrix, rhs, rcond=None)
    center = -0.5 * params[:3]
    radius_squared = float(np.dot(center, center) - params[3])
    if radius_squared < -1e-8:
        raise ValueError("least-squares fit produced an imaginary sphere")
    radius = float(np.sqrt(max(radius_squared, 0.0)))
    return Sphere3D(center, radius, 1.0)


def fit_conformal_primitive(points: Iterable[Iterable[float]], *, eps: float = 1e-8) -> PrimitiveFit:
    """Fit a dual sphere or dual plane to points using the conformal incidence matrix."""
    points = np.asarray(list(points), dtype=float)
    if points.ndim != 2 or points.shape[1] != 3 or points.shape[0] < 4:
        raise ValueError("expected at least four 3-D points")
    norms = np.sum(points * points, axis=1)
    design = np.column_stack([points, -0.5 * norms, -np.ones(points.shape[0])])
    _, _, vh = np.linalg.svd(design, full_matrices=False)
    vector = vh[-1].astype(float)

    if abs(vector[3]) > eps:
        if vector[3] < 0.0:
            vector = -vector
        vector = vector / vector[3]
        center = vector[:3].copy()
        radius_squared = float(np.dot(center, center) - 2.0 * vector[4])
        kind = "sphere" if radius_squared >= 0.0 else "imaginary_sphere"
        radius = float(np.sqrt(abs(radius_squared)))
        residual = design @ vector
        return PrimitiveFit(kind, vector, float(np.sqrt(np.mean(residual * residual))), center, radius)

    normal_length = float(np.linalg.norm(vector[:3]))
    if normal_length <= eps:
        raise ValueError("SVD returned a degenerate primitive")
    vector = vector / normal_length
    if vector[4] < 0.0:
        vector = -vector
    residual = design @ vector
    return PrimitiveFit(
        "plane",
        vector,
        float(np.sqrt(np.mean(residual * residual))),
        normal=vector[:3].copy(),
        offset=float(vector[4]),
    )


def choose_elbow_on_circle(
    intersection: SphereIntersection,
    preferred_up: Iterable[float] = (0.0, 0.0, 1.0),
) -> np.ndarray:
    """Choose one inverse-kinematics elbow point from a sphere-intersection circle."""
    if intersection.kind == "imaginary_circle":
        raise ValueError("no real elbow circle exists")
    if intersection.radius <= EPS:
        return intersection.center.copy()
    preferred = as_vector3(preferred_up)
    tangent = preferred - float(np.dot(preferred, intersection.normal)) * intersection.normal
    if np.linalg.norm(tangent) <= EPS:
        tangent, _ = circle_basis_from_normal(intersection.normal)
    else:
        tangent = normalize(tangent)
    return intersection.center + intersection.radius * tangent


def two_link_elbow_circle(
    shoulder: Iterable[float],
    target: Iterable[float],
    upper_length: float,
    lower_length: float,
) -> SphereIntersection:
    """Return the elbow locus for a two-link arm as an intersection of two spheres."""
    return two_sphere_intersection(shoulder, upper_length, target, lower_length)


def sanity_checks() -> dict[str, float | str]:
    """Run compact numerical checks used by the Chapter 14 notebook."""
    a = np.array([0.2, -0.3, 0.4])
    b = np.array([1.1, 0.4, -0.2])
    c = np.array([-0.2, 1.0, 0.3])
    d = np.array([0.5, 0.2, 1.4])
    sphere = sphere_from_points(a, b, c, d)
    dual = dual_sphere(sphere.center, sphere.radius)
    circle = circle_from_points(a, b, c)
    tangent = two_sphere_intersection([0, 0, 0], 1.0, [2, 0, 0], 1.0)
    tangent_point, tangent_u, tangent_v = tangent_frame_on_sphere([0, 0, 0], 2.0, 0.7, 1.0)
    tangent_residual = max(abs(float(np.dot(tangent_point, tangent_u))), abs(float(np.dot(tangent_point, tangent_v))))

    p2 = np.array([0.8, -0.4])
    xx, yy, zz = paraboloid_tangent_plane(p2, (p2[0], p2[0]), (p2[1], p2[1]), 1)
    tangent_height = float(zz[0, 0])
    paraboloid_height = 0.5 * float(np.dot(p2, p2))

    centers = np.array([[-1.0, 0.2], [1.0, -0.1]], dtype=float)
    radii = np.array([0.8, 1.2], dtype=float)
    axis = radical_axis_segment(centers[0], radii[0], centers[1], radii[1])
    tie_error = 0.0
    if len(axis):
        powers = power_values(axis[0], centers, radii)
        tie_error = abs(float(powers[0] - powers[1]))

    rng = np.random.default_rng(14)
    cloud = sphere.center + sphere.radius * normalize_rows(rng.normal(size=(20, 3)))
    fit = fit_sphere_least_squares(cloud)
    gx, gy = np.meshgrid(np.linspace(-1.0, 1.0, 3), np.linspace(-0.8, 0.8, 3))
    plane_points = np.column_stack([gx.ravel(), gy.ravel(), np.full(gx.size, 0.35)])
    primitive = fit_conformal_primitive(plane_points)

    shoulder = np.array([0.0, 0.0, 0.0])
    target = np.array([1.2, 0.8, 0.55])
    elbow_circle = two_link_elbow_circle(shoulder, target, 1.25, 0.95)
    elbow = choose_elbow_on_circle(elbow_circle)

    return {
        "conformal_point_null_residual": abs(conformal_norm2(conformal_point(a))),
        "distance_identity_residual": abs(distance_squared_from_inner(a, b) - float(np.dot(a - b, a - b))),
        "sphere_incidence_max_abs_power": max(abs(sphere_power(point, dual)) for point in [a, b, c, d]),
        "circle_radius_spread": float(
            np.ptp([np.linalg.norm(point - circle.center) for point in [a, b, c]])
        ),
        "tangent_intersection_kind": tangent.kind,
        "tangent_radius_squared": abs(tangent.signed_radius_squared),
        "sphere_tangent_frame_dot_error": tangent_residual,
        "paraboloid_tangent_height_error": abs(tangent_height - paraboloid_height),
        "power_radical_axis_tie_error": tie_error,
        "sphere_fit_center_error": float(np.linalg.norm(fit.center - sphere.center)),
        "conformal_fit_plane_kind": primitive.kind,
        "ik_upper_length_error": abs(float(np.linalg.norm(elbow - shoulder)) - 1.25),
        "ik_lower_length_error": abs(float(np.linalg.norm(target - elbow)) - 0.95),
    }


def normalize_rows(rows: np.ndarray, *, eps: float = EPS) -> np.ndarray:
    """Normalize each row of a 2-D array."""
    rows = np.asarray(rows, dtype=float)
    lengths = np.linalg.norm(rows, axis=1)
    if np.any(lengths <= eps):
        raise ValueError("cannot normalize rows containing near-zero vectors")
    return rows / lengths[:, None]
