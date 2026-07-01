import json

from scripts.build_slide_deck_manifest import DEFAULT_OUTPUT, build_manifest


def test_build_manifest_preserves_pdf_paths_in_source_light_checkout():
    checked_in = json.loads(DEFAULT_OUTPUT.read_text(encoding="utf-8"))
    expected_by_notebook = {
        row["notebook_path"]: row["pdf_path"]
        for row in checked_in["decks"]
    }

    generated, errors = build_manifest()

    assert not errors
    missing = [
        row["notebook_path"]
        for row in generated["decks"]
        if not row.get("pdf_path")
    ]
    assert not missing
    assert {
        row["notebook_path"]: row["pdf_path"]
        for row in generated["decks"]
    } == expected_by_notebook
