from __future__ import annotations
import argparse, re, sys
from pathlib import Path
import nbformat
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path
def wc(s): return len(re.findall(r"[A-Za-z0-9_]+", s))
def main():
    p=argparse.ArgumentParser(); p.add_argument("--min-words",type=int,default=550); p.add_argument("--min-code-cells",type=int,default=3); a=p.parse_args(); failures=[]
    for u in UNITS:
        path=canonical_notebook_path(u)
        if not path.exists(): failures.append(f'{u["id"]}: missing notebook'); continue
        nb=nbformat.read(path,as_version=4); md="\n".join("".join(c.get("source","")) for c in nb.cells if c.cell_type=="markdown"); codes=[c for c in nb.cells if c.cell_type=="code"]
        issues=[]
        if wc(md)<a.min_words: issues.append(f"too few words {wc(md)}")
        if len(codes)<a.min_code_cells: issues.append(f"too few code cells {len(codes)}")
        for marker in ["Source Span","Library Routing","Visual Sequence","Sanity Checks"]:
            if marker not in md: issues.append(f"missing {marker}")
        miss=[t for t in u["concepts"][:3] if t.lower() not in md.lower()]
        if miss: issues.append("missing terms "+", ".join(miss))
        if issues: failures.append(f'{u["id"]}: '+'; '.join(issues))
    if failures:
        print("\n".join("FAIL "+f for f in failures), file=sys.stderr); raise SystemExit(1)
    print(f"Notebook audit passed for {len(UNITS)} canonical notebooks")
if __name__=="__main__": main()
