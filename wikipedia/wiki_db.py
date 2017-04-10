#!/usr/bin/python3

import pymysql

def db_connect(user='root', password='mariadb'):
    import pymysql
    db_conn = pymysql.connect(user=user,passwd=password,port=3306,host='localhost',db='wikipedia', charset='utf8mb4')

    return db_conn

def insert_entry(entry, url):
    db_conn = db_connect()
    cursor = db_conn.cursor()
    cursor.execute('insert into entry values(%s,%s)', (entry, url))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    
if __name__ == '__main__':
    insert_entry('UNIX', '/wiki/UNIX')
