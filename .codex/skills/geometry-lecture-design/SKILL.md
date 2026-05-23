---
name: geometry-lecture-design
description: Use this skill to generate well-branded lecture slides and educational visualizations for the Geometry Atlas project. Contains design guidelines, colors, type, fonts, mathematical component styles, slide templates, and a comprehensive library of SVG visualization assets spanning pure mathematics, applied mathematics, deep learning, and differential geometry.
user-invocable: true
---

Read `D:/Geometry/lecture-design-system/README.md`, then explore only the
specific files needed for the assigned deck. The shared design system lives in
`D:/Geometry/lecture-design-system`; this skill file is only the Codex entry
point.

This workspace is dedicated to chapter-specific lecture slide creation and
mathematical visualization for the Geometry Atlas. When creating course decks,
author the deck from the assigned notebook plus its source span. Do not use a
monolithic generator, do not mass-populate generic decks, and do not copy
textbook prose, screenshots, page crops, figures, or long exercise text.

If the user invokes this skill without other guidance, ask what lecture topic
or chapter they want slides for, then act as an expert academic slide designer
who outputs static HTML deck artifacts.

## Quick Reference

### Key Files
- `D:/Geometry/lecture-design-system/README.md` — Full design system documentation (colors, type, spacing, visual foundations, visualization catalog, slide design skills)
- `D:/Geometry/lecture-design-system/colors_and_type.css` — All CSS custom properties and semantic type/component classes
- `D:/Geometry/lecture-design-system/assets/icon.svg` — Geometry Atlas brand icon (teal tile with book/map motif)
- `D:/Geometry/lecture-design-system/slides/index.html` — 10 slide templates: title, section divider, definition, theorem+proof, worked example, comparison, key formula, warning, exercise, summary
- `D:/Geometry/lecture-design-system/slides/compact-templates.html` — Dense slide templates with KaTeX math rendering
- `D:/Geometry/lecture-design-system/slides/deck-stage.js` — Deck shell component (scaling, keyboard nav, print-to-PDF)

### Visualization Library (`D:/Geometry/lecture-design-system/preview/viz-*.html`)
Each file contains reusable SVG diagram patterns for embedding in slides. See the full catalog in README.md.

| File | Topics |
|---|---|
| `viz-deep-learning.html` | MLP, CNN, attention, transformers, backprop, loss landscapes, GNN, equivariance |
| `viz-diff-geometry.html` | Tangent spaces, parallel transport, Riemann curvature, Ricci curvature, geodesics, exponential map, fiber bundles, differential forms, Lie groups, Riemannian metrics |
| `viz-geometry-topology.html` | Torus, fundamental polygon, trefoil knot, Gaussian curvature, Möbius strip, stereographic projection |
| `viz-diff-eq.html` | Phase portraits (stable node, saddle), limit cycle, pitchfork bifurcation, vector fields, stable spiral |
| `viz-linalg.html` | Vector addition, linear transformations, eigenvectors, SVD, subspaces, orthogonal projection |
| `viz-optimization.html` | Gradient descent contours, convergence rates, convexity, Lagrange/KKT, linear programming, duality |
| `viz-statistics.html` | Chi-squared, Student-t, linear regression + CI, hypothesis testing, Bayesian update, Q-Q plot |
| `viz-random-matrix.html` | Wigner semicircle, Marchenko-Pastur, eigenvalue repulsion, Tracy-Widom, GOE/GUE/GSE, free probability |
| `viz-cv-photogrammetry.html` | Pinhole camera, epipolar geometry, bundle adjustment, homography, radial distortion, stereo rectification |
| `viz-robotics.html` | Kalman filter, covariance ellipses, factor graphs, coordinate frames (SE3), particle filter, pose graph SLAM |
| `viz-algebra.html` | Group tables, homomorphisms, ring/field structure, quotient groups |
| `viz-analysis.html` | Epsilon-delta, sequences, Riemann sums, contour integration |
| `viz-discrete.html` | Combinatorics, recurrence, generating functions, lattice paths |
| `viz-graphs-networks.html` | Graph types, adjacency, spanning trees, flow networks |
| `viz-info-theory.html` | Entropy, mutual information, channel capacity, Venn diagrams |
| `viz-logic-proof.html` | Truth tables, proof trees, induction schema, logical connectives |
| `viz-number-theory.html` | Prime sieves, modular arithmetic, quadratic residues, p-adic |
| `viz-sets-relations.html` | Venn diagrams, relations, equivalence classes, partial orders |

### Color Quick-Reference
```
Slide backgrounds:  #FFFFFF (white), #F8FAFC (off-white)
Primary text:       #111827 (ink), #475569 (muted), #64748B (dimmed)
Academic accents:   #1E3A8A (deep indigo), #2563EB (blue), #0F766E (teal), #B45309 (amber), #6D28D9 (violet)
```

### Math Box Types
- **Definition** — blue tint, `#2563EB` left rule
- **Theorem** — indigo tint, `#1E3A8A` left rule
- **Proof** — slate tint, `#94A3B8` left rule
- **Example** — teal tint, `#0F766E` left rule
- **Warning** — amber tint, `#B45309` left rule
- **Exercise** — violet tint, `#6D28D9` left rule
- **Remark** — muted tint, `#CBD5E1` left rule

### Font Stacks
```
Sans (headings/body):  'Source Sans 3', Arial, sans-serif
Math:                  'STIX Two Text', 'Cambria Math', Georgia, serif
Code:                  'JetBrains Mono', Consolas, monospace
```

### Slide Dimensions
1920 × 1080px, margins: 80px top / 96px sides / 64px bottom.
Min text size: 24px. Prefer centered or cleanly aligned formulas.

### Chapter Deck Contract
- Canonical HTML deck path: `<course>/artifacts/<chapter-or-unit>/slides/<chapter-id>-lecture.html`.
- Optional PDF/PPTX exports happen only after the chapter-authored HTML deck passes QC.
- Each deck includes metadata for `course`, `chapter_id`, `notebook_path`, `source_span`, `source_pdf`, and `design_system_version`.
- Each slide contains visible academic content plus substantive instructor dialogue in `<aside class="speaker-notes">...</aside>`; mirror to `#speaker-notes` JSON when a host needs `deck-stage.js` note synchronization.
- Slides should be slightly dense and instructor-ready: definitions, theorem statements, proof roadmaps, worked examples, diagrams, formulas, misconceptions, exercises, and recap material where appropriate.

### Icon System
Lucide icons via CDN. No emoji. No custom icon font.
```html
<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>
```

### Slide Design Skills

**Visualization techniques — when and how to use each:**

1. **SVG diagram embedding**: Copy SVG patterns from the `preview/viz-*.html` files. Scale them up for 1920×1080 slides (the preview cards are ~160×120 viewBox; scale to ~800×500 for half-slide or ~1600×900 for full-bleed). Adjust stroke-width proportionally.

2. **Diagram placement patterns**:
   - *Center-stage*: Single large diagram centered, formula below. Use for key concepts (curvature, attention mechanism).
   - *Side-by-side*: Two diagrams in a 2-column grid. Use for comparisons (convex vs non-convex, sharp vs flat minima).
   - *Diagram + math box*: Left column is diagram, right column is a definition/theorem box. Use for introducing formal concepts with visual intuition.
   - *Progressive build*: Same diagram repeated 3–4 times across slides, adding one layer per slide (base shape → vectors → labels → formula). Use for complex constructions.

3. **Color-coding in diagrams**: Use the semantic accent colors consistently across a lecture:
   - Primary object: `--slide-blue` (#2563EB)
   - Secondary/comparison: `--slide-teal` (#0F766E)
   - Highlight/alert: `--slide-amber` (#B45309)
   - Tertiary/exercise: `--slide-violet` (#6D28D9)
   - Structural/axes: `--slide-border` (#CBD5E1)

4. **Mathematical notation**: Use KaTeX for complex formulas, STIX Two Text for inline math. For simple expressions (single variable, Greek letter), inline SVG text with STIX Two Text is lighter-weight than KaTeX.

5. **Annotation patterns for diagrams**:
   - Point labels: 3px filled circle + 8px italic text offset 4px
   - Dimension/measurement: thin line with end-ticks + centered label
   - Flow/direction: dashed lines with arrowhead markers
   - Regions/areas: 5–8% opacity fill with matching stroke

6. **Background patterns** (subtle, 3–6% opacity):
   - Grid: for coordinate geometry, linear algebra
   - Concentric circles: for topology, curvature
   - Triangulation: for computational geometry, mesh topics
   - Parallel lines: for differential forms, foliations

7. **Animation notes**: For progressive disclosure, use `deck-stage.js` with multiple slides that build on each other. Do not animate within a single slide — use slide transitions instead.
