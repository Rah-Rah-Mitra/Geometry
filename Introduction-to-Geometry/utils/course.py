from __future__ import annotations
from pathlib import Path
BOOK_TITLE = "Introduction to Geometry"
BOOK_AUTHOR = "H. S. M. Coxeter"
PDF_NAME = "Introduction to Geometry.pdf"
BODY_PDF_OFFSET = 18
CHAPTERS = [
  {
    "no": 1,
    "part": "I",
    "folder": "chapter-01-triangles",
    "title": "Triangles",
    "printed": "3-25",
    "pdf": "21-43",
    "focus": "Euclid, primitive concepts, congruence, medians and centroid, incenter, circumcenter, Euler line, nine-point circle, extremum problems, and Morley-style angle trisectors",
    "visual": "triangle centers, Euler line, nine-point circle, cevians, angle bisectors, and inspection of invariants"
  },
  {
    "no": 2,
    "part": "I",
    "folder": "chapter-02-regular-polygons",
    "title": "Regular Polygons",
    "printed": "26-38",
    "pdf": "44-56",
    "focus": "cyclotomy, angle trisection, isometry, symmetry groups, products of reflections, kaleidoscopes, and star polygons",
    "visual": "regular n-gons, star polygons, reflection axes, rotation orbits, and group composition tables"
  },
  {
    "no": 3,
    "part": "I",
    "folder": "chapter-03-isometry-in-the-euclidean-plane",
    "title": "Isometry in the Euclidean Plane",
    "printed": "39-49",
    "pdf": "57-67",
    "focus": "direct and opposite isometries, translations, glide reflections, half-turns, reflection products, and strip patterns",
    "visual": "motion trails for translations, rotations, reflections, glide reflections, and products of mirror lines"
  },
  {
    "no": 4,
    "part": "I",
    "folder": "chapter-04-two-dimensional-crystallography",
    "title": "Two-Dimensional Crystallography",
    "printed": "50-66",
    "pdf": "68-84",
    "focus": "lattices, Dirichlet regions, general lattice symmetry, Escher-style motifs, six brick patterns, crystallographic restriction, tessellations, and collinear-point problems",
    "visual": "lattice bases, Dirichlet cells, wallpaper-style motifs, rotation orders, and tiling adjacency"
  },
  {
    "no": 5,
    "part": "I",
    "folder": "chapter-05-similarity-in-the-euclidean-plane",
    "title": "Similarity in the Euclidean Plane",
    "printed": "67-76",
    "pdf": "85-94",
    "focus": "dilation, centers of similitude, nine-point center, invariant point of a similarity, direct similarity, and opposite similarity",
    "visual": "scale maps, spiral similarities, fixed points, homothety centers, and nested images"
  },
  {
    "no": 6,
    "part": "I",
    "folder": "chapter-06-circles-and-spheres",
    "title": "Circles and Spheres",
    "printed": "77-95",
    "pdf": "95-113",
    "focus": "circle inversion, orthogonal circles, inversions of lines and circles, inverse plane, coaxal circles, Apollonius circles, circle-preserving transformations, sphere inversion, and the elliptic plane",
    "visual": "inversion grids, orthogonal circle pencils, coaxal families, Apollonius loci, and stereographic intuition"
  },
  {
    "no": 7,
    "part": "I",
    "folder": "chapter-07-isometry-and-similarity-in-euclidean-space",
    "title": "Isometry and Similarity in Euclidean Space",
    "printed": "96-106",
    "pdf": "114-124",
    "focus": "direct and opposite spatial isometries, central inversion, rotations and translations, products of reflections, twists, dilative rotations, and sphere-preserving transformations",
    "visual": "3D frames, screw motions, reflection planes, twist traces, and projected spatial orbits"
  },
  {
    "no": 8,
    "part": "II",
    "folder": "chapter-08-coordinates",
    "title": "Coordinates",
    "printed": "107-134",
    "pdf": "125-152",
    "focus": "Cartesian coordinates, polar coordinates, circles, conics, tangent, arc length, area, hyperbolic functions, equiangular spiral, and three dimensions",
    "visual": "coordinate grids, conic level sets, polar curves, tangent and area approximations, and 3D coordinate frames"
  },
  {
    "no": 9,
    "part": "II",
    "folder": "chapter-09-complex-numbers",
    "title": "Complex Numbers",
    "printed": "135-147",
    "pdf": "153-165",
    "focus": "rational and real numbers, Argand diagrams, modulus and amplitude, Euler formula, roots of equations, and conformal transformations",
    "visual": "complex multiplication, roots of unity, phase-amplitude diagrams, and simple conformal maps"
  },
  {
    "no": 10,
    "part": "II",
    "folder": "chapter-10-the-five-platonic-solids",
    "title": "The Five Platonic Solids",
    "printed": "148-159",
    "pdf": "166-177",
    "focus": "pyramids, prisms, antiprisms, drawings and models, Euler formula, radii and angles, and reciprocal polyhedra",
    "visual": "wireframe solids, vertex-edge-face counts, dual pairs, radius comparisons, and Euler characteristic checks"
  },
  {
    "no": 11,
    "part": "II",
    "folder": "chapter-11-the-golden-section-and-phyllotaxis",
    "title": "The Golden Section and Phyllotaxis",
    "printed": "160-174",
    "pdf": "178-192",
    "focus": "extreme and mean ratio, divine proportion, golden spiral, Fibonacci numbers, and phyllotaxis",
    "visual": "golden rectangles, logarithmic spirals, Fibonacci approximants, and sunflower point sets"
  },
  {
    "no": 12,
    "part": "III",
    "folder": "chapter-12-ordered-geometry",
    "title": "Ordered Geometry",
    "printed": "175-190",
    "pdf": "193-208",
    "focus": "extracting geometries from Euclid, intermediacy, collinear point problems, planes and hyperplanes, continuity, and parallelism",
    "visual": "betweenness, separation by lines and planes, convex hulls, order-preserving maps, and parallel axiom experiments"
  },
  {
    "no": 13,
    "part": "III",
    "folder": "chapter-13-affine-geometry",
    "title": "Affine Geometry",
    "printed": "191-228",
    "pdf": "209-246",
    "focus": "parallelism, Desargues axiom, dilatations, affinities, equiaffinities, lattices, vectors and centroids, barycentric coordinates, affine space, and three-dimensional lattices",
    "visual": "affine grids, barycentric coordinates, centroid preservation, lattice deformation, and area-scale checks"
  },
  {
    "no": 14,
    "part": "III",
    "folder": "chapter-14-projective-geometry",
    "title": "Projective Geometry",
    "printed": "229-262",
    "pdf": "247-280",
    "focus": "projective-plane axioms, projective coordinates, Desargues theorem, quadrangular and harmonic sets, projectivities, collineations, correlations, conics, projective space, and Euclidean space",
    "visual": "perspective projection, points at infinity, cross-ratio experiments, Desargues configurations, and conic projectivities"
  },
  {
    "no": 15,
    "part": "III",
    "folder": "chapter-15-absolute-geometry",
    "title": "Absolute Geometry",
    "printed": "263-286",
    "pdf": "281-304",
    "focus": "congruence, parallelism, isometry, finite rotation groups, finite isometry groups, geometrical crystallography, polyhedral kaleidoscopes, and discrete groups generated by inversions",
    "visual": "axiom comparison diagrams, finite rotation groups, reflection domains, Coxeter-style mirrors, and inversion-generated orbits"
  },
  {
    "no": 16,
    "part": "III",
    "folder": "chapter-16-hyperbolic-geometry",
    "title": "Hyperbolic Geometry",
    "printed": "287-306",
    "pdf": "305-324",
    "focus": "Euclidean and hyperbolic parallel axioms, consistency, angle of parallelism, finiteness of triangles, area defect, equidistant curves, Poincare half-plane model, horospheres, and Euclidean interpretation",
    "visual": "Poincare disk and half-plane geodesics, angle defect, horocycles, equidistant curves, and model-to-model maps"
  },
  {
    "no": 17,
    "part": "IV",
    "folder": "chapter-17-differential-geometry-of-curves",
    "title": "Differential Geometry of Curves",
    "printed": "307-327",
    "pdf": "325-345",
    "focus": "vectors in Euclidean space, vector functions, curvature, evolutes, involutes, catenary, tractrix, twisted curves, circular helix, general helix, and concho-spiral",
    "visual": "parametric curves, velocity and curvature vectors, Frenet frames, evolute traces, helices, and curvature profiles"
  },
  {
    "no": 18,
    "part": "IV",
    "folder": "chapter-18-the-tensor-notation",
    "title": "The Tensor Notation",
    "printed": "328-341",
    "pdf": "346-359",
    "focus": "dual bases, fundamental tensor, reciprocal lattices, critical lattice of a sphere, general coordinates, and alternating symbol",
    "visual": "dual basis arrows, metric ellipses, reciprocal lattice cells, coordinate mesh deformation, and determinant orientation checks"
  },
  {
    "no": 19,
    "part": "IV",
    "folder": "chapter-19-differential-geometry-of-surfaces",
    "title": "Differential Geometry of Surfaces",
    "printed": "342-365",
    "pdf": "360-383",
    "focus": "two-parameter surface patches, directions on a surface, normal curvature, principal curvatures, principal directions, umbilics, Dupin and Liouville theorems, and Dupin indicatrix",
    "visual": "surface parameter grids, normals, curvature maps, principal direction fields, indicatrices, and umbilic diagnostics"
  },
  {
    "no": 20,
    "part": "IV",
    "folder": "chapter-20-geodesics",
    "title": "Geodesics",
    "printed": "366-378",
    "pdf": "384-396",
    "focus": "theorema egregium, differential equations for geodesics, integral curvature of geodesic triangles, Euler-Poincare characteristic, constant-curvature surfaces, angle of parallelism, and pseudosphere",
    "visual": "geodesic traces, triangle curvature budget, constant-curvature comparisons, pseudosphere meridians, and numerical path checks"
  },
  {
    "no": 21,
    "part": "IV",
    "folder": "chapter-21-topology-of-surfaces",
    "title": "Topology of Surfaces",
    "printed": "379-395",
    "pdf": "397-413",
    "focus": "orientable surfaces, nonorientable surfaces, regular maps, four-color problem, six-color theorem, sufficient colors for arbitrary surfaces, and surfaces requiring full color counts",
    "visual": "Euler characteristic tables, polygon edge identifications, surface graphs, colorability experiments, and orientability checks"
  },
  {
    "no": 22,
    "part": "IV",
    "folder": "chapter-22-four-dimensional-geometry",
    "title": "Four-Dimensional Geometry",
    "printed": "396-412",
    "pdf": "414-430",
    "focus": "simple four-dimensional figures, conditions for honeycomb symbols, regular polytopes, close packing of equal spheres, and statistical honeycombs",
    "visual": "4D projections, Schlegel-style shadows, 3D slices, regular polytope counts, and sphere packing experiments"
  }
]
def chapter_by_no(no: int) -> dict:
    for chapter in CHAPTERS:
        if chapter["no"] == no:
            return chapter
    raise KeyError(no)
def canonical_notebook_name(chapter: dict) -> str:
    prefix = f"chapter-{chapter['no']:02d}-"
    return f"{chapter['no']:02d}-" + chapter['folder'].replace(prefix, "", 1) + ".ipynb"
def book_root(start: Path | None = None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "00-book-index.ipynb").exists() and (candidate / "utils").exists():
            return candidate
    raise FileNotFoundError("Could not find Introduction-to-Geometry book root")
