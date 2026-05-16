"""Audit contact topology notebooks for standalone depth and structure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_canonical_notebooks, notebook_stats  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=900)
    parser.add_argument("--min-code-cells", type=int, default=4)
    args = parser.parse_args()

    stats = [notebook_stats(path, BOOK_ROOT) for path in discover_canonical_notebooks(BOOK_ROOT)]
    failing = [
        item
        for item in stats
        if item["markdown_words"] < args.min_words
        or item["code_cells"] < args.min_code_cells
        or item["display_artifact_calls"] < 1
        or item["direct_visual_calls"] < 1
        or item["assert_artifact_calls"] < 1
        or not item["has_source_span"]
        or not item["has_translation_guide"]
        or not item["has_applied_lab"]
        or not item["has_takeaways"]
        or item["stale_paths"]
    ]
    report = {"notebook_count": len(stats), "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited {len(stats)} canonical notebooks")
    if failing:
        print(f"{len(failing)} notebooks failed the audit:")
        for item in failing:
            print(
                f"- {item['path']}: {item['markdown_words']} words, {item['code_cells']} code cells, "
                f"display calls={item['display_artifact_calls']}, visual calls={item['direct_visual_calls']}, "
                f"assert calls={item['assert_artifact_calls']}, stale_paths={item['stale_paths']}"
            )
        raise SystemExit(1)
    print("All canonical notebooks meet the configured standalone structure thresholds.")


if __name__ == "__main__":
    main()
