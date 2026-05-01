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
        fig,ax=figure_axes(title=f"{name.replace('_',' ').title()} - {mode}"); _concept(ax,mode) if i==0 else _extra(ax,i); figs.append(_save(fig,root,f'{name}.png'))
    html=[_lab(root,chapter_key,mode)]
    checks_path=save_json({'chapter_key':chapter_key,'mode':mode,'figure_count':len(figs),'sample_cross_ratio':cross_ratio(-2,-.5,1.2,2.4),'sample_hyperbolic_distance':hyperbolic_distance_half_plane(1j,1+1.2j)},root,'checks','invariants.json')
    manifest=save_json({'figures':[str(p.relative_to(root)) for p in figs],'html':[str(p.relative_to(root)) for p in html],'checks':['checks/invariants.json']},root,'checks','artifact_manifest.json')
    return {'figures':figs,'html':html,'checks':[checks_path,manifest]}
