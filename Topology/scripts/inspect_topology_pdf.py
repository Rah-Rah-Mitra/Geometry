"""Read-only source inventory helper for the imposed Topology PDF."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def extract_text(pdf: Path) -> str:
    return subprocess.check_output(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"], text=True, errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(Path(__file__).resolve().parents[1] / "Topology.pdf"))
    args = parser.parse_args()
    pdf = Path(args.pdf)
    text = extract_text(pdf)
    pages = [page for page in text.split("\f") if page.strip()]
    print(f"{pdf.name}: {len(pages)} extracted physical pages")
    for marker in ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4", "Chapter 5", "Chapter 6", "Chapter 7", "Chapter 8", "Chapter 9", "Chapter 10", "Chapter 11", "Chapter 12", "Chapter 13", "Bibliography", "Index"]:
        hits = [i + 1 for i, page in enumerate(pages) if marker in page]
        if hits:
            print(f"{marker}: first extracted physical pages {hits[:5]}")
    print("Use printed page spans from topology_inventory.py because this PDF is imposed.")


if __name__ == "__main__":
    main()
