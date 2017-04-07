#!/usr/bin/python3

def dbconnect(user='', passwd='', db='QBAI'):
    import pymysql
    db_conn = pymysql.connect(host='localhost', port=3306, user=user, passwd=passwd, charset='utf8mb4', db=db)
    return db_conn

def insert_user(user_id='0001', user_name='', gender='male', age=0, constellation='', marrage='single', career='', homeland='China', qb_age='', smile_faces=0, fans=0, comments=0):
    db_conn = dbconnect('root', 'hanxiaopei')
    cursor = db_conn.cursor()
    
    query = "insert into user(\
    user_id,\
    user_name,\
    gender,\
    age,\
    constellation,\
    marrage, career,\
    homeland,\
    qb_age,\
    smile_faces,\
    fans,\
    comments)\
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    args = (user_id,
            user_name,
            gender,
            str(age),
            constellation,
            marrage,
            career,
            homeland,
            qb_age,
            str(smile_faces),
            str(fans),
            str(comments))
    rows = cursor.execute(query, args)
    db_conn.commit()
    db_conn.close()
    
def insert_article(article_id, content, author_name):
    db_conn = dbconnect('root', 'hanxiaopei')
    cursor = db_conn.cursor()
    
    cursor.execute('insert into article(\
    article_id,\
    content,\
    author_name)\
    values(%s, %s, %s)', (article_id, content, author_name))
    
    db_conn.commit()
    cursor.close()
    db_conn.close()

def test():
    insert_user(user_id='4356447', user_name='are**you', age=37)

if __name__ == '__main__':
    test()
