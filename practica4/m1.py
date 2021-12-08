#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        petition = line.split(";")[4]
        if petition == "GET":
            print(petition, end='\n')
    except:
        pass