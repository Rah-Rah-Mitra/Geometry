"""Small optimal-transport computations for the course notebooks."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any

import numpy as np
from scipy.optimize import linprog
from scipy.spatial.distance import cdist

try:
    import ot
except Exception:  # pragma: no cover - fallback exists for validation portability
    ot = None


@dataclass(frozen=True)
class DiscreteMeasure:
    points: np.ndarray
    weights: np.ndarray


def normalize(weights: np.ndarray) -> np.ndarray:
    weights = np.asarray(weights, dtype=float)
    total = float(weights.sum())
    if total <= 0 or not isfinite(total):
        raise ValueError("weights must have positive finite total")
    return weights / total


def unit_seed(unit_id: str) -> int:
    return sum((index + 1) * ord(ch) for index, ch in enumerate(unit_id)) % 10_000


def demo_measures(unit_id: str, n: int = 5) -> tuple[DiscreteMeasure, DiscreteMeasure]:
    """Create a deterministic pair of small measures from a unit id."""
    rng = np.random.default_rng(unit_seed(unit_id))
    angles = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    radial = 0.8 + 0.18 * rng.random(n)
    source = np.column_stack([radial * np.cos(angles), radial * np.sin(angles)])
    target_angles = angles + 0.35 + 0.05 * rng.normal(size=n)
    stretch = 1.05 + 0.30 * rng.random(n)
    shift = np.array([0.35 * np.sin(unit_seed(unit_id)), 0.25 * np.cos(unit_seed(unit_id))])
    target = np.column_stack([stretch * np.cos(target_angles), 0.75 * stretch * np.sin(target_angles)]) + shift
    a = normalize(0.35 + rng.random(n))
    b = normalize(0.35 + rng.random(n))
    return DiscreteMeasure(source, a), DiscreteMeasure(target, b)


def cost_matrix(source: np.ndarray, target: np.ndarray, p: int = 2) -> np.ndarray:
    return cdist(np.asarray(source, dtype=float), np.asarray(target, dtype=float)) ** p


def exact_plan(a: np.ndarray, b: np.ndarray, cost: np.ndarray) -> np.ndarray:
    a = normalize(a)
    b = normalize(b)
    if ot is not None:
        return np.asarray(ot.emd(a, b, cost), dtype=float)
    m, n = cost.shape
    objective = cost.ravel()
    rows = []
    rhs = []
    for i in range(m):
        row = np.zeros(m * n)
        row[i * n : (i + 1) * n] = 1.0
        rows.append(row)
        rhs.append(a[i])
    for j in range(n):
        row = np.zeros(m * n)
        row[j::n] = 1.0
        rows.append(row)
        rhs.append(b[j])
    result = linprog(objective, A_eq=np.vstack(rows), b_eq=np.array(rhs), bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return result.x.reshape(m, n)


def plan_cost(plan: np.ndarray, cost: np.ndarray, p: int = 2) -> float:
    value = float(np.sum(plan * cost))
    return value ** (1.0 / p) if p != 1 else value


def plan_checks(plan: np.ndarray, source: DiscreteMeasure, target: DiscreteMeasure, p: int = 2) -> dict[str, float | bool]:
    cost = cost_matrix(source.points, target.points, p=p)
    row_error = float(np.max(np.abs(plan.sum(axis=1) - source.weights)))
    column_error = float(np.max(np.abs(plan.sum(axis=0) - target.weights)))
    total_mass = float(plan.sum())
    return {
        "row_error": row_error,
        "column_error": column_error,
        "total_mass": total_mass,
        "cost_power": float(np.sum(plan * cost)),
        "wasserstein": plan_cost(plan, cost, p=p),
        "mass_conserved": row_error < 1e-9 and column_error < 1e-9 and abs(total_mass - 1.0) < 1e-9,
    }


def barycentric_projection(plan: np.ndarray, target: DiscreteMeasure) -> np.ndarray:
    row_mass = plan.sum(axis=1)
    safe = np.where(row_mass > 1e-12, row_mass, 1.0)
    return (plan @ target.points) / safe[:, None]


def interpolated_atoms(
    plan: np.ndarray,
    source: DiscreteMeasure,
    target: DiscreteMeasure,
    t: float,
    threshold: float = 1e-10,
) -> DiscreteMeasure:
    points: list[np.ndarray] = []
    weights: list[float] = []
    for i in range(plan.shape[0]):
        for j in range(plan.shape[1]):
            weight = float(plan[i, j])
            if weight > threshold:
                points.append((1.0 - t) * source.points[i] + t * target.points[j])
                weights.append(weight)
    return DiscreteMeasure(np.vstack(points), normalize(np.array(weights)))


def histogram_entropy(values: np.ndarray, eps: float = 1e-12) -> float:
    values = normalize(np.maximum(np.asarray(values, dtype=float), eps))
    return float(np.sum(values * np.log(values + eps)))


def heat_smooth_density(x: np.ndarray, center: float, width: float) -> np.ndarray:
    density = np.exp(-0.5 * ((x - center) / width) ** 2)
    density += 0.35 * np.exp(-0.5 * ((x + 0.8 * center) / (0.65 * width + 0.05)) ** 2)
    density /= np.trapz(density, x)
    return density


def sinkhorn_demo_value() -> dict[str, Any]:
    """Run a tiny GeomLoss example if available."""
    try:
        import torch
        from geomloss import SamplesLoss
    except Exception as exc:  # pragma: no cover
        return {"available": False, "reason": repr(exc)}
    torch.manual_seed(7)
    x = torch.tensor([[-1.0], [0.0], [1.0]], dtype=torch.float32)
    y = torch.tensor([[-0.7], [0.4], [1.3]], dtype=torch.float32)
    loss = SamplesLoss("sinkhorn", p=2, blur=0.15)
    value = float(loss(x, y).detach().cpu())
    return {"available": True, "sinkhorn_loss": value, "positive": value >= 0.0}


def distortion_coefficient(k: float, n: float, theta: np.ndarray, t: float) -> np.ndarray:
    """A stable teaching version of the CD(K,N) distortion coefficient."""
    theta = np.asarray(theta, dtype=float)
    if n <= 1:
        raise ValueError("n must exceed 1")
    alpha = k / (n - 1.0)
    z = np.sqrt(abs(alpha)) * theta
    if abs(alpha) < 1e-12:
        ratio = np.full_like(theta, t)
    elif alpha > 0:
        denom = np.sin(z)
        numer = np.sin(t * z)
        ratio = np.divide(numer, denom, out=np.full_like(theta, t), where=np.abs(denom) > 1e-9)
    else:
        denom = np.sinh(z)
        numer = np.sinh(t * z)
        ratio = np.divide(numer, denom, out=np.full_like(theta, t), where=np.abs(denom) > 1e-9)
    return np.maximum(ratio, 0.0) ** (n - 1.0)

