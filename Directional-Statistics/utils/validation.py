"""Validation helpers shared by notebooks and scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def artifact_record(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    try:
        root = Path(__file__).resolve().parents[1]
        shown = str(p.resolve().relative_to(root)).replace("\\", "/")
    except ValueError:
        shown = str(p)
    return {"path": shown, "exists": p.exists(), "bytes": p.stat().st_size if p.exists() else 0}


def assert_artifacts(paths: list[str | Path], min_bytes: int = 100) -> list[dict[str, Any]]:
    records = [artifact_record(path) for path in paths]
    missing = [record for record in records if not record["exists"] or record["bytes"] <= min_bytes]
    if missing:
        raise AssertionError(f"artifact checks failed: {missing}")
    return records


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))
