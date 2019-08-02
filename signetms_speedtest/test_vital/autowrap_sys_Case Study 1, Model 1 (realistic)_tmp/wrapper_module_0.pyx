import numpy as np
cimport numpy as np

cdef extern from 'wrapped_code_0.h':
    void autofunc(double *y, double *p, double *dy)

def autofunc_c(np.ndarray[np.double_t, ndim=2] y, np.ndarray[np.double_t, ndim=2] p):

    cdef np.ndarray[np.double_t, ndim=2] dy = np.empty((5,1))
    autofunc(<double*> y.data, <double*> p.data, <double*> dy.data)
    return dy