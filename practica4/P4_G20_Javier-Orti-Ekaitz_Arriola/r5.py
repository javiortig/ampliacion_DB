#!usr/bin/python

import sys

# Just like r4
res = set()
for line in sys.stdin:
    line = line.replace('\n', '')
    res.add(line)

print(res)

