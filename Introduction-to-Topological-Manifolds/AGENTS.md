# Agent Instructions: Introduction to Topological Manifolds Notebook Course

This folder is a standalone visualization-first notebook edition of John M. Lee's *Introduction to Topological Manifolds*, Second Edition. Treat this folder as the project root for this course. The workspace root owns the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning or revising a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring a canonical notebook.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops, or figures.
- Use the PDF only for title, chapter structure, page spans, terminology, definitions, theorem orientation, and concept coverage.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualizations are part of the explanation, not decoration or a quota.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook plus `00-index.ipynb` per unit folder.

## Course Structure

```text
Introduction-to-Topological-Manifolds/
  00-book-index.ipynb
  AGENTS.md
  source_map.json
  artifacts/
  scripts/
  utils/
  chapter-01-introduction/
  ...
  chapter-13-homology/
  appendix-a-review-of-set-theory/
  appendix-b-review-of-metric-spaces/
  appendix-c-review-of-group-theory/
```

## Source Map

Source file: `Introduction to Topological Manifolds.pdf`.

The PDF has 444 pages. Printed page 1 appears at physical PDF page 19, so for body pages use approximately `pdf_page = printed_page + 18`.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Chapter 1 | `chapter-01-introduction` | 1-18 | 19-36 | Examples of manifolds, invariants, classification motivation, and homeomorphism intuition. |
| Chapter 2 | `chapter-02-topological-spaces` | 19-48 | 37-66 | Topological spaces, bases, manifolds, Hausdorff, second-countable, and local Euclidean checks. |
| Chapter 3 | `chapter-03-new-spaces-from-old` | 49-84 | 67-102 | Subspaces, products, disjoint unions, quotients, adjunction spaces, and quotient pathologies. |
| Chapter 4 | `chapter-04-connectedness-and-compactness` | 85-126 | 103-144 | Connectedness, path connectedness, compactness, local compactness, and manifolds with boundary. |
| Chapter 5 | `chapter-05-cell-complexes` | 127-158 | 145-176 | CW complexes, attaching maps, weak topology, cell structures, and 1-manifold classification. |
| Chapter 6 | `chapter-06-compact-surfaces` | 159-182 | 177-200 | Compact surfaces, connected sums, polygon schemas, orientability, and surface classification. |
| Chapter 7 | `chapter-07-homotopy-and-the-fundamental-group` | 183-216 | 201-234 | Paths, homotopy, fundamental group, functoriality, and categories. |
| Chapter 8 | `chapter-08-the-circle` | 217-232 | 235-250 | The circle covering map, lifting, winding number, and pi_1(S^1). |
| Chapter 9 | `chapter-09-some-group-theory` | 233-250 | 251-268 | Free groups, presentations, free products, and free abelian groups. |
| Chapter 10 | `chapter-10-the-seifert-van-kampen-theorem` | 251-276 | 269-294 | Seifert-van Kampen, graphs, CW complexes, and surface group presentations. |
| Chapter 11 | `chapter-11-covering-maps` | 277-306 | 295-324 | Covering maps, lifting, monodromy, and universal covers. |
| Chapter 12 | `chapter-12-group-actions-and-covering-maps` | 307-338 | 325-356 | Group actions, covering transformations, classification of coverings, and manifolds as quotients. |
| Chapter 13 | `chapter-13-homology` | 339-380 | 357-398 | Singular homology, homotopy invariance, Mayer-Vietoris, CW homology, Euler characteristic, and cohomology preview. |
| Appendix A | `appendix-a-review-of-set-theory` | 381-394 | 399-412 | Set operations, functions, relations, products, quotients, and countability prerequisites. |
| Appendix B | `appendix-b-review-of-metric-spaces` | 395-400 | 413-418 | Metric spaces, balls, convergence, continuity, compactness, and complete metric intuition. |
| Appendix C | `appendix-c-review-of-group-theory` | 401-406 | 419-424 | Groups, homomorphisms, quotients, products, presentations, and group actions needed later. |

## Notebook Shape

Each canonical notebook should contain:

- title and exact source span
- standalone chapter goal or question
- translation guide from topology to computational representations
- setup cell that discovers `BOOK_ROOT` robustly
- chapter-specific library routing and visual storyboard
- original concept sections with visuals and executable examples
- proof, invariant, counterexample, or finite-model scaffolds when useful
- at least one applied lab or exploratory activity when useful
- inline display of generated artifacts
- final sanity checks asserting mathematical invariants, artifact existence, nonzero artifact sizes, and path correctness
- takeaways

## Artifact Contract

Store generated outputs under `artifacts/<unit-key>/figures/`, `html/`, `checks/`, and `tables/`. Artifact filenames should name the concept, not the renderer. Every generated artifact should be displayed inline or linked from the notebook, and final checks should assert that files exist and are nonempty.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed libraries before adding dependencies: `numpy`, `scipy`, `matplotlib`, `plotly`, `ipywidgets`, `sympy`, `pandas`, `networkx`, `shapely`, `trimesh`, `pyvista`, `ripser`, `gudhi`, `persim`, and the rest of the root geometry stack. This course should not add dependencies.

## Worker Boundaries

Assign one worker to one canonical notebook, one helper module, or one script task. Chapter workers may edit only their chapter folder, matching artifact subtree, and explicitly assigned helper module. Index workers own `00-book-index.ipynb` and `00-index.ipynb` files. QC workers run audits and validation and report findings before small mechanical fixes.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Introduction-to-Topological-Manifolds/scripts/build_itm_course_indexes.py
uv run python -m compileall -q Introduction-to-Topological-Manifolds/utils Introduction-to-Topological-Manifolds/scripts
uv run python Introduction-to-Topological-Manifolds/scripts/audit_itm_notebooks.py --min-words 1200 --min-code-cells 5
uv run python Introduction-to-Topological-Manifolds/scripts/audit_itm_visuals.py
uv run python Introduction-to-Topological-Manifolds/scripts/validate_itm_course.py --limit 4 --timeout 300
uv run python Introduction-to-Topological-Manifolds/scripts/validate_itm_course.py --all --timeout 360
git diff --check -- Introduction-to-Topological-Manifolds
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Source Reading

Use `pdftotext` for source inspection:

```powershell
pdftotext -layout -f 19 -l 36 "Introduction-to-Topological-Manifolds/Introduction to Topological Manifolds.pdf" -
```

Do not write extracted source text into the course. Source spans are orientation only.

## Notebook-First Rule

A chapter notebook is a teaching document, not the output of a generic course generator. Scripts may support indexing, auditing, validation, artifact helpers, and reproducible checks, but they must not mass-populate chapter notebooks with generic teaching cells.
