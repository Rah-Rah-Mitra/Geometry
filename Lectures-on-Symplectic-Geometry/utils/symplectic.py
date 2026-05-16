"""Small computational checks for the symplectic geometry notebooks."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def standard_omega(n: int) -> np.ndarray:
    """Matrix for the standard form sum dx_i wedge dy_i."""

    zero = np.zeros((n, n))
    ident = np.eye(n)
    return np.block([[zero, ident], [-ident, zero]])


def is_skew(matrix: np.ndarray, *, tol: float = 1e-10) -> bool:
    return np.linalg.norm(matrix + matrix.T) <= tol


def symplectic_residual(matrix: np.ndarray, omega: np.ndarray | None = None) -> float:
    """Return ||A^T Omega A - Omega|| for a candidate symplectic matrix."""

    size = matrix.shape[0]
    omega = standard_omega(size // 2) if omega is None else omega
    return float(np.linalg.norm(matrix.T @ omega @ matrix - omega))


def rotation_symplectic(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, s], [-s, c]], dtype=float)


def lagrangian_residual(basis: np.ndarray, omega: np.ndarray | None = None) -> float:
    """Return ||B^T Omega B|| for columns spanning a candidate Lagrangian."""

    omega = standard_omega(basis.shape[0] // 2) if omega is None else omega
    return float(np.linalg.norm(basis.T @ omega @ basis))


def hamiltonian_vector_field(grad_h: np.ndarray) -> np.ndarray:
    """Hamiltonian vector field in canonical coordinates for a gradient vector."""

    n = grad_h.shape[0] // 2
    return standard_omega(n) @ grad_h


def poisson_bracket(grad_f: np.ndarray, grad_g: np.ndarray) -> float:
    n = grad_f.shape[0] // 2
    return float(grad_f.T @ standard_omega(n) @ grad_g)


def moment_circle(z: complex) -> float:
    """Moment map for the standard circle action on C with omega=dx wedge dy."""

    return 0.5 * (z.real * z.real + z.imag * z.imag)


def polygon_area(points: np.ndarray) -> float:
    x = points[:, 0]
    y = points[:, 1]
    return float(0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def delzant_vertex_determinants(normals: list[tuple[int, int]]) -> list[int]:
    """Return adjacent determinant checks for a 2D Delzant polygon."""

    values: list[int] = []
    for first, second in zip(normals, normals[1:] + normals[:1]):
        values.append(int(round(np.linalg.det(np.array([first, second], dtype=int)))))
    return values


@dataclass(frozen=True)
class Diagnostic:
    name: str
    value: float
    passed: bool
    note: str


def lecture_diagnostic(theme: str, number: int) -> Diagnostic:
    """A compact invariant check used by lecture notebooks."""

    if theme in {"linear", "contact", "complex", "kahler"}:
        theta = 0.17 * number
        residual = symplectic_residual(rotation_symplectic(theta))
        return Diagnostic("symplectic matrix residual", residual, residual < 1e-12, "A rotation preserves dx wedge dy.")

    if theme in {"cotangent", "lagrangian", "generating", "darboux"}:
        basis = np.array([[1.0], [0.0]])
        residual = lagrangian_residual(basis, standard_omega(1))
        return Diagnostic("Lagrangian line residual", residual, residual < 1e-12, "The zero section is isotropic of half dimension.")

    if theme in {"hamiltonian", "variational", "legendre", "recurrence"}:
        q = 0.2 * number
        p = 1.0 - 0.01 * number
        grad = np.array([q, p])
        xh = hamiltonian_vector_field(grad)
        energy_derivative = float(grad @ xh)
        return Diagnostic("energy derivative along X_H", energy_derivative, abs(energy_derivative) < 1e-12, "Hamiltonian flow is tangent to energy levels.")

    if theme in {"actions", "moment", "reduction", "gauge", "cohomology"}:
        z = complex(math.cos(number), math.sin(number))
        value = moment_circle(z)
        return Diagnostic("circle moment value", value, abs(value - 0.5) < 1e-12, "The unit circle orbit has constant moment value.")

    if theme in {"toric", "dh"}:
        determinants = delzant_vertex_determinants([(1, 0), (0, 1), (-1, -1)])
        value = float(max(abs(abs(det) - 1) for det in determinants))
        return Diagnostic("Delzant determinant defect", value, value < 1e-12, "Adjacent primitive normals form unimodular pairs.")

    omega = standard_omega(1)
    return Diagnostic("omega skew residual", float(np.linalg.norm(omega + omega.T)), True, "The standard form is skew.")
