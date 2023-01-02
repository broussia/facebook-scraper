import time
import pandas as pd
import xlsxwriter
import json
import pymysql
import os

from utils import db_settings

like_weight = 1
comment_weight = 6
friend_weight = 20

cursor = db_settings()

# 计算friends 20
sql_friend = 'select f_host,f_name,f_link,id from fbfriends.friends where isused = false'
cursor.execute(sql_friend)
friends = cursor.fetchall()
for friend in friends:
    i_host = friend[0]
    i_name = friend[1]
    i_link = friend[2]
    id = friend[3]
    sql_is_exist = "select * from fbfriends.intimacy where i_name = \'{}\' ".format(i_name)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        continue
    sql_insert_friend = "insert  into fbfriends.intimacy(i_host,i_name,friend_score,i_link) values (\'{}\',\'{}\',{},\'{}\')".format(
        i_host, i_name, friend_weight, i_link)
    cursor.execute(sql_insert_friend)
    sql_update_isused = "update fbfriends.friends set isused = true where id = {}".format(id)
    cursor.execute(sql_update_isused)
cursor.connection.commit()

# 计算likes 1
sql_like = "select l_host,l_friend,l_link,id from fbfriends.likes where isused = false"
cursor.execute(sql_like)

likes = cursor.fetchall()
for like in likes:
    l_host = like[0]
    l_friend = like[1]
    l_link = like[2]
    id = like[3]
    if l_friend == '':
        continue
    sql_is_exist = "select * from fbfriends.intimacy where i_host = \'{}\' and i_name = \'{}\'".format(l_host ,l_friend)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        sql_update_like = "update fbfriends.intimacy set like_score = like_score + {} where i_name = \'{}\'".format(
            like_weight, l_friend)
    else:
        sql_update_like = "insert into fbfriends.intimacy(i_host,i_name,like_score,i_link) values (\'{}\',\'{}\',{},\'{}\')".format(
            l_host, l_friend, like_weight, l_link)
    cursor.execute(sql_update_like)
    sql_update_isused = "update fbfriends.likes set isused = true where id = {}".format(id)
    cursor.execute(sql_update_isused)
cursor.connection.commit()

# 计算评论 6
sql_comment = "select c_host,c_name,c_link,id from fbfriends.comments where isused = false"
cursor.execute(sql_comment)
comments = cursor.fetchall()
for comment in comments:
    c_host = comment[0]
    c_name = comment[1]
    c_link = comment[2]
    id = comment[3]
    if c_name == c_host:
        continue
    sql_is_exist = "select * from fbfriends.intimacy where i_host = \'{}\' and i_name = \'{}\'".format(c_host, c_name)
    cursor.execute(sql_is_exist)
    if len(cursor.fetchall()) > 0:
        sql_update_comment = "update fbfriends.intimacy set comment_score = comment_score + {} where i_name = \'{}\'".format(
            comment_weight, c_name)
    else:
        sql_update_comment = "insert into fbfriends.intimacy(i_host,i_name,comment_score,i_link) values (\'{}\'," \
                             "\'{}\',{},\'{}\')".format(c_host, c_name, comment_weight, c_link)
    cursor.execute(sql_update_comment)
    sql_update_isused = "update fbfriends.comments set isused = true where id = {}".format(id)
    cursor.execute(sql_update_isused)
cursor.connection.commit()

# 总计
sql_total = "update fbfriends.intimacy set total_score = comment_score + intimacy.like_score + intimacy.friend_score"
cursor.execute(sql_total)
cursor.connection.commit()
