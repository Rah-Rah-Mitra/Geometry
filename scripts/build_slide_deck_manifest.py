"""Build and check the Geometry lecture slide deck manifest.

The manifest is an index of planned, chapter-authored lecture decks. It does
not generate deck HTML, notes, figures, or exports.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COURSE_MANIFEST = ROOT / "course-manifest.json"
DEFAULT_OUTPUT = ROOT / "slide-deck-manifest.json"

EXPECTED_COURSE_COUNT = 65
EXPECTED_LESSON_COUNT = 971
DESIGN_SYSTEM_VERSION = "lecture-design-system-2026-05-23"

ROW_FIELDS = [
    "course_root",
    "course_title",
    "chapter_id",
    "chapter_title",
    "source_span",
    "pdf_path",
    "notebook_path",
    "artifact_subtree",
    "deck_path",
    "notes_path",
    "worker_scope",
]

SOURCE_MAP_FILES = [
    "source_map.json",
    "source-map.json",
    "SOURCE_MAP.json",
    "inventory/source-map.json",
    "inventory/source_map.json",
    "source/source-map.json",
    "source/source_map.json",
    "indexes/chapters.json",
    "source-map.md",
    "SOURCE_MAP.md",
    "inventory/source-map.md",
    "inventory/source_map.md",
    "source/source-map.md",
]

COMMON_ARTIFACT_LEAVES = {
    "checks",
    "data",
    "figures",
    "html",
    "images",
    "metadata",
    "slides",
    "tables",
}


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm_rel(value: str | Path) -> str:
    text = str(value).replace("\\", "/").strip()
    text = re.sub(r"^\./", "", text)
    return text.strip("/")


def strip_markdown(value: str) -> str:
    value = value.replace("`", "")
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" .;")


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("_", "-")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "chapter"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_agents(course_root: Path) -> str:
    agents_path = course_root / "AGENTS.md"
    if not agents_path.exists():
        return ""
    return agents_path.read_text(encoding="utf-8", errors="replace")


def markdown_cells(notebook: dict[str, Any]) -> list[str]:
    cells: list[str] = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        cells.append("".join(source) if isinstance(source, list) else str(source))
    return cells


def notebook_text(path: Path) -> str:
    try:
        notebook = read_json(path)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid notebook JSON in {rel_posix(path)}: {exc}") from exc
    return "\n\n".join(markdown_cells(notebook))


def split_md_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def markdown_tables(text: str) -> list[tuple[list[str], list[dict[str, str]]]]:
    lines = text.splitlines()
    tables: list[tuple[list[str], list[dict[str, str]]]] = []
    i = 0
    while i < len(lines) - 1:
        if not lines[i].lstrip().startswith("|") or not re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            i += 1
            continue
        headers = [slugify(strip_markdown(cell)).replace("-", "_") for cell in split_md_row(lines[i])]
        rows: list[dict[str, str]] = []
        i += 2
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            values = split_md_row(lines[i])
            if len(values) >= len(headers):
                rows.append(dict(zip(headers, values, strict=False)))
            i += 1
        tables.append((headers, rows))
    return tables


def clean_span_text(value: str) -> str:
    value = strip_markdown(value)
    value = re.sub(r"\bChapter question:.*$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"##\s+Chapter Question.*$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\bThis notebook is an original.*$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\bI used the source.*$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\bThe source was used.*$", "", value, flags=re.IGNORECASE).strip()
    value = re.sub(r"\s+", " ", value).strip(" ;")
    return value if value.endswith(".") else f"{value}."


def extract_page_pair(text: str) -> str:
    text = strip_markdown(text)
    page_atom = r"(?:\d+|[ivxlcdm]+)"
    page = rf"({page_atom}\s*(?:-|/|to)\s*{page_atom}|{page_atom})"
    patterns = [
        rf"printed\s+(?:pages?|pp\.?|p\.?)\s*[:.]?\s*{page}\s*(?:and|;|,|/|\(|\s)+\s*(?:physical\s+)?PDF\s+(?:pages?|pp\.?|p\.?)\s*[:.]?\s*{page}",
        rf"(?:physical\s+)?PDF(?:\s+extraction)?\s+(?:pages?|pp\.?|p\.?)\s*[:.]?\s*{page}[^.;:]+?printed(?:\s+textbook)?\s+(?:pages?|pp\.?|p\.?)\s*[:.]?\s*{page}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if not match:
            continue
        first, second = (re.sub(r"\s*(?:-|/|to)\s*", "-", group) for group in match.groups())
        if match.group(0).lower().lstrip().startswith("pdf"):
            printed, pdf = second, first
        else:
            printed, pdf = first, second
        return f"printed pages {printed}; PDF pages {pdf}."
    match = re.search(
        rf"PDF\s+page\s+({page_atom})\s+is\s+printed\s+page\s+({page_atom}).+?"
        rf"PDF\s+page\s+({page_atom})\s+is\s+printed\s+page\s+({page_atom})",
        text,
        re.I,
    )
    if match:
        return f"printed pages {match.group(2)}-{match.group(4)}; PDF pages {match.group(1)}-{match.group(3)}."
    match = re.search(
        rf"Printed\s+p\.?\s*({page_atom})\s+is\s+PDF\s+page\s+({page_atom}).+?"
        rf"Printed\s+p\.?\s*({page_atom})\s+is\s+PDF\s+page\s+({page_atom})",
        text,
        re.I,
    )
    if match:
        return f"printed pages {match.group(1)}-{match.group(3)}; PDF pages {match.group(2)}-{match.group(4)}."
    match = re.search(
        rf"physical\s+extraction\s+pages\s+{page}[^.;:]+?printed\s+pages\s+{page}",
        text,
        re.I,
    )
    if match:
        pdf = re.sub(r"\s*(?:-|/|to)\s*", "-", match.group(1))
        printed = re.sub(r"\s*(?:-|/|to)\s*", "-", match.group(2))
        return f"printed pages {printed}; PDF pages {pdf}."
    match = re.search(rf"(?:physical\s+)?PDF\s+(?:pages?|pp\.?)\s*[:.]?\s*{page}", text, re.I)
    if match:
        pdf = re.sub(r"\s*(?:-|/|to)\s*", "-", match.group(1))
        return f"PDF pages {pdf}."
    return ""


def extract_notebook_source_span(path: Path) -> str:
    text = notebook_text(path)
    page_pair = extract_page_pair(text)
    if page_pair:
        return page_pair
    patterns = [
        r"(?is)##\s+Source Span\s*(.+?)(?=\n##\s+|\Z)",
        r"(?is)(?:\*\*)?Source span(?:\.|:)?(?:\*\*)?\s*(.+?)(?=\n\s*\n|\Z)",
        r"(?is)(?:\*\*)?Source orientation(?:\.|:)?(?:\*\*)?\s*(.+?)(?=\n\s*\n|\Z)",
        r"(?is)(?:printed|source)\s+(?:pages?|pp\.)\s*\d+[^.\n]{0,160}(?:PDF|physical)[^.\n]{0,160}\.",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = match.group(1) if match.groups() else match.group(0)
            return clean_span_text(value)

    for headers, rows in markdown_tables(text):
        if not rows:
            continue
        header_set = set(headers)
        if not ({"printed_pages", "printed_pp"} & header_set) or not ({"pdf_pages", "physical_pages"} & header_set):
            continue
        row = rows[0]
        printed = row.get("printed_pages") or row.get("printed_pp")
        pdf = row.get("pdf_pages") or row.get("physical_pages")
        if printed and pdf:
            return f"printed pages {strip_markdown(printed)}; PDF pages {strip_markdown(pdf)}."
    return ""


def parse_span(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list) and len(value) == 2:
        return f"{value[0]}-{value[1]}"
    if isinstance(value, tuple) and len(value) == 2:
        return f"{value[0]}-{value[1]}"
    text = str(value).strip()
    text = text.replace("pp.", "").replace("pages", "").strip()
    return text


def first_present(raw: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in raw and raw[key] not in (None, ""):
            return raw[key]
    return None


def extract_offset(meta: Any, agents_text: str) -> int | None:
    if isinstance(meta, dict):
        for key in ("printed_to_pdf_offset", "body_page_offset", "pdf_page_offset"):
            value = meta.get(key)
            if isinstance(value, int):
                return value
            if isinstance(value, str) and value.strip().isdigit():
                return int(value.strip())
    haystack = json.dumps(meta, ensure_ascii=False) if not isinstance(meta, str) else meta
    haystack = f"{haystack}\n{agents_text}"
    match = re.search(r"(?:physical_)?pdf_?page\s*=\s*printed_?page\s*\+\s*(\d+)", haystack, re.I)
    if match:
        return int(match.group(1))
    match = re.search(r"printed\s+page\s+1\s+starts\s+at\s+physical\s+PDF\s+page\s+(\d+)", haystack, re.I)
    if match:
        return int(match.group(1)) - 1
    return None


def add_offset(span: str, offset: int | None) -> str:
    if offset is None:
        return ""
    match = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", span)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        return f"{start + offset}-{end + offset}"
    match = re.match(r"^\s*(\d+)\s*$", span)
    if match:
        return str(int(match.group(1)) + offset)
    return ""


def source_span_from_raw(raw: dict[str, Any], offset: int | None) -> str:
    existing = first_present(raw, ("source_span", "span"))
    if isinstance(existing, str) and re.search(r"(printed|pdf|physical|page)", existing, re.I):
        return clean_span_text(existing)

    printed = first_present(raw, ("printed_span", "printed", "printed_pages", "source_pages"))
    if printed is None and raw.get("printed_start") is not None:
        printed_end = raw.get("printed_end", raw.get("printed_start"))
        printed = f"{raw['printed_start']}-{printed_end}"

    pdf = first_present(raw, ("pdf_span", "pdf_pages", "physical_pages", "physical_pdf_pages"))
    if pdf is None and raw.get("pdf_start") is not None:
        pdf_end = raw.get("pdf_end", raw.get("pdf_start"))
        pdf = f"{raw['pdf_start']}-{pdf_end}"

    printed_span = parse_span(printed)
    pdf_span = parse_span(pdf)
    if printed_span and not pdf_span:
        pdf_span = add_offset(printed_span, offset)

    pieces: list[str] = []
    if printed_span:
        pieces.append(f"printed pages {printed_span}")
    if pdf_span:
        pieces.append(f"PDF pages {pdf_span}")
    return "; ".join(pieces) + ("." if pieces else "")


def span_compare_key(value: str) -> str:
    printed = re.search(r"printed pages? (\d+)(?:-(\d+))?", value, re.I)
    pdf = re.search(r"PDF pages? (\d+)(?:-(\d+))?", value, re.I)
    pieces: list[str] = []
    if printed:
        pieces.append(f"printed:{printed.group(1)}-{printed.group(2) or printed.group(1)}")
    if pdf:
        pieces.append(f"pdf:{pdf.group(1)}-{pdf.group(2) or pdf.group(1)}")
    return "|".join(pieces) if pieces else re.sub(r"\W+", "", value.lower())


def collect_pdf_names(obj: Any) -> list[str]:
    names: list[str] = []
    if isinstance(obj, dict):
        for value in obj.values():
            names.extend(collect_pdf_names(value))
    elif isinstance(obj, list):
        for value in obj:
            names.extend(collect_pdf_names(value))
    elif isinstance(obj, str):
        for match in re.finditer(r"([A-Za-z0-9][^`\"'\n\r]*?\.(?:pdf|djvu))", obj, re.I):
            names.append(match.group(1).strip())
    return names


def pdf_name_from_raw(raw: dict[str, Any]) -> str:
    for key in ("pdf_file", "source_pdf", "pdf_filename", "source_file"):
        value = raw.get(key)
        if isinstance(value, str) and re.search(r"\.(pdf|djvu)$", value, re.I):
            return value
    return ""


def source_entry_dicts(obj: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            keys = set(value)
            has_source = bool(
                keys
                & {
                    "printed",
                    "printed_pages",
                    "printed_span",
                    "printed_start",
                    "pdf",
                    "pdf_pages",
                    "pdf_span",
                    "pdf_start",
                    "physical_pages",
                    "source_span",
                }
            )
            has_identity = bool(
                keys
                & {
                    "artifact_key",
                    "filename",
                    "folder",
                    "folder_path",
                    "id",
                    "notebook",
                    "notebook_path",
                    "path",
                    "slug",
                    "title",
                }
            )
            if has_source and has_identity:
                entries.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return entries


def candidate_notebooks(raw: dict[str, Any]) -> list[str]:
    candidates: set[str] = set()
    direct_values = [
        raw.get("notebook"),
        raw.get("notebook_path"),
        raw.get("course_path"),
        raw.get("path"),
    ]
    for value in direct_values:
        if isinstance(value, str) and value.endswith(".ipynb"):
            candidates.add(norm_rel(value))

    filename = raw.get("filename")
    if isinstance(filename, str) and filename.endswith(".ipynb"):
        candidates.add(norm_rel(filename))
        prefixes = [
            raw.get("folder_path"),
            raw.get("folder"),
            raw.get("part"),
            raw.get("part_slug"),
            raw.get("slug"),
        ]
        for prefix in prefixes:
            if isinstance(prefix, str) and prefix:
                candidates.add(norm_rel(f"{prefix}/{filename}"))
        part = raw.get("part") or raw.get("part_slug")
        folder = raw.get("folder")
        if isinstance(part, str) and isinstance(folder, str):
            candidates.add(norm_rel(f"{part}/{folder}/{filename}"))

    normalized: set[str] = set()
    for candidate in candidates:
        parts = Path(candidate).parts
        if parts and (ROOT / parts[0]).exists():
            normalized.add(norm_rel(Path(*parts[1:]).as_posix()))
        normalized.add(candidate)
    return sorted(normalized)


def candidate_folders(raw: dict[str, Any], notebooks: list[str]) -> list[str]:
    candidates: set[str] = set()
    for key in ("folder_path", "folder", "part_slug", "part"):
        value = raw.get(key)
        if isinstance(value, str) and value:
            candidates.add(norm_rel(value))
    part = raw.get("part") or raw.get("part_slug")
    folder = raw.get("folder")
    if isinstance(part, str) and isinstance(folder, str):
        candidates.add(norm_rel(f"{part}/{folder}"))
    for notebook in notebooks:
        parent = str(Path(notebook).parent).replace("\\", "/")
        if parent and parent != ".":
            candidates.add(norm_rel(parent))
    return sorted(candidates)


@dataclass
class SourceEntry:
    source_file: str
    notebooks: list[str]
    folders: list[str]
    title: str
    source_span: str
    pdf_name: str
    artifact_key: str
    raw: dict[str, Any]


def entry_from_raw(raw: dict[str, Any], source_file: str, offset: int | None) -> SourceEntry:
    notebooks = candidate_notebooks(raw)
    folders = candidate_folders(raw, notebooks)
    title = str(raw.get("title") or raw.get("label") or "").strip()
    artifact_key = str(
        raw.get("artifact_key")
        or raw.get("artifact_topic")
        or raw.get("artifact_subtree")
        or raw.get("id")
        or ""
    ).strip()
    return SourceEntry(
        source_file=source_file,
        notebooks=notebooks,
        folders=folders,
        title=title,
        source_span=source_span_from_raw(raw, offset),
        pdf_name=pdf_name_from_raw(raw),
        artifact_key=norm_rel(artifact_key) if artifact_key else "",
        raw=raw,
    )


def parse_agents_source_entries(course_root: Path, agents_text: str) -> list[SourceEntry]:
    entries: list[SourceEntry] = []
    offset = extract_offset({}, agents_text)
    for headers, rows in markdown_tables(agents_text):
        header_set = set(headers)
        has_folder = "folder" in header_set or "course_path" in header_set or "notebook" in header_set
        has_printed = bool({"printed_pages", "printed", "printed_pp"} & header_set)
        has_pdf = bool({"pdf_pages", "pdf", "physical_pages"} & header_set)
        if not (has_folder and (has_printed or has_pdf)):
            continue
        for row in rows:
            raw: dict[str, Any] = {
                "title": row.get("title") or row.get("unit") or row.get("label") or "",
                "folder": strip_markdown(row.get("folder", "")),
                "notebook": strip_markdown(row.get("notebook", "")),
                "course_path": strip_markdown(row.get("course_path", "")),
                "printed_pages": strip_markdown(row.get("printed_pages") or row.get("printed") or row.get("printed_pp") or ""),
                "pdf_pages": strip_markdown(row.get("pdf_pages") or row.get("pdf") or row.get("physical_pages") or ""),
                "focus": strip_markdown(row.get("focus", "")),
            }
            if raw["folder"] or raw["notebook"] or raw["course_path"]:
                entries.append(entry_from_raw(raw, rel_posix(course_root / "AGENTS.md"), offset))
    return entries


def load_source_objects(course_root: Path) -> list[tuple[Path, Any]]:
    objects: list[tuple[Path, Any]] = []
    for relative in SOURCE_MAP_FILES:
        path = course_root / relative
        if not path.exists():
            continue
        if path.suffix.lower() == ".json":
            objects.append((path, read_json(path)))
        elif path.suffix.lower() == ".md":
            objects.append((path, path.read_text(encoding="utf-8", errors="replace")))
    return objects


def parse_md_source_entries(path: Path, text: str, agents_text: str) -> list[SourceEntry]:
    entries: list[SourceEntry] = []
    offset = extract_offset(text, agents_text)
    for headers, rows in markdown_tables(text):
        header_set = set(headers)
        notebook_key = next((key for key in ("course_path", "notebook", "path") if key in header_set), "")
        if not notebook_key:
            continue
        if not ({"printed_pages", "printed", "printed_pp"} & header_set or {"pdf_pages", "pdf", "physical_pages"} & header_set):
            continue
        for row in rows:
            raw = {
                "title": row.get("title") or row.get("unit") or row.get("label") or "",
                "notebook": strip_markdown(row.get(notebook_key, "")),
                "folder": str(Path(strip_markdown(row.get(notebook_key, ""))).parent).replace("\\", "/"),
                "printed_pages": strip_markdown(row.get("printed_pages") or row.get("printed") or row.get("printed_pp") or ""),
                "pdf_pages": strip_markdown(row.get("pdf_pages") or row.get("pdf") or row.get("physical_pages") or ""),
                "focus": strip_markdown(row.get("focus", "")),
            }
            if raw["notebook"].endswith(".ipynb"):
                entries.append(entry_from_raw(raw, rel_posix(path), offset))
    return entries


class CourseSourceIndex:
    def __init__(self, course_root: Path, agents_text: str) -> None:
        self.course_root = course_root
        self.agents_text = agents_text
        self.entries: list[SourceEntry] = []
        self.pdf_paths = self._load_pdf_paths()
        self.artifact_dirs = self._artifact_dirs()
        self._load_entries()

    def _load_pdf_paths(self) -> list[str]:
        names: list[str] = []
        for _, obj in load_source_objects(self.course_root):
            names.extend(collect_pdf_names(obj))
        names.extend(collect_pdf_names(self.agents_text))

        resolved: list[str] = []
        for name in names:
            if re.search(r"solution|answer", name, re.I):
                continue
            path = self.course_root / name
            if not path.exists():
                basename = Path(name).name.lower()
                matches = [candidate for candidate in self.course_root.glob("*") if candidate.name.lower() == basename]
                if matches:
                    path = matches[0]
            if path.exists() and path.suffix.lower() in {".pdf", ".djvu"}:
                resolved.append(rel_posix(path))

        for path in sorted(self.course_root.glob("*")):
            if path.suffix.lower() not in {".pdf", ".djvu"}:
                continue
            if re.search(r"solution|answer", path.name, re.I):
                continue
            resolved.append(rel_posix(path))

        return sorted(dict.fromkeys(resolved))

    def _artifact_dirs(self) -> set[str]:
        artifacts = self.course_root / "artifacts"
        if not artifacts.exists():
            return set()
        dirs: set[str] = set()
        for path in artifacts.rglob("*"):
            if not path.is_dir():
                continue
            rel = path.relative_to(artifacts).as_posix()
            if any(part in COMMON_ARTIFACT_LEAVES for part in Path(rel).parts):
                continue
            dirs.add(rel)
        return dirs

    def _load_entries(self) -> None:
        seen: set[tuple[str, str, str, str]] = set()
        for path, obj in load_source_objects(self.course_root):
            path_rel = rel_posix(path)
            if isinstance(obj, str):
                parsed = parse_md_source_entries(path, obj, self.agents_text)
            else:
                offset = extract_offset(obj, self.agents_text)
                parsed = [entry_from_raw(raw, path_rel, offset) for raw in source_entry_dicts(obj)]
            for entry in parsed:
                key = (
                    "|".join(entry.notebooks),
                    "|".join(entry.folders),
                    entry.source_span,
                    entry.artifact_key,
                )
                if key not in seen:
                    self.entries.append(entry)
                    seen.add(key)

        for entry in parse_agents_source_entries(self.course_root, self.agents_text):
            key = (
                "|".join(entry.notebooks),
                "|".join(entry.folders),
                entry.source_span,
                entry.artifact_key,
            )
            if key not in seen:
                self.entries.append(entry)
                seen.add(key)

    def match(self, notebook_rel_course: str, title: str) -> tuple[list[SourceEntry], bool]:
        notebook_rel_course = norm_rel(notebook_rel_course)
        parent = norm_rel(Path(notebook_rel_course).parent.as_posix())
        exact = [entry for entry in self.entries if notebook_rel_course in entry.notebooks]
        exact = self._dedupe_matches(exact)
        if exact:
            return exact, len({span_compare_key(entry.source_span) for entry in exact if entry.source_span}) > 1

        parent_matches: list[SourceEntry] = []
        parent_last = Path(parent).name
        for entry in self.entries:
            for folder in entry.folders:
                folder = norm_rel(folder)
                if folder == parent or folder == parent_last or parent.endswith(f"/{folder}") or folder.endswith(f"/{parent_last}"):
                    parent_matches.append(entry)
                    break
        parent_matches = self._dedupe_matches(parent_matches)
        if parent_matches:
            return parent_matches, len({span_compare_key(entry.source_span) for entry in parent_matches if entry.source_span}) > 1

        title_slug = slugify(title)
        title_matches = [
            entry
            for entry in self.entries
            if entry.title and (slugify(entry.title) == title_slug or title_slug.endswith(slugify(entry.title)))
        ]
        title_matches = self._dedupe_matches(title_matches)
        if len(title_matches) == 1:
            return title_matches, False

        aggregate = self.aggregate(parent, title)
        return ([aggregate], False) if aggregate else ([], False)

    def aggregate(self, parent: str, title: str) -> SourceEntry | None:
        descendants = [
            entry
            for entry in self.entries
            if any(notebook.startswith(f"{parent}/") for notebook in entry.notebooks)
            or any(folder.startswith(f"{parent}/") for folder in entry.folders)
        ]
        if not descendants:
            return None
        printed_values: list[int] = []
        pdf_values: list[int] = []
        pdf_name = ""
        for entry in descendants:
            for pair in re.findall(r"printed pages? (\d+)(?:-(\d+))?", entry.source_span):
                printed_values.extend(int(value) for value in pair if value)
            for pair in re.findall(r"PDF pages? (\d+)(?:-(\d+))?", entry.source_span):
                pdf_values.extend(int(value) for value in pair if value)
            if not pdf_name and entry.pdf_name:
                pdf_name = entry.pdf_name
        pieces: list[str] = []
        if printed_values:
            pieces.append(f"printed pages {min(printed_values)}-{max(printed_values)}")
        if pdf_values:
            pieces.append(f"PDF pages {min(pdf_values)}-{max(pdf_values)}")
        source_span = "; ".join(pieces) + ("." if pieces else "")
        volume_match = re.search(r"volume-(\d\d)", parent)
        artifact_key = f"volume-{volume_match.group(1)}" if volume_match else Path(parent).name
        return SourceEntry(
            source_file="aggregate source-map entries",
            notebooks=[],
            folders=[parent],
            title=title,
            source_span=source_span,
            pdf_name=pdf_name,
            artifact_key=artifact_key,
            raw={},
        )

    @staticmethod
    def _dedupe_matches(matches: list[SourceEntry]) -> list[SourceEntry]:
        deduped: list[SourceEntry] = []
        seen: set[tuple[str, str, str, str]] = set()
        for entry in matches:
            key = (
                "|".join(entry.notebooks),
                "|".join(entry.folders),
                span_compare_key(entry.source_span),
                entry.artifact_key,
            )
            if key not in seen:
                deduped.append(entry)
                seen.add(key)
        return deduped

    def pick_pdf_path(self, entry: SourceEntry | None) -> str:
        if entry and entry.pdf_name:
            direct = self.course_root / entry.pdf_name
            if direct.exists():
                return rel_posix(direct)
            basename = Path(entry.pdf_name).name.lower()
            for path in self.course_root.glob("*"):
                if path.name.lower() == basename:
                    return rel_posix(path)
        if not self.pdf_paths:
            return ""
        if entry:
            haystack = " ".join(
                str(entry.raw.get(key, ""))
                for key in ("part", "folder", "folder_path", "artifact_key", "id", "notebook")
            ).lower()
            if "volume-01" in haystack or "volume 1" in haystack or re.search(r"\bv1\b", haystack):
                for path in self.pdf_paths:
                    if re.search(r"(volume\s*i| i\.pdf$)", path, re.I):
                        return path
            if "volume-02" in haystack or "volume 2" in haystack or re.search(r"\bv2\b", haystack):
                for path in self.pdf_paths:
                    if re.search(r"(volume\s*ii| ii\.pdf$)", path, re.I):
                        return path
        return self.pdf_paths[0]

    def artifact_subtree(self, notebook_rel_course: str, entry: SourceEntry | None) -> str:
        parent = norm_rel(Path(notebook_rel_course).parent.as_posix())
        artifact_parent = parent.removeprefix("artifacts/")
        parent_last = Path(parent).name
        candidates: list[str] = []
        if entry:
            candidates.extend(
                candidate
                for candidate in [
                    entry.artifact_key,
                    str(entry.raw.get("artifact_key", "")),
                    str(entry.raw.get("artifact_topic", "")),
                    str(entry.raw.get("id", "")),
                    str(entry.raw.get("slug", "")),
                    str(entry.raw.get("folder_path", "")),
                    str(entry.raw.get("folder", "")),
                ]
                if candidate
            )
        volume_match = re.search(r"volume-(\d\d)", parent)
        if volume_match:
            candidates.append(f"volume-{volume_match.group(1)}")
        candidates.extend([artifact_parent, parent, parent_last])

        normalized_candidates = [norm_rel(candidate) for candidate in candidates if norm_rel(candidate)]
        for candidate in normalized_candidates:
            if candidate in self.artifact_dirs:
                return candidate
        for candidate in normalized_candidates:
            candidate_last = Path(candidate).name
            for artifact in sorted(self.artifact_dirs, key=lambda value: (-len(value), value)):
                artifact_last = Path(artifact).name
                if candidate_last == artifact_last:
                    return artifact
                if candidate_last.startswith(f"{artifact_last}-"):
                    return artifact
                if artifact_last.startswith(f"{candidate_last}-"):
                    return artifact
        for candidate in normalized_candidates:
            if candidate and candidate not in {".", ""}:
                return candidate

        prefix = re.match(r"((?:chapter|appendix|lecture|section)-[a-z0-9]+(?:-[a-z0-9]+)?)", parent_last)
        return prefix.group(1) if prefix else parent_last


def load_course_manifest() -> dict[str, Any]:
    try:
        return read_json(COURSE_MANIFEST)
    except FileNotFoundError:
        raise SystemExit(f"Missing {rel_posix(COURSE_MANIFEST)}") from None


def build_manifest() -> tuple[dict[str, Any], list[str]]:
    course_manifest = load_course_manifest()
    courses = course_manifest.get("courses", [])
    rows: list[dict[str, str]] = []
    errors: list[str] = []

    if len(courses) != EXPECTED_COURSE_COUNT:
        errors.append(f"Expected {EXPECTED_COURSE_COUNT} courses, found {len(courses)}.")

    for course in courses:
        course_root_name = course["course_dir"]
        course_root = ROOT / course_root_name
        course_title = course.get("title") or course_root_name.replace("-", " ")
        agents_path = course_root / "AGENTS.md"
        if not agents_path.exists():
            errors.append(f"Missing AGENTS.md: {course_root_name}/AGENTS.md")
        agents_text = read_agents(course_root)
        source_index = CourseSourceIndex(course_root, agents_text)

        for notebook in course.get("notebooks", []):
            if notebook.get("kind") != "lesson":
                continue
            notebook_path = ROOT / notebook["path"]
            notebook_rel_course = norm_rel(Path(notebook["path"]).relative_to(course_root_name).as_posix())
            if not notebook_path.exists():
                errors.append(f"Missing notebook: {notebook['path']}")
                notebook_span = ""
            else:
                notebook_span = extract_notebook_source_span(notebook_path)

            matches, ambiguous = source_index.match(notebook_rel_course, notebook.get("title", ""))
            source_entry = matches[0] if matches else None
            source_span = source_entry.source_span if source_entry and source_entry.source_span else notebook_span
            if ambiguous:
                errors.append(f"Ambiguous source span for {notebook['path']}")
            if not source_span:
                errors.append(f"Missing source span for {notebook['path']}")

            pdf_path = source_index.pick_pdf_path(source_entry)
            artifact_subtree = source_index.artifact_subtree(notebook_rel_course, source_entry)
            notebook_stem = Path(notebook_rel_course).stem.replace(".executed", "-executed")
            if notebook_rel_course.startswith("artifacts/") or notebook_stem.startswith("00-"):
                chapter_id = slugify(notebook_stem)
            else:
                chapter_id = slugify(Path(artifact_subtree).name)
            deck_path = f"{course_root_name}/artifacts/{artifact_subtree}/slides/{chapter_id}-lecture.html"
            notes_path = f"{course_root_name}/artifacts/{artifact_subtree}/slides/{chapter_id}-speaker-notes.json"
            notebook_parent = norm_rel(Path(notebook["path"]).parent.as_posix())
            worker_scope = (
                f"{notebook_parent}; "
                f"{course_root_name}/artifacts/{artifact_subtree}/slides"
            )

            rows.append(
                {
                    "course_root": course_root_name,
                    "course_title": course_title,
                    "chapter_id": chapter_id,
                    "chapter_title": notebook.get("title", ""),
                    "source_span": source_span,
                    "pdf_path": pdf_path,
                    "notebook_path": norm_rel(notebook["path"]),
                    "artifact_subtree": f"{course_root_name}/artifacts/{artifact_subtree}",
                    "deck_path": deck_path,
                    "notes_path": notes_path,
                    "worker_scope": worker_scope,
                }
            )

    lesson_count = len(rows)
    if lesson_count != EXPECTED_LESSON_COUNT:
        errors.append(f"Expected {EXPECTED_LESSON_COUNT} canonical lesson rows, found {lesson_count}.")

    notebook_counts = Counter(row["notebook_path"] for row in rows)
    for path, count in notebook_counts.items():
        if count > 1:
            errors.append(f"Duplicate notebook row: {path} appears {count} times.")

    deck_counts = Counter(row["deck_path"] for row in rows)
    for path, count in deck_counts.items():
        if count > 1:
            errors.append(f"Duplicate deck path: {path} appears {count} times.")

    manifest = {
        "schema_version": 1,
        "generated_by": "scripts/build_slide_deck_manifest.py",
        "design_system_version": DESIGN_SYSTEM_VERSION,
        "expected": {
            "course_count": EXPECTED_COURSE_COUNT,
            "lesson_count": EXPECTED_LESSON_COUNT,
        },
        "summary": {
            "course_count": len({row["course_root"] for row in rows}),
            "lesson_count": lesson_count,
        },
        "decks": rows,
    }
    return manifest, errors


def validate_manifest_shape(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = manifest.get("decks")
    if not isinstance(rows, list):
        return ["Manifest must contain a 'decks' list."]
    if len(rows) != EXPECTED_LESSON_COUNT:
        errors.append(f"Manifest has {len(rows)} deck rows; expected {EXPECTED_LESSON_COUNT}.")
    if len({row.get("course_root") for row in rows if isinstance(row, dict)}) != EXPECTED_COURSE_COUNT:
        errors.append(f"Manifest course coverage must be {EXPECTED_COURSE_COUNT} courses.")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"Row {index} is not an object.")
            continue
        keys = list(row)
        if keys != ROW_FIELDS:
            errors.append(f"Row {index} fields are {keys}; expected {ROW_FIELDS}.")
        for field in ROW_FIELDS:
            if not str(row.get(field, "")).strip():
                errors.append(f"Row {index} has empty {field}.")
    return errors


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", "--output", default=str(DEFAULT_OUTPUT), help="Manifest path to write or check.")
    parser.add_argument("--check", action="store_true", help="Validate that the manifest is current.")
    args = parser.parse_args(argv)

    output = Path(args.manifest)
    if not output.is_absolute():
        output = ROOT / output

    manifest, errors = build_manifest()
    errors.extend(validate_manifest_shape(manifest))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.check:
        if not output.exists():
            print(f"ERROR: Missing manifest: {rel_posix(output)}", file=sys.stderr)
            return 1
        current = read_json(output)
        if current != manifest:
            print(f"ERROR: {rel_posix(output)} is out of date; run this script without --check.", file=sys.stderr)
            return 1
        print(
            f"slide deck manifest OK: {manifest['summary']['course_count']} courses, "
            f"{manifest['summary']['lesson_count']} lesson decks planned."
        )
        return 0

    write_manifest(output, manifest)
    print(
        f"wrote {rel_posix(output)} with {manifest['summary']['course_count']} courses and "
        f"{manifest['summary']['lesson_count']} lesson decks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
