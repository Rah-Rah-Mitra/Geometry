"""Source-map helpers for this notebook course."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
BOOK_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP_PATH = BOOK_ROOT / "source_map.json"
def load_source_map() -> dict[str, Any]:
    return json.loads(SOURCE_MAP_PATH.read_text(encoding="utf-8"))
def course_units() -> list[dict[str, Any]]:
    return load_source_map()["units"]
COURSE_MAP = course_units()
