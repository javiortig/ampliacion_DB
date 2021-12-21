#!usr/bin/python

import sys
import os

# cat apache.log | python m8.py | sort | python r8_v2_1.py

# gets the line cleaned and splitted
def validator(line: str) -> list:
    line_splitted = line.strip().split(";")

    if (len(line_splitted) !=9 or (not line_splitted[7].isdigit()) or (not line_splitted[8].isdigit())):
        return []

    return line_splitted

for line in sys.stdin:
    # validate the line
    formated_line = validator(line)
    if (not formated_line):
        continue
    
    _, extension = os.path.splitext(formated_line[5])
    if extension == '':
        extension = "null"
    print(f'{formated_line[0]} {extension} {formated_line[-1]}')