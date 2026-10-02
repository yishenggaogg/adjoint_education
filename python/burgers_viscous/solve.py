#!/usr/bin/env python3
"""Sparse reproduction of the steady, smooth Appendix D.3 Burgers experiment."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import splu
from scipy.integrate import solve_bvp
from scipy.integrate import quad

VERSION = "1.0.0"
MAX_CELLS = 65536


class Burgers:
    """Integrated FV residual, cell averages, alpha=2, analytic Dirichlet data."""
    def __init__(self, n=64, nu=.01, amplitude=.2, phase=.07,
                 reconstruction="none", epsilon=.01):
        if not isinstance(n, int) or not 8 <= n <= MAX_CELLS:
            raise ValueError(f"cells must be an integer in [8,{MAX_CELLS}]")
        if not 0 < nu <= 1 or not abs(amplitude) <= .5 or epsilon <= 0:
            raise ValueError("require 0 < nu <= 1, |amplitude| <= .5, epsilon > 0")
        if not np.isfinite([nu, amplitude, phase, epsilon]).all():
            raise ValueError("all parameters must be finite")
        if reconstruction not in ("first", "none", "smooth"):
            raise ValueError("reconstruction must be first, none or smooth")
        self.n, self.h, self.nu = n, 1/n, nu
        self.p = np.array([amplitude, phase, nu])
        self.kind, self.epsilon = reconstruction, epsilon
        self.x = (np.arange(n)+.5)/n
        self.edges = np.arange(n+1)/n
        self.weights = self.h*(1+self.x)
        self.distance = np.full(n+1, self.h)
        self.distance[[0, -1]] = self.h/2
        self.div = diags([-np.ones(n), np.ones(n)], [0, 1], shape=(n, n+1)).tocsr()
        self.raw_left = csr_matrix((np.ones(n), (np.arange(1, n+1), np.arange(n))), shape=(n+1, n))
        self.raw_right = csr_matrix((np.ones(n), (np.arange(n), np.arange(n))), shape=(n+1, n))

    def exact(self, x, p=None):
        a, phase, _ = self.p if p is None else p
        return 1+a*np.sin(2*np.pi*(np.asarray(x)-phase))

    def exact_average(self, p=None):
        a, phase, _ = self.p if p is None else p
        return 1+a*np.sinc(self.h)*np.sin(2*np.pi*(self.x-phase))

    def physical_flux(self, x, p=None):
        a, phase, nu = self.p if p is None else p
        z = 2*np.pi*(np.asarray(x)-phase)
        u = 1+a*np.sin(z)
        return .5*u*u-nu*2*np.pi*a*np.cos(z)

    def slopes(self, u, jacobian=False):
        s = np.zeros_like(u)
        a, b = u[1:-1]-u[:-2], u[2:]-u[1:-1]
        if self.kind == "first":
            da, db = np.zeros_like(a), np.zeros_like(b)
        elif self.kind == "none":
            s[1:-1] = .5*(a+b)
            da, db = np.full_like(a, .5), np.full_like(b, .5)
        else:
            den, num = a*a+b*b+self.epsilon**2, a*b*(a+b)
            s[1:-1] = num/den
            da = ((2*a*b+b*b)*den-2*a*num)/den**2
            db = ((a*a+2*a*b)*den-2*b*num)/den**2
        if not jacobian:
            return s
        i = np.arange(1, self.n-1)
        S = csr_matrix((np.r_[-da, da-db, db],
                        (np.tile(i, 3), np.r_[i-1, i, i+1])), shape=(self.n, self.n))
        return s, S

    def residual(self, u, p=None, jacobian=False):
        p = self.p if p is None else p
        s = self.slopes(u, jacobian)
        if jacobian:
            s, S = s
        left = np.r_[self.exact(0, p), u+.5*s]
        right = np.r_[u-.5*s, self.exact(1, p)]
        raw_l = np.r_[self.exact(0, p), u]
        raw_r = np.r_[u, self.exact(1, p)]
        flux = .25*(left*left+right*right)-(right-left)-p[2]/self.distance*(raw_r-raw_l)
        r = np.diff(flux)-np.diff(self.physical_flux(self.edges, p))
        if not jacobian:
            return r
        L = self.raw_left + .5*self.raw_left@S
        R = self.raw_right - .5*self.raw_right@S
        F = diags(.5*left+1)@L + diags(.5*right-1)@R - diags(p[2]/self.distance)@(self.raw_right-self.raw_left)
        return r, (self.div@F).tocsc()

    def parameter_jacobian(self, u):
        """Holomorphic complex step; holds u fixed, includes sources and boundaries."""
        out = []
        for k in range(3):
            p = self.p.astype(complex)
            p[k] += 1j*1e-30
            out.append(self.residual(u, p).imag/1e-30)
        return np.column_stack(out)

    def solve(self, start=None, maxiter=35):
        # Sampled continuum values are an initial guess only, as in Appendix D.3.
        u = self.exact(self.x) if start is None else np.array(start, dtype=float)
        history = []
        for k in range(maxiter):
            r, A = self.residual(u, jacobian=True)
            factor = splu(A)
            d = factor.solve(-r)
            rn, dn = float(np.max(abs(r))), float(np.max(abs(d)))
            history.append({"iteration": k, "residual_inf": rn, "correction_inf": dn})
            if dn <= 2e-11:
                return {"u": u, "history": history, "A": A, "factor": factor}
            step = 1.
            for _ in range(25):
                trial = u+step*d
                if (trial.min() > .1 and trial.max() < 1.9
                    and np.max(abs(self.residual(trial))) < (1-1e-4*step)*rn):
                    u = trial
                    break
                step *= .5
            else:
                raise RuntimeError(f"Newton line search failed at n={self.n}; residual={rn:g}, correction={dn:g}")
        raise RuntimeError(f"Newton iteration limit at n={self.n}")

    def analyse(self, solution):
        u, A, factor = solution["u"], solution["A"], solution["factor"]
        rp = self.parameter_jacobian(u)
        tangent = factor.solve(-rp)
        psi = factor.solve(-self.weights, trans="T")
        g = psi@rp
        gt = self.weights@tangent
        v, w = np.sin(7*self.x), np.cos(3*self.x)
        transpose_error = abs(w@(A@v)-v@(A.T@w))/max(1., abs(w@(A@v)), abs(v@(A.T@w)))
        a, phase, _ = self.p
        exact_gradient = np.array([-np.cos(2*np.pi*phase)/(2*np.pi), a*np.sin(2*np.pi*phase), 0.])
        e = u-self.exact_average()
        return {"objective": float(self.weights@u),
                "exact_objective": float(1.5-a*np.cos(2*np.pi*phase)/(2*np.pi)),
                "gradient": g.tolist(), "tangent_gradient": gt.tolist(),
                "exact_gradient": exact_gradient.tolist(),
                "gradient_error_inf": float(np.max(abs(g-exact_gradient))),
                "amplitude_gradient_error": float(abs(g[0]-exact_gradient[0])),
                "phase_gradient_error": float(abs(g[1]-exact_gradient[1])),
                "viscosity_gradient_error": float(abs(g[2])),
                "gradient_duality_error": float(np.max(abs(g-gt))),
                "transpose_relative_error": float(transpose_error),
                "state_l1_error": float(self.h*np.sum(abs(e))),
                "state_linf_error": float(np.max(abs(e))),
                "primal_residual_inf": float(np.max(abs(self.residual(u)))),
                "primal_residual_density_inf": float(np.max(abs(self.residual(u)))/self.h),
                "newton_correction_inf": solution["history"][-1]["correction_inf"],
                "tangent_residual_inf": float(np.max(abs(A@tangent+rp))),
                "adjoint_residual_inf": float(np.max(abs(A.T@psi+self.weights))),
                "jacobian_nonzeros": int(A.nnz), "psi": psi, "tangent": tangent}

    def gradient_check(self, solution, analysis, step=1e-5):
        direction = np.array([1., .3, 0.])
        objectives = []
        residuals = []
        for sign in (-1, 1):
            p = self.p+sign*step*direction
            other = Burgers(self.n, p[2], p[0], p[1], self.kind, self.epsilon)
            ss = other.solve(solution["u"])
            objectives.append(float(other.weights@ss["u"]))
            residuals.append(float(np.max(abs(other.residual(ss["u"])))))
        fd = (objectives[1]-objectives[0])/(2*step)
        predicted = float(np.dot(analysis["gradient"], direction))
        return {"step": step, "direction_amplitude_phase_nu": direction.tolist(),
                "full_rerun_central_difference": fd, "adjoint_directional_gradient": predicted,
                "absolute_error": abs(fd-predicted), "perturbed_primal_residuals_inf": residuals}

    def continuous_adjoint(self):
        def fun(x, y):
            return np.vstack((y[1], ((1+x)-self.exact(x)*y[1])/self.nu))
        def boundary(a, b):
            return np.array([a[0], b[0]])
        mesh = np.linspace(0, 1, 201)
        sol = solve_bvp(fun, boundary, mesh, np.zeros((2, len(mesh))), tol=1e-9, max_nodes=50000)
        if not sol.success:
            raise RuntimeError("continuous adjoint BVP failed: "+sol.message)
        return sol

    def continuous_gradient(self, sol):
        a, phase, nu = self.p
        k = 2*np.pi
        def v(x, index):
            z = k*(x-phase)
            return np.sin(z) if index == 0 else -k*a*np.cos(z)
        def source_derivative(x, index):
            z = k*(x-phase)
            u, ux = 1+a*np.sin(z), k*a*np.cos(z)
            if index == 0:
                vx, vxx = k*np.cos(z), -k*k*np.sin(z)
            else:
                vx, vxx = k*k*a*np.sin(z), k**3*a*np.cos(z)
            return ux*v(x, index)+u*vx-nu*vxx
        return [float(-quad(lambda x: sol.sol(x)[0]*source_derivative(x, j), 0, 1, epsabs=1e-11)[0]
                      +nu*(sol.sol(1)[1]*v(1, j)-sol.sol(0)[1]*v(0, j))) for j in (0, 1)]


def provenance():
    return {"version": VERSION, "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "command": " ".join([sys.executable]+sys.argv), "python": platform.python_version(),
            "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform(),
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "formulation": "Appendix D.3 integrated FV, alpha=2, analytic source/Dirichlet, half-cell boundary diffusion",
            "mathematical_proof": False, "max_cells": MAX_CELLS}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=128)
    parser.add_argument("--grids", help="comma-separated cells for a fixed-nu mesh study")
    parser.add_argument("--nu", type=float, default=.01)
    parser.add_argument("--amplitude", type=float, default=.2)
    parser.add_argument("--phase", type=float, default=.07)
    parser.add_argument("--reconstruction", choices=("first", "none", "smooth"), default="none")
    parser.add_argument("--epsilon", type=float, default=.01)
    parser.add_argument("--gradient-check", action="store_true")
    parser.add_argument("--continuous-adjoint", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    args = parser.parse_args()
    grids = [int(n) for n in args.grids.split(",")] if args.grids else [args.cells]
    if len(grids) > 20 or grids != sorted(set(grids)):
        parser.error("use at most 20 increasing distinct grids")
    rows, previous = [], None
    continuum = None
    for n in grids:
        model = Burgers(n, args.nu, args.amplitude, args.phase, args.reconstruction, args.epsilon)
        started = time.perf_counter()
        solution = model.solve()
        result = model.analyse(solution)
        if args.gradient_check:
            result["gradient_check"] = model.gradient_check(solution, result)
        if args.continuous_adjoint:
            if continuum is None:
                continuum = model.continuous_adjoint()
            result["adjoint_l1_reference_error"] = float(model.h*np.sum(abs(result["psi"]-continuum.sol(model.x)[0])))
            result["continuous_bvp_max_rms_residual"] = float(max(continuum.rms_residuals))
            result["continuous_adjoint_gradient_amplitude_phase"] = model.continuous_gradient(continuum)
        result["elapsed_seconds"] = time.perf_counter()-started
        result.update({"cells": n, "nu": args.nu, "amplitude": args.amplitude, "phase": args.phase,
                       "reconstruction": args.reconstruction, "epsilon": args.epsilon,
                       "newton_history": solution["history"]})
        if previous:
            result["state_l1_observed_order"] = float(np.log(previous["state_l1_error"]/result["state_l1_error"])/np.log(n/previous["cells"]))
            result["gradient_observed_order"] = float(np.log(previous["gradient_error_inf"]/result["gradient_error_inf"])/np.log(n/previous["cells"]))
            result["amplitude_gradient_observed_order"] = float(np.log(previous["amplitude_gradient_error"]/result["amplitude_gradient_error"])/np.log(n/previous["cells"]))
        sample = np.linspace(0, n-1, min(n, 161), dtype=int)
        result["profile"] = {"x": model.x[sample].tolist(), "u": solution["u"][sample].tolist(),
                             "exact_cell_average": model.exact_average()[sample].tolist(),
                             "adjoint": result.pop("psi")[sample].tolist(),
                             "amplitude_tangent": result.pop("tangent")[sample, 0].tolist()}
        rows.append(result)
        previous = result
        print(f"n={n:6d} state L1={result['state_l1_error']:.6e} gradient error={result['gradient_error_inf']:.6e} time={result['elapsed_seconds']:.3f}s")
    document = {"provenance": provenance(), "results": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, allow_nan=False)+"\n")
    keys = ["cells", "nu", "reconstruction", "state_l1_error", "state_linf_error", "gradient_error_inf",
            "primal_residual_inf", "primal_residual_density_inf", "newton_correction_inf", "adjoint_residual_inf", "elapsed_seconds"]
    with args.output.with_suffix(".csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows({k: row[k] for k in keys} for row in rows)


if __name__ == "__main__":
    main()
