from __future__ import annotations
import math, numpy as np
def rotation_matrix(t):
    c,s=math.cos(t),math.sin(t); return np.array([[c,-s],[s,c]],dtype=float)
def hyperbolic_distance_half_plane(z,w): return float(math.acosh(1+abs(z-w)**2/(2*z.imag*w.imag)))
def q_from_axis_angle(axis,t):
    a=np.asarray(axis,dtype=float); a=a/np.linalg.norm(a); return np.r_[math.cos(t/2),math.sin(t/2)*a]
def q_multiply(a,b):
    w1,x1,y1,z1=np.asarray(a,dtype=float); w2,x2,y2,z2=np.asarray(b,dtype=float)
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2,w1*x2+x1*w2+y1*z2-z1*y2,w1*y2-x1*z2+y1*w2+z1*x2,w1*z2+x1*y2-y1*x2+z1*w2])
def q_conjugate(q):
    q=np.asarray(q,dtype=float); return np.array([q[0],-q[1],-q[2],-q[3]])
def q_rotate(q,v):
    q=np.asarray(q,dtype=float); q=q/np.linalg.norm(q); return q_multiply(q_multiply(q,np.r_[0.0,np.asarray(v,dtype=float)]),q_conjugate(q))[1:]
