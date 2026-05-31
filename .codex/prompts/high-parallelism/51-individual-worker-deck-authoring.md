# Individual Worker: Author One Chapter Slide Deck

This is the per-worker checklist for authoring a single Geometry lecture deck
when the parent coordinator hands you one manifest row. It distills
`50-implement-repo-wide-slides-with-subagents.md` down to the steps an
individual worker (human or model) performs end-to-end on one chapter.

You own **exactly one row**. Do not edit unrelated chapters, shared utilities,
indexes, manifests, validation scripts, or the design system.

## Inputs You Receive

From the parent you must have, before starting:

- `course_root` and `course_title`
- `chapter_id` and `chapter_title`
- `notebook_path` (canonical teaching notebook for the chapter)
- `source_span` (printed pages and PDF pages)
- `pdf_path` (relative path to the source PDF)
- `deck_path` (the HTML file you will create)
- `notes_path` (the speaker-notes JSON you will create)
- `artifact_subtree` (e.g., `<course>/artifacts/<chapter-id>`)
- `worker_scope` (the chapter-notebook directory and the slides directory)

If any of those is missing, stop and ask the parent for a corrected row. Do
not improvise paths.

## Step 1: Ground Yourself in the Chapter

Read in this order. Read, do not skim.

1. The course `AGENTS.md` and the course `00-book-index.ipynb` for tone,
   chapter boundaries, and any course-specific conventions.
2. The assigned `notebook_path` end-to-end. Note the chapter question, the
   organizing themes, the worked examples, and the artifacts the notebook
   already generated.
3. The relevant pages of the source PDF for the assigned `source_span`. Use
   this for orientation only. **Do not copy textbook prose, screenshots,
   page crops, copied figures, long exercise text, solution text, or page
   layouts.** Restate every idea in your own words.
4. `lecture-design-system/README.md` and `lecture-design-system/slides/`
   (especially `deck-stage.js`, `index.html`, `compact-templates.html`).
5. One peer deck from the same course — or a structurally similar course —
   as a template (e.g.
   `A-Course-in-Metric-Geometry/artifacts/chapter-01/slides/chapter-01-lecture.html`).

By the end of this step you should be able to write, in two sentences, the
chapter's central question and the four to eight conceptual moves the
lecture will make.

## Step 2: Draft a Chapter-Specific Brief

Before you write HTML, write a short brief (in your scratch space; do not
commit it). The brief must be specific to this chapter, not a generic outline.
Include:

- A one-sentence chapter question that the lecture will answer.
- A list of 10–16 slide stops, each with a label, the one mathematical idea
  it teaches, and what visual element (SVG, equation panel, comparison, small
  table) carries that idea.
- A "source grounding" stop that names the notebook path and the source span
  in plain text on a visible slide (this is also enforced by the audit).
- A short closing recap stop that ties the slides into one pipeline.

A reusable, course-agnostic outline ("intro / definition / example / theorem /
recap") is a failure. The brief must read like *this* chapter, not any
chapter.

## Step 3: Author the HTML Deck

Create exactly one HTML file at `deck_path`. Mirror the structure of the
exemplar peer deck. The deck **must** contain:

- `<!DOCTYPE html>` with `lang="en"`, viewport meta, and a `<title>` matching
  the chapter title.
- Required `<meta>` tags with `name=` of: `course`, `chapter_id`,
  `notebook_path`, `source_span`, `source_pdf`, `design_system_version`.
  Values must match the manifest row exactly.
- A link to `lecture-design-system/colors_and_type.css` using the correct
  relative path from the deck's slides directory.
- A `<script src="...lecture-design-system/slides/deck-stage.js">` reference
  (audit checks for the literal `deck-stage.js` token).
- KaTeX CDN links and the auto-render initializer, matching the peer deck.
- A `<script type="application/json" id="deck-metadata">` block restating the
  six metadata fields.
- A `<script type="application/json" id="speaker-notes">` block with an array
  of narration strings, one per slide, in slide order. Each must be a full
  paragraph (≥ 25 words; the audit enforces this).
- A `<deck-stage width="1920" height="1080">` element wrapping each slide as
  a `<section>`.
- Inside every `<section>`, an `<aside class="speaker-notes">` element with
  substantive instructor narration. (Set `.speaker-notes { display: none }`
  in the deck CSS so it does not render visually, matching peer decks.)
- The first content slide must visibly mention the notebook path or the
  source span (the audit greps for them in the visible text).

Slide content rules:

- Restate every idea in your own words. Translate textbook prose into
  diagrams, equations, small tables, comparisons, and step-by-step
  derivations.
- Build SVGs inline. Reuse the visualization patterns and color tokens from
  the design system. Do not include rasterized textbook scans.
- Equations go in `\\( ... \\)` (inline) or `$$ ... $$` (display) for KaTeX.
- Stay readable at 1920×1080. Use the CSS classes from the peer deck
  (`.slide`, `.cols`, `.panel`, `.visual-card`, `.chain`, etc.).
- Keep the deck self-contained: every link target must resolve to a file in
  your `artifact_subtree`, in `lecture-design-system/`, or to a public CDN
  asset that the peer decks already use.

## Step 4: Author the Speaker-Notes JSON

Create exactly one JSON file at `notes_path`. **Use a top-level list**
(matching the dominant convention), one entry per slide in deck order:

```json
[
  {
    "slide": 1,
    "label": "Title",
    "notes": "Open by ... (≥ 25 words, instructor-voice narration)."
  },
  ...
]
```

Do **not** use a top-level dict with `chapter_id`/`course`/`slides` keys —
the audit recursively counts string values in dicts, so short metadata fields
will be flagged as terse narration. (See the converted Four-Pillars notes
files for prior art.)

Speaker notes must read like instructor dialogue, not slide labels.

## Step 5: Slide-Local Assets

If your chapter needs supplementary diagrams beyond what fits inline (e.g.,
larger SVGs, generated PNG figures), drop them inside the same
`*/slides/` directory or a sibling `*/slides/assets/` directory. Reference
them with relative paths from the deck. Do not write to other chapters'
artifact subtrees.

## Step 6: Self-QC Before Handing Back

Run, from the repo root:

```powershell
uv run python scripts/audit_slide_decks.py --manifest slide-deck-manifest.json --deck <your deck_path>
uv run python scripts/validate_slide_deck_layouts.py --manifest slide-deck-manifest.json --deck <your deck_path> --viewport 1920x1080
```

(If your local script does not support `--deck`, use `--changed-only` after
staging your files.)

Also confirm by hand:

- The deck is chapter-specific and learnable without opening the textbook.
- The first slides visibly ground the lecture in the assigned notebook and
  source span.
- Every slide teaches actual mathematical content, not generic framing.
- Speaker notes read like instructor dialogue, not labels or reminders.
- All local link targets exist.
- No copied prose, screenshots, crops, figures, long exercises, solutions,
  or page-layout mimicry.

## Step 7: Hand Back to the Parent

Report:

- The manifest row you owned.
- The deck and notes files you wrote (with relative paths).
- Any slide-local assets you created.
- The QC commands you ran and their outcomes.
- Any open questions for the parent (do not edit indexes or manifests
  yourself — leave that for the assigned index-and-integration pass).

## Hard Don'ts

- Do not mass-generate decks or write a generic deck generator.
- Do not edit other chapters, indexes, manifests, validation scripts, or the
  design system.
- Do not copy textbook prose, screenshots, page crops, copied figures, long
  exercise text, solution text, or page layouts.
- Do not produce PDF/PPTX exports. The parent runs export only after deck
  QC passes.
- Do not spawn subagents. The parent owns coordination.
