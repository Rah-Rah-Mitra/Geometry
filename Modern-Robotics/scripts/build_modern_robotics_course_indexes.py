"""Build book, part, and chapter index notebooks for Modern Robotics."""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf

SCRIPT_ROOT = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_ROOT.parent
sys.path.insert(0, str(SCRIPT_ROOT))

from modern_robotics_inventory import AUTHORS, BOOK_TITLE, CHAPTERS, PARTS, PDF_FILENAME, chapters_for_part


def _write_markdown_notebook(path: Path, markdown: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    nb = nbf.v4.new_notebook()
    nb["cells"] = [nbf.v4.new_markdown_cell(markdown.strip() + "\n")]
    nbf.write(nb, path)


def chapter_dir(chapter) -> Path:
    return BOOK_ROOT / chapter.part_slug / chapter.slug


def build_book_index() -> None:
    lines = [
        f"# {BOOK_TITLE}",
        "",
        f"Standalone visualization-first notebook course based on source orientation from {AUTHORS}.",
        "",
        f"Source PDF kept locally as `{PDF_FILENAME}`. Printed pages map to PDF pages by `pdf_page = printed_page + 18`.",
        "",
        "## Course Map",
        "",
    ]
    for part_slug, part_title in PARTS:
        lines.append(f"### [{part_title}]({part_slug}/00-part-index.ipynb)")
        for chapter in chapters_for_part(part_slug):
            rel = f"{part_slug}/{chapter.slug}/{chapter.notebook}"
            lines.append(f"- [{chapter.title}]({rel}) - printed pages {chapter.printed_start}-{chapter.printed_end}")
        lines.append("")
    lines.extend(
        [
            "## Course Contract",
            "",
            "Each chapter notebook is original prose with generated diagrams, plots, computational checks, and applied labs. The textbook PDF is used only for structure and source orientation; it is not copied into the course.",
        ]
    )
    _write_markdown_notebook(BOOK_ROOT / "00-book-index.ipynb", "\n".join(lines))


def build_part_indexes() -> None:
    for part_slug, part_title in PARTS:
        lines = [f"# {part_title}", "", "## Notebooks", ""]
        for chapter in chapters_for_part(part_slug):
            rel = f"{chapter.slug}/{chapter.notebook}"
            lines.append(f"- [{chapter.title}]({rel}) - {chapter.question}")
        _write_markdown_notebook(BOOK_ROOT / part_slug / "00-part-index.ipynb", "\n".join(lines))


def build_chapter_indexes() -> None:
    for chapter in CHAPTERS:
        lines = [
            f"# {chapter.title}",
            "",
            f"- Canonical notebook: [{chapter.notebook}]({chapter.notebook})",
            f"- Printed pages: {chapter.printed_start}-{chapter.printed_end}",
            f"- PDF pages: {chapter.pdf_start}-{chapter.pdf_end}",
            f"- Chapter question: {chapter.question}",
            "",
            "## Visual Storyboard",
            "",
            f"- Main visual focus: {chapter.visual_focus}",
            f"- Representation: {chapter.visual_kind}",
            f"- Inspection target: {chapter.inspection_target}",
        ]
        _write_markdown_notebook(chapter_dir(chapter) / "00-index.ipynb", "\n".join(lines))


def main() -> None:
    build_book_index()
    build_part_indexes()
    build_chapter_indexes()
    print(f"Built indexes for {len(CHAPTERS)} Modern Robotics notebooks.")


if __name__ == "__main__":
    main()

