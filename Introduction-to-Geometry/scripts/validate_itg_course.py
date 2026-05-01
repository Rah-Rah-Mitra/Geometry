from __future__ import annotations
import argparse, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.course import CHAPTERS, canonical_notebook_name
def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("--limit",type=int,default=None); p.add_argument("--all",action="store_true"); p.add_argument("--timeout",type=int,default=300); args=p.parse_args(); notebooks=[ROOT/ch["folder"]/canonical_notebook_name(ch) for ch in CHAPTERS]
    if not args.all and args.limit is not None: notebooks=notebooks[:args.limit]
    failures=[]
    for path in notebooks:
        print(f"executing {path.relative_to(ROOT)}")
        try:
            nb=nbformat.read(path,as_version=4); NotebookClient(nb,timeout=args.timeout,kernel_name="python3",resources={"metadata":{"path":str(path.parent)}}).execute()
        except Exception as exc: failures.append(f"{path}: {type(exc).__name__}: {exc}")
    if failures:
        print("\nFAILURES:"); [print("-",f) for f in failures]; return 1
    print(f"validated {len(notebooks)} notebooks"); return 0
if __name__=="__main__": raise SystemExit(main())
