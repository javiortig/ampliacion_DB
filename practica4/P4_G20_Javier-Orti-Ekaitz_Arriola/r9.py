#!usr/bin/python

import sys

actual_dom = '---'
balance = 0

for line in sys.stdin:
    line = line.replace('\n', '').split()

    if not line[1].isdigit():
        continue

    # Domain changed, print balance of last domain calculated
    if (actual_dom != line[0]):
        print(f'{actual_dom} {balance}')
        actual_dom = line[0]
        balance = 0
    # Count balance on the actual domain
    else:
        if (line[2] == 'GET'):
            balance += int(line[1])

        elif (line[2] == 'POST'):
            balance -= int(line[1])

