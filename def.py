#!/usr/bin/python3

import sys

fibs_array = []

def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    if sys.argv.__len__() <= 1:
        print("usage: ", sys.argv[0] + " [n]")
        sys.exit(1)

    n = int(sys.argv[1])
    
    print("n=", n)
    fibs = fib(n)
    print("fib() = ", fibs)
