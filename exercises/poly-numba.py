#######################################################################
# This script compares the speed of the computation of a polynomial
# for different libraries: numpy, numexpr and numba.
#
# Author: Francesc Alted
# Date: 2013-09-04
# Updated: 2016-09-01
#######################################################################

import math
from numba import double, jit
from time import time
import numpy as np
import numexpr as ne


N = 10*1000*1000             # number of points to evaluate
x = np.linspace(-10, 10, N)  # vector x in range [-10, 10]

# The different expressions supported
expr = [
    ".25*x**3 + .75*x**2 - 1.5*x - 2",  # 0) the polynomial to compute
    "((.25*x + .75)*x - 1.5)*x - 2",    # 1) a computer-friendly polynomial
    "x",                                # 2) the identity function
    "sin(x)**2 + cos(x)**2",            # 3) a transcendental function
    ]

# Set here the index of the expression to compute
expr_to_compute = 1

ne.set_num_threads(1)   # the number of threads for numexpr

# A function that is going to be accelerated by numba
def poly(x):
    y = np.empty(N, dtype=np.float64)
    if expr_to_compute == 0:
        for i in range(N):
            y[i] = 0.25*x[i]**3 + 0.75*x[i]**2 + 1.5*x[i] - 2
    elif expr_to_compute == 1:
        for i in range(N):
            y[i] = ((0.25*x[i] + 0.75)*x[i] + 1.5)*x[i] - 2
    elif expr_to_compute == 2:
        for i in range(N):
            y[i] = x[i]
    elif expr_to_compute == 3:
        for i in range(N):
            y[i] = math.sin(x[i])**2 + math.cos(x[i])**2
    return y


print("Using expression: %s" % expr[expr_to_compute], "with:", N, "points")
print()
print("*** Running numpy!")
start = time()
if "sin" in expr[expr_to_compute]:
    y = np.sin(x)**2 + np.cos(x)**2
elif "x" == expr[expr_to_compute]:
    # Trick to force a copy with NumPy
    y = x.copy()
else:
    y = eval(expr[expr_to_compute])
tnumpy = time() - start
print("Execution time for numpy is %s sec" % round(tnumpy, 3))

print()
print("*** Running numexpr!")
start = time()
y = ne.evaluate(expr[expr_to_compute], optimization='aggressive')
tnumexpr = time() - start
print("Execution time for numexpr is %s sec" % round(tnumexpr, 3))

print()
print("*** Running numba!")
start = time()
cpoly = jit(double[:](double[:]))(poly)
tcompile = time() - start
print("Compilation time for numba is %s sec" % round(tcompile, 3))

start = time()
cpoly(x)
tnumba = time() - start
print("Execution time for numba is %s sec" % round(tnumba, 3))

# print()
# print("*** Running poly with native python!")
# start = time()
# poly(x)
# tpython = time() - start
# print("Result from python is %s in %s sec" % (y, round(tpython, 3)))


print()
print("*** Speedup summary:")
print("numexpr vs numpy speedup is %s" % (tnumpy / tnumexpr))
print("numba vs numpy speedup is %s" % (tnumpy / (tcompile + tnumba)))
#print("numba vs python speedup is %s" % (tpython / tnumpy))
print()
