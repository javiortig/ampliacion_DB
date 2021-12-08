#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        line_sep = line.split(";")
        line_traf = line_sep[-1].strip()
        line_time = line_sep[3].split(" ")[-1].split(":")[0]
        if line_time.isnumeric() and line_traf.isnumeric():
            print(f'{line_time} {line_traf}')
    except:
        pass