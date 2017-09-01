========================================
Exercises for Memory-Efficient Computing
========================================

0. Add A + A, and A + A' (A transposed), compare times. Which one
   is faster, why are they different?

I. Exercising the blocking technique
====================================

Take your time to understand the code in script ``cpu_vs_mem.py`` and
then run it.

   - Which is the minimal blocksize that provides fastest performance?

   - What do you think this minimum represents?


II. Optimizing arithmetic expressions
=====================================

a. Use script ``poly.py`` to check how much time it takes to evaluate
   the next polynomial by using numpy (note the `what` parameter)::

    y = .25*x**3 + .75*x**2 - 1.5*x - 2

   with x in the range [-10, 10], and with 10 millions points.

   - Set the `what` parameter to "numexpr" and take note of the
     speed-up versus the "numpy" case.  Why do you think the speed-up
     is so large?

b. The expression below::

    y = ((.25*x + .75)*x - 1.5)*x - 2

   represents the same polynomial as the original one, but with some
   interesting side-effects in efficiency. Repeat this computation for
   numpy and numexpr and get your own conclusions.

   - Why do you think numpy is more efficient with this form?

   - Why the speed-up in numexpr is not as high in comparison?

   - Why does numexpr continue to be faster than numpy?

c. The Cython program ``poly_cython.pyx`` does the same computation than
   above, but in C.  Execute it via its ``cython-bench.py`` driver::

    python cython-bench.py

   - Why do you think Cython is more efficient than the above approaches?

d. Activate the evaluation of the "sin(x)**2+cos(x)**2" expression in
   poly.py, a function that includes transcendental functions and run
   the script.

   - Why the difference in time between NumPy and Numexpr is so large?

e. Look at the time for the transcendental evaluation in Cython in
   exercise 3 above.

   - Do this Cython approach go faster than the Python-based ones?

   - What would be needed to accelerate the computations? 

III. Parallelism with threads
=============================

a. Activate the::

    y = ((.25*x + .75)*x - 1.5)*x - 2

   expression in poly-mp.py.  Repeat the computation for both numpy and
   numexpr for a different number of processes (numpy) or threads
   (numexpr) (pass the desired number as a parameter to the script).

   - How the efficiency scales?

   - Why do you think it scales that way?

   - How performance compares with the pure Cython computation?

b. With the previous examples, compute the expression::

    y = x

   That is, do a simple copy of the `x` vector.

   - What's the performance that you are seeing?

   - How does it evolve when using different threads? Why it scales very
     similarly than the polynomial evaluation?

   - Could you have a guess at which is the memory bandwidth of this machine?
