"""Audit Geometry lecture slide decks without generating deck content."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from build_slide_deck_manifest import (
    DEFAULT_OUTPUT,
    EXPECTED_COURSE_COUNT,
    EXPECTED_LESSON_COUNT,
    ROOT,
    build_manifest,
    rel_posix,
)


ALLOWED_SLIDE_INFRA_SCRIPTS = {
    "audit_slide_decks.py",
    "build_slide_deck_manifest.py",
    "export_slide_deck.py",
    "validate_slide_deck_layouts.py",
}

REQUIRED_METADATA_FIELDS = [
    "course",
    "chapter_id",
    "notebook_path",
    "source_span",
    "source_pdf",
    "design_system_version",
]

COPYRIGHT_PATTERNS = [
    r"screenshot",
    r"page\s+crop",
    r"cropped\s+page",
    r"copied\s+from\s+the\s+textbook",
    r"from\s+the\s+textbook\s+figure",
    r"solution\s+manual",
    r"exercise\s+solution",
    r"verbatim\s+from",
    r"PDF\s+page\s+image",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"lorem ipsum",
    r"speaker notes go here",
    r"insert (?:diagram|figure|visual)",
    r"placeholder",
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def html_text(html: str) -> str:
    parser = TextExtractor()
    parser.feed(html)
    return parser.text()


def remove_script_blocks(html: str) -> str:
    return re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.I | re.S)


def strip_tags(fragment: str) -> str:
    return html_text(fragment)


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing manifest: {rel_posix(path)}") from None
    rows = manifest.get("decks")
    if not isinstance(rows, list):
        raise SystemExit(f"{rel_posix(path)} must contain a 'decks' list")
    return manifest


def check_manifest_coverage(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    rows = manifest.get("decks", [])
    if len(rows) != EXPECTED_LESSON_COUNT:
        issues.append(f"manifest row count is {len(rows)}; expected {EXPECTED_LESSON_COUNT}")
    course_count = len({row.get("course_root") for row in rows if isinstance(row, dict)})
    if course_count != EXPECTED_COURSE_COUNT:
        issues.append(f"manifest course count is {course_count}; expected {EXPECTED_COURSE_COUNT}")

    expected, errors = build_manifest()
    if errors:
        issues.extend(f"manifest builder error: {error}" for error in errors)
    elif manifest != expected:
        issues.append("slide-deck-manifest.json is out of date with scripts/build_slide_deck_manifest.py")
    return issues


def git_paths(args: list[str]) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "-c", "safe.directory=D:/Geometry", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError:
        return set()
    if result.returncode != 0:
        return set()
    return {line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()}


def changed_paths() -> set[str]:
    paths = git_paths(["diff", "--name-only", "--relative", "HEAD", "--"])
    paths.update(git_paths(["ls-files", "--others", "--exclude-standard"]))
    return paths


def is_relative_url(value: str) -> bool:
    return not re.match(r"^(?:[a-z]+:|#|data:|mailto:)", value, re.I)


def local_target(base: Path, url: str) -> Path:
    clean = url.split("#", 1)[0].split("?", 1)[0]
    return (base / clean).resolve()


def audit_links(deck_path: Path, html: str) -> list[str]:
    issues: list[str] = []
    base = deck_path.parent
    for attr, value in re.findall(r"\b(src|href)\s*=\s*['\"]([^'\"]+)['\"]", html, re.I):
        if not is_relative_url(value):
            continue
        target = local_target(base, value)
        try:
            target.relative_to(ROOT)
        except ValueError:
            issues.append(f"{rel_posix(deck_path)} links outside repo: {value}")
            continue
        if not target.exists():
            issues.append(f"{rel_posix(deck_path)} has broken {attr} link: {value}")
        elif attr.lower() == "src" and target.is_file() and target.stat().st_size < 100:
            issues.append(f"{rel_posix(deck_path)} links a tiny or blank-looking asset: {value}")
    return issues


def note_payload_word_counts(payload: Any) -> list[int]:
    if isinstance(payload, str):
        return [word_count(payload)]
    if isinstance(payload, list):
        counts: list[int] = []
        for item in payload:
            counts.extend(note_payload_word_counts(item))
        return counts
    if isinstance(payload, dict):
        counts = []
        for key in ("notes", "speaker_notes", "narration", "text", "body"):
            if key in payload:
                counts.extend(note_payload_word_counts(payload[key]))
        if not counts:
            for value in payload.values():
                counts.extend(note_payload_word_counts(value))
        return counts
    return []


def audit_notes_json(row: dict[str, str]) -> list[str]:
    issues: list[str] = []
    notes_path = ROOT / row["notes_path"]
    if not notes_path.exists():
        return [f"missing speaker-notes JSON: {row['notes_path']}"]
    try:
        payload = json.loads(notes_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid speaker-notes JSON in {row['notes_path']}: {exc}"]
    counts = note_payload_word_counts(payload)
    if not counts:
        issues.append(f"speaker-notes JSON has no readable narration: {row['notes_path']}")
    elif min(counts) < 25:
        issues.append(f"speaker-notes JSON has terse narration entries: {row['notes_path']}")
    return issues


def audit_deck(row: dict[str, str]) -> list[str]:
    deck_path = ROOT / row["deck_path"]
    if not deck_path.exists():
        return [f"missing deck file: {row['deck_path']}"]
    html = deck_path.read_text(encoding="utf-8", errors="replace")
    visible_html = remove_script_blocks(html)
    text = html_text(visible_html)
    issues: list[str] = []

    for field in REQUIRED_METADATA_FIELDS:
        field_pattern = rf"(?:\"{re.escape(field)}\"\s*:|name=['\"]{re.escape(field)}['\"])"
        if not re.search(field_pattern, html, re.I):
            issues.append(f"{row['deck_path']} metadata is missing {field}")

    if row["notebook_path"] not in html:
        issues.append(f"{row['deck_path']} does not reference its manifest notebook_path")
    source_numbers = re.findall(r"\d+", row["source_span"])
    if source_numbers and not any(number in text for number in source_numbers[:2]):
        issues.append(f"{row['deck_path']} visible text does not ground the assigned source span")
    if "deck-stage.js" not in html:
        issues.append(f"{row['deck_path']} does not load deck-stage.js")

    sections = re.findall(r"<section\b[^>]*>(.*?)</section>", html, re.I | re.S)
    if not sections:
        issues.append(f"{row['deck_path']} has no slide <section> elements")
    notes: list[str] = []
    for index, section in enumerate(sections, start=1):
        aside_match = re.search(
            r"<aside\b[^>]*class=['\"][^'\"]*speaker-notes[^'\"]*['\"][^>]*>(.*?)</aside>",
            section,
            re.I | re.S,
        )
        if not aside_match:
            issues.append(f"{row['deck_path']} slide {index} is missing <aside class=\"speaker-notes\">")
            continue
        note_text = strip_tags(aside_match.group(1))
        notes.append(note_text)
        if word_count(note_text) < 35:
            issues.append(f"{row['deck_path']} slide {index} speaker notes are too terse")
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, note_text, re.I):
                issues.append(f"{row['deck_path']} slide {index} speaker notes contain placeholder text")

    if notes:
        normalized_notes = [re.sub(r"\W+", " ", note.lower()).strip() for note in notes]
        repeated = len(normalized_notes) - len(set(normalized_notes))
        if repeated:
            issues.append(f"{row['deck_path']} repeats identical speaker-note narration on {repeated} slides")
        generic_count = sum(1 for note in normalized_notes if "in this slide we" in note or "this slide shows" in note)
        if generic_count >= max(3, len(notes) // 2):
            issues.append(f"{row['deck_path']} uses repeated generic speaker-note framing")

    visual_markers = re.findall(r"<(?:svg|img|canvas|figure)\b", html, re.I)
    if not visual_markers:
        issues.append(f"{row['deck_path']} has no SVG, image, canvas, or figure visuals")
    for svg in re.findall(r"<svg\b[^>]*>(.*?)</svg>", html, re.I | re.S):
        if not re.search(r"<(?:path|circle|ellipse|line|polyline|polygon|rect|text)\b", svg, re.I):
            issues.append(f"{row['deck_path']} contains an apparently blank inline SVG")

    issues.extend(audit_links(deck_path, html))
    issues.extend(audit_notes_json(row))

    for pattern in COPYRIGHT_PATTERNS:
        if re.search(pattern, text, re.I):
            issues.append(f"{row['deck_path']} contains copyright-risk language matching /{pattern}/")
    for blockquote in re.findall(r"<blockquote\b[^>]*>(.*?)</blockquote>", html, re.I | re.S):
        if word_count(strip_tags(blockquote)) > 80:
            issues.append(f"{row['deck_path']} contains a long blockquote")
    for quoted in re.findall(r"\"([^\"]{400,})\"", text):
        if word_count(quoted) > 80:
            issues.append(f"{row['deck_path']} contains a long quoted passage")

    return issues


def audit_script_inventory() -> list[str]:
    issues: list[str] = []
    for script in (ROOT / "scripts").glob("*.py"):
        if script.name in ALLOWED_SLIDE_INFRA_SCRIPTS:
            continue
        text = script.read_text(encoding="utf-8", errors="replace")
        mentions_decks = re.search(r"(slide[-_ ]?deck|lecture[-_ ]?deck|deck-stage|speaker-notes)", text, re.I)
        writes_html = re.search(r"(write_text|open\([^)]*['\"]w|\.html|<section\b|pptx|powerpoint)", text, re.I)
        bulk_loop = re.search(r"for\s+\w+\s+in\s+.*(?:manifest|courses|notebooks|chapters)", text, re.I | re.S)
        if mentions_decks and writes_html and bulk_loop:
            issues.append(f"possible mass deck generator in {rel_posix(script)}")
    return issues


def selected_rows(manifest: dict[str, Any], changed_only: bool, deck: str | None) -> list[dict[str, str]]:
    rows = manifest["decks"]
    if deck:
        needle = deck.replace("\\", "/")
        return [row for row in rows if row["deck_path"] == needle or str((ROOT / row["deck_path"]).resolve()) == str(Path(deck).resolve())]
    if not changed_only:
        return [row for row in rows if (ROOT / row["deck_path"]).exists()]
    changed = changed_paths()
    selected: list[dict[str, str]] = []
    for row in rows:
        slide_dir = str(Path(row["deck_path"]).parent).replace("\\", "/")
        if row["deck_path"] in changed or row["notes_path"] in changed or any(path.startswith(f"{slide_dir}/") for path in changed):
            selected.append(row)
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_OUTPUT), help="Slide deck manifest path.")
    parser.add_argument("--changed-only", action="store_true", help="Audit only changed deck/notes files.")
    parser.add_argument("--deck", help="Audit one deck path from the manifest.")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = load_manifest(manifest_path)

    issues = check_manifest_coverage(manifest)
    issues.extend(audit_script_inventory())

    rows = selected_rows(manifest, args.changed_only, args.deck)
    if args.deck and not rows:
        issues.append(f"deck is not listed in manifest: {args.deck}")
    for row in rows:
        issues.extend(audit_deck(row))

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    scope = "changed decks" if args.changed_only else "existing decks"
    print(f"slide deck audit OK: manifest coverage checked; {len(rows)} {scope} audited.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
