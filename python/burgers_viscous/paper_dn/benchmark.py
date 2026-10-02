#!/usr/bin/env python3
"""Independent fixed-viscosity Dirichlet–Neumann Burgers paper benchmark.

This file does not replace the Appendix D.3 cell-average implementation.
All state/adjoint errors below concern the explicitly documented nodal scheme.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shlex
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from numpy.polynomial import Polynomial
from scipy.integrate import quad, solve_bvp
from scipy.sparse import diags
from scipy.sparse.linalg import splu

VERSION = "1.0.0"
MAX_INTERVALS = 65536
DEFAULT_FD_STEPS = (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7)


def infinity(values):
    return float(np.max(np.abs(values)))


class Benchmark:
    """Nodal central conservative residual; unknowns are u_1,...,u_N."""
    def __init__(self, intervals=64, mu=.2, nu=.1, objective="q0", target_mu=.2, correction_atol=2e-12,
                 correction_rtol=2e-12, max_iterations=35):
        if not isinstance(intervals, int) or not 8 <= intervals <= MAX_INTERVALS:
            raise ValueError(f"intervals must be an integer in [8,{MAX_INTERVALS}]")
        if not np.isfinite([mu, nu, target_mu, correction_atol, correction_rtol]).all():
            raise ValueError("all inputs must be finite")
        if not 0 <= mu <= 1 or not 0 < nu <= 1:
            raise ValueError("require 0 <= mu <= 1 and 0 < nu <= 1")
        if objective not in ("q0", "one_x") or not 0 <= target_mu <= 1:
            raise ValueError("objective must be q0 or one_x; require 0 <= target_mu <= 1")
        if correction_atol <= 0 or correction_rtol < 0 or max_iterations < 1:
            raise ValueError("invalid Newton stopping settings")
        self.n, self.h, self.mu, self.nu = intervals, 1/intervals, mu, nu
        self.objective_name, self.target_mu = objective, target_mu
        self.c0 = (nu+1+target_mu)/(2*nu+1+target_mu)
        self.lambda_star = Polynomial([0., 1., -self.c0])
        target_state = Polynomial([1., 2*target_mu, -target_mu])
        self.q = (-target_state*self.lambda_star.deriv()-nu*self.lambda_star.deriv(2)
                  if objective == "q0" else Polynomial([1., 1.]))
        self.z = Polynomial([0., 2., -1.])
        self.exact_gradient = float((self.q*self.z).integ()(1)-(self.q*self.z).integ()(0))
        self.x = np.arange(intervals+1, dtype=float)/intervals
        self.weights = self.h*self.q(self.x[1:])
        self.weights[-1] *= .5
        self.atol, self.rtol, self.max_iterations = correction_atol, correction_rtol, max_iterations

    def exact(self, x, mu=None):
        mu = self.mu if mu is None else mu
        x = np.asarray(x)
        return 1+mu*x*(2-x)

    def source(self, x, mu=None):
        mu = self.mu if mu is None else mu
        x = np.asarray(x)
        return 2*mu*(1-x)*self.exact(x, mu)+2*self.nu*mu

    def source_mu(self, x):
        x = np.asarray(x)
        return 2*(1-x)*(1+2*self.mu*x*(2-x))+2*self.nu

    def residual(self, unknown, mu=None, jacobian=False):
        if len(unknown) != self.n:
            raise ValueError("state length must equal the number of intervals")
        full = np.r_[1., unknown]
        residual = np.empty(self.n, dtype=np.result_type(full, self.mu if mu is None else mu))
        h, nu = self.h, self.nu
        # Algebraically identical conservative operator, evaluated without
        # subtracting separately rounded squares or 2*u from an O(1) state.
        residual[:-1] = ((full[2:]-full[:-2])*(full[2:]+full[:-2])/(4*h)
                        -nu*((full[2:]-full[1:-1])-(full[1:-1]-full[:-2]))/h**2
                        -self.source(self.x[1:-1], mu))
        residual[-1] = (3*(full[-1]-full[-2])-(full[-2]-full[-3]))/(2*h)
        if not jacobian:
            return residual
        # At row j, exact convection derivatives are +/-u_(j+/-1)/(2h).
        lower = -full[1:-1]/(2*h)-nu/h**2
        upper = full[2:]/(2*h)-nu/h**2
        A = diags((lower, np.full(self.n, 2*nu/h**2), upper),
                  (-1, 0, 1), shape=(self.n, self.n), format="lil")
        A[-1, :] = 0
        A[-1, -3:] = np.array([1., -4., 3.])/(2*h)
        return residual, A.tocsc()

    def parameter_jacobian(self, unknown=None):
        # The boundary constraints have zero explicit mu derivative.
        out = np.zeros(self.n)
        out[:-1] = -self.source_mu(self.x[1:-1])
        return out

    def objective(self, unknown):
        # q is frozen at target_mu and the chosen nu, including in FD re-solves.
        return .5*self.h*self.q(0.)+np.dot(self.weights, unknown)

    def exact_objective(self):
        product = self.q*Polynomial([1., 2*self.mu, -self.mu])
        return float(product.integ()(1)-product.integ()(0))

    def solve(self, mu=None, start=None):
        # Constant 1 is independent of the nonconstant manufactured solution.
        u = np.ones(self.n) if start is None else np.asarray(start, dtype=float).copy()
        history = []
        for iteration in range(self.max_iterations):
            residual, A = self.residual(u, mu, jacobian=True)
            factor = splu(A)
            correction = factor.solve(-residual)
            rn, cn = infinity(residual), infinity(correction)
            threshold = self.atol+self.rtol*infinity(u)
            history.append({"iteration": iteration, "residual_inf": rn,
                            "correction_inf": cn, "correction_threshold": threshold})
            if cn <= threshold:
                return {"u": u, "A": A, "factor": factor, "history": history,
                        "converged": True, "termination": "Newton correction criterion",
                        "accepted_updates": iteration, "final_correction_inf": cn,
                        "initial_guess": "constant 1" if start is None else "provided warm start"}
            damping, accepted = 1., False
            for _ in range(25):
                trial = u+damping*correction
                trial_residual = self.residual(trial, mu)
                # PDE-density residuals amplify binary64 cancellation by h^-2.
                # Use the frozen-Jacobian Newton correction as line-search merit;
                # still record the unscaled residual at every accepted state.
                trial_merit = infinity(factor.solve(-trial_residual))
                if np.min(trial) > .05 and trial_merit < (1-1e-4*damping)*cn:
                    u, accepted = trial, True
                    history[-1]["accepted_damping"] = damping
                    history[-1]["accepted_trial_correction_merit"] = trial_merit
                    break
                damping *= .5
            if not accepted:
                raise RuntimeError(f"Newton line search failed at N={self.n}, iteration={iteration}, residual={rn:g}, correction={cn:g}")
        raise RuntimeError(f"Newton iteration limit at N={self.n}")

    def continuous_reference(self, tolerance=1e-10):
        begin = time.perf_counter()
        def rhs(x, y):
            return np.vstack((y[1], (-self.q(x)-self.exact(x)*y[1])/self.nu))
        def boundary(left, right):
            return np.array([left[0], self.nu*right[1]+self.exact(1.)*right[0]])
        mesh = np.linspace(0, 1, 201)
        sol = solve_bvp(rhs, boundary, mesh, np.zeros((2, len(mesh))),
                        tol=tolerance, max_nodes=50000)
        if not sol.success:
            raise RuntimeError("continuous adjoint BVP failed: "+sol.message)
        gradient, integration_error = quad(lambda x: sol.sol(x)[0]*self.source_mu(x),
                                           0, 1, epsabs=1e-11, epsrel=1e-11)
        details = {"gradient": float(gradient), "exact_gradient": self.exact_gradient,
                   "gradient_absolute_error": abs(float(gradient)-self.exact_gradient),
                   "quad_error_estimate": float(integration_error),
                   "bvp_tolerance": tolerance, "bvp_max_nodes": 50000,
                   "bvp_mesh_nodes": len(sol.x),
                   "bvp_max_rms_residual": float(np.max(sol.rms_residuals)),
                   "left_dirichlet_residual": float(sol.sol(0)[0]),
                   "right_robin_residual": float(self.nu*sol.sol(1)[1]+self.exact(1.)*sol.sol(1)[0]),
                   "elapsed_seconds": time.perf_counter()-begin,
                   "mathematical_proof": False,
                   "convention": "physical lambda: -u*lambda_prime-nu*lambda_double_prime=q; Lagrange multiplier=-lambda"}
        if self.objective_name == "q0" and self.mu == self.target_mu:
            probe = np.linspace(0, 1, 1001)
            details["analytic_lambda_star_max_error"] = infinity(sol.sol(probe)[0]-self.lambda_star(probe))
            details["analytic_lambda_star_derivative_max_error"] = infinity(sol.sol(probe)[1]-self.lambda_star.deriv()(probe))
        return sol, details

    def analyse(self, solved, reference):
        u, A, factor = solved["u"], solved["A"], solved["factor"]
        rp = self.parameter_jacobian(u)
        tangent = factor.solve(-rp)
        psi = factor.solve(-self.weights, trans="T")
        gradient = float(np.dot(psi, rp))
        forward = float(np.dot(self.weights, tangent))
        full = np.r_[1., u]
        exact = self.exact(self.x)
        density = np.r_[0., -psi[:-1]/self.h, -psi[-1]/self.nu]
        continuous = reference.sol(self.x)[0]
        rng = np.random.default_rng(20261002)
        v, w = rng.normal(size=self.n), rng.normal(size=self.n)
        left, right = float(np.dot(w, A@v)), float(np.dot(A.T@w, v))
        state_l2 = float(np.sqrt(np.trapezoid((full-exact)**2, self.x)))
        adjoint_l2 = float(np.sqrt(np.trapezoid((density-continuous)**2, self.x)))
        return {"objective": float(self.objective(u)), "exact_objective": self.exact_objective(),
                "objective_error": abs(float(self.objective(u))-self.exact_objective()),
                "gradient": gradient, "tangent_gradient": forward, "exact_gradient": self.exact_gradient,
                "gradient_error": abs(gradient-self.exact_gradient), "tangent_adjoint_error": abs(gradient-forward),
                "state_l2_error": state_l2, "state_linf_error": infinity(full-exact),
                "adjoint_l2_error": adjoint_l2, "adjoint_linf_error": infinity(density-continuous),
                "adjoint_endpoint_error": abs(float(density[-1]-continuous[-1])),
                "adjoint_penultimate_ratio": float(density[-2]/continuous[-2]),
                "adjoint_density_normalization": "physical lambda[0]=0; lambda[j]=-psi[j-1]/h for 1<=j<N; lambda[N]=-psi[N-1]/nu; psi is the negative Lagrange multiplier convention",
                "primal_residual_inf": infinity(self.residual(u)),
                "primal_interior_pde_residual_inf": infinity(self.residual(u)[:-1]),
                "primal_neumann_residual": float(self.residual(u)[-1]),
                "tangent_residual_inf": infinity(A@tangent+rp),
                "adjoint_residual_inf": infinity(A.T@psi+self.weights),
                "transpose_relative_error": abs(left-right)/max(1., abs(left), abs(right)),
                "parameter_complex_step_error_inf": infinity(self.residual(u, self.mu+1j*1e-30).imag/1e-30-rp),
                "jacobian_shape": list(A.shape), "jacobian_nonzeros": int(A.nnz),
                "newton_correction_inf": solved["final_correction_inf"],
                "newton_accepted_updates": solved["accepted_updates"],
                "newton_converged": solved["converged"],
                "newton_termination": solved["termination"],
                "newton_line_search_merit": "frozen-Jacobian correction infinity norm, Armijo coefficient 1e-4",
                "newton_initial_guess": solved["initial_guess"],
                "newton_history": solved["history"],
                "_full_state": full, "_density": density, "_continuous": continuous, "_tangent": np.r_[0., tangent]}

    def finite_difference(self, solved, gradient, step):
        begin = time.perf_counter()
        if not np.isfinite(step) or step <= 0:
            raise ValueError("FD step must be finite and positive")
        plus = self.solve(self.mu+step, start=solved["u"])
        minus = self.solve(self.mu-step, start=solved["u"])
        value = float((self.objective(plus["u"])-self.objective(minus["u"]))/2/step)
        return {"step": step, "full_rerun_gradient": value,
                "adjoint_gradient": gradient, "absolute_error": abs(value-gradient),
                "exact_gradient_error": abs(value-self.exact_gradient),
                "elapsed_seconds": time.perf_counter()-begin,
                "perturbed_newton_updates": [plus["accepted_updates"], minus["accepted_updates"]],
                "perturbed_correction_inf": [plus["final_correction_inf"], minus["final_correction_inf"]],
                "perturbed_residual_inf": [infinity(self.residual(plus["u"], self.mu+step)), infinity(self.residual(minus["u"], self.mu-step))],
                "perturbed_initial_guess": "base root warm start; both nonlinear problems re-solved"}


def result_for(model, reference, fd_step=1e-5):
    begin = time.perf_counter()
    solved = model.solve()
    result = model.analyse(solved, reference)
    result["gradient_check"] = model.finite_difference(solved, result["gradient"], fd_step)
    # Only the profile is sampled; all norms use every node.
    indices = np.unique(np.r_[np.linspace(0, model.n, min(257, model.n+1), dtype=int), model.n-2, model.n-1, model.n])
    result["profile"] = {"node_index": indices.tolist(), "x": model.x[indices].tolist(),
                         "u": result.pop("_full_state")[indices].tolist(),
                         "exact": model.exact(model.x[indices]).tolist(),
                         "adjoint_density": result.pop("_density")[indices].tolist(),
                         "continuous_adjoint": result.pop("_continuous")[indices].tolist(),
                         "tangent": result.pop("_tangent")[indices].tolist()}
    result.update({"intervals": model.n, "nodes": model.n+1, "unknowns": model.n,
                   "mu": model.mu, "nu": model.nu, "elapsed_seconds": time.perf_counter()-begin,
                   "objective_name": model.objective_name, "target_mu": model.target_mu,
                   "q_coefficients_ascending": model.q.coef.tolist(),
                   "q_is_frozen_with_respect_to_design_mu": True,
                   "memory_measured": False, "peak_memory_bytes": None})
    return result


def provenance():
    return {"version": VERSION,
            "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "command": shlex.join([sys.executable]+sys.argv),
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "platform": platform.platform(), "mathematical_proof": False,
            "max_intervals": MAX_INTERVALS, "memory_measured": False,
            "formulation": "paper_dn nodal central conservative PDE residual plus backward 2nd-order Neumann constraint; composite-trapezoid objective"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    grid = parser.add_mutually_exclusive_group()
    grid.add_argument("--intervals", type=int, default=None)
    grid.add_argument("--grids", default=None, help="comma-separated numbers of uniform intervals")
    parser.add_argument("--mu", type=float, default=.2)
    parser.add_argument("--nu", type=float, default=.1)
    parser.add_argument("--objective", choices=("q0", "one_x"), default="q0")
    parser.add_argument("--target-mu", type=float, default=.2)
    parser.add_argument("--correction-atol", type=float, default=2e-12)
    parser.add_argument("--correction-rtol", type=float, default=2e-12)
    parser.add_argument("--max-iterations", type=int, default=35)
    parser.add_argument("--fd-step", type=float, default=1e-5)
    parser.add_argument("--fd-scan", action="store_true")
    parser.add_argument("--fd-intervals", type=int, default=256)
    parser.add_argument("--fd-steps", default=",".join(map(str, DEFAULT_FD_STEPS)))
    parser.add_argument("--output", type=Path, default=Path("results/refinement.json"))
    args = parser.parse_args()
    grids = [int(n) for n in args.grids.split(",")] if args.grids else [args.intervals or 64]
    if sorted(set(grids)) != grids:
        parser.error("grids must be distinct and increasing")
    settings = {"mu": args.mu, "nu": args.nu, "objective": args.objective, "target_mu": args.target_mu,
                "correction_atol": args.correction_atol,
                "correction_rtol": args.correction_rtol, "max_iterations": args.max_iterations}
    reference, continuous = Benchmark(grids[0], **settings).continuous_reference()
    begin = time.perf_counter()
    results = [result_for(Benchmark(n, **settings), reference, args.fd_step) for n in grids]
    for prev, current in zip(results, results[1:]):
        for key in ("state_l2_error", "adjoint_l2_error", "gradient_error", "objective_error"):
            if current[key] > 0 and prev[key] > 0:
                current[key+"_observed_order"] = float(np.log(prev[key]/current[key])/np.log(current["intervals"]/prev["intervals"]))
    scan = None
    if args.fd_scan:
        scan_model = Benchmark(args.fd_intervals, **settings)
        solved = scan_model.solve()
        analysis = scan_model.analyse(solved, reference)
        steps = [float(s) for s in args.fd_steps.split(",")]
        scan = {"intervals": args.fd_intervals, "mu": args.mu, "nu": args.nu,
                "base_gradient": analysis["gradient"], "results": [scan_model.finite_difference(solved, analysis["gradient"], step) for step in steps]}
    payload = {"provenance": provenance(), "inputs": {**settings, "grids": grids,
               "gradient_check_step": args.fd_step, "fd_scan": args.fd_scan,
               "fd_intervals": args.fd_intervals if args.fd_scan else None,
               "fd_steps": [float(s) for s in args.fd_steps.split(",")] if args.fd_scan else [],
               "fixed_viscosity_within_refinement": True},
               "continuous_reference": continuous, "results": results, "fd_scan": scan,
               "elapsed_seconds_excluding_continuous_bvp": time.perf_counter()-begin}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
    columns = ["intervals", "mu", "nu", "state_l2_error", "adjoint_l2_error", "gradient", "exact_gradient", "gradient_error",
               "objective_error", "primal_residual_inf", "newton_correction_inf", "newton_accepted_updates", "elapsed_seconds"]
    with args.output.with_suffix(".csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader(); writer.writerows(results)
    if scan:
        scan_columns = ["step", "full_rerun_gradient", "adjoint_gradient", "absolute_error", "exact_gradient_error", "elapsed_seconds"]
        with args.output.with_name(args.output.stem+"_fd.csv").open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=scan_columns, extrasaction="ignore")
            writer.writeheader(); writer.writerows(scan["results"])
    print(json.dumps({"output": str(args.output), "implementation_sha256": payload["provenance"]["implementation_sha256"],
                      "largest_intervals": max(grids), "largest_result": {k: results[-1][k] for k in columns},
                      "continuous_gradient_error": continuous["gradient_absolute_error"],
                      "max_grid_fd_error": max(r["gradient_check"]["absolute_error"] for r in results)}, indent=2))


if __name__ == "__main__":
    main()
