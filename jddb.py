#!/usr/bin/python3

import pymysql as mysql

class Jddb():
    def __init__(self, host, user, password):
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.database = 'jd'
        self.charset = 'utf8mb4'
        
    def connect(self):
        if self.conn is None:
            self.conn = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset=self.charset)

    def insert(self, Id, url, name, digest, publisher, price, keywords, comments=None):
        if self.conn is not None:
            try:
                sql = "insert into goods(id, url, name, digest, publisher, price,keywords,comments) values(%s, '%s', '%s', '%s', '%s', %.2f,'%s','%s')" % (str(Id), url, name, digest, publisher, price, keywords, comments)
                print('sql:%s' % sql)
                cur = self.conn.cursor()
                cur.execute(sql)
                cur.close()
            except Exception as e:
                print('exception: ' + str(e))
        else:
            print('Error! the connection to the database server is closed at now.')
    def delete(self):
        if self.conn is not None:
            self.conn.commit()
    def update(self):
        if self.conn is not None:
            self.conn.commit()
    def query(self, id):
        query_sql = 'select * from goods where id=%d' % id
        cid = self.conn.cursor()
        rows = cid.execute(query_sql)
        if rows > 0:
            result = cid.fetchone()
            print(result)
        else:
            result = None
        cid.close()
        
        return result
    
    def close(self):
        if self.conn is not None:
            self.conn.commit()            
            self.conn.close()
