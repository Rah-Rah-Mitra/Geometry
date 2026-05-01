"""Rebuild ENEG book and chapter index notebooks."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import SOURCE_MAP  # noqa: E402


def write_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nbformat.write(nb, path)


def main() -> None:
    lines = [
        "# Euclidean and Non-Euclidean Geometries - Standalone Notebook Course",
        "",
        "This original visualization-first course follows the scanned third edition by Marvin Jay Greenberg.",
        "Generated artifacts live under `artifacts/<work-unit-folder>`.",
        "",
        "The source PDF is image-only. Rendered source pages are used only for orientation, never as notebook content.",
        "",
        "Body printed pages map to PDF pages by `pdf_page = printed_page + 18`.",
        "",
        "## Course Units",
        "",
    ]
    for item in SOURCE_MAP:
        lines.append(
            f"- [{item['kind']} {item['number']}: {item['title']}]({item['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({item['folder']}/{item['notebook']}); printed pages {item['printed']}; "
            f"PDF pages {item['pdf']}; {item['focus']}."
        )
        chapter_index = f"""# {item['kind']} {item['number']}: {item['title']}

[Back to Book Index](../00-book-index.ipynb)

- Canonical notebook: [{item['notebook']}]({item['notebook']})
- Source span: printed pages {item['printed']}; PDF pages {item['pdf']}
- Visual center: {item['focus']}
- Artifact topic: `artifacts/{item['folder']}`
"""
        write_notebook(BOOK_ROOT / item["folder"] / "00-index.ipynb", chapter_index)
    lines.extend(
        [
            "",
            "## Reference Matter",
            "",
            "Printed pages 461-484 include suggested further reading, bibliography, axioms, symbols, and indexes.",
            "Those materials are summarized through the book index and helper metadata rather than copied into notebooks.",
        ]
    )
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))
    print(f"Updated ENEG book index and {len(SOURCE_MAP)} unit indexes.")


if __name__ == "__main__":
    main()

