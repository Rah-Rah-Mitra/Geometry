import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pag_inventory as inv


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_json_error": str(exc)}


def audit_entry(entry):
    findings = []
    root = BOOK_ROOT / "artifacts" / entry["topic"]
    checks = root / "checks"

    temp_scripts = sorted(root.rglob("*.py"))
    if temp_scripts:
        findings.append({"path": str(root), "issue": "temporary writer/helper scripts remain under artifacts", "files": [str(p) for p in temp_scripts]})
    copied_source_text = sorted(path for path in root.rglob("*.txt") if "source" in path.name.lower() or "span" in path.name.lower())
    if copied_source_text:
        findings.append({"path": str(root), "issue": "possible copied source-text artifacts remain", "files": [str(p) for p in copied_source_text]})

    coverage_path = checks / "source-coverage.json"
    if not coverage_path.exists():
        findings.append({"path": str(coverage_path), "issue": "missing source coverage ledger"})
    else:
        coverage = load_json(coverage_path)
        if coverage.get("_json_error"):
            findings.append({"path": str(coverage_path), "issue": coverage["_json_error"]})
        if coverage.get("printed_span") != entry["printed_span"] or coverage.get("pdf_span") != entry["pdf_span"]:
            findings.append({"path": str(coverage_path), "issue": "source coverage ledger span does not match inventory"})
        covered_titles = {str(item.get("title", "")).strip() for item in coverage.get("sections", []) if isinstance(item, dict)}
        expected_titles = {item["title"] for item in entry.get("sections", [])}
        missing = sorted(expected_titles - covered_titles)
        if missing:
            findings.append({"path": str(coverage_path), "issue": "source coverage ledger misses inventory sections", "missing": missing[:12], "missing_count": len(missing)})

    final_path = checks / "final-sanity.json"
    if not final_path.exists():
        findings.append({"path": str(final_path), "issue": "missing final sanity artifact"})
    else:
        final = load_json(final_path)
        if final.get("_json_error"):
            findings.append({"path": str(final_path), "issue": final["_json_error"]})
        records = final.get("artifacts", [])
        if not records:
            findings.append({"path": str(final_path), "issue": "final sanity has no artifact records"})
        for record in records:
            rel = record.get("path") if isinstance(record, dict) else None
            if not rel:
                findings.append({"path": str(final_path), "issue": "artifact record missing path"})
                continue
            if ":" in rel or rel.startswith("/") or rel.startswith("\\"):
                findings.append({"path": str(final_path), "issue": "artifact path is not book-relative", "artifact": rel})
                continue
            artifact = BOOK_ROOT / rel
            if not artifact.exists() or artifact.stat().st_size <= 40:
                findings.append({"path": str(final_path), "issue": "recorded artifact missing or tiny", "artifact": rel})
        checks_block = final.get("checks") or final.get("topic_checks") or {}
        if not checks_block:
            findings.append({"path": str(final_path), "issue": "final sanity lacks computational checks"})

    return findings


def main():
    findings = []
    for entry in inv.ENTRIES:
        findings.extend(audit_entry(entry))
    print(json.dumps({"findings": findings}, indent=2))
    raise SystemExit(1 if findings else 0)


if __name__ == "__main__":
    main()
