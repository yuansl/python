#!/usr/bin/python
# coding: utf-8
import urllib, urllib2
import re
import threading

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
    request = urllib2.Request(url)
    resp = urllib2.urlopen(request)
    html = resp.read()
    groups = re.finditer(reg, html)
    for i in groups:
        name = i.group(1).strip() + '.mp3'
        url = i.group(2).replace('\\', '')
        thrd = downloader(url, name)
        threads.append(thrd)
        thrd.start()
    
if __name__ == "__main__":
    url = 'http://site.douban.com/huazhou/'
    main(url)
    for t in threads:
        t.join()
