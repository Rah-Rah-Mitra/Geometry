
"""Riemannian geometry helpers for two-dimensional metrics."""
from __future__ import annotations
import numpy as np
import sympy as sp
def christoffel_symbols_2d(metric: sp.Matrix, coords: tuple[sp.Symbol, sp.Symbol]):
    inv=sp.simplify(metric.inv()); gamma=[[[sp.Integer(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for k in range(2):
        for i in range(2):
            for j in range(2):
                expr=sum(inv[k,l]*(sp.diff(metric[l,j],coords[i])+sp.diff(metric[l,i],coords[j])-sp.diff(metric[i,j],coords[l])) for l in range(2))/2
                gamma[k][i][j]=sp.simplify(expr)
    return gamma
def constant_curvature_jacobi(K: float, r: np.ndarray) -> np.ndarray:
    r=np.asarray(r,dtype=float)
    if abs(K)<1e-12: return r
    root=np.sqrt(abs(K)); return np.sin(root*r)/root if K>0 else np.sinh(root*r)/root
def jacobi_residual(K: float, r: np.ndarray) -> float:
    y=constant_curvature_jacobi(K,r); ypp=np.gradient(np.gradient(y,r,edge_order=2),r,edge_order=2); return float(np.max(np.abs(ypp+K*y)[3:-3]))
def clairaut_constant(radius: np.ndarray, angle: np.ndarray) -> np.ndarray: return np.asarray(radius,dtype=float)*np.sin(angle)
def geodesic_energy(metric_values: np.ndarray, velocity: np.ndarray) -> np.ndarray: return np.einsum("...i,...ij,...j->...",velocity,metric_values,velocity)
