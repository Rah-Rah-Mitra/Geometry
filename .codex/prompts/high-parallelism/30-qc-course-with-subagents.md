# QC Course With Subagents

Use this prompt after implementation workers have completed chapter notebooks and artifacts.

## Parent Setup

1. Read course AGENTS.md, changed-file list, implementation reports, and validation hints.
2. Keep `agents.max_depth = 1`.
3. Use read-only QC first. Fixing passes require explicit write scopes.
4. Check whether other Codex sessions are using Geometry subagents. If a session cannot spawn any QC workers because the shared pool is exhausted, adjust `agents.max_threads` within the approved ceiling range or stop/finish existing workers before retrying.

## QC Workers

Spawn `geometry_notebook_qc` agents by custom agent name:

- one QC worker per chapter for large courses, or one QC worker per small chapter batch
- cap active QC concurrency at 8 to 12
- if another session cannot spawn workers, treat it as a configured-ceiling issue and raise `agents.max_threads` within the approved range
- each QC worker reads the assigned notebook, artifacts, source-map notes, AGENTS.md, and relevant scripts
- each QC worker uses the geometry library catalog
- QC workers do not edit files

Each QC worker must check:

- standalone teaching quality
- source grounding
- chapter-specific terms, definitions, constructions, examples, proof moves, pitfalls, labs, and takeaways
- visual relevance and learner inspection targets
- whether library choices match the chapter concept
- stale or root-hardcoded paths
- nonzero artifacts and inline displays
- generic notebook factories, repeated markdown shingles, repeated code fingerprints, and repeated placeholder visuals
- copyright constraints
- execution readiness and final sanity checks

Each QC worker returns a structured report:

```json
{
  "chapter_id": "",
  "files_read": [],
  "pass_fail": "",
  "standalone_teaching_issues": [],
  "visualization_issues": [],
  "artifact_issues": [],
  "execution_issues": [],
  "generic_generation_warnings": [],
  "recommended_fixes": [],
  "checks_run": [],
  "gaps": []
}
```

## Validation Worker

Spawn one `geometry_validation_worker` after QC triage. It should:

- run compileall for course utils/scripts
- run available notebook audits and visual audits
- run artifact audits when present
- run limited nbclient validation when appropriate
- run git diff --check
- fix only high-confidence mechanical issues within assigned files
- report conceptual gaps rather than rewriting chapters

## Parent Consolidation

Return:

- pass/fail summary
- highest-priority findings
- chapters needing fixes
- validation commands and results
- mechanical fixes applied
- conceptual gaps
- recommended next implementation batch
