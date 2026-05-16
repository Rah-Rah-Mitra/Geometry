"""Audit generated course artifacts for presence and nonzero size."""

from __future__ import annotations

from pathlib import Path
import json
import sys

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BOOK_ROOT))

from scripts import otonn_inventory as inventory
from utils.visuals import artifact_paths_for_unit


def main() -> None:
    findings = []
    for unit in inventory.UNITS:
        paths = artifact_paths_for_unit(unit)
        for kind, path in paths.items():
            if not path.exists():
                findings.append(f"{unit['id']}: missing {kind} {path.relative_to(BOOK_ROOT)}")
            elif path.stat().st_size < 200:
                findings.append(f"{unit['id']}: tiny {kind} {path.relative_to(BOOK_ROOT)}")
        check_path = paths["checks"]
        if check_path.exists():
            data = json.loads(check_path.read_text(encoding="utf-8"))
            if not data.get("invariant_ok"):
                findings.append(f"{unit['id']}: invariant_ok is false in {check_path.relative_to(BOOK_ROOT)}")
    if findings:
        for finding in findings:
            print(f"- {finding}")
        raise SystemExit(1)
    print(f"Artifacts present and nonzero for {len(inventory.UNITS)} units.")


if __name__ == "__main__":
    main()
