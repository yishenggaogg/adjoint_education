#!/usr/bin/env python3
"""Independent FD-step scan for the preserved Appendix D.3 viscous model."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
import numpy as np
from solve import Burgers, provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cells', type=int, default=128)
    parser.add_argument('--output', type=Path, default=Path('examples/fd_scan.json'))
    args = parser.parse_args()
    model = Burgers(args.cells)
    start = time.perf_counter()
    solution = model.solve()
    analysis = model.analyse(solution)
    direction = np.array([1., .3, 0.])
    predicted = float(np.dot(analysis['gradient'], direction))
    inputs = {'cells':args.cells, 'nu':.01, 'amplitude':.2, 'phase':.07,
              'reconstruction':'none', 'direction':direction.tolist()}
    rows = []
    for step in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]:
        values, solves = [], []
        started = time.perf_counter()
        for sign in (-1, 1):
            p = model.p+sign*step*direction
            other = Burgers(args.cells, p[2], p[0], p[1])
            ss = other.solve()  # fresh solve from this perturbed problem's own initial guess
            values.append(float(other.weights@ss['u']))
            solves.append({'sign':sign, 'parameters_amplitude_phase_nu':p.tolist(),
                           'iterations':len(ss['history'])-1, 'history':ss['history'],
                           'residual_inf':float(np.max(abs(other.residual(ss['u'])))),
                           'residual_density_inf':float(np.max(abs(other.residual(ss['u'])))/other.h),
                           'correction_inf':ss['history'][-1]['correction_inf'],
                           'termination_reason':'Newton correction infinity norm <= 2e-11'})
        fd = (values[1]-values[0])/(2*step)
        rows.append({'step':step,'finite_difference':fd,'adjoint_gradient':predicted,
                     'absolute_error':abs(fd-predicted),'perturbed_solves':solves,
                     'elapsed_seconds':time.perf_counter()-started})
    root = Path(__file__).parent
    report = {'provenance':provenance(), 'inputs':inputs,
              'input_sha256':hashlib.sha256(json.dumps(inputs,sort_keys=True).encode()).hexdigest(),
              'source_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest()
                               for name in ['solve.py','fd_scan.py']},
              'baseline_gradient':analysis['gradient'], 'baseline_history':solution['history'],
              'stopping_correction_tolerance':2e-11,'max_newton_iterations':35,
              'memory_peak_measured':False,'memory_peak_bytes':None,
              'elapsed_seconds':time.perf_counter()-start,'results':rows,
              'mathematical_proof':False}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'cells':args.cells,'rows':len(rows),'best_error':min(r['absolute_error'] for r in rows),
                      'elapsed_seconds':report['elapsed_seconds'],'output':str(args.output)}))


if __name__ == '__main__':
    main()
