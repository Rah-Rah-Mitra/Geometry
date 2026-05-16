"""Structured source map and chapter-specific teaching metadata."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

BOOK_TITLE = "Introduction to Symplectic Topology"
PDF_FILENAME = "Introduction to Symplectic Topology Third Edition.pdf"
PRINTED_TO_PDF_OFFSET = 13
BOOK_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Unit:
    label: str
    slug: str
    filename: str
    part_slug: str
    part_title: str
    printed_start: int
    printed_end: int
    sections: tuple[str, ...]
    goal: str
    focus: str
    translation: tuple[str, ...]
    route: tuple[str, ...]
    lab: str
    visual_slug: str
    visual_concept: str
    visual_representation: str
    inspection_target: str
    invariant: str
    keywords: tuple[str, ...]

    @property
    def pdf_start(self) -> int:
        return self.printed_start + PRINTED_TO_PDF_OFFSET

    @property
    def pdf_end(self) -> int:
        return self.printed_end + PRINTED_TO_PDF_OFFSET

    @property
    def printed_span(self) -> str:
        return f"{self.printed_start}-{self.printed_end}"

    @property
    def pdf_span(self) -> str:
        return f"{self.pdf_start}-{self.pdf_end}"

    @property
    def notebook_relpath(self) -> str:
        return f"{self.part_slug}/{self.slug}/{self.filename}"

    @property
    def index_relpath(self) -> str:
        return f"{self.part_slug}/{self.slug}/00-index.ipynb"

    def to_dict(self) -> dict[str, object]:
        return {
            "label": self.label,
            "slug": self.slug,
            "filename": self.filename,
            "part_slug": self.part_slug,
            "part_title": self.part_title,
            "printed_pages": self.printed_span,
            "pdf_pages": self.pdf_span,
            "sections": list(self.sections),
            "goal": self.goal,
            "focus": self.focus,
            "translation": list(self.translation),
            "route": list(self.route),
            "lab": self.lab,
            "visual_slug": self.visual_slug,
            "visual_concept": self.visual_concept,
            "visual_representation": self.visual_representation,
            "inspection_target": self.inspection_target,
            "invariant": self.invariant,
            "keywords": list(self.keywords),
            "notebook": self.notebook_relpath,
            "index": self.index_relpath,
        }


COURSE_UNITS: tuple[Unit, ...] = (
    Unit(
        label="Introduction",
        slug="introduction",
        filename="introduction.ipynb",
        part_slug="part-00-introduction",
        part_title="Orientation",
        printed_start=1,
        printed_end=8,
        sections=("local-to-global transition", "Darboux and Moser", "Hamiltonian flows", "global rigidity questions"),
        goal="See why symplectic topology has local normal forms but global invariants.",
        focus="The introduction frames symplectic topology as a subject born from mechanics and sharpened by global rigidity, fixed point, and embedding phenomena.",
        translation=(
            "A symplectic form becomes a matrix that pairs displacements into signed area.",
            "Darboux removes local invariants; the course therefore searches for global obstructions.",
            "The main questions become executable checks: flow conservation, nonsqueezing, fixed points, and deformation classes.",
        ),
        route=(
            "Start from Hamiltonian motion and the closed nondegenerate 2-form.",
            "Compare local flexibility with global rigidity.",
            "Organize later chapters by the invariants they add.",
        ),
        lab="Edit the dependency graph by adding one favorite invariant and ask which earlier constructions it depends on.",
        visual_slug="roadmap",
        visual_concept="global symplectic question map",
        visual_representation="directed dependency graph",
        inspection_target="which later invariants depend on Hamiltonian flow, Darboux charts, moment maps, or variational methods",
        invariant="the graph must contain the four recurring pillars: form, flow, moment map, and capacity",
        keywords=("Darboux", "Moser", "Hamiltonian", "nonsqueezing", "Arnold conjecture"),
    ),
    Unit(
        label="Chapter 1",
        slug="chapter-01-from-classical-to-modern",
        filename="01-from-classical-to-modern.ipynb",
        part_slug="part-01-foundations",
        part_title="Foundations",
        printed_start=11,
        printed_end=36,
        sections=("1.1 Hamiltonian mechanics", "1.2 The symplectic topology of Euclidean space"),
        goal="Derive Hamiltonian motion from action and see the symplectic form preserve phase area.",
        focus="The chapter moves from variational mechanics to Hamiltonian vector fields, symplectomorphisms, Poisson brackets, and the first global problems.",
        translation=(
            "A Hamiltonian function is an energy landscape on phase space.",
            "The standard symplectic matrix turns the gradient of energy into the vector field of motion.",
            "Area preservation and fixed energy are numerical shadows of the symplectic equation.",
        ),
        route=(
            "Legendre transform second-order Euler-Lagrange equations into first-order Hamilton equations.",
            "Use the standard form to compute vector fields and symplectic matrices.",
            "Test why global questions begin even in Euclidean space.",
        ),
        lab="Change the oscillator frequencies in the code and compare energy drift with symplectic area drift.",
        visual_slug="hamiltonian-flow",
        visual_concept="Hamiltonian flow on phase space",
        visual_representation="phase portrait with energy contours and transported area cell",
        inspection_target="the orbit follows a level set while a small phase-space cell keeps its signed symplectic area",
        invariant="energy drift and symplectic area drift stay within numerical tolerance",
        keywords=("Legendre transform", "Hamiltonian mechanics", "symplectic action", "Poisson bracket", "nonsqueezing"),
    ),
    Unit(
        label="Chapter 2",
        slug="chapter-02-linear-symplectic-geometry",
        filename="02-linear-symplectic-geometry.ipynb",
        part_slug="part-01-foundations",
        part_title="Foundations",
        printed_start=37,
        printed_end=93,
        sections=("2.1 Symplectic vector spaces", "2.2 The symplectic linear group", "2.3 Lagrangian subspaces", "2.4 Affine nonsqueezing", "2.5 Linear complex structures", "2.6 Bundles", "2.7 First Chern class"),
        goal="Recognize the linear algebra that every Darboux chart carries.",
        focus="The chapter builds the standard matrix model, symplectic linear group, Lagrangian planes, compatible complex structures, bundles, and first Chern class.",
        translation=(
            "The symplectic form is an invertible skew matrix.",
            "A linear map is symplectic when it preserves that matrix by transpose-conjugation.",
            "A Lagrangian subspace is a maximal place where the form vanishes.",
        ),
        route=(
            "Compute the standard form and test matrices against it.",
            "Watch Lagrangian planes rotate through the Grassmannian in dimension two.",
            "Connect compatible complex structures to the positive metric built from omega and J.",
        ),
        lab="Perturb the shear matrix and see exactly when the symplectic residual stops vanishing.",
        visual_slug="linear-form",
        visual_concept="linear symplectic form and Lagrangian planes",
        visual_representation="matrix residual heatmap plus rotating plane diagram",
        inspection_target="which matrix entries break the identity A^T J A = J and when omega vanishes on a plane",
        invariant="symplectic residual is zero for the chosen shear and omega(v,w)=0 on each plotted Lagrangian line",
        keywords=("symplectic vector space", "symplectic group", "Lagrangian subspace", "complex structure", "Chern class"),
    ),
    Unit(
        label="Chapter 3",
        slug="chapter-03-symplectic-manifolds",
        filename="03-symplectic-manifolds.ipynb",
        part_slug="part-01-foundations",
        part_title="Foundations",
        printed_start=94,
        printed_end=151,
        sections=("3.1 Basic concepts", "3.2 Moser isotopy and Darboux", "3.3 Isotopy extension", "3.4 Submanifolds", "3.5 Contact structures"),
        goal="Translate the linear form into manifold language and track what Moser and Darboux actually preserve.",
        focus="The chapter defines symplectic manifolds, proves normal-form principles, organizes submanifolds, and introduces contact structures.",
        translation=(
            "Closedness is a differential equation; nondegeneracy is a pointwise determinant condition.",
            "Moser isotopy is a controlled deformation between cohomologous forms.",
            "Contact structures appear as odd-dimensional boundary data for symplectic geometry.",
        ),
        route=(
            "Sample an interpolating family of two-forms and watch nondegeneracy.",
            "Use submanifold labels to separate symplectic, isotropic, coisotropic, and Lagrangian cases.",
            "Check a contact form by computing alpha wedge d alpha in coordinates.",
        ),
        lab="Move the interpolation parameter and look for the first place the determinant would vanish.",
        visual_slug="moser-contact",
        visual_concept="Moser deformation and contact boundary",
        visual_representation="nondegeneracy tracker with contact-plane sketch",
        inspection_target="how a family of forms stays symplectic while contact planes twist on a boundary slice",
        invariant="determinant of the interpolated form remains positive and alpha wedge d alpha is nonzero",
        keywords=("Darboux theorem", "Moser isotopy", "submanifold", "contact structure", "isotopy extension"),
    ),
    Unit(
        label="Chapter 4",
        slug="chapter-04-almost-complex-structures",
        filename="04-almost-complex-structures.ipynb",
        part_slug="part-01-foundations",
        part_title="Foundations",
        printed_start=152,
        printed_end=190,
        sections=("4.1 Almost complex structures", "4.2 Integrability", "4.3 Kahler manifolds", "4.4 Kahler surfaces", "4.5 J-holomorphic curves"),
        goal="Use compatible almost complex structures as a bridge from symplectic forms to complex and holomorphic geometry.",
        focus="The chapter explains almost complex structures, integrability, Kahler examples, surfaces, and the first J-holomorphic curve viewpoint.",
        translation=(
            "A compatible J rotates tangent vectors and turns omega into a positive metric.",
            "Integrability is an extra condition, not automatic from J squared equals minus identity.",
            "J-holomorphic curves can be tested by a Cauchy-Riemann residual.",
        ),
        route=(
            "Verify J^2=-I and positivity of omega(.,J.).",
            "Visualize holomorphic and non-holomorphic trial maps from a disk.",
            "Read the residual as the computational form of the curve equation.",
        ),
        lab="Change the anti-holomorphic coefficient and watch the residual heatmap brighten.",
        visual_slug="almost-complex",
        visual_concept="compatible J and holomorphic residual",
        visual_representation="disk map comparison and residual heatmap",
        inspection_target="where the Cauchy-Riemann residual vanishes and where compatibility produces a positive metric",
        invariant="J squared equals minus identity and the holomorphic residual is smaller than the perturbed residual",
        keywords=("almost complex structure", "integrability", "Kahler", "J-holomorphic curve", "compatibility"),
    ),
    Unit(
        label="Chapter 5",
        slug="chapter-05-symplectic-group-actions",
        filename="05-symplectic-group-actions.ipynb",
        part_slug="part-02-symplectic-manifolds",
        part_title="Symplectic Manifolds",
        printed_start=191,
        printed_end=251,
        sections=("5.1 Circle actions", "5.2 Moment maps", "5.3 Examples", "5.4 Symplectic quotients", "5.5 Convexity", "5.6 Localization", "5.7 GIT"),
        goal="Make moment maps visible as conserved quantities and convex images of group actions.",
        focus="The chapter studies symplectic group actions, moment maps, quotients, convexity, localization, and links to geometric invariant theory.",
        translation=(
            "A moment map packages infinitesimal action data into Hamiltonian functions.",
            "For torus actions on complex coordinates, the moment image is a polytope.",
            "Reduction cuts a level set and divides by the group action.",
        ),
        route=(
            "Compute the standard torus moment map on C^2.",
            "Plot the moment image and mark reduced levels.",
            "Use a finite localization graph to remember fixed components and weights.",
        ),
        lab="Slide the reduction level and predict the dimension and residual circle before reading the check output.",
        visual_slug="moment-map",
        visual_concept="moment map and symplectic reduction",
        visual_representation="moment polytope with level-set fibers",
        inspection_target="how points in C^2 collapse to moment-map coordinates and why convexity is visible",
        invariant="moment coordinates are nonnegative and the selected reduction level has constant radius squared",
        keywords=("circle action", "moment map", "symplectic quotient", "convexity", "localization", "GIT"),
    ),
    Unit(
        label="Chapter 6",
        slug="chapter-06-symplectic-fibrations",
        filename="06-symplectic-fibrations.ipynb",
        part_slug="part-02-symplectic-manifolds",
        part_title="Symplectic Manifolds",
        printed_start=252,
        printed_end=288,
        sections=("6.1 Symplectic fibrations", "6.2 2-sphere bundles", "6.3 Connections", "6.4 Hamiltonian holonomy and coupling form", "6.5 Hamiltonian fibrations"),
        goal="See a symplectic fibration as fibers plus a connection whose holonomy remembers Hamiltonian data.",
        focus="The chapter develops symplectic fibrations, symplectic connections, Hamiltonian holonomy, coupling forms, and Hamiltonian fibrations.",
        translation=(
            "A fibration separates base motion from fiber geometry.",
            "A connection chooses horizontal lifts; curvature measures failure to close.",
            "Hamiltonian holonomy rotates fibers by a symplectic transformation controlled by the coupling form.",
        ),
        route=(
            "Draw a base loop and a fiber coordinate carried around it.",
            "Measure the holonomy angle as curvature times enclosed area.",
            "Relate the check to the coupling-form normalization.",
        ),
        lab="Increase the curvature parameter and compare the predicted and measured holonomy angles.",
        visual_slug="fibration-holonomy",
        visual_concept="symplectic fibration holonomy",
        visual_representation="base loop with transported fiber phase and curvature table",
        inspection_target="the fiber returns rotated by the integrated curvature over the base disk",
        invariant="computed holonomy angle equals curvature times enclosed base area modulo 2 pi",
        keywords=("symplectic fibration", "connection", "holonomy", "coupling form", "Hamiltonian fibration"),
    ),
    Unit(
        label="Chapter 7",
        slug="chapter-07-constructing-symplectic-manifolds",
        filename="07-constructing-symplectic-manifolds.ipynb",
        part_slug="part-02-symplectic-manifolds",
        part_title="Symplectic Manifolds",
        printed_start=289,
        printed_end=340,
        sections=("7.1 Blowing up and down", "7.2 Connected sums", "7.3 Telescope construction", "7.4 Donaldson submanifolds"),
        goal="Track how new symplectic manifolds are made by cutting, gluing, and controlled hypersurfaces.",
        focus="The chapter constructs symplectic manifolds through blow-ups, connected sums, telescope constructions, and Donaldson submanifolds.",
        translation=(
            "A blow-up replaces a point by an exceptional direction and removes a corner from a moment polytope.",
            "Connected sums and fiber sums glue along compatible symplectic pieces.",
            "Donaldson hypersurfaces trade high tensor powers for controlled symplectic submanifolds.",
        ),
        route=(
            "Visualize a blow-up as a clipped moment polytope.",
            "Compare the lost area with the blow-up size.",
            "Use a construction dependency graph to keep the cut-and-paste operations distinct.",
        ),
        lab="Change the blow-up size and confirm the exceptional edge length and area loss.",
        visual_slug="blow-up",
        visual_concept="symplectic blow-up and construction graph",
        visual_representation="clipped moment polytope with dependency diagram",
        inspection_target="the exceptional edge records the size of the blow-up while the rest of the polytope remains toric",
        invariant="area loss equals one half times the square of the clipping size",
        keywords=("blow-up", "connected sum", "telescope", "Donaldson submanifold", "Lefschetz fibration"),
    ),
    Unit(
        label="Chapter 8",
        slug="chapter-08-area-preserving-diffeomorphisms",
        filename="08-area-preserving-diffeomorphisms.ipynb",
        part_slug="part-03-symplectomorphisms",
        part_title="Symplectomorphisms",
        printed_start=341,
        printed_end=355,
        sections=("8.1 Periodic orbits", "8.2 Poincare-Birkhoff theorem", "8.3 Billiard problem"),
        goal="Use annulus twist maps as a laboratory for area preservation and forced fixed points.",
        focus="The chapter treats periodic orbits, the Poincare-Birkhoff theorem, and billiards as concrete two-dimensional symplectic dynamics.",
        translation=(
            "An area-preserving annulus map is a two-dimensional symplectomorphism.",
            "A twist condition makes the two boundary circles rotate in different ways.",
            "Fixed-point forcing becomes visible by plotting angular displacement.",
        ),
        route=(
            "Build a monotone twist map on the annulus.",
            "Plot images of radial lines and the displacement zero set.",
            "Check that the Jacobian determinant is one.",
        ),
        lab="Reverse the twist on one boundary and watch how the zero-displacement crossings change.",
        visual_slug="twist-map",
        visual_concept="area-preserving twist map",
        visual_representation="annulus map with displacement graph",
        inspection_target="where positive and negative boundary twists force crossings of the fixed-point equation",
        invariant="the twist map has determinant one and displacement changes sign across the annulus",
        keywords=("area-preserving diffeomorphism", "periodic orbit", "Poincare-Birkhoff", "twist map", "billiard"),
    ),
    Unit(
        label="Chapter 9",
        slug="chapter-09-generating-functions",
        filename="09-generating-functions.ipynb",
        part_slug="part-03-symplectomorphisms",
        part_title="Symplectomorphisms",
        printed_start=356,
        printed_end=384,
        sections=("9.1 Generating functions and symplectic action", "9.2 Discrete Hamiltonian mechanics", "9.3 Hamiltonian symplectomorphisms", "9.4 Lagrangian submanifolds"),
        goal="Read a symplectic map through a scalar generating function and its variational critical points.",
        focus="The chapter connects generating functions, symplectic action, discrete Hamiltonian mechanics, Hamiltonian symplectomorphisms, and Lagrangian graphs.",
        translation=(
            "A generating function stores a Lagrangian graph as derivatives of one scalar function.",
            "Discrete Hamiltonian mechanics turns paths into finite-dimensional action sums.",
            "Critical points of the action are the computed orbits.",
        ),
        route=(
            "Plot a generating function landscape.",
            "Mark stationary points and compare them with the discrete Euler equation.",
            "Connect the Hessian sign to Morse-style data used later.",
        ),
        lab="Change the coupling parameter and count how many stationary points survive.",
        visual_slug="generating-function",
        visual_concept="generating function and discrete action",
        visual_representation="action landscape with critical-point residuals",
        inspection_target="where the gradient vanishes and how those points encode a symplectic correspondence",
        invariant="gradient norm at marked critical points is below tolerance",
        keywords=("generating function", "symplectic action", "discrete Hamiltonian mechanics", "Hamiltonian symplectomorphism", "Lagrangian graph"),
    ),
    Unit(
        label="Chapter 10",
        slug="chapter-10-group-of-symplectomorphisms",
        filename="10-group-of-symplectomorphisms.ipynb",
        part_slug="part-03-symplectomorphisms",
        part_title="Symplectomorphisms",
        printed_start=385,
        printed_end=416,
        sections=("10.1 Basic properties", "10.2 Flux homomorphism", "10.3 Calabi homomorphism", "10.4 Topology of symplectomorphism groups"),
        goal="Separate symplectic, Hamiltonian, flux, and Calabi information in families of maps.",
        focus="The chapter studies the symplectomorphism group, Hamiltonian subgroup, flux homomorphism, Calabi homomorphism, and topology of these groups.",
        translation=(
            "A path of symplectomorphisms sweeps area through cycles.",
            "Flux records that swept cohomology class.",
            "Calabi integrates compactly supported Hamiltonians into a homomorphism in exact settings.",
        ),
        route=(
            "Represent torus translations and Hamiltonian shears.",
            "Compute flux vectors and compare exact versus non-exact isotopies.",
            "Use a subgroup diagram to track inclusions and invariants.",
        ),
        lab="Set the translation vector to zero and check that the remaining shear has zero flux.",
        visual_slug="flux-calabi",
        visual_concept="flux and subgroup structure",
        visual_representation="torus strip sweep with subgroup diagram",
        inspection_target="which isotopies sweep nonzero area through the fundamental cycles",
        invariant="translation flux equals the swept vector while the Hamiltonian shear has zero average flux",
        keywords=("symplectomorphism group", "Hamiltonian group", "flux homomorphism", "Calabi homomorphism", "topology"),
    ),
    Unit(
        label="Chapter 11",
        slug="chapter-11-arnold-conjecture",
        filename="11-arnold-conjecture.ipynb",
        part_slug="part-04-symplectic-invariants",
        part_title="Symplectic Invariants",
        printed_start=417,
        printed_end=456,
        sections=("11.1 Symplectic fixed points", "11.2 Morse theory and Conley index", "11.3 Lagrangian intersections", "11.4 Floer homology"),
        goal="Connect Hamiltonian fixed points with Morse/Floer-style lower bounds.",
        focus="The chapter develops the Arnold conjecture, fixed points, Morse and Conley tools, Lagrangian intersections, and a first Floer homology overview.",
        translation=(
            "Fixed points of a Hamiltonian map become critical points of an action functional.",
            "Morse inequalities supply the finite-dimensional counting model.",
            "Floer homology upgrades the count when the space of paths is infinite-dimensional.",
        ),
        route=(
            "Plot a torus Morse function whose critical points model the lower-bound idea.",
            "Count critical points by index and compare with Betti numbers.",
            "Use a small boundary graph to preview Floer differential constraints.",
        ),
        lab="Change the perturbation and verify that the critical count does not fall below the torus Betti sum.",
        visual_slug="arnold-fixed-points",
        visual_concept="Arnold fixed-point lower bound",
        visual_representation="torus Morse landscape with critical points and chain graph",
        inspection_target="how minima, saddles, and maxima provide a finite-dimensional shadow of Hamiltonian fixed points",
        invariant="critical point count is at least the sum of Betti numbers of the torus",
        keywords=("Arnold conjecture", "fixed point", "Morse theory", "Conley index", "Lagrangian intersection", "Floer homology"),
    ),
    Unit(
        label="Chapter 12",
        slug="chapter-12-symplectic-capacities",
        filename="12-symplectic-capacities.ipynb",
        part_slug="part-04-symplectic-invariants",
        part_title="Symplectic Invariants",
        printed_start=457,
        printed_end=502,
        sections=("12.1 Nonsqueezing and capacities", "12.2 Rigidity", "12.3 Hofer metric", "12.4 Hofer-Zehnder capacity", "12.5 Variational argument"),
        goal="Use capacities as numerical obstructions to symplectic embeddings.",
        focus="The chapter treats nonsqueezing, rigidity, Hofer geometry, Hofer-Zehnder capacity, and a variational proof of capacities.",
        translation=(
            "A capacity is a monotone, conformal measurement with a fixed normalization on balls and cylinders.",
            "Nonsqueezing says the smallest symplectic shadow can obstruct an embedding even when volume allows it.",
            "Hofer length and variational loops give dynamic ways to detect the same rigidity.",
        ),
        route=(
            "Compare ball and cylinder capacities against volume intuition.",
            "Draw an attempted embedding that fails by radius, not by volume.",
            "Compute a toy variational action curve and record capacity axioms.",
        ),
        lab="Scale every radius and check that capacity scales quadratically while volume scales by the full dimension.",
        visual_slug="capacity-variational",
        visual_concept="capacity and variational obstruction",
        visual_representation="nonsqueezing diagram with capacity bar chart and action curve",
        inspection_target="where volume comparison is too weak and the capacity inequality catches the obstruction",
        invariant="capacity is monotone and conformal; the selected ball cannot squeeze into the smaller cylinder",
        keywords=("symplectic capacity", "nonsqueezing", "rigidity", "Hofer metric", "Hofer-Zehnder", "variational argument"),
    ),
    Unit(
        label="Chapter 13",
        slug="chapter-13-existence-and-uniqueness",
        filename="13-existence-and-uniqueness.ipynb",
        part_slug="part-04-symplectic-invariants",
        part_title="Symplectic Invariants",
        printed_start=503,
        printed_end=548,
        sections=("13.1 Existence and uniqueness", "13.2 Examples", "13.3 Taubes-Seiberg-Witten theory", "13.4 Symplectic four-manifolds"),
        goal="Organize existence and uniqueness questions by the invariants that survive deformation.",
        focus="The chapter surveys symplectic existence and uniqueness, examples, Taubes-Seiberg-Witten theory, and symplectic four-manifolds.",
        translation=(
            "Existence asks whether a closed nondegenerate two-form can live in a topological class.",
            "Uniqueness asks how many deformation or isotopy classes remain after cohomology is fixed.",
            "Four-dimensional invariants bring gauge-theoretic information into symplectic topology.",
        ),
        route=(
            "Compare model cohomology cones and obstruction labels.",
            "Use a dependency diagram to separate constructive examples from classification tools.",
            "Check a toy intersection form for a positive symplectic square.",
        ),
        lab="Move the candidate cohomology class and watch when the positive-square condition fails.",
        visual_slug="existence-uniqueness",
        visual_concept="existence and uniqueness invariant atlas",
        visual_representation="cohomology cone sketch with invariant dependency graph",
        inspection_target="which data are topological, which are symplectic, and which enter through four-dimensional gauge theory",
        invariant="candidate symplectic class has positive square in the toy intersection form",
        keywords=("existence", "uniqueness", "Seiberg-Witten", "symplectic four-manifold", "deformation"),
    ),
    Unit(
        label="Chapter 14",
        slug="chapter-14-open-problems",
        filename="14-open-problems.ipynb",
        part_slug="part-04-symplectic-invariants",
        part_title="Symplectic Invariants",
        printed_start=549,
        printed_end=573,
        sections=("14.1 Structures", "14.2 Symplectomorphisms", "14.3 Lagrangians and cotangent bundles", "14.4 Fano manifolds", "14.5 Donaldson hypersurfaces", "14.6 Contact geometry", "14.7 Continuous symplectic topology", "14.8 Embeddings", "14.9 Euclidean space"),
        goal="Turn open problems into a navigable map of methods, objects, and obstructions.",
        focus="The chapter lists open questions across structures, symplectomorphisms, Lagrangians, Fano manifolds, Donaldson hypersurfaces, contact geometry, continuous symplectic topology, embeddings, and Euclidean space.",
        translation=(
            "An open problem can be studied by naming its objects, known invariants, and missing implication.",
            "Problem clusters reveal which earlier chapters supply the language.",
            "Visual dependency maps help separate computational experiments from research-level theorems.",
        ),
        route=(
            "Classify each problem cluster by object type and method.",
            "Link clusters to capacities, Floer theory, contact boundaries, and construction tools.",
            "Record modest computational experiments that are honest toy models, not solutions.",
        ),
        lab="Pick one node and list the minimal earlier notebook path needed to understand its vocabulary.",
        visual_slug="open-problem-atlas",
        visual_concept="open-problem dependency atlas",
        visual_representation="clustered graph of problem families and prerequisite invariants",
        inspection_target="which problems are driven by embeddings, Lagrangians, contact geometry, or four-dimensional invariants",
        invariant="each problem cluster is connected to at least one earlier method node",
        keywords=("open problem", "embedding", "Lagrangian", "contact geometry", "Fano", "continuous symplectic topology"),
    ),
    Unit(
        label="Appendix A",
        slug="appendix-a-smooth-maps",
        filename="appendix-a-smooth-maps.ipynb",
        part_slug="appendix-a-smooth-maps",
        part_title="Appendix A",
        printed_start=574,
        printed_end=582,
        sections=("A.1 Smooth functions on manifolds with corners", "A.2 Extension", "A.3 Smooth-function construction"),
        goal="Build the smoothing and extension tools that support isotopy and gluing arguments.",
        focus="The appendix supplies smooth maps on manifolds with corners, extension lemmas, and a concrete smooth-function construction.",
        translation=(
            "A corner is a coordinate model that needs compatible smoothness from several boundary faces.",
            "Extension replaces local boundary data by a global smooth function.",
            "Bump functions give executable checks for support, flatness, and interpolation.",
        ),
        route=(
            "Plot a smooth step function and its derivatives.",
            "Use a product bump to extend data from a face into a quadrant.",
            "Check endpoint flatness and support numerically.",
        ),
        lab="Change the collar width and verify that flatness at the boundary is preserved.",
        visual_slug="smooth-extension",
        visual_concept="smooth extension near corners",
        visual_representation="bump and collar-extension plots",
        inspection_target="where the function is flat at the boundary but still interpolates through the collar",
        invariant="endpoint derivatives vanish numerically and the bump remains supported inside the chosen collar",
        keywords=("smooth map", "manifold with corners", "extension", "bump function", "isotopy"),
    ),
)


PARTS: tuple[dict[str, str], ...] = tuple(
    {"slug": slug, "title": title}
    for slug, title in dict((unit.part_slug, unit.part_title) for unit in COURSE_UNITS).items()
)


def unit_by_slug(slug: str) -> Unit:
    for unit in COURSE_UNITS:
        if unit.slug == slug:
            return unit
    raise KeyError(slug)


def units_by_part(part_slug: str) -> list[Unit]:
    return [unit for unit in COURSE_UNITS if unit.part_slug == part_slug]


def source_map_payload() -> dict[str, object]:
    return {
        "book_title": BOOK_TITLE,
        "source_pdf": PDF_FILENAME,
        "printed_to_pdf_offset": PRINTED_TO_PDF_OFFSET,
        "copyright_policy": "Original course prose only; no textbook prose, screenshots, page crops, or long exercise text.",
        "units": [unit.to_dict() for unit in COURSE_UNITS],
    }
