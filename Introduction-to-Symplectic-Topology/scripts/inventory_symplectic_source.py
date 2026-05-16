"""Build the source inventory for the symplectic topology notebook course."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.course_data import PDF_FILENAME, COURSE_UNITS, source_map_payload


def word_count_for_pdf_span(pdf_path: Path, first_page: int, last_page: int) -> int | None:
    executable = shutil.which("pdftotext")
    if executable is None or not pdf_path.exists():
        return None
    completed = subprocess.run(
        [executable, "-f", str(first_page), "-l", str(last_page), "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    return len(re.findall(r"\b[\w'-]+\b", completed.stdout))


def build_inventory(include_counts: bool) -> dict[str, object]:
    payload = source_map_payload()
    pdf_path = BOOK_ROOT / PDF_FILENAME
    for unit_payload, unit in zip(payload["units"], COURSE_UNITS, strict=True):
        if include_counts:
            unit_payload["pdftotext_word_count"] = word_count_for_pdf_span(pdf_path, unit.pdf_start, unit.pdf_end)
        unit_payload["source_policy"] = "Used for structure and topic orientation only; no copied prose or page images."
    payload["source_pdf_exists"] = pdf_path.exists()
    payload["source_pdf_bytes"] = pdf_path.stat().st_size if pdf_path.exists() else None
    payload["unit_count"] = len(COURSE_UNITS)
    return payload


def write_inventory(payload: dict[str, object]) -> None:
    inventory_dir = BOOK_ROOT / "inventory"
    inventory_dir.mkdir(parents=True, exist_ok=True)
    json_path = inventory_dir / "source-map.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# Source Map: Introduction to Symplectic Topology",
        "",
        f"- Source PDF: `{payload['source_pdf']}`",
        f"- Body page rule: `pdf_page = printed_page + {payload['printed_to_pdf_offset']}`",
        f"- Unit count: {payload['unit_count']}",
        "- Copyright guard: original course prose and generated visuals only; no textbook prose, screenshots, crops, or long exercise text.",
        "",
        "| Unit | Printed pages | PDF pages | Notebook | Core visual/check |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for unit in payload["units"]:
        lines.append(
            f"| {unit['label']} | {unit['printed_pages']} | {unit['pdf_pages']} | `{unit['notebook']}` | {unit['visual_concept']} |"
        )
    lines.extend(
        [
            "",
            "## Source Use",
            "",
            "The local PDF was used for chapter order, section names, page spans, and concept coverage. The notebooks, utilities, diagrams, checks, and lab prose are original course material.",
        ]
    )
    (inventory_dir / "source-map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write inventory/source-map.json and inventory/source-map.md")
    parser.add_argument("--no-counts", action="store_true", help="skip pdftotext word counts")
    args = parser.parse_args()
    payload = build_inventory(include_counts=not args.no_counts)
    if args.write:
        write_inventory(payload)
    print(json.dumps({"unit_count": payload["unit_count"], "source_pdf_exists": payload["source_pdf_exists"]}, indent=2))


if __name__ == "__main__":
    main()
