"""Author the canonical geometric group theory teaching notebooks."""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

SCRIPT_ROOT = Path(__file__).resolve().parent
BOOK_ROOT = SCRIPT_ROOT.parents[0]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from ggt_inventory import ENTRIES  # noqa: E402


DETAILS = {
    "chapter-01": {
        "builder": "build_intro_cayley_gallery",
        "figure_files": ["basic-cayley-graph-gallery.png", "group-to-geometry-pipeline.png"],
        "html_file": "free-group-cayley-ball.html",
        "checks_file": "intro-cayley-gallery-checks.json",
        "question": "How can an abstract multiplication table become a geometric object whose large-scale shape says something group-theoretic?",
        "motivation": """
        The opening chapter sets the working rhythm for the whole course. A group is not drawn directly; instead we choose generators, turn multiplication by those generators into edges, and then study the resulting metric graph at a scale where finite presentation choices blur away. This notebook makes that rhythm visible with three test spaces: an infinite cyclic group that looks like a line, a rank-two Abelian group that looks planar, and a free group whose reduced words branch like a tree.

        The point is not that every group comes with one perfect picture. The point is that geometric group theory repeatedly asks for a useful model, a coarse invariant, and a translation back to algebra. A Cayley graph is the first such model. Growth, hyperbolicity, ends, and amenability will later become more refined probes of the same basic move.
        """,
        "translation": """
        - A group element becomes a vertex.
        - Multiplication by a chosen generator becomes an edge.
        - Word length becomes graph distance from the identity.
        - Changing finite generators changes local details, not the intended large-scale questions.
        - A theorem about the group often appears first as a robust geometric pattern.
        """,
        "routing": "NetworkX builds the Cayley graph balls and verifies the tree property; Matplotlib gives durable side-by-side diagrams; Plotly saves an inspectable HTML view for reduced words; the four-point delta check records a first hyperbolic-graph diagnostic.",
        "storyboard": """
        The first visual is a gallery, not decoration: it asks you to compare the coarse signatures of the line, the grid, and the free tree. The second visual is a route map for the course: group data creates a Cayley graph, the graph creates a word metric, the metric exposes a coarse invariant, and the invariant returns as algebraic information.
        """,
        "inspection": """
        In the gallery, ignore the boundary cut off by the finite window and look at the pattern near the identity. The line has two directions, the grid has planar spreading, and the free group keeps splitting into new branches. In the pipeline diagram, read every arrow as a design decision: no invariant appears until the algebra has been converted into a geometric object.
        """,
        "lab": """
        Applied lab: replace the free group in your head with a group that has one new relation. Predict what relation should do to the tree before computing anything. A relation identifies words that were previously different, so the tree should acquire cycles or folded branches. Later notebooks make this prediction concrete for finite presentations, quasi-isometry, and hyperbolicity.
        """,
        "takeaways": [
            "Cayley graphs are the first bridge from algebra to metric geometry.",
            "Large-scale questions deliberately ignore finite local noise.",
            "The free group is tree-like, which is why it will keep reappearing as the clean negative-curvature model.",
        ],
        "assertion": 'assert checks["free_group_ball_is_tree"] and checks["free_group_four_point_delta"] == 0.0',
    },
    "chapter-02": {
        "builder": "build_generating_groups_visuals",
        "figure_files": ["generators-relations-and-dihedral-cayley.png", "dihedral-degree-regularity.png"],
        "html_file": "dihedral-cayley-graph.html",
        "checks_file": "presentation-relation-checks.json",
        "question": "What algebraic data is needed before geometry can be attached to a group?",
        "motivation": """
        This chapter supplies the algebraic raw material: subgroups, quotients, kernels, generators, relations, free groups, products, and extensions. For a visualization-first course, the central computational idea is that a presentation is a machine for producing identifications. Before relations are imposed, reduced words in a free group form a tree. After relations are imposed, formerly distinct words can land on the same vertex, and the Cayley graph records the quotient geometry.

        The notebook uses the dihedral group as a finite laboratory because every relation can be checked exactly. Rotation and reflection generate a concrete symmetry group; the relators force a finite Cayley graph; the resulting graph is regular because every group element has the same generator moves available.
        """,
        "translation": """
        - A generating set is an alphabet for writing group elements.
        - A free group is the space of reduced words before extra equations are imposed.
        - A normal closure of relators is the bookkeeping device that says which words become invisible in the quotient.
        - A presentation is useful geometrically because it predicts cycles in a Cayley graph.
        - Product and extension constructions can be read as ways of assembling new metric graph models from old ones.
        """,
        "routing": "NetworkX renders the finite Cayley graph and relation pipeline; exact integer arithmetic checks the dihedral relations; Matplotlib records regularity and presentation structure; Plotly provides an interactive finite Cayley graph where vertices are group elements.",
        "storyboard": """
        The overview visual puts two views side by side: the concrete Cayley graph of a dihedral group and the abstract pipeline from alphabet to quotient. The diagnostic visual checks that the Cayley graph is regular, reinforcing that generator moves are attached uniformly to every group element rather than to a preferred basepoint.
        """,
        "inspection": """
        In the Cayley graph, separate rotation vertices from reflection vertices and notice how the reflection generator jumps between the two rings. The relation check is the computational version of a presentation: powers and alternating products are evaluated in the group law, and the output must return to the identity exactly.
        """,
        "lab": """
        Applied lab: change the rotation order from 8 to another integer n in the helper call. Predict the order of the group and the two-ring geometry before looking at the image. This is a low-risk way to see how presentations control finite models and why changing a relator changes global graph size.
        """,
        "takeaways": [
            "Generators create words; relations create identifications.",
            "Finite presentations are geometric instructions for Cayley graph cycles.",
            "Exact relation checks keep the computational model honest.",
        ],
        "assertion": 'assert checks["r_to_8_identity"] and checks["s_to_2_identity"] and checks["sr_to_2_identity"]',
    },
    "chapter-03": {
        "builder": "build_cayley_graph_visuals",
        "figure_files": ["cayley-grid-versus-free-tree.png", "word-length-sphere-counts.png"],
        "html_file": "reduced-word-tree.html",
        "checks_file": "cayley-graph-metric-checks.json",
        "question": "What does a Cayley graph remember about a group, and what does it intentionally forget?",
        "motivation": """
        Cayley graphs are the first official geometric objects of the book. Once a finite generating set is chosen, every group element becomes a vertex and every generator step becomes a labelled edge. The graph remembers word length, adjacency, cycles forced by relations, and large-scale features such as branching or planar spread. It forgets the literal syntax of a word whenever two words represent the same group element.

        The free group is the cleanest contrast case. Reduced words have unique normal form, so the Cayley graph has no cycles and is a tree. Abelian groups such as Z^2 have commuting generator moves, so square cycles appear immediately. Those square cycles are not an error; they are the visible trace of the relation that horizontal then vertical equals vertical then horizontal.
        """,
        "translation": """
        - Vertices are group elements, usually explored from the identity.
        - Edge labels are generator names; graph distance is word length.
        - Free reduction prevents immediate backtracking in free groups.
        - Relations create cycles, and the absence of cycles in the free case is a structural theorem.
        - Sphere counts around the identity provide the first growth data.
        """,
        "routing": "NetworkX constructs finite Cayley graph balls and computes BFS word spheres; Matplotlib compares grid and free-tree geometries; Plotly makes the reduced-word tree inspectable; the validation checks tree-ness, root degree, sphere counts, and four-point delta.",
        "storyboard": """
        The first visual compares Z^2 and F(a,b) at the same conceptual scale. The second visual turns graph distance into a sequence of sphere sizes, making the word metric visible before growth type is formally studied in Chapter 6.
        """,
        "inspection": """
        In the grid, locate a square and read it as a commuting relation. In the tree, follow a path away from the identity and notice that every non-root vertex has exactly one route back toward shorter words. The sphere-count plot then translates this local branching rule into numerical growth.
        """,
        "lab": """
        Applied lab: add a third free generator mentally. The root degree should become six, and each non-root outward step should have five choices after excluding immediate cancellation. This predicts much faster sphere growth and gives a quick sanity check for any generated free-group Cayley ball.
        """,
        "takeaways": [
            "Word length is graph distance from the identity.",
            "Relations are visible as cycles in Cayley graphs.",
            "Free groups give tree models because reduced words have unique geodesics to the identity.",
        ],
        "assertion": 'assert checks["free_group_ball_is_tree"] and checks["free_group_root_degree"] == 4',
    },
    "chapter-04": {
        "builder": "build_group_action_visuals",
        "figure_files": ["tree-action-and-ping-pong-domains.png", "orbit-stabiliser-action-audit.png"],
        "html_file": "tree-action-sectors.html",
        "checks_file": "action-and-ping-pong-checks.json",
        "question": "How does a group reveal itself by moving another space?",
        "motivation": """
        A group action turns algebra into controlled motion. Instead of studying group elements only as vertices in their own Cayley graph, we let them move points, trees, intervals, vector spaces, or other geometric objects. Orbits show where points can travel; stabilisers show what remains fixed; free actions remove hidden symmetries; transitive actions reduce a space to one orbit.

        The chapter is especially important because actions on trees expose free structure, while ping-pong arguments show freeness from disjoint dynamical domains. The notebook keeps both ideas visible. A colored free-tree model suggests how sectors move under generators, and interval domains show the ping-pong logic: a generator sends almost everything into its own attracting region, leaving no room for an unexpected relation.
        """,
        "translation": """
        - An action is a homomorphism from the group to transformations of a space.
        - Orbits are reachable sets; stabilisers are symmetry leftovers.
        - A tree action can encode decompositions and freeness.
        - Ping-pong domains are disjoint regions that certify reduced words act nontrivially.
        - Matrix group applications often become tractable after choosing the right action.
        """,
        "routing": "NetworkX draws the tree action sectors and finite orbit-stabiliser audit; Matplotlib makes ping-pong intervals explicit; Plotly saves an interactive tree-sector view; exact arithmetic verifies the orbit-stabiliser product in the finite S3 model.",
        "storyboard": """
        The overview visual pairs a tree action model with ping-pong domains. The diagnostic visual reduces the abstract orbit-stabiliser theorem to a finite audit: orbit size times stabiliser size equals the group order for the action of S3 on three letters.
        """,
        "inspection": """
        In the tree, colors are not mere decoration: they mark first-letter sectors, which act like coarse domains for generator dynamics. In the ping-pong panel, inspect which regions are declared attracting and how the arrows encode a proof strategy. In the finite audit, check that the stabiliser accounts for exactly the symmetries invisible from one chosen point.
        """,
        "lab": """
        Applied lab: try to invent a failed ping-pong setup by letting two attracting domains overlap. The visual proof should break immediately, because a reduced word could no longer be forced into a unique final domain. This failure mode is useful: it shows why the hypotheses are geometric, not cosmetic.
        """,
        "takeaways": [
            "Actions let groups be studied through motion on other spaces.",
            "Tree actions and ping-pong domains are visual proof machines for freeness.",
            "Orbit-stabiliser is a finite prototype of the same action bookkeeping.",
        ],
        "assertion": 'assert checks["orbit_stabiliser_product"] == checks["s3_order"]',
    },
    "chapter-05": {
        "builder": "build_quasi_isometry_visuals",
        "figure_files": ["same-group-different-word-metrics.png", "quasi-isometry-distortion-envelope.png"],
        "html_file": "word-metric-distortion.html",
        "checks_file": "quasi-isometry-distortion-checks.json",
        "question": "When should two metric spaces count as the same from far away?",
        "motivation": """
        Quasi-isometry is the course language for large-scale sameness. It allows bounded additive error and multiplicative distortion, so it does not care about small wrinkles, local subdivision, or a particular finite generating set. This is exactly what finitely generated groups need: different generating sets can give different Cayley graphs, but the group should not acquire a different large-scale geometry just because we chose a different alphabet.

        The notebook uses Z^2 with two word metrics. The standard generators move horizontally and vertically; adding a diagonal generator shortens some paths. Locally the graphs differ. Coarsely, the identity map still carries one metric to the other within a uniform linear envelope.
        """,
        "translation": """
        - A quasi-isometric embedding controls distances above and below up to linear distortion and bounded error.
        - A quasi-isometry also has a coarse inverse, so both spaces see each other at finite distance.
        - Different finite generating sets on the same group define quasi-isometric word metrics.
        - Quasi-geodesics are paths that are efficient after coarse distortion is allowed.
        - The Svarc-Milnor perspective turns good geometric actions into quasi-isometries with groups.
        """,
        "routing": "NetworkX builds the competing Cayley graph windows; Matplotlib compares their local edge structures and plots the distortion envelope; Plotly saves the sampled distance scatter; exact grid-distance checks bound the identity map by a factor-two coarse Lipschitz constant.",
        "storyboard": """
        The first visual shows the same finite patch of Z^2 under two generating sets. The second visual samples many group elements and plots the standard word distance against the distance after adding a diagonal generator. The factor-two line is the promised coarse envelope.
        """,
        "inspection": """
        Find points on the diagonal: they become closer when the diagonal generator is available. Then look at points with opposite signs, where the diagonal generator does not help. The scatter plot teaches the definition: quasi-isometry is not equality of distances, but controlled distortion across the whole sample.
        """,
        "lab": """
        Applied lab: add more generators to Z^2, such as (2,1). The graph becomes locally denser and some distances shrink, but any finite addition should still be coarsely equivalent to the original word metric. The expected validation is another linear envelope, perhaps with a different constant.
        """,
        "takeaways": [
            "Quasi-isometry is the correct equivalence relation for finitely generated groups as large-scale spaces.",
            "Changing finite generators changes local geometry but not the coarse type.",
            "The proof habit is to replace exact equality by uniform distance inequalities.",
        ],
        "assertion": 'assert checks["max_standard_over_diagonal"] <= checks["coarse_lipschitz_constant"]',
    },
    "chapter-06": {
        "builder": "build_growth_visuals",
        "figure_files": ["growth-profiles-z-z2-free-group.png", "growth-boundary-volume-preview.png"],
        "html_file": "growth-profile-comparison.html",
        "checks_file": "growth-profile-checks.json",
        "question": "How fast does a group fill space as word length increases?",
        "motivation": """
        Growth converts the word metric into a counting invariant. Around the identity, count how many group elements can be reached with at most r generator steps. The resulting function is not meant to be an exact fingerprint; it is studied up to coarse comparison because changing generators changes constants. Even so, growth type separates major geometric behaviors: linear for Z, quadratic for Z^2, and exponential for a free group of rank two.

        This chapter later connects polynomial growth with virtual nilpotence and treats uniform exponential growth as a robust opposite behavior. The notebook begins with exact small-radius formulas, then previews boundary-to-volume ratios because the same shape intuition returns in amenability.
        """,
        "translation": """
        - A growth function counts word-metric balls.
        - Growth type compares functions after rescaling radius and size by coarse constants.
        - Polynomial growth signals constrained algebraic structure.
        - Exponential growth signals persistent branching or many independent word choices.
        - Growth is a quasi-isometry invariant when interpreted coarsely.
        """,
        "routing": "Exact formulas provide reproducible growth profiles for Z, Z^2, and F2; Matplotlib displays both ordinary and log-scaled plots; Plotly saves an interactive comparison; boundary ratio computations connect growth geometry to later Folner diagnostics.",
        "storyboard": """
        The first visual plots ball volumes on ordinary and logarithmic scales. The second visual compares boundary-to-volume behavior for square sets and free-tree balls, preparing the amenability notebook without replacing its definitions.
        """,
        "inspection": """
        On the ordinary plot, Z and Z^2 are visible but the free group quickly dominates. On the logarithmic plot, exponential growth becomes closer to a straight line. In the boundary preview, notice that a square's boundary is lower-order compared with its area, while a tree ball keeps a frontier comparable to its volume.
        """,
        "lab": """
        Applied lab: estimate growth from a finite Cayley graph ball by computing sphere sizes and cumulative ball sizes. Decide whether your evidence is local or genuinely asymptotic. This distinction matters: finite windows can suggest a trend, but the theorem-level invariant lives at large radius.
        """,
        "takeaways": [
            "Growth functions turn metric balls into algebraic evidence.",
            "Polynomial and exponential behavior are coarse, not exact, classifications.",
            "Boundary size already hints at the amenability split developed later.",
        ],
        "assertion": 'assert checks["f2_successive_ratio_last"] > 2.5 and checks["square_boundary_ratio_radius_8"] < checks["free_tree_boundary_ratio_radius_8"]',
    },
    "chapter-07": {
        "builder": "build_hyperbolic_visuals",
        "figure_files": ["thin-triangles-tree-versus-grid.png", "four-point-hyperbolicity-diagnostic.png"],
        "html_file": "hyperbolic-free-tree.html",
        "checks_file": "hyperbolic-graph-checks.json",
        "question": "What does negative curvature mean when the space is a graph?",
        "motivation": """
        Hyperbolic groups are defined by applying a negative-curvature condition to Cayley graphs. Instead of differentiable curvature, the graph version asks whether geodesic triangles are uniformly thin. Trees are the model case: every geodesic triangle is really a tripod. Grids fail because triangles can contain broad regions far from the other sides.

        The notebook uses both a visible triangle comparison and a finite four-point diagnostic. The four-point condition is not a replacement for the full theory, but it is a reliable computational probe for small graph models. It also prepares the later ideas around quasi-geodesics, word problem algorithms, centralisers, quasi-convexity, and why products tend to fight negative curvature.
        """,
        "translation": """
        - Classical curvature intuition is replaced by metric triangle thinness.
        - A hyperbolic graph has a uniform delta controlling all geodesic triangles.
        - A hyperbolic group is one whose Cayley graph is hyperbolic for a finite generating set.
        - Quasi-geodesics are stable in hyperbolic spaces, which supports algorithmic applications.
        - Products and large flat grids create thick triangles and obstruct hyperbolicity.
        """,
        "routing": "NetworkX computes shortest paths and four-point hyperbolicity samples; Matplotlib highlights geodesic triangles in tree and grid models; Plotly saves an interactive free-tree model; JSON checks record that the grid diagnostic exceeds the tree diagnostic.",
        "storyboard": """
        The first visual highlights a geodesic triangle in a free tree and in a grid. The second visual compresses the comparison into a sampled four-point delta bar chart. The purpose is to tie the definition to something a learner can inspect rather than merely recite.
        """,
        "inspection": """
        In the tree panel, each side shares a central stem with the others; there is no thick middle. In the grid panel, the route between two vertices can run along a broad Manhattan corridor. The diagnostic bar is the numerical shadow of that visual difference.
        """,
        "lab": """
        Applied lab: build a larger grid window and watch the sampled delta grow. Then build a larger free-tree ball and check that the tree diagnostic stays at zero. This experiment is the quickest way to feel the difference between finite-size artifacts and a uniform hyperbolicity constant.
        """,
        "takeaways": [
            "Hyperbolicity in graphs is a metric thin-triangle condition.",
            "Free groups are hyperbolic because their Cayley graphs are trees.",
            "Grid-like flats produce thick triangles and are the standard obstruction.",
        ],
        "assertion": 'assert checks["free_tree_delta"] == 0.0 and checks["grid_delta_exceeds_tree_delta"]',
    },
    "chapter-08": {
        "builder": "build_ends_boundary_visuals",
        "figure_files": ["ends-after-removing-balls.png", "free-tree-boundary-prefix-cylinders.png"],
        "html_file": "free-tree-boundary-prefixes.html",
        "checks_file": "ends-boundary-checks.json",
        "question": "What can a group look like from infinitely far away?",
        "motivation": """
        Ends and boundaries study geometry at infinity. Ends ask a coarse connectivity question: remove a large ball and count the unbounded directions that remain. Boundaries, especially Gromov boundaries of hyperbolic spaces, remember richer classes of rays. Both ideas are quasi-isometry flavored because they are designed to survive bounded local changes.

        The notebook compares three model Cayley geometries. The line has two directions after a central ball is removed. The grid remains connected outside the ball, so it has one coarse end. The free tree splits into many branches, and its boundary can be approximated by cylinder sets of infinite reduced words sharing a prefix.
        """,
        "translation": """
        - An end is a persistent component outside larger and larger balls.
        - A boundary point of a hyperbolic graph is represented by a ray, up to finite fellow travelling.
        - Free-tree boundary neighborhoods are prefix cylinders of infinite reduced words.
        - Quasi-isometries preserve the large-scale structure needed for ends and boundaries.
        - Rigidity results use boundary behavior as a high-resolution invariant at infinity.
        """,
        "routing": "NetworkX removes metric balls and counts remaining components; Matplotlib colors components and prefix cylinders; Plotly saves the free-tree boundary approximation; JSON checks record the line, grid, and tree component counts.",
        "storyboard": """
        The first visual removes a small ball from three graph models and colors what remains. The second visual counts length-four prefixes in the free tree, turning boundary neighborhoods into finite data that can be inspected and checked.
        """,
        "inspection": """
        In the line, the removed center separates left from right. In the grid, paths can still go around the missing center. In the tree, every first generator direction opens into a separate component. The prefix bar chart then shifts from ends to boundary: it counts initial choices of rays rather than components alone.
        """,
        "lab": """
        Applied lab: increase the removal radius. The exact finite component count near the boundary of the drawn window may change, but the stable coarse pattern should not: two for the line, one for the grid, and many branching directions for the tree. This is the right mental model for ends as eventual behavior.
        """,
        "takeaways": [
            "Ends measure coarse directions that survive outside large balls.",
            "Boundaries refine infinity by tracking ray classes.",
            "Free groups have boundary behavior encoded by infinite reduced words.",
        ],
        "assertion": 'assert checks["line_components_after_radius_1"] == 2 and checks["grid_components_after_radius_1"] == 1 and checks["tree_components_after_radius_1"] == 4',
    },
    "chapter-09": {
        "builder": "build_amenability_visuals",
        "figure_files": ["folner-ratios-and-square-set.png", "free-tree-persistent-frontier.png"],
        "html_file": "folner-boundary-volume-ratios.html",
        "checks_file": "amenability-folner-checks.json",
        "question": "When can a group support averaging that is compatible with translation?",
        "motivation": """
        Amenability has several equivalent faces: invariant means, Folner sequences, failure of paradoxical decomposition, and homological characterisations. For a computational geometry course, the Folner viewpoint is the most inspectable. We look for finite sets whose boundary is small compared with their volume. In groups like Z^2, large squares have boundary growing like side length and volume growing like area, so the ratio shrinks. In a free group, balls keep a frontier comparable to their size.

        This notebook does not try to prove all equivalences. It builds the visual reflex needed for the chapter: amenability is detected by whether finite regions can become almost invariant under generator moves.
        """,
        "translation": """
        - A mean is an abstract averaging functional that should ignore translation.
        - A Folner set is a finite witness for approximate invariance.
        - Boundary means generator moves that leave the chosen finite set.
        - Paradoxical decomposition is the opposite signal: pieces can be shifted into too much space.
        - Amenability is a quasi-isometry invariant for finitely generated groups.
        """,
        "routing": "Exact formulas compare square boundary ratios in Z^2 with free-tree ball ratios; Matplotlib highlights candidate finite sets and persistent frontiers; Plotly saves an interactive ratio chart; JSON checks assert shrinking square ratios and large tree ratios.",
        "storyboard": """
        The first visual plots boundary-to-volume ratios and shows a square candidate Folner set. The second visual highlights the frontier of a tree ball, where new branches keep appearing as fast as the ball grows.
        """,
        "inspection": """
        The square set should feel increasingly stable under small translations as it grows: most points remain internal. The tree ball should feel unstable because a large share of its vertices live near the frontier. The ratio plot makes this contrast numerical without hiding the geometry.
        """,
        "lab": """
        Applied lab: compare boxes, diamonds, and random connected sets in Z^2. Different shapes have different finite ratios, but good growing families should push the ratio toward zero. This is the same coarse habit as quasi-isometry: finite noise is less important than asymptotic behavior.
        """,
        "takeaways": [
            "Folner ratios turn amenability into a boundary-size experiment.",
            "Abelian lattice groups admit increasingly invariant finite regions.",
            "Free groups fail the visual Folner test because branching creates persistent frontier.",
        ],
        "assertion": 'assert checks["z2_ratio_decreases"] and checks["free_tree_ratio_stays_large"]',
    },
    "appendix-a": {
        "builder": "build_appendix_visuals",
        "figure_files": ["covering-and-poincare-disk-models.png", "hyperbolic-plane-distance-samples.png"],
        "html_file": "poincare-disk-geodesics.html",
        "checks_file": "appendix-hyperbolic-distance-checks.json",
        "question": "Which background models support the main course without becoming a separate topology or geometry course?",
        "motivation": """
        The appendix gathers tools that appear throughout geometric group theory: fundamental groups, covering spaces, group cohomology, the hyperbolic plane, and programming tasks. In this notebook those tools are treated as reference models. The emphasis is on reusable pictures and checks: a line wrapping around a circle for covering theory, Poincare disk geodesics for hyperbolic geometry, and exact distance symmetry as a sanity check.

        The goal is not to replace a full course in algebraic topology or hyperbolic geometry. Instead, the appendix gives a computational shelf of models that can be pulled into the main chapters when actions, fundamental groups, hyperbolic spaces, or programming exercises need a concrete anchor.
        """,
        "translation": """
        - Fundamental groups record loop classes and become group-valued invariants of spaces.
        - Covering spaces turn local homeomorphism data into lifted paths and deck transformations.
        - Group cohomology packages algebraic obstructions and invariants.
        - The hyperbolic plane supplies a classical model for negative curvature.
        - Programming tasks become reproducible experiments when paired with saved artifacts and numeric checks.
        """,
        "routing": "Matplotlib draws durable covering and Poincare disk diagrams; Plotly saves an interactive disk-geodesic sketch; NumPy evaluates the Poincare disk distance formula; JSON checks record distance symmetry and positivity.",
        "storyboard": """
        The first visual places a covering-space schematic beside a Poincare disk model. The second visual samples points in the disk and prepares distance computations. The HTML artifact keeps the geodesic sketch available outside notebook execution.
        """,
        "inspection": """
        In the covering schematic, imagine a path on the circle lifting to a path upstairs whose endpoint may shift by a deck translation. In the disk, geodesics are represented by diameters or arcs orthogonal to the boundary circle. The distance check is deliberately modest: symmetry and positivity are the first alarms for a broken model.
        """,
        "lab": """
        Applied lab: choose two points closer to the boundary and compare their hyperbolic distance with their Euclidean distance. The hyperbolic distance should feel larger near the edge. This prepares the intuition that negative-curvature models stretch the boundary into an infinite horizon.
        """,
        "takeaways": [
            "The appendix supplies reusable topological and hyperbolic models.",
            "Covering spaces connect path lifting with group actions.",
            "Hyperbolic-plane computations need explicit model conventions and sanity checks.",
        ],
        "assertion": 'assert checks["distance_symmetry_error"] < 1e-12 and checks["positive_distance_check"]',
    },
}


def setup_code() -> str:
    return dedent(
        """
        from pathlib import Path
        import sys

        HERE = Path.cwd()
        for candidate in (HERE, *HERE.parents):
            if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
                BOOK_ROOT = candidate
                break
        else:
            raise RuntimeError("Could not locate the Geometric Group Theory course root.")

        if str(BOOK_ROOT) not in sys.path:
            sys.path.insert(0, str(BOOK_ROOT))

        BOOK_ROOT
        """
    ).strip()


def generation_code(builder: str, unit: str) -> str:
    return dedent(
        f"""
        from utils.chapter_visuals import {builder}

        UNIT = "{unit}"
        outputs = {builder}(UNIT)
        outputs
        """
    ).strip()


def display_figures_code(unit: str, figures: list[str]) -> str:
    figure_lines = "\n".join(
        f'display_artifact(artifact_root / "figures" / "{filename}", width=920)' for filename in figures
    )
    return dedent(
        f"""
        from utils.artifacts import display_artifact

        artifact_root = BOOK_ROOT / "artifacts" / "{unit}"
        {figure_lines}
        """
    ).strip()


def display_html_checks_code(unit: str, html_file: str, checks_file: str) -> str:
    return dedent(
        f"""
        from utils.artifacts import display_artifact, read_json

        artifact_root = BOOK_ROOT / "artifacts" / "{unit}"
        display_artifact(artifact_root / "html" / "{html_file}", height=560)
        checks = read_json(artifact_root / "checks" / "{checks_file}")
        checks
        """
    ).strip()


def final_checks_code(unit: str, checks_file: str, assertion: str) -> str:
    return dedent(
        f"""
        from utils.artifacts import assert_artifact, read_json

        artifact_root = BOOK_ROOT / "artifacts" / "{unit}"
        final = read_json(artifact_root / "checks" / "final-sanity.json")
        checks = read_json(artifact_root / "checks" / "{checks_file}")

        for row in final["artifacts"]:
            path = BOOK_ROOT / row["path"]
            assert_artifact(
                path,
                min_bytes=1024 if path.suffix.lower() == ".html" else 512,
                nonblank_image=path.suffix.lower() == ".png",
            )

        {assertion}
        final
        """
    ).strip()


def markdown_intro(entry: dict[str, object], details: dict[str, object]) -> str:
    return dedent(
        f"""
        # {entry['label']}: {entry['title']}

        **Source span:** printed pp. {entry['printed_span']}; physical PDF pp. {entry['pdf_span']}. The local PDF is used for orientation and concept coverage only. The prose, examples, diagrams, code, and checks in this notebook are original.

        **Chapter question:** {details['question']}

        {str(details['motivation']).strip()}

        This notebook is standalone: it introduces the working objects, builds the relevant finite models, saves artifacts under `artifacts/{entry['artifact']}/`, and ends with sanity checks. When a finite graph window is used, treat it as a controlled model of the local or coarse pattern, not as a claim that the infinite group has been exhausted.
        """
    ).strip()


def markdown_translation(details: dict[str, object]) -> str:
    return dedent(
        f"""
        ## Translation Guide

        {str(details['translation']).strip()}

        ## Library routing

        {details['routing']}
        """
    ).strip()


def markdown_storyboard(details: dict[str, object]) -> str:
    return dedent(
        f"""
        ## Visual Storyboard

        {str(details['storyboard']).strip()}

        Each visual has a nearby computational check. The check is intentionally small enough to be readable: graph connectivity, relation identities, distance distortion bounds, hyperbolicity samples, component counts, boundary ratios, or model-distance sanity tests. The artifacts are saved before display so the notebook can be audited outside the live kernel.
        """
    ).strip()


def markdown_inspection(details: dict[str, object]) -> str:
    return dedent(
        f"""
        ## What To Inspect

        {str(details['inspection']).strip()}

        The useful habit is to ask which feature of the picture survives when the finite drawing is enlarged. Vertices at the edge of a rendered ball are artifacts of the cut window; branching, cycles, distance envelopes, shrinking ratios, and stable component counts are the features meant to carry mathematical information.
        """
    ).strip()


def markdown_lab(details: dict[str, object]) -> str:
    return dedent(
        f"""
        ## Applied Lab

        {str(details['lab']).strip()}

        A good extension of this lab should add one new parameter, state the predicted invariant before running code, and save a check JSON next to any new figure. That pattern keeps experimentation tied to proof-relevant evidence rather than to attractive but untested pictures.
        """
    ).strip()


def markdown_takeaways(details: dict[str, object]) -> str:
    bullets = "\n".join(f"- {item}" for item in details["takeaways"])
    return dedent(
        f"""
        ## Takeaways

        {bullets}

        The final cell below re-reads the saved artifact manifest and the chapter-specific check file. It is deliberately redundant: rerunning the notebook should both rebuild the visuals and verify that the saved course assets remain present, nonempty, and mathematically consistent.
        """
    ).strip()


def build_notebook(entry: dict[str, object]) -> nbformat.NotebookNode:
    unit = str(entry["artifact"])
    details = DETAILS[unit]
    cells = [
        new_markdown_cell(markdown_intro(entry, details)),
        new_markdown_cell(markdown_translation(details)),
        new_code_cell(setup_code()),
        new_markdown_cell(markdown_storyboard(details)),
        new_code_cell(generation_code(str(details["builder"]), unit)),
        new_markdown_cell(markdown_inspection(details)),
        new_code_cell(display_figures_code(unit, list(details["figure_files"]))),
        new_code_cell(display_html_checks_code(unit, str(details["html_file"]), str(details["checks_file"]))),
        new_markdown_cell(markdown_lab(details)),
        new_markdown_cell(markdown_takeaways(details)),
        new_code_cell(final_checks_code(unit, str(details["checks_file"]), str(details["assertion"]))),
    ]
    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python", "pygments_lexer": "ipython3"}
    return nb


def main() -> None:
    for entry in ENTRIES:
        path = BOOK_ROOT / str(entry["folder"]) / str(entry["notebook"])
        path.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(build_notebook(entry), path)
        print(path.relative_to(BOOK_ROOT).as_posix())


if __name__ == "__main__":
    main()

