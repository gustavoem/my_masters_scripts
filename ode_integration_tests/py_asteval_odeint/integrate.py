from scipy.integrate import odeint
import random
import sys
from asteval import Interpreter

def sys_fun_creator(args):
    rate_eq_evaluator = Interpreter()
    for i in range(len(args)):
        rate_eq_evaluator.symtable['p' + str(i + 1)] = args[i]

    def system_function(t, state):
        dstatedt = [0] * len (state)
        var_idx = {
            'S' : 0,
            'dS' : 1,
            'R' : 2,
            'RS' : 3,
            'Rpp' : 4
        }
        for var, idx in var_idx.items():
            rate_eq_evaluator.symtable[var] = state[idx]
        
        dstatedt[0] = rate_eq_evaluator('- p1 * S - (p2 * R * S - p3 * RS)')
        dstatedt[1] = rate_eq_evaluator('p1 * S')
        dstatedt[2] = rate_eq_evaluator('- (p2 * R * S - p3 * RS) + (p5 * Rpp / (p6 + Rpp))')
        dstatedt[3] = rate_eq_evaluator('(p2 * R * S - p3 * RS) -  p4 * RS')
        dstatedt[4] = rate_eq_evaluator('p4 * RS - (p5 * Rpp / (p6 + Rpp))')
        return dstatedt
    return system_function

def set_rand_args():
    args = [random.random () for _ in range (6)]
    for i in range(len(args)):
        if random.random () > .5:
            args[i] *= 10
    return args


y0 = [1, 0, 1, 0, 0]
m = 20 # number of time steps
reps = int(sys.argv[1])
t = [(x + 1) * 100 / m for x in range (m)]
args = set_rand_args()
for _ in range(reps):
    system_function = sys_fun_creator(args)
    odeint(system_function, y0, t, atol=1e-8, rtol=1e-8, tfirst=True)
