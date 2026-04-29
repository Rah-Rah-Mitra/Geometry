"""Transform, camera, and projection helpers."""

from __future__ import annotations

import numpy as np

from .graphics_math import normalize


def rotation2(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def scale2(sx: float, sy: float) -> np.ndarray:
    return np.array([[sx, 0.0], [0.0, sy]], dtype=float)


def shear2(kx: float = 0.0, ky: float = 0.0) -> np.ndarray:
    return np.array([[1.0, kx], [ky, 1.0]], dtype=float)


def translate(tx: float, ty: float, tz: float = 0.0) -> np.ndarray:
    m = np.eye(4)
    m[:3, 3] = [tx, ty, tz]
    return m


def as_point(v: np.ndarray) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    return np.append(arr[:3], 1.0)


def as_vector(v: np.ndarray) -> np.ndarray:
    arr = np.asarray(v, dtype=float)
    return np.append(arr[:3], 0.0)


def homogeneous_divide(points: np.ndarray) -> np.ndarray:
    pts = np.asarray(points, dtype=float)
    return pts[..., :-1] / pts[..., -1:]


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    eye = np.asarray(eye, dtype=float)
    w = normalize(eye - np.asarray(target, dtype=float))
    u = normalize(np.cross(np.asarray(up, dtype=float), w))
    v = np.cross(w, u)
    view = np.eye(4)
    view[:3, :3] = np.vstack([u, v, w])
    view[:3, 3] = -view[:3, :3] @ eye
    return view, {"u": u, "v": v, "w": w, "eye": eye}


def perspective(fovy_degrees: float, aspect: float, near: float, far: float) -> np.ndarray:
    f = 1.0 / np.tan(np.radians(fovy_degrees) / 2.0)
    m = np.zeros((4, 4))
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = 2.0 * far * near / (near - far)
    m[3, 2] = -1.0
    return m


def orthographic(left: float, right: float, bottom: float, top: float, near: float, far: float) -> np.ndarray:
    m = np.eye(4)
    m[0, 0] = 2.0 / (right - left)
    m[1, 1] = 2.0 / (top - bottom)
    m[2, 2] = -2.0 / (far - near)
    m[0, 3] = -(right + left) / (right - left)
    m[1, 3] = -(top + bottom) / (top - bottom)
    m[2, 3] = -(far + near) / (far - near)
    return m


def viewport(ndc_xy: np.ndarray, width: int, height: int) -> np.ndarray:
    xy = np.asarray(ndc_xy, dtype=float)
    x = (xy[..., 0] + 1.0) * 0.5 * width
    y = (1.0 - (xy[..., 1] + 1.0) * 0.5) * height
    return np.stack([x, y], axis=-1)
