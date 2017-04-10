#!/usr/bin/python3

class stack():
    def __init__(self):
        self.slots = list()
        
    def push(self, ele):
        self.slots.append(ele)
        
    def top(self):
        return self.slots[-1]

    def rtop(self):
        return self.slots[0]
    
    def pop(self):
        tmp = self.top()
        self.slots.pop()
        return tmp

    def rpop(self):
        tmp = self.rtop()
        self.slots.pop(0)
        return tmp

    def empty(self):
        return self.slots.__len__() == 0

class queue():
    def __init__(self):
        self.slots = list()
        
    def enque(self, ele):
        self.slots.append(ele)
        
    def deque(self):
        tmp = self.slots[0]
        self.slots.pop(0)
        return tmp
    def empty(self):
        return self.slots.__len__() == 0

def test(s):
    while not (s.empty()):
        tmp = s.rtop()
        print(tmp,end='')
        s.rpop()

    print()

def calculator(expression):
    result_set = stack()
    symbol_set = queue()

    while expression.__len__() > 0:
        
        if c.isdigit():
            i = 0
            while c[i].is
            result_set.push(c)
            while not (symbol_set.empty()):
                symbol = symbol_set.deque()
                result_set.push(symbol)
                
        elif not c.isspace():
            symbol_set.enque(c)
            last_symbol = result_set.top()
            if (c == '*' or c == '/') and (last_symbol == '+' or last_symbol == '-'):
                symbol_set.enque(last_symbol)
                result_set.pop()

    result = stack()
    while not (result_set.empty()):
        c = result_set.rpop()
        print(c)
        if c.isalnum():
            result.push(c)
        else:
            if c == '+':
                b = int(result.pop())
                a = int(result.pop())
                sum = a + b
                result.push(sum)
                
            elif c == '-':
                b = int(result.pop())
                a = int(result.pop())
                sum = a - b
                result.push(sum)
            elif c == '*':
                b = int(result.pop())
                a = int(result.pop())
                sum = a * b
                result.push(sum)

            elif c == '/':
                b = int(result.pop())
                a = int(result.pop())
                sum = a / b
                result.push(sum)
            else:
                pass
    return sum
while True:
    expression=input('input express:')
    sum = calculator(expression)
    print('sum of expression', expression, '=', sum)
