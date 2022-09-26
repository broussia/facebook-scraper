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
    browser.get(url)
    hostname_xpath = '//*[@class="alzwoclg cqf1kptm kzdo7wvt osvssn79"]/div'
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
    for num in range(1000):
        find = True
        posts_path = '//*[@class="bdao358l om3e55n1 g4tp4svg aeinzg81 i15ihif8 th51lws0 h07fizzr mfn553m3 jbg88c62 s9djjbeh t1fg2s7t sjylff4p poaa5t79"]/div[2]/div[' + str(
            num + 1) + ']'
        posts = browser.find_elements_by_xpath(posts_path)

        sql_post = "insert into fbfriends.posts values(0,\'{}\','null')".format(num + 1)
        cursor.execute(sql_post)
        cursor.connection.commit()
        like_class = posts_path + '//*[@class="i85zmo3j alzwoclg cgu29s5g lq84ybu9 hf30pyar"]/div'
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
            while t:
                js = 'return document.getElementsByClassName("r7ybg2qv qbc87b33 jk4gexc9 alzwoclg cqf1kptm lq84ybu9 g4tp4svg ly56v2vv h67akvdo ir1gxh3s sqler345 by1hb0a5 id4k59z1 jfw19y2w om3e55n1 b95sz57d mm05nxu8 izce65as kzemv7a0 q46jt4gp oxkhqvkx r5g9zsuq nch0832m")[0].scrollHeight;'
                js2 = 'document.getElementsByClassName("r7ybg2qv qbc87b33 jk4gexc9 alzwoclg cqf1kptm lq84ybu9 g4tp4svg ly56v2vv h67akvdo ir1gxh3s sqler345 by1hb0a5 id4k59z1 jfw19y2w om3e55n1 b95sz57d mm05nxu8 izce65as kzemv7a0 q46jt4gp oxkhqvkx r5g9zsuq nch0832m")[0].scrollTop=10000;'
                check_height = browser.execute_script(js)
                for r in range(5):
                    # t = random.uniform(1, 2)
                    time.sleep(1)
                    browser.execute_script(js2)
                check_height1 = browser.execute_script(js)
                if check_height == check_height1:
                    t = False
                pass

            # 获取点赞人信息
            like_people_xpath = '//*[@class="r7ybg2qv qbc87b33 jk4gexc9 alzwoclg cqf1kptm lq84ybu9 g4tp4svg ly56v2vv h67akvdo ir1gxh3s sqler345 by1hb0a5 id4k59z1 jfw19y2w om3e55n1 b95sz57d mm05nxu8 izce65as kzemv7a0 q46jt4gp oxkhqvkx r5g9zsuq nch0832m"]/div/div'
            like_peoples = browser.find_elements_by_xpath(like_people_xpath)
            like_num = 1

            for people in like_peoples:
                name = people.text.split('\n')[0].replace("'", " ")
                if hostname == name or name == "":
                    continue
                link_xpath = like_people_xpath + '[' + str(like_num) + ']/div/div/div/div/a'
                link = browser.find_element_by_xpath(link_xpath).get_attribute("href").split('[0]')[0]
                print(link)
                like_num += 1
                sql = "insert into fbfriends.likes values (0,\'{}\',\'{}\',\'{}\',\'{}\',false)".format(hostname, name,
                                                                                                        str(num + 1),
                                                                                                        link)
                cursor.execute(sql)
                # print(name)
            cursor.connection.commit()
            close_xpath = '//*[@class="qi72231t n3hqoq4p r86q59rh b3qcqh3k fq87ekyn fsf7x5fv s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk cr00lzj9 rn8ck1ys s3jn8y49 f14ij5to l3ldwz01 icdlwmnq i85zmo3j qmqpeqxj e7u6y3za qwcclf47 nmlomj2f frfouenu bonavkto djs4p424 r7bn319e bdao358l alzwoclg jcxyg2ei srn514ro oxkhqvkx rl78xhln nch0832m om3e55n1 jvc6uz2b g90fjkqk a5wdgl2o"]'
            close = browser.find_element_by_xpath(close_xpath)
            ActionChains(browser).click(close).perform()
            pass

        # 展开所有评论
        view_more_comment_xpath = posts_path + '//*[@class="alzwoclg lxowtz8q aeinzg81"]'
        # print(view_more_comment_xpath)
        view_more_comment = browser.find_elements_by_xpath(view_more_comment_xpath)
        times = 0
        while len(view_more_comment) > 0 and times < 5:
            for i in range(len(view_more_comment)):
                try:
                    ActionChains(browser).click(view_more_comment[i]).perform()
                except:
                    # print('点击失败')
                    pass

                time.sleep(1)
            view_more_comment = browser.find_elements_by_xpath(view_more_comment_xpath)
            times += 1
        # 获取评论信息
        comment_people_xpath = posts_path + '//*[@class="e4ay1f3w r5g9zsuq aesu6q9g q46jt4gp"]'
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
            print(comment_link)
            # c_comment = comment_content[n].text.replace("'", " ")
            sql_comment = "insert into fbfriends.comments values (0,\'{}\',\'{}\',null,\'{}\',\'{}\',false)".format(
                hostname, c_name,
                str(num + 1), comment_link)
            # print(sql_comment)
            cursor.execute(sql_comment)
            cursor.connection.commit()
    cursor.close()
    browser.close()


# exit()
