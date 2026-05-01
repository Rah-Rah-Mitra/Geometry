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
