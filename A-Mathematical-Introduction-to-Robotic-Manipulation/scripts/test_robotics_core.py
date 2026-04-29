"""Smoke tests for robotics course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.dynamics import lyapunov_grid, two_link_inertia
from utils.grasping import grasp_wrenches, internal_force_basis, origin_in_convex_hull
from utils.lie import adjoint, hat_so3, instantaneous_power, se3_exp, se3_log, so3_exp
from utils.nonholonomic import bracket_loop, lie_bracket_sympy, sinusoid_controls, integrate_brockett
from utils.robots import planar_2r, planar_position_jacobian
from utils.visuals import build_storyboard, storyboard_check_payload


def test_so3_and_se3_roundtrip() -> None:
    w = np.array([0.2, -0.1, 0.3])
    R = so3_exp(w)
    assert np.allclose(R.T @ R, np.eye(3), atol=1e-10)
    assert abs(np.linalg.det(R) - 1.0) < 1e-10
    xi = np.array([0.1, -0.2, 0.15, 0.3, 0.1, -0.2])
    assert np.allclose(se3_log(se3_exp(xi)), xi, atol=1e-9)


def test_adjoint_power_invariance() -> None:
    T = se3_exp(np.array([0.1, 0.2, -0.1, 0.4, -0.2, 0.1]))
    V = np.array([0.2, -0.1, 0.4, 0.3, 0.1, -0.2])
    F = np.array([0.5, -0.2, 0.1, 0.3, -0.6, 0.2])
    Ad = adjoint(T)
    F_changed = np.linalg.inv(Ad).T @ F
    assert np.isclose(instantaneous_power(F, V), instantaneous_power(F_changed, Ad @ V))


def test_planar_robot_jacobian_shape() -> None:
    robot = planar_2r()
    theta = np.array([0.4, -0.8])
    T = robot.fkine(theta)
    J = robot.spatial_jacobian(theta)
    Jp = planar_position_jacobian(theta, (1.0, 0.75))
    assert T.shape == (4, 4)
    assert J.shape == (6, 2)
    assert Jp.shape == (2, 2)
    assert abs(np.linalg.det(Jp)) > 0.1


def test_two_link_inertia_positive_definite() -> None:
    for q2 in np.linspace(-1.0, 1.0, 5):
        eig = np.linalg.eigvalsh(two_link_inertia([0.2, q2]))
        assert eig.min() > 0


def test_grasp_closure_and_internal_basis() -> None:
    points = [np.array([-0.5, 0.0]), np.array([0.5, 0.0]), np.array([0.0, 0.5])]
    normals = [np.array([1.0, 0.2]), np.array([-1.0, 0.2]), np.array([0.0, -1.0])]
    G = grasp_wrenches(points, normals, mu=0.8)
    assert G.shape[0] == 3
    assert origin_in_convex_hull(G)
    basis = internal_force_basis(G)
    assert np.linalg.norm(G @ basis) < 1e-9


def test_lie_bracket_and_brockett_loop() -> None:
    x, y, z = sp.symbols("x y z")
    bracket = lie_bracket_sympy([1, 0, -y], [0, 1, x], [x, y, z])
    assert bracket == [0, 0, 2]
    drift = bracket_loop(0.05)
    assert abs(drift[2]) > 0
    _t, controls = sinusoid_controls(steps=64)
    path = integrate_brockett(controls, dt=2 * np.pi / 64)
    assert path.shape == (65, 3)


def test_visual_storyboard_smoke(tmp_path: Path) -> None:
    storyboard = {
        "label": "smoke",
        "artifact_topic": "chapter-00",
        "visual_sequence": [
            {"kind": "frames", "concept": "Frame Smoke", "filename": "frame-smoke.png"},
            {"kind": "screw", "concept": "Screw Smoke", "filename": "screw-smoke.png"},
            {"kind": "grasp", "concept": "Grasp Smoke", "filename": "grasp-smoke.png"},
        ],
    }
    results = build_storyboard(storyboard, tmp_path, "chapter-00")
    payload = storyboard_check_payload(storyboard, results)
    assert payload["assertions"]["has_multiple_visuals"]
    assert payload["assertions"]["all_visuals_nonblank"]
