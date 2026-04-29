"""Validation helpers for notebooks and artifacts."""

from __future__ import annotations

from pathlib import Path


def require_nonempty(paths: list[str | Path], min_bytes: int = 1000) -> None:
    for path in paths:
        p = Path(path)
        if not p.exists():
            raise AssertionError(f"missing artifact: {p}")
        if p.stat().st_size < min_bytes:
            raise AssertionError(f"artifact too small: {p} ({p.stat().st_size} bytes)")


def artifact_report(paths: list[str | Path], root: str | Path | None = None) -> list[dict[str, int | str]]:
    report = []
    base = Path(root).resolve() if root is not None else None
    for path in paths:
        p = Path(path)
        label = p.resolve()
        if base is not None:
            try:
                label = label.relative_to(base)
            except ValueError:
                pass
        report.append({"path": Path(label).as_posix(), "bytes": int(p.stat().st_size)})
    return report
