"""Helpers for Chapter 9's bridge notebook on modeling geometries."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np

EPS = 1e-12


@dataclass(frozen=True)
class ModelProfile:
    """Compact description of a geometric model used in Part II."""

    chapter: str
    model: str
    representational_space: str
    extra_dimensions: int | None
    metric_role: str
    embedding: str
    primary_operations: tuple[str, ...]
    practical_question: str
    incidence: int
    metric: int
    motions: int
    primitive_range: int
    implementation_cost: int


MODEL_PROFILES: tuple[ModelProfile, ...] = (
    ModelProfile(
        chapter="10",
        model="Vector-space model",
        representational_space="R^n",
        extra_dimensions=0,
        metric_role="A physical metric is used directly on directions through the origin.",
        embedding="A direction, plane attitude, or volume attitude is stored as a blade.",
        primary_operations=("wedge", "contraction", "geometric product", "rotor sandwich"),
        practical_question="What can be solved when only attitude and angle matter?",
        incidence=2,
        metric=5,
        motions=3,
        primitive_range=2,
        implementation_cost=1,
    ),
    ModelProfile(
        chapter="11-12",
        model="Homogeneous model",
        representational_space="R^(n+1)",
        extra_dimensions=1,
        metric_role="The added coordinate makes offsets linear, but the inherited metric is weak.",
        embedding="A Euclidean point x becomes the projective point [x, 1].",
        primary_operations=("outer product", "duality", "meet", "linear maps"),
        practical_question="How do finite and infinite flats meet under projective operations?",
        incidence=5,
        metric=2,
        motions=3,
        primitive_range=3,
        implementation_cost=2,
    ),
    ModelProfile(
        chapter="13-16",
        model="Conformal model",
        representational_space="R^(n+1,1)",
        extra_dimensions=2,
        metric_role="A null metric encodes Euclidean distance and angle-preserving operators.",
        embedding="A point x becomes a null vector x + e0 + 0.5 |x|^2 einf.",
        primary_operations=("wedge", "inner product", "meet", "versor sandwich"),
        practical_question="How can points, flats, rounds, and Euclidean motions share one algebra?",
        incidence=5,
        metric=5,
        motions=5,
        primitive_range=5,
        implementation_cost=4,
    ),
    ModelProfile(
        chapter="17",
        model="Operational model choice",
        representational_space="Chosen per geometry",
        extra_dimensions=None,
        metric_role="The metric is part of the specification of the geometry to be operated on.",
        embedding="Objects are accepted when their operations preserve the intended invariants.",
        primary_operations=("model audit", "operator design", "invariant checks"),
        practical_question="Which representation makes the desired operations native?",
        incidence=4,
        metric=4,
        motions=4,
        primitive_range=4,
        implementation_cost=3,
    ),
)


def profile_table() -> list[dict[str, object]]:
    """Return model profiles as JSON-friendly rows."""
    return [
        {
            "chapter": profile.chapter,
            "model": profile.model,
            "representational_space": profile.representational_space,
            "extra_dimensions": profile.extra_dimensions,
            "metric_role": profile.metric_role,
            "embedding": profile.embedding,
            "primary_operations": list(profile.primary_operations),
            "practical_question": profile.practical_question,
            "scores": {
                "incidence": profile.incidence,
                "metric": profile.metric,
                "motions": profile.motions,
                "primitive_range": profile.primitive_range,
                "implementation_cost": profile.implementation_cost,
            },
        }
        for profile in MODEL_PROFILES
    ]


def score_matrix() -> tuple[list[str], list[str], np.ndarray]:
    """Return labels and a matrix for plotting model strengths."""
    criteria = ["incidence", "metric", "motions", "primitive_range", "implementation_cost"]
    labels = [profile.model for profile in MODEL_PROFILES]
    matrix = np.array(
        [
            [
                profile.incidence,
                profile.metric,
                profile.motions,
                profile.primitive_range,
                profile.implementation_cost,
            ]
            for profile in MODEL_PROFILES
        ],
        dtype=float,
    )
    return labels, criteria, matrix


def homogeneous_point_2d(x: float, y: float, w: float = 1.0) -> np.ndarray:
    """Return a homogeneous 2-D point in coordinates [x, y, w]."""
    return np.array([float(x), float(y), float(w)], dtype=float)


def normalize_homogeneous(point: Iterable[float]) -> np.ndarray:
    """Normalize a finite homogeneous point to w=1."""
    point = np.asarray(point, dtype=float)
    if abs(point[-1]) < EPS:
        raise ZeroDivisionError("point at infinity cannot be normalized in this affine chart")
    return point / point[-1]


def homogeneous_line_from_points(a: Iterable[float], b: Iterable[float]) -> np.ndarray:
    """Return the homogeneous line through two homogeneous 2-D points."""
    line = np.cross(np.asarray(a, dtype=float), np.asarray(b, dtype=float))
    length = np.linalg.norm(line[:2])
    if length < EPS:
        raise ValueError("distinct finite points are required for a stable line")
    return line / length


def intersect_homogeneous_lines(a: Iterable[float], b: Iterable[float]) -> np.ndarray:
    """Return the homogeneous meet point of two homogeneous lines."""
    return np.cross(np.asarray(a, dtype=float), np.asarray(b, dtype=float))


def line_residual(line: Iterable[float], point: Iterable[float]) -> float:
    """Evaluate the incidence equation line dot point."""
    return float(np.dot(np.asarray(line, dtype=float), np.asarray(point, dtype=float)))


def translation_matrix(dx: float, dy: float) -> np.ndarray:
    """Return a homogeneous 2-D translation matrix."""
    return np.array([[1.0, 0.0, float(dx)], [0.0, 1.0, float(dy)], [0.0, 0.0, 1.0]])


def apply_projective(matrix: np.ndarray, point: Iterable[float]) -> np.ndarray:
    """Apply a homogeneous point transform."""
    return np.asarray(matrix, dtype=float) @ np.asarray(point, dtype=float)


def transform_line(matrix: np.ndarray, line: Iterable[float]) -> np.ndarray:
    """Transform a homogeneous line by the inverse-transpose rule."""
    return np.linalg.inv(np.asarray(matrix, dtype=float)).T @ np.asarray(line, dtype=float)


def conformal_point_2d(x: float, y: float) -> np.ndarray:
    """Embed a Euclidean 2-D point as [e1, e2, e0, einf] coordinates."""
    squared = float(x) * float(x) + float(y) * float(y)
    return np.array([float(x), float(y), 1.0, 0.5 * squared], dtype=float)


def conformal_inner_2d(a: Iterable[float], b: Iterable[float]) -> float:
    """Inner product with e0.einf = -1 and e1,e2 Euclidean."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(a[0] * b[0] + a[1] * b[1] - a[2] * b[3] - a[3] * b[2])


def conformal_distance_squared_2d(a: Iterable[float], b: Iterable[float]) -> float:
    """Recover Euclidean squared distance from two conformal point embeddings."""
    return -2.0 * conformal_inner_2d(conformal_point_2d(*a), conformal_point_2d(*b))


def null_residual(point: Iterable[float]) -> float:
    """Return the conformal self-inner product of an embedded point."""
    return conformal_inner_2d(point, point)


def rotate2d(points: np.ndarray, angle: float) -> np.ndarray:
    """Rotate 2-D points by angle radians."""
    c = math.cos(angle)
    s = math.sin(angle)
    matrix = np.array([[c, -s], [s, c]])
    return np.asarray(points, dtype=float) @ matrix.T


def euclidean_distance_matrix(points: np.ndarray) -> np.ndarray:
    """Return pairwise Euclidean distances for rows of 2-D points."""
    points = np.asarray(points, dtype=float)
    deltas = points[:, None, :] - points[None, :, :]
    return np.linalg.norm(deltas, axis=-1)


def chapter_route() -> list[dict[str, str]]:
    """Return a concise Part II route map."""
    return [
        {
            "chapter": "10",
            "role": "Directional baseline",
            "question": "What survives when geometry is only about attitudes through one origin?",
        },
        {
            "chapter": "11",
            "role": "Offset flats",
            "question": "How does one extra coordinate make translated points, lines, and planes linear?",
        },
        {
            "chapter": "12",
            "role": "Projective applications",
            "question": "Where do homogeneous incidence tools pay off in cameras and line geometry?",
        },
        {
            "chapter": "13",
            "role": "Metric Euclidean operations",
            "question": "How do two added null directions make distance and rigid motion native?",
        },
        {
            "chapter": "14",
            "role": "Rounds as primitives",
            "question": "What new objects appear once spheres, circles, and point pairs are blades?",
        },
        {
            "chapter": "15",
            "role": "Conformal constructions",
            "question": "How do incidence, tangency, projection, and factorization become algorithms?",
        },
        {
            "chapter": "16",
            "role": "Conformal operators",
            "question": "How do inversion, scaling, and angle-preserving maps act as versors?",
        },
        {
            "chapter": "17",
            "role": "Model design",
            "question": "How should the representation be chosen for a new geometry or task?",
        },
    ]
