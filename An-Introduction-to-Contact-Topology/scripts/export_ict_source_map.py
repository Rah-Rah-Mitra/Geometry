"""Export the contact topology source map as JSON."""

from __future__ import annotations

import json
from pathlib import Path

from ict_inventory import source_map

BOOK_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    path = BOOK_ROOT / "source-map.json"
    path.write_text(json.dumps(source_map(), indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote {path.relative_to(BOOK_ROOT)}")


if __name__ == "__main__":
    main()
