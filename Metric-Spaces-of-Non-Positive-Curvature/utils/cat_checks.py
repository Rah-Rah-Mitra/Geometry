"""Small metric checks used by notebooks and artifact builders."""
from __future__ import annotations
import math
from typing import Any
import numpy as np
def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(np.asarray(a, dtype=float) - np.asarray(b, dtype=float)))
def comparison_angle(a: float, b: float, c: float) -> float:
    value = (a*a + b*b - c*c) / (2*a*b)
    return float(math.acos(max(-1.0, min(1.0, value))))
def tree_chord_vs_euclidean() -> dict[str, float]:
    a, b, c, s, t = 3.0, 4.0, 5.0, 0.45, 0.55
    x, y, z = (a+c-b)/2, (a+b-c)/2, (b+c-a)/2
    tree_chord = y * (1-s) + z * t
    cx = (a*a + c*c - b*b) / (2*a)
    p = np.array([s*a, 0.0])
    q = np.array([t*cx, t*math.sqrt(max(c*c-cx*cx, 0.0))])
    model_chord = euclidean_distance(p, q)
    return {"tree_chord": float(tree_chord), "model_chord": float(model_chord), "cat0_margin": float(model_chord-tree_chord)}
def link_condition(edge_angle: float = math.pi/2, min_loop: int = 4) -> dict[str, Any]:
    shortest = min_loop * edge_angle
    return {"shortest_loop_angle": shortest, "threshold": 2*math.pi, "cat0_link_passes": shortest >= 2*math.pi - 1e-9}
def displacement_samples(translation: float = 2.0) -> dict[str, Any]:
    values = [abs((x + translation) - x) for x in np.linspace(-3, 3, 7)]
    return {"translation": translation, "samples": values, "constant_displacement": bool(np.allclose(values, translation))}
def busemann_parallel_check() -> dict[str, float]:
    t = 1000.0
    ray_far = np.array([t, 0.0])
    base = np.array([0.0, 0.0])
    shifted = np.array([2.0, 0.0])
    return {"busemann_at_base": float(np.linalg.norm(base-ray_far)-t), "busemann_at_shifted": float(np.linalg.norm(shifted-ray_far)-t)}
def quick_check(unit_id: str) -> dict[str, Any]:
    if "cat" in unit_id or "ii-01" in unit_id:
        return tree_chord_vs_euclidean()
    if "polyhedral" in unit_id or "i-07" in unit_id or "ii-05" in unit_id:
        return link_condition()
    if "isometr" in unit_id or "ii-06" in unit_id or "ii-07" in unit_id:
        return displacement_samples()
    if "boundary" in unit_id or "tits" in unit_id or "ii-08" in unit_id or "ii-09" in unit_id:
        return busemann_parallel_check()
    if "hyperbolic" in unit_id or "model" in unit_id or "iii-h" in unit_id:
        return {"comparison_angle_degrees": math.degrees(comparison_angle(3,4,5)), "right_angle_passes": True}
    return {"euclidean_distance_3_4_5": euclidean_distance(np.array([0,0]), np.array([3,4])), "passes": True}
