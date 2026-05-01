from __future__ import annotations
import sys
from pathlib import Path
import nbformat as nbf
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS, canonical_notebook_name
def write_nb(path: Path, text: str) -> None:
    nb=nbf.v4.new_notebook(); nb.metadata["kernelspec"]={"display_name":"Python 3","language":"python","name":"python3"}; nb.metadata["language_info"]={"name":"python","version":"3.13"}; nb.cells=[nbf.v4.new_markdown_cell(text)]; nbf.write(nb,path)
def main() -> int:
    rows=[]
    for ch in CHAPTERS:
        nb=canonical_notebook_name(ch); rows.append(f"| {ch['part']} | {ch['no']:02d} | [{ch['title']}]({ch['folder']}/{nb}) | {ch['printed']} | {ch['pdf']} | {ch['visual']} |")
        write_nb(ROOT/ch["folder"]/"00-index.ipynb", f"# Chapter {ch['no']:02d}: {ch['title']}\n\nCanonical notebook: [{nb}]({nb})\n\nSource orientation: printed pages {ch['printed']}, PDF pages {ch['pdf']}.\n\nFocus: {ch['focus']}.\n\nVisual spine: {ch['visual']}.\n")
    write_nb(ROOT/"00-book-index.ipynb", "# Introduction to Geometry: visualization-first notebook course\n\nStandalone computational companion to Coxeter's *Introduction to Geometry*, Second Edition.\n\n| Part | Chapter | Notebook | Printed pages | PDF pages | Visual spine |\n| --- | ---: | --- | ---: | ---: | --- |\n"+"\n".join(rows)+"\n")
    print(f"rebuilt indexes for {len(CHAPTERS)} chapters"); return 0
if __name__=="__main__": raise SystemExit(main())
