from scipy.integrate import ode
import random
import sys

def system_function(t, state, args):
    dstatedt = [0] * len (state)
    S = state[0]
    dS = state[1]
    R = state[2]
    RS = state[3]
    Rpp = state[4]
    p1 = args[0]
    p2 = args[1]
    p3 = args[2]
    p4 = args[3]
    p5 = args[4]
    p6 = args[5]
    dstatedt[0] = - p1 * S - (p2 * R * S - p3 * RS)
    dstatedt[1] = p1 * S
    dstatedt[2] = - (p2 * R * S - p3 * RS) + (p5 * Rpp / (p6 + Rpp))
    dstatedt[3] = (p2 * R * S - p3 * RS) -  p4 * RS
    dstatedt[4] = p4 * RS - (p5 * Rpp / (p6 + Rpp))
    return dstatedt


def set_rand_args():
    args = [random.random () for _ in range (6)]
    for i in range(len(args)):
        if random.random () > .5:
            args[i] *= 10
    return args


y0 = [1, 0, 1, 0, 0]
m = 20 # number of time steps
reps = int(sys.argv[1])
t = [(x + 1) * 120 / m for x in range (m)]
integrator = ode(system_function)
integrator.set_integrator('vode', method='bdf', atol=1e-8, rtol=1e-8,\
        max_step=5000)
for _ in range(reps):
    integrator.set_initial_value(y0, 0)
    args = set_rand_args()
    integrator.set_f_params(tuple (args,))
    for t_step in t:
        y = integrator.integrate(t_step)
