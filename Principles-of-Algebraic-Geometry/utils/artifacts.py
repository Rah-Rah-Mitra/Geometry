import json
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]


def ensure_dir(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def chapter_artifact_dirs(topic):
    root = BOOK_ROOT / "artifacts" / topic
    return {
        "root": ensure_dir(root),
        "figures": ensure_dir(root / "figures"),
        "html": ensure_dir(root / "html"),
        "checks": ensure_dir(root / "checks"),
        "data": ensure_dir(root / "data"),
    }


def save_json(data, path):
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    return path


def save_text(text, path):
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(text, encoding="utf-8")
    return path


def relative_artifact(path):
    path = Path(path)
    try:
        return path.relative_to(BOOK_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def artifact_record(path):
    path = Path(path)
    return {
        "path": relative_artifact(path),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
    }


def assert_artifacts(paths, min_bytes=40):
    records = [artifact_record(path) for path in paths]
    missing = [record for record in records if not record["exists"] or record["bytes"] <= min_bytes]
    if missing:
        raise AssertionError(f"missing or tiny artifacts: {missing}")
    return records


def display_artifact(path, width=760):
    path = Path(path)
    suffix = path.suffix.lower()
    try:
        from IPython.display import HTML, Image, display
    except ImportError:
        return path
    if suffix == ".png":
        display(Image(filename=str(path), width=width))
    elif suffix in {".html", ".svg"}:
        display(HTML(path.read_text(encoding="utf-8")))
    else:
        display(path)
    return path
