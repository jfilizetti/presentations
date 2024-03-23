#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
import numpy as np
import re
import optparse

# parse results file, looking for lines like this
#     90.74%    87.11%     3.63%     9897:cp             
def parse_file(path, axis, title, options):
    with open(path) as f:
        lines = f.readlines()

    data= np.zeros((len(lines), 3), dtype=float)
    commands = []
    count = 0

    for line in lines:
        col = line.strip().split()
        if len(col) < 4:
            continue
        if not re.match('[0-9]+\.[0-9]+%', col[0]):
            continue

        total, system, user = [float(x[:-1]) for x in col[0:3]]
        if total <= 1:
            continue

        command = ' '.join(col[3:])
        i = command.find(':')
        if i != -1:
            command = command[i+1:]

        # skip idle
        if command == 'swapper':
            continue

        data[count] = total, system, user
        commands.append(command[0:12])
        count += 1

    # user time
    user = data[:count,2]
    axis.bar(np.arange(count), user, width=.75, label='User')

    # system time 
    system = data[:count,1]
    axis.bar(np.arange(count), system, bottom=user, width=.75, label='System')

    # total time is wall so subtract user and sys time
    total = data[:count, 0]
    ydata = total - system - user
    ydata[ydata < 0] = 0
    rects = axis.bar(np.arange(count), ydata, bottom=system+user, width=.75, label='Total')
    axis.bar_label(rects, fontsize=8, fmt='%.1f%%', label_type='edge', padding=10)

    axis.set_ylim((0, int(options.ylimit)))
    axis.set_ylabel('CPU Utilization')
#    axis.set_title('Processes over 1% CPU Utilization for local cp of linux kernel source (6.7.2) %s' % (path))
    if title:
        axis.set_title('%s' % title)
    axis.legend()
    axis.set_xticks(np.arange(count), commands, rotation=-45, fontsize=8)

def main():
    parser = optparse.OptionParser()
    parser.add_option('-y', '--ylimit', dest='ylimit', default='100')
    parser.add_option('-t', '--title', dest='title', default=None)
    parser.add_option('-o', '--output', dest='output', default=None)
    parser.add_option('--suptitle', dest='suptitle', default=None)
    options, args = parser.parse_args()

    f = plt.figure(figsize=(16,10))

    rows = 3
    cols = 1
    if len(args) > 4:
        print('Too many items to graph')
    elif len(args) == 4:
        rows = 2
        cols = 2

    i = 1
    titles = []
    if options.title:
        titles = options.title.split(':')

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
        f.suptitle(options.suptitle)
    if options.output:
        plt.savefig('%s' % (options.output))
    plt.show()

if __name__ == '__main__':
    main()
