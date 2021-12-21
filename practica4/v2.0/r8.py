#!usr/bin/python

import sys
import heapq

res = {}
for line in sys.stdin:
    line = line.replace('\n', '').split()

    if not line[2].isdigit():
        continue

    if not line[0] in res:
        res[line[0]] = dict()


    if line[1] in res[line[0]]:
        res[line[0]][line[1]] += int(line[2])
    else:
        res[line[0]][line[1]] = int(line[2])

for dom in res.items():
    print(f'{dom[0]}: {heapq.nlargest(3, dom[1], key=dom[1].get)}')

print(len(res)) # TODO: diccionario