"""Course-local figure builders for generated artifacts."""
from __future__ import annotations
import html, json, math
from pathlib import Path
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .cat_checks import quick_check
PALETTE = ["#28587b", "#d95f02", "#1b9e77", "#7570b3", "#b35806", "#4d9221"]
def _finish(ax):
    ax.set_aspect("equal", adjustable="box"); ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values(): spine.set_visible(False)
def _triangle(ax, unit):
    pts = np.array([[0,0],[4.2,0],[1.15,2.85]])
    ax.fill(pts[:,0], pts[:,1], color="#eaf2f8", ec="#28587b", lw=2)
    p = pts[0]*0.55 + pts[1]*0.45; q = pts[0]*0.35 + pts[2]*0.65
    ax.plot([p[0], q[0]], [p[1], q[1]], color="#4d9221", lw=3)
    ax.plot([pts[0,0], pts[2,0]], [pts[0,1], pts[2,1]], "--", color="#d95f02", lw=2)
    for label, point in zip(["x","y","z"], pts): ax.text(point[0], point[1]+0.15, label, ha="center", fontsize=12, fontweight="bold")
    ax.scatter([p[0], q[0]], [p[1], q[1]], s=55, color="#4d9221")
    ax.text(2.05, 1.05, "tested comparison chord", ha="center", fontsize=10)
def _norm(ax, unit):
    th = np.linspace(0, 2*math.pi, 400); ax.plot(np.cos(th), np.sin(th), color="#28587b", lw=2, label="l2")
    ax.plot([1,0,-1,0,1], [0,1,0,-1,0], color="#d95f02", lw=2, label="l1")
    ax.plot([1,-1,-1,1,1], [1,1,-1,-1,1], color="#1b9e77", lw=2, label="l infinity")
    ax.plot([-0.7,0.8], [-0.55,0.65], color="#4d9221", lw=3); ax.legend(frameon=False)
def _graph(ax, unit, directed=False):
    labels = unit["concepts"][:5]; G = nx.DiGraph() if directed else nx.Graph()
    for label in labels: G.add_node(label)
    for a, b in zip(labels, labels[1:]): G.add_edge(a, b)
    if len(labels) > 3: G.add_edge(labels[0], labels[3])
    pos = nx.spring_layout(G, seed=8)
    nx.draw_networkx_edges(G, pos, ax=ax, arrows=directed, edge_color="#666", width=1.5, arrowsize=15)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[PALETTE[i%len(PALETTE)] for i in range(len(labels))], node_size=1550, alpha=.9)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color="white")
def _complex(ax, unit):
    for sq, color in [(((0,0),(1,0),(1,1),(0,1)),"#eaf2f8"),(((1,0),(2,0),(2,1),(1,1)),"#fff4d6"),(((0,1),(1,1),(1,2),(0,2)),"#e8f5e9")]:
        xy = np.array(sq + (sq[0],)); ax.fill(xy[:,0], xy[:,1], color=color, ec="#28587b", lw=2)
    ax.scatter([1],[1], s=90, color="#d95f02")
    c = np.array([3.3,1]); a = np.linspace(0,2*math.pi,5)[:-1]; link = np.c_[c[0]+.75*np.cos(a), c[1]+.75*np.sin(a)]
    ax.plot(np.r_[link[:,0],link[0,0]], np.r_[link[:,1],link[0,1]], color="#4d9221", lw=2); ax.scatter(link[:,0], link[:,1], color="#4d9221")
    ax.text(3.3, -.08, "link loop >= 2*pi", ha="center", fontsize=10); ax.set_xlim(-.3,4.3); ax.set_ylim(-.3,2.4)
def _boundary(ax, unit):
    ax.add_patch(plt.Circle((0,0),1, fill=False, color="#28587b", lw=2))
    for ang, color in [(0.2,"#d95f02"),(.75,"#4d9221"),(2.2,"#7570b3")]:
        e = np.array([math.cos(ang), math.sin(ang)]); ax.arrow(0,0,.88*e[0],.88*e[1], head_width=.04, head_length=.06, color=color); ax.scatter([e[0]],[e[1]], color=color)
    for r in [.35,.55,.75]:
        th = np.linspace(-.9,.9,100); ax.plot(.85-r*(1-np.cos(th)), r*np.sin(th), color="#9aa6b2")
def _hyperbolic(ax, unit):
    ax.add_patch(plt.Circle((0,0),1, fill=False, color="#28587b", lw=2))
    th = np.linspace(.18,2.65,180); ax.plot(.1+.95*np.cos(th), -.4+.95*np.sin(th), color="#d95f02", lw=2.5)
    ax.plot([-.65,.72],[.55,-.35], color="#4d9221", lw=2.5); ax.plot([-.58,.58,0,-.58],[.45,.37,-.55,.45], "--", color="#7570b3")
def _projection(ax, unit):
    ax.plot([-2,2],[0,0], color="#28587b", lw=4); pts=np.array([[-1.4,1],[-.4,1.55],[.9,1.2],[1.5,.7]])
    ax.scatter(pts[:,0],pts[:,1], color="#d95f02"); [ax.plot([x,x],[y,0],"--",color="#9aa6b2") for x,y in pts]; ax.scatter(pts[:,0],np.zeros(len(pts)), color="#4d9221")
def _flat(ax, unit):
    for i in range(-3,4): ax.plot([-3,3],[i,i], color="#c6d4df"); ax.plot([i,i],[-3,3], color="#c6d4df")
    ax.arrow(0,0,1.8,0, head_width=.12, color="#d95f02"); ax.arrow(0,0,0,1.8, head_width=.12, color="#4d9221"); ax.fill([0,1.8,1.8,0],[0,0,1.8,1.8], color="#fff4d6", alpha=.7)
def _symmetric(ax, unit):
    for x in np.linspace(-2,2,5): ax.plot([x,x+1.2],[-1.2,1.2], color="#c6d4df"); ax.plot([x,x-1.2],[-1.2,1.2], color="#c6d4df")
    ax.fill([0,1.25,.62,0],[0,0,1.08,0], color="#fff4d6", ec="#d95f02", lw=2); ax.text(.62,.38,"Weyl chamber", ha="center")
def _patch(ax, unit):
    for i,c in enumerate([(-.8,0),(.2,.35),(1.15,-.05),(.35,-.65)]): ax.add_patch(plt.Circle(c,.78,color=PALETTE[i],alpha=.18,ec=PALETTE[i],lw=2))
    ax.plot([-.75,.05,1.05,.25,-.75],[0,.45,.05,-.55,0], color="#d95f02", lw=2.5)
def _gluing(ax, unit):
    ax.fill([-2,0,0,-2],[-1,-1,1,1], color="#eaf2f8", ec="#28587b", lw=2); ax.fill([0,2,2,0],[-1,-1,1,1], color="#fff4d6", ec="#d95f02", lw=2); ax.plot([0,0],[-1,1], color="#4d9221", lw=4)
def _cone(ax, unit):
    apex=np.array([0,1.4]); ax.plot([0,-1.5],[1.4,-1], color="#28587b", lw=2); ax.plot([0,1.5],[1.4,-1], color="#28587b", lw=2)
    th=np.linspace(math.pi,2*math.pi,120); ax.plot(1.5*np.cos(th), -1+.35*np.sin(th), color="#d95f02", lw=2)
def _curvature(ax, unit):
    x=np.linspace(-2,2,120); ax.plot(x,.35*x*x,color="#d95f02",lw=2.5,label="positive bend"); ax.plot(x,-.25*x*x+.9,color="#28587b",lw=2.5,label="negative bend"); ax.legend(frameon=False)
DRAW = {"triangle":_triangle,"model":_triangle,"cat":_triangle,"norm":_norm,"construction":_graph,"complex":_complex,"group":_graph,"boundary":_boundary,"hyperbolic":_hyperbolic,"projection":_projection,"flat":_flat,"symmetric":_symmetric,"category":lambda ax,u:_graph(ax,u,True),"patchwork":_patch,"gluing":_gluing,"cone":_cone,"curvature":_curvature}
def draw_unit_figure(unit: dict, path: Path) -> Path:
    fig, ax = plt.subplots(figsize=(8.8,5.6)); DRAW.get(unit["visual_family"], _triangle)(ax, unit)
    ax.set_title(f'{unit["number"]}: {unit["title"]}', fontsize=14, color="#1f2d3d"); ax.text(.5,.02,unit["focus"], transform=fig.transFigure, ha="center", fontsize=9); _finish(ax)
    path.parent.mkdir(parents=True, exist_ok=True); fig.savefig(path, dpi=160, bbox_inches="tight"); plt.close(fig); return path
def write_interactive_html(unit: dict, path: Path) -> Path:
    rows = "".join(f"<li><button data-index='{i}'>{html.escape(c)}</button></li>" for i,c in enumerate(unit["concepts"]))
    title = html.escape(f'{unit["number"]}: {unit["title"]}'); checks = html.escape(str(quick_check(unit["id"])))
    text = f"""<!doctype html><meta charset='utf-8'><title>{title}</title><style>body{{font-family:system-ui,sans-serif;margin:0;background:#fbfcfd;color:#1f2d3d}}main{{max-width:950px;margin:auto;padding:24px}}.stage{{display:grid;grid-template-columns:280px 1fr;gap:20px}}button{{width:100%;text-align:left;margin:4px 0;padding:8px;border:1px solid #c6d4df;background:white;border-radius:6px}}button.active{{background:#fff4d6;border-color:#d95f02}}.panel{{border:1px solid #c6d4df;background:white;border-radius:8px;padding:18px}}svg{{width:100%;height:220px}}</style><main><h1>{title}</h1><p>{html.escape(unit["focus"])}</p><div class='stage'><ol>{rows}</ol><div class='panel'><svg viewBox='0 0 600 220'><line x1='55' y1='165' x2='535' y2='55' stroke='#9aa6b2' stroke-width='5'/><circle id='dot' cx='55' cy='165' r='18' fill='#d95f02'/><text id='label' x='80' y='160' font-size='22'></text></svg><p id='explain'></p><details><summary>Recorded invariant check</summary><code>{checks}</code></details></div></div></main><script>const concepts={json.dumps(unit["concepts"])};const bs=[...document.querySelectorAll('button')],dot=document.querySelector('#dot'),label=document.querySelector('#label'),explain=document.querySelector('#explain');function sel(i){{bs.forEach((b,j)=>b.classList.toggle('active',i===j));let x=55+i*(480/Math.max(1,concepts.length-1)),y=165-i*(110/Math.max(1,concepts.length-1));dot.setAttribute('cx',x);dot.setAttribute('cy',y);label.setAttribute('x',Math.min(x+24,390));label.setAttribute('y',y+7);label.textContent=concepts[i];explain.textContent='Inspection target: connect '+concepts[i]+' to the saved invariant.'}}bs.forEach((b,i)=>b.onclick=()=>sel(i));sel(0);</script>"""
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding="utf-8"); return path
