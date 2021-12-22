#!usr/bin/python

import sys

counts = {}
total = 0 
# Just like r2
for line in sys.stdin:
    line = line.replace('\n', '')
    if (line in counts):
        counts[line] += 1
    else:
        counts[line] = 1
    total += 1 

# Calculates the percent of each sum
for k in counts:
    counts[k] = str(counts[k]/total * 100) + ' %'    

print(counts)
