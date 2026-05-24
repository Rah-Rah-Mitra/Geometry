"""Export one QC-passed Geometry HTML lecture deck.

This script is deliberately per-deck. It refuses bulk export and never authors
or modifies deck HTML.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from audit_slide_decks import audit_deck, load_manifest
from build_slide_deck_manifest import DEFAULT_OUTPUT, ROOT, rel_posix
from validate_slide_deck_layouts import parse_viewport, static_layout_checks


def manifest_row_for_deck(manifest: dict, deck: str) -> dict[str, str] | None:
    deck_path = deck.replace("\\", "/")
    absolute = Path(deck)
    if not absolute.is_absolute():
        absolute = ROOT / absolute
    try:
        absolute_resolved = absolute.resolve()
    except OSError:
        absolute_resolved = absolute
    for row in manifest.get("decks", []):
        row_absolute = (ROOT / row["deck_path"]).resolve()
        if row["deck_path"] == deck_path or row_absolute == absolute_resolved:
            return row
    return None


def default_output(row: dict[str, str], fmt: str) -> Path:
    deck = ROOT / row["deck_path"]
    return deck.with_suffix(f".{fmt}")


def export_pdf(row: dict[str, str], output: Path, viewport: tuple[int, int]) -> str:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        raise RuntimeError(f"Playwright is unavailable for PDF export ({type(exc).__name__}: {exc}).") from exc

    deck_path = ROOT / row["deck_path"]
    width, height = viewport
    output.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:  # pragma: no cover - optional browser path
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        page.goto(deck_path.as_uri(), wait_until="networkidle")
        page.emulate_media(media="screen")
        page.pdf(
            path=str(output),
            width=f"{width}px",
            height=f"{height}px",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()
    return rel_posix(output)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_OUTPUT), help="Slide deck manifest path.")
    parser.add_argument("--deck", required=True, help="One deck path listed in slide-deck-manifest.json.")
    parser.add_argument("--format", choices=["pdf", "pptx"], default="pdf", help="Export format.")
    parser.add_argument("--output", help="Output file path. Defaults beside the deck.")
    parser.add_argument("--viewport", default="1920x1080", type=parse_viewport, help="Viewport WIDTHxHEIGHT.")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = load_manifest(manifest_path)
    row = manifest_row_for_deck(manifest, args.deck)
    if row is None:
        print(f"ERROR: deck is not listed in manifest: {args.deck}", file=sys.stderr)
        return 1
    if not (ROOT / row["deck_path"]).exists():
        print(f"ERROR: missing deck file: {row['deck_path']}", file=sys.stderr)
        return 1

    issues = audit_deck(row)
    issues.extend(static_layout_checks(row, args.viewport))
    if issues:
        for issue in issues:
            print(f"ERROR: export blocked until QC issues are fixed: {issue}", file=sys.stderr)
        return 1

    output = Path(args.output) if args.output else default_output(row, args.format)
    if not output.is_absolute():
        output = ROOT / output

    if args.format == "pptx":
        print(
            "ERROR: PPTX export is not available in this runtime yet; use per-deck PDF export "
            "or add a reviewed single-deck PPTX renderer.",
            file=sys.stderr,
        )
        return 1

    try:
        exported = export_pdf(row, output, args.viewport)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"exported {exported}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
