"""Helpers for Chapter 17's operational-model synthesis notebook.

The module intentionally keeps the algebra small and inspectable. It supplies
coordinate representatives for the three model families compared in the chapter:
ordinary vector space, homogeneous/projective space, and a 2-D conformal model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import numpy as np

EPS = 1e-10

MODEL_CRITERIA: tuple[str, ...] = (
    "directions",
    "incidence",
    "metric_distances",
    "rigid_motions",
    "rounds",
    "projective_maps",
    "simplicity",
)

CGA_METRIC_2D = np.array(
    [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, -1.0],
        [0.0, 0.0, -1.0, 0.0],
    ],
    dtype=float,
)
CGA_INFINITY_2D = np.array([0.0, 0.0, 0.0, 1.0], dtype=float)


@dataclass(frozen=True)
class ModelProfile:
    """A compact implementation profile for a geometry model."""

    name: str
    representational_space: str
    point_embedding: str
    native_objects: tuple[str, ...]
    native_operators: tuple[str, ...]
    design_question: str
    scores: Mapping[str, int]


MODEL_PROFILES: tuple[ModelProfile, ...] = (
    ModelProfile(
        name="Vector-space model",
        representational_space="R^n with the Euclidean metric",
        point_embedding="No distinguished finite points; vectors are directions from one origin.",
        native_objects=("directions", "oriented subspaces", "rotors about the origin"),
        native_operators=("orthogonal maps", "rotor sandwiches", "linear combinations"),
        design_question="Are attitudes, angles, and rotations around a fixed origin enough?",
        scores={
            "directions": 5,
            "incidence": 2,
            "metric_distances": 3,
            "rigid_motions": 3,
            "rounds": 1,
            "projective_maps": 1,
            "simplicity": 5,
        },
    ),
    ModelProfile(
        name="Homogeneous model",
        representational_space="R^(n+1) up to nonzero scale",
        point_embedding="[x, 1] for finite points, [d, 0] for points at infinity",
        native_objects=("points", "lines", "planes", "incidence", "projective conics"),
        native_operators=("affine maps", "projective maps", "join and meet"),
        design_question="Is the core task about incidence, projection, and affine/projective maps?",
        scores={
            "directions": 3,
            "incidence": 5,
            "metric_distances": 2,
            "rigid_motions": 4,
            "rounds": 2,
            "projective_maps": 5,
            "simplicity": 4,
        },
    ),
    ModelProfile(
        name="Conformal model",
        representational_space="R^(n+1,1) with two null directions",
        point_embedding="x + no + 0.5*|x|^2*ni as a null vector",
        native_objects=("points", "flats", "spheres", "circles", "point pairs"),
        native_operators=("Euclidean motions", "inversions", "dilations", "conformal versors"),
        design_question="Do distance, rounds, and Euclidean operators need to be first-class?",
        scores={
            "directions": 4,
            "incidence": 5,
            "metric_distances": 5,
            "rigid_motions": 5,
            "rounds": 5,
            "projective_maps": 2,
            "simplicity": 2,
        },
    ),
)


def as_points2(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    """Return a row stack of 2-D points."""
    array = np.asarray(points, dtype=float)
    if array.ndim == 1:
        array = array.reshape(1, 2)
    if array.ndim != 2 or array.shape[1] != 2:
        raise ValueError("expected a 2-D point or an array of 2-D points")
    return array


def normalize(vector: Iterable[float] | np.ndarray, *, eps: float = EPS) -> np.ndarray:
    """Return a Euclidean unit vector."""
    array = np.asarray(vector, dtype=float)
    length = float(np.linalg.norm(array))
    if length <= eps:
        raise ValueError("cannot normalize a near-zero vector")
    return array / length


def rotation2(angle: float) -> np.ndarray:
    """Return a 2-by-2 rotation matrix."""
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    return np.array([[c, -s], [s, c]], dtype=float)


def rotate_vectors(vectors: Iterable[Iterable[float]] | np.ndarray, angle: float) -> np.ndarray:
    """Rotate row-vector directions in the ordinary vector-space model."""
    return as_points2(vectors) @ rotation2(angle).T


def pairwise_distances(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    """Return the pairwise Euclidean distance matrix for 2-D points."""
    points = as_points2(points)
    delta = points[:, None, :] - points[None, :, :]
    return np.linalg.norm(delta, axis=-1)


def signed_polygon_area(points: Iterable[Iterable[float]] | np.ndarray) -> float:
    """Return the signed area of a finite 2-D polygon."""
    points = as_points2(points)
    x = points[:, 0]
    y = points[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - y * np.roll(x, -1)))


def best_linear_fit(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Fit a linear map ``source @ A.T ~= target`` by least squares."""
    source = as_points2(source)
    target = as_points2(target)
    if source.shape != target.shape:
        raise ValueError("source and target must have the same shape")
    transpose, *_ = np.linalg.lstsq(source, target, rcond=None)
    matrix = transpose.T
    predicted = source @ matrix.T
    error = float(np.linalg.norm(predicted - target))
    return matrix, predicted, error


def vector_space_translation_error(points: np.ndarray, translation: Iterable[float]) -> dict[str, object]:
    """Measure how poorly a pure vector space can imitate translation as a linear map."""
    points = as_points2(points)
    translation = np.asarray(translation, dtype=float)
    target = points + translation
    matrix, predicted, error = best_linear_fit(points, target)
    return {"matrix": matrix, "predicted": predicted, "target": target, "error": error}


def hpoint2(x: float, y: float, w: float = 1.0) -> np.ndarray:
    """Return a 2-D homogeneous point in coordinates ``[x, y, w]``."""
    return np.array([float(x), float(y), float(w)], dtype=float)


def embed_homogeneous(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    """Embed finite 2-D points as homogeneous row vectors with weight one."""
    points = as_points2(points)
    return np.column_stack([points, np.ones(len(points), dtype=float)])


def normalize_hpoint(point: Iterable[float] | np.ndarray, *, eps: float = EPS) -> np.ndarray:
    """Scale a finite homogeneous point to unit weight."""
    point = np.asarray(point, dtype=float)
    if point.shape != (3,):
        raise ValueError("expected a homogeneous 2-D point")
    if abs(point[2]) <= eps:
        raise ZeroDivisionError("point at infinity cannot be normalized in this chart")
    return point / point[2]


def affine_from_homogeneous(points: Iterable[Iterable[float]] | np.ndarray) -> np.ndarray:
    """Recover finite affine coordinates from homogeneous points."""
    points = np.asarray(points, dtype=float)
    if points.ndim == 1:
        return normalize_hpoint(points)[:2]
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("expected homogeneous 2-D points")
    weights = points[:, 2]
    if np.any(np.abs(weights) <= EPS):
        raise ZeroDivisionError("cannot recover a finite affine location from zero weight")
    return points[:, :2] / weights[:, None]


def homogeneous_line(
    point_a: Iterable[float] | np.ndarray,
    point_b: Iterable[float] | np.ndarray,
    *,
    unit_normal: bool = True,
) -> np.ndarray:
    """Return the homogeneous line through two 2-D homogeneous points."""
    line = np.cross(np.asarray(point_a, dtype=float), np.asarray(point_b, dtype=float))
    if np.linalg.norm(line) <= EPS:
        raise ValueError("two distinct points are required")
    if unit_normal:
        scale = float(np.linalg.norm(line[:2]))
        if scale <= EPS:
            raise ValueError("line at infinity has no finite unit normal")
        line = line / scale
    return line


def line_residual(line: Iterable[float], point: Iterable[float]) -> float:
    """Evaluate the homogeneous incidence equation ``line dot point``."""
    return float(np.asarray(line, dtype=float) @ np.asarray(point, dtype=float))


def meet_lines(line_a: Iterable[float], line_b: Iterable[float]) -> np.ndarray:
    """Return the homogeneous point where two lines meet."""
    point = np.cross(np.asarray(line_a, dtype=float), np.asarray(line_b, dtype=float))
    if np.linalg.norm(point) <= EPS:
        raise ValueError("distinct lines are required")
    return point


def translation_homogeneous(dx: float, dy: float) -> np.ndarray:
    """Return a homogeneous translation matrix for column-vector convention."""
    return np.array([[1.0, 0.0, float(dx)], [0.0, 1.0, float(dy)], [0.0, 0.0, 1.0]], dtype=float)


def rotation_homogeneous(angle: float) -> np.ndarray:
    """Return a homogeneous rotation matrix about the origin."""
    matrix = np.eye(3, dtype=float)
    matrix[:2, :2] = rotation2(angle)
    return matrix


def apply_homogeneous(matrix: Iterable[Iterable[float]], points: np.ndarray) -> np.ndarray:
    """Apply a homogeneous matrix to one point or a row stack of points."""
    matrix = np.asarray(matrix, dtype=float)
    points = np.asarray(points, dtype=float)
    if points.ndim == 1:
        return matrix @ points
    return points @ matrix.T


def transform_line_homogeneous(matrix: Iterable[Iterable[float]], line: Iterable[float]) -> np.ndarray:
    """Transform a line by the inverse-transpose rule."""
    transformed = np.linalg.solve(np.asarray(matrix, dtype=float).T, np.asarray(line, dtype=float))
    scale = float(np.linalg.norm(transformed[:2]))
    return transformed / scale if scale > EPS else transformed


def cga_inner(a: Iterable[float], b: Iterable[float]) -> float:
    """Return the 2-D conformal inner product."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != (4,) or b.shape != (4,):
        raise ValueError("conformal vectors must have four coordinates")
    return float(a @ CGA_METRIC_2D @ b)


def cga_point2(point: Iterable[float]) -> np.ndarray:
    """Embed a finite 2-D point as a null conformal vector."""
    point = np.asarray(point, dtype=float)
    if point.shape != (2,):
        raise ValueError("expected a finite 2-D point")
    squared = float(point @ point)
    return np.array([point[0], point[1], 1.0, 0.5 * squared], dtype=float)


def cga_weight(vector: Iterable[float]) -> float:
    """Return the conformal point weight ``-X.ni``."""
    return -cga_inner(vector, CGA_INFINITY_2D)


def normalize_cga_point(vector: Iterable[float], *, eps: float = EPS) -> np.ndarray:
    """Scale a conformal point representative to unit weight."""
    vector = np.asarray(vector, dtype=float)
    weight = cga_weight(vector)
    if abs(weight) <= eps:
        raise ZeroDivisionError("cannot normalize a zero-weight point")
    return vector / weight


def recover_cga_point(vector: Iterable[float]) -> np.ndarray:
    """Recover finite 2-D coordinates from a conformal point vector."""
    vector = normalize_cga_point(vector)
    return vector[:2]


def cga_distance_squared(point_a: Iterable[float], point_b: Iterable[float]) -> float:
    """Recover Euclidean squared distance from two points or conformal point vectors."""
    a = np.asarray(point_a, dtype=float)
    b = np.asarray(point_b, dtype=float)
    a = cga_point2(a) if a.shape == (2,) else normalize_cga_point(a)
    b = cga_point2(b) if b.shape == (2,) else normalize_cga_point(b)
    return float(-2.0 * cga_inner(a, b))


def cga_rigid_matrix2(
    rotation: Iterable[Iterable[float]] | None = None,
    translation: Iterable[float] = (0.0, 0.0),
) -> np.ndarray:
    """Return the 4-by-4 conformal matrix for ``x -> R*x + t``."""
    rotation = np.eye(2, dtype=float) if rotation is None else np.asarray(rotation, dtype=float)
    translation = np.asarray(translation, dtype=float)
    if rotation.shape != (2, 2) or translation.shape != (2,):
        raise ValueError("expected a 2-by-2 rotation and a 2-D translation")
    matrix = np.zeros((4, 4), dtype=float)
    matrix[:2, :2] = rotation
    matrix[:2, 2] = translation
    matrix[2, 2] = 1.0
    matrix[3, :2] = translation @ rotation
    matrix[3, 2] = 0.5 * float(translation @ translation)
    matrix[3, 3] = 1.0
    return matrix


def apply_cga_matrix(matrix: Iterable[Iterable[float]], vectors: np.ndarray) -> np.ndarray:
    """Apply a conformal matrix to one vector or a row stack of vectors."""
    matrix = np.asarray(matrix, dtype=float)
    vectors = np.asarray(vectors, dtype=float)
    if vectors.ndim == 1:
        return matrix @ vectors
    return vectors @ matrix.T


def cga_metric_error(matrix: Iterable[Iterable[float]]) -> float:
    """Return ``||M.T G M - G||`` for the 2-D conformal metric."""
    matrix = np.asarray(matrix, dtype=float)
    return float(np.linalg.norm(matrix.T @ CGA_METRIC_2D @ matrix - CGA_METRIC_2D))


def cga_infinity_error(matrix: Iterable[Iterable[float]]) -> float:
    """Return ``||M ni - ni||``."""
    matrix = np.asarray(matrix, dtype=float)
    return float(np.linalg.norm(matrix @ CGA_INFINITY_2D - CGA_INFINITY_2D))


def cga_transform_points(points: np.ndarray, matrix: Iterable[Iterable[float]]) -> np.ndarray:
    """Apply a conformal rigid matrix and recover finite 2-D points."""
    embedded = np.array([cga_point2(point) for point in as_points2(points)])
    transformed = apply_cga_matrix(matrix, embedded)
    return np.array([recover_cga_point(point) for point in transformed])


def profile_table() -> list[dict[str, object]]:
    """Return model profiles as JSON-friendly dictionaries."""
    return [
        {
            "name": profile.name,
            "representational_space": profile.representational_space,
            "point_embedding": profile.point_embedding,
            "native_objects": list(profile.native_objects),
            "native_operators": list(profile.native_operators),
            "design_question": profile.design_question,
            "scores": dict(profile.scores),
        }
        for profile in MODEL_PROFILES
    ]


def model_score_matrix() -> tuple[list[str], list[str], np.ndarray]:
    """Return ``(model labels, criteria labels, score matrix)``."""
    labels = [profile.name for profile in MODEL_PROFILES]
    matrix = np.array(
        [[profile.scores[criterion] for criterion in MODEL_CRITERIA] for profile in MODEL_PROFILES],
        dtype=float,
    )
    return labels, list(MODEL_CRITERIA), matrix


def weighted_model_scores(weights: Mapping[str, float]) -> list[dict[str, float | str]]:
    """Score models for a workload described by nonnegative criterion weights."""
    unknown = sorted(set(weights) - set(MODEL_CRITERIA))
    if unknown:
        raise KeyError(f"unknown model criteria: {unknown}")
    weight_vector = np.array([float(weights.get(criterion, 0.0)) for criterion in MODEL_CRITERIA], dtype=float)
    total = float(weight_vector.sum())
    if total <= EPS:
        raise ValueError("at least one criterion weight must be positive")
    labels, _criteria, matrix = model_score_matrix()
    raw_scores = matrix @ weight_vector
    normalized = raw_scores / total
    rows = [
        {"model": label, "score": float(score), "raw_score": float(raw)}
        for label, score, raw in zip(labels, normalized, raw_scores, strict=True)
    ]
    return sorted(rows, key=lambda row: row["score"], reverse=True)


def sanity_checks() -> dict[str, float]:
    """Run compact invariant checks for the chapter notebook."""
    points = np.array([[0.0, 0.0], [1.2, -0.2], [0.4, 0.9], [-0.8, 0.35]], dtype=float)
    translation = np.array([0.7, -0.35], dtype=float)
    vector_fit = vector_space_translation_error(points, translation)

    homogeneous = embed_homogeneous(points)
    moved_h = apply_homogeneous(translation_homogeneous(*translation), homogeneous)
    homogeneous_translation_error = float(np.linalg.norm(affine_from_homogeneous(moved_h) - (points + translation)))

    line = homogeneous_line(homogeneous[1], homogeneous[2])
    moved_line = transform_line_homogeneous(translation_homogeneous(*translation), line)
    moved_points = apply_homogeneous(translation_homogeneous(*translation), homogeneous)
    incidence_error = max(abs(line_residual(moved_line, moved_points[1])), abs(line_residual(moved_line, moved_points[2])))

    angle = 0.4
    rotation = rotation2(angle)
    cga_matrix = cga_rigid_matrix2(rotation, translation)
    cga_points = np.array([cga_point2(point) for point in points])
    null_error = float(max(abs(cga_inner(point, point)) for point in cga_points))
    euclidean_distance = float(np.sum((points[1] - points[3]) ** 2))
    cga_distance_error = abs(cga_distance_squared(cga_points[1], cga_points[3]) - euclidean_distance)
    transformed = cga_transform_points(points, cga_matrix)
    expected = points @ rotation.T + translation
    cga_motion_error = float(np.linalg.norm(transformed - expected))

    return {
        "vector_space_translation_fit_error": float(vector_fit["error"]),
        "homogeneous_translation_error": homogeneous_translation_error,
        "homogeneous_incidence_error": float(incidence_error),
        "cga_null_error": null_error,
        "cga_distance_error": float(cga_distance_error),
        "cga_metric_error": cga_metric_error(cga_matrix),
        "cga_infinity_error": cga_infinity_error(cga_matrix),
        "cga_motion_error": cga_motion_error,
    }
