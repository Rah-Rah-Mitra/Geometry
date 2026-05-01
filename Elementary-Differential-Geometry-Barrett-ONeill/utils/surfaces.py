
"""Surface sampling, metrics, and curvature helpers."""
from __future__ import annotations
import numpy as np
EPS=1e-12
def uv_grid(u_range=(-1.0,1.0), v_range=(-1.0,1.0), n: int=80):
    u=np.linspace(u_range[0],u_range[1],n); v=np.linspace(v_range[0],v_range[1],n); U,V=np.meshgrid(u,v); return u,v,U,V
def graph_surface(U: np.ndarray, V: np.ndarray, kind: str="saddle") -> np.ndarray:
    Z=0.35*np.exp(-(U*U+V*V)) if kind=="bump" else (np.sqrt(np.maximum(1.0-0.2*U*U-0.2*V*V,0.0)) if kind=="sphere-cap" else 0.25*(U*U-V*V))
    return np.stack([U,V,Z],axis=-1)
def sphere(U: np.ndarray, V: np.ndarray, radius: float=1.0) -> np.ndarray:
    return np.stack([radius*np.cos(U)*np.cos(V), radius*np.sin(U)*np.cos(V), radius*np.sin(V)], axis=-1)
def cylinder(U: np.ndarray, V: np.ndarray, radius: float=1.0) -> np.ndarray:
    return np.stack([radius*np.cos(U), radius*np.sin(U), V], axis=-1)
def torus(U: np.ndarray, V: np.ndarray, major: float=2.0, minor: float=0.65) -> np.ndarray:
    return np.stack([(major+minor*np.cos(V))*np.cos(U), (major+minor*np.cos(V))*np.sin(U), minor*np.sin(V)], axis=-1)
def helicoid(U: np.ndarray, V: np.ndarray, pitch: float=0.35) -> np.ndarray:
    return np.stack([U*np.cos(V), U*np.sin(V), pitch*V], axis=-1)
def catenoid(U: np.ndarray, V: np.ndarray, a: float=0.75) -> np.ndarray:
    return np.stack([a*np.cosh(U/a)*np.cos(V), a*np.cosh(U/a)*np.sin(V), U], axis=-1)
def partials(X: np.ndarray, u: np.ndarray, v: np.ndarray):
    return np.gradient(X,u,axis=1,edge_order=2), np.gradient(X,v,axis=0,edge_order=2)
def normals(Xu: np.ndarray, Xv: np.ndarray) -> np.ndarray:
    N=np.cross(Xu,Xv); return N/np.maximum(np.linalg.norm(N,axis=-1,keepdims=True),EPS)
def first_fundamental_form(Xu: np.ndarray, Xv: np.ndarray):
    return np.einsum("...i,...i->...",Xu,Xu), np.einsum("...i,...i->...",Xu,Xv), np.einsum("...i,...i->...",Xv,Xv)
def area_density(E: np.ndarray, F: np.ndarray, G: np.ndarray) -> np.ndarray: return np.sqrt(np.maximum(E*G-F*F,0.0))
def second_fundamental_form(X: np.ndarray, u: np.ndarray, v: np.ndarray):
    Xu,Xv=partials(X,u,v); N=normals(Xu,Xv); Xuu=np.gradient(Xu,u,axis=1,edge_order=2); Xuv=np.gradient(Xu,v,axis=0,edge_order=2); Xvv=np.gradient(Xv,v,axis=0,edge_order=2)
    return np.einsum("...i,...i->...",Xuu,N), np.einsum("...i,...i->...",Xuv,N), np.einsum("...i,...i->...",Xvv,N)
def gaussian_mean_curvature(X: np.ndarray, u: np.ndarray, v: np.ndarray):
    Xu,Xv=partials(X,u,v); E,F,G=first_fundamental_form(Xu,Xv); L,M,Nc=second_fundamental_form(X,u,v); denom=np.maximum(E*G-F*F,EPS)
    return (L*Nc-M*M)/denom, (E*Nc-2*F*M+G*L)/(2*denom)
def graph_curvature(Z: np.ndarray, du: float, dv: float):
    zx=np.gradient(Z,du,axis=1,edge_order=2); zy=np.gradient(Z,dv,axis=0,edge_order=2); zxx=np.gradient(zx,du,axis=1,edge_order=2); zyy=np.gradient(zy,dv,axis=0,edge_order=2); zxy=np.gradient(zx,dv,axis=0,edge_order=2); q=1+zx*zx+zy*zy
    H=((1+zy*zy)*zxx-2*zx*zy*zxy+(1+zx*zx)*zyy)/(2*q**1.5); K=(zxx*zyy-zxy*zxy)/(q*q); return H,K
def principal_curvatures(H: np.ndarray, K: np.ndarray):
    root=np.sqrt(np.maximum(H*H-K,0.0)); return H-root,H+root
def integrate_density(density: np.ndarray, u: np.ndarray, v: np.ndarray) -> float:
    return float(np.trapezoid(np.trapezoid(density,u,axis=1),v))
