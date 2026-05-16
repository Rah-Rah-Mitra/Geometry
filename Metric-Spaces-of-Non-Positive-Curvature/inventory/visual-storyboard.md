# Visualization Storyboard

## I.1 Basic Concepts
- Chapter goal: Build the dictionary from distance to geodesic behavior, then turn angle and length into measurable notebook objects.
- Source span read: printed 2-14 / PDF 21-33
- Visual sequence: `i-01-metric-geodesic-angle-dashboard.png`, `i-01-metric-geodesic-angle-dashboard-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a dependency graph to show how the triangle inequality supports length, midpoint, geodesic, and angle comparisons.

## I.2 The Model Spaces
- Chapter goal: Treat E^n, S^n, and H^n as measuring instruments for later CAT(k) comparisons.
- Source span read: printed 15-31 / PDF 34-50
- Visual sequence: `i-02-model-space-comparison-triangle.png`, `i-02-model-space-comparison-triangle-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Place one side-length triple into all admissible models and compare angle and midpoint data.

## I.3 Length Spaces
- Chapter goal: Turn curves into distances and separate induced metrics from intrinsic length metrics.
- Source span read: printed 32-46 / PDF 51-65
- Visual sequence: `i-03-length-space-intrinsic-distance.png`, `i-03-length-space-intrinsic-distance-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Track how a distance defined by infimum over curves changes under completion, covering, and compactness hypotheses.

## I.4 Normed Spaces
- Chapter goal: Use norm balls to see exactly when straight segments are unique geodesics.
- Source span read: printed 47-55 / PDF 66-74
- Visual sequence: `i-04-norm-ball-geodesic-uniqueness.png`, `i-04-norm-ball-geodesic-uniqueness-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Represent equality in the triangle inequality as flat spots on the unit ball.

## I.5 Some Basic Constructions
- Chapter goal: Assemble new geodesic spaces and record which metric features survive the operation.
- Source span read: printed 56-80 / PDF 75-99
- Visual sequence: `i-05-construction-survival-map.png`, `i-05-construction-survival-map-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a construction flow chart with invariant ledgers for geodesic existence, completeness, and curvature input.

## I.6 More on the Geometry of H^n
- Chapter goal: Compare hyperbolic models so geodesics, boundary points, and isometries can be moved between coordinates.
- Source span read: printed 81-96 / PDF 100-115
- Visual sequence: `i-06-hyperbolic-model-coordinate-dictionary.png`, `i-06-hyperbolic-model-coordinate-dictionary-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Show the same ideal chord and geodesic in two models and track which straight lines become circular arcs.

## I.7 M_k-Polyhedral Complexes
- Chapter goal: Make piecewise constant curvature complexes inspectable through cells, links, and local geodesic tests.
- Source span read: printed 97-122 / PDF 116-141
- Visual sequence: `i-07-polyhedral-link-neighborhood.png`, `i-07-polyhedral-link-neighborhood-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Pair a cell complex view with a link view so local metric statements become finite combinatorial checks.

## I.7 Appendix Metrizing Abstract Simplicial Complexes
- Chapter goal: Turn combinatorial incidence data into a metric realization without smuggling in a picture.
- Source span read: printed 123-130 / PDF 142-149
- Visual sequence: `app-i-07-abstract-simplex-metric-realization.png`, `app-i-07-abstract-simplex-metric-realization-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use an incidence-to-coordinate pipeline and verify that shared faces receive the same metric data.

## I.8 Group Actions and Quasi-Isometries
- Chapter goal: Translate coarse group data into metric actions and quasi-isometry invariants.
- Source span read: printed 131-152 / PDF 150-171
- Visual sequence: `i-08-cayley-action-quasi-isometry-lab.png`, `i-08-cayley-action-quasi-isometry-lab-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use Cayley graphs and orbit maps to show how algebra becomes a large-scale metric object.

## I.8 Appendix Combinatorial 2-Complexes
- Chapter goal: Represent a group presentation as a two-dimensional space whose loops remember relations.
- Source span read: printed 153-156 / PDF 172-175
- Visual sequence: `app-i-08-presentation-complex-relation-loops.png`, `app-i-08-presentation-complex-relation-loops-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw a presentation complex and label how each relator becomes a 2-cell boundary.

## II.1 Definitions and Characterizations of CAT(k) Spaces
- Chapter goal: Make the CAT(k) inequality operational by comparing every chord in a geodesic triangle with its model counterpart.
- Source span read: printed 158-168 / PDF 177-187
- Visual sequence: `ii-01-cat-k-comparison-inequality.png`, `ii-01-cat-k-comparison-inequality-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a triangle dashboard where moving two comparison points updates the tested chord inequality.

## II.1 Appendix The Curvature of Riemannian Manifolds
- Chapter goal: Connect the metric CAT language back to sectional curvature without requiring tensor fluency.
- Source span read: printed 169-174 / PDF 188-193
- Visual sequence: `app-ii-01-sectional-curvature-to-cat-k.png`, `app-ii-01-sectional-curvature-to-cat-k-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a surface patch with two geodesic spreads and compare second-order triangle behavior.

## II.2 Convexity and Its Consequences
- Chapter goal: Use CAT(0) convexity to make projection, center, and flatness statements computationally checkable.
- Source span read: printed 175-183 / PDF 194-202
- Visual sequence: `ii-02-cat0-convex-projection-center.png`, `ii-02-cat0-convex-projection-center-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Track squared-distance convexity along a geodesic and show why nearest-point projection is forced.

## II.3 Angles, Limits, Cones and Joins
- Chapter goal: Build tangent-like information from directions, cones, joins, and stable comparison angles.
- Source span read: printed 184-192 / PDF 203-211
- Visual sequence: `ii-03-space-of-directions-cone-join.png`, `ii-03-space-of-directions-cone-join-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Show rays leaving a point, identify their angle metric, and compare the cone built from those directions.

## II.4 The Cartan-Hadamard Theorem
- Chapter goal: Expose the mechanism that turns local upper curvature bounds into global CAT(k) control on the universal cover.
- Source span read: printed 193-204 / PDF 212-223
- Visual sequence: `ii-04-cartan-hadamard-patchwork-lift.png`, `ii-04-cartan-hadamard-patchwork-lift-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use overlapping CAT neighborhoods and lifted triangles to visualize why simply connected patching removes monodromy.

## II.5 M_k-Polyhedral Complexes of Bounded Curvature
- Chapter goal: Turn upper curvature in a polyhedral complex into the link condition and then into examples.
- Source span read: printed 205-227 / PDF 224-246
- Visual sequence: `ii-05-link-condition-flag-complex-test.png`, `ii-05-link-condition-flag-complex-test-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw a vertex star and its link side by side, then mark loops whose length certifies or violates CAT(0).

## II.6 Isometries of CAT(0) Spaces
- Chapter goal: Classify isometries by displacement and connect translation behavior to product splitting.
- Source span read: printed 228-243 / PDF 247-262
- Visual sequence: `ii-06-displacement-functions-isometry-types.png`, `ii-06-displacement-functions-isometry-types-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Plot displacement profiles for sample actions and identify minima, axes, and constant-translation behavior.

## II.7 The Flat Torus Theorem
- Chapter goal: Show how commuting semisimple isometries carve Euclidean flats out of a CAT(0) action.
- Source span read: printed 244-259 / PDF 263-278
- Visual sequence: `ii-07-flat-torus-minset-grid.png`, `ii-07-flat-torus-minset-grid-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a lattice of commuting translations and a product minset diagram to see why a flat appears.

## II.8 The Boundary at Infinity of a CAT(0) Space
- Chapter goal: Construct the boundary from geodesic rays and compare cone-topology and horofunction viewpoints.
- Source span read: printed 260-276 / PDF 279-295
- Visual sequence: `ii-08-cat0-boundary-rays-horoballs.png`, `ii-08-cat0-boundary-rays-horoballs-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw rays based at different points and show how bounded-distance classes become the same ideal point.

## II.9 The Tits Metric and Visibility Spaces
- Chapter goal: Put a metric on ideal directions and use it to detect flats, splittings, and visibility behavior.
- Source span read: printed 277-298 / PDF 296-317
- Visual sequence: `ii-09-tits-boundary-visibility-flats.png`, `ii-09-tits-boundary-visibility-flats-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Compare ideal angle data in a flat plane with the angle data in a negatively curved visibility example.

## II.10 Symmetric Spaces
- Chapter goal: Use symmetric spaces as high-rank CAT(0) laboratories with flats, Weyl chambers, and building-like boundaries.
- Source span read: printed 299-341 / PDF 318-360
- Visual sequence: `ii-10-symmetric-space-flats-weyl-chambers.png`, `ii-10-symmetric-space-flats-weyl-chambers-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Represent diagonal positive-definite matrices as a flat and mark Weyl chamber walls created by eigenvalue ordering.

## II.10 Appendix Spherical and Euclidean Buildings
- Chapter goal: Treat buildings as apartment systems where local chamber combinatorics controls global CAT geometry.
- Source span read: printed 342-346 / PDF 361-365
- Visual sequence: `app-ii-10-building-apartment-chamber-atlas.png`, `app-ii-10-building-apartment-chamber-atlas-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw overlapping apartments and record which chamber galleries can be folded by Weyl symmetries.

## II.11 Gluing Constructions
- Chapter goal: Track when gluing CAT(k) pieces preserves curvature and when a nonconvex seam breaks the comparison test.
- Source span read: printed 347-366 / PDF 366-385
- Visual sequence: `ii-11-convex-gluing-curvature-ledger.png`, `ii-11-convex-gluing-curvature-ledger-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Show a tree of pieces glued along convex subsets and contrast it with a seam where shortest paths kink incorrectly.

## II.12 Simple Complexes of Groups
- Chapter goal: Encode group stabilizer data over a stratified space and test curvature through the local development.
- Source span read: printed 367-396 / PDF 386-415
- Visual sequence: `ii-12-simple-complex-of-groups-development.png`, `ii-12-simple-complex-of-groups-development-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw the base stratification, attach local groups, and unfold one vertex into its local development.

## III.H delta-Hyperbolic Spaces
- Chapter goal: Compare negative-curvature large-scale behavior through slim triangles, isoperimetry, and boundary metrics.
- Source span read: printed 398-437 / PDF 417-456
- Visual sequence: `iii-h-slim-triangle-boundary-isoperimetry.png`, `iii-h-slim-triangle-boundary-isoperimetry-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a slim triangle overlay and a coarse filling ledger to connect hyperbolicity with linear area bounds.

## III.Gamma Non-Positive Curvature and Group Theory
- Chapter goal: Use non-positive curvature to make group-theoretic algorithms and subgroup phenomena geometric.
- Source span read: printed 438-518 / PDF 457-537
- Visual sequence: `iii-g-group-theory-dehn-distortion-dashboard.png`, `iii-g-group-theory-dehn-distortion-dashboard-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Tie normal forms, Dehn reduction, and subgroup distortion to visible paths in Cayley-type graphs.

## III.C Complexes of Groups
- Chapter goal: Upgrade simple complexes of groups to the full scwol language and follow fundamental groups through developments and coverings.
- Source span read: printed 519-572 / PDF 538-591
- Visual sequence: `iii-c-scwol-complex-of-groups-covering.png`, `iii-c-scwol-complex-of-groups-covering-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw the scwol, its local groups, twisting data, and the covering fibers that encode the universal construction.

## III.C Appendix Fundamental Groups and Coverings of Small Categories
- Chapter goal: Make category paths, loops, and covering fibers visible enough to support the complexes-of-groups chapter.
- Source span read: printed 573-583 / PDF 592-602
- Visual sequence: `app-iii-c-category-covering-monodromy.png`, `app-iii-c-category-covering-monodromy-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Use a directed covering diagram and lift a closed category path to read monodromy on the fiber.

## III.Q Groupoids of Local Isometries
- Chapter goal: Use groupoids to encode local isometries, orbifold charts, and developability through lifted geodesics.
- Source span read: printed 584-619 / PDF 603-638
- Visual sequence: `iii-q-local-isometry-groupoid-covering.png`, `iii-q-local-isometry-groupoid-covering-interactive.html`, `concept-routing.csv`.
- Proof visualization strategy: Draw local charts as objects, local isometries as arrows, and the lifted geodesic space used in the main theorem.
