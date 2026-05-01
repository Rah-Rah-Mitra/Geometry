from __future__ import annotations
import math
import numpy as np
def regular_polygon(n: int, radius: float = 1.0, phase: float = 0.0) -> np.ndarray:
    angles = phase + 2*np.pi*np.arange(n)/n; return np.column_stack([radius*np.cos(angles), radius*np.sin(angles)])
def polygon_area(points: np.ndarray) -> float:
    x, y = points[:,0], points[:,1]; return 0.5*float(np.dot(x, np.roll(y,-1)) - np.dot(y, np.roll(x,-1)))
def rotate(points: np.ndarray, theta: float, center=(0.0,0.0)) -> np.ndarray:
    points=np.asarray(points,float); center=np.asarray(center,float); R=np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]]); return (points-center)@R.T+center
def reflect(points: np.ndarray, angle: float = 0.0, offset: float = 0.0) -> np.ndarray:
    points=np.asarray(points,float); n=np.array([-math.sin(angle), math.cos(angle)]); signed=points@n-offset; return points-2*signed[:,None]*n
def triangle_centers(a,b,c) -> dict[str, np.ndarray]:
    a=np.asarray(a,float); b=np.asarray(b,float); c=np.asarray(c,float); return {"centroid":(a+b+c)/3, "side_midpoints":np.array([(b+c)/2,(a+c)/2,(a+b)/2])}
def invert_points(points: np.ndarray, radius: float = 1.0) -> np.ndarray:
    points=np.asarray(points,float); norm2=np.sum(points*points,axis=1); norm2=np.where(norm2<1e-12,np.nan,norm2); return radius*radius*points/norm2[:,None]
