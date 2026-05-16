"""Regenerate source maps and indexes without touching notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from build_hodge_course import write_indexes, write_source_maps


if __name__ == "__main__":
    write_source_maps()
    write_indexes()

