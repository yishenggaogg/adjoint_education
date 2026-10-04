# 1D viscous Burgers: independent Python reproduction of the NODE-centred scheme

This directory reproduces the **steady, smooth experiment of the node-centred viscous Burgers page**. It is the partner of the cell-centred package (`../solve.py`): the same equation, manufactured solution, design `D = (a, phi, nu)`, objective, Rusanov flux and reconstructions, but the unknowns are the point values at the **nodes** and the control volumes are the **dual intervals** around them; the two end rows are Dirichlet constraints. It has its own entry point `solve_node.py`, imports nothing from the cell package and was written from the page's specification, independently of the page's JavaScript model. It does not implement the cell-centred scheme, the transient problem or any proof.

## Run

Python 3.10 or newer, NumPy and SciPy are required. From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q test_solver_node.py          # or: .venv/bin/python test_solver_node.py
.venv/bin/python solve_node.py --cells 128 --nu 0.01 --amplitude 0.2 --phase 0.07 \
  --reconstruction none --gradient-check --output results/run128.json
.venv/bin/python solve_node.py --grids 32,64,128,256,512,1024,2048,4096,8192,16384 \
  --nu 0.01 --amplitude 0.2 --phase 0.07 --reconstruction none --gradient-check --continuous-adjoint \
  --output results/refinement_none.json
.venv/bin/python solve_node.py --cells 65536 --nu 0.01 --amplitude 0.2 --phase 0.07 --reconstruction none \
  --gradient-check --output results/large_65536.json
```

`--cells N` is the number of **intervals** (the unknown vector has `N+1` entries); `--reconstruction first` selects the first-order scheme (zero slopes), `none` the unlimited linear reconstruction, `smooth` the rational reconstruction with `--epsilon 0.01`. The grid is uniform. Amplitude and phase change the source and the Dirichlet data together; the viscosity is held fixed across each mesh study. The viscosity gradient varies `nu` **and the manufactured source together**, so the continuum value is zero; it is not the sensitivity of a fixed external source. The invocation writes JSON and a CSV twin. Every output records the invoked command (relative: `python3 solve_node.py ...`), the implementation version and the SHA-256 of `solve_node.py`, the UTC time, the package versions and the host platform, and is labelled `mathematical_proof = false`. The files in `examples/` are measured evidence; editing the solver requires regenerating them (`test_published_examples_are_current` checks the hash). Times are measured on the recorded machine, not performance guarantees.

## The scheme (statement by statement)

`h = 1/N`, nodes `x_j = j h` (`j = 0..N`), unknown `U_j` = point value, dual volume `V_j` of width `h` (interior) and `h/2` (`j = 0, N`). Face `f` (`f = 0..N-1`) lies between node `f` and node `f+1` at `x_{f+1/2}`; every face has a node on each side, the boundary faces included.

```text
1  slopes     interior j: sigma_j = 0 | (l+r)/2 | l r (l+r)/(l^2+r^2+eps^2)   (first | none | smooth),  l = U_j-U_{j-1}, r = U_{j+1}-U_j
              boundary nodes: sigma_0 = 0 | U_1-U_0 | U_1-U_0,  sigma_N = 0 | U_N-U_{N-1} | U_N-U_{N-1}
2  flux       H_f = (qL^2+qR^2)/4 - (qR-qL) - nu (U_{f+1}-U_f)/h,   qL = U_f + sigma_f/2,  qR = U_{f+1} - sigma_{f+1}/2
3  scatter    R_f += H_f (f >= 1),   R_{f+1} -= H_f (f <= N-2)
4  source     R_j -= Q_j - Q_{j-1}  (1 <= j <= N-1),   Q_f = q*(x_{f+1/2}) = u*^2/2 - nu u*_x   (exact integrated source)
5  rows       R_0 = U_0 - u_in,   R_N = U_N - u_out        (unit scaling; u_in = u_out = u*(0) = u*(1))
J_h = sum_j w_j U_j,   w_0 = h/2,  w_j = h (1 + x_j),  w_N = h          (trapezoid rule for (1+x) u)
```

The manufactured solution is `u*(x) = 1 + a sin(2 pi (x-phi))`, `q* = u*^2/2 - nu u*_x`, `s = q*_x`, `J* = 3/2 - a cos(2 pi phi)/(2 pi)`, `grad J* = (-cos(2 pi phi)/(2 pi), a sin(2 pi phi), 0)`. Defaults `nu = 0.01, a = 0.2, phi = 0.07`. The reference states are the exact **nodal values** `u*(x_j)` (there are no cell averages); sampling `u*` is only Newton's initial guess. For the exact nodal values `J_h(u*) - J* = (h^2/12) u*_x(0) + O(h^4)` (Euler-Maclaurin; `u*` is periodic), so even a perfect nodal solution has a quadrature error against the continuum objective.

## Tangent, adjoint, gradients

The state Jacobian `A = dR/dU` has at most five bands (three for `first`), rows `0` and `N` are identity rows; it is assembled sparsely and factorised by sparse LU, which also solves the transposed system. `R_D = dR/dD` has the closed-form source and boundary derivatives (the code verifies it against holomorphic complex step); `u_in`, `u_out` enter only the constraint rows.

```text
A v_k = -R_D e_k  (three solves),   J-dot = w^T v_k        A^T psi = -w,   dJ_h/dD = R_D^T psi
```

`solve_node.py` also contains the vectorised statement-level tangent sweep (`residual_d`) and reverse sweep (`residual_b`, seed `R-bar = psi` gives `U-bar = A^T psi = -w` and `D-bar = dJ_h/dD`) used by the tests for the dot identity `R-bar^T R-dot = U-bar^T U-dot + D-bar^T D-dot`. With `--gradient-check` the adjoint gradient is compared with central differences of `J_h` with two **complete** perturbed Newton re-solves each, along the direction `(1, 0.3, 0)` (as in the cell package) and along each design axis (the viscosity axis included).

## The multipliers of the rows (measured; differs from a statement one might expect)

The adjoint multipliers of the flux-balance rows are the continuous adjoint itself, **`psi_j ~ lambda(x_j)` (no factor `h`)**: the weights `w_j` and the rows `R_j` both carry one factor `h`. The multipliers of the two constraint rows are the boundary fluxes of the continuous adjoint, **`psi_0 -> nu lambda_x(0)` and `psi_N -> -nu lambda_x(1)`**, where `-u lambda_x - nu lambda_xx = -(1+x)`, `lambda(0) = lambda(1) = 0` (at the defaults `nu lambda_x(0) = -1.4265680`, `-nu lambda_x(1) = -0.022034551`; there is no `h/2` factor and no end-cell formula). `--continuous-adjoint` solves this boundary value problem independently with SciPy's `solve_bvp`, reports its defect (`continuous_bvp_max_rms_residual`), `adjoint_l1_reference_error = h sum_{j=1}^{N-1} |psi_j - lambda(x_j)|` (interior nodes), `nu_lambda_x_0`, `minus_nu_lambda_x_1`, the errors `psi_0_boundary_flux_error`, `psi_N_boundary_flux_error`, and the amplitude/phase gradient obtained from `-int lambda s_p dx + nu [lambda_x g_p]_0^1` (both boundary terms matter).

## Output fields (per grid, `results[i]`)

| field | meaning |
|---|---|
| `cells`, `nu`, `amplitude`, `phase`, `reconstruction`, `epsilon` | the run (`cells` = number of intervals `N`) |
| `objective`, `exact_objective` | `J_h` and the continuum `J*` |
| `gradient`, `tangent_gradient`, `reverse_gradient`, `exact_gradient` | `dJ_h/dD` by the adjoint solve, by the three tangent solves, by the reverse sweep; the exact `grad J*` (viscosity component 0) |
| `gradient_error_inf`, `amplitude_gradient_error`, `phase_gradient_error`, `viscosity_gradient_error` | errors of the adjoint gradient against the exact one (`viscosity_gradient_error = abs(g_nu)`) |
| `gradient_duality_error`, `gradient_reverse_error`, `reverse_state_adjoint_error`, `transpose_relative_error` | tangent = adjoint, reverse sweep = adjoint, `U-bar = -w`, `w^T A v = v^T A^T w` |
| `state_l1_error`, `state_linf_error` | `h sum_j abs(U_j - u*(x_j))` and `max_j abs(U_j - u*(x_j))` against the exact **nodal** values |
| `primal_residual_inf`, `primal_residual_density_inf` | `max abs(R)`; `max_{1<=j<=N-1} abs(R_j)/h` |
| `newton_correction_inf`, `newton_history` | last Newton correction; per iteration `residual_inf`, `correction_inf`, `step` |
| `tangent_residual_inf`, `adjoint_residual_inf`, `jacobian_nonzeros` | linear residuals, number of nonzeros of `A` |
| `psi_0`, `psi_N` | multipliers of the constraint rows |
| `exact_nodal_residual_inf`, `..._boundary_rows_inf`, `..._inner_rows_inf`, `..._constraint_rows_inf` | `R(u*_nodal)`: rows `1..N-1`; rows `1` and `N-1`; rows `2..N-2`; rows `0` and `N` |
| `exact_nodal_objective`, `objective_quadrature_error`, `objective_quadrature_remainder` | `J_h(u*)`, `J_h(u*) - J*`, `J_h(u*) - J* - (h^2/12) u*_x(0)` |
| `gradient_check` | central differences with full re-solves: along `(1, 0.3, 0)` and along each axis (`axis_central_differences`, `axis_absolute_errors`) |
| `adjoint_l1_reference_error`, `adjoint_linf_reference_error`, `continuous_bvp_max_rms_residual`, `continuous_adjoint_gradient_amplitude_phase`, `nu_lambda_x_0`, `minus_nu_lambda_x_1`, `psi_0_boundary_flux_error`, `psi_N_boundary_flux_error` | with `--continuous-adjoint` (see above) |
| `*_observed_order` | `log(e_previous/e)/log(N/N_previous)` for the state (`L1`, `Linf`), the gradient (`inf`, amplitude, phase, viscosity) and the adjoint quantities, from the second grid on (`null` if an error vanishes) |
| `profile` | at most 161 sampled nodes: `x`, `u`, `exact_nodal_value`, `adjoint` (`psi_j`, ends included), `amplitude_tangent`, and `continuous_adjoint` (`lambda(x_j)`) when computed |

The CSV twin has the columns `cells, nu, reconstruction, state_l1_error, state_linf_error, gradient_error_inf, primal_residual_inf, primal_residual_density_inf, newton_correction_inf, adjoint_residual_inf, elapsed_seconds` (those of the cell package) followed by `psi_0, psi_N, exact_nodal_residual_boundary_rows_inf, exact_nodal_residual_inner_rows_inf`.

## Validation and limits

`test_solver_node.py` checks: the state and design Jacobians against complex step (all kinds), the band structure and the identity constraint rows; the statement-level reverse sweep against `A^T` and `R_D^T` and the dot identity; the first-order interior row in closed form; a constant exact solution; the residual of the exact nodal values and its orders; the Euler-Maclaurin form of `J_h(u*) - J*`; tangent = adjoint = reverse gradient, against central differences with full re-solves (every design axis) and against the complex-step residual; Newton from the exact nodal values (full steps) and from a poor start (backtracking); orders of convergence of the state; the continuous adjoint, the gradient formula with its boundary terms and the boundary-flux behaviour of `psi_0`, `psi_N`; the command line round trip; the provenance hash. When the independent dense reference `viscous_node/audit/ref_model.py` is present (it is not part of the published package) the solutions, adjoints and gradients are compared with it too. Planted faults in the solver (sign errors, a lost term, wrong weights, a wrong boundary slope derivative, a line search that accepts everything, an adjoint solve with `A` instead of `A^T`) are each caught by at least one test.

The CLI rejects nonfinite inputs, `N < 8`, `N > 65536`, `nu <= 0`, `nu > 1`, `|a| > 0.5` and nonpositive epsilon. Newton has 35 iterations, 30 backtracking halvings per iteration, the positive state box `0.1 < U < 1.9` and stops when the max-norm of the correction is at most `1e-13` (that last correction is applied); `newton_history` has one entry per linear solve, the last one included. A trial step is accepted if `max abs(R)` decreases by the factor `1 - 1e-4 step`, **or** if it is below the rounding floor `16 eps (1 + nu/h)` of the residual: for `N = 65536` the residual of a converged state is about `3e-13` (the ulp of `U` times `nu/h`), and below that level the merit function cannot see a real correction of `4e-11`, which the finite-difference re-solves of the largest run need. For `N <= 4096` the floor is never reached before the last step. The primal residual of a converged large-`N` run is limited by rounding in the viscous flux (about `nu * 1e-16 / h`), so `primal_residual_inf` grows like `N` for large `N`. Profiles contain at most 161 samples. For many simultaneous jobs set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`.

## What the recorded runs show (numerical evidence, not theorems)

In the fixed-viscosity studies of `examples/` (`nu = 0.01`, `N = 32 ... 16384`): `none` shows second-order decay of the nodal state error, `first` first order; `smooth` with `epsilon` fixed stagnates on moderate meshes and approaches the `first` errors on fine meshes (the limiter then switches off the interior slopes). Errors of individual gradient components are not monotone (they change sign), so their observed orders scatter on moderate meshes. Unresolved layers (`h` larger than `nu/u_in`) dominate the early grids. The scoped results of the separate inviscid Burgers proof cannot be imported as a proof of this viscous scheme: these tests assume a locally differentiable discrete solution branch with a nonsingular Jacobian, and no existence, uniqueness, uniform stability, convergence or Lean statement is made.
