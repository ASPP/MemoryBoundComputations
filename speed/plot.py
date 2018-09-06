import sys
import numpy as np
import pandas
import matplotlib
import itertools
from matplotlib import pyplot as plt
plt.style.use('ggplot')
matplotlib.rcParams['font.size'] = 12

for fl in ('cpu_frequency.csv', 'memory_reduced.csv', 'storage_reduced.csv'):
    if fl == 'cpu_frequency.csv':
        plt.figure(figsize=(8.5,7.5))
        data = np.loadtxt(fl, delimiter=',', skiprows=1)

        plt.semilogy(data[:, 0], data[:, 1], 'o')
        # my laptop here
        plt.semilogy([2015], [2300], 'o', color='darkblue')
        plt.grid(None)
        plt.grid(which='both', axis='y')
        plt.ylim(0.4, 10000)
        plt.xlim(1970, 2017)
        years = (1970, 1980, 1990, 2000, 2010, 2015)
        plt.xticks(years, years)
        plt.yticks([1,10,100,1000, 10000], ['1 MHz\n1 µs', '10 MHz\n100 ns',
            '100 MHz\n10 ns', '1 GHz\n1 ns', '10 GHz\n0.1 ns'])
        plt.title('CPU clock rate')
        plt.xlabel('year')
        plt.savefig('cpu_frequency.svg')
    elif fl == 'memory_reduced.csv':
        plt.figure(figsize=(8.5,7.5))
        data = pandas.read_csv(fl)
        data = data.sort_values('Memory clock (MHz)')
        freqs = list(data['Memory clock (MHz)'])
        labels = list(data['Chip type'])
        xloc = range(len(freqs))[::4]
        plt.semilogy(range(len(freqs)), freqs, 'o')
        # my memory here
        plt.semilogy(xloc[-1], [1600], 'o', color='darkblue')
        plt.grid(None)
        plt.grid(which='both', axis='y')
        plt.ylim(9, 3000)
        plt.yticks([10,100,1000], ['10 MHz\n100 ns', '100 MHz\n10 ns', '1 GHz\n1 ns'])
        plt.xticks(xloc, labels[::4], rotation=30, ha='right')
        plt.title('RAM clock rate')
        plt.savefig('memory_reduced_clock.svg')
        plt.figure(figsize=(8.5,7.5))
        data = data.sort_values(' Transfer rate (GB/s)')
        speed = list(data[' Transfer rate (GB/s)'])
        plt.semilogy(range(len(freqs)), speed, 'o')
        # my memory here
        plt.semilogy(xloc[-1], [25.6], 'o', color='darkblue')
        plt.grid(None)
        plt.grid(which='both', axis='y')
        plt.ylim(0.05, 101)
        plt.yticks([0.1,1,10, 100], ['100 MB/s', '1 GB/s', '10 GB/s', '100 GB/s'])
        plt.xticks(xloc, labels[::4], rotation=30, ha='right')
        plt.title('RAM Transfer rate')
        plt.savefig('memory_reduced_transfer_rate.svg')
    elif fl == 'storage_reduced.csv':
        plt.figure(figsize=(8.5,9.5))
        data = pandas.read_csv(fl)
        speed = list(data['Speed (MB/s)'])
        labels = list(data['Type'])
        xloc = range(len(speed))
        #xloc = range(len(freqs))[::4]
        plt.semilogy(range(len(speed)), speed, 'o')
        # my memory here
        plt.semilogy(xloc[-5], [300], 'o', color='darkblue')
        plt.grid(None)
        plt.grid(which='both', axis='y')
        plt.ylim(0.05, 4500)
        plt.yticks([0.1,1,10,100,1000], ['100 KB/s', '1 MB/s', '10 MB/s', '100 MB/s', '1 GB/s'])
        plt.xticks(xloc[::1], labels[::1], rotation=45, ha='right')
        plt.title('Storage speed')
        plt.savefig('storage_reduced.svg')

plt.show()
