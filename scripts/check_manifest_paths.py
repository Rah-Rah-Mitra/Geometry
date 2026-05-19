"""Validate that the committed course manifest points at existing repo paths."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "course-manifest.json"

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "repository",
    "tracks",
    "runtime_profiles",
    "summary",
    "courses",
}

REQUIRED_COURSE_KEYS = {
    "course_dir",
    "links",
    "notebook_count",
    "notebooks",
    "path",
    "runtime_profile",
    "runtimes",
    "slug",
    "title",
    "track",
}

REQUIRED_NOTEBOOK_KEYS = {
    "colab_url",
    "github_url",
    "kind",
    "path",
    "title",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_keys(label: str, data: dict, keys: set[str], errors: list[str]) -> None:
    missing = sorted(keys - set(data))
    if missing:
        errors.append(f"{label} is missing keys: {', '.join(missing)}")


def require_existing_path(label: str, path_value: str, errors: list[str]) -> None:
    path = ROOT / path_value
    if not path.exists():
        errors.append(f"{label} does not exist: {path_value}")


def main() -> int:
    errors: list[str] = []

    if not MANIFEST_PATH.exists():
        raise SystemExit(f"Missing manifest: {rel(MANIFEST_PATH)}")

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {rel(MANIFEST_PATH)}: {exc}") from exc

    if not isinstance(manifest, dict):
        raise SystemExit("course-manifest.json must contain a JSON object")

    require_keys("manifest", manifest, REQUIRED_TOP_LEVEL_KEYS, errors)

    runtime_profiles = manifest.get("runtime_profiles", {})
    if not isinstance(runtime_profiles, dict) or not runtime_profiles:
        errors.append("manifest.runtime_profiles must be a non-empty object")
    else:
        for profile, profile_data in sorted(runtime_profiles.items()):
            if not isinstance(profile_data, dict):
                errors.append(f"runtime profile {profile!r} must be an object")
                continue
            requirements = profile_data.get("requirements")
            if not requirements:
                errors.append(f"runtime profile {profile!r} is missing requirements")
                continue
            require_existing_path(
                f"runtime profile {profile!r} requirements",
                requirements,
                errors,
            )

    courses = manifest.get("courses", [])
    if not isinstance(courses, list) or not courses:
        errors.append("manifest.courses must be a non-empty array")
        courses = []

    known_profiles = set(runtime_profiles)
    notebook_total = 0

    for index, course in enumerate(courses):
        label = f"course[{index}]"
        if not isinstance(course, dict):
            errors.append(f"{label} must be an object")
            continue

        require_keys(label, course, REQUIRED_COURSE_KEYS, errors)

        course_title = course.get("title") or label
        course_path = course.get("path")
        if course_path:
            require_existing_path(f"{course_title} course path", course_path, errors)

        profile = course.get("runtime_profile")
        if profile and profile not in known_profiles:
            errors.append(f"{course_title} uses unknown runtime profile: {profile}")

        notebooks = course.get("notebooks", [])
        if not isinstance(notebooks, list) or not notebooks:
            errors.append(f"{course_title} notebooks must be a non-empty array")
            notebooks = []

        expected_count = course.get("notebook_count")
        if isinstance(expected_count, int) and expected_count != len(notebooks):
            errors.append(
                f"{course_title} notebook_count is {expected_count}, "
                f"but notebooks has {len(notebooks)} entries"
            )

        notebook_total += len(notebooks)
        for notebook_index, notebook in enumerate(notebooks):
            notebook_label = f"{course_title} notebooks[{notebook_index}]"
            if not isinstance(notebook, dict):
                errors.append(f"{notebook_label} must be an object")
                continue
            require_keys(notebook_label, notebook, REQUIRED_NOTEBOOK_KEYS, errors)
            notebook_path = notebook.get("path")
            if notebook_path:
                require_existing_path(notebook_label, notebook_path, errors)

    summary = manifest.get("summary", {})
    if isinstance(summary, dict):
        course_count = summary.get("course_count")
        if isinstance(course_count, int) and course_count != len(courses):
            errors.append(
                f"summary.course_count is {course_count}, but courses has {len(courses)} entries"
            )
        manifest_notebook_count = summary.get("notebook_count")
        if isinstance(manifest_notebook_count, int) and manifest_notebook_count != notebook_total:
            errors.append(
                "summary.notebook_count is "
                f"{manifest_notebook_count}, but manifest lists {notebook_total} notebooks"
            )
    else:
        errors.append("manifest.summary must be an object")

    if errors:
        raise SystemExit("Manifest path check failed:\n" + "\n".join(f"- {e}" for e in errors))

    print(f"manifest path check passed: {len(courses)} courses, {notebook_total} notebooks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
