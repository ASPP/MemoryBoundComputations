# -*- coding: utf-8 -*-
#######################################################################
# This script compares the speed of the computation of a polynomial
# for different (numpy and numexpr) in-memory paradigms.
#
# Author: Stéfan van der Walt
# Adapted by: Francesc Alted
# Adapted by: Zbigniew Jędrzejewski-Szmek
# Date: 2011-09-01
#######################################################################

import numpy as np
import timeit
import sys

N = 10*1000*1000
x = np.linspace(-10, 10, N)

def raw():
    """Straight-forward NumPy evaluation of polynomial.
    """
    return (((.25 * x) + .75) * x - 1.5) * x - 2

def inplace(block_size=20000):
    """Blocked evaluation of polynomial.
    """
    y = np.empty(len(x))
    for k in range(len(x) // block_size + 1):
        b, e = k * block_size, (k+1) * block_size
        y[b:e] = x[b:e]
        y[b:e] *= .25
        y[b:e] += .75
        y[b:e] *= x[b:e]
        y[b:e] -= 1.5
        y[b:e] *= x[b:e]
        y[b:e] -= 2

    return y

def bench():
    """Illustrate CPU vs memory trade-off.

    Break up a computation in chunks and benchmark. Small blocks fit
    into cache easily, but the NumPy overhead and the outer Python
    for-loop takes longer to execute.  With large blocks, the overhead
    for NumPy and the for-loop is negligible, but the blocks no longer
    fit into cache, resulting in delays.

    Returns
    -------
    block_sizes : list
        Size of the different data chunks.
    times : list
        Execution times.

    """
    times = []
    blocks = np.round(np.logspace(3, 7, num=50)).astype(int)
    for b in blocks:
        t = timeit.timeit(f'cpu_vs_mem.inplace(block_size={b})',
                          'import cpu_vs_mem',
                          number=1)
        times.append(t)
        print(f'Block size: {b}  Execution time: {times[-1]:.3f} s')
        sys.stdout.flush()

    return blocks, times


if __name__ == "__main__":

    # NumPy raw computation
    time = timeit.timeit('cpu_vs_mem.raw()', 'import cpu_vs_mem', number=1)
    print(f'Execution time for raw NumPy calculation: {time:.2f}')

    # NumPy blocked computation
    blocks, times = bench()
    try:
        import matplotlib.pyplot as plt
        plt.figure(facecolor="white")
        plt.semilogx(blocks, times, 'o-')
        plt.xlabel('Block size [b]')
        plt.ylabel('Execution time [s]')
        plt.ylim([0., None])
        plt.title('CPU vs Memory Benchmark')
        plt.show()
    except ImportError:
        pass
