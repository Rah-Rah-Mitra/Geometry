# Implement Course With Subagents

Use this prompt after chapter-specific briefs or storyboards exist.

## Parent Setup

1. Read the course AGENTS.md, approved chapter briefs, repo-local skills, and geometry library catalog.
2. Confirm each implementation row has chapter_id, source_pages, notebook_path, artifact_subtree, and brief_path.
3. Keep `agents.max_depth = 1`. Chapter workers must not spawn workers.
4. Cap active chapter authors at 8 to 12 even when `agents.max_threads = 16`.

## Worker Allocation

Spawn custom agents by name:

- `geometry_chapter_author`: one worker per assigned chapter folder.
- `geometry_artifact_engineer`: one worker only for shared utilities or difficult shared visual assets.
- `geometry_index_builder`: one worker after chapter workers finish.
- `geometry_validation_worker`: one worker after implementation for scoped checks.

## Chapter Author Instruction

For each `geometry_chapter_author`:

- read the course AGENTS.md
- read the assigned source pages before editing
- read the approved brief/storyboard
- write only the assigned chapter folder and matching artifact subtree
- use the geometry library catalog
- choose concept-appropriate libraries from the installed geometry stack
- implement the canonical notebook directly
- do not use monolithic notebook generators
- do not mass-populate generic notebooks
- include original prose, visual explanations, code experiments, artifacts, applied labs, sanity checks, and takeaways
- run the narrowest relevant course checks
- return a structured report with files read, files changed, artifacts generated, libraries used, checks run, validation result, and gaps

## Shared Utility Guardrail

Only one `geometry_artifact_engineer` may edit shared helpers at a time. The parent must name the exact files or artifact subtree it owns.

## Index And Validation

After chapter authors finish:

1. Spawn `geometry_index_builder` to update 00-book-index.ipynb and chapter 00-index.ipynb files only.
2. Spawn `geometry_validation_worker` to run compileall, relevant audits, limited nbclient validation, and git diff --check.
3. Do not run full expensive notebook validation unless the course AGENTS.md or parent task requires it.

## Final Parent Report

Return:

- completed chapters
- changed files by worker
- artifacts generated
- libraries used by chapter
- indexes updated
- validation commands and results
- failed workers or gaps
- follow-up fixes
