#!/usr/bin/python

import urllib2
import urllib

post = {
    "_xsrf":"bd83150c8689dcd7e866a86efd93a1e2",
    "email":"yuanshenglong@126.com",
    "password":"Iloveh3r4ever",
    "rememberme":"y" }

user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"

header_data = {
    "Host":"www.zhihu.com",
    "User-Agent": user_agent,
    "Accept":"*/*",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-with":"XMLHttpRequest",
    "Referer":"http://www.zhihu.com/",
    "Connection":"keep-alive",
    "Pragma":"no-cache",
    "Cache-Control":"no-cache" }

url = "http://www.zhihu.com/login"

data = urllib.urlencode(post)

try:
    request = urllib2.Request(url, data=data, headers = header_data)

    response = urllib2.urlopen(request)
    print response.info()

    print response.read()
    response = urllib2.urlopen('http://www.zhihu.com')
    
except urllib2.URLError, e:
    print "reason:", e.reason
except urllib2.HTTPError, e:
    print "error code:", e.code
