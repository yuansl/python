#!/usr/bin/python

class A(object):
    def __init__(self):
        self.data = [11, 22, 3]
        self.idx = 0
    def __iter__(self):
        return self
    def next(self):
        if self.idx < len(self.data):
            x = self.data[self.idx]
            self.idx += 1
            return x
        else:
            raise StopIteration

class A_:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.list = []

    def next(self):
        return self.list.pop()

    def add(self, val):
        self.list.append(val)

class B:
    def __init__(self):
        self.data = [4, 5, 6]
        self.idx = 0
    def __iter__(self):
        return self

    def next(self):
        if self.idx < len(self.data):
            x = self.data[self.idx]
            self.idx += 1
            return x
        else:
            raise StopIteration
        

def a_test(max = 5, *keys, **keyarguments):
    a = A()
    b = B()
    print 'max = %d' % max
    print keys
    print keyarguments
    for x in a:
        print x
    for x in b:
        print x

def recursive(alist):
    if len(alist) == 0:
        return 0
    return alist.pop() + recursive(alist)

def main():
    a_test(3, 'a', 'b', 'c', I = 'Iloveyou')
    sum = recursive([2, 3, 4])
    print sum
    
    a = A_()
    a.add(32)
    a.add(43)
    a.add(54)
    a.add(62)
    print(a.next())

if __name__ == '__main__':
    main()

