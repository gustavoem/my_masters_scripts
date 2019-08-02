/******************************************************************************
 *                     Code generated with sympy 1.5.dev                      *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                      This file is part of 'autowrap'                       *
 ******************************************************************************/
#include "wrapped_code_1.h"
#include <math.h>

void autofunc(double *y, double *p, double *J) {

   J[0] = -p[0] - p[1]*y[2];
   J[1] = 0;
   J[2] = -p[1]*y[0];
   J[3] = p[2];
   J[4] = 0;
   J[5] = p[0];
   J[6] = 0;
   J[7] = 0;
   J[8] = 0;
   J[9] = 0;
   J[10] = -p[1]*y[2];
   J[11] = 0;
   J[12] = -p[1]*y[0];
   J[13] = p[2];
   J[14] = p[4]/(p[5] + y[4]) - p[4]*y[4]/pow(p[5] + y[4], 2);
   J[15] = p[1]*y[2];
   J[16] = 0;
   J[17] = p[1]*y[0];
   J[18] = -p[2] - p[3];
   J[19] = 0;
   J[20] = 0;
   J[21] = 0;
   J[22] = 0;
   J[23] = p[3];
   J[24] = -p[4]/(p[5] + y[4]) + p[4]*y[4]/pow(p[5] + y[4], 2);

}
