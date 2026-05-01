
"""Small helpers for coordinate differential forms."""
from __future__ import annotations
from collections.abc import Callable
from typing import Any
import numpy as np
import sympy as sp
from scipy.integrate import quad
def wedge_1forms(alpha: tuple[Any,Any], beta: tuple[Any,Any]) -> Any:
    a,b=alpha; c,d=beta; return a*d-b*c
def exterior_derivative_1form(alpha: tuple[Any,Any], x: Any, y: Any) -> Any:
    p,q=alpha; return sp.diff(q,x)-sp.diff(p,y)
def differential_of_function(f: Any, x: Any, y: Any) -> tuple[Any,Any]: return sp.diff(f,x), sp.diff(f,y)
def pullback_1form(alpha: tuple[Any,Any], F: tuple[Any,Any], u: Any, v: Any, x: Any, y: Any):
    p,q=alpha; X,Y=F; ps=p.subs({x:X,y:Y}); qs=q.subs({x:X,y:Y}); return sp.simplify(ps*sp.diff(X,u)+qs*sp.diff(Y,u)), sp.simplify(ps*sp.diff(X,v)+qs*sp.diff(Y,v))
def numeric_line_integral(p: Callable[[float,float],float], q: Callable[[float,float],float], curve: Callable[[float],tuple[float,float]], dcurve: Callable[[float],tuple[float,float]], a: float, b: float) -> float:
    return float(quad(lambda t: p(*curve(t))*dcurve(t)[0]+q(*curve(t))*dcurve(t)[1], a, b, limit=150)[0])
def winding_number(points: np.ndarray, center=(0.0,0.0)) -> float:
    pts=np.asarray(points,dtype=float)-np.asarray(center,dtype=float); angle=np.unwrap(np.arctan2(pts[:,1],pts[:,0])); return float((angle[-1]-angle[0])/(2*np.pi))
