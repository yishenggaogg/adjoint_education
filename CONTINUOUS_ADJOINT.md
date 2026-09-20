# Continuous adjoints and what adjoint consistency means here

This note derives the continuous problems corresponding to the teaching pages. It accompanies Section 15 of the six two-dimensional and quasi-one-dimensional pages. The original Burgers pair already treats this question. Results below concern smooth, steady solutions on the stated fixed domains. A discrete dot-product test proves a transpose identity, not consistency with a continuous boundary-value problem.

## 1. Signs, measures and three distinct checks

Write the steady PDE as `R(u,p)=0`, the functional as `J`, and use

$$
\mathcal L=J-\int_\Omega\lambda^T R\,d\Omega.
$$

The pages solve `A_h^T ψ_h = −g_h`. Our continuous multiplier has the opposite sign: `λ_h=−ψ_h` on conservation equations. Those residuals are **integrated** balances, so there is no additional division by control-volume measure. Rows replaced by algebraic boundary constraints carry constraint multipliers; their values are not point samples of the continuous field.

Three tests answer different questions:

1. A transpose/dot test checks the implementation of `A_h^T`.
2. Finite differences of the same discrete problem check `dJ_h/dp`.
3. Comparing an independently solved continuous dual with a sequence of refined discrete duals tests consistency in a stated norm. It requires matching PDE, boundary conditions, functional, domain, and target data.

A decreasing error on finitely many meshes is numerical evidence, not a theorem of convergence. Boundary layers or characteristic jumps can prevent maximum-norm convergence even when an integral norm decreases.

## 2. Well-posedness is not the same as adjoint consistency

A discrepancy is a diagnostic opportunity, not by itself proof of ill-posedness. Specify the state and trace spaces, admissible data, functional, and norms first. Hadamard well-posedness requires existence, uniqueness and continuous dependence. A correctly derived continuous dual can be well posed while a discrete boundary closure is inconsistent; a well-posed equation with the wrong objective boundary data is simply the wrong dual. Constraint multipliers, limited regularity and finite reference error are other sources of apparent disagreement.

### Linearization, kernels and stability

Include the homogeneous linearized primal boundary constraints in the domain `X` of the operator `D:X→Y`. If this is a bounded isomorphism between suitable spaces, its Banach adjoint is also a bounded isomorphism between the dual spaces. This is a sufficient local framework, not a conclusion obtained merely by writing a formal differential expression. An unbounded PDE operator must first be given a domain/graph norm or a suitable weak realization. For a nonlinear primal, existence and uniqueness alone do not guarantee a differentiable solution map; the local smoothness and invertibility hypotheses must be checked on the chosen branch.

For `D*λ=g`, a primal null mode implies the necessary compatibility condition

$$
 Dv=0\quad\Longrightarrow\quad g[v]=\langle\lambda,Dv\rangle=0.
$$

A nonzero element of `ker D*` makes a solvable dual nonunique. Orthogonality to the primal kernel alone is not a general infinite-dimensional existence theorem: closed range and stability still matter. The required estimate has the form

$$
 \|\lambda\|_{Y^*}\le C\|g\|_{X^*}
$$

for homogeneous dual boundary data; inhomogeneous boundary data contribute their appropriate trace norm. A bounded inverse at every mesh size is not enough either: the stability bound must be uniform in the properly weighted discrete norms. Raw Euclidean condition numbers without accounting for integrated residuals and control-volume weights are not themselves a continuum diagnosis.

### An explicit transport example

For `c>0`, fixed primal inflow and objective variation `∫₀¹g v dx+b v(1)`, the Green identity for the primal linearization `c v'` gives

$$
 -c\lambda'=g,\qquad c\lambda(1)=b,\qquad
 \lambda(x)=\frac{b}{c}+\frac1c\int_x^1g(s)\,ds.
$$

- **Missing outlet data:** an arbitrary additive constant remains, so uniqueness fails.
- **An extra copied primal inlet datum `λ(0)=0`:** existence requires `b+∫g=0`. With `g=1,b=0`, the correct solution is `(1−x)/c`; the extra inlet condition makes the problem unsolvable.
- **Loss of uniform stability:** `‖λ‖∞≤(|b|+‖g‖₁)/c`. Taking `g=1,b=0` attains the `1/c` amplification. Each fixed `c>0` is well posed, but there is no bound uniform as `c→0` for this data class. At zero speed the original operator degenerates.

In the original 2-D body example, normals point out of the **fluid** domain: the upwind body is therefore primal outflow. A characteristic already carrying `u=1` cannot satisfy zero physical flux there. This is first a failure of the assumed smooth positive primal problem, not merely a poor discrete approximation to an otherwise established dual. At a putative wall state `u=0`,

$$
 \delta(\tfrac12u^2\beta\cdot n)=u(\beta\cdot n)v=0
$$

for every variation `v`: the flux constraint loses its first-order information while the characteristic speed degenerates. Copying the wall condition onto a formal dual cannot restore a valid smooth solution branch. Weak/entropy formulations would need separate trace and differentiability analysis.

For the characteristic-boundary contrast, every interior ray reaches outflow in finite distance. Boundary data determine the field almost everywhere; tangency/corner jumps are compatible with a nonsmooth solution space and do not by themselves imply ill-posedness. The ratio `b_u/(a·n)` requires compatibility at characteristic boundaries: in this particular body objective its numerator and denominator contain a cancelling normal factor. One must not infer blow-up from the denominator alone.

### What the other cases demonstrate

**Advection–diffusion.** Positive diffusion provides an elliptic principal part, not a universal invertibility proof for arbitrary lower-order and Robin coefficients. Homogeneous kernels and the assumptions of applicable energy or maximum-principle estimates still need attention. The independent solves support this parameter set; they do not prove a theorem for all parameters. Setting the wall dual to zero instead of the objective-required one can define a different well-posed problem, but yields the wrong functional sensitivity. Imposing both state and normal derivative at the far field is generally an overconstraint. Treating a replaced-row multiplier as a wall field sample is yet another, algebraic interpretation error.

**Quasi-1-D Euler.** The speeds `u−c,u,u+c` explain the two inlet/one outlet primal conditions and reversed dual counts for the stated positive subsonic branch. Counts are necessary, not sufficient: propagation and the boundary constraints together must yield an invertible boundary-value operator. At a sonic point `B` is singular, so the current representation using `(Bᵀ)⁻¹` fails; throat compatibility/regularity analysis is required. This does not imply that all transonic adjoints fail to exist. Shocks require shock-position variations and internal conditions. These phenomena are outside the current numerical evidence; see the [continuous nozzle analysis of Giles and Pierce](https://authors.library.caltech.edu/records/p4y1e-z6x26). The distinct effects of strong/weak boundary treatment on numerical duals are discussed by [Duivesteijn et al.](https://ir.cwi.nl/pub/10851).

The teaching sequence is therefore: identify the continuous primal and chosen branch; derive the dual **including its boundary domain**; examine existence, uniqueness and stability; only then test consistent, stable approximation of that problem. A counterexample should retain its failed premise visibly, rather than silently substituting another model and declaring success.

## 3. Nonlinear scalar transport: a formal adjoint is not enough

The actual flux is nonlinear:

$$
 R(u)=\nabla\cdot\bigl(\tfrac12u^2\beta\bigr),\qquad
 \beta=(1,\tfrac12),\quad a=u\beta.
$$

For a state variation `v=δu`,

$$
 R_u v=\nabla\cdot(av),\qquad
 \int_\Omega\lambda R_uv
 =-\int_\Omega(a\cdot\nabla\lambda)v
  +\int_{\partial\Omega}\lambda(a\cdot n)v.
$$

For `J=∫Ω j(u) + ∫∂Ω b(u)`, stationarity gives

$$
 -a\cdot\nabla\lambda=j_u,\qquad
 b_u-\lambda(a\cdot n)=0
$$

on portions where the primal trace is free. On a prescribed inflow trace `v=0`, no adjoint datum is prescribed. Thus the adjoint receives its data at **primal outflow**, with `λ=b_u/(a·n)`, away from characteristic points.

### The original closed zero-flux body is not a smooth transport wall

The original two-dimensional pages set the numerical body flux to zero independently of the interior state. But a smooth trace of the stated PDE has physical flux

$$
 \tfrac12u^2\beta\cdot n.
$$

The fixed vector `β` is not tangent to the closed polygon. Wherever `β·n≠0`, zero physical flux requires `u=0`. This would impose an additional zero value at body **outflow**. In the positive, source-free branch, `u` is constant along each straight characteristic. A characteristic entering from the far field with `u=1` and ending on the upwind side of the body cannot also have `u=0` there. At `u=0` the characteristic speed degenerates, so one cannot repair the derivation by dividing the boundary condition by `u`.

Consequently the present zero-flux numerical closure does not provide the smooth, positive classical boundary-value problem needed for the above continuous-dual comparison. This is not a proof that no weak or measure-valued formulation could ever be defined. Such a formulation would require an entropy/boundary-trace specification and an appropriate sensitivity analysis, absent from these pages. The finite-dimensional residual, transpose, and discrete gradients remain well defined.

### A clearly separated, computable characteristic-boundary contrast

For the new comparison only, treat both outer and inner boundaries by characteristics: prescribe `u=1` where `β·n<0`, and use the physical interior flux where `β·n>0`. The domain, interior numerical flux and its `ε=0.8` remain the pages' own. The exact primal is `u=1`.

Keep the drag-like functional

$$
 J=\int_{\Gamma_w}\tfrac12u^2(e\cdot n)\,ds,
 \qquad e=\beta/|\beta|,
$$

but at prescribed inflow use the **prescribed trace** in the functional, not a free interior value. This readout change is part of the contrast and is not silently applied to the original example. The continuous dual is

$$
 -\beta\cdot\nabla\lambda=0,\quad
 \lambda=1/|\beta|\text{ on body outflow},\quad
 \lambda=0\text{ on outer outflow}.
$$

At an interior point, follow the ray in direction `+β` to its first boundary intersection. The value is `1/|β|` if that intersection is the body, and zero otherwise. This is an exact characteristic calculation, not a transpose solve. It has jumps along rays from body tangencies/corners. The comparison uses volume-weighted L2 error; boundary nodes are excluded from the node-centred norm. No smooth maximum-norm convergence is claimed. This contrast does not validate continuous consistency of the original zero-flux wall.

## 4. Advection–diffusion: keep the total boundary flux

Here

$$
 R(u)=\nabla\cdot q,\qquad q=\tfrac12u^2\beta-\nu\nabla u,
 \quad \nu=0.5,\quad a=u\beta.
$$

The complete Green identity is

$$
 \int_\Omega\lambda R_uv
 =\int_\Omega(-a\cdot\nabla\lambda-\nu\Delta\lambda)v
 +\int_{\partial\Omega}\{\lambda[(a\cdot n)v-\nu\partial_n v]
                         +\nu(\partial_n\lambda)v\}\,ds.
$$

There is no `−(∇·a)λ` in the volume dual: the primal linearization is in conservative form.

### Wall functional and wall dual value

The wall has fixed Dirichlet data `u=u_w=0`. Its objective is the total outward fluid flux into the body,

$$
 J=\int_{\Gamma_w}q\cdot n\,ds.
$$

At fixed geometry, `v=0` on the wall but `∂n v` is free. Hence

$$
 \delta J=-\nu\int_{\Gamma_w}\partial_n v\,ds.
$$

Combining this with the boundary term of `−∫λR` gives `ν(λ−1)∂n v`. Therefore

$$
 -u\beta\cdot\nabla\lambda-\nu\Delta\lambda=0,
 \qquad \lambda|_{\Gamma_w}=1.
$$

Zero wall adjoint data would be wrong for this flux functional.

### What the implemented far field means in the continuous limit

Let `b=β·n` for the **unit** outward normal. Dividing the integrated numerical face flux by face length, the implemented far-field total flux is

$$
 H(u,u_\infty,n)=
 \begin{cases}
 \tfrac14b(u^2+u_\infty^2)+\epsilon(u-u_\infty),&b<0,\\
 \tfrac12bu^2,&b\ge0.
 \end{cases}
$$

The consistent continuum interpretation is the single condition `q·n=H`. In particular, on inflow this is a nonlinear Robin condition,

$$
 -\nu\partial_nu=\tfrac14b(u_\infty^2-u^2)+\epsilon(u-u_\infty).
$$

The code's “zero diffusive face flux” and external convective state must **not** be read as simultaneously imposing continuum `u=u∞` and `∂n u=0`. On outflow, `q·n=H` reduces to `∂n u=0`.

Linearization gives `δ(q·n)=H_u v`, so the free far-field variation yields

$$
 \nu\partial_n\lambda+H_u\lambda=0,\qquad
 H_u=\begin{cases}\tfrac12bu+\epsilon,&b<0,\\bu,&b\ge0.\end{cases}
$$

Notice that `ε` remains in this boundary-value problem. It vanishes with refinement as an interior artificial diffusion, but the boundary flux per unit length retains it.

For the incoming datum, stationarity gives an independently checkable scalar sensitivity:

$$
 \frac{dJ}{du_\infty}
 =-\int_{\Gamma_{\rm in}}\lambda(\tfrac12b u_\infty-\epsilon)\,ds.
$$

### Node-centred reaction objective: reconstruct the field

The node page has `J_h=−1_W^T R_raw` and replaced rows `u_i−u_w=0`. Partition the raw Jacobian into free and wall blocks. The free part of the adjoint satisfies

$$
 A_{ff}^T\psi_f=A_{wf}^T1_W.
$$

Thus the continuous field to compare is `λ_f=−ψ_f` and **λ_W=1**, since

$$
 A_{ff}^T\lambda_f+A_{wf}^T1_W=0.
$$

The raw `−ψ_W` is a boundary-constraint multiplier. Plotting it as the wall trace would manufacture an apparent inconsistency.

### Shape derivative, with fixed boundary classification

For completeness, let `x_t=x+tV(x)` be a smooth domain deformation, with constant physical `β,ν,ε,u∞,u_w=0`. The inflow/outflow partition is held fixed and no face crosses `b=0`. Write `DV_ij=∂j V_i`. At a stationary state the Lagrangian reduces to

$$
 \mathcal L=\int_\Omega[\nabla\lambda\cdot f(u)-\nu\nabla\lambda\cdot\nabla u],dx
             -\int_{\Gamma_\infty}\lambda H,ds.
$$

The wall objective cancels the wall residual boundary term because `λ=1`. Differentiating this expression while holding the pulled-back state and multiplier fixed gives

$$
\begin{aligned}
\delta J={}&\int_\Omega\{[\nabla\lambda\cdot f-\nu\nabla\lambda\cdot\nabla u]\nabla\cdot V
 -(DV^T\nabla\lambda)\cdot f\\
 &\hspace{12mm}+\nu(DV^T\nabla\lambda)\cdot\nabla u
 +\nu\nabla\lambda\cdot(DV^T\nabla u)\}\,dx\\
 &-\int_{\Gamma_\infty}\lambda\{C\beta\cdot[(\nabla\cdot V)I-DV^T]n
 +\epsilon(u-u_\infty)\,1_{b<0}\nabla_\Gamma\cdot V\}\,ds,
\end{aligned}
$$

where `C=(u²+u∞²)/4` on inflow and `C=u²/2` on outflow. Nonconstant transported boundary data would add their material derivatives. This formula is derived here but the added experiment validates `dJ/du∞`, **not this full shape derivative**; the earlier pages' coordinate checks remain discrete checks.

### Independent numerical reference

A P1 finite-element reference solves the nonlinear primal weak form on a triangulation of the **same polygon**, then directly assembles the derived continuous dual weak form

$$
 \int_\Omega[\nu\nabla\lambda\cdot\nabla v-u(\beta\cdot\nabla\lambda)v]
 +\int_{\Gamma_\infty}H_u\lambda v=0,
$$

with `λ=1` on the wall. It does not call the finite-volume transpose. Triangle and edge quadrature integrate the polynomial integrands. References on 1,088, 4,224 and 16,640 vertices check reference resolution. The final reference is still a numerical approximation. FV state and dual equations use the original page cores, solved to tight algebraic residuals with sparse direct Newton/linear solves for this offline study. This changes the verification solver, not the finite-volume equations or the page's Jacobi demonstrations.

## 5. Quasi-one-dimensional Euler

This note denotes the continuous objective by `J`; the quasi-1-D pages call it `L`, reserving `J_h` for the discrete Jacobian and `Ψ` for its discrete adjoint. The equations are otherwise identical.

Let `U=(ρ,ρu,ρE)^T`, `B=∂F/∂U`, `e₂=(0,1,0)^T` and `p_U=∂p/∂U` as a row. On `0<x<1`,

$$
 R(U,A)=(AF(U))'-A'p(U)e_2=0.
$$

At fixed area,

$$
 R_Uv=(ABv)'-A'e_2p_Uv.
$$

Integrating once,

$$
 \int_0^1\lambda^TR_Uv
 =[\lambda^TABv]_0^1+
 \int_0^1[-AB^T\lambda'-A'p_U^T\lambda_2]^Tv.
$$

For `J=∫j(U,A,A')dx`, the continuous adjoint is therefore

$$
 -AB^T\lambda'-A'p_U^T\lambda_2=j_U^T.
$$

There is **no derivative of `AB`** left in this expression: integration by parts acts on the entire conservative product. The pressure-source term must not be omitted.

The two existing objectives give

$$
\begin{array}{ll}
 j=\tfrac12A(p-p_t)^2:&j_U^T=A(p-p_t)p_U^T,\\
 j=pA':&j_U^T=A'p_U^T.
\end{array}
$$

The target is fixed during differentiation. Each FV grid generates its target by solving the original target duct `A_t=A(1−0.04 sin πx)` with the same FV scheme; the continuous reference uses that duct's smooth isentropic solution. The targets therefore converge with refinement instead of being accidentally reoptimized during a derivative evaluation.

### Boundary conditions from admissible primal variations

At the subsonic inlet,

$$
 C_0v(0)=0,\qquad C_0=\begin{bmatrix}(p_0)_U\\(T_0)_U\end{bmatrix};
$$

at the outlet, `C₁v(1)=0` with `C₁=p_U`. If columns of `N₀,N₁` span these null spaces, the uncancelled endpoint term vanishes for every admissible variation exactly when

$$
 N_0^TAB^T\lambda(0)=0,\qquad
 N_1^TAB^T\lambda(1)=0.
$$

There is one scalar adjoint condition at the inlet and two at the outlet. Giving all three adjoint components zero at either end would overconstrain the system. Equivalently, `AB^Tλ=C^Tμ` at an endpoint; `μ` is a boundary multiplier. If boundary data `c` change, their contribution is `+μ₀^Tδc₀−μ₁^Tδc₁`, with this sign convention.

For the node page, three conservation rows are replaced, leaving fewer conservation multipliers at the endpoints. Neither endpoint triplet is a complete sample of the continuous vector field. Field norms in the new study exclude the two endpoint nodes; all equations and multipliers are retained when checking residuals and gradients. This exclusion does not certify pointwise boundary consistency.

### Area sensitivity, including endpoint terms

At fixed state,

$$
 R_A\delta A=(\delta A F)'-p e_2\delta A'.
$$

Consequently

$$
\begin{aligned}
 \delta J={}&\int_0^1(j_A+\lambda'^TF)\delta A
                 +(j_{A'}+p\lambda_2)\delta A'\,dx
             -[\lambda^TF\delta A]_0^1\\
 ={}&\int_0^1\{j_A+\lambda'^TF-(j_{A'}+p\lambda_2)'\}\delta A\,dx
       +[(j_{A'}+p\lambda_2-\lambda^TF)\delta A]_0^1.
\end{aligned}
$$

For inverse design `j_A=(p−p_t)²/2`, `j_A'=0`; for thrust `j_A=0`, `j_A'=p`. The experiment uses `δA=−0.02 sin²(πx)`, so endpoint terms vanish. A general area change cannot drop them.

### Reference calculation and limitations

With unit total pressure and temperature and `γ=1.4`,

$$
 T=(1+0.2M^2)^{-1},\quad p=T^{3.5},\quad\rho=T^{2.5},\quad
 \dot m=A\sqrt{1.4}M(1+0.2M^2)^{-3}.
$$

Back pressure `p_b=0.9` fixes outlet Mach and mass flow. At every position the unique positive subsonic root gives the smooth primal reference. The continuous dual is solved as a three-component boundary-value ODE using the null-space conditions. Tightening its tolerance checks reference error; independently perturbing the smooth duct checks the continuous gradient. Native FV refinement uses 12 through 384 intervals and both original schemes.

An instructive special case is thrust: integration of the momentum equation gives `J=[A(ρu²+p)]₀¹`. For this isentropic subsonic family with fixed endpoint areas, total data and back pressure, the endpoint states are fixed. Thus the continuous thrust sensitivity to the tested interior area direction is exactly zero. The nonzero finite-grid sensitivities are discretization effects, not evidence that the continuous derivative is wrong. Use absolute error for this comparison, never divide by a vanishing continuous gradient.

This calculation excludes shocks, sonic throats, characteristic sign changes and nonunique branches. Those need additional analysis; a successful smooth subsonic test does not establish their adjoint consistency.

## 6. Evidence and references

The new page tables and interactive field plots contain offline-computed results from the local `adjoint_edu_src/consistency` implementation. Reproduce locally with `python3 numerics.py ad`, `python3 numerics.py q1d`, and `python3 numerics.py transport`; `check_consistency.py` checks the stored numerical contracts. These intermediate implementation files are deliberately not published or committed in `adjoint_edu`.

The equations above are derived for the actual teaching models. For related continuous nozzle solutions and the significance of boundary treatment, see [Giles and Pierce, *Analytic adjoint solutions for the quasi-one-dimensional Euler equations*](https://authors.library.caltech.edu/records/p4y1e-z6x26) and [Duivesteijn et al., *On the adjoint solution of the quasi-1D Euler equations: the effect of boundary conditions and the numerical flux function*](https://ir.cwi.nl/pub/10851).
