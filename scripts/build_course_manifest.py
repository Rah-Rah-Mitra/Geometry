"""Build the public course manifest for the Geometry atlas.

The metadata files use JSON syntax in ``.yml`` files so this script stays
stdlib-only while remaining readable by YAML-aware tooling.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "metadata"
COURSES_METADATA = METADATA_DIR / "courses.yml"
RUNTIME_METADATA = METADATA_DIR / "runtime_profiles.yml"
DEFAULT_OUTPUT = ROOT / "course-manifest.json"

OWNER = "Rah-Rah-Mitra"
REPO = "Geometry"
BRANCH = "main"

IGNORED_PARTS = {
    ".codex",
    ".git",
    ".ipynb_checkpoints",
    ".pytest_cache",
    ".ruff_cache",
    ".validation-work",
    ".venv",
    "__pycache__",
}

TITLE_SUFFIXES = (
    " - Standalone Notebook Course",
    " - Standalone Notebook Edition",
    " - Visualization-First Notebook Course",
    " - Standalone Course",
)

TRACK_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "geometry-data-statistics-ml",
        (
            "deep-learning",
            "information-geometry",
            "directional-statistics",
            "statistics-on",
            "nonparametric",
            "optimal-transport",
        ),
    ),
    (
        "computational-geometry-graphics-vision-robotics",
        (
            "computational-geometry",
            "computer-graphics",
            "graphics",
            "robotic",
            "robotics",
            "vision",
            "geometric-algebra",
        ),
    ),
    (
        "topology-manifolds-curvature",
        (
            "topology",
            "topological",
            "manifold",
            "riemannian",
            "differential-geometry",
            "differential-forms",
            "symplectic",
            "contact",
            "curvature",
            "metric-geometry",
            "metric-spaces",
        ),
    ),
    (
        "graduate-geometry-branches",
        (
            "algebraic-geometry",
            "complex-geometry",
            "hodge",
            "principles-of-algebraic",
            "geometric-measure",
            "geometric-group",
            "einstein",
            "j-holomorphic",
            "convex-analysis",
        ),
    ),
)

RUNTIME_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "ml_geometry",
        (
            "deep-learning",
            "geometric-deep-learning",
            "optimal-transport",
            "information-geometry",
            "statistics",
            "nonparametric",
            "directional",
            "manifolds-with-applications-to-shape",
        ),
    ),
    (
        "graphics",
        (
            "computer-graphics",
            "graphics",
            "vision",
            "geometric-tools",
            "multiple-view",
        ),
    ),
    ("robotics", ("robotic", "robotics")),
    ("topology", ("topology", "topological", "persistent", "homology", "knots")),
    (
        "algebraic_geometry",
        (
            "algebraic-geometry",
            "ideals",
            "varieties",
            "commutative-algebra",
            "hodge",
            "complex-geometry",
        ),
    ),
)

TAG_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("euclidean", ("euclid", "euclidean")),
    ("projective-geometry", ("projective",)),
    ("linear-algebra", ("linear-algebra", "geometric-algebra")),
    ("topology", ("topology", "topological")),
    ("manifolds", ("manifold", "manifolds")),
    ("riemannian-geometry", ("riemannian", "curvature")),
    ("symplectic-geometry", ("symplectic", "contact", "hamiltonian")),
    ("algebraic-geometry", ("algebraic-geometry", "varieties", "hodge", "complex")),
    ("computational-geometry", ("computational-geometry", "discrete")),
    ("graphics", ("graphics", "ray-tracing", "raster")),
    ("vision", ("vision", "camera")),
    ("robotics", ("robot", "robotics")),
    ("statistics", ("statistics", "nonparametric", "inference")),
    ("machine-learning", ("deep-learning", "machine-learning")),
    ("optimal-transport", ("optimal-transport", "transport")),
)


def load_json_metadata(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing metadata file: {path.relative_to(ROOT)}") from None
    except json.JSONDecodeError as exc:
        rel = path.relative_to(ROOT)
        raise SystemExit(f"Invalid JSON-style YAML in {rel}: {exc}") from exc


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_ignored(path: Path) -> bool:
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError:
        parts = path.parts
    return any(part in IGNORED_PARTS or part.startswith(".") for part in parts)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def normalize_title(title: str) -> str:
    title = title.strip()
    for suffix in TITLE_SUFFIXES:
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


def read_notebook(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid notebook JSON: {rel_posix(path)}: {exc}") from exc


def markdown_cells(notebook: dict) -> list[str]:
    cells = []
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell.get("source", "")
        cells.append("".join(source) if isinstance(source, list) else str(source))
    return cells


def first_heading(notebook: dict, fallback: str) -> str:
    for source in markdown_cells(notebook):
        for line in source.splitlines():
            match = re.match(r"^#\s+(.+?)\s*$", line)
            if match:
                return normalize_title(match.group(1))
    return normalize_title(fallback.replace("-", " "))


def first_paragraph(notebook: dict) -> str:
    for source in markdown_cells(notebook):
        lines: list[str] = []
        seen_heading = False
        for raw_line in source.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("[![") or line.startswith("!["):
                if lines:
                    break
                continue
            if line.startswith("#"):
                seen_heading = True
                continue
            if seen_heading and not line.startswith("|") and not line.startswith("- "):
                lines.append(line)
            if lines and not line:
                break
        if lines:
            return " ".join(lines)
    return ""


def notebook_kind(path: Path, course_root: Path) -> str:
    name = path.name
    if path == course_root / "00-book-index.ipynb":
        return "book-index"
    if name == "00-part-index.ipynb":
        return "part-index"
    if name == "00-index.ipynb":
        return "unit-index"
    return "lesson"


def infer_track(folder: str, title: str) -> str:
    haystack = f"{folder} {slugify(title)}"
    for track, keywords in TRACK_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return track
    return "foundations-classical-geometry"


def infer_runtime_profile(folder: str, title: str) -> str:
    haystack = f"{folder} {slugify(title)}"
    for profile, keywords in RUNTIME_KEYWORDS:
        if any(keyword in haystack for keyword in keywords):
            return profile
    return "classic"


def infer_tags(folder: str, title: str) -> list[str]:
    haystack = f"{folder} {slugify(title)}"
    tags = [
        tag
        for tag, keywords in TAG_KEYWORDS
        if any(keyword in haystack for keyword in keywords)
    ]
    return sorted(set(tags))


def url_for(path: str, service: str) -> str:
    encoded_path = quote(path, safe="/")
    if service == "github":
        return f"https://github.com/{OWNER}/{REPO}/blob/{BRANCH}/{encoded_path}"
    if service == "colab":
        return (
            "https://colab.research.google.com/github/"
            f"{OWNER}/{REPO}/blob/{BRANCH}/{encoded_path}"
        )
    if service == "raw":
        return f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{encoded_path}"
    raise ValueError(service)


def merge_metadata(base: dict, *overrides: dict | None) -> dict:
    merged = dict(base)
    for override in overrides:
        if not override:
            continue
        for key, value in override.items():
            if key == "tags":
                merged[key] = sorted(set(merged.get(key, [])) | set(value or []))
            elif key == "prerequisites":
                merged[key] = list(value or [])
            else:
                merged[key] = value
    return merged


def discover_course(course_root: Path, course_metadata: dict, runtime_profiles: dict) -> dict:
    index_path = course_root / "00-book-index.ipynb"
    index_nb = read_notebook(index_path)
    title = first_heading(index_nb, course_root.name)
    course_path = rel_posix(index_path)

    defaults = course_metadata.get("defaults", {})
    explicit = course_metadata.get("courses", {}).get(course_root.name, {})
    track = explicit.get("track") or infer_track(course_root.name, title)
    track_defaults = course_metadata.get("course_defaults_by_track", {}).get(track, {})
    inferred = {
        "title": title,
        "track": track,
        "tags": infer_tags(course_root.name, title),
    }
    merged = merge_metadata(defaults, track_defaults, inferred, explicit)
    if not merged.get("runtime_profile"):
        merged["runtime_profile"] = infer_runtime_profile(course_root.name, title)
    profile = merged["runtime_profile"]
    if "jupyterlite" not in explicit and "jupyterlite" not in track_defaults:
        merged["jupyterlite"] = bool(
            runtime_profiles.get(profile, {}).get("jupyterlite_default", False)
        )

    notebooks = []
    for notebook_path in sorted(course_root.rglob("*.ipynb"), key=lambda path: rel_posix(path)):
        if is_ignored(notebook_path):
            continue
        nb = read_notebook(notebook_path)
        nb_path = rel_posix(notebook_path)
        notebooks.append(
            {
                "path": nb_path,
                "title": first_heading(nb, notebook_path.stem),
                "kind": notebook_kind(notebook_path, course_root),
                "github_url": url_for(nb_path, "github"),
                "colab_url": url_for(nb_path, "colab"),
            }
        )

    runtimes = {
        "colab": bool(merged.get("colab", True)),
        "jupyterlite": bool(merged.get("jupyterlite", False)),
        "binder": bool(merged.get("binder", False)),
        "local": bool(merged.get("local", True)),
    }

    return {
        "slug": merged.get("slug") or slugify(course_root.name),
        "title": merged.get("title") or title,
        "description": merged.get("description") or first_paragraph(index_nb),
        "path": course_path,
        "course_dir": rel_posix(course_root),
        "track": track,
        "difficulty": merged.get("difficulty", "varies"),
        "runtime_profile": profile,
        "estimated_hours": merged.get("estimated_hours"),
        "prerequisites": merged.get("prerequisites", []),
        "tags": sorted(set(merged.get("tags", []))),
        "runtimes": runtimes,
        "links": {
            "github": url_for(course_path, "github"),
            "colab": url_for(course_path, "colab") if runtimes["colab"] else None,
            "jupyterlite": merged.get("jupyterlite_url"),
            "binder": merged.get("binder_url"),
            "download": url_for(course_path, "raw"),
        },
        "notebook_count": len(notebooks),
        "notebooks": notebooks,
    }


def build_manifest() -> dict:
    course_metadata = load_json_metadata(COURSES_METADATA)
    runtime_profiles = load_json_metadata(RUNTIME_METADATA)

    course_roots = sorted(
        {
            path.parent
            for path in ROOT.rglob("00-book-index.ipynb")
            if not is_ignored(path)
        },
        key=lambda path: rel_posix(path),
    )

    courses = [
        discover_course(course_root, course_metadata, runtime_profiles)
        for course_root in course_roots
    ]

    manifest = {
        "schema_version": 1,
        "repository": {
            "owner": OWNER,
            "name": REPO,
            "branch": BRANCH,
            "source_url": f"https://github.com/{OWNER}/{REPO}",
        },
        "tracks": course_metadata.get("tracks", {}),
        "runtime_profiles": runtime_profiles,
        "summary": {
            "course_count": len(courses),
            "notebook_count": sum(course["notebook_count"] for course in courses),
            "track_counts": dict(Counter(course["track"] for course in courses)),
            "runtime_profile_counts": dict(
                Counter(course["runtime_profile"] for course in courses)
            ),
        },
        "courses": courses,
    }
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict) -> None:
    slugs = [course["slug"] for course in manifest["courses"]]
    duplicate_slugs = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicate_slugs:
        raise SystemExit(f"Duplicate course slugs: {', '.join(duplicate_slugs)}")

    runtime_profiles = set(manifest["runtime_profiles"])
    for profile, data in manifest["runtime_profiles"].items():
        requirements = ROOT / data["requirements"]
        if not requirements.exists():
            raise SystemExit(
                f"Runtime profile {profile!r} points to missing {data['requirements']}"
            )

    for course in manifest["courses"]:
        if course["runtime_profile"] not in runtime_profiles:
            raise SystemExit(
                f"{course['course_dir']} uses unknown profile {course['runtime_profile']}"
            )
        if not (ROOT / course["path"]).exists():
            raise SystemExit(f"Missing course index: {course['path']}")
        if not course["notebooks"]:
            raise SystemExit(f"No notebooks discovered for {course['course_dir']}")
        for notebook in course["notebooks"]:
            if not (ROOT / notebook["path"]).exists():
                raise SystemExit(f"Missing notebook: {notebook['path']}")


def manifest_text(manifest: dict) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the output file does not match the generated manifest",
    )
    args = parser.parse_args(argv)

    manifest = build_manifest()
    text = manifest_text(manifest)
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        if not output.exists():
            print(f"{output.relative_to(ROOT)} is missing", file=sys.stderr)
            return 1
        current = output.read_text(encoding="utf-8")
        if current != text:
            print(f"{output.relative_to(ROOT)} is out of date", file=sys.stderr)
            return 1
        print(
            "course-manifest.json is current: "
            f"{manifest['summary']['course_count']} courses, "
            f"{manifest['summary']['notebook_count']} notebooks."
        )
        return 0

    output.write_text(text, encoding="utf-8")
    print(
        f"Wrote {output.relative_to(ROOT)} with "
        f"{manifest['summary']['course_count']} courses and "
        f"{manifest['summary']['notebook_count']} notebooks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
