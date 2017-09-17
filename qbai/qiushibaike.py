#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup
import bs4
from urllib import request
import qbai_db
import os
import time

saved_users = set()

def get_god_comment(article_id):
    article_url = 'http://www.qiushibaike.com'

def get_article(html):
    global saved_users
    bsobj = BeautifulSoup(html, 'lxml')
    articles = bsobj.findAll('div', id=re.compile('qiushi_tag_\d+'))
    for article in articles:
        # author
        div = article.find('div', {'class': re.compile('author')})
        a = div.find('a', title=re.compile('\w+'))
        if a is None:
            user_id = '0'
            author = 'Unknown'
        else:
            user_href = a['href']
            user_id = user_href[7:].strip('/')
            author = a.text.strip()
            div = div.find('div', {'class':re.compile('articleGender')})
            if div is not None:
                age = div.text.strip()
            else:
                age = 0
                
        if user_id not in saved_users and user_id != '0':
            save_user_info(user_id)
            saved_users.add(user_id)
        
        a = article.find('a', {'class':'contentHerf'})
        if a is None:
            continue

        article_id = a['href'][9:].strip()
        location = os.getcwd() + '/articles/' + article_id + '.txt'
        print('article:%s location: %s' % (article_id,location))
        try:
            fd = open(location, 'w')
            content = a.text.strip()
            fd.write(content)
            fd.close()
        except Exception as e:
            if os.path.exists(os.getcwd()+'/articles'):
                os.mkdir(os.getcwd()+'articles')
            print(e)

        a = article.find('a', {'class':'indexGodCmt'})
        if a is not None:
            god_name = a.find('span', {'class':'cmt-name'}).text.strip().replace('\n', '')
            god_comment = a.find('div', {'class':'main-text'}).text.strip().replace('\n', '')
        else:
            god_name = ''
            god_comment = ''
        if qbai_db.article_exists(article_id):
            return
        qbai_db.insert_article(article_id, author, location)
        
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
    if userinf_div is None:
        return
    for ul in userinf_div.findAll('ul'):
        for li in ul.findAll('li'):
            user_info.append(li.text.strip())
            
    div = bsobj.find('div', {'class':'user-header-cover'})
    if div is None:
        return
    
    uname = div.text.strip()
    fans = user_info[0]
    nfans = int(fans[fans.index(':')+1:])
    comments = user_info[3]
    ncomments = int(comments[comments.index(':')+1:])
    smile_faces = user_info[4]
    nsmile_faces = int(smile_faces[smile_faces.index(':')+1:])
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
    
    qbai_db.insert_user(user_id, uname=uname, marrage=marrage, gender='male', constel=constellation, career=career, smilefaces=nsmile_faces, fans=nfans, comments=ncomments, qb_age=qage)

def get_links(article_id):
    base_url = 'http://www.qiushibaike.com'
    url = base_url + '/article/' + article_id
    resp = requests.get(url)
    get_article(resp.text)

    # other pages
    bsobj = BeautifulSoup(resp.text, 'lxml')
    link = bsobj.find('a', href=re.compile('page'))
    if link is not None and 'href' in link.attrs:
        uri = link['href']
        query_pos = uri.index('?')
        for j in range(999):
            for i in range(2, 36):
                # /8hr/page/3?s=4972xxx
                url = base_url + '/8hr/page/' + str(i) + '?s=4972%03d' % (j)
                print('url:' + url)
                resp = requests.get(url)
                html = resp.text
                get_article(html)
                time.sleep(2)
        time.sleep(10)
    
if __name__ == '__main__':
    rows, saved_users = qbai_db.get_all_users()
    get_links('')
