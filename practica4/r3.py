#!usr/bin/python

import sys

groupby_dict = {}
for line in sys.stdin:
    line_clean = line.rstrip("\n")
    if line_clean in groupby_dict.keys():
        groupby_dict[line_clean] = groupby_dict[line_clean]+1
    else:
        groupby_dict[line_clean] = 1

total = sum(groupby_dict.values())
for a in groupby_dict.keys():
    groupby_dict[a] = groupby_dict[a]/total

print(groupby_dict)
