#!/usr/bin/python3

from selenium import webdriver
from bs4 import BeautifulSoup

from urllib import parse
import requests
import re
import json
import os
import time

import douban_db

base_url = 'https://douban.fm/#/channel'

def doubanfm_get_sid():
    host = 'https://erebor.douban.com'
    data = { 'unit':'dale_fm_channel_new', 'uid':'', 'bid':'_34xbyGwbVQ', 'crtr':'4:76','ts':'1495291955667', 'prv':'', 'debug':'false', 'callback':'reqwest_1495257506692' }
    browser = webdriver.PhantomJS()
    url = host + '/?' + parse.urlencode(data)
    print('url: ', url)
    browser.get(url)
    print('page source: ', browser.page_source)
    browser.delete_all_cookies()
    browser.quit()

def doubanfm_get_channel_info(browser, id):
    url = 'https://douban.fm/j/v2/channel_info?id=%s' % id
    browser.get(url)
    time.sleep(2)
    body = browser.find_element_by_tag_name('body')
    channel_info = json.loads(body.text)
    data = channel_info['data']
    channels = data['channels']
    song_num = channels[0]['song_num']
    return song_num

def save_song_info(song, data):
    for item in song:
        if isinstance(item, dict):
            print('title: ', item.get('title', ''), ' artist: ', item.get('artist', ''))
            if 'public_time' in item:
                print('public time: ', item['public_time'])
            if 'albumtitle' in item:
                print('Album title: ', item['albumtitle'])
            if 'genre' in item:
                print('genre: ', item['genre'])
            if 'region' in item:
                print('region: ', item['region'])

            if 'kbps' in item:
                print('kbps: ', item['kbps'])
                data['kbps'] = item['kbps']
            if 'sid' in item:
                print('sid: ', item['sid'])
                data['sid'] = item['sid']
                next = True
            if 'length' in item:
                print('Time: ', item['length'])
            try:
                douban_db.insert_song(item['title'], item['artist'], item['url'], item['albumtitle'], item['length'], item['public_time'])
            except Exception as e:
                print(e)
    return next

def doubanfm_get_songinfo(browser, data, song_num):
    host = 'https://douban.fm/j/v2/playlist'    
    next = False
    count = 0
    while count < song_num:
        if next:
            data['type'] = 'p'
            data['pt'] = ''
            data['pb'] = '128'
            data['apikey'] = ''

        url = host + '/?' + parse.urlencode(data)
        print('url: ', url)
        browser.get(url)
        time.sleep(2)
        body = browser.find_element_by_tag_name('body')
        song_info = json.loads(body.text)
        song = song_info['song']
        if song is not None:
            next = save_song_info(song, data)
        count += 1

def browser_doubanfm():
    browser = webdriver.PhantomJS()
    browser.get('https://douban.fm')
    time.sleep(2)
    browser.save_screenshot('douban_screenshot')
    print('title: ', browser.title)
    
    bsobj = BeautifulSoup(browser.page_source, "lxml")
    hrefs = bsobj.findAll('a', href=re.compile('channel'))

    channel_ids = set()
    for a in hrefs:
        if 'href' in a.attrs:
            uri = a['href']
            i = uri.rindex('/') + 1
            channel_ids.add(uri[i:])
            
    query = { 'kbps':'192', 'client':'s:mainsite|y:3.0', 'app_name':'radio_website', 'version':'100', 'type':'n' }

    for id in channel_ids:
        song_num = doubanfm_get_channel_info(browser, id)
        query['channel'] = id
        doubanfm_get_songinfo(browser, query, song_num)
        
    browser.delete_all_cookies()
    browser.quit()
    
def do_download(url, title):
    resp = requests.get(url)
    file_name = '/home/yuansl/Music/' + title.replace('/', '_') + '.mp4'
    if not os.path.exists(file_name):
        fd = open(file_name, 'wb')
        fd.write(resp.content)
        fd.close()
    
def downloader():
    db_conn = douban_db.db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    rows = cursor.execute('select url, title from song')
    while rows > 0:
        result = cursor.fetchone()
        print(result[0], result[1])
        do_download(result[0], result[1])
        rows -= 1
    cursor.close()
    db_conn.close()

def search_doubanfm():
    pass

if __name__ == '__main__':
    #search_doubanfm()

