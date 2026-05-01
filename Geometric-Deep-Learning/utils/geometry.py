"""Small geometry and equivariance helpers used by the GDL notebooks."""

from __future__ import annotations

import numpy as np
from scipy.sparse import coo_matrix


def permutation_matrix(order: list[int] | np.ndarray) -> np.ndarray:
    """Return a permutation matrix P such that P @ x reorders rows by order."""
    order = np.asarray(order, dtype=int)
    n = len(order)
    p = np.zeros((n, n), dtype=float)
    p[np.arange(n), order] = 1.0
    return p


def shift2d(array: np.ndarray, dy: int, dx: int) -> np.ndarray:
    """Circularly shift a 2D array."""
    return np.roll(np.roll(np.asarray(array), dy, axis=0), dx, axis=1)


def circulant_matrix(kernel: np.ndarray, n: int | None = None) -> np.ndarray:
    """Build a circular convolution matrix from a one-dimensional kernel."""
    kernel = np.asarray(kernel, dtype=float)
    if n is None:
        n = kernel.size
    padded = np.zeros(n, dtype=float)
    padded[: min(n, kernel.size)] = kernel[: min(n, kernel.size)]
    return np.array([np.roll(padded, i) for i in range(n)])


def dft_matrix(n: int) -> np.ndarray:
    """Return the unitary discrete Fourier transform matrix."""
    j, k = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    omega = np.exp(-2j * np.pi / n)
    return omega ** (j * k) / np.sqrt(n)


def graph_message_pass(adjacency: np.ndarray, features: np.ndarray, self_weight: float = 1.0) -> np.ndarray:
    """A simple permutation-equivariant graph layer with normalized neighbor sums."""
    adjacency = np.asarray(adjacency, dtype=float)
    features = np.asarray(features, dtype=float)
    degree = adjacency.sum(axis=1, keepdims=True)
    normalized = np.divide(adjacency, np.maximum(degree, 1.0), where=np.ones_like(adjacency, dtype=bool))
    return self_weight * features + normalized @ features


def pairwise_distances(points: np.ndarray) -> np.ndarray:
    """Pairwise Euclidean distances."""
    points = np.asarray(points, dtype=float)
    diff = points[:, None, :] - points[None, :, :]
    return np.linalg.norm(diff, axis=-1)


def rigid_transform(points: np.ndarray, rotation: np.ndarray, translation: np.ndarray | None = None) -> np.ndarray:
    """Apply a rigid transform to row-vector points."""
    points = np.asarray(points, dtype=float)
    rotation = np.asarray(rotation, dtype=float)
    if translation is None:
        translation = np.zeros(rotation.shape[0])
    return points @ rotation.T + np.asarray(translation, dtype=float)


def random_rotation_matrix(seed: int = 0) -> np.ndarray:
    """Generate a deterministic 3D rotation matrix."""
    rng = np.random.default_rng(seed)
    q = rng.normal(size=4)
    q = q / np.linalg.norm(q)
    w, x, y, z = q
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def sphere_expmap(base: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    """Exponential map on the unit sphere."""
    base = np.asarray(base, dtype=float)
    base = base / np.linalg.norm(base)
    tangent = np.asarray(tangent, dtype=float)
    tangent = tangent - base * np.dot(base, tangent)
    norm = np.linalg.norm(tangent)
    if norm < 1e-12:
        return base.copy()
    return np.cos(norm) * base + np.sin(norm) * tangent / norm


def parallel_transport_sphere(base: np.ndarray, target: np.ndarray, vector: np.ndarray) -> np.ndarray:
    """Parallel transport a tangent vector along the short geodesic on S2."""
    base = np.asarray(base, dtype=float)
    target = np.asarray(target, dtype=float)
    vector = np.asarray(vector, dtype=float)
    base = base / np.linalg.norm(base)
    target = target / np.linalg.norm(target)
    vector = vector - base * np.dot(base, vector)
    denom = 1.0 + float(np.dot(base, target))
    if denom < 1e-8:
        return vector - target * np.dot(target, vector)
    transported = vector - np.dot(vector, target) / denom * (base + target)
    return transported - target * np.dot(target, transported)


def cotangent_laplacian(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    """Dense cotangent Laplacian for a small triangular mesh."""
    vertices = np.asarray(vertices, dtype=float)
    faces = np.asarray(faces, dtype=int)
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    for tri in faces:
        pts = vertices[tri]
        for local in range(3):
            i = tri[(local + 1) % 3]
            j = tri[(local + 2) % 3]
            k = tri[local]
            u = pts[(local + 1) % 3] - pts[local]
            v = pts[(local + 2) % 3] - pts[local]
            cross = np.linalg.norm(np.cross(u, v))
            cot = float(np.dot(u, v) / max(cross, 1e-12))
            weight = 0.5 * cot
            rows.extend([i, j])
            cols.extend([j, i])
            vals.extend([-weight, -weight])
            rows.extend([i, j])
            cols.extend([i, j])
            vals.extend([weight, weight])
    n = len(vertices)
    return coo_matrix((vals, (rows, cols)), shape=(n, n)).toarray()


def dilated_receptive_field(kernel_size: int, dilations: list[int] | np.ndarray) -> int:
    """Receptive field width for stacked 1D dilated convolutions."""
    return 1 + (kernel_size - 1) * int(np.sum(dilations))

