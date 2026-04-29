"""Serial manipulator helpers built on the course SE(3) utilities."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from utils.lie import adjoint, prismatic_twist, se3_exp, twist_from_axis


@dataclass(frozen=True)
class JointTwist:
    name: str
    S: np.ndarray


def revolute(name: str, axis: np.ndarray, point: np.ndarray) -> JointTwist:
    return JointTwist(name, twist_from_axis(axis, point))


def prismatic(name: str, direction: np.ndarray) -> JointTwist:
    return JointTwist(name, prismatic_twist(direction))


@dataclass
class SerialRobot:
    joints: list[JointTwist]
    home: np.ndarray

    def fkine(self, theta: np.ndarray) -> np.ndarray:
        T = np.eye(4)
        for joint, value in zip(self.joints, np.asarray(theta, dtype=float)):
            T = T @ se3_exp(joint.S * value)
        return T @ self.home

    def spatial_jacobian(self, theta: np.ndarray) -> np.ndarray:
        theta = np.asarray(theta, dtype=float)
        J = np.zeros((6, len(self.joints)))
        T = np.eye(4)
        for i, (joint, value) in enumerate(zip(self.joints, theta)):
            J[:, i] = adjoint(T) @ joint.S
            T = T @ se3_exp(joint.S * value)
        return J

    def body_jacobian(self, theta: np.ndarray) -> np.ndarray:
        T = self.fkine(theta)
        return np.linalg.inv(adjoint(T)) @ self.spatial_jacobian(theta)


def planar_2r(lengths: tuple[float, float] = (1.0, 0.75)) -> SerialRobot:
    l1, l2 = lengths
    home = np.eye(4)
    home[:3, 3] = [l1 + l2, 0.0, 0.0]
    return SerialRobot(
        [
            revolute("shoulder", [0, 0, 1], [0, 0, 0]),
            revolute("elbow", [0, 0, 1], [l1, 0, 0]),
        ],
        home,
    )


def planar_arm_points(theta: np.ndarray, lengths: tuple[float, ...]) -> np.ndarray:
    pts = [np.array([0.0, 0.0])]
    angle = 0.0
    p = np.array([0.0, 0.0])
    for th, length in zip(theta, lengths):
        angle += float(th)
        p = p + length * np.array([np.cos(angle), np.sin(angle)])
        pts.append(p.copy())
    return np.vstack(pts)


def planar_position_jacobian(theta: np.ndarray, lengths: tuple[float, ...]) -> np.ndarray:
    """Return the 2 x n endpoint-velocity Jacobian for a planar serial arm."""
    theta = np.asarray(theta, dtype=float)
    J = np.zeros((2, len(theta)))
    cumulative = np.cumsum(theta)
    for joint_index in range(len(theta)):
        dx = 0.0
        dy = 0.0
        for link_index in range(joint_index, len(theta)):
            angle = cumulative[link_index]
            dx -= lengths[link_index] * np.sin(angle)
            dy += lengths[link_index] * np.cos(angle)
        J[:, joint_index] = [dx, dy]
    return J


def planar_workspace(lengths: tuple[float, ...], samples: int = 60) -> np.ndarray:
    grid = np.linspace(-np.pi, np.pi, samples)
    pts = []
    if len(lengths) == 2:
        for a in grid:
            for b in grid:
                pts.append(planar_arm_points([a, b], lengths)[-1])
    else:
        for a in grid:
            for b in grid:
                pts.append(planar_arm_points([a, b, -0.5 * a], lengths)[-1])
    return np.asarray(pts)


def manipulability(J: np.ndarray) -> float:
    J = np.asarray(J, dtype=float)
    gram = J @ J.T if J.shape[0] <= J.shape[1] else J.T @ J
    return float(np.sqrt(max(np.linalg.det(gram), 0.0)))
