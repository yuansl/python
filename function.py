#!/usr/bin/python3
# fn = fn-1+fn-2

def how_much(n):
    print('how_much:', n)

def repeat_lyrics(func):
    func('repeat_lyrics')

def fibnaci(n):
    if n <= 1:
        return n
    else:
        return fibnaci(n-1) + fibnaci(n-2)

def print_twice(tw):
    print(tw)
    print(tw)

def right_justify(s):
    remind_space = 70 - len(s)
    i = 0
    while i < remind_space:
        print(' ', end='')
        i += 1
    print(s)

def print_spam(s):
    print(s)
    
def do_twice(functor, s):
    functor(s)
    functor(s)

def do_four(functor, s):
    do_twice(print_spam, s)
    do_twice(print_spam, s)

def draw_squre():
    row = 0
    while row <= 10:
        if row % 5 == 0:
            print('+', end='')
        else:
            print('|', end='')
        col = 1
        while col <= 10:
            if row % 5 == 0:
                if col % 5 == 0:
                    print('+', end='')
                else:
                    print('-', end='')
            else:
                if col % 5 == 0:
                    print('|', end='')
                else:
                    print(' ', end='')
                    
            col += 1
        print()
        row += 1
    
def main(n):
    print('fibnaci %d = ' % n, fibnaci(n))

    repeat_lyrics(how_much)
    print_twice(34)
    print_twice('twice')
    print_twice((3, 43, 43,3))
    print_twice([34, 3, 43, 2, 4])
    print_twice('d')
    functor = print_twice
    functor('functor')
    right_justify('fuck you and fuck your sister and you')
    right_justify('monty')
    do_four(do_twice, 'spam')
    draw_squre()

if __name__ == '__main__':
    n = input('input a number:')
    main(int(n))
