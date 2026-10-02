# `paper_dn`: independent viscous Burgers paper benchmark

This directory is a separate nodal Dirichlet–Neumann case. It preserves the parent Appendix D.3 `solve.py`, cell-average residual, data and page. It does not replace that benchmark or claim that its proof status applies here.

Use Python 3.10 or newer:

```sh
cd python/burgers_viscous/paper_dn
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v test_dn.py
python benchmark.py --grids 16,32,64,128,256,512,1024,2048,4096,8192,16384 \
  --mu .2 --nu .1 --objective q0 --target-mu .2 \
  --fd-scan --fd-intervals 256 --output results/refinement_q0.json
python benchmark.py --grids 16,32,64,128,256,512,1024,2048,4096,8192,16384 \
  --mu .2 --nu .05 --objective one_x \
  --fd-scan --fd-intervals 256 --output results/refinement_one_x.json
```

The data delivered here were generated with system Python and dependencies exposed through `PYTHONPATH=/tmp/adjoint_python_deps`; installing the declared dependencies is the portable reproduction route. JSON records the actual Python/NumPy/SciPy versions, platform, command, time and SHA-256 of `benchmark.py`. Rerunning after code changes produces new provenance rather than reusing old results.

## Frozen problem and two explicit objectives

The PDE, boundary conditions and manufactured family are

\[
(u^2/2-\nu u')'=s(x,\mu),\quad 0<x<1,\qquad u(0)=1,\quad u'(1)=0,
\]
\[
u_*(x,\mu)=1+\mu x(2-x),\qquad
s(x,\mu)=2\mu(1-x)u_*(x,\mu)+2\nu\mu.
\]

Only \(\mu\) is differentiated. Every refinement and FD scan holds \(\nu>0\) fixed. Defaults are \(\mu=\mu_0=0.2\), \(\nu=0.1\), `objective=q0`. CLI accepts \(0\le\mu,\mu_0\le1\) and \(0<\nu\le1\), but numerical success outside the delivered baselines is not certified.

The default paper weight is constructed once, from the frozen target \(\mu_0\) and the fixed case viscosity:

\[
c_0=\frac{\nu+1+\mu_0}{2\nu+1+\mu_0},\qquad
\lambda_*(x)=x(1-c_0x),\qquad
q_0=-u_*(x,\mu_0)\lambda_*'-\nu\lambda_*''.
\]

\(J(\mu)=\int_0^1q_0(x)u(x,\mu)dx\). The code builds \(q_0\) as a polynomial and **does not change it when \(\mu\) is perturbed**. `--target-mu` controls the target only; `--mu` controls the differentiated state/source. Changing `--nu` constructs a different fixed-viscosity case and its weight; no viscosity design derivative is claimed.

`--objective one_x` retains the secondary weight \(q(x)=1+x\), with
\(J_*=3/2+13\mu/12\) and \(g_*=13/12\). Its delivered baseline uses \(\nu=0.05\), explicitly distinguished from the paper default. For either weight, the code obtains \(J_*\) and \(g_*\) by exact polynomial integration of \(q u_*\) and \(q x(2-x)\), respectively. At the default `q0` parameters, \(g_*=0.26047619047619053\).

## Exact discrete operator and objective

Let \(h=1/N\), \(x_j=jh\), \(j=0,\ldots,N\). The \(N\) unknowns are \(u_1,\ldots,u_N\); \(u_0=1\) is fixed. These are nodal values, not cell averages. Interior rows are PDE-density residuals:

\[
R_j=\frac{u_{j+1}^2-u_{j-1}^2}{4h}
-\nu\frac{u_{j+1}-2u_j+u_{j-1}}{h^2}-s(x_j,\mu),
\qquad 1\le j<N.
\]

The final row is the Neumann constraint, with different units from the interior PDE density:

\[
R_N=\frac{3u_N-4u_{N-1}+u_{N-2}}{2h}=0.
\]

The discrete objective uses the composite trapezoid:

\[
J_h=h\left[\tfrac12q(0)u_0+\sum_{j=1}^{N-1}q(x_j)u_j+\tfrac12q(1)u_N\right].
\]

The implementation evaluates square differences as a product of sum and difference and second differences as differences of adjacent increments, including the final constraint. These are algebraically the displayed residual; the ordering reduces binary64 cancellation. It assembles an exact sparse Jacobian, with tridiagonal interior rows and three entries in the constraint row. No dense \(N\times N\) matrix is created.

Every main solve starts from the constant state \(u_j=1\), independently of the nonconstant manufactured solution. Newton uses sparse LU, a positive-state safeguard and a backtracking merit equal to the current Jacobian inverse residual correction. The stopping threshold is explicitly \(2\times10^{-12}+2\times10^{-12}\|u\|_\infty\) by default. Large-grid raw PDE residuals can be amplified by \(h^{-2}\) even when the Newton correction reaches machine precision. JSON reports both without replacing one by the other. A failed line search or iteration limit raises an error rather than saving a successful-looking root.

## Tangent, multiplier, physical adjoint and the endpoint layer

With \(A=R_u\), \(r_\mu=R_\mu\), and \(j=J_u\),

\[
Av=-r_\mu,\qquad A^T\psi=-j^T,\qquad
g_h=\psi^Tr_\mu=jv.
\]

The explicit \(r_\mu\) includes every manufactured-source derivative; both boundary derivatives are zero. The weight is frozen, so \(J_\mu=0\) at fixed unknowns. Independent complex-step residual checks validate the analytic parameter derivative, and full-rerun central differences re-solve both perturbed nonlinear roots at fixed weight/viscosity. FD roots use the base root as a warm start and satisfy the same stopping criterion.

The continuous **physical** adjoint convention is

\[
-u_*\lambda'-\nu\lambda''=q,\quad
\lambda(0)=0,\quad \nu\lambda'(1)+u_*(1)\lambda(1)=0,\qquad
g=\int_0^1\lambda s_\mu dx.
\]

The Lagrange multiplier convention in the transpose solve has the opposite sign: its continuum counterpart is \(-\lambda\). Consequently the displayed physical density is

\[
\lambda_{h,0}=0,\qquad
\lambda_{h,j}=-\psi_j/h\ (1\le j<N),\qquad
\lambda_{h,N}=-\psi_N/\nu.
\]

Here \(\psi_N\) is the multiplier of the derivative constraint; the continuous Green identity identifies the corresponding multiplier as \(-\nu\lambda(1)\), explaining the endpoint normalization. This normalization preserves the raw transpose result: **the measured penultimate-node ratio \(\lambda_{h,N-1}/\lambda(x_{N-1})\) approaches \(3/2\)** in the delivered baselines. The exact last two transpose equations imply this limit if the neighbouring interior trace convergence is additionally established; that trace theorem is unfinished. No artificial factor of \(2/3\) is applied. The raw physical adjoint has an observed global grid-L² rate near \(1/2\), while the state and objective gradient have observed rates near 2. These measured rates and the apparent lack of global adjoint \(L^\infty\) convergence are not presented as proved asymptotic results.

The reported `state_l2_error` and `adjoint_l2_error` are **trapezoidal nodal grid norms**:

\[
\|e\|_{2,h}=\left[h\left(\tfrac12 e_0^2+\sum_{j=1}^{N-1}e_j^2+\tfrac12 e_N^2\right)\right]^{1/2}.
\]

They are not advertised as exact integrals of interpolated error fields. All errors use the full grid; only plot profiles are subsampled, with the last three nodes always preserved. The continuous reference uses `solve_bvp` and independent quadrature. At \(\mu=\mu_0\) in `q0`, the analytic \(\lambda_*\) independently checks its value and derivative.

## Actual data and limits

Both stored refinements run from N=16 through **16384**. The N=16384 `q0` run reports state grid-L² error \(7.87\times10^{-11}\), raw adjoint grid-L² error \(2.79\times10^{-4}\), gradient error \(1.44\times10^{-9}\), and about **0.191 s** including two full FD re-solves. The corresponding `one_x` run reports \(8.54\times10^{-11}\), \(2.66\times10^{-4}\), \(8.70\times10^{-10}\), and about **0.198 s**. These are measurements on the recorded machine, not runtime guarantees.

Each result JSON contains `provenance`, frozen `inputs`, `continuous_reference`, full-grid `results`, and `fd_scan`. Each refinement exports a summary CSV and an additional `_fd.csv`. The six-step FD scan at N=256 uses 10⁻² through 10⁻⁷. JSON records step, actual FD result, adjoint difference, perturbed residuals/corrections/iterations and elapsed time. Tiny FD steps show roundoff effects; no monotone error decrease is promised.

The resource cap is **N≤65536**, but N=65536 was not run for this case. Peak memory was **not measured** and is stored as `null`; sparse storage structure is not presented as a measured memory number. Timing of the continuous BVP is reported separately from per-grid solve/derivative/FD timing.

## Mathematical status

The manufactured continuous state and baseline `q0` adjoint are explicit analytic candidates. For fixed positive viscosity, monotone positive \(u_*\), and homogeneous tangent conditions \(v(0)=0\), \(v'(1)=0\), integration by parts gives the coercivity identity

\[
a(v,v)=\nu\int_0^1(v')^2dx+\tfrac12\int_0^1u_*'v^2dx+\tfrac12u_*(1)v(1)^2
\ge\nu\int_0^1(v')^2dx.
\]

The accompanying [independent theoretical review](THEORY_REVIEW.md) proves continuous positive classical-solution uniqueness, a constructive linear inverse and the stated coercivity. For the original discrete operator it proves a unique nearby root in a specified ball, state/objective \(O(h^2)\) bounds and a weaker \(O(h)\) tangent/gradient convergence estimate under

\[
0\le\mu\le\tfrac12,\quad h<\frac{2\nu}{1+\mu},\quad
h\le\frac{\nu^2}{4\mu^2}\quad(\mu>0).
\]

The sufficient delivered-parameter mesh thresholds are N≥16 for `q0` with ν=0.1 and N≥64 for `one_x` with ν=0.05. The smaller secondary grids remain numerical experiments outside that sufficient certificate threshold. The theory's nearby-ball uniqueness does not imply global uniqueness of all discrete branches or certify that a particular Newton program entered the ball.

This is a hand-checkable analytic review with exact rational algebra, **not a Lean certificate or binary64/SciPy program-execution proof**. The observed second-order tangent/gradient rate, strong adjoint-field rate, near-boundary trace theorem and strict endpoint-layer lower bound remain unfinished. Numerical convergence and FD tests do not complete those obligations.
