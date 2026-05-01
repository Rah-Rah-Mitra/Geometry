from __future__ import annotations
import math, numpy as np
def hpoint(x,y,w=1.0): return np.array([x,y,w],dtype=float)
def normalize_h(v):
    a=np.asarray(v,dtype=float); i=int(np.argmax(np.abs(a))); return a if abs(a[i])<1e-12 else a/a[i]
def join(p,q): return np.cross(np.asarray(p,dtype=float),np.asarray(q,dtype=float))
def meet(l,m): return np.cross(np.asarray(l,dtype=float),np.asarray(m,dtype=float))
def affine(p):
    p=np.asarray(p,dtype=float)
    if abs(p[2])<1e-12: raise ValueError('point at infinity')
    return p[:2]/p[2]
def incidence(p,l,tol=1e-9): return abs(float(np.dot(np.asarray(p,dtype=float),np.asarray(l,dtype=float))))<tol
def cross_ratio(a,b,c,d): return float(((a-c)*(b-d))/((a-d)*(b-c)))
def mobius_real(x,a,b,c,d):
    den=c*x+d
    return math.inf if abs(den)<1e-12 else float((a*x+b)/den)
def mobius_complex(z,a,b,c,d): return (a*z+b)/(c*z+d)
