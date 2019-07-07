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
    float S   = NV_Ith_S(y, 0);
    float dS  = NV_Ith_S(y, 1);
    float R   = NV_Ith_S(y, 2);
    float RS  = NV_Ith_S(y, 3);
    float Rpp = NV_Ith_S(y, 4);
    NV_Ith_S(ydot, 0) = - p1 * S - (p2 * R * S - p3 * RS);
    NV_Ith_S(ydot, 1) = p1 * S;
    NV_Ith_S(ydot, 2) = - (p2 * R * S - p3 * RS) + \
                        (p5 * Rpp / (p6 + Rpp));
    NV_Ith_S(ydot, 3) = (p2 * R * S - p3 * RS) -  p4 * RS;
    NV_Ith_S(ydot, 4) = p4 * RS - (p5 * Rpp / (p6 + Rpp));
    return 0;
}


void set_rand_args(float *args)
{
    int i;
    for (i = 0; i < 6; i++)
    {
        args[i] = (rand() / (float) RAND_MAX);
        if (rand () / (float) RAND_MAX > .5)
            args[i] *= 10;
    }
}


int main(int argc, char **argv)
{
    SimpleCVODESolver *solver = new_cvode_solver(STIFF_INTEGRATOR);
    int i, j, n = 5, m = 20, reps;
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
    args = malloc(6 * sizeof (float));
    reps = atoi(argv[1]);
    
    t = malloc(m * sizeof (float));
    for (i = 0; i < m; i++)
        t[i] = tf * (i + 1) / (float) m;
    y0 = malloc(n * sizeof (float));
    y0[0] = 1;
    y0[1] = 0;
    y0[2] = 1;
    y0[3] = 0;
    y0[4] = 0;
     
    init_solver(solver, f, t0, y0, n);
    set_tolerance(solver, 1e-8, 1e-8);
    set_max_step(solver, 5000);
    prepare_solver(solver);
    for (i = 0; i < reps; i++) 
    {
        set_rand_args(args);
        /*printf("args[0] = %.3f\n", args[0]);*/
        /*printf("args[1] = %.3f\n", args[1]);*/
        /*printf("args[2] = %.3f\n", args[2]);*/
        /*printf("args[3] = %.3f\n", args[3]);*/
        /*printf("args[4] = %.3f\n", args[4]);*/
        /*printf("args[5] = %.3f\n", args[5]);*/
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
