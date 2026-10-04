"""Regression tests of the node-centred solver: identities of the discrete model, gradients against finite differences and complex step,
orders of convergence, the continuous adjoint and the boundary multipliers.  No PDE proof is claimed.

    python3 -m pytest -q test_solver_node.py          (pytest style: plain functions and asserts)
    python3 test_solver_node.py                       (the same tests without pytest)
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np

import solve_node
from solve_node import NodeBurgers, provenance

HERE = Path(__file__).resolve().parent
KINDS = ("first", "none", "smooth")
TWO_PI = 2 * np.pi


def random_state(m, rng):
    return 1 + .12 * rng.normal(size=m.n + 1) + .1 * np.sin(rng.uniform(1, 9) * m.x)


def random_model(n, kind, rng):
    return NodeBurgers(n, rng.uniform(.002, .2), rng.uniform(-.4, .4), rng.uniform(0, 1), kind, .01)


def solve_and_analyse(n, kind, **kwargs):
    m = NodeBurgers(n, reconstruction=kind, **kwargs)
    s = m.solve()
    return m, s, m.analyse(s)


def order(a, b, n_a, n_b):
    return float(np.log(a / b) / np.log(n_b / n_a))


# ------------------------------------------------------------------------------------------------ identities of the discrete model
def test_jacobians_match_complex_step():
    rng = np.random.default_rng(20261004)
    for kind in KINDS:
        for n in (8, 24):
            m = random_model(n, kind, rng)
            u = random_state(m, rng)
            A = m.jacobian(u)
            v, pd = rng.normal(size=n + 1), rng.normal(size=3)
            cs = m.residual(u.astype(complex) + 1j * 1e-30 * v).imag / 1e-30
            np.testing.assert_allclose(A @ v, cs, atol=2e-14, rtol=2e-13)
            np.testing.assert_allclose(m.parameter_jacobian(u), m.parameter_jacobian_complex_step(u), atol=2e-13, rtol=2e-13)
            np.testing.assert_allclose(m.residual_d(u, v, pd), A @ v + m.parameter_jacobian(u) @ pd, atol=2e-13, rtol=2e-13)
            dense = A.toarray()
            assert dense[0, 0] == 1 and dense[n, n] == 1 and np.count_nonzero(dense[0]) == 1 and np.count_nonzero(dense[n]) == 1   # constraint rows
            for j in range(1, n):                                                       # bands: five (three for first order)
                half = 1 if kind == "first" else 2
                outside = [k for k in range(n + 1) if not j - half <= k <= j + half]
                assert not dense[j, outside].any()


def test_reverse_statements_and_dot_test():
    rng = np.random.default_rng(910)
    for kind in KINDS:
        for n in (8, 24):
            m = random_model(n, kind, rng)
            u = random_state(m, rng)
            A, rp = m.jacobian(u), m.parameter_jacobian(u)
            rb, ud, pd = rng.normal(size=n + 1), rng.normal(size=n + 1), rng.normal(size=3)
            ub, pb = m.residual_b(u, rb)
            np.testing.assert_allclose(ub, A.T @ rb, atol=2e-13, rtol=2e-13)
            np.testing.assert_allclose(pb, rp.T @ rb, atol=2e-13, rtol=2e-13)
            lhs, rhs = rb @ m.residual_d(u, ud, pd), ub @ ud + pb @ pd
            assert abs(lhs - rhs) <= 1e-13 * max(1., abs(lhs))                          # R-bar^T R-dot = U-bar^T U-dot + p-bar^T p-dot


def test_first_order_interior_row_in_closed_form():
    rng = np.random.default_rng(3)
    m = random_model(20, "first", rng)
    u = random_state(m, rng)
    r, q = m.residual(u), m.physical_flux(m.xm)
    nu, h = m.nu, m.h
    for j in range(1, m.n):
        closed = (u[j + 1] ** 2 - u[j - 1] ** 2) / 4 - (1 + nu / h) * (u[j + 1] - 2 * u[j] + u[j - 1]) - (q[j] - q[j - 1])
        assert abs(r[j] - closed) < 1e-13


def test_constant_exact_solution_and_weights():
    m = NodeBurgers(32, amplitude=0.)
    s = m.solve()
    np.testing.assert_allclose(s["u"], 1., atol=1e-14)
    assert abs(m.weights.sum() - 1.5) < 1e-14                                            # the trapezoid rule is exact for (1 + x)
    assert m.weights[0] == m.h / 2 and abs(m.weights[-1] - m.h) < 1e-16


# ------------------------------------------------------------------------------------------------ Newton
def test_newton_line_search_from_a_poor_start():
    """from the exact nodal values Newton takes full steps; from a start with a large error the backtracking is used and the same solution is reached"""
    for kind in ("none", "smooth"):
        m = NodeBurgers(64, reconstruction=kind)
        reference = m.solve()
        assert all(h["step"] == 1. for h in reference["history"]) and reference["history"][-1]["correction_inf"] <= 1e-13
        poor = m.solve(start=m.exact_nodal() + .7 * np.sin(TWO_PI * m.x))
        steps = [h["step"] for h in poor["history"]]
        assert min(steps) < 1., steps                                                    # the line search was active
        residuals = [h["residual_inf"] for h in poor["history"]]
        assert all(residuals[k + 1] < residuals[k] for k in range(len(steps) - 1) if steps[k] < 1.)     # an accepted backtracked step decreases max|R|
        np.testing.assert_allclose(poor["u"], reference["u"], atol=1e-12)
    try:
        NodeBurgers(64).solve(start=np.full(65, 1.8), maxiter=1)
    except RuntimeError:
        return
    raise AssertionError("the iteration limit must raise")


def test_newton_converges_at_the_rounding_floor_of_the_residual():
    """N = 65536: after the first step of a perturbed re-solve max|R| (about 3e-13) is at its rounding floor while a real correction (4e-11) remains;
    the acceptance rule must still take that step (the finite-difference gradient check of the largest run needs it)"""
    n = 65536
    base = NodeBurgers(n).solve()
    other = NodeBurgers(n, .01, .2 + 1e-5, .07 + 3e-6, "none", .01)
    s = other.solve(base["u"])
    assert len(s["history"]) <= 5 and s["history"][-1]["correction_inf"] <= 1e-13
    assert max(h["correction_inf"] for h in s["history"][1:]) < 1e-10 and np.max(abs(other.residual(s["u"]))) < 1e-11


# ------------------------------------------------------------------------------------------------ the exact nodal values
def test_residual_of_the_exact_nodal_values():
    """rows 0 and N vanish; none: rows next to the boundary O(h^2), inner rows O(h^3); first: O(h^2) everywhere (integrated rows);
    smooth (eps fixed): inner rows O(h^2), boundary rows only O(h) (measured, see README)"""
    norms = {}
    for kind in KINDS:
        norms[kind] = {}
        for n in (256, 512, 1024):
            m = NodeBurgers(n, reconstruction=kind)
            r = m.residual(m.exact_nodal())
            assert max(abs(r[0]), abs(r[n])) < 1e-15
            norms[kind][n] = (max(abs(r[1]), abs(r[n - 1])), np.max(abs(r[2:n - 1])))
    for kind, (lo, hi) in {"none": ((1.8, 2.2), (2.8, 3.2)), "first": ((1.9, 2.2), (1.9, 2.1)), "smooth": ((.5, 1.2), (1.9, 2.1))}.items():
        for n in (256, 512):
            ob = order(norms[kind][n][0], norms[kind][2 * n][0], n, 2 * n)
            oi = order(norms[kind][n][1], norms[kind][2 * n][1], n, 2 * n)
            assert lo[0] < ob < lo[1], (kind, n, "boundary rows", ob)
            assert hi[0] < oi < hi[1], (kind, n, "inner rows", oi)


def test_objective_of_the_exact_nodal_values_euler_maclaurin():
    """J_h(u*) - J* = (h^2/12) u*_x(0) - (h^4/720) u*_xxx(0) + O(h^6)"""
    a, phase = .2, .07
    jstar = 1.5 - a * np.cos(TWO_PI * phase) / TWO_PI
    for n, tolerance in ((16, 1e-2), (64, 1e-3)):                                        # relative to the h^4 term; the next term is O(h^2) smaller
        m = NodeBurgers(n)
        err = m.weights @ m.exact_nodal() - jstar
        em2 = m.h ** 2 / 12 * TWO_PI * a * np.cos(TWO_PI * phase)
        em4 = -(m.h ** 4 / 720) * (-a * TWO_PI ** 3 * np.cos(TWO_PI * phase))
        assert abs(err - em2 - em4) < tolerance * abs(em4), (n, err - em2, em4)
    m = NodeBurgers(64)
    assert abs(m.exact_objective() - jstar) < 1e-15
    np.testing.assert_allclose(m.exact_gradient(), [-np.cos(TWO_PI * phase) / TWO_PI, a * np.sin(TWO_PI * phase), 0.], atol=1e-16)


# ------------------------------------------------------------------------------------------------ gradients
def test_tangent_adjoint_reverse_fd_and_complex_step():
    for kind in KINDS:
        for n in (16, 32):
            m, s, an = solve_and_analyse(n, kind)
            assert an["gradient_duality_error"] < 2e-12                                  # tangent = adjoint
            assert an["gradient_reverse_error"] < 2e-12                                  # reverse code with the seed psi = adjoint
            assert an["reverse_state_adjoint_error"] < 2e-12                             # U-bar = A^T psi = -g
            assert an["adjoint_residual_inf"] < 1e-12 and an["tangent_residual_inf"] < 1e-12
            gc = m.gradient_check(s, an)
            assert gc["absolute_error"] < 2e-8, (kind, n, gc["absolute_error"])          # direction (1, .3, 0)
            assert max(gc["axis_absolute_errors"]) < 2e-8, (kind, n, gc["axis_absolute_errors"])   # every design axis, nu included
            # complex step of the residual through the solve: Im R(U + i t v, p + i t e_k) = 0 with v from the tangent solve
            for k in range(3):
                t = 1e-30
                pc = m.p.astype(complex)
                pc[k] += 1j * t
                v = an["tangent"][:, k]                                                  # from the sparse tangent solve A v_k = -R_D e_k
                r = m.residual(s["u"].astype(complex) + 1j * t * v, pc)
                assert np.max(abs(r.imag)) / t < 1e-9                                    # the complex-step residual of the perturbed state vanishes
                assert abs(m.weights @ v - an["gradient"][k]) < 1e-10


def test_gradient_equals_the_exact_gradient_up_to_discretisation_error():
    m, s, an = solve_and_analyse(512, "none")
    assert an["amplitude_gradient_error"] < 1e-5 and an["phase_gradient_error"] < 2e-4 and an["viscosity_gradient_error"] < 5e-3
    assert abs(an["objective"] - an["exact_objective"]) < 1e-5


# ------------------------------------------------------------------------------------------------ refinement
def test_orders_of_convergence():
    rows = {}
    for kind in KINDS:
        rows[kind] = {n: solve_and_analyse(n, kind)[2] for n in (64, 128, 256, 512, 4096)}
    none, first, smooth = rows["none"], rows["first"], rows["smooth"]
    assert 1.9 < order(none[128]["state_l1_error"], none[256]["state_l1_error"], 128, 256) < 2.3       # second order
    assert 1.7 < order(none[256]["state_linf_error"], none[512]["state_linf_error"], 256, 512) < 2.5
    assert 0.95 < order(first[256]["state_l1_error"], first[512]["state_l1_error"], 256, 512) < 1.05  # first order
    assert 0.95 < order(first[256]["gradient_error_inf"], first[512]["gradient_error_inf"], 256, 512) < 1.05
    # smooth with epsilon fixed: stagnates on moderate meshes and is first order, practically the first-order scheme, on fine ones
    assert smooth[256]["state_l1_error"] > 100 * none[256]["state_l1_error"]
    assert abs(smooth[4096]["state_l1_error"] / first[4096]["state_l1_error"] - 1) < .05
    assert 1.9 < order(none[512]["state_l1_error"], none[4096]["state_l1_error"], 512, 4096) < 2.1


def test_large_grid_smoke():
    m, s, an = solve_and_analyse(4096, "none")
    assert len(s["history"]) <= 4 and s["history"][-1]["correction_inf"] <= 1e-13
    assert an["gradient_duality_error"] < 1e-10 and an["state_l1_error"] < 1e-7 and an["primal_residual_inf"] < 1e-12


# ------------------------------------------------------------------------------------------------ continuous adjoint and boundary multipliers
def test_continuous_adjoint_gradient_formula_and_boundary_flux():
    m = NodeBurgers(512)
    sol = m.continuous_adjoint()
    lam_x0, lam_x1 = float(sol.sol(0.)[1]), float(sol.sol(1.)[1])
    assert abs(lam_x0 + 142.65679653909865) < 1e-6 and abs(lam_x1 - 2.203455145731823) < 1e-8       # layer at x = 0 (SPEC section 1)
    np.testing.assert_allclose(m.continuous_gradient(sol), m.exact_gradient()[:2], atol=2e-9, rtol=0)  # boundary term included
    # multipliers of the constraint rows are the boundary fluxes of the continuous adjoint; the other multipliers are lambda(x_j), not h lambda(x_j)
    errors = {}
    for n in (512, 1024):
        mm, s, an = solve_and_analyse(n, "none")
        psi, lam = an["psi"], sol.sol(mm.x)[0]
        errors[n] = (abs(an["psi_0"] - m.nu * lam_x0), abs(an["psi_N"] + m.nu * lam_x1), mm.h * np.sum(abs(psi[1:n] - lam[1:n])))
        assert abs(psi[n // 2] / lam[n // 2] - 1) < .01
        assert abs(an["psi_0"] / (m.nu * lam_x0) - 1) < 1e-3
    for k in range(3):
        assert 1.8 < order(errors[512][k], errors[1024][k], 512, 1024) < 2.2


# ------------------------------------------------------------------------------------------------ the command line and the data files
def test_limits_and_arguments():
    for kwargs in ({"nu": 0.}, {"nu": 1.5}, {"n": 65537}, {"n": 7}, {"amplitude": 3.}, {"epsilon": 0.}, {"nu": float("nan")}, {"reconstruction": "central"}):
        try:
            NodeBurgers(**kwargs)
        except ValueError:
            continue
        raise AssertionError(f"{kwargs} must be rejected")


def test_provenance_hash_and_command():
    p = provenance()
    assert p["implementation_sha256"] == hashlib.sha256((HERE / "solve_node.py").read_bytes()).hexdigest()
    assert p["mathematical_proof"] is False and p["version"]
    for key in ("command", "python", "numpy", "scipy", "platform", "generated_utc"):
        assert isinstance(p[key], str) and p[key]


def test_command_line_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "run.json"
        subprocess.run([sys.executable, str(HERE / "solve_node.py"), "--grids", "16,32,64", "--nu", "0.01", "--amplitude", "0.2", "--phase", "0.07",
                        "--reconstruction", "none", "--gradient-check", "--continuous-adjoint", "--output", str(out)], check=True, capture_output=True, cwd=tmp)
        doc = json.loads(out.read_text())
        assert doc["provenance"]["command"].startswith("python3 solve_node.py --grids 16,32,64")
        assert [r["cells"] for r in doc["results"]] == [16, 32, 64]
        r = doc["results"][-1]
        for key in ("objective", "exact_objective", "gradient", "tangent_gradient", "exact_gradient", "gradient_error_inf", "amplitude_gradient_error",
                    "phase_gradient_error", "viscosity_gradient_error", "gradient_duality_error", "state_l1_error", "state_linf_error", "primal_residual_inf",
                    "newton_correction_inf", "elapsed_seconds", "adjoint_l1_reference_error", "newton_history", "profile", "psi_0", "psi_N",
                    "nu_lambda_x_0", "minus_nu_lambda_x_1", "exact_nodal_residual_inner_rows_inf", "exact_nodal_residual_boundary_rows_inf",
                    "gradient_check", "state_l1_observed_order", "reconstruction", "epsilon", "nu", "amplitude", "phase"):
            assert key in r, key
        assert r["nu"] == .01 and r["amplitude"] == .2 and r["phase"] == .07 and r["reconstruction"] == "none"
        assert len(r["profile"]["x"]) == 65 and abs(r["profile"]["x"][-1] - 1.) == 0.
        assert r["gradient_check"]["absolute_error"] < 2e-8 and r["gradient_duality_error"] < 1e-11
        assert abs(r["nu_lambda_x_0"] + 1.4265679653909865) < 1e-9
        csv_lines = out.with_suffix(".csv").read_text().strip().splitlines()
        assert len(csv_lines) == 4 and csv_lines[0].split(",")[:3] == ["cells", "nu", "reconstruction"]


def test_published_examples_are_current():
    """every examples/*.json must carry the SHA-256 of this solver (regenerate the data after editing solve_node.py)"""
    digest = hashlib.sha256((HERE / "solve_node.py").read_bytes()).hexdigest()
    for f in sorted((HERE / "examples").glob("*.json")):
        d = json.loads(f.read_text())
        assert d["provenance"]["implementation_sha256"] == digest, f.name
        assert d["provenance"]["mathematical_proof"] is False and d["results"], f.name


def test_agrees_with_the_dense_reference_when_present():
    """the independent dense reference (viscous_node/audit/ref_model.py, written statement by statement) is not part of the published package: skipped there"""
    path = HERE.parent / "audit" / "ref_model.py"
    if not path.exists():
        return
    spec = importlib.util.spec_from_file_location("ref_model", path)
    ref = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ref)
    rng = np.random.default_rng(11)
    for kind in KINDS:
        for n in (16, 33):
            D = np.array([rng.uniform(-.4, .4), rng.uniform(0, 1), rng.uniform(.002, .2)])
            m, M = NodeBurgers(n, D[2], D[0], D[1], kind, .01), ref.Model(n, kind)
            u = random_state(m, rng)
            np.testing.assert_allclose(m.residual(u), M.residual(u, D), atol=1e-13)
            np.testing.assert_allclose(m.jacobian(u).toarray(), M.jac_state(u, D), atol=1e-13)
            np.testing.assert_allclose(m.parameter_jacobian(u), M.jac_design(u, D), atol=1e-13)
        for n in (8, 33):                                                                # Newton solutions, adjoint and gradients at the defaults
            m, s, an = solve_and_analyse(n, kind)
            S = ref.Model(n, kind).sensitivities(ref.DEFAULT_D)
            np.testing.assert_allclose(s["u"], S["U"], atol=1e-12)
            np.testing.assert_allclose(an["psi"], S["psi"], atol=1e-10)
            np.testing.assert_allclose(an["gradient"], S["gradAdjoint"], atol=1e-11)
            assert len(s["history"]) == len(S["hist"])


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted((k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)):
        try:
            fn()
            print(f"PASS {name}")
        except Exception:
            failed += 1
            print(f"FAIL {name}")
            traceback.print_exc()
    print("all tests passed" if not failed else f"{failed} test(s) failed")
    sys.exit(1 if failed else 0)
