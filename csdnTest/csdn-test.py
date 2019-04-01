from csdnTest import *

#1.链接本地数据库服务
name = MongoClient('localhost')
#2.链接本地数据库 demo 没有会创建
db = name.demo   #demo数据库名
# 3.创建，连接集合
emp = db.employees  # employees集合名
page = db.page # page集合名
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
    print("当前访问的url:" + url + ",访问的ip:" + ip);
    try:
        request = requests.get(url=url, proxies=proxies, headers=headers, timeout=4)
        if request.status_code != 200:
            return False
        text = request.text
        soup = BeautifulSoup(text, 'lxml')
        content = soup.find('div',class_='blog-content-box')
        content = html.escape(str(content))
        handleData.writeDetail(page, {
           'link':link,
           'content':content
        })
    except:
        if (index==5):
            # handleData.writeDetail(page, {
            #     'link': link,
            #     'content': 'None'
            # })
            return False
        else:
            index = index+1 if index==1 else 1
            findDetail(link ,index)


def findTitle(pagenum): # ip类型,页码,目标url,存放ip的路径
    url=str("https://blog.csdn.net/github_39570717/article/list/")+str(pagenum) # 配置url
    headers = getHeader() # 定制请求头
    # 获取代理ip
    ip = handleData.getIp(emp)
    if ip=='':
        print("爬取代理ip失败");
        return  False
    # 代理ip
    proxies = {"http": "http://" + ip, "https": "http://" + ip}
    # 打印出当前用于请求的ip 和请求地址
    print("当前访问的url:"+url+",访问的ip:"+ip);
    try:
        request= requests.get(url=url,proxies=proxies,headers=headers,timeout=4)
        if request.status_code!= 200 :
            return False
        html = request.text
        soup = BeautifulSoup(html,'lxml')
        all=soup.find_all('div',class_='article-item-box')
        index = 0;
        spider_date = datetime.datetime.now()
        spider_date = spider_date.strftime('%Y%m%d')
        links = []
        for i in all:
            if index != 0:
                # 获取标题
                t=i.find('h4')
                title = t.text
                title = re.sub(r'[(原|译|转)(\s+)]+', '', title, 1)
                title = re.sub(r'\s+$', '', title)

                # 获取阅读数
                read_num = i.find_all(class_ ='num')

                # 获取链接
                a = i.find('a')

                # 创建日期转成时间戳保存
                original = i.find(attrs={'class':'date'})
                original = original.text
                create_time = time.strptime(original, "%Y-%m-%d %H:%M:%S")
                create_time = time.strftime("%Y%m%d", create_time)
                links.append(a['href'])
                try:
                    handleData.write(page,{
                        'title': title,
                        'pagenum': pagenum,
                        'link': a['href'],
                        'create_time': create_time,
                        'last_spider_data':str(spider_date),
                        'spider_data': {
                            str(spider_date): {
                                'read_num': read_num[0].text,
                                'comment_num': read_num[1].text,
                                'last_update_time':str(spider_date)
                            }
                        }
                    })
                    print("写入成功："+title)
                except:
                    print("写入失败")
            index =index+1
        if (index > 0):
            findTitle(pagenum + 1)
        else:
            print("最后一页是：" + str(pagenum-1))
            return False
    except:
        print('失败了,删除ip' + ip)
        # 删除失效ip
        handleData.delete(emp,{'ip': ip})
        # 重新从数据库去除ip执行
        findTitle(pagenum)
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

    print('爬取完成')
    end = datetime.datetime.now()  # 结束时间
    diff = gettimediff(start, end)  # 计算耗时
    print('一共耗时: %s \n' % (diff))



if __name__ == '__main__':
    getip()