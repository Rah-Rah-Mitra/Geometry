from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

COURSE_ROOT = Path(__file__).resolve().parents[1]
if str(COURSE_ROOT) not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT))

from utils.cameras import camera_center, project_points, synthetic_cameras
from utils.epipolar import eight_point, fundamental_from_cameras, sampson_errors
from utils.projective import apply_homography, dlt_homography, homogenize, line_through, incidence


def test_line_incidence_scale_invariant():
    p = np.array([0.2, -0.4, 1.0])
    q = np.array([1.3, 0.7, 1.0])
    line = line_through(p, q)
    assert abs(incidence(line, 3.0 * p)) < 1e-9
    assert abs(incidence(2.0 * line, q)) < 1e-9


def test_homography_dlt_recovers_synthetic_mapping():
    src = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [0.2, 0.4], [-0.4, 0.7]], dtype=float)
    H = np.array([[1.2, 0.2, 0.4], [-0.1, 0.9, 0.2], [0.05, -0.03, 1.0]])
    dst = apply_homography(H, src)
    Hhat = dlt_homography(src, dst)
    reproj = apply_homography(Hhat, src)
    assert np.max(np.linalg.norm(reproj - dst, axis=1)) < 1e-8


def test_camera_center_and_epipolar_residuals():
    _, P1, P2 = synthetic_cameras()
    C1 = camera_center(P1)
    assert np.linalg.norm(P1 @ C1) < 1e-7
    rng = np.random.default_rng(4)
    pts3 = rng.normal(size=(12, 3)) * [0.8, 0.5, 0.4] + [0.0, 0.0, 3.0]
    x1 = project_points(P1, pts3)
    x2 = project_points(P2, pts3)
    F = fundamental_from_cameras(P1, P2)
    errs = sampson_errors(F, x1, x2)
    assert float(np.median(errs)) < 1e-8
    Fest = eight_point(x1, x2)
    assert np.linalg.matrix_rank(Fest, tol=1e-7) == 2
