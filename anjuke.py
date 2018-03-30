#!/usr/bin/python3

import os
import threading
import requests
from bs4 import BeautifulSoup

from anjukedb import Anjukedb

mozilla_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
    'Connection': 'keep-alive'
}

def __(raws):
    if isinstance(raws, str):
        return raws.strip().replace('\t','').replace('\n', '').replace(' ', '')

class downloader(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.data = None

    def start(self):
        self.data = get_house_info(self.url)

class House():
    def __init__(self, url, house_info, rent_mode, specs, contact):
        self.url = url
        self.house_info = house_info
        self.rent_mode = rent_mode
        self.specs = specs
        self.address = ''
        self.contact = contact

    def __str__(self):
        house_info = { 'url': self.url,
                       'house_info': self.house_info,
                       'rent-mode': self.rent_mode,
                       'specification': self.specs,
                       'contact': self.contact }
        return str(house_info)
        
def get_house_info(url):
    """print house info from `url` at anjuke.com
    url = 'https://sh.zu.anjuke.com/fangyuan/$id'
    """
    if os.path.exists('./1138350612.fangyuan.html'):
        with open('./1138350612.fangyuan.html', 'r') as fd:
            html_page = fd.read()
    else:
        req = requests.get(url,headers=mozilla_headers)
        html_page = req.text
        
    bsobj = BeautifulSoup(html_page, "lxml")
    info = bsobj.find('div', {'class': 'auto-general'})
    if info is not None:
        house_info = __(info.text)
        title_basic_info = bsobj.find('div', {'class': 'title-basic-info'})
        if title_basic_info is not None:
            specs_desc = ''
            specs = title_basic_info.findAll('span', {'class': 'info-tag'})
            for spec in specs:
                specs_desc += __(spec.text)
            street = title_basic_info.find('ul')
            if street is not None:
                rent_mode = __(street.text)
    # contact
    brokerInfo = bsobj.find('div', {'class': 'brokerInfo'})
    if brokerInfo is not None:
        bInfo = brokerInfo.find('div', {'class': 'bInfo'})
        if bInfo is not None:
            name = bInfo.find('strong', class_='name')
            phone = bInfo.find('strong', class_='phone')
            contact = __(name.text) + ' ' + __(phone.text)
    return House(url, house_info, rent_mode, specs_desc, contact)
            
class anjuke_entry():
    def __init__(self, location='songjiang'):
        self.headers = mozilla_headers
        self.url = 'https://sh.zu.anjuke.com/fangyuan/%s/' % location
        self.db = Anjukedb()
        self.tasks = []
        
    def run(self):
        self.db.connect()
        if os.path.exists('./jiuting.html'):
            with open('./jiuting.html', 'r') as fd:
                html_page = fd.read()
        else:
            req = requests.get(self.url,headers=self.headers)
            html_page = req.text
        
        bsobj = BeautifulSoup(html_page, "lxml")
        items = bsobj.findAll('div', {'class': 'zu-itemmod'})
        for item in items:
            self.digest_info(item)
        
        # waiting for tasks to stop
        for task in self.tasks:
            if task.is_alive():
                task.join()
            print(task.data)
            #self.db.insert_house()
        self.db.close()

    def digest_info(self, item):
        # image info of the house link
        item_a = item.find('a', {'class': 'img'})
        img = item_a.find('img')
        url = item_a['href']
        task = downloader(url)
        task.start()
        self.tasks.append(task)
        
        print('fangyuan: %s\ntitle: %s\nalt: %s\nimage: %s' % (item_a['href'], item_a['title'], item_a['alt'], img['src']))
        
        info = item.find('div', {'class': 'zu-info'})
        detail_item = info.find('p', {'class': 'tag'})
        address = info.find('address')

        location = __(address.text)
        print('address: %s' % location)
        zu_side = item.find('div', {'class': 'zu-side'})
        price = __(zu_side.text)
        print("price: %s" % price)
        self.db.insert_resource(item_a['title'], item_a['href'], price, img['src'], location)

if __name__ == '__main__':
    app = anjuke_entry('jiuting')
    app.run()
