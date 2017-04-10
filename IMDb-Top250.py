#!/usr/bin/python3

import re
import os
import bs4
from urllib.request import urlopen

base_url = 'https://www.douban.com/doulist/212485/?start='
index = 1
fd = open('IMDb-top250.txt', 'a')

def process_page(url):
    html = urlopen(url).read()
    bs = bs4.BeautifulSoup(html)
    divs = bs.findAll('div', class_=re.compile('(post|title|abstract)'))
    global index
    
    for div in divs:
        if 'post' in div['class']:
            fd.write(str(index) + ": ")            
            fd.write(div.a['href'] + ' ')
            index += 1
        else:
            fd.write(div.text.strip() + '\n')
    fd.write('\n')
    
def download_from_douban():
    global base_url
    for start in range(0, 250, 25):
        url = base_url + str(start) + '&sort=seq&sub_type='
        process_page(url)

download_from_douban()


