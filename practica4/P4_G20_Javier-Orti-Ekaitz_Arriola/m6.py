#!usr/bin/python

import sys
import os
import datetime

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

    date = datetime.datetime.strptime(formated_line[3], "%Y-%m-%d %H:%M:%S")
    
    print(f'{date.hour} {formated_line[8]}')
