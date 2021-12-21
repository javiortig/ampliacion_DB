#!usr/bin/python

import sys
import heapq

#_maxlen = -1

traffic_dict = {}
actual_dom = '---'
max_files = 3

for line in sys.stdin:
    line = line.replace('\n', '').split()

    if not line[2].isdigit():
        continue

    # Changing domain
    if (actual_dom != line[0]):
        #_maxlen = max([len(traffic_dict), _maxlen]) # Solo para comprobar si crecia mucho(no)

        print(f'From \'{actual_dom}\':')
        i = 0
        for key in sorted(traffic_dict, key=traffic_dict.get, reverse=True):
            if (i >=max_files):
                break

            print(f'    {key} {traffic_dict[key]}')
            i += 1

        print('\n')

        actual_dom = line[0]
        traffic_dict = {}
    # Same domain, adding files
    else:
        # Check if already exists to add 
        if (line[1] not in traffic_dict):
            traffic_dict[line[1]] = 0
        else:
            traffic_dict[line[1]] += int(line[2])


#print(_maxlen)