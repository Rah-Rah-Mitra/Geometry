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
