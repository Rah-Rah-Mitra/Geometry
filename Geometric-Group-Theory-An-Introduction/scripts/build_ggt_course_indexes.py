"""Build geometric group theory book, part, chapter, and source-map indexes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from ggt_inventory import BACK_MATTER, ENTRIES, PARTS, SOURCE_SPAN_NOTES, source_map, write_source_map  # noqa: E402


def write_markdown_notebook(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = new_notebook(cells=[new_markdown_cell(text.strip() + "\n")])
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    nbformat.write(nb, path)


def canonical_link(entry: dict[str, object]) -> str:
    return f"{entry['folder']}/{entry['notebook']}"


def build_book_index() -> str:
    lines = [
        "# Geometric Group Theory: An Introduction - Standalone Notebook Course",
        "",
        "This is an original executable notebook course built from the local Clara Loeh PDF as a source map, not as copied text. The notebooks teach geometric group theory through generated Cayley graphs, quasi-isometry experiments, hyperbolic graph diagnostics, growth and amenability checks, and boundary-at-infinity visuals.",
        "",
        "## Source Notes",
        "",
    ]
    for note in SOURCE_SPAN_NOTES:
        lines.append(f"- {note}")
    lines.extend(["", "## Parts", ""])
    for part in PARTS:
        lines.append(
            f"- [{part['label']}: {part['title']}]({part['folder']}/00-part-index.ipynb) - "
            f"printed pp. {part['printed_span']}; PDF pp. {part['pdf_span']}; {part['focus']}."
        )
    lines.extend(["", "## Course Units", ""])
    for entry in ENTRIES:
        lines.append(
            f"- [{entry['label']}: {entry['title']}]({entry['folder']}/00-index.ipynb) - "
            f"[canonical notebook]({canonical_link(entry)}); printed pp. {entry['printed_span']}; "
            f"PDF pp. {entry['pdf_span']}; {entry['focus']}."
        )
    lines.extend(["", "## Back Matter Inventory", ""])
    for item in BACK_MATTER:
        lines.append(f"- {item['title']}: printed pp. {item['printed_span']}; PDF pp. {item['pdf_span']}.")
    lines.extend(
        [
            "",
            "## Generated Course Assets",
            "",
            "- Source map JSON: `artifacts/source-map/checks/source-map.json` and `source-map.json`.",
            "- Chapter artifacts: `artifacts/chapter-01/` through `artifacts/chapter-09/`.",
            "- Appendix artifacts: `artifacts/appendix-a/`.",
            "",
            "## Validation",
            "",
            "Run the book-local artifact generator, compile check, index builder, notebook audit, visual audit, limited nbclient execution, optional full execution, and `git diff --check -- Geometric-Group-Theory-An-Introduction` from the workspace root.",
        ]
    )
    return "\n".join(lines)


def build_part_index(part: dict[str, object], entries: list[dict[str, object]]) -> str:
    lines = [
        f"# {part['label']}: {part['title']}",
        "",
        "[Back to Book Index](../00-book-index.ipynb)",
        "",
        f"- Source span: printed pp. {part['printed_span']}; PDF pp. {part['pdf_span']}",
        f"- Focus: {part['focus']}",
        "",
        "## Units",
        "",
    ]
    for entry in entries:
        folder_name = str(entry["folder"]).split("/")[-1]
        lines.append(f"- [{entry['label']}: {entry['title']}]({folder_name}/00-index.ipynb) - {entry['focus']}.")
    return "\n".join(lines)


def build_unit_index(entry: dict[str, object]) -> str:
    topics = "\n".join(f"- {topic}" for topic in entry["topics"])
    return f"""
# {entry['label']}: {entry['title']}

[Back to Book Index](../../00-book-index.ipynb)

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
    for part in PARTS:
        entries = [entry for entry in ENTRIES if str(entry["folder"]).startswith(str(part["folder"]) + "/")]
        write_markdown_notebook(BOOK_ROOT / str(part["folder"]) / "00-part-index.ipynb", build_part_index(part, entries))
    for entry in ENTRIES:
        write_markdown_notebook(BOOK_ROOT / str(entry["folder"]) / "00-index.ipynb", build_unit_index(entry))
    source_artifact = write_source_map()
    (BOOK_ROOT / "source-map.json").write_text(json.dumps(source_map(), indent=2, sort_keys=True), encoding="utf-8")
    print(f"Updated book index, {len(PARTS)} part indexes, {len(ENTRIES)} unit indexes, and {_rel(source_artifact)}.")


def _rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


if __name__ == "__main__":
    main()

