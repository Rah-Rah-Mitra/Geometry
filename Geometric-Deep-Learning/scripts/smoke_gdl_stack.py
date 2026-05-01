"""Smoke-test the libraries used by the GDL course."""

from __future__ import annotations

import importlib

MODULES = [
    "numpy",
    "scipy",
    "matplotlib",
    "plotly",
    "networkx",
    "pandas",
    "PIL",
    "nbformat",
    "nbclient",
]


def main() -> None:
    missing = []
    for module in MODULES:
        try:
            importlib.import_module(module)
        except Exception as exc:  # noqa: BLE001
            missing.append((module, repr(exc)))
    if missing:
        for module, error in missing:
            print(f"Missing {module}: {error}")
        raise SystemExit(1)
    print(f"GDL stack smoke test passed for {len(MODULES)} modules.")


if __name__ == "__main__":
    main()
