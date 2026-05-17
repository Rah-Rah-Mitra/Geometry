import argparse
import asyncio
import json
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pag_inventory as inv

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_paths(include_indexes=False):
    paths = [BOOK_ROOT / entry["folder"] / entry["notebook"] for entry in inv.ENTRIES]
    if include_indexes:
        index_paths = [BOOK_ROOT / "00-book-index.ipynb"]
        index_paths.extend(BOOK_ROOT / entry["folder"] / "00-index.ipynb" for entry in inv.ENTRIES)
        paths = index_paths + paths
    return paths


def execute_notebook(path, timeout, write_executed=False):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    if write_executed:
        nbformat.write(nb, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--include-indexes", action="store_true")
    parser.add_argument("--write-executed", action="store_true")
    args = parser.parse_args()

    paths = notebook_paths(include_indexes=args.include_indexes)
    if not args.all:
        paths = paths[: args.limit]

    executed = []
    for path in paths:
        print(path.relative_to(BOOK_ROOT))
        execute_notebook(path, args.timeout, write_executed=args.write_executed)
        executed.append(str(path.relative_to(BOOK_ROOT)))

    print(json.dumps({"executed": len(executed), "notebooks": executed}, indent=2))


if __name__ == "__main__":
    main()
