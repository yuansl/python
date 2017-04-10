#!/usr/bin/python3

def sumall(*args):
    sum = 0
    for arg in args:
        sum += arg
    return sum

print('sum:', sumall(3, 4, 5,-1))

s = 'abc'
l = [1, 2, 3]
nl = []
d = {}
for pair in zip(s, l):
    nl.append(pair)
    d[pair[0]] = pair[1]
    print(pair)

print('new list=', nl)
print('new dict=', d)
