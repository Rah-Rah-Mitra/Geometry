import sys
from pathlib import Path

import nbformat as nbf

BOOK_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pag_inventory as inv


def markdown_cell(text):
    return nbf.v4.new_markdown_cell(text)


def code_cell(text):
    return nbf.v4.new_code_cell(text)


def write_notebook(path, cells):
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb["metadata"]["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    nbf.write(nb, path)


def chapter_index(entry):
    section_lines = "\n".join(
        f"- Printed p. {item['printed_start']} / PDF p. {item['pdf_start']}: {item['title']}"
        for item in entry.get("sections", [])
    )
    notebook = entry["notebook"]
    artifact_root = f"../artifacts/{entry['topic']}"
    return [
        markdown_cell(
            f"# {entry['label']}: {entry['title']}\n\n"
            f"**Source span.** Printed pages {entry['printed_span']}; PDF pages {entry['pdf_span']}.\n\n"
            f"**Canonical notebook.** [{notebook}]({notebook})\n\n"
            f"**Artifact root.** `{artifact_root}`\n\n"
            f"## Section Map\n\n{section_lines}\n\n"
            "Use this index as a navigation map only. The chapter notebook contains the original standalone lesson, visuals, and checks."
        ),
        code_cell(
            "from pathlib import Path\n"
            f"notebook = Path('{notebook}')\n"
            f"artifact_root = Path('{artifact_root}')\n"
            "assert notebook.exists()\n"
            "assert artifact_root.exists()\n"
            "(notebook, artifact_root)"
        ),
    ]


def book_index():
    rows = []
    for entry in inv.ENTRIES:
        rows.append(
            "| {label} | {title} | {printed} | {pdf} | [{notebook}]({folder}/{notebook}) | `{topic}` |".format(
                label=entry["label"],
                title=entry["title"],
                printed=entry["printed_span"],
                pdf=entry["pdf_span"],
                folder=entry["folder"],
                notebook=entry["notebook"],
                topic=entry["topic"],
            )
        )
    table = "\n".join(
        [
            "| Chapter | Title | Printed pages | PDF pages | Notebook | Artifact topic |",
            "|---|---|---:|---:|---|---|",
            *rows,
        ]
    )
    return [
        markdown_cell(
            f"# {inv.BOOK_TITLE}\n\n"
            f"Author: {inv.BOOK_AUTHOR}\n\n"
            "This is the book-level index for the visualization-first notebook course. "
            "Each canonical chapter notebook is source-grounded, original in prose and code, "
            "and backed by local artifact checks.\n\n"
            f"{table}"
        ),
        code_cell(
            "from pathlib import Path\n"
            "root = Path.cwd()\n"
            "notebooks = [\n"
            + "\n".join(
                f"    root / '{entry['folder']}' / '{entry['notebook']}',"
                for entry in inv.ENTRIES
            )
            + "\n]\n"
            "missing = [path for path in notebooks if not path.exists()]\n"
            "assert not missing, missing\n"
            "len(notebooks)"
        ),
    ]


def main():
    write_notebook(BOOK_ROOT / "00-book-index.ipynb", book_index())
    for entry in inv.ENTRIES:
        write_notebook(BOOK_ROOT / entry["folder"] / "00-index.ipynb", chapter_index(entry))
    print(f"wrote {1 + len(inv.ENTRIES)} index notebooks")


if __name__ == "__main__":
    main()
