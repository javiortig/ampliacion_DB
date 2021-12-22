#!usr/bin/python

import sys

# Remember to sort after
# cat apache.log | python m7.py | sort | python r7.py | python r7_2.py

# gets the line cleaned and splitted
def validator(line: str) -> list:
    line_splitted = line.strip().split(";")

    if (len(line_splitted) !=9 or (not line_splitted[7].isdigit()) or (not line_splitted[8].isdigit())):
        return []

    return line_splitted

for line in sys.stdin:
    # validate the line
    formated_line = validator(line)
    if (not formated_line) or formated_line[0] == '' or not formated_line[-1].isdigit():
        continue

    print(f'{formated_line[0]} {formated_line[-1]}')
    