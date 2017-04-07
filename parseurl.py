#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, re

def parseurl(url):
    strlen = len(url[1:])
    rows = int(url[0])
    cols = strlen / rows
    right_rows = strlen % rows
    new_str = url[1:]
    url_true = ''

    for i in xrange(strlen):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
    url_true += new_str[p]
    print "url_true: ", urllib2.unquote(url_true)
    return urllib2.unquote(url_true).replace('^', '0')

if __name__ == '__main__':
    url = raw_input('please input a song ID:')
    url = parseurl(url)
    print "url: ", url

