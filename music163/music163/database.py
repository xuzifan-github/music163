# -*- coding: utf-8 -*-

import pymysql

MYSQL_DB = '163music'
MYSQL_USER = 'root'
MYSQL_PASS = 'A123456'
MYSQL_HOST = 'localhost'
MYSQL_PORT = 50036

connection = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
