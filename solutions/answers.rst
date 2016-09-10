==================================================
Exercises for Memory-Efficient Computing (answers)
==================================================

For the solutions of the exercises, you may want to check the
accompanying material:

  - `Timings-escher.ods`, a LibreOffice spreadsheet with data and
    graphs for exercises 1 to 6.  This has benchmarks ran on a machine
    (called escher) with 8 physical cores.


Exercising the blocking technique
=================================

Exercise 0
~~~~~~~~~~

   - Which is the minimal blocksize that provides fastest performance?

It is around 100 KB.

   - What do you think this minimum represents?

This figure is close to the size of L2 cache size in modern CPUs
(256 KB).  Apparently L2 is the optimal cache for making this
blocking computation to work best with the Python interpreter.

Optimizing arithmetic expressions
=================================

Exercise 1
~~~~~~~~~~

- Set the `what` parameter to "numexpr" and take note of the speed-up
  versus the "numpy" case.  Why do you think the speed-up is so large?

Numexpr basically follows the blocking technique as explained above.
The additional speed-up is due to the fact that the virtual machine in
numexpr is implemented at C level, and hence, it is faster than the
above pure-python implementation.

Also, numexpr can do the ``x**3`` --> ``x*x*x`` expansion, avoiding the
expensive `pow()` operation (which is performed in software).

Exercise 2
~~~~~~~~~~

- Why do you think numpy is doing much more efficient with this new
  expression?

Because the `pow()` is computationally very expensive, and we removed it.

Note that NumPy cannot expand `pow()` too much as it would create too
much (*big*) temporaries. As Numexpr temporaries are much smaller
(fits in cache), it can expand pow() much more cheaply.

- Why the speed-up in numexpr is not so high in comparison?

The virtual machine of numexpr already made the `x**3 -> x*x*x` expansion
automatically, although the factorized version contains less temporaries, so
this is why we can still get a bit more of performance.

- Why numexpr continues to be faster than numpy?

In this case, basically just because numexpr uses the blocking
technique. Hence, this is a pretty much fair comparison on how much
this technique can do for your computations.

Exercise 3
~~~~~~~~~~

- Why do you think it is more efficient than the above approaches?

The reason is two-folded. In one hand, C code only needs atomic
temporaries that are kept in registers in CPU, as computation is done
element-by-element, so no blocking technique is really needed here.
Also, C-code does not have numexpr's virtual machine overhead,
resulting in the fastest implementation.

Evaluating transcendental functions
===================================

Exercise 4
~~~~~~~~~~

- Why the difference in time between NumPy and Numexpr is so small?

Because in this case the bottleneck is mainly the CPU, not memory, so numexpr
(using 1 single thread) cannot offer too much speed-up (but still, there is
some).

Exercise 5
~~~~~~~~~~

- Do this pure C approach go faster than the Python-based ones?

Not very much because of the same reason than above: the bottleneck is
the same than above, the CPU.

- What would be needed to accelerate the computations?

As this is a CPU-bounded calculation, using several cores would probably
help.

Parallelism with threads
========================

Exercise 6
~~~~~~~~~~

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

Exercise 7
~~~~~~~~~~

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


Using Numba
===========

Exercise 8
~~~~~~~~~~

- Run several expressions and determine which method is faster.  What is
  the compilation time for numba and how it compares with the execution
  time?

  In most machines is between 0.3s and 0.5s (depends on the hardware).
  In this case, it is pretty close to the time that it takes the run,
  and that overhead should be taken in account when evaluating speedups.

- Raise the amount of data points to 100 millions.  What happens?

  The execution time scales linearly, while the compilation remains the
  same, so the compilation time is much less overhead compared to the
  run time.

- Set the number of threads for numexpr to 12 and redo the computation.
  How its speed compares with numba?

  numexpr clearly wins numba in this case (specially when evaluating the
  expression with transcendental functions).

- Set the expression to evaluate to the transcendental one
  (`expr_to_compute = 3`).  How the speeds change?  Why do you think
  numexpr is faster here?

  numexpr is much faster here because it uses multithreading by
  default, but with numba you need to program multi-threaded operation
  explicitly.

- Provided this, which do you think is the best scenario for numba?
  Which is the best scenario for numexpr?

  numba adapts very well to scenarios where you want to accelerate
  generic python code, and specially the ones that are not easy to
  vectorize.

  numexpr adapts better for the cases where you want to get rid of the
  relatively high compilation times of numba, but also when dealing
  with either memory-bounded and CPU-bounded problems because it
  supports efficient multi-threading and also Intel MKL.
