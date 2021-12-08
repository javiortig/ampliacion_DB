#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        print(line.split(";")[4])
    except:
        pass