#!usr/bin/python

import sys
from collections import Counter

peticiones = {f'{i:02d}':0 for i in range(24)}
for line in sys.stdin:
    line_sep = line.split(" ")
    peticiones[line_sep[0]] += int(line_sep[1].rstrip("\n"))

print(dict(peticiones))
print("SIN TERMINAR")