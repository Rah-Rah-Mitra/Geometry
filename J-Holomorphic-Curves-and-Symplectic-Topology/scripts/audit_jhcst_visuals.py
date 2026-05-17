"""Audit generated JHCST artifacts for source-grounded visual notebooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jhcst_inventory import ENTRIES

BOOK_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CHECKS = {
    "source-coverage.json",
    "visual-storyboard.json",
    "final-sanity.json",
}


def inspect_unit(entry: dict[str, object]) -> dict[str, object]:
    root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
    figures = sorted((root / "figures").glob("*")) if (root / "figures").exists() else []
    checks = sorted((root / "checks").glob("*.json")) if (root / "checks").exists() else []
    tables = sorted((root / "tables").glob("*")) if (root / "tables").exists() else []
    files = figures + checks + tables
    small = [path.relative_to(BOOK_ROOT).as_posix() for path in files if path.stat().st_size <= 80]
    check_names = {path.name for path in checks}
    json_failures: list[str] = []
    for path in checks:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            json_failures.append(path.relative_to(BOOK_ROOT).as_posix() + ":invalid-json")
            continue
        if isinstance(data, dict) and data.get("passed") is False:
            json_failures.append(path.relative_to(BOOK_ROOT).as_posix() + ":passed-false")
    return {
        "unit": str(entry["artifact"]),
        "figure_count": len(figures),
        "check_count": len(checks),
        "table_count": len(tables),
        "missing_required_checks": sorted(REQUIRED_CHECKS - check_names),
        "json_failures": json_failures,
        "small_files": small,
        "exists": root.exists(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    stats = [inspect_unit(entry) for entry in ENTRIES]
    failing = [
        item
        for item in stats
        if not item["exists"]
        or item["figure_count"] < 2
        or item["check_count"] < 3
        or item["table_count"] < 1
        or item["missing_required_checks"]
        or item["json_failures"]
        or item["small_files"]
    ]
    report = {"unit_count": len(stats), "failing_count": len(failing), "failing": failing, "stats": stats}
    if args.json:
        print(json.dumps(report, indent=2))
        return
    print(f"Audited artifacts for {len(stats)} units")
    if failing:
        print(f"{len(failing)} units failed artifact audit:")
        for item in failing:
            print(
                f"- {item['unit']}: figures={item['figure_count']}, checks={item['check_count']}, "
                f"tables={item['table_count']}, missing_required_checks={item['missing_required_checks']}, "
                f"json_failures={item['json_failures']}, small={item['small_files']}"
            )
        raise SystemExit(1)
    print("All artifact folders contain the expected nonempty figures, checks, and tables.")


if __name__ == "__main__":
    main()
