#!/usr/bin/python3
# Run it with /usr/bin/taskset --cpu-list 0 ./bench.py
import os
import sys
import time

# Size of one dimensional numpy arrays of dtype 'float64':
# A fix overhead of 96 bytes plus a variable size:
# (n_items x 8 bytes)
import numpy as np

TS_DB = 'ts_db'

def create_ts(count, length, array):
    if not os.path.isdir(TS_DB):
        os.mkdir(TS_DB)
    for idx in range(count):
        name = f'ts_{idx}_{length}.npy'
        path = os.path.join(TS_DB, name)
        if not os.path.exists(path):
            np.save(path, array)
            os.sync()

def load_ts_bad(count, shape):
    ts = np.empty((*shape, count), dtype='float64')
    for idx in range(count):
        name = f'ts_{idx}_{length}.npy'
        path = os.path.join(TS_DB, name)
        ts[..., idx] = np.load(path)
    return ts

def load_ts_good(count, shape):
    ts = np.empty((count, *shape), dtype='float64')
    for idx in range(count):
        name = f'ts_{idx}_{length}.npy'
        path = os.path.join(TS_DB, name)
        ts[idx, ...] = np.load(path)
    return ts

def timeit(func, *args):
    # run the thing twice to fill the I/O buffer
    func(*args)
    func(*args)
    min_ = np.inf
    for i in range(3):
        start = time.monotonic()
        func(*args)
        min_ = min(min_, time.monotonic()-start)
    return min_

#L1 = 64K   -> 8192  float64 elements
#L2 = 512K  -> 65536 float64 elements
#L3 = 3072K -> 393216 float64 elements
# so an array of 4096K -> 524288 float64 elements is bigger than L3

if __name__ == '__main__':
#    if len(sys.argv) != 3:
#        print('You have to specify count and length', file=sys.stderr)
#        sys.exit(1)
    # let the user confirm that she knows what she is doing
    try:
        input("""===== WARNINGS! =====
- This benchmark must be run with CPU affinity (to force the process to stick on
  a single CPU). In Linux this is achieved by running it with:
      taskset --cpu-list 0 ./bench.py
- When run with default parameters, it will take ~50GB of disk space and kill
  your system if that space is not available. 

You have been warned! Press any key to continue or Control-C to exit
""")
    except KeyboardInterrupt:
        sys.exit(1)

    COUNT=50
    for COUNT in (10, 20, 30, 40, 50):
        POWS = (9, 28) # this is (512B, 256M)

        byte_sizes = 2**np.arange(POWS[0], POWS[1]+1, dtype=int)
        float_items = byte_sizes//8
        labels = []
        for i, floats in enumerate(float_items):
            b = byte_sizes[i]
            if b < 1024:
                labels.append(f'{b}B')
            elif b < 1048576:
                labels.append(f'{b//1024}K')
            elif b < 1073741824:
                labels.append(f'{b//1024//1024}M')
            else:
                labels.append(f'{b//1024//1024//1024}G')
        bads = []
        goods = []
        results = open(f'results_{COUNT}_{float_items[-1]}', 'wt')
        for i, length in enumerate(float_items):
            print('Creating db...')
            shape = (length,)
            array = np.zeros(shape, dtype='float64')
            create_ts(COUNT, length, array)
            # start with the timings
            print('Timing bad...')
            bad = timeit(load_ts_bad, COUNT, shape)
            print('Timing good...')
            good = timeit(load_ts_good, COUNT, shape)
            print(f'{labels[i]} {bad} {good}')
            bads.append(bad)
            goods.append(good)
            results.write(f'{labels[i]} {bad} {good}\n')
            results.flush()
        results.close()

