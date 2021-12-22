#!usr/bin/python

import sys

res = set()
# We use a set so we won't repeat each type
for line in sys.stdin:
    line = line.replace('\n', '')
    res.add(line)

print(res)

