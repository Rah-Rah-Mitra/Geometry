"""Rebuild Geometry I book and source-unit indexes."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import geometry_i_inventory as inventory  # noqa: E402


def write_markdown_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(new_notebook(cells=[new_markdown_cell(markdown.strip() + "\n")]), path)


def build_book_index() -> str:
    lines = [
        "# Geometry I - Standalone Visualization-First Notebook Course",
        "",
        "This course is an original executable notebook edition of Marcel Berger's *Geometry I*. The source PDF remains local and is used only for chapter orientation. The notebooks teach with fresh prose, equations, code, generated diagrams, computational checks, and artifacts.",
        "",
        f"PDF source: `{inventory.PDF_SOURCE}`. Arabic printed pages follow `{inventory.PRINTED_TO_PDF_RULE}`.",
        "",
        "## Course Units",
        "",
    ]
    for entry in inventory.ENTRIES:
        path = f"{entry['folder']}/00-index.ipynb"
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({path}) - printed {entry['printed_span']}, PDF {entry['pdf_span']}."
        )
    lines.extend(["", "## Back Matter", ""])
    for item in inventory.BACK_MATTER:
        lines.append(f"- {item['title']}: printed {item['printed_span']}, PDF {item['pdf_span']}.")
    lines.extend(
        [
            "",
            "## Course Contract",
            "",
            "The notebooks stand alone from the PDF and avoid copied prose, long exercise text, screenshots, page crops, and textbook figures. Artifacts are generated under `artifacts/` and are displayed inline by the canonical notebooks.",
        ]
    )
    return "\n".join(lines)


def build_unit_index(entry: dict) -> str:
    notebook = entry["notebook"]
    lines = [
        f"# {entry['label']}: {entry['title']}",
        "",
        f"- Source span: printed `{entry['printed_span']}`, PDF `{entry['pdf_span']}`.",
        f"- Artifact topic: `artifacts/{entry['artifact_topic']}/`.",
        f"- Canonical notebook: [{notebook}]({notebook}).",
        "",
        "## Standalone Focus",
        "",
        str(entry["focus"]),
        "",
        "## Concept Map",
        "",
    ]
    for topic in entry["topics"]:
        lines.append(f"- {topic}")
    lines.extend(
        [
            "",
            "## Notebook Expectations",
            "",
            "The canonical notebook gives original exposition, visual storyboards, generated figures, an applied lab, sanity checks, and takeaways. The PDF is not needed while reading the notebook.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in inventory.ENTRIES:
        write_markdown_notebook(BOOK_ROOT / entry["folder"] / "00-index.ipynb", build_unit_index(entry))
    print(f"Wrote {1 + len(inventory.ENTRIES)} index notebooks")


if __name__ == "__main__":
    main()

