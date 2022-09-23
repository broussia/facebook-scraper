from catchComment import catchComments
from catchFriends import catchFriends
from utils import chrome_setting, db_settings, login

# 设置数据库
cursor = db_settings()
# 访问facebook网页

sql_getHosts = "select name,h_link from fbfriends.hosts"
cursor.execute(sql_getHosts)
hosts = cursor.fetchall()
browser = chrome_setting()
login(browser)
for host in hosts:
    print(host[0])
    catchFriends(host[1], browser, cursor)
    catchComments(host[1], browser, cursor)
