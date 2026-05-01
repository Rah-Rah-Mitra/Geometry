from __future__ import annotations
import math, numpy as np
def distance(a,b): return float(np.linalg.norm(np.asarray(a,dtype=float)-np.asarray(b,dtype=float)))
def rotate(v,t):
    c,s=math.cos(t),math.sin(t); return np.array([[c,-s],[s,c]])@np.asarray(v,dtype=float)
def regular_polygon(n,radius=1.0,phase=0.0,center=(0,0)):
    a=phase+np.linspace(0,2*math.pi,n,endpoint=False); c=np.asarray(center,dtype=float); return c+radius*np.column_stack([np.cos(a),np.sin(a)])
def equilateral_from_segment(a,b):
    a=np.asarray(a,dtype=float); b=np.asarray(b,dtype=float); return a+rotate(b-a,math.pi/3)
def circle_points(center,radius,n=240):
    t=np.linspace(0,2*math.pi,n); c=np.asarray(center,dtype=float); return c+radius*np.column_stack([np.cos(t),np.sin(t)])
def polygon_area(points):
    p=np.asarray(list(points),dtype=float); x,y=p[:,0],p[:,1]; return float(abs(np.dot(x,np.roll(y,-1))-np.dot(y,np.roll(x,-1)))/2)
def affine_combination(points,weights):
    p=np.asarray(list(points),dtype=float); w=np.asarray(list(weights),dtype=float); return (p*w[:,None]).sum(axis=0)/w.sum()
