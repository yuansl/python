#!/usr/bin/python
# coding: utf-8

import urllib
import urllib2
import re
import threading


class downloader(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name

    def run(self):
        urllib.urlretrieve(self.url, self.name)

threads = []

url = 'http://www.zhihu.com/question/19857451/answer/19064788'
regx = re.compile('data-original="(.+?)".*?>(.+?)</noscript>', re.I)
response = urllib2.urlopen(url)
html = response.read()
pics = re.finditer(regx, html)
