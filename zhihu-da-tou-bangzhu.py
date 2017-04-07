#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import threading

class download(threading.Thread):
    def __init__(self, url, name):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name

    def run(self):
        urllib.urlretrieve(self.url, self.name)

threads = []
folders = []
            
def main(url):
    title_regx = re.compile('<title>(.+?)</title>')
    edu_regx = re.compile('<span class="education item".+? data-topicid=".+?">(.+?)</a></span>', re.I)
    answer_regx = re.compile('<a class="question_link" href="(.+?)">(.+?)</a>', re.I)
    question_url = 'http://www.zhihu.com'
    response = urllib2.urlopen(url)
    html = response.read()
    title = re.search(title_regx, html)
    print 'Title:', title.group(1)
    edu = re.search(edu_regx, html)
    print 'Education:', edu.group(1)
    answers = re.finditer(answer_regx, html)
    for answer in answers:
        answer_url = question_url + answer.group(1)
        name = answer.group(2).strip() + '.txt'
        folders.append(name)
        thrd = download(answer_url, name)
        threads.append(thrd)
        thrd.start()
        print answer.group(2) + ':' + answer_url

if __name__ == "__main__":
    url = 'http://www.zhihu.com/people/da-tou-bang-zhu/answers'
    main(url)
    for t in threads:
        t.join()
    for filename in folders:
        with open(filename, 'w+') as fd:
            buff = fd.read(8192)
            
