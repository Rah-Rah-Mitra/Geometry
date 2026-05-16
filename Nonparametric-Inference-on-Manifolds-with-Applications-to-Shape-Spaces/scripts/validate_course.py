"""Execute canonical notebooks with nbclient."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from utils.course_manifest import CHAPTERS


def execute(path: Path, timeout: int) -> dict[str, object]:
    nb = nbformat.read(path, as_version=4)
    start = time.time()
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    return {"path": str(path.relative_to(BOOK_ROOT)), "seconds": round(time.time() - start, 2)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Validate only the first N notebooks; 0 means all.")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    selected = list(CHAPTERS)
    if args.limit:
        selected = selected[: args.limit]
    passed = []
    failures = []
    for chapter in selected:
        try:
            passed.append(execute(chapter.path, args.timeout))
            print(f"ok {chapter.path.relative_to(BOOK_ROOT)}")
        except Exception as exc:  # noqa: BLE001 - validation should report any notebook failure
            failures.append({"path": str(chapter.path.relative_to(BOOK_ROOT)), "error": f"{type(exc).__name__}: {exc}"})
            print(f"fail {chapter.path.relative_to(BOOK_ROOT)}: {type(exc).__name__}: {exc}")
            break
    report = {"requested": len(selected), "passed": passed, "failures": failures}
    if args.json:
        print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)
    print(f"Validated {len(passed)} notebook(s)")


if __name__ == "__main__":
    main()
