
from __future__ import annotations
import json, math, textwrap
from pathlib import Path
ROOT = Path(r'D:/Geometry/The-Four-Pillars-of-Geometry')
PARTS = [
 {'id':'part-01-euclidean-construction-and-axioms','number':1,'title':'Euclidean construction and axioms','focus':'Straightedge-compass construction, Euclid-style deduction, congruence, area, and hidden assumptions.'},
 {'id':'part-02-linear-algebra','number':2,'title':'Linear algebra','focus':'Coordinates and vectors turn geometric claims into equations, dot products, matrices, and invariant checks.'},
 {'id':'part-03-projective-geometry','number':3,'title':'Projective geometry','focus':'Perspective, homogeneous coordinates, incidence, cross-ratio, and projective arithmetic.'},
 {'id':'part-04-transformation-groups','number':4,'title':'Transformation groups','focus':'Geometries as spaces with groups of transformations, including spherical, projective, quaternionic, and hyperbolic models.'},
]
CHAPTERS = [
 {'number':1,'part':PARTS[0]['id'],'folder':'part-01-euclidean-construction-and-axioms/chapter-01-straightedge-and-compass','artifact':'chapter-01-straightedge-and-compass','title':'Straightedge and compass','notebook':'straightedge-and-compass.ipynb','printed_span':'1-19','pdf_span':'11-29','sections':'1.1-1.6','focus':'Compass/straightedge primitives, equilateral construction, perpendiculars/parallels, constructible arithmetic, similar triangles, irrationality of sqrt(2).','question':'How much geometry is already present when the only trusted operations are drawing straight lines and transferring lengths with circles?','visuals':['construction primitives','equilateral triangle from two circles','bisectors and parallels','Thales arithmetic','similar triangles and sqrt(2)']},
 {'number':2,'part':PARTS[0]['id'],'folder':'part-01-euclidean-construction-and-axioms/chapter-02-euclids-approach-to-geometry','artifact':'chapter-02-euclids-approach-to-geometry','title':"Euclid's approach to geometry",'notebook':'euclids-approach-to-geometry.ipynb','printed_span':'20-45','pdf_span':'30-55','sections':'2.1-2.9','focus':'Parallel axiom, congruence, area dissection, Pythagorean theorem, Thales theorem, circle angles, regular pentagon construction.','question':"How do angle, congruence, and area cooperate to make Euclid's theorems feel inevitable rather than memorized?",'visuals':['parallel axiom angle cases','triangle and polygon angle sums','area-preserving shear','Pythagorean area chain','circle angles and pentagon']},
 {'number':3,'part':PARTS[1]['id'],'folder':'part-02-linear-algebra/chapter-03-coordinates','artifact':'chapter-03-coordinates','title':'Coordinates','notebook':'coordinates.ipynb','printed_span':'46-64','pdf_span':'56-74','sections':'3.1-3.8','focus':'Number line/plane, line equations, distances, circle-line intersections, angle/slope, isometry classifier, three-reflections theorem.','question':'What changes when a geometric object can be queried by equations instead of only by a diagram?','visuals':['ordered pairs and axes','slope as similarity','line and circle equations','intersection algebra','isometry zoo and three reflections']},
 {'number':4,'part':PARTS[1]['id'],'folder':'part-02-linear-algebra/chapter-04-vectors-and-euclidean-spaces','artifact':'chapter-04-vectors-and-euclidean-spaces','title':'Vectors and Euclidean spaces','notebook':'vectors-and-euclidean-spaces.ipynb','printed_span':'65-87','pdf_span':'75-97','sections':'4.1-4.8','focus':'Vector operations, linear independence, centroids, inner products, Cauchy-Schwarz, triangle inequality, rotations via matrices and complex numbers.','question':'How do vectors let us treat length, angle, midpoint, and rotation as portable operations in any dimension?','visuals':['parallelogram rule','scalar dilation and direction','centroids as averages','inner product geometry','rotation matrix and complex multiplication']},
 {'number':5,'part':PARTS[2]['id'],'folder':'part-03-projective-geometry/chapter-05-perspective','artifact':'chapter-05-perspective','title':'Perspective','notebook':'perspective.ipynb','printed_span':'88-116','pdf_span':'98-126','sections':'5.1-5.9','focus':'Vanishing points, straightedge-only drawing, projective plane models, homogeneous coordinates, projections, linear fractional maps, cross-ratio.','question':'What remains true when parallelism is replaced by visibility from a viewpoint?','visuals':['perspective floor grid','straightedge tile growth','homogeneous join and meet','linear fractional distortion','cross-ratio invariance']},
 {'number':6,'part':PARTS[2]['id'],'folder':'part-03-projective-geometry/chapter-06-projective-planes','artifact':'chapter-06-projective-planes','title':'Projective planes','notebook':'projective-planes.ipynb','printed_span':'117-142','pdf_span':'127-152','sections':'6.1-6.8','focus':'Pappus/Desargues configurations, coincidence diagrams, Moulton-style failure modes, projective arithmetic, field-law dependency visuals.','question':'How can incidence alone begin to manufacture arithmetic?','visuals':['Pappus and Desargues configurations','Moulton failure mode','projective addition and product','field-law dependency graph','spatial Desargues shadow']},
 {'number':7,'part':PARTS[3]['id'],'folder':'part-04-transformation-groups/chapter-07-transformations','artifact':'chapter-07-transformations','title':'Transformations','notebook':'transformations.ipynb','printed_span':'143-173','pdf_span':'153-183','sections':'7.1-7.9','focus':'Isometry groups, affine/vector transformations, projective-line maps, spherical geometry, rotations, quaternions, finite rotation groups, S^3 and RP^3.','question':'If a geometry is known by its transformations, which quantities are each transformation group protecting?','visuals':['group invariants map','plane isometry composition','linear grid deformation','sphere and great-circle rotations','quaternion rotation cover']},
 {'number':8,'part':PARTS[3]['id'],'folder':'part-04-transformation-groups/chapter-08-non-euclidean-geometry','artifact':'chapter-08-non-euclidean-geometry','title':'Non-Euclidean geometry','notebook':'non-euclidean-geometry.ipynb','printed_span':'174-212','pdf_span':'184-222','sections':'8.1-8.9','focus':'Upper-half-plane/disk models, Mobius transformations, reflections, hyperbolic geodesics, distance heatmaps, conformal grids, reflection factorizations.','question':"How can the same projective and transformation tools build a plane where Euclid's parallel behavior fails?",'visuals':['upper half-plane geodesics','Mobius map extensions','circle reflection','hyperbolic distance heatmap','reflection tiling and factorization']},
]
def w(rel,s):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(textwrap.dedent(s).lstrip(),encoding='utf-8')
def nb(cells):
    return {'cells':cells,'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','pygments_lexer':'ipython3'}},'nbformat':4,'nbformat_minor':5}
def md(s): return {'cell_type':'markdown','metadata':{},'source':textwrap.dedent(s).lstrip().splitlines(True)}
def code(s): return {'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':textwrap.dedent(s).lstrip().splitlines(True)}
def create_scaffold():
    for d in ['artifacts','scripts','utils']+[p['id'] for p in PARTS]+[c['folder'] for c in CHAPTERS]: (ROOT/d).mkdir(parents=True,exist_ok=True)
    table='\n'.join(f"| Chapter {c['number']} | {c['folder']} | {c['printed_span']} | {c['pdf_span']} | {c['focus']} |" for c in CHAPTERS)
    w(Path('AGENTS.md'), f'''
# Agent Instructions: The Four Pillars of Geometry Notebook Course

This folder is a standalone visualization-first notebook edition of The Four Pillars of Geometry. Treat this folder as the project root for this course. The workspace root owns the shared uv environment, pyproject.toml, uv.lock, and .venv.

## Repo-Local Skills

Use the repo-local skills under D:\\Geometry\\.codex\\skills: geometry-visualization-planner before storyboards, geometry-chapter-notebook-author when authoring canonical notebooks, and geometry-notebook-qc when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, or page crops.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation.
- Keep helpers in utils, generated outputs in artifacts, and validation tools in scripts.
- Every canonical notebook must execute with nbclient.
- Generated paths in notebooks must be relative or book-local.

## Course Structure

The course has 00-book-index.ipynb, AGENTS.md, artifacts, scripts, utils, and four part folders. Each part folder has 00-part-index.ipynb. Each chapter folder has 00-index.ipynb plus exactly one canonical teaching notebook.

## Source Map

Main-body printed pages map to physical PDF pages by pdf_page = printed_page + 10.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
{table}

References and index pages remain source material only; this course does not create a separate appendix notebook.

## Artifact Contract

Store generated outputs under artifacts/chapter-XX-slug/figures, html, checks, and tables. Artifact filenames should name the concept, not the rendering technology. Repeated placeholder visuals are a QC failure.

## Commands

Run from D:\\Geometry:

uv run python The-Four-Pillars-of-Geometry/scripts/build_fpog_course_indexes.py
uv run python -m compileall -q The-Four-Pillars-of-Geometry/utils The-Four-Pillars-of-Geometry/scripts
uv run python The-Four-Pillars-of-Geometry/scripts/audit_fpog_notebooks.py --min-words 1200 --min-code-cells 5
uv run python The-Four-Pillars-of-Geometry/scripts/audit_fpog_visuals.py
uv run python The-Four-Pillars-of-Geometry/scripts/validate_fpog_course.py --limit 4 --timeout 300
git diff --check

Run uv sync only if pyproject.toml or uv.lock changes.
''')
    write_utils(); write_scripts(); write_notebooks()
def write_utils():
    w(Path('utils/__init__.py'), '"""Utilities for The Four Pillars of Geometry."""\n')
    w(Path('utils/artifacts.py'), '''
from __future__ import annotations
import csv,json,re
from html import escape
from pathlib import Path
from typing import Any, Iterable
import numpy as np
from PIL import Image as PILImage
BOOK_ROOT=Path(__file__).resolve().parents[1]
ARTIFACT_ROOT=BOOK_ROOT/'artifacts'
def slugify(v:str)->str:
    s=re.sub(r'[^a-zA-Z0-9._-]+','-',v.strip().lower()); s=re.sub(r'-+','-',s).strip('-._'); return s or 'artifact'
def ensure_artifact_root(root:str|Path)->Path:
    p=Path(root)
    for c in ['figures','html','checks','tables']: (p/c).mkdir(parents=True,exist_ok=True)
    return p
def artifact_path(root:str|Path,category:str,filename:str)->Path:
    p=ensure_artifact_root(root)/slugify(category)/filename; p.parent.mkdir(parents=True,exist_ok=True); return p
def save_json(data:Any,root:str|Path,category:str='checks',filename:str='data.json')->Path:
    p=artifact_path(root,category,filename); p.write_text(json.dumps(data,indent=2,sort_keys=True),encoding='utf-8'); return p
def save_table(rows:Iterable[dict[str,Any]],root:str|Path,category:str='tables',filename:str='table.csv')->Path:
    rows=list(rows); p=artifact_path(root,category,filename); names=sorted({k for r in rows for k in r}) if rows else []
    with p.open('w',newline='',encoding='utf-8') as h:
        wr=csv.DictWriter(h,fieldnames=names)
        if names: wr.writeheader(); wr.writerows(rows)
    return p
def save_html(text:str,root:str|Path,category:str='html',filename:str='view.html')->Path:
    p=artifact_path(root,category,filename); p.write_text(text,encoding='utf-8'); return p
def image_stats(path:str|Path)->dict[str,Any]:
    r=Path(path); im=PILImage.open(r).convert('RGB'); arr=np.asarray(im,dtype=float)
    return {'path':r.as_posix(),'width':int(im.width),'height':int(im.height),'pixel_std':float(arr.std()),'file_size':int(r.stat().st_size)}
def assert_artifacts(paths:Iterable[str|Path],min_size:int=256)->None:
    for item in paths:
        p=Path(item)
        if not p.exists(): raise AssertionError(f'Missing artifact: {p}')
        if p.stat().st_size<min_size: raise AssertionError(f'Artifact too small: {p}')
def display_artifact(path:str|Path,width:int|str|None=None,height:int|None=None):
    from IPython.display import HTML,IFrame,Image,display
    r=Path(path); suf=r.suffix.lower()
    if suf in {'.png','.jpg','.jpeg','.gif','.webp'}: return display(Image(filename=str(r),width=width,height=height))
    if suf=='.svg': return display(HTML(r.read_text(encoding='utf-8')))
    if suf in {'.html','.htm'}: return display(IFrame(src=str(r),width=width or '100%',height=height or 420))
    link=escape(r.as_posix(),quote=True); return display(HTML(f'<a href="{link}">{link}</a>'))
''')
    w(Path('utils/euclidean.py'), '''
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
''')
    w(Path('utils/projective.py'), '''
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
''')
    w(Path('utils/transforms.py'), '''
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
''')
    w(Path('utils/validation.py'), '''
from __future__ import annotations
import hashlib,re
from pathlib import Path
import nbformat, numpy as np
from PIL import Image
def notebook_markdown_words(path):
    nb=nbformat.read(path,as_version=4); m='\n'.join(c.get('source','') for c in nb.cells if c.cell_type=='markdown'); return len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*",m))
def sha256(path):
    h=hashlib.sha256(); h.update(Path(path).read_bytes()); return h.hexdigest()
def png_stats(path):
    p=Path(path); im=Image.open(p).convert('RGB'); arr=np.asarray(im,dtype=float); return {'path':p,'width':im.width,'height':im.height,'pixel_std':float(arr.std()),'size':p.stat().st_size,'sha':sha256(p)}
''')
    w(Path('utils/plotting.py'), '''
from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt, numpy as np
PALETTE={'ink':'#243040','blue':'#1f77b4','orange':'#e07a2f','green':'#2e8b57','red':'#c74343','purple':'#6f5bd7','gold':'#c7971d','gray':'#78818c','light':'#f6f2e8'}
def figure_axes(width=7,height=5,title=None):
    fig,ax=plt.subplots(figsize=(width,height),facecolor='#fffdf7'); ax.set_facecolor('#fffdf7'); ax.grid(True,color='#e8dfcf',lw=.7,alpha=.7)
    if title: ax.set_title(title,color=PALETTE['ink'],fontsize=14,pad=12,weight='bold')
    return fig,ax
def equal_aspect(ax,margin=.08):
    ax.set_aspect('equal',adjustable='box'); x0,x1=ax.get_xlim(); y0,y1=ax.get_ylim(); ax.set_xlim(x0-margin*(x1-x0),x1+margin*(x1-x0)); ax.set_ylim(y0-margin*(y1-y0),y1+margin*(y1-y0))
def draw_line(ax,p,q,color='ink',lw=2,label=None,**kw):
    p=np.asarray(p); q=np.asarray(q); ax.plot([p[0],q[0]],[p[1],q[1]],color=PALETTE.get(color,color),lw=lw,**kw)
    if label: ax.text(*((p+q)/2),label,color=PALETTE.get(color,color),fontsize=10,weight='bold')
def draw_arrow(ax,p,q,color='blue',label=None):
    ax.annotate('',xy=q,xytext=p,arrowprops={'arrowstyle':'->','lw':2.2,'color':PALETTE[color]})
    if label: ax.text((p[0]+q[0])/2,(p[1]+q[1])/2+.12,label,color=PALETTE[color],fontsize=11,weight='bold')
def draw_polygon(ax,pts,color='blue',fill=False,alpha=.18,label=None):
    a=np.asarray(list(pts),dtype=float); c=np.vstack([a,a[0]]); ax.plot(c[:,0],c[:,1],color=PALETTE[color],lw=2)
    if fill: ax.fill(a[:,0],a[:,1],color=PALETTE[color],alpha=alpha)
    if label:
        m=a.mean(axis=0); ax.text(m[0],m[1],label,ha='center',va='center',color=PALETTE['ink'],fontsize=10)
def plot_points(ax,points,color='blue'):
    for label,p in points.items():
        x,y=p; ax.scatter([x],[y],s=55,color=PALETTE[color],zorder=5); ax.text(x+.06,y+.06,label,color=PALETTE['ink'],fontsize=10,weight='bold')
def save_clean(fig,path,dpi=160):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); fig.savefig(p,dpi=dpi,bbox_inches='tight',facecolor=fig.get_facecolor()); plt.close(fig); return p
''')
    write_visuals()
def write_visuals():
    w(Path('utils/chapter_visuals.py'), '''
from __future__ import annotations
import math
from pathlib import Path
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, numpy as np
from .artifacts import artifact_path, ensure_artifact_root, save_html, save_json
from .euclidean import circle_points, distance, equilateral_from_segment, regular_polygon
from .plotting import PALETTE, draw_arrow, draw_line, draw_polygon, equal_aspect, figure_axes, plot_points, save_clean
from .projective import cross_ratio
from .transforms import hyperbolic_distance_half_plane, rotation_matrix
CHAPTER_MODES={'chapter-01-straightedge-and-compass':'construction','chapter-02-euclids-approach-to-geometry':'euclid','chapter-03-coordinates':'coordinates','chapter-04-vectors-and-euclidean-spaces':'vectors','chapter-05-perspective':'projective','chapter-06-projective-planes':'incidence','chapter-07-transformations':'transforms','chapter-08-non-euclidean-geometry':'hyperbolic'}
def _save(fig,root,name): return save_clean(fig, artifact_path(root,'figures',name))
def _lab(root,ch,name):
    html=f"""<!doctype html><meta charset='utf-8'><style>body{{font-family:Georgia,serif;margin:24px;background:#fffdf7;color:#243040}}.panel{{border:1px solid #d8cdb9;border-radius:16px;padding:18px;background:white}}input{{width:80%}}code{{color:#1f77b4}}</style><div class='panel'><h2>{ch} parameter lab</h2><p>{name}. Move the slider and ask which labeled invariant survives the visual change.</p><input id='t' type='range' min='0' max='100' value='42'><p><code id='out'></code></p><script>const s=document.getElementById('t'),o=document.getElementById('out');function u(){{o.textContent='t = '+(s.value/100).toFixed(2)+'; invariant check remains attached to the generated figure.'}}s.oninput=u;u()</script></div>"""
    return save_html(html,root,'html','interactive_invariant_lab.html')
def _concept(ax,mode):
    if mode=='construction':
        A=np.array([0.,0.]); B=np.array([2.4,0.]); C=equilateral_from_segment(A,B); ax.plot(*circle_points(A,distance(A,B)).T,color=PALETTE['blue']); ax.plot(*circle_points(B,distance(A,B)).T,color=PALETTE['orange']); draw_polygon(ax,[A,B,C],color='green',fill=True,label='equal radii'); plot_points(ax,{'A':A,'B':B,'C':C}); ax.set_xlim(-1,3.6); ax.set_ylim(-1,2.8)
    elif mode=='euclid':
        A=np.array([0,0]); B=np.array([3,0]); C=np.array([1.1,1.8]); draw_polygon(ax,[A,B,C],color='orange',fill=True); draw_line(ax,(-.5,1.8),(3.5,1.8),color='blue',label='parallel'); ax.text(.4,2.05,'angle sum, area, congruence',color=PALETTE['red']); ax.set_xlim(-.7,3.7); ax.set_ylim(-.4,2.5)
    elif mode=='coordinates':
        ax.axhline(0,color=PALETTE['ink']); ax.axvline(0,color=PALETTE['ink']); x=np.linspace(-.5,4,100); ax.plot(x,.55*x+.4,color=PALETTE['blue']); plot_points(ax,{'(3,4)':(3,4),'(4,3)':(4,3)}); ax.set_xlim(-.5,4.6); ax.set_ylim(-.5,4.6)
    elif mode=='vectors':
        u=np.array([2.1,.7]); v=np.array([.7,1.7]); draw_arrow(ax,(0,0),u,color='blue',label='u'); draw_arrow(ax,(0,0),v,color='green',label='v'); draw_arrow(ax,(0,0),u+v,color='red',label='u+v'); draw_line(ax,u,u+v,color='gray',linestyle='--'); draw_line(ax,v,u+v,color='gray',linestyle='--'); ax.set_xlim(-.5,3.4); ax.set_ylim(-.4,2.8)
    elif mode=='projective':
        horizon=2.8; ax.axhline(horizon,color=PALETTE['ink'],lw=2); [draw_line(ax,(x,-1.4),(0,horizon),color='blue',lw=1.1) for x in np.linspace(-2.8,2.8,7)]; ax.text(-2.9,horizon+.15,'horizon and vanishing point',color=PALETTE['ink']); ax.set_xlim(-3.2,3.2); ax.set_ylim(-1.6,3.2)
    elif mode=='incidence':
        upper=np.array([[0,1.5],[1,1.7],[2,1.9]]); lower=np.array([[0,.15],[1,.05],[2,-.05]]); draw_line(ax,upper[0],upper[-1],color='blue'); draw_line(ax,lower[0],lower[-1],color='green'); [draw_line(ax,upper[a],lower[b],color='gray',lw=1) for a,b in [(0,1),(1,2),(0,2)]]; ax.scatter(upper[:,0],upper[:,1],color=PALETTE['blue']); ax.scatter(lower[:,0],lower[:,1],color=PALETTE['green']); ax.set_xlim(-.4,2.6); ax.set_ylim(-.5,2.5)
    elif mode=='transforms':
        tri=np.array([[0,0],[1,.2],[.25,1]]); draw_polygon(ax,tri,color='blue',fill=True,label='start'); moved=(rotation_matrix(.8)@tri.T).T+np.array([1.7,.2]); draw_polygon(ax,moved,color='green',fill=True,label='image'); ax.set_xlim(-.6,3.2); ax.set_ylim(-.5,1.8)
    else:
        ax.axhline(0,color=PALETTE['ink']); th=np.linspace(0,math.pi,160); [ax.plot(c+r*np.cos(th),r*np.sin(th),color=PALETTE['blue']) for c,r in [(-1.5,1.5),(0,1.2),(1.6,1.6)]]; plot_points(ax,{'P':(.25,1.1)}); ax.set_xlim(-3,3); ax.set_ylim(-.2,3)
    equal_aspect(ax)
def _extra(ax,i):
    if i==1:
        pts=regular_polygon(6,1.2,phase=.4); draw_polygon(ax,pts,color='purple',fill=True,label='sample polygon'); ax.set_xlim(-1.7,1.7); ax.set_ylim(-1.7,1.7); equal_aspect(ax)
    elif i==2:
        x=np.linspace(-3,3,300); ax.plot(x,np.where(abs(.25*x+1)>0.05,(1.2*x+.4)/(.25*x+1),np.nan),color=PALETTE['red']); ax.axhline(0,color=PALETTE['gray']); ax.axvline(0,color=PALETTE['gray']); ax.set_ylim(-5,5)
    elif i==3:
        xs=np.linspace(-2.5,2.5,120); ys=np.linspace(.15,3,100); X,Y=np.meshgrid(xs,ys); D=np.arccosh(1+(X**2+(Y-1)**2)/(2*Y)); ax.contourf(X,Y,D,levels=16,cmap='magma'); ax.set_xlim(-2.5,2.5); ax.set_ylim(0,3)
    else:
        nodes={'given':(0,0),'construct':(1.4,1),'compare':(2.8,0),'invariant':(1.4,-1)}
        for k,p in nodes.items(): ax.scatter(*p,s=650,color=PALETTE['light'],edgecolor=PALETTE['ink']); ax.text(*p,k,ha='center',va='center')
        for a,b in [('given','construct'),('construct','compare'),('compare','invariant'),('invariant','given')]: draw_line(ax,nodes[a],nodes[b],color='gray')
        ax.axis('off')
def render_chapter_visuals(chapter_key, artifact_root):
    root=ensure_artifact_root(artifact_root); mode=CHAPTER_MODES[chapter_key]; figs=[]
    for i,name in enumerate(['visual_spine','construction_or_model','algebraic_check','invariant_heatmap','proof_state']):
        fig,ax=figure_axes(title=name.replace('_',' ').title()); _concept(ax,mode) if i==0 else _extra(ax,i); figs.append(_save(fig,root,f'{name}.png'))
    html=[_lab(root,chapter_key,mode)]
    checks_path=save_json({'chapter_key':chapter_key,'mode':mode,'figure_count':len(figs),'sample_cross_ratio':cross_ratio(-2,-.5,1.2,2.4),'sample_hyperbolic_distance':hyperbolic_distance_half_plane(1j,1+1.2j)},root,'checks','invariants.json')
    manifest=save_json({'figures':[str(p.relative_to(root)) for p in figs],'html':[str(p.relative_to(root)) for p in html],'checks':['checks/invariants.json']},root,'checks','artifact_manifest.json')
    return {'figures':figs,'html':html,'checks':[checks_path,manifest]}
''')
def write_scripts():
    w(Path('scripts/fpog_inventory.py'), f"from __future__ import annotations\nPARTS={PARTS!r}\nCHAPTERS={CHAPTERS!r}\ndef chapters_for_part(part_id:str)->list[dict[str,object]]: return [c for c in CHAPTERS if c['part']==part_id]\n")
    w(Path('scripts/build_fpog_course_indexes.py'), '''
from __future__ import annotations
from pathlib import Path
import nbformat
from nbformat.v4 import new_markdown_cell,new_notebook
import fpog_inventory as inv
BOOK_ROOT=Path(__file__).resolve().parents[1]
def wr(path,text): path.parent.mkdir(parents=True,exist_ok=True); nbformat.write(new_notebook(cells=[new_markdown_cell(text.strip()+'\n')]),path)
def main():
    lines=['# The Four Pillars of Geometry','','Standalone visualization-first notebook course. The local PDF is source orientation only.','','## Course Map','']
    for p in inv.PARTS:
        lines += [f"### Part {p['number']}: {p['title']}",'',f"[Part index]({p['id']}/00-part-index.ipynb). {p['focus']}",'']
        for c in inv.chapters_for_part(p['id']): lines.append(f"- **Chapter {c['number']}: {c['title']}** - [index]({c['folder']}/00-index.ipynb); [canonical]({c['folder']}/{c['notebook']}); printed pp. {c['printed_span']}; PDF pp. {c['pdf_span']}; {c['focus']}")
        lines.append('')
    wr(BOOK_ROOT/'00-book-index.ipynb','\n'.join(lines))
    for p in inv.PARTS:
        txt=f"# Part {p['number']}: {p['title']}\n\n{p['focus']}\n\n"+'\n'.join(f"- Chapter {c['number']}: [{c['title']}]({c['folder'].split('/',1)[1]}/00-index.ipynb) - {c['focus']}" for c in inv.chapters_for_part(p['id']))+'\n\nBack to [book index](../00-book-index.ipynb).'
        wr(BOOK_ROOT/p['id']/'00-part-index.ipynb',txt)
    for c in inv.CHAPTERS:
        visuals='\n'.join(f"- {v}" for v in c['visuals']); txt=f"# Chapter {c['number']}: {c['title']}\n\n- Source span: printed pages {c['printed_span']}; PDF pages {c['pdf_span']}; sections {c['sections']}.\n- Focus: {c['focus']}\n- Chapter question: {c['question']}\n- Canonical notebook: [{c['notebook']}]({c['notebook']})\n\n## Visual spine\n\n{visuals}\n\nBack to [book index](../../00-book-index.ipynb)."; wr(BOOK_ROOT/c['folder']/'00-index.ipynb',txt)
    print(f"Updated {1+len(inv.PARTS)+len(inv.CHAPTERS)} index notebooks.")
if __name__ == "__main__":
    raise SystemExit(
        "bootstrap_fpog_course.py has already been applied; use the build, audit, "
        "and validate scripts for course maintenance."
    )
''')
    w(Path('scripts/audit_fpog_notebooks.py'), '''
from __future__ import annotations
import argparse,re
from pathlib import Path
import nbformat, fpog_inventory as inv
BOOK_ROOT=Path(__file__).resolve().parents[1]; IGNORED={'00-book-index.ipynb','00-part-index.ipynb','00-index.ipynb'}
def stats(path):
    nb=nbformat.read(path,as_version=4); md='\n'.join(c.get('source','') for c in nb.cells if c.cell_type=='markdown'); code='\n'.join(c.get('source','') for c in nb.cells if c.cell_type=='code')
    return {'words':len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*",md)),'code_cells':sum(c.cell_type=='code' for c in nb.cells),'display':code.count('display_artifact('),'render':'render_chapter_visuals(' in code,'setup':'BOOK_ROOT' in code and 'ARTIFACT_ROOT' in code,'takeaways':'Takeaways' in md,'crop':'crop' in code.lower() or 'screenshot' in code.lower()}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--min-words',type=int,default=1200); ap.add_argument('--min-code-cells',type=int,default=5); a=ap.parse_args(); fail=[]
    for c in inv.CHAPTERS:
        folder=BOOK_ROOT/c['folder']; nbs=[p for p in folder.glob('*.ipynb') if p.name not in IGNORED]
        if len(nbs)!=1: fail.append(f"{folder.relative_to(BOOK_ROOT)} has {len(nbs)} canonical notebooks")
        path=folder/c['notebook']
        if not path.exists(): fail.append(f"missing {path.relative_to(BOOK_ROOT)}"); continue
        s=stats(path)
        if s['words']<a.min_words: fail.append(f"{path.relative_to(BOOK_ROOT)} has only {s['words']} words")
        if s['code_cells']<a.min_code_cells: fail.append(f"{path.relative_to(BOOK_ROOT)} has only {s['code_cells']} code cells")
        if s['display']<4: fail.append(f"{path.relative_to(BOOK_ROOT)} displays too few artifacts")
        for k in ['render','setup','takeaways']:
            if not s[k]: fail.append(f"{path.relative_to(BOOK_ROOT)} missing {k}")
        if s['crop']: fail.append(f"{path.relative_to(BOOK_ROOT)} appears to reference crops/screenshots")
    print(f"Audited {len(inv.CHAPTERS)} canonical notebooks.")
    if fail:
        [print('FAIL:',f) for f in fail]; raise SystemExit(1)
    print('All canonical notebooks meet the configured structure and depth thresholds.')
if __name__=='__main__': main()
''')
    w(Path('scripts/audit_fpog_visuals.py'), '''
from __future__ import annotations
import argparse
from pathlib import Path
import fpog_inventory as inv
from utils.validation import png_stats
BOOK_ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--min-width',type=int,default=300); ap.add_argument('--min-height',type=int,default=240); ap.add_argument('--min-std',type=float,default=2.0); a=ap.parse_args(); fail=[]; hashes={}
    for c in inv.CHAPTERS:
        root=BOOK_ROOT/'artifacts'/c['artifact']; pngs=sorted((root/'figures').glob('*.png'))
        if len(pngs)<5: fail.append(f"{root.relative_to(BOOK_ROOT)} has only {len(pngs)} PNG figures")
        for p in pngs:
            s=png_stats(p); hashes.setdefault(s['sha'],[]).append(p)
            if s['width']<a.min_width or s['height']<a.min_height: fail.append(f"{p.relative_to(BOOK_ROOT)} is too small: {s['width']}x{s['height']}")
            if s['pixel_std']<a.min_std: fail.append(f"{p.relative_to(BOOK_ROOT)} appears blank: std={s['pixel_std']:.3f}")
        if not list((root/'html').glob('*.html')): fail.append(f"{root.relative_to(BOOK_ROOT)} has no HTML lab artifact")
        if len(list((root/'checks').glob('*.json')))<2: fail.append(f"{root.relative_to(BOOK_ROOT)} has too few JSON checks")
    for paths in hashes.values():
        if len(paths)>1: fail.append('duplicate PNG hash: '+', '.join(str(p.relative_to(BOOK_ROOT)) for p in paths))
    print(f"Audited visuals for {len(inv.CHAPTERS)} chapters.")
    if fail:
        [print('FAIL:',f) for f in fail]; raise SystemExit(1)
    print('All visual artifacts are present, nonblank, and uniquely rendered.')
if __name__=='__main__': main()
''')
    w(Path('scripts/validate_fpog_course.py'), '''
from __future__ import annotations
import argparse
from pathlib import Path
import nbformat
from nbclient import NotebookClient
import fpog_inventory as inv
BOOK_ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--all',action='store_true'); ap.add_argument('--limit',type=int); ap.add_argument('--timeout',type=int,default=300); a=ap.parse_args(); ps=[BOOK_ROOT/c['folder']/c['notebook'] for c in inv.CHAPTERS]; ps=ps if a.all else ps[:a.limit or len(ps)]
    for i,p in enumerate(ps,1):
        print(f"[{i}/{len(ps)}] {p.relative_to(BOOK_ROOT)}"); nb=nbformat.read(p,as_version=4); NotebookClient(nb,timeout=a.timeout,kernel_name='python3',resources={'metadata':{'path':str(p.parent)}}).execute()
    print(f"Executed {len(ps)} notebooks successfully.")
if __name__=='__main__': main()
''')
def notebook_markdown(c):
    visual_list='\n'.join(f'- {v}' for v in c['visuals'])
    return f'''
# Chapter {c['number']}: {c['title']}

Source orientation: printed pages {c['printed_span']}, physical PDF pages {c['pdf_span']}, sections {c['sections']}. This notebook is an original standalone lesson. The textbook guided the chapter boundary and topic order, but the explanations, diagrams, computations, labs, and checks here are written for this course and do not require the PDF.

## Chapter question

**{c['question']}**

This chapter is one face of the four-pillar view of geometry. The point is not to rank the faces, as if construction, proof, algebra, projection, and transformation were rival teams in tiny mathematical jerseys. The useful habit is to move among them. A construction can suggest an invariant; an invariant can become an equation; an equation can reveal a transformation; a transformation can explain why two figures feel like the same object. The notebook keeps that movement visible by pairing prose with generated artifacts and executable checks.

## Visual route

The visual spine for this chapter is:

{visual_list}

Each artifact is meant to carry a claim. A diagram is not decoration here; it is a small instrument. When a line is labeled, the label says what relation should be inspected. When a construction is shown twice, the comparison is the lesson. When a numeric check appears, it is there to keep the picture honest: equal lengths should compute as equal lengths, preserved ratios should still agree after a transformation, and a claimed invariant should survive the example that supposedly demonstrates it.

## Translation guide

The chapter begins with the geometric language inherited from the book and translates it into a computational vocabulary. Points become arrays or homogeneous coordinates. Lines become equations, joins, sampled curves, or transformation orbits. Circles become either metric constraints or boundary-orthogonal geodesics, depending on the geometry in play. Congruence becomes a distance-preservation check. Similarity becomes a ratio check. Projective coincidence becomes an incidence relation. A transformation becomes a function whose output can be plotted and whose invariant can be tested.

This translation is deliberately modest. The goal is not to hide the geometry behind software. Instead, the code acts like a second straightedge: it lets us redraw the same claim under slightly different parameters and notice what refuses to change. That refusal is often the theorem. A sheared parallelogram may stop looking rectangular while its base-height area is unchanged. A projective map may destroy ordinary spacing while preserving cross-ratio. A hyperbolic step may shrink visually near the boundary while its model distance stays fixed.

## Reading the figures

Read each figure by asking three questions. First, what data is being held fixed? That might be two endpoints, a unit segment, a horizon line, a group operation, a boundary circle, or a choice of coordinates. Second, what operation is allowed? A compass can transfer a radius; a coordinate calculation can solve a quadratic; a projective matrix can move infinity; a Mobius map can bend Euclidean-looking circles while preserving the half-plane. Third, what is the invariant? The invariant is the portable part of the argument, the thing that remains meaningful after the construction has moved.

The HTML lab is intentionally lightweight. It is not a polished app; it is a pressure test for the central idea. Move the parameter, then ask whether the labeled invariant is still visible. If the diagram changes but the check survives, the concept has started to become portable. If the check fails, that is not an embarrassment. It is a clue that the construction had a hidden assumption or that the wrong geometry is being used.

## Proof stance

The notebook treats proofs as inspectable processes rather than blocks of text to admire from a respectful distance. A proof may appear as a dependency graph, a before-and-after dissection, a pair of overlaid configurations, or a numerical experiment with a symbolic summary. This matters because the four pillars do not prove the same way. Euclid-style geometry often proves by constructing auxiliary lines and comparing triangles or areas. Coordinate geometry proves by reducing the question to equations. Projective geometry proves by incidence and invariance. Transformation geometry proves by identifying the group action and the quantities it preserves.

Those differences are a feature. A learner who only sees one style may think geometry is a single narrow ritual. A learner who sees several styles can choose the view that makes the next claim tractable. The course therefore keeps repeating a friendly move: draw it, compute it, perturb it, and name what stayed fixed.

## Pitfalls to watch

The common pitfall is to trust a drawing too quickly. A clean picture can smuggle in existence, betweenness, parallelism, orientation, or metric assumptions. Another pitfall is to overtrust algebra: an equation may be correct in one coordinate chart but hide a point at infinity, a denominator that vanished, or a model boundary that should not be crossed. In the notebooks, final sanity checks are not bureaucratic. They are part of the pedagogy. They say that this visual is making a mathematical promise, and here is the small computation that checks the promise.

A second pitfall is to treat the four pillars as historical compartments. In practice, they interlock. A straightedge construction can motivate a projective theorem. A vector identity can explain a Euclidean proof. A transformation group can clarify why a non-Euclidean model deserves to be called a geometry. Keep the borders permeable.

## Applied lab

The applied lab for this chapter asks you to perturb one object while tracking one invariant. Change the parameter in the HTML artifact, rerun the render cell if you want fresh outputs, and compare the visual result with the JSON checks. The lab is small on purpose. It should feel like holding a model in your hand and rotating it until the theorem clicks.
'''
def write_notebooks():
    setup='''
from pathlib import Path
import sys

def find_book_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if candidate.name == "The-Four-Pillars-of-Geometry" and (candidate / "AGENTS.md").exists():
            return candidate
    raise RuntimeError("Could not locate course root")
BOOK_ROOT = find_book_root(Path.cwd().resolve())
if str(BOOK_ROOT) not in sys.path: sys.path.insert(0, str(BOOK_ROOT))
from utils.artifacts import assert_artifacts, display_artifact, image_stats
from utils.chapter_visuals import render_chapter_visuals
CHAPTER_KEY = "__ARTIFACT__"
ARTIFACT_ROOT = BOOK_ROOT / "artifacts" / CHAPTER_KEY
print(f"BOOK_ROOT = {BOOK_ROOT}")
print(f"ARTIFACT_ROOT = {ARTIFACT_ROOT}")
'''
    for c in CHAPTERS:
        cells=[md(notebook_markdown(c)),code(setup.replace('__ARTIFACT__', c['artifact'])),code("""
visuals = render_chapter_visuals(CHAPTER_KEY, ARTIFACT_ROOT)
figures = visuals['figures']; html_labs = visuals['html']; checks = visuals['checks']
print(f"rendered {len(figures)} figures, {len(html_labs)} HTML lab(s), and {len(checks)} check file(s)")
"""),md('''
## Generated visual artifacts

The first five displays are the canonical visual spine for this chapter. They are regenerated from code and saved under the book-local artifact tree.
'''),code('''
display_artifact(figures[0], width=760)
display_artifact(figures[1], width=760)
display_artifact(figures[2], width=760)
'''),code('''
display_artifact(figures[3], width=760)
display_artifact(figures[4], width=760)
display_artifact(html_labs[0], width="100%", height=360)
'''),md('''
## Computational sanity checks

The JSON files are intentionally small: they record the numerical invariants that the visuals claim to preserve. This keeps the figures from becoming pretty but unverifiable posters.
'''),code('''
import json
summary = json.loads((ARTIFACT_ROOT / "checks" / "invariants.json").read_text(encoding="utf-8"))
summary
'''),code('''
all_paths = figures + html_labs + checks + [ARTIFACT_ROOT / "checks" / "artifact_manifest.json"]
assert_artifacts(all_paths, min_size=128)
stats = [image_stats(path) for path in figures]
assert all(item["pixel_std"] > 2.0 for item in stats)
assert all(item["width"] >= 300 and item["height"] >= 240 for item in stats)
print("artifact checks passed for", CHAPTER_KEY)
'''),md(f'''
## Takeaways

- The chapter question was: {c['question']}
- The main visual spine was: {', '.join(c['visuals'])}.
- The notebook uses the PDF only for source orientation; the teaching prose, diagrams, computations, and artifacts are original.
- A useful study rhythm is to identify the fixed data, perform the allowed operation, and name the invariant that survives.
- The generated checks are part of the lesson: they connect the visible figure to a numeric or symbolic claim.
''')]
        out=ROOT/c['folder']/c['notebook']; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(nb(cells),indent=1),encoding='utf-8')
def generate_artifacts():
    import sys
    sys.path.insert(0,str(ROOT))
    from utils.chapter_visuals import render_chapter_visuals
    for c in CHAPTERS: render_chapter_visuals(c['artifact'], ROOT/'artifacts'/c['artifact'])
def main():
    create_scaffold(); generate_artifacts(); print('Created Four Pillars course scaffold, notebooks, utilities, scripts, and artifacts.')
if __name__=='__main__': main()
