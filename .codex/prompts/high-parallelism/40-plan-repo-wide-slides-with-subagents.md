# Plan Repo-Wide Slides With Subagents

Use this prompt to plan a full repo-wide implementation of chapter lecture slide
decks for `D:/Geometry`. Do not implement yet. Produce a decision-complete plan
suitable for multiple Codex agents.

## Setup

First inspect the repo: root README, `course-manifest.json`, `.codex/agents`,
`.codex/prompts`, repo-local geometry skills, `D:/Geometry/lecture-design-system`,
and representative course `AGENTS.md` files. Use course `AGENTS.md` files and
source maps as the source of truth for chapter folders, notebooks, PDF names,
printed pages, PDF pages, worker boundaries, and validation commands.

## Goal

Every canonical chapter/notebook eventually receives a companion academic
lecture deck. The deck must be authored from that specific notebook plus its
assigned textbook source span. Do not mass-generate decks across the repo. Do
not write a monolithic script that fabricates PowerPoint or HTML from generic
templates. Scripts may only support indexing, validation, export, and
mechanical checks.

## Plan Stages

1. Inventory all courses and canonical notebooks from `course-manifest.json` and
   course `AGENTS.md` files.
2. Define a slide-deck manifest row format: `course_root`, `course_title`,
   `chapter_id`, `chapter_title`, `source_span`, `pdf_path`, `notebook_path`,
   `artifact_subtree`, `deck_path`, `notes_path`, `worker_scope`.
3. Create planner batches: one slide planner per assigned chapter/notebook. Each
   planner must read the notebook, course `AGENTS.md`, source span, and lecture
   design system before proposing deck structure.
4. Create author batches only after chapter-specific slide briefs exist. One
   author owns one chapter deck and matching slide artifact subtree. Authors may
   not edit unrelated chapters, shared utilities, or indexes unless explicitly
   assigned.
5. Create index, QC, and validation passes after deck authors finish.

## Deck Quality Requirements

- Slightly dense academic slides: definitions, theorem statements, proof
  roadmaps, worked examples, diagrams, formulas, misconceptions, exercises, and
  recap slides as appropriate.
- Full instructor speaker dialogue for every slide, written as actual teaching
  narration, not terse presenter notes.
- Slide content must be original teaching prose. No copied textbook paragraphs,
  long exercise text, screenshots, page crops, or traced textbook figures.
- Each deck must cite its source span as provenance but be learnable without
  opening the textbook.
- Visuals must teach a concept; each major visual needs a nearby explanation of
  what to inspect.
- Use the Geometry Lecture Design System: 1920x1080 HTML decks, `deck-stage.js`,
  KaTeX/STIX math, semantic math boxes, and the existing visualization catalog
  when appropriate.
- HTML is the canonical editable deck source. PDF/PPTX export, if planned, must
  be per-deck after QC, not a bulk substitute for academic authoring.

## Validation Rules

- Manifest coverage: every planned deck maps to exactly one canonical notebook
  and one source span.
- Source grounding: deck metadata, visible intro, and speaker notes name the
  chapter/notebook/source span.
- Anti-generic audit: flag repeated slide outlines, repeated prose shingles,
  placeholder diagrams, identical speaker notes, and decks with only title
  substitutions.
- Speaker dialogue audit: every slide has substantive instructor dialogue; no
  empty notes; no repeated stock narration.
- Visual audit: no decorative-only diagrams; no broken SVG/HTML/image links;
  visuals are nonblank and relevant.
- Layout audit: rendered slides are 1920x1080, no overflowing text, no incoherent
  overlaps, math renders, and deck navigation works.
- Copyright audit: no textbook screenshots, copied figures, page crops, long
  passages, or solution copying.
- Script audit: reject mass deck generators; allow only validators, exporters,
  index updaters, and small helpers.
- Execution checks: run `git diff --check`, targeted link/layout validators, and
  course-local checks where deck index links are changed.

## Subagent Rules

- Keep `agents.max_depth = 1`.
- Parent agent coordinates; workers do not spawn workers.
- Cap active chapter slide workers around 8-12 even if `max_threads` is higher.
- Shared design-system changes belong to one explicitly assigned worker only.
- Every worker reports files read, source span used, files changed, slides
  authored, visuals used, speaker-dialogue status, checks run, and gaps.

## Required Final Plan

Return the final plan with: summary, repo interfaces/paths, worker roles,
manifest format, phased implementation, validation commands, acceptance
criteria, risks, and assumptions.
