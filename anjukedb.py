#!/usr/bin/python3

import pymysql as mysql

class Anjukedb():
    def __init__(self, host='172.17.0.2', user='admin', password='mariadb'):
        self.conn = None
        self.host = host
        self.user = user
        self.password = password
        self.database = 'anjuke'
        self.charset = 'utf8mb4'
        
    def connect(self):
        if self.conn is None:
            self.conn = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset=self.charset)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
        self.conn = None
        
    def sql_exec(self, sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            cur.close()
        except Exception as error:
            print("db insert error: ", error)
            
    def insert_resource(self, title, fangyuan_url, price, img_src, address):
        if self.conn is not None:
            sql = "insert into resource(title, fangyuan_url, price, img_src, address) values('%s','%s','%s','%s','%s')" % (title, fangyuan_url, price, img_src, address)
            self.sql_exec(sql)
        else:
            print('Error! the connection to the database server is closed at now.')
    def insert_house(self, fangyuan_url, rent_mode, address, spec, contact, detail):
        if self.conn is not None:
            try:
                sql = "insert into house(fangyuan_url, rent_mode, address, spec, contact, detail) values('%s','%s','%s','%s','%s','%s')" % (fangyuan_url, rent_mode, address, spec, contact, detail)
                self.sql_exec(sql)
            except Exception as error:
                print('Error encountered while inserting into the table: %s', str(error))
    
    def delete(self):
        if self.conn is not None:
            self.conn.commit()
    def update(self):
        if self.conn is not None:
            self.conn.commit()
    def query(self, url):
        query_sql = 'select * from house where fangyuan_url=%s' % url
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

if __name__ == '__main':
    db = Anjukedb()
    db.connect()
    db.insert_resource('haha', 'https://example.com', '9300', 'https://example.com', 'Shanghai fifth street #33 , China')
    db.insert_house('https://example.com', 'single', 'Shanghai fifth street #33 , China', 'big house', 'mzd 1383088888', 'good house resource')
    db.close()
