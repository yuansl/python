#!/usr/bin/python3

def printall(*args, **kargs):
    """printall: print the arguments"""
    print(args)
    print(kargs)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def show(self):
        print('x=', self.x, 'y=', self.y)
        

d = {3:4, 6:'what', '8':'what'}

#printall((3, 4, 5), d)

d = dict(x=1,y=2)
point = Point(**d)
point.show()

Point.show(point)
