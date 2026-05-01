from __future__ import annotations

import numpy as np

from .projective import affine


def circle_conic(cx: float, cy: float, radius: float) -> np.ndarray:
    return np.array(
        [
            [1.0, 0.0, -cx],
            [0.0, 1.0, -cy],
            [-cx, -cy, cx * cx + cy * cy - radius * radius],
        ],
        dtype=float,
    )


def ellipse_conic(rx: float = 1.5, ry: float = 0.9, cx: float = 0.0, cy: float = 0.0) -> np.ndarray:
    return np.array(
        [
            [1.0 / (rx * rx), 0.0, -cx / (rx * rx)],
            [0.0, 1.0 / (ry * ry), -cy / (ry * ry)],
            [
                -cx / (rx * rx),
                -cy / (ry * ry),
                cx * cx / (rx * rx) + cy * cy / (ry * ry) - 1.0,
            ],
        ],
        dtype=float,
    )


def evaluate_conic(conic: np.ndarray, point: np.ndarray) -> float:
    p = np.asarray(point, dtype=float)
    return float(p @ np.asarray(conic, dtype=float) @ p)


def polar_line(conic: np.ndarray, point: np.ndarray) -> np.ndarray:
    return np.asarray(conic, dtype=float) @ np.asarray(point, dtype=float)


def tangent_line(conic: np.ndarray, point: np.ndarray) -> np.ndarray:
    return polar_line(conic, point)


def dual_conic(conic: np.ndarray) -> np.ndarray:
    return np.linalg.inv(np.asarray(conic, dtype=float))


def fit_conic_through_points(points: list[np.ndarray]) -> np.ndarray:
    rows = []
    for point in points:
        x, y, z = point
        rows.append([x * x, y * y, z * z, 2 * x * y, 2 * x * z, 2 * y * z])
    _, _, vh = np.linalg.svd(np.asarray(rows, dtype=float))
    a, b, c, d, e, f = vh[-1, :]
    return np.array([[a, d, e], [d, b, f], [e, f, c]], dtype=float)


def line_conic_intersections(conic: np.ndarray, p: np.ndarray, q: np.ndarray) -> list[np.ndarray]:
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    c = np.asarray(conic, dtype=float)
    direction = q - p
    aa = float(direction @ c @ direction)
    bb = float(2 * p @ c @ direction)
    cc = float(p @ c @ p)
    roots = np.roots([aa, bb, cc])
    return [p + complex(root) * direction for root in roots]


def sampled_conic(conic: np.ndarray, limit: float = 2.2, samples: int = 220) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = np.linspace(-limit, limit, samples)
    ys = np.linspace(-limit, limit, samples)
    xx, yy = np.meshgrid(xs, ys)
    zz = (
        conic[0, 0] * xx * xx
        + conic[1, 1] * yy * yy
        + conic[2, 2]
        + 2 * conic[0, 1] * xx * yy
        + 2 * conic[0, 2] * xx
        + 2 * conic[1, 2] * yy
    )
    return xx, yy, zz


def affine_point_on_conic(theta: float, rx: float = 1.5, ry: float = 0.9) -> np.ndarray:
    return np.array([rx * np.cos(theta), ry * np.sin(theta), 1.0], dtype=float)


def affine_or_none(point: np.ndarray) -> tuple[float, float] | None:
    try:
        xy = affine(point)
    except ValueError:
        return None
    return float(xy[0]), float(xy[1])

