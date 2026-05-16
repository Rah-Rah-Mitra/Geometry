"""Regenerate reproducible course artifacts."""

from __future__ import annotations

from pathlib import Path
import sys

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from scripts import otonn_inventory as inventory
from utils.visuals import build_unit_artifacts


def main() -> None:
    failures = []
    for unit in inventory.UNITS:
        result = build_unit_artifacts(unit)
        if not result["invariant_ok"]:
            failures.append(unit["id"])
        print(f"{unit['id']}: {result['figure']['path']} | invariant_ok={result['invariant_ok']}")
    if failures:
        raise SystemExit(f"artifact invariant failures: {', '.join(failures)}")
    print(f"Generated artifacts for {len(inventory.UNITS)} units.")


if __name__ == "__main__":
    main()
