from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd
import xlsxwriter
import json
import pymysql
import os

from utils import chrome_setting, db_settings, login

browser = chrome_setting()

# 设置数据库
cursor = db_settings()
# 访问facebook网页
login(browser)

# 好友列表结构：#https://www.facebook.com/rushan.abbas/following
# 构造url
hostname = 'kene.shadrack.79'
# Wang.Dingyuan
# kene.shadrack.79
# jbkatente.king
# antony.olentiati
url = 'https://www.facebook.com/' + hostname + '/friends'
print(url)
browser.get(url)
time.sleep(1)
hostname_xpath = '//*[@class="alzwoclg cqf1kptm kzdo7wvt osvssn79"]/div'
hostname = browser.find_element_by_xpath(hostname_xpath).text.split(' （')[0].split(' (')[0].replace("'", " ")
print(hostname)

# 下拉滑动条至底部，加载出所有好友信息
t = True
while t:
    check_height = browser.execute_script("return document.body.scrollHeight;")
    for r in range(20):
        # t = random.uniform(1, 2)
        time.sleep(2)
        browser.execute_script("window.scrollBy(0,1500)")
    check_height1 = browser.execute_script("return document.body.scrollHeight;")
    if check_height == check_height1:
        t = False

# 定位好友信息对应的元素
following_path = "//div[@class='gt60zsk1 ez8dtbzv r227ecj6 g4qalytl']/div[@class='alzwoclg jl2a5g8c o7bt71qk sl27f92c']/div"
num = 1
# print(following_path)
elements = browser.find_elements_by_xpath(following_path)
# 抓取前100个好友信息
for num in range(1, len(elements) - 1):
    item = {}
    # 获取好友名字
    namepath = following_path + "[" + str(num) + "]/div[2]/div/a/span"
    # print(namepath)
    try:
        name = browser.find_element_by_xpath(namepath).text
    except:
        name = "空"

    # 获取好友链接
    linkpath = following_path + "[" + str(num) + "]/div[2]/div/a"
    try:
        link = browser.find_element_by_xpath(linkpath).get_attribute("href")
    except:
        link = "空"
    # 将一个好友的信息组合为一个列表，追加数据库
    try:
        name = name.replace("'", " ")
        sql = "insert into fbfriends.friends values (0,\'{}\',\'{}\',\'{}\')".format(hostname, name, link)
        cursor.execute(sql)
    except:
        print(hostname + "  " + name + "  " + link)
        pass
    # time.sleep(3)
cursor.connection.commit()

#遍历friends
# url = 'https://www.facebook.com/' + hostname + '/friends'
# browser.get(url)
# t = True
# while t:
#     check_height = browser.execute_script("return document.body.scrollHeight;")
#     for r in range(20):
#         # t = random.uniform(1, 2)
#         time.sleep(1)
#         browser.execute_script("window.scrollBy(0,1500)")
#     check_height1 = browser.execute_script("return document.body.scrollHeight;")
#     if check_height == check_height1:
#         t = False
#
# # 定位好友信息对应的元素
# following_path = "//div[@class='dati1w0a ihqw7lf3 hv4rvrfc discj3wi']/div[@class='j83agx80 btwxx1t3 lhclo0ds i1fnvgqd']/div"
# num = 1
# elements = browser.find_elements_by_xpath(following_path)
# # 抓取前100个好友信息
# for num in range(1, len(elements) - 1):
#     namepath = following_path + "[" + str(num) + "]/div[2]/div/a/span"
#     f_name = browser.find_element_by_xpath(namepath).text.replace("'", " ")
#     sql2 = "select count(*) from fbfriends.friends where f_host = \'{}\' and f_name = \'{}\'".format(hostname,f_name)
#     cursor.execute(sql2)
#     res = cursor.fetchall()
#     if res[0][0]>0:
#         sql3 = "insert into fbfriends.mutual_friends values (0,\'{}\',\'{}\')".format(hostname,f_name)
#         cursor.connection.commit()
#     # cursor.connection.commit()

print('finish')
cursor.close()
# browser.close()
exit()