# Plan Course With Subagents

Use this prompt to plan a visualization-first course before implementation.

## Parent Setup

1. Read the repo-local skills:
   - D:/Geometry/.codex/skills/geometry-visualization-planner/SKILL.md
   - D:/Geometry/.codex/skills/geometry-chapter-notebook-author/SKILL.md
   - D:/Geometry/.codex/skills/geometry-notebook-qc/SKILL.md
2. Read the course AGENTS.md if present.
3. Spawn `geometry_book_mapper` to map the PDF, chapter/appendix spans, section hierarchy, source mapping, existing folders, scripts, indexes, and artifact conventions.
4. Build a chapter manifest with chapter_id, chapter_title, source_pages, notebook_path, artifact_subtree, and brief_path.

## Chapter Planning

Spawn `geometry_visual_planner` agents, one per chapter or small chapter batch. Cap active planning concurrency at 8 to 12 even when `agents.max_threads = 16`.

Each planner must:

- read the assigned source pages
- read the course AGENTS.md
- use the geometry library catalog
- choose libraries by concept rather than defaulting to Matplotlib
- produce a chapter-specific storyboard
- write no files unless explicitly told to save a brief
- avoid copied textbook prose, screenshots, page crops, figures, and page layouts
- return a structured report with files read, source span, library routing, visual sequence, artifact plan, checks, risks, acceptance criteria, and gaps

## Parent Consolidation

Merge planner outputs into a course implementation plan:

- chapter manifest
- source span map
- per-chapter storyboard status
- utility/helper needs
- artifact plan
- worker allocation for implementation
- validation sequence
- risks and gaps

Do not start implementation until the chapter briefs are specific enough for one `geometry_chapter_author` to work independently.
