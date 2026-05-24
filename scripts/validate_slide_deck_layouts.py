"""Validate Geometry lecture deck layout contracts.

Browser rendering is best-effort: when Playwright is unavailable, the script
still performs static 1920x1080, math, navigation, and slide-structure checks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from audit_slide_decks import check_manifest_coverage, html_text, load_manifest, selected_rows
from build_slide_deck_manifest import DEFAULT_OUTPUT, ROOT, rel_posix


def parse_viewport(value: str) -> tuple[int, int]:
    match = re.match(r"^(\d+)x(\d+)$", value.lower())
    if not match:
        raise argparse.ArgumentTypeError("viewport must be WIDTHxHEIGHT, for example 1920x1080")
    return int(match.group(1)), int(match.group(2))


def static_layout_checks(row: dict[str, str], viewport: tuple[int, int]) -> list[str]:
    deck_path = ROOT / row["deck_path"]
    if not deck_path.exists():
        return [f"missing deck file: {row['deck_path']}"]
    html = deck_path.read_text(encoding="utf-8", errors="replace")
    text = html_text(html)
    width, height = viewport
    issues: list[str] = []

    if str(width) not in html or str(height) not in html:
        issues.append(f"{row['deck_path']} does not declare the {width}x{height} stage size")
    if "deck-stage.js" not in html:
        issues.append(f"{row['deck_path']} does not load lecture-design-system deck-stage.js")
    if not re.search(r"(katex|STIX Two|STIX)", html, re.I):
        issues.append(f"{row['deck_path']} does not declare KaTeX or STIX math support")
    if not re.search(r"<section\b", html, re.I):
        issues.append(f"{row['deck_path']} has no slide sections")
    if not re.search(r"speaker-notes", html, re.I):
        issues.append(f"{row['deck_path']} has no speaker-notes asides")
    if re.search(r"font-size\s*:\s*(?:1\d|[0-9])px", html, re.I):
        issues.append(f"{row['deck_path']} contains slide CSS below the 20px readability floor")
    if re.search(r"(overflow\s*:\s*hidden|position\s*:\s*absolute)", html, re.I) and len(text) > 25000:
        issues.append(f"{row['deck_path']} has high text volume with clipping-prone CSS")
    if re.search(r"\$\$|\\\(|\\\[", html) and not re.search(r"renderMathInElement|katex", html, re.I):
        issues.append(f"{row['deck_path']} has TeX delimiters without a KaTeX renderer")
    return issues


def browser_layout_checks(rows: list[dict[str, str]], viewport: tuple[int, int]) -> tuple[list[str], str]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - depends on optional runtime
        return [], f"Playwright unavailable; static layout checks only ({type(exc).__name__}: {exc})."

    issues: list[str] = []
    width, height = viewport
    with sync_playwright() as playwright:  # pragma: no cover - optional browser path
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        for row in rows:
            deck_path = ROOT / row["deck_path"]
            page.goto(deck_path.as_uri(), wait_until="networkidle")
            result: dict[str, Any] = page.evaluate(
                """() => {
                    const slides = Array.from(document.querySelectorAll('section'));
                    const body = document.body.getBoundingClientRect();
                    const overflowing = slides.map((slide, index) => ({
                        index: index + 1,
                        scrollW: slide.scrollWidth,
                        clientW: slide.clientWidth,
                        scrollH: slide.scrollHeight,
                        clientH: slide.clientHeight,
                        rect: slide.getBoundingClientRect().toJSON()
                    })).filter(item => item.scrollW > item.clientW + 2 || item.scrollH > item.clientH + 2);
                    return {
                        slideCount: slides.length,
                        bodyWidth: body.width,
                        bodyHeight: body.height,
                        overflowing,
                        hasDeckStage: Boolean(window.DeckStage || document.querySelector('script[src*="deck-stage.js"]')),
                        hasKatexCss: Boolean(document.querySelector('link[href*="katex"]') || document.querySelector('.katex'))
                    };
                }"""
            )
            if result["slideCount"] == 0:
                issues.append(f"{row['deck_path']} rendered with no slide sections")
            if result["overflowing"]:
                indexes = ", ".join(str(item["index"]) for item in result["overflowing"][:8])
                issues.append(f"{row['deck_path']} has overflowing rendered slides: {indexes}")
            if not result["hasDeckStage"]:
                issues.append(f"{row['deck_path']} rendered without deck-stage navigation")
            if not result["hasKatexCss"] and re.search(r"\$\$|\\\(|\\\[", deck_path.read_text(encoding="utf-8", errors="replace")):
                issues.append(f"{row['deck_path']} rendered TeX without KaTeX CSS")
        browser.close()
    return issues, "Playwright browser layout checks ran."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_OUTPUT), help="Slide deck manifest path.")
    parser.add_argument("--changed-only", action="store_true", help="Validate only changed deck files.")
    parser.add_argument("--deck", help="Validate one deck path from the manifest.")
    parser.add_argument("--viewport", default="1920x1080", type=parse_viewport, help="Viewport WIDTHxHEIGHT.")
    parser.add_argument("--no-browser", action="store_true", help="Skip optional Playwright rendering.")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = load_manifest(manifest_path)
    issues = check_manifest_coverage(manifest)
    rows = selected_rows(manifest, args.changed_only, args.deck)
    if args.deck and not rows:
        issues.append(f"deck is not listed in manifest: {args.deck}")

    for row in rows:
        issues.extend(static_layout_checks(row, args.viewport))

    evidence = "No changed or selected decks required browser layout checks."
    if rows and not args.no_browser:
        browser_issues, evidence = browser_layout_checks(rows, args.viewport)
        issues.extend(browser_issues)
    elif rows and args.no_browser:
        evidence = "Browser layout checks skipped by --no-browser."

    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        print(evidence, file=sys.stderr)
        return 1

    scope = "changed decks" if args.changed_only else "existing decks"
    print(f"slide deck layout validation OK: {len(rows)} {scope} checked. {evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
