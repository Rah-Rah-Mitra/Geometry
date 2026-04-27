"""Small symbolic and numeric Riemannian-geometry utilities."""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
import sympy as sp

EPS = 1e-12


def _as_matrix(values: sp.Matrix | Sequence[Sequence[sp.Expr]]) -> sp.Matrix:
    return values if isinstance(values, sp.MatrixBase) else sp.Matrix(values)


def _simplify_array(values: sp.MutableDenseNDimArray) -> sp.ImmutableDenseNDimArray:
    for index in np.ndindex(*values.shape):
        values[index] = sp.simplify(values[index])
    return sp.ImmutableDenseNDimArray(values)


def metric_tensor(
    embedding: sp.Matrix | Sequence[sp.Expr],
    coords: Sequence[sp.Symbol],
    ambient_metric: sp.Matrix | Sequence[Sequence[sp.Expr]] | None = None,
) -> sp.Matrix:
    """Return the pullback metric ``J.T * ambient_metric * J`` for an embedding."""

    coords = tuple(coords)
    embedding = sp.Matrix(embedding)
    jacobian = embedding.jacobian(coords)
    if ambient_metric is None:
        ambient = sp.eye(embedding.rows)
    else:
        ambient = _as_matrix(ambient_metric)
    return sp.simplify(jacobian.T * ambient * jacobian)


def christoffel_symbols(
    metric: sp.Matrix | Sequence[Sequence[sp.Expr]],
    coords: Sequence[sp.Symbol],
) -> sp.ImmutableDenseNDimArray:
    """Return Levi-Civita symbols ``Gamma[i, j, k] = Gamma^i_{jk}``."""

    metric = _as_matrix(metric)
    coords = tuple(coords)
    dimension = len(coords)
    if metric.shape != (dimension, dimension):
        raise ValueError("metric shape must match the coordinate dimension")

    inverse_metric = sp.simplify(metric.inv())
    gamma = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension)
    for upper in range(dimension):
        for lower_a in range(dimension):
            for lower_b in range(dimension):
                total = 0
                for contracted in range(dimension):
                    total += inverse_metric[upper, contracted] * (
                        sp.diff(metric[contracted, lower_b], coords[lower_a])
                        + sp.diff(metric[contracted, lower_a], coords[lower_b])
                        - sp.diff(metric[lower_a, lower_b], coords[contracted])
                    )
                gamma[upper, lower_a, lower_b] = sp.Rational(1, 2) * total
    return _simplify_array(gamma)


def riemann_tensor(
    metric: sp.Matrix | Sequence[Sequence[sp.Expr]],
    coords: Sequence[sp.Symbol],
    gamma: sp.ImmutableDenseNDimArray | None = None,
) -> sp.ImmutableDenseNDimArray:
    """Return ``R[upper, lower, direction_a, direction_b] = R^i_{jkl}``."""

    coords = tuple(coords)
    dimension = len(coords)
    if gamma is None:
        gamma = christoffel_symbols(metric, coords)
    riemann = sp.MutableDenseNDimArray.zeros(dimension, dimension, dimension, dimension)
    for upper in range(dimension):
        for lower in range(dimension):
            for direction_a in range(dimension):
                for direction_b in range(dimension):
                    total = sp.diff(gamma[upper, direction_b, lower], coords[direction_a])
                    total -= sp.diff(gamma[upper, direction_a, lower], coords[direction_b])
                    for contracted in range(dimension):
                        total += (
                            gamma[upper, direction_a, contracted]
                            * gamma[contracted, direction_b, lower]
                        )
                        total -= (
                            gamma[upper, direction_b, contracted]
                            * gamma[contracted, direction_a, lower]
                        )
                    riemann[upper, lower, direction_a, direction_b] = total
    return _simplify_array(riemann)


def ricci_tensor(
    metric: sp.Matrix | Sequence[Sequence[sp.Expr]],
    coords: Sequence[sp.Symbol],
    gamma: sp.ImmutableDenseNDimArray | None = None,
) -> sp.Matrix:
    """Return the Ricci tensor ``Ric[j, l] = R^i_{jil}``."""

    coords = tuple(coords)
    dimension = len(coords)
    riemann = riemann_tensor(metric, coords, gamma)
    ricci = sp.zeros(dimension, dimension)
    for lower in range(dimension):
        for direction_b in range(dimension):
            ricci[lower, direction_b] = sp.simplify(
                sum(riemann[upper, lower, upper, direction_b] for upper in range(dimension))
            )
    return ricci


def gaussian_curvature_2d(
    metric: sp.Matrix | Sequence[Sequence[sp.Expr]],
    coords: Sequence[sp.Symbol],
    gamma: sp.ImmutableDenseNDimArray | None = None,
) -> sp.Expr:
    """Return Gaussian curvature for a two-dimensional metric."""

    metric = _as_matrix(metric)
    coords = tuple(coords)
    if metric.shape != (2, 2) or len(coords) != 2:
        raise ValueError("gaussian_curvature_2d expects a 2x2 metric and two coordinates")
    riemann = riemann_tensor(metric, coords, gamma)
    lowered = sum(metric[0, contracted] * riemann[contracted, 1, 0, 1] for contracted in range(2))
    return sp.simplify(lowered / metric.det())


def shape_operator(
    embedding: sp.Matrix | Sequence[sp.Expr],
    coords: Sequence[sp.Symbol],
    normal: sp.Matrix | Sequence[sp.Expr] | None = None,
    *,
    return_data: bool = False,
) -> sp.Matrix | tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]:
    """Return the Weingarten map ``S = I^{-1} II`` for a surface in ``R^3``."""

    coords = tuple(coords)
    if len(coords) != 2:
        raise ValueError("shape_operator expects two surface coordinates")
    embedding = sp.Matrix(embedding)
    if embedding.shape != (3, 1):
        raise ValueError("shape_operator expects a 3D column-vector embedding")

    derivatives = [embedding.diff(coord) for coord in coords]
    first_form = sp.Matrix([[sp.simplify(a.dot(b)) for b in derivatives] for a in derivatives])

    if normal is None:
        normal_vector = derivatives[0].cross(derivatives[1])
    else:
        normal_vector = sp.Matrix(normal)
    normal_length = sp.sqrt(sp.simplify(normal_vector.dot(normal_vector)))
    unit_normal = sp.simplify(normal_vector / normal_length)

    second_form = sp.Matrix(
        [
            [sp.simplify(unit_normal.dot(embedding.diff(coords[i], coords[j]))) for j in range(2)]
            for i in range(2)
        ]
    )
    operator = sp.simplify(first_form.inv() * second_form)
    if return_data:
        return operator, first_form, second_form, unit_normal
    return operator


def _connection_at(
    gamma: Callable[[np.ndarray], np.ndarray] | np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    values = gamma(position) if callable(gamma) else gamma
    values = np.asarray(values, dtype=float)
    if values.ndim != 3 or values.shape[0] != values.shape[1] or values.shape[1] != values.shape[2]:
        raise ValueError("connection must have shape (n, n, n)")
    if values.shape[0] != position.size:
        raise ValueError("connection dimension must match position dimension")
    return values


def geodesic_rhs(
    state: np.ndarray,
    gamma: Callable[[np.ndarray], np.ndarray] | np.ndarray,
) -> np.ndarray:
    """First-order geodesic ODE for state ``[q0..qn, v0..vn]``."""

    state = np.asarray(state, dtype=float)
    if state.ndim != 1 or state.size % 2:
        raise ValueError("geodesic state must be a flat vector of length 2n")
    dimension = state.size // 2
    position = state[:dimension]
    velocity = state[dimension:]
    connection = _connection_at(gamma, position)
    acceleration = -np.einsum("ijk,j,k->i", connection, velocity, velocity)
    return np.concatenate([velocity, acceleration])


def parallel_transport_rhs(
    position: np.ndarray,
    tangent: np.ndarray,
    vector: np.ndarray,
    gamma: Callable[[np.ndarray], np.ndarray] | np.ndarray,
) -> np.ndarray:
    """Derivative of a vector field parallel transported along a parameterized path."""

    position = np.asarray(position, dtype=float)
    tangent = np.asarray(tangent, dtype=float)
    vector = np.asarray(vector, dtype=float)
    if position.ndim != 1 or tangent.shape != position.shape or vector.shape != position.shape:
        raise ValueError("position, tangent, and vector must be flat arrays with the same shape")
    connection = _connection_at(gamma, position)
    return -np.einsum("ijk,j,k->i", connection, tangent, vector)
