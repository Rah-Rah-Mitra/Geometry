"""Source inventory for the Optimal Transport, Old and New course."""

from __future__ import annotations

from pathlib import Path

BOOK_ROOT = Path(__file__).resolve().parents[1]
PDF_NAME = "Optimal Transport Old and New.pdf"
PDF_PAGES = 997
MAIN_TEXT_PDF_OFFSET = 22


PARTS = [
    {
        "folder": "part-00-orientation-and-foundations",
        "title": "Orientation and Foundations",
        "description": "The opening units set up couplings, examples, and the historical move from maps to plans.",
    },
    {
        "folder": "part-01-qualitative-description-of-optimal-transport",
        "title": "Part I: Qualitative Description of Optimal Transport",
        "description": "Existence, duality, Wasserstein geometry, displacement interpolation, Monge solvability, and regularity.",
    },
    {
        "folder": "part-02-optimal-transport-and-riemannian-geometry",
        "title": "Part II: Optimal Transport and Riemannian Geometry",
        "description": "Ricci curvature, Otto calculus, displacement convexity, functional inequalities, and gradient flows.",
    },
    {
        "folder": "part-03-synthetic-treatment-of-ricci-curvature",
        "title": "Part III: Synthetic Treatment of Ricci Curvature",
        "description": "Analytic versus synthetic definitions, metric-measure convergence, stability, and weak Ricci bounds.",
    },
    {
        "folder": "part-04-conclusions-and-open-problems",
        "title": "Conclusions and Open Problems",
        "description": "A final research map tying numerical transport, curvature, regularity, and applications together.",
    },
]


def _pdf_span(printed: str) -> str:
    first, last = [int(part) for part in printed.split("-")]
    return f"{first + MAIN_TEXT_PDF_OFFSET}-{last + MAIN_TEXT_PDF_OFFSET}"


def _slug(text: str) -> str:
    keep = []
    for ch in text.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in {" ", "-", ":"}:
            keep.append("-")
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def _unit(
    unit_id: str,
    label: str,
    title: str,
    printed: str,
    part: str,
    focus: str,
    concepts: list[str],
    visual: str,
    check: str,
    mode: str,
    lab: str,
    terms: list[str],
) -> dict[str, object]:
    folder = _slug(f"{unit_id}-{title}") if unit_id.startswith("chapter") else _slug(title)
    notebook_stem = unit_id[-2:] if unit_id.startswith("chapter") else unit_id
    if unit_id == "introduction":
        notebook = "introduction.ipynb"
    elif unit_id == "conclusions":
        notebook = "conclusions-and-open-problems.ipynb"
    else:
        notebook = f"{notebook_stem}-{_slug(title)}.ipynb"
    topic = f"{unit_id}-{_slug(title)}"
    return {
        "id": unit_id,
        "label": label,
        "title": title,
        "printed": printed,
        "pdf": _pdf_span(printed),
        "part": part,
        "folder": folder,
        "notebook": notebook,
        "topic": topic,
        "focus": focus,
        "concepts": concepts,
        "visual": visual,
        "check": check,
        "mode": mode,
        "lab": lab,
        "terms": terms,
    }


UNITS = [
    _unit(
        "introduction",
        "Introduction",
        "Introduction",
        "1-4",
        "part-00-orientation-and-foundations",
        "Build the course map: optimal transport as a bridge between probability, geometry, dynamics, and curvature.",
        [
            "Why a transport plan can be a geometric object rather than only a probabilistic coupling.",
            "How displacement interpolation lets probability measures move along visible paths.",
            "Why Ricci curvature enters through volume distortion and convexity along those paths.",
        ],
        "A dependency graph from couplings to Wasserstein geodesics to Ricci curvature bounds.",
        "The graph has every required hub and a path from coupling to synthetic Ricci curvature.",
        "course-map",
        "Modify the dependency graph by adding one application domain and explain which edge it uses.",
        ["coupling", "Wasserstein", "displacement interpolation", "Ricci curvature"],
    ),
    _unit(
        "chapter-01",
        "Chapter 01",
        "Couplings and changes of variables",
        "5-20",
        "part-00-orientation-and-foundations",
        "Make couplings concrete as matrices and maps, then track how mass and Jacobians account for changes of variables.",
        [
            "Coupling as a joint law with prescribed marginals.",
            "Deterministic transport as a graph-supported coupling.",
            "Gluing and change-of-variables formulas as bookkeeping devices.",
        ],
        "A coupling heatmap with source and target marginals plus arrows for the barycentric map.",
        "Row and column sums match the prescribed measures and the cost agrees with the plan.",
        "coupling",
        "Change one target weight and watch which row of the transport matrix adapts first.",
        ["coupling", "pushforward", "Jacobian", "gluing"],
    ),
    _unit(
        "chapter-02",
        "Chapter 02",
        "Three examples of coupling techniques",
        "21-28",
        "part-00-orientation-and-foundations",
        "Use three small models to see coupling as a proof method: contraction, comparison, and transport-based inequality.",
        [
            "Synchronous Langevin coupling turns shared noise into deterministic contraction.",
            "Knothe-Rosenblatt style triangular maps support an isoperimetric comparison.",
            "Coupling estimates translate pathwise control into distributional control.",
        ],
        "A contractive path diagram paired with a small transport comparison.",
        "The distance curve decreases and the associated coupling keeps both marginals normalized.",
        "contraction",
        "Vary the convexity constant in the contraction model and identify the slowest decay.",
        ["Langevin", "Knothe-Rosenblatt", "isoperimetry", "coupling estimate"],
    ),
    _unit(
        "chapter-03",
        "Chapter 03",
        "The founding fathers of optimal transport",
        "29-38",
        "part-00-orientation-and-foundations",
        "Trace the conceptual move from Monge's deterministic map to Kantorovich's relaxed plan and dual variables.",
        [
            "Monge asks for a map and forbids splitting mass.",
            "Kantorovich relaxes the problem to plans and gains compactness.",
            "Dual variables turn the transport problem into a certificate of optimality.",
        ],
        "A timeline and primal-dual diagram connecting maps, plans, and potentials.",
        "The primal plan cost and dual certificate agree within numerical tolerance.",
        "duality",
        "Construct a two-source example where map-only transport is too rigid but a plan is natural.",
        ["Monge", "Kantorovich", "duality", "transport plan"],
    ),
    _unit(
        "chapter-04",
        "Chapter 04",
        "Basic properties",
        "43-50",
        "part-01-qualitative-description-of-optimal-transport",
        "Organize the basic existence theorem around compactness of plans, lower semicontinuity of cost, and tightness.",
        [
            "The admissible set of plans is convex and controlled by its marginals.",
            "Lower semicontinuity turns limiting plans into minimizers.",
            "Restriction and approximation are practical tools for noncompact problems.",
        ],
        "A small transport polytope with the optimal corner highlighted.",
        "All candidate plans have valid marginals and the chosen plan minimizes total cost among enumerated alternatives.",
        "polytope",
        "Perturb one cost entry and record when the optimal corner changes.",
        ["existence", "compactness", "lower semicontinuity", "restriction"],
    ),
    _unit(
        "chapter-05",
        "Chapter 05",
        "Cyclical monotonicity and Kantorovich duality",
        "51-92",
        "part-01-qualitative-description-of-optimal-transport",
        "Turn optimality into a finite certificate: no improving cycle and matching dual potentials.",
        [
            "Cyclical monotonicity rules out cheaper cyclic reassignment.",
            "The c-transform builds potentials adapted to the cost.",
            "Complementary slackness explains why support points are special.",
        ],
        "A matching diagram plus slack matrix for the dual certificate.",
        "Every active plan entry has near-zero dual slack and every inactive slack is nonnegative.",
        "duality",
        "Find a three-point permutation that violates cyclical monotonicity after a cost perturbation.",
        ["cyclical monotonicity", "c-transform", "dual potential", "slack"],
    ),
    _unit(
        "chapter-06",
        "Chapter 06",
        "The Wasserstein distances",
        "93-112",
        "part-01-qualitative-description-of-optimal-transport",
        "Read Wasserstein distance as a metric on probability measures whose scale depends on both geometry and moments.",
        [
            "The order p changes how far tails and long moves are penalized.",
            "Finite moments are part of the space, not a technical afterthought.",
            "Metric axioms become visible through gluing and optimal plans.",
        ],
        "Side-by-side W1 and W2 transport costs on the same measures.",
        "The computed W2 obeys a triangle inequality check on a third measure.",
        "wasserstein",
        "Move a tiny amount of mass far away and compare the response of W1 and W2.",
        ["Wasserstein distance", "moment", "metric", "triangle inequality"],
    ),
    _unit(
        "chapter-07",
        "Chapter 07",
        "Displacement interpolation",
        "113-162",
        "part-01-qualitative-description-of-optimal-transport",
        "Make geodesics in probability space visible by moving mass along optimal transport rays.",
        [
            "A coupling plus minimizing curves defines intermediate measures.",
            "Quadratic Euclidean cost turns interpolation into straight-line particle motion.",
            "Lagrangian action gives a common language for smooth and nonsmooth settings.",
        ],
        "Snapshots of a discrete displacement interpolation with particle weights preserved.",
        "All interpolated measures have total mass one and endpoints match the source and target.",
        "interpolation",
        "Animate or sample more times along the interpolation and identify when the density is most spread out.",
        ["displacement interpolation", "Lagrangian action", "geodesic", "endpoint"],
    ),
    _unit(
        "chapter-08",
        "Chapter 08",
        "The Monge-Mather shortening principle",
        "163-204",
        "part-01-qualitative-description-of-optimal-transport",
        "Use shortening as the geometric reason optimal curves do not cross in the wrong way.",
        [
            "Action-minimizing curves encode the cost.",
            "Crossing configurations suggest a cheaper rewiring.",
            "Intermediate-time maps can be better behaved than endpoint maps.",
        ],
        "A before-and-after crossing diagram where swapped endpoints reduce action.",
        "The shortened pairing has lower or equal total action than the crossing pairing.",
        "shortening",
        "Move the crossing point and find the configuration where shortening disappears.",
        ["Mather", "shortening", "action", "no crossing"],
    ),
    _unit(
        "chapter-09",
        "Chapter 09",
        "Solution of the Monge problem I: Global approach",
        "205-214",
        "part-01-qualitative-description-of-optimal-transport",
        "Explain the global strategy for proving that a c-subdifferential is single valued almost everywhere.",
        [
            "A c-convex potential gathers possible destinations into a c-subdifferential.",
            "Path-connected subdifferentials turn multivaluedness into a visible branching event.",
            "Exceptional sets are small enough to be invisible to absolutely continuous mass.",
        ],
        "A branching c-subdifferential cartoon with the exceptional set isolated.",
        "The plotted branch set has lower estimated dimension than the ambient sample grid.",
        "subdifferential",
        "Create a toy potential with two candidate destinations and locate the switch set.",
        ["Monge problem", "c-convex", "subdifferential", "exceptional set"],
    ),
    _unit(
        "chapter-10",
        "Chapter 10",
        "Solution of the Monge problem II: Local approach",
        "215-272",
        "part-01-qualitative-description-of-optimal-transport",
        "Study local hypotheses, especially twist, that let first-order information select a unique transport destination.",
        [
            "Twist turns a derivative with respect to the source into destination information.",
            "Local semiconcavity and differentiability make the selection measurable.",
            "Local arguments must still be patched across singular regions.",
        ],
        "A local twist map where gradient directions label destinations.",
        "The twist sampling map is injective on the displayed neighborhood.",
        "twist",
        "Break the twist condition in the toy model and find two destinations with the same source derivative.",
        ["twist", "local differentiability", "semiconcavity", "Monge map"],
    ),
    _unit(
        "chapter-11",
        "Chapter 11",
        "The Jacobian equation",
        "273-280",
        "part-01-qualitative-description-of-optimal-transport",
        "Turn mass conservation for a smooth map into a determinant equation that can be checked numerically.",
        [
            "A transport map changes volume by its Jacobian determinant.",
            "Density ratios must match the determinant along the map.",
            "For quadratic cost this becomes the Monge-Ampere equation for a convex potential.",
        ],
        "A deformed grid colored by local determinant and density ratio.",
        "The determinant-based mass equation has small residual on the sample grid.",
        "jacobian",
        "Tune the map strength until the determinant first becomes nonpositive.",
        ["Jacobian", "Monge-Ampere", "density ratio", "change of variables"],
    ),
    _unit(
        "chapter-12",
        "Chapter 12",
        "Smoothness",
        "281-332",
        "part-01-qualitative-description-of-optimal-transport",
        "Separate existence of a map from smoothness of that map, using cost curvature and singular examples as guides.",
        [
            "Smooth data do not automatically give smooth transport.",
            "Cost geometry controls whether singularities are suppressed or amplified.",
            "Regularity theory studies the transport potential as a nonlinear PDE solution.",
        ],
        "A smooth potential and a kinked potential compared through their transport fields.",
        "The smooth field has bounded finite-difference variation while the kinked field has a detected jump.",
        "smoothness",
        "Vary the smoothing scale and watch the jump detector converge to zero or stay positive.",
        ["smoothness", "regularity", "MTW", "singularity"],
    ),
    _unit(
        "chapter-13",
        "Chapter 13",
        "Qualitative picture",
        "333-352",
        "part-01-qualitative-description-of-optimal-transport",
        "Synthesize Part I into a decision map: which assumptions buy existence, maps, interpolation, and regularity.",
        [
            "Plans are robust; maps need source regularity and cost structure.",
            "Interpolation can reveal regularity not visible at endpoints.",
            "Different costs create different qualitative transport worlds.",
        ],
        "A decision-flow graph connecting assumptions to transport conclusions.",
        "Every conclusion node is reachable from at least one assumption path.",
        "decision",
        "Pick a cost and mark which branches of the decision map are unavailable.",
        ["qualitative picture", "assumption", "transport map", "regularity"],
    ),
    _unit(
        "chapter-14",
        "Chapter 14",
        "Ricci curvature",
        "357-420",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Visualize Ricci curvature as averaged geodesic spreading and volume distortion, the curvature signal used later by transport.",
        [
            "Sectional curvature describes a plane; Ricci traces over directions transverse to motion.",
            "Positive Ricci slows the spreading of geodesic fans.",
            "Distortion coefficients package curvature and dimension for transport estimates.",
        ],
        "Model-space geodesic fans and Ricci distortion coefficient curves.",
        "Positive, zero, and negative curvature curves are ordered as expected for small distances.",
        "ricci",
        "Compare two dimensions and explain why tracing over more directions changes the coefficient.",
        ["Ricci curvature", "sectional curvature", "volume distortion", "distortion coefficient"],
    ),
    _unit(
        "chapter-15",
        "Chapter 15",
        "Otto calculus",
        "421-434",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Treat probability densities as a formal Riemannian manifold where tangent vectors are velocity fields.",
        [
            "A tangent vector to a density is represented through a continuity equation.",
            "The Wasserstein metric pairs gradients of potentials.",
            "Gradient flows become steepest-descent curves for functionals on measures.",
        ],
        "A density with a velocity field and its induced continuity-equation change.",
        "The discrete divergence integrates to zero, preserving total mass.",
        "otto",
        "Change the velocity potential and identify where mass is created locally and removed locally.",
        ["Otto calculus", "continuity equation", "velocity potential", "Wasserstein metric"],
    ),
    _unit(
        "chapter-16",
        "Chapter 16",
        "Displacement convexity I",
        "435-448",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Study entropy along Wasserstein geodesics as the transport-facing form of lower Ricci curvature.",
        [
            "Ordinary linear interpolation and displacement interpolation bend entropy differently.",
            "Convexity along transport geodesics is stronger and more geometric than pointwise convexity.",
            "Lower Ricci bounds can be read from entropy convexity behavior.",
        ],
        "Entropy sampled along a displacement interpolation and a linear-mixture path.",
        "The displacement entropy curve satisfies a discrete convexity residual in the toy model.",
        "entropy",
        "Move the source and target closer together and compare the convexity residual.",
        ["displacement convexity", "entropy", "geodesic", "Ricci lower bound"],
    ),
    _unit(
        "chapter-17",
        "Chapter 17",
        "Displacement convexity II",
        "449-492",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Add dimension-sensitive convexity classes and distortion coefficients to the entropy story.",
        [
            "The dimension parameter changes which entropy powers are convex.",
            "Distortion coefficients record how geodesic volumes deviate from flat space.",
            "Curvature-dimension inequalities combine K and N in a transport-ready form.",
        ],
        "Curvature-dimension distortion curves for several K and N choices.",
        "The flat coefficient is the baseline and positive curvature stays below it before conjugate effects.",
        "ricci",
        "Increase N and observe how strongly the same K affects the plotted coefficient.",
        ["curvature-dimension", "DCN", "distortion coefficient", "entropy power"],
    ),
    _unit(
        "chapter-18",
        "Chapter 18",
        "Volume control",
        "493-504",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Turn curvature information into volume comparison by watching balls and interpolated sets expand.",
        [
            "Bishop-Gromov type ratios compare measured balls at different radii.",
            "Transport interpolation converts pointwise distortion into set-volume control.",
            "Model spaces provide the baseline for comparison.",
        ],
        "Volume-growth curves for flat, positive, and negative curvature model spaces.",
        "The normalized positive-curvature volume ratio decreases over the sampled radii.",
        "volume",
        "Change the model curvature and find the radius where flat intuition fails visibly.",
        ["volume control", "Bishop-Gromov", "Brunn-Minkowski", "model space"],
    ),
    _unit(
        "chapter-19",
        "Chapter 19",
        "Density control and local regularity",
        "505-524",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Track how upper density bounds propagate along interpolation and why that helps local regularity.",
        [
            "Density control is a quantitative version of no mass collapse.",
            "Curvature modifies the interpolation density estimate.",
            "Local regularity arguments often start from such uniform bounds.",
        ],
        "Density envelopes along an interpolating family with maximum values annotated.",
        "Every sampled density integrates to one and remains below the computed envelope.",
        "density",
        "Sharpen or loosen the initial density cap and compare the propagated envelope.",
        ["density control", "local regularity", "interpolation", "mass cap"],
    ),
    _unit(
        "chapter-20",
        "Chapter 20",
        "Infinitesimal displacement convexity",
        "525-544",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Connect global displacement convexity to infinitesimal second-variation and Gamma2 style checks.",
        [
            "Infinitesimal criteria replace an entire geodesic by local differential data.",
            "Bochner-type terms split into Hessian energy and Ricci contribution.",
            "Numerical Hessians let the learner see convexity residuals pointwise.",
        ],
        "A heatmap of a toy second-variation residual over a two-dimensional grid.",
        "The residual is nonnegative after adding the chosen Ricci lower-bound term.",
        "infinitesimal",
        "Decrease the curvature lower bound until the residual heatmap first shows negative values.",
        ["infinitesimal convexity", "Gamma2", "Bochner", "Hessian"],
    ),
    _unit(
        "chapter-21",
        "Chapter 21",
        "Isoperimetric-type inequalities",
        "545-566",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Use transport and curvature to organize geometric and functional inequalities with boundary-size content.",
        [
            "Isoperimetric inequalities compare volume to boundary measure.",
            "Transport maps can convert a comparison body into a test object.",
            "Functional inequalities often appear as softened isoperimetric statements.",
        ],
        "A shape comparison plot with area, perimeter, and normalized deficit.",
        "The disk has the smallest sampled isoperimetric deficit among the displayed shapes.",
        "isoperimetric",
        "Add an elongated ellipse and quantify how its deficit changes with eccentricity.",
        ["isoperimetric inequality", "functional inequality", "perimeter", "deficit"],
    ),
    _unit(
        "chapter-22",
        "Chapter 22",
        "Concentration inequalities",
        "567-628",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Translate transport inequalities into visible tail bounds and concentration profiles.",
        [
            "A transport inequality controls how expensive it is to move away from equilibrium.",
            "Concentration bounds turn that cost into tail decay.",
            "Gaussian models give a baseline for the shape of the estimate.",
        ],
        "Gaussian tail and transport-bound curves on the same axis.",
        "The bound curve stays above the empirical tail curve on the sampled grid.",
        "concentration",
        "Increase the variance proxy and explain how the concentration profile weakens.",
        ["concentration", "transport inequality", "tail bound", "Gaussian"],
    ),
    _unit(
        "chapter-23",
        "Chapter 23",
        "Gradient flows I",
        "629-692",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Build the JKO idea in a finite setting: alternate entropy descent with Wasserstein movement cost.",
        [
            "A gradient flow in Wasserstein space balances energy descent and transport cost.",
            "The heat equation is the model example for entropy gradient flow.",
            "JKO steps turn continuous flow into repeated minimization.",
        ],
        "A sequence of one-dimensional densities smoothing under a toy JKO/heat step.",
        "Entropy decreases and total mass stays one at each sampled step.",
        "gradient-flow",
        "Change the time step and compare how much entropy is dissipated per step.",
        ["gradient flow", "JKO", "heat equation", "entropy dissipation"],
    ),
    _unit(
        "chapter-24",
        "Chapter 24",
        "Gradient flows II: Qualitative properties",
        "693-718",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Inspect qualitative properties of metric gradient flows: contraction, comparison, and asymptotic behavior.",
        [
            "Contractivity says two flows approach each other in Wasserstein distance.",
            "Energy dissipation and comparison principles give qualitative control.",
            "Long-time behavior is read from decay curves, not only from explicit formulas.",
        ],
        "Two smoothing density flows with their Wasserstein distance over time.",
        "The displayed distance curve is nonincreasing within numerical tolerance.",
        "flow-quality",
        "Start the two flows farther apart and compare the contraction rate.",
        ["contractivity", "EVI", "asymptotic behavior", "comparison"],
    ),
    _unit(
        "chapter-25",
        "Chapter 25",
        "Gradient flows III: Functional inequalities",
        "719-730",
        "part-02-optimal-transport-and-riemannian-geometry",
        "Read functional inequalities as quantitative decay statements along a gradient flow.",
        [
            "Log-Sobolev and Poincare-type inequalities translate into entropy or variance decay.",
            "Gradient-flow estimates connect one-step dissipation to long-time behavior.",
            "Transport viewpoints clarify which metric is measuring the decay.",
        ],
        "Entropy and Fisher-information proxies with an inequality gap shaded.",
        "The sampled dissipation inequality has a nonnegative gap.",
        "functional",
        "Lower the inequality constant and identify when the sampled gap becomes uninformative.",
        ["functional inequality", "entropy decay", "Poincare", "log-Sobolev"],
    ),
    _unit(
        "chapter-26",
        "Chapter 26",
        "Analytic and synthetic points of view",
        "735-742",
        "part-03-synthetic-treatment-of-ricci-curvature",
        "Contrast analytic tests that are easy to compute with synthetic tests that survive low-regularity limits.",
        [
            "Hessian nonnegativity is local and computational.",
            "Chord convexity is synthetic and stable under weak limits.",
            "Curvature bounds need both viewpoints: checkability and stability.",
        ],
        "A convexity panel comparing Hessian samples with chord inequalities.",
        "The nonsmooth convex example passes chord checks even where finite-difference Hessians are unstable.",
        "synthetic",
        "Replace the absolute-value example by a smoothed version and compare the two tests.",
        ["analytic", "synthetic", "convexity", "Alexandrov"],
    ),
    _unit(
        "chapter-27",
        "Chapter 27",
        "Convergence of metric-measure spaces",
        "743-772",
        "part-03-synthetic-treatment-of-ricci-curvature",
        "Model metric-measure convergence with finite point clouds whose distances and weights approach a limit.",
        [
            "Gromov-Hausdorff convergence compares metric spaces without fixed coordinates.",
            "Measured convergence adds the probability distribution to the geometry.",
            "Finite correspondences make the abstract definitions inspectable.",
        ],
        "A sequence of sampled metric-measure spaces approaching a circle.",
        "The distance-matrix distortion and weight mismatch decrease along the sequence.",
        "mm-convergence",
        "Add a persistent outlier and observe which convergence diagnostic fails first.",
        ["metric-measure", "Gromov-Hausdorff", "measured convergence", "correspondence"],
    ),
    _unit(
        "chapter-28",
        "Chapter 28",
        "Stability of optimal transport",
        "773-794",
        "part-03-synthetic-treatment-of-ricci-curvature",
        "Show that transport costs, plans, and interpolations vary continuously under controlled convergence.",
        [
            "Tightness and lower semicontinuity keep limiting plans admissible.",
            "Costs converge when geometry and measures converge compatibly.",
            "Interpolation stability is the bridge to synthetic curvature bounds.",
        ],
        "A sequence of perturbed target measures with transport cost convergence.",
        "The cost sequence converges to the limiting cost and marginal errors remain small.",
        "stability",
        "Add random metric noise and identify when the transport plan changes abruptly.",
        ["stability", "limiting plan", "lower semicontinuity", "interpolation"],
    ),
    _unit(
        "chapter-29",
        "Chapter 29",
        "Weak Ricci curvature bounds I: Definition and Stability",
        "795-846",
        "part-03-synthetic-treatment-of-ricci-curvature",
        "Present weak Ricci bounds as convexity of entropy-like functionals along Wasserstein geodesics, then test stability.",
        [
            "CD(K,N) style definitions are synthetic because they use measure geodesics.",
            "Distortion coefficients encode the chosen curvature and dimension.",
            "The definition is designed to survive convergence of metric-measure spaces.",
        ],
        "Entropy convexity curves with distortion-coefficient correction terms.",
        "The corrected convexity residual is nonnegative for the displayed stable family.",
        "weak-ricci",
        "Vary K and locate the threshold where the toy family no longer passes the residual check.",
        ["weak Ricci", "CD(K,N)", "stability", "entropy convexity"],
    ),
    _unit(
        "chapter-30",
        "Chapter 30",
        "Weak Ricci curvature bounds II: Geometric and analytic properties",
        "847-902",
        "part-03-synthetic-treatment-of-ricci-curvature",
        "Organize consequences of weak Ricci bounds: volume comparison, local-to-global behavior, and analytic inequalities.",
        [
            "Synthetic Ricci lower bounds imply recognizable geometric controls.",
            "Analytic consequences include functional inequalities and heat-flow behavior.",
            "The final chapter tests how much classical Riemannian geometry survives nonsmooth limits.",
        ],
        "A consequence matrix linking CD assumptions to geometric and analytic outputs.",
        "Every displayed consequence is connected to at least one assumption and one transport mechanism.",
        "consequence",
        "Remove one assumption from the matrix and mark which consequences become unsupported.",
        ["weak Ricci", "geometric property", "analytic property", "local-to-global"],
    ),
    _unit(
        "conclusions",
        "Conclusions",
        "Conclusions and open problems",
        "903-914",
        "part-04-conclusions-and-open-problems",
        "Close the course with a research map: numerics, regularity, curvature, dynamics, and applications.",
        [
            "Numerical transport is a major practical frontier even when not developed in the book.",
            "Regularity and curvature remain linked through difficult nonlinear structure.",
            "Synthetic Ricci theory suggests new spaces where transport can do geometry.",
        ],
        "A radar-style open-problem map with computational and geometric axes.",
        "The open-problem graph contains links from every course part to at least one future direction.",
        "open-problems",
        "Choose one open direction and propose a small computational experiment that would make it teachable.",
        ["open problem", "numerics", "regularity", "synthetic geometry"],
    ),
]


UNIT_BY_ID = {unit["id"]: unit for unit in UNITS}
PART_BY_FOLDER = {part["folder"]: part for part in PARTS}


def unit_path(unit: dict[str, object]) -> Path:
    return BOOK_ROOT / str(unit["part"]) / str(unit["folder"]) / str(unit["notebook"])


def unit_index_path(unit: dict[str, object]) -> Path:
    return BOOK_ROOT / str(unit["part"]) / str(unit["folder"]) / "00-index.ipynb"


def part_index_path(part: dict[str, str]) -> Path:
    return BOOK_ROOT / part["folder"] / "00-part-index.ipynb"


def artifact_root(unit: dict[str, object]) -> Path:
    return BOOK_ROOT / "artifacts" / str(unit["topic"])


def rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def expected_notebooks(include_indexes: bool = False) -> list[Path]:
    paths = [unit_path(unit) for unit in UNITS]
    if include_indexes:
        paths.append(BOOK_ROOT / "00-book-index.ipynb")
        paths.extend(part_index_path(part) for part in PARTS)
        paths.extend(unit_index_path(unit) for unit in UNITS)
    return paths


def smoke_unit_ids() -> set[str]:
    return {
        "introduction",
        "chapter-01",
        "chapter-05",
        "chapter-07",
        "chapter-14",
        "chapter-23",
        "chapter-29",
        "conclusions",
    }
