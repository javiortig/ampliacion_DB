#!usr/bin/python

import sys

counts = {}
for line in sys.stdin:
    line = line.replace('\n', '')
    if (line in counts):
        counts[line] += 1
    else:
        counts[line] = 1


print(counts)