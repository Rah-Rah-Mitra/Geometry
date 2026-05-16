"""Audit canonical Hodge notebooks for source grounding and anti-generic signals."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import nbformat

from utils.course_data import CHAPTERS


WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def audit_notebook(path: Path, min_words: int, min_code_cells: int) -> list[str]:
    issues: list[str] = []
    nb = nbformat.read(path, as_version=4)
    markdown = "\n".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
    code_cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    word_count = len(words(markdown))
    if word_count < min_words:
        issues.append(f"{path}: markdown word count {word_count} < {min_words}")
    if len(code_cells) < min_code_cells:
        issues.append(f"{path}: code cell count {len(code_cells)} < {min_code_cells}")
    required_phrases = ["Source span", "Translation Guide", "Library Routing", "Computational Checks", "Takeaways"]
    for phrase in required_phrases:
        if phrase not in markdown:
            issues.append(f"{path}: missing section phrase {phrase!r}")
    if "screenshots" not in markdown or "copied" not in markdown:
        issues.append(f"{path}: missing copyright-safeguard note")
    return issues


def shingle_counter(paths: list[Path]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        text = " ".join(cell.source for cell in nb.cells if cell.cell_type == "markdown")
        tokens = [token.lower() for token in words(text)]
        for i in range(max(0, len(tokens) - 11)):
            shingle = " ".join(tokens[i : i + 12])
            counter[shingle] += 1
    return counter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-words", type=int, default=700)
    parser.add_argument("--min-code-cells", type=int, default=5)
    parser.add_argument("--max-repeated-shingles", type=int, default=60)
    args = parser.parse_args()

    notebook_paths = [ROOT / chapter.notebook_path for chapter in CHAPTERS]
    issues: list[str] = []
    for chapter, path in zip(CHAPTERS, notebook_paths):
        if not path.exists():
            issues.append(f"{path}: missing canonical notebook")
            continue
        issues.extend(audit_notebook(path, args.min_words, args.min_code_cells))
        text = path.read_text(encoding="utf-8").lower()
        for concept in chapter.concepts[:3]:
            if concept.lower() not in text:
                issues.append(f"{path}: missing chapter-specific concept {concept!r}")
        if chapter.id not in text:
            issues.append(f"{path}: missing chapter id {chapter.id}")

    repeated = [
        (shingle, count)
        for shingle, count in shingle_counter(notebook_paths).most_common(10)
        if count > args.max_repeated_shingles
    ]
    for shingle, count in repeated:
        issues.append(f"repeated markdown shingle appears {count} times: {shingle!r}")

    report = {
        "notebooks": len(notebook_paths),
        "issues": issues,
        "status": "pass" if not issues else "fail",
    }
    print(json.dumps(report, indent=2))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

