# Implement Repo-Wide Slides With Subagents

Use this prompt to implement chapter-specific Geometry lecture decks in staged,
high-parallelism batches. This is for authored decks, not generic generation.

## Setup

Start at `D:/Geometry`. Inspect the root README, `course-manifest.json`,
`slide-deck-manifest.json`, `.codex/agents`, `.codex/prompts`, repo-local
geometry skills, `lecture-design-system`, the relevant course `AGENTS.md`, and
the relevant source maps.

Use these source-of-truth interfaces:

- `course-manifest.json`: canonical notebook inventory.
- `slide-deck-manifest.json`: planned lecture deck rows for `kind == "lesson"`.
- Course `AGENTS.md` and source maps: folders, source spans, PDF/DJVU names,
  worker boundaries, and validation commands.
- `lecture-design-system`: 1920x1080 HTML, `deck-stage.js`, KaTeX/STIX,
  semantic math boxes, and visualization catalog.

## Non-Negotiables

- Do not mass-generate decks.
- Do not write a monolithic HTML, PDF, PPTX, or PowerPoint deck generator.
- HTML is the deck source of record.
- PDF/PPTX export is per deck after QC only.
- Do not copy textbook prose, long exercise text, screenshots, page crops,
  copied figures, solution text, or page layouts.
- One author owns one chapter deck plus its matching slide artifact subtree.
- Authors may not edit unrelated chapters, shared utilities, indexes, manifests,
  validation scripts, or the design system unless explicitly assigned.

## Staged Workflow

1. Manifest gate
   - Run `uv run python scripts/build_slide_deck_manifest.py --check`.
   - Select a bounded batch of manifest rows.
   - Confirm each row has a specific notebook, source span, PDF/DJVU path, deck
     path, notes path, and worker scope.

2. Planner batches
   - Spawn `geometry_slide_planner` workers only after assigning concrete rows.
   - Keep `agents.max_depth = 1`.
   - The parent/root agent coordinates all workers; workers do not spawn workers.
   - Cap active slide workers around 8-12.
   - Each planner reads the row, notebook, source map/source span, course
     `AGENTS.md`, and lecture design system.
   - Output must be a chapter-specific slide brief, not a reusable generic deck
     outline.

3. Author batches
   - Start `geometry_slide_author` workers only after chapter-specific briefs
     exist and have enough detail to author from.
   - Assign one author to one deck path and one notes path.
   - Author only the assigned HTML deck, speaker-notes JSON, and slide-local
     assets in the matching artifact subtree.
   - Every slide needs substantive `<aside class="speaker-notes">` narration.
   - Metadata must include course, chapter_id, notebook_path, source_span,
     source_pdf, and design_system_version.

4. Index and integration
   - Add deck links to course indexes only in a separate, explicitly assigned
     index pass.
   - Do not let chapter authors edit indexes incidentally.
   - Preserve source maps and manifests unless the parent explicitly assigns a
     manifest/index maintenance task.

5. QC and validation
   - Run `geometry_slide_qc` after deck authoring.
   - Run root validators:

```powershell
uv run python scripts/audit_slide_decks.py --manifest slide-deck-manifest.json --changed-only
uv run python scripts/validate_slide_deck_layouts.py --manifest slide-deck-manifest.json --changed-only --viewport 1920x1080
uv run python -m compileall -q scripts
git -c safe.directory=D:/Geometry diff --check
```

   - Run course-local commands from the relevant `AGENTS.md` when indexes,
     helpers, or course-local validation files change.

## Deck Acceptance Criteria

- The deck is chapter-specific and learnable without opening the textbook.
- The first slides visibly ground the lecture in the assigned notebook and
  source span.
- The visual sequence teaches actual mathematical content.
- Speaker notes read like instructor dialogue, not labels or reminders.
- Layout is readable at 1920x1080 and navigates with `deck-stage.js`.
- All local links and slide assets resolve.
- Copyright guard passes: no copied textbook text, screenshots, crops, figures,
  long exercises, solutions, or page-layout mimicry.

## Final Report

Report the selected manifest rows, workers launched, files changed, decks
authored, notes files authored, assets created, checks run, QC findings fixed,
and remaining gaps. Keep any follow-up batch list explicit and row-based.
