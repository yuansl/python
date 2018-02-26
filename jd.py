#!/usr/bin/python3

import re
from urllib import parse
import requests
import os
from bs4 import BeautifulSoup
from jddb import Jddb

def parse_jd_goods_info(htmldoc, db):
    obj = BeautifulSoup(htmldoc, "lxml")
    titie_tag = obj.find('title')
    kw_end = titie_tag.text.find('-')
    keywords = titie_tag.text[:kw_end]
    goods_div = obj.find('div', {'id': 'J_goodsList'})
    goods_list = goods_div.findAll('li', {'class': 'gl-item'})
    '''https://search.jd.com/Search?keyword=alienware&enc=utf-8&qrst=2&rt=1&stop=1&vt=2&bs=1&wq=alienware%20area53&ev=exbrand_%E5%A4%96%E6%98%9F%E4%BA%BA%EF%BC%88Alienware%EF%BC%89%5E&page=3&s=71&click=0
    '''
    for goods in goods_list:
        Id = int(goods.attrs['data-sku'])
        url = 'https://item.jd.com/%d.html' % Id        
        div_name = goods.find('div', {'class': 'p-name'})
        goods_name = div_name.find('em').text.strip().replace('\'', '^')
        goods_name = goods_name.replace('\n', ' ')
        digest = div_name.find('i', {'class': 'promo-words'}).text.strip()
        div_price = goods.find('div', {'class': 'p-price'})
        goods_price = div_price.find('strong')
        price_text = goods_price.text.strip()
        price_starter = price_text.find(u'￥')
        if price_starter < 0:
            continue
        price = price_text[price_starter+1:]
        print('price: %s' % price)

        publisher = None
        div_shopnum = goods.find('div', {'class': re.compile('shop')})
        if div_shopnum is not None:
            link = div_shopnum.find('a', {'class': 'curr-shop'})
            if link is None:
                continue
            publisher = link.text.strip()
        else:
            publisher = 'jd'
        print('url: %s, publisher: %s' % (url, publisher))
        div_comments = goods.find('div', {'class': 'p-commit'})
        goods_comments = div_comments.text.strip().replace('\'', '^')
        db.insert(Id, url, goods_name, digest, publisher, float(price), keywords, goods_comments)

def search_jd(db, keyword='', n=1):
    if not os.path.exists('jd.html'):
        uri = 'https://search.jd.com/Search?'
        query = {
            'keyword': keyword,
            'wq': keyword,
            'enc': 'utf-8',
            'page': 2 * n - 1
        }
        url = uri+parse.urlencode(query)
        print('url=%s' % url)
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                htmldoc = resp.content.decode('utf-8')
                parse_jd_goods_info(htmldoc, db)
                
                # with open('jd.html', 'w') as fd:
                #     fd.write(htmldoc)
            except Exception as e:
                print('Error: ' + str(e))
        else:
            print('jd-search fails')
            print(resp.status_code, resp.reason)
    else:
        with open('jd.html', 'r') as fd:
            print('jd.html exists already')
            htmldoc = fd.read()
            parse_jd_goods_info(htmldoc)
if __name__ == '__main__':
    db = Jddb('172.17.0.2', 'admin', 'mariadb')
    db.connect()
    keyword = input('input a keyword for searching on jd.com: ')
    search_jd(db, keyword)
    db.close()
