#!/usr/bin/env python3
"""Sparse reproduction of the steady viscous Burgers experiment with the NODE-centred finite-volume scheme.

Unknowns are the point values U_j at the nodes x_j = j h (j = 0..N, h = 1/N); the control volumes are the dual intervals around the nodes; the two end rows are
the Dirichlet constraints.  The flux of every face (between node f and node f+1) is Rusanov with the fixed speed alpha = 2 plus the central viscous flux; the
source is the exact integrated manufactured flux difference.  Vectorised NumPy/SciPy code, sparse LU for the state Jacobian and its transpose (N up to 65536).
"""
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
from scipy.integrate import quad, solve_bvp
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import splu

VERSION = "1.0.0"
MAX_CELLS = 65536          # largest number of intervals N the command line accepts
TWO_PI = 2.0 * np.pi
NEWTON_TOLERANCE = 1e-13   # max-norm of the Newton correction at which the iteration stops
NEWTON_MAX_ITERATIONS = 35
LINE_SEARCH_HALVINGS = 30
RESIDUAL_FLOOR_FACTOR = 16.   # rounding floor of max|R|: 16 eps (1 + nu/h); a trial below it is accepted even if max|R| did not decrease


class NodeBurgers:
    """Node-centred finite volumes for q_x = s, q = u^2/2 - nu u_x, u(0) = u_in, u(1) = u_out; design p = (amplitude, phase, nu)."""

    def __init__(self, n=64, nu=.01, amplitude=.2, phase=.07, reconstruction="none", epsilon=.01):
        if not isinstance(n, (int, np.integer)) or not 8 <= n <= MAX_CELLS:
            raise ValueError(f"the number of intervals must be an integer in [8,{MAX_CELLS}]")
        if not np.isfinite([nu, amplitude, phase, epsilon]).all():
            raise ValueError("all parameters must be finite")
        if not 0 < nu <= 1 or not abs(amplitude) <= .5 or epsilon <= 0:
            raise ValueError("require 0 < nu <= 1, |amplitude| <= .5, epsilon > 0")
        if reconstruction not in ("first", "none", "smooth"):
            raise ValueError("reconstruction must be first, none or smooth")
        n = int(n)
        self.n, self.h, self.nu = n, 1.0 / n, nu
        self.p = np.array([amplitude, phase, nu])
        self.kind, self.epsilon = reconstruction, epsilon
        self.x = np.arange(n + 1) / n                  # nodes (j / n is exactly 1 at j = n)
        self.xm = (np.arange(n) + .5) / n              # face midpoints x_{f+1/2}
        width = np.full(n + 1, self.h)
        width[[0, n]] = self.h / 2                     # dual-volume widths
        self.weights = width * (1 + self.x)            # J_h = weights . U (trapezoid rule for (1 + x) u); also the state gradient g
        f = np.arange(n)
        ones = np.ones(n)
        self.pick_left = csr_matrix((ones, (f, f)), shape=(n, n + 1))        # U_L = U_f
        self.pick_right = csr_matrix((ones, (f, f + 1)), shape=(n, n + 1))   # U_R = U_{f+1}
        j = np.arange(1, n)                            # rows of the flux balance: R_j = H_j - H_{j-1}
        self.balance = csr_matrix((np.r_[np.ones(n - 1), -np.ones(n - 1)], (np.r_[j, j], np.r_[j, j - 1])), shape=(n + 1, n))
        self.constraints = csr_matrix((np.ones(2), ([0, n], [0, n])), shape=(n + 1, n + 1))

    # ---------------------------------------------------------------- exact manufactured solution
    def exact(self, x, p=None):
        a, phase, _ = self.p if p is None else p
        return 1 + a * np.sin(TWO_PI * (np.asarray(x) - phase))

    def exact_nodal(self, p=None):
        return self.exact(self.x, p)

    def physical_flux(self, x, p=None):
        """q* = (u*)^2/2 - nu u*_x at the points x"""
        a, phase, nu = self.p if p is None else p
        z = TWO_PI * (np.asarray(x) - phase)
        u = 1 + a * np.sin(z)
        return .5 * u * u - nu * TWO_PI * a * np.cos(z)

    def exact_objective(self):
        a, phase, _ = self.p
        return float(1.5 - a * np.cos(TWO_PI * phase) / TWO_PI)

    def exact_gradient(self):
        a, phase, _ = self.p
        return np.array([-np.cos(TWO_PI * phase) / TWO_PI, a * np.sin(TWO_PI * phase), 0.])

    # ---------------------------------------------------------------- primal residual
    def slopes(self, u, derivatives=False):
        """Slopes sigma_j at the nodes (interior: first 0, none (l+r)/2, smooth l r (l+r)/(l^2+r^2+eps^2); boundary nodes: 0 for first,
        else the one-sided difference) and, optionally, the partial derivatives (sigma_l, sigma_r) at the interior nodes."""
        n = self.n
        s = np.zeros(n + 1, dtype=u.dtype)
        dl, dr = np.zeros(n - 1), np.zeros(n - 1)
        if self.kind == "first":
            return (s, dl, dr) if derivatives else s
        l, r = u[1:-1] - u[:-2], u[2:] - u[1:-1]
        s[0], s[n] = u[1] - u[0], u[n] - u[n - 1]
        if self.kind == "none":
            s[1:-1] = .5 * (l + r)
            dl[:], dr[:] = .5, .5
        else:
            den, num = l * l + r * r + self.epsilon ** 2, l * r * (l + r)
            s[1:-1] = num / den
            if derivatives:
                dl = ((2 * l * r + r * r) * den - 2 * l * num) / den ** 2
                dr = ((l * l + 2 * l * r) * den - 2 * r * num) / den ** 2
        return (s, dl, dr) if derivatives else s

    def face_states(self, u):
        s = self.slopes(u)
        return u[:-1] + .5 * s[:-1], u[1:] - .5 * s[1:]

    def face_flux(self, u, nu):
        qL, qR = self.face_states(u)
        return .25 * (qL * qL + qR * qR) - (qR - qL) - nu * (u[1:] - u[:-1]) / self.h

    def residual(self, u, p=None):
        """R(U, p) in R^(N+1): rows 1..N-1 the dual-volume flux balance minus the exact integrated source, rows 0 and N the constraints."""
        p = self.p if p is None else p
        n = self.n
        u = np.asarray(u)
        flux = self.face_flux(u, p[2])
        q = self.physical_flux(self.xm, p)
        r = np.zeros(n + 1, dtype=np.result_type(flux.dtype, q.dtype))
        r[1:n] = (flux[1:] - flux[:-1]) - (q[1:] - q[:-1])
        r[0] = u[0] - self.exact(0.0, p)
        r[n] = u[n] - self.exact(1.0, p)
        return r

    # ---------------------------------------------------------------- Jacobians
    def slope_matrix(self, dl, dr):
        """d sigma / d U as a sparse (N+1) x (N+1) matrix"""
        n = self.n
        if self.kind == "first":
            return csr_matrix((n + 1, n + 1))
        j = np.arange(1, n)
        rows = np.r_[j, j, j, 0, 0, n, n]
        cols = np.r_[j - 1, j, j + 1, 0, 1, n - 1, n]
        vals = np.r_[-dl, dl - dr, dr, -1., 1., -1., 1.]
        return csr_matrix((vals, (rows, cols)), shape=(n + 1, n + 1))

    def jacobian(self, u, p=None):
        """A = dR/dU (sparse, at most five bands; the rows 0 and N are identity rows)"""
        p = self.p if p is None else p
        s, dl, dr = self.slopes(u, derivatives=True)
        qL, qR = u[:-1] + .5 * s[:-1], u[1:] - .5 * s[1:]
        S = self.slope_matrix(dl, dr)
        flux = diags(.5 * qL + 1) @ (self.pick_left + .5 * S[:-1]) + diags(.5 * qR - 1) @ (self.pick_right - .5 * S[1:]) \
            + (p[2] / self.h) * (self.pick_left - self.pick_right)
        return (self.balance @ flux + self.constraints).tocsc()

    def parameter_jacobian(self, u):
        """R_D = dR/dp (N+1 rows, columns amplitude, phase, nu) from the closed-form derivatives of the source and the constraint data."""
        a, phase, nu = self.p
        n, h = self.n, self.h
        z = TWO_PI * (self.xm - phase)
        sn, cs = np.sin(z), np.cos(z)
        flux_a = (1 + a * sn) * sn - TWO_PI * nu * cs                                # dQ/da
        flux_phase = -TWO_PI * a * (1 + a * sn) * cs - TWO_PI ** 2 * nu * a * sn     # dQ/dphase
        flux_nu = -TWO_PI * a * cs                                                   # dQ/dnu
        explicit_nu = -(u[1:] - u[:-1]) / h                                          # dH/dnu
        rp = np.zeros((n + 1, 3))
        rp[1:n, 0] = -(flux_a[1:] - flux_a[:-1])
        rp[1:n, 1] = -(flux_phase[1:] - flux_phase[:-1])
        rp[1:n, 2] = (explicit_nu[1:] - explicit_nu[:-1]) - (flux_nu[1:] - flux_nu[:-1])
        zin, zout = TWO_PI * (0. - phase), TWO_PI * (1. - phase)
        rp[0, 0], rp[0, 1] = -np.sin(zin), TWO_PI * a * np.cos(zin)                  # -d u_in / dp
        rp[n, 0], rp[n, 1] = -np.sin(zout), TWO_PI * a * np.cos(zout)                # -d u_out / dp
        return rp

    def parameter_jacobian_complex_step(self, u, step=1e-30):
        """The same R_D by holomorphic complex step of the primal residual (state held fixed)"""
        cols = []
        for k in range(3):
            p = self.p.astype(complex)
            p[k] += 1j * step
            cols.append(self.residual(u, p).imag / step)
        return np.column_stack(cols)

    # ---------------------------------------------------------------- tangent and reverse statements (vectorised, matrix-free)
    def residual_d(self, u, ud, pd):
        """Tangent of the residual for the state seed ud and the design seed pd = (a-dot, phase-dot, nu-dot), statement by statement."""
        a, phase, nu = self.p
        n, h = self.n, self.h
        s, dl, dr = self.slopes(u, derivatives=True)
        sd = np.zeros(n + 1)
        if self.kind != "first":
            sd[1:-1] = dl * (ud[1:-1] - ud[:-2]) + dr * (ud[2:] - ud[1:-1])
            sd[0], sd[n] = ud[1] - ud[0], ud[n] - ud[n - 1]
        qL, qR = u[:-1] + .5 * s[:-1], u[1:] - .5 * s[1:]
        qLd, qRd = ud[:-1] + .5 * sd[:-1], ud[1:] - .5 * sd[1:]
        hd = (.5 * qL + 1) * qLd + (.5 * qR - 1) * qRd + (nu / h) * (ud[:-1] - ud[1:]) - pd[2] * (u[1:] - u[:-1]) / h
        z = TWO_PI * (self.xm - phase)
        sn, cs = np.sin(z), np.cos(z)
        qd = ((1 + a * sn) * sn - TWO_PI * nu * cs) * pd[0] + (-TWO_PI * a * (1 + a * sn) * cs - TWO_PI ** 2 * nu * a * sn) * pd[1] \
            + (-TWO_PI * a * cs) * pd[2]
        rd = np.zeros(n + 1)
        rd[1:n] = (hd[1:] - hd[:-1]) - (qd[1:] - qd[:-1])
        zin, zout = TWO_PI * (0. - phase), TWO_PI * (1. - phase)
        rd[0] = ud[0] - (np.sin(zin) * pd[0] - TWO_PI * a * np.cos(zin) * pd[1])
        rd[n] = ud[n] - (np.sin(zout) * pd[0] - TWO_PI * a * np.cos(zout) * pd[1])
        return rd

    def residual_b(self, u, rb):
        """Reverse sweep for the seed R-bar = rb: returns (U-bar, p-bar) = (A^T rb, R_D^T rb); statements in reverse order of the primal."""
        a, phase, nu = self.p
        n, h = self.n, self.h
        ub, pb = np.zeros(n + 1), np.zeros(3)
        ub[n] += rb[n]; uout_b = -rb[n]                                  # constraint rows
        ub[0] += rb[0]; uin_b = -rb[0]
        qb = np.zeros(n)                                                 # source: R_j -= Q_j - Q_{j-1}
        qb[1:n] -= rb[1:n]
        qb[0:n - 1] += rb[1:n]
        z = TWO_PI * (self.xm - phase)
        sn, cs = np.sin(z), np.cos(z)
        pb[0] += np.sum(((1 + a * sn) * sn - TWO_PI * nu * cs) * qb)
        pb[1] += np.sum((-TWO_PI * a * (1 + a * sn) * cs - TWO_PI ** 2 * nu * a * sn) * qb)
        pb[2] += np.sum((-TWO_PI * a * cs) * qb)
        s, dl, dr = self.slopes(u, derivatives=True)                     # forward values needed by the sweep
        qL, qR = u[:-1] + .5 * s[:-1], u[1:] - .5 * s[1:]
        hb = np.zeros(n)                                                 # scatter reversed: H-bar_f = [f >= 1] R-bar_f - [f <= N-2] R-bar_{f+1}
        hb[1:] += rb[1:n]
        hb[:n - 1] -= rb[1:n]
        qLb, qRb = (.5 * qL + 1) * hb, (.5 * qR - 1) * hb
        uLb, uRb = (nu / h) * hb, -(nu / h) * hb
        pb[2] += np.sum(-(u[1:] - u[:-1]) / h * hb)
        sb = np.zeros(n + 1)
        ub[:-1] += qLb + uLb
        sb[:-1] += .5 * qLb
        ub[1:] += qRb + uRb
        sb[1:] += -.5 * qRb
        if self.kind != "first":                                         # slopes reversed
            mb, pbar = dl * sb[1:-1], dr * sb[1:-1]
            ub[1:-1] += mb - pbar
            ub[:-2] -= mb
            ub[2:] += pbar
            ub[1] += sb[0]; ub[0] -= sb[0]
            ub[n] += sb[n]; ub[n - 1] -= sb[n]
        zin, zout = TWO_PI * (0. - phase), TWO_PI * (1. - phase)         # constraint data reversed
        pb[0] += np.sin(zin) * uin_b + np.sin(zout) * uout_b
        pb[1] += -TWO_PI * a * (np.cos(zin) * uin_b + np.cos(zout) * uout_b)
        return ub, pb

    # ---------------------------------------------------------------- primal solve
    def solve(self, start=None, maxiter=NEWTON_MAX_ITERATIONS, tol=NEWTON_TOLERANCE):
        """Newton with backtracking on max|R| (positive box .1 < U < 1.9); stops when the max-norm of the correction is <= tol (that last correction is applied).
        A trial is accepted if it is inside the box and max|R(trial)| < (1 - 1e-4 step) max|R|, or max|R(trial)| is below the rounding floor of the residual
        (the ulp of U times nu/h, about 3e-13 at N = 65536: below it the merit function cannot see a real correction of 4e-11).
        The start is the exact nodal values (an initial guess only) unless `start` is given."""
        u = self.exact_nodal() if start is None else np.array(start, dtype=float)
        floor = RESIDUAL_FLOOR_FACTOR * np.finfo(float).eps * (1 + self.nu / self.h)
        history = []
        for k in range(maxiter):
            r = self.residual(u)
            factor = splu(self.jacobian(u))
            d = factor.solve(-r)
            rn, dn = float(np.max(abs(r))), float(np.max(abs(d)))
            step = 1.
            if dn > tol:
                for _ in range(LINE_SEARCH_HALVINGS + 1):
                    trial = u + step * d
                    if trial.min() > .1 and trial.max() < 1.9 and np.max(abs(self.residual(trial))) < max((1 - 1e-4 * step) * rn, floor):
                        break
                    step *= .5
                else:
                    raise RuntimeError(f"Newton line search failed at n={self.n}; residual={rn:g}, correction={dn:g}")
            u = u + step * d
            history.append({"iteration": k, "residual_inf": rn, "correction_inf": dn, "step": step})
            if dn <= tol:
                return {"u": u, "history": history}
        raise RuntimeError(f"Newton iteration limit at n={self.n}")

    # ---------------------------------------------------------------- tangent, adjoint, gradients
    def analyse(self, solution):
        u = solution["u"]
        A = self.jacobian(u)
        factor = splu(A)
        rp = self.parameter_jacobian(u)
        tangent = factor.solve(-rp)                                   # three tangent solves A v_k = -R_D e_k
        psi = factor.solve(-self.weights, trans="T")                  # adjoint solve A^T psi = -g, g = weights
        g, gt = psi @ rp, self.weights @ tangent
        ub, pb = self.residual_b(u, psi)                              # reverse sweep with the seed psi: U-bar = A^T psi = -g, p-bar = gradient
        v, w = np.sin(7 * self.x), np.cos(3 * self.x)
        transpose_error = abs(w @ (A @ v) - v @ (A.T @ w)) / max(1., abs(w @ (A @ v)), abs(v @ (A.T @ w)))
        exact_gradient = self.exact_gradient()
        exact_u = self.exact_nodal()
        e = u - exact_u
        h, n = self.h, self.n
        r_exact = self.residual(exact_u)
        r = self.residual(u)
        a, phase, _ = self.p
        objective_exact_nodal = float(self.weights @ exact_u)
        em = h ** 2 / 12 * TWO_PI * a * np.cos(TWO_PI * phase)        # (h^2/12) u*_x(0)
        return {"objective": float(self.weights @ u),
                "exact_objective": self.exact_objective(),
                "gradient": g.tolist(), "tangent_gradient": gt.tolist(), "reverse_gradient": pb.tolist(),
                "exact_gradient": exact_gradient.tolist(),
                "gradient_error_inf": float(np.max(abs(g - exact_gradient))),
                "amplitude_gradient_error": float(abs(g[0] - exact_gradient[0])),
                "phase_gradient_error": float(abs(g[1] - exact_gradient[1])),
                "viscosity_gradient_error": float(abs(g[2])),
                "gradient_duality_error": float(np.max(abs(g - gt))),
                "gradient_reverse_error": float(np.max(abs(g - pb))),
                "reverse_state_adjoint_error": float(np.max(abs(ub + self.weights))),
                "transpose_relative_error": float(transpose_error),
                "state_l1_error": float(h * np.sum(abs(e))),
                "state_linf_error": float(np.max(abs(e))),
                "primal_residual_inf": float(np.max(abs(r))),
                "primal_residual_density_inf": float(np.max(abs(r[1:n])) / h),
                "newton_correction_inf": solution["history"][-1]["correction_inf"],
                "tangent_residual_inf": float(np.max(abs(A @ tangent + rp))),
                "adjoint_residual_inf": float(np.max(abs(A.T @ psi + self.weights))),
                "jacobian_nonzeros": int(A.nnz),
                "psi_0": float(psi[0]), "psi_N": float(psi[n]),
                "exact_nodal_residual_inf": float(np.max(abs(r_exact[1:n]))),
                "exact_nodal_residual_boundary_rows_inf": float(max(abs(r_exact[1]), abs(r_exact[n - 1]))),
                "exact_nodal_residual_inner_rows_inf": float(np.max(abs(r_exact[2:n - 1]))),
                "exact_nodal_residual_constraint_rows_inf": float(max(abs(r_exact[0]), abs(r_exact[n]))),
                "exact_nodal_objective": objective_exact_nodal,
                "objective_quadrature_error": float(objective_exact_nodal - self.exact_objective()),
                "objective_quadrature_remainder": float(objective_exact_nodal - self.exact_objective() - em),
                "psi": psi, "tangent": tangent}

    def gradient_check(self, solution, analysis, step=1e-5):
        """Central differences of J_h with two complete perturbed re-solves each: along the direction (1, .3, 0) and along every design axis."""
        def perturbed(direction):
            objectives, residuals = [], []
            for sign in (-1, 1):
                p = self.p + sign * step * np.asarray(direction, dtype=float)
                other = NodeBurgers(self.n, p[2], p[0], p[1], self.kind, self.epsilon)
                ss = other.solve(solution["u"])
                objectives.append(float(other.weights @ ss["u"]))
                residuals.append(float(np.max(abs(other.residual(ss["u"])))))
            return (objectives[1] - objectives[0]) / (2 * step), residuals
        direction = np.array([1., .3, 0.])
        fd, residuals = perturbed(direction)
        predicted = float(np.dot(analysis["gradient"], direction))
        axes = [perturbed(np.eye(3)[k])[0] for k in range(3)]
        return {"step": step, "direction_amplitude_phase_nu": direction.tolist(),
                "full_rerun_central_difference": fd, "adjoint_directional_gradient": predicted,
                "absolute_error": abs(fd - predicted), "perturbed_primal_residuals_inf": residuals,
                "axis_central_differences": axes, "axis_absolute_errors": [float(abs(axes[k] - analysis["gradient"][k])) for k in range(3)]}

    # ---------------------------------------------------------------- continuous adjoint (independent scipy BVP solution)
    def continuous_adjoint(self):
        """-u lambda_x - nu lambda_xx = -(1 + x), lambda(0) = lambda(1) = 0, solved with scipy's collocation BVP solver"""
        def fun(x, y):
            return np.vstack((y[1], ((1 + x) - self.exact(x) * y[1]) / self.nu))

        def boundary(ya, yb):
            return np.array([ya[0], yb[0]])
        mesh = np.linspace(0, 1, 201)
        sol = solve_bvp(fun, boundary, mesh, np.zeros((2, len(mesh))), tol=1e-9, max_nodes=50000)
        if not sol.success:
            raise RuntimeError("continuous adjoint BVP failed: " + sol.message)
        return sol

    def continuous_gradient(self, sol):
        """dJ/dp = -int lambda s_p dx + nu [lambda_x g_p]_0^1 for the amplitude and the phase (g_p = d u_in / dp = d u_out / dp)"""
        a, phase, nu = self.p
        k = TWO_PI

        def boundary_data_derivative(index):
            z = k * (0. - phase)
            return np.sin(z) if index == 0 else -k * a * np.cos(z)

        def source_derivative(x, index):
            z = k * (x - phase)
            u, ux = 1 + a * np.sin(z), k * a * np.cos(z)
            if index == 0:
                v, vx, vxx = np.sin(z), k * np.cos(z), -k * k * np.sin(z)
            else:
                v, vx, vxx = -k * a * np.cos(z), k * k * a * np.sin(z), k ** 3 * a * np.cos(z)
            return ux * v + u * vx - nu * vxx
        return [float(-quad(lambda x: sol.sol(x)[0] * source_derivative(x, j), 0, 1, epsabs=1e-11, limit=200)[0]
                      + nu * (sol.sol(1)[1] - sol.sol(0)[1]) * boundary_data_derivative(j)) for j in (0, 1)]


def provenance():
    return {"version": VERSION, "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "command": " ".join(["python3", Path(sys.argv[0]).name] + sys.argv[1:]), "python": platform.python_version(),
            "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform(),
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "formulation": "node-centred finite volumes: point values at the nodes, dual volumes, one-sided boundary slopes, constraint rows, "
                           "alpha=2, analytic source and Dirichlet data, trapezoid objective",
            "mathematical_proof": False, "max_cells": MAX_CELLS}


def observed_order(previous, current, key, n_previous, n):
    if previous is None or previous[key] <= 0 or current[key] <= 0:
        return None
    return float(np.log(previous[key] / current[key]) / np.log(n / n_previous))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cells", type=int, default=128, help="number of intervals N (the unknowns are the N+1 nodal values)")
    parser.add_argument("--grids", help="comma-separated numbers of intervals for a fixed-nu mesh study")
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
        try:
            model = NodeBurgers(n, args.nu, args.amplitude, args.phase, args.reconstruction, args.epsilon)
        except ValueError as error:
            parser.error(str(error))
        started = time.perf_counter()
        solution = model.solve()
        result = model.analyse(solution)
        if args.gradient_check:
            result["gradient_check"] = model.gradient_check(solution, result)
        lam_nodes = None
        if args.continuous_adjoint:
            if continuum is None:
                continuum = model.continuous_adjoint()
            lam_nodes = continuum.sol(model.x)
            # psi_j (not psi_j / h) is compared with lambda(x_j): the multipliers of the flux-balance rows are O(1), see README
            result["adjoint_l1_reference_error"] = float(model.h * np.sum(abs(result["psi"][1:n] - lam_nodes[0][1:n])))
            result["adjoint_linf_reference_error"] = float(np.max(abs(result["psi"][1:n] - lam_nodes[0][1:n])))
            result["continuous_bvp_max_rms_residual"] = float(max(continuum.rms_residuals))
            result["continuous_adjoint_gradient_amplitude_phase"] = model.continuous_gradient(continuum)
            lam_x0, lam_x1 = float(continuum.sol(0.)[1]), float(continuum.sol(1.)[1])
            result["nu_lambda_x_0"], result["minus_nu_lambda_x_1"] = args.nu * lam_x0, -args.nu * lam_x1
            result["psi_0_boundary_flux_error"] = float(abs(result["psi_0"] - args.nu * lam_x0))
            result["psi_N_boundary_flux_error"] = float(abs(result["psi_N"] + args.nu * lam_x1))
        result["elapsed_seconds"] = time.perf_counter() - started
        result.update({"cells": n, "nu": args.nu, "amplitude": args.amplitude, "phase": args.phase,
                       "reconstruction": args.reconstruction, "epsilon": args.epsilon,
                       "newton_history": solution["history"]})
        if previous:
            n0 = previous["cells"]
            for name, key in (("state_l1_observed_order", "state_l1_error"), ("state_linf_observed_order", "state_linf_error"),
                              ("gradient_observed_order", "gradient_error_inf"), ("amplitude_gradient_observed_order", "amplitude_gradient_error"),
                              ("phase_gradient_observed_order", "phase_gradient_error"), ("viscosity_gradient_observed_order", "viscosity_gradient_error"),
                              ("adjoint_l1_observed_order", "adjoint_l1_reference_error"), ("psi_0_observed_order", "psi_0_boundary_flux_error"),
                              ("psi_N_observed_order", "psi_N_boundary_flux_error")):
                if key in previous and key in result:
                    result[name] = observed_order(previous, result, key, n0, n)
        sample = np.linspace(0, n, min(n + 1, 161), dtype=int)
        profile = {"x": model.x[sample].tolist(), "u": solution["u"][sample].tolist(),
                   "exact_nodal_value": model.exact_nodal()[sample].tolist(),
                   "adjoint": result.pop("psi")[sample].tolist(),
                   "amplitude_tangent": result.pop("tangent")[sample, 0].tolist()}
        if lam_nodes is not None:
            profile["continuous_adjoint"] = lam_nodes[0][sample].tolist()
        result["profile"] = profile
        rows.append(result)
        previous = result
        print(f"n={n:6d} state L1={result['state_l1_error']:.6e} gradient error={result['gradient_error_inf']:.6e} time={result['elapsed_seconds']:.3f}s")
    document = {"provenance": provenance(), "results": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, allow_nan=False) + "\n")
    keys = ["cells", "nu", "reconstruction", "state_l1_error", "state_linf_error", "gradient_error_inf",
            "primal_residual_inf", "primal_residual_density_inf", "newton_correction_inf", "adjoint_residual_inf", "elapsed_seconds",
            "psi_0", "psi_N", "exact_nodal_residual_boundary_rows_inf", "exact_nodal_residual_inner_rows_inf"]
    with args.output.with_suffix(".csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows({k: row[k] for k in keys} for row in rows)


if __name__ == "__main__":
    main()
