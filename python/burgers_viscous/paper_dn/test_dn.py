"""Small deterministic checks for the independent paper_dn formulation."""
import unittest
import numpy as np
from benchmark import Benchmark, MAX_INTERVALS, infinity


class DirichletNeumannChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q0 = Benchmark(32)
        cls.q0_reference, cls.q0_reference_details = cls.q0.continuous_reference()
        cls.one_x = Benchmark(32, nu=.05, objective="one_x")
        cls.one_x_reference, _ = cls.one_x.continuous_reference()

    def test_input_resource_and_parameter_limits(self):
        for settings in ({"intervals": 7}, {"intervals": MAX_INTERVALS+1},
                         {"nu": 0}, {"mu": -.1}, {"mu": float("nan")},
                         {"objective": "tracking"}, {"correction_atol": 0}):
            with self.assertRaises(ValueError):
                Benchmark(**settings)

    def test_manufactured_state_has_expected_central_truncation(self):
        model = self.q0
        residual = model.residual(model.exact(model.x[1:]))
        truncation = -2*model.mu**2*model.h**2*(1-model.x[1:-1])
        self.assertLess(infinity(residual[:-1]-truncation), 1e-12)
        self.assertLess(abs(residual[-1]), 1e-12)
        # The nonconstant exact PDE solution is not inserted as a discrete root.
        self.assertGreater(infinity(residual), 1e-6)

    def test_exact_sparse_jacobian_and_source_mu_with_complex_step(self):
        model = self.q0
        u = 1+.03*np.cos(model.x[1:]*3)
        v = np.sin(model.x[1:]*5)
        _, A = model.residual(u, jacobian=True)
        state_cs = model.residual(u.astype(complex)+1j*1e-30*v).imag/1e-30
        parameter_cs = model.residual(u, model.mu+1j*1e-30).imag/1e-30
        self.assertLess(infinity(A@v-state_cs), 1e-10)
        self.assertLess(infinity(model.parameter_jacobian(u)-parameter_cs), 1e-12)
        self.assertLessEqual(A.nnz, 3*model.n)

    def test_q0_is_frozen_at_target_mu(self):
        left = Benchmark(32, mu=.1, target_mu=.2)
        right = Benchmark(32, mu=.3, target_mu=.2)
        np.testing.assert_array_equal(left.q.coef, right.q.coef)
        probe = np.linspace(0, 1, 37)
        manufactured_rhs = (-left.exact(probe, left.target_mu)*left.lambda_star.deriv()(probe)
                            -left.nu*left.lambda_star.deriv(2)(probe))
        self.assertLess(infinity(left.q(probe)-manufactured_rhs), 1e-14)
        robin = left.nu*left.lambda_star.deriv()(1)+(1+left.target_mu)*left.lambda_star(1)
        self.assertLess(abs(robin), 1e-14)

    def test_continuous_physical_reference_matches_analytic_baseline(self):
        details = self.q0_reference_details
        self.assertLess(details["gradient_absolute_error"], 1e-10)
        self.assertLess(details["analytic_lambda_star_max_error"], 1e-10)
        self.assertLess(abs(details["right_robin_residual"]), 1e-10)

    def test_tangent_adjoint_full_rerun_and_stopping(self):
        for model, ref in ((self.q0, self.q0_reference), (self.one_x, self.one_x_reference)):
            with self.subTest(objective=model.objective_name):
                root = model.solve()
                result = model.analyse(root, ref)
                fd = model.finite_difference(root, result["gradient"], 1e-5)
                self.assertEqual(root["initial_guess"], "constant 1")
                self.assertLessEqual(root["final_correction_inf"], model.atol+model.rtol*infinity(root["u"]))
                self.assertLess(result["tangent_adjoint_error"], 1e-10)
                self.assertLess(result["transpose_relative_error"], 1e-12)
                self.assertLess(fd["absolute_error"], 1e-8)

    def test_zero_mu_one_x_has_known_discrete_tangent_objective(self):
        model = Benchmark(32, mu=0., nu=.05, objective="one_x")
        ref, _ = model.continuous_reference()
        root = model.solve()
        result = model.analyse(root, ref)
        np.testing.assert_array_equal(root["u"], np.ones(model.n))
        self.assertAlmostEqual(result["gradient"], 13/12-model.h**2/12, delta=1e-11)
        self.assertAlmostEqual(result["objective"], 1.5, delta=1e-14)

    def test_refinement_and_actual_neumann_adjoint_layer(self):
        coarse, fine = Benchmark(64), Benchmark(128)
        c = coarse.analyse(coarse.solve(), self.q0_reference)
        f = fine.analyse(fine.solve(), self.q0_reference)
        self.assertGreater(c["state_l2_error"]/f["state_l2_error"], 3.7)
        self.assertGreater(c["gradient_error"]/f["gradient_error"], 3.7)
        # Preserve the actual unweighted transpose density near the 3-point BC.
        # An artificial 2/3 rescaling of the penultimate node would hide this.
        model = Benchmark(256)
        layer = model.analyse(model.solve(), self.q0_reference)
        self.assertGreater(layer["adjoint_penultimate_ratio"], 1.43)
        self.assertLess(layer["adjoint_penultimate_ratio"], 1.5)
        self.assertGreater(layer["adjoint_l2_error"], 1e-3)


if __name__ == "__main__":
    unittest.main()
