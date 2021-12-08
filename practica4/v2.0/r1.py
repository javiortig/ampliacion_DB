#!usr/bin/python

import sys

#print(len(sys.stdin.readlines())) No usar esto porque tmb crea array gigant
k = 0
for line in sys.stdin:
    k += 1

print(k)