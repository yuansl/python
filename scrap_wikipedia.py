#!/usr/bin/python3

import os
import bs4
from urllib.request import urlopen
import re

links = set()
base_url = 'http://wikipedia.org/'
def process_page(url):
    global base_url
    html = urlopen(url).read()
    bs = bs4.BeautifulSoup(html, 'lxml')
    print('page:', bs.find('title').text)
    for href in bs.findAll('a', href=re.compile('^/wiki/')):
        if 'href' in href.attrs:
            links.add(base_url + href.attrs['href'])

process_page(base_url + 'wiki')

while links.__len__() > 0:
    link = links.pop()
    process_page(link)

