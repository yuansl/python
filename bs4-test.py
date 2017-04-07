#!/usr/bin/python3

import bs4

fd = open('/tmp/index.html.1')
lines = fd.readlines()
fd.close()

shtml = ''
for line in lines:
    shtml += line

soup = bs4.BeautifulSoup(shtml, 'lxml')
print(soup.find('head'))
print(soup.find('title'))
