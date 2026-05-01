
"""Execute Barrett O'Neill notebooks with nbclient."""
from __future__ import annotations
import argparse, asyncio, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
BOOK_ROOT=Path(__file__).resolve().parents[1]
if sys.platform.startswith("win"): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
def notebook_paths(all_notebooks: bool, limit: int | None) -> list[Path]:
    artifact_root=BOOK_ROOT/"artifacts"; paths=[p for p in sorted(BOOK_ROOT.rglob("*.ipynb")) if artifact_root not in p.parents]
    if not all_notebooks:
        names={"00-book-index.ipynb","00-how-to-use-this-course.ipynb","01-calculus-on-euclidean-space.ipynb","02-frame-fields.ipynb","03-euclidean-geometry.ipynb","04-calculus-on-a-surface.ipynb","05-shape-operators.ipynb","06-geometry-of-surfaces-in-r3.ipynb","07-riemannian-geometry.ipynb","08-global-structure-of-surfaces.ipynb","appendix-a-computer-formulas.ipynb"}
        paths=[p for p in paths if p.name in names]
    return paths[:limit] if limit is not None else paths
def execute_notebook(path: Path, timeout: int) -> None:
    nb=nbformat.read(path, as_version=4); NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata":{"path":str(path.parent)}}).execute()
def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--all", action="store_true"); parser.add_argument("--limit", type=int); parser.add_argument("--timeout", type=int, default=120); args=parser.parse_args(); paths=notebook_paths(args.all,args.limit)
    if not paths: raise SystemExit("no notebooks found")
    failures=[]
    for i,path in enumerate(paths,1):
        print(f"[{i}/{len(paths)}] {path.relative_to(BOOK_ROOT)}")
        try: execute_notebook(path,args.timeout)
        except Exception as exc: failures.append((path,repr(exc)))
    if failures:
        for path,error in failures: print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")
if __name__=="__main__": main()
