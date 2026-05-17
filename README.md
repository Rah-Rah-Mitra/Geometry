# Geometry Notebook Roadmap

This repository is a growing library of standalone, visualization-first geometry
notebook courses. Each book folder turns a source text into an executable study
path with original prose, generated diagrams, computational experiments,
book-local artifacts, and sanity checks. The notebooks use source books for
structure and topic orientation; they do not redistribute textbook prose,
screenshots, page crops, or long exercise text.

The project is intentionally broad. Undergraduate geometry can stretch from
Euclidean, affine, projective, and non-Euclidean geometry into differential
geometry, topology, algebraic geometry, computational geometry, geometric
algebra, graphics, robotics, statistics on manifolds, information geometry, and
modern geometric machine learning. Graduate geometry then turns these languages
into separate ecosystems: manifolds, topology, Riemannian geometry, algebraic
and complex geometry, symplectic/contact geometry, metric geometry, convex and
discrete geometry, geometric group theory, geometric measure theory, optimal
transport, and geometric statistics.

## Status Legend

| Status | Meaning |
| --- | --- |
| Implemented | A book folder exists in this repo with notebook scaffolding or canonical notebooks. |
| Planned | The book is part of the roadmap, but no folder exists yet. |

Last updated: 2026-05-17

## What Each Notebook Course Entails

Each implemented book is treated as a self-contained course. A typical course
folder contains a `00-book-index.ipynb`, chapter or appendix folders, one
canonical teaching notebook per unit, and a local `00-index.ipynb` for navigation.
Generated figures, HTML labs, JSON checks, and other outputs live under
`artifacts/`. Course-specific helpers live in `utils/`, and validation or audit
commands live in `scripts/` when the course has them.

The intended reader should be able to learn from the notebooks without keeping
the source PDF open. That means each chapter should translate the book's ideas
into diagrams, equations, small simulations, numeric checks, and applied labs
that make the geometry inspectable.

## Implemented Courses

| Course | Status | What the notebooks cover |
| --- | --- | --- |
| [A Course in Metric Geometry](./A-Course-in-Metric-Geometry) | Implemented | Metric spaces, length spaces, constructions, curvature bounds, Gromov hyperbolicity, convergence, and Alexandrov spaces. |
| [A Mathematical Introduction to Robotic Manipulation](./A-Mathematical-Introduction-to-Robotic-Manipulation) | Implemented | Rigid-body motion, twists, wrenches, robot kinematics, dynamics, grasping, multifingered manipulation, nonholonomic motion, and Lie-theoretic robotics labs. |
| [Algebraic Geometry](./Algebraic-Geometry) | Implemented | Varieties, schemes, cohomology, curves, surfaces, sheaves, and projective algebraic geometry. |
| [An Introduction to Contact Topology](./An-Introduction-to-Contact-Topology) | Implemented | Contact manifolds, contact structures, knots in contact 3-manifolds, characteristic foliations, and contact-topology diagnostics. |
| [Basic Topology](./Basic-Topology) | Implemented | Euler characteristic, continuity, compactness, connectedness, quotient spaces, fundamental groups, triangulations, surfaces, simplicial homology, degree, Lefschetz number, knots, and covering spaces. |
| [Complex Geometry: An Introduction](./Complex-Geometry-An-Introduction) | Implemented | Holomorphic functions, complex manifolds, vector bundles, Kahler manifolds, sheaves, line bundles, and ddbar-formality intuition. |
| [Computational Geometry: Algorithms and Applications](./Computational-Geometry-Algorithms-and-Applications) | Implemented | Convex hulls, sweep-line algorithms, triangulations, Voronoi diagrams, arrangements, range search, motion planning, quadtrees, visibility, and robust geometric predicates. |
| [Computational Topology: An Introduction](./Computational-Topology-An-Introduction) | Implemented | Graphs, surfaces, complexes, homology, persistence, algorithms, and data-driven topological summaries. |
| [Convex Analysis](./Convex-Analysis) | Implemented | Convex sets and functions, separation, conjugacy, duality, optimization, minimax, Lagrange multipliers, and convex programs. |
| [Differential Geometry of Curves and Surfaces](./Differential-Geometry-of-Curves-and-Surfaces) | Implemented | Curves, regular surfaces, first fundamental forms, Gauss maps, Gaussian curvature, geodesics, intrinsic surface geometry, Gauss-Bonnet intuition, and global surface diagnostics. |
| [Differential Geometry: From Elastic Curves to Willmore Surfaces](./Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces) | Implemented | Curves, reparametrization, curvature, variational calculus, surface metrics, Stokes' theorem, Gauss-Bonnet, minimal surfaces, CMC surfaces, and Willmore energy. |
| [Directional Statistics](./Directional-Statistics) | Implemented | Circular and spherical data, von Mises and Fisher models, uniformity tests, regression, shape analysis, special functions, and executable replacements for statistical tables. |
| [Elementary Differential Geometry: Andrew Pressley](./Elementary-Differential-Geometry-Andrew-Pressley) | Implemented | Plane and space curves, curvature, torsion, global curve properties, surface patches, first and second fundamental forms, geodesics, hyperbolic geometry, minimal surfaces, and Gauss-Bonnet. |
| [Elementary Differential Geometry: Barrett O'Neill](./Elementary-Differential-Geometry-Barrett-ONeill) | Implemented | Calculus on Euclidean spaces, frame fields, Euclidean geometry, calculus on surfaces, shape operators, intrinsic and global surface geometry, Riemannian geometry, and computer-formula labs. |
| [Euclid and Beyond](./Euclid-and-Beyond) | Implemented | Euclidean foundations, Hilbert axioms, fields, segment arithmetic, area, construction problems, field extensions, non-Euclidean geometry, and polyhedra. |
| [Euclidean and Non-Euclidean Geometries](./Euclidean-and-Non-Euclidean-Geometries) | Implemented | Euclidean axioms, incidence and logic, neutral geometry, parallel postulate history, hyperbolic models, transformations, elliptic geometry, and continuity variants. |
| [Fundamentals of Computer Graphics](./Fundamentals-of-Computer-Graphics) | Implemented | Ray tracing, rasterization, transformations, sampling, materials, animation, color, perception, tone mapping, implicit modeling, games, and visualization workflows. |
| [Geometric Algebra for Computer Science](./Geometric-Algebra-for-Computer-Science) | Implemented | Blades, products, meets and joins, rotors, homogeneous and conformal models, geometric differentiation, implementation issues, and graphics/vision applications. |
| [Geometric Deep Learning](./Geometric-Deep-Learning) | Implemented | Representation learning, high-dimensional generalization, geometric priors, graphs, groups, grids, manifolds, gauges, equivariant models, applications, and historical lineage. |
| [Geometric Group Theory: An Introduction](./Geometric-Group-Theory-An-Introduction) | Implemented | Cayley graphs, word metrics, quasi-isometries, growth, amenability, hyperbolic spaces, boundaries, and group actions. |
| [Geometric Measure Theory](./Geometric-Measure-Theory) | Implemented | Multilinear algebra, measure and integration, differentiation theory, rectifiability, currents, area, and measure-theoretic geometry. |
| [Geometric Tools for Computer Graphics](./Geometric-Tools-for-Computer-Graphics) | Implemented | Vectors, matrices, transformations, distance and intersection queries, curves, surfaces, meshes, spatial data structures, and practical geometry algorithms for graphics. |
| [Geometry: A Metric Approach with Models](./Geometry-A-Metric-Approach-with-Models) | Implemented | Incidence and metric geometry, betweenness, plane separation, angle measure, neutral geometry, parallels, hyperbolic and Euclidean models, area, and isometries. |
| [Geometry I](./Geometry-I) | Implemented | Group actions, affine and projective spaces, barycenters, cross-ratios, complexification, Euclidean affine and vector geometry, triangles, spheres, circles, and convexity. |
| [Geometry II](./Geometry-II) | Implemented | Polytopes, quadratic forms, projective and affine quadrics, conics, sphere geometry, elliptic and hyperbolic geometry, and spaces of spheres. |
| [Geometry with an Introduction to Cosmic Topology](./Geometry-with-an-Introduction-to-Cosmic-Topology) | Implemented | Complex coordinates, transformations, Mobius geometry, hyperbolic and elliptic models, surface geometry, quotient spaces, cosmic topology, and universe-shape diagnostics. |
| [Hodge Theory and Complex Algebraic Geometry](./Hodge-Theory-and-Complex-Algebraic-Geometry) | Implemented | Compact Kahler manifolds, Hodge structures, Kahler identities, hard Lefschetz, variations, and complex algebraic geometry. |
| [Ideals, Varieties, and Algorithms](./Ideals-Varieties-and-Algorithms-An-Introduction-to-Computational-Algebraic-Geometry-and-Commutative-Algebra) | Implemented | Polynomial ideals, affine varieties, Grobner bases, elimination, robotics, theorem proving, invariant theory, projective algebraic geometry, and dimension. |
| [Information Geometry and Its Applications](./Information-Geometry-and-Its-Applications) | Implemented | Divergence functions, dually flat geometry, exponential and mixture families, alpha geometry, dual connections, statistical inference, EM, semiparametrics, time series, ML, natural gradients, and signal processing. |
| [Introduction to Geometry](./Introduction-to-Geometry) | Implemented | Classical Euclidean geometry, symmetry, coordinates, complex numbers, Platonic solids, affine and projective geometry, hyperbolic geometry, curves, surfaces, topology, and four-dimensional geometry. |
| [Introduction to Symplectic Topology](./Introduction-to-Symplectic-Topology) | Implemented | Symplectic manifolds, Hamiltonian dynamics, moment maps, symplectic reduction, and global symplectic invariants. |
| [J-holomorphic Curves and Symplectic Topology](./J-Holomorphic-Curves-and-Symplectic-Topology) | Implemented | Pseudoholomorphic curves, compactness, gluing, moduli spaces, Gromov-Witten-style checks, and symplectic topology. |
| [Lectures on Symplectic Geometry](./Lectures-on-Symplectic-Geometry) | Implemented | Symplectic forms, Darboux and Moser arguments, cotangent bundles, Hamiltonian actions, moment maps, reduction, and toric manifolds. |
| [Mathematical Foundations of Geometric Deep Learning](./Mathematical-Foundations-of-Geometric-Deep-Learning) | Implemented | Algebraic structures, metric and analytical geometry, vector calculus, topology, differential geometry, functional analysis, spectral theory, graph theory, and message-passing foundations. |
| [Mathematical Methods of Classical Mechanics](./Mathematical-Methods-of-Classical-Mechanics) | Implemented | Variational principles, Lagrangian and Hamiltonian mechanics, symplectic geometry, canonical transformations, rigid bodies, and perturbation ideas. |
| [Methods of Information Geometry](./Methods-of-Information-Geometry) | Implemented | Statistical manifolds, tangent and tensor fields, Riemannian metrics, affine connections, dual flatness, information theory, and convexity. |
| [Metric Spaces of Non-Positive Curvature](./Metric-Spaces-of-Non-Positive-Curvature) | Implemented | CAT(0) spaces, geodesic metric spaces, comparison geometry, group actions, boundaries, and non-positive curvature diagnostics. |
| [Modern Robotics](./Modern-Robotics) | Implemented | Screw theory, configuration spaces, rigid-body motions, forward and inverse kinematics, velocity kinematics, dynamics, trajectory generation, motion planning, control, grasping, and mobile robots. |
| [Multiple View Geometry in Computer Vision](./Multiple-View-Geometry-in-Computer-Vision) | Implemented | Projective transformations, camera models, calibration, epipolar geometry, fundamental and trifocal tensors, structure computation, homographies, auto-calibration, cheirality, degeneracies, and estimation appendices. |
| [Nonparametric Inference on Manifolds](./Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces) | Implemented | Manifold data, Frechet means, nonparametric inference, bootstrap methods, shape spaces, image analysis, and machine vision applications. |
| [Optimal Transport: Old and New](./Optimal-Transport-Old-and-New) | Implemented | Monge-Kantorovich transport, Wasserstein geometry, duality, PDE, probability, curvature, and executable transport examples. |
| [Perspectives on Projective Geometry](./Perspectives-on-Projective-Geometry) | Implemented | Pappus configurations, projective planes, homogeneous coordinates, cross-ratios, bracket algebra, conics, diagram techniques, Cayley-Klein geometries, complex projective lines, and hyperbolic models. |
| [Principles of Algebraic Geometry](./Principles-of-Algebraic-Geometry) | Implemented | Complex algebraic varieties, Riemann surfaces, algebraic curves, divisors, sheaves, surfaces, and Hodge-flavored methods. |
| [Statistics on Special Manifolds](./Statistics-on-Special-Manifolds) | Implemented | Special manifolds, population distributions, decompositions, Jacobians, distributional problems, Stiefel and Grassmann data, and matrix-valued samples. |
| [The Four Pillars of Geometry](./The-Four-Pillars-of-Geometry) | Implemented | Euclidean construction and axioms, linear algebra, projective geometry, transformation groups, and non-Euclidean geometry. |
| [Topology](./Topology) | Implemented | Set theory, topological spaces, continuity, connectedness, compactness, countability and separation axioms, Tychonoff, metrization, function spaces, Baire spaces, fundamental groups, plane separation, van Kampen, surfaces, and covering spaces. |
| [Undergraduate Algebraic Geometry](./Undergraduate-Algebraic-Geometry) | Implemented | Conics, cubics, group law, affine varieties, coordinate rings, projective and birational geometry, tangent spaces, dimension, and the 27 lines on a cubic surface. |
| [Visual Differential Geometry and Forms](./Visual-Differential-Geometry-and-Forms) | Implemented | Euclidean and non-Euclidean geometry, metrics, geodesics, curvature, Gauss-Bonnet, manifolds, vector fields, differential forms, Stokes' theorem, and de Rham intuition. |

## Long-Term Geometry Roadmap

The roadmap below is the working shelf for future notebook courses. Implemented
books remain visible here when they are part of the broader learning path; planned
books mark future expansion targets.

### Classical Undergraduate Foundations

These books form the broad classical spine. They introduce the major geometric
languages before specialization: construction, axioms, metric reasoning, linear
and affine geometry, transformations, projective ideas, and non-Euclidean models.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| John Stillwell, *The Four Pillars of Geometry* | [Implemented](./The-Four-Pillars-of-Geometry) | A panoramic first course linking Euclidean construction, linear algebra, projective geometry, transformation groups, and non-Euclidean geometry. |
| H. S. M. Coxeter, *Introduction to Geometry* | [Implemented](./Introduction-to-Geometry) | A high-breadth classical course for synthetic, Euclidean, projective, non-Euclidean, differential, and topological geometric thinking. |
| Marcel Berger, *Geometry I* | [Implemented](./Geometry-I) | A selective advanced undergraduate course on affine spaces, projective spaces, symmetry, Euclidean geometry, and convexity. |
| Marcel Berger, *Geometry II* | [Implemented](./Geometry-II) | A continuation through polytopes, quadratic forms, quadrics, conics, sphere geometry, and elliptic and hyperbolic models. |
| Robin Hartshorne, *Geometry: Euclid and Beyond* | [Implemented](./Euclid-and-Beyond) | A rigorous Euclidean foundations course moving from axioms and constructions toward fields, area, non-Euclidean geometry, and polyhedra. |
| Marvin Greenberg, *Euclidean and Non-Euclidean Geometries* | [Implemented](./Euclidean-and-Non-Euclidean-Geometries) | A foundations and history course centered on Euclidean axioms, models, transformations, continuity, and the discovery of hyperbolic geometry. |
| Millman and Parker, *Geometry: A Metric Approach with Models* | [Implemented](./Geometry-A-Metric-Approach-with-Models) | A model-based metric geometry course comparing incidence, metric, neutral, Euclidean, hyperbolic, and isometry-focused geometries. |

### Projective Geometry, Transformations, Vision, and Geometric Algebra

This branch follows the path from homogeneous coordinates and projective
transformations into camera geometry, conformal models, and computational
representations of geometric operations.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| Jurgen Richter-Gebert, *Perspectives on Projective Geometry* | [Implemented](./Perspectives-on-Projective-Geometry) | A modern projective geometry course emphasizing duality, cross-ratio, conics, and projective models of other geometries. |
| Hartley and Zisserman, *Multiple View Geometry in Computer Vision* | [Implemented](./Multiple-View-Geometry-in-Computer-Vision) | A computer vision geometry course on cameras, epipolar geometry, reconstruction, calibration, and projective estimation. |
| Dorst, Fontijne, and Mann, *Geometric Algebra for Computer Science* | [Implemented](./Geometric-Algebra-for-Computer-Science) | A multivector and conformal-model course for representing subspaces, rotations, intersections, and 3D geometric computation. |

### Differential Geometry and Topology

This branch turns geometry into the study of curves, surfaces, spaces, continuity,
compactness, connectedness, curvature, geodesics, topology, and global invariants.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| Manfredo do Carmo, *Differential Geometry of Curves and Surfaces* | [Implemented](./Differential-Geometry-of-Curves-and-Surfaces) | A classic curves-and-surfaces course on curvature, geodesics, Gauss maps, and global surface geometry. |
| Andrew Pressley, *Elementary Differential Geometry* | [Implemented](./Elementary-Differential-Geometry-Andrew-Pressley) | A gentler curves-and-surfaces course with visual pacing and computational checks. |
| Barrett O'Neill, *Elementary Differential Geometry* | [Implemented](./Elementary-Differential-Geometry-Barrett-ONeill) | A curves-and-surfaces course with early exposure to forms and modern differential-geometric notation. |
| M. A. Armstrong, *Basic Topology* | [Implemented](./Basic-Topology) | An intuition-first course in point-set, geometric, and algebraic topology. |
| James Munkres, *Topology* | [Implemented](./Topology) | A rigorous senior undergraduate path through general topology and algebraic topology foundations. |
| Tristan Needham, *Visual Differential Geometry and Forms* | [Implemented](./Visual-Differential-Geometry-and-Forms) | A visual route through metrics, curvature, manifolds, vector fields, differential forms, and Stokes-style theorems. |
| Pinkall and Gross, *Differential Geometry: From Elastic Curves to Willmore Surfaces* | [Implemented](./Differential-Geometry-From-Elastic-Curves-to-Willmore-Surfaces) | A variational geometry course connecting elastic curves, surface curvature, topology, Gauss-Bonnet, and Willmore surfaces. |
| Weeks, *Geometry with an Introduction to Cosmic Topology* | [Implemented](./Geometry-with-an-Introduction-to-Cosmic-Topology) | A non-Euclidean and topology course linking transformation geometry, hyperbolic/elliptic models, surfaces, and cosmic topology. |

### Algebraic, Discrete, Convex, and Computational Geometry

This branch makes geometric objects algebraic, combinatorial, and algorithmic:
varieties, ideals, convex hulls, triangulations, Voronoi diagrams, arrangements,
incidence, lattices, and robust computation.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| Miles Reid, *Undergraduate Algebraic Geometry* | [Implemented](./Undergraduate-Algebraic-Geometry) | A first algebraic geometry course on conics, cubics, affine/projective varieties, singularities, dimension, and classical configurations. |
| Cox, Little, and O'Shea, *Ideals, Varieties, and Algorithms* | [Implemented](./Ideals-Varieties-and-Algorithms-An-Introduction-to-Computational-Algebraic-Geometry-and-Commutative-Algebra) | A computational algebraic geometry course on Grobner bases, elimination, polynomial systems, robotics, theorem proving, and invariant theory. |
| Devadoss and O'Rourke, *Discrete and Computational Geometry* | [Implemented](./Discrete-and-Computational-Geometry) | An undergraduate-friendly course on convex hulls, triangulations, Voronoi diagrams, pseudotriangulations, reconstruction, and geometric applications. |
| de Berg, van Kreveld, Overmars, and Schwarzkopf, *Computational Geometry: Algorithms and Applications* | [Implemented](./Computational-Geometry-Algorithms-and-Applications) | An algorithmic geometry course on data structures, arrangements, range searching, motion planning, and robustness. |
| Joseph O'Rourke, *Computational Geometry in C* | [Implemented](./Computational-Geometry-in-C) | An implementation-oriented geometry algorithms course for graphics, robotics, engineering design, and low-level geometric predicates. |
| Jiri Matousek, *Lectures on Discrete Geometry* | [Implemented](./Lectures-on-Discrete-Geometry) | A more advanced discrete geometry course on convexity, polytopes, arrangements, incidence theory, lattices, and Helly-type theorems. |

### Applied Geometry: Graphics, Robotics, Statistics, Information, and ML

Applied geometry is where the languages above become tools for rendering,
manipulation, data analysis, inference, optimization, and learned geometric
representations.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| Schneider and Eberly, *Geometric Tools for Computer Graphics* | [Implemented](./Geometric-Tools-for-Computer-Graphics) | A practical geometry course for transformations, intersections, distance queries, curves, surfaces, meshes, and graphics algorithms. |
| Marschner and Shirley, *Fundamentals of Computer Graphics* | [Implemented](./Fundamentals-of-Computer-Graphics) | A graphics course covering image formation, ray tracing, rasterization, shading, sampling, animation, color, perception, and visualization. |
| Murray, Li, and Sastry, *A Mathematical Introduction to Robotic Manipulation* | [Implemented](./A-Mathematical-Introduction-to-Robotic-Manipulation) | A Lie-group and screw-theoretic robotics course for rigid motion, manipulation, grasping, dynamics, and nonholonomic systems. |
| Lynch and Park, *Modern Robotics* | [Implemented](./Modern-Robotics) | A modern robotics course on screw theory, kinematics, dynamics, planning, control, and executable robot models. |
| Mardia and Jupp, *Directional Statistics* | [Implemented](./Directional-Statistics) | A statistics-on-circles-and-spheres course for circular data, spherical data, shape spaces, models, inference, and table replacement. |
| Shun-ichi Amari, *Information Geometry and Its Applications* | [Implemented](./Information-Geometry-and-Its-Applications) | An applied information geometry course connecting Fisher metrics, divergences, optimization, inference, signal processing, and machine learning. |
| Haitz Saez de Ocariz Borde and Michael Bronstein, *Mathematical Foundations of Geometric Deep Learning* | [Implemented](./Mathematical-Foundations-of-Geometric-Deep-Learning) | A mathematical primer for geometric ML covering algebra, metric geometry, calculus, topology, functional analysis, spectral theory, and graph theory. |
| Bronstein, Bruna, Cohen, and Velickovic, *Geometric Deep Learning* | [Implemented](./Geometric-Deep-Learning) | A modern ML geometry course on graphs, groups, geodesics, gauges, invariance, equivariance, and geometric priors. |

### Graduate Manifolds, Topology, and Riemannian Geometry

The graduate core develops the language of manifolds, differential topology,
algebraic topology, Riemannian metrics, curvature, global analysis, and
low-dimensional topology.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| John M. Lee, *Introduction to Topological Manifolds* | Planned | A beginning graduate course on topological manifolds and the topology needed for geometry and algebraic topology. |
| John M. Lee, *Introduction to Smooth Manifolds* | [Implemented](./Introduction-to-Smooth-Manifolds) | A core smooth-manifold course covering tangent spaces, bundles, tensors, forms, flows, Lie groups, foliations, and de Rham cohomology. |
| Guillemin and Pollack, *Differential Topology* | [Implemented](./Differential-Topology) | A compact course on transversality, Sard's theorem, degree, intersection theory, and geometric applications. |
| Frank Warner, *Foundations of Differentiable Manifolds and Lie Groups* | [Implemented](./Foundations-of-Differentiable-Manifolds-and-Lie-Groups) | A compressed advanced course on differentiable manifolds, Lie groups, integration, de Rham theory, and Hodge theory. |
| Allen Hatcher, *Algebraic Topology* | [Implemented](./Algebraic-Topology) | A standard graduate algebraic topology course on fundamental groups, homology, cohomology, and homotopy. |
| Bott and Tu, *Differential Forms in Algebraic Topology* | [Implemented](./Differential-Forms-in-Algebraic-Topology) | A bridge course from differential geometry to algebraic topology through forms, de Rham theory, and characteristic ideas. |
| A. B. Sossinsky, *Knots, Links and Their Invariants* | [Implemented](./Knots-Links-and-Their-Invariants-An-Elementary-Course-in-Contemporary-Knot-Theory) | A knot theory and low-dimensional topology course built around diagrams, invariants, groups, and covering-space methods. |
| William Thurston, *Three-Dimensional Geometry and Topology* | [Implemented](./Three-Dimensional-Geometry-and-Topology) | A geometry/topology course on surfaces, 3-manifolds, geometric structures, and the bridge to low-dimensional topology. |
| John M. Lee, *Introduction to Riemannian Manifolds* | [Implemented](./Introduction-to-Riemannian-Manifolds) | A modern Riemannian geometry course on metrics, connections, geodesics, curvature, submanifolds, Jacobi fields, and comparison ideas. |
| Manfredo do Carmo, *Riemannian Geometry* | [Implemented](./Riemannian-Geometry) | A compact classic graduate Riemannian course for curvature, geodesics, completeness, and global results. |
| Kobayashi and Nomizu, *Foundations of Differential Geometry*, Vols. I-II | [Implemented](./Foundations-of-Differential-Geometry) | A reference-level course on connections, principal bundles, curvature, holonomy, homogeneous spaces, and complex/Hermitian geometry. |
| Besse, *Einstein Manifolds* | [Implemented](./Einstein-Manifolds) | A specialized Riemannian geometry course on Einstein metrics, curvature identities, and geometric analysis. |
| Helgason, *Differential Geometry, Lie Groups, and Symmetric Spaces* | [Implemented](./Differential-Geometry-Lie-Groups-and-Symmetric-Spaces) | A Lie groups and symmetric spaces course connecting Riemannian geometry, homogeneous spaces, and representation-flavored geometry. |

### Graduate Algebraic, Complex, Symplectic, Metric, and Statistical Geometry

This shelf holds the specialized graduate branches: schemes and sheaves,
complex/Kahler geometry, symplectic and contact geometry, metric spaces, convex
analysis, geometric group theory, geometric measure theory, computational
topology, information geometry, statistics on manifolds, and optimal transport.

| Book | Status | Planned notebook purpose |
| --- | --- | --- |
| Robin Hartshorne, *Algebraic Geometry* | [Implemented](./Algebraic-Geometry) | A graduate algebraic geometry course on schemes, sheaves, cohomology, curves, and surfaces. |
| Griffiths and Harris, *Principles of Algebraic Geometry* | [Implemented](./Principles-of-Algebraic-Geometry) | A complex-manifold and projective-variety course on Riemann surfaces, algebraic curves, surfaces, and Hodge-flavored methods. |
| Daniel Huybrechts, *Complex Geometry: An Introduction* | [Implemented](./Complex-Geometry-An-Introduction) | A modern bridge course through complex manifolds, Hermitian and Kahler geometry, sheaves, and line bundles. |
| Claire Voisin, *Hodge Theory and Complex Algebraic Geometry I-II* | [Implemented](./Hodge-Theory-and-Complex-Algebraic-Geometry) | An advanced course on Hodge structures, Kahler identities, hard Lefschetz, and complex algebraic geometry. |
| McDuff and Salamon, *Introduction to Symplectic Topology* | [Implemented](./Introduction-to-Symplectic-Topology) | A standard symplectic geometry/topology course on symplectic manifolds, Hamiltonian dynamics, and global symplectic invariants. |
| Ana Cannas da Silva, *Lectures on Symplectic Geometry* | [Implemented](./Lectures-on-Symplectic-Geometry) | A faster introductory symplectic course emphasizing examples, moment maps, and geometric mechanics. |
| V. I. Arnold, *Mathematical Methods of Classical Mechanics* | [Implemented](./Mathematical-Methods-of-Classical-Mechanics) | A geometric mechanics course linking flows, Lie groups, symplectic geometry, Hamiltonian systems, and classical mechanics. |
| Hansjorg Geiges, *An Introduction to Contact Topology* | [Implemented](./An-Introduction-to-Contact-Topology) | A contact topology course focused on contact manifolds, especially in dimension three, and their relation to symplectic geometry. |
| McDuff and Salamon, *J-holomorphic Curves and Symplectic Topology* | [Implemented](./J-Holomorphic-Curves-and-Symplectic-Topology) | A research-level course on pseudoholomorphic curves, compactness, gluing, and quantum-flavored symplectic topology. |
| Rockafellar, *Convex Analysis* | [Implemented](./Convex-Analysis) | A convex analysis course on convex sets/functions, duality, optimization, minimax, Lagrange multipliers, and convex programs. |
| Burago, Burago, and Ivanov, *A Course in Metric Geometry* | [Implemented](./A-Course-in-Metric-Geometry) | A metric geometry course on length spaces, curvature bounds, Gromov hyperbolicity, convergence, and Alexandrov spaces. |
| Bridson and Haefliger, *Metric Spaces of Non-Positive Curvature* | [Implemented](./Metric-Spaces-of-Non-Positive-Curvature) | A CAT(0) and non-positive curvature course for metric spaces and groups acting geometrically on them. |
| Clara Loh, *Geometric Group Theory: An Introduction* | [Implemented](./Geometric-Group-Theory-An-Introduction) | A first geometric group theory course on Cayley graphs, quasi-isometries, group actions, and hyperbolic groups. |
| Federer, *Geometric Measure Theory* | [Implemented](./Geometric-Measure-Theory) | A geometric analysis course on rectifiability, currents, area, and measure-theoretic treatment of geometric objects. |
| Edelsbrunner and Harer, *Computational Topology: An Introduction* | [Implemented](./Computational-Topology-An-Introduction) | A computational topology course on complexes, algorithms, persistent homology, and data-driven topological summaries. |
| Amari and Nagaoka, *Methods of Information Geometry* | [Implemented](./Methods-of-Information-Geometry) | A mathematical information geometry course on statistical manifolds, dual affine connections, information theory, and convexity. |
| Shun-ichi Amari, *Information Geometry and Its Applications* | [Implemented](./Information-Geometry-and-Its-Applications) | An application-facing graduate path through information-geometric methods in inference, optimization, neural networks, and signal processing. |
| Chikuse, *Statistics on Special Manifolds* | [Implemented](./Statistics-on-Special-Manifolds) | A statistics-on-manifolds course for Stiefel and Grassmann data, orientations, subspaces, and matrix-valued samples. |
| Bhattacharya and Bhattacharya, *Nonparametric Inference on Manifolds* | [Implemented](./Nonparametric-Inference-on-Manifolds-with-Applications-to-Shape-Spaces) | A manifold statistics course on nonparametric inference, shape spaces, image analysis, and machine vision applications. |
| Villani, *Optimal Transport: Old and New* | [Implemented](./Optimal-Transport-Old-and-New) | A graduate optimal transport course on Monge-Kantorovich transport, Wasserstein geometry, PDE, probability, and curvature. |
| Bronstein, Bruna, Cohen, and Velickovic, *Geometric Deep Learning* | [Implemented](./Geometric-Deep-Learning) | A geometric machine learning course on graphs, manifolds, groups, gauges, equivariance, and learned geometric priors. |

## Suggested Reading Spine

A compact undergraduate path is Stillwell, Greenberg or Hartshorne, Coxeter,
selected Berger, then one curves-and-surfaces text, one topology text, one
algebraic geometry text, and one discrete or computational geometry text. The
applied branch then splits naturally into graphics, robotics, geometric algebra,
computer vision, directional statistics, information geometry, and geometric ML.

A compact graduate path is Lee's topological and smooth manifolds, Hatcher,
Bott-Tu, Guillemin-Pollack, Lee's Riemannian manifolds, then a specialization:
Hartshorne or Griffiths-Harris for algebraic/complex geometry, McDuff-Salamon for
symplectic geometry, Burago-Burago-Ivanov for metric geometry, Amari-Nagaoka for
information geometry, or Villani for optimal transport.
