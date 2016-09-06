#######################################################################
# This script compares the speed of the computation of a polynomial
# using multiple processes (numpy) or threads (numexpr).
#
# Author: Francesc Alted
# Date: 2013-09-04
# Updated: 2016-09-01
#######################################################################

import sys
from time import time
from multiprocessing import Pool
import numpy as np
import numexpr as ne

N = 10 * 1000 * 1000  # number of points to evaluate
x = np.linspace(-10, 10, N)  # vector x in range [-1, 1]

expr = ".25*x**3 + .75*x**2 - 1.5*x - 2"  # 1) the polynomial to compute
#expr = "((.25*x + .75)*x - 1.5)*x - 2"   # 2) a computer-friendly polynomial
#expr = "x"                                # 3) the identity function
#expr = "sin(x)**2+cos(x)**2"             # 4) a transcendental function

# Set here which library you want to use
what = "numpy"  # uses numpy for computations
#what = "numexpr"           # uses numexpr for computations


def compute(x, nt):
    if what == "numpy":
        y = compute_parallel(expr, x, nt)
    else:
        ne.set_num_threads(nt)
        y = ne.evaluate(expr)
    return y


def compute_block(expr_, xp, nt, i):
    x = xp[i * N // nt:(i + 1) * N // nt]
    if "sin" in expr_:
        # Trick to allow numpy evaluate this
        expr_ = "np.sin(x)**2+np.cos(x)**2"
    elif expr_ == "x":
        # Trick to force a copy with numpy
        return x.copy(), nt, i
    y = eval(expr_)
    return y, nt, i


global result
result = np.empty(N, dtype='float64')


def cb(r):
    global result
    # print(r, counter)
    y, nt, i = r  # unpack return code
    result[i * N // nt:(i + 1) * N // nt] = y  # assign the correct chunk


# Parallel computation for numpy via multiprocessing
def compute_parallel(expr_, x, nt):
    global result
    # print("Computing with %d threads in parallel: %s" % (nt, expr_))
    po = Pool(processes=nt)
    for i in range(nt):
        po.apply_async(compute_block, (expr_, x, nt, i), callback=cb)
    po.close()
    po.join()
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please pass the number of threads/processes as an argument")
        sys.exit()
    nthreads = int(sys.argv[1])
    print("Computing: '%s' using %s with %d threads and %d million points" % \
          (expr, what, nthreads, N // 1e6))
    for nt in range(nthreads):
        t0 = time()
        y = compute(x, nt + 1)
        ts = round(time() - t0, 3)
        print("*** Time elapsed for %d threads:" % (nt + 1), ts, "s")
