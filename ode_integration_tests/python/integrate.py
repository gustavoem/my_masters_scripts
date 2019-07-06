from scipy.integrate import odeint
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

y0 = [1, 0, 1, 0, 0]
args = [0] * 6
m = int(sys.argv[1])
args[0] = float(sys.argv[2])
args[1] = float(sys.argv[3])
args[2] = float(sys.argv[4])
args[3] = float(sys.argv[5])
args[4] = float(sys.argv[6])
args[5] = float(sys.argv[7])
t = [(x + 1) * 100 / m for x in range (m)]
odeint(system_function, y0, t, atol=1e-8, rtol=1e-8, args=(args,), 
        tfirst=True)
