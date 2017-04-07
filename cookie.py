#!/usr/bin/python
# coding: utf-8

import urllib2
import urllib
import re
import cookielib

def http_request(url, data, headers):
    req = urllib2.Request(url, data, headers)    
    try:
        response = urllib2.urlopen(req)
        return response
    except urllib2.URLError, e:
        print 'reason:', e.reason
    except urllib2.HTTPError, e:
        print 'error code:', e.code

def login_zhihu(url, post, headers):
    try:    
        data = urllib.urlencode(post)
        req = urllib2.Request(url, data=data, headers=headers)
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        resp = opener.open(req)
        return cookie
    except urllib2.URLError, e:
        print '[failure reason~]:', e.code, e.reason
    except urllib2.HTTPError, e:
        print 'error code:', e.code
        
def cookie_string(ck_name, zhihu_ck):
    string = ''
    for item in ck_name:
        string += item + '=' + zhihu_ck[item]
    return string

def process_cookie(cookie):
    ck_name = []
    zhihu_ck = {}    
    for item in cookie:
        zhihu_ck[item.name] = item.value
        ck_name.append(item.name)
    return ck_name, zhihu_ck
    
def main():

    url = 'http://www.zhihu.com/#slogin'
    post = {
        "email":"yuanshenglong@126.com",
        "password":"Iloveh3r4ever",
        "rememberme":"y" }
    
    user_agent = "\
Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"    

    headers = {
        "Host":"www.zhihu.com",
        "User-Agent": user_agent,
        "Accept":"*/*",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-with":"XMLHttpRequest",
        "Referer":"http://www.zhihu.com/",
        "Connection":"keep-alive",
        "Pragma":"no-cache",
        "Cache-Control":"no-cache" }
    post['_xsrf'] = "bd83150c8689dcd7e866a86efd93a1e2"
    cookie = login_zhihu(url, post, headers)
    print cookie
    ck_name, zhihu_ck = process_cookie(cookie)
    string = cookie_string(ck_name, zhihu_ck)    
        
    url = 'http://www.zhihu.com/'
    headers['Cookie'] = string

    try:
        html = http_request(url, None, headers)
        print html.read()
    except urllib2.URLError, e:
        print e.reason
    except urllib2.HTTPError, e:
        print e.code

if __name__ == "__main__":
    main()
