"""Build Basic Topology book and unit indexes."""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

from bt_inventory import BACK_MATTER, ENTRIES, SOURCE_SPAN_NOTES

BOOK_ROOT = Path(__file__).resolve().parents[1]


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "version": "3.13"}
    nbformat.write(nb, path)


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Basic Topology - Standalone Notebook Course",
        "",
        "This course is an original executable notebook edition of M. A. Armstrong's *Basic Topology*. It uses the local PDFs only for source orientation and replaces passive reading with generated diagrams, plots, algebra checks, and computational labs.",
        "",
        "## Source Notes",
        "",
    ]
    for note in SOURCE_SPAN_NOTES:
        lines.append(f"- {note}")
    lines.extend(["", "## Course Units", ""])
    for entry in ENTRIES:
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({canonical_link(entry)}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}"
        )
    lines.extend(["", "## Back Matter Inventory", ""])
    for item in BACK_MATTER:
        lines.append(f"- {item['title']}: printed pp. {item['printed_span']}; PDF pp. {item['pdf_span']}")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run the book-local index builder, compile check, notebook audit, visual audit, limited execution, and `git diff --check` from the workspace root.",
        ]
    )
    return "\n".join(lines)


def build_unit_index(entry: dict[str, object]) -> str:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{entry['notebook']}]({entry['notebook']})
- Source span: printed pp. {entry['printed_span']}; PDF pp. {entry['pdf_span']}
- Sections: {entry['sections']}
- Focus: {entry['focus']}

## Topics

{topics}

## Artifact Root

Generated diagrams, interactive HTML, and check JSON for this unit live under
`artifacts/{entry['artifact']}/`.
"""


def main() -> None:
    missing = []
    for entry in ENTRIES:
        canonical = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
        if not canonical.exists():
            missing.append(canonical)
    if missing:
        raise FileNotFoundError("\n".join(str(path) for path in missing))

    write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", build_book_index())
    for entry in ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_unit_index(entry))
    print(f"Updated book index and {len(ENTRIES)} unit indexes.")


if __name__ == "__main__":
    main()
