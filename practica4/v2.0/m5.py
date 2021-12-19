#!usr/bin/python

import sys
import os
import datetime

# The hour we want to scan
input_hour = 22

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

    if (formated_line[7] == '404'):
        date = datetime.datetime.strptime(formated_line[3], "%Y-%m-%d %H:%M:%S")
        name, extension = os.path.splitext(formated_line[5])
        
        # Check if belongs to same hour as given in input:
        if(date.hour == input_hour):
            print(f'{extension}')
