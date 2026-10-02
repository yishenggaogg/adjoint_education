# 1D viscous Burgers — independent Python reproduction

This directory reproduces the **steady, smooth, cell-average experiment in Appendix D.3** of the teaching pages. It has its own `solve.py` entry point. It does not implement the inviscid main-page model, the transient Appendix D.4 experiment, or the full shock-proof goal.

## Run

Python 3.10 or newer, NumPy and SciPy are required. From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest -v test_solver.py
.venv/bin/python solve.py --cells 128 --nu .01 --amplitude .2 --phase .07 \
  --reconstruction none --gradient-check --output results/run128.json
.venv/bin/python solve.py --grids 32,64,128,256,512,1024,2048,4096,8192,16384 \
  --nu .01 --reconstruction none --gradient-check --continuous-adjoint \
  --output results/refinement_none.json
.venv/bin/python solve.py --cells 65536 --nu .01 --reconstruction none \
  --gradient-check --output results/large_65536.json
.venv/bin/python fd_scan.py --cells 128 --output results/fd_scan.json
```

`--reconstruction first` selects the first-order D.3 operator; `none` selects the unlimited linear reconstruction; `smooth` selects the original rational reconstruction with `--epsilon .01`. The grid is uniform. Source and both Dirichlet data change together when amplitude or phase changes. The viscosity is held fixed across each mesh study. The third reported gradient varies viscosity **and the manufactured source together**, so the exact continuum viscosity gradient is zero; it is not the sensitivity of a fixed external source.

An invocation writes JSON and CSV. JSON stores all three gradients, errors against exact cell averages, Newton correction and integrated residual norms, linear residuals, a complete rerun directional finite difference, observed orders, and a sampled profile. Every output records the invoked command, implementation version and SHA-256, UTC generation time, package versions and host platform. Existing example files are measured evidence; editing the solver requires regenerating them. Times are measured on the recorded machine, not performance guarantees.

## Equation, boundary and objective

On `0 <= x <= 1`, with fixed positive `nu`, solve

```text
q_x = s(x,a,phi,nu),        q = u²/2 - nu u_x
u*(x) = 1 + a sin(2 pi (x-phi))
s = (u*²/2 - nu u*_x)_x
u(0)=u*(0),                u(1)=u*(1)
J = integral_0^1 (1+x)u dx
```

Default parameters are `nu=.01, a=.2, phi=.07`. The exact objective is `1.5-a cos(2 pi phi)/(2 pi)`; its amplitude and phase derivatives are `-cos(2 pi phi)/(2 pi)` and `a sin(2 pi phi)`.

Unknowns are cell averages, `h=1/N`, `x_i=(i+.5)h`. The integrated residual and discrete objective are exactly those of the original JavaScript D.3 experiment:

```text
R_i = H_{i+1} - H_i - [q*(x_{i+1/2}) - q*(x_{i-1/2})]
J_h = h sum_i (1+x_i) U_i
H_f = (L_f²+R_f²)/4 - (R_f-L_f) - nu (U_right-U_left)/d_f
```

Rusanov speed is the fixed value `alpha=2`. The convective states use `U +/- slope/2`; viscous differences use unreconstructed cell averages. End cells have zero reconstruction slope. Boundary states are the analytic Dirichlet data, and diffusion distance is `h/2` at either boundary and `h` internally. Interior unlimited slope is `(U_{i+1}-U_{i-1})/2`. The smooth slope is `ab(a+b)/(a²+b²+epsilon²)` for one-sided differences `a,b`; it has no hard switch. Neither a TVD nor a positivity theorem is asserted for this smooth reconstruction.

The exact reference cell average is `1+a sinc(h) sin(2 pi (x_i-phi))`. Sampling `u*` is only Newton's initial guess; the nonlinear residual is solved. The objective uses midpoint cell weights, so even a perfect cell-average solution has quadrature error relative to the continuum objective.

## Tangent and adjoint

The analytic state Jacobian has at most five bands and is assembled sparsely. Sparse LU solves the same Jacobian and its transpose, with no dense `N x N` allocation. Source and boundary parameter derivatives use holomorphic complex step with the state held fixed; all three parameter paths are included.

```text
A v = -R_p dp
A^T psi = -J_U^T
g = J_p + psi^T R_p       (J_p=0 at fixed U for this objective)
```

For amplitude or phase, the continuous tangent satisfies `(u v - nu v_x)_x=s_p` with `v(0)=u*_p(0), v(1)=u*_p(1)`. The continuous adjoint satisfies `-u lambda_x - nu lambda_xx=-(1+x)`, `lambda(0)=lambda(1)=0`. Its gradient is

```text
g_p = -integral lambda s_p dx + nu [lambda_x u*_p]_0^1
```

Both boundary terms matter. Optional `--continuous-adjoint` solves this independent BVP with SciPy, reports its defect and the discrete-adjoint L1 difference, and checks this boundary pairing against the exact amplitude/phase gradient. Varying viscosity also differentiates the physical diffusion term itself, not merely `s`.

## Validation and limits

`test_solver.py` checks the analytic state Jacobian against complex step, transposes, parameter boundary/source derivatives, constant exact solutions, gradients against full reruns, refinement, the independent continuous boundary pairing, and six real runs of the original JS D.3 kernel at N=16/32 for all three smooth reconstruction choices. The JS results and source SHA-256 are archived in `examples/javascript_reference.json`; they are an explicit comparison fixture, not replacements for solver output.

The CLI rejects nonfinite inputs, `N<8`, `N>65536`, `nu<=0`, `nu>1`, `|a|>.5`, and nonpositive epsilon. Newton has 35 iterations and 25 line-search trials per iteration, with the original positive state box `.1<U<1.9`. A small Newton correction is required before success; both raw integrated and divided-by-h residuals are recorded. A finite difference performs two full perturbed solves. Profiles contain at most 161 samples. These bounds keep memory and output bounded. For many simultaneous jobs, set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1` in the invocation environment.

Unlimited reconstruction shows an asymptotic second-order trend in the recorded fixed-viscosity study; unreconstructed boundary cells and coarse unresolved viscous layers can dominate earlier. First-order errors approach first order. Finite-grid gradient errors need not be monotone, particularly the additional viscosity derivative.

These tests are **numerical evidence**, not a new existence, uniqueness, uniform stability, convergence or Lean proof. They assume a locally differentiable discrete solution branch with nonsingular Jacobian. No inviscid-limit, general shock, binary64 execution-certification or transient claim is made. The scoped proof of the separate inviscid Burgers model cannot be imported as a proof of this viscous equation.

The separate `fd_scan.py` measures seven finite-difference steps with fresh positive and negative primal solves. It records the actual histories, correction stopping threshold, residual density, inputs/code hashes and termination reason. Peak process memory was not measured (`memory_peak_measured=false`); a sparse nonzero count is not a process-memory measurement. The preserved D.3 and the newly authorized paper Dirichlet/Neumann benchmark have separate scripts and result files; their boundaries and discrete operators are not interchangeable.
