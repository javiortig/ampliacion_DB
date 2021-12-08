#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        if line.split(";")[4] == "GET":
            print(line, end='')
    except:
        pass
