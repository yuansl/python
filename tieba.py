#!/usr/bin/python
# coding: utf-8

import urllib
import urllib2
import re

def get_page(url, data):
    try:
        response = urllib2.urlopen(url, data=data)
        return response.read()
    except urllib2.URLError, e:
        print e.reason
        exit()

def main():
    
    regx = re.compile('<div id="post_content_.+?" class=".+?">(.+?)</div>', re.I)
    subregx = re.compile('<img class=.+?>', re.I)
    
    url = 'http://tieba.baidu.com/p/1672347448'
    form = { 'see_lz': 1, 'pn': '%d' }
    data = urllib.urlencode(form)    
    html = get_page(url, data)
    pages = int(re.search('<span class="red">(.+?)</span>', html).group(1))

    with open('linuxbar.txt', 'w') as fd:
        for i in range(1, pages + 1):
            page = get_page(url, data % i)
            groups = re.finditer(regx, page)
            for g in groups:
                line = g.group(1)
                img = re.search(subregx, g.group(1))
                if img is not None:
                    line = g.group(1).replace(img.group(), '\n')
                fd.write(line)
                fd.write('\n')

if __name__ == "__main__":
    main()
