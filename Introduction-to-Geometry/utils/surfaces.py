from __future__ import annotations
import numpy as np
def helix(t: np.ndarray, radius: float = 1.0, pitch: float = 0.15) -> np.ndarray: return np.column_stack([radius*np.cos(t), radius*np.sin(t), pitch*t])
def saddle_grid(n: int = 17):
    x=np.linspace(-1.6,1.6,n); y=np.linspace(-1.6,1.6,n); X,Y=np.meshgrid(x,y); Z=0.35*(X*X-Y*Y); return X,Y,Z
