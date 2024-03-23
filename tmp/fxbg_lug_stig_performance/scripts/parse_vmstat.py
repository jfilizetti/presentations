#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import optparse

# parse vmstat -t 1 style output
#procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu----- -----timestamp-----
# r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st                 EST
# 1  0      0 31971728      0 206484    0    0  6584  8320 2222 2943  1 11 88  0  0 2024-03-02 11:44:41
def parse_file(path, options):
    with open(path) as f:
        lines = f.readlines()

    i = 0
    x = np.zeros(len(lines), dtype='int')
    y = np.zeros((5, len(lines)), dtype='int')
    for line in lines:
        col = line.strip().split()
        if not col[0].isnumeric():
            continue
        user, system, idle, wait, stolen = [int(x) for x in col[-7:-2]]
        x[i] = i
        y[0, i] = wait
        y[1, i] = user
        y[2, i] = system
        y[3, i] = stolen
        y[4, i] = idle
        i += 1

    plt.figure(figsize=(20, 5), dpi=100)
    plt.bar(x, height=y[0], bottom=0, width=1, label='Wait', color='red')
    plt.bar(x, height=y[1], bottom=y[0], width=1, label='User', color='blue')
    plt.bar(x, height=y[2], bottom=y[0]+y[1], width=1, label='System', color='orange')
    plt.bar(x, height=y[3], bottom=y[0]+y[1]+y[2], width=1, label='Stolen', color='yellow')
    plt.bar(x, height=y[4], bottom=y[0]+y[1]+y[2]+y[3], width=1, label='Idle', color='g')
    plt.xlabel('Seconds')
    plt.ylim([0,100])
    plt.xlim([0, i])
    plt.suptitle('CPU Utilization during 10 sequential copies of kernel source code (6.7.2)')
    if options.title:
        plt.title(options.title)
    #plt.plot(x, y1, label='User')
    #plt.plot(x, y2, label='System')
    #plt.plot(x, y3, label='Wait')
    plt.legend()
    plt.savefig('%s.png' % (path))
    plt.show()

def main():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--title', dest='title')
    options, args = parser.parse_args()
    parse_file(args[0], options)

if __name__ == '__main__':
    main()
