#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        line_sep = line.split(";")
        line_fam = line_sep[7]
        line_extension = line_sep[5].split(".")[-1]
        if line_fam == "404" and line_extension.isalnum():
            print(f'{line_sep[3].split(" ")[1]} {line_extension}')
    except:
        pass