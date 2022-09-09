import time
import pandas as pd
import xlsxwriter
import json
import pymysql
import os

from utils import db_settings

like_weight = 1
comment_weight = 6
friend_weight = 100

cursor = db_settings()

# 计算friends 20
sql_friend = 'select f_host,f_name from fbfriends.friends '
cursor.execute(sql_friend)
friends = cursor.fetchall()
for friend in friends:
    i_host = friend[0]
    i_name = friend[1]
    sql_is_exist = "select * from fbfriends.intimacy where i_name = \'{}\'".format(i_name)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        continue
    sql_insert_friend = "insert  into fbfriends.intimacy(i_host,i_name,friend_score) values (\'{}\',\'{}\',20)".format(
        i_host, i_name)
    cursor.execute(sql_insert_friend)
cursor.connection.commit()

# 计算likes 1
sql_like = "select l_host,l_friend from fbfriends.likes"
cursor.execute(sql_like)
likes = cursor.fetchall()
for like in likes:
    l_host = like[0]
    l_friend = like[1]
    if l_friend == '':
        continue
    sql_is_exist = "select * from fbfriends.intimacy where i_name = \'{}\'".format(l_friend)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        sql_update_like = "update fbfriends.intimacy set like_score = like_score + 1 where i_name = \'{}\'".format(
            l_friend)
    else:
        sql_update_like = "insert into fbfriends.intimacy(i_host,i_name,like_score) values (\'{}\',\'{}\',1)".format(
            l_host, l_friend)
    cursor.execute(sql_update_like)
cursor.connection.commit()

# 计算评论 6
sql_comment = "select c_host,c_name from fbfriends.comments"
cursor.execute(sql_comment)
comments = cursor.fetchall()
for comment in comments:
    c_host = comment[0]
    c_name = comment[1]
    if c_name == c_host:
        continue
    sql_is_exist = "select * from fbfriends.intimacy where i_name = \'{}\'".format(c_name)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        sql_update_comment = "update fbfriends.intimacy set comment_score = comment_score + 6 where i_name = \'{}\'".format(
            c_name)
    else:
        sql_update_comment = "insert into fbfriends.intimacy(i_host,i_name,comment_score) values (\'{}\',\'{}\',6)".format(
            c_host, c_name)
    cursor.execute(sql_update_comment)
cursor.connection.commit()

# 总计
sql_total = "update fbfriends.intimacy set total_score = comment_score + intimacy.like_score + intimacy.friend_score"
cursor.execute(sql_total)
cursor.connection.commit()
