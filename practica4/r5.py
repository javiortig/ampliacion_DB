#!usr/bin/python

import sys

# With tuple(line.split(' ')) you get the same thing, 
# but you get a '\n' in the second element.
resp_gen = ( (line.split(' ')[1].rstrip('\n'), line.split(' ')[0]) for line in sys.stdin)
resp_set = set(resp_gen)

print(resp_set)