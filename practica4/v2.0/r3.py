#!usr/bin/python

import sys

counts = {}
for line in sys.stdin:
    line = line.replace('\n', '')
    if (line in counts):
        counts[line] += 1
    else:
        counts[line] = 1

total = 0
for v in counts.values():
    total += v

for k in counts:
    counts[k] = str(counts[k]/total * 100) + ' %'    

print(counts)