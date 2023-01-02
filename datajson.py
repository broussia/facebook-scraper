import json
import pymysql
import os

from utils import db_settings

score = 1
categories = []
nodes = []
links = []
names = []

cursor = db_settings()

sql_get_host = "select h_name,h_link from fbfriends.hosts"
cursor.execute(sql_get_host)
hosts = cursor.fetchall()
now = 0
for host in hosts:
    # print (host)
    categories.append({'name': host[0]})
    nodes.append({'name': host[0],
                  'symbolSize': 100,
                  'category': now,
                  'weblink': host[1]
                  })
    names.append(host[0])
    now += 1

now = 0
for host in hosts:
    # print (host)
    sql_get_nodes_and_links = "select i_name,total_score,i_link from fbfriends.intimacy where total_score >= {} and i_host = \'{}\' ".format(
        score, host[0])
    # print(sql_get_nodes_and_links)
    cursor.execute(sql_get_nodes_and_links)
    contents = cursor.fetchall()
    for content in contents:
        i_name = content[0]
        total_score = content[1]
        link = content[2]
        hasname = False
        for name_judge in names:
            if i_name == name_judge:
                hasname = True
        if not hasname:
            nodes.append({'name': i_name,
                          'symbolSize': 50,
                          'category': now,
                          'weblink': link})
            names.append(i_name)

        links.append({'source': host[0],
                      'target': i_name,
                      'name': total_score})
    now += 1

total_json = {'categories': categories,
              'nodes': nodes,
              'links': links}
file = 'data.json'
# categories_file = 'data/categories.json'
# nodes_file = 'data/nodes.json'
# links_file = 'data/links.json'
with open(file, 'w', encoding='utf-8') as fw:
    # print(total_json)
    # jsonstr = json.dumps(total_json)
    json.dump(total_json, fw, indent=4, ensure_ascii=False)
# with open(categories_file, 'w', encoding='utf-8') as fw:
#     jsonstr = json.dumps(categories)
#     json.dump(jsonstr, fw, indent=4, ensure_ascii=False)
# with open(nodes_file, 'w', encoding='utf-8') as fw:
#     jsonstr = json.dumps(nodes)
#     json.dump(jsonstr, fw, indent=4, ensure_ascii=False)
# with open(links_file, 'w', encoding='utf-8') as fw:
#     jsonstr = json.dumps(links)
#     json.dump(jsonstr, fw, indent=4, ensure_ascii=False)
