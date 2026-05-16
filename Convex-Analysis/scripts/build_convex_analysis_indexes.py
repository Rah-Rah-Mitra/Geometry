"""Rebuild Convex Analysis course indexes and source-map inventory."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.section_catalog import PDF_OFFSET, parts, sections, sections_by_part, source_map_records  # noqa: E402


def write_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(markdown.strip() + "\n")])
    nb.metadata["course"] = "Convex Analysis"
    nbformat.write(nb, path)


def write_source_map(records: list[dict[str, object]]) -> None:
    inventory = BOOK_ROOT / "inventory"
    inventory.mkdir(parents=True, exist_ok=True)
    (inventory / "source_map.json").write_text(
        json.dumps(
            {
                "book": "Convex Analysis",
                "author": "R. Tyrrell Rockafellar",
                "pdf": "Convex Analysis.pdf",
                "body_page_rule": f"pdf_page = printed_page + {PDF_OFFSET}",
                "copyright_guard": "Original course prose and synthetic visuals only; no copied textbook text, screenshots, crops, or figures.",
                "sections": records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    with (inventory / "source_map.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
    lines = [
        "# Convex Analysis Source Map",
        "",
        "The local PDF is used for structure, terminology, and page orientation only. Course prose, code, and visuals are original.",
        "",
        f"Body pages map by `pdf_page = printed_page + {PDF_OFFSET}`.",
        "",
        "| Section | Part | Printed pages | PDF pages | Notebook | Focus |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in records:
        lines.append(
            f"| {item['number']}. {item['title']} | {item['part']}. {item['part_title']} | "
            f"{item['printed_start']}-{item['printed_end']} | {item['pdf_start']}-{item['pdf_end']} | "
            f"`{item['folder']}/{item['notebook']}` | {item['focus']} |"
        )
    (inventory / "source_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_storyboard() -> None:
    inventory = BOOK_ROOT / "inventory"
    lines = [
        "# Visualization Storyboard",
        "",
        "Every section notebook uses a synthetic, inspectable convex-geometry visual plus a proof or dependency map. The recurring audit target is not a fixed visual count; it is whether a reader can inspect the central invariant without opening the PDF.",
        "",
    ]
    for part in parts():
        lines.append(f"## Part {part['number']}: {part['title']}")
        for section in sections_by_part()[part["number"]]:
            lines.append(
                f"- Section {section['number']}: {section['title']} - {section['visual_story']} "
                f"Check: {section['check']}"
            )
        lines.append("")
    (inventory / "visual_storyboard.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> None:
    records = source_map_records()
    write_source_map(records)
    write_storyboard()

    book_lines = [
        "# Convex Analysis - Visualization-First Notebook Course",
        "",
        "This standalone course follows the numbered-section structure of Rockafellar's local PDF. It uses original exposition, synthetic diagrams, numerical checks, and proof-state maps; it does not copy textbook prose or figures.",
        "",
        f"Source rule: body printed page `p` maps to PDF page `p + {PDF_OFFSET}`.",
        "",
    ]
    for part in parts():
        book_lines.append(f"## Part {part['number']}: {part['title']}")
        book_lines.append(f"- [Part index]({part['slug']}/00-part-index.ipynb)")
        for section in sections_by_part()[part["number"]]:
            book_lines.append(
                f"- [{section['number']:02d}. {section['title']}]({section['folder']}/00-index.ipynb) - "
                f"[canonical notebook]({section['folder']}/{section['notebook']}); "
                f"printed pages {section['printed_start']}-{section['printed_end']}; {section['focus']}."
            )
        book_lines.append("")
    book_lines.extend(
        [
            "## Inventory",
            "- [Source map](inventory/source_map.md)",
            "- [Visualization storyboard](inventory/visual_storyboard.md)",
        ]
    )
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(book_lines))

    for part in parts():
        part_sections = sections_by_part()[part["number"]]
        part_lines = [
            f"# Part {part['number']}: {part['title']}",
            "",
            "[Back to book index](../00-book-index.ipynb)",
            "",
        ]
        for section in part_sections:
            part_lines.append(
                f"- [{section['number']:02d}. {section['title']}]({section['slug']}/00-index.ipynb) - "
                f"[canonical notebook]({section['slug']}/{section['notebook']}); "
                f"PDF pages {section['pdf_start']}-{section['pdf_end']}; {section['visual_story']}"
            )
        write_notebook(BOOK_ROOT / part["slug"] / "00-part-index.ipynb", "\n".join(part_lines))

        for section in part_sections:
            section_lines = [
                f"# Section {section['number']}: {section['title']}",
                "",
                f"[Back to Part {part['number']} index](../00-part-index.ipynb)",
                "",
                f"- Canonical notebook: [{section['notebook']}]({section['notebook']})",
                f"- Source span: printed pages {section['printed_start']}-{section['printed_end']}; PDF pages {section['pdf_start']}-{section['pdf_end']}",
                f"- Artifact subtree: `artifacts/{section['artifact_key']}`",
                f"- Visual center: {section['visual_story']}",
                f"- Check: {section['check']}",
                "",
                "The notebook is original course material and should be revised directly for deeper section-specific teaching passes.",
            ]
            write_notebook(BOOK_ROOT / section["folder"] / "00-index.ipynb", "\n".join(section_lines))
            (BOOK_ROOT / "artifacts" / section["artifact_key"] / "figures").mkdir(parents=True, exist_ok=True)
            (BOOK_ROOT / "artifacts" / section["artifact_key"] / "checks").mkdir(parents=True, exist_ok=True)
            (BOOK_ROOT / "artifacts" / section["artifact_key"] / "tables").mkdir(parents=True, exist_ok=True)

    print(f"Updated Convex Analysis indexes for {len(records)} sections across {len(parts())} parts.")


if __name__ == "__main__":
    main()

