#!/usr/bin/python

import urllib2
url = 'http://p4.music.126.net/JYJ4xcxiRohQCkTBMVVQ3g==/7869204721009791.jpg'

req = urllib2.Request(url)
req.add_header('Host', 'p4.music.126.net')
req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0')

req.add_header('Referer', 'http://music.163.com/discover')
req.add_header('Connection', 'keep-alive')
req.add_header('Accept', 'image/png, image/*; q=0.8,*/*;q=0.5')
req.add_data('param=100y100')
try:
    resp = urllib2.urlopen(req)
    data = resp.read()
    with open('png', 'w') as outf:
        outf.write(data)
    outf.close()

except urllib2.URLError, e:
    print e.code, e.reason
except urllib2.HTTPError, e:
    print e.code
