#!/usr/bin/python3

import os

def db_connect(user='root', password=''):
    import pymysql
    db_conn = pymysql.connect(user=user,passwd=password,port=3306,host='localhost',db='douban', charset='utf8mb4')

    return db_conn

def insert_song(title,artist,url,albumtitle,len_time, public_time):
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    cursor.execute('insert into song(title, artist, url,albumtitle, time, public_time) values(%s,%s,%s,%s,%s,%s)', (title,artist,url,albumtitle,str(len_time), public_time))
    db_conn.commit()
    cursor.close()
    db_conn.close()

def db_fetch():
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    rows = cursor.execute('select url, title from song where public_time=2017')
    while rows > 0:
        result = cursor.fetchone()
        print(result[0], result[1])
        rows -= 1

    cursor.close()
    db_conn.close()

def test():
    db_fetch()
    
if __name__ == '__main__':
    test()
