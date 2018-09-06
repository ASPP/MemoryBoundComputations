import sys
import numpy as np
import matplotlib
import itertools
from matplotlib import pyplot as plt
plt.style.use('ggplot')
matplotlib.rcParams['font.size'] = 12
fl1 = sys.argv[1]
fl2 = sys.argv[2]
type_ = sys.argv[3]
pic = sys.argv[4]
data1 = np.loadtxt(fl1, delimiter=',')
data2 =  np.loadtxt(fl2, delimiter=',')
#L1 = 64K
#L2 = 512K
#L3 = 3M

labs = ['2K', '4K', '8K', '16K', '32K', '64K', '128K', '256K',
         '512K', '1M', '2M', '4M', '8M', '16M', '32M', '64M', '128M', '256M',
         '512M', '1G']

L1i = 5
L2i = 8
L3i = 10

if type_ == 'bw':
    x1 = np.log2(data1[2:,0])
    x2 = np.log2(data2[2:,0])
    y1 = data1[2:,1]/1024
    y2 = data2[2:,1]/1024
    ylabel = 'bandwidth (GB/s)'
    title = 'Memory Bandwidth'
    legend1, legend2 = 'read', 'write'
else:
    x1 = np.log2(data1[::2,0])[1:]
    x2 = np.log2(data2[::2,0])[1:]
    y1 = data1[::2,1][1:]
    y2 = data2[::2,1][1:]
    ylabel = 'latency (ns)'
    title = 'Memory latency '
    legend1, legend2 = 'random access', 'sequential access'

xlabel='block size'
maxy = max(y1.max(), y2.max())
miny = min(y1.min(), y2.min())

plt.figure(figsize=(8.5,7.5))
p1, = plt.plot(x1, y1, 'o')
plt.xticks(x1, labs)
plt.ylabel(ylabel)
plt.xlabel(xlabel)
p2, = plt.plot(x2, y2, 'o')
plt.xticks(x2, labs, rotation=60)
if type_ != 'bw':
    plt.yticks(range(0, 110, 10))
plt.legend((p1, p2), (legend1, legend2))
# draw caches
# L1
plt.plot((x1[L1i], x1[L1i]), (miny,maxy), color='darkblue', alpha=0.4)
plt.text(x1[L1i-1], (miny+maxy)/2, 'L1\n⟵', color='darkblue', verticalalignment='top')
# L2
plt.plot((x1[L2i], x1[L2i]), (miny,maxy), color='darkblue', alpha=0.4)
plt.text(x1[L2i-1], (miny+maxy)/2, 'L2\n⟵', color='darkblue', verticalalignment='top')
# L3
plt.plot(((x1[L3i]+x1[L3i+1])/2, (x1[L3i]+x1[L3i+1])/2), (miny,maxy), color='darkblue', alpha=0.4)
plt.text(x1[L3i-1]+(x1[L3i]-x1[L3i-1])/2, (miny+maxy)/2, 'L3\n⟵', color='darkblue', verticalalignment='top')
plt.title(title)
plt.savefig(pic)
plt.show()
