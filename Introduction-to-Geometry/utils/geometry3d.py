from __future__ import annotations
import itertools
import numpy as np
def cube_vertices() -> np.ndarray: return np.array(list(itertools.product([-1.0,1.0], repeat=3)))
def tesseract_vertices() -> np.ndarray: return np.array(list(itertools.product([-1.0,1.0], repeat=4)))
def project_3d(points: np.ndarray) -> np.ndarray:
    M=np.array([[0.9,-0.35,0.0],[0.2,0.35,-0.8]]); return np.asarray(points,float)@M.T
def project_4d(points: np.ndarray, distance: float = 4.0) -> np.ndarray:
    p=np.asarray(points,float); return p[:,:3]*distance/(distance-p[:,3])[:,None]
