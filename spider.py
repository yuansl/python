#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, gzip, StringIO, re

header = { "Host": "www.matrix67.com",
           "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) \
Gecko/20100101 Firefox/35.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;\
q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5",
           "Accept-Encoding": "gzip, deflate, sdch",
           "Connection": "keep-alive",
           "Cache-Control": "max-age=0" }

def get_html(url):
    print "url: ", url
    urlreq = urllib2.Request(url, headers=header)
    html_page = urllib2.urlopen(urlreq).read()
    print "html get done"
    return html_page

def controller():
    url_list = "http://www.matrix67.com/blog/page/%d"
    regex = re.compile('(<div class=\"post-wrapper.*?)<p class=\"pagination\">', re.I)

    with open('org.html', 'a') as fd1, open('text.txt', 'a') as fd2:
        for i in range(1, 3):
            html_c = get_html(url_list % i)
            fd1.write(html_c)
            #html_c = gzip.GzipFile(fileobj = StringIO.StringIO(html_c)).read()
            res = regex.findall(html_c)
            for line in res:
                fd2.write(line)
                fd2.write("\n\n\n")
            print "write done"
    fd1.close()
    fd2.close()

if __name__ == '__main__':
    controller()
