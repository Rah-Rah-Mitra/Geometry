"""Generate all geometric group theory visual artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.chapter_visuals import build_all_visuals  # noqa: E402


def main() -> None:
    outputs = build_all_visuals()
    total = 0
    for unit, groups in outputs.items():
        unit_count = sum(len(value) for value in groups.values())
        total += unit_count
        print(f"{unit}: {unit_count} artifacts/check files")
    print(f"Generated {total} artifact/check files.")


if __name__ == "__main__":
    main()

