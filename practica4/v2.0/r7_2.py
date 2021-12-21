#!usr/bin/python

import sys

last = ''
num = 0
domains = dict()
max_domain = 3
for i in range(max_domain):
    domains[f'placeholder_{i}'] = -1

for line in sys.stdin:
    line = line.replace('\n', '').split()
    
    # Esto es lento como sup-
    # domains[line[0]] = line[1]
    # # se que >3, pero si uso not se queda un corason <3
    # if not len(domains) <3:
    #     domains.pop(min(domains,key=domains.get))

    domains[line[0]] = int(line[1])
    domains.pop(min(domains,key=domains.get))


print(sorted(domains.items(), key=lambda x: x[1], reverse=True))

# print(len(domains))