/******************************************************************************
 *                     Code generated with sympy 1.5.dev                      *
 *                                                                            *
 *              See http://www.sympy.org/ for more information.               *
 *                                                                            *
 *                      This file is part of 'autowrap'                       *
 ******************************************************************************/
#include "wrapped_code_0.h"
#include <math.h>

void autofunc(double *y, double *p, double *dy) {

   dy[0] = -p[0]*y[0] - p[1]*y[0]*y[2] + p[2]*y[3];
   dy[1] = p[0]*y[0];
   dy[2] = -p[1]*y[0]*y[2] + p[2]*y[3] + p[4]*y[4]/(p[5] + y[4]);
   dy[3] = p[1]*y[0]*y[2] - p[2]*y[3] - p[3]*y[3];
   dy[4] = p[3]*y[3] - p[4]*y[4]/(p[5] + y[4]);

}
