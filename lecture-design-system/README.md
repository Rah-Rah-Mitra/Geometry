# Geometry Lecture Design System

A professional academic design system for undergraduate and graduate Geometry lecture slides. Designed for formula-heavy mathematical presentations with clean white backgrounds, subtle geometric patterns, strong typographic hierarchy, reusable slide layouts, and a comprehensive library of SVG visualization assets.

---

## Sources

This design system was built from:

- **[Rah-Rah-Mitra/Geometry](https://github.com/Rah-Rah-Mitra/Geometry)** — The primary course atlas: 45+ visualization-first notebook courses covering Euclidean geometry, differential geometry, algebraic topology, projective geometry, computational geometry, and more.

Explore the repository for deeper context on the course structure and visualization libraries.

---

## Product Context

The **Geometry Atlas** is an educational platform for self-directed learning in geometry and related mathematical fields. It spans five tracks of courses from undergraduate foundations (Euclidean constructions, coordinate geometry) through advanced graduate material (Riemannian geometry, algebraic topology, geometric deep learning).

This design system's primary output: professional 16:9 slides for university-level teaching, supported by a rich library of reusable SVG visualization patterns.

---

## CONTENT FUNDAMENTALS

### Tone & Voice
- **Rigorous but approachable**: Content is written for mathematically serious audiences but avoids unnecessary formalism. Prose explains *why* before *how*.
- **Third-person academic**: "We define…", "Consider the mapping…", "This gives us…" — standard mathematical lecture voice.
- **No filler**: Every sentence and visual must teach something. Decorative elements are not acceptable. Visualizations require justification (concept taught, reason for representation, inspection target).
- **No emoji**: All iconography comes from Lucide icons.
- **Title case for headings**: "Straightedge and Compass", "Euclid's Approach to Geometry".
- **Mathematical conventions**: Standard LaTeX-style notation. Variables in italics. Theorems, definitions, and lemmas are labeled and numbered.

---

## VISUAL FOUNDATIONS

### Color System

**Lecture slide palette**:
| Token | Value | Usage |
|---|---|---|
| `--slide-bg` | `#FFFFFF` | Slide background |
| `--slide-bg-alt` | `#F8FAFC` | Soft off-white for section starters |
| `--slide-ink` | `#111827` | Main text |
| `--slide-muted` | `#475569` | Secondary text |
| `--slide-dimmed` | `#64748B` | Captions, annotations |
| `--slide-accent` | `#1E3A8A` | Deep indigo — primary academic accent |
| `--slide-blue` | `#2563EB` | Lecture blue — definitions, links |
| `--slide-teal` | `#0F766E` | Examples, applied math |
| `--slide-amber` | `#B45309` | Warnings, common mistakes |
| `--slide-violet` | `#6D28D9` | Exercises, problem sets |
| `--slide-border` | `#CBD5E1` | Slate border for proof boxes |

### Semantic Color Mapping
- **Definitions** → blue/indigo left rule + light blue tint
- **Theorems / Propositions / Lemmas** → deep indigo left rule, bold label
- **Proofs** → neutral slate border, numbered steps
- **Examples** → teal accent, may include diagrams
- **Warnings / Common Mistakes** → amber accent
- **Exercises** → violet or slate accent
- **Remarks** → muted border, understated

### Diagram Color Convention
When building SVG visualizations for slides, apply colors consistently:
| Role | Color | Token |
|---|---|---|
| Primary object / structure | `#2563EB` | `--slide-blue` |
| Secondary / comparison | `#0F766E` | `--slide-teal` |
| Highlight / alert / annotation | `#B45309` | `--slide-amber` |
| Tertiary / exercise element | `#6D28D9` | `--slide-violet` |
| Deep emphasis / headings | `#1E3A8A` | `--slide-accent` |
| Structural axes / grids | `#CBD5E1` / `#E2E8F0` | `--slide-border` |
| Light fills / regions | 5–12% opacity of accent color | — |
| Dashed / auxiliary lines | `#94A3B8` | — |

### Typography

**Lecture slide fonts**:
- Headings & body: **Source Sans 3** (clean, modern, highly readable at projection sizes)
- Mathematics: **STIX Two Math** (professional mathematical typesetting, OpenType MATH table)
- Code snippets: **JetBrains Mono** (clear at small sizes, ligatures for code)

Google Fonts CDN links:
- Source Sans 3: `https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,300;0,400;0,600;0,700;1,400;1,600&display=swap`
- STIX Two Math/Text: `https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400;0,600;0,700;1,400&display=swap`
- JetBrains Mono: `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap`

### Type Scale (Slides, 1920×1080)
| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Slide title | Source Sans 3 | 48–56px | 700 | `--slide-ink` |
| Section header | Source Sans 3 | 40–48px | 700 | `--slide-accent` |
| Subtitle | Source Sans 3 | 28–32px | 400 | `--slide-muted` |
| Body text | Source Sans 3 | 26–30px | 400 | `--slide-ink` |
| Math display | STIX Two Text | 32–40px | 400 | `--slide-ink` |
| Math inline | STIX Two Text | 26–30px | 400 | `--slide-ink` |
| Labels/captions | Source Sans 3 | 20–24px | 600 | `--slide-dimmed` |
| Code | JetBrains Mono | 22–26px | 400 | `--slide-ink` |

### Spacing & Layout

**Slide dimensions**: 1920 × 1080px (16:9)

**Margins**:
- Top: 80px (title area)
- Left/Right: 96–120px
- Bottom: 64px

**Spacing tokens**:
| Token | Value | Usage |
|---|---|---|
| `--space-xs` | `8px` | Tight padding |
| `--space-sm` | `16px` | Inline spacing |
| `--space-md` | `24px` | Component gaps |
| `--space-lg` | `40px` | Section spacing |
| `--space-xl` | `64px` | Major divisions |

**Corner radii**: Cards/boxes `8px`, tags/badges `6px`.

**Shadows**: Minimal — `shadow-sm` only (`0 1px 2px 0 rgb(0 0 0 / 0.05)`). Flat-forward aesthetic.

**Borders**: Default `1px solid #CBD5E1`. Left rules on math boxes: `3–4px solid` accent color.

### Background Patterns
Slides use very subtle geometric motifs at 3–6% opacity:
- Thin compass arcs
- Faint Euclidean grids
- Low-opacity triangles and circles
- Coordinate axes
- Tessellation fragments
- Manifold-like curves

These are rendered as SVG patterns or pseudo-elements. They must NEVER interfere with formulas or content.

Choose patterns that match the lecture topic:
| Topic area | Recommended pattern |
|---|---|
| Linear algebra, coordinates | Grid lines |
| Topology, curvature | Concentric circles, arcs |
| Computational geometry | Triangulation mesh |
| Differential forms, foliations | Parallel curves |
| Deep learning, networks | Dot grids, node patterns |
| Number theory | Lattice dots |

---

## ICONOGRAPHY

### Icon System
**Lucide** icons exclusively — no emoji, no Unicode symbols, no PNG icons.

Lucide CDN:
```html
<script src="https://unpkg.com/lucide@0.460.0/dist/umd/lucide.min.js"></script>
```

### Icon Style Rules
- Stroke width: `2` (default) or `2.1–2.2` for emphasis
- Size: `16–19px` for slide context
- Color: inherits from text color (typically `--slide-muted` or `--slide-accent`)
- No filled icons except `Star` when bookmarked

### Brand Mark
The Geometry Atlas logo is an SVG icon: a teal (`#087568`) rounded rectangle with a white book/map motif. See `assets/icon.svg`. Appears on title slides at 48×48px.

### Slide Iconography
For lecture slides, use minimal iconography:
- Geometric constructions (compass, straightedge) as thin-stroke SVG
- Mathematical symbols rendered via STIX Two Math font
- Diagram labels with consistent point markers (small filled circles, 4–6px)
- Avoid decorative icons; every visual element must serve a mathematical purpose

---

## MATH RENDERING

### KaTeX (recommended for complex formulas)
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
```
Auto-render with `renderMathInElement(document.body)` after DOM load. Delimiters: `$$…$$` for display, `\(…\)` for inline.

### STIX Two Text (for lightweight inline math)
For single variables, Greek letters, or simple expressions, use `<span>` with `font-family: var(--font-math); font-style: italic;` instead of loading KaTeX. This keeps slides lighter.

### Math Box Components
Seven semantic types, each with a left-rule accent and tinted background. See `colors_and_type.css` for full CSS classes (`.math-box`, `.math-box--definition`, etc.).

| Type | Background | Left Rule | Label Color |
|---|---|---|---|
| Definition | `#EFF6FF` | `#2563EB` | blue |
| Theorem | `#EEF2FF` | `#1E3A8A` | indigo |
| Proof | `#F8FAFC` | `#94A3B8` | slate |
| Example | `#F0FDFA` | `#0F766E` | teal |
| Warning | `#FFFBEB` | `#B45309` | amber |
| Exercise | `#F5F3FF` | `#6D28D9` | violet |
| Remark | `#F8FAFC` | `#CBD5E1` | muted |

---

## VISUALIZATION CATALOG

The `preview/` directory contains reusable SVG diagram patterns organized by mathematical topic. Each file provides 6–8 diagrams at a compact `~160×120` viewBox, ready to be scaled up for slides.

### How to Use Visualization Assets

1. **Browse**: Open a `preview/viz-*.html` file to see available diagram patterns for that topic.
2. **Copy**: Lift the `<svg>` element you need and paste it into your slide markup.
3. **Scale**: The preview viewBox is small (~160×120). For slides, scale to:
   - Half-slide (beside text): set `width="800"` or wrap in a container ~800px wide
   - Full-width diagram: set `width="1600"` or use `width="100%"` with a max-width
   - Center-stage: `width="1000"` centered with formulas below
4. **Adjust strokes**: When scaling up 5–10×, thicken strokes proportionally (preview uses 0.5–2px; slides want 2–6px).
5. **Swap labels**: Replace compact preview labels with full-size slide text (preview uses 7–8px fonts; slides want 24–32px).

### Catalog by Topic

#### Pure Mathematics
| File | Diagrams included |
|---|---|
| `viz-algebra.html` | Group multiplication tables, homomorphism diagrams, ring/field structure, quotient groups, isomorphism arrows |
| `viz-analysis.html` | Epsilon-delta neighborhoods, sequence convergence, Riemann sums, contour integration paths, uniform vs pointwise |
| `viz-geometry-topology.html` | Torus with tangent plane, fundamental polygon, trefoil knot, Gaussian curvature signs, Möbius strip, stereographic projection |
| `viz-number-theory.html` | Prime sieve grids, modular arithmetic wheels, quadratic residues, p-adic valuations, Farey sequences |
| `viz-sets-relations.html` | Venn diagrams (2-set, 3-set), Hasse diagrams, equivalence classes, partial order lattices |
| `viz-logic-proof.html` | Truth tables, natural deduction trees, induction schema, logical connective gates, sequent calculus |

#### Applied Mathematics & Computation
| File | Diagrams included |
|---|---|
| `viz-linalg.html` | Vector addition parallelogram, linear transformation (shear), eigenvectors/eigenvalues, SVD block diagram, subspace plane in R³, orthogonal projection |
| `viz-diff-eq.html` | Stable node (sink), saddle point, limit cycle (Poincaré-Bendixson), pitchfork bifurcation, vector field, stable spiral (focus) |
| `viz-optimization.html` | Gradient descent on contours, convergence rate comparison, convex vs non-convex sets, Lagrange/KKT conditions, LP feasible polytope, duality gap |
| `viz-statistics.html` | Chi-squared distribution, Student-t vs Normal, linear regression + CI band, two-tailed hypothesis test, Bayesian update, Q-Q plot |
| `viz-graphs-networks.html` | Graph types (directed/undirected), adjacency matrix, spanning trees, max-flow networks |
| `viz-discrete.html` | Binomial lattice paths, recurrence trees, generating function coefficients, inclusion-exclusion, Catalan structures |
| `viz-info-theory.html` | Entropy curve, mutual information Venn, channel capacity diagram, rate-distortion, source coding |

#### Differential Geometry & Topology
| File | Diagrams included |
|---|---|
| `viz-diff-geometry.html` | **Tangent space** T_pM with basis vectors and normal · **Parallel transport** along a curve with Levi-Civita connection · **Riemann curvature tensor** via holonomy around a loop · **Ricci curvature** volume comparison (sphere/flat/hyperbolic) · **Geodesics on S²** as great circles · **Exponential map** from tangent space to manifold · **Fiber bundle** with section and projection · **Differential forms** (1-form level sets, 2-form area element, Stokes' theorem) · **Lie group & Lie algebra** relationship with exponential map · **Riemannian metric tensor** isotropic vs anisotropic |
| `viz-geometry-topology.html` | Torus, fundamental polygon, trefoil knot, Gaussian curvature, Möbius strip, stereographic projection |

#### Deep Learning & Geometric ML
| File | Diagrams included |
|---|---|
| `viz-deep-learning.html` | **Feedforward MLP** (3-layer fully connected) · **Convolution + ReLU** (input/kernel/output feature maps) · **Scaled dot-product attention** (Q/K/V projections, attention matrix, softmax) · **Transformer encoder block** (multi-head attention, FFN, residual + LayerNorm, ×N) · **Backpropagation graph** (computational graph with forward/backward passes, chain rule) · **Loss landscape geometry** (sharp vs flat minima, generalization) · **GNN message passing** (neighbor aggregation, update function) · **Equivariance diagram** (commutative diagram f∘g = g∘f) |

#### Computer Vision & Robotics
| File | Diagrams included |
|---|---|
| `viz-cv-photogrammetry.html` | Pinhole camera model, epipolar geometry + fundamental matrix, bundle adjustment, homography mapping, radial distortion, stereo rectification + disparity |
| `viz-robotics.html` | Kalman filter predict-update cycle, covariance ellipses, factor graph (SLAM), coordinate frames SE(3), particle filter, pose graph optimization |

#### Spectral Theory
| File | Diagrams included |
|---|---|
| `viz-random-matrix.html` | Wigner semicircle law, Marchenko-Pastur distribution, eigenvalue repulsion (GOE vs Poisson), Tracy-Widom distribution, classical ensembles (GOE/GUE/GSE), free probability addition |

---

## SLIDE DESIGN SKILLS

### Slide Layout Patterns

**1. Title Slide**
- Centered title (52–56px, 700 weight), subtitle below (30px, 400 weight, muted)
- 4px accent rule between title and subtitle
- Optional: brand icon top-left, date/lecture number bottom-right
- Background: white with subtle grid pattern at 3% opacity

**2. Section Divider**
- Large section number or label (44px, 700, accent color)
- Section title centered or left-aligned
- Background: `--slide-bg-alt` (#F8FAFC) or white
- Optional: full-width thin rule below title

**3. Definition / Theorem / Proof**
- Use the math-box component with appropriate semantic type
- Title line: "**DEFINITION 3.1** — Riemannian Metric" (label in accent color, title in ink)
- Body: mathematical content in STIX Two Text or KaTeX
- Keep one concept per slide

**4. Diagram + Explanation (Split Layout)**
- Left 55%: SVG diagram from visualization library
- Right 45%: explanatory text, formula, or math box
- Or: diagram centered top 60%, text/formula bottom 40%

**5. Comparison (Two-Column)**
- Two equal columns with related diagrams or concepts
- Shared title across top, column labels below
- Use contrasting accent colors (blue vs teal, or blue vs amber)

**6. Worked Example**
- Teal accent math box
- Step-by-step numbered list with math
- Optional: diagram that builds across steps

**7. Key Formula (Showcase)**
- Single important formula, large and centered (40px KaTeX display)
- Brief name/attribution above in small caps
- Minimal surrounding content — let the formula breathe

**8. Warning / Common Mistake**
- Amber accent math box
- Often paired with a "correct" version in blue for contrast

**9. Exercise**
- Violet accent math box
- Problem statement, optional hint in dimmed text

**10. Summary / Recap**
- Bulleted list of key takeaways
- Optional: mini versions of key diagrams inline

### Visualization Composition Techniques

**Center-stage diagram**: Place one large diagram (800–1200px wide) centered on the slide with the formula or definition below. Best for introducing a key concept — curvature, attention mechanism, a specific theorem's geometric intuition.

**Side-by-side comparison**: Two diagrams at ~700px each in a flex row. Use for contrasts: convex vs non-convex, sharp vs flat minima, GOE vs Poisson spacing, positive vs negative curvature.

**Diagram + math-box**: Left column holds a 700px diagram, right column holds a definition or theorem box. The diagram provides geometric intuition; the box provides the formal statement.

**Progressive build**: Create 3–5 consecutive slides that build one diagram layer by layer. Slide 1: base structure (axes, surface). Slide 2: add the primary object (vector, point, curve). Slide 3: add annotations (labels, measurements). Slide 4: add the conclusion (formula, result). Each slide is a complete `<section>` in the deck.

**Annotated formula**: Place a key formula (KaTeX, centered) with SVG annotation arrows pointing to each term, labeling its geometric meaning. Use dashed lines from formula terms to diagram elements.

**Grid of mini-diagrams**: For survey or taxonomy slides, arrange 4–6 small diagrams (300×200 each) in a 2×3 or 3×2 grid. Each has a short label. Use for "types of curvature", "activation functions", "matrix ensembles", etc.

### Diagram Scaling Reference

| Context | Suggested width | Stroke scale | Font scale |
|---|---|---|---|
| Preview card (as-is) | 130–150px | 1× | 7–8px |
| Slide: small inline | 300–400px | 2× | 16–18px |
| Slide: half-width | 700–800px | 3–4× | 24–28px |
| Slide: full-width | 1400–1700px | 5–8× | 28–36px |

### Creating New Diagram Patterns

When the existing library doesn't cover a topic, create new SVG diagrams following these conventions:

1. **ViewBox**: Use `0 0 160 120` for standard aspect or `0 0 170 120` for wide diagrams
2. **Stroke widths**: 0.4–0.6px for auxiliary lines, 0.8–1.2px for primary elements, 1.5–2px for emphasis
3. **Arrow markers**: Define `<marker>` elements with 4–6px markerWidth, use `marker-end` on directional lines
4. **Point markers**: Filled circles, 2–3.5px radius, in accent colors
5. **Text labels**: Source Sans 3 at 7–8px for labels, STIX Two Text italic for variables
6. **Fills**: Use 4–12% opacity of the corresponding accent color for region fills
7. **Dashed lines**: `stroke-dasharray="3 2"` for hidden/auxiliary, `"2 1.5"` for projected/implied
8. **Cell container**: Wrap in `.cell` class (`#F8FAFC` bg, `1px solid #E2E8F0`, `6px` radius, `8px` padding)

---

## CHAPTER DECK CONVENTIONS

For Geometry Atlas course work, the canonical editable deck is HTML:

```text
<course>/artifacts/<chapter-or-unit>/slides/<chapter-id>-lecture.html
```

Optional PDF or PPTX exports should be created only after the chapter-authored
HTML deck passes quality control. Exported files are derivatives, not the source
of record.

Each chapter deck should include metadata for:

- `course`
- `chapter_id`
- `notebook_path`
- `source_span`
- `source_pdf`
- `design_system_version`

Each slide should contain visible, slightly dense academic material plus full
instructor speaker dialogue in an `<aside class="speaker-notes">...</aside>`.
Mirror notes into the `#speaker-notes` JSON block when the host environment
needs `deck-stage.js` note synchronization.

Decks must be authored from the assigned notebook and textbook source span.
Do not mass-generate chapter decks, do not use a monolithic deck generator, and
do not copy textbook prose, screenshots, page crops, figures, or long exercise
text. Scripts may support validation, indexing, export, and mechanical checks;
they must not substitute for chapter-specific academic authoring.

---

## FILES INDEX

```
├── README.md                    ← You are here
├── colors_and_type.css          ← CSS custom properties: colors, type, spacing
├── assets/
│   ├── icon.svg                 ← Geometry Atlas brand icon
│   └── globals-reference.css    ← Original Geometry-Web globals.css (reference only)
├── preview/                     ← Design system preview cards
│   ├── color-*.html             ← Color palette cards
│   ├── type-*.html              ← Typography cards
│   ├── spacing-*.html           ← Spacing & radii cards
│   ├── comp-*.html              ← Component cards (buttons, math boxes, cards, badges)
│   ├── brand-*.html             ← Brand mark & pattern cards
│   └── viz-*.html               ← Visualization diagram libraries (18 topic files)
│       ├── viz-algebra.html
│       ├── viz-analysis.html
│       ├── viz-cv-photogrammetry.html
│       ├── viz-deep-learning.html        ← NEW: MLP, CNN, attention, transformers, GNN
│       ├── viz-diff-eq.html
│       ├── viz-diff-geometry.html        ← NEW: tangent spaces, curvature, geodesics, Lie groups
│       ├── viz-discrete.html
│       ├── viz-geometry-topology.html
│       ├── viz-graphs-networks.html
│       ├── viz-info-theory.html
│       ├── viz-linalg.html
│       ├── viz-logic-proof.html
│       ├── viz-number-theory.html
│       ├── viz-optimization.html
│       ├── viz-random-matrix.html
│       ├── viz-robotics.html
│       ├── viz-sets-relations.html
│       └── viz-statistics.html
└── slides/
    ├── index.html               ← 10 slide templates (title, section, definition, theorem, etc.)
    ├── compact-templates.html   ← Dense slide templates with KaTeX
    └── deck-stage.js            ← Deck shell component (scaling, nav, print)
```

Agent-facing skill metadata lives at
`D:/Geometry/.codex/skills/geometry-lecture-design/SKILL.md`.
