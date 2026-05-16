"""Audit generated JHCST artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jhcst_inventory import ENTRIES

BOOK_ROOT = Path(__file__).resolve().parents[1]


def inspect_unit(entry: dict[str, object]) -> dict[str, object]:
    root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
    figures = sorted((root / "figures").glob("*")) if (root / "figures").exists() else []
    checks = sorted((root / "checks").glob("*.json")) if (root / "checks").exists() else []
    tables = sorted((root / "tables").glob("*")) if (root / "tables").exists() else []
    files = figures + checks + tables
    small = [path.relative_to(BOOK_ROOT).as_posix() for path in files if path.stat().st_size <= 80]
    return {
        "unit": str(entry["artifact"]),
        "figure_count": len(figures),
        "check_count": len(checks),
        "table_count": len(tables),
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
                f"tables={item['table_count']}, small={item['small_files']}"
            )
        raise SystemExit(1)
    print("All artifact folders contain the expected nonempty figures, checks, and tables.")


if __name__ == "__main__":
    main()
