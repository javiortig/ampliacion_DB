#!usr/bin/python

import sys
import heapq

res = {}
for line in sys.stdin:
    line = line.replace('\n', '').split()

    if not line[1].isdigit():
        continue

    # print(line)
    if line[0] in res:
        res[line[0]] += int(line[1]) * int( 2*(-0.5 + int(line[2]=="GET")) )
    else:
        res[line[0]] = int(line[1]) * int( 2*(-0.5 + int(line[2]=="GET")) )


# No, no hay ninguno con balance negativo, quien se lo hubiera imaginado...
# for a in res.values():
#     if a < 0:
#         print(a)
#         break

print(res)