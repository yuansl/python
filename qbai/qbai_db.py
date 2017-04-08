#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup
import bs4
from urllib import request
import qbai_db
import os

def get_god_comment(article_id):
    article_url = 'http://www.qiushibaike.com'

def get_article(html):
    bsobj = BeautifulSoup(html, 'lxml')
    articles = bsobj.findAll('div', id=re.compile('qiushi_tag_\d+'))
    for article in articles:
        div = article.find('div', {'class': re.compile('author')})
        a = div.find('a', title=re.compile('\w+'))

        if a is None:
            continue
        user_href = a['href']
        user_id = user_href[7:].strip('/')
        user_name = a.text.strip()
        div = div.find('div', {'class':re.compile('articleGender')})
        if div is not None:
            age = div.text.strip()
        else:
            age = 0
        
        #save_user_info(user_id)
        
        a = article.find('a', {'class':'contentHerf'})
        if a is None:
            continue
        # /article/0000000
        article_id = a['href'][9:].strip()
        content = a.text.strip()

        a = article.find('a', {'class':'indexGodCmt'})
        if a is not None:
            god_name = a.find('span', {'class':'cmt-name'}).text.strip().replace('\n', '')
            god_comment = a.find('div', {'class':'main-text'}).text.strip().replace('\n', '')
        else:
            god_name = ''
            god_comment = ''

        qbai_db.insert_article(article_id, content, user_name)
        
def save_user_info(user_id):
    if not os.path.exists(str(user_id) + '.html'):
        user_url = 'http://www.qiushibaike.com/users/' + str(user_id)
        resp = requests.get(user_url)
        html = resp.text
        fd = open(str(user_id) + '.html', 'w')
        fd.write(html)
        fd.close()
    else:
        fd = open(str(user_id) + '.html')
        html = fd.read()
        fd.close()

    user_info = []
    bsobj = BeautifulSoup(html, 'lxml')
    userinf_div = bsobj.find('div', {'class' : 'user-col-left'})
    for ul in userinf_div.findAll('ul'):
        for li in ul.findAll('li'):
            user_info.append(li.text.strip())
            
    div = bsobj.find('div', {'class':'user-header-cover'})
    if div is None:
        return
    
    uname = div.text.strip()
    fans = user_info[0]
    fans = int(fans[fans.index(':')+1:])
    comments = user_info[3]
    comments = int(comments[comments.index(':')+1:])
    smile_faces = user_info[4]
    smile_faces = int(smile_faces[smile_faces.index(':')+1:])
    marrage = user_info[6]
    marrage = marrage[marrage.index(':')+1:]
    constellation = user_info[7]
    constellation = constellation[constellation.index(':')+1:]
    career = user_info[8]
    career = career[career.index(':')+1:]
    homeland = user_info[9]
    homeland = homeland[homeland.index(':')+1:]
    qage = user_info[10]
    qage = qage[qage.index(':')+1:]
    
    qbai_db.dbinsert_user(user_id=user_id, user_name=uname, marrage=marrage, gender='male', constellation=constellation, career=career, smile_faces=smile_faces, fans=fans, comments=comments, qb_age=qage)
        
if __name__ == '__main__':
    if not os.path.exists('index.html'):
        resp = requests.get('http://www.qiushibaike.com')
        html = resp.text
        fd = open('index.html', 'w')
        fd.write(html)
        fd.close()
    else:
        fd = open('index.html')
        html = fd.read()
        fd.close()
        get_article(html)
        
