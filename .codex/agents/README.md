# Geometry Subagent Orchestration

This repo uses project-scoped Codex custom agents for visualization-first textbook notebook work. The default shape is broad parallelism with shallow delegation:

- Keep `agents.max_depth = 1` unless nested delegation is explicitly requested.
- Only the parent/root agent should spawn chapter workers.
- Chapter workers must not spawn further workers unless the user explicitly authorizes nested delegation.
- Use one chapter worker per chapter folder.
- Use one utilities/artifact worker for shared code or difficult shared visuals.
- Use one index worker after chapter work completes.
- Use one QC or validation worker after implementation.
- Read-only agents must not request write access.
- Workspace-write agents must respect their assigned file boundaries.
- Shared utilities should be edited by one worker at a time.
- Raise `agents.max_threads` only when chapter briefs, source spans, and QC capacity are ready. More threads do not improve weak briefs.
- Treat the subagent cap as a global repo/session capacity constraint. If another Codex session is already using all available Geometry subagent threads, a new Codex session working on this repo may be unable to spawn additional subagents.
- When a Codex session cannot spawn any subagents because the shared pool is exhausted, adjust the configured ceiling instead of relying on spare-capacity discipline. For this repo, keep the ceiling at or below 20 unless the user explicitly requests a higher cap and accepts the machine-load tradeoff.

## Roles

- `geometry_book_mapper`: read-only book/PDF/course structure mapper.
- `geometry_visual_planner`: read-only chapter storyboard and library-routing planner.
- `geometry_chapter_author`: workspace-write author for one assigned chapter notebook and matching artifact subtree.
- `geometry_artifact_engineer`: workspace-write helper/artifact worker for assigned utilities or artifact subtrees.
- `geometry_index_builder`: workspace-write index updater for 00-book-index.ipynb and chapter 00-index.ipynb files.
- `geometry_notebook_qc`: read-only QC auditor for teaching quality, visuals, artifacts, repetition, execution readiness, and copyright constraints.
- `geometry_validation_worker`: workspace-write validation worker that fixes only high-confidence mechanical issues when assigned.

## Required Worker Report

Every worker must report:

- files read
- files changed
- artifacts generated
- checks run
- gaps

## Safe Batch Pattern

For many chapters, keep the flow staged:

1. Run `geometry_book_mapper` once per book to confirm structure and page spans.
2. Spawn `geometry_visual_planner` workers for chapter briefs, capped below the thread limit.
3. Spawn one `geometry_chapter_author` per chapter only after a chapter-specific brief exists.
4. Assign `geometry_artifact_engineer` to shared helpers or hard visual assets, with a unique write scope.
5. Run `geometry_index_builder` after chapter authors finish.
6. Run `geometry_notebook_qc` and `geometry_validation_worker` after implementation.

When running multiple Codex sessions against `D:/Geometry`, coordinate the ceiling deliberately. If a second session cannot spawn subagents because another session consumed the shared budget, raise `agents.max_threads` within the approved range or stop/finish existing workers before retrying.

CSV fan-out guidance lives in `D:/Geometry/.codex/prompts/subagent-batches/chapter-workers-csv.md`.
High-parallelism workflow prompts live in `D:/Geometry/.codex/prompts/high-parallelism/`.
