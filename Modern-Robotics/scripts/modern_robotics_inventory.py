"""Course metadata for the Modern Robotics notebook edition."""

from __future__ import annotations

from dataclasses import dataclass

PDF_FILENAME = "Mordern Robotics.pdf"
PDF_PAGE_OFFSET = 18
BOOK_TITLE = "Modern Robotics: Mechanics, Planning, and Control"
AUTHORS = "Kevin M. Lynch and Frank C. Park"


@dataclass(frozen=True)
class Chapter:
    number: int
    slug: str
    title: str
    notebook: str
    printed_start: int
    printed_end: int
    part_slug: str
    part_title: str
    theme: str
    visual_focus: str
    visual_kind: str
    artifact_stem: str
    inspection_target: str
    question: str
    terms: tuple[str, ...]
    translation: tuple[str, ...]
    lab: str
    pitfalls: tuple[str, ...]
    takeaways: tuple[str, ...]

    @property
    def pdf_start(self) -> int:
        return self.printed_start + PDF_PAGE_OFFSET

    @property
    def pdf_end(self) -> int:
        return self.printed_end + PDF_PAGE_OFFSET

    @property
    def is_appendix(self) -> bool:
        return self.slug.startswith("appendix-")

    def as_dict(self) -> dict[str, object]:
        return {
            "number": self.number,
            "slug": self.slug,
            "title": self.title,
            "notebook": self.notebook,
            "printed_start": self.printed_start,
            "printed_end": self.printed_end,
            "pdf_start": self.pdf_start,
            "pdf_end": self.pdf_end,
            "part_slug": self.part_slug,
            "part_title": self.part_title,
            "theme": self.theme,
            "visual_focus": self.visual_focus,
            "visual_kind": self.visual_kind,
            "artifact_stem": self.artifact_stem,
            "inspection_target": self.inspection_target,
            "question": self.question,
            "terms": list(self.terms),
            "translation": list(self.translation),
            "lab": self.lab,
            "pitfalls": list(self.pitfalls),
            "takeaways": list(self.takeaways),
        }


PARTS = [
    ("part-01-geometric-foundations", "Geometric Foundations"),
    ("part-02-manipulator-kinematics", "Manipulator Kinematics"),
    ("part-03-dynamics-trajectories-and-planning", "Dynamics, Trajectories, and Planning"),
    ("part-04-control-contact-and-mobile-robots", "Control, Contact, and Mobile Robots"),
    ("part-05-reference-appendices", "Reference Appendices"),
]


def _chapter(
    number: int,
    slug: str,
    title: str,
    notebook: str,
    pages: tuple[int, int],
    part_index: int,
    theme: str,
    visual_focus: str,
    visual_kind: str,
    artifact_stem: str,
    inspection_target: str,
    question: str,
    terms: tuple[str, ...],
    translation: tuple[str, ...],
    lab: str,
    pitfalls: tuple[str, ...],
    takeaways: tuple[str, ...],
) -> Chapter:
    part_slug, part_title = PARTS[part_index]
    return Chapter(
        number,
        slug,
        title,
        notebook,
        pages[0],
        pages[1],
        part_slug,
        part_title,
        theme,
        visual_focus,
        visual_kind,
        artifact_stem,
        inspection_target,
        question,
        terms,
        translation,
        lab,
        pitfalls,
        takeaways,
    )


CHAPTERS: list[Chapter] = [
    _chapter(1, "chapter-01-preview", "Preview", "01-preview.ipynb", (1, 10), 0, "configuration", "robotics as geometry plus decisions", "course map and workspace sketch", "robotics-preview", "how mechanics, planning, and control become one pipeline", "What does a robot need to know about shape, motion, force, and choice before it can act?", ("configuration", "task", "motion", "planning", "control", "contact", "mobile base"), ("Robot behavior becomes a chain from state representation to feasible motion.", "A mechanism is not just a drawing; it is a space of possible configurations.", "Planning and control are easier to reason about when their geometry is visible."), "Trace a simple manipulation task from configuration variables to a path and controller.", ("Treating chapters as isolated formulas hides the shared geometry.", "Task space is not the same object as configuration space."), ("Robotics is organized around spaces, maps, velocities, forces, and feedback.", "The later chapters reuse the same geometric vocabulary.")),
    _chapter(2, "chapter-02-configuration-space", "Configuration Space", "02-configuration-space.ipynb", (11, 58), 0, "configuration", "configuration spaces, constraints, and workspaces", "joint torus heat map and workspace annulus", "configuration-space", "where topology, dimension, and singular constraints become visible", "How do joints, loops, and constraints turn a mechanism into a geometric space?", ("degrees of freedom", "joint", "Gruebler count", "configuration space", "workspace", "holonomic constraint", "Pfaffian velocity constraint"), ("Degrees of freedom are dimension counts, not a guarantee of useful motion.", "Implicit constraints cut surfaces out of larger coordinate spaces.", "Velocity constraints can be tested locally even when no global equation exists."), "Compare a 2R arm's joint torus with its reachable workspace and singular set.", ("Counting constraints blindly can fail at singular mechanisms.", "A coordinate chart can tear or duplicate a circular configuration space."), ("Configuration space is the robot's true stage.", "Workspace pictures are useful projections, not replacements for C-space.")),
    _chapter(3, "chapter-03-rigid-body-motions", "Rigid-Body Motions", "03-rigid-body-motions.ipynb", (59, 136), 0, "rigid", "SO(3), SE(3), twists, screws, and wrenches", "3D frames and screw path", "rigid-body-motion", "how exponentials move frames while preserving rigid distances", "How can a rigid displacement, a velocity, and a force all be represented without losing frame information?", ("SO(3)", "SE(3)", "homogeneous transform", "twist", "screw axis", "adjoint", "wrench"), ("Rotation matrices encode orthonormal frames.", "A twist is a tangent vector to rigid motion.", "The adjoint is the bookkeeping map between frames."), "Build a screw path and verify that the adjoint preserves twist/wrench power pairing.", ("Confusing active motion with coordinate change flips multiplication order.", "Ignoring frames makes the same vector appear to contradict itself."), ("Rigid motion lives on Lie groups, not flat vector spaces.", "Twists and wrenches are dual objects tied together by power.")),
    _chapter(4, "chapter-04-forward-kinematics", "Forward Kinematics", "04-forward-kinematics.ipynb", (137, 170), 1, "kinematics", "product of exponentials for open chains", "planar arm and end-effector velocity ellipsoid", "forward-kinematics", "how screw axes compose into an end-effector pose", "How does a list of joint motions become a single end-effector transform?", ("home configuration", "space screw axis", "body screw axis", "product of exponentials", "URDF", "open chain", "frame assignment"), ("The home pose is the anchor for every exponential product.", "Space and body formulations are equivalent but compose in opposite directions.", "A robot description is useful when geometry and axes agree."), "Compute a three-link arm pose and compare geometric intuition with matrix products.", ("Changing joint order changes the pose.", "A link-frame drawing is not a substitute for screw-axis data."), ("PoE gives a coordinate-light way to compose joint motion.", "The same model supports visualization, simulation, and later Jacobians.")),
    _chapter(5, "chapter-05-velocity-kinematics-and-statics", "Velocity Kinematics and Statics", "05-velocity-kinematics-and-statics.ipynb", (171, 218), 1, "kinematics", "Jacobians, singularities, statics, and manipulability", "Jacobian image and velocity ellipsoid", "velocity-kinematics", "where rank and ellipsoid shape reveal available motion and force directions", "What does the Jacobian say about instantaneous motion, lost directions, and static force balance?", ("space Jacobian", "body Jacobian", "singularity", "manipulability", "wrench", "virtual work", "rank"), ("A Jacobian maps joint rates to a twist.", "The transpose maps endpoint wrench to joint torques by virtual work.", "Singularities are rank events, not just bad numbers."), "Sweep a planar arm near singularity and watch the velocity ellipsoid collapse.", ("Large joint speeds near singularity do not imply large endpoint freedom.", "Manipulability is representation dependent unless the metric is stated."), ("Instantaneous kinematics is linear geometry around a configuration.", "Statics is the dual linear map seen through power.")),
    _chapter(6, "chapter-06-inverse-kinematics", "Inverse Kinematics", "06-inverse-kinematics.ipynb", (219, 244), 1, "kinematics", "analytic and numerical inverse kinematics", "iterative endpoint correction", "inverse-kinematics", "how pose error is converted into a joint update and when it stalls", "How can we solve for joint coordinates when the forward map is nonlinear and sometimes many-to-one?", ("Newton-Raphson", "body error twist", "pseudoinverse", "redundancy", "closed loop", "damping", "convergence basin"), ("Inverse kinematics is root finding on the forward kinematics residual.", "The pseudoinverse chooses one local joint update among many possibilities.", "Damping trades exact correction for robustness."), "Run a damped iterative IK update for a planar arm target and inspect the residual curve.", ("A local method can converge to the wrong branch or fail outside its basin.", "Small task error can require large joint motion near singularity."), ("IK is numerical geometry on a nonlinear map.", "Rank, damping, and initial guess decide much of the behavior.")),
    _chapter(7, "chapter-07-kinematics-of-closed-chains", "Kinematics of Closed Chains", "07-kinematics-of-closed-chains.ipynb", (245, 270), 1, "configuration", "parallel mechanisms and loop constraints", "constraint residual and singular loop geometry", "closed-chain-kinematics", "how loop closure creates implicit surfaces and singular branches", "How do closed loops change kinematics from composition to constraint solving?", ("loop closure", "parallel mechanism", "Stewart-Gough platform", "constraint Jacobian", "singularity", "branch", "actuation"), ("Closed chains impose equations rather than a simple serial product.", "Forward and inverse kinematics exchange difficulty for parallel mechanisms.", "A singularity appears when the constraint Jacobian loses rank."), "Visualize a planar loop constraint and measure how a residual surface pinches near singularity.", ("Counting actuators does not reveal all constraint singularities.", "A closed chain can have multiple assembly modes for one actuator vector."), ("Closed-chain kinematics is implicit geometry.", "The Jacobian of constraints is the local diagnostic.")),
    _chapter(8, "chapter-08-dynamics-of-open-chains", "Dynamics of Open Chains", "08-dynamics-of-open-chains.ipynb", (271, 324), 2, "dynamics", "mass matrices, Newton-Euler recursion, and task-space inertia", "mass eigenvalue and response plots", "open-chain-dynamics", "how inertia changes with configuration and coordinates", "How do forces, torques, velocities, and accelerations interact through the robot's configuration?", ("mass matrix", "Coriolis term", "gravity term", "Newton-Euler", "Lagrangian dynamics", "task-space inertia", "gearing"), ("The mass matrix is a metric on joint velocity.", "Recursive dynamics computes forces by passing motion and wrench information along the chain.", "Actuators and gearing reshape apparent inertia."), "Plot a two-link mass matrix over configuration and connect eigenvalues to kinetic-energy ellipses.", ("The same physical energy can look different in different coordinates.", "Ignoring motor inertia can make high gear ratios look unrealistically easy."), ("Dynamics adds a metric to kinematics.", "Efficient algorithms are structured passes through the chain.")),
    _chapter(9, "chapter-09-trajectory-generation", "Trajectory Generation", "09-trajectory-generation.ipynb", (325, 352), 2, "planning", "time scaling and smooth paths", "time-scaling curves and phase limits", "trajectory-generation", "how a path becomes a timed motion subject to boundary and speed limits", "How do we turn geometric waypoints into a smooth, executable time history?", ("path", "trajectory", "time scaling", "cubic", "quintic", "via point", "phase plane"), ("A path names where to go; a trajectory names when to be there.", "Boundary conditions decide polynomial degree.", "Time-optimal scaling is a phase-plane feasibility problem."), "Compare cubic and quintic timing, then mark where acceleration constraints would bind.", ("Smooth position alone is not enough for torque-controlled machines.", "Via points can create hidden velocity discontinuities."), ("Trajectory generation separates geometry from timing.", "Boundary derivatives are design constraints, not afterthoughts.")),
    _chapter(10, "chapter-10-motion-planning", "Motion Planning", "10-motion-planning.ipynb", (353, 402), 2, "planning", "configuration-space obstacles and graph search", "grid planner, obstacle field, and sampling intuition", "motion-planning", "how collision constraints turn geometry into search", "How does a robot find a feasible path through a high-dimensional space with obstacles?", ("C-space obstacle", "complete planner", "grid", "RRT", "PRM", "potential field", "smoothing"), ("Collision checking defines the free subset of configuration space.", "Search trades resolution, optimality, and speed.", "Sampling planners replace exhaustive grids with exploration bias."), "Solve a grid planning problem and compare the resulting path with a potential-field intuition.", ("A workspace obstacle becomes a complicated C-space obstacle.", "Potential fields can create false local traps."), ("Planning is geometry plus search policy.", "Resolution and sampling choices are part of the model.")),
    _chapter(11, "chapter-11-robot-control", "Robot Control", "11-robot-control.ipynb", (403, 460), 3, "dynamics", "feedback, force control, impedance, and hybrid control", "response plots and projection geometry", "robot-control", "how error dynamics and task constraints shape closed-loop behavior", "How do feedback laws turn desired motion or contact behavior into stable robot action?", ("error dynamics", "PD control", "computed torque", "force control", "hybrid control", "impedance", "low-level loop"), ("A controller is a chosen error dynamics, not only a torque formula.", "Model-based cancellation simplifies behavior when the model is trustworthy.", "Contact tasks split motion and force directions."), "Tune a second-order joint response and inspect how damping changes overshoot and settling.", ("High gains can hide model error until contact or saturation appears.", "Force control without a contact model is ill posed."), ("Control closes the loop around the geometry and dynamics.", "Hybrid and impedance ideas are projections of task intent.")),
    _chapter(12, "chapter-12-grasping-and-manipulation", "Grasping and Manipulation", "12-grasping-and-manipulation.ipynb", (461, 512), 3, "contact", "contact kinematics, friction cones, and closure", "friction cone and grasp matrix", "grasping-manipulation", "how contact normals and friction span or fail to span object wrenches", "What can contacts prevent, permit, or command when a robot touches an object?", ("contact mode", "rolling", "sliding", "friction cone", "form closure", "force closure", "grasp matrix"), ("A contact constrains relative motion and can transmit only certain forces.", "Friction cones turn unilateral contact into geometry.", "Closure is a spanning question in wrench space."), "Build a planar grasp matrix and compare rank with friction-cone intuition.", ("A visually symmetric grasp can still miss a wrench direction.", "Force closure depends on friction and contact placement together."), ("Manipulation is contact geometry plus actuation.", "Motion freedoms and force freedoms are dual views.")),
    _chapter(13, "chapter-13-wheeled-mobile-robots", "Wheeled Mobile Robots", "13-wheeled-mobile-robots.ipynb", (513, 564), 3, "mobile", "omnidirectional and nonholonomic mobile bases", "unicycle rollout and wheel velocity map", "wheeled-mobile-robots", "how wheel constraints shape reachable velocity and path geometry", "How do wheel designs decide which chassis velocities are directly available?", ("SE(2)", "wheel constraint", "omniwheel", "mecanum wheel", "nonholonomic", "odometry", "mobile manipulation"), ("Wheel rolling constraints map chassis twists to wheel speeds.", "Omnidirectional bases span planar velocity directly.", "Nonholonomic bases can reach poses by paths, not arbitrary instantaneous sideways motion."), "Roll out a unicycle trajectory and compare it with a mecanum wheel velocity map.", ("A car-like robot can be controllable while still unable to move sideways instantly.", "Odometry integrates small errors into pose drift."), ("Mobile robot kinematics is constraint geometry on SE(2).", "Instantaneous mobility and global reachability are different questions.")),
    _chapter(14, "appendix-a-summary-of-useful-formulas", "Summary of Useful Formulas", "appendix-a-summary-of-useful-formulas.ipynb", (565, 574), 4, "appendix", "formula dependency and quick checks", "formula map with residual checks", "formula-summary", "which identities are safe to reuse and what they preserve", "Which formulas are the course's reusable computational contracts?", ("SO(3)", "SE(3)", "adjoint", "PoE", "Jacobian", "dynamics", "planning"), ("A formula is a contract between representation and invariant.", "The safest summary includes the domain, frame, and failure modes.", "Numerical checks catch frame-order mistakes early."), "Assemble a formula checklist and run compact residual tests for rotations and transforms.", ("Memorizing formulas without domains creates frame errors.", "A summary page is dangerous if it omits conventions."), ("Reusable formulas should be paired with invariants.", "The appendix works as a computational checklist.")),
    _chapter(15, "appendix-b-other-representations-of-rotations", "Other Representations of Rotations", "appendix-b-other-representations-of-rotations.ipynb", (575, 584), 4, "appendix", "Euler angles, roll-pitch-yaw, quaternions, and Cayley parameters", "rotation parameter comparison curves", "rotation-representations", "where each parameterization is smooth, singular, or redundant", "Why do so many rotation coordinates exist, and what does each one trade away?", ("Euler angles", "roll-pitch-yaw", "unit quaternion", "Cayley-Rodrigues", "singularity", "double cover", "minimal coordinate"), ("Three-parameter coordinates are compact but cannot be globally nonsingular.", "Unit quaternions avoid gimbal lock by adding a constraint and a sign ambiguity.", "Cayley parameters exclude rotations by pi."), "Compare parameter curves as the rotation angle approaches pi.", ("A coordinate singularity is not a physical singularity.", "Quaternion sign flips can break interpolation if ignored."), ("Rotation representations are engineering tradeoffs.", "The invariant object is the rotation, not the coordinate chart.")),
    _chapter(16, "appendix-c-denavit-hartenberg-parameters", "Denavit-Hartenberg Parameters", "appendix-c-denavit-hartenberg-parameters.ipynb", (585, 596), 4, "kinematics", "D-H frames compared with product of exponentials", "link-frame assignment and transform comparison", "denavit-hartenberg", "how local link conventions differ from screw-axis models", "How do D-H parameters encode a serial chain, and when is PoE clearer?", ("link frame", "common normal", "D-H table", "alpha", "a", "d", "theta", "PoE comparison"), ("D-H is a local frame convention for neighboring links.", "PoE stores joint screws in a common frame.", "Both describe the same forward kinematics when conventions match."), "Build a two-link D-H transform and compare the endpoint with a PoE-style planar model.", ("Frame assignment ambiguity can move signs between parameters.", "A D-H table without a diagram is easy to misread."), ("D-H remains useful for compact serial-chain tables.", "PoE often exposes geometric screw axes more directly.")),
    _chapter(17, "appendix-d-optimization-and-lagrange-multipliers", "Optimization and Lagrange Multipliers", "appendix-d-optimization-and-lagrange-multipliers.ipynb", (597, 598), 4, "appendix", "constraint gradients and multiplier geometry", "level curves and active constraint normals", "optimization-lagrange", "how optimality appears as aligned gradients under constraints", "What does a multiplier say geometrically about constrained robot decisions?", ("objective", "constraint", "gradient", "multiplier", "KKT condition", "active set", "normal direction"), ("At a constrained optimum, feasible tangent motion cannot reduce the objective.", "The multiplier scales a constraint normal to match objective gradient.", "Optimization shows up in planning, control allocation, and contact forces."), "Draw level sets and a constraint curve, then check gradient alignment at a candidate optimum.", ("A stationary point can be a maximum, minimum, or saddle.", "Inactive inequality constraints should not appear as active normals."), ("Lagrange multipliers are geometry of normals.", "Robotics optimization is easier to debug by drawing feasible directions.")),
]


def chapters_for_part(part_slug: str) -> list[Chapter]:
    return [chapter for chapter in CHAPTERS if chapter.part_slug == part_slug]


def chapter_by_slug(slug: str) -> Chapter:
    for chapter in CHAPTERS:
        if chapter.slug == slug:
            return chapter
    raise KeyError(slug)

