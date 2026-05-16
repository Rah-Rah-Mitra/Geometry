"""Static source map and chapter inventory for the Voisin Hodge course.

The data in this module is an original teaching inventory built from the local
tables of contents and body page offsets. It does not contain copied textbook
prose, exercises, screenshots, or figures.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PDF_PAGE_OFFSET = 12


@dataclass(frozen=True)
class Chapter:
    id: str
    volume: int
    volume_slug: str
    volume_title: str
    part: str
    part_slug: str
    number: str
    title: str
    printed_start: int
    printed_end: int
    pdf_file: str
    folder_slug: str
    notebook_slug: str
    sections: tuple[str, ...]
    goal: str
    overview: str
    concepts: tuple[str, ...]
    proof_moves: tuple[str, ...]
    pitfalls: tuple[str, ...]
    visual_kind: str
    visual_focus: str
    library_routes: tuple[str, ...]
    checks: tuple[str, ...]
    lab: str
    hodge_numbers: tuple[tuple[int, ...], ...]

    @property
    def pdf_start(self) -> int:
        return self.printed_start + PDF_PAGE_OFFSET

    @property
    def pdf_end(self) -> int:
        return self.printed_end + PDF_PAGE_OFFSET

    @property
    def source_span(self) -> str:
        return (
            f"volume {self.volume}, printed pages {self.printed_start}-{self.printed_end}, "
            f"PDF pages {self.pdf_start}-{self.pdf_end}"
        )

    @property
    def part_path(self) -> Path:
        return Path(self.volume_slug) / self.part_slug

    @property
    def chapter_path(self) -> Path:
        return self.part_path / self.folder_slug

    @property
    def notebook_name(self) -> str:
        return f"{self.notebook_slug}.ipynb"

    @property
    def notebook_path(self) -> Path:
        return self.chapter_path / self.notebook_name

    @property
    def artifact_key(self) -> str:
        return f"volume-{self.volume:02d}/{self.id}"


VOLUME_PDFS = {
    1: "Hodge Theory and Complex Algebraic Geometry I.pdf",
    2: "Hodge Theory and Complex Algebraic Geometry II.pdf",
}


PARTS = {
    1: (
        ("part-00-orientation", "Orientation"),
        ("part-01-preliminaries", "Preliminaries"),
        ("part-02-hodge-decomposition", "The Hodge Decomposition"),
        ("part-03-variations-of-hodge-structure", "Variations of Hodge Structure"),
        ("part-04-cycles-and-cycle-classes", "Cycles and Cycle Classes"),
    ),
    2: (
        ("part-00-orientation", "Orientation"),
        ("part-01-topology-of-algebraic-varieties", "The Topology of Algebraic Varieties"),
        ("part-02-variations-of-hodge-structure", "Variations of Hodge Structure"),
        ("part-03-algebraic-cycles", "Algebraic Cycles"),
    ),
}


def diamond(*rows: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    return rows


CHAPTERS: tuple[Chapter, ...] = (
    Chapter(
        id="v1-c00",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Orientation",
        part_slug="part-00-orientation",
        number="0",
        title="Introduction",
        printed_start=1,
        printed_end=18,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-00-introduction",
        notebook_slug="00-introduction",
        sections=("Kahler and projective manifolds", "Hodge decomposition", "Lefschetz decomposition", "Cycle classes and Abel-Jacobi"),
        goal="Turn the first volume into a navigable map from differential forms to Hodge theory and algebraic cycles.",
        overview="This opening chapter sets the contract for the volume: start with compact Kahler geometry, extract cohomological decompositions, and then read those decompositions as constraints on topology and cycles. The notebook treats Hodge and Lefschetz decompositions as two coordinate systems on cohomology, one coming from complex type and one from the Kahler class.",
        concepts=("compact Kahler manifold", "Hodge decomposition", "Hodge symmetry", "Hard Lefschetz", "primitive cohomology", "cycle class", "intermediate Jacobian"),
        proof_moves=("compare type decomposition with de Rham cohomology", "use the Kahler class as a raising operator", "track which constraints are topological and which remember complex structure"),
        pitfalls=("confusing a form of type (p,q) with a cohomology class that has a representative of that type", "forgetting that projectivity is stronger than being Kahler", "treating the Abel-Jacobi invariant as a primary cycle class"),
        visual_kind="hodge-lefschetz",
        visual_focus="A Hodge diamond overlaid with a Lefschetz staircase shows the two decompositions acting on the same cohomology.",
        library_routes=("Matplotlib for a durable Hodge diamond and Lefschetz arrows", "SymPy for small rank and symmetry checks"),
        checks=("Hodge diamond symmetry", "odd Betti parity in a toy Kahler diamond", "Lefschetz staircase rank monotonicity"),
        lab="Compare a toy Kahler surface with a Hopf-like odd Betti ledger and identify which notebook checks fail.",
        hodge_numbers=diamond((1,), (1, 1), (1, 4, 1), (1, 1), (1,)),
    ),
    Chapter(
        id="v1-c01",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Preliminaries",
        part_slug="part-01-preliminaries",
        number="1",
        title="Holomorphic Functions of Many Variables",
        printed_start=21,
        printed_end=37,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-01-holomorphic-functions-of-many-variables",
        notebook_slug="01-holomorphic-functions-of-many-variables",
        sections=("One complex variable", "Stokes and Cauchy", "Several variables", "The dbar equation"),
        goal="Make Cauchy propagation, separate holomorphy, and the local dbar equation visible as tools for later sheaf resolutions.",
        overview="The chapter supplies the analytic engine behind the later Dolbeault and de Rham resolutions. The notebook follows values from boundary data into the interior of a polydisc, then rewrites the dbar problem as a solvability checkpoint for local exactness.",
        concepts=("Cauchy integral formula", "polydisc", "analyticity", "several complex variables", "dbar equation", "Stokes formula"),
        proof_moves=("reduce local holomorphic control to boundary averages", "separate variables before recombining them", "turn local exactness into an integral operator problem"),
        pitfalls=("thinking several-variable holomorphy is just two unrelated one-variable stories", "forgetting orientation in Stokes formula", "treating dbar solvability as global without hypotheses"),
        visual_kind="polydisc-cauchy",
        visual_focus="A polydisc contour diagram shows how boundary samples determine interior values and where dbar correction terms enter.",
        library_routes=("Matplotlib for contour and kernel diagrams", "NumPy for sampling a synthetic holomorphic function", "SymPy for exact Cauchy-Riemann checks"),
        checks=("Cauchy-Riemann residual is zero for the model holomorphic function", "dbar residual is nonzero for a controlled non-holomorphic perturbation"),
        lab="Move a sample point through a bidisc and watch which boundary circles dominate the Cauchy estimate.",
        hodge_numbers=diamond((1,), (0, 0), (0, 1, 0), (0, 0), (1,)),
    ),
    Chapter(
        id="v1-c02",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Preliminaries",
        part_slug="part-01-preliminaries",
        number="2",
        title="Complex Manifolds",
        printed_start=38,
        printed_end=62,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-02-complex-manifolds",
        notebook_slug="02-complex-manifolds",
        sections=("Manifolds and vector bundles", "Almost complex structures", "Frobenius and Newlander-Nirenberg", "The operators partial and dbar", "Examples"),
        goal="Show how atlases, tangent splitting, and integrability produce the Dolbeault complex used throughout Hodge theory.",
        overview="Complex manifolds are built from holomorphic coordinate changes, but the later theory wants a coordinate-free language. This notebook translates an atlas into a split complexified tangent bundle and uses bracket closure as the visible obstruction to integrability.",
        concepts=("complex atlas", "holomorphic vector bundle", "almost complex structure", "integrability", "Frobenius theorem", "Newlander-Nirenberg theorem", "Dolbeault complex"),
        proof_moves=("compare local charts through transition functions", "split tangent vectors into type (1,0) and type (0,1)", "measure integrability by closure of a distribution under brackets"),
        pitfalls=("assuming every almost complex structure is integrable", "mixing real tangent rank with complex rank", "forgetting that d splits only after complexification"),
        visual_kind="complex-atlas",
        visual_focus="Overlapping charts and tangent cones show where the type decomposition lives and how bracket closure is tested.",
        library_routes=("Matplotlib for atlas and tangent splitting diagrams", "NetworkX for dependency flow from atlas to Dolbeault complex", "SymPy for a bracket closure toy check"),
        checks=("projectors onto type components are idempotent", "toy bracket closure flag separates integrable and nonintegrable models"),
        lab="Perturb a local almost complex matrix and inspect which algebraic identity fails first.",
        hodge_numbers=diamond((1,), (1, 1), (0, 2, 0), (1, 1), (1,)),
    ),
    Chapter(
        id="v1-c03",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Preliminaries",
        part_slug="part-01-preliminaries",
        number="3",
        title="Kahler Metrics",
        printed_start=63,
        printed_end=82,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-03-kahler-metrics",
        notebook_slug="03-kahler-metrics",
        sections=("Hermitian geometry", "Kahler forms", "Connections", "Fubini-Study metric", "Blowups"),
        goal="Connect Hermitian metric data, closed Kahler forms, and compatible connections to the later operator identities.",
        overview="The notebook treats the Kahler condition as an alignment of three languages: metric, symplectic form, and complex structure. Fubini-Study space gives the model, while blowups provide a first warning that positivity must be watched carefully.",
        concepts=("Hermitian metric", "Kahler form", "closed (1,1)-form", "Chern form", "Fubini-Study metric", "blowup"),
        proof_moves=("encode metric data as a positive Hermitian matrix", "test the closedness of the fundamental form", "pull the model metric from projective space"),
        pitfalls=("confusing a Hermitian metric with a Kahler metric", "ignoring positivity when changing a form", "treating local potentials as globally single-valued"),
        visual_kind="kahler-identities",
        visual_focus="A metric-form-complex triangle records the compatibility identities that define the Kahler package.",
        library_routes=("Matplotlib for compatibility diagrams and Fubini-Study potential contours", "SymPy for a local closedness calculation", "NumPy for positivity checks"),
        checks=("Hermitian matrix is positive definite", "toy Kahler form has zero exterior derivative", "Fubini-Study potential Hessian is positive at sample points"),
        lab="Vary a Hermitian matrix and watch the notebook distinguish positivity from the closedness condition.",
        hodge_numbers=diamond((1,), (0, 0), (1, 2, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v1-c04",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Preliminaries",
        part_slug="part-01-preliminaries",
        number="4",
        title="Sheaves and Cohomology",
        printed_start=83,
        printed_end=114,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-04-sheaves-and-cohomology",
        notebook_slug="04-sheaves-and-cohomology",
        sections=("Sheaves, stalks, kernels, images", "Resolutions", "Derived functors", "Acyclic resolutions", "de Rham theorems", "Interpreting H1"),
        goal="Make sheaf cohomology computationally legible through resolutions, exactness tests, and de Rham comparison.",
        overview="Sheaves record local-to-global failure. The notebook uses a small cover and a resolution ladder to show how local exactness feeds global cohomology, preparing the reader for Dolbeault and hypercohomology.",
        concepts=("sheaf", "stalk", "exact sequence", "resolution", "injective resolution", "acyclic resolution", "sheaf cohomology", "de Rham theorem"),
        proof_moves=("replace a sheaf by a complex that is easier to compute", "track kernels and images through a ladder", "interpret H1 as gluing failure"),
        pitfalls=("mistaking a presheaf restriction rule for the sheaf gluing axiom", "assuming exactness survives global sections", "forgetting that resolutions compute only when acyclicity is available"),
        visual_kind="resolution-ladder",
        visual_focus="A cover nerve and a resolution ladder expose where cochains, coboundaries, and sheaf cohomology sit.",
        library_routes=("NetworkX for cover and dependency graphs", "Matplotlib for exact-sequence ladders", "NumPy for boundary matrix checks"),
        checks=("toy Cech boundary squares to zero", "rank-nullity ledger is consistent", "acyclic ladder has the expected cohomology"),
        lab="Change a gluing cocycle on a three-open cover and inspect whether it becomes a coboundary.",
        hodge_numbers=diamond((1,), (2, 2), (1, 3, 1), (2, 2), (1,)),
    ),
    Chapter(
        id="v1-c05",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="The Hodge Decomposition",
        part_slug="part-02-hodge-decomposition",
        number="5",
        title="Harmonic Forms and Cohomology",
        printed_start=117,
        printed_end=136,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-05-harmonic-forms-and-cohomology",
        notebook_slug="05-harmonic-forms-and-cohomology",
        sections=("L2 metric", "Formal adjoints", "Laplacians", "Elliptic operators", "Cohomology and harmonic forms", "Duality"),
        goal="Turn the analytic Hodge theorem into an inspectable decomposition of forms into harmonic, exact, and coexact parts.",
        overview="The chapter links differential operators to finite-dimensional cohomology. The notebook models adjoints and Laplacians with small matrices, then uses the kernel of the Laplacian as the visible representative space for cohomology classes.",
        concepts=("L2 metric", "formal adjoint", "Laplacian", "elliptic operator", "harmonic form", "Hodge theorem", "Poincare duality", "Serre duality"),
        proof_moves=("construct adjoints from an inner product", "identify harmonic representatives by the Laplacian kernel", "use ellipticity to pass from analysis to finite-dimensional cohomology"),
        pitfalls=("thinking every closed form is harmonic", "forgetting that the adjoint depends on the metric", "treating elliptic regularity as a formal algebra identity"),
        visual_kind="laplacian-hodge",
        visual_focus="A three-summand form decomposition shows harmonic, exact, and coexact components with a matrix Laplacian check.",
        library_routes=("Matplotlib for decomposition diagrams", "NumPy for finite-dimensional Laplacian experiments", "SymPy for exact kernel dimensions"),
        checks=("Laplacian matrix is symmetric positive semidefinite", "kernel dimension matches toy cohomology", "exact and harmonic components are orthogonal"),
        lab="Change the inner product and compare how the harmonic representative changes while the cohomology dimension stays fixed.",
        hodge_numbers=diamond((1,), (1, 1), (1, 6, 1), (1, 1), (1,)),
    ),
    Chapter(
        id="v1-c06",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="The Hodge Decomposition",
        part_slug="part-02-hodge-decomposition",
        number="6",
        title="The Case of Kahler Manifolds",
        printed_start=137,
        printed_end=155,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-06-the-case-of-kahler-manifolds",
        notebook_slug="06-the-case-of-kahler-manifolds",
        sections=("Kahler identities", "Comparison of Laplacians", "Lefschetz decomposition", "Commutators", "Hodge index theorem"),
        goal="Show why the Kahler identities force de Rham cohomology to split by type and support Lefschetz sl2 structure.",
        overview="This is the first main summit of the course. The notebook visualizes the operator grid formed by d, partial, dbar, adjoints, L, and Lambda, then checks a finite exterior-algebra model for the commutator pattern behind Hodge and Lefschetz decompositions.",
        concepts=("Kahler identities", "Dolbeault Laplacian", "de Rham Laplacian", "Lefschetz operator", "primitive forms", "sl2 commutators", "Hodge index theorem"),
        proof_moves=("compare Laplacians through commutator identities", "use L and Lambda to build weight strings", "separate primitive pieces before applying powers of the Kahler class"),
        pitfalls=("using the Hodge decomposition without compact Kahler hypotheses", "forgetting primitive means killed after enough Lefschetz raising", "mixing the Hodge index form with a positive definite metric"),
        visual_kind="kahler-identities",
        visual_focus="An operator commutator board makes the identities and the Lefschetz string decomposition inspectable.",
        library_routes=("Matplotlib for operator board and Lefschetz strings", "SymPy for commutator checks in a toy exterior algebra", "NumPy for signature checks"),
        checks=("toy commutator H=[Lambda,L] has expected weights", "Hodge diamond symmetry", "intersection form signature matches a surface example"),
        lab="Build Lefschetz strings for a toy surface and identify primitive classes by the failed next raise.",
        hodge_numbers=diamond((1,), (0, 0), (1, 20, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v1-c07",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="The Hodge Decomposition",
        part_slug="part-02-hodge-decomposition",
        number="7",
        title="Hodge Structures and Polarisations",
        printed_start=156,
        printed_end=183,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-07-hodge-structures-and-polarisations",
        notebook_slug="07-hodge-structures-and-polarisations",
        sections=("Hodge structures", "Polarisations", "Polarised varieties", "Projective space", "Weight 1 and abelian varieties", "Weight 2", "Functoriality and blowups"),
        goal="Separate pure Hodge structure data from the varieties that produce it, and use polarisations as the metric that makes the data rigid.",
        overview="The notebook turns the Hodge diamond into linear algebra with a rational lattice, a decomposition, and a bilinear form. Examples from projective space, abelian varieties, and blowups show what information is preserved by functorial operations.",
        concepts=("pure Hodge structure", "weight", "filtration", "polarisation", "abelian variety", "weight two structure", "pullback", "Gysin morphism", "blowup formula"),
        proof_moves=("translate Hodge decomposition into a filtration", "test positivity with a polarising form", "track functorial maps through bidegree"),
        pitfalls=("forgetting the rational lattice", "treating every decomposition as polarised", "losing degree shifts in Gysin maps and blowups"),
        visual_kind="hodge-diamond",
        visual_focus="A polarised Hodge diamond with a lattice overlay shows weight, conjugation, and positivity constraints.",
        library_routes=("Matplotlib for Hodge diamonds and lattice slices", "NumPy for bilinear-form signatures", "SymPy for filtration dimensions"),
        checks=("filtration dimensions recover the Hodge numbers", "polarisation matrix has the expected signature on primitive part", "blowup contribution has the correct shifted type"),
        lab="Assemble a weight-one Hodge structure from a period matrix and test the Riemann bilinear relation in a toy case.",
        hodge_numbers=diamond((1,), (2, 2), (1, 8, 1), (2, 2), (1,)),
    ),
    Chapter(
        id="v1-c08",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="The Hodge Decomposition",
        part_slug="part-02-hodge-decomposition",
        number="8",
        title="Holomorphic de Rham Complexes and Spectral Sequences",
        printed_start=184,
        printed_end=216,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-08-holomorphic-de-rham-complexes-and-spectral-sequences",
        notebook_slug="08-holomorphic-de-rham-complexes-and-spectral-sequences",
        sections=("Hypercohomology", "Holomorphic de Rham complexes", "Logarithmic complexes", "Filtered complexes", "Spectral sequences", "Frolicher sequence", "Open manifolds and Deligne theorem"),
        goal="Make filtered complexes and spectral-sequence pages concrete enough to see how mixed Hodge data emerges.",
        overview="This chapter provides the language for filtrations, hypercohomology, and the spectral sequences that organize them. The notebook follows a small filtered double complex across pages and watches differentials disappear or survive.",
        concepts=("hypercohomology", "filtered complex", "spectral sequence", "Frolicher spectral sequence", "logarithmic de Rham complex", "mixed Hodge structure", "Deligne theorem"),
        proof_moves=("resolve a complex before taking cohomology", "filter a complex and read successive pages", "use degeneration to extract a filtration on cohomology"),
        pitfalls=("reading an E1 term as the final answer", "forgetting total degree p+q", "mixing the Hodge filtration with the weight filtration"),
        visual_kind="spectral-sequence",
        visual_focus="An E-page grid with visible arrows, deaths, and survivors trains the eye to read filtered cohomology.",
        library_routes=("Matplotlib for spectral-sequence pages", "NumPy for boundary matrices", "JSON ledgers for ranks and survivors"),
        checks=("differential squares to zero in the toy double complex", "survivor ranks match the final associated graded", "filtration dimensions are monotone"),
        lab="Change one differential on the E1 page and observe which class survives to E2 and which becomes a boundary.",
        hodge_numbers=diamond((1,), (1, 1), (2, 5, 2), (1, 1), (1,)),
    ),
    Chapter(
        id="v1-c09",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Variations of Hodge Structure",
        part_slug="part-03-variations-of-hodge-structure",
        number="9",
        title="Families and Deformations",
        printed_start=219,
        printed_end=238,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-09-families-and-deformations",
        notebook_slug="09-families-and-deformations",
        sections=("Families of manifolds", "Trivialisations", "Kodaira-Spencer map", "Local systems and flat connections", "Cartan-Lie formula", "Semicontinuity", "Stability of Kahler manifolds"),
        goal="Explain how a moving complex manifold has locally constant topology but varying complex and Hodge data.",
        overview="Families are the bridge from static Hodge structures to variation. The notebook shows an Ehresmann-style trivialization over a small base, then marks the Kodaira-Spencer class as the derivative of complex structure rather than the derivative of topology.",
        concepts=("proper submersion", "differentiable trivialization", "Kodaira-Spencer map", "Gauss-Manin connection", "local system", "semicontinuity", "Kahler stability"),
        proof_moves=("separate topological local constancy from holomorphic variation", "differentiate transition data to obtain Kodaira-Spencer classes", "transport cohomology with a flat connection"),
        pitfalls=("thinking all nearby fibers are holomorphically isomorphic", "confusing the Gauss-Manin connection with a metric connection", "turning upper semicontinuity into equality without extra input"),
        visual_kind="family-deformation",
        visual_focus="A base disk with fibers and tangent arrows distinguishes flat transport from Kodaira-Spencer variation.",
        library_routes=("Matplotlib for family diagrams", "Plotly HTML for a small period-path preview", "NumPy for flat transport matrices"),
        checks=("parallel transport matrix preserves a toy intersection form", "semicontinuity ledger is upper semicontinuous", "Kodaira-Spencer map lands in the expected Hom space"),
        lab="Move along two paths in a punctured base and compare flat transport with the changing Hodge filtration.",
        hodge_numbers=diamond((1,), (2, 2), (1, 6, 1), (2, 2), (1,)),
    ),
    Chapter(
        id="v1-c10",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Variations of Hodge Structure",
        part_slug="part-03-variations-of-hodge-structure",
        number="10",
        title="Variations of Hodge Structure",
        printed_start=239,
        printed_end=260,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-10-variations-of-hodge-structure",
        notebook_slug="10-variations-of-hodge-structure",
        sections=("Grassmannians", "Period map", "Period domain", "Hodge bundles", "Transversality", "Differential of the period map", "Curves", "Calabi-Yau manifolds"),
        goal="Make the period map visible as a horizontal map into a constrained flag domain.",
        overview="The chapter packages moving Hodge filtrations into a holomorphic period map. The notebook draws the period domain as a constrained target, then checks Griffiths transversality by forcing the derivative to lower the filtration by at most one step.",
        concepts=("period domain", "period map", "Hodge bundle", "Griffiths transversality", "horizontal tangent", "variation of Hodge structure", "Calabi-Yau period"),
        proof_moves=("identify filtrations with points in a Grassmannian or flag domain", "differentiate the filtration and read bidegree", "use polarisation to restrict the target"),
        pitfalls=("forgetting the period map is locally defined after choosing a flat trivialization", "confusing arbitrary tangent directions with horizontal directions", "ignoring monodromy when leaving a simply connected patch"),
        visual_kind="period-map",
        visual_focus="A period map curve enters a flag-domain slice with horizontal tangent directions highlighted.",
        library_routes=("Matplotlib for period-domain diagrams", "Plotly HTML for a rotating filtration path", "NumPy for transversality block checks"),
        checks=("derivative matrix has only allowed lower-block entries", "polarisation form is preserved by toy transport", "period path avoids an isotropic forbidden region"),
        lab="Toggle forbidden derivative blocks and watch the transversality checker reject a non-horizontal period path.",
        hodge_numbers=diamond((1,), (0, 0), (1, 3, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v1-c11",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Cycles and Cycle Classes",
        part_slug="part-04-cycles-and-cycle-classes",
        number="11",
        title="Hodge Classes",
        printed_start=263,
        printed_end=289,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-11-hodge-classes",
        notebook_slug="11-hodge-classes",
        sections=("Analytic subsets", "Cohomology class", "Kahler case", "Chern classes", "Hodge classes", "Hodge conjecture", "Correspondences"),
        goal="Connect analytic cycles to cohomology classes of type (k,k), and frame the Hodge conjecture as a visibility problem.",
        overview="This chapter is where geometry re-enters cohomology. The notebook highlights the diagonal band of the Hodge diamond, draws cycle classes landing there, and uses correspondences as operators on cohomology.",
        concepts=("analytic subset", "cycle class", "Chern class", "Hodge class", "Hodge conjecture", "correspondence", "Kunneth component"),
        proof_moves=("associate a cohomology class to an analytic cycle", "prove type constraints using currents or resolutions", "read correspondences as pull-push operators"),
        pitfalls=("assuming every rational Hodge class is known to come from a cycle", "dropping codimension-degree conversion", "forgetting correspondences have degree shifts"),
        visual_kind="cycle-class",
        visual_focus="A Hodge diamond with the (k,k) diagonal highlighted shows where cycle classes can land.",
        library_routes=("Matplotlib for Hodge diamonds and cycle arrows", "NetworkX for correspondence graphs", "NumPy for pull-push matrix checks"),
        checks=("cycle class lands on diagonal bidegrees", "correspondence matrix composition is associative in a toy model", "Chern class degree is even"),
        lab="Compose two toy correspondences and inspect how a Hodge class moves through the bidegree grid.",
        hodge_numbers=diamond((1,), (1, 1), (2, 10, 2), (1, 1), (1,)),
    ),
    Chapter(
        id="v1-c12",
        volume=1,
        volume_slug="volume-01-foundations",
        volume_title="Volume I: Foundations on compact Kahler manifolds",
        part="Cycles and Cycle Classes",
        part_slug="part-04-cycles-and-cycle-classes",
        number="12",
        title="Deligne-Beilinson Cohomology and the Abel-Jacobi Map",
        printed_start=290,
        printed_end=314,
        pdf_file=VOLUME_PDFS[1],
        folder_slug="chapter-12-deligne-beilinson-cohomology-and-the-abel-jacobi-map",
        notebook_slug="12-deligne-beilinson-cohomology-and-the-abel-jacobi-map",
        sections=("Intermediate Jacobians", "Abel-Jacobi map", "Picard and Albanese varieties", "Correspondences", "Deligne complex", "Differential characters", "Cycle class"),
        goal="Explain the Abel-Jacobi invariant as a secondary measurement for homologically trivial cycles.",
        overview="Primary cycle classes vanish on homologically trivial cycles, but geometry can still leave a period. The notebook builds a toy intermediate Jacobian as a torus and draws how integration over a bounding chain gives a well-defined point modulo periods.",
        concepts=("intermediate Jacobian", "Abel-Jacobi map", "homologically trivial cycle", "Picard variety", "Albanese variety", "Deligne complex", "differential character"),
        proof_moves=("quotient a complex vector space by a Hodge subspace and a lattice", "integrate forms over a chain bounding the cycle", "check indeterminacy is exactly the period lattice"),
        pitfalls=("using Abel-Jacobi on a cycle with nonzero primary class", "forgetting the lattice quotient", "treating Deligne cohomology as ordinary de Rham cohomology"),
        visual_kind="abel-jacobi",
        visual_focus="A torus with a chain-integral vector shows how Abel-Jacobi records secondary period data.",
        library_routes=("Matplotlib for torus quotient and path diagrams", "NumPy for lattice reductions", "JSON checks for period ambiguity"),
        checks=("lattice reduction is invariant under changing the bounding chain by a cycle", "primary class flag is zero before Abel-Jacobi is evaluated", "correspondence action respects the quotient"),
        lab="Change a bounding chain by an integral cycle and verify that the Abel-Jacobi point is unchanged on the torus.",
        hodge_numbers=diamond((1,), (3, 3), (1, 7, 1), (3, 3), (1,)),
    ),
    Chapter(
        id="v2-c00",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Orientation",
        part_slug="part-00-orientation",
        number="0",
        title="Introduction",
        printed_start=1,
        printed_end=16,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-00-introduction",
        notebook_slug="00-introduction",
        sections=("Review of volume I", "Mixed Hodge structures", "Variations", "Cycle classes and Abel-Jacobi", "Lefschetz and Leray themes"),
        goal="Orient the second volume around the three-way interaction of topology, variation of Hodge structure, and algebraic cycles.",
        overview="The second volume applies the structures built in the first. This notebook draws the recurring triangle: Lefschetz theorems constrain topology, Leray spectral sequences organize maps, and cycle-theoretic invariants test how much Hodge theory remembers.",
        concepts=("Hard Lefschetz", "mixed Hodge structure", "variation of Hodge structure", "Hodge locus", "Lefschetz theorem", "Leray spectral sequence", "algebraic cycle"),
        proof_moves=("reuse volume I as a toolkit", "compare hyperplane-section topology with Hodge-theoretic decomposition", "organize morphisms through Leray filtrations"),
        pitfalls=("forgetting which results are from compact Kahler geometry and which require projectivity", "treating the three parts as independent", "using mixed Hodge vocabulary without tracking both filtrations"),
        visual_kind="theme-triangle",
        visual_focus="A topology-VHS-cycles triangle marks how the second volume routes results through Lefschetz and Leray mechanisms.",
        library_routes=("Matplotlib for the theme triangle", "NetworkX for dependency edges across the volume", "JSON checks for source-span coverage"),
        checks=("all three volume themes have chapter coverage", "volume I prerequisite nodes are connected to volume II applications"),
        lab="Pick a later theorem and trace which side of the triangle supplies its input.",
        hodge_numbers=diamond((1,), (1, 1), (2, 6, 2), (1, 1), (1,)),
    ),
    Chapter(
        id="v2-c01",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="The Topology of Algebraic Varieties",
        part_slug="part-01-topology-of-algebraic-varieties",
        number="1",
        title="The Lefschetz Theorem on Hyperplane Sections",
        printed_start=19,
        printed_end=40,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-01-the-lefschetz-theorem-on-hyperplane-sections",
        notebook_slug="01-the-lefschetz-theorem-on-hyperplane-sections",
        sections=("Morse lemma", "Level sets", "Global Morse theory", "Affine varieties", "Hyperplane sections", "Vanishing theorems"),
        goal="Visualize how Morse handles on affine pieces explain the cohomology comparison between a variety and a hyperplane section.",
        overview="The chapter proves a topological theorem with Morse theory. The notebook draws critical levels, handles, and hyperplane slices so the degree range in the Lefschetz theorem becomes a dimension-counting picture rather than a slogan.",
        concepts=("Morse function", "critical point", "handle attachment", "affine variety", "hyperplane section", "Lefschetz theorem", "vanishing theorem"),
        proof_moves=("localize near a nondegenerate critical point", "attach handles as levels cross critical values", "bound the index range on affine varieties"),
        pitfalls=("thinking every hyperplane is good", "forgetting affine reduction", "misreading the theorem's isomorphism and injection degree ranges"),
        visual_kind="morse-lefschetz",
        visual_focus="Level-set handles and a hyperplane slice show why cohomology changes only in controlled degrees.",
        library_routes=("Matplotlib for Morse-level diagrams", "NumPy for Hessian index checks", "NetworkX for theorem dependency graph"),
        checks=("sample Hessian index is within the allowed range", "restriction-map degree ledger matches theorem statement", "handle-count Euler characteristic is consistent"),
        lab="Move a hyperplane through a synthetic affine surface and count which critical levels affect the middle degree.",
        hodge_numbers=diamond((1,), (0, 0), (1, 5, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v2-c02",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="The Topology of Algebraic Varieties",
        part_slug="part-01-topology-of-algebraic-varieties",
        number="2",
        title="Lefschetz Pencils",
        printed_start=41,
        printed_end=66,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-02-lefschetz-pencils",
        notebook_slug="02-lefschetz-pencils",
        sections=("Existence of pencils", "Holomorphic Morse lemma", "Lefschetz degeneration", "Vanishing spheres", "Blowup of the base locus", "Vanishing and primitive cohomology"),
        goal="Show how a pencil turns a projective variety into a one-parameter laboratory with isolated singular fibers and vanishing cycles.",
        overview="A Lefschetz pencil compresses a variety into a family over a projective line. The notebook shows the base locus, the blowup, critical values, and the vanishing sphere that collapses at a singular fiber.",
        concepts=("Lefschetz pencil", "base locus", "blowup", "critical value", "vanishing sphere", "primitive cohomology", "vanishing cohomology"),
        proof_moves=("choose a pencil with controlled singularities", "blow up the base locus to obtain a morphism", "compare smooth and singular fibers through vanishing cycles"),
        pitfalls=("ignoring the base locus", "confusing the original variety with its blowup", "treating every degeneration as Lefschetz type"),
        visual_kind="lefschetz-pencil",
        visual_focus="A pencil over a base line marks critical values and a vanishing cycle shrinking in the fiber.",
        library_routes=("Matplotlib for pencil and fiber diagrams", "Plotly HTML for a shrinking-cycle parameter", "NumPy for intersection-pairing checks"),
        checks=("critical values are isolated in the toy pencil", "vanishing-cycle length tends to zero in the model", "primitive and vanishing dimensions add correctly"),
        lab="Slide toward a critical value and watch the vanishing circle collapse while the base locus remains fixed.",
        hodge_numbers=diamond((1,), (1, 1), (1, 9, 1), (1, 1), (1,)),
    ),
    Chapter(
        id="v2-c03",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="The Topology of Algebraic Varieties",
        part_slug="part-01-topology-of-algebraic-varieties",
        number="3",
        title="Monodromy",
        printed_start=67,
        printed_end=97,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-03-monodromy",
        notebook_slug="03-monodromy",
        sections=("Local systems and pi1 representations", "Fibrations", "Monodromy and VHS", "Picard-Lefschetz formula", "Zariski theorem", "Noether-Lefschetz theorem"),
        goal="Make monodromy a concrete action on cohomology, with Picard-Lefschetz transvections as inspectable matrices.",
        overview="The chapter studies what happens when a fiber travels around a singular value. The notebook represents local systems by matrices, draws loops around critical values, and checks that the Picard-Lefschetz transformation preserves the intersection form.",
        concepts=("local system", "fundamental group representation", "monodromy action", "Picard-Lefschetz formula", "vanishing cycle", "Zariski theorem", "Noether-Lefschetz locus"),
        proof_moves=("translate parallel transport around loops into a representation", "write the vanishing-cycle transvection", "use irreducibility to constrain algebraic classes"),
        pitfalls=("forgetting loop orientation", "using the wrong sign convention for intersection pairing", "confusing fixed cycles with all Hodge cycles"),
        visual_kind="monodromy",
        visual_focus="Loops around critical values feed Picard-Lefschetz matrices acting on a two-dimensional symplectic lattice.",
        library_routes=("Matplotlib for loop and cycle diagrams", "NumPy for symplectic matrix checks", "NetworkX for orbit graphs"),
        checks=("Picard-Lefschetz matrix preserves the symplectic form", "monodromy orbit spans the toy vanishing lattice", "fixed subspace dimension is computed"),
        lab="Compose two monodromy loops and inspect the orbit of a test cohomology class.",
        hodge_numbers=diamond((1,), (2, 2), (2, 12, 2), (2, 2), (1,)),
    ),
    Chapter(
        id="v2-c04",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="The Topology of Algebraic Varieties",
        part_slug="part-01-topology-of-algebraic-varieties",
        number="4",
        title="The Leray Spectral Sequence",
        printed_start=98,
        printed_end=126,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-04-the-leray-spectral-sequence",
        notebook_slug="04-the-leray-spectral-sequence",
        sections=("Hypercohomology spectral sequence", "Composed functors", "Leray spectral sequence", "Cup product", "Relative Lefschetz decomposition", "Degeneration", "Invariant cycles"),
        goal="Use the Leray spectral sequence to read the cohomology of a total space from base, fiber, and monodromy data.",
        overview="Leray is the bookkeeping engine for morphisms. The notebook constructs a small E2 page, displays how base degree and fiber degree combine, and marks Deligne-style degeneration and invariant cycles as structural events.",
        concepts=("Leray spectral sequence", "higher direct image", "composed functor", "relative Lefschetz", "degeneration", "global invariant cycles", "mixed Hodge background"),
        proof_moves=("filter cochains by base degree", "identify E2 terms as base cohomology with local-system coefficients", "use relative Lefschetz to control differentials"),
        pitfalls=("forgetting local systems in the coefficients", "adding p and q incorrectly", "treating degeneration as automatic outside the theorem's setting"),
        visual_kind="spectral-sequence",
        visual_focus="A Leray E2 page shows base-degree and fiber-degree axes, with surviving boxes feeding the total cohomology.",
        library_routes=("Matplotlib for spectral-sequence grids", "NumPy for rank ledgers", "JSON checks for survivor counts"),
        checks=("toy Leray differential squares to zero", "E-infinity ranks add to total Betti numbers", "invariant-cycle subspace equals fixed monodromy classes"),
        lab="Turn on one monodromy action and observe how the invariant-cycle term changes on the E2 page.",
        hodge_numbers=diamond((1,), (1, 1), (2, 8, 2), (1, 1), (1,)),
    ),
    Chapter(
        id="v2-c05",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Variations of Hodge Structure",
        part_slug="part-02-variations-of-hodge-structure",
        number="5",
        title="Transversality and Applications",
        printed_start=129,
        printed_end=155,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-05-transversality-and-applications",
        notebook_slug="05-transversality-and-applications",
        sections=("de Rham complex of a flat bundle", "Transversality", "Complexes associated to IVHS", "Holomorphic Leray sequence", "Infinitesimal invariants", "Local study of Hodge loci"),
        goal="Expose Griffiths transversality as a complex whose cohomology controls Hodge-locus and infinitesimal-invariant questions.",
        overview="The chapter turns the horizontal condition into algebra. The notebook represents an infinitesimal variation by a block-lowering matrix, builds the associated complex, and interprets kernels as tangent constraints for Hodge loci.",
        concepts=("flat bundle", "infinitesimal variation of Hodge structure", "transversality", "Hodge locus", "infinitesimal invariant", "holomorphic Leray spectral sequence"),
        proof_moves=("turn the connection into a filtered complex", "read transversality as a one-step drop", "identify tangent spaces by annihilation conditions"),
        pitfalls=("allowing two-step filtration drops", "forgetting that Hodge loci are cut out analytically", "confusing infinitesimal invariants with global normal functions"),
        visual_kind="period-map",
        visual_focus="A block matrix and tangent slice show which derivatives are horizontal and which cut out the Hodge locus.",
        library_routes=("Matplotlib for block and tangent-space diagrams", "NumPy for block-zero checks", "NetworkX for complex maps"),
        checks=("forbidden derivative blocks vanish", "complex differential squares to zero", "toy Hodge-locus tangent dimension matches a kernel computation"),
        lab="Modify the IVHS matrix and watch the predicted Hodge-locus tangent space grow or shrink.",
        hodge_numbers=diamond((1,), (1, 1), (1, 4, 1), (1, 1), (1,)),
    ),
    Chapter(
        id="v2-c06",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Variations of Hodge Structure",
        part_slug="part-02-variations-of-hodge-structure",
        number="6",
        title="Hodge Filtration of Hypersurfaces",
        printed_start=156,
        printed_end=187,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-06-hodge-filtration-of-hypersurfaces",
        notebook_slug="06-hodge-filtration-of-hypersurfaces",
        sections=("Pole-order filtration", "Logarithmic complexes", "Hypersurfaces in projective space", "IVHS of hypersurfaces", "Macaulay theorem", "Symmetriser lemma", "Torelli application"),
        goal="Show how residues and pole order translate the Hodge filtration of a hypersurface into computable graded algebra.",
        overview="Hypersurfaces provide a concrete arena for Hodge filtrations. The notebook draws pole-order filtration levels and a small Jacobian-ring multiplication table, showing how IVHS becomes multiplication by deformation classes.",
        concepts=("pole-order filtration", "residue", "Jacobian ring", "hypersurface", "Macaulay theorem", "symmetriser lemma", "generic Torelli"),
        proof_moves=("compare logarithmic forms with residues", "identify Hodge pieces by pole order", "translate the infinitesimal period map into graded multiplication"),
        pitfalls=("treating pole order as the same as cohomological degree", "ignoring the Jacobian ideal", "using Torelli conclusions outside generic hypotheses"),
        visual_kind="filtration",
        visual_focus="Nested pole-order bands feed a Jacobian-ring multiplication grid for hypersurface IVHS.",
        library_routes=("Matplotlib for filtration ladders", "SymPy for small polynomial quotient checks", "NumPy for multiplication-rank ledgers"),
        checks=("filtration dimensions are nested", "toy Jacobian quotient has expected monomial basis", "multiplication map rank is recorded"),
        lab="Change the degree of a Fermat-type polynomial and compare the available residue monomials.",
        hodge_numbers=diamond((1,), (0, 0), (1, 19, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v2-c07",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Variations of Hodge Structure",
        part_slug="part-02-variations-of-hodge-structure",
        number="7",
        title="Normal Functions and Infinitesimal Invariants",
        printed_start=188,
        printed_end=214,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-07-normal-functions-and-infinitesimal-invariants",
        notebook_slug="07-normal-functions-and-infinitesimal-invariants",
        sections=("Jacobian fibration", "Normal functions", "Infinitesimal invariants", "Abel-Jacobi map", "High-degree hypersurfaces"),
        goal="Interpret normal functions as moving Abel-Jacobi classes and infinitesimal invariants as the derivative-level obstruction they carry.",
        overview="Normal functions turn a family of homologically trivial cycles into a section of intermediate Jacobians. The notebook draws such a section over a base and records where its derivative fails to be explained by a trivial cycle.",
        concepts=("Jacobian fibration", "normal function", "infinitesimal invariant", "Abel-Jacobi map", "higher-degree hypersurface", "symmetriser obstruction"),
        proof_moves=("build a torus fibration from a variation of Hodge structure", "lift a family of cycles to a normal function", "differentiate the section and project to an invariant"),
        pitfalls=("confusing a normal function with a scalar function", "forgetting the quotient by periods in every fiber", "declaring an invariant trivial without checking the relevant complex"),
        visual_kind="abel-jacobi",
        visual_focus="A moving torus quotient with a section path shows a normal function and its infinitesimal derivative.",
        library_routes=("Matplotlib for torus-fibration sections", "Plotly HTML for a moving section", "NumPy for quotient and derivative checks"),
        checks=("section values are reduced modulo each fiber lattice", "infinitesimal invariant vanishes for a toy constant section", "nonconstant section produces a nonzero projected derivative"),
        lab="Drag a section through a family of tori and compare constant, flat, and genuinely normal behavior.",
        hodge_numbers=diamond((1,), (3, 3), (2, 9, 2), (3, 3), (1,)),
    ),
    Chapter(
        id="v2-c08",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Variations of Hodge Structure",
        part_slug="part-02-variations-of-hodge-structure",
        number="8",
        title="Nori's Work",
        printed_start=215,
        printed_end=242,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-08-noris-work",
        notebook_slug="08-noris-work",
        sections=("Connectivity theorem", "Algebraic translation", "Hypersurfaces of projective space", "Algebraic equivalence", "Hodge class of a normal function", "Griffiths theorem", "Nori equivalence"),
        goal="Use connectivity and incidence geometry to explain why families of cycles can force strong equivalence results.",
        overview="Nori's results connect algebraic equivalence, normal functions, and connectivity of parameter spaces. The notebook uses an incidence graph to show when moving cycles through connected families collapses distinctions.",
        concepts=("connectivity theorem", "incidence correspondence", "algebraic equivalence", "normal function", "Hodge class", "Nori equivalence", "Nori theorem"),
        proof_moves=("translate geometric connectivity into algebraic control", "use incidence correspondences to propagate cycle relations", "compare equivalence relations through normal functions"),
        pitfalls=("assuming connectivity without the numerical hypotheses", "mixing rational and algebraic equivalence", "forgetting the role of parameter-space dimension"),
        visual_kind="connectivity",
        visual_focus="An incidence graph connects cycles, hypersurfaces, and parameter spaces to show how equivalence propagates.",
        library_routes=("NetworkX for incidence and connectivity graphs", "Matplotlib for graph rendering", "JSON checks for component counts"),
        checks=("incidence graph is connected under the model hypotheses", "dropping one hypothesis increases components", "equivalence classes merge exactly along connected paths"),
        lab="Remove incidence edges and identify which algebraic-equivalence conclusions no longer follow.",
        hodge_numbers=diamond((1,), (1, 1), (2, 7, 2), (1, 1), (1,)),
    ),
    Chapter(
        id="v2-c09",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Algebraic Cycles",
        part_slug="part-03-algebraic-cycles",
        number="9",
        title="Chow Groups",
        printed_start=245,
        printed_end=277,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-09-chow-groups",
        notebook_slug="09-chow-groups",
        sections=("Rational equivalence", "Proper and flat functoriality", "Localisation", "Intersection", "Correspondences", "Cycle classes", "Examples"),
        goal="Make Chow groups feel like computable cycle ledgers modulo rational equivalence, with functorial moves and intersections tracked explicitly.",
        overview="Chow groups refine homology by remembering algebraic movement. The notebook uses a rational-equivalence animation frame, a push-pull diagram, and an intersection ledger to show how cycles are added, moved, and compared.",
        concepts=("Chow group", "rational equivalence", "proper pushforward", "flat pullback", "localisation", "intersection product", "correspondence", "cycle class map"),
        proof_moves=("mod out cycles by divisors of rational functions", "track functoriality through proper and flat maps", "use correspondences as cycle-theoretic operators"),
        pitfalls=("confusing rational equivalence with homological equivalence", "using pullback without flatness or refined hypotheses", "forgetting dimensions in intersection products"),
        visual_kind="cycle-correspondence",
        visual_focus="A cycle ledger and push-pull square display rational equivalence, functoriality, and intersection products.",
        library_routes=("Matplotlib for ledger and square diagrams", "NetworkX for correspondence composition", "NumPy for intersection matrices"),
        checks=("intersection matrix is symmetric in the smooth toy model", "push-pull dimensions match", "cycle-class map sends rationally equivalent cycles to the same class"),
        lab="Move a divisor on a toy curve by a rational function and watch the Chow class remain fixed.",
        hodge_numbers=diamond((1,), (2, 2), (3, 9, 3), (2, 2), (1,)),
    ),
    Chapter(
        id="v2-c10",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Algebraic Cycles",
        part_slug="part-03-algebraic-cycles",
        number="10",
        title="Mumford's Theorem and its Generalisations",
        printed_start=278,
        printed_end=306,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-10-mumfords-theorem-and-its-generalisations",
        notebook_slug="10-mumfords-theorem-and-its-generalisations",
        sections=("Representable CH0", "Roitman theorem", "Mumford theorem", "Bloch-Srinivas construction", "Decomposition of the diagonal", "Generalised decomposition"),
        goal="Explain how decomposition of the diagonal turns CH0 representability questions into cohomological consequences.",
        overview="The chapter studies when zero-cycles can be represented by simpler geometric data. The notebook draws the diagonal as a correspondence and decomposes it into supported pieces, making the Bloch-Srinivas argument a visible operator identity.",
        concepts=("CH0", "representability", "Roitman theorem", "Mumford theorem", "Bloch-Srinivas construction", "decomposition of the diagonal", "supported correspondence"),
        proof_moves=("turn a statement about zero-cycles into an identity of correspondences", "decompose the diagonal into pieces with controlled support", "read support restrictions as annihilation on Hodge pieces"),
        pitfalls=("forgetting the diagonal is an operator on cohomology", "assuming representability for all varieties", "losing support conditions in the decomposition"),
        visual_kind="diagonal-decomposition",
        visual_focus="A diagonal correspondence splits into supported components whose action on a Hodge ledger is checked.",
        library_routes=("Matplotlib for diagonal decomposition diagrams", "NumPy for idempotent and support matrix checks", "NetworkX for correspondence action graph"),
        checks=("toy diagonal matrix decomposes as supported pieces", "sum of supported correspondences acts as identity on allowed classes", "forbidden Hodge piece is annihilated"),
        lab="Alter a support component and inspect whether the diagonal identity still holds.",
        hodge_numbers=diamond((1,), (0, 0), (1, 2, 1), (0, 0), (1,)),
    ),
    Chapter(
        id="v2-c11",
        volume=2,
        volume_slug="volume-02-applications",
        volume_title="Volume II: Topology, variations, and algebraic cycles",
        part="Algebraic Cycles",
        part_slug="part-03-algebraic-cycles",
        number="11",
        title="The Bloch Conjecture and its Generalisations",
        printed_start=307,
        printed_end=342,
        pdf_file=VOLUME_PDFS[2],
        folder_slug="chapter-11-the-bloch-conjecture-and-its-generalisations",
        notebook_slug="11-the-bloch-conjecture-and-its-generalisations",
        sections=("Surfaces with pg=0", "Classification", "Godeaux surfaces", "Filtrations on Chow groups", "Generalised Bloch conjecture", "Saito filtration", "Abelian varieties", "Pontryagin product", "Fourier transform", "Beauville results"),
        goal="Present Bloch-type conjectures as a filtration story linking geometric genus, Chow groups, and Fourier operations on abelian varieties.",
        overview="The final chapter gathers conjectural and proven structures around Chow groups. The notebook builds a filtration tower for Chow groups, marks the pg=0 surface prediction, and uses a toy finite Fourier transform to model Beauville-style decompositions on abelian varieties.",
        concepts=("Bloch conjecture", "geometric genus", "Godeaux surface", "Chow filtration", "generalised Bloch conjecture", "Saito filtration", "abelian variety", "Pontryagin product", "Fourier transform", "Beauville decomposition"),
        proof_moves=("relate vanishing Hodge pieces to expected Chow simplification", "organize cycle groups by conjectural filtrations", "diagonalize operations on abelian varieties using Fourier transform"),
        pitfalls=("treating conjectural filtrations as established in all cases", "confusing Pontryagin and intersection products", "reading pg=0 as the only hypothesis in surface classification"),
        visual_kind="chow-filtration",
        visual_focus="A Chow filtration tower and a finite Fourier transform grid show how cycle operations split into graded pieces.",
        library_routes=("Matplotlib for filtration towers", "NumPy for finite Fourier matrix checks", "JSON ledgers for product compatibility"),
        checks=("finite Fourier matrix is unitary after normalization", "Pontryagin convolution diagonalizes under Fourier transform", "filtration dimensions decrease"),
        lab="Convolve two toy cycle vectors on a finite abelian group and compare before and after Fourier transform.",
        hodge_numbers=diamond((1,), (0, 0), (0, 6, 0), (0, 0), (1,)),
    ),
)


CHAPTER_BY_ID = {chapter.id: chapter for chapter in CHAPTERS}


def get_chapter(chapter_id: str) -> Chapter:
    try:
        return CHAPTER_BY_ID[chapter_id]
    except KeyError as exc:
        known = ", ".join(CHAPTER_BY_ID)
        raise KeyError(f"unknown chapter id {chapter_id!r}; known ids: {known}") from exc


def chapters_for_volume(volume: int) -> tuple[Chapter, ...]:
    return tuple(chapter for chapter in CHAPTERS if chapter.volume == volume)


def chapters_for_part(volume: int, part_slug: str) -> tuple[Chapter, ...]:
    return tuple(
        chapter
        for chapter in CHAPTERS
        if chapter.volume == volume and chapter.part_slug == part_slug
    )


def source_map_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for chapter in CHAPTERS:
        rows.append(
            {
                "id": chapter.id,
                "volume": chapter.volume,
                "volume_title": chapter.volume_title,
                "part": chapter.part,
                "chapter": chapter.number,
                "title": chapter.title,
                "printed_start": chapter.printed_start,
                "printed_end": chapter.printed_end,
                "pdf_start": chapter.pdf_start,
                "pdf_end": chapter.pdf_end,
                "pdf_file": chapter.pdf_file,
                "notebook": chapter.notebook_path.as_posix(),
                "artifact_key": chapter.artifact_key,
                "sections": list(chapter.sections),
                "concepts": list(chapter.concepts),
            }
        )
    return rows


def chapter_to_dict(chapter: Chapter) -> dict[str, Any]:
    data = asdict(chapter)
    data["pdf_start"] = chapter.pdf_start
    data["pdf_end"] = chapter.pdf_end
    data["source_span"] = chapter.source_span
    data["notebook_path"] = chapter.notebook_path.as_posix()
    data["artifact_key"] = chapter.artifact_key
    return data


def course_root_from(path: Path | None = None) -> Path:
    start = (path or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if (candidate / "Hodge Theory and Complex Algebraic Geometry I.pdf").exists():
            return candidate
    raise RuntimeError("Could not locate Hodge course root from current path")

