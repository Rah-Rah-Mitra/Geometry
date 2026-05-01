
"""Frame and orientation helpers."""
from __future__ import annotations
import numpy as np
EPS=1e-12
def normalize(v: np.ndarray) -> np.ndarray:
    arr=np.asarray(v,dtype=float); return arr/np.maximum(np.linalg.norm(arr,axis=-1,keepdims=True),EPS)
def attitude_matrix(frame: np.ndarray) -> np.ndarray:
    mat=np.asarray(frame,dtype=float)
    if mat.shape!=(3,3): raise ValueError("frame must be a 3 by 3 array whose rows are frame vectors")
    return mat
def orthonormality_error(frame: np.ndarray) -> float:
    mat=attitude_matrix(frame); return float(np.linalg.norm(mat@mat.T-np.eye(3)))
def orientation_sign(frame: np.ndarray) -> float: return float(np.linalg.det(attitude_matrix(frame)))
def triple_scalar_product(a: np.ndarray,b: np.ndarray,c: np.ndarray) -> float: return float(np.dot(a,np.cross(b,c)))
def rotation_about_z(theta: float) -> np.ndarray:
    c,s=np.cos(theta),np.sin(theta); return np.array([[c,-s,0.0],[s,c,0.0],[0.0,0.0,1.0]])
def reflection_x() -> np.ndarray: return np.diag([-1.0,1.0,1.0])
def skew_error(matrix: np.ndarray) -> float:
    mat=np.asarray(matrix,dtype=float); return float(np.linalg.norm(mat+mat.T))
def connection_from_frame_derivative(frame: np.ndarray, derivative: np.ndarray) -> np.ndarray:
    e=attitude_matrix(frame); de=np.asarray(derivative,dtype=float)
    if de.shape!=(3,3): raise ValueError("derivative must be a 3 by 3 array")
    return de@e.T
