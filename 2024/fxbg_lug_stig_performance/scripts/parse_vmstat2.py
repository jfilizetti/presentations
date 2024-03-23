#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import numpy as np
import optparse

# parse vmstat -t 1 style output
#procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu----- -----timestamp-----
# r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st                 EST
# 1  0      0 31971728      0 206484    0    0  6584  8320 2222 2943  1 11 88  0  0 2024-03-02 11:44:41
def parse_file(path, axis, title, options):
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

    axis.bar(x, height=y[0], bottom=0, width=1, label='Wait', color='red')
    axis.bar(x, height=y[1], bottom=y[0], width=1, label='User', color='blue')
    axis.bar(x, height=y[2], bottom=y[0]+y[1], width=1, label='System', color='orange')
    axis.bar(x, height=y[3], bottom=y[0]+y[1]+y[2], width=1, label='Stolen', color='yellow')
    axis.bar(x, height=y[4], bottom=y[0]+y[1]+y[2]+y[3], width=1, label='Idle', color='g')
    axis.legend()
    axis.set_xlabel('Seconds')
    axis.set_ylim([0,100])
    axis.set_xlim([0, i])
    if title:
        axis.set_title(title)
    #plt.plot(x, y1, label='User')
    #plt.plot(x, y2, label='System')
    #plt.plot(x, y3, label='Wait')

def main():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--title', dest='title')
    parser.add_option('--suptitle', dest='suptitle', default=None)
    options, args = parser.parse_args()

    titles = []
    if options.title:
        titles = options.title.split(':')

    i = 1
    rows = 3
    cols = 1
    if len(args) > 4:
        print('Too many items to graph')
    elif len(args) == 4:
        rows = 2
        cols = 2

    f = plt.figure(figsize=(16, 10), dpi=100)

    for path in args:
        ax = f.add_subplot(rows, cols, i)
        title = None
        if len(titles) >= i:
            title = titles[i-1]
        parse_file(path, ax, title, options)
        i += 1

    f.tight_layout()
    f.subplots_adjust(bottom=.10, top=.90, hspace=.25)
    if options.suptitle:
        plt.suptitle(options.suptitle)
    plt.legend()
    plt.savefig('vmstat.png')
    plt.show()

if __name__ == '__main__':
    main()
