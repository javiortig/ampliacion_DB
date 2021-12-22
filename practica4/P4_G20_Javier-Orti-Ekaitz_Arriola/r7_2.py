#!usr/bin/python

import sys


# Fill a dictionary that will have 4 elements.
# on each iteration it inserts the line input and pops the min of
# the 4 elements, so the top 3 will remain. Then we sort those 3 winners
last = ''
num = 0
domains = dict()
max_domain = 3

for i in range(max_domain):
    domains[f'placeholder_{i}'] = -1

for line in sys.stdin:
    line = line.replace('\n', '').split()
    
    domains[line[0]] = int(line[1])
    domains.pop(min(domains,key=domains.get))


print(sorted(domains.items(), key=lambda x: x[1], reverse=True))