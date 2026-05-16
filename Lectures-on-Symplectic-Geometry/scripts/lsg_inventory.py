"""Lecture inventory and source map for Ana Cannas da Silva's notes."""

from __future__ import annotations

import argparse
import json
import re
from typing import Any

PDF_SOURCE = "Lectures on Symplectic Geometry.pdf"
PDF_PAGE_COUNT = 223
BODY_PAGE_OFFSET = 14

SOURCE_SPAN_NOTES = [
    "The PDF table of contents was read from the local source file.",
    "Arabic printed body pages map to physical PDF pages by adding 14.",
    "Lecture spans include the homework section that closes the lecture when the table of contents places one before the next lecture or part.",
    "References begin on printed page 197 / physical PDF page 211; the index begins on printed page 203 / physical PDF page 217.",
]

PARTS: list[dict[str, str]] = [
    {"folder": "part-01-introduction", "title": "Part I: Introduction", "description": "Symplectic forms, first examples, and cotangent bundles."},
    {"folder": "part-02-symplectomorphisms", "title": "Part II: Symplectomorphisms", "description": "Lagrangian submanifolds, generating functions, and recurrence."},
    {"folder": "part-03-local-forms", "title": "Part III: Local Forms", "description": "Isotopies, Moser's method, Darboux normal form, and Weinstein neighborhoods."},
    {"folder": "part-04-contact-manifolds", "title": "Part IV: Contact Manifolds", "description": "Contact forms, Reeb fields, and symplectization."},
    {"folder": "part-05-compatible-almost-complex-structures", "title": "Part V: Compatible Almost Complex Structures", "description": "Compatible complex structures, triples, and Dolbeault decompositions."},
    {"folder": "part-06-kahler-manifolds", "title": "Part VI: Kahler Manifolds", "description": "Complex manifolds, Kahler forms, Hodge restrictions, and examples."},
    {"folder": "part-07-hamiltonian-mechanics", "title": "Part VII: Hamiltonian Mechanics", "description": "Hamiltonian vector fields, variational principles, and Legendre transform."},
    {"folder": "part-08-moment-maps", "title": "Part VIII: Moment Maps", "description": "Group actions, Hamiltonian actions, and first moment-map examples."},
    {"folder": "part-09-symplectic-reduction", "title": "Part IX: Symplectic Reduction", "description": "Marsden-Weinstein-Meyer reduction and conservation principles."},
    {"folder": "part-10-moment-maps-revisited", "title": "Part X: Moment Maps Revisited", "description": "Gauge-theoretic moment maps, existence, uniqueness, and convexity."},
    {"folder": "part-11-symplectic-toric-manifolds", "title": "Part XI: Symplectic Toric Manifolds", "description": "Delzant classification, construction, and Duistermaat-Heckman variation."},
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return re.sub(r"-+", "-", slug)


def pdf_span(printed_span: str) -> str:
    first, last = [int(piece) for piece in printed_span.split("-")]
    return f"{first + BODY_PAGE_OFFSET}-{last + BODY_PAGE_OFFSET}"


def entry(
    number: int,
    part: str,
    title: str,
    printed_span: str,
    focus: str,
    sections: list[str],
    concepts: list[str],
    visual: str,
    lab: str,
    theme: str,
    proof: str,
) -> dict[str, Any]:
    slug = slugify(title)
    return {
        "kind": "lecture",
        "number": number,
        "label": f"Lecture {number:02d}",
        "part": part,
        "title": title,
        "folder": f"lecture-{number:02d}-{slug}",
        "notebook": f"{number:02d}-{slug}.ipynb",
        "printed_span": printed_span,
        "pdf_span": pdf_span(printed_span),
        "focus": focus,
        "sections": sections,
        "concepts": concepts,
        "visual": visual,
        "lab": lab,
        "theme": theme,
        "proof": proof,
        "artifact_topic": f"lecture-{number:02d}",
    }


ENTRIES: list[dict[str, Any]] = [
    entry(1, "part-01-introduction", "Symplectic Forms", "1-6", "Builds the linear and manifold definition of a symplectic form from skew-symmetric bilinear algebra.", ["Skew-symmetric bilinear maps", "Symplectic vector spaces", "Symplectic manifolds", "Symplectomorphisms"], ["standard form for a skew map", "symplectic basis", "nondegenerate two-form", "Darboux chart preview"], "matrix normal form and area-pair basis diagram", "Classify random skew matrices by rank and check when the induced form is nondegenerate.", "linear", "Track the standard-form theorem as a finite algorithm: split the kernel, pair directions, and test the matrix residual."),
    entry(2, "part-01-introduction", "Symplectic Form on the Cotangent Bundle", "7-12", "Introduces the tautological one-form and canonical symplectic form on a cotangent bundle.", ["Cotangent bundle", "Tautological and canonical forms in coordinates", "Coordinate-free definitions", "Naturality"], ["cotangent coordinates", "tautological one-form", "canonical two-form", "naturality under lifted maps"], "cotangent fibers and canonical-form grid", "Compute alpha and omega on a simple cotangent bundle and verify coordinate-free pullback behavior.", "cotangent", "Use the projection diagram to show why the same one-form appears in every coordinate chart."),
    entry(3, "part-02-symplectomorphisms", "Lagrangian Submanifolds", "13-19", "Recasts symplectomorphisms as Lagrangian graphs and explains graphs of closed one-forms in cotangent bundles.", ["Submanifolds", "Lagrangian submanifolds of T*X", "Conormal bundles", "Application to symplectomorphisms"], ["Lagrangian condition", "closed one-form graph", "conormal bundle", "twisted product form"], "closed one-form graph and conormal slice", "Check that the graph of df is Lagrangian and that a conormal bundle kills the tautological form.", "lagrangian", "Follow pullbacks of the tautological form through the graph inclusion until the condition becomes dmu=0."),
    entry(4, "part-02-symplectomorphisms", "Generating Functions", "20-26", "Uses generating functions to manufacture Lagrangian graphs and hence symplectomorphisms.", ["Constructing symplectomorphisms", "Method of generating functions", "Application to geodesic flow"], ["twisted graph", "generating function", "mixed Hessian", "geodesic flow"], "contours of a generating function and the induced twist map", "Vary a quadratic generating function and check the symplectic residual of the resulting map.", "generating", "The proof view is a three-step route: exact graph, twist, projection test."),
    entry(5, "part-02-symplectomorphisms", "Recurrence", "27-32", "Connects symplectic area preservation with periodic points, billiards, and Poincare recurrence.", ["Periodic points", "Billiards", "Poincare recurrence"], ["area-preserving map", "billiard return map", "recurrence", "periodic point"], "billiard chords and recurrence histogram", "Simulate a simple area-preserving rotation and estimate first return times to a window.", "recurrence", "Treat recurrence as a measure bookkeeping theorem rather than as a pointwise convergence claim."),
    entry(6, "part-03-local-forms", "Preparation for the Local Theory", "33-39", "Assembles isotopies, vector fields, tubular neighborhoods, and the homotopy formula needed for Moser arguments.", ["Isotopies and vector fields", "Tubular neighborhood theorem", "Homotopy formula"], ["time-dependent vector field", "tubular neighborhood", "flow box", "Cartan homotopy formula"], "flowbox with normal disk fibers", "Numerically compare a finite-flow deformation with the infinitesimal vector field that generates it.", "local", "Make Cartan's formula visible as a balance between derivative along a flow and exterior algebra operations."),
    entry(7, "part-03-local-forms", "Moser Theorems", "40-43", "Develops Moser's trick as a controlled deformation of symplectic forms by solving for a vector field.", ["Equivalence of symplectic structures", "Moser trick", "Moser local theorem"], ["isotopy", "cohomologous forms", "Moser vector field", "volume constraint"], "Moser density interpolation and vector-field arrows", "Interpolate two equal-volume area forms and solve the one-dimensional Moser equation in a toy model.", "moser", "The invariant tracker is the derivative of phi_t^* omega_t; the chosen vector field cancels it."),
    entry(8, "part-03-local-forms", "Darboux-Moser-Weinstein Theory", "44-48", "Proves local symplectic normal forms and relates Lagrangian neighborhoods to cotangent models.", ["Classical Darboux theorem", "Lagrangian subspaces", "Weinstein Lagrangian neighborhood theorem"], ["Darboux chart", "Lagrangian subspace", "cotangent model", "local normal form"], "Darboux deformation ellipses and Lagrangian plane family", "Track a path of nondegenerate forms and verify that the final chart has the standard matrix.", "darboux", "The proof is a local Moser argument with a linear algebra anchor at the point or Lagrangian."),
    entry(9, "part-03-local-forms", "Weinstein Tubular Neighborhood Theorem", "49-54", "Applies local models to symplectic tubular neighborhoods, symplectomorphism groups, and fixed points.", ["Linear algebra observation", "Tubular neighborhoods", "Tangent space to the symplectomorphism group", "Fixed points of symplectomorphisms"], ["symplectic normal bundle", "graph near diagonal", "closed one-form tangent model", "fixed-point intersection"], "graph-near-diagonal fixed-point detector", "Represent a near-identity map by its graph and test when it is Lagrangian in the twisted product.", "darboux", "Translate fixed points into intersections of a graph with the diagonal, then use local Lagrangian coordinates."),
    entry(10, "part-04-contact-manifolds", "Contact Forms", "55-60", "Introduces maximally nonintegrable hyperplane fields and first contact examples.", ["Contact structures", "Examples", "First properties"], ["contact form", "contact distribution", "maximal nonintegrability", "local normal form"], "contact planes twisting along a curve", "Evaluate alpha wedge d alpha in the standard R3 model and compare it with an integrable plane field.", "contact", "The proof view is a Frobenius failure meter: planes twist enough that alpha wedge d alpha never vanishes."),
    entry(11, "part-04-contact-manifolds", "Contact Dynamics", "61-64", "Studies Reeb fields, symplectization, and the dynamical conjectures that motivate contact geometry.", ["Reeb vector fields", "Symplectization", "Seifert and Weinstein conjectures"], ["Reeb vector field", "symplectization", "periodic orbit", "contact energy level"], "Reeb flow helix and symplectization layer", "Compute the Reeb vector field for a standard contact form and plot representative flow lines.", "contact", "Reeb dynamics are isolated by two equations: alpha(R)=1 and i_R d alpha=0."),
    entry(12, "part-05-compatible-almost-complex-structures", "Almost Complex Structures", "65-71", "Compares symplectic, metric, and almost-complex linear structures and the compatibility conditions between them.", ["Three geometries", "Complex structures on vector spaces", "Compatible structures"], ["almost complex structure", "J squared equals minus identity", "compatible metric", "positive tame form"], "compatibility matrix triangle", "Construct J from the standard symplectic matrix and verify J^2=-I and positive g(u,v)=omega(u,Jv).", "complex", "Compatibility is checked by closing a triangle: any two of omega, J, and g determine the third under positivity."),
    entry(13, "part-05-compatible-almost-complex-structures", "Compatible Triples", "72-75", "Packages symplectic forms, metrics, and complex structures into mutually determining compatible triples.", ["Compatibility", "Triple of structures", "First consequences"], ["compatible triple", "Hermitian metric", "contractible choice", "orthogonality"], "omega-J-g reconstruction diagram", "Perturb a compatible complex structure and measure whether the induced metric remains symmetric positive.", "complex", "The invariant scaffold records which identities are algebraic and which depend on positivity."),
    entry(14, "part-05-compatible-almost-complex-structures", "Dolbeault Theory", "76-80", "Introduces type decompositions of forms and the Dolbeault operators for almost complex and complex settings.", ["Splittings", "Forms of type (l,m)", "J-holomorphic functions", "Dolbeault cohomology"], ["type decomposition", "partial and dbar", "J-holomorphic function", "Dolbeault cohomology"], "bigraded form lattice with operator arrows", "Use symbolic z and zbar coordinates to check which simple functions are killed by dbar.", "complex", "The proof diagram is a bigraded lattice: d splits into components whose squares encode integrability."),
    entry(15, "part-06-kahler-manifolds", "Complex Manifolds", "81-87", "Moves from almost complex linear algebra to holomorphic charts and differential forms on complex manifolds.", ["Complex charts", "Forms on complex manifolds", "Differentials"], ["holomorphic atlas", "complex coordinates", "forms of type", "complex projective space"], "two-chart atlas for CP1 and type decomposition", "Compute the transition map between stereographic charts and verify holomorphic behavior away from overlap poles.", "complex", "A chart-transition graph separates topological atlas data from holomorphic restrictions."),
    entry(16, "part-06-kahler-manifolds", "Kahler Forms", "88-95", "Builds Kahler forms from compatible triples and potentials, including the Fubini-Study model.", ["Kahler forms", "An application", "Recipe to obtain Kahler forms", "Local canonical form"], ["Kahler form", "Kahler potential", "Fubini-Study form", "local canonical coordinates"], "Kahler potential contours and Fubini-Study density", "Differentiate a radial potential and verify positivity of the associated Hermitian form.", "kahler", "The invariant tracker is closedness plus positivity: d omega=0 is automatic from a potential, while eigenvalues detect positivity."),
    entry(17, "part-06-kahler-manifolds", "Compact Kahler Manifolds", "96-102", "Explains Hodge-theoretic restrictions and compares compact Kahler examples with symplectic nonexamples.", ["Hodge theory", "Immediate topological consequences", "Compact examples and counterexamples", "Main Kahler manifolds"], ["Hodge diamond", "Betti parity", "Kodaira-Thurston contrast", "projective examples"], "Hodge diamond and topology ledger", "Build small Hodge diamonds and check the evenness constraints they impose on Betti numbers.", "kahler", "The proof view is a ledger of topological invariants forced by the Hodge decomposition."),
    entry(18, "part-07-hamiltonian-mechanics", "Hamiltonian Vector Fields", "103-110", "Defines Hamiltonian and symplectic vector fields and connects them to mechanics, brackets, and integrable systems.", ["Hamiltonian and symplectic vector fields", "Classical mechanics", "Brackets", "Integrable systems"], ["Hamiltonian vector field", "Poisson bracket", "energy conservation", "integrable system"], "phase portrait with Hamiltonian level sets", "Integrate the harmonic oscillator and check that the Poisson bracket with its Hamiltonian vanishes.", "hamiltonian", "The identity i_X omega=dH becomes visible because X_H is tangent to level curves of H."),
    entry(19, "part-07-hamiltonian-mechanics", "Variational Principles", "111-118", "Relates equations of motion to least action, Euler-Lagrange equations, and minimizing behavior.", ["Equations of motion", "Principle of least action", "Variational problems", "Euler-Lagrange equations", "Minimizing properties"], ["action functional", "Euler-Lagrange equation", "geodesic minimizer", "first variation"], "path-action comparison and residual plot", "Compare nearby polygonal paths and verify that the straight path has zero first-variation residual.", "variational", "The proof scaffold turns a family of paths into an action curve and reads the derivative at zero."),
    entry(20, "part-07-hamiltonian-mechanics", "Legendre Transform", "119-124", "Uses strict convexity to pass between Lagrangian and Hamiltonian descriptions.", ["Strict convexity", "Legendre transform", "Application to variational problems"], ["strict convexity", "dual variables", "Fenchel inequality", "Hamiltonian from Lagrangian"], "convex graph with tangent slopes and dual curve", "Compute the Legendre transform of a quadratic-plus-quartic model and check Fenchel equality at the matching slope.", "legendre", "The invariant is dual contact: p=dL/dv selects the tangent line that supports the convex graph."),
    entry(21, "part-08-moment-maps", "Actions", "125-130", "Introduces one-parameter groups, Lie group actions, symplectic and Hamiltonian actions, and adjoint/coadjoint representations.", ["One-parameter groups", "Lie groups", "Smooth actions", "Symplectic and Hamiltonian actions", "Adjoint and coadjoint representations"], ["group action", "infinitesimal generator", "symplectic action", "coadjoint orbit"], "orbits and infinitesimal generators for a circle action", "Plot a circle action on the plane and check that the infinitesimal generator preserves the standard form.", "actions", "The proof view separates global group motion from the infinitesimal vector field it differentiates to."),
    entry(22, "part-08-moment-maps", "Hamiltonian Actions", "131-138", "Defines moment and comoment maps, previews reduction, and works through classical Hamiltonian action examples.", ["Moment and comoment maps", "Orbit spaces", "Preview of reduction", "Classical examples"], ["moment map", "comoment map", "orbit space", "coadjoint orbit example"], "moment-map fibers for circle and torus actions", "Verify d<mu,xi>=i_X omega for the standard circle action on C.", "moment", "A moment map is a readable certificate that infinitesimal symmetry is Hamiltonian."),
    entry(23, "part-09-symplectic-reduction", "The Marsden-Weinstein-Meyer Theorem", "139-144", "States and proves the main regular-level reduction theorem.", ["Statement", "Ingredients", "Proof of the theorem"], ["regular value", "level set", "group orbit", "reduced symplectic form"], "level set quotient and dimension count", "Check the dimension formula for a free circle action and identify the kernel directions of the restricted form.", "reduction", "The proof is a kernel calculation: the directions killed by restricted omega are exactly the group orbit directions."),
    entry(24, "part-09-symplectic-reduction", "Reduction", "145-152", "Explores Noether's principle, elementary reduction, product groups, other levels, and orbifold warnings.", ["Noether principle", "Elementary reduction", "Product groups", "Reduction at other levels", "Orbifolds"], ["Noether conserved quantity", "product reduction", "shifted level", "orbifold quotient"], "conserved level slices and quotient fibers", "Run a toy reduction of C2 by a circle and inspect how different levels change the reduced space.", "reduction", "The invariant scaffold keeps the conserved moment value fixed while quotienting redundant group directions."),
    entry(25, "part-10-moment-maps-revisited", "Moment Map in Gauge Theory", "153-161", "Reinterprets curvature of connections as a moment map for gauge-group action.", ["Connections on a principal bundle", "Connection and curvature forms", "Symplectic structure on the space of connections", "Action of the gauge group", "Case of circle bundles"], ["connection", "curvature", "gauge action", "moment map as curvature"], "discrete connection grid and curvature cells", "Use a square lattice connection toy model and verify that curvature changes by a boundary term under a gauge shift.", "gauge", "The proof diagram upgrades finite-dimensional moment-map logic to an affine space of connections."),
    entry(26, "part-10-moment-maps-revisited", "Existence and Uniqueness of Moment Maps", "162-167", "Uses Lie algebra cohomology to organize obstructions and uniqueness for moment maps.", ["Lie algebras of vector fields", "Lie algebra cohomology", "Existence of moment maps", "Uniqueness of moment maps"], ["Lie algebra cocycle", "Hamiltonian obstruction", "equivariant moment map", "constant ambiguity"], "cocycle obstruction ledger", "Compute a small Chevalley-Eilenberg-style coboundary table for an abelian example and check when ambiguity is constant.", "cohomology", "The proof view isolates two questions: does each infinitesimal action have a Hamiltonian, and do the Hamiltonians respect brackets?"),
    entry(27, "part-10-moment-maps-revisited", "Convexity", "168-174", "Presents convexity of moment-map images for torus actions and examples of effective actions.", ["Convexity theorem", "Effective actions", "Examples"], ["Atiyah-Guillemin-Sternberg convexity", "effective torus action", "fixed-point image", "moment polytope"], "fixed-point images and convex hull", "Sample a torus action on CP2 and verify that the moment image lies inside the convex hull of fixed points.", "moment", "Convexity is visualized as a global theorem forced by local normal forms near fixed points."),
    entry(28, "part-11-symplectic-toric-manifolds", "Classification of Symplectic Toric Manifolds", "175-180", "States Delzant polytopes and the classification theorem for compact symplectic toric manifolds.", ["Delzant polytopes", "Delzant theorem", "Sketch of Delzant construction"], ["Delzant polytope", "primitive normal", "smooth vertex", "toric classification"], "Delzant polygons with primitive normal checks", "Compute adjacent normal determinants for triangle and square polytopes and flag a nonsmooth corner.", "toric", "The proof scaffold turns geometry into combinatorics: compact toric manifolds are encoded by labeled smooth polytopes."),
    entry(29, "part-11-symplectic-toric-manifolds", "Delzant Construction", "181-188", "Builds the toric manifold from a Delzant polytope via a quotient construction.", ["Algebraic set-up", "The zero-level", "Conclusion of the construction", "Idea behind the construction"], ["facet map", "kernel torus", "zero level", "quotient construction"], "facet inequalities and quotient dimension flow", "Construct the matrix of inward normals for a triangle and verify the quotient dimension count.", "toric", "The proof diagram follows data through exact sequences, a moment level, and the final quotient."),
    entry(30, "part-11-symplectic-toric-manifolds", "Duistermaat-Heckman Theorems", "189-196", "Describes how reduced symplectic volume varies polynomially with the moment-map level.", ["Duistermaat-Heckman polynomial", "Local form for reduced spaces", "Variation of symplectic volume"], ["reduced volume", "piecewise polynomial", "equivariant local form", "volume variation"], "reduced-volume curve across moment levels", "Compute a CP1/CP2 toy volume density and check its piecewise polynomial behavior.", "dh", "The invariant tracker is the pushforward of symplectic volume along the moment map."),
]


def inventory() -> dict[str, Any]:
    return {
        "pdf_source": PDF_SOURCE,
        "pdf_page_count": PDF_PAGE_COUNT,
        "body_page_offset": BODY_PAGE_OFFSET,
        "source_span_notes": SOURCE_SPAN_NOTES,
        "parts": PARTS,
        "entries": ENTRIES,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = inventory()
    if args.json:
        print(json.dumps(data, indent=2))
        return
    for entry_data in ENTRIES:
        print(f"{entry_data['label']}: {entry_data['title']} | printed {entry_data['printed_span']} | PDF {entry_data['pdf_span']}")


if __name__ == "__main__":
    main()
