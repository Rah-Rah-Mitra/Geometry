"""Audit Pressley notebooks for standalone depth and executable structure."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_notebooks, notebook_stats  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=1200)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()
    stats = [notebook_stats(path, BOOK_ROOT) for path in discover_notebooks(BOOK_ROOT)]
    failing = [item for item in stats if item.markdown_words < args.min_words or item.code_cells < args.min_code_cells]
    report = {
        "notebook_count": len(stats),
        "failing_count": len(failing),
        "failing": [asdict(item) for item in failing],
        "stats": [asdict(item) for item in stats],
    }
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing:
        for item in failing:
            print(f"- {item.path}: {item.markdown_words} words, {item.code_cells} code cells")
        raise SystemExit(1)
    print("All canonical notebooks meet the configured depth thresholds.")


if __name__ == "__main__":
    main()
