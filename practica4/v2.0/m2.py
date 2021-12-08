#!usr/bin/python

import sys


# Nota para Ekaitz: hacerlo por error no sirve ya que si por ejemplo hay una linea
# Con columnas de mas pero con el formato bien la aceptará 
# No estoy seguro pero creo que hay que revisar todos los errores en todos los ejercicios

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

    