import random
from module.getIp import getAgentIp
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
        txt = aggregate.find({'$or':[{'content': {"$exists": False}}, {'content': 'None'}]})
        list = [];
        for each in txt:
            if each['link'] != '':
                list.append(each['link'])
        return list
    # 插入一条数据
    # @param emp 集合名称
    # @param obj 数据对象
    def write(self,aggregate,obj):
        aggregate.update(
            {
                'title': obj['title'],
            },
            {'$set': {
                'link': obj['link'],
                'pagenum': obj['pagenum'],
                'create_time': obj['create_time'],
                'spider_data.' + str(obj['last_spider_data']): obj['spider_data'][
                    str(obj['last_spider_data'])],
                'last_spider_data': obj['last_spider_data']
            }},
            upsert=True
        )
    def writeDetail(self,aggregate,obj):
        aggregate.update(
            {
                'link': obj['link'],
            },
            {'$set': {
                'content': obj['content'],
            }},
        )

    # 删除文档
    # @param emp 集合名称
    # @param obj 数据对象
    def delete(self,aggregate, obj):
        aggregate.delete_many(obj)

handleData = handleData()