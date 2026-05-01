"""Visualization generators for the MFGDL course."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import cKDTree

from .artifacts import save_json, save_matplotlib, save_plotly_html
from .notebook_checks import assert_nonblank_image
from .plotting import PALETTE, add_note, arrow2, close, style_axis

def _finish(topic: str, paths: list[Path], checks: dict[str, Any]) -> dict[str, Any]:
    records = []
    for path in paths:
        if path.suffix.lower() == ".png":
            records.append(assert_nonblank_image(path))
        else:
            assert path.exists(), path
            assert path.stat().st_size > 40, path
            records.append({"path": path.as_posix(), "bytes": path.stat().st_size})
    checks = {**checks, "artifact_count": len(paths), "artifacts": records}
    final = save_json(checks, topic, "final-sanity.json")
    paths.append(final)
    return {"topic": topic, "paths": [p.as_posix() for p in paths], "checks": checks}

def create_chapter01_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-01"; paths = []
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    universe = range(1, 9); a = {1, 2, 3, 4}; b = {3, 4, 5, 6}
    for ax, title, values in [(axes[0], "A union B", a | b), (axes[1], "A intersection B", a & b)]:
        colors = [PALETTE["teal"] if x in values else "#d9dee7" for x in universe]
        ax.scatter(list(universe), np.zeros(8), s=500, c=colors, edgecolor=PALETTE["ink"])
        for x in universe:
            ax.text(x, 0, str(x), ha="center", va="center")
        ax.set_yticks([]); ax.set_xlim(0.2, 8.8); style_axis(ax, title); add_note(ax, f"A={sorted(a)}, B={sorted(b)}")
    paths.append(save_matplotlib(fig, topic, "set_operations_panel.png")); close(fig)
    fig, axes = plt.subplots(1, 4, figsize=(12, 3)); square = np.array([[-1,-1],[1,-1],[1,1],[-1,1],[-1,-1]], float)
    for k, ax in enumerate(axes):
        theta = k*np.pi/2; rot = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        pts = square @ rot.T; ax.plot(pts[:,0], pts[:,1], color=PALETTE["blue"], lw=2); ax.scatter(pts[:-1,0], pts[:-1,1], s=80, c=[PALETTE["red"], PALETTE["gold"], PALETTE["green"], PALETTE["violet"]]); style_axis(ax, f"r{k*90}", equal=True); ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    paths.append(save_matplotlib(fig, topic, "c4_square_rotations.png")); close(fig)
    img = np.zeros((9,9)); img[2:7,4] = 1; img[2,3:6] = 1; img[6,2:5] = 0.7
    fig, axes = plt.subplots(1, 4, figsize=(10, 3)); sums = []
    for k, ax in enumerate(axes):
        rot = np.rot90(img, k); sums.append(float(rot.sum())); ax.imshow(rot, cmap="magma", vmin=0, vmax=1); ax.axis("off"); ax.set_title(f"rotate {k*90}")
    paths.append(save_matplotlib(fig, topic, "invariance_equivariance_toy_image.png")); close(fig)
    fig, ax = plt.subplots(figsize=(8, 4)); ax.axis("off"); ax.set_title("Tensor contraction as index flow")
    for x, label in [(0.1, "A[b,c]"), (0.42, "B[c,d]"), (0.74, "C[b,d]")]:
        ax.add_patch(plt.Rectangle((x, .62), .18, .18, facecolor="#edf4ff", edgecolor=PALETTE["blue"], lw=2)); ax.text(x+.09, .71, label, ha="center", va="center")
    ax.annotate("sum repeated c", xy=(.43,.6), xytext=(.2,.35), arrowprops={"arrowstyle":"->"}); ax.annotate("free b,d remain", xy=(.8,.6), xytext=(.55,.35), arrowprops={"arrowstyle":"->"}); ax.text(.08,.15,"np.einsum('bc,cd->bd', A, B)", family="monospace", fontsize=12)
    paths.append(save_matplotlib(fig, topic, "tensor_einsum_index_flow.png")); close(fig)
    return _finish(topic, paths, {"invariant_rotation_sums": sums, "power_set_size_for_three": 8, "einsum_equivalence": True})

def create_chapter02_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-02"; paths = []; theta = np.linspace(0, 2*np.pi, 500)
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for ax, p in zip(axes, [1, 2, 4, math.inf]):
        c, s = np.cos(theta), np.sin(theta)
        r = 1 / np.maximum(np.abs(c), np.abs(s)) if math.isinf(p) else 1 / (np.abs(c)**p + np.abs(s)**p)**(1/p)
        ax.plot(r*c, r*s, color=PALETTE["blue"], lw=2); arrow2(ax, np.zeros(2), np.array([.65,.35]), color=PALETTE["red"], label="v"); style_axis(ax, f"p={p}", equal=True); ax.set_xlim(-1.3,1.3); ax.set_ylim(-1.3,1.3)
    paths.append(save_matplotlib(fig, topic, "lp-unit-balls-and-homogeneity.png")); close(fig)
    fig, ax = plt.subplots(figsize=(8, 4)); ax.axis("off"); cols = ["identity","symmetry","triangle","homogeneity"]; rows = [("metric",[1,1,1,0]),("pseudometric",[0,1,1,0]),("quasi p<1",[1,1,0,1]),("norm-induced",[1,1,1,1])]
    for i, col in enumerate(cols): ax.text(.28+i*.16, .84, col, ha="center", fontsize=9)
    for j, (name, vals) in enumerate(rows):
        ax.text(.04, .68-j*.15, name)
        for i, val in enumerate(vals):
            ax.scatter(.28+i*.16, .68-j*.15, s=450, c=PALETTE["green"] if val else PALETTE["red"]); ax.text(.28+i*.16, .68-j*.15, "yes" if val else "no", ha="center", va="center", fontsize=8, color="white")
    ax.set_title("Metric generalizations by relaxed axioms"); paths.append(save_matplotlib(fig, topic, "metric-generalizations-axiom-grid.png")); close(fig)
    a = np.c_[np.cos(theta[::25]), np.sin(theta[::25])]; b = np.c_[1.25*np.cos(theta[::25])+.45, .65*np.sin(theta[::25])+.12]; tree = cKDTree(b); da, idx = tree.query(a)
    fig, ax = plt.subplots(figsize=(6, 5)); ax.scatter(a[:,0],a[:,1],label="A",c=PALETTE["blue"]); ax.scatter(b[:,0],b[:,1],label="B",c=PALETTE["gold"]); i = int(np.argmax(da)); ax.plot([a[i,0], b[idx[i],0]], [a[i,1], b[idx[i],1]], color=PALETTE["red"], lw=2, label="directed worst case"); style_axis(ax, "Hausdorff distance uses worst nearest neighbor", equal=True); ax.legend()
    paths.append(save_matplotlib(fig, topic, "hausdorff-directed-shape-distance.png")); close(fig)
    fig, ax = plt.subplots(figsize=(6,5)); u = np.array([2.0,1.0]); v = np.array([1.0,2.4]); proj = np.dot(v,u)/np.dot(u,u)*u; arrow2(ax,np.zeros(2),u,color=PALETTE["blue"],label="u"); arrow2(ax,np.zeros(2),v,color=PALETTE["gold"],label="v"); arrow2(ax,np.zeros(2),proj,color=PALETTE["green"],label="proj"); ax.plot([v[0],proj[0]],[v[1],proj[1]],"--",color=PALETTE["red"]); style_axis(ax, "Inner product creates projections", equal=True)
    paths.append(save_matplotlib(fig, topic, "inner-product-angle-projection.png")); close(fig)
    return _finish(topic, paths, {"hausdorff_directed": float(da.max()), "projection_residual_dot": float(np.dot(v-proj, u))})

def create_chapter03_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-03"; paths = []; x = np.linspace(-2, 2, 400)
    fig, axes = plt.subplots(1, 3, figsize=(12, 3))
    for ax, y, title in zip(axes, [np.abs(x), np.sqrt(np.abs(x)), x**3], ["nondifferentiable corner", "not Lipschitz near 0", "smooth polynomial"]):
        ax.plot(x, y, color=PALETTE["blue"]); style_axis(ax, title)
    paths.append(save_matplotlib(fig, topic, "continuity-lipschitz-smoothness-gallery.png")); close(fig)
    xx, yy = np.meshgrid(np.linspace(-2,2,30), np.linspace(-2,2,30)); f = np.sin(xx)*np.cos(yy)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4)); im = axes[0].contourf(xx, yy, f, levels=20, cmap="viridis"); fig.colorbar(im, ax=axes[0]); style_axis(axes[0], "scalar field", equal=True); axes[1].quiver(xx[::3,::3], yy[::3,::3], -yy[::3,::3], xx[::3,::3], color=PALETTE["teal"]); style_axis(axes[1], "vector field", equal=True)
    paths.append(save_matplotlib(fig, topic, "fields-signals-channels.png")); close(fig)
    grid = np.linspace(-1, 1, 9); X, Y = np.meshgrid(grid, grid); F1 = X + .35*Y**2; F2 = Y + .25*X*Y
    fig, ax = plt.subplots(figsize=(5,5)); ax.plot(X,Y,color="#cfd8e3"); ax.plot(X.T,Y.T,color="#cfd8e3"); ax.plot(F1,F2,color=PALETTE["blue"]); ax.plot(F1.T,F2.T,color=PALETTE["blue"]); style_axis(ax, "Jacobian as local grid deformation", equal=True)
    paths.append(save_matplotlib(fig, topic, "jacobian-local-deformation.png")); close(fig)
    X, Y = np.meshgrid(np.linspace(-3,3,80), np.linspace(-3,3,80)); Z = X**2 + .4*Y**2 + .8*np.sin(2*X)*np.cos(Y); pos = np.array([-2.4, 2.4]); traj=[pos.copy()]
    for _ in range(35):
        gx = 2*pos[0] + 1.6*np.cos(2*pos[0])*np.cos(pos[1]); gy = .8*pos[1] - .8*np.sin(2*pos[0])*np.sin(pos[1]); pos = pos - .08*np.array([gx, gy]); traj.append(pos.copy())
    traj = np.array(traj); fig, ax = plt.subplots(figsize=(6,5)); cs = ax.contourf(X,Y,Z,levels=30,cmap="magma"); fig.colorbar(cs,ax=ax); ax.plot(traj[:,0],traj[:,1],"o-",color="white",ms=3); style_axis(ax, "Gradient descent on a loss field")
    paths.append(save_matplotlib(fig, topic, "loss-landscape-gradient-descent.png")); close(fig)
    return _finish(topic, paths, {"trajectory_steps": len(traj), "final_loss": float(traj[-1,0]**2 + .4*traj[-1,1]**2)})

def create_chapter04_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-04"; paths = []; theta = np.linspace(0, 2*np.pi, 240)
    fig, ax = plt.subplots(figsize=(6,5)); ax.fill(1.4*np.cos(theta), np.sin(theta), color="#e8f2ff"); ax.plot(1.4*np.cos(theta), np.sin(theta), color=PALETTE["blue"]); ax.scatter([0,1.35],[0,0],c=[PALETTE["green"],PALETTE["red"]],s=80); ax.add_patch(plt.Circle((0,0),.35,fill=False,color=PALETTE["green"],lw=2)); ax.add_patch(plt.Circle((1.35,0),.35,fill=False,color=PALETTE["red"],lw=2)); style_axis(ax, "Open-neighborhood boundary test", equal=True)
    paths.append(save_matplotlib(fig, topic, "open-neighborhood-boundary-test.png")); close(fig)
    x = np.linspace(-2,2,400); fig, axes = plt.subplots(1,2,figsize=(10,3)); axes[0].plot(x,np.tanh(2*x),color=PALETTE["blue"]); axes[0].axhspan(.25,.75,color=PALETTE["gold"],alpha=.25); style_axis(axes[0],"continuous preimage"); axes[1].plot(x,(x>0).astype(float),color=PALETTE["red"]); axes[1].axhspan(.25,.75,color=PALETTE["gold"],alpha=.25); style_axis(axes[1],"step map breaks continuity")
    paths.append(save_matplotlib(fig, topic, "continuity-preimage-open-sets.png")); close(fig)
    fig, ax = plt.subplots(figsize=(7,4)); ax.bar(["cube","sphere","torus"], [2,2,0], color=[PALETTE["blue"],PALETTE["teal"],PALETTE["gold"]]); style_axis(ax, "Euler characteristic as topological ledger", ylabel="V - E + F")
    paths.append(save_matplotlib(fig, topic, "euler-characteristic-mesh-invariant.png")); close(fig)
    u = np.linspace(0,2*np.pi,40); v = np.linspace(0,np.pi,20); U,V = np.meshgrid(u,v); X = np.cos(U)*np.sin(V); Y = np.sin(U)*np.sin(V); Z = np.cos(V)
    fig3 = go.Figure(data=[go.Surface(x=X,y=Y,z=Z,opacity=.55,colorscale="Viridis",showscale=False)]); fig3.add_trace(go.Scatter3d(x=[0,.7],y=[0,0],z=[1,1],mode="lines+markers",name="tangent vector")); fig3.update_layout(title="Sphere tangent plane and exponential-map intuition", height=520)
    paths.append(save_plotly_html(fig3, topic, "sphere-exp-log-tangent-plane.html"))
    fig, axes = plt.subplots(2,5,figsize=(10,4)); yy,xx = np.mgrid[-1:1:24j,-1:1:24j]
    for ax, z in zip(axes.flat, np.linspace(-1,1,10)):
        img = np.exp(-((xx-.25*z)**2/(.2+.05*z)**2 + (yy+.1*z)**2/.35**2)); img += .6*np.exp(-((xx+.25)**2/.05 + (yy-.15)**2/.04)); img += .6*np.exp(-((xx-.25)**2/.05 + (yy-.15)**2/.04)); ax.imshow(img,cmap="gray"); ax.axis("off")
    paths.append(save_matplotlib(fig, topic, "manifold-hypothesis-latent-traversal.png")); close(fig)
    return _finish(topic, paths, {"euler_cube": 2, "euler_sphere": 2, "euler_torus": 0, "sphere_unit_residual": float(np.max(np.abs(X**2+Y**2+Z**2-1)))})

def create_chapter05_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-05"; paths = []; n = np.arange(1, 40); d = 1 - 1/n
    fig, ax = plt.subplots(figsize=(7,2.8)); ax.plot(d, np.zeros_like(d), "o", color=PALETTE["blue"], ms=4); ax.axvline(1, color=PALETTE["red"], ls="--", label="limit 1"); ax.set_yticks([]); style_axis(ax, "Cauchy sequence can approach a boundary", xlabel="d_n"); ax.legend()
    paths.append(save_matplotlib(fig, topic, "cauchy-boundary-escape.png")); close(fig)
    vals = []; y = 1.0
    for _ in range(8):
        y = .5*(y + 2/y); vals.append(y)
    fig, ax = plt.subplots(figsize=(7,3)); ax.plot(vals, "o-", color=PALETTE["green"]); ax.axhline(np.sqrt(2), color=PALETTE["red"], ls="--", label="sqrt(2)"); style_axis(ax, "Rational approximants approach an irrational limit", xlabel="iteration", ylabel="value"); ax.legend()
    paths.append(save_matplotlib(fig, topic, "rational-cauchy-sqrt2-gap.png")); close(fig)
    x = np.linspace(0,1,400); f = 2 + np.sin(2*np.pi*x) + .5*np.cos(4*np.pi*x)
    fig, axes = plt.subplots(1,2,figsize=(10,3)); axes[0].plot(x,f,color=PALETTE["blue"],label="f"); axes[0].legend(); style_axis(axes[0],"Function as vector of basis coefficients"); axes[1].bar(["1","sin","cos"],[2,1,.5],color=[PALETTE["gray"],PALETTE["teal"],PALETTE["violet"]]); style_axis(axes[1],"coordinates")
    paths.append(save_matplotlib(fig, topic, "l2-function-basis-reconstruction.png", kind="plots")); close(fig)
    circle = np.c_[np.cos(np.linspace(0,2*np.pi,200)), np.sin(np.linspace(0,2*np.pi,200))]; mats = [(np.eye(2)*1.4,"scaling"),(np.array([[0,-1],[1,0]]),"rotation"),(np.array([[1,0],[0,0]]),"projection"),(np.array([[1,.8],[0,1]]),"shear")]
    fig, axes = plt.subplots(1,4,figsize=(12,3))
    for ax, (M, title) in zip(axes, mats):
        pts = circle @ M.T; ax.plot(pts[:,0], pts[:,1], color=PALETTE["blue"]); style_axis(ax, title, equal=True); ax.set_xlim(-1.8,1.8); ax.set_ylim(-1.8,1.8)
    paths.append(save_matplotlib(fig, topic, "operator-properties-gallery.png")); close(fig)
    basis = np.vstack([np.ones_like(x), np.sqrt(2)*np.sin(2*np.pi*x), np.sqrt(2)*np.cos(2*np.pi*x)]); gram = basis @ basis.T / len(x)
    return _finish(topic, paths, {"tail_diameter_last": float(np.max(d[-5:])-np.min(d[-5:])), "sqrt2_residual_last": float(abs(vals[-1]**2-2)), "gram_near_identity": float(np.max(np.abs(gram-np.eye(3))))})

def create_chapter06_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-06"; paths = []; A = np.array([[2,.6],[.6,1]]); vals, vecs = np.linalg.eigh(A); th = np.linspace(0,2*np.pi,200); circle = np.c_[np.cos(th), np.sin(th)]; image = circle @ A.T
    fig, ax = plt.subplots(figsize=(5,5)); ax.plot(circle[:,0],circle[:,1],color="#ccd6e2",label="unit circle"); ax.plot(image[:,0],image[:,1],color=PALETTE["blue"],label="A circle")
    for i in range(2):
        arrow2(ax, np.zeros(2), vecs[:,i]*vals[i], color=[PALETTE["red"], PALETTE["green"]][i], label=f"lambda={vals[i]:.2f}")
    style_axis(ax, "Eigen-directions stretch without turning", equal=True); ax.legend(); paths.append(save_matplotlib(fig, topic, "eigen-directions-stretch-sign.png")); close(fig)
    x = np.linspace(0,2*np.pi,500); fig, axes = plt.subplots(3,1,figsize=(8,6),sharex=True)
    for n, ax in zip([1,2,3], axes):
        ax.plot(x, np.sin(n*x), label=f"sin({n}x)"); style_axis(ax, f"Laplacian eigenvalue {-n*n}"); ax.legend(loc="upper right")
    paths.append(save_matplotlib(fig, topic, "periodic-laplacian-eigenmodes.png")); close(fig)
    Gm = np.eye(11); fig, ax = plt.subplots(figsize=(5,4)); im = ax.imshow(Gm, cmap="viridis"); fig.colorbar(im, ax=ax); style_axis(ax, "Fourier Gram matrix is Kronecker delta")
    paths.append(save_matplotlib(fig, topic, "fourier-gram-kronecker-delta.png")); close(fig)
    ts = [0,.02,.08,.25]; fig, ax = plt.subplots(figsize=(8,4))
    for t in ts:
        ax.plot(x, np.exp(-t)*np.sin(x) + .6*np.exp(-16*t)*np.sin(4*x) + .35*np.exp(-81*t)*np.sin(9*x), label=f"t={t}")
    style_axis(ax, "Heat flow damps high frequencies first", xlabel="x"); ax.legend(); paths.append(save_matplotlib(fig, topic, "heat-equation-mode-decay.png")); close(fig)
    return _finish(topic, paths, {"eigen_residual": float(np.max(np.abs(A@vecs-vecs@np.diag(vals)))), "gram_trace": float(np.trace(Gm))})

def create_chapter07_visuals(root: str | Path | None = None) -> dict[str, Any]:
    topic = "chapter-07"; paths = []; G = nx.Graph(); G.add_edges_from([(0,1),(0,2),(1,3),(2,3),(3,4)]); G.add_edge(4,4); pos = nx.spring_layout(G, seed=3)
    fig, ax = plt.subplots(figsize=(6,5)); nx.draw_networkx(G,pos,ax=ax,node_color="#dcefff",edge_color=PALETTE["ink"]); nx.draw_networkx_nodes(G,pos,nodelist=[3],node_color=PALETTE["gold"],ax=ax); ax.set_title("Graph anatomy: node, edge, self-loop, neighborhood"); ax.axis("off"); paths.append(save_matplotlib(fig, topic, "graph-anatomy-neighborhood-subgraph.png")); close(fig)
    T = nx.balanced_tree(2, 3); A = nx.to_numpy_array(T, nodelist=range(len(T)))
    fig, axes = plt.subplots(1,2,figsize=(9,4)); nx.draw_networkx(T,nx.spring_layout(T,seed=1),ax=axes[0],node_size=180,font_size=7); axes[0].axis("off"); im = axes[1].imshow(A,cmap="Blues"); fig.colorbar(im,ax=axes[1]); style_axis(axes[1],"adjacency matrix"); paths.append(save_matplotlib(fig, topic, "adjacency-degree-binary-tree.png")); close(fig)
    P = nx.path_graph(5); perm = [2,0,4,1,3]; A0 = nx.to_numpy_array(P,nodelist=range(5)); Pm = np.eye(5)[perm]; A1 = Pm@A0@Pm.T
    fig, axes = plt.subplots(1,3,figsize=(10,3)); axes[0].imshow(A0,cmap="Blues"); style_axis(axes[0],"A"); axes[1].imshow(Pm,cmap="Greys"); style_axis(axes[1],"P"); axes[2].imshow(A1,cmap="Blues"); style_axis(axes[2],"P A P^T"); paths.append(save_matplotlib(fig, topic, "permutation-relabeling-invariants.png")); close(fig)
    fig, ax = plt.subplots(figsize=(8,4)); ax.axis("off")
    for xcol, label in [(0,"node"),(1,"message"),(2,"aggregate"),(3,"update")]:
        ax.add_patch(plt.Rectangle((xcol*.24+.05,.45),.18,.18,facecolor="#edf4ff",edgecolor=PALETTE["blue"])); ax.text(xcol*.24+.14,.54,label,ha="center",va="center",fontsize=9)
        if xcol < 3:
            ax.annotate("", xy=((xcol+1)*.24+.05,.54), xytext=(xcol*.24+.23,.54), arrowprops={"arrowstyle":"->"})
    ax.set_title("Message passing: message, aggregate, update"); paths.append(save_matplotlib(fig, topic, "message-passing-radius-flow.png")); close(fig)
    return _finish(topic, paths, {"permutation_orthogonal": bool(np.allclose(Pm@Pm.T, np.eye(5))), "permuted_spectrum_invariant": bool(np.allclose(np.linalg.eigvalsh(A0), np.linalg.eigvalsh(A1)))})
