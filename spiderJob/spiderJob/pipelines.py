# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


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


class SpiderjobPipeline2(object):
    def process_item(self, item, spider):
        return {
            't1': '岗位:'+item['t1'],
            't2': '公司:'+item['t2'],
            't3': '地区:'+item['t3'],
            't4': '薪资:'+item['t4'],
        }

    # spider (Spider 对象) – 被开启的spider
    # 可选实现，当spider被开启时，这个方法被调用。
    # def open_spider(self, spider):

    # spider (Spider 对象) – 被关闭的spider
    # 可选实现，当spider被关闭时，这个方法被调用
    # def close_spider(self, spider):
