#!usr/bin/python

import sys

# gets the line cleaned and splitted
# cat apache.log | python m9.py | sort | python r9_v2_1.py
def validator(line: str) -> list:
    line_splitted = line.strip().split(";")

    if (len(line_splitted) !=9 or (not line_splitted[7].isdigit()) or (not line_splitted[8].isdigit())):
        return []

    return line_splitted

for line in sys.stdin:
    # validate the line
    formated_line = validator(line)

    # Filters get or posts
    if (not formated_line) or (formated_line[4]!="GET" and formated_line[4]!="POST") or formated_line[0] == '' or not formated_line[-1].isdigit():
        continue

    print(f'{formated_line[0]} {formated_line[-1]} {formated_line[4]}')
    