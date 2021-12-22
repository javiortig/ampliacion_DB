#!usr/bin/python

import sys

# Reduces by key (domain) and spits on stdout. Remember the input
# domains should be sorted
last = ''
num = 0
for line in sys.stdin:
    line = line.replace('\n', '').split()

    #checks if we changed domain
    if line[0] != last and last!='':
        print(f'{last} {num}')
        num = int(line[1])
    else:
        num += int(line[1])
    last = line[0]
    
