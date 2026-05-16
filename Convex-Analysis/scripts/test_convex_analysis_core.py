"""Core tests for Convex Analysis course helpers."""

from __future__ import annotations

import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.section_catalog import PDF_OFFSET, get_section, sections, sections_by_part  # noqa: E402


def test_source_page_offset_and_count() -> None:
    all_sections = sections()
    assert len(all_sections) == 39
    assert PDF_OFFSET == 18
    first = get_section(1)
    assert first["printed_start"] == 3
    assert first["pdf_start"] == 21


def test_grouping_covers_all_parts() -> None:
    grouped = sections_by_part()
    assert sorted(grouped) == list(range(1, 9))
    assert sum(len(items) for items in grouped.values()) == 39


def test_section_paths_are_book_local() -> None:
    for section in sections():
        assert section["folder"].startswith(section["part_slug"])
        assert ".." not in section["folder"]
        assert section["notebook"].endswith(".ipynb")

