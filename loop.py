#!/usr/bin/python3

import math

# for loop
for i in range(434):
    if i % 2 == 0:
        print('odd')
    elif i % 4 == 0:
        print('times of 4')
    else:
        pass

# while loop

i = 0
while i < 10:
    print(i, i * math.pi)
    i += 1

