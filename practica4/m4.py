#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        line_sep = line.split(";")
        line_fam = line_sep[7]
        if line_fam.isnumeric():
            print(f'{line_sep[4]} {line_fam[0]}XX')
    except:
        pass