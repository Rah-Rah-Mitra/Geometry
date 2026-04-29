"""Smoke test the packages used by the Directional Statistics course."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

MODULES = ["numpy", "scipy", "matplotlib", "plotly", "PIL", "nbformat", "nbclient"]


def main() -> None:
    versions = {}
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        versions[module_name] = str(getattr(module, "__version__", "unknown"))
    print(json.dumps({"status": "ok", "versions": versions}, indent=2))


if __name__ == "__main__":
    main()
