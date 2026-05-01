
"""Curve calculations used by the notebooks."""
from __future__ import annotations
import numpy as np
from scipy.interpolate import interp1d
EPS=1e-12
def as_points(points: np.ndarray) -> np.ndarray:
    arr=np.asarray(points,dtype=float)
    if arr.ndim!=2: raise ValueError("points must have shape (n, dim)")
    return arr
def derivatives(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts=as_points(points)
    return np.gradient(pts, axis=0, edge_order=2) if parameter is None else np.gradient(pts, np.asarray(parameter,dtype=float), axis=0, edge_order=2)
def speed(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray: return np.linalg.norm(derivatives(points, parameter), axis=1)
def length(points: np.ndarray) -> float: return float(np.linalg.norm(np.diff(as_points(points), axis=0), axis=1).sum())
def arclength(points: np.ndarray) -> np.ndarray:
    ds=np.linalg.norm(np.diff(as_points(points), axis=0), axis=1); return np.concatenate([[0.0], np.cumsum(ds)])
def resample_by_arclength(points: np.ndarray, samples: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    pts=as_points(points); s=arclength(pts); samples=samples or len(pts); target=np.linspace(0.0,float(s[-1]),samples)
    return np.column_stack([interp1d(s, pts[:,i], kind="linear")(target) for i in range(pts.shape[1])]), target
def unit_tangent(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    d=derivatives(points, parameter); n=np.linalg.norm(d, axis=1, keepdims=True)
    if np.any(n<=EPS): raise ValueError("unit tangent undefined where speed vanishes")
    return d/n
def plane_curvature(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts=as_points(points); d1=derivatives(pts,parameter); d2=derivatives(d1,parameter); cross=d1[:,0]*d2[:,1]-d1[:,1]*d2[:,0]
    return cross/np.maximum(np.linalg.norm(d1,axis=1)**3, EPS)
def space_curvature(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts=as_points(points); d1=derivatives(pts,parameter); d2=derivatives(d1,parameter); cross=np.cross(d1,d2)
    return np.linalg.norm(cross,axis=1)/np.maximum(np.linalg.norm(d1,axis=1)**3, EPS)
def torsion(points: np.ndarray, parameter: np.ndarray | None = None) -> np.ndarray:
    pts=as_points(points); d1=derivatives(pts,parameter); d2=derivatives(d1,parameter); d3=derivatives(d2,parameter); cross=np.cross(d1,d2)
    return np.einsum("ij,ij->i",cross,d3)/np.maximum(np.einsum("ij,ij->i",cross,cross),EPS)
def frenet_frame(points: np.ndarray, parameter: np.ndarray | None = None) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    t=unit_tangent(points,parameter); dt=derivatives(t,parameter); n=dt/np.maximum(np.linalg.norm(dt,axis=1,keepdims=True),EPS); b=np.cross(t,n); b=b/np.maximum(np.linalg.norm(b,axis=1,keepdims=True),EPS); return t,n,b
def bending_energy(points: np.ndarray, parameter: np.ndarray | None = None) -> float:
    pts=as_points(points); k=plane_curvature(pts,parameter) if pts.shape[1]==2 else space_curvature(pts,parameter); return float(0.5*np.trapezoid(k*k, arclength(pts)))
def signed_area(points: np.ndarray) -> float:
    pts=as_points(points); x,y=pts[:,0],pts[:,1]; return float(0.5*np.sum(x[:-1]*y[1:]-x[1:]*y[:-1]))
def tangent_winding(points: np.ndarray) -> float:
    t=unit_tangent(points); angle=np.unwrap(np.arctan2(t[:,1],t[:,0])); return float((angle[-1]-angle[0])/(2*np.pi))
def kabsch_align(source: np.ndarray, target: np.ndarray) -> tuple[np.ndarray,float]:
    src=as_points(source); tgt=as_points(target); sc=src.mean(axis=0); tc=tgt.mean(axis=0); src0=src-sc; tgt0=tgt-tc; u,_,vt=np.linalg.svd(src0.T@tgt0); r=u@vt
    if np.linalg.det(r)<0: u[:,-1]*=-1; r=u@vt
    aligned=src0@r+tc; return aligned, float(np.sqrt(np.mean(np.sum((aligned-tgt)**2,axis=1))))
