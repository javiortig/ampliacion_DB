#!usr/bin/python

import sys
import heapq

res = {}
# TODO: el diccionario final tiene 50K entradas. Asi no se puede hacer
for line in sys.stdin:
    line = line.replace('\n', '').split()

    if not line[1].isdigit():
        continue

    # print(line)
    if line[0] in res:
        res[line[0]] += int(line[1])
    else:
        res[line[0]] = int(line[1])


print(heapq.nlargest(3, res, key=res.get))
print(len(res))
# print(sorted(res, key=res.get, reverse=True)[:3])