#!usr/bin/python

import sys

# Receives: Hour byte_traffic

traffic = {i: 0 for i in range(24)}

# Sums traffic
for line in sys.stdin:
    formatted_line = line_splitted = line.strip().split(" ")
    if (len(formatted_line) != 2):
        continue

    traffic[int(formatted_line[0])] += int(formatted_line[1])


#Calculates the increment/decrement of the first hour (exception)
# and then loops for the rest
last_value = traffic[0]
traffic[0] = (traffic[0] - traffic[23])/traffic[0] * 100
for i in range(1, 24):
    temp = traffic[i]
    traffic[i] = (traffic[i] - last_value)/traffic[i] * 100
    last_value = temp

# round for prettier printing
for i in range(0, 24):
    traffic[i] = str(round(traffic[i], 6)) + ' %'

print(traffic)

