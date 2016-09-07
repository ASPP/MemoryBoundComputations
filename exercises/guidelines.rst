========================================
Exercises for Memory-Efficient Computing
========================================

Exercising the blocking technique
=================================

0. Take your time to understand the code in script ``cpu_vs_mem.py``
   and then run it.

   - Which is the minimal blocksize that provides fastest performance?

   - What do you think this minimum represents?


Optimizing arithmetic expressions
=================================

1. Use script ``poly.py`` to check how much time it takes to evaluate
   the next polynomial by using numpy (note the `what` parameter)::

    y = .25*x**3 + .75*x**2 - 1.5*x - 2

   with x in the range [-10, 10], and with 10 millions points.

   - Set the `what` parameter to "numexpr" and take note of the
     speed-up versus the "numpy" case.  Why do you think the speed-up
     is so large?

2. The expression below::

    y = ((.25*x + .75)*x - 1.5)*x - 2

   represents the same polynomial than the original one, but with some
   interesting side-effects in efficiency.  Repeat this computation for
   numpy and numexpr and get your own conclusions.

   - Why do you think numpy is doing much more efficiently with this
     new expression?

   - Why the speed-up in numexpr is not so high in comparison?

   - Why numexpr continues to be faster than numpy?

3. The Cython program ``poly_cython.pyx`` does the same computation than
   above, but in C.  Execute it via its driver::

    python cython-bench.py

   - Why do you think Cython is more efficient than the above approaches?

Evaluating transcendental functions
===================================

4. Activate the evaluation of the "sin(x)**2+cos(x)**2" expression in
   poly.py, a function that includes transcendental functions and run
   the script.

   - Why the difference in time between NumPy and Numexpr is so large?

5. Look at the time for the transcendental evaluation in Cython in
   exercise 3 above.

   - Do this Cython approach go faster than the Python-based ones?

   - What would be needed to accelerate the computations? 

Parallelism with threads
========================

6. Be sure that you are on a multi-processor machine and activate the::

    y = ((.25*x + .75)*x - 1.5)*x - 2

   expression in poly-mp.py.  Repeat the computation for both numpy and
   numexpr for a different number of processes (numpy) or threads
   (numexpr) (pass the desired number as a parameter to the script).

   - How the efficiency scales?

   - Why do you think it scales that way?

   - How performance compares with the pure Cython computation?

7. With the previous examples, compute the expression::

    y = x

   That is, do a simple copy of the `x` vector.  What's the
   performance that you are seeing?

   - How does it evolve when using different threads? Why it scales very
     similarly than the polynomial evaluation?

   - Could you have a guess at which is the memory bandwidth of this machine?


Using Numba
===========

The goal of Numba is to compile arbitrarily complex Python code
on-the-flight and executing it for you.  It is fast, although one should
take in account the compile times.

8. Edit poly-numba.py and look at how numba works.

   - Run several expressions and determine which method is faster.  What
     is the compilation time for numba and how it compares with the
     execution time?

   - Raise the amount of data points to 100 millions.  What happens?

   - Set the number of threads for numexpr to 12 and redo the
     computation.  How its speed compares with numba?

   - Set the expression to evaluate to the transcendental one (
     `expr_to_compute = 3`).  How the speeds change?  Why do you think
     numexpr is faster here?

   - Provided this, which do you think is the best scenario for numba?
     Which is the best scenario for numexpr?


Using compressed data containers (in preparation for forthcoming tutorial)
================================

The bcolz package that mainly following NumPy semantics and allowing you
to work with compressed datasets as if they where uncompressed.  The
`query-bcolz.py` script creates a bcolz ctable, a compressed version of an
structured NumPy array, and an actual structured array.  Both are then
queried and the timings are presented.

9. Edit query-bcolz.py and look at how a ctable query works.

   - Why do you think the pure NumPy approach works slower than bcolz?
     Try to improve the NumPy version runtime.  Would you be able to beat
     bcolz performance?  Hint: Use numexpr.evaluate() for the expression.

   - Use different compressors in bcolz ('blosclz', 'lz4' and 'zlib') and
     note the differences between them.  Which one would you use for maximum
     performance?  Which one for dealing with larger tables than available
     memory?  Which one shows a better balance?

   - Deactivate the multithreading in the script.  What's the performance of
     a ctable query, with settings put to maximum performance, with respect to
     an structured array?
