"""Compact differential forms utilities for visual differential geometry.

The module favors plain SymPy expressions and tiny data containers so it is
easy to inspect in notebooks. A k-form is stored as coefficients of ordered
basis wedges, for example ``{(0, 1): f}`` means ``f dx0 ^ dx1``.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from itertools import combinations
from typing import Any, Optional

import sympy as sp

try:  # NumPy is useful in notebooks, but the symbolic core does not require it.
    import numpy as np
except ImportError:  # pragma: no cover - only for minimal Python environments.
    np = None


Index = int | str | sp.Symbol
IndexTuple = tuple[int, ...]


def _sympify(value: Any) -> Any:
    try:
        return sp.sympify(value)
    except (sp.SympifyError, TypeError):
        return value


def _safe_subs(value: Any, substitutions: Mapping[Any, Any]) -> Any:
    if hasattr(value, "subs"):
        return value.subs(substitutions)
    return value


def _safe_simplify(value: Any) -> Any:
    try:
        return sp.simplify(value)
    except (TypeError, ValueError):
        return value


def _is_zero(value: Any) -> bool:
    try:
        return bool(value == 0)
    except TypeError:
        return False


def _permutation_sign(indices: Sequence[int]) -> tuple[int, IndexTuple]:
    items = tuple(indices)
    if len(set(items)) != len(items):
        return 0, tuple(sorted(items))

    inversions = 0
    for i, left in enumerate(items):
        for right in items[i + 1 :]:
            if left > right:
                inversions += 1
    sign = -1 if inversions % 2 else 1
    return sign, tuple(sorted(items))


def _basis_keys(dim: int, degree: int) -> list[IndexTuple]:
    if degree < 0 or degree > dim:
        return []
    return [tuple(key) for key in combinations(range(dim), degree)]


@dataclass(frozen=True, init=False)
class CoordinateSystem:
    """Named coordinate symbols used by forms and tensors."""

    name: str
    symbols: tuple[sp.Symbol, ...]

    def __init__(self, name: str, symbols: str | Sequence[str | sp.Symbol]):
        if isinstance(symbols, str):
            raw_symbols = sp.symbols(symbols)
            if isinstance(raw_symbols, sp.Symbol):
                raw_symbols = (raw_symbols,)
        else:
            raw_symbols = tuple(symbols)

        normalized = tuple(
            symbol if isinstance(symbol, sp.Symbol) else sp.Symbol(str(symbol))
            for symbol in raw_symbols
        )
        if not normalized:
            raise ValueError("CoordinateSystem needs at least one coordinate.")

        object.__setattr__(self, "name", name)
        object.__setattr__(self, "symbols", normalized)

    @property
    def dim(self) -> int:
        return len(self.symbols)

    @property
    def coframe(self) -> tuple["Form", ...]:
        return tuple(basis_form(self, i) for i in range(self.dim))

    def index(self, key: Index) -> int:
        if isinstance(key, int):
            if 0 <= key < self.dim:
                return key
            raise IndexError(f"Coordinate index {key} outside 0..{self.dim - 1}.")

        name = key.name if isinstance(key, sp.Symbol) else str(key)
        if name.startswith("d") and name[1:] in {symbol.name for symbol in self.symbols}:
            name = name[1:]

        for i, symbol in enumerate(self.symbols):
            if key == symbol or name == symbol.name:
                return i
        raise KeyError(f"{key!r} is not a coordinate of {self.name}.")

    def __iter__(self):
        return iter(self.symbols)

    def __len__(self) -> int:
        return self.dim

    def __repr__(self) -> str:
        names = ", ".join(symbol.name for symbol in self.symbols)
        return f"CoordinateSystem({self.name!r}, ({names}))"


@dataclass
class Form:
    """Differential k-form in a coordinate basis.

    Components are keyed by sorted coordinate indices. Repeated or unsorted
    keys are canonicalized with the appropriate antisymmetric sign.
    """

    coords: CoordinateSystem
    degree: int
    components: Mapping[Index | Sequence[Index], Any] | Any = field(default_factory=dict)
    name: Optional[str] = None

    def __post_init__(self) -> None:
        if self.degree < 0:
            raise ValueError("Form degree must be non-negative.")

        if self.degree == 0 and not isinstance(self.components, Mapping):
            raw_components: Mapping[Any, Any] = {(): self.components}
        elif self.components is None:
            raw_components = {}
        else:
            raw_components = self.components

        normalized: dict[IndexTuple, Any] = {}
        for raw_key, raw_value in raw_components.items():
            if self.degree == 0:
                key: IndexTuple = ()
                sign = 1
            else:
                key_items = self._normalize_key(raw_key)
                if len(key_items) != self.degree:
                    raise ValueError(
                        f"Component key {raw_key!r} has degree {len(key_items)}, "
                        f"expected {self.degree}."
                    )
                sign, key = _permutation_sign(key_items)
                if sign == 0:
                    continue

            value = _sympify(raw_value)
            if sign == -1:
                value = -value
            if _is_zero(value):
                continue

            normalized[key] = normalized.get(key, sp.S.Zero) + value

        cleaned = {
            key: value
            for key, value in sorted(normalized.items())
            if not _is_zero(value)
        }
        self.components = cleaned

    @classmethod
    def zero(cls, coords: CoordinateSystem, degree: int) -> "Form":
        return cls(coords, degree, {})

    @classmethod
    def scalar(cls, coords: CoordinateSystem, value: Any) -> "Form":
        return cls(coords, 0, {(): value})

    def _normalize_key(self, key: Index | Sequence[Index]) -> IndexTuple:
        if isinstance(key, (int, str, sp.Symbol)):
            key = (key,)
        return tuple(self.coords.index(part) for part in key)

    def coefficient(self, key: Index | Sequence[Index] = ()) -> Any:
        if self.degree == 0:
            return self.components.get((), sp.S.Zero)
        indices = self._normalize_key(key)
        sign, canonical = _permutation_sign(indices)
        if sign == 0:
            return sp.S.Zero
        return sign * self.components.get(canonical, sp.S.Zero)

    def items(self):
        return self.components.items()

    def simplify(self) -> "Form":
        return Form(
            self.coords,
            self.degree,
            {key: _safe_simplify(value) for key, value in self.components.items()},
            self.name,
        )

    def subs(self, *args: Any, **kwargs: Any) -> "Form":
        substitutions = dict(*args, **kwargs)
        return Form(
            self.coords,
            self.degree,
            {key: _safe_subs(value, substitutions) for key, value in self.components.items()},
            self.name,
        )

    def wedge(self, other: "Form") -> "Form":
        return wedge(self, other)

    def d(self) -> "Form":
        return d(self)

    def pullback(
        self,
        mapping: Mapping[Any, Any] | Sequence[Any],
        target_coords: CoordinateSystem | None = None,
    ) -> "Form":
        return pullback(self, mapping, target_coords)

    def evaluate(self, *vectors: Any, at: Mapping[Any, Any] | None = None) -> Any:
        return evaluate(self, *vectors, at=at)

    def __getitem__(self, key: Index | Sequence[Index]) -> Any:
        return self.coefficient(key)

    def __add__(self, other: Any) -> "Form":
        other = _coerce_form(other, self.coords)
        _check_compatible(self, other)
        components = dict(self.components)
        for key, value in other.components.items():
            components[key] = components.get(key, sp.S.Zero) + value
        return Form(self.coords, self.degree, components)

    def __radd__(self, other: Any) -> "Form":
        return self.__add__(other)

    def __neg__(self) -> "Form":
        return Form(
            self.coords,
            self.degree,
            {key: -value for key, value in self.components.items()},
        )

    def __sub__(self, other: Any) -> "Form":
        return self + (-_coerce_form(other, self.coords))

    def __rsub__(self, other: Any) -> "Form":
        return _coerce_form(other, self.coords) + (-self)

    def __mul__(self, scalar: Any) -> "Form":
        if isinstance(scalar, Form):
            if self.degree == 0 or scalar.degree == 0:
                return wedge(self, scalar)
            raise TypeError("Use wedge(a, b) or a ^ b for products of forms.")
        return Form(
            self.coords,
            self.degree,
            {key: value * _sympify(scalar) for key, value in self.components.items()},
        )

    def __rmul__(self, scalar: Any) -> "Form":
        return self * scalar

    def __truediv__(self, scalar: Any) -> "Form":
        return self * (sp.S.One / _sympify(scalar))

    def __xor__(self, other: "Form") -> "Form":
        return wedge(self, other)

    def __bool__(self) -> bool:
        return bool(self.components)

    def __repr__(self) -> str:
        if not self.components:
            return f"0 ({self.degree}-form on {self.coords.name})"

        terms: list[str] = []
        for key, value in self.components.items():
            basis = _basis_label(self.coords, key)
            if self.degree == 0:
                terms.append(str(value))
            elif value == 1:
                terms.append(basis)
            elif value == -1:
                terms.append(f"-{basis}")
            else:
                terms.append(f"({value}) {basis}")
        return " + ".join(terms).replace("+ -", "- ")


@dataclass
class Tensor:
    """Lightweight tensor container, mainly for metrics in this module."""

    coords: CoordinateSystem
    components: Any
    variance: str = "covariant"
    name: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.components, sp.MatrixBase):
            self.components = sp.Matrix(self.components)
        elif np is not None and isinstance(self.components, np.ndarray):
            self.components = sp.ImmutableDenseNDimArray(self.components.tolist())
        elif isinstance(self.components, (list, tuple)):
            self.components = sp.ImmutableDenseNDimArray(self.components)

    @property
    def shape(self) -> tuple[int, ...]:
        if isinstance(self.components, sp.MatrixBase):
            return self.components.shape
        return tuple(self.components.shape)

    @property
    def rank(self) -> int:
        return len(self.shape)

    def as_matrix(self) -> sp.Matrix:
        if isinstance(self.components, sp.MatrixBase):
            return sp.Matrix(self.components)
        if self.rank != 2:
            raise ValueError("Only rank-2 tensors can be converted to a matrix.")
        return sp.Matrix(self.components.tolist())

    def __getitem__(self, key: Any) -> Any:
        return self.components[key]


def _basis_label(coords: CoordinateSystem, key: IndexTuple) -> str:
    if not key:
        return "1"
    return " ^ ".join(f"d{coords.symbols[index].name}" for index in key)


def _coerce_form(value: Any, coords: CoordinateSystem) -> Form:
    if isinstance(value, Form):
        return value
    return Form.scalar(coords, value)


def _check_compatible(left: Form, right: Form) -> None:
    if left.coords != right.coords:
        raise ValueError("Forms live on different coordinate systems.")
    if left.degree != right.degree:
        raise ValueError(f"Cannot combine {left.degree}-form and {right.degree}-form.")


def basis_form(coords: CoordinateSystem, indices: Index | Sequence[Index]) -> Form:
    """Return ``dx_i`` or a basis wedge such as ``dx ^ dy``."""

    if isinstance(indices, (int, str, sp.Symbol)):
        indices = (indices,)
    normalized = tuple(coords.index(index) for index in indices)
    sign, key = _permutation_sign(normalized)
    if sign == 0:
        return Form.zero(coords, len(normalized))
    return Form(coords, len(normalized), {key: sign})


def wedge(*forms: Form) -> Form:
    """Exterior product of forms."""

    if not forms:
        raise ValueError("wedge() needs at least one form.")
    result = forms[0]
    if not isinstance(result, Form):
        raise TypeError("wedge() arguments must be Form instances.")

    for other in forms[1:]:
        if not isinstance(other, Form):
            result = result * other
            continue
        if result.coords != other.coords:
            raise ValueError("Cannot wedge forms on different coordinate systems.")

        degree = result.degree + other.degree
        components: dict[IndexTuple, Any] = {}
        for left_key, left_value in result.items():
            for right_key, right_value in other.items():
                sign, key = _permutation_sign(left_key + right_key)
                if sign == 0:
                    continue
                components[key] = components.get(key, sp.S.Zero) + sign * left_value * right_value
        result = Form(result.coords, degree, components)
    return result


def d(form: Form) -> Form:
    """Exterior derivative."""

    if form.degree > form.coords.dim:
        return Form.zero(form.coords, form.degree + 1)

    components: dict[IndexTuple, Any] = {}
    for key, value in form.items():
        for axis, symbol in enumerate(form.coords.symbols):
            derivative = sp.diff(value, symbol)
            if _is_zero(derivative):
                continue
            sign, new_key = _permutation_sign((axis,) + key)
            if sign == 0:
                continue
            components[new_key] = components.get(new_key, sp.S.Zero) + sign * derivative
    return Form(form.coords, form.degree + 1, components).simplify()


def _mapping_sequence(
    source: CoordinateSystem,
    mapping: Mapping[Any, Any] | Sequence[Any],
    target: CoordinateSystem | None,
) -> tuple[Any, ...]:
    if callable(mapping):
        if target is None:
            raise ValueError("Callable pullback maps need explicit target_coords.")
        mapping = mapping(*target.symbols)

    if isinstance(mapping, Mapping):
        values = []
        for symbol in source.symbols:
            candidates = (symbol, symbol.name, f"d{symbol.name}")
            for candidate in candidates:
                if candidate in mapping:
                    values.append(mapping[candidate])
                    break
            else:
                raise KeyError(f"Missing image for coordinate {symbol}.")
        return tuple(_sympify(value) for value in values)

    if not isinstance(mapping, Sequence) or isinstance(mapping, (str, bytes)):
        raise TypeError("Pullback map must be a mapping, sequence, or callable.")

    if len(mapping) != source.dim:
        raise ValueError(
            f"Pullback map has {len(mapping)} components, expected {source.dim}."
        )
    return tuple(_sympify(value) for value in mapping)


def _infer_target_coords(images: Sequence[Any]) -> CoordinateSystem:
    symbols: set[sp.Symbol] = set()
    for image in images:
        symbols.update(getattr(image, "free_symbols", set()))
    if not symbols:
        raise ValueError("Could not infer target_coords from a constant map.")
    ordered = tuple(sorted(symbols, key=lambda symbol: symbol.name))
    return CoordinateSystem("target", ordered)


def pullback(
    form: Form,
    mapping: Mapping[Any, Any] | Sequence[Any],
    target_coords: CoordinateSystem | None = None,
) -> Form:
    """Pull a form back along a map into ``form.coords``.

    ``mapping`` gives the source coordinates as expressions in ``target_coords``.
    For example, polar-to-Cartesian is ``[r*cos(t), r*sin(t)]`` for a form on
    Cartesian coordinates.
    """

    images = _mapping_sequence(form.coords, mapping, target_coords)
    if target_coords is None:
        target_coords = _infer_target_coords(images)

    substitutions = dict(zip(form.coords.symbols, images))
    if form.degree == 0:
        return Form.scalar(target_coords, _safe_subs(form.coefficient(), substitutions)).simplify()

    result = Form.zero(target_coords, form.degree)
    differential_images = [d(Form.scalar(target_coords, image)) for image in images]

    for key, value in form.items():
        term = Form.scalar(target_coords, _safe_subs(value, substitutions))
        for axis in key:
            term = wedge(term, differential_images[axis])
        result = result + term
    return result.simplify()


def _vector_components(coords: CoordinateSystem, vector: Any) -> list[Any]:
    if isinstance(vector, Mapping):
        values = []
        for index, symbol in enumerate(coords.symbols):
            for candidate in (index, symbol, symbol.name):
                if candidate in vector:
                    values.append(_sympify(vector[candidate]))
                    break
            else:
                raise KeyError(f"Vector is missing component {symbol}.")
        return values

    if isinstance(vector, sp.MatrixBase):
        values = list(vector)
    elif np is not None and isinstance(vector, np.ndarray):
        values = list(vector.reshape(-1))
    else:
        values = list(vector)

    if len(values) != coords.dim:
        raise ValueError(f"Vector has {len(values)} components, expected {coords.dim}.")
    return [_sympify(value) for value in values]


def evaluate(form: Form, *vectors: Any, at: Mapping[Any, Any] | None = None) -> Any:
    """Evaluate a k-form on k vectors, optionally substituting a point first."""

    if len(vectors) != form.degree:
        raise ValueError(f"A {form.degree}-form needs {form.degree} vectors.")

    substitutions = dict(at or {})
    if form.degree == 0:
        return _safe_simplify(_safe_subs(form.coefficient(), substitutions))

    vector_values = [_vector_components(form.coords, vector) for vector in vectors]
    total = sp.S.Zero
    for key, value in form.items():
        coefficient = _safe_subs(value, substitutions)
        matrix = sp.Matrix([[vector[index] for index in key] for vector in vector_values])
        total += coefficient * matrix.det()
    return _safe_simplify(total)


def _metric_matrix(coords: CoordinateSystem, metric: Tensor | Any | None) -> sp.Matrix:
    if metric is None:
        return sp.eye(coords.dim)
    if isinstance(metric, Tensor):
        matrix = metric.as_matrix()
    elif isinstance(metric, sp.MatrixBase):
        matrix = sp.Matrix(metric)
    else:
        matrix = sp.Matrix(metric)

    if matrix.shape != (coords.dim, coords.dim):
        raise ValueError(f"Metric must be a {coords.dim}x{coords.dim} matrix.")
    return matrix


def hodge_star(form: Form, metric: Tensor | Any | None = None, orientation: int = 1) -> Form:
    """Hodge star with respect to ``metric`` in the coordinate basis."""

    n = form.coords.dim
    k = form.degree
    if k > n:
        raise ValueError("Cannot take the Hodge star of forms above top degree.")
    if orientation not in (-1, 1):
        raise ValueError("orientation must be +1 or -1.")

    g = _metric_matrix(form.coords, metric)
    g_inverse = g.inv()
    volume_density = sp.sqrt(abs(g.det()))

    components: dict[IndexTuple, Any] = {}
    for test_key in _basis_keys(n, k):
        inner = sp.S.Zero
        for form_key, coefficient in form.items():
            minor = sp.Matrix([[g_inverse[row, col] for col in form_key] for row in test_key])
            inner += coefficient * (minor.det() if k else sp.S.One)

        complement = tuple(index for index in range(n) if index not in test_key)
        sign, _ = _permutation_sign(test_key + complement)
        components[complement] = components.get(complement, sp.S.Zero) + (
            orientation * sign * volume_density * inner
        )

    return Form(form.coords, n - k, components).simplify()


def _symbol(value: str | sp.Symbol) -> sp.Symbol:
    return value if isinstance(value, sp.Symbol) else sp.Symbol(str(value))


def _line_bounds(parameter: sp.Symbol, bounds: Sequence[Any]) -> tuple[Any, Any, Any]:
    if len(bounds) == 2:
        return (parameter, bounds[0], bounds[1])
    if len(bounds) == 3:
        return tuple(bounds)
    raise ValueError("Line bounds must be (a, b) or (parameter, a, b).")


def line_integral(
    form: Form,
    parameterization: Mapping[Any, Any] | Sequence[Any],
    parameter: str | sp.Symbol,
    bounds: Sequence[Any] | None = None,
) -> Any:
    """Integrate a 1-form over a parameterized curve.

    Without ``bounds`` the pulled-back integrand is returned.
    """

    if form.degree != 1:
        raise ValueError("line_integral expects a 1-form.")

    parameter = _symbol(parameter)
    line_coords = CoordinateSystem("line", (parameter,))
    pulled = pullback(form, parameterization, line_coords)
    integrand = pulled.coefficient((0,))
    integrand = _safe_simplify(integrand)
    if bounds is None:
        return integrand
    return _safe_simplify(sp.integrate(integrand, _line_bounds(parameter, bounds)))


def _surface_bounds(
    parameters: tuple[sp.Symbol, sp.Symbol],
    bounds: Sequence[Sequence[Any]],
) -> list[tuple[Any, Any, Any]]:
    if len(bounds) != 2:
        raise ValueError("Surface bounds must provide one interval for each parameter.")

    normalized = []
    for parameter, interval in zip(parameters, bounds):
        if len(interval) == 2:
            normalized.append((parameter, interval[0], interval[1]))
        elif len(interval) == 3:
            normalized.append(tuple(interval))
        else:
            raise ValueError("Each surface bound must be (a, b) or (parameter, a, b).")
    return normalized


def surface_integral(
    form: Form,
    parameterization: Mapping[Any, Any] | Sequence[Any],
    parameters: Sequence[str | sp.Symbol],
    bounds: Sequence[Sequence[Any]] | None = None,
) -> Any:
    """Integrate a 2-form over a parameterized surface.

    Without ``bounds`` the coefficient of ``du ^ dv`` is returned.
    """

    if form.degree != 2:
        raise ValueError("surface_integral expects a 2-form.")
    if len(parameters) != 2:
        raise ValueError("surface_integral needs exactly two parameters.")

    parameter_symbols = tuple(_symbol(parameter) for parameter in parameters)
    surface_coords = CoordinateSystem("surface", parameter_symbols)
    pulled = pullback(form, parameterization, surface_coords)
    integrand = _safe_simplify(pulled.coefficient((0, 1)))
    if bounds is None:
        return integrand
    return _safe_simplify(sp.integrate(integrand, *_surface_bounds(parameter_symbols, bounds)))


def connection_forms(
    coords: CoordinateSystem,
    metric: Tensor | Any,
    simplify: bool = True,
) -> list[list[Form]]:
    """Levi-Civita connection 1-forms in the coordinate frame.

    The returned matrix has entries ``omega[i][j] = Gamma^i_{j k} dx^k``.
    """

    n = coords.dim
    symbols = coords.symbols
    g = _metric_matrix(coords, metric)
    g_inverse = g.inv()

    omega: list[list[Form]] = []
    for i in range(n):
        row: list[Form] = []
        for j in range(n):
            components: dict[IndexTuple, Any] = {}
            for k in range(n):
                christoffel = sp.S.Zero
                for ell in range(n):
                    christoffel += g_inverse[i, ell] * (
                        sp.diff(g[k, ell], symbols[j])
                        + sp.diff(g[j, ell], symbols[k])
                        - sp.diff(g[j, k], symbols[ell])
                    )
                christoffel = christoffel / 2
                if simplify:
                    christoffel = _safe_simplify(christoffel)
                if not _is_zero(christoffel):
                    components[(k,)] = christoffel
            row.append(Form(coords, 1, components))
        omega.append(row)
    return omega


def _connection_coords(connection: Sequence[Sequence[Form]]) -> CoordinateSystem:
    for row in connection:
        for entry in row:
            if isinstance(entry, Form):
                return entry.coords
    raise ValueError("Connection matrix does not contain any Form entries.")


def curvature_forms(
    connection_or_coords: Sequence[Sequence[Form]] | CoordinateSystem,
    metric: Tensor | Any | None = None,
    simplify: bool = True,
) -> list[list[Form]]:
    """Curvature 2-forms ``Omega^i_j = d omega^i_j + omega^i_k ^ omega^k_j``."""

    if isinstance(connection_or_coords, CoordinateSystem):
        if metric is None:
            raise ValueError("curvature_forms(coords, metric) needs a metric.")
        connection = connection_forms(connection_or_coords, metric, simplify=simplify)
    else:
        connection = connection_or_coords

    coords = _connection_coords(connection)
    n = len(connection)
    curvature: list[list[Form]] = []
    for i in range(n):
        row: list[Form] = []
        for j in range(n):
            entry = d(connection[i][j])
            for k in range(n):
                entry = entry + wedge(connection[i][k], connection[k][j])
            row.append(entry.simplify() if simplify else entry)
        curvature.append(row)
    return curvature

