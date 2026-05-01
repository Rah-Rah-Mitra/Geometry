"""Create the initial ENEG canonical notebooks.

This is an initial course materialization helper, not the normal chapter-editing
workflow. Future chapter revisions should edit the canonical notebooks directly.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

BOOK_ROOT = Path(__file__).resolve().parents[1]
if str(BOOK_ROOT) not in sys.path:
    sys.path.insert(0, str(BOOK_ROOT))

from utils.validation import SOURCE_MAP  # noqa: E402


EXTRA = {
    "00": {
        "question": "How can one postulate about parallels reorganize the meaning of geometry?",
        "claim": "The introduction places Euclidean geometry beside other consistent ways to organize space.",
        "translation": [
            "parallel behavior becomes a model choice",
            "diagrams are evidence only after axioms say what diagrams mean",
            "curvature is treated as an observable pattern in angle sums and geodesics",
        ],
        "route": ["compare three parallel regimes", "track the role of models", "set up visual tests used throughout the course"],
        "story": ["Parallel problem", "Axiom choice", "Model", "Observable behavior", "Interpretation"],
        "scene": "parallel-regimes",
        "lab": "model-comparison",
    },
    "01": {
        "question": "What does Euclid's system achieve, and where does a diagram quietly overpromise?",
        "claim": "Euclid's postulates support powerful constructions, while the parallel postulate behaves differently from local ruler-and-compass permissions.",
        "translation": ["postulates become construction permissions", "proof steps become dependency edges", "diagram facts are tested by perturbing the drawing"],
        "route": ["read the postulates as operations", "build a construction diagram", "separate local construction from global parallel behavior"],
        "story": ["Postulates", "Construction", "Diagram risk", "Parallel attempt", "Axiom audit"],
        "scene": "euclid-construction",
        "lab": "diagram-perturbation",
    },
    "02": {
        "question": "How do logic and finite models make incidence geometry inspectable?",
        "claim": "A model is a machine for testing sentences: it tells us which incidence claims follow from axioms and which require stronger assumptions.",
        "translation": ["statements become predicates over points and lines", "isomorphism becomes relabeling with the same incidence table", "projective and affine planes become small graphs"],
        "route": ["make proof vocabulary explicit", "build finite incidence tables", "compare affine and projective behavior"],
        "story": ["Statement", "Predicate", "Model", "Isomorphism", "Proof"],
        "scene": "fano-plane",
        "lab": "truth-table",
    },
    "03": {
        "question": "Why split geometry into axiom families instead of one list of obvious facts?",
        "claim": "Hilbert-style organization makes hidden assumptions visible by separating incidence, order, congruence, continuity, and parallelism.",
        "translation": ["axiom families become modules", "dependency diagrams show which proof tools are currently licensed", "countermodels show what breaks when one family is removed"],
        "route": ["map the axiom families", "visualize betweenness and congruence", "test continuity as a limiting assumption"],
        "story": ["Incidence", "Order", "Congruence", "Continuity", "Parallelism"],
        "scene": "axiom-dependencies",
        "lab": "betweenness",
    },
    "04": {
        "question": "What remains true before committing to Euclid's parallel postulate?",
        "claim": "Neutral geometry proves many Euclidean-looking facts while keeping angle sums and parallel behavior open.",
        "translation": ["Saccheri quadrilaterals become diagnostic instruments", "angle-sum bounds become numerical experiments", "equivalent postulates become a proof dependency network"],
        "route": ["work without a parallel axiom", "measure Saccheri summit behavior", "compare equivalent Euclidean statements"],
        "story": ["Neutral facts", "Saccheri quadrilateral", "Angle sum", "Equivalent postulates", "Decision point"],
        "scene": "saccheri",
        "lab": "angle-sum",
    },
    "05": {
        "question": "What did historical attempts to prove the parallel postulate actually reveal?",
        "claim": "The long history matters mathematically because each failed proof isolates an assumption that later becomes a model choice.",
        "translation": ["authors become nodes in a dependency timeline", "failed proofs become assumption detectors", "quadrilateral cases become computable regimes"],
        "route": ["follow the historical chain", "mark the hidden assumptions", "turn the Saccheri/Lambert split into a visual lab"],
        "story": ["Proclus", "Wallis", "Saccheri", "Lambert", "Legendre"],
        "scene": "history-timeline",
        "lab": "quadrilateral-regimes",
    },
    "06": {
        "question": "What changes when hyperbolic geometry is treated as coherent rather than contradictory?",
        "claim": "Hyperbolic geometry keeps much of neutral geometry but changes the global behavior of parallels, similarity, and angle defect.",
        "translation": ["geodesics become arcs orthogonal to the disk boundary", "limiting parallels become boundary endpoints", "defect becomes area in curvature -1"],
        "route": ["draw disk geodesics", "measure defect", "see why similar triangles become congruent"],
        "story": ["Bolyai", "Gauss", "Lobachevsky", "Limiting parallels", "Defect"],
        "scene": "poincare-geodesics",
        "lab": "hyperbolic-defect",
    },
    "07": {
        "question": "How can a model prove that the parallel postulate is independent?",
        "claim": "If a hyperbolic model satisfies the neutral axioms inside a Euclidean host, a proof of Euclid's parallel postulate from those axioms cannot exist.",
        "translation": ["model consistency becomes interpretation", "Klein chords and Poincare arcs become two views of the same geometry", "inversion supplies circle-orthogonal geodesics"],
        "route": ["compare models", "compute disk distances", "read independence as a relative-consistency result"],
        "story": ["Neutral axioms", "Klein model", "Poincare model", "Interpretation", "Independence"],
        "scene": "model-comparison",
        "lab": "cross-ratio",
    },
    "08": {
        "question": "What does non-Euclidean geometry change about mathematical and physical truth?",
        "claim": "The discovery shifts geometry from a single picture of space to a disciplined relation among axioms, models, measurement, and interpretation.",
        "translation": ["physical claims become model-selection problems", "foundational positions become diagrams of commitment", "mathematical truth is checked inside an axiom system"],
        "route": ["separate formal and physical questions", "map foundations", "design a measurement thought experiment"],
        "story": ["Formal system", "Model", "Measurement", "Physical space", "Philosophy"],
        "scene": "philosophy-map",
        "lab": "measurement-noise",
    },
    "09": {
        "question": "How do transformations turn geometry into the study of invariants?",
        "claim": "The Erlangen viewpoint treats a geometry by the transformations that preserve its meaningful relations.",
        "translation": ["motions become functions on points", "groups become closure tables", "reflections and rotations generate larger symmetry classes"],
        "route": ["visualize transformations", "check invariants", "connect Euclidean and hyperbolic automorphisms"],
        "story": ["Transformation", "Invariant", "Group", "Motion", "Symmetry"],
        "scene": "transformations",
        "lab": "group-closure",
    },
    "10": {
        "question": "Which quantitative formulas make hyperbolic geometry feel like a complete measuring system?",
        "claim": "Angle defect, cycles, angle of parallelism, and hyperbolic trigonometry are the measurement language of negative curvature.",
        "translation": ["defect becomes area", "angle of parallelism becomes a decaying function", "the pseudosphere supplies a local surface model"],
        "route": ["plot the angle of parallelism", "compare cycle types", "inspect a pseudosphere mesh"],
        "story": ["Defect", "Parallel angle", "Cycles", "Trig", "Pseudosphere"],
        "scene": "pseudosphere",
        "lab": "parallel-angle",
    },
    "A": {
        "question": "How do elliptic and Riemannian geometries broaden the model landscape?",
        "claim": "Positive curvature and variable curvature show that parallel behavior is one visible symptom of a more general metric structure.",
        "translation": ["elliptic lines become great circles with antipodal identification", "curvature becomes reciprocal radius for simple models", "a Riemannian metric becomes a local measuring rule"],
        "route": ["compare spherical and elliptic pictures", "measure great-circle behavior", "visualize metric ellipses"],
        "story": ["Sphere", "Antipodes", "Great circles", "Curvature", "Metric"],
        "scene": "elliptic-sphere",
        "lab": "metric-ellipses",
    },
    "B": {
        "question": "What happens when continuity is removed from geometry?",
        "claim": "Without continuity, incidence and separation can still be studied, but limiting arguments and familiar ruler intuition no longer automatically apply.",
        "translation": ["finite models become laboratories", "missing limits become visible gaps", "reflection-generated geometries become algebraic rather than analytic"],
        "route": ["build a finite incidence world", "watch continuity fail", "separate combinatorial and metric information"],
        "story": ["Incidence", "Finite model", "Reflection", "Gap", "Continuity"],
        "scene": "finite-grid",
        "lab": "missing-limits",
    },
}


DETAILS = {
    "00": {
        "definitions": [
            ("Parallel regime", "a rule for how many lines through an external point avoid a chosen line"),
            ("Model", "an interpretation where undefined geometric words become concrete objects"),
            ("Observable", "a measurable feature such as angle sum, geodesic shape, or parallel count"),
        ],
        "equations": ["Euclidean: N(P,l)=1", "Hyperbolic sample: N(P,l)>1", "Elliptic: N(P,l)=0"],
        "worked": "Put a point P above a line l. In the Euclidean plane there is one line through P with the same direction as l. In a disk picture of hyperbolic geometry there are multiple geodesics through P that do not meet l inside the model. On a sphere, every pair of great circles meets, so there is no parallel. The same input question therefore separates three geometries before any long theorem is proved.",
        "artifacts": {
            "relationship": "parallel-problem-interpretation-map.png",
            "scene": "three-parallel-regimes.png",
            "lab": "parallel-count-model-lab.png",
        },
    },
    "01": {
        "definitions": [
            ("Postulate", "a licensed construction or relation rather than a fact read directly from a drawing"),
            ("Diagram risk", "the danger that a special picture supplies an unstated assumption"),
            ("Construction dependency", "the ordered record of which objects were allowed before later objects were drawn"),
        ],
        "equations": ["equilateral check: |AB|=|AC|=|BC|", "parallel claim: through P not on l, exactly one candidate is Euclidean"],
        "worked": "The equilateral-triangle construction is a clean example of local postulates at work. Given AB, draw the circle centered at A through B and the circle centered at B through A. Their intersection C gives AC=AB and BC=AB because both are radii. The proof does not need the parallel postulate. That contrast is the lesson: some Euclidean facts are local construction facts, while the parallel postulate controls a global behavior of the whole plane.",
        "artifacts": {
            "relationship": "euclid-postulate-dependency-map.png",
            "scene": "equilateral-circle-construction.png",
            "lab": "diagram-perturbation-risk-lab.png",
        },
    },
    "02": {
        "definitions": [
            ("Incidence model", "a finite or infinite collection of points and lines with a lies-on relation"),
            ("Isomorphism", "a relabeling that preserves incidence exactly"),
            ("Predicate", "a statement whose truth can be tested against a model"),
        ],
        "equations": ["Fano sample: 7 points, 7 lines, 3 points per line", "incidence count = 7*3 = 21"],
        "worked": "In the seven-point projective-plane sample, each listed line contains three points and each point lies on three lines. A statement such as any two points determine a line becomes a finite search over pairs. If a relabeling keeps the same point-line table, the geometry has not changed. This is the computational meaning of isomorphism in the notebook.",
        "artifacts": {
            "relationship": "logic-model-proof-map.png",
            "scene": "finite-fano-incidence-model.png",
            "lab": "predicate-truth-table-lab.png",
        },
    },
    "03": {
        "definitions": [
            ("Incidence axioms", "rules that decide which points lie on which lines"),
            ("Order axioms", "rules that make betweenness and separation meaningful"),
            ("Continuity axioms", "rules that prevent limiting constructions from falling into gaps"),
        ],
        "equations": ["axiom modules = {incidence, order, congruence, continuity, parallelism}", "neutral core = all modules except a chosen parallel axiom"],
        "worked": "A triangle proof may start with incidence to name the sides, use order to talk about interiors, use congruence to copy an angle, and use continuity to justify a limiting point. If the proof later uses uniqueness of parallels, that final step belongs to a separate module. The dependency diagram makes that handoff visible.",
        "artifacts": {
            "relationship": "hilbert-axiom-family-map.png",
            "scene": "axiom-modules-to-theorems.png",
            "lab": "betweenness-order-witness-lab.png",
        },
    },
    "04": {
        "definitions": [
            ("Neutral geometry", "the common geometry before choosing Euclidean or hyperbolic parallel behavior"),
            ("Saccheri quadrilateral", "a quadrilateral with equal perpendicular legs erected from a base"),
            ("Defect", "the amount by which a triangle angle sum falls below pi in curvature -1"),
        ],
        "equations": ["neutral bound: angle_sum <= pi", "hyperbolic model check: area = pi - angle_sum"],
        "worked": "A Saccheri quadrilateral is a diagnostic instrument. The base angles are right angles by construction, and the legs have equal length. Neutral geometry can prove the summit angles are equal. What it cannot decide by itself is whether those summit angles are right, acute, or obtuse; that undecided branch is where the parallel question hides.",
        "artifacts": {
            "relationship": "neutral-geometry-decision-map.png",
            "scene": "saccheri-quadrilateral-probe.png",
            "lab": "triangle-angle-sum-defect-lab.png",
        },
    },
    "05": {
        "definitions": [
            ("Hidden assumption", "a step that acts like a parallel axiom while pretending to be neutral"),
            ("Historical probe", "a failed proof reinterpreted as a test of which assumption is necessary"),
            ("Lambert case", "a quadrilateral branch that points toward curvature before models are explicit"),
        ],
        "equations": ["timeline span = latest attempt - earliest attempt", "right summit case corresponds to Euclidean behavior"],
        "worked": "A historical proof attempt can be read like a dependency trace. If the argument assumes similar but noncongruent triangles, it has smuggled in a Euclidean-like behavior. If it rules out an acute summit angle by diagram intuition, it has used a geometric assumption not licensed by neutral axioms. The timeline artifact marks those attempts as assumption detectors.",
        "artifacts": {
            "relationship": "parallel-postulate-history-map.png",
            "scene": "failed-proof-assumption-timeline.png",
            "lab": "saccheri-lambert-regime-lab.png",
        },
    },
    "06": {
        "definitions": [
            ("Poincare disk geodesic", "a diameter or a circle arc orthogonal to the boundary circle"),
            ("Limiting parallel", "a geodesic through a point sharing an ideal endpoint with a given line"),
            ("Similarity rigidity", "the hyperbolic fact that same angles force same size"),
        ],
        "equations": ["distance in disk: d(0,r)=2*atanh(r)", "area for K=-1: A = pi - (A+B+C)"],
        "worked": "Choose two interior points of the disk. If they lie on a diameter, the geodesic is a Euclidean segment. Otherwise, the geodesic is a Euclidean circle arc meeting the boundary at right angles. This visual rule lets the notebook draw limiting parallels and makes it plausible that boundary behavior, not ordinary straightness, controls hyperbolic parallelism.",
        "artifacts": {
            "relationship": "hyperbolic-discovery-concept-map.png",
            "scene": "poincare-disk-geodesics.png",
            "lab": "hyperbolic-angle-defect-area-lab.png",
        },
    },
    "07": {
        "definitions": [
            ("Relative consistency", "a model-based argument showing that a contradiction would transfer to the host theory"),
            ("Klein model", "a disk model where geodesics are chords and angle measurement is not Euclidean"),
            ("Poincare model", "a disk model where angles are represented conformally by Euclidean angles"),
        ],
        "equations": ["Klein to Poincare: p = k/(1+sqrt(1-|k|^2))", "diameter distance: d(0,r)=log((1+r)/(1-r))"],
        "worked": "The same hyperbolic line can be drawn as a chord in the Klein disk and as an orthogonal arc in the Poincare disk. If both models interpret the same neutral statements, then a neutral proof of Euclid's parallel postulate would force that statement inside the hyperbolic model. Since the model has many parallels, the supposed proof cannot exist.",
        "artifacts": {
            "relationship": "parallel-independence-model-map.png",
            "scene": "klein-poincare-geodesic-comparison.png",
            "lab": "cross-ratio-distance-lab.png",
        },
    },
    "08": {
        "definitions": [
            ("Formal truth", "truth relative to stated axioms"),
            ("Physical interpretation", "a claim that measurements in the world fit a model"),
            ("Foundational stance", "a policy for how axioms, intuition, and models are allowed to interact"),
        ],
        "equations": ["formal theorem: axioms -> conclusion", "physical claim: model + measurement error -> fit decision"],
        "worked": "The same theorem can be formally true and physically untested. A geometer may prove a result inside an axiom system, while a physicist asks whether measurements choose that system as a good model of space. The diagram separates those jobs so the reader does not confuse mathematical consistency with empirical confirmation.",
        "artifacts": {
            "relationship": "axioms-models-measurement-map.png",
            "scene": "foundations-interpretation-flow.png",
            "lab": "physical-measurement-error-band-lab.png",
        },
    },
    "09": {
        "definitions": [
            ("Transformation", "a rule sending points to points"),
            ("Invariant", "a property unchanged by a chosen class of transformations"),
            ("Group", "a set of transformations closed under composition and inverses"),
        ],
        "equations": ["closure: g,h in G implies g*h in G", "reflection reverses oriented area but preserves area magnitude"],
        "worked": "Take a triangle and move it by translation, reflection, and rotation. Side lengths and ordinary area magnitude survive all three motions, but orientation changes under reflection. This is the Erlangen idea in miniature: a geometry studies the features preserved by its transformation group.",
        "artifacts": {
            "relationship": "erlanger-invariant-map.png",
            "scene": "euclidean-motion-transformations.png",
            "lab": "four-motion-closure-table-lab.png",
        },
    },
    "10": {
        "definitions": [
            ("Angle of parallelism", "the limiting angle made by a parallel through a point at a given distance from a line"),
            ("Cycle", "a hyperbolic curve family including circles, horocycles, and equidistant curves"),
            ("Pseudosphere", "a surface patch that locally models constant negative curvature"),
        ],
        "equations": ["Pi(d)=2*atan(exp(-d))", "area = defect when curvature is -1"],
        "worked": "The angle of parallelism shrinks as the point moves farther from the line. That decay is a quantitative signature of hyperbolic geometry. The pseudosphere visual gives a surface intuition for negative curvature, while the lab records the formula that a reader can perturb and compare with the disk model.",
        "artifacts": {
            "relationship": "hyperbolic-measurement-map.png",
            "scene": "pseudosphere-negative-curvature-patch.png",
            "lab": "angle-of-parallelism-decay-lab.png",
        },
    },
    "A": {
        "definitions": [
            ("Elliptic line", "a great circle with antipodal points identified"),
            ("Positive curvature", "curvature like a sphere, where geodesics tend to meet"),
            ("Riemannian metric", "a smoothly varying rule for measuring tangent vectors"),
        ],
        "equations": ["circle curvature sample: k=1/r", "sphere great circles meet in antipodal pairs"],
        "worked": "On a sphere, the shortest paths are great-circle arcs. If antipodal points are identified, opposite points represent the same elliptic point and a great circle becomes an elliptic line. This removes parallels for a reason opposite to hyperbolic geometry: geodesics close up and meet rather than spreading apart.",
        "artifacts": {
            "relationship": "elliptic-riemannian-model-map.png",
            "scene": "elliptic-great-circle-sphere.png",
            "lab": "riemannian-metric-ellipse-lab.png",
        },
    },
    "B": {
        "definitions": [
            ("Continuity gap", "a missing limiting point that finite incidence data cannot supply"),
            ("Finite geometry", "a geometry with finitely many points or lines used to test axiom dependence"),
            ("Reflection-generated geometry", "a geometry organized by algebraic operations rather than a continuum"),
        ],
        "equations": ["finite sample: |P|=9", "candidate limit (1.5,1.0) is not in the 3 by 3 grid"],
        "worked": "A finite grid can satisfy simple incidence statements, but it cannot support every limiting argument familiar from the real plane. A sequence may point toward a coordinate that is not present in the model. That failure is not a bug in the diagram; it is the chapter's subject.",
        "artifacts": {
            "relationship": "continuity-free-geometry-map.png",
            "scene": "finite-grid-missing-limit-model.png",
            "lab": "missing-limit-sequence-lab.png",
        },
    },
}


def markdown(text: str):
    return new_markdown_cell(textwrap.dedent(text).strip() + "\n")


def code(text: str):
    return new_code_cell(textwrap.dedent(text).strip() + "\n")


def intro_markdown(item: dict[str, str], extra: dict[str, object]) -> str:
    translations = "\n".join(f"- {entry}." for entry in extra["translation"])
    route = "\n".join(f"{index + 1}. {entry}." for index, entry in enumerate(extra["route"]))
    return f"""
    # {item['kind']} {item['number']}: {item['title']}

    ## Source Span

    Source orientation: printed pages {item['printed']}, PDF pages {item['pdf']}. The source PDF is scanned, so this notebook does not depend on copied page text. It uses the span to identify the chapter's concepts and then rebuilds the lesson with original explanations, executable constructions, and locally generated artifacts.

    ## Chapter Question

    {extra['question']}

    {extra['claim']} The central habit in this course is to treat every geometric sentence as something that can be represented in more than one way: a diagram, a finite model, an algebraic rule, a metric computation, or a dependency graph. That habit is especially important for this book because the historical narrative is not just background. The history records which claims seemed visually obvious, which claims resisted proof, and which claims became visible only after mathematicians learned to separate axioms from models.

    A reader should not need the textbook open while using this notebook. The notebook therefore states the working definitions it needs, explains how each computation should be read, and ends with small sanity checks. The checks are not a replacement for proof; they are a way to keep the visualization honest. If a diagram claims an invariant, the code records a numerical or structural witness for that invariant. If a construction is meant to compare geometries, the artifact names the comparison instead of serving as decoration.

    ## Translation Guide

    {translations}

    These translations are deliberately modest. They do not try to mechanize the whole chapter. Instead, they identify the parts of the chapter where a reader benefits from touching the geometry: moving a point, inspecting a model, checking an angle, or following a proof dependency. In a foundations chapter, the visual object may be a graph of assumptions. In a hyperbolic chapter, it may be a disk model. In a history chapter, it may be a timeline whose edges mark hidden assumptions rather than a list of dates.

    ## Route Through The Notebook

    {route}

    The route moves from language to inspection. First we name the concepts, then we build one structural visual and one geometric visual, and finally we run a small applied lab. The lab is intentionally small enough to modify: change a point, a parameter, or a model assumption and rerun the cells. If the outcome changes in the expected way, the chapter's main distinction has become operational rather than merely verbal.
    """


def concept_markdown(item: dict[str, str], extra: dict[str, object]) -> str:
    story = ", ".join(extra["story"])
    return f"""
    ## Conceptual Core

    The visual sequence for this unit is organized around: {story}. The first artifact is a relationship map. It should be read as a proof or interpretation diagram: arrows mean that one idea gives usable structure to the next. The second artifact is geometric. It makes the chapter's main distinction visible as an object that can be inspected directly.

    For this unit the key idea is: {extra['claim']} That sentence has two sides. On the formal side, we need precise permissions: what can be constructed, copied, ordered, measured, or inferred. On the model side, we need examples that make the permissions believable without smuggling in facts from a stronger geometry. The danger is subtle. A Euclidean drawing can accidentally make a non-Euclidean theorem look false, while a hyperbolic model drawn inside the Euclidean plane can accidentally make a curved fact look like an ordinary flat one. The notebook keeps those layers separate.

    A useful working rule is this: a diagram may suggest, a model may interpret, a computation may test, but only the stated assumptions license a theorem. The artifacts below are built under that rule. They are meant to be inspected with a question in mind: which part of the picture is a convention of drawing, which part is an invariant of the model, and which part is a theorem waiting for proof?

    ## Standalone Study Notes

    The chapter can be studied as a sequence of contrasts. One contrast is between local construction and global structure. Local construction is what a ruler, compass, incidence rule, or congruence rule lets us do immediately. Global structure is what happens when those local permissions are repeated across the whole plane. The parallel problem is powerful precisely because it is global: it is not settled by staring at one short segment or one small triangle.

    A second contrast is between syntax and semantics. Syntax is the formal statement of an axiom or theorem. Semantics is a model in which the statement is interpreted. A finite incidence model, a Euclidean coordinate plane, a Poincare disk, a Klein disk, a sphere with antipodal identification, or a small grid without limiting points can all serve as semantic laboratories. When a theorem survives translation into many models, we gain confidence that the proof used only the intended assumptions. When it fails in a model, the failure is not noise; it is information about which assumption was missing.

    A third contrast is between measurement and proof. Measurement supplies evidence and intuition. Proof explains why the observation is forced by assumptions. This notebook keeps measurement visible because the subject is easy to misread without it. Angle sums, geodesic shapes, closure tables, and model maps are all chosen so that the reader can see what the formal language is trying to protect.
    """


def definitions_markdown(details: dict[str, object]) -> str:
    definition_lines = "\n".join(f"- **{name}.** {body}." for name, body in details["definitions"])
    equation_lines = "\n".join(f"- `${equation}$`" for equation in details["equations"])
    return f"""
    ## Definition Bank And Equations

    {definition_lines}

    The definitions above are the local vocabulary for this notebook. They are intentionally stated in operational language because the goal is to connect the synthetic discussion to artifacts that can be inspected and rerun. A reader should be able to point to a plotted object, model table, or numerical check and say which definition it is representing.

    The equations or symbolic checks used in this unit are:

    {equation_lines}

    These formulas are not a substitute for the synthetic proofs. They are a compact way to make the chapter's claims testable. When a formula appears again in a sanity check, it is being used as a consistency witness for the artifact, not as copied textbook prose.
    """


def worked_example_markdown(details: dict[str, object]) -> str:
    return f"""
    ## Worked Example

    {details['worked']}

    To read this as a proof exercise, separate the construction from the inference. The construction tells us which objects are present. The inference tells us which relation is licensed by the definitions or axioms. The computational version mirrors that separation: first the code creates a model or diagram, then the final check records the invariant that should survive rerunning the notebook.
    """


def lab_markdown() -> str:
    return """
    ## Applied Lab

    The lab turns the chapter's main contrast into a small experiment. Treat the plotted quantity as a diagnostic rather than as a final theorem. The point is to learn what would change if the underlying geometry or axiom choice changed. For example, a parallel-count plot separates Euclidean, hyperbolic, and elliptic behavior; a closure table checks whether transformations stay inside a proposed symmetry set; a defect plot translates the statement "angle sum is less than two right angles" into a measurable area rule.

    When adapting the lab, change one assumption at a time. In synthetic geometry, changing two assumptions at once often hides the reason a conclusion failed. In computational work the same discipline appears as a small parameter sweep or a finite model table. The table or curve is not the proof, but it is a compact way to see where the proof should look.
    """


def takeaways_markdown(extra: dict[str, object]) -> str:
    return f"""
    ## Takeaways

    - The main standalone lesson is: {extra['claim']}
    - The structural artifact records the dependency or interpretation pattern; the geometric artifact records what the pattern looks like in a concrete model.
    - The applied lab is a reusable check: it lets a reader perturb a parameter and watch which conclusion is stable.
    - The source span supplies orientation, but the course notebook supplies its own definitions, examples, visuals, and sanity checks.

    A good next reading move is to reopen the earlier notebooks whenever a later model seems visually surprising. Most surprises in non-Euclidean geometry are not caused by a single strange diagram; they come from moving a familiar proof step into a world where one hidden assumption has been removed or replaced.
    """


def notebook_for(item: dict[str, str]):
    extra = EXTRA[item["number"]]
    details = DETAILS[item["number"]]
    cells = [
        markdown(intro_markdown(item, extra)),
        code(
            f"""
            from pathlib import Path
            import sys

            import numpy as np

            for candidate in [Path.cwd(), *Path.cwd().parents]:
                if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
                    BOOK_ROOT = candidate
                    break
            else:
                raise RuntimeError("Could not locate BOOK_ROOT")

            if str(BOOK_ROOT) not in sys.path:
                sys.path.insert(0, str(BOOK_ROOT))

            from utils.artifacts import assert_artifacts, display_artifact, save_json
            from utils.axioms import AXIOM_FAMILIES, DEPENDENCIES, MODEL_DICTIONARY
            from utils.chapter_visuals import chapter_sanity, save_lab, save_relationship_map, save_scene

            TOPIC = {item['folder']!r}
            ARTIFACT_DIR = BOOK_ROOT / "artifacts" / TOPIC
            ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
            print(f"Writing artifacts to {{ARTIFACT_DIR.relative_to(BOOK_ROOT)}}")
            """
        ),
        markdown(concept_markdown(item, extra)),
        markdown(definitions_markdown(details)),
        markdown(worked_example_markdown(details)),
        code(
            f"""
            chapter_profile = {{
                "title": {item['title']!r},
                "source_printed_pages": {item['printed']!r},
                "source_pdf_pages": {item['pdf']!r},
                "visual_center": {item['focus']!r},
                "chapter_question": {extra['question']!r},
                "translation": {extra['translation']!r},
                "route": {extra['route']!r},
                "relationship_labels": {extra['story']!r},
                "scene_kind": {extra['scene']!r},
                "lab_kind": {extra['lab']!r},
                "sanity_kind": {extra['scene']!r},
                "artifact_names": {details['artifacts']!r},
            }}
            chapter_profile
            """
        ),
        markdown(
            """
            ## Visual Storyboard

            The storyboard chooses a compact set of generated artifacts for this chapter. The relationship map provides a view of proof or interpretation structure. The geometric scene gives an inspectable construction, model, or surface. The lab plot records a numerical or finite diagnostic. Each artifact filename names the concept it carries, and each artifact is regenerated from code so the reader can modify it.
            """
        ),
        code(
            """
            relationship_path = ARTIFACT_DIR / chapter_profile["artifact_names"]["relationship"]
            save_relationship_map(chapter_profile["relationship_labels"], relationship_path, chapter_profile["title"] + ": structure")
            display_artifact(relationship_path)
            """
        ),
        code(
            """
            geometry_path = ARTIFACT_DIR / chapter_profile["artifact_names"]["scene"]
            save_scene(chapter_profile["scene_kind"], geometry_path)
            display_artifact(geometry_path)
            """
        ),
        markdown(lab_markdown()),
        code(
            """
            lab_path = ARTIFACT_DIR / chapter_profile["artifact_names"]["lab"]
            save_lab(chapter_profile["lab_kind"], lab_path)
            display_artifact(lab_path)
            """
        ),
        markdown(
            """
            ## Sanity Checks

            The checks below make the notebook auditable. They assert that the visual artifacts exist, record a few small invariants, and save a JSON summary next to the images. These values are intentionally simple: they are there to catch stale paths, blank artifacts, and broken helper functions before a reader encounters them.
            """
        ),
        code(
            """
            final_sanity = {
                "topic": TOPIC,
                "artifact_count": 3,
                "axiom_family_count": len(AXIOM_FAMILIES),
                "model_dictionary_count": len(MODEL_DICTIONARY),
                "dependency_count": len(DEPENDENCIES),
            }
            final_sanity.update(chapter_sanity(chapter_profile["sanity_kind"]))
            sanity_path = save_json(final_sanity, ARTIFACT_DIR / "final-sanity.json")
            assert final_sanity["sanity_kind"] == chapter_profile["sanity_kind"]
            assert_artifacts([relationship_path, geometry_path, lab_path, sanity_path], min_bytes=64)
            final_sanity
            """
        ),
        markdown(takeaways_markdown(extra)),
    ]
    return new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
    )


def main() -> None:
    for item in SOURCE_MAP:
        path = BOOK_ROOT / item["folder"] / item["notebook"]
        nbformat.write(notebook_for(item), path)
        print(f"wrote {path.relative_to(BOOK_ROOT)}")


if __name__ == "__main__":
    main()
