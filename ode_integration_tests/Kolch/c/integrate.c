#include "scvodew.h"
#include <nvector/nvector_serial.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


static int f(realtype t, N_Vector y, N_Vector ydot, void *f_data) 
{
    float p1 = ((float *) f_data)[0];
    float p2 = ((float *) f_data)[1];
    float p3 = ((float *) f_data)[2];
    float p4 = ((float *) f_data)[3];
    float p5 = ((float *) f_data)[4];
    float p6 = ((float *) f_data)[5];
    float p7 = ((float *) f_data)[6];
    float p8 = ((float *) f_data)[7];
    float p9 = ((float *) f_data)[8];
    float p10 = ((float *) f_data)[9];
    float p11 = ((float *) f_data)[10];
    float p12 = ((float *) f_data)[11];
    float p13 = ((float *) f_data)[12];
    float p14 = ((float *) f_data)[13];
    float p15 = ((float *) f_data)[14];
    float p16 = ((float *) f_data)[15];
    float p17 = ((float *) f_data)[16];
    float p18 = ((float *) f_data)[17];
    float p19 = ((float *) f_data)[18];
    float p20 = ((float *) f_data)[19];
    float p21 = ((float *) f_data)[20];
    float p22 = ((float *) f_data)[21];
    float p23 = ((float *) f_data)[22];
    float p24 = ((float *) f_data)[23];
    float p25 = ((float *) f_data)[24];
    float p26 = ((float *) f_data)[25];
    float p27 = ((float *) f_data)[26];
    float p28 = ((float *) f_data)[27];
    float p29 = ((float *) f_data)[28];
    float p30 = ((float *) f_data)[29];
    float p31 = ((float *) f_data)[30];
    float p32 = ((float *) f_data)[31];
    float p33 = ((float *) f_data)[32];
    float p34 = ((float *) f_data)[33];
    float p35 = ((float *) f_data)[34];
    float p36 = ((float *) f_data)[35];
    float p37 = ((float *) f_data)[36];
    float p38 = ((float *) f_data)[37];
    float p39 = ((float *) f_data)[38];
    float p40 = ((float *) f_data)[39];
    float p41 = ((float *) f_data)[40];
    float p42 = ((float *) f_data)[41];
    float p43 = ((float *) f_data)[42];
    float p44 = ((float *) f_data)[43];
    float p45 = ((float *) f_data)[44];
    float p46 = ((float *) f_data)[45];
    float p47 = ((float *) f_data)[46];
    float p48 = ((float *) f_data)[47];
    float SosKcat = ((float *) f_data)[48];
    float SosKm = ((float *) f_data)[49];

	float EGF = NV_Ith_S(y, 0);
	float boundEGFR = NV_Ith_S(y, 1);
	float unboundEGFR = NV_Ith_S(y, 2);
	float activeSos = NV_Ith_S(y, 3);
	float inactiveSos = NV_Ith_S(y, 4);
	float activeRas = NV_Ith_S(y, 5);
	float inactiveRas = NV_Ith_S(y, 6);
	float cRaf = NV_Ith_S(y, 7);
	float cRafPP = NV_Ith_S(y, 8);
	float MEK = NV_Ith_S(y, 9);
	float MEKPP = NV_Ith_S(y, 10);
	float ERK = NV_Ith_S(y, 11);
	float ERKPP = NV_Ith_S(y, 12);
	float removedSos = NV_Ith_S(y, 13);
	float PKA = NV_Ith_S(y, 14);
	float removedcRaf = NV_Ith_S(y, 15);
	float inactivePKA = NV_Ith_S(y, 16);
	float EPAC = NV_Ith_S(y, 17);
	float inactiveEPAC = NV_Ith_S(y, 18);
	float activeRap1 = NV_Ith_S(y, 19);
	float inactiveRap1 = NV_Ith_S(y, 20);
	float BRaf = NV_Ith_S(y, 21);
	float BRafPP = NV_Ith_S(y, 22);
	float Gap = NV_Ith_S(y, 23);
	float EPACA = NV_Ith_S(y, 24);
	float Cilostamide = NV_Ith_S(y, 25);
	float PKAA = NV_Ith_S(y, 26);

	NV_Ith_S(ydot, 0)  = - p3 * EGF * unboundEGFR + p4 * boundEGFR;
	NV_Ith_S(ydot, 1)  = + p3 * EGF * unboundEGFR - p4 * boundEGFR;
	NV_Ith_S(ydot, 2)  = - p3 * EGF * unboundEGFR + p4 * boundEGFR;
	NV_Ith_S(ydot, 3)  = + p1 * boundEGFR * inactiveSos / (p2 + inactiveSos) - p6 * activeSos / (p5 + activeSos) - SosKcat * activeSos * ERKPP / (SosKm + activeSos);
	NV_Ith_S(ydot, 4)  = - p1 * boundEGFR * inactiveSos / (p2 + inactiveSos) + p6 * activeSos / (p5 + activeSos) - SosKcat * ERKPP * inactiveSos / (SosKm + inactiveSos);
	NV_Ith_S(ydot, 5)  = + p7 * activeSos * inactiveRas / (p8 + inactiveRas) - p9 * Gap * activeRas / (p10 + activeRas);
	NV_Ith_S(ydot, 6)  = - p7 * activeSos * inactiveRas / (p8 + inactiveRas) + p9 * Gap * activeRas / (p10 + activeRas);
	NV_Ith_S(ydot, 7)  = - p11 * cRaf * activeRas / (p12 + cRaf) + p14 * cRafPP / (p13 + cRafPP) - p21 * cRaf * PKA / (p22 + cRaf);
	NV_Ith_S(ydot, 8)  = + p11 * cRaf * activeRas / (p12 + cRaf) - p14 * cRafPP / (p13 + cRafPP);
	NV_Ith_S(ydot, 9)  = - p15 * cRafPP * MEK / (p16 + MEK) + p18 * MEKPP / (p17 + MEKPP) - p43 * MEK * BRafPP / (p44 + MEK);
	NV_Ith_S(ydot, 10) = + p15 * cRafPP * MEK / (p16 + MEK) - p18 * MEKPP / (p17 + MEKPP) + p43 * MEK * BRafPP / (p44 + MEK);
	NV_Ith_S(ydot, 11) = - p19 * ERK * MEKPP / (p20 + ERK) + p47 * ERKPP / (p48 + ERKPP);
	NV_Ith_S(ydot, 12) = + p19 * ERK * MEKPP / (p20 + ERK) - p47 * ERKPP / (p48 + ERKPP);
	NV_Ith_S(ydot, 13) = + SosKcat * ERKPP * inactiveSos / (SosKm + inactiveSos) + SosKcat * activeSos * ERKPP / (SosKm + activeSos);
	NV_Ith_S(ydot, 14) = + p23 * inactivePKA * PKAA / (p24 + inactivePKA) + p25 * inactivePKA * Cilostamide / (p26 + inactivePKA) - p28 * PKA / (p27 + PKA);
	NV_Ith_S(ydot, 15) = + p21 * cRaf * PKA / (p22 + cRaf);
	NV_Ith_S(ydot, 16) = - p23 * inactivePKA * PKAA / (p24 + inactivePKA) - p25 * inactivePKA * Cilostamide / (p26 + inactivePKA) + p28 * PKA / (p27 + PKA);
	NV_Ith_S(ydot, 17) = + p29 * inactiveEPAC * EPACA / (p30 + inactiveEPAC) + p31 * inactiveEPAC * Cilostamide / (p32 + inactiveEPAC) - p34 * EPAC / (p33 + EPAC);
	NV_Ith_S(ydot, 18) = - p29 * inactiveEPAC * EPACA / (p30 + inactiveEPAC) - p31 * inactiveEPAC * Cilostamide / (p32 + inactiveEPAC) + p34 * EPAC / (p33 + EPAC);
	NV_Ith_S(ydot, 19) = + p35 * inactiveRap1 * EPAC / (p36 + inactiveRap1) - p37 * activeRap1 * Gap / (p38 + activeRap1);
	NV_Ith_S(ydot, 20) = - p35 * inactiveRap1 * EPAC / (p36 + inactiveRap1) + p37 * activeRap1 * Gap / (p38 + activeRap1);
	NV_Ith_S(ydot, 21) = - p39 * BRaf * activeRap1 / (p40 + BRaf) + p42 * BRafPP / (p41 + BRafPP) - p45 * BRaf * activeRas / (p46 + BRaf);
	NV_Ith_S(ydot, 22) = + p39 * BRaf * activeRap1 / (p40 + BRaf) - p42 * BRafPP / (p41 + BRafPP) + p45 * BRaf * activeRas / (p46 + BRaf);
	NV_Ith_S(ydot, 23) = 0;
	NV_Ith_S(ydot, 24) = 0;
	NV_Ith_S(ydot, 25) = 0;
	NV_Ith_S(ydot, 26) = 0;
    return 0;
}


void set_rand_args(float *args)
{
    int i;
    for (i = 0; i < 50; i++)
    {
        args[i] = (rand() / (float) RAND_MAX);
        if (rand () / (float) RAND_MAX > .5)
            args[i] *= 100;
    }
}


int main(int argc, char **argv)
{
    SimpleCVODESolver *solver = new_cvode_solver(STIFF_INTEGRATOR);
    int i, j, n = 27, m = 10, reps;
    float t0 = 0;
    float tf = 120;
    float *y0, *args, *t;
    float **result;
    
    srand(time(0));
    if (argc != 2)
    {
        printf("Wrong number of parameters!\n");
        return -1;
    }
    args = malloc(50 * sizeof (float));
    reps = atoi(argv[1]);
    
    t = malloc(m * sizeof (float));
    for (i = 0; i < m; i++)
        t[i] = tf * (i + 1) / (float) m;
    y0 = malloc(n * sizeof (float));
    y0[0] = 1000;
    y0[1] = 0;
    y0[2] = 500;
    y0[3] = 0;
    y0[4] = 1200;
    y0[5] = 0;
    y0[6] = 1200;
    y0[7] = 1500;
    y0[8] = 0;
    y0[9] = 3000;
    y0[10] = 0;
    y0[11] = 9000;
    y0[12] = 1000;
    y0[13] = 0;
    y0[14] = 0;
    y0[15] = 0;
    y0[16] = 1000;
    y0[17] = 0;
    y0[18] = 1000;
    y0[19] = 0;
    y0[20] = 1200;
    y0[21] = 1500;
    y0[22] = 0;
    y0[23] = 2400;
    y0[24] = 0;
    y0[25] = 0;
    y0[26] = 0;
    
     
    init_solver(solver, f, t0, y0, n);
    set_tolerance(solver, 1e-8, 1e-8);
    set_max_step(solver, 5000);
    prepare_solver(solver);
    for (i = 0; i < reps; i++) 
    {
        set_rand_args(args);
        set_system_data(solver, args);
        result = integrate(solver, t, m);
        reset_solver(solver, t0, y0);
        if (result != NULL) 
        {
            for (j = 0; j < m; j++)
                free(result[j]);
            free(result);

        }
    }
    delete_solver(solver);
    free(t);
    free(y0);
    free(args);
    return 0;
}
