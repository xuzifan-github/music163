#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

MYSQL_DB = '163music'
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
MYSQL_HOST = 'localhost'

connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    cursor = connection.cursor()
    sql = 'SELECT music_id,title,artist FROM music WHERE music_id NOT IN \
                (SELECT music_id FROM music_file) ORDER BY music_id DESC'
    cursor.execute(sql)
    movies = cursor.fetchall()
    for i in movies:
        print(i)
