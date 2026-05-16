"""Run the vendored read-only DjVu text extractor."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    env = os.environ.copy()
    env.setdefault("CARGO_TARGET_DIR", str(BOOK_ROOT / ".cargo-target"))
    subprocess.run(
        [
            "cargo",
            "run",
            "--manifest-path",
            str(BOOK_ROOT / "vendor" / "djvu_text_extractor" / "Cargo.toml"),
            "--",
            str(BOOK_ROOT / "Methods of Information Geometry.djvu"),
            str(BOOK_ROOT / "source" / "djvu_text"),
        ],
        check=True,
        cwd=BOOK_ROOT,
        env=env,
    )


if __name__ == "__main__":
    main()

