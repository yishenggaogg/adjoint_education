"""Small-grid mathematical and source-parity regressions; no PDE proof claim."""
import json
import unittest
from pathlib import Path
import numpy as np
from solve import Burgers


class Tests(unittest.TestCase):
    def test_exact_jacobian_and_transpose(self):
        rng = np.random.default_rng(910)
        for kind in ("first", "none", "smooth"):
            m = Burgers(24, reconstruction=kind)
            u = m.exact(m.x)+.003*rng.normal(size=m.n)
            _, A = m.residual(u, jacobian=True)
            v, w = rng.normal(size=m.n), rng.normal(size=m.n)
            cs = m.residual(u.astype(complex)+1j*1e-30*v).imag/1e-30
            np.testing.assert_allclose(A@v, cs, atol=2e-14, rtol=2e-13)
            self.assertLess(abs(w@(A@v)-v@(A.T@w)), 1e-12)

    def test_gradient_and_refinement(self):
        errors = []
        for n in (32, 64, 128):
            m = Burgers(n)
            s = m.solve()
            a = m.analyse(s)
            self.assertLess(a["gradient_duality_error"], 2e-12)
            self.assertLess(m.gradient_check(s, a)["absolute_error"], 2e-8)
            self.assertLess(a["adjoint_residual_inf"], 1e-12)
            errors.append(a["state_l1_error"])
        self.assertLess(errors[-1], errors[0]/3)

    def test_constant_exact_and_parameter_boundaries(self):
        m = Burgers(32, amplitude=0.)
        s = m.solve()
        np.testing.assert_allclose(s["u"], 1., atol=1e-14)
        m = Burgers(16)
        u = m.exact(m.x)
        rp = m.parameter_jacobian(u)
        for k in range(3):
            pp, pm = m.p.copy(), m.p.copy()
            pp[k] += 1e-6
            pm[k] -= 1e-6
            np.testing.assert_allclose(rp[:, k], (m.residual(u, pp)-m.residual(u, pm))/2e-6, atol=3e-10)

    def test_original_javascript_snapshot(self):
        fixture = json.loads((Path(__file__).parent/"examples/javascript_reference.json").read_text())
        for row in fixture["results"]:
            m = Burgers(row["cells"], reconstruction=row["kind"])
            s = m.solve()
            a = m.analyse(s)
            np.testing.assert_allclose(s["u"], row["u"], atol=3e-10, rtol=0)
            np.testing.assert_allclose(a["gradient"][:2], row["gradient"], atol=3e-10, rtol=0)
            self.assertLess(abs(a["objective"]-row["objective"]), 3e-10)

    def test_limits(self):
        for kwargs in ({"nu": 0}, {"n": 65537}, {"amplitude": 3}):
            with self.assertRaises(ValueError):
                Burgers(**kwargs)

    def test_continuous_adjoint_boundary_pairing(self):
        m = Burgers(16)
        c = m.continuous_adjoint()
        expected = m.analyse(m.solve())["exact_gradient"][:2]
        np.testing.assert_allclose(m.continuous_gradient(c), expected, atol=2e-10, rtol=0)


if __name__ == "__main__":
    unittest.main()
