#!/usr/bin/python3

def countdown(n):
    if n <= 0:
        print("Blastoff!")
    else:
        print(n)
        countdown(n-1)

def fibnaci(n):
    if n <= 1:
        return n
    else:
        return fibnaci(n-1) + fibnaci(n-2)

def print_n(s, n):
    if n <= 0:
        return
    else:
        print(s)
        print_n(s, n-1)

def do_n(fn, n):
    for i in range(n):
        fn('hello, world', 3)

countdown(3)
print(fibnaci(5))
s = 'hello'
n = 2
print_n(s, n)

do_n(print_n, 3)
