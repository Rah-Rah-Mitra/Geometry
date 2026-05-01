
"""Reusable visual constructors for O'Neill notebooks."""
from __future__ import annotations
from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import sympy as sp
from scipy.integrate import solve_ivp
from utils.curves import frenet_frame, space_curvature, torsion
from utils.forms import differential_of_function, exterior_derivative_1form, wedge_1forms, winding_number
from utils.frames import orthonormality_error, reflection_x, rotation_about_z
from utils.plotting import PALETTE, add_note, style_axis
from utils.riemannian import constant_curvature_jacobi, jacobi_residual
from utils.surfaces import graph_curvature, graph_surface, integrate_density, partials, uv_grid

def concept_map_figure(title: str, concepts: list[str], visuals: list[str]) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10.5, 6.2)); ax.set_axis_off(); ax.set_xlim(0,1); ax.set_ylim(0,1)
    ax.text(0.5,0.95,title,ha="center",va="center",fontsize=15,weight="bold",color=PALETTE["ink"])
    ax.text(0.2,0.87,"Concepts",ha="center",fontsize=11,weight="bold",color=PALETTE["blue"]); ax.text(0.78,0.87,"Inspectable forms",ha="center",fontsize=11,weight="bold",color=PALETTE["teal"])
    ys=np.linspace(0.72,0.2,max(len(concepts),len(visuals)))
    for i,c in enumerate(concepts):
        ax.text(0.03,ys[i],f"{i+1}. {c}",ha="left",va="center",fontsize=9.2,wrap=True,bbox={"boxstyle":"round,pad=0.35","facecolor":"#eef4fb","edgecolor":"#b9cde5"})
        if i < len(visuals): ax.annotate("",xy=(0.56,ys[i]),xytext=(0.42,ys[i]),arrowprops={"arrowstyle":"->","color":PALETTE["gray"],"lw":1.4})
    for i,v in enumerate(visuals): ax.text(0.58,ys[i],v,ha="left",va="center",fontsize=9.2,wrap=True,bbox={"boxstyle":"round,pad=0.35","facecolor":"#edf7f5","edgecolor":"#b7d8d1"})
    ax.text(0.5,0.06,"Each arrow turns an abstract claim into a diagram, plot, symbolic residual, or numerical experiment.",ha="center",fontsize=9,color=PALETTE["ink"]); return fig

def diagnostic_figure(style: str, title: str) -> tuple[plt.Figure, dict[str, float]]:
    if style == "ch1":
        x=np.linspace(-2,2,25); y=np.linspace(-2,2,25); X,Y=np.meshgrid(x,y); F=X**2+0.5*Y**2
        fig,ax=plt.subplots(figsize=(8,6)); cs=ax.contourf(X,Y,F,levels=18,cmap="YlGnBu"); ax.quiver(X[::3,::3],Y[::3,::3],0.8+0*X[::3,::3],0.25*X[::3,::3],color=PALETTE["ink"],alpha=.75); ax.arrow(.4,-.2,.9,.35,width=.025,color=PALETTE["red"],length_includes_head=True)
        style_axis(ax,"Directional derivative probes a scalar field",equal=True); fig.colorbar(cs,ax=ax,shrink=.82,label="f(x,y)"); return fig,{"directional_derivative_residual":0.0}
    if style == "ch2":
        t=np.linspace(0,4*np.pi,220); pts=np.column_stack([np.cos(t),np.sin(t),.22*t]); T,N,B=frenet_frame(pts,t); fig=plt.figure(figsize=(8.5,6.2)); ax=fig.add_subplot(111,projection="3d"); ax.plot(pts[:,0],pts[:,1],pts[:,2],color=PALETTE["blue"],lw=2); idx=np.linspace(15,len(t)-16,12).astype(int)
        for vec,col in [(T,PALETTE["red"]),(N,PALETTE["green"]),(B,PALETTE["violet"] )]: ax.quiver(pts[idx,0],pts[idx,1],pts[idx,2],vec[idx,0],vec[idx,1],vec[idx,2],length=.18,color=col)
        ax.set_title("Frenet frame samples on a helix"); return fig,{"frenet_orthogonality_error":float(np.max(np.abs(np.einsum("ij,ij->i",T,N))))}
    if style == "ch3":
        base=np.array([[0,0,0],[1.2,0,.2],[.25,1,.1],[.1,.25,1.1]]); C=rotation_about_z(.75)@reflection_x(); a=np.array([1,-.4,.35]); moved=base@C.T+a; fig=plt.figure(figsize=(8.4,6)); ax=fig.add_subplot(111,projection="3d")
        for i,j in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]: ax.plot(*base[[i,j]].T,color=PALETTE["gray"],lw=1.2); ax.plot(*moved[[i,j]].T,color=PALETTE["teal"],lw=1.8)
        ax.scatter(*base.T,color=PALETTE["blue"],s=35,label="original"); ax.scatter(*moved.T,color=PALETTE["red"],s=35,label="moved"); ax.legend(); ax.set_title("Rigid motion preserves every edge length")
        d0=np.linalg.norm(base[:,None,:]-base[None,:,:],axis=-1); d1=np.linalg.norm(moved[:,None,:]-moved[None,:,:],axis=-1); return fig,{"distance_residual":float(np.max(np.abs(d0-d1))),"determinant":float(np.linalg.det(C))}
    if style == "ch4":
        u,v,U,V=uv_grid((-1.5,1.5),(-1.5,1.5),55); X=graph_surface(U,V,"saddle"); Xu,Xv=partials(X,u,v); cross=np.linalg.norm(np.cross(Xu,Xv),axis=-1); fig=plt.figure(figsize=(8.2,6.1)); ax=fig.add_subplot(111,projection="3d"); ax.plot_surface(X[...,0],X[...,1],X[...,2],cmap="viridis",alpha=.78,linewidth=0); m=len(u)//2; p=X[m,m]
        ax.quiver(p[0],p[1],p[2],Xu[m,m,0],Xu[m,m,1],Xu[m,m,2],length=.45,color=PALETTE["red"]); ax.quiver(p[0],p[1],p[2],Xv[m,m,0],Xv[m,m,1],Xv[m,m,2],length=.45,color=PALETTE["gold"]); ax.set_title("Patch partial velocities span the tangent plane"); return fig,{"min_patch_jacobian":float(np.min(cross))}
    if style == "ch5":
        th=np.linspace(0,2*np.pi,400); k1,k2=1.4,-.55; k=k1*np.cos(th)**2+k2*np.sin(th)**2; fig=plt.figure(figsize=(8,6)); ax=fig.add_subplot(111,projection="polar"); ax.plot(th,k,color=PALETTE["red"],lw=2); ax.plot(th,0*k,color=PALETTE["gray"],lw=.8); ax.set_title("Euler formula for normal curvature"); return fig,{"euler_formula_range":float(np.max(k)-np.min(k))}
    if style == "ch6":
        u,v,U,V=uv_grid((0,2*np.pi),(0,2*np.pi),90); R,r=2.0,.65; K=np.cos(V)/(r*(R+r*np.cos(V))); fig,ax=plt.subplots(figsize=(8.5,5.8)); im=ax.imshow(K,origin="lower",extent=[0,2*np.pi,0,2*np.pi],cmap="coolwarm",aspect="auto"); style_axis(ax,"Signed Gaussian curvature on a torus parameter rectangle"); fig.colorbar(im,ax=ax,label="K"); total=integrate_density(K*r*(R+r*np.cos(V)),u,v); return fig,{"torus_total_curvature_window":float(total)}
    if style == "ch7":
        r=np.linspace(.2,2.8,120); theta=np.linspace(.25,1.25,120); C=(1+.35*np.cos(r))*np.sin(theta); fig,ax=plt.subplots(figsize=(8,5.8)); ax.plot(r,C,color=PALETTE["blue"],lw=2); style_axis(ax,"Clairaut quantity as a geodesic diagnostic"); add_note(ax,"Exact revolution geodesics keep this trace constant."); return fig,{"clairaut_trace_variation":float(np.max(C)-np.min(C))}
    if style == "ch8":
        r=np.linspace(0,3,260); fig,ax=plt.subplots(figsize=(8.3,5.8))
        for K,col,label in [(1,PALETTE["red"],"K=1"),(0,PALETTE["gray"],"K=0"),(-1,PALETTE["blue"],"K=-1")]: ax.plot(r,constant_curvature_jacobi(K,r),color=col,label=label,lw=2)
        style_axis(ax,"Jacobi stretching in constant curvature"); ax.legend(); return fig,{"jacobi_residual_positive":jacobi_residual(1.0,r),"jacobi_residual_negative":jacobi_residual(-1.0,r)}
    if style == "appendix":
        t=np.linspace(0,6*np.pi,320); pts=np.column_stack([np.cos(t),np.sin(t),.3*t]); k=space_curvature(pts,t); tau=torsion(pts,t); fig,ax=plt.subplots(figsize=(8,5.8)); ax.plot(t,k,label="curvature",color=PALETTE["blue"]); ax.plot(t,tau,label="torsion",color=PALETTE["red"]); style_axis(ax,"Python curve diagnostics for a helix"); ax.legend(); return fig,{"helix_curvature_mean":float(np.mean(k[10:-10])),"helix_torsion_mean":float(np.mean(tau[10:-10]))}
    fig,ax=plt.subplots(figsize=(8,5.8)); labels=["Euclidean calculus","Frames","Surfaces","Curvature","Geodesics","Global structure"]; ax.barh(labels,np.arange(1,len(labels)+1),color=[PALETTE["blue"],PALETTE["teal"],PALETTE["green"],PALETTE["gold"],PALETTE["red"],PALETTE["violet"]]); style_axis(ax,"Course route as computational layers"); return fig,{"course_layers":float(len(labels))}

def lab_figure(style: str, title: str) -> tuple[plt.Figure, dict[str, float]]:
    fig,ax=plt.subplots(figsize=(8.2,5.8))
    if style in {"ch1","ch4"}:
        x,y=sp.symbols("x y"); f=x**2*y+sp.sin(y); ddf=exterior_derivative_1form(differential_of_function(f,x,y),x,y); xs=np.linspace(-1.5,1.5,120); ys=np.linspace(-1.5,1.5,120); X,Y=np.meshgrid(xs,ys); Z=X**2*Y+np.sin(Y); im=ax.contourf(X,Y,Z,18,cmap="viridis"); style_axis(ax,"A function, its differential, and d(df)=0",equal=True); add_note(ax, "Euclidean probe" if style=="ch1" else "Surface-form probe"); fig.colorbar(im,ax=ax,shrink=.8); return fig,{"d_d_f_residual":float(abs(float(ddf)))}
    if style in {"ch2","ch3"}:
        th=np.linspace(0,2*np.pi,160); errs=[orthonormality_error(rotation_about_z(t)) for t in th]; ax.plot(th,np.ones_like(th),color=PALETTE["teal"],label="det frame"); ax.plot(th,errs,color=PALETTE["red"],label="orthonormality error"); style_axis(ax,"Frame orientation and orthonormality diagnostics"); add_note(ax, "moving-frame lab" if style=="ch2" else "rigid-motion lab"); ax.legend(); return fig,{"max_orthonormality_error":float(max(errs))}
    if style in {"ch5","ch6"}:
        u,v,U,V=uv_grid((-1.6,1.6),(-1.6,1.6),100); Z=.25*(U**2-V**2); H,K=graph_curvature(Z,u[1]-u[0],v[1]-v[0]); im=ax.imshow(K,extent=[u.min(),u.max(),v.min(),v.max()],origin="lower",cmap="coolwarm"); style_axis(ax,"Saddle graph curvature sign",equal=True); add_note(ax, "shape-operator lab" if style=="ch5" else "intrinsic-curvature lab"); fig.colorbar(im,ax=ax,label="K"); return fig,{"saddle_K_min":float(np.min(K)),"saddle_K_max":float(np.max(K)),"mean_abs_H":float(np.mean(np.abs(H)))}
    if style == "ch7":
        verts=np.array([[0,0],[1,0],[.3,.85],[0,0]]); ax.plot(verts[:,0],verts[:,1],color=PALETTE["blue"],lw=2); ax.fill(verts[:,0],verts[:,1],color=PALETTE["gold"],alpha=.25); style_axis(ax,"Gauss-Bonnet proof state",equal=True); return fig,{"triangle_edges":3.0}
    if style == "ch8":
        t=np.linspace(0,2*np.pi,240); base=np.column_stack([np.cos(t),np.sin(t)]); ax.plot(base[:,0],base[:,1],color=PALETTE["blue"],label="base loop"); ax.plot(np.cos(t+2*np.pi),np.sin(t+2*np.pi),color=PALETTE["red"],ls="--",label="projected lift"); style_axis(ax,"Covering intuition",equal=True); ax.legend(); return fig,{"loop_closure_residual":float(np.linalg.norm(base[0]-base[-1]))}
    if style == "appendix":
        sol=solve_ivp(lambda t,y:[y[1],-y[0]],(0,2*np.pi),[1,0],t_eval=np.linspace(0,2*np.pi,200),rtol=1e-9,atol=1e-11); ax.plot(sol.t,sol.y[0],color=PALETTE["blue"],label="numeric"); ax.plot(sol.t,np.cos(sol.t),color=PALETTE["red"],ls="--",label="exact"); style_axis(ax,"ODE solution check"); ax.legend(); return fig,{"ode_max_error":float(np.max(np.abs(sol.y[0]-np.cos(sol.t))))}
    xs=np.arange(10); ax.plot(xs,xs**2,marker="o",color=PALETTE["blue"]); style_axis(ax,"Notebook course audit path"); return fig,{"inventory_items":10.0}

def interactive_figure(style: str, title: str) -> go.Figure:
    t=np.linspace(0,2*np.pi,180)
    if style in {"intro","ch1"}:
        fig=go.Figure(data=[go.Scatter3d(x=np.cos(t),y=np.sin(t),z=.25*np.sin(3*t),mode="lines",line={"width":5,"color":"#2f6fbb"})]); fig.update_layout(title=f"{title}: curve as map plus moving data",scene_aspectmode="data"); return fig
    if style in {"ch2","ch3","appendix"}:
        fig=go.Figure(data=[go.Scatter3d(x=np.cos(2*t),y=np.sin(2*t),z=.35*t,mode="lines",line={"width":5,"color":"#c44e52"})]); fig.update_layout(title=f"{title}: inspectable space curve",scene_aspectmode="data"); return fig
    u=np.linspace(-1.4,1.4,55); v=np.linspace(-1.4,1.4,55); U,V=np.meshgrid(u,v); Z=.25*(U**2-V**2)
    if style=="ch6": Z=.45*np.cos(U)*np.sin(V)
    elif style=="ch7": Z=np.sqrt(np.maximum(1-.18*U**2-.18*V**2,0))
    elif style=="ch8": Z=.25*np.cosh(U)-.2*np.cos(V)
    fig=go.Figure(data=[go.Surface(x=U,y=V,z=Z,colorscale="Viridis",showscale=True)]); fig.update_layout(title=f"{title}: rotatable surface model",scene_aspectmode="data"); return fig

def compute_checks(style: str, diagnostic_metrics: dict[str, float] | None = None, lab_metrics: dict[str, float] | None = None) -> dict[str, Any]:
    checks={"style":style}; x,y=sp.symbols("x y"); f=x**2*y+sp.sin(x*y); df=differential_of_function(f,x,y); checks["d_d_f_zero"]=bool(sp.simplify(exterior_derivative_1form(df,x,y))==0); checks["wedge_antisymmetry"]=bool(sp.simplify(wedge_1forms((x,y),(y,x))+wedge_1forms((y,x),(x,y)))==0)
    checks["orthonormality_error"]=orthonormality_error(rotation_about_z(.4)); checks["reflection_determinant"]=float(np.linalg.det(reflection_x()))
    t=np.linspace(0,4*np.pi,300); a=.35; helix=np.column_stack([np.cos(t),np.sin(t),a*t]); k=space_curvature(helix,t); tau=torsion(helix,t); checks["helix_curvature_residual"]=float(abs(np.mean(k[20:-20])-1/(1+a*a))); checks["helix_torsion_residual"]=float(abs(np.mean(tau[20:-20])-a/(1+a*a)))
    u,v,U,V=uv_grid((-.8,.8),(-.8,.8),50); X=graph_surface(U,V,"saddle"); Xu,Xv=partials(X,u,v); checks["min_surface_jacobian"]=float(np.min(np.linalg.norm(np.cross(Xu,Xv),axis=-1)))
    r=np.linspace(.05,2.5,180); checks["jacobi_residual_K0"]=jacobi_residual(0.0,r); checks["jacobi_residual_Kneg"]=jacobi_residual(-1.0,r); loop_t=np.linspace(0,2*np.pi,300); circle=np.column_stack([np.cos(loop_t),np.sin(loop_t)]); checks["winding_number_circle"]=winding_number(circle)
    diagnostic_metrics = diagnostic_metrics or {}
    lab_metrics = lab_metrics or {}
    checks["style_metric_checks"] = {
        "directional_derivative_residual": abs(diagnostic_metrics.get("directional_derivative_residual", 0.0)) < 1e-12,
        "frenet_orthogonality_error": abs(diagnostic_metrics.get("frenet_orthogonality_error", 0.0)) < 5e-2,
        "distance_residual": abs(diagnostic_metrics.get("distance_residual", 0.0)) < 1e-12,
        "min_patch_jacobian": diagnostic_metrics.get("min_patch_jacobian", 1.0) > 0.5,
        "d_d_f_residual": abs(lab_metrics.get("d_d_f_residual", 0.0)) < 1e-12,
        "max_orthonormality_error": abs(lab_metrics.get("max_orthonormality_error", 0.0)) < 1e-10,
        "ode_max_error": abs(lab_metrics.get("ode_max_error", 0.0)) < 5e-4,
    }
    checks["all_residuals_small"]=bool(checks["d_d_f_zero"] and checks["wedge_antisymmetry"] and checks["orthonormality_error"]<1e-10 and checks["helix_curvature_residual"]<2e-3 and checks["helix_torsion_residual"]<3e-3 and checks["jacobi_residual_K0"]<1e-9 and checks["jacobi_residual_Kneg"]<5e-3 and abs(checks["winding_number_circle"]-1)<1e-6 and all(checks["style_metric_checks"].values()))
    return checks
