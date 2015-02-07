#!/usr/bin/python
# coding: utf-8

import urllib2
import urllib
import re

regx = re.compile('\"question-link\">(.+?)</a></div>', re.DOTALL)

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

question = raw_input("input your question for query: ")
url = 'http://www.zhihu.com/search?q=%s&type=question' % question
url = url.strip().replace(' ', '%20').replace('\\x', '%')

try:
    response = urllib2.urlopen(url)
    html = response.read()
    groups = re.findall(regx, html)

    if groups == []:
        print "I am sorry, there is nothing found"
    else:
        for g in groups:
            print g.replace('<em>', '').replace('</em>', '')
except urllib2.URLError, e:
    print 'URLError: ', e.reason
except urllib2.HTTPError, e:
    print 'Error code: ', e.code
