from scipy.integrate import ode
import random
import sys

def system_function(t, state, args):
    dstatedt = [0] * len (state)

    EGF = state[0]
    boundEGFR = state[1]
    unboundEGFR = state[2]
    activeSos = state[3]
    inactiveSos = state[4]
    activeRas = state[5]
    inactiveRas = state[6]
    cRaf = state[7]
    cRafPP = state[8]
    MEK = state[9]
    MEKPP = state[10]
    ERK = state[11]
    ERKPP = state[12]
    removedSos = state[13]
    PKA = state[14]
    removedcRaf = state[15]
    inactivePKA = state[16]
    EPAC = state[17]
    inactiveEPAC = state[18]
    activeRap1 = state[19]
    inactiveRap1 = state[20]
    BRaf = state[21]
    BRafPP = state[22]
    Gap = state[23]
    EPACA = state[24]
    Cilostamide = state[25]
    PKAA = state[26]

    p1 = args[0]
    p2 = args[1]
    p3 = args[2]
    p4 = args[3]
    p5 = args[4]
    p6 = args[5]
    p7 = args[6]
    p8 = args[7]
    p9 = args[8]
    p10 = args[9]
    p11 = args[10]
    p12 = args[11]
    p13 = args[12]
    p14 = args[13]
    p15 = args[14]
    p16 = args[15]
    p17 = args[16]
    p18 = args[17]
    p19 = args[18]
    p20 = args[19]
    p21 = args[20]
    p22 = args[21]
    p23 = args[22]
    p24 = args[23]
    p25 = args[24]
    p26 = args[25]
    p27 = args[26]
    p28 = args[27]
    p29 = args[28]
    p30 = args[29]
    p31 = args[30]
    p32 = args[31]
    p33 = args[32]
    p34 = args[33]
    p35 = args[34]
    p36 = args[35]
    p37 = args[36]
    p38 = args[37]
    p39 = args[38]
    p40 = args[39]
    p41 = args[40]
    p42 = args[41]
    p43 = args[42]
    p44 = args[43]
    p45 = args[44]
    p46 = args[45]
    p47 = args[46]
    p48 = args[47]
    SosKcat = args[48]
    SosKm = args[49]

    dstatedt[0]  = - p3 * EGF * unboundEGFR + p4 * boundEGFR
    dstatedt[1]  = + p3 * EGF * unboundEGFR - p4 * boundEGFR
    dstatedt[2]  = - p3 * EGF * unboundEGFR + p4 * boundEGFR
    dstatedt[3]  = + p1 * boundEGFR * inactiveSos / (p2 + inactiveSos) - p6 * activeSos / (p5 + activeSos) - SosKcat * activeSos * ERKPP / (SosKm + activeSos)
    dstatedt[4]  = - p1 * boundEGFR * inactiveSos / (p2 + inactiveSos) + p6 * activeSos / (p5 + activeSos) - SosKcat * ERKPP * inactiveSos / (SosKm + inactiveSos)
    dstatedt[5]  = + p7 * activeSos * inactiveRas / (p8 + inactiveRas) - p9 * Gap * activeRas / (p10 + activeRas)
    dstatedt[6]  = - p7 * activeSos * inactiveRas / (p8 + inactiveRas) + p9 * Gap * activeRas / (p10 + activeRas)
    dstatedt[7]  = - p11 * cRaf * activeRas / (p12 + cRaf) + p14 * cRafPP / (p13 + cRafPP) - p21 * cRaf * PKA / (p22 + cRaf)
    dstatedt[8]  = + p11 * cRaf * activeRas / (p12 + cRaf) - p14 * cRafPP / (p13 + cRafPP)
    dstatedt[9]  = - p15 * cRafPP * MEK / (p16 + MEK) + p18 * MEKPP / (p17 + MEKPP) - p43 * MEK * BRafPP / (p44 + MEK)
    dstatedt[10] = + p15 * cRafPP * MEK / (p16 + MEK) - p18 * MEKPP / (p17 + MEKPP) + p43 * MEK * BRafPP / (p44 + MEK)
    dstatedt[11] = - p19 * ERK * MEKPP / (p20 + ERK) + p47 * ERKPP / (p48 + ERKPP)
    dstatedt[12] = + p19 * ERK * MEKPP / (p20 + ERK) - p47 * ERKPP / (p48 + ERKPP)
    dstatedt[13] = + SosKcat * ERKPP * inactiveSos / (SosKm + inactiveSos) + SosKcat * activeSos * ERKPP / (SosKm + activeSos)
    dstatedt[14] = + p23 * inactivePKA * PKAA / (p24 + inactivePKA) + p25 * inactivePKA * Cilostamide / (p26 + inactivePKA) - p28 * PKA / (p27 + PKA)
    dstatedt[15] = + p21 * cRaf * PKA / (p22 + cRaf)
    dstatedt[16] = - p23 * inactivePKA * PKAA / (p24 + inactivePKA) - p25 * inactivePKA * Cilostamide / (p26 + inactivePKA) + p28 * PKA / (p27 + PKA)
    dstatedt[17] = + p29 * inactiveEPAC * EPACA / (p30 + inactiveEPAC) + p31 * inactiveEPAC * Cilostamide / (p32 + inactiveEPAC) - p34 * EPAC / (p33 + EPAC)
    dstatedt[18] = - p29 * inactiveEPAC * EPACA / (p30 + inactiveEPAC) - p31 * inactiveEPAC * Cilostamide / (p32 + inactiveEPAC) + p34 * EPAC / (p33 + EPAC)
    dstatedt[19] = + p35 * inactiveRap1 * EPAC / (p36 + inactiveRap1) - p37 * activeRap1 * Gap / (p38 + activeRap1)
    dstatedt[20] = - p35 * inactiveRap1 * EPAC / (p36 + inactiveRap1) + p37 * activeRap1 * Gap / (p38 + activeRap1)
    dstatedt[21] = - p39 * BRaf * activeRap1 / (p40 + BRaf) + p42 * BRafPP / (p41 + BRafPP) - p45 * BRaf * activeRas / (p46 + BRaf)
    dstatedt[22] = + p39 * BRaf * activeRap1 / (p40 + BRaf) - p42 * BRafPP / (p41 + BRafPP) + p45 * BRaf * activeRas / (p46 + BRaf)
    dstatedt[23] = 0
    dstatedt[24] = 0
    dstatedt[25] = 0
    dstatedt[26] = 0
    return dstatedt

def set_rand_args():
    args = [random.random () for _ in range (50)]
    for i in range(len(args)):
        if random.random () > .5:
            args[i] *= 100
    return args


y0 = [1000,
     0,
     500,
     0,
     1200,
     0,
     1200,
     1500,
     0,
     3000,
     0,
     9000,
     1000,
     0,
     0,
     0,
     1000,
     0,
     1000,
     0,
     1200,
     1500,
     0,
     2400,
     0,
     0,
     0]
m = 10 # number of time steps
reps = int(sys.argv[1])
t = [(x + 1) * 120 / m for x in range (m)]
integrator = ode(system_function)
integrator.set_integrator('vode', method='bdf', atol=1e-8, rtol=1e-8,\
        nsteps=5000)
for _ in range(reps):
    integrator.set_initial_value(y0, 0)
    args = set_rand_args()
    integrator.set_f_params(tuple (args,))
    for t_step in t:
        y = integrator.integrate(t_step)
