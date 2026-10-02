"""Exact finite algebra checks supporting THEORY_REVIEW.md; no PDE solver.

Run with the Python standard library: python3 check_algebra.py.
Use --check to compare the stored report without writing it.
Universal-in-N arguments remain the human-readable analytic proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import argparse

checks = []

def check(condition, label):
    assert condition, label
    checks.append(label)

def add(a, b):
    out = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] += x
    return out

def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i+j] += x*y
    return out

def scale(a, c): return [c*x for x in a]
def integ(a): return sum(x/Q(i+1) for i, x in enumerate(a))
def deriv(a): return [Q(i)*a[i] for i in range(1, len(a))]
def value(a, x): return sum(c*x**i for i, c in enumerate(a))

mu, nu = Q(1,5), Q(1,10)
c = (nu+1+mu)/(2*nu+1+mu)
z = [Q(0), Q(2), Q(-1)]
u = add([Q(1)], scale(z, mu))
lam = [Q(0), Q(1), -c]
q = add(scale(mul(u, deriv(lam)), -1), scale(deriv(deriv(lam)), -nu))
smu = add(mul([Q(2),Q(-2)], add([Q(1)],scale(z,2*mu))), [2*nu])
g, pairing = integ(mul(q,z)), integ(mul(lam,smu))
j0, jbase = integ(q), integ(q)+mu*g
check(q == [Q(-57,70),Q(51,35),Q(33,35),Q(-13,35)], 'primary q0 polynomial')
check(nu*value(deriv(lam),1)+(1+mu)*value(lam,1)==0, 'physical adjoint Robin data')
check(g == pairing == Q(547,2100), 'exact frozen gradient and Green pairing')
check(j0 == Q(19,140) and jbase == Q(493,2625), 'exact primary J')
check(integ(mul([Q(1),Q(1)],z)) == Q(13,12), 'secondary gradient')
fpp = deriv(deriv(mul(q,z)))
bernstein = [fpp[0], fpp[0]+fpp[1]/3,
             fpp[0]+2*fpp[1]/3+fpp[2]/3, sum(fpp)]
check(bernstein == [Q(261,35),Q(291,35),Q(85,35),Q(-97,35)], 'q0*z Bernstein curvature enclosure')
check(value(q,1) == Q(17,14) and value(q,0) == Q(-57,70), 'q0 endpoint values for monotone sup bound')
check(Q(85,42)*16 == Q(680,21) and Q(85,42)*8+Q(97,140)==Q(7091,420), 'explicit O(h) primary gradient constants')

for visc, n in [(Q(1,10),16),(Q(1,20),64)]:
    h = Q(1,n)
    U = [1+mu*value(z,i*h) for i in range(n+1)]
    Z = [value(z,i*h) for i in range(n+1)]
    rho = 2*mu*mu*h*h/visc
    contract = rho/(visc*h)
    check(h < 2*visc/(1+mu) and contract <= Q(1,2), f'N{n} M and contraction thresholds')
    check((3*U[n]-4*U[n-1]+U[n-2])/(2*h)==0, f'N{n} exact primal Neumann row')
    check((4*Z[n-1]-Z[n-2])/3==Z[n], f'N{n} exact tangent endpoint extension')
    for i in range(1,n):
        x = i*h
        source = 2*mu*(1-x)*U[i]+2*visc*mu
        residual = (U[i+1]**2-U[i-1]**2)/(4*h)-visc*(U[i+1]-2*U[i]+U[i-1])/h**2-source
        assert residual == 2*mu*mu*h*h*(x-1)
        az = (U[i+1]*Z[i+1]-U[i-1]*Z[i-1])/(2*h)-visc*(Z[i+1]-2*Z[i]+Z[i-1])/h**2
        assert az == 2*visc+2*(1-x)*(1+2*mu*Z[i]-2*mu*h*h)
        assert az >= 2*visc
    checks.append(f'N{n} all exact residual and barrier rows')
    lower = -2*visc/(3*h*h)-U[n-2]/(2*h)-U[n]/(6*h)
    diagonal = 2*visc/(3*h*h)+2*U[n]/(3*h)
    check(lower < 0 and diagonal > 0 and lower+diagonal == 2*mu*h, f'N{n} reduced last-row coefficients and row sum')
    for a in [Q(-1),Q(1)]:
        for b in [Q(-1),Q(1)]:
            row_norm = (abs(2*a+4*b)+abs(8*a-2*b))/(9*h)
            assert row_norm <= Q(4,3)/h
    checks.append(f'N{n} convex corner check for reduced Jacobian Lipschitz bound')

report = {
    'method': 'Python fractions exact polynomial and finite-row algebra only; no solver, Lean, or floating arithmetic',
    'scope_note': 'Finite checks support algebra; universal mesh/root/IFT arguments are analytic in THEORY_REVIEW.md.',
    'mu0': str(mu), 'nu0': str(nu), 'c0': str(c),
    'q0_coefficients': [str(x) for x in q], 'J_constant': str(j0),
    'J_mu_coefficient': str(g), 'J_at_mu0': str(jbase),
    'adjoint_source_pairing': str(pairing), 'secondary_gradient': '13/12',
    'q0_sup_norm': '17/14', 'q0_z_second_derivative_sup_upper': '291/35',
    'primary_gradient_error_bound': '(680/21)*h + (7091/420)*h^2 for N>=16',
    'checks_passed_count': len(checks), 'checks_passed': checks,
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check', action='store_true', help='read-only comparison with the recorded JSON')
args = parser.parse_args()
target = Path(__file__).resolve().parent/'algebra_checks.json'
if args.check:
    if json.loads(target.read_text()) != report:
        raise RuntimeError('Stored exact-algebra report differs from the recomputed report')
else:
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(f'PASS {len(checks)} exact algebra groups; no PDE solver executed')
