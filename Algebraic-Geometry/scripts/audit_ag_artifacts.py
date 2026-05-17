"""Audit Hartshorne Algebraic Geometry artifact metadata.

The artifact tree should contain generated teaching aids and compact JSON/CSV
checks only. Source extracts, temporary writer scripts, absolute paths, and
generic placeholder records are treated as failures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ag_inventory as inventory


def relpath(path: Path) -> str:
    return str(path.relative_to(BOOK_ROOT)).replace("\\", "/")


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_json_error": str(exc)}


def audit_entry(entry: dict[str, object]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    root = BOOK_ROOT / "artifacts" / str(entry["artifact"])
    checks = root / "checks"

    if not root.exists():
        return [{"path": relpath(root), "issue": "missing artifact root"}]

    temp_scripts = sorted(root.rglob("*.py"))
    if temp_scripts:
        findings.append(
            {
                "path": relpath(root),
                "issue": "temporary writer/helper scripts remain under artifacts",
                "files": [relpath(path) for path in temp_scripts],
            }
        )

    copied_source_text = sorted(
        path for path in root.rglob("*.txt") if "source" in path.name.lower() or "span" in path.name.lower()
    )
    if copied_source_text:
        findings.append(
            {
                "path": relpath(root),
                "issue": "possible copied source-text artifacts remain",
                "files": [relpath(path) for path in copied_source_text],
            }
        )

    coverage_path = checks / "source-coverage.json"
    if not coverage_path.exists():
        findings.append({"path": relpath(coverage_path), "issue": "missing source coverage ledger"})
    else:
        coverage = load_json(coverage_path)
        if isinstance(coverage, dict) and coverage.get("_json_error"):
            findings.append({"path": relpath(coverage_path), "issue": coverage["_json_error"]})
        if not isinstance(coverage, dict):
            findings.append({"path": relpath(coverage_path), "issue": "source coverage ledger is not an object"})
        else:
            if coverage.get("printed_span") != entry["printed_span"] or coverage.get("pdf_span") != entry["pdf_span"]:
                findings.append({"path": relpath(coverage_path), "issue": "source coverage ledger span does not match inventory"})
            covered_titles = {
                str(item.get("title", "")).strip()
                for item in coverage.get("sections", [])
                if isinstance(item, dict)
            }
            expected_titles = {str(item["title"]) for item in entry.get("sections", [])}
            missing = sorted(expected_titles - covered_titles)
            if missing:
                findings.append(
                    {
                        "path": relpath(coverage_path),
                        "issue": "source coverage ledger misses inventory sections",
                        "missing": missing[:12],
                        "missing_count": len(missing),
                    }
                )

    final_path = checks / "final-sanity.json"
    if not final_path.exists():
        findings.append({"path": relpath(final_path), "issue": "missing final sanity artifact"})
    else:
        final = load_json(final_path)
        if isinstance(final, dict) and final.get("_json_error"):
            findings.append({"path": relpath(final_path), "issue": final["_json_error"]})
        if not isinstance(final, dict):
            findings.append({"path": relpath(final_path), "issue": "final sanity artifact is not an object"})
        else:
            records = final.get("artifacts", [])
            if not records:
                findings.append({"path": relpath(final_path), "issue": "final sanity has no artifact records"})
            for record in records:
                rel = record.get("path") if isinstance(record, dict) else None
                if not rel:
                    findings.append({"path": relpath(final_path), "issue": "artifact record missing path"})
                    continue
                if ":" in rel or str(rel).startswith("/") or str(rel).startswith("\\"):
                    findings.append({"path": relpath(final_path), "issue": "artifact path is not book-relative", "artifact": rel})
                    continue
                artifact = BOOK_ROOT / str(rel)
                if not artifact.exists() or artifact.stat().st_size <= 40:
                    findings.append({"path": relpath(final_path), "issue": "recorded artifact missing or tiny", "artifact": rel})
            checks_block = final.get("checks") or final.get("topic_checks") or {}
            if not checks_block:
                findings.append({"path": relpath(final_path), "issue": "final sanity lacks computational checks"})

    return findings


def main() -> None:
    findings: list[dict[str, object]] = []
    for entry in inventory.ENTRIES:
        findings.extend(audit_entry(entry))
    print(json.dumps({"findings": findings}, indent=2))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
