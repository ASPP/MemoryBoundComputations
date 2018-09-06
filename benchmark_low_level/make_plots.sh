#!/bin/bash
python3 plot.py memory_read_bandwidth.csv memory_write_bandwidth.csv  bw bandwidth.svg
python3 plot.py memory_random_latency.csv memory_seq_latency.csv  test latency.svg
