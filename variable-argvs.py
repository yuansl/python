#!/usr/bin/python3

def printall(*args):
    print(args)
    
printall(1, 2.0, '3')

s = 'abc'
t = [1, 2, 3]
for pair in zip(s, t):
    print(pair)

l = list(zip(s, t))
print(l)



