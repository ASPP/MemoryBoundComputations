#######################################################################
# This script compares the speed of the computation of a polynomial
# for different in-memory libraries: numpy and numexpr.  Always using
# a single thread here.
#
# Author: Francesc Alted
# Date: 2013-09-04
#######################################################################

from time import time
from numpy import linspace, sin, cos
import numexpr as ne

N = 10*1000*1000            # the number of points to compute expression
x = linspace(-10, 10, N)   # the x in range [-1, 1]

expr = ".25*x**3 + .75*x**2 - 1.5*x - 2"  # 1) the polynomial to compute
#expr = "((.25*x + .75)*x - 1.5)*x - 2"   # 2) a computer-friendly polynomial
#expr = "x"                                # 3) the identity function
#expr = "sin(x)**2+cos(x)**2"             # 4) a transcendental function

what = "numpy"              # uses numpy for computations
#what = "numexpr"           # uses numexpr for computations

ne.set_num_threads(1)  # the number of threads for numexpr computations


def compute():
    """Compute the polynomial with `nt` threads."""
    global expr
    if what == "numpy":
        if expr == "x":
            # Trick to force a copy with NumPy
            y = x.copy()
        y = eval(expr)
    else:
        y = ne.evaluate(expr)
    return y

if __name__ == '__main__':
    print(f'Computing: {expr} using {what} with {N} points')
    t0 = time()
    result = compute()
    ts = time() - t0
    print(f'*** Time elapsed: {ts:.3f} s')
