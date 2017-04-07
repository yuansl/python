#!/usr/bin/python3

from urllib.request import urlopen
import bs4
import os

if os.path.exists('index.html'):
    fd = open('index.html')
    html = fd.readlines()
    fd.close()
else:
    html = urlopen('http://wikipedia.org').read()
    fd = open('index.html', 'w')
    fd.write(html.decode('utf-8'))
    fd.close()

file_not_exists = False
if os.path.exists('wiki-lists.txt') == False:
    fd = open('wiki-lists.txt', 'w')
    file_not_exists = True
else:
    fd = open('wiki-lists.txt')

links = set()

document = bs4.BeautifulSoup(html)
hrefs = document.findAll('a')
for tag in hrefs:
    if 'href' in tag.attrs:
        if file_not_exists:
            fd.write(tag.attrs['href'])
            fd.write('\n')            
        links.add(tag.attrs['href'])

fd.close()

print(links)
