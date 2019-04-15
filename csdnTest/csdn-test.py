import sys
sys.path.append(r'E:\projects\python-spider')
from csdnTest import *

#1.链接本地数据库服务
name = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = name.demo   #demo数据库名
# 3.创建，连接集合
emp = db.employees  # employees集合名
page = db.page # page集合名
spider = db.page_spider_data # 爬取数据集合
users = db.csdn_users # 爬取数据集合


logger = logging.getLogger('mylogger')
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

# ------------------------------------------------------函数--------------------------------------------------------
def openFindDetailThread(links):
    threads = []
    for pagenum in range(len(links)):
        t = threading.Thread(target=findDetail, args=(links[pagenum],0))
        threads.append(t)
    for s in threads:  # 开启多线程爬取
        s.start()
    for e in threads:  # 等待所有线程结束
        e.join()

def findDetail(link,index):
    url = link
    headers = getHeader()  # 定制请求头
    ip = handleData.getIp(emp)
    # 代理ip
    proxies = {"http": "http://" + ip, "https": "http://" + ip}
    # print("当前访问的url:" + url + ",访问的ip:" + ip);
    logger.info("当前访问的url:" + url + ",访问的ip:" + ip)
    try:
        request = requests.get(url=url, proxies=proxies, headers=headers, timeout=4)
        if request.status_code != 200:
            logger.info("【!200】url:"+url)
            return False
    except:
        logger.info("【网络错误】url："+url+"访问失败，可以遇上验证了")
        if (index==5):
            logger.info("【爬取失败】url：" + url + "进行5次后依然爬取失败")
            logger.error("【error】"+url+'爬取详情失败')
            return False
        else:
            index = index+1 if index==1 else 1
            time.sleep(5)
            logger.info("url:"+url+"进行第"+index+"次尝试")
            findDetail(link ,index)

    try:
        text = request.text
        soup = BeautifulSoup(text, 'lxml')
        content = soup.find('div', class_='blog-content-box')
        content = html.escape(str(content))
        handleData.writeDetail(page, {
            'link': link,
            'content': content
        })
    except:
        logger.error("【error】" + url+'读取数据失败')


def findTitle(pagenum,retryNum = 0): # ip类型,页码,目标url,存放ip的路径
    userName = handleData.getUser(users)
    url=str("https://blog.csdn.net/"+userName[0]+"/article/list/")+str(pagenum) # 配置url
    headers = getHeader() # 定制请求头
    # 获取代理ip
    ip = handleData.getIp(emp)
    if ip=='':
        logger.error("爬取代理ip失败");
        return  False
    # 代理ip
    proxies = {"http": "http://" + ip, "https": "http://" + ip}
    # 打印出当前用于请求的ip 和请求地址
    logger.info("当前访问的url:"+url+",访问的ip:"+ip);
    try:
        request= requests.get(url=url,proxies=proxies,headers=headers,timeout=4)
        if request.status_code!= 200 :
            logger.info("【!200】url:" + url)
            return False
    except:
        logger.info('失败了,删除ip' + ip)
        # 删除失效ip
        handleData.delete(emp,{'ip': ip})
        # 重新从数据库去除ip执行
        findTitle(pagenum)
        return False

    try:
        html = request.text
        soup = BeautifulSoup(html, 'lxml')
        all = soup.find_all('div', class_='article-item-box')
        index = 0
        spider_date = datetime.datetime.now()
        spider_date = spider_date.strftime('%Y%m%d')
        links = []
        for i in all:
            index = index + 1
            if index != 1:
                # 获取标题
                t = i.find('h4')
                title = t.text
                title = re.sub(r'[(原|译|转)(\s+)]+', '', title, 1)
                title = re.sub(r'\s+$', '', title)

                # 获取阅读数
                read_num = i.find_all(class_='num')

                # 获取链接
                a = i.find('a')

                # 创建日期转成时间戳保存
                original = i.find(attrs={'class': 'date'})
                original = original.text
                create_time = time.strptime(original, "%Y-%m-%d %H:%M:%S")
                create_time = time.strftime("%Y%m%d", create_time)
                links.append(a['href'])

                # 获取文章id
                pageId = (a['href'].split('/'))[-1]
                try:
                    handleData.write(page, spider, {
                        'title': title,
                        'pagenum': pagenum,
                        'link': a['href'],
                        'create_time': create_time,
                        'last_spider_date': str(spider_date),
                        'user_name': userName[0],
                        'page_id': pageId,
                        'read_num': read_num[0].text,
                        'comment_num': read_num[1].text,
                    })
                    logger.info("写入成功：" + title)
                except:
                    logger.info("写入失败")
        if (index > 0):
            findTitle(pagenum + 1)
        else:
            # 重新尝试，确认是否最后一页
            if(retryNum==0):
                time.sleep(2)
                findTitle(pagenum,1)
            else:
                logger.info("最后一页是：" + str(pagenum - 1))
            return False
    except:
        logger.info("url"+url+"读取或写入失败")
        return False

def getip():
    start = datetime.datetime.now()  # 开始时间
    threads = []
    # 先开始1条线程来爬取
    t = threading.Thread(target=findTitle, args=(1,))
    t.start()
    t.join()

    # 爬取文章内容（如果内容为空或者None才爬取）
    links = handleData.needGetContentLinks(page);
    openFindDetailThread(links)

    logger.info('爬取完成')
    end = datetime.datetime.now()  # 结束时间
    diff = gettimediff(start, end)  # 计算耗时
    logger.info('一共耗时: %s \n' % (diff))



if __name__ == '__main__':
    getip()