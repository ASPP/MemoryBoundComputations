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

   represents the same polynomial as the original one, but with some
   interesting side-effects in efficiency. Repeat this computation for
   numpy and numexpr and get your own conclusions.

   - Why do you think numpy is more efficient with this form?

   - Why the speed-up in numexpr is not as high in comparison?

   - Why does numexpr continue to be faster than numpy?

3. The Cython program ``poly_cython.pyx`` does the same computation than
   above, but in C.  Execute it via its ``cython-bench.py`` driver::

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

   That is, do a simple copy of the `x` vector.

   - What's the performance that you are seeing?

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
