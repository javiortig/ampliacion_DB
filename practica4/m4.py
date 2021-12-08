#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        line_sep = line.split(";")
        line_fam = line_sep[7].strip()
        if line_fam.isnumeric():
            print(f'{line_sep[4].strip()} {line_fam.strip()[0]}XX')
    except:
        pass