# Memory-bound Problems
**Important**: these are instructor notes, remove this file before showing the materials to the students. The notes can be added after the lecture, of course.

## Introduction

  - [Puzzling issues](puzzling_issues.ipynb) (how swapping two nested for-loops makes out for a &gt;4× slowdown
  - a more thorough benchmark is [here](benchmark_python/) (ignore the blue vertical lines for now)

## A digression in CPU architecture and the memory hierarchy

  - Have a look at the historical evolution of [speeds](speed/) of different components in a computer:
    - the CPU clock rate
    - the memory (RAM) clock rate
    - the memory (RAM) transfer rate
    - some storage media access rates
  - the need for a hierarchical access to data for the CPU should be clear now
  - draw a sketch of the CPU/registers/L1-cache/L2-cache/L3-cache/RAM/Disk/Network hierarchy (something on the lines of [this](https://en.wikipedia.org/wiki/Memory_hierarchy))
  - understand the trade-offs involved (speed, costs, heat dissipation, capacity)
  - try `lstopo` on my machine, talk about temporal and spacial locality of data
  - now go back to the [Python benchmark](benchmark_python/) and interpret the vertical blue lines
  - measure size and timings for the memory hierarchy on my machine with a low level [C benchmark](benchmark_low_level)
  - explain the concepts of [latency](https://en.wikipedia.org/wiki/CAS_latency) (also known as _delay_) and [bandwidth](https://en.wikipedia.org/wiki/Memory_bandwidth) (also known as _speed_ or _throughput_) and their [relationship](http://www.crucial.com/usa/en/memory-performance-speed-latency):
      - `latency ≈ (time-when-data-available-on-output-pins – time-when-data-requested) #measured in ns, depends on clock ticks ⟶ clock_ticks × number-of-ticks-per-operation` 
      - `bandwidth ≈ clock_tick x data-transfer/tick x bus-width`

## Concluding remarks

  - it is difficult to “defeat” the cache and the CPU intelligence (think about registers for [speculative execution](https://en.wikipedia.org/wiki/Speculative_execution) and the latest news about [Spectre and Meltdown](https://meltdownattack.com/) vulnerabilities in modern Intel CPUs)
  - by the way, this is the reason why, for matrix multiplication, the clever [ATLAS](http://math-atlas.sourceforge.net/) or [openBLAS](http://www.openblas.net/) implementations are much faster than your manual C, or Cython or numba implementation ;-)
  - if you use a “proper” `numpy` installation, it is already linked with an optimized [BLAS](http://www.netlib.org/blas/) implementation
  - if there is time, you may want to explain what BLAS, LAPACK, ATLAS, openBLAS is all about, what `numpy` and `scipy` do about it, why life is so much easier in this case in the Linux world

