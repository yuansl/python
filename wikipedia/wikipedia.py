#!/usr/bin/python3

import requests
import re
import wiki_db
from bs4 import BeautifulSoup

base_url = 'https://en.wikipedia.org'
looked_entries = set()
def get_links(wiki_entry):
    global looked_entries
    resp = requests.get(base_url + wiki_entry)
    bsobj = BeautifulSoup(resp.text, 'lxml')
    links = bsobj.findAll('a', {'href':re.compile('^/wiki/'), 'class':'mw-redirect'})
    wiki_entry = wiki_entry.strip()
    print('page: %s' % wiki_entry)
    looked_entries.add(wiki_entry)
    for link in links:
        if link['href'] not in looked_entries:
            wiki_db.insert_entry(link['title'], link['href'])
            get_links(link['href'])

def robots():
    pass

if __name__ == '__main__':
    get_links("/wiki/linus_torvalds")
