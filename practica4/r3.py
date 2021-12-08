#!usr/bin/python

import sys
from collections import Counter

peticiones = Counter()
for line in sys.stdin:
    line_clean = line.rstrip("\n")
    if line_clean in peticiones:
        peticiones[line_clean] += 1
    else:
        peticiones[line_clean] = 0

# In python 3.10
# total = peticiones.total()
total = sum(peticiones.values())

for a in peticiones.keys():
    peticiones[a] /= total

print(dict(peticiones))
