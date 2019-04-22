"""
获取csdn用户资料

"""
import sys
import json
sys.path.append(r'E:\projects\python-spider')
from csdnTest import *


#1.链接本地数据库服务
name = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = name.demo   #demo数据库名
# 3.创建，连接集合
emp = db.employees  # employees集合名
user = db.csdn_users # page集合名

# 爬取‘前端’模块
category = 'web'
headers = getHeader()  # 定制请求头

#开启多线程
def openThread():
    return False;

def getData(proxies,shown_offset):
    url = 'https://blog.csdn.net/api/articles?type=more&category=' + category+'&shown_offset='+shown_offset
    print("当前访问的url:" + url + ",访问的proxies:" + str(proxies))
    try:
        request = requests.get(url=url, proxies=proxies, headers=headers, timeout=4)
        if request.status_code != 200:
            print('200')
            return False
    except:
        print('3333')
        return False

    content = json.loads(request.content)
    shownOffset = str(content['shown_offset'])
    print(shownOffset)
    all = content['articles']
    list = []
    for each in all:
        print(each['user_name'])
        handleData.writeUser(user, {
            "user_name": each['user_name'],
            "user_url": each['user_url'],
            "avatar": each['avatar']
        })
    sleepTime = random.choice([3,4,5,6]);
    time.sleep(sleepTime)
    getData(proxies, shownOffset)

def start():
    url = 'https://blog.csdn.net/nav/'+category
    ip = handleData.getIp(emp)
    # 代理ip
    proxies = {"http": "http://" + ip, "https": "http://" + ip}
    print("当前访问的url:" + url + ",访问的ip:" + ip)
    try:
        request = requests.get(url=url, proxies=proxies, headers=headers, timeout=4)
        if request.status_code != 200:
            return False
        text = request.text
        soup = BeautifulSoup(text, 'lxml')
        content = soup.find('ul', class_='feedlist_mod')
        shownOffset = str(content['shown-offset'])

    except:
        print('失败了,删除ip' + ip)
        # 删除失效ip
        handleData.delete(emp, {'ip': ip})
        start()
        return False
    getData(proxies, shownOffset)


if __name__ == '__main__':
    start()