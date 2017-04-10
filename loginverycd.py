#!/usr/bin/python
# coding: utf-8

import urllib
import urllib2

post_data = { "username":"yuansl2111",
              "password":"Iloveh3r4ever",
              "continue":"http://www.verycd.com/",
              "fk":"",
              "save_cookie":"1",
              "login_submit":"登录" }

post = urllib.urlencode(post_data)

url = "http://secure.verycd.com/signin"

request = urllib2.Request(url, data=post)
try:
    response = urllib2.urlopen(request)
    print response.read()
except urllib2.URLError, e:
    print e.reson
except urllib2.HTTPError, e:
    print e.code
              
