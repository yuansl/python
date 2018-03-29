#!/usr/bin/python3

import threading
import requests
from bs4 import BeautifulSoup

def __(raws):
    if isinstance(raws, str):
        return raws.strip().replace('\t','').replace('\n', '')

mozilla_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', 'Connection': 'keep-alive'
}

def get_house_info(url):
    """print house info from `url` at anjuke.com
    url = 'https://sh.zu.anjuke.com/fangyuan/$id'
    """
    req = requests.get(url,headers=mozilla_headers)
    html_page = req.text
    bsobj = BeautifulSoup(html_page, "lxml")
    info = bsobj.find('div', {'class': 'auto-general'})
    if info is not None:
        print('house-info: ', __(info.text))
    title_basic_info = bsobj.find('div', {'class': 'title-basic-info'})
    if title_basic_info is not None:
        specs_desc = ''
        specs = title_basic_info.findAll('span', {'class': 'info-tag'})
        for spec in specs:
            specs_desc += __(spec.text)
        print('specs: %s' % specs_desc)
        location = title_basic_info.find('ul')
        if location is not None:
            print("location: ", __(location.text))

    # contact
    brokerInfo = bsobj.find('div', {'class': 'brokerInfo'})
    if brokerInfo is not None:
        bInfo = brokerInfo.find('div', {'class': 'bInfo'})
        if bInfo is not None:
            print("contact: ", end='')
            name = bInfo.find('strong', class_='name')
            print('name: ', name.text if name is not None else 'unknown', end='')
            phone = bInfo.find('strong', class_='phone')
            print(' phone: ', phone.text if phone is not None else "unknown")

tasks = []
class downloader(threading.Thread):
    def __init__(self, url):
        self.url = url
    def start(self):
        get_house_info(self.url)
            
class anjuke_entry():
    def __init__(self, location='songjiang'):
        self.headers = mozilla_headers
        self.url = 'https://sh.zu.anjuke.com/fangyuan/%s/' % location
        
    def run(self):
        req = requests.get(self.url,headers=self.headers)
        html_page = req.text
        bsobj = BeautifulSoup(html_page, "lxml")
        items = bsobj.findAll('div', {'class': 'zu-itemmod'})
        for item in items:
            self.look_into(item)
            break

    def look_into(self, item):
        item_a = item.find('a', {'class': 'img'})
        img = item_a.find('img')
        url = item_a['href']
        task = downloader(url)
        tasks.append(task)
        task.start()
        print('fangyuan: %s title: %s alt: %s image: %s' % (item_a['href'], item_a['title'], item_a['alt'], img['src']))
        info = item.find('div', {'class': 'zu-info'})
        detail_item = info.find('p', {'class': 'tag'})
        address = info.find('address')
        print('address: %s' % __(address.text))
        price = item.find('div', {'class': 'zu-side'})
        print("price: %s" % __(price.text))

if __name__ == '__main__':
    app = anjuke_entry('jiuting')
    app.run()
