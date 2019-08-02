import numpy as np
cimport numpy as np

cdef extern from 'wrapped_code_1.h':
    void autofunc(double *y, double *p, double *J)

def autofunc_c(np.ndarray[np.double_t, ndim=2] y, np.ndarray[np.double_t, ndim=2] p):

    cdef np.ndarray[np.double_t, ndim=2] J = np.empty((5,5))
    autofunc(<double*> y.data, <double*> p.data, <double*> J.data)
    return J