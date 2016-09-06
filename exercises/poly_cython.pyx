# cython: language_level=3, boundscheck=False, wraparound=False

import numpy as np
from libc.math cimport sin, cos


def poly_i(double[:] x):
    cdef double[:] out = np.empty_like(x)
    cdef int i

    for i in range(len(x)):
        out[i] = .25*x[i]**3 + .75*x[i]**2 - 1.5*x[i] - 2
    return np.asarray(out)


def poly_ii(double[:] x):
    cdef double[:] out = np.empty_like(x)
    cdef int i

    for i in range(len(x)):
        out[i] = ((.25*x[i] + .75)*x[i] - 1.5)*x[i] - 2
    return np.asarray(out)


def copy(double[:] x):
    cdef double[:] out = np.empty_like(x)
    cdef int i

    for i in range(len(x)):
        out[i] = x[i]
    return np.asarray(out)


def transcendent(double[:] x):
    cdef double[:] out = np.empty_like(x)
    cdef int i

    for i in range(len(x)):
        out[i] = sin(x[i])**2 + cos(x[i])**2
    return np.asarray(out)
