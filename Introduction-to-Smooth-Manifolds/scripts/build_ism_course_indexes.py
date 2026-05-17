from __future__ import annotations
import json
from pathlib import Path
BOOK_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = json.loads((BOOK_ROOT / "source_map.json").read_text(encoding="utf-8"))
def cell(kind: str, source: str) -> dict:
    base = {"cell_type": kind, "metadata": {}, "source": source.strip() + "\n"}
    if kind == "code":
        base.update({"execution_count": None, "outputs": []})
    return base
def nb(cells: list[dict]) -> dict:
    return {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
def write(path: Path, cells: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb(cells), indent=1) + "\n", encoding="utf-8")
def main() -> None:
    rows = []
    for item in SOURCE_MAP["units"]:
        rows.append(f"| {item['label']} | {item['title']} | {item.get('printed', '')} | [`{item['notebook']}`]({item['folder_path']}/{item['notebook']}) |")
        write(BOOK_ROOT / item["folder_path"] / "00-index.ipynb", [
            cell("markdown", f"# {item['label']}: {item['title']}\n\nSource span: printed pages `{item.get('printed', '')}`.\n\nCanonical notebook: [`{item['notebook']}`]({item['notebook']}).\n\nFocus: {item.get('focus', '')}"),
            cell("code", "from pathlib import Path\nBOOK_ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents] if (p / 'source_map.json').exists())\nprint(BOOK_ROOT.name)"),
        ])
    table = "| Unit | Title | Printed Pages | Notebook |\n| --- | --- | ---: | --- |\n" + "\n".join(rows)
    write(BOOK_ROOT / "00-book-index.ipynb", [
        cell("markdown", f"# {SOURCE_MAP['title']}\n\nStandalone visualization-first notebook course. Source method: {SOURCE_MAP['source_method']}.\n\n" + table),
        cell("code", "import json\nfrom pathlib import Path\nsource = json.loads((Path.cwd() / 'source_map.json').read_text()) if (Path.cwd() / 'source_map.json').exists() else json.loads((Path.cwd().parent / 'source_map.json').read_text())\nprint(f\"{source['title']}: {len(source['units'])} canonical units\")"),
    ])
if __name__ == "__main__":
    main()
