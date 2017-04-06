create table article(article_id varchar(16) primary key, content varchar(150), author_name varchar(40));
create table user(user_id varchar(10), user_name varchar(40), gender varchar(5), age int(3), constellation varchar(40), marrage varchar(10), career varchar(30), homeland varchar(40), qb_age varchar(10), smile_faces int(11), fans int(11), coments int(11), primary key (user_id));
create table god_comment(article_id varchar(16) primary key, god_name varchar(40), content varchar(150));
