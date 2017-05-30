#!/usr/bin/python3

class Test:
    local_data = 25

    def __init__(self, data):
        self.local_data = data

if __name__ == '__main__':
    t = Test(35)
    print(t.local_data)
    print(Test.local_data)
