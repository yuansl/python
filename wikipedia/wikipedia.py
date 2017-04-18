#!/usr/bin/python3

import requests
import re
import wiki_db
from bs4 import BeautifulSoup

entry = wiki_db.wiki_db()
def get_links(wiki_entry):
    resp = requests.get('https://en.wikipedia.org' + wiki_entry)
    bsobj = BeautifulSoup(resp.text, 'lxml')
    links = bsobj.findAll('a', href=re.compile('^/wiki/((?!:).)*$'))
    for link in links:
        if entry.db_fetch(link['href']) is None:
            print('link:' + link['href'])
            entry.db_store(link['title'], link['href'])
            get_links(link['href'])
            
if __name__ == '__main__':
    get_links("")
