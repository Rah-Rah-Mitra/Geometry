"""Audit JHCST notebooks for standalone, source-grounded teaching quality."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import discover_canonical_notebooks, notebook_stats  # noqa: E402


def failure_reasons(item: dict[str, object], min_words: int, min_code_cells: int) -> list[str]:
    reasons: list[str] = []
    if int(item["markdown_words"]) < min_words:
        reasons.append(f"markdown_words<{min_words}")
    if int(item["code_cells"]) < min_code_cells:
        reasons.append(f"code_cells<{min_code_cells}")
    if int(item["display_artifact_calls"]) < 2:
        reasons.append("display_artifact_calls<2")
    if int(item["visual_generation_calls"]) < 2:
        reasons.append("visual_generation_calls<2")
    if int(item["assert_artifact_calls"]) < 3:
        reasons.append("assert_artifact_calls<3")
    if not bool(item["has_applied_lab"]):
        reasons.append("missing_applied_lab")
    if not bool(item["has_takeaways"]):
        reasons.append("missing_takeaways")
    missing_markers = [
        name
        for name, present in dict(item.get("required_markers", {})).items()
        if not bool(present)
    ]
    if missing_markers:
        reasons.append("missing_markers:" + ",".join(missing_markers))
    generic_hits = list(item.get("generic_phrase_hits", []))
    if generic_hits:
        reasons.append(f"generic_scaffold_phrases:{len(generic_hits)}")
    if item["stale_paths"]:
        reasons.append("stale_paths")
    return reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-words", type=int, default=650)
    parser.add_argument("--min-code-cells", type=int, default=5)
    args = parser.parse_args()

    stats = [notebook_stats(path, BOOK_ROOT) for path in discover_canonical_notebooks(BOOK_ROOT)]
    failing = []
    for item in stats:
        reasons = failure_reasons(item, args.min_words, args.min_code_cells)
        if reasons:
            item = dict(item)
            item["failure_reasons"] = reasons
            failing.append(item)
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
                f"display calls={item['display_artifact_calls']}, visual generation={item['visual_generation_calls']}, "
                f"assert calls={item['assert_artifact_calls']}, reasons={item['failure_reasons']}"
            )
        raise SystemExit(1)
    print("All canonical notebooks meet the configured standalone structure thresholds.")


if __name__ == "__main__":
    main()
