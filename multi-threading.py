#!/usr/bin/python3

import threading

def foo(args=None):
    print('foo test')

class downloader(threading.Thread):
    def __init__(self, target=None, name='', args=None):
        super().__init__()
        self.name = name
        self.args = args
        self.target = target
        
    def run(self):
        self.target(self.args)

def test(what, ever, postion, argument, args, *, iname=None):

    threads = []
    for i in range(10):
        t = downloader(name=iname, target=foo, args=args)
        threads.append(t)
        t.start()
        print("thread name is: %s" % t.getName())
    
    for t in threads:
        t.join()
    
if __name__ == '__main__':
    test('what','ever','po', 'en', 'he', iname='downloader')
