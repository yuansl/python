#!/usr/bin/python3

import pymysql

class wiki_db():
    def __init__(self, user='root', password='mariadb'):
        import pymysql
        self.db_conn = pymysql.connect(user=user,passwd=password,port=3306,host='localhost',db='wikipedia', charset='utf8mb4')

    def db_store(self, entry, url):
        """
        Insert a record into database.
        """
        cursor = self.db_conn.cursor()
        cursor.execute('insert into entry(wiki_entry, entry_url) values(%s,%s)', (entry, url))
        self.db_conn.commit()
        cursor.close()
        
    def db_delete(self, fetch_key):
        """
        Delete a record from database specified by the condition.
        Not supported
        """
        if self.db_fetch(fetch_key) is not None:
            cursor = self.db_conn.cursor()
            cursor.execute('delete from entry where entry_url=%s', fetch_key)
            self.db_conn.commit()
            cursor.close()
            return 0
        else:
            print("DB_DELETE_ERROR: db_not_found!!!")
            return -1
            
    def db_update(self, fetch_key, data={}):
        """
        update a record already exists in the database.
        """
        if self.db_fetch(fetch_key) is not None:
            cursor = self.db_conn.cursor()
            cursor.execute('update entry set wiki_entry=%s,entry_url=%s where entry_url=%s', (data['wiki_entry'], data['entry_url'], fetch_key))
            self.db_conn.commit()
            cursor.close()
            return 0
        else:
            print("DB_UPDATE_ERROR: db_not_found!!!")
            return -1

    def db_fetch(self, key):
        """
        Fetch the specified record from the database.
        """
        cursor = self.db_conn.cursor()
        result_rows = cursor.execute('select wiki_entry from entry where entry_url= %s', key)
        if result_rows > 0:
            result_set = cursor.fetchone()
        else:
            result_set = None
        cursor.close()
        return result_set
    
if __name__ == '__main__':
    db = wiki_db()
    db.db_delete(fetch_key='/wiki/Linux')
