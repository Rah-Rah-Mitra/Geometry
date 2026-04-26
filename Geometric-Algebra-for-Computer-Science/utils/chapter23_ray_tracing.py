"""Small ray-tracing helpers for Chapter 23.

The module intentionally stays close to the geometric concepts in the notebook:
rays are point-direction pairs, meshes are vertices plus triangular faces, BSP nodes
are spatial half-space splits, and shading is a compact Phong-style computation.
It is not a production renderer; it is a readable lab implementation with enough
structure to test the choices discussed in the chapter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import radians, tan
from typing import Iterable

import numpy as np

EPSILON = 1.0e-8


def as_vector3(value: Iterable[float]) -> np.ndarray:
    """Return *value* as a length-three float array."""
    array = np.asarray(value, dtype=float)
    if array.shape != (3,):
        raise ValueError(f"expected a 3-vector, got shape {array.shape}")
    return array


def normalize(value: Iterable[float], *, eps: float = EPSILON) -> np.ndarray:
    """Return a unit vector, raising on near-zero input."""
    vector = as_vector3(value)
    length = float(np.linalg.norm(vector))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return vector / length


def reflect_direction(direction: Iterable[float], normal: Iterable[float]) -> np.ndarray:
    """Reflect a direction vector in the plane with unit normal *normal*."""
    d = normalize(direction)
    n = normalize(normal)
    return normalize(d - 2.0 * np.dot(d, n) * n)


def refract_direction(
    direction: Iterable[float],
    normal: Iterable[float],
    eta_in_over_out: float,
) -> np.ndarray | None:
    """Refract a direction by Snell's law.

    The return value is ``None`` when total internal reflection occurs. The input
    direction points toward the surface; the normal is expected to point against the
    incoming ray.
    """
    d = normalize(direction)
    n = normalize(normal)
    cos_i = -float(np.dot(n, d))
    sin_t2 = eta_in_over_out * eta_in_over_out * (1.0 - cos_i * cos_i)
    if sin_t2 > 1.0:
        return None
    cos_t = float(np.sqrt(max(0.0, 1.0 - sin_t2)))
    return normalize(eta_in_over_out * d + (eta_in_over_out * cos_i - cos_t) * n)


def rotation_matrix(axis: Iterable[float], angle_radians: float) -> np.ndarray:
    """Rodrigues rotation matrix for a right-handed rotation about *axis*."""
    x, y, z = normalize(axis)
    c = float(np.cos(angle_radians))
    s = float(np.sin(angle_radians))
    one_c = 1.0 - c
    return np.array(
        [
            [c + x * x * one_c, x * y * one_c - z * s, x * z * one_c + y * s],
            [y * x * one_c + z * s, c + y * y * one_c, y * z * one_c - x * s],
            [z * x * one_c - y * s, z * y * one_c + x * s, c + z * z * one_c],
        ],
        dtype=float,
    )


def cga_point(point: Iterable[float]) -> np.ndarray:
    """A compact conformal point coordinate stand-in.

    Coordinates are ordered as ``(x, y, z, no, ni)`` with ``no.ni = -1``. This is
    enough for the notebook's distance identity checks without implementing a full
    multivector algebra.
    """
    x = as_vector3(point)
    return np.array([x[0], x[1], x[2], 1.0, 0.5 * float(np.dot(x, x))], dtype=float)


def cga_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Inner product for the compact conformal coordinates from :func:`cga_point`."""
    aa = np.asarray(a, dtype=float)
    bb = np.asarray(b, dtype=float)
    return float(np.dot(aa[:3], bb[:3]) - aa[3] * bb[4] - aa[4] * bb[3])


def cga_distance_squared(a: Iterable[float], b: Iterable[float]) -> float:
    """Recover Euclidean squared distance from two conformal point stand-ins."""
    return -2.0 * cga_inner(cga_point(a), cga_point(b))


@dataclass
class Material:
    """Surface parameters used by the small renderer."""

    color: np.ndarray
    ambient: float = 0.08
    diffuse: float = 0.78
    specular: float = 0.25
    shininess: float = 40.0
    reflectivity: float = 0.0

    def __post_init__(self) -> None:
        self.color = np.asarray(self.color, dtype=float)
        if self.color.shape != (3,):
            raise ValueError("material color must be an RGB triple")
        self.color = np.clip(self.color, 0.0, 1.0)


@dataclass
class Light:
    """A small point light."""

    position: np.ndarray
    color: np.ndarray = field(default_factory=lambda: np.ones(3))
    intensity: float = 1.0

    def __post_init__(self) -> None:
        self.position = as_vector3(self.position)
        self.color = np.asarray(self.color, dtype=float)
        if self.color.shape != (3,):
            raise ValueError("light color must be an RGB triple")


@dataclass
class Ray:
    """A ray represented by an origin, unit direction, and parameter interval."""

    origin: np.ndarray
    direction: np.ndarray
    t_min: float = 1.0e-4
    t_max: float = np.inf

    def __post_init__(self) -> None:
        self.origin = as_vector3(self.origin)
        self.direction = normalize(self.direction)
        self.t_min = float(self.t_min)
        self.t_max = float(self.t_max)

    def at(self, t: float) -> np.ndarray:
        """Point at parameter *t*."""
        return self.origin + float(t) * self.direction


@dataclass
class HitRecord:
    """Intersection result for one ray and one mesh."""

    t: float
    point: np.ndarray
    normal: np.ndarray
    face_index: int
    barycentric: np.ndarray
    material: Material
    mesh_name: str


@dataclass
class IntersectStats:
    """Counters that make acceleration effects inspectable."""

    sphere_tests: int = 0
    box_tests: int = 0
    triangle_tests: int = 0
    nodes_visited: int = 0
    leaves_visited: int = 0

    def add(self, other: "IntersectStats") -> None:
        self.sphere_tests += other.sphere_tests
        self.box_tests += other.box_tests
        self.triangle_tests += other.triangle_tests
        self.nodes_visited += other.nodes_visited
        self.leaves_visited += other.leaves_visited

    def as_dict(self) -> dict[str, int]:
        return {
            "sphere_tests": self.sphere_tests,
            "box_tests": self.box_tests,
            "triangle_tests": self.triangle_tests,
            "nodes_visited": self.nodes_visited,
            "leaves_visited": self.leaves_visited,
        }


@dataclass
class TriangleMesh:
    """A triangular mesh with optional smooth vertex normals."""

    vertices: np.ndarray
    faces: np.ndarray
    material: Material
    name: str = "mesh"
    vertex_normals: np.ndarray | None = None

    def __post_init__(self) -> None:
        self.vertices = np.asarray(self.vertices, dtype=float)
        self.faces = np.asarray(self.faces, dtype=int)
        if self.vertices.ndim != 2 or self.vertices.shape[1] != 3:
            raise ValueError("vertices must have shape (n, 3)")
        if self.faces.ndim != 2 or self.faces.shape[1] != 3:
            raise ValueError("faces must have shape (m, 3)")
        if self.vertex_normals is None:
            self.vertex_normals = compute_vertex_normals(self.vertices, self.faces)
        else:
            self.vertex_normals = np.asarray(self.vertex_normals, dtype=float)
            if self.vertex_normals.shape != self.vertices.shape:
                raise ValueError("vertex normals must match vertices")
            self.vertex_normals = normalize_rows(self.vertex_normals)

    @property
    def face_normals(self) -> np.ndarray:
        return compute_face_normals(self.vertices, self.faces)[0]

    @property
    def face_areas(self) -> np.ndarray:
        return compute_face_normals(self.vertices, self.faces)[1]

    @property
    def triangle_count(self) -> int:
        return int(self.faces.shape[0])

    def bounds(self, face_indices: np.ndarray | None = None) -> tuple[np.ndarray, np.ndarray]:
        if face_indices is None:
            points = self.vertices
        else:
            points = self.vertices[self.faces[np.asarray(face_indices, dtype=int)].reshape(-1)]
        return points.min(axis=0), points.max(axis=0)

    def bounding_sphere(self) -> tuple[np.ndarray, float]:
        b_min, b_max = self.bounds()
        center = 0.5 * (b_min + b_max)
        radius = float(np.max(np.linalg.norm(self.vertices - center, axis=1)))
        return center, radius

    def transformed(
        self,
        *,
        matrix: np.ndarray | None = None,
        translation: Iterable[float] | None = None,
        name: str | None = None,
    ) -> "TriangleMesh":
        mat = np.eye(3) if matrix is None else np.asarray(matrix, dtype=float)
        shift = np.zeros(3) if translation is None else as_vector3(translation)
        vertices = self.vertices @ mat.T + shift
        normals = normalize_rows(self.vertex_normals @ mat.T)
        return TriangleMesh(
            vertices=vertices,
            faces=self.faces.copy(),
            material=self.material,
            name=name or self.name,
            vertex_normals=normals,
        )


def normalize_rows(values: np.ndarray, *, eps: float = EPSILON) -> np.ndarray:
    """Normalize each row and leave near-zero rows unchanged."""
    array = np.asarray(values, dtype=float)
    lengths = np.linalg.norm(array, axis=1, keepdims=True)
    safe = np.where(lengths > eps, lengths, 1.0)
    return array / safe


def compute_face_normals(vertices: np.ndarray, faces: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return unit face normals and triangle areas."""
    triangles = vertices[faces]
    raw = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    lengths = np.linalg.norm(raw, axis=1)
    normals = raw / np.where(lengths[:, None] > EPSILON, lengths[:, None], 1.0)
    return normals, 0.5 * lengths


def compute_vertex_normals(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    """Area-weighted vertex normal average."""
    face_normals, face_areas = compute_face_normals(vertices, faces)
    normals = np.zeros_like(vertices, dtype=float)
    for face, normal, area in zip(faces, face_normals, face_areas, strict=True):
        normals[face] += normal * area
    return normalize_rows(normals)


def triangle_centroids(mesh: TriangleMesh, face_indices: np.ndarray | None = None) -> np.ndarray:
    """Centroids for all or selected mesh triangles."""
    faces = mesh.faces if face_indices is None else mesh.faces[np.asarray(face_indices, dtype=int)]
    return mesh.vertices[faces].mean(axis=1)


def ray_sphere_interval(ray: Ray, center: Iterable[float], radius: float) -> tuple[float, float] | None:
    """Intersection interval between a ray and a sphere."""
    c = as_vector3(center)
    oc = ray.origin - c
    b = float(np.dot(oc, ray.direction))
    c_term = float(np.dot(oc, oc) - radius * radius)
    discriminant = b * b - c_term
    if discriminant < 0.0:
        return None
    root = float(np.sqrt(discriminant))
    t0 = -b - root
    t1 = -b + root
    lo = max(t0, ray.t_min)
    hi = min(t1, ray.t_max)
    if hi < lo:
        return None
    return lo, hi


def ray_aabb_interval(
    ray: Ray,
    bounds_min: Iterable[float],
    bounds_max: Iterable[float],
    *,
    t_max: float | None = None,
) -> tuple[float, float] | None:
    """Intersection interval between a ray and an axis-aligned bounding box."""
    lo = ray.t_min
    hi = ray.t_max if t_max is None else min(ray.t_max, float(t_max))
    b_min = as_vector3(bounds_min)
    b_max = as_vector3(bounds_max)
    for axis in range(3):
        direction = ray.direction[axis]
        if abs(direction) <= EPSILON:
            if ray.origin[axis] < b_min[axis] or ray.origin[axis] > b_max[axis]:
                return None
            continue
        inv = 1.0 / direction
        t0 = (b_min[axis] - ray.origin[axis]) * inv
        t1 = (b_max[axis] - ray.origin[axis]) * inv
        if t0 > t1:
            t0, t1 = t1, t0
        lo = max(lo, float(t0))
        hi = min(hi, float(t1))
        if hi < lo:
            return None
    return lo, hi


def ray_triangle_intersection(
    ray: Ray,
    v0: np.ndarray,
    v1: np.ndarray,
    v2: np.ndarray,
) -> tuple[float, np.ndarray] | None:
    """Moller-Trumbore intersection of a ray with one two-sided triangle."""
    edge1 = v1 - v0
    edge2 = v2 - v0
    pvec = np.cross(ray.direction, edge2)
    det = float(np.dot(edge1, pvec))
    if abs(det) <= EPSILON:
        return None
    inv_det = 1.0 / det
    tvec = ray.origin - v0
    u = float(np.dot(tvec, pvec) * inv_det)
    if u < -EPSILON or u > 1.0 + EPSILON:
        return None
    qvec = np.cross(tvec, edge1)
    v = float(np.dot(ray.direction, qvec) * inv_det)
    if v < -EPSILON or u + v > 1.0 + EPSILON:
        return None
    t = float(np.dot(edge2, qvec) * inv_det)
    if t < ray.t_min or t > ray.t_max:
        return None
    barycentric = np.array([1.0 - u - v, u, v], dtype=float)
    return t, barycentric


def _hit_from_face(mesh: TriangleMesh, ray: Ray, face_index: int, t: float, bary: np.ndarray) -> HitRecord:
    face = mesh.faces[face_index]
    point = ray.at(t)
    normal = bary @ mesh.vertex_normals[face]
    if np.linalg.norm(normal) <= EPSILON:
        normal = mesh.face_normals[face_index]
    normal = normalize(normal)
    if np.dot(normal, ray.direction) > 0.0:
        normal = -normal
    return HitRecord(
        t=float(t),
        point=point,
        normal=normal,
        face_index=int(face_index),
        barycentric=bary,
        material=mesh.material,
        mesh_name=mesh.name,
    )


def intersect_mesh_naive(mesh: TriangleMesh, ray: Ray) -> tuple[HitRecord | None, IntersectStats]:
    """Intersect *ray* with every triangle after a bounding-sphere rejection test."""
    stats = IntersectStats(sphere_tests=1)
    center, radius = mesh.bounding_sphere()
    if ray_sphere_interval(ray, center, radius) is None:
        return None, stats

    best: tuple[float, int, np.ndarray] | None = None
    for face_index, face in enumerate(mesh.faces):
        stats.triangle_tests += 1
        vertices = mesh.vertices[face]
        result = ray_triangle_intersection(ray, vertices[0], vertices[1], vertices[2])
        if result is None:
            continue
        t, bary = result
        if best is None or t < best[0]:
            best = (t, face_index, bary)

    if best is None:
        return None, stats
    t, face_index, bary = best
    return _hit_from_face(mesh, ray, face_index, t, bary), stats


@dataclass
class BSPNode:
    """A binary spatial partition node using triangle-centroid splits."""

    face_indices: np.ndarray
    bounds_min: np.ndarray
    bounds_max: np.ndarray
    depth: int
    axis: int | None = None
    split: float | None = None
    left: "BSPNode | None" = None
    right: "BSPNode | None" = None

    @property
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


def build_bsp_tree(
    mesh: TriangleMesh,
    *,
    max_triangles: int = 6,
    max_depth: int = 16,
    face_indices: np.ndarray | None = None,
    depth: int = 0,
) -> BSPNode:
    """Build a simple BSP-like binary partition tree over triangle centroids."""
    if face_indices is None:
        face_indices = np.arange(mesh.triangle_count, dtype=int)
    else:
        face_indices = np.asarray(face_indices, dtype=int)

    b_min, b_max = mesh.bounds(face_indices)
    node = BSPNode(face_indices=face_indices, bounds_min=b_min, bounds_max=b_max, depth=depth)
    if len(face_indices) <= max_triangles or depth >= max_depth:
        return node

    centroids = triangle_centroids(mesh, face_indices)
    extent = centroids.max(axis=0) - centroids.min(axis=0)
    axis = int(np.argmax(extent))
    if extent[axis] <= EPSILON:
        return node

    split = float(np.median(centroids[:, axis]))
    left_mask = centroids[:, axis] <= split
    right_mask = ~left_mask
    if not left_mask.any() or not right_mask.any():
        order = np.argsort(centroids[:, axis])
        half = len(face_indices) // 2
        left_indices = face_indices[order[:half]]
        right_indices = face_indices[order[half:]]
    else:
        left_indices = face_indices[left_mask]
        right_indices = face_indices[right_mask]

    if len(left_indices) == 0 or len(right_indices) == 0:
        return node

    node.axis = axis
    node.split = split
    node.left = build_bsp_tree(
        mesh,
        max_triangles=max_triangles,
        max_depth=max_depth,
        face_indices=left_indices,
        depth=depth + 1,
    )
    node.right = build_bsp_tree(
        mesh,
        max_triangles=max_triangles,
        max_depth=max_depth,
        face_indices=right_indices,
        depth=depth + 1,
    )
    return node


def bsp_nodes(root: BSPNode) -> list[BSPNode]:
    """Return every node in preorder."""
    nodes = [root]
    if root.left is not None:
        nodes.extend(bsp_nodes(root.left))
    if root.right is not None:
        nodes.extend(bsp_nodes(root.right))
    return nodes


def bsp_leaf_count(root: BSPNode) -> int:
    """Number of leaves under *root*."""
    return sum(1 for node in bsp_nodes(root) if node.is_leaf)


def intersect_mesh_bsp(
    mesh: TriangleMesh,
    ray: Ray,
    root: BSPNode,
) -> tuple[HitRecord | None, IntersectStats]:
    """Intersect a ray with a mesh through a BSP tree traversal."""
    stats = IntersectStats(sphere_tests=1)
    center, radius = mesh.bounding_sphere()
    sphere_interval = ray_sphere_interval(ray, center, radius)
    if sphere_interval is None:
        return None, stats

    best: tuple[float, int, np.ndarray] | None = None

    def visit(node: BSPNode, best_t: float) -> float:
        nonlocal best
        stats.nodes_visited += 1
        stats.box_tests += 1
        interval = ray_aabb_interval(ray, node.bounds_min, node.bounds_max, t_max=best_t)
        if interval is None:
            return best_t
        if node.is_leaf:
            stats.leaves_visited += 1
            for face_index in node.face_indices:
                stats.triangle_tests += 1
                vertices = mesh.vertices[mesh.faces[face_index]]
                result = ray_triangle_intersection(ray, vertices[0], vertices[1], vertices[2])
                if result is None:
                    continue
                t, bary = result
                if t < best_t:
                    best_t = t
                    best = (t, int(face_index), bary)
            return best_t

        children: list[tuple[float, BSPNode]] = []
        for child in (node.left, node.right):
            if child is None:
                continue
            child_interval = ray_aabb_interval(ray, child.bounds_min, child.bounds_max, t_max=best_t)
            stats.box_tests += 1
            if child_interval is not None:
                children.append((child_interval[0], child))

        for _, child in sorted(children, key=lambda item: item[0]):
            best_t = visit(child, best_t)
        return best_t

    visit(root, ray.t_max)
    if best is None:
        return None, stats
    t, face_index, bary = best
    return _hit_from_face(mesh, ray, face_index, t, bary), stats


@dataclass
class Camera:
    """Pinhole camera with a vertical field of view."""

    origin: np.ndarray
    look_at: np.ndarray
    up: np.ndarray = field(default_factory=lambda: np.array([0.0, 1.0, 0.0]))
    fov_y_degrees: float = 45.0
    aspect: float = 4.0 / 3.0

    def __post_init__(self) -> None:
        self.origin = as_vector3(self.origin)
        self.look_at = as_vector3(self.look_at)
        self.up = normalize(self.up)
        self.fov_y_degrees = float(self.fov_y_degrees)
        self.aspect = float(self.aspect)

    def frame(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        forward = normalize(self.look_at - self.origin)
        right = normalize(np.cross(forward, self.up))
        true_up = normalize(np.cross(right, forward))
        return forward, right, true_up

    def ray(self, x_ndc: float, y_ndc: float) -> Ray:
        """Ray through normalized device coordinates in ``[-1, 1]``."""
        forward, right, true_up = self.frame()
        half_y = tan(radians(self.fov_y_degrees) * 0.5)
        half_x = self.aspect * half_y
        direction = forward + x_ndc * half_x * right + y_ndc * half_y * true_up
        return Ray(self.origin, direction)


def camera_rays(camera: Camera, width: int, height: int) -> list[Ray]:
    """Generate one center-sample camera ray per pixel."""
    rays: list[Ray] = []
    for j in range(height):
        y = 1.0 - 2.0 * ((j + 0.5) / height)
        for i in range(width):
            x = 2.0 * ((i + 0.5) / width) - 1.0
            rays.append(camera.ray(x, y))
    return rays


def intersect_scene(
    meshes: list[TriangleMesh],
    ray: Ray,
    *,
    trees: dict[str, BSPNode] | None = None,
    use_bsp: bool = True,
) -> tuple[HitRecord | None, IntersectStats]:
    """Return the closest hit across all meshes."""
    stats = IntersectStats()
    closest: HitRecord | None = None
    for mesh in meshes:
        if use_bsp and trees is not None and mesh.name in trees:
            hit, local_stats = intersect_mesh_bsp(mesh, ray, trees[mesh.name])
        else:
            hit, local_stats = intersect_mesh_naive(mesh, ray)
        stats.add(local_stats)
        if hit is not None and (closest is None or hit.t < closest.t):
            closest = hit
            ray = Ray(ray.origin, ray.direction, ray.t_min, hit.t)
    return closest, stats


def shade_hit(
    hit: HitRecord,
    ray: Ray,
    meshes: list[TriangleMesh],
    lights: list[Light],
    *,
    trees: dict[str, BSPNode] | None = None,
    use_bsp: bool = True,
    shadows: bool = True,
) -> tuple[np.ndarray, IntersectStats]:
    """Shade a hit with ambient, diffuse, specular, and optional shadow rays."""
    material = hit.material
    color = material.ambient * material.color.copy()
    stats = IntersectStats()
    view = normalize(-ray.direction)

    for light in lights:
        to_light = light.position - hit.point
        light_distance = float(np.linalg.norm(to_light))
        if light_distance <= EPSILON:
            continue
        light_dir = to_light / light_distance
        visible = True
        if shadows:
            shadow_ray = Ray(hit.point + hit.normal * 1.0e-4, light_dir, t_max=light_distance - 2.0e-4)
            shadow_hit, shadow_stats = intersect_scene(
                meshes,
                shadow_ray,
                trees=trees,
                use_bsp=use_bsp,
            )
            stats.add(shadow_stats)
            visible = shadow_hit is None
        if not visible:
            continue

        ndotl = max(0.0, float(np.dot(hit.normal, light_dir)))
        reflected_light = reflect_direction(-light_dir, hit.normal)
        spec_angle = max(0.0, float(np.dot(reflected_light, view)))
        diffuse = material.diffuse * ndotl * material.color
        specular = material.specular * (spec_angle**material.shininess) * np.ones(3)
        color += light.intensity * light.color * (diffuse + specular)

    return np.clip(color, 0.0, 1.0), stats


def trace_ray(
    ray: Ray,
    meshes: list[TriangleMesh],
    lights: list[Light],
    *,
    trees: dict[str, BSPNode] | None = None,
    use_bsp: bool = True,
    max_depth: int = 1,
    background: np.ndarray | None = None,
) -> tuple[np.ndarray, IntersectStats]:
    """Trace one ray and return color plus counters."""
    if background is None:
        background = np.array([0.74, 0.80, 0.88], dtype=float)
    hit, stats = intersect_scene(meshes, ray, trees=trees, use_bsp=use_bsp)
    if hit is None:
        t = 0.5 * (ray.direction[1] + 1.0)
        sky = (1.0 - t) * background + t * np.array([0.94, 0.97, 1.0])
        return np.clip(sky, 0.0, 1.0), stats

    local_color, shade_stats = shade_hit(
        hit,
        ray,
        meshes,
        lights,
        trees=trees,
        use_bsp=use_bsp,
        shadows=True,
    )
    stats.add(shade_stats)

    if max_depth > 0 and hit.material.reflectivity > 0.0:
        reflected = reflect_direction(ray.direction, hit.normal)
        reflected_ray = Ray(hit.point + hit.normal * 1.0e-4, reflected)
        reflected_color, reflected_stats = trace_ray(
            reflected_ray,
            meshes,
            lights,
            trees=trees,
            use_bsp=use_bsp,
            max_depth=max_depth - 1,
            background=background,
        )
        stats.add(reflected_stats)
        r = hit.material.reflectivity
        local_color = (1.0 - r) * local_color + r * reflected_color

    return np.clip(local_color, 0.0, 1.0), stats


def render_scene(
    meshes: list[TriangleMesh],
    lights: list[Light],
    camera: Camera,
    *,
    width: int = 96,
    height: int = 72,
    trees: dict[str, BSPNode] | None = None,
    use_bsp: bool = True,
    max_depth: int = 1,
) -> tuple[np.ndarray, IntersectStats]:
    """Render a small RGB image."""
    image = np.zeros((height, width, 3), dtype=float)
    totals = IntersectStats()
    camera.aspect = width / height
    for j in range(height):
        y = 1.0 - 2.0 * ((j + 0.5) / height)
        for i in range(width):
            x = 2.0 * ((i + 0.5) / width) - 1.0
            color, stats = trace_ray(
                camera.ray(x, y),
                meshes,
                lights,
                trees=trees,
                use_bsp=use_bsp,
                max_depth=max_depth,
            )
            image[j, i] = color
            totals.add(stats)
    return image, totals


def uv_sphere_mesh(
    *,
    center: Iterable[float] = (0.0, 0.0, 0.0),
    radius: float = 1.0,
    stacks: int = 10,
    slices: int = 20,
    material: Material | None = None,
    name: str = "sphere",
) -> TriangleMesh:
    """Create a faceted UV sphere mesh with radial vertex normals."""
    center_v = as_vector3(center)
    if stacks < 3 or slices < 6:
        raise ValueError("sphere needs at least 3 stacks and 6 slices")
    vertices = [center_v + np.array([0.0, radius, 0.0])]
    normals = [np.array([0.0, 1.0, 0.0])]
    for stack in range(1, stacks):
        phi = np.pi * stack / stacks
        y = np.cos(phi)
        ring = np.sin(phi)
        for slc in range(slices):
            theta = 2.0 * np.pi * slc / slices
            normal = np.array([ring * np.cos(theta), y, ring * np.sin(theta)])
            vertices.append(center_v + radius * normal)
            normals.append(normal)
    vertices.append(center_v + np.array([0.0, -radius, 0.0]))
    normals.append(np.array([0.0, -1.0, 0.0]))

    bottom = len(vertices) - 1
    faces: list[list[int]] = []
    for slc in range(slices):
        faces.append([0, 1 + (slc + 1) % slices, 1 + slc])
    for stack in range(stacks - 2):
        ring0 = 1 + stack * slices
        ring1 = ring0 + slices
        for slc in range(slices):
            a = ring0 + slc
            b = ring0 + (slc + 1) % slices
            c = ring1 + slc
            d = ring1 + (slc + 1) % slices
            faces.append([a, b, c])
            faces.append([b, d, c])
    last_ring = 1 + (stacks - 2) * slices
    for slc in range(slices):
        faces.append([last_ring + slc, last_ring + (slc + 1) % slices, bottom])

    return TriangleMesh(
        vertices=np.asarray(vertices, dtype=float),
        faces=np.asarray(faces, dtype=int),
        material=material or Material(np.array([0.8, 0.2, 0.18]), reflectivity=0.15),
        name=name,
        vertex_normals=np.asarray(normals, dtype=float),
    )


def box_mesh(
    *,
    center: Iterable[float] = (0.0, 0.0, 0.0),
    size: Iterable[float] = (1.0, 1.0, 1.0),
    material: Material | None = None,
    name: str = "box",
) -> TriangleMesh:
    """Create a box as 12 triangles."""
    c = as_vector3(center)
    sx, sy, sz = as_vector3(size) * 0.5
    vertices = np.array(
        [
            [-sx, -sy, -sz],
            [sx, -sy, -sz],
            [sx, sy, -sz],
            [-sx, sy, -sz],
            [-sx, -sy, sz],
            [sx, -sy, sz],
            [sx, sy, sz],
            [-sx, sy, sz],
        ],
        dtype=float,
    ) + c
    faces = np.array(
        [
            [0, 2, 1],
            [0, 3, 2],
            [4, 5, 6],
            [4, 6, 7],
            [0, 1, 5],
            [0, 5, 4],
            [3, 6, 2],
            [3, 7, 6],
            [1, 2, 6],
            [1, 6, 5],
            [0, 4, 7],
            [0, 7, 3],
        ],
        dtype=int,
    )
    return TriangleMesh(
        vertices=vertices,
        faces=faces,
        material=material or Material(np.array([0.18, 0.43, 0.76]), reflectivity=0.08),
        name=name,
    )


def ground_mesh(
    *,
    y: float = -1.0,
    size: float = 6.0,
    material: Material | None = None,
    name: str = "ground",
) -> TriangleMesh:
    """Create a square floor from two triangles."""
    s = float(size) * 0.5
    vertices = np.array(
        [[-s, y, -s], [s, y, -s], [s, y, s], [-s, y, s]],
        dtype=float,
    )
    faces = np.array([[0, 2, 1], [0, 3, 2]], dtype=int)
    normals = np.tile(np.array([[0.0, 1.0, 0.0]]), (4, 1))
    return TriangleMesh(
        vertices=vertices,
        faces=faces,
        material=material or Material(np.array([0.72, 0.70, 0.64]), specular=0.05),
        name=name,
        vertex_normals=normals,
    )


def demo_scene() -> tuple[list[TriangleMesh], list[Light], Camera]:
    """Return a small scene used throughout the notebook."""
    sphere = uv_sphere_mesh(
        center=(-0.72, -0.15, 0.05),
        radius=0.82,
        stacks=12,
        slices=24,
        material=Material(np.array([0.86, 0.23, 0.18]), specular=0.45, reflectivity=0.18),
        name="red sphere mesh",
    )
    box = box_mesh(
        center=(0.84, -0.42, -0.20),
        size=(0.92, 1.05, 0.92),
        material=Material(np.array([0.14, 0.38, 0.78]), specular=0.30, reflectivity=0.05),
        name="blue box mesh",
    ).transformed(matrix=rotation_matrix((0.0, 1.0, 0.0), radians(-22.0)), name="blue box mesh")
    ground = ground_mesh()
    lights = [
        Light(np.array([-2.8, 4.4, 3.0]), np.array([1.0, 0.96, 0.90]), intensity=1.05),
        Light(np.array([2.4, 2.6, -2.6]), np.array([0.62, 0.72, 1.0]), intensity=0.35),
    ]
    camera = Camera(
        origin=np.array([3.1, 1.75, 4.1]),
        look_at=np.array([0.0, -0.28, 0.0]),
        fov_y_degrees=42.0,
        aspect=4.0 / 3.0,
    )
    return [sphere, box, ground], lights, camera


def mesh_edge_segments(mesh: TriangleMesh) -> np.ndarray:
    """Return line segment endpoints for every unique mesh edge."""
    edges: set[tuple[int, int]] = set()
    for face in mesh.faces:
        for a, b in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
            edge = (int(min(a, b)), int(max(a, b)))
            edges.add(edge)
    segments = []
    for a, b in sorted(edges):
        segments.append([mesh.vertices[a], mesh.vertices[b]])
    return np.asarray(segments, dtype=float)


def representative_bsp_planes(root: BSPNode, *, max_planes: int = 12) -> list[tuple[int, float, np.ndarray, np.ndarray]]:
    """Return a small list of partition planes as ``(axis, split, b_min, b_max)``."""
    planes: list[tuple[int, float, np.ndarray, np.ndarray]] = []
    for node in bsp_nodes(root):
        if node.axis is not None and node.split is not None:
            planes.append((node.axis, node.split, node.bounds_min, node.bounds_max))
        if len(planes) >= max_planes:
            break
    return planes


def barycentric_point(vertices: np.ndarray, barycentric: Iterable[float]) -> np.ndarray:
    """Convert barycentric coordinates on one triangle to a 3-D point."""
    bary = np.asarray(barycentric, dtype=float)
    if vertices.shape != (3, 3) or bary.shape != (3,):
        raise ValueError("expected three triangle vertices and three barycentric weights")
    return bary @ vertices
