#!usr/bin/python

import sys

for line in sys.stdin:
    try:
        line_sep = line.split(";")
        line_fam = line_sep[7]
        line_file_sep = line_sep[5].split(".")
        line_extension = line_file_sep[-1]
        # pa que comprobar si len(line_file_sep)>1 si ya esta el try
        if line_fam == "404" and line_extension.isalnum() and line_extension == line_file_sep[2]:
            print(f'{line_sep[3].split(" ")[-1]} {line_extension.strip()}')
    except:
        pass