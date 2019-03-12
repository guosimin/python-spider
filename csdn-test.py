# 用于做随机header
import fake_useragent
from fake_useragent import UserAgent

# 基础包等,模拟请求，多线程
import requests,threading,datetime,time
from bs4 import BeautifulSoup
import random

# 用于数据库存储
import pymongo
from pymongo import MongoClient

# 正则
import re

#1.链接本地数据库服务
name = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = name.demo   #demo数据库名
# 3.创建，连接集合
emp = db.employees  # employees集合名
page = db.page # page集合名
# ------------------------------------------------------函数--------------------------------------------------------

# 读取文档（随机返回数据库中的一个ip）
def read():
    txt = emp.find()
    list = [];
    for each in txt:
        if each['ip']!= '':
            list.append(each['ip'])
    ip = random.choice(list)
    return ip

# 写入一条数据到文档
# @param obj 数据对象
def write(obj):
    page.insert_one(obj)


# 删除文档
# @param emp 集合名称
# @param obj 数据对象
def delete(emp,obj):
    emp.delete_many(obj)

# 获取随机头部
def getHeader():
    newUserAgent = UserAgent().random;
    headers = {'User-Agent': newUserAgent}
    return headers

# 计算时间差,格式: 时分秒
# @param start 开始时间
# @param end 结束时间
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff

def findip(pagenum): # ip类型,页码,目标url,存放ip的路径
    url=str("https://blog.csdn.net/github_39570717/article/list/")+str(pagenum) # 配置url
    headers = getHeader() # 定制请求头
    # 获取代理ip
    ip = read()
    # 代理ip
    proxies = {"http": "http://" + ip, "https": "http://" + ip}

    # 打印出当前用于请求的ip 和请求地址
    print(ip)
    print(url)
    try:
        request= requests.get(url=url,proxies=proxies,headers=headers,timeout=4)
        print(request)
        if request.status_code!= 200 :
            return False
        html = request.text
        soup = BeautifulSoup(html,'lxml')
        all=soup.find_all('div',class_='article-item-box')
        index = 0;
        for i in all:
            if index != 0:
                t=i.find('h4')
                title = t.text
                title = re.sub(r'[(原|译|转)(\s+)]+', '', title, 1)
                title = re.sub(r'\s+$', '', title);
                read_num = i.find_all(class_ ='num')
                a = i.find('a')
                # 创建日期转成时间戳保存
                original = i.find(attrs={'class':'date'})
                original = original.text
                create_date = time.strptime(original, "%Y-%m-%d %H:%M:%S")
                create_date = time.mktime(create_date)
                write({
                    'title':title,
                    'pagenum':pagenum,
                    'read_num':read_num[0].text,
                    'comment_num':read_num[1].text,
                    'link':a['href'],
                    'create_date':create_date,
                    'original_create_date':original
                })
                print(title)
            index =index+1
    except:
        print('失败了,删除ip' + ip)
        # 删除失效ip
        delete(emp,{'ip': ip})
        # 重新从数据库去除ip执行
        findip(pagenum)
        return False

def getip():
    delete(page,{})
    start = datetime.datetime.now()  # 开始时间
    threads = []
    # 开启4条线程来爬取
    for pagenum in range(4):
        t = threading.Thread(target=findip, args=(pagenum + 1,))
        threads.append(t)
    for s in threads:  # 开启多线程爬取
        s.start()
    for e in threads:  # 等待所有线程结束
        e.join()
    print('爬取完成')
    end = datetime.datetime.now()  # 结束时间
    diff = gettimediff(start, end)  # 计算耗时
    # ips = read(path)  # 读取爬到的ip数量
    # print('一共爬取代理ip: %s 个,共耗时: %s \n' % (len(ips), diff))



if __name__ == '__main__':
    getip()