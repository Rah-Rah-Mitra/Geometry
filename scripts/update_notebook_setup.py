"""Insert or verify machine-managed setup cells in Geometry notebooks.

The updater preserves all authored cells exactly. It may only remove cells that
carry the managed setup marker and insert the current managed setup cell after
the first authored markdown/title cell.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "course-manifest.json"
RUNTIME_PROFILES_PATH = ROOT / "metadata" / "runtime_profiles.yml"
SETUP_TAG = "geometry-setup:v1"
SETUP_SCRIPT = "scripts/update_notebook_setup.py"

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


@dataclass(frozen=True)
class NotebookContext:
    path: str
    title: str
    kind: str
    course_dir: str | None
    course_title: str | None
    runtime_profile: str
    requirements: str
    jupyterlite: bool
    colab_url: str
    github_url: str
    repository: dict[str, str]


@dataclass
class NotebookResult:
    path: str
    current_setup_blocks: int
    changed: bool
    preserved_cell_count: int
    managed_cell_count: int
    first_cell_hash: str | None
    preserved_digest_before: str
    preserved_digest_after: str
    errors: list[str]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"Missing required file: {path.relative_to(ROOT).as_posix()}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path.relative_to(ROOT).as_posix()}: {exc}") from exc


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_ignored(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return any(part in IGNORED_PARTS or part.startswith(".") for part in parts)


def notebook_paths() -> list[Path]:
    return sorted(
        (path for path in ROOT.rglob("*.ipynb") if not is_ignored(path)),
        key=rel_posix,
    )


def url_for(repository: dict[str, str], path: str, service: str) -> str:
    owner = repository["owner"]
    name = repository["name"]
    branch = repository["branch"]
    encoded_path = quote(path, safe="/")
    if service == "github":
        return f"https://github.com/{owner}/{name}/blob/{branch}/{encoded_path}"
    if service == "colab":
        return (
            "https://colab.research.google.com/github/"
            f"{owner}/{name}/blob/{branch}/{encoded_path}"
        )
    raise ValueError(service)


def build_contexts(manifest: dict[str, Any], runtime_profiles: dict[str, Any]) -> dict[str, NotebookContext]:
    repository = manifest.get("repository", {})
    required_repository = {"owner", "name", "branch", "source_url"}
    missing_repository = sorted(required_repository - set(repository))
    if missing_repository:
        raise SystemExit(
            "course-manifest.json repository is missing keys: "
            + ", ".join(missing_repository)
        )

    contexts: dict[str, NotebookContext] = {}
    for course in manifest.get("courses", []):
        profile_name = course.get("runtime_profile")
        profile = runtime_profiles.get(profile_name)
        if not isinstance(profile, dict):
            raise SystemExit(f"{course.get('course_dir')} uses unknown runtime profile {profile_name!r}")
        requirements = profile.get("requirements")
        if not requirements:
            raise SystemExit(f"Runtime profile {profile_name!r} is missing requirements")
        for notebook in course.get("notebooks", []):
            path = notebook["path"]
            contexts[path] = NotebookContext(
                path=path,
                title=notebook.get("title") or Path(path).stem,
                kind=notebook.get("kind") or "lesson",
                course_dir=course.get("course_dir"),
                course_title=course.get("title"),
                runtime_profile=profile_name,
                requirements=requirements,
                jupyterlite=bool(course.get("runtimes", {}).get("jupyterlite", False)),
                colab_url=notebook.get("colab_url") or url_for(repository, path, "colab"),
                github_url=notebook.get("github_url") or url_for(repository, path, "github"),
                repository=dict(repository),
            )

    classic_profile = runtime_profiles.get("classic")
    if not isinstance(classic_profile, dict) or not classic_profile.get("requirements"):
        raise SystemExit("Runtime profile 'classic' is required for root index.ipynb")
    root_index = "index.ipynb"
    contexts[root_index] = NotebookContext(
        path=root_index,
        title="Geometry Course Atlas",
        kind="root-index",
        course_dir=None,
        course_title=None,
        runtime_profile="classic",
        requirements=classic_profile["requirements"],
        jupyterlite=bool(classic_profile.get("jupyterlite_default", False)),
        colab_url=url_for(repository, root_index, "colab"),
        github_url=url_for(repository, root_index, "github"),
        repository=dict(repository),
    )
    return contexts


def cell_source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    if isinstance(source, list):
        return "".join(str(part) for part in source)
    return str(source)


def is_setup_cell(cell: dict[str, Any]) -> bool:
    metadata = cell.get("metadata", {})
    tags = metadata.get("tags", [])
    if isinstance(tags, list) and SETUP_TAG in tags:
        return True
    setup_metadata = metadata.get("geometry_setup")
    if isinstance(setup_metadata, dict) and setup_metadata.get("marker") == SETUP_TAG:
        return True
    if cell.get("cell_type") == "code":
        first_line = cell_source_text(cell).lstrip().splitlines()[:1]
        return bool(first_line and first_line[0].strip() == f"# {SETUP_TAG}")
    return False


def cell_hash(cell: dict[str, Any]) -> str:
    payload = json.dumps(cell, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def digest_hashes(hashes: list[str]) -> str:
    payload = "\n".join(hashes).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def setup_context_payload(context: NotebookContext) -> dict[str, Any]:
    return {
        "marker": SETUP_TAG,
        "notebook_path": context.path,
        "notebook_title": context.title,
        "notebook_kind": context.kind,
        "course_dir": context.course_dir,
        "course_title": context.course_title,
        "runtime_profile": context.runtime_profile,
        "requirements": context.requirements,
        "jupyterlite": context.jupyterlite,
        "colab_url": context.colab_url,
        "github_url": context.github_url,
        "repository": context.repository,
    }


def setup_code(context: NotebookContext) -> str:
    payload = json.dumps(setup_context_payload(context), ensure_ascii=False, indent=2, sort_keys=True)
    return f'''# {SETUP_TAG}
# Machine-managed by {SETUP_SCRIPT}. Do not edit this cell by hand.

from __future__ import annotations

import json as _geometry_json
import os as _geometry_os
from pathlib import Path as _GeometryPath
import sys as _geometry_sys

GEOMETRY_SETUP = _geometry_json.loads(
    r"""
{payload}
"""
)


def _geometry_is_colab():
    try:
        import google.colab  # type: ignore  # noqa: F401
        return True
    except Exception:
        return False


def _geometry_is_jupyterlite():
    return _geometry_sys.platform == "emscripten" or "pyodide" in _geometry_sys.modules


def _geometry_add_path(path):
    text = str(path)
    if text not in _geometry_sys.path:
        _geometry_sys.path.insert(0, text)


def _geometry_find_repo_root():
    candidates = []
    env_root = _geometry_os.environ.get("GEOMETRY_REPO_ROOT")
    if env_root:
        candidates.append(_GeometryPath(env_root).expanduser())
    candidates.append(_GeometryPath.cwd())
    for start in candidates:
        start = start.resolve()
        for current in (start, *start.parents):
            if (current / "course-manifest.json").exists() and (
                current / "metadata" / "runtime_profiles.yml"
            ).exists():
                return current
    raise RuntimeError(
        "Could not find the Geometry repository root. Start JupyterLab inside the "
        "Geometry checkout or set GEOMETRY_REPO_ROOT."
    )


def _geometry_run(command):
    import subprocess as _geometry_subprocess

    printable = " ".join(str(part) for part in command)
    print(f"+ {{printable}}")
    _geometry_subprocess.check_call([str(part) for part in command])


def _geometry_requirement_names(requirements_path, seen=None):
    seen = set() if seen is None else seen
    requirements_path = requirements_path.resolve()
    if requirements_path in seen or not requirements_path.exists():
        return []
    seen.add(requirements_path)
    names = []
    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith(("-r ", "--requirement ")):
            _, nested = line.split(maxsplit=1)
            names.extend(_geometry_requirement_names(requirements_path.parent / nested, seen))
            continue
        if line.startswith("-"):
            continue
        name = line
        for separator in ("==", ">=", "<=", "~=", "!=", ">", "<", ";"):
            name = name.split(separator, 1)[0]
        name = name.split("[", 1)[0].strip()
        if name:
            names.append(name)
    return sorted(set(names))


def _geometry_missing_requirements(requirements_path):
    import importlib.metadata as _geometry_metadata

    missing = []
    for name in _geometry_requirement_names(requirements_path):
        try:
            _geometry_metadata.distribution(name)
        except _geometry_metadata.PackageNotFoundError:
            missing.append(name)
    return missing


def _geometry_configured_roots(repo_root):
    course_dir = GEOMETRY_SETUP.get("course_dir")
    course_root = repo_root / course_dir if course_dir else repo_root
    return repo_root, course_root


if _geometry_is_jupyterlite():
    if not GEOMETRY_SETUP["jupyterlite"]:
        raise RuntimeError(
            "This Geometry notebook uses runtime profile "
            f"{{GEOMETRY_SETUP['runtime_profile']!r}}, which is not enabled for "
            "JupyterLite in course-manifest.json. Open it in Colab or local JupyterLab."
        )
    GEOMETRY_REPO_ROOT = _GeometryPath.cwd()
    GEOMETRY_COURSE_ROOT = (
        GEOMETRY_REPO_ROOT / GEOMETRY_SETUP["course_dir"]
        if GEOMETRY_SETUP.get("course_dir")
        else GEOMETRY_REPO_ROOT
    )
    _geometry_add_path(GEOMETRY_REPO_ROOT)
    if GEOMETRY_COURSE_ROOT.exists():
        _geometry_add_path(GEOMETRY_COURSE_ROOT)
    GEOMETRY_RUNTIME_PROFILE = GEOMETRY_SETUP["runtime_profile"]
    print(
        "Geometry setup: JupyterLite/Pyodide detected; shell, git, and pip steps "
        "were skipped."
    )
elif _geometry_is_colab():
    repository = GEOMETRY_SETUP["repository"]
    repo_url = repository["source_url"].rstrip("/") + ".git"
    branch = repository["branch"]
    GEOMETRY_REPO_ROOT = _GeometryPath(
        _geometry_os.environ.get("GEOMETRY_REPO_ROOT", "/content/Geometry")
    )
    sparse_paths = ["requirements", "metadata", "scripts", "course-manifest.json", "index.ipynb"]
    if GEOMETRY_SETUP.get("course_dir"):
        sparse_paths.append(GEOMETRY_SETUP["course_dir"])
    if not (GEOMETRY_REPO_ROOT / ".git").exists():
        if GEOMETRY_REPO_ROOT.exists() and any(GEOMETRY_REPO_ROOT.iterdir()):
            raise RuntimeError(
                f"{{GEOMETRY_REPO_ROOT}} exists but is not a git checkout. "
                "Set GEOMETRY_REPO_ROOT to an empty path or remove the directory."
            )
        _geometry_run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                branch,
                repo_url,
                GEOMETRY_REPO_ROOT,
            ]
        )
        _geometry_run(["git", "-C", GEOMETRY_REPO_ROOT, "sparse-checkout", "init", "--cone"])
    _geometry_run(["git", "-C", GEOMETRY_REPO_ROOT, "sparse-checkout", "set", *sparse_paths])
    _geometry_run(["git", "-C", GEOMETRY_REPO_ROOT, "checkout", branch])
    requirements_path = GEOMETRY_REPO_ROOT / GEOMETRY_SETUP["requirements"]
    _geometry_run([_geometry_sys.executable, "-m", "pip", "install", "-q", "-r", requirements_path])
    GEOMETRY_REPO_ROOT, GEOMETRY_COURSE_ROOT = _geometry_configured_roots(GEOMETRY_REPO_ROOT)
    _geometry_os.chdir(GEOMETRY_COURSE_ROOT if GEOMETRY_COURSE_ROOT.exists() else GEOMETRY_REPO_ROOT)
    _geometry_add_path(GEOMETRY_REPO_ROOT)
    _geometry_add_path(GEOMETRY_COURSE_ROOT)
    GEOMETRY_RUNTIME_PROFILE = GEOMETRY_SETUP["runtime_profile"]
    print(
        f"Geometry setup: Colab ready at {{_GeometryPath.cwd()}} "
        f"with profile {{GEOMETRY_RUNTIME_PROFILE!r}}."
    )
else:
    GEOMETRY_REPO_ROOT = _geometry_find_repo_root()
    requirements_path = GEOMETRY_REPO_ROOT / GEOMETRY_SETUP["requirements"]
    missing = _geometry_missing_requirements(requirements_path)
    skip_install = _geometry_os.environ.get("GEOMETRY_SKIP_INSTALL") == "1"
    if missing and skip_install:
        print(
            "Geometry setup: GEOMETRY_SKIP_INSTALL=1, so missing profile packages "
            f"were not installed: {{', '.join(missing)}}"
        )
    elif missing:
        print(
            "Geometry setup: installing missing profile packages from "
            f"{{requirements_path.relative_to(GEOMETRY_REPO_ROOT)}}: {{', '.join(missing)}}"
        )
        _geometry_run([_geometry_sys.executable, "-m", "pip", "install", "-r", requirements_path])
    GEOMETRY_REPO_ROOT, GEOMETRY_COURSE_ROOT = _geometry_configured_roots(GEOMETRY_REPO_ROOT)
    _geometry_os.chdir(GEOMETRY_COURSE_ROOT if GEOMETRY_COURSE_ROOT.exists() else GEOMETRY_REPO_ROOT)
    _geometry_add_path(GEOMETRY_REPO_ROOT)
    _geometry_add_path(GEOMETRY_COURSE_ROOT)
    GEOMETRY_RUNTIME_PROFILE = GEOMETRY_SETUP["runtime_profile"]
    print(
        f"Geometry setup: local checkout ready at {{_GeometryPath.cwd()}} "
        f"with profile {{GEOMETRY_RUNTIME_PROFILE!r}}."
    )
'''


def setup_cell(context: NotebookContext) -> dict[str, Any]:
    source = setup_code(context).splitlines(keepends=True)
    return {
        "cell_type": "code",
        "id": "geom-setup-" + hashlib.sha1(context.path.encode("utf-8")).hexdigest()[:8],
        "metadata": {
            "geometry_setup": {
                "managed_by": SETUP_SCRIPT,
                "marker": SETUP_TAG,
                "runtime_profile": context.runtime_profile,
            },
            "tags": [SETUP_TAG],
        },
        "execution_count": None,
        "outputs": [],
        "source": source,
    }


def transform_notebook(
    notebook: dict[str, Any],
    context: NotebookContext,
) -> tuple[dict[str, Any], NotebookResult]:
    errors: list[str] = []
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        cells = []
        errors.append("notebook.cells must be a list")

    current_setup_blocks = sum(1 for cell in cells if isinstance(cell, dict) and is_setup_cell(cell))
    authored_cells = [
        copy.deepcopy(cell)
        for cell in cells
        if isinstance(cell, dict) and not is_setup_cell(cell)
    ]
    managed_cell_count = len(cells) - len(authored_cells)

    if not authored_cells:
        errors.append("notebook has no authored cells")
    elif authored_cells[0].get("cell_type") != "markdown":
        errors.append("first authored cell is not markdown")

    before_hashes = [cell_hash(cell) for cell in authored_cells]
    expected_cells = copy.deepcopy(authored_cells)
    if authored_cells:
        expected_cells.insert(1, setup_cell(context))

    transformed = copy.deepcopy(notebook)
    transformed["cells"] = expected_cells

    after_authored_cells = [cell for cell in transformed["cells"] if not is_setup_cell(cell)]
    after_hashes = [cell_hash(cell) for cell in after_authored_cells]
    if before_hashes != after_hashes:
        errors.append("preservation audit failed: authored cell hashes changed")

    if sum(1 for cell in transformed["cells"] if is_setup_cell(cell)) != 1:
        errors.append("transformed notebook does not contain exactly one setup block")

    return transformed, NotebookResult(
        path=context.path,
        current_setup_blocks=current_setup_blocks,
        changed=notebooks_differ(notebook, transformed),
        preserved_cell_count=len(authored_cells),
        managed_cell_count=managed_cell_count,
        first_cell_hash=before_hashes[0] if before_hashes else None,
        preserved_digest_before=digest_hashes(before_hashes),
        preserved_digest_after=digest_hashes(after_hashes),
        errors=errors,
    )


def notebooks_differ(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return left != right


def newline_for(path: Path) -> str:
    data = path.read_bytes()
    if b"\r\r\n" in data:
        return "\r\n"
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n")
    return "\r\n" if crlf and crlf == lf else "\n"


def notebook_text(notebook: dict[str, Any], *, newline: str = "\n") -> str:
    text = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    if newline != "\n":
        text = text.replace("\n", newline)
    return text


def analyze_all() -> tuple[list[tuple[Path, dict[str, Any]]], list[tuple[Path, dict[str, Any]]], list[NotebookResult]]:
    manifest = load_json(MANIFEST_PATH)
    runtime_profiles = load_json(RUNTIME_PROFILES_PATH)
    contexts = build_contexts(manifest, runtime_profiles)

    transformed: list[tuple[Path, dict[str, Any]]] = []
    originals: list[tuple[Path, dict[str, Any]]] = []
    results: list[NotebookResult] = []

    discovered = {rel_posix(path): path for path in notebook_paths()}
    unknown = sorted(set(discovered) - set(contexts))
    missing = sorted(set(contexts) - set(discovered))
    if unknown:
        raise SystemExit("Notebook(s) missing from manifest context: " + ", ".join(unknown[:20]))
    if missing:
        raise SystemExit("Manifest context points at missing notebook(s): " + ", ".join(missing[:20]))

    for rel_path, path in sorted(discovered.items()):
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result = NotebookResult(
                path=rel_path,
                current_setup_blocks=0,
                changed=False,
                preserved_cell_count=0,
                managed_cell_count=0,
                first_cell_hash=None,
                preserved_digest_before="",
                preserved_digest_after="",
                errors=[f"invalid notebook JSON: {exc}"],
            )
            results.append(result)
            continue
        expected, result = transform_notebook(notebook, contexts[rel_path])
        originals.append((path, notebook))
        transformed.append((path, expected))
        results.append(result)

    return originals, transformed, results


def result_summary(results: list[NotebookResult]) -> dict[str, Any]:
    changed = [result.path for result in results if result.changed]
    errors = {
        result.path: result.errors
        for result in results
        if result.errors
    }
    current_setup_counts: dict[str, int] = {}
    for result in results:
        key = str(result.current_setup_blocks)
        current_setup_counts[key] = current_setup_counts.get(key, 0) + 1
    return {
        "notebook_count": len(results),
        "changed_count": len(changed),
        "current_setup_block_counts": current_setup_counts,
        "managed_cell_count": sum(result.managed_cell_count for result in results),
        "preserved_cell_count": sum(result.preserved_cell_count for result in results),
        "preservation_audit": {
            "passed": not errors
            and all(
                result.preserved_digest_before == result.preserved_digest_after
                for result in results
            ),
            "digest": digest_hashes([result.preserved_digest_after for result in results]),
        },
        "changed": changed,
        "errors": errors,
    }


def print_human_summary(results: list[NotebookResult], *, label: str) -> None:
    summary = result_summary(results)
    print(
        f"{label}: {summary['notebook_count']} notebooks, "
        f"{summary['changed_count']} needing update, "
        f"{summary['preserved_cell_count']} authored cells audited."
    )
    print(f"current setup block counts: {summary['current_setup_block_counts']}")
    print(
        "preservation audit: "
        + ("passed" if summary["preservation_audit"]["passed"] else "failed")
        + f" ({summary['preservation_audit']['digest']})"
    )
    if summary["errors"]:
        print("errors:", file=sys.stderr)
        for path, errors in summary["errors"].items():
            for error in errors:
                print(f"- {path}: {error}", file=sys.stderr)
    if summary["changed"]:
        preview = "\n".join(f"- {path}" for path in summary["changed"][:20])
        print("notebooks needing update:")
        print(preview)
        if len(summary["changed"]) > 20:
            print(f"- ... {len(summary['changed']) - 20} more")


def write_changed(
    originals: list[tuple[Path, dict[str, Any]]],
    transformed: list[tuple[Path, dict[str, Any]]],
) -> int:
    written = 0
    for (path, original), (_, expected) in zip(originals, transformed, strict=True):
        newline_cleanup_needed = b"\r\r\n" in path.read_bytes()
        if notebooks_differ(original, expected) or newline_cleanup_needed:
            text = notebook_text(expected, newline=newline_for(path))
            write_text_controlled(path, text)
            written += 1
    return written


def write_text_controlled(path: Path, text: str) -> None:
    tmp = path.with_name(f".{path.name}.{os.getpid()}.setup.tmp")
    last_error: OSError | None = None
    for attempt in range(6):
        try:
            with tmp.open("w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            tmp.replace(path)
            return
        except OSError as exc:
            last_error = exc
            try:
                if tmp.exists():
                    tmp.unlink()
            except OSError:
                pass
            time.sleep(0.25 * (attempt + 1))
    assert last_error is not None
    raise last_error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail if notebooks are not up to date")
    mode.add_argument("--write", action="store_true", help="insert or replace managed setup cells")
    mode.add_argument("--report", action="store_true", help="emit a JSON setup/preservation report")
    args = parser.parse_args(argv)

    originals, transformed, results = analyze_all()
    summary = result_summary(results)
    has_errors = bool(summary["errors"])

    if args.report:
        print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
        return 1 if has_errors else 0

    if args.check:
        print_human_summary(results, label="setup check")
        if has_errors or summary["changed_count"]:
            return 1
        return 0

    if has_errors:
        print_human_summary(results, label="setup write preflight")
        return 1
    written = write_changed(originals, transformed)
    _, _, after_results = analyze_all()
    after_summary = result_summary(after_results)
    print_human_summary(after_results, label=f"setup write complete ({written} written)")
    if after_summary["errors"] or after_summary["changed_count"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
