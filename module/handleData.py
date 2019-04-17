import random
from module.getIp import getAgentIp
#日志
import logging
logger = logging.getLogger('【data-logger】')
# 级别高低顺序：NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('run.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

class handleData:
    # 返回随机ip
    def getIp(self,aggregate,index=0):
        try:
            txt = aggregate.find()
            list = [];
            for each in txt:
                if each['ip'] != '':
                    list.append(each['ip'])
                    if len(list)>0:
                        ip = random.choice(list)
                    else:
                        self.getIp(self, aggregate, 1)
            return ip
        except:
            getAgentIp()
            if index == 0:
                self.getIp(self, aggregate,1)
            else:
                return ''

    def needGetContentLinks(self,aggregate):
        txt = aggregate.find({'$or':[{'content': {"$exists": False}}, {'content': 'None'}, {'content': ''}]})
        list = [];
        for each in txt:
            if each['link'] != '':
                list.append(each['link'])
        return list
    def writeUser(self,aggregate,obj):
        try:
            aggregate.update(
                {
                     "user_name":obj['user_name'],
                },
                {'$set': {
                    "user_url": obj['user_url'],
                    "avatar": obj['avatar']
                }},
                upsert=True
            )
        except:
            logger.error('用户资料写入失败')

    # 插入一条数据
    # @param emp 集合名称
    # @param obj 数据对象
    def write(self,aggregate,spiderAggregate,obj):
        try:
            aggregate.update(
                {
                    'page_id': obj['page_id'],
                    'user_name': obj['user_name'],
                    'link': obj['link'],
                },
                {'$set': {
                    'title': obj['title'],
                    'pagenum': obj['pagenum'],
                    'create_time': obj['create_time'],
                    'last_spider_date': obj['last_spider_date']
                }},
                upsert=True
            )
        except:
            logger.error('文章基本信息写入失败')
        try:
            spiderAggregate.update(
                {
                    'user_name': obj['user_name'],
                    'page_id': obj['page_id'],
                    'spider_date':obj['last_spider_date'],
                },
                {'$set': {
                    'read_num':int(obj['read_num']),
                    'comment_num':int(obj['comment_num'])
                }},
                upsert=True
            )
        except:
            logger.error('爬虫基本信息写入失败')
    def writeDetail(self,aggregate,obj):
        try:
            aggregate.update(
                {
                    'link': obj['link'],
                },
                {'$set': {
                    'content': obj['content'],
                }},
            )
        except:
            logger.error('详情写入失败')

    def getUser(self,aggreate):
        list = [];
        try:
            txt = aggreate.find({})
            for each in txt:
                if each['user_name'] != '':
                    list.append(each['user_name'])
        except:
            logger.error('获取用户资料失败')
        return list
    # 删除文档
    # @param emp 集合名称
    # @param obj 数据对象
    def delete(self,aggregate, obj):
        try:
            aggregate.delete_many(obj)
        except:
            logger.error('删除失败')

handleData = handleData()