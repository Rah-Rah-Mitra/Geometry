# Visualization Storyboard

Every section notebook uses a synthetic, inspectable convex-geometry visual plus a proof or dependency map. The recurring audit target is not a fixed visual count; it is whether a reader can inspect the central invariant without opening the PDF.

## Part 1: Basic Concepts
- Section 1: Affine Sets - A point cloud is extended to its affine hull while a normal vector exposes the hyperplane equation. Check: Affine coefficients add to one and the recovered point lies on the displayed affine hull.
- Section 2: Convex Sets and Cones - Segments inside a convex polygon are compared with cone rays and a half-space cut. Check: Midpoints stay in the convex set, cone sums stay in the cone, and the half-space sign is correct.
- Section 3: The Algebra of Convex Sets - Two small convex bodies are added pointwise, then their support values confirm the algebra. Check: A support value of the sum equals the sum of support values in the same direction.
- Section 4: Convex Functions - A convex curve is taught through its epigraph rather than only through its graph. Check: A sampled Jensen inequality is nonnegative and the epigraph points sit above the curve.
- Section 5: Functional Operations - Pointwise maximum and sum operations are plotted as generators of new convex functions. Check: Midpoint convexity survives the displayed functional operations on the sampled grid.

## Part 2: Topological Properties
- Section 6: Relative Interiors of Convex Sets - A full-dimensional square, an edge, and a singleton separate ambient from relative interior. Check: Relative interior sample points have the expected affine-hull dimension and boundary status.
- Section 7: Closures of Convex Functions - An endpoint gap is closed by moving from an open epigraph boundary to a closed one. Check: The closed function has the same interior samples and adds the missing boundary value.
- Section 8: Recession Cones and Unboundedness - An unbounded convex region is annotated by every direction in which it can recede. Check: Adding a recession direction keeps sampled points inside the set.
- Section 9: Some Closedness Criteria - A closed epigraph is projected to a nonclosed interval, making the missing limit visible. Check: The projection has infimum zero but no point with projected coordinate zero.
- Section 10: Continuity of Convex Functions - Secant slopes bracket a convex graph and show why interior continuity is forced. Check: Displayed secant slopes are monotone in the sample order.

## Part 3: Duality Correspondences
- Section 11: Separation Theorems - Two disjoint convex bodies are certified by a signed-distance separating line. Check: All points of the two bodies have opposite signed margins with a positive gap.
- Section 12: Conjugates of Convex Functions - A quadratic is reconstructed from its supporting affine minorants indexed by slope. Check: Fenchel equality holds at the slope paired with the sampled primal point.
- Section 13: Support Functions - A polygon is scanned by rotating normals and recording the farthest support line. Check: The support value equals the maximum dot product over the sampled vertices.
- Section 14: Polars of Convex Sets - A centrally placed convex body is drawn beside its polar body in dual coordinates. Check: Sampled primal-dual dot products stay below the polar threshold.
- Section 15: Polars of Convex Functions - The l1 and l-infinity unit balls show how a norm's polar is read geometrically. Check: The dual norm inequality bounds sampled pairings by the product of primal and dual norms.
- Section 16: Dual Operations - Two convex functions combine in primal space while the dual view tracks infimal convolution. Check: A grid infimum is no larger than either unshifted summand and keeps convex midpoint behavior.

## Part 4: Representation and Inequalities
- Section 17: Caratheodory's Theorem - A point in a planar hull is represented by three vertices rather than by all points. Check: The reduced barycentric coefficients are nonnegative and add to one.
- Section 18: Extreme Points and Faces of Convex Sets - A support line exposes a face of a polygon and distinguishes vertices from edge interiors. Check: All points on the exposed face share the same support value.
- Section 19: Polyhedral Convex Sets and Functions - A max of affine functions is plotted as a polyhedral convex function with active regions. Check: Each sampled function value equals the maximum of its affine pieces.
- Section 20: Some Applications of Polyhedral Convexity - A small linear program highlights active inequalities and a vertex certificate. Check: The selected optimum satisfies all inequalities and ties the active constraints.
- Section 21: Helly's Theorem and Systems of Inequalities - Several convex half-planes are inspected through a small witness point and subfamilies. Check: The witness point satisfies every displayed inequality.
- Section 22: Linear Inequalities - A target vector outside a cone is separated by a certificate normal. Check: The certificate is nonnegative on cone generators and negative on the rejected target.

## Part 5: Differential Theory
- Section 23: Directional Derivatives and Subgradients - The absolute-value cusp displays a full interval of supporting slopes at one point. Check: Every sampled supporting line remains below the convex graph.
- Section 24: Differential Continuity and Monotonicity - A piecewise-linear convex function produces a monotone vertical-jump subgradient graph. Check: All sampled pairs satisfy the monotonicity inequality.
- Section 25: Differentiability of Convex Functions - A smooth quadratic and a kinked absolute-value term separate gradient from subgradient behavior. Check: Central finite differences match the analytic gradient away from the kink.
- Section 26: The Legendre Transformation - A strictly convex quadratic sends primal positions to slopes and back through the conjugate. Check: The primal gradient and conjugate gradient invert one another on the sample grid.

## Part 6: Constrained Extremum Problems
- Section 27: The Minimum of a Convex Function - Level sets contract toward the minimizer while the subgradient condition marks optimality. Check: The sampled minimizer has zero gradient and the smallest displayed objective value.
- Section 28: Ordinary Convex Programs and Lagrange Multipliers - A constrained quadratic minimization shows objective contours balanced by active constraint normals. Check: Stationarity and complementary slackness residuals are near zero for the displayed solution.
- Section 29: Bifunctions and Generalized Convex Programs - A perturbation parameter moves the right-hand side and traces a convex value function. Check: The sampled value curve satisfies midpoint convexity.
- Section 30: Adjoint Bifunctions and Dual Programs - Primal and dual objective curves are paired to make weak duality a visible inequality. Check: Every displayed primal value is no smaller than the paired dual lower bound.
- Section 31: Fenchel's Duality Theorem - A quadratic-plus-indicator problem is paired with its dual support calculation. Check: The selected primal and dual values agree within numerical tolerance.
- Section 32: The Maximum of a Convex Function - A convex function over a polygon puts its maximum on a vertex rather than in the middle. Check: The maximum over a sampled grid is bounded by the maximum over vertices.

## Part 7: Saddle-Functions and Minimax Theory
- Section 33: Saddle-Functions - Contours of a convex-concave quadratic display descent in one variable and ascent in another. Check: The saddle point has zero partial derivatives and the expected saddle inequalities nearby.
- Section 34: Closures and Equivalence Classes - A saddle surface over an open rectangle is compared with its closed boundary extension. Check: Boundary samples match the closure values prescribed by the extension.
- Section 35: Continuity and Differentiability of Saddle-functions - A vector field of partial gradients shows monotone behavior in x and antimonotone behavior in y. Check: The sampled partial-gradient pairing has the expected signs.
- Section 36: Minimax Problems - A convex-concave payoff on a box shows when min max and max min agree. Check: The computed minmax and maximin values agree for the displayed saddle example.
- Section 37: Conjugate Saddle-functions and Minimax Theorems - A quadratic saddle is transformed through a conjugate pairing and compared with the original. Check: The sampled biconjugate reconstruction matches the original quadratic saddle values.

## Part 8: Convex Algebra
- Section 38: The Algebra of Bifunctions - A small matrix model visualizes the algebraic shape of adding and composing convex bifunction analogues. Check: The displayed matrices satisfy the adjoint-of-composition identity.
- Section 39: Convex Processes - A cone-valued process maps one input ray to a wedge of outputs through a convex graph. Check: The graph samples are closed under positive scaling and convex addition.
