"""Deterministic visual builders for the Topology course."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

from utils.artifacts import save_html, save_matplotlib


PALETTE = {
    "ink": "#233142",
    "blue": "#2f6fb0",
    "teal": "#1f8a83",
    "green": "#5d8c3a",
    "gold": "#c4912c",
    "red": "#bd4f4f",
    "violet": "#6b5aa8",
    "gray": "#6f7c8a",
    "light": "#edf2f7",
}


def style_axis(ax: Any, title: str, *, equal: bool = True) -> None:
    ax.set_title(title, fontsize=11, color=PALETTE["ink"])
    ax.grid(True, color="#d6dee8", linewidth=0.7, alpha=0.75)
    if equal:
        ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_color("#aeb9c5")


def _save(fig: Any, artifact_root: str | Path, filename: str) -> Path:
    path = save_matplotlib(fig, artifact_root, "figures", filename)
    plt.close(fig)
    return path


def make_html_lab(artifact_root: str | Path, filename: str, title: str, bullets: list[str]) -> Path:
    items = "\n".join(f"<li>{item}</li>" for item in bullets)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: system-ui, Segoe UI, sans-serif; margin: 0; padding: 24px; color: #233142; background: #f7fafc; }}
main {{ max-width: 900px; margin: auto; background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 20px; }}
.bar {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; margin: 20px 0; }}
.bar span {{ height: 46px; border-radius: 4px; background: linear-gradient(135deg, #2f6fb0, #1f8a83); opacity: calc(.35 + var(--i) * .1); }}
li {{ margin: 8px 0; }}
</style>
</head>
<body><main>
<h1>{title}</h1>
<p>This lightweight HTML lab records the interactive question for the notebook. Re-run the notebook cells to vary the parameters and compare the invariant that stays visible.</p>
<div class="bar">{''.join(f'<span style="--i:{i}"></span>' for i in range(6))}</div>
<ul>{items}</ul>
</main></body></html>"""
    return save_html(html, artifact_root, "html", filename)


def render_chapter_visual(chapter: int, index: int, artifact_root: str | Path, filename: str, title: str) -> Path:
    builders = [
        _venn,
        _function_fibers,
        _graph_partition,
        _grid_path,
        _flow_diagram,
        _topology_lattice,
        _basis_unions,
        _product_grid,
        _preimage_test,
        _quotient_map,
        _components,
        _intervals,
        _cover_subcover,
        _clusters,
        _neighborhoods,
        _basis_grid,
        _separation_witnesses,
        _closed_set_separation,
        _heatmap_function,
        _embedding_map,
        _cube_product,
        _subbase_cover,
        _tube_lemma,
        _extension_map,
        _choice_flow,
        _locally_finite,
        _refinement,
        _bumps,
        _distance_field,
        _paracompact_flow,
        _cauchy_track,
        _hilbert_curve,
        _metric_compactness,
        _convergence_tubes,
        _equicontinuity,
        _baire_game,
        _rough_function,
        _meagre_dense,
        _dimension_cover,
        _atlas,
        _homotopy_strip,
        _loop_group,
        _covering_lift,
        _retraction,
        _surface_polygon,
        _jordan_regions,
        _domain_grid,
        _planar_graph,
        _winding_field,
        _contour,
        _free_product,
        _overlap_diagram,
        _rose,
        _two_cell,
        _presentation_pair,
        _schema,
        _orientability,
        _euler_table,
        _surface_meshes,
        _classification_flow,
        _cover_ladder,
        _universal_grid,
        _deck_orbits,
        _subgroup_lattice,
        _lifting_tree,
    ]
    pos = (chapter - 1) * 5 + (index - 1)
    builder = builders[pos] if pos < len(builders) else _flow_diagram
    return builder(artifact_root, filename, title)


def _venn(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.add_patch(Circle((-0.45, 0), 1.0, color=PALETTE["blue"], alpha=0.28))
    ax.add_patch(Circle((0.45, 0), 1.0, color=PALETTE["teal"], alpha=0.28))
    ax.text(-0.95, 0.05, "A", fontsize=15)
    ax.text(0.95, 0.05, "B", fontsize=15)
    ax.text(0, 0, "A and B", ha="center", va="center", fontsize=10)
    ax.text(0, -1.35, "Union accepts either side; intersection asks for both.", ha="center", fontsize=9)
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.6, 1.4); ax.axis("off")
    style_axis(ax, title)
    return _save(fig, root, filename)


def _function_fibers(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    xs = np.linspace(-2, 2, 300)
    ax.plot(xs, xs**2, color=PALETTE["blue"], lw=2, label="f(x)=x^2")
    ax.axhline(1, color=PALETTE["red"], ls="--", label="fiber over 1")
    ax.scatter([-1, 1], [1, 1], s=55, color=PALETTE["red"])
    ax.text(0, 2.6, "two preimages: not injective", ha="center")
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-0.2, 4.3); ax.legend(fontsize=8)
    style_axis(ax, title, equal=False)
    return _save(fig, root, filename)


def _graph_partition(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    groups = [[0, 1, 2], [3, 4], [5]]
    x = 0
    for group in groups:
        xs = np.arange(len(group)) + x
        ax.scatter(xs, [0]*len(group), s=80, color=PALETTE["teal"])
        ax.add_patch(Rectangle((x-0.35, -0.35), len(group)-0.3, 0.7, fill=False, ec=PALETTE["blue"], lw=2))
        for j, item in enumerate(group):
            ax.text(x+j, 0.12, str(item), ha="center")
        x += len(group) + 0.8
    ax.text(2.5, -0.9, "Equivalence classes partition the space; order arrows add direction.", ha="center")
    ax.arrow(0, 1, 4.8, 0, width=0.025, color=PALETTE["gold"], length_includes_head=True)
    ax.text(2.5, 1.18, "order direction", ha="center")
    ax.set_xlim(-0.8, 6.7); ax.set_ylim(-1.2, 1.55); ax.axis("off")
    return _save(fig, root, filename)


def _grid_path(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    n = 7
    pts = [(i, j) for s in range(2*n-1) for i in range(n) for j in range(n) if i+j == s]
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=16, color=PALETTE["gray"])
    path = pts[:32]
    ax.plot([p[0] for p in path], [p[1] for p in path], color=PALETTE["blue"], lw=2)
    for k, p in enumerate(path[:12]):
        ax.text(p[0]+0.05, p[1]+0.05, str(k), fontsize=7)
    style_axis(ax, title)
    return _save(fig, root, filename)


def _flow_diagram(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    labels = ["objects", "rules", "witnesses", "theorem"]
    for i, label in enumerate(labels):
        ax.add_patch(Rectangle((i*1.6, 0), 1.15, 0.62, fc=PALETTE["light"], ec=PALETTE["blue"], lw=1.5))
        ax.text(i*1.6+0.575, 0.31, label, ha="center", va="center", fontsize=9)
        if i < len(labels)-1:
            ax.add_patch(FancyArrowPatch((i*1.6+1.15, 0.31), ((i+1)*1.6, 0.31), arrowstyle="->", mutation_scale=12, color=PALETTE["gold"]))
    ax.set_xlim(-0.2, 5.95); ax.set_ylim(-0.3, 1.1); ax.axis("off"); ax.set_title(title, fontsize=11)
    return _save(fig, root, filename)


def _topology_lattice(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    G = nx.DiGraph()
    nodes = ["∅", "{a}", "{a,b}", "{a,b,c}"]
    G.add_edges_from([("∅", "{a}"), ("{a}", "{a,b}"), ("{a,b}", "{a,b,c}")])
    pos = {"∅": (0,0), "{a}": (0,1), "{a,b}": (0,2), "{a,b,c}": (0,3)}
    nx.draw(G, pos, ax=ax, with_labels=True, node_color="#d9f0f0", edge_color=PALETTE["blue"], node_size=1450, arrows=True)
    ax.set_title(title, fontsize=11); ax.axis("off")
    return _save(fig, root, filename)


def _basis_unions(root, filename, title):
    fig, ax = plt.subplots(figsize=(6.2,4))
    for x, y, w, h, c in [(0,0,1.7,1.0,"blue"), (1.0,0.35,1.7,1.0,"teal"), (2.1,0.0,1.7,1.0,"gold")]:
        ax.add_patch(Rectangle((x,y),w,h,fc=PALETTE[c],alpha=0.25,ec=PALETTE[c],lw=2))
    ax.text(1.9,-0.45,"basis pieces union into open neighborhoods",ha="center")
    ax.set_xlim(-0.2,4.0); ax.set_ylim(-0.7,1.7); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig, root, filename)


def _product_grid(root, filename, title):
    fig, ax = plt.subplots(figsize=(5.4,4.4))
    for i in range(5):
        for j in range(4):
            ax.add_patch(Rectangle((i,j),0.85,0.75,fc="#f7fafc",ec="#cbd5e1"))
    ax.add_patch(Rectangle((1,1),2.7,1.5,fc=PALETTE["blue"],alpha=0.25,ec=PALETTE["blue"],lw=2))
    ax.plot([0,4.7],[1.5,1.5],color=PALETTE["red"],lw=2,label="subspace slice")
    ax.legend(fontsize=8); style_axis(ax,title)
    return _save(fig, root, filename)


def _preimage_test(root, filename, title):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.add_patch(Rectangle((0,0),2,2,fc="#edf2f7",ec=PALETTE["blue"],lw=2))
    ax.add_patch(Circle((1,1),0.65,fc=PALETTE["teal"],alpha=.35,ec=PALETTE["teal"]))
    ax.add_patch(Rectangle((3,0.2),2,1.6,fc="#fff7e8",ec=PALETTE["gold"],lw=2))
    ax.add_patch(Circle((4,1),0.5,fc=PALETTE["red"],alpha=.28,ec=PALETTE["red"]))
    ax.add_patch(FancyArrowPatch((2.1,1),(2.9,1),arrowstyle="->",mutation_scale=15,color=PALETTE["ink"]))
    ax.text(2.5,1.2,"f",ha="center"); ax.text(1,-.35,"preimage open?",ha="center"); ax.text(4,-.35,"target open",ha="center")
    ax.set_xlim(-.2,5.3); ax.set_ylim(-.6,2.4); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig, root, filename)


def _quotient_map(root, filename, title):
    fig, ax = plt.subplots(figsize=(6,4))
    xs=np.linspace(0,4,80); ax.plot(xs,np.sin(xs),color=PALETTE["blue"],lw=2)
    ax.scatter([0,4],[0,np.sin(4)],s=70,color=PALETTE["red"])
    ax.add_patch(FancyArrowPatch((0,0),(4,np.sin(4)),arrowstyle="<->",connectionstyle="arc3,rad=.35",mutation_scale=12,color=PALETTE["red"]))
    ax.text(2,-.95,"identify endpoints: interval becomes a loop",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig, root, filename)


def _components(root, filename, title):
    fig, ax=plt.subplots(figsize=(5.6,4))
    G=nx.Graph(); G.add_edges_from([(0,1),(1,2),(3,4),(5,6),(6,7),(7,5)])
    pos=nx.spring_layout(G,seed=4)
    colors=[PALETTE["blue"] if n<3 else PALETTE["teal"] if n<5 else PALETTE["gold"] for n in G.nodes]
    nx.draw(G,pos,ax=ax,with_labels=True,node_color=colors,node_size=650,edge_color="#94a3b8")
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _intervals(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    xs=np.linspace(0,1,200); ax.plot(xs,xs*(1-xs),color=PALETTE["blue"],lw=2)
    ax.axhline(.18,color=PALETTE["red"],ls="--"); ax.scatter([.235,.765],[.18,.18],color=PALETTE["red"])
    ax.text(.5,-.08,"connected interval forces crossings between endpoint values",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _cover_subcover(root, filename, title):
    fig,ax=plt.subplots(figsize=(6.3,3.6))
    ax.plot([0,5],[0,0],color=PALETTE["ink"],lw=2)
    intervals=[(.0,1.5),(1.0,2.7),(2.4,3.8),(3.5,5.0),(.7,4.3)]
    for k,(a,b) in enumerate(intervals):
        y=.25+.22*k; ax.plot([a,b],[y,y],lw=8,solid_capstyle="round",color=PALETTE["blue" if k in [0,2,3] else "gray"],alpha=.75)
    ax.text(2.5,1.7,"highlighted intervals already cover the compact segment",ha="center")
    ax.set_xlim(-.2,5.2); ax.set_ylim(-.25,1.95); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _clusters(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    n=np.arange(1,60); pts=np.c_[1/n, np.sin(n)/n]
    ax.scatter(pts[:,0],pts[:,1],s=18,c=n,cmap="viridis")
    ax.scatter([0],[0],s=90,color=PALETTE["red"],label="limit point")
    ax.legend(fontsize=8); style_axis(ax,title)
    return _save(fig,root,filename)


def _neighborhoods(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    for r,c in [(1.2,"blue"),(.8,"teal"),(.42,"gold")]:
        ax.add_patch(Circle((0,0),r,fill=False,ec=PALETTE[c],lw=2))
    ax.scatter([0],[0],color=PALETTE["red"]); ax.scatter([1.55],[0],marker="x",s=80,color=PALETTE["red"])
    ax.text(0,-1.55,"compact neighborhoods shrink around the point; missing points break local tests",ha="center",fontsize=8)
    ax.set_xlim(-1.8,1.9); ax.set_ylim(-1.75,1.55); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _basis_grid(root, filename, title):
    return _grid_path(root, filename, title)


def _separation_witnesses(root, filename, title):
    fig,ax=plt.subplots(figsize=(6.2,4))
    labels=["T0","T1","Hausdorff","normal"]
    for i,label in enumerate(labels):
        ax.scatter([i*1.4,i*1.4+.5],[0,0],color=[PALETTE["blue"],PALETTE["red"]],s=45)
        ax.add_patch(Circle((i*1.4,0),.38,fill=False,ec=PALETTE["blue"],lw=1.5))
        if label in ["Hausdorff","normal"]:
            ax.add_patch(Circle((i*1.4+.5,0),.38,fill=False,ec=PALETTE["red"],lw=1.5))
        ax.text(i*1.4+.25,-.75,label,ha="center")
    ax.set_xlim(-.6,5.4); ax.set_ylim(-1.1,.8); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _closed_set_separation(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.6,4))
    ax.add_patch(Rectangle((-1.8,-1.2),1.2,1.0,fc=PALETTE["blue"],alpha=.25,ec=PALETTE["blue"]))
    ax.add_patch(Rectangle((.6,.1),1.2,1.0,fc=PALETTE["red"],alpha=.25,ec=PALETTE["red"]))
    ax.add_patch(Rectangle((-2.0,-1.4),1.6,1.4,fill=False,ec=PALETTE["teal"],lw=2))
    ax.add_patch(Rectangle((.4,-.1),1.6,1.4,fill=False,ec=PALETTE["gold"],lw=2))
    ax.text(0,-1.65,"closed sets get disjoint open buffers",ha="center")
    ax.set_xlim(-2.4,2.4); ax.set_ylim(-1.9,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _heatmap_function(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4.3))
    x=np.linspace(-2,2,150); y=np.linspace(-1.5,1.5,120); X,Y=np.meshgrid(x,y)
    Z=1/(1+np.exp(-3*X))
    im=ax.imshow(Z,extent=[-2,2,-1.5,1.5],origin="lower",cmap="viridis",aspect="auto")
    ax.scatter([-1.3,1.3],[0,0],color=["white","black"],s=70)
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04)
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _embedding_map(root, filename, title):
    return _preimage_test(root, filename, title)


def _cube_product(root, filename, title):
    fig=plt.figure(figsize=(5.6,4.4)); ax=fig.add_subplot(111,projection="3d")
    pts=np.array([[i,j,k] for i in [0,1] for j in [0,1] for k in [0,1]])
    ax.scatter(pts[:,0],pts[:,1],pts[:,2],s=60,c=pts[:,2],cmap="viridis")
    for a in pts:
        for b in pts:
            if np.sum(np.abs(a-b))==1:
                ax.plot(*zip(a,b),color="#94a3b8")
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _subbase_cover(root, filename, title):
    return _basis_unions(root, filename, title)


def _tube_lemma(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    ax.add_patch(Rectangle((-.5,-.2),4.5,1.4,fc=PALETTE["light"],ec=PALETTE["gray"]))
    ax.add_patch(Rectangle((.4,.1),2.7,.8,fc=PALETTE["blue"],alpha=.25,ec=PALETTE["blue"],lw=2))
    ax.plot([1.75,1.75],[-.2,1.2],color=PALETTE["red"],lw=2,label="compact fiber")
    ax.legend(fontsize=8); ax.text(1.75,-.55,"tube surrounds a whole compact slice",ha="center")
    ax.set_xlim(-.8,4.3); ax.set_ylim(-.8,1.5); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _extension_map(root, filename, title):
    return _flow_diagram(root, filename, title)


def _choice_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _locally_finite(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    for i,x in enumerate(np.linspace(-2,2,8)):
        ax.add_patch(Circle((x,0),.55,fill=False,ec=PALETTE["blue" if i%2 else "teal"],lw=1.5,alpha=.8))
    ax.scatter([0],[0],color=PALETTE["red"]); ax.text(0,-.95,"each point meets only finitely many chosen neighborhoods",ha="center")
    ax.set_xlim(-2.8,2.8); ax.set_ylim(-1.2,1.0); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _refinement(root, filename, title):
    return _flow_diagram(root, filename, title)


def _bumps(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,6,300)
    for c,col in [(1,"blue"),(2.4,"teal"),(3.7,"gold"),(5,"red")]:
        y=np.maximum(0,1-np.abs(x-c)/1.0)
        ax.plot(x,y,color=PALETTE[col],lw=2)
    ax.text(3,-.25,"local bump functions encode a cover",ha="center")
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _distance_field(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.3,4.2))
    x=np.linspace(-2,2,120); y=np.linspace(-2,2,120); X,Y=np.meshgrid(x,y)
    Z=np.sqrt((X+1)**2+Y**2)-np.sqrt((X-1)**2+Y**2)
    im=ax.contourf(X,Y,Z,levels=20,cmap="coolwarm")
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04)
    style_axis(ax,title)
    return _save(fig,root,filename)


def _paracompact_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _cauchy_track(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4))
    n=np.arange(1,45); x=np.cumsum(1/(n**1.35)); y=np.sin(n)/n
    ax.plot(x,y,"-o",ms=3,color=PALETTE["blue"]); ax.scatter([x[-1]],[0],s=70,color=PALETTE["red"],label="completion target")
    ax.legend(fontsize=8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _hilbert_curve(root, filename, title):
    fig,ax=plt.subplots(figsize=(4.8,4.8))
    pts=[(0,0),(0,1),(1,1),(1,0),(2,0),(2,1),(3,1),(3,0),(3,2),(2,2),(2,3),(3,3),(1,3),(1,2),(0,2),(0,3)]
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=PALETTE["blue"],lw=2)
    ax.scatter([p[0] for p in pts],[p[1] for p in pts],s=18,color=PALETTE["gold"])
    style_axis(ax,title)
    return _save(fig,root,filename)


def _metric_compactness(root, filename, title):
    return _clusters(root, filename, title)


def _convergence_tubes(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,1,200); f=x*(1-x)
    ax.plot(x,f,color=PALETTE["ink"],lw=2,label="limit")
    for eps in [.05,.12,.22]:
        ax.fill_between(x,f-eps,f+eps,color=PALETTE["blue"],alpha=.08)
    ax.legend(fontsize=8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _equicontinuity(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.7,4))
    x=np.linspace(-1,1,120)
    for a in np.linspace(.4,1.4,6):
        ax.plot(x,np.tanh(a*x),color=PALETTE["teal"],alpha=.7)
    ax.add_patch(Rectangle((-.2,-.35),.4,.7,fill=False,ec=PALETTE["red"],lw=2))
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _baire_game(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    for k in range(6):
        ax.plot([k*.35, 5-k*.35],[k*.24,k*.24],lw=8,solid_capstyle="round",color=PALETTE["blue" if k%2 else "teal"],alpha=.75)
    ax.text(2.5,-.3,"nested open choices keep a point in the intersection",ha="center")
    ax.set_xlim(-.2,5.2); ax.set_ylim(-.55,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _rough_function(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    x=np.linspace(0,1,600); y=np.zeros_like(x)
    for n in range(1,7):
        y += (0.55**n)*np.abs((x*2**n)%1-.5)
    ax.plot(x,y,color=PALETTE["blue"],lw=1.8); style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _meagre_dense(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.5))
    ax.plot([0,1],[0,0],color=PALETTE["ink"],lw=2)
    xs=np.linspace(0,1,25)
    ax.scatter(xs,0*xs,s=25,color=PALETTE["red"],label="thin pieces")
    for a,b in [(0.05,.25),(.28,.62),(.65,.95)]:
        ax.plot([a,b],[.25,.25],lw=8,color=PALETTE["teal"],alpha=.6)
    ax.legend(fontsize=8); ax.set_ylim(-.35,.65); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _dimension_cover(root, filename, title):
    return _product_grid(root, filename, title)


def _atlas(root, filename, title):
    return _basis_unions(root, filename, title)


def _homotopy_strip(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    t=np.linspace(0,1,100)
    for s in np.linspace(0,1,7):
        y=(1-s)*np.sin(2*np.pi*t)*.35+s*(t-.5)**2
        ax.plot(t,y,color=PALETTE["blue"],alpha=.35+.08*s)
    ax.scatter([0,1],[0,0],color=PALETTE["red"])
    style_axis(ax,title,equal=False)
    return _save(fig,root,filename)


def _loop_group(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,4))
    for cx,col,label in [(-1.1,"blue","alpha"),(.2,"teal","beta"),(1.4,"gold","alpha beta")]:
        ax.add_patch(Circle((cx,0),.5,fill=False,ec=PALETTE[col],lw=2))
        ax.text(cx,-.75,label,ha="center")
    ax.add_patch(FancyArrowPatch((-.55,0),(-.35,0),arrowstyle="->",mutation_scale=12,color=PALETTE["ink"]))
    ax.add_patch(FancyArrowPatch((.75,0),(.9,0),arrowstyle="->",mutation_scale=12,color=PALETTE["ink"]))
    ax.set_xlim(-1.9,2.1); ax.set_ylim(-1,1); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _covering_lift(root, filename, title):
    fig=plt.figure(figsize=(5.8,4.4)); ax=fig.add_subplot(111,projection="3d")
    t=np.linspace(0,5*np.pi,250)
    ax.plot(np.cos(t),np.sin(t),t/(2*np.pi),color=PALETTE["blue"],lw=2)
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _retraction(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.4))
    ax.add_patch(Circle((0,0),1.0,fill=False,ec=PALETTE["ink"],lw=2))
    ax.add_patch(Circle((0,0),.28,fc="white",ec=PALETTE["red"],lw=2))
    for ang in np.linspace(0,2*np.pi,10,endpoint=False):
        ax.arrow(.35*np.cos(ang),.35*np.sin(ang),.45*np.cos(ang),.45*np.sin(ang),head_width=.05,color=PALETTE["blue"])
    ax.text(0,-1.3,"retraction would push punctured disk to boundary",ha="center",fontsize=8)
    ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.45,1.3); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _surface_polygon(root, filename, title):
    return _schema(root, filename, title)


def _jordan_regions(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.4))
    t=np.linspace(0,2*np.pi,300); r=1+.18*np.sin(3*t)
    ax.fill(r*np.cos(t),r*np.sin(t),color=PALETTE["blue"],alpha=.18)
    ax.plot(r*np.cos(t),r*np.sin(t),color=PALETTE["blue"],lw=2)
    ax.text(0,0,"inside",ha="center"); ax.text(1.55,1.15,"outside",ha="center")
    ax.set_xlim(-1.8,1.9); ax.set_ylim(-1.6,1.6); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _domain_grid(root, filename, title):
    return _product_grid(root, filename, title)


def _planar_graph(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.5,4.2))
    G=nx.cycle_graph(6); G.add_edge(0,3); G.add_edge(1,4)
    pos=nx.circular_layout(G)
    nx.draw(G,pos,ax=ax,with_labels=True,node_color="#d9f0f0",edge_color=PALETTE["blue"],node_size=650)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _winding_field(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.3))
    x=np.linspace(-2,2,120); y=np.linspace(-2,2,120); X,Y=np.meshgrid(x,y)
    Z=np.arctan2(Y,X)
    im=ax.imshow(Z,extent=[-2,2,-2,2],origin="lower",cmap="twilight",aspect="auto")
    ax.add_patch(Circle((0,0),1,fill=False,ec="white",lw=2))
    fig.colorbar(im,ax=ax,fraction=.046,pad=.04); style_axis(ax,title)
    return _save(fig,root,filename)


def _contour(root, filename, title):
    return _winding_field(root, filename, title)


def _free_product(root, filename, title):
    return _flow_diagram(root, filename, title)


def _overlap_diagram(root, filename, title):
    return _venn(root, filename, title)


def _rose(root, filename, title):
    fig,ax=plt.subplots(figsize=(5,4.2))
    for ang,col in [(0,"blue"),(2*np.pi/3,"teal"),(4*np.pi/3,"gold")]:
        cx=.55*np.cos(ang); cy=.55*np.sin(ang)
        ax.add_patch(Circle((cx,cy),.55,fill=False,ec=PALETTE[col],lw=2))
    ax.scatter([0],[0],color=PALETTE["red"],s=50)
    ax.set_xlim(-1.4,1.4); ax.set_ylim(-1.25,1.25); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _two_cell(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.4,4.2))
    ax.add_patch(Circle((0,0),1,fc=PALETTE["blue"],alpha=.16,ec=PALETTE["blue"],lw=2))
    t=np.linspace(0,2*np.pi,120); ax.plot(np.cos(t),np.sin(2*t)/2,color=PALETTE["red"],lw=2)
    ax.text(0,-1.3,"attaching loop becomes a relation",ha="center")
    ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.55,1.25); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _presentation_pair(root, filename, title):
    return _schema(root, filename, title)


def _schema(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.2,4.4))
    angles=np.linspace(0,2*np.pi,7)[:-1]+np.pi/6
    pts=np.c_[np.cos(angles),np.sin(angles)]
    ax.add_patch(Polygon(pts,fill=False,ec=PALETTE["ink"],lw=2))
    labels=["a","b","a⁻","b⁻","c","c⁻"]
    for i,label in enumerate(labels):
        p=(pts[i]+pts[(i+1)%6])/2
        ax.text(p[0]*1.15,p[1]*1.15,label,ha="center",va="center",color=PALETTE["blue"])
    ax.set_xlim(-1.45,1.45); ax.set_ylim(-1.35,1.35); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _orientability(root, filename, title):
    fig,ax=plt.subplots(figsize=(6,3.8))
    ax.add_patch(Rectangle((-.2,-.4),2.2,.8,fill=False,ec=PALETTE["blue"],lw=2))
    ax.add_patch(FancyArrowPatch((0,0),(1.8,0),arrowstyle="->",mutation_scale=14,color=PALETTE["blue"]))
    ax.add_patch(Rectangle((3,-.4),2.2,.8,fill=False,ec=PALETTE["red"],lw=2))
    ax.add_patch(FancyArrowPatch((3.2,0),(4.8,0),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.add_patch(FancyArrowPatch((4.8,.25),(3.2,.25),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.text(1,-.85,"matched orientation",ha="center"); ax.text(4.1,-.85,"twist conflict",ha="center")
    ax.set_xlim(-.6,5.5); ax.set_ylim(-1.2,.8); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _euler_table(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,3.8))
    data=[["sphere",2],["torus",0],["double torus",-2],["projective plane",1]]
    ax.axis("off")
    table=ax.table(cellText=data,colLabels=["surface","chi"],loc="center",cellLoc="center")
    table.scale(1,1.6)
    ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _surface_meshes(root, filename, title):
    fig=plt.figure(figsize=(6,4.2)); ax=fig.add_subplot(111,projection="3d")
    u=np.linspace(0,2*np.pi,40); v=np.linspace(0,2*np.pi,20)
    U,V=np.meshgrid(u,v); R=1.1; r=.35
    X=(R+r*np.cos(V))*np.cos(U); Y=(R+r*np.cos(V))*np.sin(U); Z=r*np.sin(V)
    ax.plot_surface(X,Y,Z,color="#d9edf7",edgecolor="white",linewidth=.2)
    ax.set_title(title,fontsize=11); ax.set_axis_off()
    return _save(fig,root,filename)


def _classification_flow(root, filename, title):
    return _flow_diagram(root, filename, title)


def _cover_ladder(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    for y in [0,1,2]:
        ax.plot([0,4],[y,y],color=PALETTE["blue"],lw=2)
    for x in np.linspace(.5,3.5,4):
        ax.plot([x,x],[0,2],color=PALETTE["gray"],ls="--")
    ax.add_patch(FancyArrowPatch((4.25,2),(4.25,0),arrowstyle="->",mutation_scale=14,color=PALETTE["red"]))
    ax.text(4.45,1,"p",va="center")
    ax.set_xlim(-.2,4.8); ax.set_ylim(-.3,2.4); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _universal_grid(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.2,4.4))
    for i in range(-3,4):
        ax.plot([i,i],[-2,2],color="#cbd5e1")
    for j in range(-2,3):
        ax.plot([-3,3],[j,j],color="#cbd5e1")
    ax.arrow(-2.5,0,5,0,head_width=.08,color=PALETTE["blue"],length_includes_head=True)
    ax.arrow(0,-1.5,0,3,head_width=.08,color=PALETTE["teal"],length_includes_head=True)
    ax.set_xlim(-3.2,3.2); ax.set_ylim(-2.2,2.2); ax.axis("off"); ax.set_title(title,fontsize=11)
    return _save(fig,root,filename)


def _deck_orbits(root, filename, title):
    return _universal_grid(root, filename, title)


def _subgroup_lattice(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.6,4.2))
    G=nx.DiGraph(); G.add_edges_from([("Z","2Z"),("Z","3Z"),("2Z","6Z"),("3Z","6Z"),("6Z","0")])
    pos={"Z":(0,3),"2Z":(-1,2),"3Z":(1,2),"6Z":(0,1),"0":(0,0)}
    nx.draw(G,pos,ax=ax,with_labels=True,node_color="#fff1c7",edge_color=PALETTE["gold"],node_size=950,arrows=True)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)


def _lifting_tree(root, filename, title):
    fig,ax=plt.subplots(figsize=(5.8,4))
    G=nx.balanced_tree(2,3); pos=nx.nx_agraph.graphviz_layout(G,prog="dot") if False else nx.spring_layout(G,seed=8)
    nx.draw(G,pos,ax=ax,node_color="#d9f0f0",edge_color=PALETTE["teal"],node_size=300)
    ax.set_title(title,fontsize=11); ax.axis("off")
    return _save(fig,root,filename)
