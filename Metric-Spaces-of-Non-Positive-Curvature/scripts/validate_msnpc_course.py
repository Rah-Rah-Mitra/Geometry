from __future__ import annotations
import argparse, asyncio, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
BOOK_ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(BOOK_ROOT))
from utils.source_map import UNITS, canonical_notebook_path
if sys.platform.startswith("win"): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
SMOKE={"chapter-i-02","chapter-ii-01","chapter-ii-05","chapter-ii-08","chapter-iii-h"}
def paths(all_notebooks, smoke, limit):
    units=[u for u in UNITS if (not smoke or u["id"] in SMOKE)]
    out=[canonical_notebook_path(u) for u in units]
    if not all_notebooks and not smoke and limit is None: out=out[:4]
    return out[:limit] if limit else out
def main():
    p=argparse.ArgumentParser(); p.add_argument("--all",action="store_true"); p.add_argument("--smoke",action="store_true"); p.add_argument("--limit",type=int); p.add_argument("--timeout",type=int,default=180); a=p.parse_args(); failures=[]; ps=paths(a.all,a.smoke,a.limit)
    for i,path in enumerate(ps,1):
        print(f"[{i}/{len(ps)}] {path.relative_to(BOOK_ROOT)}")
        try: NotebookClient(nbformat.read(path,as_version=4),timeout=a.timeout,kernel_name="python3",resources={"metadata":{"path":str(path.parent)}}).execute()
        except Exception as exc: failures.append((path,repr(exc)))
    if failures:
        for path,error in failures: print(f"FAILED {path.relative_to(BOOK_ROOT)}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(ps)} notebooks successfully")
if __name__=="__main__": main()
