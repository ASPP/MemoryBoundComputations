==================================================
Exercises for Memory-Efficient Computing (answers)
==================================================

For the solutions of the exercises, you may want to check the
accompanying material:

- `Timings-escher.ods`, a LibreOffice spreadsheet with data and graphs
  for exercises 1 to 6.  This has benchmarks ran on a machine (called
  escher) with 8 physical cores.

Exercise 0
~~~~~~~~~~

N = 1000
A = np.linspace(-1, +1, N**2).reshape(N, N)
%timeit A + A
%timeit A + A.T

The second is slower because of memory access non-locality.


Exercise I: the blocking technique
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Which is the minimal blocksize that provides fastest performance?

Between 10k and 500k is the "sweet spot", but 100k may be the
minimum.

- What do you think this minimum represents?

This figure is close to the size of L2 cache size in modern CPUs
(256 KB).  Apparently L2 is the optimal cache for making this
blocking computation to work best with the Python interpreter.


Exercise II: optimizing arithmetic expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Set the `what` parameter to "numexpr" and take note of the speed-up
  versus the "numpy" case.  Why do you think the speed-up is so large?

Numexpr basically follows the blocking technique as explained above.
The additional speed-up is due to the fact that the virtual machine in
numexpr is implemented at C level, and hence, it is faster than the
above pure-python implementation.

Also, numexpr can do the ``x**3`` --> ``x*x*x`` expansion, avoiding the
expensive `pow()` operation (which is performed in software).

Exercise III: Parallelism with threads and processes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

a. The polynomial

- How the efficiency scales?

Scaling should approximately follow a negative exponential
distribution. However, you will notice that the asymptote is different
from zero. Such an asymptote is basically fixed by the memory bandwidth
of the machine.

- Why do you think it scales that way?

The answer is that you are hitting the memory bandwidth limit in some of
your computations. So, the reason is that the problem becomes
bottle-necked by memory access when you use a large number of threads.

- How performance compares with the pure Cython computation?

We are seeing that numexpr can beat a pure Cython computation. This is
for a good reason: numexpr uses several threads here, while Cython code
does not.  But see below.

b. "memcpy"

- What is the performance that you are seeing?

`y = x` performs pretty similarly to the polynomial::

       y = ((.25*x + .75)*x - 1.5)*x - 2

- Why it scales very similarly than the polynomial evaluation?

The bottleneck is in memory access, no CPU computing time.

- Could you have a guess at the memory bandwidth of this machine?

A rough estimation is that, if saturation point is around 0.01 seconds
for computing an array of size::

   8 * 1e7 ~ 76 MB

then the bandwidth for this is around::

   (76 / .01) ~ 7600 MB/s ~ 7.5 GB/s
