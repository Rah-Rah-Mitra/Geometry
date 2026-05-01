from __future__ import annotations
import re
from pathlib import Path
import nbformat
from .course import CHAPTERS, canonical_notebook_name
WORD_RE=re.compile(r"[A-Za-z][A-Za-z0-9'-]*")
def canonical_notebooks(root: Path) -> list[Path]: return [root/ch["folder"]/canonical_notebook_name(ch) for ch in CHAPTERS]
def notebook_stats(path: Path) -> dict[str,int]:
    nb=nbformat.read(path, as_version=4); markdown="\n".join(cell.get("source","") for cell in nb.cells if cell.cell_type=="markdown"); return {"words":len(WORD_RE.findall(markdown)), "code_cells":sum(1 for cell in nb.cells if cell.cell_type=="code"), "cells":len(nb.cells)}
