# Chapter Workers CSV Fan-Out

Use this template when `spawn_agents_on_csv` is available and the book has many similar chapter tasks. This workflow is experimental in Codex, so keep concurrency explicit and require every worker to report a structured result.

Subagent capacity is shared across Codex sessions working on this repo. Before launching a large CSV batch, check whether another Codex session is already using the Geometry subagent pool. If it is, lower `max_concurrency` or wait so follow-up sessions can still spawn QC, validation, or emergency fix workers.

## Input CSV

Create one CSV row per chapter with these columns:

```csv
chapter_id,chapter_title,source_pages,notebook_path,artifact_subtree,brief_path
```

Optional useful columns:

```csv
course_root,agents_path,pdf_path,chapter_folder,validation_hint,worker_scope
```

## Planner Batch

Spawn one `geometry_visual_planner` per row. If the batch tool exposes an agent or role selector, set it to `geometry_visual_planner`. Otherwise, include this at the start of the worker instruction:

```text
Use the custom agent geometry_visual_planner for this row.
```

Worker instruction template:

```text
Read course AGENTS.md, the assigned source pages {source_pages}, and the geometry library catalog.
Create a chapter-specific visualization storyboard for {chapter_id}: {chapter_title}.
Notebook path: {notebook_path}
Artifact subtree: {artifact_subtree}
Write no files. Return JSON via report_agent_job_result with keys:
chapter_id, chapter_title, files_read, source_span_read, library_routing_summary,
visual_count, artifact_plan, acceptance_criteria, risks, gaps.
```

Recommended batch controls:

```text
max_concurrency: 8 to 12
max_runtime_seconds: 3600
output_csv_path: <course_root>/planning-results.csv
```

## Author Batch

Run author workers only after chapter briefs exist. Spawn one `geometry_chapter_author` per row. If the batch tool exposes an agent or role selector, set it to `geometry_chapter_author`. Otherwise, include this at the start of the worker instruction:

```text
Use the custom agent geometry_chapter_author for this row.
```

Worker instruction template:

```text
Read course AGENTS.md, the assigned source pages {source_pages}, and the approved brief at {brief_path}.
Implement the canonical notebook at {notebook_path} directly.
Write only the assigned chapter folder and {artifact_subtree}, plus explicitly assigned helpers if worker_scope names any.
Do not use a monolithic notebook generator. Do not populate generic notebooks.
Use the geometry library catalog and implement chapter-specific visuals.
Run the narrowest relevant checks from course AGENTS.md.
Return JSON via report_agent_job_result with keys:
chapter_id, notebook_path, files_read, files_changed, artifacts_generated,
libraries_used, checks_run, validation_result, gaps.
```

Recommended batch controls:

```text
max_concurrency: 8 to 12
max_runtime_seconds: 7200
output_csv_path: <course_root>/implementation-results.csv
```

## Consolidation

After the batch finishes:

- Inspect the output CSV for `status`, `last_error`, and `result_json`.
- Assign one `geometry_index_builder` after successful chapter work.
- Assign one `geometry_notebook_qc` and one `geometry_validation_worker` after implementation.
- Keep `agents.max_depth = 1`; batch workers must not spawn nested workers.
- If another Codex session also needs this repo, reserve spare subagent capacity instead of saturating all 16 threads.
