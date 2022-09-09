#数据库中操作


# insert into csvnode (label)
# select i_host from intimacy;
#
# insert into csvnode(label)
# select i_name from intimacy
# ON DUPLICATE KEY UPDATE label = i_name;
#
# insert into csvedge(source_name,target_name,weight)
# select i_host ,i_name ,total_score weight from intimacy;
#
# update csvedge,csvnode set source = id where source_name = label;
#
# update csvedge,csvnode set target = id where target_name = label;

#数据库导出csv
