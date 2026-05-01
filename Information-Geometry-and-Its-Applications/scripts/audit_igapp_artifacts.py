"""Audit non-image artifact presence and readability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import igapp_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"


def rel(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def audit(*, allow_missing: bool = False) -> list[tuple[str, str]]:
    findings = []
    for entry in inventory.ENTRIES:
        root = ARTIFACT_ROOT / entry["topic"]
        if not root.exists():
            if not allow_missing:
                findings.append((rel(root), "missing artifact root"))
            continue
        for suffix in ["*.png", "*.html", "*.json"]:
            if not list(root.rglob(suffix)):
                findings.append((rel(root), f"missing {suffix} artifact"))
        for path in root.rglob("*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                findings.append((rel(path), f"invalid JSON: {exc}"))
                continue
            if path.name == "final-sanity.json":
                for key in ["artifacts", "topic_checks", "standalone_contract", "pdf_used_for"]:
                    if key not in data:
                        findings.append((rel(path), f"missing final sanity key {key}"))
                for record in data.get("artifacts", []):
                    for key in ["path", "exists", "bytes"]:
                        if key not in record:
                            findings.append((rel(path), f"artifact record missing {key}"))
                    if isinstance(record.get("path"), str) and ":" in record["path"][:4]:
                        findings.append((rel(path), "artifact path is machine-absolute"))
        for path in root.rglob("*.html"):
            text = path.read_text(encoding="utf-8", errors="replace").lower()
            if "<html" not in text and "<div" not in text:
                findings.append((rel(path), "HTML artifact lacks html/div markup"))
            if 'src="https://cdn.plot.ly' in text or "src='https://cdn.plot.ly" in text:
                findings.append((rel(path), "HTML artifact depends on Plotly CDN"))
    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    findings = audit(allow_missing=args.allow_missing)
    if findings:
        print(f"Artifact audit found {len(findings)} issue(s)")
        for path, message in findings:
            print(f"- {path}: {message}")
        raise SystemExit(1)
    print(f"Artifact audit passed for {len(inventory.ENTRIES)} topics.")


if __name__ == "__main__":
    main()
