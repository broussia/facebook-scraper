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

browser = chrome_setting()

# 设置数据库
cursor = db_settings()
# 访问facebook网页
login(browser)

# 好友列表结构：#https://www.facebook.com/kene.shadrack.79

host = 'antony.olentiati'
# Wang.Dingyuan
# kene.shadrack.79
url = 'https://www.facebook.com/' + host
browser.get(url)
hostname_xpath = '//*[@class="j83agx80 cbu4d94t obtkqiv7 sv5sfqaa"]/div'
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
    posts_path = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div'
    posts = browser.find_elements_by_xpath(posts_path)
    sql_post = "insert into fbfriends.posts values(0,\'{}\','null')".format(num + 1)
    cursor.execute(sql_post)
    cursor.connection.commit()
    like_class = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div[' + str(
        num + 1) + ']//*[@class="bzsjyuwj ni8dbmo4 stjgntxs ltmttdrg gjzvkazv"]'
    browser.execute_script("window.scrollBy(0,500)")
    like = browser.find_elements_by_xpath(like_class)
    if len(like) == 0:
        print("本篇无人点赞，跳过")
        find = False
    if find:
        ActionChains(browser).click(like[0]).perform()
        time.sleep(1)
        # 滚动点赞页面（暂未完成）
        t = True
        while t:
            js = 'return document.getElementsByClassName("rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 du4w35lb q5bimw55 ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 l9j0dhe7 kh7kg01d eg9m0zos c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso")[0].scrollHeight;'
            js2 = 'document.getElementsByClassName("rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 du4w35lb q5bimw55 ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 l9j0dhe7 kh7kg01d eg9m0zos c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso")[0].scrollTop=10000;'
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
        like_people_xpath = '//*[@class="l9j0dhe7 du4w35lb cjfnh4rs j83agx80 cbu4d94t lzcic4wl ni8dbmo4 stjgntxs oqq733wu cwj9ozl2 io0zqebd m5lcvass fbipl8qg nwvqtn77 nwpbqux9 iy3k6uwz e9a99x49 g8p4j16d bv25afu3 gc7gaz0o k4urcfbm"]/div[3]/div[1]/div'
        like_peoples = browser.find_elements_by_xpath(like_people_xpath)

        for people in like_peoples:
            name = people.text.split('\n')[0].replace("'", " ")
            if hostname == name:
                continue
            sql = "insert into fbfriends.likes values (0,\'{}\',\'{}\',\'{}\')".format(hostname, name, str(num + 1))
            cursor.execute(sql)
            # print(name)
        cursor.connection.commit()
        close_xpath = '//*[@class="oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn s45kfl79 emlxlaya bkmhp75w spb7xbtv rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv j83agx80 taijpn5t jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 tv7at329 thwo4zme tdjehn4e"]'
        close = browser.find_element_by_xpath(close_xpath)
        ActionChains(browser).click(close).perform()
        pass
    # 展开所有评论
    view_more_comment_xpath = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div[' + str(
        num + 1) + ']//*[@class="j83agx80 fv0vnmcu hpfvmrgz"]'
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
    comment_people_xpath = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div[' + str(
        num + 1) + ']//*[@class="pq6dq46d"]'
    comment_people = browser.find_elements_by_xpath(comment_people_xpath)
    comment_content_xpath = '//*[@class="rq0escxv l9j0dhe7 du4w35lb hpfvmrgz g5gj957u aov4n071 oi9244e8 bi6gxh9e h676nmdw aghb5jc5 gile2uim pwa15fzy fhuww2h9"]/div[2]/div[' + str(
        num + 1) + ']//*[@class="ecm0bbzt e5nlhep0 a8c37x1j"]'
    # comment_content = browser.find_elements_by_xpath(comment_content_xpath)
    # if len(comment_people) > 0:
    #     print()
    #     print(comment_content[0].text)
    for n in range(len(comment_people)):
        c_name = comment_people[n].text.replace("'", " ")
        # c_comment = comment_content[n].text.replace("'", " ")
        sql_comment = "insert into fbfriends.comments values (0,\'{}\',\'{}\',\'null\',\'{}\')".format(hostname, c_name,
                                                                                                       str(num + 1))
        # print(sql_comment)
        cursor.execute(sql_comment)
        cursor.connection.commit()
cursor.close()
# browser.close()
exit()
