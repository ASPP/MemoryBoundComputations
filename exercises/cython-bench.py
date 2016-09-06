#######################################################################
# Script that benchmarks the computation of a polynomial
# by using Cython.
#
# Author: Francesc Alted
# Date: 2016-09-01
#######################################################################

from time import time
import numpy as np
# Easy way to compile an extension with Cython:
# http://cython.readthedocs.io/en/latest/src/reference/compilation.html#compiling-with-pyximport
import pyximport; pyximport.install()

# The Cython extension to be compiled
import poly_cython

N = 10*1000*1000
x = np.linspace(-10, 10, N)

t0 = time()
poly_cython.poly_i(x)
print("Evaluation of the original poly: \t\t%.3f" % (time() - t0))

t0 = time()
poly_cython.poly_ii(x)
print("Evaluation of computer-friendly poly: \t\t%.3f" % (time() - t0))

t0 = time()
poly_cython.copy(x)
print("Simple copy: \t\t\t\t\t%.3f" % (time() - t0))

t0 = time()
poly_cython.transcendent(x)
print("Evaluation of a transcendental expression: \t%.3f" % (time() - t0))
