"""Audit MVG notebook artifact references and artifact metadata."""

from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import nbformat

import mvg_inventory as inventory

BOOK_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = BOOK_ROOT / "artifacts"
FORBIDDEN_IMAGE_HINTS = ("screenshot", "page-crop", "page_crop", "pdf-page", "pdf_page", "textbook-page")
GENERIC_ARTIFACT_NAMES = {
    "concept-map.png",
    "geometry-scene.png",
    "diagnostic-dashboard.png",
    "constraint-dashboard.png",
    "numeric-summary.json",
}


def entry_folder(entry: dict[str, Any]) -> Path:
    if entry["part"] is None:
        return BOOK_ROOT / entry["folder"]
    return BOOK_ROOT / entry["part"] / entry["folder"]


def rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def literal_strings(source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return re.findall(r"['\"]([^'\"]*artifacts/[^'\"]*)['\"]", source)
    values: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            values.append(node.value)
    return values


def notebook_paths() -> list[tuple[dict[str, Any], Path]]:
    return [(entry, entry_folder(entry) / entry["notebook"]) for entry in inventory.ENTRIES]


def source_mentions_artifact(markdown: str, artifact_name: str) -> bool:
    paragraphs = [part.lower() for part in re.split(r"\n\s*\n", markdown)]
    name_words = set(re.findall(r"[a-z0-9]+", Path(artifact_name).stem.lower()))
    for paragraph in paragraphs:
        if artifact_name.lower() in paragraph:
            return True
        if len(name_words.intersection(re.findall(r"[a-z0-9]+", paragraph))) >= min(2, len(name_words)):
            return True
    return False


def audit() -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    referenced: set[Path] = set()
    displayed: set[Path] = set()
    source_by_topic: dict[str, str] = {}

    for entry, path in notebook_paths():
        nb = nbformat.read(path, as_version=4)
        topic_root = ARTIFACT_ROOT / entry["topic"]
        markdown = "\n".join("".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "markdown")
        code = "\n".join("".join(cell.get("source", "")) for cell in nb.cells if cell.cell_type == "code")
        lower_all = (markdown + "\n" + code).lower()
        source_by_topic[entry["topic"]] = lower_all

        if "source orientation:" not in lower_all or entry["printed"] not in lower_all or entry["pdf"] not in lower_all:
            findings.append(
                {
                    "check": "missing-source-map",
                    "path": rel(path),
                    "message": "source orientation does not include expected printed/PDF span",
                }
            )

        if "display_artifact(" not in code:
            findings.append({"check": "missing-inline-artifact-display", "path": rel(path), "message": "no display_artifact calls"})

        artifact_literals = [value for value in literal_strings(code) if "artifacts/" in value.replace("\\", "/")]
        for value in artifact_literals:
            normalized = value.replace("\\", "/")
            if re.match(r"^[A-Za-z]:/", normalized):
                findings.append({"check": "absolute-artifact-reference", "path": rel(path), "message": normalized})
                continue
            if not normalized.startswith("artifacts/"):
                continue
            candidate = BOOK_ROOT / normalized
            referenced.add(candidate)
            if entry["topic"] not in normalized:
                findings.append(
                    {
                        "check": "cross-topic-artifact-reference",
                        "path": rel(path),
                        "message": f"{normalized} does not live under {entry['topic']}",
                    }
                )
            if not candidate.exists():
                findings.append({"check": "broken-artifact-reference", "path": rel(path), "message": normalized})

        for match in re.finditer(r"display_artifact\(([^)\n]+)", code):
            text = match.group(1)
            for value in literal_strings(text):
                if "artifacts/" in value.replace("\\", "/"):
                    displayed.add(BOOK_ROOT / value.replace("\\", "/"))

        for artifact in sorted(topic_root.rglob("*")) if topic_root.exists() else []:
            if not artifact.is_file():
                continue
            name = artifact.name
            artifact_rel = rel(artifact)
            if artifact.stat().st_size == 0:
                findings.append({"check": "empty-artifact", "path": artifact_rel, "message": "zero-byte artifact"})
            if name in GENERIC_ARTIFACT_NAMES:
                findings.append({"check": "generic-artifact-name", "path": artifact_rel, "message": "artifact name is generic"})
            if any(hint in artifact_rel.lower() for hint in FORBIDDEN_IMAGE_HINTS):
                findings.append({"check": "forbidden-page-image-hint", "path": artifact_rel, "message": "artifact name suggests PDF screenshot/page crop"})
            if artifact.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".html"} and not source_mentions_artifact(markdown, name):
                findings.append(
                    {
                        "check": "artifact-not-explained-near-prose",
                        "path": artifact_rel,
                        "message": "artifact filename/concept is not mentioned in markdown prose",
                    }
                )
            if artifact.suffix.lower() == ".json":
                try:
                    raw = artifact.read_text(encoding="utf-8")
                    json.loads(raw)
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    findings.append({"check": "invalid-json-artifact", "path": artifact_rel, "message": str(exc)})
                    continue
                if re.search(r"[A-Za-z]:[\\/]", raw):
                    findings.append({"check": "absolute-path-in-json", "path": artifact_rel, "message": "JSON contains a drive-qualified path"})

    orphaned = []
    for artifact in ARTIFACT_ROOT.rglob("*"):
        if artifact.is_file() and artifact.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".html"}:
            topic = artifact.relative_to(ARTIFACT_ROOT).parts[0]
            mentioned_by_topic_notebook = artifact.name.lower() in source_by_topic.get(topic, "")
            if artifact not in referenced and artifact.name not in GENERIC_ARTIFACT_NAMES and not mentioned_by_topic_notebook:
                orphaned.append(rel(artifact))
    if orphaned:
        findings.append(
            {
                "check": "possibly-orphaned-visual-artifacts",
                "path": "artifacts",
                "message": f"{len(orphaned)} non-generic visual artifacts are not referenced by literal artifact paths",
                "details": orphaned[:20],
            }
        )

    by_check = Counter(finding["check"] for finding in findings)
    return {
        "summary": {
            "notebook_count": len(inventory.ENTRIES),
            "artifact_count": sum(1 for path in ARTIFACT_ROOT.rglob("*") if path.is_file()),
            "finding_count": len(findings),
            "findings_by_check": dict(sorted(by_check.items())),
        },
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()

    report = audit()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        summary = report["summary"]
        print(f"Audited {summary['notebook_count']} notebooks and {summary['artifact_count']} artifacts")
        if report["findings"]:
            for finding in report["findings"]:
                print(f"- {finding['check']} [{finding.get('path', '')}]: {finding['message']}")
        else:
            print("All artifact checks passed.")
    if report["findings"] and not args.no_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
