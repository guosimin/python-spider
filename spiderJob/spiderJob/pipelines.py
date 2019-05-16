# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 用于数据库存储
import pymongo
from pymongo import MongoClient
#1.链接本地数据库服务
name = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = name.demo   #demo数据库名
# 3.创建，连接集合
job = db.gsm_job  # gsm_job集合

#保存为txt
class SpiderjobPipeline(object):
    # 可选实现，做参数初始化等
    def __init__(self):
        print("//////////////")

    # item (Item 对象) – 被爬取的item
    # spider (Spider 对象) – 爬取该item的spider
    # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
    # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
    def process_item(self, item, spider):
        fileName = 'aa.txt'  # 定义文件名
        if str(item['t1'])=='None':
            return item;
        with open(fileName, "a+", encoding='utf-8') as f:
            f.write('\n')  # ‘\n’ 表示换行
            item = str(item['t1']) + "," + str(item['t2']) + "," + str(item['t3']) + "," + str(item['t4'])
            f.write(item)
            # f.write('标签：' + tags)
            f.write('\n-------\n')
            f.close()
        return item


#保存数据到数据库
class Save(object):
    def process_item(self, item, spider):
        job.update(
            {
                'id': item['id'],
            },
            {'$set': {
                'position_link': item['positionLink'],
                'company_link':item['companyLink'],
                'position': item['t1'],
                'company': item['t2'],
                'region': item['t3'],
                'salary': item['t4']
            }},
            upsert=True
        )
        return item

