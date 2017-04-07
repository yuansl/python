#!/usr/bin/python

import simplepackages.simple as sim

class Simth():
    x = 21
    
    def __init__(self):
        self.x = 3
        self.y = 4
        self.xarray = ['This', 'is', 'just', 'a', 'Test']
    def show(self):
        print(self.x)
    def loop(self):
        for i in range(5):
            if i % 2 == 0:
                print("%s" % self.xarray[i])
            elif i % 3 == 0:
                print('what')
            else:
                print('hello world')

def test():
    with open('infile1.txt', 'r') as infile, open('outfile1.txt', 'w') as outfile:
        for line in infile:
            line = line.upper()
            print line,
            outfile.write(line)
    infile.close()
    outfile.close()


if __name__ == '__main__':

    sim.test1()
    Simth().show()
    simth = Simth()
    simth.loop()
