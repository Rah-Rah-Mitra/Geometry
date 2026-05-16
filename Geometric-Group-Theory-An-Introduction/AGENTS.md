# Agent Instructions: Geometric Group Theory Notebook Course

This folder is a standalone visualization-first notebook edition of Clara
Loeh's *Geometric Group Theory: An Introduction*. The local PDF is used only
for orientation, source spans, terminology, and concept coverage.

Treat this folder as the project root for this course. The workspace root owns
the shared `uv` environment, `pyproject.toml`, `uv.lock`, and `.venv`.

## Repo-Local Skills

Use the repo-local skills under `D:\Geometry\.codex\skills`:

- `geometry-visualization-planner` before planning a chapter storyboard.
- `geometry-chapter-notebook-author` when authoring canonical notebooks.
- `geometry-notebook-qc` when reviewing notebooks, artifacts, helpers, and
  validation output.

## Non-Negotiables

- Write original teaching prose, examples, code, diagrams, and checks.
- Do not copy textbook passages, long exercise text, screenshots, page crops,
  or textbook figures.
- A reader must be able to learn from each notebook without opening the PDF.
- Visualization is part of the explanation. Use Cayley graph diagrams,
  quasi-isometry experiments, hyperbolic graph diagnostics, growth plots,
  boundary-at-infinity pictures, and invariant checks wherever they clarify
  the chapter.
- Keep helpers in `utils/`, generated outputs in `artifacts/`, and validation
  tools in `scripts/`.
- Every canonical notebook must execute with `nbclient`.
- Generated paths in notebooks must be relative or book-local.
- Preserve one canonical teaching notebook per chapter or appendix folder plus
  a local `00-index.ipynb`.

## Source Map

The PDF has 390 physical pages. The body printed pagination begins with
Chapter 1 on physical PDF page 12, so body and back-matter printed pages map
by `pdf_page = printed_page + 11`. Front matter uses physical PDF pages 1-11.

| Unit | Folder | Printed Pages | PDF Pages | Focus |
| --- | --- | ---: | ---: | --- |
| Front matter | `00-book-index.ipynb` | i-xi | 1-11 | About this book, contents, course route |
| Chapter 01 | `part-00-orientation/chapter-01-introduction` | 1-6 | 12-17 | geometric group theory workflow and basic Cayley graph examples |
| Chapter 02 | `part-01-groups/chapter-02-generating-groups` | 9-50 | 20-61 | groups, generators, relations, free products, extensions |
| Chapter 03 | `part-02-groups-to-geometry/chapter-03-cayley-graphs` | 53-74 | 64-85 | graph notation, Cayley graphs, free groups and trees |
| Chapter 04 | `part-02-groups-to-geometry/chapter-04-group-actions` | 75-114 | 86-125 | group actions, tree actions, ping-pong, matrix-group examples |
| Chapter 05 | `part-02-groups-to-geometry/chapter-05-quasi-isometry` | 115-164 | 126-175 | quasi-isometry, word metrics, Svarc-Milnor, invariants |
| Chapter 06 | `part-03-geometry-of-groups/chapter-06-growth-types-of-groups` | 167-202 | 178-213 | growth functions, polynomial/exponential growth, quasi-isometry invariance |
| Chapter 07 | `part-03-geometry-of-groups/chapter-07-hyperbolic-groups` | 203-256 | 214-267 | hyperbolic spaces, hyperbolic groups, word problem, infinite-order elements |
| Chapter 08 | `part-03-geometry-of-groups/chapter-08-ends-and-boundaries` | 257-288 | 268-299 | ends, Gromov boundary, geometry at infinity, rigidity applications |
| Chapter 09 | `part-03-geometry-of-groups/chapter-09-amenable-groups` | 289-316 | 300-327 | means, Følner sequences, paradoxical decompositions, quasi-isometry invariance |
| Appendix A | `part-04-reference-material/appendix-a-reference-material` | 319-352 | 330-363 | fundamental groups, group cohomology, hyperbolic plane, programming tasks |

Part openers are inventoried in `scripts/ggt_inventory.py`. Bibliography,
notation index, and subject index are inventoried but not converted into copied
notes or exercise text.

## Notebook Shape

Each canonical notebook should contain:

1. Title and source span.
2. Standalone chapter question and motivation.
3. Translation guide from book concepts into computational language.
4. Setup cell that discovers `BOOK_ROOT`.
5. Original concept sections with equations and diagrams.
6. Executable examples using book-local utilities.
7. Generated visual artifacts displayed inline.
8. Applied lab or exploration prompt.
9. Sanity checks asserting identities, artifact existence, nonblank visuals,
   and chapter-specific invariants.
10. Takeaways.

The setup cell should search upward for a folder containing both
`00-book-index.ipynb` and `utils`, then insert that folder into `sys.path`.

## Artifact Contract

Store generated outputs under:

```text
artifacts/chapter-XX/figures/
artifacts/chapter-XX/html/
artifacts/chapter-XX/checks/
artifacts/chapter-XX/tables/
artifacts/chapter-XX/data/
artifacts/appendix-a/figures/
artifacts/appendix-a/html/
artifacts/appendix-a/checks/
```

Artifact filenames should name the concept, not the rendering technology.
Repeated placeholder visuals are a QC failure. Every generated artifact should
be displayed inline or linked from the notebook, and final checks should assert
that files exist, are nonempty, and nonblank when they are images.

## Geometry Stack

Use the shared `uv` environment at the workspace root. Prefer installed
libraries before adding dependencies: `numpy`, `matplotlib`, `networkx`,
`plotly`, `sympy`, `pandas`, and the rest of the root geometry stack. This
course should not require root dependency changes.

## Worker Boundaries

Other workers may edit other course folders. Keep changes inside
`Geometric-Group-Theory-An-Introduction` unless explicitly assigned otherwise.
Never revert unrelated changes.

## Commands

Run from `D:\Geometry`:

```powershell
uv run python Geometric-Group-Theory-An-Introduction/scripts/generate_ggt_artifacts.py
uv run python -m compileall -q Geometric-Group-Theory-An-Introduction/utils Geometric-Group-Theory-An-Introduction/scripts
uv run python Geometric-Group-Theory-An-Introduction/scripts/build_ggt_course_indexes.py
uv run python Geometric-Group-Theory-An-Introduction/scripts/audit_ggt_notebooks.py --min-words 650 --min-code-cells 5
uv run python Geometric-Group-Theory-An-Introduction/scripts/audit_ggt_visuals.py
uv run python Geometric-Group-Theory-An-Introduction/scripts/validate_ggt_course.py --limit 3 --timeout 240
uv run python Geometric-Group-Theory-An-Introduction/scripts/validate_ggt_course.py --all --timeout 240
git diff --check -- Geometric-Group-Theory-An-Introduction
```

Run `uv sync` only if `pyproject.toml` or `uv.lock` changes.

## Visualization Library Policy

Use the installed geometry stack intentionally.

- Use Matplotlib for durable 2D Cayley graph diagrams, proof sketches,
  incidence labels, growth plots, and Følner boundary diagrams.
- Use NetworkX for Cayley graph balls, tree/action graphs, dependency graphs,
  coarse metric computations, ends, and sampled hyperbolicity checks.
- Use Plotly for standalone HTML graph and parameter explorations.
- Use SymPy or exact integer checks where a group law, relation, or coarse
  inequality can be verified symbolically.
- Use richer 3D or hyperbolic-geometry packages only when they clarify the
  assigned notebook and remain reproducible in the shared environment.

Every major visualization must have:

1. the concept it teaches,
2. the reason this representation was chosen,
3. an inspection target for the learner,
4. a nearby prose explanation,
5. a check, invariant, or sanity test where practical.

Decorative visuals are not acceptable.

