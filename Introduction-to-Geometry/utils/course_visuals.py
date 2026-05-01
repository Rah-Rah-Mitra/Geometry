from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from .artifacts import artifact_path, ensure_chapter_artifact_dirs, write_csv, write_json
from .course import CHAPTERS, chapter_by_no
from .geometry2d import regular_polygon, rotate, triangle_centers
from .geometry3d import cube_vertices, project_3d, project_4d, tesseract_vertices
from .plotting import PALETTE, svg_escape
from .surfaces import saddle_grid
def _xy(p, scale=118, cx=380, cy=260): return (cx+scale*float(p[0]), cy-scale*float(p[1]))
def _line(a,b,color,width=2,dash=""):
    x1,y1=_xy(a); x2,y2=_xy(b); d=f' stroke-dasharray="{dash}"' if dash else ""; return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"{d}/>'
def _circle(c,r,color,fill="none",width=2):
    x,y=_xy(c); return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{118*r:.1f}" fill="{fill}" stroke="{color}" stroke-width="{width}"/>'
def _poly(points,color,fill="none",width=2):
    pts=" ".join(f"{_xy(p)[0]:.1f},{_xy(p)[1]:.1f}" for p in points); return f'<polyline points="{pts}" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"/>'
def _dot(p,color,label="",r=5):
    x,y=_xy(p); text=f'<text x="{x+7:.1f}" y="{y-7:.1f}" font-size="13" fill="{PALETTE["ink"]}">{svg_escape(label)}</text>' if label else ""; return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>'+text
def _svg(title,subtitle,elements):
    body="\n".join(elements); return f'<svg xmlns="http://www.w3.org/2000/svg" width="760" height="520" viewBox="0 0 760 520"><rect width="760" height="520" fill="#fffdf7"/><text x="28" y="38" font-size="24" font-family="DejaVu Sans, Arial" font-weight="700" fill="{PALETTE["ink"]}">{svg_escape(title)}</text><text x="28" y="64" font-size="14" font-family="DejaVu Sans, Arial" fill="{PALETTE["ink"]}">{svg_escape(subtitle[:110])}</text><g font-family="DejaVu Sans, Arial">{body}</g></svg>'
def _concept(ch):
    no=ch["no"]; mode=no%8; e=[]
    if mode==1:
        tri=np.array([[-1.55,-0.75],[1.55,-0.45],[0.15,1.35]]); centers=triangle_centers(*tri); e.append(_poly(np.vstack([tri,tri[0]]),PALETTE["blue"],"#dbeafe",3)); [e.append(_dot(p,PALETTE["blue"],lab)) for p,lab in zip(tri,["A","B","C"])] ; e.append(_dot(centers["centroid"],PALETTE["red"],"centroid",7)); [e.append(_dot(m,PALETTE["gold"],"mid",4)) for m in centers["side_midpoints"]]
    elif mode==2:
        n=5+(no%5); pts=regular_polygon(n,1.45,math.pi/2); e += [_circle((0,0),1.45,PALETTE["grid"],width=1), _poly(np.vstack([pts,pts[0]]),PALETTE["orange"],"none",3)]; star=pts[[2*i % n for i in range(n+1)]]; e.append(_poly(star,PALETTE["violet"],"none",2))
    elif mode==3:
        base=np.array([[-1.3,-0.35],[-0.3,-0.25],[-0.65,0.55]]); [e.append(_poly(np.vstack([rotate(base,0.25*k)+np.array([0.58*k,0.08*k]), rotate(base,0.25*k)[0]+np.array([0.58*k,0.08*k])]), PALETTE["red" if k==4 else "blue"],"none",2)) for k in range(5)]
    elif mode==4:
        a=np.array([0.55,0.0]); b=np.array([0.25,0.45]); [e.append(_dot(i*a+j*b,PALETTE["blue"],"",2.8)) for i in range(-4,5) for j in range(-3,4)]; cell=np.array([[0,0],a,a+b,b,[0,0]]); e.append(_poly(cell,PALETTE["red"],"#fee2e2",3))
    elif mode==5:
        pts=regular_polygon(3,0.62,math.pi/2)+np.array([-0.8,0.05]); center=np.array([0.45,-0.2]); colors=[PALETTE["blue"],PALETTE["green"],PALETTE["orange"],PALETTE["red"]]; [e.append(_poly(np.vstack([center+s*(pts-center), center+s*(pts[0]-center)]), colors[k],"none",2)) for k,s in enumerate([0.7,1.0,1.35,1.8])]; e.append(_dot(center,PALETTE["red"],"fixed"))
    elif mode==6:
        [e.append(_circle((0,0),r,PALETTE["blue" if r<=1 else "orange"],width=2)) for r in [0.45,0.7,1.0,1.55]]; e.append(_line((-1.8,0.4),(1.8,0.4),PALETTE["green"],2,"6 5"))
    elif mode==7:
        verts=project_3d(cube_vertices()); raw=cube_vertices(); [e.append(_dot(p,PALETTE["orange"],"",4)) for p in verts]; [e.append(_line(verts[i],verts[j],PALETTE["blue"],1.5)) for i,a in enumerate(raw) for j,b in enumerate(raw) if i<j and np.sum(np.abs(a-b)>1e-9)==1]
    else:
        t=np.linspace(0,5*math.pi,120); r=np.linspace(0.1,1.55,120); pts=np.column_stack([r*np.cos(t),r*np.sin(t)]); e.append(_poly(pts,PALETTE["orange"],"none",3)); [e.append(_dot(p,PALETTE["blue"],"",3)) for p in pts[::18]]
    return _svg(f"Chapter {no:02d}: {ch['title']}", ch["visual"], e)
def _experiment(ch):
    no=ch["no"]; e=[]
    if no in {16,20}:
        e.append(_circle((0,0),1.55,PALETTE["ink"],width=2));
        for c,r in [((0,1.9),1.45),((0,-1.9),1.45),((1.8,0),1.25),((-1.8,0),1.25)]:
            pts=np.array([[c[0]+r*math.cos(t),c[1]+r*math.sin(t)] for t in np.linspace(0,2*math.pi,180)]); pts=pts[np.linalg.norm(pts,axis=1)<1.57];
            if len(pts)>1: e.append(_poly(pts,PALETTE["green"],"none",2))
    elif no in {17,19}:
        X,Y,Z=saddle_grid(13); [e.append(_poly(np.column_stack([X[i],Y[i]+0.2*Z[i]])*0.7,PALETTE["blue"],"none",1)) for i in range(X.shape[0])]; [e.append(_poly(np.column_stack([X[:,j],Y[:,j]+0.2*Z[:,j]])*0.7,PALETTE["orange"],"none",1)) for j in range(X.shape[1])]
    elif no==22:
        raw=tesseract_vertices(); pts2=project_3d(project_4d(raw))*0.75; [e.append(_line(pts2[i],pts2[j],PALETTE["violet"],1.2)) for i,a in enumerate(raw) for j,b in enumerate(raw) if i<j and np.sum(np.abs(a-b)>1e-9)==1]; [e.append(_dot(p,PALETTE["red"],"",3.5)) for p in pts2]
    elif no==21:
        for k,(name,chi) in enumerate([("sphere",2),("torus",0),("projective",1)]):
            x=220+k*150; h=45+30*chi; e.append(f'<rect x="{x}" y="{360-h}" width="76" height="{h}" fill="{[PALETTE["blue"],PALETTE["orange"],PALETTE["green"]][k]}" opacity="0.75"/><text x="{x-10}" y="385" font-size="13">{name}</text>')
    else:
        x=np.linspace(-1.8,1.8,140); colors=[PALETTE["blue"],PALETTE["orange"],PALETTE["green"]]
        for k,phase in enumerate([0,0.65,1.3]): e.append(_poly(np.column_stack([x,0.45*np.sin((1+0.1*no)*x+phase)+0.35*(k-1)]),colors[k],"none",2))
        e.append(_line((-1.8,0),(1.8,0),PALETTE["grid"],1,"4 4"))
    return _svg(f"Chapter {no:02d} experiment", "Perturb the model and inspect what remains invariant", e)
def render_chapter_visuals(chapter_no: int, root: str | Path | None = None) -> dict:
    root=Path(root) if root is not None else Path.cwd(); ch=chapter_by_no(chapter_no); ensure_chapter_artifact_dirs(chapter_no, root); fig1=artifact_path(chapter_no,"figures","concept_configuration.svg",root); fig2=artifact_path(chapter_no,"figures","parameter_experiment.svg",root); fig1.write_text(_concept(ch),encoding="utf-8"); fig2.write_text(_experiment(ch),encoding="utf-8"); write_csv(artifact_path(chapter_no,"tables","artifact_manifest.csv",root),[{"artifact":fig1.name,"role":"configuration"},{"artifact":fig2.name,"role":"experiment"}]); payload={"chapter":chapter_no,"title":ch["title"],"figures":[str(fig1.relative_to(root)),str(fig2.relative_to(root))],"checks":{"figure_count":2,"printed_pages":ch["printed"],"pdf_pages":ch["pdf"]}}; check=artifact_path(chapter_no,"checks","visual_summary.json",root); write_json(check,payload); payload["check_path"]=str(check.relative_to(root)); return payload
def render_all(root: str | Path | None = None) -> list[dict]:
    root=Path(root) if root is not None else Path.cwd(); return [render_chapter_visuals(ch["no"], root) for ch in CHAPTERS]
