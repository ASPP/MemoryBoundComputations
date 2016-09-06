# Benchmark to compare the times for evaluating queries.
# Numexpr is needed in order to execute this.

import math
from time import time

import numpy as np
import numexpr as ne

import bcolz


N = int(1e7)  # the number of elements in the tables
clevel = 5  # the compression level
cname = "blosclz"  # the compressor name, blosclz is usually the fastest in Blosc
#cname = "lz4"     # LZ4 is a well balanced compressor
#cname = "zlib"     # you may want to try this compressor classic too
sexpr = "(2*x*x + .3*y*y + z + 1) < 100"  # the query to compute

# Uncomment the next for disabling threading
#ne.set_num_threads(1)
#bcolz.set_nthreads(1)

print("Creating inputs...")

x = np.arange(N)
y = np.linspace(1, 10, N)
z = np.arange(N) * 10

# Build a ctable making use of above arrays as columns
cparams = bcolz.cparams(clevel=clevel, cname=cname)
t = bcolz.ctable((x, y, z, x * 2, y + .5, z // 10),
                 names=['x', 'y', 'z', 'xp', 'yp', 'zp'],
                 cparams=cparams)
# The NumPy structured array version
nt = t[:]

del x, y, z  # we are not going to need these arrays anymore

print("Querying '%s' with 10^%d points" % (sexpr, int(math.log10(N))))

t0 = time()
out = [r for r in nt[eval(sexpr, {'x': nt['x'], 'y': nt['y'], 'z': nt['z']})]]
print("Time for structured array-->  *** %.3fs ***" % (time() - t0,))
#print("out-->", len(out), out[:10])

t0 = time()
cout = [r for r in t.where(sexpr)]
print("Time for ctable--> *** %.3fs ***" % (time() - t0,))
#print("cout-->", len(cout), cout[:10])

print("ctable sizes--> uncompr: %.3f MB, compr: %.3f MB, ratio: %.3f" % (
    t.nbytes / 2.**20, t.cbytes/ 2**20., (t.nbytes / t.cbytes)))
