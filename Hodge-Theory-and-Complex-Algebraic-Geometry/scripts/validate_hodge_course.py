"""Execute canonical notebooks with nbclient."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import nbformat
from nbclient import NotebookClient

from utils.course_data import CHAPTERS


def execute_notebook(path: Path, timeout: int) -> dict[str, str]:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    return {"path": path.relative_to(ROOT).as_posix(), "status": "executed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()

    chapters = list(CHAPTERS if args.all else CHAPTERS[: args.limit])
    results = []
    for chapter in chapters:
        path = ROOT / chapter.notebook_path
        results.append(execute_notebook(path, args.timeout))
    report = {"executed": len(results), "results": results, "status": "pass"}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

