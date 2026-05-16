"""Validation helpers shared by notebooks and course scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def _effective_min_bytes(path: Path, min_bytes: int) -> int:
    if path.suffix.lower() in {".json", ".csv", ".txt", ".md"}:
        return min(min_bytes, 64)
    return min_bytes


def assert_artifacts(paths: Iterable[str | Path], min_bytes: int = 200) -> list[dict[str, object]]:
    records = []
    for path_like in paths:
        path = Path(path_like)
        if not path.exists():
            raise AssertionError(f"missing artifact: {path}")
        size = path.stat().st_size
        required_size = _effective_min_bytes(path, min_bytes)
        if size < required_size:
            raise AssertionError(f"artifact too small: {path} ({size} bytes)")
        records.append({"path": str(path), "bytes": int(size)})
    return records


def load_check(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assert_check_flag(path: str | Path, key: str = "invariant_ok") -> dict[str, object]:
    data = load_check(path)
    if not data.get(key):
        raise AssertionError(f"{path} does not set {key}=true")
    return data
