#!usr/bin/python

import sys

res = set()
for line in sys.stdin:
    line = line.replace('\n', '')
    res.add(line)

print(res)

