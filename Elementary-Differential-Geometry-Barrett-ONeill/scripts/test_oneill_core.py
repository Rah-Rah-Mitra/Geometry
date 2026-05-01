
"""Smoke tests for Barrett O'Neill course helpers."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import sympy as sp
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.curves import space_curvature, torsion
from utils.forms import differential_of_function, exterior_derivative_1form, wedge_1forms
from utils.frames import orthonormality_error, rotation_about_z
from utils.riemannian import constant_curvature_jacobi, jacobi_residual
from utils.surfaces import graph_surface, partials, uv_grid

def test_helix_curvature_and_torsion() -> None:
    a=.35; t=np.linspace(0,4*np.pi,400); pts=np.column_stack([np.cos(t),np.sin(t),a*t]); k=space_curvature(pts,t)[30:-30]; tau=torsion(pts,t)[30:-30]
    assert abs(float(np.mean(k))-1/(1+a*a))<1e-3
    assert abs(float(np.mean(tau))-a/(1+a*a))<2e-3

def test_frame_and_form_identities() -> None:
    assert orthonormality_error(rotation_about_z(.3))<1e-12
    x,y=sp.symbols("x y"); f=x**2*y+sp.sin(x*y); df=differential_of_function(f,x,y)
    assert sp.simplify(exterior_derivative_1form(df,x,y))==0
    assert sp.simplify(wedge_1forms((x,y),(y,x))+wedge_1forms((y,x),(x,y)))==0

def test_surface_jacobian_and_jacobi_models() -> None:
    u,v,U,V=uv_grid((-1,1),(-1,1),40); X=graph_surface(U,V,"saddle"); Xu,Xv=partials(X,u,v)
    assert float(np.min(np.linalg.norm(np.cross(Xu,Xv),axis=-1)))>.9
    r=np.linspace(.1,2,160); assert np.allclose(constant_curvature_jacobi(0.0,r),r); assert jacobi_residual(0.0,r)<1e-10
