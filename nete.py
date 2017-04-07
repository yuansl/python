#!/usr/bin/python3

def ask_ok(prompt, retries=4, complaint='yes or no, please!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'Y', 'yes', 'Yes'):
            return True
        if ok in ('n', 'N', 'no', 'No'):
            return False
        retries = retries - 1
        if retries < 0:
            raise OSError('uncooperative user!!!')
        print(complaint)

def foo(a, L=[]):
    L.append(a)
    return L

def bar():
    pass

def parrot(voltage, state='a stiff', action='voom', type='Norwegain Blue'):
    print('-- This parrot would not', action, end=' ')
    print('if you put', voltage, 'volts through it.')
    print('-- It is', state, '!')

class ClassTest(object):
    """I hate you"""
    def __init__(self):
        self.mlist = []

    def print_mlist(self):
        for i in range(10):
            self.mlist.append(i)
        print(self.mlist[:])

if __name__ == '__main__':
    #reply = ask_ok('Do you really want to quit ? ')
    #if reply:
        #print('Thank you.')
        
    #for i in range(20):
        #print(foo(i))
    myclass = ClassTest()
    myclass.print_mlist()

