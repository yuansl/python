#!/usr/bin/python3

import os
import bs4
from urllib.request import urlopen

base_url = 'http://www.debian.org/'

def browser(url):
    html = urlopen(url).read()
    bs = bs4.BeautifulSoup(html)
    imgs = bs.findAll('img')
    img_links = set()
    for img in imgs:
        img_links.add(base_url + img.attrs['src'])

    while img_links.__len__() > 0:
        link = img_links.pop()
        print('link:', link)
        filename = link[link.rindex('/') + 1:]
        print('filename=', filename)
        html = urlopen(link)
        if not os.path.exists(filename):
            fd = open(filename, 'wb')
            fd.write(html.read())
            fd.close()
            
base_url = input('input a url:')
base_url += '/'
browser(base_url)
