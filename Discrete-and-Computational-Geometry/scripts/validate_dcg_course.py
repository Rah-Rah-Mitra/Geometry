from __future__ import annotations
import argparse, asyncio, sys
from pathlib import Path
import nbformat
from nbclient import NotebookClient
BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path: sys.path.insert(0, str(BOOK_ROOT))
from utils.validation import canonical_notebooks, index_notebooks, relative
if sys.platform.startswith("win"): asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
def selected(all_notebooks: bool, limit: int | None) -> list[Path]:
    paths = [BOOK_ROOT / "00-book-index.ipynb", *canonical_notebooks(BOOK_ROOT)]
    if all_notebooks: paths = [*index_notebooks(BOOK_ROOT), *canonical_notebooks(BOOK_ROOT)]
    return paths[:limit] if limit is not None else paths
def execute(path: Path, timeout: int) -> None:
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}}).execute()
    nbformat.write(nb, path)
def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument("--all", action="store_true"); p.add_argument("--limit", type=int, default=4); p.add_argument("--timeout", type=int, default=300); args = p.parse_args()
    failures = []; paths = selected(args.all, args.limit)
    for i, path in enumerate(paths, 1):
        print(f"[{i}/{len(paths)}] {relative(path)}")
        try: execute(path, args.timeout)
        except Exception as exc: failures.append((path, repr(exc)))
    if failures:
        for path, error in failures: print(f"FAILED {path}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Executed {len(paths)} notebooks successfully")
if __name__ == "__main__": main()
