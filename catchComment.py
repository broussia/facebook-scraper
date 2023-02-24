from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
import time
import configparser

import pandas as pd
import xlsxwriter
import json
import pymysql
import os

from utils import chrome_setting, db_settings, login, tobuttom, totop

# browser = chrome_setting()
#
# # 设置数据库
# cursor = db_settings()
# # 访问facebook网页
# login(browser)

# 好友列表结构：#https://www.facebook.com/kene.shadrack.79

host = 'kook.wanwisa.1'


# Wang.Dingyuan
# kene.shadrack.79
def catchComments(url, browser, cursor):

    config = configparser.ConfigParser()
    path = 'xpaths.ini'
    config.read(path)

    print("*******"+url+"******")
    browser.get(url)
    # hostname_xpath = '//*[@class="x78zum5 xdt5ytf x1wsgfga x9otpla"]/div'
    hostname_xpath = config.get('common', 'hostname_xpath')
    hostname = browser.find_element_by_xpath(hostname_xpath).text.split(' （')[0].split(' (')[0].replace("'", " ")
    print(hostname)
    # 下拉滑动条至底部，加载出所有好友信息
    # tobuttom(browser)

    # totop(browser)

    # 设置缩放比例
    # browser.execute_script("document.body.style.zoom='0.25';")

    # posts_path = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div'
    # posts = browser.find_elements_by_xpath(posts_path)
    # like_class = '//*[@class="bzsjyuwj ni8dbmo4 stjgntxs ltmttdrg gjzvkazv"]'
    # like = browser.find_elements_by_xpath(like_class)

    # num = 0
    for num in range(100):
        find = True
        posts_path = config.get('catchComments', 'posts_path') + str(num + 1) + ']'
        print(posts_path)
        posts = browser.find_elements_by_xpath(posts_path)

        sql_post = "insert into fbfriends.posts values(0,\'{}\','null')".format(num + 1)
        cursor.execute(sql_post)
        cursor.connection.commit()
        like_class_xpath = posts_path + config.get('catchComments', 'like_class_xpath')
        browser.execute_script("window.scrollBy(0,500)")
        like = browser.find_elements_by_xpath(like_class_xpath)
        if len(like) == 0:
            # browser.save_screenshot('/root/facebook-scraper/screenshots/failOn'+str(num)+'.png')
            print("本篇无人点赞，跳过  "+like_class_xpath)
            find = False
        if find:
            # print(like_class)
            try:
                ActionChains(browser).click(like[0]).perform()
                time.sleep(1)
            except:
                continue
            # 滚动点赞页面
            t = True
            fail_times = 0;
            failtoslip = False
            while t:
                time.sleep(1)
                like_box_xpath = config.get('catchComments', 'like_box_xpath')
                js = 'return document.getElementsByClassName("'+like_box_xpath+'")[0].scrollHeight;'
                js2 = 'document.getElementsByClassName("'+like_box_xpath+'")[0].scrollTop=10000;'
                try:
                    check_height = browser.execute_script(js)
                    for r in range(5):
                        # t = random.uniform(1, 2)
                        time.sleep(1)
                        browser.execute_script(js2)
                    check_height1 = browser.execute_script(js)
                    if check_height == check_height1:
                        t = False
                    pass
                except:
                    # print("下滑失败，重试中")
                    fail_times += 1
                    if fail_times > 3:
                        fail_times = 0
                        failtoslip = True
                        break
                    time.sleep(3)
            if failtoslip:
                print("下滑失败")
                continue
            # 获取点赞人信息
            like_people_xpath = config.get('catchComments', 'like_people_xpath')
            like_peoples = browser.find_elements_by_xpath(like_people_xpath)
            like_num = 1

            for people in like_peoples:
                name = people.text.split('\n')[0].replace("'", " ")
                if hostname == name or name == "":
                    continue
                link_xpath = like_people_xpath + '[' + str(like_num) + ']/div/div/div/div/a'
                link = browser.find_element_by_xpath(link_xpath).get_attribute("href").split('[0]')[0]
                print("like link: "+link)
                like_num += 1
                sql = "insert into fbfriends.likes values (0,\'{}\',\'{}\',\'{}\',\'{}\',false)".format(hostname, name,
                                                                                                        str(num + 1),
                                                                                                        link)
                cursor.execute(sql)
                # print(name)
            cursor.connection.commit()
            like_close_xpath = config.get('catchComments', 'like_close_xpath')
            try:
                close = browser.find_element_by_xpath(like_close_xpath)
            except:
                browser.save_screenshot('login_file.png')
            ActionChains(browser).click(close).perform()
            pass

        # 展开所有评论
        view_more_comment_xpath = posts_path + config.get('catchComments', 'view_more_comment_xpath')
        # print(view_more_comment_xpath)
        try:
            view_more_comment = browser.find_element_by_xpath(view_more_comment_xpath)
            ActionChains(browser).click(view_more_comment).perform()
        except:
            print('点击失败或没有评论')
            continue

        time.sleep(1)
        # view_more_comment = browser.find_elements_by_xpath(view_more_comment_xpath)
        # 获取评论信息
        comment_people_xpath = config.get('catchComments', 'comment_people_xpath')
        # print(comment_people_xpath)
        comment_people = browser.find_elements_by_xpath(comment_people_xpath)
        comment_link_xpath = comment_people_xpath + '/div/span/a'
        comment_links = browser.find_elements_by_xpath(comment_link_xpath)

        for n in range(len(comment_people)):
            c_name = comment_people[n].text.replace("'", " ")
            if len(c_name.split("\n")) > 1:
                if c_name.__contains__("作者"):
                    c_name = c_name.split("\n")[1]
                else:
                    c_name = c_name.split("\n")[0]
            if c_name == "":
                continue
            comment_link = comment_links[n].get_attribute("href").split('[0]')[0]
            print("comment link : "+comment_link)
            # c_comment = comment_content[n].text.replace("'", " ")
            sql_comment = "insert into fbfriends.comments values (0,\'{}\',\'{}\',null,\'{}\',\'{}\',false)".format(
                hostname, c_name,
                str(num + 1), comment_link)
            # print(sql_comment)
            cursor.execute(sql_comment)
            cursor.connection.commit()
    # cursor.close()
    # browser.close()


# exit()
