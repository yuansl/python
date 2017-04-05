#!/usr/bin/env python

import os, urllib, urllib2, thread, threading, re

reg = re.compile('{"name":"(.+?)",.+?,"rawUrl":"(.+?)",.+?}', re.I)

class downloader(threading.Thread):
        def __init__(self, url, name):
                threading.Thread.__init__(self)
                self.url = url
                self.name = name 
        def run(self):
                urllib.urlretrieve(self.url, self.name) 
threads = []

def main(url):
        resp = urllib.urlopen(url)
        data = resp.read()
        groups = re.finditer(reg, data)
        for g in groups:
                name = g.group(1).strip() + ".mp3"
                path = g.group(2).replace('\\', '')
                t = downloader(path, name)
                threads.append(t)
                t.start()
                
if __name__ == '__main__':
        main("http://site.douban.com/huazhou/")
        for t in threads:
                t.join()

