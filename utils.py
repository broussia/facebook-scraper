from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import pandas as pd
import xlsxwriter
import json
import pymysql
import os


# 设置浏览器
def chrome_setting():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {'notifications': 2}  # 禁止谷歌浏览器弹出通知消息
    }
    options.add_experimental_option('prefs', prefs)
    # options.binary_location = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    # linux环境
    # browser = webdriver.Chrome(r"/root/facebook-scraper/facebook-scraper/chromedriver",chrome_options=options)

    # win环境
    browser = webdriver.Chrome(r"D:\programs\chromedriver.exe")
    browser.maximize_window()  # 浏览器窗口最大化
    browser.implicitly_wait(10)
    return browser


# 设置数据库
def db_settings():
    # 设置数据库 win环境
    fbDB = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        charset="utf8mb4",
        database="fbfriends"
    )
    #Linux环境
    fbDB = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        charset="utf8",
        database="fbfriends"
    )
    cursor = fbDB.cursor()
    return cursor


#登录操作
def login(browser):
    try:
        browser.get('https://www.facebook.com/login.php?login_attempt=1&lwv=110/')
        time.sleep(2)
    # 如果打开facebook页面失败，则尝试重新加载
    except:
        # 鼠标移动到 ac 位置并单击
        ac = browser.find_element_by_id('reload-button')
        ActionChains(browser).move_to_element(ac).click(ac).perform()
        # self.browser.find_element_by_id('reload-button').click()
        print('重新刷新页面~')
        time.sleep(2)

    # 输入账户密码
    browser.find_element_by_id('email').clear()
    browser.find_element_by_id('email').send_keys('leopshk@outlook.com')
    browser.find_element_by_id('pass').clear()
    browser.find_element_by_id('pass').send_keys('aa112211')
    # 模拟点击登录按钮，两种不同的点击方法
    try:
        browser.find_element_by_xpath('//button[@id="loginbutton"]').send_keys(Keys.ENTER)
    except:
        browser.find_element_by_xpath('//input[@tabindex="4"]').send_keys(Keys.ENTER)
        browser.find_element_by_xpath('//a[@href="https://www.facebook.com/?ref=logo"]').send_keys(Keys.ENTER)
    time.sleep(2)


def tobuttom(browser):
    t = True
    while t:
        check_height = browser.execute_script("return document.body.scrollHeight;")
        for r in range(2):
            # t = random.uniform(1, 2)
            time.sleep(1)
            browser.execute_script("window.scrollBy(0,1500)")
        check_height1 = browser.execute_script("return document.body.scrollHeight;")
        if check_height == check_height1:
            t = False


def totop(browser):
    t = True
    while t:
        check_height = 0
        for r in range(10):
            # t = random.uniform(1, 2)
            time.sleep(2)
            browser.execute_script("window.scrollBy(1500,0)")
        check_height1 = browser.execute_script("return document.body.scrollHeight;")
        if check_height == check_height1:
            t = False