from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
import time
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
    print("*******"+url+"******")
    browser.get(url)
    hostname_xpath = '//*[@class="x78zum5 xdt5ytf x1wsgfga x9otpla"]/div'
    hostname = browser.find_element_by_xpath(hostname_xpath).text.split(' （')[0].split(' (')[0].replace("'", " ")
    # print(hostname)
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
        posts_path = '//*[@class="x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv"]/div[2]/div[' + str(
            num + 1) + ']'
        posts = browser.find_elements_by_xpath(posts_path)

        sql_post = "insert into fbfriends.posts values(0,\'{}\','null')".format(num + 1)
        cursor.execute(sql_post)
        cursor.connection.commit()
        like_class = posts_path + '//*[@class="x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62"]/div'
        browser.execute_script("window.scrollBy(0,500)")
        like = browser.find_elements_by_xpath(like_class)
        if len(like) == 0:
            print("本篇无人点赞，跳过")
            find = False
        if find:
            # print(like_class)
            ActionChains(browser).click(like[0]).perform()
            time.sleep(1)
            # 滚动点赞页面
            t = True
            fail_times = 0;
            while t:
                time.sleep(1)
                js = 'return document.getElementsByClassName("xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd")[0].scrollHeight;'
                js2 = 'document.getElementsByClassName("xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd")[0].scrollTop=10000;'
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
                    print("下滑失败，重试中")
                    fail_times += 1
                    if fail_times > 3:
                        fail_times = 0
                        break
                    time.sleep(3)

            # 获取点赞人信息
            like_people_xpath = '//*[@class="xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd"]/div/div'
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
            close_xpath = '//*[@class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1"]'
            close = browser.find_element_by_xpath(close_xpath)
            ActionChains(browser).click(close).perform()
            pass

        # 展开所有评论
        view_more_comment_xpath = posts_path + '//*[@class="x78zum5 x1w0mnb xeuugli"]'
        # print(view_more_comment_xpath)
        view_more_comment = browser.find_elements_by_xpath(view_more_comment_xpath)
        times = 0
        while len(view_more_comment) > 0 and times < 5:
            for i in range(len(view_more_comment)):
                try:
                    ActionChains(browser).click(view_more_comment[i]).perform()
                except:
                    print('点击失败')
                    pass

                time.sleep(1)
            view_more_comment = browser.find_elements_by_xpath(view_more_comment_xpath)
            times += 1
        # 获取评论信息
        comment_people_xpath = posts_path + '//*[@class="x1ye3gou xwib8y2 xn6708d x1y1aw1k"]'
        # print(comment_people_xpath)
        comment_people = browser.find_elements_by_xpath(comment_people_xpath)
        comment_link_xpath = comment_people_xpath + '/span/a'
        comment_links = browser.find_elements_by_xpath(comment_link_xpath)

        # comment_content_xpath = posts_path + '//*[@class="d2hqwtrz o9wcebwi b6ax4al1"]'
        # print(comment_content_xpath)
        # comment_content = browser.find_elements_by_xpath(comment_content_xpath)
        # if len(comment_people) > 0:
        #     print()
        #     print(comment_content[0].text)
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
