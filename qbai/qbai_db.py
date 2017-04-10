#!/usr/bin/python3

import os

def db_connect(user='root', password=''):
    import pymysql
    db_conn = pymysql.connect(user=user,passwd=password,port=3306,host='localhost',db='QBAI', charset='utf8mb4')

    return db_conn

def insert_user(uid,uname='',gender='male',age=0,constel='',marrage='single',career='',homeland='China',qb_age='0 day',smilefaces=0,fans=0,comments=0):
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    cursor.execute('insert into user(\
    user_id,\
    user_name,\
    gender,\
    age,\
    constellation,\
    marrage,\
    career,\
    homeland,\
    qb_age,\
    smile_faces,\
    fans,\
    comments) values(\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s,\
    %s)', (uid,uname,gender,str(age),constel,marrage,career,homeland,qb_age,str(smilefaces),str(fans),str(comments)))
    db_conn.commit()
    cursor.close()
    db_conn.close()

def user_exists(user_id):
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    rows = cursor.execute('select user_id from user where user_id = %s', (user_id))
    cursor.close()
    db_conn.close()
    
    if rows > 0:
        return True
    return False

def get_all_users():
    saved_users = set()
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    rows = cursor.execute('select user_id from user')
    while rows > 0:
        result = cursor.fetchone()
        saved_users.add(result[0])
        rows -= 1

    cursor.close()
    db_conn.close()
    return rows, saved_users
def article_exists(article_id):
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    rows = cursor.execute('select article_id from article where article_id = %s', (article_id))
    cursor.close()
    db_conn.close()
    
    if rows > 0:
        return True
    return False

def insert_article(article_id, author, location):
    db_conn = db_connect('root', 'mariadb')
    cursor = db_conn.cursor()
    cursor.execute('insert into article(\
    article_id,\
    author_name,\
    location) values(\
    %s,\
    %s,\
    %s)', (article_id,author,location))
    db_conn.commit()
    cursor.close()
    db_conn.close()

def test():
    article_id = '43436'
    location = os.getcwd() + '/articles/' + article_id + '.txt'
    insert_article(article_id, 'yuansl', location)
        
if __name__ == '__main__':
    rows, result_sets = get_all_users()
