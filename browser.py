#!/usr/bin/python3

from selenium import webdriver
import time
import threading
import json

host = 'https://douban.fm'
browser = webdriver.PhantomJS()
def doubanfm_get(url, timeout):
    browser.get(url)
    time.sleep(timeout)
    body = browser.find_element_by_tag_name('body')
    data = json.loads(body.text)

    return data
        
def doubanfm_get_songlist(id):
    """
    Get songlist from douban.fm with given songlist id
    """
    songlist_path = '/j/v2/songlist/%s/' % id
    query = 'kbps=192'
    url = host + songlist_path + '?' + query
    songlist = doubanfm_get(url, 0)
    if songlist is None:
        return None
    return songlist.get('songs', None)

songlists = [
    {'type': 'songlist',
     'total': 131,
     'items': [{'collected_count': 116, 'cover': 'https://img3.doubanio.com/view/fm_songlist_cover/small/public/292215.jpg', 'title': '周杰伦＋方文山作品 他人演唱（一）', 'play_count': 0, 'id': 259267}, {'collected_count': 88, 'cover': 'https://img3.doubanio.com/view/fm_songlist_cover/small/public/292240.jpg', 'title': '周杰伦作曲 他人演唱（二）', 'play_count': 0, 'id': 259346}, {'collected_count': 12, 'cover': 'https://img1.doubanio.com/view/fm_songlist_cover/small/public/336378.jpg', 'title': '没有周杰伦的歌？', 'play_count': 0, 'id': 425179}, {'collected_count': 2052, 'cover': 'https://img3.doubanio.com/img/songlist/small/1034361-2.jpg', 'title': '80後的那些事儿40', 'play_count': 0, 'id': 1034361}, {'collected_count': 46, 'cover': 'https://img1.doubanio.com/view/fm_songlist_cover/small/public/417548.jpg', 'title': '喜欢的歌', 'play_count': 0, 'id': 4700616}]
    }]
songlists = songlists[0]['items']

class downloader(threading.Thread):
    def __init__(self, id):
        super(downloader, self).__init__()
        self.id = id

    def run(self):
        doubanfm_get_songlist(self.id)


def thread_based_downloader():
    tasks = []
    for songlist in songlists:
        t = downloader(songlist['id'])
        tasks.append(t)
        t.start()

    # waiting for thread termination
    for t in tasks:
        if t.is_alive():
            t.join()

def normal_downloader():
    for songlist in songlists:
        doubanfm_get_songlist(songlist['id'])
        
def test_positionarg(*args):
    positionargs(*args)

def positionargs(id, name, url):
    print('id = %s' % id)
    print('name = %s' % name)
    print('url = %s' % url)
        
if __name__ == '__main__':
    test_positionarg('yuansl', 'shenglong', 'www.baidu.com')

